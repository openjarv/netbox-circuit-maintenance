"""Test utilities for netbox_circuit_maintenance."""

from django.test import TestCase
from django.utils import timezone

from circuits.models import Circuit, CircuitType, Provider
from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices


class CircuitMaintenanceTestCase(TestCase):
    """Base test case with helper methods for CircuitMaintenance tests."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data used across test methods."""
        cls.provider = Provider.objects.create(
            name="Test Provider",
            slug="test-provider",
        )
        cls.circuit_type = CircuitType.objects.create(
            name="Test Circuit Type",
            slug="test-circuit-type",
        )
        cls.circuit = Circuit.objects.create(
            cid="TEST-001",
            provider=cls.provider,
            type=cls.circuit_type,
        )
        cls.start_time = timezone.now()
        cls.end_time = cls.start_time + timezone.timedelta(hours=4)

    def _create_maintenance(self, **kwargs):
        """Helper to create a CircuitMaintenance with sensible defaults."""
        defaults = {
            "name": "Scheduled Maintenance",
            "circuit": self.circuit,
            "status": MaintenanceStatusChoices.STATUS_PLANNED,
            "impact": MaintenanceImpactChoices.IMPACT_DEGRADED,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": "Test maintenance window",
        }
        defaults.update(kwargs)
        return CircuitMaintenance.objects.create(**defaults)