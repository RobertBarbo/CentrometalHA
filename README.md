# CentrometalHA - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/RobertBarbo/CentrometalHA.svg)](https://github.com/RobertBarbo/CentrometalHA/releases)
[![License](https://img.shields.io/github/license/RobertBarbo/CentrometalHA.svg)](LICENSE)

Custom Home Assistant integration for Centrometal boilers with WiFi Box module. Provides complete control and monitoring of your Centrometal pellet boiler through Home Assistant.

## Features

### Real-time MQTT Updates
- Subscribes directly to Centrometal MQTT broker
- Instant status updates (no polling delay)
- All MQTT parameters available as sensors

### Complete Sensor Coverage

**Temperature Sensors (17 total):**
- Boiler Temperature (`B_Tk1`)
- Hot Water Temperature (`B_Tptv1`)
- Outdoor Temperature (`B_Tva1`)
- Buffer Tank Up/Down (`B_Tak1`, `B_Tak2`)
- Flue Gas Temperature (`B_Tdpl1`)
- Hydraulic Crossover (`B_Ths1`)
- Mixer Temperature (`B_Tpov1`)
- Low Temperature Sensor (`B_Tlo1`)
- Circuit 1/2 Temperatures (multiple sensors)
- Circuit 1/2 Room Temperatures

**Status Sensors:**
- Oxygen Level (`B_Oxy1`) - Lambda sensor %
- Fan State (`B_fan`) - RPM or ON/OFF
- Heater State (`B_gri`)
- Boiler Pump (`B_Pk`)
- Pellet Transporter (`B_puz`)
- Circuit 1/2 ON/OFF states
- Freeze Guard status
- Remote Start Enabled
- Day/Night modes

**Counter Sensors (16 total):**
- Burner Work Time (`CNT_0`)
- DHW Only Time (`CNT_1`)
- Freeze Protection Time (`CNT_2`)
- Burner Start Count (`CNT_3`)
- Fan Work Time (`CNT_4`)
- Electric Heater Work Time (`CNT_5`)
- Electric Heater Starts (`CNT_6`)
- Vacuum Turbine Work Time (`CNT_7`)
- Boiler Pump Work Time (`CNT_8`)
- And more counters (`CNT_9` - `CNT_15`)

**Additional Sensors:**
- Pellet Tank Level
- Fire Sensor
- Mixing Valve
- Circuit Corrections
- Pellet Transporter Timing

**Status Information:**
- Boiler State (OFF, PP3, S7-2, etc.)
- Product Name
- Brand
- Nominal Power
- WiFi Version
- Firmware Version
- Configuration
- Operation Mode

### Climate Control
- Climate entity for boiler control
- Turn boiler ON/OFF
- Shows current temperature
- HVAC modes: OFF, HEAT

### Easy Configuration
- Configuration via Home Assistant UI
- No YAML configuration required
- Automatic portal authentication
- Stores credentials securely

## Supported Devices

- **Centrometal BioTec-L** - Biomass pellet boiler
- **Centrometal Cm Pelet-set** - Pellet boiler
- **Other Centrometal boilers** with WiFi Box module

All devices using Centrometal WiFi Box (ESP32-based) with MQTT connectivity are supported.

## Installation

### Method 1: HACS (Recommended)

1. **Add Custom Repository:**
   - Open HACS in Home Assistant
   - Go to "Integrations"
   - Click the three dots (⋮) in the top right corner
   - Select "Custom repositories"
   - Add repository URL: `https://github.com/RobertBarbo/CentrometalHA`
   - Category: "Integration"
   - Click "Add"

2. **Install Integration:**
   - Search for "CentrometalHA" in HACS
   - Click "Download"
   - Restart Home Assistant

3. **Configure:**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "CentrometalHA"
   - Follow setup wizard

### Method 2: Manual Installation

1. **Download Integration:**
   ```bash
   cd /config
   mkdir -p custom_components
   cd custom_components
   git clone https://github.com/RobertBarbo/CentrometalHA centrometal
   ```

2. **Restart Home Assistant**

3. **Configure:**
   - Settings → Devices & Services → Add Integration → CentrometalHA

## Configuration

### Setup via UI

1. Navigate to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"CentrometalHA"**
4. Enter your credentials:
   - **Email:** Your portal.centrometal.hr login email
   - **Password:** Your portal password
   - **Installation ID:** Your installation ID (see below)

### Finding Your Installation ID

Your Installation ID is required to identify your boiler on the portal.

**Method 1: Browser Developer Tools**
1. Login to https://portal.centrometal.hr
2. Open Developer Tools (F12)
3. Go to **Network** tab
4. Refresh the page
5. Find `/api/inst/list` request
6. In the response, find your installation's `id` field

Example response:
```json
[
  {
    "id": "1844",  ← This is your Installation ID
    "name": "My Boiler",
    "device_id": "AD53C83A",
    ...
  }
]
```

**Method 2: URL**
1. Login to portal
2. Look at the URL when viewing your boiler
3. The ID is in the URL: `portal.centrometal.hr/installation/1844`

## Entities

After successful configuration, the integration creates the following entities:

### Climate Entity
```
climate.centrometal_boiler_1844
```
- **Features:** Turn ON/OFF, view current temperature
- **HVAC Modes:** OFF, HEAT
- **Services:** `climate.turn_on`, `climate.turn_off`, `climate.set_hvac_mode`

### Sensor Entities

All sensors follow the naming pattern: `sensor.centrometal_<name>`

**Temperature Sensors:**
- `sensor.centrometal_boiler_temperature`
- `sensor.centrometal_hot_water_temperature`
- `sensor.centrometal_outdoor_temperature`
- `sensor.centrometal_buffer_tank_up`
- `sensor.centrometal_buffer_tank_down`
- `sensor.centrometal_flue_gas_temperature`
- `sensor.centrometal_hydraulic_crossover`
- `sensor.centrometal_mixer_temperature`
- `sensor.centrometal_low_temp_sensor`
- `sensor.centrometal_circuit1_temperature`
- `sensor.centrometal_circuit2_temperature`
- And more...

**Status Sensors:**
- `sensor.centrometal_oxygen_level`
- `sensor.centrometal_fan_state`
- `sensor.centrometal_heater_state`
- `sensor.centrometal_boiler_pump`
- `sensor.centrometal_pellet_transporter`
- `sensor.centrometal_boiler_status` (with extensive attributes)

**Counter Sensors:**
- `sensor.centrometal_cnt_burner_work`
- `sensor.centrometal_cnt_burner_starts`
- `sensor.centrometal_cnt_fan_work`
- And 13 more counters...

## Usage Examples

### Lovelace Cards

**Thermostat Card:**
```yaml
type: thermostat
entity: climate.centrometal_boiler_1844
name: Centrometal Boiler
```

**Entities Card:**
```yaml
type: entities
title: Centrometal Boiler
entities:
  - entity: climate.centrometal_boiler_1844
    name: Boiler Control
  - type: section
    label: Temperatures
  - entity: sensor.centrometal_boiler_temperature
    name: Boiler
  - entity: sensor.centrometal_hot_water_temperature
    name: Hot Water
  - entity: sensor.centrometal_outdoor_temperature
    name: Outdoor
  - entity: sensor.centrometal_flue_gas_temperature
    name: Flue Gas
  - type: section
    label: Status
  - entity: sensor.centrometal_oxygen_level
    name: Oxygen Level
  - entity: sensor.centrometal_fan_state
    name: Fan
  - entity: sensor.centrometal_boiler_status
    name: State
  - type: section
    label: Counters
  - entity: sensor.centrometal_cnt_burner_work
    name: Burner Hours
  - entity: sensor.centrometal_cnt_burner_starts
    name: Burner Starts
```

**Gauge Card (Oxygen Level):**
```yaml
type: gauge
entity: sensor.centrometal_oxygen_level
name: Oxygen Level
min: 0
max: 20
severity:
  green: 0
  yellow: 12
  red: 15
```

### Automations

**Turn on boiler at 6 AM:**
```yaml
automation:
  - alias: "Boiler ON in morning"
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

**Turn off boiler at 10 PM:**
```yaml
automation:
  - alias: "Boiler OFF at night"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: climate.turn_off
      target:
        entity_id: climate.centrometal_boiler_1844
```

**Alert if oxygen level too high:**
```yaml
automation:
  - alias: "High oxygen alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.centrometal_oxygen_level
      above: 15
    action:
      service: notify.mobile_app_your_phone
      data:
        title: "Boiler Alert"
        message: "Oxygen level is {{ states('sensor.centrometal_oxygen_level') }}%"
        data:
          priority: high
```

**Temperature-based control:**
```yaml
automation:
  - alias: "Auto boiler based on outdoor temp"
    trigger:
      platform: numeric_state
      entity_id: sensor.centrometal_outdoor_temperature
      below: 10
    action:
      service: climate.turn_on
      target:
        entity_id: climate.centrometal_boiler_1844
```

**Notification when burner starts:**
```yaml
automation:
  - alias: "Burner started notification"
    trigger:
      platform: state
      entity_id: sensor.centrometal_heater_state
      to: "ON"
    action:
      service: notify.mobile_app_your_phone
      data:
        message: "Boiler burner has started"
```

## How It Works

The integration uses a hybrid approach:

### Control Commands (Portal API)
```
Home Assistant → Portal API → MQTT → WiFi Box → Boiler
```
- Commands (ON/OFF, REFRESH) sent via Centrometal portal API
- Portal generates valid MQTT signatures
- WiFi Box receives and executes commands

### Status Updates (MQTT)
```
Boiler → WiFi Box → MQTT → Home Assistant
```
- Real-time status via MQTT subscription
- No polling delay
- All parameters updated instantly

### Architecture Diagram
```
┌─────────────────────┐
│  Home Assistant     │
│  + Centrometal      │
│    Integration      │
└──────┬──────┬───────┘
       │      │
       │      │ MQTT Subscribe
       │      │ (Real-time status)
       │      ▼
       │  ┌─────────────────────┐
       │  │  MQTT Broker        │
       │  │  136.243.62.164     │
       │  └─────────┬───────────┘
       │            │
       │ API        │ MQTT
       │ Commands   │ Messages
       ▼            ▼
┌─────────────────────┐
│  Centrometal Portal │
│  portal.centrometal │
│  .hr                │
└──────────┬──────────┘
           │
           │ MQTT (signed)
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

## Troubleshooting

### Integration doesn't appear

1. **Check file location:**
   ```bash
   ls -la /config/custom_components/centrometal/
   ```
   Should contain: `__init__.py`, `manifest.json`, etc.

2. **Check logs:**
   ```bash
   grep centrometal /config/home-assistant.log
   ```

3. **Restart Home Assistant**

### Login fails

1. **Verify credentials:**
   - Test login at https://portal.centrometal.hr
   - Check email and password

2. **Check Installation ID:**
   - Verify ID from portal API or URL

3. **Check logs:**
   Settings → System → Logs

### Entities don't update

1. **Check MQTT connection:**
   - Integration logs should show "Connected to MQTT broker"
   - Check internet connectivity

2. **Verify device ID:**
   - Integration uses device ID from portal
   - Check logs for MQTT subscription topic

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.centrometal: debug
    paho.mqtt: debug
```

Restart Home Assistant and check logs at Settings → System → Logs.

## Advanced Configuration

### Multiple Boilers

The integration supports multiple installations. Add each one separately:

1. Add Integration
2. Enter credentials for first installation
3. Repeat for additional installations

Each will create separate entities with unique IDs.

### Custom Device ID

By default, the integration uses a placeholder device ID. To use your specific device ID:

Edit `/config/custom_components/centrometal/__init__.py` and update:
```python
self.device_id = "YOUR_DEVICE_ID"  # Replace with your actual device ID
```

Find your device ID from MQTT traffic or portal API response.

## Technical Details

### MQTT Topics

**Device → Server (Status):**
```
cm.inst.biotec.{DEVICE_ID}
```
Example: `cm.inst.biotec.AD53C83A`

**Server → Device (Commands):**
```
cm/srv/biotec/{DEVICE_ID}
```
Example: `cm/srv/biotec/AD53C83A`

### MQTT Broker
- **Host:** 136.243.62.164 (web-boiler.com)
- **Port:** 1883 (plaintext MQTT)
- **Username:** appuser
- **Password:** appuser
- **Protocol:** MQTT v3.1

### Portal API
- **Base URL:** https://portal.centrometal.hr
- **Authentication:** Session-based (PHPSESSID)
- **Commands:** `/api/inst/control/multiple`

### Command Format

**Turn ON:**
```json
{"PWR 99": 1, "srvMsgId": 123456, "_sign": "..."}
```

**Turn OFF:**
```json
{"PWR 99": 0, "srvMsgId": 123457, "_sign": "..."}
```

**Refresh Status:**
```json
{"REFRESH": 0, "srvMsgId": 123458, "_sign": "..."}
```

Signatures (`_sign`) are generated by the portal API.

## Known Limitations

1. **Device ID mapping:** Currently uses placeholder device ID
2. **Internet required:** Requires connection to Centrometal portal and MQTT broker
3. **Read-only counters:** Counter values are read-only
4. **No temperature setpoint:** Only ON/OFF control (temperature setpoint control can be added)

## Future Enhancements

- [ ] Automatic device ID detection from portal
- [ ] Temperature setpoint control (`PWR 3`)
- [ ] Additional command support
- [ ] Energy consumption tracking
- [ ] Historical data charts
- [ ] Local MQTT broker support
- [ ] Offline mode (local control)

## Contributing

Contributions are welcome! Please open an issue or pull request on GitHub.

## Support

- **Issues:** [GitHub Issues](https://github.com/RobertBarbo/CentrometalHA/issues)
- **Discussions:** [GitHub Discussions](https://github.com/RobertBarbo/CentrometalHA/discussions)

## Credits

- Based on reverse engineering of Centrometal WiFi Box MQTT protocol
- Inspired by existing Centrometal integrations
- Built with Home Assistant integration best practices

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Disclaimer

**This is an unofficial custom integration.**

- Use at your own risk
- Not affiliated with or endorsed by Centrometal
- May stop working if Centrometal changes their API/MQTT protocol
- No warranty or support from Centrometal

---

**Made with ❤️ for the Home Assistant community**

If you find this integration useful, consider starring the repository on GitHub!
