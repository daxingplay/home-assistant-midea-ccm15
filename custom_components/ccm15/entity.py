"""CCM15 base entity class."""

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import ATTRIBUTION, DOMAIN


class CCM15Entity(CoordinatorEntity):
    """CCM15 base entity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self, coordinator: DataUpdateCoordinator[dict[str, Any]], unique_id: str
    ) -> None:
        """
        Initialize the CCM15 entity.

        Args:
            coordinator: The data update coordinator for CCM15.
            unique_id: Unique identifier for the entity.

        """
        super().__init__(coordinator)
        self._attr_unique_id = unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            name="Midea CCM-15",
            manufacturer="Midea",
            model="CCM-15",
        )
