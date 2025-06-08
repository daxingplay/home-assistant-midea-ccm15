"""DataUpdateCoordinator for CCM15."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CCM15ApiClient
from .const import LOGGER

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


class CCM15DataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for CCM15."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """
        Initialize the CCM15 data update coordinator.

        Args:
            hass: Home Assistant instance.
            entry: Config entry for CCM15.

        """
        self._host = entry.data["host"]
        self._port = entry.data["port"]
        LOGGER.debug(
            "Initializing CCM15DataUpdateCoordinator with host %s and port %s",
            self._host,
            self._port,
        )
        self.api = CCM15ApiClient(entry.data["host"], entry.data["port"], hass)
        super().__init__(
            hass,
            LOGGER,
            name="CCM15 Data Coordinator",
            update_interval=timedelta(seconds=10),
        )

    def get_host(self) -> str:
        """Get the host."""
        return self._host

    def get_port(self) -> int:
        """Get the port."""
        return self._port

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the CCM15 device."""
        try:
            return await self.api.async_get_status()
        except Exception as err:
            error_message = f"Error communicating with CCM15 device: {err}"
            raise UpdateFailed(error_message) from err
