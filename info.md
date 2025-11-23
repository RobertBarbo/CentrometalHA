# CentrometalHA

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/RobertBarbo/CentrometalHA.svg)](https://github.com/RobertBarbo/CentrometalHA/releases)
[![License](https://img.shields.io/github/license/RobertBarbo/CentrometalHA.svg)](LICENSE)

Custom Home Assistant integration for Centrometal boilers with WiFi Box module.

## Features

- **Real-time MQTT Updates** - Subscribe to MQTT broker for instant status changes
- **Complete Sensor Coverage** - All MQTT parameters exposed as sensors:
  - 17 Temperature sensors (boiler, hot water, outdoor, circuits, etc.)
  - Oxygen level sensor
  - 13 Binary state sensors (pumps, fans, circuits)
  - 16 Counter sensors (work time, start counts)
  - Additional sensors (pellet level, fire sensor, mixing valve)
- **Climate Control** - Turn boiler ON/OFF via climate entity
- **Configuration UI** - Easy setup via Home Assistant UI
- **Automatic Portal Login** - Handles authentication automatically

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

1. Copy the `custom_components/centrometal` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Centrometal Boiler"
4. Enter your credentials:
   - **Email**: Your portal.centrometal.hr email
   - **Password**: Your portal password
   - **Installation ID**: Your installation ID

### Finding Your Installation ID

1. Login to https://portal.centrometal.hr
2. Open browser Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Look for `/api/inst/list` request
6. In the response, find your installation's `id` field

## Entities

After configuration, you'll get:

### Climate
- `climate.centrometal_boiler_XXXX` - Boiler control (ON/OFF)

### Temperature Sensors
- Boiler Temperature
- Hot Water Temperature
- Outdoor Temperature
- Buffer Tank Up/Down
- Flue Gas Temperature
- Hydraulic Crossover
- Mixer Temperature
- Circuit 1/2 Temperatures
- Room Temperatures

### Status Sensors
- Oxygen Level
- Fan State
- Heater State
- Boiler Pump
- Circuit ON/OFF states
- Freeze Guard
- Remote Start Enabled

### Counter Sensors
- Burner Work Time
- DHW Only Time
- Fan Work Time
- Electric Heater Work Time
- Burner Start Count
- And more...

### Additional Sensors
- Pellet Tank Level
- Fire Sensor
- Mixing Valve
- Circuit Corrections
- Pellet Transporter Timing

## Usage Examples

See the [README](https://github.com/RobertBarbo/CentrometalHA/blob/main/README.md) for automation examples and Lovelace card configurations.

## How It Works

The integration uses two methods:
1. **Portal API** - For sending commands (ON/OFF)
2. **MQTT Subscription** - For real-time status updates

```
Portal API → Commands → Boiler
MQTT Broker ← Status ← Boiler → Real-time updates → Home Assistant
```

## Troubleshooting

Enable debug logging:

```yaml
logger:
  default: info
  logs:
    custom_components.centrometal: debug
```

## Support

For issues and feature requests, please open an issue on [GitHub](https://github.com/RobertBarbo/CentrometalHA/issues).

## Disclaimer

This is an unofficial custom integration. Use at your own risk. Not affiliated with or endorsed by Centrometal.
