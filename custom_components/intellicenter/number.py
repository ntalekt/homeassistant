"""Pentair Intellicenter numbers."""

import logging
from typing import Optional

from homeassistant.components.number import (
    NumberEntity,
    DEFAULT_MIN_VALUE,
    DEFAULT_MAX_VALUE,
    DEFAULT_STEP,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from . import PoolEntity
from .const import CONST_RPM, DOMAIN
from homeassistant.const import PERCENTAGE
from .pyintellicenter import (
    CHEM_TYPE,
    PRIM_ATTR,
    ModelController,
    PoolObject,
)

_LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
):
    """Load pool numbers based on a config entry."""

    controller: ModelController = hass.data[DOMAIN][entry.entry_id].controller

    numbers = []

    object: PoolObject
    for object in controller.model.objectList:
        if (
            object.objtype == CHEM_TYPE
            and object.subtype == "ICHLOR"
            and PRIM_ATTR in object.attributes
        ):
            numbers.append(
                PoolNumber(
                    entry,
                    controller,
                    object,
                    unit_of_measurement=PERCENTAGE,
                    attribute_key=PRIM_ATTR,
                    name="+ Output %",
                    icon="mdi:gauge",
                )
            )
    async_add_entities(numbers)


# -------------------------------------------------------------------------------------


class PoolNumber(PoolEntity, NumberEntity):
    """Representation of a number."""

    def __init__(
        self,
        entry: ConfigEntry,
        controller: ModelController,
        poolObject: PoolObject,
        min_value: float = DEFAULT_MIN_VALUE,
        max_value: float = DEFAULT_MAX_VALUE,
        step: float = DEFAULT_STEP,
        **kwargs,
    ):
        """Initialize."""
        super().__init__(entry, controller, poolObject, **kwargs)
        self._min_value = min_value
        self._max_value = max_value
        self._step = step

    @property
    def min_value(self) -> float:
        """Return the minimum value."""
        return self._min_value

    @property
    def max_value(self) -> float:
        """Return the maximum value."""
        return self._max_value

    @property
    def step(self) -> float:
        """Return the increment/decrement step."""
        return self._step

    @property
    def value(self) -> float:
        """Return the current value."""
        return self._poolObject[self._attribute_key]

    def set_value(self, value: float) -> None:
        """Update the current value."""
        changes = {self._attribute_key: str(int(value))}
        self.requestChanges(changes)
