import pytest
from unittest.mock import AsyncMock, patch
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType
from custom_components.ccm15.config_flow import CCM15ConfigFlow
from custom_components.ccm15.const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT


@pytest.fixture
def mock_config_flow():
    return CCM15ConfigFlow()


@pytest.mark.asyncio
async def test_async_step_user(mock_config_flow):
    with patch(
        "custom_components.ccm15.api.CCM15ApiClient.async_get_status",
        new_callable=AsyncMock,
    ) as mock_get_status:
        mock_get_status.return_value = {"status": "ok"}

        user_input = {
            CONF_HOST: "192.168.1.100",
            CONF_PORT: DEFAULT_PORT,
        }

        result = await mock_config_flow.async_step_user(user_input)

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["title"] == "192.168.1.100"
        assert result["data"] == user_input


@pytest.mark.asyncio
async def test_async_step_user_connection_error(mock_config_flow):
    with patch(
        "custom_components.ccm15.api.CCM15ApiClient.async_get_status",
        new_callable=AsyncMock,
    ) as mock_get_status:
        mock_get_status.side_effect = Exception("Connection error")

        user_input = {
            CONF_HOST: "192.168.1.100",
            CONF_PORT: DEFAULT_PORT,
        }

        result = await mock_config_flow.async_step_user(user_input)

        assert result["type"] == FlowResultType.FORM
        assert result["errors"] == {"base": "connection"}
