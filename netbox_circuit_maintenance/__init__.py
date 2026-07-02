from netbox.plugins import PluginConfig

from .version import __version__


class CircuitMaintenanceConfig(PluginConfig):
    name = "netbox_circuit_maintenance"
    verbose_name = "Circuit Maintenance"
    description = "Track planned circuit maintenance windows in NetBox"
    version = __version__
    base_url = "circuit-maintenance"
    min_version = "3.5.0"


config = CircuitMaintenanceConfig