"""Sensor definitions with friendly names from reference implementation."""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfTime

# Temperature sensors (based on 9a4gl/hass-centrometal-boiler)
TEMPERATURE_SENSORS = {
    "B_Tk1": {
        "name": "Boiler Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tptv1": {
        "name": "Domestic Hot Water",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tva1": {
        "name": "Outdoor Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tak1_1": {
        "name": "Buffer Tank Temperature Up",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tak2_1": {
        "name": "Buffer Tank Temperature Down",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tdpl1": {
        "name": "Flue Gas",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Ths1": {
        "name": "Hydraulic Crossover",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tpov1": {
        "name": "Mixer Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "B_Tlo1": {
        "name": "Firebox Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K1B_Tpol": {
        "name": "Circuit 1 Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K1B_Tpol1": {
        "name": "Circuit 1 Temp Sensor",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K2B_Tpol": {
        "name": "Circuit 2 Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K2B_Tpol1": {
        "name": "Circuit 2 Temp Sensor",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K1B_Tsob": {
        "name": "Circuit 1 Room Temp",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K1B_Tsob1": {
        "name": "Circuit 1 Room Sensor",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K2B_Tsob": {
        "name": "Circuit 2 Room Temp",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
    "K2B_Tsob1": {
        "name": "Circuit 2 Room Sensor",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
    },
}

# Counter sensors
COUNTER_SENSORS = {
    "CNT_0": {
        "name": "Burner Work",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
    "CNT_1": {
        "name": "DHW Only Time",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
    "CNT_2": {
        "name": "Freeze Protection Time",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
    "CNT_3": {
        "name": "Burner Start Count",
        "unit": None,
        "icon": "mdi:counter",
        "device_class": None,
    },
    "CNT_4": {
        "name": "Fan Working Time",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
    "CNT_5": {
        "name": "Electric Heater Work Time",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
    "CNT_6": {
        "name": "Electric Heater Starts",
        "unit": None,
        "icon": "mdi:counter",
        "device_class": None,
    },
    "CNT_7": {
        "name": "Vacuum Turbine Work Time",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
    "CNT_8": {
        "name": "Boiler Pump Work Time",
        "unit": UnitOfTime.MINUTES,
        "icon": "mdi:timer",
        "device_class": None,
    },
}

# Misc sensors
MISC_SENSORS = {
    "B_fan": {
        "name": "Fan",
        "unit": "rpm",
        "icon": "mdi:fan",
        "device_class": None,
    },
    "B_Oxy1": {
        "name": "Lambda Sensor",
        "unit": "% O2",
        "icon": "mdi:gas-cylinder",
        "device_class": None,
    },
    "B_cm2k": {
        "name": "CM2K Status",
        "unit": None,
        "icon": "mdi:state-machine",
        "device_class": None,
    },
    "B_P1": {
        "name": "Boiler Pump",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "B_zahP1": {
        "name": "Boiler Pump Demand",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "B_P2": {
        "name": "Second Pump",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "B_zahP2": {
        "name": "Second Pump Demand",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "B_P3": {
        "name": "Third Pump",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "B_zahP3": {
        "name": "Third Pump Demand",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "B_priS": {
        "name": "Air Flow Engine Primary",
        "unit": PERCENTAGE,
        "icon": "mdi:air-filter",
        "device_class": None,
    },
    "B_secS": {
        "name": "Air Flow Engine Secondary",
        "unit": PERCENTAGE,
        "icon": "mdi:air-filter",
        "device_class": None,
    },
    "B_zar": {
        "name": "Glow",
        "unit": None,
        "icon": "mdi:campfire",
        "device_class": None,
    },
    "K1B_onOff": {
        "name": "Circuit 1 ON/OFF",
        "unit": None,
        "icon": "mdi:heating-coil",
        "device_class": None,
    },
    "K2B_onOff": {
        "name": "Circuit 2 ON/OFF",
        "unit": None,
        "icon": "mdi:heating-coil",
        "device_class": None,
    },
    "K1B_P": {
        "name": "Circuit 1 Pump",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "K2B_P": {
        "name": "Circuit 2 Pump",
        "unit": None,
        "icon": "mdi:pump",
        "device_class": None,
    },
    "K1B_kor": {
        "name": "Circuit 1 Correction",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": None,
    },
    "K2B_kor": {
        "name": "Circuit 2 Correction",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": None,
    },
    "PVAL_3_0": {
        "name": "Temperature Setpoint",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": None,
    },
    "PVAL_99_0": {
        "name": "Power Value",
        "unit": None,
        "icon": "mdi:power",
        "device_class": None,
    },
    "PVAL_129_0": {
        "name": "Power Management",
        "unit": None,
        "icon": "mdi:power-settings",
        "device_class": None,
    },
    "B_lvl": {
        "name": "Pellet Level",
        "unit": None,
        "icon": "mdi:gauge",
        "device_class": None,
    },
}

# Combine all sensors
ALL_SENSORS = {
    **TEMPERATURE_SENSORS,
    **COUNTER_SENSORS,
    **MISC_SENSORS,
}
