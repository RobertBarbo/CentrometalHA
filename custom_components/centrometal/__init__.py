"""Centrometal Boiler Integration for Home Assistant."""
import asyncio
import json
import logging
from datetime import timedelta

import paho.mqtt.client as mqtt

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CentrometalAPI
from .const import DOMAIN, MQTT_BROKER, MQTT_PASS, MQTT_PORT, MQTT_USER, DEFAULT_INSTALL_ID

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.SWITCH, Platform.NUMBER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Centrometal from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]
    install_id = entry.data.get("install_id", DEFAULT_INSTALL_ID)  # Default: 1844 (same for all)
    device_id = entry.data.get("device_id", "AD53C83A")  # Fallback for existing configs

    # Create API instance
    api = CentrometalAPI(email, password, install_id)

    # Create MQTT client and coordinator
    mqtt_client = CentrometalMQTTClient(hass, install_id, device_id)
    coordinator = CentrometalDataUpdateCoordinator(hass, api, mqtt_client)

    # Start MQTT client
    await hass.async_add_executor_job(mqtt_client.start)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Stop MQTT client
    if coordinator.mqtt_client:
        await hass.async_add_executor_job(coordinator.mqtt_client.stop)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class CentrometalMQTTClient:
    """MQTT client for real-time boiler status updates."""

    def __init__(self, hass: HomeAssistant, install_id: str, device_id: str):
        """Initialize MQTT client."""
        self.hass = hass
        self.install_id = install_id
        self.device_id = device_id
        self.client = None
        self.data = {}
        self._connected = False

        # MQTT topics based on device ID
        self.topic_device_status = f"cm/inst/biotec/{self.device_id}"
        self.topic_server_commands = f"cm/srv/biotec/{self.device_id}"

    def start(self):
        """Start MQTT client."""
        try:
            # paho-mqtt 2.x requires callback API version
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
            self.client.username_pw_set(MQTT_USER, MQTT_PASS)
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.on_disconnect = self._on_disconnect

            _LOGGER.info("Connecting to MQTT broker %s:%s", MQTT_BROKER, MQTT_PORT)
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as err:
            _LOGGER.error("Failed to connect to MQTT broker: %s", err)

    def stop(self):
        """Stop MQTT client."""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            _LOGGER.info("MQTT client disconnected")

    def _on_connect(self, client, userdata, flags, rc):
        """Handle MQTT connection."""
        if rc == 0:
            _LOGGER.info("Connected to MQTT broker successfully")
            self._connected = True
            # Subscribe to device status topic
            result = client.subscribe(self.topic_device_status)
            _LOGGER.info("Subscribed to topic: %s (result: %s)", self.topic_device_status, result)
        else:
            _LOGGER.error("Failed to connect to MQTT broker, return code %d", rc)

    def _on_disconnect(self, client, userdata, rc):
        """Handle MQTT disconnection."""
        self._connected = False
        if rc != 0:
            _LOGGER.warning("Unexpected MQTT disconnection. Will auto-reconnect")

    def _on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages."""
        try:
            payload = json.loads(msg.payload.decode())
            _LOGGER.info("MQTT message received on %s with %d fields", msg.topic, len(payload))
            _LOGGER.debug("MQTT payload: %s", payload)

            # Update data dictionary with new values
            self.data.update(payload)
            _LOGGER.debug("Total data fields after update: %d", len(self.data))

            # Notify Home Assistant about data update
            self.hass.loop.call_soon_threadsafe(self._notify_update)
        except json.JSONDecodeError as err:
            _LOGGER.error("Failed to decode MQTT message: %s (payload: %s)", err, msg.payload)
        except Exception as err:
            _LOGGER.error("Error processing MQTT message: %s", err, exc_info=True)

    def _notify_update(self):
        """Notify coordinator about data update."""
        # This will be called when new MQTT data arrives
        # The coordinator will handle updating entities
        pass


class CentrometalDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Centrometal data."""

    def __init__(self, hass: HomeAssistant, api: CentrometalAPI, mqtt_client: CentrometalMQTTClient):
        """Initialize."""
        self.api = api
        self.mqtt_client = mqtt_client

        # Link coordinator to MQTT client for updates
        mqtt_client._notify_update = self._handle_mqtt_update

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),  # Less frequent polling since we have MQTT
        )

    def _handle_mqtt_update(self):
        """Handle MQTT data update."""
        # Merge MQTT data with existing coordinator data (preserves PVAL values)
        combined_data = dict(self.data) if self.data else {}
        combined_data.update(self.mqtt_client.data)
        self.async_set_updated_data(combined_data)

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # Request status refresh via API
            await self.api.send_command({"REFRESH": 0})

            # Get PVAL parameters from portal (for number controls)
            pval_data = await self.api.get_installation_status()

            # Merge MQTT data with PVAL data
            combined_data = {}
            if self.mqtt_client.data:
                combined_data.update(self.mqtt_client.data)

            # Add/update PVAL values from portal
            if pval_data:
                combined_data.update(pval_data)
                _LOGGER.debug("Combined MQTT data (%d keys) with PVAL data (%d keys)",
                             len(self.mqtt_client.data), len(pval_data))

            return combined_data if combined_data else {}

        except Exception as err:
            _LOGGER.warning("Error communicating with API: %s", err)
            # Even if API fails, return MQTT data if available
            return self.mqtt_client.data if self.mqtt_client.data else {}
