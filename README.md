# netbox-circuit-maintenance

A [NetBox](https://netbox.dev) plugin for tracking planned circuit maintenance windows.

## Features

- Track planned maintenance windows for circuits
- Associate maintenances with NetBox circuits and tenants
- Status lifecycle: Planned → Scheduled → In Progress → Completed / Cancelled
- Impact levels: Degraded, Interrupted, No Impact
- Full REST API support
- Search and filter by status, impact, circuit, and more
- Custom links and webhooks compatible

## Installation

```bash
pip install netbox-circuit-maintenance
```

Then add the plugin to your NetBox configuration (`/etc/netbox/configuration.py`):

```python
PLUGINS = [
    "netbox_circuit_maintenance",
]
```

Run database migrations:

```bash
cd /opt/netbox
python manage.py migrate
```

Restart NetBox services:

```bash
sudo systemctl restart netbox netbox-rq
```

## Configuration

This plugin has no required configuration. Optional settings can be added to `PLUGINS_CONFIG`:

```python
PLUGINS_CONFIG = {
    "netbox_circuit_maintenance": {
        # No configuration required for v0.1.0
    },
}
```

## Usage

### Creating a Maintenance

1. Navigate to **Plugins → Circuit Maintenances** in the NetBox sidebar
2. Click **Add** to create a new maintenance window
3. Fill in:
   - **Name**: Short identifier (e.g., "Q1 Fiber Upgrade")
   - **Circuit**: Select from existing NetBox circuits
   - **Status**: Planned, Scheduled, In Progress, Completed, or Cancelled
   - **Impact**: Degraded, Interrupted, or No Impact
   - **Start Time** / **End Time**: Maintenance window
   - **Ticket ID**: Internal tracking reference
   - **Provider Tracking ID**: Reference from the circuit provider
   - **Contact**: Person or team responsible
4. Click **Create**

### REST API

The plugin exposes a REST API at `/api/plugins/circuit-maintenance/maintenances/`.

```bash
# List all maintenances
curl -s http://netbox/api/plugins/circuit-maintenance/maintenances/ | jq

# Filter by status
curl -s "http://netbox/api/plugins/circuit-maintenance/maintenances/?status=planned" | jq

# Create a new maintenance
curl -s -X POST http://netbox/api/plugins/circuit-maintenance/maintenances/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "name": "Q1 Fiber Upgrade",
    "circuit": 1,
    "status": "planned",
    "impact": "degraded",
    "start_time": "2026-07-15T02:00:00Z",
    "end_time": "2026-07-15T06:00:00Z",
    "description": "Quarterly fiber upgrade maintenance window"
  }'
```

## Data Model

### CircuitMaintenance

| Field | Type | Description |
|-------|------|-------------|
| name | CharField(100) | Short identifier for the maintenance |
| circuit | ForeignKey(Circuit) | The affected NetBox circuit |
| status | CharField(30) | Planned, Scheduled, In Progress, Completed, Cancelled |
| impact | CharField(30) | Degraded, Interrupted, No Impact |
| start_time | DateTimeField | Planned start time |
| end_time | DateTimeField | Planned end time |
| description | TextField | Detailed description (optional) |
| ticket_id | CharField(50) | Internal ticket reference (optional) |
| provider_tracking_id | CharField(50) | Provider tracking reference (optional) |
| contact | CharField(100) | Contact person/team (optional) |
| notes | TextField | Additional notes (optional) |

## Development

```bash
# Clone the repo
git clone https://github.com/acrossthewire/netbox-circuit-maintenance.git
cd netbox-circuit-maintenance

# Install dev dependencies
pip install -e ".[dev]"

# Run linting
black --check .
isort --check-only .
flake8 .

# Run tests (requires a NetBox development environment)
pytest
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.