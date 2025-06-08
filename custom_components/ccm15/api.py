"""Async API client for CCM15."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import aiohttp
import xmltodict
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    BYTE_MASK_CTL,
    BYTE_MASK_DEGREE_F,
    BYTE_MASK_ERR,
    BYTE_MASK_HTL,
    BYTE_MASK_MODE,
    BYTE_MASK_WIND,
    BYTE_SHIFT_FAN,
    BYTE_SHIFT_ML,
    BYTE_SHIFT_MODE,
    BYTE_SHIFT_TEMP,
    BYTE_TEMP_THRESHOLD,
    HTTP_OK,
    LOCKED_MODE_1,
    LOCKED_MODE_2,
    LOCKED_MODE_DEFAULT,
    LOCKED_MODE_NONE,
    LOGGER,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


class CCM15ApiClient:
    """
    API client for CCM15 device.

    Handles communication with a CCM15 device, including status retrieval
    and state updates.
    """

    def __init__(self, host: str, port: int, hass: HomeAssistant) -> None:
        """
        Initialize the API client.

        Args:
            host: The IP address or hostname of the CCM15 device.
            port: The port number of the CCM15 device.
            hass: The Home Assistant instance.

        """
        self._host = host
        self._port = port
        self._base_url = f"http://{host}:{port}"
        self._hass = hass

    def _get_status_from(self, s: str) -> dict[str, Any] | None:
        """
        Parse binary data from the device.

        Args:
            s: The binary data string from the device.

        Returns:
            A dictionary containing the parsed AC state, or None if parsing fails.

        """
        if s == "-":
            return None

        bytesarr = bytes.fromhex(s.strip(","))

        # Parse first byte
        buf = bytesarr[0]
        is_degree_f = buf & BYTE_MASK_DEGREE_F
        ctl = (buf >> 3) & BYTE_MASK_CTL

        # Parse second byte
        buf = bytesarr[1]
        htl = buf & BYTE_MASK_HTL
        locked_wind = (buf >> 5) & BYTE_MASK_WIND

        # Parse third byte
        buf = bytesarr[2]
        locked_mode = buf & BYTE_MASK_MODE
        err = (buf >> 2) & BYTE_MASK_ERR

        # Convert locked_mode
        if locked_mode == LOCKED_MODE_1:
            locked_mode = 0
        elif locked_mode == LOCKED_MODE_2:
            locked_mode = 1
        else:
            locked_mode = LOCKED_MODE_DEFAULT

        # Parse fourth byte
        buf = bytesarr[3]
        mode = (buf >> BYTE_SHIFT_MODE) & 7
        fan = (buf >> BYTE_SHIFT_FAN) & 7
        ml = 1 if ((buf >> BYTE_SHIFT_ML) & 1) != 0 else 0

        # Parse fifth byte
        buf = bytesarr[4]
        settemp = (buf >> BYTE_SHIFT_TEMP) & BYTE_MASK_CTL
        if is_degree_f:
            settemp += 62
            ctl += 62
            htl += 62

        # Parse sixth byte
        buf = bytesarr[5]
        if ((buf >> 3) & 1) == 0:
            ctl = 0
        if ((buf >> 4) & 1) == 0:
            htl = 0
        fl = 0 if ((buf >> 5) & 1) == 0 else 1
        rml = 1 if ((buf >> 6) & 1) != 0 else 0

        # Parse seventh byte
        buf = bytesarr[6]
        temp = buf if buf < BYTE_TEMP_THRESHOLD else buf - 256

        # Determine locked state
        is_locked = ml == 1 or fl == 1 or ctl > 0 or htl > 0 or rml == 1

        return {
            "ac_mode": mode,
            "fan": fan,
            "current_temperature": temp,
            "settemp": settemp,
            "err": err,
            "locked": 1 if is_locked else 0,
            "l_rm": rml,
            "l_mode": LOCKED_MODE_NONE if ml == 0 else locked_mode,
            "l_wind": LOCKED_MODE_NONE if fl == 0 else locked_wind,
            "l_cool_temp": ctl,
            "l_heat_temp": htl,
        }

    async def async_get_status(self) -> dict[str, dict[str, Any]]:
        """
        Get the status of all AC units.

        Returns:
            A dictionary mapping AC names to their states.

        """
        url = f"{self._base_url}/status.xml"
        session = async_get_clientsession(self._hass)
        timeout = aiohttp.ClientTimeout(total=10)

        async with session.get(url, timeout=timeout) as resp:
            text = await resp.text()
            data = xmltodict.parse(text)
            response_data = data["response"]

            acs = {}
            for ac_name, ac_binary in response_data.items():
                if len(ac_binary) > 1:
                    ac_state = self._get_status_from(ac_binary)
                    if ac_state:
                        acs[ac_name] = ac_state
                        LOGGER.debug("Parsed AC state for %s: %s", ac_name, ac_state)

            return acs

    async def async_set_state(
        self,
        ac_id: int,
        mode: int,
        fan: int,
        temp: int,
    ) -> bool:
        """
        Set the state of an AC unit.

        Args:
            ac_id: The ID of the AC unit.
            mode: The HVAC mode to set.
            fan: The fan mode to set.
            temp: The target temperature to set.

        Returns:
            True if the state was set successfully, False otherwise.

        """
        params = f"ac0={ac_id}&ac1=0&mode={mode}&fan={fan}&temp={temp}"
        url = f"{self._base_url}/ctrl.xml?{params}"
        LOGGER.debug(
            "Setting state for AC %d: mode=%d, fan=%d, temp=%d", ac_id, mode, fan, temp
        )
        session = async_get_clientsession(self._hass)
        timeout = aiohttp.ClientTimeout(total=10)

        async with session.get(url, timeout=timeout) as resp:
            return resp.status == HTTP_OK
