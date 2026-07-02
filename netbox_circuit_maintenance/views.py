from netbox.views import generic
from netbox_circuit_maintenance import forms, filtersets
from netbox_circuit_maintenance.models import CircuitMaintenance
from netbox_circuit_maintenance.tables import CircuitMaintenanceTable


class CircuitMaintenanceListView(generic.ObjectListView):
    queryset = CircuitMaintenance.objects.all()
    table = CircuitMaintenanceTable
    filterset = filtersets.CircuitMaintenanceFilterSet
    filterset_form = forms.CircuitMaintenanceFilterForm


class CircuitMaintenanceView(generic.ObjectView):
    queryset = CircuitMaintenance.objects.all()


class CircuitMaintenanceEditView(generic.ObjectEditView):
    queryset = CircuitMaintenance.objects.all()
    form = forms.CircuitMaintenanceForm


class CircuitMaintenanceDeleteView(generic.ObjectDeleteView):
    queryset = CircuitMaintenance.objects.all()


class CircuitMaintenanceBulkImportView(generic.BulkImportView):
    queryset = CircuitMaintenance.objects.all()
    model_form = forms.CircuitMaintenanceForm


class CircuitMaintenanceBulkEditView(generic.BulkEditView):
    queryset = CircuitMaintenance.objects.all()
    table = CircuitMaintenanceTable


class CircuitMaintenanceBulkDeleteView(generic.BulkDeleteView):
    queryset = CircuitMaintenance.objects.all()
    table = CircuitMaintenanceTable