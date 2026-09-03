"""HICS sensor drivers.

The driver re-exports below are resolved lazily (PEP 562). They used to be
eager `from .dht22 import DHT22` imports, which pulled Adafruit `board`,
`spidev` and `smbus2` into the process the moment anything under `sensors.`
was touched — so `sensors.config` and `sensors.health`, which need no
hardware at all, could not be imported on a development machine or in CI.
Every consumer in the tree imports the submodule directly anyway.
"""

__all__ = ['DHT22', 'BMP280Sensor', 'DS18B20', 'MCP3208', 'OLED', 'RTC']

_LAZY = {
    'DHT22':        ('.dht22', 'DHT22'),
    'BMP280Sensor': ('.bmp280_sensor', 'BMP280Sensor'),
    'DS18B20':      ('.ds18b20', 'DS18B20'),
    'MCP3208':      ('.mcp3208', 'MCP3208'),
    'OLED':         ('.oled', 'OLED'),
    'RTC':          ('.rtc', 'RTC'),
}


def __getattr__(name):
    try:
        module, attr = _LAZY[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    from importlib import import_module
    value = getattr(import_module(module, __name__), attr)
    globals()[name] = value        # cache, so this runs once per name
    return value


def __dir__():
    return sorted(__all__)
