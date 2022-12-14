"""Pentair Intellicenter water heaters."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.water_heater import (
    SUPPORT_OPERATION_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    WaterHeaterEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, STATE_IDLE, STATE_OFF, STATE_ON
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import HomeAssistantType

from . import PoolEntity
from .const import DOMAIN
from .pyintellicenter import (
    BODY_ATTR,
    BODY_TYPE,
    HEATER_ATTR,
    HEATER_TYPE,
    HTMODE_ATTR,
    LISTORD_ATTR,
    LOTMP_ATTR,
    LSTTMP_ATTR,
    NULL_OBJNAM,
    STATUS_ATTR,
    ModelController,
    PoolObject,
)

# from homeassistant.components.climate.const import CURRENT_HVAC_OFF, CURRENT_HVAC_HEAT, CURRENT_HVAC_IDLE
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
):
    """Load pool sensors based on a config entry."""

    controller = hass.data[DOMAIN][entry.entry_id].controller

    # here we try to figure out which heater, if any, can be used for a given
    # body of water

    # first find all heaters
    # and sort them by their UI order (if they don't have one, use 100 and place them last)
    heaters = sorted(
        controller.model.getByType(HEATER_TYPE),
        key=lambda h: int(h[LISTORD_ATTR]) if h[LISTORD_ATTR] else 100,
    )

    bodies = controller.model.getByType(BODY_TYPE)

    water_heaters = []
    body: PoolObject
    for body in bodies:
        heater_list = []
        heater: PoolObject
        for heater in heaters:
            # if the heater supports this body, add it to the list
            if body.objnam in heater[BODY_ATTR].split(" "):
                heater_list.append(heater.objnam)
        if heater_list:
            water_heaters.append(PoolWaterHeater(entry, controller, body, heater_list))

    async_add_entities(water_heaters)


# -------------------------------------------------------------------------------------


class PoolWaterHeater(PoolEntity, WaterHeaterEntity, RestoreEntity):
    """Representation of a Pentair water heater."""

    LAST_HEATER_ATTR = "LAST_HEATER"

    def __init__(
        self,
        entry: ConfigEntry,
        controller: ModelController,
        poolObject: PoolObject,
        heater_list,
    ):
        """Initialize."""
        super().__init__(
            entry,
            controller,
            poolObject,
            extraStateAttributes=[HEATER_ATTR, HTMODE_ATTR],
        )
        self._heater_list = heater_list
        self._lastHeater = self._poolObject[HEATER_ATTR]
        self._attr_icon = "mdi:thermometer"

    @property
    def extra_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes of the entity."""

        state_attributes = super().extra_state_attributes

        if self._lastHeater != NULL_OBJNAM:
            state_attributes[self.LAST_HEATER_ATTR] = self._lastHeater

        return state_attributes

    @property
    def state(self) -> str:
        """Return the current state."""
        status = self._poolObject[STATUS_ATTR]
        heater = self._poolObject[HEATER_ATTR]
        if status == "OFF" or heater == NULL_OBJNAM:
            return STATE_OFF
        htmode = self._poolObject[HTMODE_ATTR]
        return STATE_ON if htmode != "0" else STATE_IDLE

    @property
    def unique_id(self):
        """Return a unique ID."""
        return super().unique_id + LOTMP_ATTR

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return self.pentairTemperatureSettings()

    @property
    def min_temp(self):
        """Return the minimum value."""
        return 5.0 if self._controller.systemInfo.usesMetric else 4.0

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 40.0 if self._controller.systemInfo.usesMetric else 104.0

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return float(self._poolObject[LSTTMP_ATTR])

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return float(self._poolObject[LOTMP_ATTR])

    def set_temperature(self, **kwargs):
        """Set new target temperatures."""
        target_temperature = kwargs.get(ATTR_TEMPERATURE)
        self.requestChanges({LOTMP_ATTR: str(int(target_temperature))})

    @property
    def current_operation(self):
        """Return current operation."""
        heater = self._poolObject[HEATER_ATTR]
        if heater in self._heater_list:
            return self._controller.model[heater].sname
        return STATE_OFF

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return [STATE_OFF] + [
            self._controller.model[heater].sname for heater in self._heater_list
        ]

    def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        if operation_mode == STATE_OFF:
            self._turnOff()
        else:
            for heater in self._heater_list:
                if operation_mode == self._controller.model[heater].sname:
                    self.requestChanges({HEATER_ATTR: heater})
                    break

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        heater = (
            self._lastHeater
            if self._lastHeater != NULL_OBJNAM
            else self._heater_list[0]
        )
        self.requestChanges({HEATER_ATTR: heater})

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        self._turnOff()

    def _turnOff(self):
        self.requestChanges({HEATER_ATTR: NULL_OBJNAM})

    def isUpdated(self, updates: Dict[str, Dict[str, str]]) -> bool:
        """Return true if the entity is updated by the updates from Intellicenter."""

        myUpdates = updates.get(self._poolObject.objnam, {})

        updated = (
            myUpdates
            and {STATUS_ATTR, HEATER_ATTR, HTMODE_ATTR, LOTMP_ATTR, LSTTMP_ATTR}
            & myUpdates.keys()
        )

        if updated and self._poolObject[HEATER_ATTR] != NULL_OBJNAM:
            self._lastHeater = self._poolObject[HEATER_ATTR]

        return updated

    async def async_added_to_hass(self):
        """Entity is added to Home Assistant."""

        await super().async_added_to_hass()

        if self._lastHeater == NULL_OBJNAM:
            # our current state is OFF so
            # let's see if we find a previous value stored in out state
            last_state = await self.async_get_last_state()

            if last_state:
                value = last_state.attributes.get(self.LAST_HEATER_ATTR)
                if value != NULL_OBJNAM:
                    self._lastHeater = value
