from django.db import models


class MaintenanceStatusChoices(models.TextChoices):
    STATUS_PLANNED = "planned", "Planned"
    STATUS_SCHEDULED = "scheduled", "Scheduled"
    STATUS_IN_PROGRESS = "in_progress", "In Progress"
    STATUS_COMPLETED = "completed", "Completed"
    STATUS_CANCELLED = "cancelled", "Cancelled"


class MaintenanceImpactChoices(models.TextChoices):
    IMPACT_DEGRADED = "degraded", "Degraded"
    IMPACT_INTERRUPTED = "interrupted", "Interrupted"
    IMPACT_NO_IMPACT = "no_impact", "No Impact"