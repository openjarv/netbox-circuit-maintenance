#!/usr/bin/env bash
# dev-worktree.sh — manage per-issue git worktrees for netbox-circuit-maintenance.
#
# Ported from netbox-pyats/scripts/dev-worktree.sh (ATW-259). This repo has no
# dev compose stack, so `up`/`cleanup`/`audit` are worktree-only (no Docker).
# The command surface mirrors the netbox-pyats helper so the daily worktree-
# audit routine can call `scripts/dev-worktree.sh remove <issue-id>` from
# either trunk uniformly.
#
# Conventions:
#   - Trunk worktree at /home/hermes/netbox-circuit-maintenance stays on main;
#     no feature work happens there. Each issue gets its own worktree under
#     ../netbox-circuit-maintenance-wt/.
#   - One issue = one branch = one worktree. Branch name: <type>/<issue-id>-<slug>.
#
# Commands:
#   dev-worktree.sh add <issue-id> <type> <slug>
#       Create ../netbox-circuit-maintenance-wt/<issue-id> on branch
#       <type>/<issue-id>-<slug> based on the latest origin/main (fetch first;
#       offline fallback to local main), and print path + base SHA. Refuses to
#       run when the trunk worktree is not on main (or a branch tracking
#       origin/main) so worktrees never branch from a stale feature branch.
#       (ATW-208, ported in ATW-259)
#
#   dev-worktree.sh up
#       No-op for this repo (no dev compose stack). Prints guidance for running
#       the plugin's tests directly. Kept for command-surface parity with the
#       netbox-pyats helper so agents can call it uniformly.
#
#   dev-worktree.sh remove <issue-id>
#       `git worktree remove` the worktree. Use when the issue reaches a
#       terminal state (done/cancelled). No compose stack to tear down.
#
#   dev-worktree.sh cleanup
#       Find and remove orphaned worktree directories whose git worktree link is
#       gone (stale left-behind dirs). Safe to run on a schedule.
#
#   dev-worktree.sh audit
#       Print a worktree-inventory report: git worktree list, orphaned /tmp
#       worktree dirs, and any leftover branch refs. Post the output back to
#       the originating issue.
#
# Base branch policy (ATW-208, ported in ATW-259): every new worktree branch is
# based on the latest origin/main, unless a documented reason on the
# originating issue names an alternate base. The script fetches origin/main
# before branching, bases on origin/main (falling back to local main only
# when offline and local main exists), refreshes local main from origin/main
# when present, refuses to add when the trunk is off main, and prints the
# base SHA used.

set -euo pipefail

# Resolve the trunk repo root (the worktree this script lives alongside, or the
# common dir for linked worktrees). We anchor everything to the trunk so the
# script works no matter which worktree it is invoked from.
TRUNK="$(git rev-parse --git-common-dir 2>/dev/null)"
if [ -z "$TRUNK" ]; then
  echo "error: not inside a git repo" >&2
  exit 1
fi
# git-common-dir is relative to cwd for main worktree, absolute for linked ones.
case "$TRUNK" in
  /*) TRUNK="$(cd "$TRUNK" && pwd)" ;;
  *)  TRUNK="$(cd "$(pwd)/$TRUNK" && pwd)" ;;
esac
# The trunk working tree is the parent of the .git dir for the main worktree.
TRUNK_ROOT="$(dirname "$TRUNK")"
# Worktrees live in a sibling directory of the trunk repo (not nested inside
# it), so e.g. /home/hermes/netbox-circuit-maintenance
#  -> /home/hermes/netbox-circuit-maintenance-wt.
WT_ROOT="$(dirname "$TRUNK_ROOT")/$(basename "$TRUNK_ROOT")-wt"

die() { echo "error: $*" >&2; exit 1; }

usage() {
  cat >&2 <<EOF
usage: dev-worktree.sh <command> [args]

  add <issue-id> <type> <slug>     create a worktree for an issue
  up                               no-op for this repo (no compose stack)
  remove <issue-id>                remove the worktree
  cleanup                          remove orphaned worktree dirs (ATW-259)
  audit                            print worktree-inventory report (ATW-259)

examples:
  dev-worktree.sh add atw-44 chore worktree-helper
  dev-worktree.sh up
  dev-worktree.sh remove atw-44
  dev-worktree.sh cleanup
  dev-worktree.sh audit
EOF
  exit 2
}

cmd_add() {
  local issue_id="${1:-}" type="${2:-}" slug="${3:-}"
  [ -n "$issue_id" ] && [ -n "$type" ] && [ -n "$slug" ] || usage

  # Accept both short (feat) and long (feature) forms; normalise to short.
  case "$type" in
    feat|feature)   type=feat ;;
    fix)            type=fix ;;
    chore)          type=chore ;;
    docs)           type=docs ;;
    infra)          type=infra ;;
    refactor)       type=refactor ;;
    test)           type=test ;;
    *) die "type must be one of: feat fix chore docs infra refactor test (got '$type')" ;;
  esac

  local branch="$type/$issue_id-$slug"
  local wt="$WT_ROOT/$issue_id"

  [ -e "$wt" ] && die "worktree already exists: $wt"

  # Ensure the worktree directory exists.
  mkdir -p "$WT_ROOT"

  # Refuse to clobber an existing branch.
  if git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null; then
    die "branch already exists: $branch (delete it or pick a new slug)"
  fi

  # --- Base branch policy (ATW-208, ported in ATW-259) ---------------------
  # Every new worktree branches from the latest origin/main. We:
  #   1. Refuse to add when the trunk working tree is not on main (or a
  #      branch tracking origin/main), so worktrees never silently branch
  #      from a stale feature branch.
  #   2. Fetch origin/main (non-fatal on network failure with a warning).
  #   3. Refresh local main from origin/main when present, or create it
  #      from origin/main when missing, so the trunk worktree can return
  #      to it.
  #   4. Base the new branch on origin/main; fall back to local main only
  #      when offline and local main exists. Never fall back to the current
  #      HEAD or another feature branch.
  #   5. Print the base SHA used so the worktree's origin is auditable.

  local trunk_branch
  trunk_branch="$(git -C "$TRUNK_ROOT" branch --show-current 2>/dev/null || true)"

  # A branch is an acceptable trunk base iff it is `main` or tracks
  # origin/main. Anything else (a feature branch, detached HEAD) is refused.
  local trunk_tracks_main=0
  if [ "$trunk_branch" = "main" ]; then
    trunk_tracks_main=1
  elif [ -n "$trunk_branch" ]; then
    local upstream
    upstream="$(git -C "$TRUNK_ROOT" rev-parse --abbrev-ref --symbolic-full-name "$trunk_branch@{upstream}" 2>/dev/null || true)"
    if [ "$upstream" = "refs/remotes/origin/main" ]; then
      trunk_tracks_main=1
    fi
  fi

  if [ "$trunk_tracks_main" -ne 1 ]; then
    cat >&2 <<EOF
error: trunk worktree is not on main (or a branch tracking origin/main).
  trunk branch: ${trunk_branch:-<detached HEAD>}
  trunk root:   $TRUNK_ROOT

Worktrees must branch from the latest origin/main, not from the current
checkout. Restore the trunk to main first:

  git -C "$TRUNK_ROOT" fetch origin main
  git -C "$TRUNK_ROOT" branch -f main origin/main
  git -C "$TRUNK_ROOT" checkout main

Then re-run: $0 add $issue_id $type $slug

If you genuinely need to base this work on a different branch, record the
alternate base and the reason on the originating issue, then run git
worktree add by hand.
EOF
    exit 1
  fi

  # Fetch origin/main so the base is current. Non-fatal on network failure:
  # we fall back to local main below. (ATW-208)
  local online=1
  if ! git -C "$TRUNK_ROOT" fetch --quiet origin main 2>/dev/null; then
    online=0
    echo "warning: 'git fetch origin main' failed — continuing offline from local main if present" >&2
  fi

  # Resolve the base SHA. Prefer origin/main; fall back to local main only
  # when offline and local main exists. Never fall back to HEAD.
  local base_ref="" base_sha=""
  if [ "$online" -eq 1 ] && git -C "$TRUNK_ROOT" rev-parse --verify --quiet origin/main >/dev/null 2>&1; then
    base_ref="origin/main"
    base_sha="$(git -C "$TRUNK_ROOT" rev-parse origin/main)"
  elif git -C "$TRUNK_ROOT" rev-parse --verify --quiet main >/dev/null 2>&1; then
    if [ "$online" -eq 1 ]; then
      base_ref="origin/main"
      base_sha="$(git -C "$TRUNK_ROOT" rev-parse origin/main)"
    else
      base_ref="main (offline — may be stale; fetch when network returns)"
      base_sha="$(git -C "$TRUNK_ROOT" rev-parse main)"
    fi
  else
    die "no origin/main and no local main to base on. Run: git -C \"$TRUNK_ROOT\" fetch origin main && git -C \"$TRUNK_ROOT\" branch -f main origin/main"
  fi

  # Refresh / create local main from origin/main so the trunk worktree can
  # return to it. Only when online and origin/main moved ahead of local main
  # (or local main is missing). (ATW-208)
  if [ "$online" -eq 1 ]; then
    if ! git -C "$TRUNK_ROOT" rev-parse --verify --quiet main >/dev/null 2>&1; then
      echo "local main missing — creating from origin/main" >&2
      git -C "$TRUNK_ROOT" branch main origin/main
    else
      local local_main_sha
      local_main_sha="$(git -C "$TRUNK_ROOT" rev-parse main)"
      if [ "$local_main_sha" != "$base_sha" ]; then
        # Fast-forward local main to origin/main. Use -f only as a safety net;
        # origin/main is an ancestor-fast-forward of main in normal flow, but
        # if local main diverged we refuse rather than rewrite history.
        if git -C "$TRUNK_ROOT" merge-base --is-ancestor "$local_main_sha" "$base_sha"; then
          git -C "$TRUNK_ROOT" branch -f main "$base_sha" >/dev/null 2>&1 || true
        else
          echo "warning: local main ($local_main_sha) has diverged from origin/main ($base_sha) — not rewriting local main. Trunk checkout unchanged." >&2
        fi
      fi
    fi
  fi

  # Create the worktree branched from the resolved base. Use origin/main
  # directly when online so the new branch starts at the fetched tip; use
  # local main only when offline.
  local create_from="$base_sha"
  if [ "$online" -eq 1 ]; then
    create_from="origin/main"
  fi
  git -C "$TRUNK_ROOT" worktree add "$wt" -b "$branch" "$create_from"
  base_sha="$(git -C "$wt" rev-parse HEAD)"

  cat <<EOF
created worktree: $wt
branch:          $branch
base:            $base_ref
base SHA:        $base_sha

Next:
  cd $wt
  # this repo has no dev compose stack — run tests directly:
  pytest netbox_circuit_maintenance
EOF
}

cmd_up() {
  # This repo has no docker-compose.dev.yml. Kept for command-surface parity
  # with the netbox-pyats helper so agents can call `scripts/dev-worktree.sh up`
  # uniformly. Prints guidance instead of starting a stack.
  cat <<EOF
netbox-circuit-maintenance has no dev compose stack.

Run the plugin's tests directly from this worktree:

  pytest netbox_circuit_maintenance

(See pyproject.toml [project.optional-dependencies] dev for the test deps.)
EOF
}

cmd_remove() {
  local issue_id="${1:-}"
  [ -n "$issue_id" ] || usage
  local wt="$WT_ROOT/$issue_id"

  [ -d "$wt" ] || die "no worktree for $issue_id at $wt"

  # No compose stack to tear down — just remove the git worktree.
  git -C "$TRUNK_ROOT" worktree remove --force "$wt"

  # Clean up the worktree directory if git left it behind.
  rmdir "$wt" 2>/dev/null || true

  echo "removed worktree: $wt"
  echo "note: matching branches (<type>/$issue_id-*) were not auto-deleted; remove with:"
  echo "  git -C \"$TRUNK_ROOT\" branch -D <branch>"
}

cmd_cleanup() {
  # Find and remove orphaned worktree directories whose git worktree link is
  # gone (stale left-behind dirs). Safe to run on a schedule. (ATW-259)
  echo "=== dev-worktree cleanup: scanning for orphaned worktree dirs ==="

  local git_wts
  git_wts="$(git -C "$TRUNK_ROOT" worktree list --porcelain 2>/dev/null \
    | awk '/^worktree /{print $2}' || true)"

  if [ ! -d "$WT_ROOT" ]; then
    echo "no worktree root ($WT_ROOT) — nothing to clean."
    return 0
  fi

  local cleaned=0
  for d in "$WT_ROOT"/*/; do
    [ -d "$d" ] || continue
    local dir="${d%/}"
    if ! printf '%s\n' "$git_wts" | grep -qxF "$dir"; then
      echo "  $dir: not a registered git worktree — removing stale dir"
      rm -rf "$dir"
      cleaned=$((cleaned + 1))
    fi
  done

  if [ "$cleaned" -eq 0 ]; then
    echo "no orphaned worktree dirs found — nothing to clean."
  else
    echo
    echo "cleanup complete: $cleaned stale worktree dir(s) removed."
  fi
}

cmd_audit() {
  # Print a worktree-inventory report. Post the output back to the originating
  # issue. (ATW-259)
  echo "=== dev-worktree audit: $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo

  echo "--- worktree inventory ---"
  git -C "$TRUNK_ROOT" worktree list 2>/dev/null | sed 's/^/  /' || echo "  (no worktrees)"
  echo

  echo "--- branches ---"
  git -C "$TRUNK_ROOT" branch --list 2>/dev/null | sed 's/^/  /' || echo "  (none)"
  echo

  echo "--- orphaned worktree dirs (no matching git worktree) ---"
  local git_wts
  git_wts="$(git -C "$TRUNK_ROOT" worktree list --porcelain 2>/dev/null \
    | awk '/^worktree /{print $2}' || true)"
  local found_orphan=0
  if [ -d "$WT_ROOT" ]; then
    for d in "$WT_ROOT"/*/; do
      [ -d "$d" ] || continue
      local dir="${d%/}"
      if ! printf '%s\n' "$git_wts" | grep -qxF "$dir"; then
        echo "  $dir"
        found_orphan=1
      fi
    done
  fi
  if [ "$found_orphan" -eq 0 ]; then
    echo "  (none)"
  fi
}

[ $# -ge 1 ] || usage
sub="$1"; shift
case "$sub" in
  add)     cmd_add "$@" ;;
  up)      cmd_up "$@" ;;
  remove)  cmd_remove "$@" ;;
  cleanup) cmd_cleanup "$@" ;;
  audit)   cmd_audit "$@" ;;
  -h|--help|help) usage ;;
  *)       usage ;;
esac