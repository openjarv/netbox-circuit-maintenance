from django.utils.translation import gettext_lazy as _

from netbox.plugins import PluginMenuItem

menu_items = [
    PluginMenuItem(
        link="plugins:netbox_circuit_maintenance:circuitmaintenance_list",
        link_text="Circuit Maintenances",
        permissions=["netbox_circuit_maintenance.view_circuitmaintenance"],
    ),
]