"""
Component to show with breaking_changes.

For more details about this component, please refer to
https://github.com/custom-components/breaking_changes
"""
import logging
from datetime import timedelta

from awesomeversion import AwesomeVersion

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers import discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from integrationhelper import Throttle, WebClient
from pyhaversion import HaVersion, HaVersionSource

from .const import (
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    DEFAULT_NAME,
    DOMAIN,
    DOMAIN_DATA,
    INTERVAL,
    PLATFORMS,
    STARTUP,
    URL,
)

_LOGGER = logging.getLogger(__name__)

MINIMUM_VERSION = AwesomeVersion("2021.3")

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up this component."""

    # Print startup message
    _LOGGER.info(STARTUP)

    throttle = Throttle()

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}
    hass.data[DOMAIN_DATA]["throttle"] = throttle
    hass.data[DOMAIN_DATA]["integrations"] = ["homeassistant"]
    hass.data[DOMAIN_DATA]["potential"] = {
        "changes": [],
        "versions": set(),
        "covered": set(),
    }

    throttle.interval = timedelta(
        seconds=config[DOMAIN].get(CONF_SCAN_INTERVAL, INTERVAL)
    )

    # Load platforms
    for platform in PLATFORMS:
        # Get platform specific configuration
        platform_config = config[DOMAIN]

        hass.async_create_task(
            discovery.async_load_platform(
                hass, platform, DOMAIN, platform_config, config
            )
        )

    return True


async def update_data(hass):
    """Update data."""
    throttle = hass.data[DOMAIN_DATA]["throttle"]
    if throttle.throttle:
        return

    integrations = []
    changes = hass.data[DOMAIN_DATA]["potential"]["changes"]

    session = async_get_clientsession(hass)
    webclient = WebClient(session)
    localversion = HaVersion(session, source=HaVersionSource.LOCAL)
    pypiversion = HaVersion(session, source=HaVersionSource.PYPI)
    throttle.set_last_run()

    try:
        await localversion.get_version()
        currentversion = AwesomeVersion(localversion.version)

        await pypiversion.get_version()
        remoteversion = AwesomeVersion(pypiversion.version)
    except Exception:  # pylint: disable=broad-except
        _LOGGER.warning("Could not get version data.")
        return

    if currentversion >= remoteversion:
        _LOGGER.debug(
            "Current version is %s and remote version is %s skipping update",
            currentversion,
            remoteversion,
        )
        return

    for integration in hass.config.components or []:
        if "." in integration:
            integration = integration.split(".")[0]
        if integration not in integrations:
            integrations.append(integration)

    _LOGGER.debug("Loaded integrations - %s", integrations)

    c_split = [int(x) for x in currentversion.split(".")]
    r_split = [int(x) for x in remoteversion.split(".")]

    request_versions = []
    if c_split[0] < r_split[0]:
        for version in range(c_split[1] + 1, 13):
            request_versions.append(f"{c_split[0]}.{version}")
        for version in range(1, r_split[1] + 1):
            request_versions.append(f"{r_split[0]}.{version}")
    else:
        for version in range(c_split[1] + 1, r_split[1] + 1):
            request_versions.append(f"{r_split[0]}.{version}")

    request_versions = [x for x in request_versions if x >= MINIMUM_VERSION]
    if len(request_versions) == 0:
        _LOGGER.debug("no valid versions")
        return

    if hass.data[DOMAIN_DATA]["integrations"] != integrations:
        hass.data[DOMAIN_DATA]["potential"]["versions"] = set()
        changes = []
    hass.data[DOMAIN_DATA]["integrations"] = integrations

    for version in request_versions:
        if version in hass.data[DOMAIN_DATA]["potential"]["versions"]:
            _LOGGER.debug("Allready have information for %s", version)
            continue
        try:
            _LOGGER.debug("Checking breaking changes for %s", version)
            request = await webclient.async_get_json(URL.format(version))

            for change in request or []:
                if change["integration"] in integrations:
                    data = {
                        "title": change["title"],
                        "integration": change["integration"],
                        "description": change["description"],
                    }
                    changes.append(data)

            if version not in hass.data[DOMAIN_DATA]["potential"]["versions"]:
                hass.data[DOMAIN_DATA]["potential"]["versions"].add(version)

        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error("Could not update data - %s", error)

    hass.data[DOMAIN_DATA]["potential"]["changes"] = changes
