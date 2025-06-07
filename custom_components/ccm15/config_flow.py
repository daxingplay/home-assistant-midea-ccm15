"""Adds config flow for CCM15."""

from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import selector
from .const import DOMAIN, LOGGER, DEFAULT_PORT
from .api import CCM15ApiClient


class CCM15ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for CCM15."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the user step in the config flow."""
        errors = {}
        if user_input is not None:
            try:
                # Test connection to the CCM15 device
                client = CCM15ApiClient(
                    user_input[CONF_HOST], user_input[CONF_PORT], self.hass
                )
                await client.async_get_status()
            except ConnectionError as err:
                LOGGER.error(f"Connection error with CCM15 device: {err}")
                errors["base"] = "connection"
            except TimeoutError as err:
                LOGGER.error(f"Timeout error with CCM15 device: {err}")
                errors["base"] = "timeout"
            except Exception as err:
                LOGGER.error(f"Unexpected error with CCM15 device: {err}")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_PORT, default=DEFAULT_PORT
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1, max=65535, mode=selector.NumberSelectorMode.BOX
                        ),
                    ),
                }
            ),
            errors=errors,
        )
