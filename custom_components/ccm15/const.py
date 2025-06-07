"""Constants for ccm15 integration."""

import http
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ccm15"
ATTRIBUTION = "Data provided by Midea CCM-15 device."

CONF_HOST = "host"
CONF_PORT = "port"
DEFAULT_NAME = "Midea Thermostat"
DEFAULT_PORT = 80
DEFAULT_TIMEOUT = 5

# Constants for parsing binary data
BYTE_MASK_DEGREE_F = 0x01
BYTE_MASK_CTL = 0x1F
BYTE_MASK_HTL = 0x1F
BYTE_MASK_WIND = 0x07
BYTE_MASK_MODE = 0x03
BYTE_MASK_ERR = 0x3F
BYTE_SHIFT_MODE = 2
BYTE_SHIFT_FAN = 5
BYTE_SHIFT_ML = 1
BYTE_SHIFT_TEMP = 3
BYTE_TEMP_THRESHOLD = 128
HTTP_OK = http.HTTPStatus.OK

# Constants for locked mode
LOCKED_MODE_1 = 1
LOCKED_MODE_2 = 2
LOCKED_MODE_DEFAULT = -1
LOCKED_MODE_NONE = 10
