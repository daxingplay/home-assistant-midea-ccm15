"""Async API client for CCM15."""

import xmltodict
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class CCM15ApiClient:
    def __init__(self, host, port, hass):
        self._host = host
        self._port = port
        self._base_url = f"http://{host}:{port}"
        self._hass = hass

    async def async_get_status(self):
        url = f"{self._base_url}/status.xml"
        session = async_get_clientsession(self._hass)
        async with session.get(url, timeout=10) as resp:
            text = await resp.text()
            data = xmltodict.parse(text)
            return data["response"]

    async def async_set_state(self, ac_id, mode, fan, temp):
        url = f"{self._base_url}/ctrl.xml?ac0={ac_id}&ac1=0&mode={mode}&fan={fan}&temp={temp}"
        session = async_get_clientsession(self._hass)
        async with session.get(url, timeout=10) as resp:
            return resp.status == 200
