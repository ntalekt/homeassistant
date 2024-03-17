"""Pentair Intellicenter lights."""

from functools import reduce
import logging
from typing import Any, Dict

from homeassistant.components.light import (
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from . import PoolEntity
from .const import DOMAIN
from .pyintellicenter import (
    ACT_ATTR,
    CIRCUIT_ATTR,
    STATUS_ATTR,
    USE_ATTR,
    ModelController,
    PoolObject,
)

_LOGGER = logging.getLogger(__name__)

LIGHTS_EFFECTS = {
    "PARTY": "Party Mode",
    "CARIB": "Caribbean",
    "SSET": "Sunset",
    "ROMAN": "Romance",
    "AMERCA": "American",
    "ROYAL": "Royal",
    "WHITER": "White",
    "REDR": "Red",
    "BLUER": "Blue",
    "GREENR": "Green",
    "MAGNTAR": "Magenta",
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
):
    """Load pool lights based on a config entry."""

    controller: ModelController = hass.data[DOMAIN][entry.entry_id].controller

    lights = []

    object: PoolObject
    for object in controller.model.objectList:
        if object.isALight:
            lights.append(
                PoolLight(
                    entry,
                    controller,
                    object,
                    LIGHTS_EFFECTS if object.supportColorEffects else None,
                )
            )
        elif object.isALightShow:
            supportColorEffects = reduce(
                lambda x, y: x and y,
                map(
                    lambda obj: controller.model[obj[CIRCUIT_ATTR]].supportColorEffects,
                    controller.model.getChildren(object),
                ),
                True,
            )
            lights.append(
                PoolLight(
                    entry,
                    controller,
                    object,
                    LIGHTS_EFFECTS if supportColorEffects else None,
                )
            )

    async_add_entities(lights)


class PoolLight(PoolEntity, LightEntity):
    """Representation of an Pentair light."""

    def __init__(
        self,
        entry: ConfigEntry,
        controller: ModelController,
        poolObject: PoolObject,
        colorEffects: dict = None,
    ):
        """Initialize."""
        super().__init__(entry, controller, poolObject)
        # USE appears to contain extra info like color...
        self._extra_state_attributes = [USE_ATTR]

        self._features = 0
        self._supported_color_modes = ColorMode.ONOFF

        self._lightEffects = colorEffects
        self._reversedLightEffects = (
            dict(map(reversed, colorEffects.items())) if colorEffects else None
        )

        if self._lightEffects:
            self._features |= LightEntityFeature.EFFECT

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        return self._features

    @property
    def supported_color_modes(self) -> set[ColorMode] | set[str] | None:
        """Return supported color modes."""
        return self._supported_color_modes

    @property
    def effect_list(self) -> list:
        """Return the list of supported effects."""
        return list(self._reversedLightEffects.keys())

    @property
    def effect(self) -> str:
        """Return the current effect."""
        return self._lightEffects.get(self._poolObject[USE_ATTR])

    @property
    def is_on(self) -> bool:
        """Return the state of the light."""
        return self._poolObject.status == self._poolObject.onStatus

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        self.requestChanges({STATUS_ATTR: "OFF"})

    def turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""

        changes = {STATUS_ATTR: self._poolObject.onStatus}

        if ATTR_EFFECT in kwargs:
            effect = kwargs[ATTR_EFFECT]
            new_use = self._reversedLightEffects.get(effect)
            if new_use:
                changes[ACT_ATTR] = new_use

        self.requestChanges(changes)

    def isUpdated(self, updates: Dict[str, Dict[str, str]]) -> bool:
        """Return true if the entity is updated by the updates from Intellicenter."""

        myUpdates = updates.get(self._poolObject.objnam, {})

        return myUpdates and {STATUS_ATTR, USE_ATTR} & myUpdates.keys()
