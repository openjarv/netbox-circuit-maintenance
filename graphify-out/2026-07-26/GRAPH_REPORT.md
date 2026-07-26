# Graph Report - .  (2026-07-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 194 nodes · 292 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4692ff3d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CircuitMaintenanceModelTest
- MaintenanceImpactChoices
- CircuitMaintenance
- CircuitMaintenanceViewTest
- CircuitMaintenanceAPITest
- MaintenanceStatusChoicesTest
- views.py
- netbox-circuit-maintenance
- __init__.py
- 0001_initial.py
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
10. `MaintenanceImpactChoicesTest` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Meta` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/api/serializers.py → netbox_circuit_maintenance/models.py
- `Meta` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/filtersets.py → netbox_circuit_maintenance/models.py
- `CircuitMaintenanceSerializer` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/api/serializers.py → netbox_circuit_maintenance/models.py
- `CircuitMaintenanceViewSet` --uses--> `CircuitMaintenance`  [INFERRED]
  netbox_circuit_maintenance/api/views.py → netbox_circuit_maintenance/models.py
- `CircuitMaintenance` --uses--> `MaintenanceStatusChoices`  [INFERRED]
  netbox_circuit_maintenance/models.py → netbox_circuit_maintenance/choices.py

## Import Cycles
- None detected.

## Communities (14 total, 2 thin omitted)

### Community 0 - "CircuitMaintenanceModelTest"
Cohesion: 0.05
Nodes (21): CircuitMaintenanceModelTest, Test that Circuit has a 'maintenances' reverse relation., Test the human-readable status display., Test the human-readable impact display., Test that name field respects max_length., Tests for CircuitMaintenance model., Test that ticket_id field respects max_length., Test that provider_tracking_id field respects max_length. (+13 more)

### Community 1 - "MaintenanceImpactChoices"
Cohesion: 0.16
Nodes (18): MaintenanceImpactChoices, MaintenanceStatusChoices, CircuitMaintenanceFilterForm, CircuitMaintenanceForm, Meta, Filter form for CircuitMaintenance list view., Form for creating/editing CircuitMaintenance objects., Meta (+10 more)

### Community 2 - "CircuitMaintenance"
Cohesion: 0.13
Nodes (20): CircuitMaintenanceType, Meta, Query, CircuitMaintenance, A planned maintenance window affecting one or more circuits., CircuitMaintenanceIndex, CircuitMaintenanceTable, Meta (+12 more)

### Community 3 - "CircuitMaintenanceViewTest"
Cohesion: 0.09
Nodes (12): CircuitMaintenanceViewTest, Test filtering maintenances by status., Tests for CircuitMaintenance views., Test the maintenance list view returns 200., Test the list view shows created maintenances., Test the maintenance detail view returns 200., Test the create view returns 200 on GET., Test creating a maintenance via POST. (+4 more)

### Community 4 - "CircuitMaintenanceAPITest"
Cohesion: 0.10
Nodes (11): CircuitMaintenanceAPITest, Tests for CircuitMaintenance REST API., Test GET /api/plugins/circuit-maintenance/maintenances/., Test POST /api/plugins/circuit-maintenance/maintenances/., Test GET /api/plugins/circuit-maintenance/maintenances/{id}/., Test PATCH /api/plugins/circuit-maintenance/maintenances/{id}/., Test DELETE /api/plugins/circuit-maintenance/maintenances/{id}/., Test filtering API results by status. (+3 more)

### Community 5 - "MaintenanceStatusChoicesTest"
Cohesion: 0.12
Nodes (5): MaintenanceImpactChoicesTest, MaintenanceStatusChoicesTest, TestCase, Tests for MaintenanceImpactChoices., Tests for MaintenanceStatusChoices.

### Community 6 - "views.py"
Cohesion: 0.17
Nodes (11): CircuitMaintenanceSerializer, Meta, Serializer for CircuitMaintenance model., CircuitMaintenanceViewSet, API viewset for CircuitMaintenance model., CircuitMaintenanceFilterSet, Meta, FilterSet for CircuitMaintenance model. (+3 more)

### Community 7 - "netbox-circuit-maintenance"
Cohesion: 0.17
Nodes (11): CircuitMaintenance, Configuration, Creating a Maintenance, Data Model, Development, Features, Installation, License (+3 more)

### Community 8 - "__init__.py"
Cohesion: 0.40
Nodes (3): CircuitMaintenanceConfig, Version information for netbox-circuit-maintenance., PluginConfig

## Knowledge Gaps
- **10 isolated node(s):** `Migration`, `netbox-circuit-maintenance`, `Features`, `Installation`, `Configuration` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CircuitMaintenance` connect `CircuitMaintenance` to `CircuitMaintenanceModelTest`, `MaintenanceImpactChoices`, `CircuitMaintenanceViewTest`, `CircuitMaintenanceAPITest`, `views.py`?**
  _High betweenness centrality (0.380) - this node is a cross-community bridge._
- **Why does `CircuitMaintenanceModelTest` connect `CircuitMaintenanceModelTest` to `MaintenanceImpactChoices`, `CircuitMaintenance`?**
  _High betweenness centrality (0.290) - this node is a cross-community bridge._
- **Why does `CircuitMaintenanceViewTest` connect `CircuitMaintenanceViewTest` to `MaintenanceImpactChoices`, `CircuitMaintenance`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `CircuitMaintenance` (e.g. with `CircuitMaintenanceSerializer` and `Meta`) actually correct?**
  _`CircuitMaintenance` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `CircuitMaintenanceModelTest` (e.g. with `MaintenanceImpactChoices` and `MaintenanceStatusChoices`) actually correct?**
  _`CircuitMaintenanceModelTest` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MaintenanceStatusChoices` (e.g. with `CircuitMaintenanceFilterForm` and `CircuitMaintenanceForm`) actually correct?**
  _`MaintenanceStatusChoices` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MaintenanceImpactChoices` (e.g. with `CircuitMaintenanceFilterForm` and `CircuitMaintenanceForm`) actually correct?**
  _`MaintenanceImpactChoices` has 11 INFERRED edges - model-reasoned connections that need verification._