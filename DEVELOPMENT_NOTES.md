# Centrometal Home Assistant Integration - Development Notes

**Zadnja posodobitev:** 23. November 2025 (10:57)
**Status:** ✅ Deluje (v razvoju)
**Verzija:** 1.1.0

---

## 📋 Pregled Projekta

Custom Home Assistant integracija za Centrometal pelete/biomass kotle z WiFi Box modulom (ESP32).

**Uporabnik:** robert.barbiric@gmail.com
**Device ID:** AD53C83A
**Install ID:** 1844 (hard-coded, globalen za vse uporabnike)
**Tip kotla:** BioTec-L (25kW)

---

## 🎯 Kaj Dela

### ✅ MQTT Monitoring (Real-time)
- Povezava na Centrometal MQTT broker (136.243.62.164:1883)
- Real-time posodabljanje vseh senzorjev
- Subscribe na topic: `cm/inst/biotec/AD53C83A`

### ✅ Sensors (50+ entitet)
- 17 temperature sensors
- 9 counter sensors (burner work, fan time, itd.)
- 25+ misc sensors (pumps, oxygen, corrections, itd.)
- 1 status sensor z attributes

### ✅ Control Switches
- **PWR 99** - 1st Heating Circuit ON/OFF
- **PWR 129** - 2nd Heating Circuit ON/OFF
- Ukazi se pošiljajo preko Portal API

### ✅ Number Controls (NEW!)
- **PWR 3** - Boiler Temperature Setpoint (75-90°C, korak 1°)
- **PWR 10** - DHW Temperature Setpoint (40-80°C, korak 1°)
- **PWR 140** - Day Room Temperature 2nd Circuit (5-30°C, korak 0.1°)
- Nastavitve se pošiljajo preko Portal API
- Vrednosti se avtomatsko pulljajo iz Portal API (vsako minuto)

---

## 🏗️ Struktura Datotek

```
custom_components/centrometal/
├── __init__.py                 # Main setup, MQTT client, Coordinator
├── manifest.json              # Integration metadata
├── const.py                   # Konstante (MQTT, API URLs)
├── config_flow.py             # UI konfiguracija
├── api.py                     # Portal API client
├── sensor.py                  # Sensor platform
├── sensor_definitions.py      # Friendly names za vse senzorje
├── switch.py                  # Switch platform (PWR 99, PWR 129)
├── number.py                  # Number platform (PWR 3, PWR 140) - NEW!
├── icon.png                   # Integration icon (256x256)
└── icon@2x.png                # Integration icon hi-res (512x512)
```

---

## 🔧 Konfiguracijski Parametri

**Uporabnik vnese (via UI):**
- Email: robert.barbiric@gmail.com
- Password: strom123
- Device ID: AD53C83A

**Hard-coded v kodi:**
- Install ID: "1844" (v `const.py` kot `DEFAULT_INSTALL_ID`)
- MQTT Broker: 136.243.62.164:1883
- MQTT Credentials: appuser / appuser

---

## 🔄 Kako Deluje

### MQTT Real-time Updates (Monitoring)
```
1. Home Assistant startup
2. __init__.py kreira MQTT client
3. MQTT client se poveže na broker (136.243.62.164:1883)
4. Subscribe na: cm/inst/biotec/{device_id}
5. Kotel pošilja MQTT sporočila (vsake par sekund)
6. MQTT client sprejme JSON: {"B_Tk1": 67.4, "B_fan": 0, ...}
7. Coordinator posodobi data
8. Vsi senzorji se posodobijo
```

### Portal API Control (Commands)
```
1. Uporabnik klikne switch v HA
2. switch.py kliče coordinator.api.send_command({"PWR 99": 1})
3. api.py se prijavi na portal (CSRF token + session)
4. Pošlje POST /api/inst/control/multiple:
   {"messages": {"1844": {"PWR 99": 1}}}
5. Portal backend generira _sign podpis
6. Portal pošlje MQTT sporočilo na broker
7. Broker posreduje na topic: cm/srv/biotec/AD53C83A
8. Kotel sprejme ukaz (preverja _sign) in izvede
9. Kotel pošlje novo stanje nazaj preko MQTT
10. HA senzorji se posodobijo
```

### Portal API Parameters Pull (Number Controls)
```
1. Coordinator periodic update (vsako minuto)
2. api.py kliče get_installation_status()
3. GET /wdata/data/installation-status/{install_id}
4. Portal vrne JSON z "params" sekcijo:
   {"PVAL_3_0": {"v": "90", "ut": "..."}, ...}
5. api.py izlušči vse PVAL_* vrednosti
6. Coordinator merge-a PVAL vrednosti z MQTT podatki
7. Number entitete imajo vedno aktualne vrednosti
```

**Prednost:** Number entitete niso več "unknown" ob startupu!

---

## 🐛 Popravljene Kritične Napake

### 1. MQTT Topic (GLAVNA NAPAKA!)
```python
# PREJ (NAPAČNO):
topic = f"cm.inst.biotec.{device_id}"  # ❌ PIKA

# ZDAJ (PRAVILNO):
topic = f"cm/inst/biotec/{device_id}"  # ✅ SLASH
```
**Razlog:** Subscribe na napačen topic → nobeni podatki niso prihajali!

### 2. MQTT Credentials
```python
# PREJ:
username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  # ❌ Ne obstajata

# ZDAJ:
username_pw_set(MQTT_USER, MQTT_PASS)  # ✅
```

### 3. paho-mqtt 2.x Compatibility
```python
# PREJ:
mqtt.Client()  # ❌ Deprecated v verziji 2.x

# ZDAJ:
mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  # ✅
```

### 4. Sensor Keys
```python
# PREJ:
("buffer_tank_up", "B_Tak1")      # ❌ Napačen key
("buffer_tank_down", "B_Tak2")    # ❌ Napačen key

# ZDAJ:
("buffer_tank_up", "B_Tak1_1")    # ✅ Pravilen
("buffer_tank_down", "B_Tak2_1")  # ✅ Pravilen
```

### 5. Vrednosti niso bile vidne
```python
# Dodal v sensor.py:
if not self.coordinator.data:
    return None

@property
def available(self):
    return self.coordinator.last_update_success and self.coordinator.data is not None
```

---

## 📊 Sensor Definicije

### Temperature Sensors (17)
Iz `sensor_definitions.py` - friendly names based on [9a4gl/hass-centrometal-boiler](https://github.com/9a4gl/hass-centrometal-boiler):

```python
"B_Tk1" → "Boiler Temperature"
"B_Tptv1" → "Domestic Hot Water"
"B_Tva1" → "Outdoor Temperature"
"B_Tak1_1" → "Buffer Tank Temperature Up"
"B_Tak2_1" → "Buffer Tank Temperature Down"
"B_Tdpl1" → "Flue Gas"
"B_Tlo1" → "Firebox Temperature"
"B_Tpov1" → "Mixer Temperature"
"K1B_Tpol" → "Circuit 1 Temperature"
"K2B_Tpol" → "Circuit 2 Temperature"
# + več...
```

### Counter Sensors (9)
```python
"CNT_0" → "Burner Work" (minutes)
"CNT_4" → "Fan Working Time" (minutes)
# + ostali counters
```

### Misc Sensors (25+)
```python
"B_fan" → "Fan" (rpm)
"B_Oxy1" → "Lambda Sensor" (% O2)
"B_P1" → "Boiler Pump" (ON/OFF)
"K1B_onOff" → "Circuit 1 ON/OFF"
"PVAL_3_0" → "Temperature Setpoint" (°C)
# + več...
```

---

## 🎛️ Control Switches

Definirano v `switch.py`:

```python
SWITCHES = [
    ("PWR 99", "pwr99", "1st Heating Circuit", "1st heating circuit control", "mdi:radiator", "PVAL_99_0"),
    ("PWR 129", "pwr129", "2nd Heating Circuit", "2nd heating circuit control", "mdi:radiator", "PVAL_129_0"),
]
```

**Uporaba:**
- `switch.centrometal_1st_heating_circuit` - vklop/izklop 1st heating circuit
- `switch.centrometal_2nd_heating_circuit` - vklop/izklop 2nd heating circuit

---

## 🔢 Number Controls

Definirano v `number.py`:

```python
NUMBERS = [
    ("PWR 3", "pwr3", "Boiler Temperature", "Boiler temperature setpoint", "mdi:thermometer", "PVAL_3_0", 75, 90, 1, "°C"),
    ("PWR 10", "pwr10", "DHW Temperature", "Domestic hot water temperature setpoint", "mdi:water-thermometer", "PVAL_10_0", 40, 80, 1, "°C"),
    ("PWR 140", "pwr140", "Day Room Temperature (2nd Circuit)", "Day room temperature setpoint for 2nd circuit", "mdi:home-thermometer", "PVAL_140_0", 5, 30, 0.1, "°C"),
]
```

**Uporaba:**
- `number.centrometal_boiler_temperature` - nastavi boiler temperature setpoint (75-90°C)
- `number.centrometal_dhw_temperature` - nastavi domestic hot water temperature setpoint (40-80°C)
- `number.centrometal_day_room_temperature_2nd_circuit` - nastavi room temperature za 2nd circuit (5-30°C)

---

## 🔌 MQTT Protokol

### Topics
```
Device → Server (status):
  cm/inst/biotec/AD53C83A

Server → Device (commands):
  cm/srv/biotec/AD53C83A
```

### Message Format
**Device → Server (status update):**
```json
{
  "B_Tk1": 67.4,
  "B_Tptv1": 61,
  "B_fan": 0,
  "B_STATE": "GLW2",
  "clMsgId": 11709667,
  "_sign": "f90cee634a17814f4a77835116bed3f9d8ac1db3"
}
```

**Server → Device (command):**
```json
{
  "PWR 99": 1,
  "srvMsgId": 938063,
  "_sign": "e8d7a8fbdb48cbdb9cfa061704b888db283c083d"
}
```

**Note:** `_sign` signature je HMAC-SHA1 generiran na portal backend-u. Brez veljavnega podpisa kotel ignorira ukaze.

---

## 🌐 Portal API

### Endpoints
```
Login:
  GET  /login                     - CSRF token
  POST /login_check               - Prijava (email, password)

Control:
  POST /api/inst/control/multiple - Pošiljanje ukazov

Status:
  GET  /wdata/data/installation-status/{install_id} - Status podatki
```

### API Request Example
```http
POST /api/inst/control/multiple
Content-Type: application/json
Cookie: PHPSESSID=...

{
  "messages": {
    "1844": {
      "PWR 99": 1
    }
  }
}
```

### Response
```json
{
  "status": "success",
  "info": {
    "permissions": {
      "1844": 2
    }
  }
}
```

---

## 🔍 Debugging

### Logovi v Home Assistant
```bash
# Real-time logs
tail -f /config/home-assistant.log | grep -i centrometal

# MQTT connection
grep "Connected to MQTT broker" /config/home-assistant.log

# Entity creation
grep "Created.*Centrometal sensors" /config/home-assistant.log
```

### Debug Logging
Dodaj v `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.centrometal: debug
    paho.mqtt: debug
```

### MQTT Testing
```bash
# Subscribe to device messages
mosquitto_sub -h 136.243.62.164 -p 1883 \
  -u appuser -P appuser \
  -t 'cm/inst/biotec/AD53C83A' -v

# Send command (manual testing)
mosquitto_pub -h 136.243.62.164 -p 1883 \
  -u appuser -P appuser \
  -t 'cm/srv/biotec/AD53C83A' \
  -m '{"PWR 99":1,"srvMsgId":123456}'
```

---

## ⚠️ Known Issues / Omejitve

### 1. Install ID je hard-coded
- **Trenutno:** Install ID = "1844" v `const.py`
- **Razlog:** Uporabnik potrdi da je isti za vse uporabnike
- **Če ni res:** Dodaj CONF_INSTALL_ID nazaj v config_flow.py

### 2. Device ID mora biti ročno vnesen
- Uporabnik mora poznati svoj Device ID (AD53C83A)
- **Kako najti:** MQTT monitoring ali portal dashboard

### 3. Climate Entity odstranjena
- Uporabnik je želel samo switches (PWR 99, PWR 129)
- Climate entity je bila odstranjena iz platforms

### 4. Signature ne moremo generirati
- `_sign` podpis se generira na portal backend-u
- Ne moremo direktno pošiljati MQTT ukazov brez portala
- **Rešitev:** Vse ukaze pošiljamo preko Portal API

---

## 📚 Reference Viri

### GitHub Repos
- **9a4gl/hass-centrometal-boiler**: https://github.com/9a4gl/hass-centrometal-boiler
  - Friendly names za senzorje
  - Sensor struktura
  - Reference implementacija

### Dokumentacija
- **/root/CENTROMETAL_MQTT_ANALIZA.md** - MQTT protokol analiza
- **/root/PORTAL_API_RESITEV.md** - Portal API reverse engineering
- **/root/HOMEASSISTANT_INSTALLATION.md** - Installation navodila

### Portal
- **URL:** https://portal.centrometal.hr
- **Email:** robert.barbiric@gmail.com
- **Password:** strom123

---

## 🎨 Integration Icon

### Current Icon
Placeholder ikona ustvarjena s Python PIL:
- **Design:** Orange background + "CM" white text + flame icon
- **Size:** 256x256px (icon.png) + 512x512px (icon@2x.png)
- **Format:** PNG
- **Color scheme:**
  - Background: `#FF6B35` (orange - fire/heat)
  - Text: White
  - Flame: `#FFD93D` (yellow)

### Prikaže se v:
- ✅ HACS integration list
- ✅ Home Assistant Devices & Services
- ✅ Integration card

### Zamenjava z pravim Centrometal logom (opcijsko)

**Če želiš uporabiti pravi Centrometal logo:**

1. **Najdi logo:**
   - Centrometal website
   - Portal dashboard
   - Marketing materiali

2. **Pripravi logo:**
   - Format: PNG
   - Velikost: 256x256px (ali večje, avtomatsko resize)
   - Transparent background (priporočeno)

3. **Zamenjaj ikono:**
   ```bash
   # Copy logo to integration folder
   cp centrometal_logo.png /config/custom_components/centrometal/icon.png

   # Opcijsko: ustvari hi-res verzijo
   # (lahko uporabiš online resize tool ali imagemagick)
   cp centrometal_logo_512.png /config/custom_components/centrometal/icon@2x.png
   ```

4. **Restart Home Assistant**
   - Settings → System → Restart
   - Ali samo: Developer Tools → YAML → Reload: All

**Note:** Ikona je avtomatsko zaznana s strani HACS in Home Assistant. Ni potrebno spreminjati manifest.json.

---

## 🚀 Installation & Testing

### 1. Namestitev
```bash
# Copy to Home Assistant
cp -r /root/homeassistant/custom_components/centrometal \
  /config/custom_components/

# Restart Home Assistant
ha core restart
```

### 2. Dodaj Integracijo
1. Settings → Devices & Services
2. Add Integration → "Centrometal"
3. Vnesi:
   - Email: robert.barbiric@gmail.com
   - Password: strom123
   - Device ID: AD53C83A

### 3. Preveri
```bash
# Check logs
tail -f /config/home-assistant.log | grep centrometal

# Expected output:
# ✅ "Connected to MQTT broker successfully"
# ✅ "Subscribed to topic: cm/inst/biotec/AD53C83A"
# ✅ "Created 50+ Centrometal sensors"
# ✅ "MQTT message received on cm/inst/biotec/AD53C83A with XX fields"
```

---

## 📈 Statistika Seje

**Token Usage:** ~107k / 200k (~53%)
**Files Changed:** 7
**Lines Added:** ~800
**Critical Bugs Fixed:** 5

---

## 🎯 Naslednji Koraki (Opcijsko)

### Možne Izboljšave
1. **Device Discovery** - avtomatsko najdi Device ID iz portala
2. **Additional Controls** - temperature setpoint (PWR 3)
3. **Binary Sensors** - pump state, circuit ON/OFF kot binary_sensor
4. **Energy Monitoring** - tracking burner hours, pellet consumption
5. **Notifications** - alerts za errors, low pellet, maintenance

### Če Install ID ni globalen
Če se izkaže da Install ID ni isti za vse:
1. Odmakni comment iz `CONF_INSTALL_ID` v config_flow.py
2. Odstrani hard-coded DEFAULT_INSTALL_ID
3. Zahtevaj install_id kot user input

---

## 💡 Tips za Naslednjo Sejo

### Preveriti
- Ali so vse vrednosti vidne v HA
- Ali switchi delujejo (ON/OFF)
- Ali MQTT real-time updates delujejo
- Logove za morebitne napake

### Debug Questions
1. **Če vrednosti niso vidne:**
   - Preveri `coordinator.data` v logih
   - Preveri MQTT connection status
   - Preveri topic subscribe result

2. **Če kontrola ne dela:**
   - Preveri Portal API login
   - Preveri command response
   - Preveri MQTT commands topic

3. **Če entitete manjkajo:**
   - Preveri `sensor_definitions.py`
   - Preveri sensor.py creation loop
   - Preveri entity registry (Developer Tools)

---

## 🆕 Changelog v1.1.0 (2025-11-23 11:50)

### Dodano
- ✅ **Number Platform** - nova platforma za številske nastavitve
- ✅ **PWR 3** - Boiler Temperature Setpoint (75-90°C, korak 1°)
- ✅ **PWR 10** - DHW Temperature Setpoint (40-80°C, korak 1°)
- ✅ **PWR 140** - Day Room Temperature 2nd Circuit (5-30°C, korak 0.1°)
- ✅ **Portal API Parameters Pull** - avtomatsko branje PVAL vrednosti iz portala (vsako minuto)
- ✅ **get_installation_status()** - nova funkcija v api.py za branje installation status

### Popravljeno
- ✅ **PWR 99** - preimenovan iz "Heating Circuit" v "1st Heating Circuit"
- ✅ **PWR 129** - preimenovan iz "Power Management" v "2nd Heating Circuit"
- ✅ **Switch ikone** - spremenjene iz `mdi:power` v `mdi:radiator`
- ✅ **PWR 3 max vrednost** - popravljen iz 95°C na 90°C (dejanska max vrednost iz MQTT)
- ✅ **Number entitete "unknown"** - vrednosti se zdaj pulljajo iz Portal API (niso več unknown)

### Datoteke
- 📝 Ustvarjena: `number.py` (113 linij)
- 📝 Posodobljena: `switch.py` (popravljen opisi)
- 📝 Posodobljena: `__init__.py` (dodan Platform.NUMBER, PVAL pulling)
- 📝 Posodobljena: `api.py` (dodana get_installation_status funkcija)
- 📝 Posodobljena: `const.py` (dodana API_STATUS konstanta)

---

**🎉 Integration Status: WORKING (v razvoju)**

**Avtor:** Claude Code + robert.barbiric@gmail.com
**Datum:** 2025-11-23
