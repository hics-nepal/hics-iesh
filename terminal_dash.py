"""HICS Terminal Dashboard — live sensor readout in the terminal."""
import time
import os
import socket
from datetime import datetime

from sensors.dht22 import DHT22
from sensors.bmp280_sensor import BMP280Sensor
from sensors.ds18b20 import DS18B20
from sensors.mcp3208 import MCP3208
from sensors.rtc import RTC
from sensors.config import CH_MQ7, CH_MQ135, SEA_LEVEL_HPA

W = 60


def pressure_to_altitude(pressure_hpa):
    return 44330.0 * (1.0 - (pressure_hpa / SEA_LEVEL_HPA) ** 0.1903)


def heat_index_c(temp_c, humidity):
    """Steadman heat index in °C. Returns None if temp < 20°C."""
    if temp_c is None or humidity is None or temp_c < 20:
        return None
    T = temp_c * 9 / 5 + 32
    H = humidity
    HI = (-42.379 + 2.04901523 * T + 10.14333127 * H
          - 0.22475541 * T * H - 0.00683783 * T ** 2
          - 0.05481717 * H ** 2 + 0.00122874 * T ** 2 * H
          + 0.00085282 * T * H ** 2 - 0.00000199 * T ** 2 * H ** 2)
    return (HI - 32) * 5 / 9


def wifi_ok():
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket()
        s.connect(('8.8.8.8', 53))
        s.close()
        return True
    except Exception:
        return False


def bar(frac, width=20):
    n = int(max(0.0, min(1.0, frac)) * width)
    return '#' * n + '.' * (width - n)


dht  = DHT22()
bmp  = BMP280Sensor()
ds18 = DS18B20()
adc  = MCP3208()
rtc  = RTC()

last_air_t = None
last_air_h = None

os.system('clear')

try:
    while True:
        mq7_raw   = adc.read_raw(CH_MQ7)
        mq135_raw = adc.read_raw(CH_MQ135)
        mq7_v     = adc.read_voltage(CH_MQ7)
        mq135_v   = adc.read_voltage(CH_MQ135)
        soil_pct  = adc.read_soil_pct()
        soil_raw  = adc.read_raw(2)

        _, pressure = bmp.read()
        altitude    = pressure_to_altitude(pressure) if pressure else None
        soil_temp   = ds18.read()

        new_t, new_h = dht.read(retries=1, delay=0)
        if new_t is not None:
            last_air_t, last_air_h = new_t, new_h

        hi       = heat_index_c(last_air_t, last_air_h)
        rtc_dt   = rtc.read() if rtc.ok else None
        ts       = (rtc_dt.strftime('%Y-%m-%d  %H:%M:%S') if rtc_dt
                    else datetime.now().strftime('%Y-%m-%d  %H:%M:%S (sys)'))

        t_s  = f"{last_air_t:.1f} C"   if last_air_t is not None else "Wait..."
        h_s  = f"{last_air_h:.1f} %"   if last_air_h is not None else "Wait..."
        hi_s = f"{hi:.1f} C"           if hi is not None          else "--"
        p_s  = f"{pressure:.2f} hPa"   if pressure               else "--"
        a_s  = f"{altitude:.0f} m ASL" if altitude is not None   else "--"
        st_s = f"{soil_temp:.1f} C"    if soil_temp is not None  else "--"

        print("\033[H", end="")
        print("=" * W)
        print(f"  HICS IESH                    {ts}")
        print("=" * W)

        print("\n  [ CLIMATE ]")
        print(f"  Air Temp   : {t_s:<12}  Heat Index : {hi_s}")
        print(f"  Humidity   : {h_s}")
        print(f"  Pressure   : {p_s:<12}  Altitude   : {a_s}")

        print("\n  [ SOIL MODULE ]")
        print(f"  Soil Temp  : {st_s}")
        print(f"  Soil Moist : {soil_pct:5.1f} %   [{bar(soil_pct / 100)}]")

        mq7_sv    = adc.read_sensor_voltage(CH_MQ7)
        mq135_sv  = adc.read_sensor_voltage(CH_MQ135)
        mq7_rs    = adc.read_mq_rs(CH_MQ7)
        mq135_rs  = adc.read_mq_rs(CH_MQ135)
        rs7_s   = f"{mq7_rs:.0f} Ω"   if mq7_rs   is not None else "--"
        rs135_s = f"{mq135_rs:.0f} Ω" if mq135_rs is not None else "--"

        print("\n  [ AIR QUALITY ]  (divider-corrected sensor voltage)")
        print(f"  CO  (MQ-7)  ch{CH_MQ7}  {mq7_raw:4d} raw  {mq7_sv:.3f}V sensor  RS:{rs7_s:>8}  [{bar(mq7_raw/4095)}]")
        print(f"  AQI (MQ-135)ch{CH_MQ135}  {mq135_raw:4d} raw  {mq135_sv:.3f}V sensor  RS:{rs135_s:>8}  [{bar(mq135_raw/4095)}]")
        print(f"  Note: raw ADC is relative only. ppm needs RS/R0 calibration in clean air.")

        print("\n  [ SYSTEM ]")
        clock_src = "RTC (DS3231)" if rtc_dt else "System clock"
        net_s     = "Connected"   if wifi_ok() else "Offline"
        print(f"  Clock src  : {clock_src}")
        print(f"  Internet   : {net_s}")

        print("\n" + "=" * W)
        print("  Press Ctrl+C to exit.")
        print("\033[J", end="")

        time.sleep(2.0)

except KeyboardInterrupt:
    print("\n\nShutdown.")
    dht.cleanup()
    adc.cleanup()
