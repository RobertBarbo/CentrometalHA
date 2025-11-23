"""Constants for the Centrometal integration."""

DOMAIN = "centrometal"

# Configuration
CONF_DEVICE_ID = "device_id"

# Default installation ID (same for all users)
DEFAULT_INSTALL_ID = "1844"

# Portal API
PORTAL_URL = "https://portal.centrometal.hr"
LOGIN_PAGE = PORTAL_URL + "/login"
LOGIN_POST = PORTAL_URL + "/login_check"
API_CONTROL = PORTAL_URL + "/api/inst/control/multiple"
API_STATUS = PORTAL_URL + "/wdata/data/installation-status/{install_id}"

# MQTT (for monitoring - optional)
MQTT_BROKER = "136.243.62.164"
MQTT_PORT = 1883
MQTT_USER = "appuser"
MQTT_PASS = "appuser"
