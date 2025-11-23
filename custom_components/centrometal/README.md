# Centrometal Boiler Integration for Home Assistant

Custom Home Assistant integration for Centrometal boilers with WiFi Box module.

## Features

- ✅ Climate entity (thermostat) - Turn boiler ON/OFF
- ✅ Temperature sensors (boiler, hot water, outdoor)
- ✅ Oxygen level sensor
- ✅ Boiler status sensor with attributes
- ✅ Configuration via UI (Config Flow)
- ✅ Automatic portal login and session management

## Supported Devices

- Centrometal BioTec-L
- Centrometal Cm Pelet-set
- Other Centrometal boilers with WiFi Box module

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL
6. Select "Integration" as the category
7. Click "Add"
8. Find "Centrometal Boiler" in HACS and install it
9. Restart Home Assistant

### Manual Installation

1. Copy the `centrometal` folder to your `custom_components` directory:

```bash
# On your Home Assistant server
cd /config
mkdir -p custom_components
cd custom_components

# Copy the integration
cp -r /root/homeassistant/custom_components/centrometal ./
```

2. Restart Home Assistant

3. Go to Configuration → Integrations

4. Click "+ Add Integration"

5. Search for "Centrometal"

## Configuration

### Via UI (Recommended)

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Centrometal Boiler"
4. Enter your credentials:
   - **Email**: Your portal.centrometal.hr email
   - **Password**: Your portal password
   - **Installation ID**: Your installation ID (default: 1844)

### Finding Your Installation ID

1. Login to https://portal.centrometal.hr
2. Open browser Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Look for `/api/inst/list` request
6. In the response, find your installation's `id` field

Example:
```json
[
  {
    "id": "1844",  ← This is your Installation ID
    "name": "My Boiler",
    ...
  }
]
```

## Entities

After configuration, the following entities will be created:

### Climate

- **climate.centrometal_boiler_1844**
  - Turn boiler ON/OFF
  - Shows current state (OFF/HEAT)
  - Shows current temperature (if available)

### Sensors

- **sensor.centrometal_boiler_temperature**
  - Boiler temperature (°C)

- **sensor.centrometal_hot_water_temperature**
  - Domestic hot water temperature (°C)

- **sensor.centrometal_outdoor_temperature**
  - Outdoor temperature sensor (°C)

- **sensor.centrometal_oxygen_level**
  - Lambda sensor oxygen level (%)

- **sensor.centrometal_boiler_status**
  - Current boiler state (OFF, GLW2, PP3, etc.)
  - Attributes:
    - Product name
    - Power rating
    - WiFi firmware version
    - Boiler firmware version

## Usage Examples

### Automations

#### Turn on boiler at 6 AM

```yaml
automation:
  - alias: "Turn on boiler in the morning"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      service: climate.set_hvac_mode
      target:
        entity_id: climate.centrometal_boiler_1844
      data:
        hvac_mode: heat
```

#### Turn off boiler at 10 PM

```yaml
automation:
  - alias: "Turn off boiler at night"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: climate.turn_off
      target:
        entity_id: climate.centrometal_boiler_1844
```

#### Alert if oxygen level is too high

```yaml
automation:
  - alias: "Oxygen level alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.centrometal_oxygen_level
      above: 15
    action:
      service: notify.mobile_app
      data:
        message: "Boiler oxygen level is {{ states('sensor.centrometal_oxygen_level') }}%"
```

### Lovelace Card

```yaml
type: thermostat
entity: climate.centrometal_boiler_1844
name: Centrometal Boiler
```

Or use entities card:

```yaml
type: entities
title: Centrometal Boiler
entities:
  - entity: climate.centrometal_boiler_1844
    name: Boiler Control
  - entity: sensor.centrometal_boiler_temperature
    name: Boiler Temperature
  - entity: sensor.centrometal_hot_water_temperature
    name: Hot Water
  - entity: sensor.centrometal_oxygen_level
    name: Oxygen Level
  - entity: sensor.centrometal_boiler_status
    name: Status
```

## How It Works

```
┌─────────────────────┐
│  Home Assistant     │
│  + Centrometal      │
│    Integration      │
└──────────┬──────────┘
           │
           │ HTTPS
           ▼
┌─────────────────────┐
│  Centrometal Portal │
│  portal.centrometal │
│  .hr                │
└──────────┬──────────┘
           │
           │ MQTT
           ▼
┌─────────────────────┐
│  CM WiFi Box        │
│  (ESP32)            │
└──────────┬──────────┘
           │
           │ RS485
           ▼
┌─────────────────────┐
│  Boiler Controller  │
└─────────────────────┘
```

The integration:
1. Logs into the Centrometal portal with your credentials
2. Sends commands via the portal API
3. Portal generates valid signatures and publishes to MQTT
4. WiFi Box receives commands and controls the boiler

## Troubleshooting

### Integration doesn't show up

- Make sure you've restarted Home Assistant after copying files
- Check `custom_components/centrometal/manifest.json` exists
- Check Home Assistant logs for errors

### Login fails

- Verify your email and password at https://portal.centrometal.hr
- Check your internet connection
- Check Home Assistant logs for details

### Entities don't update

- The integration polls every 30 seconds
- Check if portal is accessible
- Check Home Assistant logs

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.centrometal: debug
```

Restart Home Assistant and check the logs.

## Known Limitations

1. **No real-time status updates**: The integration uses portal API polling. For real-time updates, MQTT subscription would be needed (future enhancement).

2. **Internet required**: Integration requires internet access to communicate with Centrometal portal.

3. **Temperature control**: Currently only ON/OFF control is implemented. Temperature setpoint control can be added in future versions.

## Future Enhancements

- [ ] MQTT integration for real-time status updates
- [ ] Temperature setpoint control (PWR 3)
- [ ] More sensors (all available parameters from MQTT)
- [ ] Services for custom commands
- [ ] Energy consumption tracking
- [ ] Historical data charts

## Support

For issues and feature requests, please open an issue on GitHub.

## Credits

Based on reverse engineering of Centrometal WiFi Box MQTT protocol.

## License

MIT License - See LICENSE file for details

---

**Disclaimer**: This is an unofficial custom integration. Use at your own risk. Not affiliated with or endorsed by Centrometal.
