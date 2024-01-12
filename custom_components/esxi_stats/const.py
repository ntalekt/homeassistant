"""Constants for ESXi Stats."""
DOMAIN = "esxi_stats"
DOMAIN_DATA = f"{DOMAIN}_data"

PLATFORMS = ["sensor"]
REQUIRED_FILES = [
    "const.py",
    "esxi.py",
    "manifest.json",
    "sensor.py",
    "config_flow.py",
    "services.yaml",
    "translations/en.json",
]
VERSION = "0.7.0"
ISSUE_URL = "https://github.com/wxt9861/esxi_stats/issues"

STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

CONF_NAME = "name"
CONF_DS_STATE = "datastore"
CONF_HOST_STATE = "vmhost"
CONF_LIC_STATE = "license"
CONF_VM_STATE = "vm"
CONF_NOTIFY = "notify"

# DEFAULT_NAME = "ESXi Stats"
DEFAULT_NAME = "ESXi"
DEFAULT_PORT = 443
DEFAULT_DS_STATE = "free_space_gb"
DEFAULT_HOST_STATE = "vms"
DEFAULT_LIC_STATE = "status"
DEFAULT_VM_STATE = "state"

# used to set default states for yaml config.
DEFAULT_OPTIONS = {
    "datastore": "free_space_gb",
    "vmhost": "vms",
    "license": "status",
    "vm": "state",
    "notify": "true",
}

DATASTORE_STATES = [
    "connected_hosts",
    "free_space_gb",
    "total_space_gb",
    "type",
    "virtual _machines",
]

LICENSE_STATES = ["expiration_days", "status"]

VMHOST_STATES = [
    "cpuusage_ghz",
    "memusage_gb",
    "state",
    "uptime_hours",
    "vms",
    "shutdown_supported",
]

VM_STATES = [
    "cpu_use_pct",
    "memory_used_mb",
    "snapshots",
    "status",
    "state",
    "uptime_hours",
    "used_space_gb",
]

MAP_TO_MEASUREMENT = {
    "cpu_count": "CPUs",
    "cpuusage_ghz": "CPU Use (GHz)",
    "expiration_days": "Expiration (D)",
    "free_space_gb": "Free (GB)",
    "memusage_gb": "Mem Use (GB)",
    "total_space_gb": "Total (GB)",
    "uptime_hours": "Uptime (H)",
    "virtual_machines": "VMs",
    "vms": "VMs",
}

SUPPORTED_PRODUCTS = ["VMware ESX Server", "VMware VirtualCenter Server"]
AVAILABLE_CMND_VM_POWER = ["on", "off", "reboot", "reset", "shutdown", "suspend"]
AVAILABLE_CMND_VM_SNAP = ["all", "first", "last"]
AVAILABLE_CMND_HOST_POWER = ["shutdown", "reboot"]
HOST = "host"
VM = "vm"
COMMAND = "command"
FORCE = "force"
