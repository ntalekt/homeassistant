"""Model class for storing a Pentair system."""

import logging
from typing import List

from .attributes import (
    ALL_ATTRIBUTES_BY_TYPE,
    CIRCUIT_TYPE,
    FEATR_ATTR,
    OBJTYP_ATTR,
    PARENT_ATTR,
    SNAME_ATTR,
    STATUS_ATTR,
    SUBTYP_ATTR,
)

_LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------


class PoolObject:
    """Representation of an object in the Pentair system."""

    def __init__(self, objnam, params):
        """Initialize."""
        self._objnam = objnam
        self._objtyp = params.pop(OBJTYP_ATTR)
        self._subtyp = params.pop(SUBTYP_ATTR, None)
        self._properties = params

    @property
    def objnam(self):
        """Return the id of the object (OBJNAM)."""
        return self._objnam

    @property
    def sname(self):
        """Return the friendly name (SNAME)."""
        return self._properties.get(SNAME_ATTR)

    @property
    def objtype(self):
        """Return the object type."""
        return self._objtyp

    @property
    def subtype(self):
        """Return the object subtype."""
        return self._subtyp

    @property
    def status(self) -> str:
        """Return the object status."""
        return self._properties.get(STATUS_ATTR)

    @property
    def offStatus(self) -> str:
        """Return the value of an OFF status."""
        return "4" if self.objtype == "PUMP" else "OFF"

    @property
    def onStatus(self) -> str:
        """Return the value of an ON status."""
        return "10" if self.objtype == "PUMP" else "ON"

    @property
    def isALight(self) -> bool:
        """Return True is the object is a light."""
        return self.objtype == CIRCUIT_TYPE and self.subtype in [
            "LIGHT",
            "INTELLI",
            "GLOW",
            "GLOWT",
            "DIMMER",
            "MAGIC2",
        ]

    @property
    def supportColorEffects(self) -> bool:
        """Return True is object is a light that support color effects."""
        return self.isALight and self.subtype in ["INTELLI", "MAGIC2"]

    @property
    def isALightShow(self) -> bool:
        """Return True is the object is a light show."""
        return self.objtype == CIRCUIT_TYPE and self.subtype == "LITSHO"

    @property
    def isFeatured(self) -> bool:
        """Return True is the object is Featured."""
        return self[FEATR_ATTR] == "ON"

    def __getitem__(self, key):
        """Return the value for attribure 'key'."""
        return self._properties.get(key)

    def __str__(self):
        """Return a friendly string representation."""
        result = f"{self.objnam} "
        result += (
            f"({self.objtype}/{self.subtype}):"
            if self.subtype
            else f"({self.objtype}):"
        )
        for key in sorted(set(self._properties.keys())):
            value = self._properties[key]
            if type(value) is list:
                value = "[" + ",".join(map(lambda v: f"{  {str(v)} }", value)) + "]"
            result += f" {key}: {value}"
        return result

    @property
    def attributes(self) -> list:
        """Return the list of attributes for this object."""
        return list(self._properties.keys())

    def update(self, updates):
        """Update the object from a set of key/value pairs, return the changed attributes."""

        changed = {}

        for (key, value) in updates.items():

            if key in self._properties:
                if self._properties[key] == value:
                    # ignore unchanged existing value
                    continue

            # there are a few case when we receive the type/subtype in an update
            if key == OBJTYP_ATTR:
                self._objtyp = value
            elif key == SUBTYP_ATTR:
                self._subtyp = value
            else:
                self._properties[key] = value
            changed[key] = value

        return changed


# ---------------------------------------------------------------------------


class PoolModel:
    """Representation of a subset of the underlying Pentair system."""

    def __init__(self, attributeMap=ALL_ATTRIBUTES_BY_TYPE):
        """Initialize."""
        self._objects: dict[str, PoolObject] = {}
        self._systemObject: PoolObject = None
        self._attributeMap = attributeMap

    @property
    def objectList(self):
        """Return the list of objects contained in the model."""
        return self._objects.values()

    @property
    def objects(self):
        """Return the dictionary of objects contained in the model."""
        return self._objects

    @property
    def numObjects(self) -> int:
        """Return the number of objects contained in the model."""
        return len(self._objects)

    def __iter__(self):
        """Allow iteration over all values."""
        return iter(self._objects.values())

    def __getitem__(self, key) -> PoolObject:
        """Return an object based on its objnam."""
        return self._objects.get(key)

    def getByType(self, type: str, subtype: str = None) -> List[PoolObject]:
        """Return all the object which match the type and the optional subtype.

        examples:
            getByType('BODY') will return the object of type 'BODY'
            getByType('BODY','SPA') will only return the Spa
        """
        return list(
            filter(
                lambda object: object.objtype == type
                and (not subtype or object.subtype == subtype),
                self,
            )
        )

    def getChildren(self, object: PoolObject) -> List[PoolObject]:
        """Return the children of a given object."""
        return list(filter(lambda v: v[PARENT_ATTR] == object.objnam, self))

    def addObject(self, objnam, params):
        """Update the model with a new object."""
        # because the controller may be started more than once
        # we don't override existing objects
        object = self._objects.get(objnam)

        if not object:
            object = PoolObject(objnam, params)
            if object.objtype == "SYSTEM":
                self._systemObject = object
            if object.objtype in self._attributeMap:
                self._objects[objnam] = object
            else:
                object = None
        else:
            object.update(params)
        return object

    def addObjects(self, objList: list):
        """Create or update from all the objects in the list."""
        for elt in objList:
            self.addObject(elt["objnam"], elt["params"])

    def attributesToTrack(self):
        """Return all the object/attributes we want to track."""
        query = []
        for object in self.objectList:
            attributes = self._attributeMap.get(object.objtype)
            if not attributes:
                # if we don't specify a set of attributes for this object type
                # we will default to all know attributes for this type
                attributes = ALL_ATTRIBUTES_BY_TYPE.get(object.objtype)
            if attributes:
                query.append({"objnam": object.objnam, "keys": list(attributes)})
        return query

    def processUpdates(self, updates: list):
        """Update the state of the objects in the model."""
        updated = {}
        for update in updates:
            objnam = update["objnam"]
            object = self._objects.get(objnam)
            if object:
                changed = object.update(update["params"])
                if changed:
                    updated[objnam] = changed
        return updated
