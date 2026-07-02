"""View tests for netbox_circuit_maintenance."""

from django.test import TestCase
from django.urls import reverse

from circuits.models import Circuit, CircuitType, Provider
from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices
from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.tests import CircuitMaintenanceTestCase


class CircuitMaintenanceViewTest(CircuitMaintenanceTestCase):
    """Tests for CircuitMaintenance views."""

    def test_list_view(self):
        """Test the maintenance list view returns 200."""
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_with_data(self):
        """Test the list view shows created maintenances."""
        maintenance = self._create_maintenance()
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, maintenance.name)

    def test_detail_view(self):
        """Test the maintenance detail view returns 200."""
        maintenance = self._create_maintenance()
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance", kwargs={"pk": maintenance.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, maintenance.name)

    def test_create_view_get(self):
        """Test the create view returns 200 on GET."""
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_post(self):
        """Test creating a maintenance via POST."""
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_add")
        data = {
            "name": "New Maintenance",
            "circuit": self.circuit.pk,
            "status": MaintenanceStatusChoices.STATUS_PLANNED,
            "impact": MaintenanceImpactChoices.IMPACT_DEGRADED,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Created via POST",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            CircuitMaintenance.objects.filter(name="New Maintenance").exists()
        )

    def test_edit_view_get(self):
        """Test the edit view returns 200 on GET."""
        maintenance = self._create_maintenance()
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_edit", kwargs={"pk": maintenance.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_view_post(self):
        """Test updating a maintenance via POST."""
        maintenance = self._create_maintenance()
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_edit", kwargs={"pk": maintenance.pk})
        data = {
            "name": "Updated Maintenance",
            "circuit": self.circuit.pk,
            "status": MaintenanceStatusChoices.STATUS_SCHEDULED,
            "impact": MaintenanceImpactChoices.IMPACT_INTERRUPTED,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        maintenance.refresh_from_db()
        self.assertEqual(maintenance.name, "Updated Maintenance")
        self.assertEqual(maintenance.status, MaintenanceStatusChoices.STATUS_SCHEDULED)

    def test_delete_view_get(self):
        """Test the delete view returns 200 on GET."""
        maintenance = self._create_maintenance()
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_delete", kwargs={"pk": maintenance.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_post(self):
        """Test deleting a maintenance via POST."""
        maintenance = self._create_maintenance()
        pk = maintenance.pk
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_delete", kwargs={"pk": pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CircuitMaintenance.objects.filter(pk=pk).exists())

    def test_filter_by_status(self):
        """Test filtering maintenances by status."""
        planned = self._create_maintenance(name="Planned", status=MaintenanceStatusChoices.STATUS_PLANNED)
        completed = self._create_maintenance(name="Completed", status=MaintenanceStatusChoices.STATUS_COMPLETED)
        url = reverse("plugins:netbox_circuit_maintenance:circuitmaintenance_list")
        response = self.client.get(url + f"?status={MaintenanceStatusChoices.STATUS_PLANNED}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, planned.name)
        # Completed should not appear in filtered results