"""Choices tests for netbox_circuit_maintenance."""

from django.test import TestCase

from netbox_circuit_maintenance.choices import MaintenanceStatusChoices, MaintenanceImpactChoices


class MaintenanceStatusChoicesTest(TestCase):
    """Tests for MaintenanceStatusChoices."""

    def test_planned_exists(self):
        self.assertEqual(MaintenanceStatusChoices.STATUS_PLANNED, "planned")

    def test_scheduled_exists(self):
        self.assertEqual(MaintenanceStatusChoices.STATUS_SCHEDULED, "scheduled")

    def test_in_progress_exists(self):
        self.assertEqual(MaintenanceStatusChoices.STATUS_IN_PROGRESS, "in_progress")

    def test_completed_exists(self):
        self.assertEqual(MaintenanceStatusChoices.STATUS_COMPLETED, "completed")

    def test_cancelled_exists(self):
        self.assertEqual(MaintenanceStatusChoices.STATUS_CANCELLED, "cancelled")

    def test_choices_count(self):
        self.assertEqual(len(MaintenanceStatusChoices.choices), 5)

    def test_labels_are_human_readable(self):
        for value, label in MaintenanceStatusChoices.choices:
            self.assertNotEqual(value, label)
            self.assertTrue(label[0].isupper())


class MaintenanceImpactChoicesTest(TestCase):
    """Tests for MaintenanceImpactChoices."""

    def test_degraded_exists(self):
        self.assertEqual(MaintenanceImpactChoices.IMPACT_DEGRADED, "degraded")

    def test_interrupted_exists(self):
        self.assertEqual(MaintenanceImpactChoices.IMPACT_INTERRUPTED, "interrupted")

    def test_no_impact_exists(self):
        self.assertEqual(MaintenanceImpactChoices.IMPACT_NO_IMPACT, "no_impact")

    def test_choices_count(self):
        self.assertEqual(len(MaintenanceImpactChoices.choices), 3)

    def test_labels_are_human_readable(self):
        for value, label in MaintenanceImpactChoices.choices:
            self.assertNotEqual(value, label)