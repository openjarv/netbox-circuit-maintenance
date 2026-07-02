from netbox.api.viewsets import NetBoxModelViewSet
from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.filtersets import CircuitMaintenanceFilterSet
from .serializers import CircuitMaintenanceSerializer


class CircuitMaintenanceViewSet(NetBoxModelViewSet):
    """API viewset for CircuitMaintenance model."""

    queryset = CircuitMaintenance.objects.all()
    serializer_class = CircuitMaintenanceSerializer
    filterset_class = CircuitMaintenanceFilterSet