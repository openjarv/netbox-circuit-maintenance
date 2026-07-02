from django.db import models as db_models
import django_filters

from netbox.filtersets import NetBoxModelFilterSet
from netbox_circuit_maintenance.models import CircuitMaintenance


class CircuitMaintenanceFilterSet(NetBoxModelFilterSet):
    """FilterSet for CircuitMaintenance model."""

    class Meta:
        model = CircuitMaintenance
        fields = [
            "id",
            "name",
            "status",
            "impact",
            "circuit_id",
            "start_time",
            "end_time",
            "ticket_id",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            db_models.Q(name__icontains=value)
            | db_models.Q(description__icontains=value)
            | db_models.Q(ticket_id__icontains=value)
            | db_models.Q(provider_tracking_id__icontains=value)
            | db_models.Q(contact__icontains=value)
        )