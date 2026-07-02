import django_tables2 as tables
from netbox.tables import NetBoxTable
from netbox_circuit_maintenance.models import CircuitMaintenance


class CircuitMaintenanceTable(NetBoxTable):
    """Table configuration for CircuitMaintenance list view."""

    id = tables.LinkColumn()
    name = tables.LinkColumn()
    circuit = tables.LinkColumn()
    status = tables.Column()
    impact = tables.Column()
    start_time = tables.Column()
    end_time = tables.Column()
    ticket_id = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = CircuitMaintenance
        fields = (
            "id",
            "name",
            "circuit",
            "status",
            "impact",
            "start_time",
            "end_time",
            "ticket_id",
        )
        default_columns = (
            "name",
            "circuit",
            "status",
            "impact",
            "start_time",
            "end_time",
        )