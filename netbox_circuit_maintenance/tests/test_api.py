"""API tests for netbox_circuit_maintenance."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from circuits.models import Circuit, CircuitType, Provider
from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices
from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.tests import CircuitMaintenanceTestCase


class CircuitMaintenanceAPITest(CircuitMaintenanceTestCase):
    """Tests for CircuitMaintenance REST API."""

    def test_list_maintenances(self):
        """Test GET /api/plugins/circuit-maintenance/maintenances/."""
        url = "/api/plugins/circuit-maintenance/maintenances/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_maintenance(self):
        """Test POST /api/plugins/circuit-maintenance/maintenances/."""
        url = "/api/plugins/circuit-maintenance/maintenances/"
        data = {
            "name": "API Maintenance",
            "circuit": self.circuit.pk,
            "status": MaintenanceStatusChoices.STATUS_PLANNED,
            "impact": MaintenanceImpactChoices.IMPACT_DEGRADED,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "description": "Created via API",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CircuitMaintenance.objects.filter(name="API Maintenance").count(), 1)

    def test_retrieve_maintenance(self):
        """Test GET /api/plugins/circuit-maintenance/maintenances/{id}/."""
        maintenance = self._create_maintenance()
        url = f"/api/plugins/circuit-maintenance/maintenances/{maintenance.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], maintenance.name)

    def test_update_maintenance(self):
        """Test PATCH /api/plugins/circuit-maintenance/maintenances/{id}/."""
        maintenance = self._create_maintenance()
        url = f"/api/plugins/circuit-maintenance/maintenances/{maintenance.pk}/"
        data = {"status": MaintenanceStatusChoices.STATUS_IN_PROGRESS}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        maintenance.refresh_from_db()
        self.assertEqual(maintenance.status, MaintenanceStatusChoices.STATUS_IN_PROGRESS)

    def test_delete_maintenance(self):
        """Test DELETE /api/plugins/circuit-maintenance/maintenances/{id}/."""
        maintenance = self._create_maintenance()
        pk = maintenance.pk
        url = f"/api/plugins/circuit-maintenance/maintenances/{pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CircuitMaintenance.objects.filter(pk=pk).exists())

    def test_filter_by_status(self):
        """Test filtering API results by status."""
        planned = self._create_maintenance(name="Planned", status=MaintenanceStatusChoices.STATUS_PLANNED)
        completed = self._create_maintenance(name="Completed", status=MaintenanceStatusChoices.STATUS_COMPLETED)
        url = "/api/plugins/circuit-maintenance/maintenances/"
        response = self.client.get(url + f"?status={MaintenanceStatusChoices.STATUS_PLANNED}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item["name"] for item in response.data["results"]]
        self.assertIn("Planned", names)

    def test_filter_by_impact(self):
        """Test filtering API results by impact."""
        degraded = self._create_maintenance(name="Degraded", impact=MaintenanceImpactChoices.IMPACT_DEGRADED)
        interrupted = self._create_maintenance(name="Interrupted", impact=MaintenanceImpactChoices.IMPACT_INTERRUPTED)
        url = "/api/plugins/circuit-maintenance/maintenances/"
        response = self.client.get(url + f"?impact={MaintenanceImpactChoices.IMPACT_INTERRUPTED}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item["name"] for item in response.data["results"]]
        self.assertIn("Interrupted", names)

    def test_search(self):
        """Test the search filter."""
        maintenance = self._create_maintenance(
            name="Emergency Fix",
            description="Critical fiber cut repair",
            ticket_id="TKT-12345",
        )
        url = "/api/plugins/circuit-maintenance/maintenances/"
        response = self.client.get(url + "?q=TKT-12345")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item["name"] for item in response.data["results"]]
        self.assertIn("Emergency Fix", names)

    def test_required_fields_validation(self):
        """Test that required fields are enforced."""
        url = "/api/plugins/circuit-maintenance/maintenances/"
        data = {}  # Missing all required fields
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("circuit", response.data)
        self.assertIn("start_time", response.data)
        self.assertIn("end_time", response.data)