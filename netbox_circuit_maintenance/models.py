from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from netbox.models.fields import CounterCacheField

from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices


class CircuitMaintenance(NetBoxModel):
    """A planned maintenance window affecting one or more circuits."""

    name = models.CharField(
        max_length=100,
        help_text="Short identifier for this maintenance window",
    )
    circuit = models.ForeignKey(
        to="circuits.Circuit",
        on_delete=models.CASCADE,
        related_name="maintenances",
        help_text="The circuit affected by this maintenance",
    )
    status = models.CharField(
        max_length=30,
        choices=MaintenanceStatusChoices,
        default=MaintenanceStatusChoices.STATUS_PLANNED,
        help_text="Current status of the maintenance window",
    )
    impact = models.CharField(
        max_length=30,
        choices=MaintenanceImpactChoices,
        default=MaintenanceImpactChoices.IMPACT_DEGRADED,
        help_text="Expected impact level during maintenance",
    )
    start_time = models.DateTimeField(
        help_text="Planned start time of the maintenance window",
    )
    end_time = models.DateTimeField(
        help_text="Planned end time of the maintenance window",
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the maintenance activity",
    )
    ticket_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="External ticket or reference number",
    )
    provider_tracking_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Tracking ID from the circuit provider",
    )
    contact = models.CharField(
        max_length=100,
        blank=True,
        help_text="Contact person or team for this maintenance",
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes",
    )

    class Meta:
        ordering = ["-start_time"]
        verbose_name = "Circuit Maintenance"
        verbose_name_plural = "Circuit Maintenances"

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse("plugins:netbox_circuit_maintenance:circuitmaintenance", pk=self.pk)