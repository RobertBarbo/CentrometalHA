"""Constants for the Centrometal integration."""

DOMAIN = "centrometal"

# Configuration
CONF_INSTALL_ID = "install_id"

# Portal API
PORTAL_URL = "https://portal.centrometal.hr"
LOGIN_PAGE = PORTAL_URL + "/login"
LOGIN_POST = PORTAL_URL + "/login_check"
API_CONTROL = PORTAL_URL + "/api/inst/control/multiple"

# MQTT (for monitoring - optional)
MQTT_BROKER = "136.243.62.164"
MQTT_PORT = 1883
MQTT_USER = "appuser"
MQTT_PASS = "appuser"
