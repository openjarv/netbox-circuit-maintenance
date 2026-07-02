from netbox.graphql.types import NetBoxObjectType
from netbox_circuit_maintenance.models import CircuitMaintenance


class CircuitMaintenanceType(NetBoxObjectType):
    class Meta:
        model = CircuitMaintenance
        fields = "__all__"


class Query:
    pass