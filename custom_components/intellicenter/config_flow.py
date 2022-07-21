"""Config flow for Pentair Intellicenter integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant.config_entries import CONN_CLASS_LOCAL_PUSH, ConfigFlow
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol

from .const import DOMAIN
from .pyintellicenter import BaseController, SystemInfo

_LOGGER = logging.getLogger(__name__)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Pentair Intellicenter config flow."""

    VERSION = 1

    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize a new Intellicenter ConfigFlow."""
        pass

    async def async_step_user(
        self, user_input: Optional[ConfigType] = None
    ) -> Dict[str, Any]:
        """Handle a flow initiated by the user."""
        if user_input is None:
            return self._show_setup_form()

        try:
            system_info = await self._get_system_info(user_input[CONF_HOST])

            # Check if already configured
            await self.async_set_unique_id(system_info.uniqueID)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=system_info.propName, data={CONF_HOST: user_input[CONF_HOST]}
            )
        except CannotConnect:
            return self._show_setup_form({"base": "cannot_connect"})
        except Exception:  # pylint: disable=broad-except
            return self._show_setup_form({"base": "cannot_connect"})

    async def async_step_zeroconf(self, discovery_info: ConfigType) -> Dict[str, Any]:
        """Handle device found via zeroconf."""

        _LOGGER.debug(f"zeroconf discovery {discovery_info}")

        host = discovery_info.host

        if self._host_already_configured(host):
            return self.async_abort(reason="already_configured")

        try:
            system_info = await self._get_system_info(host)

            await self.async_set_unique_id(system_info.uniqueID)

            # if there is already a flow for this system, update the host ip address for it
            self._abort_if_unique_id_configured(updates={CONF_HOST: host})

            self.context.update(
                {
                    CONF_HOST: host,
                    CONF_NAME: system_info.propName,
                    "title_placeholders": {"name": system_info.propName},
                }
            )

            return self._show_confirm_dialog()

        except CannotConnect:
            return self.async_abort(reason="cannot_connect")
        except Exception:  # pylint: disable=broad-except
            return self.async_abort(reason="unknown")

    async def async_step_zeroconf_confirm(
        self, user_input: ConfigType = None
    ) -> Dict[str, Any]:
        """Handle a flow initiated by zeroconf."""
        if user_input is None:
            return self._show_confirm_dialog()

        try:
            system_info = await self._get_system_info(self.context.get(CONF_HOST))

            # Check if already configured
            await self.async_set_unique_id(system_info.uniqueID)
            self._abort_if_unique_id_configured()

        except CannotConnect:
            return self.async_abort(reason="cannot_connect")
        except Exception:  # pylint: disable=broad-except
            return self.async_abort(reason="unknown")

        return self.async_create_entry(
            title=system_info.propName, data={CONF_HOST: self.context.get(CONF_HOST)}
        )

    def _show_setup_form(self, errors: Optional[Dict] = None) -> Dict[str, Any]:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors or {},
        )

    def _show_confirm_dialog(self) -> Dict[str, Any]:
        """Show the confirm dialog to the user."""

        host = self.context.get(CONF_HOST)
        name = self.context.get(CONF_NAME)

        return self.async_show_form(
            step_id="zeroconf_confirm",
            description_placeholders={"host": host, "name": name},
        )

    async def _get_system_info(self, host: str) -> SystemInfo:
        """Attempt to connect to the host and retrieve basic system information."""

        controller = BaseController(host, loop=self.hass.loop)

        try:
            await controller.start()

            return controller.systemInfo
        except ConnectionRefusedError as err:
            raise CannotConnect from err
        finally:
            controller.stop()

    def _host_already_configured(self, host):
        """Check if we already have a system with the same host address."""
        existing_hosts = {
            entry.data[CONF_HOST]
            for entry in self._async_current_entries()
            if CONF_HOST in entry.data
        }
        return host in existing_hosts
