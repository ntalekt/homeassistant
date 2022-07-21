"""Adds config flow for NWS Alerts."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    API_ENDPOINT,
    CONF_INTERVAL,
    CONF_TIMEOUT,
    CONF_ZONE_ID,
    DEFAULT_INTERVAL,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
    USER_AGENT,
)

JSON_FEATURES = "features"
JSON_PROPERTIES = "properties"
JSON_ID = "id"

_LOGGER = logging.getLogger(__name__)


def _get_schema(hass: Any, user_input: list, default_dict: list) -> Any:
    """Gets a schema using the default_dict as a backup."""
    if user_input is None:
        user_input = {}

    def _get_default(key):
        """Gets default value for key."""
        return user_input.get(key, default_dict.get(key))

    return vol.Schema(
        {
            vol.Required(CONF_ZONE_ID, default=_get_default(CONF_ZONE_ID)): str,
            vol.Optional(CONF_NAME, default=_get_default(CONF_NAME)): str,
            vol.Optional(CONF_INTERVAL, default=_get_default(CONF_INTERVAL)): int,
            vol.Optional(CONF_TIMEOUT, default=_get_default(CONF_TIMEOUT)): int,
        }
    )


async def _get_zone_list(self) -> list | None:
    """Return list of zone by lat/lon"""

    data = None
    lat = self.hass.config.latitude
    lon = self.hass.config.longitude

    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}

    url = API_ENDPOINT + "/zones?point=%s,%s" % (lat, lon)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            _LOGGER.debug("getting zone list for %s,%s from %s" % (lat, lon, url))
            if r.status == 200:
                data = await r.json()

    zone_list = []
    if data is not None:
        if "features" in data:
            x = 0
            while len(data[JSON_FEATURES]) > x:
                zone_list.append(data[JSON_FEATURES][x][JSON_PROPERTIES][JSON_ID])
                x += 1
            _LOGGER.debug("Zones list: %s", zone_list)
            zone_list = ",".join(str(x) for x in zone_list) # convert list to str
            return zone_list
    return None


@config_entries.HANDLERS.register(DOMAIN)
class NWSAlertsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for NWS Alerts."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._data = {}
        self._errors = {}

    # async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
    #     """Import a config entry."""

    #     user_input = user_input[DOMAIN]
    #     result: FlowResult = await self.async_step_user(user_input=user_input)
    #     if errors := result.get("errors"):
    #         return self.async_abort(reason=next(iter(errors.values())))
    #     return result

    async def async_step_user(self, user_input={}):
        """Handle a flow initialized by the user."""
        self._errors = {}
        self._zone_list = await _get_zone_list(self)

        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title=self._data[CONF_NAME], data=self._data)
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""

        # Defaults
        defaults = {
            CONF_NAME: DEFAULT_NAME,
            CONF_INTERVAL: DEFAULT_INTERVAL,
            CONF_TIMEOUT: DEFAULT_TIMEOUT,
            CONF_ZONE_ID: self._zone_list,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=_get_schema(self.hass, user_input, defaults),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return NWSAlertsOptionsFlow(config_entry)


class NWSAlertsOptionsFlow(config_entries.OptionsFlow):
    """Options flow for NWS Alerts."""

    def __init__(self, config_entry):
        """Initialize."""
        self.config = config_entry
        self._data = dict(config_entry.options)
        self._errors = {}

    async def async_step_init(self, user_input=None):
        """Manage Mail and Packages options."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title="", data=self._data)
        return await self._show_options_form(user_input)

    async def _show_options_form(self, user_input):
        """Show the configuration form to edit location data."""

        return self.async_show_form(
            step_id="init",
            data_schema=_get_schema(self.hass, user_input, self._data),
            errors=self._errors,
        )
