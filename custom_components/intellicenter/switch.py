"""Pentair Intellicenter switches."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from . import PoolEntity
from .const import DOMAIN
from .pyintellicenter import (
    BODY_TYPE,
    CHEM_TYPE,
    CIRCUIT_TYPE,
    HEATER_ATTR,
    HTMODE_ATTR,
    SUPER_ATTR,
    SYSTEM_TYPE,
    VACFLO_ATTR,
    VOL_ATTR,
    ModelController,
    PoolObject,
)

_LOGGER = logging.getLogger(__name__)

# FIXME: for freeze swtch use icon mdi:snowflake

# -------------------------------------------------------------------------------------


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
):
    """Load a Pentair switch based on a config entry."""
    controller: ModelController = hass.data[DOMAIN][entry.entry_id].controller

    switches = []

    object: PoolObject
    for object in controller.model.objectList:
        if object.objtype == BODY_TYPE:
            switches.append(PoolBody(entry, controller, object))
        elif (
            object.objtype == CHEM_TYPE
            and object.subtype == "ICHLOR"
            and SUPER_ATTR in object.attributes
        ):
            switches.append(
                PoolCircuit(
                    entry,
                    controller,
                    object,
                    attribute_key=SUPER_ATTR,
                    name="+ Superchlorinate",
                    icon="mdi:alpha-s-box-outline",
                )
            )
        elif (
            object.objtype == CIRCUIT_TYPE
            and not (object.isALight or object.isALightShow)
            and object.isFeatured
        ):
            switches.append(PoolCircuit(entry, controller, object))
        elif object.objtype == SYSTEM_TYPE:
            switches.append(
                PoolCircuit(
                    entry,
                    controller,
                    object,
                    VACFLO_ATTR,
                    name="Vacation mode",
                    enabled_by_default=False,
                )
            )

    async_add_entities(switches)


# -------------------------------------------------------------------------------------


class PoolCircuit(PoolEntity, SwitchEntity):
    """Representation of an standard pool circuit."""

    @property
    def is_on(self) -> bool:
        """Return the state of the circuit."""
        return self._poolObject[self._attribute_key] == self._poolObject.onStatus

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self.requestChanges({self._attribute_key: self._poolObject.offStatus})

    def turn_on(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self.requestChanges({self._attribute_key: self._poolObject.onStatus})


# -------------------------------------------------------------------------------------


class PoolBody(PoolCircuit):
    """Representation of a body of water."""

    def __init__(self, entry: ConfigEntry, controller, poolObject):
        """Initialize a Pool body from the underlying circuit."""
        super().__init__(entry, controller, poolObject)
        self._extra_state_attributes = [VOL_ATTR, HEATER_ATTR, HTMODE_ATTR]

    @property
    def icon(self):
        """Return the icon for the entity."""
        return "mdi:pool"
