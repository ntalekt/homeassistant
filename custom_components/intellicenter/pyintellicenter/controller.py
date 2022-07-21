"""Controller classes for Pentair Intellicenter."""

import asyncio
from asyncio import Future
from hashlib import blake2b
import logging
import traceback
from typing import Dict, Optional

from .attributes import (
    MODE_ATTR,
    OBJTYP_ATTR,
    PARENT_ATTR,
    PROPNAME_ATTR,
    SNAME_ATTR,
    SUBTYP_ATTR,
    SYSTEM_TYPE,
    VER_ATTR,
)
from .model import PoolModel
from .protocol import ICProtocol

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class CommandError(Exception):
    """Represents an error in response to a Pentair request."""

    def __init__(self, errorCode):
        """Initialize from a Pentair errorCode."""
        self._errorCode = errorCode

    @property
    def errorCode(self):
        """Return the error code."""
        return self._errorCode


# -------------------------------------------------------------------------------------


class SystemInfo:
    """Represents minimal information about a Pentair system."""

    ATTRIBUTES_LIST = [PROPNAME_ATTR, VER_ATTR, MODE_ATTR, SNAME_ATTR]

    def __init__(self, objnam: str, params: dict):
        """Initialize from a dictionary."""
        self._objnam = objnam
        self._propName = params[PROPNAME_ATTR]
        self._sw_version = params[VER_ATTR]
        self._mode = params[MODE_ATTR]
        # here we compute what is expected to be a unique_id
        # from the internal name of the system object
        h = blake2b(digest_size=8)
        h.update(params[SNAME_ATTR].encode())
        self._unique_id = h.hexdigest()

    @property
    def propName(self):
        """Return the name of the 'property' where the system is."""
        return self._propName

    @property
    def swVersion(self):
        """Return the software version of the system."""
        return self._sw_version

    @property
    def usesMetric(self):
        """Return True if the system uses metric for temperature units."""
        return self._mode == "METRIC"

    @property
    def uniqueID(self):
        """Return a unique id for that system."""
        return self._unique_id

    def update(self, updates):
        """Update the object from a set of key/value pairs."""
        _LOGGER.debug(f"updating system info with {updates}")
        self._propName = updates.get(PROPNAME_ATTR, self._propName)
        self._sw_version = updates.get(VER_ATTR, self._sw_version)
        self._mode = updates.get(MODE_ATTR, self._mode)


# -------------------------------------------------------------------------------------


def prune(obj):
    """Cleanup a full object tree from undefined parameters."""

    # undefined meaning key == value which is what Pentair returns
    if type(obj) is list:
        return [prune(item) for item in obj]
    elif type(obj) is dict:
        result = {}
        for (key, value) in obj.items():
            if key != value:
                result[key] = prune(value)
        return result
    return obj


class BaseController:
    """A basic controller connecting to a Pentair system."""

    def __init__(self, host, port=6681, loop=None):
        """Initialize the controller."""
        self._host = host
        self._port = port
        self._loop = loop

        self._transport = None
        self._protocol = None

        self._diconnectedCallback = None

        self._requests = {}

    @property
    def host(self) -> str:
        """Return the host the controller is connected to."""
        return self._host

    def connection_made(self, protocol, transport):
        """Handle the callback from the protocol."""
        _LOGGER.debug(f"Connection established to {self._host}")

    def connection_lost(self, exc):
        """Handle the callback from the protocol."""
        self.stop()  # should that be a cleanup instead?
        if self._diconnectedCallback:
            self._diconnectedCallback(self, exc)

    async def start(self) -> None:
        """Connect to the Pentair system and retrieves some system information."""
        self._transport, self._protocol = await self._loop.create_connection(
            lambda: ICProtocol(self), self._host, self._port
        )

        # we start by requesting a few attributes from the SYSTEM object
        # and therefore validate that the system connected is indeed a IntelliCenter
        msg = await self.sendCmd(
            "GetParamList",
            {
                "condition": f"{OBJTYP_ATTR}={SYSTEM_TYPE}",
                "objectList": [
                    {
                        "objnam": "INCR",
                        "keys": SystemInfo.ATTRIBUTES_LIST,
                    }
                ],
            },
        )

        info = msg["objectList"][0]
        self._systemInfo = SystemInfo(info["objnam"], info["params"])

    def stop(self):
        """Stop all activities from this controller and disconnect."""
        if self._transport:
            for request in self._requests.values():
                request.cancel()
            self._transport.close()
            self._transport = None
            self._protocol = None

    def sendCmd(self, cmd, extra=None, waitForResponse=True) -> Optional[Future]:
        """
        Send a command with optional extra parameters to the system.

        if waitForResponse is True, a Future is created and returned
        so either call resp = await controller.sendCmd(cmd,extra)
        or controller.sendCmd(cmd,extra,waitForResponse=False)
        """

        _LOGGER.debug(f"CONTROLLER: sendCmd: {cmd} {extra} {waitForResponse}")
        future = Future() if waitForResponse else None

        if self._protocol:
            msg_id = self._protocol.sendCmd(cmd, extra)
            self._requests[msg_id] = future
        elif future:
            future.setException(Exception("controller disconnected"))

        return future

    def requestChanges(
        self, objnam: str, changes: dict, waitForResponse=True
    ) -> Future:
        """Submit a change for a given object."""
        return self.sendCmd(
            "SETPARAMLIST",
            {"objectList": [{"objnam": objnam, "params": changes}]},
            waitForResponse=waitForResponse,
        )

    async def getAllObjects(self, attributeList: list):
        """Return the values of given attributes for all objects in the system."""

        result = await self.sendCmd(
            "GetParamList",
            {
                "condition": "",
                "objectList": [{"objnam": "INCR", "keys": attributeList}],
            },
        )

        # since we might have asked for more attributes than any given object
        # might define, we prune the resulting tree from these 'undefined' values
        return prune(result["objectList"])

    async def getQuery(self, queryName: str, arguments: str = ""):
        """Return the result of a Query."""
        result = await self.sendCmd(
            "GetQuery", {"queryName": queryName, "arguments": arguments}
        )
        return result["answer"]

    def getCircuitNames(self):
        """Return the list of circuit names."""
        return self.getQuery("GetCircuitNames")

    async def getCircuitTypes(self):
        """Return a dictionary: key: circuit's SUBTYP , value: 'friendly' readable string."""

        return {
            v["systemValue"]: v["readableValue"]
            for v in await self.getQuery("GetCircuitTypes")
        }

    def getHardwareDefinition(self):
        """Return the full hardware definition of the system."""
        return prune(self.getQuery("GetHardwareDefinition"))

    def getConfiguration(self):
        """Return the current 'configuration' of the system."""
        return self.getQuery("GetConfiguration")

    def receivedMessage(self, msg_id: str, command: str, response: str, msg: dict):
        """Handle the callback for a incoming message.

        msd_id is the id of the incoming message
        response is the success (200) or error code or None (if this was a notification)
        msg is the while message as a dictionary (parsing of the JSON object)
        """

        future = self._requests.pop(msg_id, 0)

        # here future can be either:
        #  - 0 if there was no corresponding request matching this response
        #      like in the case of a notification
        #  - a future is the sender of the request wanted to get the results
        #  - None is the sender declined to wait for the response (in sendCmd)

        _LOGGER.debug(
            f"CONTROLLER: receivedMessage: {msg_id} {command} {response} {future}"
        )

        if not future == 0:
            if future:
                if response == "200":
                    future.set_result(msg)
                else:
                    future.set_exception(CommandError(response))
            else:
                _LOGGER.debug(f"ignoring response for msg_id {msg_id}")
        elif response is None or response == "200":
            self.processMessage(command, msg)
        else:
            _LOGGER.warning(f"CONTROLLER: error {response} : {msg}")

    def processMessage(self, command: str, msg):
        """Process a notification message."""
        pass

    @property
    def systemInfo(self):
        """Return the (cached) system information."""
        return self._systemInfo


# -------------------------------------------------------------------------------------


class ModelController(BaseController):
    """A controller creating and updating a PoolModel."""

    def __init__(self, host, model, port=6681, loop=None):
        """Initialize the controller."""
        super().__init__(host, port, loop)
        self._model: PoolModel = model

        self._updatedCallback = None

    @property
    def model(self) -> PoolModel:
        """Return the model this controller manages."""
        return self._model

    async def start(self):
        """Start the controller, fetch and start monitoring the model."""
        await super().start()

        # now we retrieve all the objects type, subtype, sname and parent
        allObjects = await self.getAllObjects(
            [OBJTYP_ATTR, SUBTYP_ATTR, SNAME_ATTR, PARENT_ATTR]
        )
        # and process that list into our model
        self.model.addObjects(allObjects)

        # _LOGGER.debug(f"objects received: {allObjects}")

        _LOGGER.info(f"model now contains {self.model.numObjects} objects")

        try:
            # now that I have my object loaded in the model
            # build a query to monitors all their relevant attributes

            attributes = self._model.attributesToTrack()

            query = []
            numAttributes = 0
            for items in attributes:
                query.append(items)
                numAttributes += len(items["keys"])
                # a query too large can choke the protocol...
                # we split them in maximum of 50 attributes (arbitrary but seems to work)
                if numAttributes >= 50:
                    res = await self.sendCmd("RequestParamList", {"objectList": query})
                    self._applyUpdates(res["objectList"])
                    query = []
                    numAttributes = 0
            # and issue the remaining elements if any
            if query:
                res = await self.sendCmd("RequestParamList", {"objectList": query})
                self._applyUpdates(res["objectList"])

        except Exception as err:
            traceback.print_exc()
            raise err

    def receivedQueryResult(self, queryName: str, answer):
        """Handle the result of all 'getQuery' responses."""

        # none are used by default
        # see Pentair protocol documentation for details
        # GetHardwareDefinition, GetConfiguration

        pass

    def _applyUpdates(self, changesAsList):
        """Apply updates received to the model."""

        updates = self._model.processUpdates(changesAsList)

        # if an update happens on the SYSTEM object
        # also applies it to our cached SystemInfo
        systemObjnam = self._systemInfo._objnam
        if systemObjnam in updates:
            self._systemInfo.update(updates[systemObjnam])

        if updates and self._updatedCallback:
            self._updatedCallback(self, updates)

        return updates

    def receivedNotifyList(self, changes):
        """Handle the notifications from IntelliCenter when tracked objects are modified."""

        try:
            # apply the changes back to the model
            self._applyUpdates(changes)

        except Exception as err:
            _LOGGER.error(f"CONTROLLER: receivedNotifyList {err}")

    def receivedWriteParamList(self, changes):
        """Handle the response to a change requested on an object."""

        try:
            self._applyUpdates(changes)

        except Exception as err:
            _LOGGER.error(f"CONTROLLER: receivedWriteParamList {err}")

    def receivedSystemConfig(self, objectList):
        """Handle the response for a request for objects."""

        _LOGGER.debug(
            f"CONTROLLER: received SystemConfig for {len(objectList)} object(s)"
        )

        # note that here we might create new objects
        self.model.addObjects(objectList)

    def processMessage(self, command: str, msg):
        """Handle the callback for an incoming message."""

        _LOGGER.debug(f"CONTROLLER: received {command} response: {msg}")

        try:
            if command == "SendQuery":
                self.receivedQueryResult(msg["queryName"], msg["answer"])
            elif command == "NotifyList":
                self.receivedNotifyList(msg["objectList"])
            elif command == "WriteParamList":
                self.receivedWriteParamList(msg["objectList"][0]["changes"])
            elif command == "SendParamList":
                self.receivedSystemConfig(msg["objectList"])
            else:
                _LOGGER.debug(f"no handler for {command}")
        except Exception as err:
            _LOGGER.error(f"error {err} while processing {msg}")
            # traceback.print_exc()


# -------------------------------------------------------------------------------------


class ConnectionHandler:
    """Helper class to recover the connect/disconnect/reconnect cycle of a controller."""

    def __init__(self, controller, timeBetweenReconnects=30):
        """Initialize the handler."""
        self._controller = controller

        self._starterTask = None
        self._stopped = False
        self._firstTime = True

        self._timeBetweenReconnects = timeBetweenReconnects

        controller._diconnectedCallback = self._diconnectedCallback

        if hasattr(controller, "_updatedCallback"):
            controller._updatedCallback = self.updated

    @property
    def controller(self):
        """Return the controller the handler manages."""
        return self._controller

    async def start(self):
        """Start the handler loop."""
        if not self._starterTask:
            self._starterTask = asyncio.create_task(self._starter())

    def _next_delay(self, currentDelay: int) -> int:
        """Compute the delay before the next reconnection attempt.

        default is exponential backoff with a 1.5 factor
        """
        return int(currentDelay * 1.5)

    async def _starter(self, initialDelay=0):
        """Attempt to start the controller."""
        started = False
        delay = self._timeBetweenReconnects
        while not started:
            try:
                if initialDelay:
                    self.retrying(delay)
                    await asyncio.sleep(initialDelay)
                _LOGGER.debug("trying to start controller")

                await self._controller.start()

                if self._firstTime:
                    self.started(self._controller)
                    self._firstTime = False
                else:
                    self.reconnected(self._controller)

                started = True
                self._starterTask = None
            except Exception as err:
                _LOGGER.error(f"cannot start: {err}")
                self.retrying(delay)
                await asyncio.sleep(delay)
                delay = self._next_delay(delay)

    def stop(self):
        """Stop the handler and the associated controller."""
        _LOGGER.debug(f"terminating connection to {self._controller.host}")
        self._stopped = True
        if self._starterTask:
            self._starterTask.cancel()
            self._starterTask = None
        self._controller.stop()

    def _diconnectedCallback(self, controller, err):
        """Handle the disconnection of the underlying controller."""
        self.disconnected(controller, err)
        if not self._stopped:
            _LOGGER.error(
                f"system disconnected  from {self._controller.host} {err if err else ''}"
            )
            self._starterTask = asyncio.create_task(
                self._starter(self._timeBetweenReconnects)
            )

    def started(self, controller):
        """Handle the first time the controller is started.

        further reconnections will trigger reconnected method instead
        """
        pass

    def retrying(self, delay):
        """Handle the fact that we will retry connection in {delay} seconds."""
        _LOGGER.info(f"will attempt to reconnect in {delay}s")

    def updated(self, controller: ModelController, updates: Dict):
        """Handle the callback that our underlying system has been modified.

        only invoked if the controller has a _updatedCallback attribute
        changes is expected to contain the list of modified objects
        """
        pass

    def disconnected(self, controller, exc):
        """Handle the controller being disconnected.

        exc will contain the underlying exception except if
        the hearbeat has been missed, in this case exc is None
        """
        pass

    def reconnected(self, controller):
        """Handle the controller being reconnected.

        only occurs if the controller was connected before
        """
        pass
