from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_circuit_maintenance.models import CircuitMaintenance


class CircuitMaintenanceSerializer(NetBoxModelSerializer):
    """Serializer for CircuitMaintenance model."""

    class Meta:
        model = CircuitMaintenance
        fields = [
            "id",
            "name",
            "circuit",
            "status",
            "impact",
            "start_time",
            "end_time",
            "description",
            "ticket_id",
            "provider_tracking_id",
            "contact",
            "notes",
            "tags",
            "created",
            "last_updated",
        ]