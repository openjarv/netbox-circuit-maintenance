from django import forms

from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices


class CircuitMaintenanceForm(forms.ModelForm):
    """Form for creating/editing CircuitMaintenance objects."""

    class Meta:
        model = CircuitMaintenance
        fields = [
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
        ]


class CircuitMaintenanceFilterForm(forms.Form):
    """Filter form for CircuitMaintenance list view."""

    model = CircuitMaintenance

    q = forms.CharField(required=False, label="Search")
    status = forms.ChoiceField(
        required=False,
        choices=[("", "---------")] + MaintenanceStatusChoices.choices,
    )
    impact = forms.ChoiceField(
        required=False,
        choices=[("", "---------")] + MaintenanceImpactChoices.choices,
    )
    circuit_id = forms.IntegerField(required=False, label="Circuit ID")