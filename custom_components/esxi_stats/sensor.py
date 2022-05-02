"""Sensor platform for esxi_stats."""
import logging
from string import capwords
from datetime import timedelta
from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
    DOMAIN_DATA,
    DEFAULT_NAME,
    DEFAULT_OPTIONS,
    MAP_TO_MEASUREMENT,
)

SCAN_INTERVAL = timedelta(seconds=15)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Set up sensor platform."""
    for cond in hass.data[DOMAIN_DATA]["monitored_conditions"]:
        for obj in hass.data[DOMAIN_DATA][cond]:
            async_add_entities([esxiSensor(hass, discovery_info, cond, obj)], True)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up sensor platform."""
    config = config_entry.data
    entry_id = config_entry.entry_id
    for cond in hass.data[DOMAIN_DATA][entry_id]["monitored_conditions"]:
        for obj in hass.data[DOMAIN_DATA][entry_id][cond]:
            async_add_devices([esxiSensor(hass, config, cond, obj, config_entry)], True)


class esxiSensor(Entity):
    """ESXi_stats Sensor class."""

    def __init__(self, hass, config, cond, obj, config_entry=None):
        """Init."""
        self.hass = hass
        self._attr = {}
        self._config_entry = config_entry
        self._entry_id = config_entry.entry_id
        self._state = None
        self.config = config
        # If configured via yaml, set options to defaults
        # This is likely a temporary fix because yaml config will likely be removed
        if config_entry is not None:
            self._options = self._config_entry.options
        else:
            self._options = DEFAULT_OPTIONS
        self._cond = cond
        self._obj = obj

    def update(self):
        """Update the sensor."""
        self.hass.data[DOMAIN_DATA][self._entry_id]["client"].update_data()
        self._data = self.hass.data[DOMAIN_DATA][self._entry_id][self._cond][self._obj]

        # Set state and measurement
        if self._options[self._cond] not in self._data.keys():
            self._state = "Error"
            self._measurement = ""
            _LOGGER.error(
                "State is set to incorrect key. Check Options in Integration UI"
            )
        else:
            self._state = self._data[self._options[self._cond]]
            self._measurement = measureFormat(self._options[self._cond])

        # Set attributes
        for key, value in self._data.items():
            self._attr[key] = value

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return "{}_{}_{}_{}".format(
            self.config["host"].replace(".", "_"), self._entry_id, self._cond, self._obj
        )

    @property
    def should_poll(self):
        """Return the name of the sensor."""
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {} {}".format(DEFAULT_NAME, self._cond, self._obj)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._measurement

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attr

    @property
    def device_info(self):
        """Return device info for this sensor."""
        if self._config_entry is None:
            indentifier = {(DOMAIN, self.config["host"].replace(".", "_"))}
        else:
            indentifier = {(DOMAIN, self._config_entry.entry_id)}
        return {
            "identifiers": indentifier,
            "name": "ESXi Stats",
            "manufacturer": "VMware, Inc.",
        }


def measureFormat(input):
    """Return measurement in readable form."""
    if input in MAP_TO_MEASUREMENT.keys():
        return MAP_TO_MEASUREMENT[input]
    else:
        return capwords(input.replace("_", " "))
