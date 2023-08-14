""" NWS Alerts """
import logging
from datetime import timedelta

import aiohttp
from async_timeout import timeout
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import (
    async_entries_for_config_entry,
    async_get,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_ENDPOINT,
    CONF_GPS_LOC,
    CONF_INTERVAL,
    CONF_TIMEOUT,
    CONF_TRACKER,
    CONF_ZONE_ID,
    COORDINATOR,
    DEFAULT_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
    ISSUE_URL,
    PLATFORMS,
    USER_AGENT,
    VERSION,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Load the saved entities."""
    # Print startup message
    _LOGGER.info(
        "Version %s is starting, if you have any issues please report" " them here: %s",
        VERSION,
        ISSUE_URL,
    )
    hass.data.setdefault(DOMAIN, {})

    if config_entry.unique_id is not None:
        hass.config_entries.async_update_entry(config_entry, unique_id=None)

        ent_reg = async_get(hass)
        for entity in async_entries_for_config_entry(ent_reg, config_entry.entry_id):
            ent_reg.async_update_entity(
                entity.entity_id, new_unique_id=config_entry.entry_id
            )

    updated_config = config_entry.data.copy()

    # Strip spaces from manually entered GPS locations
    if CONF_GPS_LOC in updated_config:
        updated_config[CONF_GPS_LOC].replace(" ", "")

    if updated_config != config_entry.data:
        hass.config_entries.async_update_entry(config_entry, data=updated_config)

    config_entry.add_update_listener(update_listener)

    # Setup the data coordinator
    coordinator = AlertsDataUpdateCoordinator(
        hass,
        config_entry.data,
        config_entry.data.get(CONF_TIMEOUT),
        config_entry.data.get(CONF_INTERVAL),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN][config_entry.entry_id] = {
        COORDINATOR: coordinator,
    }

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Handle removal of an entry."""
    try:
        await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
        _LOGGER.info("Successfully removed sensor from the " + DOMAIN + " integration")
    except ValueError:
        pass
    return True


async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry):
    """Update listener."""
    if config_entry.data == config_entry.options:
        _LOGGER.debug("No changes detected not reloading sensors.")
        return

    new_data = config_entry.options.copy()
    hass.config_entries.async_update_entry(
        entry=config_entry,
        data=new_data,
    )

    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate an old config entry."""
    version = config_entry.version

    # 1-> 2: Migration format
    if version == 1:
        _LOGGER.debug("Migrating from version %s", version)
        updated_config = config_entry.data.copy()

        if CONF_INTERVAL not in updated_config.keys():
            updated_config[CONF_INTERVAL] = DEFAULT_INTERVAL
        if CONF_TIMEOUT not in updated_config.keys():
            updated_config[CONF_TIMEOUT] = DEFAULT_TIMEOUT

        if updated_config != config_entry.data:
            hass.config_entries.async_update_entry(config_entry, data=updated_config)

        config_entry.version = 2
        _LOGGER.debug("Migration to version %s complete", config_entry.version)

    return True


class AlertsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching NWS Alert data."""

    def __init__(self, hass, config, the_timeout: int, interval: int):
        """Initialize."""
        self.interval = timedelta(minutes=interval)
        self.name = config[CONF_NAME]
        self.timeout = the_timeout
        self.config = config
        self.hass = hass

        _LOGGER.debug("Data will be update every %s", self.interval)

        super().__init__(hass, _LOGGER, name=self.name, update_interval=self.interval)

    async def _async_update_data(self):
        """Fetch data"""
        coords = None
        if CONF_TRACKER in self.config:
            coords = await self._get_tracker_gps()
        async with timeout(self.timeout):
            try:
                data = await update_alerts(self.config, coords)
            except Exception as error:
                raise UpdateFailed(error) from error
            return data

    async def _get_tracker_gps(self):
        """Return device tracker GPS data."""
        tracker = self.config[CONF_TRACKER]
        entity = self.hass.states.get(tracker)
        if entity and "source_type" in entity.attributes:
            return f"{entity.attributes['latitude']},{entity.attributes['longitude']}"
        return None


async def update_alerts(config, coords) -> dict:
    """Fetch new state data for the sensor.
    This is the only method that should fetch new data for Home Assistant.
    """

    data = await async_get_state(config, coords)
    return data


async def async_get_state(config, coords) -> dict:
    """Query API for status."""

    zone_id = ""
    gps_loc = ""
    url = "%s/alerts/active/count" % API_ENDPOINT
    values = {
        "state": 0,
        "event": None,
        "event_id": None,
        "message_type": None,
        "event_status": None,
        "event_severity": None,
        "event_expires": None,
        "display_desc": None,
        "spoken_desc": None,
    }
    headers = {"User-Agent": USER_AGENT, "Accept": "application/ld+json"}
    data = None

    if CONF_ZONE_ID in config:
        zone_id = config[CONF_ZONE_ID]
        _LOGGER.debug("getting state for %s from %s" % (zone_id, url))
    elif CONF_GPS_LOC in config or CONF_TRACKER in config:
        if coords is not None:
            gps_loc = coords
        else:
            gps_loc = config[CONF_GPS_LOC].replace(" ", "")
        _LOGGER.debug("getting state for %s from %s" % (gps_loc, url))

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            if r.status == 200:
                data = await r.json()
            else:
                _LOGGER.error("Problem updating NWS data: (%s) - %s", r.status, r.body)

    if data is not None:
        # Reset values before reassigning
        if "zones" in data and zone_id != "":
            for zone in zone_id.split(","):
                if zone in data["zones"]:
                    values = await async_get_alerts(zone_id=zone_id)
                    break
        else:
            values = await async_get_alerts(gps_loc=gps_loc)

    return values


async def async_get_alerts(zone_id: str = "", gps_loc: str = "") -> dict:
    """Query API for Alerts."""

    url = ""
    values = {
        "state": 0,
        "event": None,
        "event_id": None,
        "message_type": None,
        "event_status": None,
        "event_severity": None,
        "event_expires": None,
        "display_desc": None,
        "spoken_desc": None,
    }
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    data = None

    if zone_id != "":
        url = "%s/alerts/active?zone=%s" % (API_ENDPOINT, zone_id)
        _LOGGER.debug("getting alert for %s from %s" % (zone_id, url))
    elif gps_loc != "":
        url = "%s/alerts/active?point=%s" % (API_ENDPOINT, gps_loc)
        _LOGGER.debug("getting alert for %s from %s" % (gps_loc, url))

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            if r.status == 200:
                data = await r.json()
            else:
                _LOGGER.error("Problem updating NWS data: (%s) - %s", r.status, r.body)

    if data is not None:
        events = []
        headlines = []
        event_id = ""
        message_type = ""
        event_status = ""
        event_severity = ""
        event_expires = ""
        display_desc = ""
        spoken_desc = ""
        features = data["features"]
        for alert in features:
            event = alert["properties"]["event"]
            if "NWSheadline" in alert["properties"]["parameters"]:
                headline = alert["properties"]["parameters"]["NWSheadline"][0]
            else:
                headline = event

            id = alert["id"]
            type = alert["properties"]["messageType"]
            status = alert["properties"]["status"]
            description = alert["properties"]["description"]
            instruction = alert["properties"]["instruction"]
            severity = alert["properties"]["severity"]
            certainty = alert["properties"]["certainty"]
            expires = alert["properties"]["expires"]

            # if event in events:
            #    continue

            events.append(event)
            headlines.append(headline)

            if display_desc != "":
                display_desc += "\n\n-\n\n"

            display_desc += (
                "\n>\nHeadline: %s\nStatus: %s\nMessage Type: %s\nSeverity: %s\nCertainty: %s\nExpires: %s\nDescription: %s\nInstruction: %s"
                % (
                    headline,
                    status,
                    type,
                    severity,
                    certainty,
                    expires,
                    description,
                    instruction,
                )
            )

            if event_id != "":
                event_id += " - "

            event_id += id

            if message_type != "":
                message_type += " - "

            message_type += type

            if event_status != "":
                event_status += " - "

            event_status += status

            if event_severity != "":
                event_severity += " - "

            event_severity += severity

            if event_expires != "":
                event_expires += " - "

            event_expires += expires

        if headlines:
            num_headlines = len(headlines)
            i = 0
            for headline in headlines:
                i += 1
                if spoken_desc != "":
                    if i == num_headlines:
                        spoken_desc += "\n\n-\n\n"
                    else:
                        spoken_desc += "\n\n-\n\n"

                spoken_desc += headline

        if len(events) > 0:
            event_str = ""
            for item in events:
                if event_str != "":
                    event_str += " - "
                event_str += item

            values["state"] = len(events)
            values["event"] = event_str
            values["event_id"] = event_id
            values["message_type"] = message_type
            values["event_status"] = event_status
            values["event_severity"] = event_severity
            values["event_expires"] = event_expires
            values["display_desc"] = display_desc
            values["spoken_desc"] = spoken_desc

    return values
