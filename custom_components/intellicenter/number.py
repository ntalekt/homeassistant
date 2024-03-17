"""Pentair Intellicenter numbers."""

import logging

from homeassistant.components.number import (
    NumberEntity,
    DEFAULT_MIN_VALUE,
    DEFAULT_MAX_VALUE,
    DEFAULT_STEP,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from . import PoolEntity
from .const import DOMAIN
from homeassistant.const import PERCENTAGE
from .pyintellicenter import (
    BODY_ATTR,
    BODY_TYPE,
    CHEM_TYPE,
    PRIM_ATTR,
    SEC_ATTR,
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
            bodies = controller.model.getByType(BODY_TYPE)
            intellichlor_bodies = object[BODY_ATTR].split(" ")

            body: PoolObject
            for body in bodies:
                intellichlor_index = intellichlor_bodies.index(body.objnam)
                attribute_key = None
                if intellichlor_index == 0:
                    attribute_key = PRIM_ATTR
                elif intellichlor_index == 1:
                    attribute_key = SEC_ATTR
                if attribute_key is not None:
                    numbers.append(
                        PoolNumber(
                            entry,
                            controller,
                            # body,
                            object,
                            unit_of_measurement=PERCENTAGE,
                            attribute_key=attribute_key,
                            name=f"+ Output % ({body.sname})",
                        )
                    )

    async_add_entities(numbers)


# -------------------------------------------------------------------------------------


class PoolNumber(PoolEntity, NumberEntity):
    """Representation of a pool number entity."""

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
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_icon = "mdi:gauge"

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return self._poolObject[self._attribute_key]

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        changes = {self._attribute_key: str(int(value))}
        self.requestChanges(changes)
