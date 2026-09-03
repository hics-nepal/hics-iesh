# Kickoff — IESH firmware Module framework (plug-and-play sensors)

Self-contained brief for a **fresh, independent session**. This is **pure software** in this
repo (`hics-iesh-v0.1`) — it needs no hardware and runs in parallel with the PCB/enclosure
work. Background memory auto-loads; also read `../iesh-production-reference/05-modular-platform/`
(the architecture) and that repo's `02-pcb/carrier-hat-v1/` (the connector this targets).

## Goal
Turn the v0.1 hardcoded per-sensor drivers into a **Module framework**: a sensor module plugs
into the Carrier HAT's **MODBUS connector**, firmware **auto-detects** it, loads its driver,
logs it, shows it on the OLED + web dashboard, and teaches with it — **no rewiring, no reflash**.
This is what makes "add a new sensor" a small driver instead of edits across the codebase.

## Where things are today (v0.1)
- `sensors/` — one module per sensor (`dht22.py`, `bmp280_sensor.py`, `mcp3208.py`,
  `air_quality.py`, `ds18b20.py`, `rtc.py`, `oled.py`, `camera.py`), each with an ad-hoc API
  and an `.ok` flag. `sensors/config.py` is the hardware map (pins/addresses/calibration).
- `core_dash.py` — the sensor loop: reads each sensor, renders OLED, logs to SQLite.
- `data/database.py` — `telemetry` table (fixed columns), `data/uploader.py` — cloud sync.
- `web/app.py` — dashboard; `curriculum/modules/*.py` — activities bound to sensor values.

## The hardware contract it targets (frozen)
From `../iesh-production-reference/02-pcb/carrier-hat-v1/docs/DESIGN.md`:
- **MODBUS v1** connector: 5V, 3V3, I²C (SDA/SCL), UART, SPI, 2 spare ADC (CH3/CH4),
  **DETECT/ID**, ENABLE, IRQ. Plus a dedicated PMS5003 UART slot.
- **I²C address map (reserved):** SHT4x 0x44, SCD40 0x62, ADS1115 0x48 — discovery can probe these.
- **DETECT line:** a resistor-code (or ID EEPROM later) identifies a module type cheaply.

## Build this (suggested order)
1. **`Module` interface** (an ABC), per `05-modular-platform/00-architecture.md`:
   `identity()` → {type, revision, logical_channels, track} · `present()` → bool ·
   `read()` → {channel: value} · `calibration()` → {status, date, params}.
2. **Module registry + discovery at boot:** probe known I²C addresses + read the DETECT
   resistor-code → instantiate the matching `Module`. Fall back to the built-in base sensors.
3. **Refactor the existing sensors** to implement `Module` (keep `config.py` values identical
   so behavior is unchanged — the PCB preserves the v0.1 pin/divider/RL values on purpose).
4. **Logical channels:** modules declare names (`pm2_5`, `co2_ppm`, `air_temp`, …); make the
   data model, OLED, dashboard, and curriculum **bind to channel names**, not fixed columns
   (so a new module's data flows end-to-end without schema edits). Add a `modules`/discovery
   record + a per-module calibration record.
5. **Wire it through:** `core_dash.py` iterates discovered modules; `database.py` stores by
   channel (consider a long/EAV table or JSON column); `uploader.py` sends channel-keyed
   batches (note: real API is `POST /api/v1/ingest/environmental/`, `Authorization: Token`,
   `{station_id, readings:[…]}` — see the himalayansciences-web repo).
6. **A driver template** others copy to add a module (mirrors the KiCad module template).

## Verify
Run the loop on dev (sensors stubbed/mocked) — discovery picks up "present" modules, logs
channel-keyed data, dashboard renders them. Then on real hardware, plug an SHT4x/SCD40 and
confirm it auto-appears. Don't break the existing base sensors (regression-test `tests/`).

## Independence
No dependency on the PCB/enclosure being finished — the connector pinout + address map above
are frozen. Ship the framework; real modules (PMS5003/SCD40) get built in parallel on the HW side.
