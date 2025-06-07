"""CCM15 base entity class."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ATTRIBUTION

class CCM15Entity(CoordinatorEntity):
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator, unique_id):
        super().__init__(coordinator)
        self._attr_unique_id = unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            name="Midea CCM-15",
            manufacturer="Midea",
            model="CCM-15",
        ) 