# Generated migration for CircuitMaintenance model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("circuits", "0001_initial"),  # NetBox circuits app must exist
    ]

    operations = [
        migrations.CreateModel(
            name="CircuitMaintenance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True),
                ),
                (
                    "name",
                    models.CharField(max_length=100),
                ),
                (
                    "status",
                    models.CharField(
                        default="planned",
                        max_length=30,
                    ),
                ),
                (
                    "impact",
                    models.CharField(
                        default="degraded",
                        max_length=30,
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(),
                ),
                (
                    "end_time",
                    models.DateTimeField(),
                ),
                (
                    "description",
                    models.TextField(blank=True),
                ),
                (
                    "ticket_id",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "provider_tracking_id",
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    "contact",
                    models.CharField(blank=True, max_length=100),
                ),
                (
                    "notes",
                    models.TextField(blank=True),
                ),
                (
                    "circuit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintenances",
                        to="circuits.circuit",
                    ),
                ),
            ],
            options={
                "verbose_name": "Circuit Maintenance",
                "verbose_name_plural": "Circuit Maintenances",
                "ordering": ["-start_time"],
            },
        ),
    ]