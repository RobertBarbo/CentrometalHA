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

### Control Features

**Switches:**
- 1st Heating Circuit (PWR 99) - ON/OFF control
- 2nd Heating Circuit (PWR 129) - ON/OFF control

**Number Controls:**
- Boiler Temperature Setpoint (PWR 3) - 75-90°C
- DHW (Domestic Hot Water) Temperature (PWR 10) - 40-80°C
- Day Room Temperature 2nd Circuit (PWR 140) - 5-30°C

All control values are automatically synchronized with portal

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
   - **Device ID:** Your WiFi Box device ID (see below)

### Finding Your Device ID

Your Device ID is the unique identifier of your WiFi Box (ESP32 module). This is required for MQTT communication.

**Method 1: MQTT Monitoring (Recommended)**
1. Install mosquitto-clients: `sudo apt-get install mosquitto-clients`
2. Run this command and wait for your boiler to send data:
   ```bash
   mosquitto_sub -h 136.243.62.164 -p 1883 -u appuser -P appuser -t 'cm/inst/biotec/#' -v
   ```
3. You'll see messages like: `cm/inst/biotec/AD53C83A {"B_Tk1":68.3,...}`
4. The Device ID is the part after `cm/inst/biotec/` (e.g., `AD53C83A`)

**Method 2: Portal API (Advanced)**
1. Login to https://portal.centrometal.hr
2. Open Developer Tools (F12) → Network tab
3. Refresh the page
4. Find API requests to `/api/inst/list` or `/api/inst/status`
5. In the response, look for `device_id` field

**Method 3: WiFi Box Label**
1. Check the WiFi Box module on your boiler
2. The MAC address or device ID may be printed on a label
3. It's usually 8 hexadecimal characters (e.g., AD53C83A)

**Method 4: Mobile App**
1. If you use the Centrometal mobile app
2. The device ID may be visible in device settings or details

## Entities

After successful configuration, the integration creates the following entities:

### Switch Entities
```
switch.centrometal_1st_heating_circuit    # PWR 99
switch.centrometal_2nd_heating_circuit    # PWR 129
```
- **Features:** Turn heating circuits ON/OFF
- **Services:** `switch.turn_on`, `switch.turn_off`, `switch.toggle`

### Number Entities
```
number.centrometal_boiler_temperature                      # PWR 3 (75-90°C)
number.centrometal_dhw_temperature                         # PWR 10 (40-80°C)
number.centrometal_day_room_temperature_2nd_circuit        # PWR 140 (5-30°C)
```
- **Features:** Set temperature setpoints
- **Services:** `number.set_value`
- **Auto-sync:** Values automatically pulled from portal every minute

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

**Entities Card with Controls:**
```yaml
type: entities
title: Centrometal Boiler Control
entities:
  - entity: switch.centrometal_1st_heating_circuit
    name: 1st Heating Circuit
  - entity: switch.centrometal_2nd_heating_circuit
    name: 2nd Heating Circuit
  - type: section
    label: Temperature Setpoints
  - entity: number.centrometal_boiler_temperature
    name: Boiler Temperature
  - entity: number.centrometal_dhw_temperature
    name: Hot Water Temperature
  - entity: number.centrometal_day_room_temperature_2nd_circuit
    name: Room Temperature (2nd Circuit)
```

**Entities Card with Sensors:**
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

**Turn on heating circuit at 6 AM:**
```yaml
automation:
  - alias: "1st Heating Circuit ON in morning"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      service: switch.turn_on
      target:
        entity_id: switch.centrometal_1st_heating_circuit
```

**Turn off heating circuit at 10 PM:**
```yaml
automation:
  - alias: "1st Heating Circuit OFF at night"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: switch.turn_off
      target:
        entity_id: switch.centrometal_1st_heating_circuit
```

**Adjust boiler temperature based on outdoor temp:**
```yaml
automation:
  - alias: "Adjust boiler temp for cold weather"
    trigger:
      platform: numeric_state
      entity_id: sensor.centrometal_outdoor_temperature
      below: 0
    action:
      service: number.set_value
      target:
        entity_id: number.centrometal_boiler_temperature
      data:
        value: 90
```

**Set DHW temperature in morning:**
```yaml
automation:
  - alias: "Higher DHW temperature in morning"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      service: number.set_value
      target:
        entity_id: number.centrometal_dhw_temperature
      data:
        value: 60
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
- Commands (switches, number setpoints) sent via Centrometal portal API
- Portal generates valid MQTT signatures
- WiFi Box receives and executes commands

### Status Updates (MQTT)
```
Boiler → WiFi Box → MQTT → Home Assistant
```
- Real-time sensor status via MQTT subscription
- No polling delay
- All sensor parameters updated instantly

### Parameters Sync (Portal API)
```
Portal API → Home Assistant (every 60 seconds)
```
- Number control values (PVAL_*) pulled from portal
- Ensures setpoints are always synchronized
- No more "unknown" states on startup

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

## Technical Details

### MQTT Topics

**Device → Server (Status):**
```
cm/inst/biotec/{DEVICE_ID}
```
Example: `cm/inst/biotec/AD53C83A`

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

1. **Internet required:** Requires connection to Centrometal portal and MQTT broker
2. **Read-only counters:** Counter values are read-only (cannot be reset)
3. **Portal dependency:** All control commands require portal authentication

## Future Enhancements

- [ ] Automatic device ID detection from portal
- [ ] Additional command support (more PWR parameters)
- [ ] Energy consumption tracking and statistics
- [ ] Historical data charts
- [ ] Local MQTT broker support
- [ ] Offline mode (local control without portal)

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
