from django.urls import path

from netbox_circuit_maintenance import views

app_name = "netbox_circuit_maintenance"

urlpatterns = [
    path("circuit-maintenances/", views.CircuitMaintenanceListView.as_view(), name="circuitmaintenance_list"),
    path("circuit-maintenances/add/", views.CircuitMaintenanceEditView.as_view(), name="circuitmaintenance_add"),
    path("circuit-maintenances/<int:pk>/", views.CircuitMaintenanceView.as_view(), name="circuitmaintenance"),
    path(
        "circuit-maintenances/<int:pk>/edit/",
        views.CircuitMaintenanceEditView.as_view(),
        name="circuitmaintenance_edit",
    ),
    path(
        "circuit-maintenances/<int:pk>/delete/",
        views.CircuitMaintenanceDeleteView.as_view(),
        name="circuitmaintenance_delete",
    ),
    path(
        "circuit-maintenances/import/",
        views.CircuitMaintenanceBulkImportView.as_view(),
        name="circuitmaintenance_import",
    ),
    path(
        "circuit-maintenances/edit/",
        views.CircuitMaintenanceBulkEditView.as_view(),
        name="circuitmaintenance_bulk_edit",
    ),
    path(
        "circuit-maintenances/delete/",
        views.CircuitMaintenanceBulkDeleteView.as_view(),
        name="circuitmaintenance_bulk_delete",
    ),
]