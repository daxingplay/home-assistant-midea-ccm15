"""Support for Midea's CCM-15 thermostats (refactored for HACS and modern HA)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_OFF,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.ccm15.coordinator import CCM15DataUpdateCoordinator

FAN_MAP = {
    FAN_AUTO: 0,
    FAN_LOW: 2,
    FAN_MEDIUM: 3,
    FAN_HIGH: 4,
    FAN_OFF: 5,
}
REV_FAN_MAP: dict[str, str] = {
    FAN_OFF: "off",
    FAN_AUTO: "auto",
    FAN_LOW: "low",
    FAN_MEDIUM: "medium",
    FAN_HIGH: "high",
}

HVAC_MAP = {
    HVACMode.COOL: 0,
    HVACMode.HEAT: 1,
    HVACMode.DRY: 2,
    HVACMode.FAN_ONLY: 3,
    HVACMode.OFF: 4,
    HVACMode.AUTO: 5,
}
REV_HVAC_MAP: dict[int, HVACMode] = {
    HVACMode.COOL: "cool",
    HVACMode.HEAT: "heat",
    HVACMode.DRY: "dry",
    HVACMode.FAN_ONLY: "fan_only",
    HVACMode.OFF: "off",
    HVACMode.AUTO: "auto",
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up CCM15 climate entities."""
    coordinator: CCM15DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    status = await coordinator.api.async_get_status()
    entities = [CCM15Climate(coordinator, ac_name) for ac_name in status]
    async_add_entities(entities)


class CCM15Climate(CoordinatorEntity, ClimateEntity):
    """Representation of a CCM15 climate entity."""

    def __init__(self, coordinator: CCM15DataUpdateCoordinator, ac_name: str) -> None:
        """Initialize the CCM15 climate entity."""
        super().__init__(coordinator)
        self._ac_name = ac_name
        self._ac_id = 2 ** int(ac_name.strip("a"))
        self._attr_name = f"Midea CCM15 {ac_name}"
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
        )
        self._attr_hvac_modes = [
            HVACMode.COOL,
            HVACMode.HEAT,
            HVACMode.DRY,
            HVACMode.FAN_ONLY,
            HVACMode.OFF,
            HVACMode.AUTO,
        ]
        self._attr_fan_modes = [FAN_OFF, FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self.coordinator.data[self._ac_name]["current_temperature"]

    @property
    def target_temperature(self):
        return self._get_ac_state().get("settemp")

    @property
    def fan_mode(self):
        fan = self._get_ac_state().get("fan")
        return REV_FAN_MAP.get(fan, FAN_AUTO)

    @property
    def hvac_mode(self):
        mode = self._get_ac_state().get("ac_mode")
        return REV_HVAC_MAP.get(mode, HVACMode.OFF)

    def _get_ac_state(self) -> dict:
        """Get the current state of the AC unit."""
        return self.coordinator.data.get(self._ac_name, {})

    async def async_set_temperature(self, **kwargs: float) -> None:
        """Set the target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        ac_state = self._get_ac_state()
        await self.coordinator.api.async_set_state(
            self._ac_id,
            ac_state.get("ac_mode", 0),
            ac_state.get("fan", 0),
            int(temp),
        )
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        ac_state = self._get_ac_state()
        await self.coordinator.api.async_set_state(
            self._ac_id,
            HVAC_MAP[hvac_mode],
            ac_state.get("fan", 0),
            ac_state.get("settemp", 24),
        )
        await self.coordinator.async_request_refresh()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set the fan mode."""
        ac_state = self._get_ac_state()
        await self.coordinator.api.async_set_state(
            self._ac_id,
            ac_state.get("ac_mode", 0),
            FAN_MAP[fan_mode],
            ac_state.get("settemp", 24),
        )
        await self.coordinator.async_request_refresh()
