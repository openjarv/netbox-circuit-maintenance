from netbox.search import SearchIndex, register_search
from netbox_circuit_maintenance.models import CircuitMaintenance


@register_search
class CircuitMaintenanceIndex(SearchIndex):
    model = CircuitMaintenance
    fields = (
        ("name", 100),
        ("description", 500),
        ("ticket_id", 200),
        ("provider_tracking_id", 200),
        ("contact", 300),
    )