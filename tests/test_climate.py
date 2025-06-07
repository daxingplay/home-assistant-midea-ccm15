import pytest
from unittest.mock import AsyncMock, MagicMock
from homeassistant.components.climate.const import HVACMode, FAN_AUTO, FAN_LOW
from custom_components.ccm15.climate import CCM15Climate
from custom_components.ccm15.coordinator import CCM15DataUpdateCoordinator


@pytest.fixture
def mock_coordinator():
    coordinator = MagicMock(spec=CCM15DataUpdateCoordinator)
    coordinator.data = {
        "ac1": {
            "temp": 22,
            "settemp": 24,
            "fan": 2,
            "ac_mode": 0,
        }
    }
    coordinator.api.async_set_state = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def climate_entity(mock_coordinator):
    return CCM15Climate(mock_coordinator, "ac1")


def test_current_temperature(climate_entity):
    assert climate_entity.current_temperature == 22


def test_target_temperature(climate_entity):
    assert climate_entity.target_temperature == 24


def test_fan_mode(climate_entity):
    assert climate_entity.fan_mode == FAN_LOW


def test_hvac_mode(climate_entity):
    assert climate_entity.hvac_mode == HVACMode.COOL


@pytest.mark.asyncio
async def test_async_set_temperature(climate_entity, mock_coordinator):
    await climate_entity.async_set_temperature(temperature=25)
    mock_coordinator.api.async_set_state.assert_called_once_with(2, 0, 2, 25)
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_async_set_hvac_mode(climate_entity, mock_coordinator):
    await climate_entity.async_set_hvac_mode(HVACMode.HEAT)
    mock_coordinator.api.async_set_state.assert_called_once_with(2, 1, 2, 24)
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_async_set_fan_mode(climate_entity, mock_coordinator):
    await climate_entity.async_set_fan_mode(FAN_AUTO)
    mock_coordinator.api.async_set_state.assert_called_once_with(2, 0, 0, 24)
    mock_coordinator.async_request_refresh.assert_called_once()
