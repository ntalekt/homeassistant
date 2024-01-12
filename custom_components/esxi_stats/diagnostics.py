"""Diagnostics support for ESXi Stats."""
from typing import Any, Dict

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from .const import (
    DOMAIN_DATA,
)

REDACT_KEYS = {CONF_HOST, CONF_PASSWORD, CONF_USERNAME, "name"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> Dict[str, Any]:
    """Return diagnostics for a config entry."""

    entities = hass.data[DOMAIN_DATA]
    diag: dict[str, Any] = {}
    diag["config"] = config_entry.as_dict()

    for entity in entities.items():
        print(entity)
        diag["storage_data"] = entity

    return async_redact_data(diag, REDACT_KEYS)
