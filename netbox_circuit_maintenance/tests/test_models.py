"""Model tests for netbox_circuit_maintenance."""

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices
from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.tests import CircuitMaintenanceTestCase


class CircuitMaintenanceModelTest(CircuitMaintenanceTestCase):
    """Tests for CircuitMaintenance model."""

    def test_create_maintenance(self):
        """Test creating a CircuitMaintenance record."""
        maintenance = self._create_maintenance()
        self.assertIsNotNone(maintenance.pk)
        self.assertEqual(maintenance.name, "Scheduled Maintenance")
        self.assertEqual(maintenance.circuit, self.circuit)
        self.assertEqual(maintenance.status, MaintenanceStatusChoices.STATUS_PLANNED)
        self.assertEqual(maintenance.impact, MaintenanceImpactChoices.IMPACT_DEGRADED)

    def test_str_representation(self):
        """Test the string representation includes name and status."""
        maintenance = self._create_maintenance(name="Weekend Window")
        self.assertEqual(str(maintenance), "Weekend Window (Planned)")

    def test_default_status_is_planned(self):
        """Test that the default status is 'planned'."""
        maintenance = CircuitMaintenance(
            name="Auto Status",
            circuit=self.circuit,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        self.assertEqual(maintenance.status, MaintenanceStatusChoices.STATUS_PLANNED)

    def test_default_impact_is_degraded(self):
        """Test that the default impact is 'degraded'."""
        maintenance = CircuitMaintenance(
            name="Auto Impact",
            circuit=self.circuit,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        self.assertEqual(maintenance.impact, MaintenanceImpactChoices.IMPACT_DEGRADED)

    def test_all_status_choices(self):
        """Test that all status choices can be set."""
        for status_val, status_label in MaintenanceStatusChoices.choices:
            maintenance = self._create_maintenance(status=status_val)
            maintenance.refresh_from_db()
            self.assertEqual(maintenance.status, status_val)

    def test_all_impact_choices(self):
        """Test that all impact choices can be set."""
        for impact_val, impact_label in MaintenanceImpactChoices.choices:
            maintenance = self._create_maintenance(impact=impact_val)
            maintenance.refresh_from_db()
            self.assertEqual(maintenance.impact, impact_val)

    def test_optional_fields_blank(self):
        """Test that optional fields can be left blank."""
        maintenance = self._create_maintenance(
            description="",
            ticket_id="",
            provider_tracking_id="",
            contact="",
            notes="",
        )
        maintenance.refresh_from_db()
        self.assertEqual(maintenance.description, "")
        self.assertEqual(maintenance.ticket_id, "")
        self.assertEqual(maintenance.provider_tracking_id, "")
        self.assertEqual(maintenance.contact, "")
        self.assertEqual(maintenance.notes, "")

    def test_circuit_foreign_key(self):
        """Test that maintenance links to a circuit."""
        maintenance = self._create_maintenance()
        self.assertEqual(maintenance.circuit, self.circuit)
        self.assertEqual(maintenance.circuit.cid, "TEST-001")

    def test_circuit_cascade_delete(self):
        """Test that deleting a circuit cascades to its maintenances."""
        maintenance = self._create_maintenance()
        maintenance_pk = maintenance.pk
        self.circuit.delete()
        with self.assertRaises(CircuitMaintenance.DoesNotExist):
            CircuitMaintenance.objects.get(pk=maintenance_pk)

    def test_ordering_by_start_time_desc(self):
        """Test that maintenances are ordered by start_time descending."""
        early = self._create_maintenance(
            name="Early",
            start_time=self.start_time,
            end_time=self.end_time,
        )
        later = self._create_maintenance(
            name="Later",
            start_time=self.start_time + timezone.timedelta(days=1),
            end_time=self.end_time + timezone.timedelta(days=1),
        )
        qs = CircuitMaintenance.objects.all()
        self.assertEqual(qs[0], later)
        self.assertEqual(qs[1], early)

    def test_related_name_maintenances(self):
        """Test that Circuit has a 'maintenances' reverse relation."""
        maintenance = self._create_maintenance()
        self.assertIn(maintenance, self.circuit.maintenances.all())

    def test_get_status_display(self):
        """Test the human-readable status display."""
        maintenance = self._create_maintenance(status=MaintenanceStatusChoices.STATUS_IN_PROGRESS)
        self.assertEqual(maintenance.get_status_display(), "In Progress")

    def test_get_impact_display(self):
        """Test the human-readable impact display."""
        maintenance = self._create_maintenance(impact=MaintenanceImpactChoices.IMPACT_INTERRUPTED)
        self.assertEqual(maintenance.get_impact_display(), "Interrupted")

    def test_name_max_length(self):
        """Test that name field respects max_length."""
        # Should succeed at max length
        maintenance = self._create_maintenance(name="A" * 100)
        self.assertEqual(len(maintenance.name), 100)

    def test_ticket_id_max_length(self):
        """Test that ticket_id field respects max_length."""
        maintenance = self._create_maintenance(ticket_id="T" * 50)
        self.assertEqual(len(maintenance.ticket_id), 50)

    def test_provider_tracking_id_max_length(self):
        """Test that provider_tracking_id field respects max_length."""
        maintenance = self._create_maintenance(provider_tracking_id="P" * 50)
        self.assertEqual(len(maintenance.provider_tracking_id), 50)

    def test_contact_max_length(self):
        """Test that contact field respects max_length."""
        maintenance = self._create_maintenance(contact="C" * 100)
        self.assertEqual(len(maintenance.contact), 100)

    def test_verbose_name(self):
        """Test model verbose name."""
        self.assertEqual(
            CircuitMaintenance._meta.verbose_name,
            "Circuit Maintenance",
        )

    def test_verbose_name_plural(self):
        """Test model verbose name plural."""
        self.assertEqual(
            CircuitMaintenance._meta.verbose_name_plural,
            "Circuit Maintenances",
        )