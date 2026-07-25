# Graph Report - .  (2026-07-23)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 268 nodes · 354 edges · 26 communities (19 shown, 7 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bbfdfe5a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CircuitMaintenanceModelTest
- CircuitMaintenance
- MaintenanceImpactChoices
- What You Must Do When Invoked
- CircuitMaintenanceViewTest
- CircuitMaintenanceAPITest
- MaintenanceStatusChoicesTest
- views.py
- netbox-circuit-maintenance
- Graphify
- graphify reference: extra exports and benchmark
- graphify reference: query, path, explain
- __init__.py
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify.js
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- AGENTS.md
- 0001_initial.py
- extraction-spec.md
- netbox-circuit-maintenance

## God Nodes (most connected - your core abstractions)
1. `CircuitMaintenance` - 47 edges
2. `CircuitMaintenanceModelTest` - 25 edges
3. `MaintenanceStatusChoices` - 19 edges
4. `MaintenanceImpactChoices` - 19 edges
5. `CircuitMaintenanceViewTest` - 16 edges
6. `CircuitMaintenanceAPITest` - 15 edges
7. `CircuitMaintenanceTestCase` - 14 edges
8. `CircuitMaintenanceTable` - 12 edges
9. `MaintenanceStatusChoicesTest` - 12 edges
10. `What You Must Do When Invoked` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Meta` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/api/serializers.py → netbox_circuit_maintenance/models.py
- `CircuitMaintenanceSerializer` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/api/serializers.py → netbox_circuit_maintenance/models.py
- `CircuitMaintenanceViewSet` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/api/views.py → netbox_circuit_maintenance/models.py
- `CircuitMaintenance` --uses--> `MaintenanceStatusChoices`  [INFERRED]
  netbox_circuit_maintenance/models.py → netbox_circuit_maintenance/choices.py
- `CircuitMaintenanceAPITest` --uses--> `MaintenanceStatusChoices`  [INFERRED]
  netbox_circuit_maintenance/tests/test_api.py → netbox_circuit_maintenance/choices.py

## Import Cycles
- None detected.

## Communities (26 total, 7 thin omitted)

### Community 0 - "CircuitMaintenanceModelTest"
Cohesion: 0.05
Nodes (21): CircuitMaintenanceModelTest, Test that Circuit has a 'maintenances' reverse relation., Test the human-readable status display., Test the human-readable impact display., Test that name field respects max_length., Tests for CircuitMaintenance model., Test that ticket_id field respects max_length., Test that provider_tracking_id field respects max_length. (+13 more)

### Community 1 - "CircuitMaintenance"
Cohesion: 0.12
Nodes (21): Meta, CircuitMaintenanceType, Meta, Query, CircuitMaintenance, A planned maintenance window affecting one or more circuits., CircuitMaintenanceIndex, CircuitMaintenanceTable (+13 more)

### Community 2 - "MaintenanceImpactChoices"
Cohesion: 0.16
Nodes (18): MaintenanceImpactChoices, MaintenanceStatusChoices, CircuitMaintenanceFilterForm, CircuitMaintenanceForm, Meta, Filter form for CircuitMaintenance list view., Form for creating/editing CircuitMaintenance objects., Meta (+10 more)

### Community 3 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 4 - "CircuitMaintenanceViewTest"
Cohesion: 0.09
Nodes (12): CircuitMaintenanceViewTest, Test filtering maintenances by status., Tests for CircuitMaintenance views., Test the maintenance list view returns 200., Test the list view shows created maintenances., Test the maintenance detail view returns 200., Test the create view returns 200 on GET., Test creating a maintenance via POST. (+4 more)

### Community 5 - "CircuitMaintenanceAPITest"
Cohesion: 0.10
Nodes (11): CircuitMaintenanceAPITest, Tests for CircuitMaintenance REST API., Test GET /api/plugins/circuit-maintenance/maintenances/., Test POST /api/plugins/circuit-maintenance/maintenances/., Test GET /api/plugins/circuit-maintenance/maintenances/{id}/., Test PATCH /api/plugins/circuit-maintenance/maintenances/{id}/., Test DELETE /api/plugins/circuit-maintenance/maintenances/{id}/., Test filtering API results by status. (+3 more)

### Community 6 - "MaintenanceStatusChoicesTest"
Cohesion: 0.12
Nodes (5): MaintenanceImpactChoicesTest, MaintenanceStatusChoicesTest, TestCase, Tests for MaintenanceImpactChoices., Tests for MaintenanceStatusChoices.

### Community 7 - "views.py"
Cohesion: 0.19
Nodes (10): CircuitMaintenanceSerializer, Meta, Serializer for CircuitMaintenance model., CircuitMaintenanceViewSet, API viewset for CircuitMaintenance model., CircuitMaintenanceFilterSet, FilterSet for CircuitMaintenance model., NetBoxModelFilterSet (+2 more)

### Community 8 - "netbox-circuit-maintenance"
Cohesion: 0.17
Nodes (11): CircuitMaintenance, Configuration, Creating a Maintenance, Data Model, Development, Features, Installation, License (+3 more)

### Community 9 - "Graphify"
Cohesion: 0.22
Nodes (8): Graphify, How the graph stays current, How to query the graph, How to refresh manually, Notes, Setup (already done — for reference), What is committed, What is NOT committed (gitignored)

### Community 10 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 11 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 12 - "__init__.py"
Cohesion: 0.40
Nodes (3): CircuitMaintenanceConfig, Version information for netbox-circuit-maintenance., PluginConfig

### Community 13 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 14 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 15 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **59 isolated node(s):** `Migration`, `netbox-circuit-maintenance`, `Usage`, `What graphify is for`, `Step 0 - GitHub repos and multi-path merge (only if a URL or several paths)` (+54 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CircuitMaintenance` connect `CircuitMaintenance` to `CircuitMaintenanceModelTest`, `MaintenanceImpactChoices`, `CircuitMaintenanceViewTest`, `CircuitMaintenanceAPITest`, `views.py`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `CircuitMaintenanceModelTest` connect `CircuitMaintenanceModelTest` to `CircuitMaintenance`, `MaintenanceImpactChoices`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Why does `CircuitMaintenanceViewTest` connect `CircuitMaintenanceViewTest` to `CircuitMaintenance`, `MaintenanceImpactChoices`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `CircuitMaintenance` (e.g. with `CircuitMaintenanceSerializer` and `Meta`) actually correct?**
  _`CircuitMaintenance` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `CircuitMaintenanceModelTest` (e.g. with `MaintenanceImpactChoices` and `MaintenanceStatusChoices`) actually correct?**
  _`CircuitMaintenanceModelTest` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MaintenanceStatusChoices` (e.g. with `CircuitMaintenanceFilterForm` and `CircuitMaintenanceForm`) actually correct?**
  _`MaintenanceStatusChoices` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MaintenanceImpactChoices` (e.g. with `CircuitMaintenanceFilterForm` and `CircuitMaintenanceForm`) actually correct?**
  _`MaintenanceImpactChoices` has 11 INFERRED edges - model-reasoned connections that need verification._