"""Constants for ccm15 integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ccm15"
ATTRIBUTION = "Data provided by Midea CCM-15 device."

CONF_HOST = "host"
CONF_PORT = "port"
DEFAULT_NAME = "Midea Thermostat"
DEFAULT_PORT = 80
DEFAULT_TIMEOUT = 5 