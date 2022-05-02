"""Constants for breaking_changes."""
# Base component constants
DOMAIN = "breaking_changes"
DOMAIN_DATA = "{}_data".format(DOMAIN)
INTEGRATION_VERSION = "21.12.0"
PLATFORMS = ["sensor"]
ISSUE_URL = "https://github.com/custom-components/breaking_changes/issues"

STARTUP = f"""
-------------------------------------------------------------------
{DOMAIN}
Version: {INTEGRATION_VERSION}
This is a custom component
If you have any issues with this you need to open an issue here:
https://github.com/custom-components/breaking_changes/issues
-------------------------------------------------------------------
"""

# Operational
URL = "https://hachanges.entrypoint.xyz/v1/{0}"

# Icons
ICON = "mdi:package-up"

# Configuration
CONF_NAME = "name"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_NAME = "Potential breaking changes"

# Interval in seconds
INTERVAL = 300
