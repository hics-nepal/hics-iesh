# IESH v0.2 — handoff

> **The single document for this work** — everything a fresh session or a new person needs
> in order to pick it up and redo it in detail. Established **2026-09-03** from a live
> diagnosis of the station at `pawan@iesh.local`; audited and extended the same evening
> (§4 second pass, §16.8). **Bench-ready: start at [`docs/README.md`](docs/README.md)** for
> the sheets, then §14.
>
> Read §1 first if you don't know the repos; §3 for what is broken and how we know; §16 for
> what to question rather than inherit; §14 for what to actually do.
>
> **House rule, inherited:** *if this document and reality disagree, this document is the
> bug.* Sections marked **⚠ UNVERIFIED** were never confirmed — see §16.

## Contents

| § | |
|---|---|
| [0](#0-the-one-paragraph-situation) | The one-paragraph situation |
| [1](#1-the-repos-and-where-truth-lives) | **The repos and where truth lives** — hics-docs · this repo · iesh-production-reference · himalayansciences-web |
| [2](#2-what-is-physically-true-right-now) | What is physically true on the station right now |
| [3](#3-the-six-faults-with-their-evidence) | The six faults, with their evidence |
| [4](#4-what-changed-this-session--firmware-committed) | What changed this session — firmware, committed |
| [5](#5-reference-photographs-and-the-parts-inventory) | Reference photographs, dimensions, parts inventory |
| [6](#6-artifacts-and-how-to-regenerate-them) | Artifacts and how to regenerate them |
| [7](#7-the-one-design-decision-everything-follows-from) | **The one design decision everything follows from** |
| [8](#8-power--fix-this-before-anything-else) | Power — fix this before anything else |
| [9](#9-wiring--the-protoboard-hat) | Wiring — the protoboard rework |
| [10](#10-how-the-sensors-actually-connect) | How the sensors actually connect — CAT5e |
| [11](#11-pi-configuration-changes) | Pi configuration changes |
| [12](#12-sensor-placement-one-by-one) | Sensor placement, one by one |
| [13](#13-shopping-list) | Shopping list |
| [14](#14-build-order) | Build order, with gates |
| [15](#15-website--before-going-public-again) | Website — before going public again |
| [16](#16-the-rethink--what-to-question-rather-than-inherit) | **The rethink — what to question rather than inherit** |
| [17](#17--unverified--measure-or-confirm-before-relying-on-any-of-these) | ⚠ UNVERIFIED assumptions |
| [18](#18-open-decisions--not-for-an-agent-to-make-alone) | Open decisions — not an agent's to make alone |
| [19](#19-things-that-will-waste-your-time-if-you-dont-know-them) | Gotchas that will waste your time |
| [20](#20-what-this-deployment-does-not-claim) | What this deployment does *not* claim |

---

## 0. The one-paragraph situation

The station has **never logged a usable day of data**, and the reasons are now known rather
than suspected. The root cause is a **live 5 V undervoltage** that makes I²C and 1-Wire
devices drop off their buses intermittently; on top of that, v0.1's firmware logged a dead
sensor's last value forever, so roughly half the existing record is garbage that reached
the website looking like data. The firmware half is **fixed and committed**. The hardware
half is **not started** — the circuit is currently part-disassembled on the bench, the
camera is removed, and the undervoltage is still present on both supplies tried so far.
The immediate next action is not building anything; it is **making `vcgencmd get_throttled`
read `0x0` and keeping it there.**

### 0.1 ⚠ Site plan revised 2026-10-05: read before §7, §10, §12, §13

The site details are now known: a black **1000 L water tank on a ≈1 m iron-frame stand** with
an open-bar top, and **crows and monkeys** on the roof. The plan built on them is
**[`docs/rooftop-plan.html`](docs/rooftop-plan.html)** (rev 6). **Where it conflicts with
§7/§10/§12/§13, the plan wins.** Those sections get rewritten once a spot on the roof is chosen.

- ✅ **F6 closed, per Pawan 2026-10-05:** the OV5647 and the clip-on fisheye both work.
- **Settled:** the station is **one compact unit in the existing container**. The camera is in
  a lid tower under a small hood. The Pi and HAT sit on the shaded inside wall. Every outdoor
  sensor stays within ~0.5 m: the DHT22 shield on a short arm ≥300 mm from the box, the gas pod
  under the shelf, and the raindrop and LDR on the hood. The camera logs every sky object, not
  just meteors. New parts only if cheap and sold in Kathmandu; otherwise DIY.
- **Siting rule:** the lens needs no tall object within atan(Δh/d) > 15°, i.e. d ≥ 3.7 × Δh.
  First choice is a parapet or stairwell spot far enough from the tank. Fallback is a pipe at
  the stand corner above the tank.
- **Superseded:** the box on a tile, the large hood table, the sensor mast, the 8-core mast
  cable map (sheet 3), and the "drill the lid nowhere" rule.
- **Settled, power:** as built (BOARD-BUILD §2). 5 V 2 A into the GPIO feed, 1000 µF, 3.3 V
  from the Pi, heater rail on the other 5 V source. **No buck.** F1 is managed in software:
  `arm_freq=1000`, Bluetooth off, the sky pipeline at 640 × 480 on one core, the shortest 5 V
  lead (extend the mains side, not the 5 V side), and `get_throttled` logged and flagged. The
  LM2596 is only the last rung of the fallback ladder.
- **Settled, ribbon:** keep the 110 mm ribbon. The 100 × 150 HAT covers the camera connector
  (≈44 mm from the Pi's power end, ≈20 mm under the board), so the **only** orientation that
  can reach is: Pi on the inside wall, **USB/Ethernet end up** under the lid, ribbon out at the
  board's A-edge through the ~4 mm gap before the USB jack, short tower. Paper-strip test
  before fixing anything; the 30 cm ribbon (Himalayan Solution) is the fallback.
  ⚠ **Correction:** `roofbox_check.py`'s "110 mm FFC reaches (~90 mm)" was computed for a
  65 × 70 HAT that did not cover the connector. It does not hold for the board being built.
  Hanging the Pi from the lid (sheet 4) does not reach with this board.
- **Sequencing:** the Tools Competition Phase I abstract (13 Oct 11:59 PM ET = 14 Oct
  09:44 NPT; see `hics-docs/funding/tools-competition/2027/APPLICATION-PLAN.md`) comes first.
  That entry keeps IESH outside its claims, so station work after submission. Add a dew heater
  from day one: eight 220 Ω resistors on the heater rail.

---

## 1. The repos and where truth lives

Four repositories matter. The rule from `hics-docs/WORKING-AGREEMENT.md`: **an
institute-level fact is stated once in `hics-docs` and linked everywhere else; a repo-level
fact lives in that repo's own truth document. Never restate across the boundary.**

```
~/Documents/HICS/
├── hics-docs/                     institute hub — strategy, funding, naming, decisions G1-Gn
├── hics-iesh/
│   ├── hics-iesh-v0.1/            THIS REPO — the firmware actually running on the station
│   └── iesh-production-reference/ productisation: PCBs, enclosure CAD, costing, roadmap
├── himalayansciences-web/         the Django site + the ingest API the station uploads to
└── imp/                           credentials — never read, quote or commit
```

### 1.1 `hics-docs/` — the institute hub
Loads in no session automatically; **open it.** Start at `README.md` (the board of external
deadlines, plus standing decisions G1–Gn), then `HICS-MAP.md` (every folder and where its
truth lives) and `WORKING-AGREEMENT.md`.

Decisions that bear directly on this work:
- **G9 / D28** — installed school stations are calibrated on every channel that can be, with
  **MQ staying a labelled proxy**. This is why `quality_flag = suspect` is correct, not a bug.
- **G10** — this repo's `curriculum/` is to be *unified* with the learning platform, not
  duplicated. Don't extend it here.
- **G29 (2026-08-26)** — the Himalaya AI / DeepGyan collaboration is **ended**. HICS has **no
  partners and no external adopters**. Do not describe either as one in any material.
- **Swiss Week is 21–25 Sep 2026, travel from 20 Sep.** The one hard external date this work
  feeds. Nepal Week (the Swiss cohort visiting Nepal) is 8–12 Mar 2027 — that is the chance to
  *show* a working station rather than describe one.

### 1.2 This repo — `hics-iesh-v0.1/`
The firmware on the station. Layout that matters:

| Path | What |
|---|---|
| `core_dash.py` | the sensor loop: reads, OLED, DB write, upload. **The main program** |
| `sensors/config.py` | single source of truth for pins, addresses, calibration, API key. **Never synced by `deploy.sh`** and `--assume-unchanged` on the Pi |
| `sensors/health.py` | **new this session** — the freshness + plausibility gate (§4) |
| `sensors/*.py` | one driver per device: `dht22` `bmp280_sensor` `ds18b20` `mcp3208` `oled` `rtc` `camera` `air_quality` |
| `data/database.py` | SQLite interface. Every sensor column is nullable |
| `data/uploader.py` | batch upload to the website, with a `synced` flag per row |
| `web/app.py` | Flask dashboard on :5000 (dev server — fine for LAN) |
| `curriculum/` | 5 modules, 25+ activities. **Frozen pending G10** |
| `scripts/gen_drawings.py` | **new** — generates both 2D sheets from one net list |
| `tests/test_health.py` | **new** — 21 checks, runs with no hardware |
| `deploy.sh` | rsync to the Pi. `--restart` · `--pull` · `--file` |
| `flash.sh` / `setup.sh` | provision a blank SD card / repair a running Pi |

Station DB lives at `~/hics-data/hics.db` on the Pi — deliberately outside the code tree so
it survives re-deploys and re-flashes.

### 1.3 `../iesh-production-reference/` — the product, and it already exists
**Read this before proposing any hardware design.** It is a reference library, not the
product itself, and it is further along than you might assume. Decisions are registered as
D1–D29 in `07-roadmap/02-decisions-register.md`.

| Folder | What's in it |
|---|---|
| `00-overview/` | product vision, the two-track EDU/SCI strategy, current-state audit |
| `01-hardware/` | v0.1 teardown, calibration, **`04-power-architecture.md` (authoritative, numeric)** |
| `02-pcb/` | **two routed boards, DRC-clean, gerbers ready to fab** |
| `03-enclosure/` | OpenSCAD CAD for both variants, a browser 3D viewer, print STLs |
| `04-costing/` | BOM costing, pricing, unit economics |
| `05-modular-platform/` | the plug-and-play module architecture and use-case configs |
| `06-firmware-data/` | firmware production-readiness, ingest contract, OTA/fleet |
| `07-roadmap/` | phased plan, milestones, **decisions register D1–D29**, risks |

**The two PCBs — already designed, not yet fabbed:**
- **`carrier-hat-v1`** — 65 × 70 mm, 2-layer, DRC 0/0. Gerbers at
  `02-pcb/carrier-hat-v1/out/fab/carrier_hat_v1_gerbers.zip`.
  ⚠ **J1 (the 40-pin socket) is on the BOTTOM copper** so the HAT seats down onto the Pi.
  The protoboard layout in §9 deliberately matches this footprint so it transfers.
- **`power-mgmt-v1`** — 60 × 46 mm. LT3652 MPPT charger (wall DC *and* solar), 2× LM74700
  ideal-diode OR, 2× TPS3808 supervisors.
  ⚠ **Input is 18–24 V, not 12 V** — a buck charger needs Vin above pack voltage. **Do not
  wire this into the Lalitpur deployment**; it belongs to the production build.

**Power tiers** (`01-hardware/04-power-architecture.md`) — *field ≠ remote*: the difference
is the charge source and battery size, not the topology.
1. **indoor / mains-primary** — `EDU-BASE`, `KIT`
2. **powered outdoor site** — `SCI-AIR`, `SCI-BUILDING`. **← the Lalitpur rooftop is this one**
3. **off-grid** — `FIELD-REMOTE` (Dolpo transect): solar + large LiFePO₄ + low-power firmware

**Enclosure CAD** in `03-enclosure/cad/`: `edu.scad` (desk/classroom), `sci.scad` (sealed
outdoor), shared `iesh_lib.scad`, and **`roofbox.scad` — added this session** for the found
container. `viewer.html` + `serve.sh` give a browser 3D view; `build_glb.py` bakes GLBs.

⚠ **Three traps in that folder:**
- **It is not a git repository.** Everything in it, including this session's CAD, is
  unversioned. See §18.
- **`iesh_lib.scad` models a Raspberry Pi 4B.** The deployed station is a **3B+**. That is
  why `roofbox.scad` defines its own board dimensions rather than reusing the library's.
- **`cad/render_views.py` has a stale hardcoded path** —
  `~/Documents/HICS/iesh-production-reference`, missing the `hics-iesh/` segment. It will
  fail until fixed. Not touched this session.

### 1.4 `../../himalayansciences-web/` — the site and the ingest API
Django + Wagtail. `hics/settings/base.py` has **`USE_TZ = True`, `TIME_ZONE = 'Asia/Kathmandu'`**
and `HICS_PRIMARY_STATION_ID = 'IESH-KMC-001'`.

**The contract is `docs/INGEST_CONTRACT.md`** — read it before changing anything in
`data/uploader.py`. Authoritative implementation: `instruments/api.py` and
`instruments/authentication.py`.

```
POST https://himalayansciences.org/api/v1/ingest/environmental/
Authorization: Token <station-api-key>
{"station_id": "IESH-KMC-001", "readings": [{...}, {...}]}
-> 201 {"accepted": n, "duplicates": n, "errors": n}
```

| Route (`/api/v1/…`) | Auth | Purpose |
|---|---|---|
| `ingest/environmental/` | Token | the station's upload endpoint |
| `stations/` | public | station list / GeoJSON. **Filters `status in (active, maintenance)`** |
| `data/latest/` | public | latest reading, `?station=IESH-KMC-001` |
| `data/historical/`, `data/aggregate/`, `data/compare/`, `data/download/` | public | series, rollups, CSV |
| `health/`, `stats/` | public | platform |

**Models** (`instruments/models.py`):
- **`Station`** — `station_id` · lat/lon/`altitude_m` · `location_name` · `status`
  (`active` / `offline` / `maintenance` / `planned`, default `planned`) · **`api_key_hash`**
  (SHA-256; the plaintext key is unrecoverable) · `last_seen` (stamped on every authenticated
  ingest). **It is a Wagtail snippet — edit it in the CMS**, so flipping `status` is an admin
  action, not a shell command.
- **`EnvironmentalReading`** — wide nullable columns (`temperature_c`, `humidity_rh`,
  `pressure_hpa`, `altitude_m`, `pm1_0/2_5/10`, `co2_ppm`, `co_ppm`, `uv_index`,
  `soil_temp_c`, `soil_moisture_pct`) **plus a `module_data` JSON blob** for everything else.
  That blob is the extension point — raw `mq7_raw`/`mq135_raw` land there, and new channels
  need no migration. Promote a channel to a column only once it stabilises.

**Four behaviours to know:**
1. **Dedup is `get_or_create` on `(station, timestamp)`.** Re-POSTing a window is safe and is
   how offline backfill reconciles — but it also means **a corrected row will never overwrite
   a bad one at the same timestamp.** This is why fault F4 (wrong clock) is permanent, and why
   §15 exists.
2. **Field aliases are accepted** — `air_temp`, `air_hum`, `pressure`, `soil_temp`,
   `soil_moist` map onto the canonical names, so the v0.1 payload works unchanged. New code
   should send canonical names; this repo now does.
3. **Any `v0.*` firmware marks every reading `suspect`**, whatever the values. Deliberate:
   uncalibrated sensors, an MQ proxy, unverifiable timestamps. Matches `hics-docs` G9. **Do
   not bump `FIRMWARE_VERSION` to clear it.**
4. **Plausibility bounds** in `_auto_quality_flag` — `sensors/health.py` deliberately mirrors
   them, so a value the server would reject is dropped at the device edge. **Keep the two
   lists in step.**

**API keys** are issued by `python manage.py seed_hics`
(`pages/management/commands/seed_hics.py`), or rotated with `Station.generate_api_key()`
(`secrets.token_urlsafe(32)`). Only the hash is stored — the plaintext is printed once, then
lives on the device in `sensors/config.py`. Auth is rate-limited to 10 req/min, and the
station is identified by the `station_id` in the body (or `?station=`), then the key checked
against that station's hash.

---

## 2. What is physically true right now

Verified by SSH on 2026-09-03, not assumed.

| Thing | State |
|---|---|
| Board | **Raspberry Pi 3B+** (not a 4B — `iesh_lib.scad` models a 4B, which matters for CAD) |
| Power | ⚠ **`throttled=0x50005` — under-voltage NOW, currently THROTTLED.** Measured on a 2-minute-old boot, so not stale history. Present on the original power bank *and* on the replacement plug adapter. |
| I²C | `0x3c` OLED ✅ · `0x57` DS3231 EEPROM ✅ · `0x68` DS3231 RTC ✅ · **`0x76` BMP280 ABSENT** ❌ |
| 1-Wire | `28-062261761e24` present — but it **disappeared and reappeared** during a single session |
| DS3231 | Responds, but reads **`2000-01-05`** — coin cell flat or never set. No `/dev/rtc0`: the overlay isn't loaded, so the OS never uses it |
| Camera | **Physically removed.** `config.txt` still has both `camera_auto_detect=1` and `dtoverlay=ov5647` (conflicting) |
| Network | `wlan0` on `liverpool08_2.4`, signal 70. **No `wlan1`** — a 3B+ has one radio, so the `IESH_Hub` hotspot in the README does not exist on this unit |
| DB | 749 rows total. Rows/day: Jun 11 → 598, Jun 12 → 35, Jun 13 → 101, Sep 3 → 26. A full day is 1440 |
| Services | `hics-core` + `hics-web` enabled and running |
| Website | Station exists and ingest works; deliberately **not** in the public list (`status` outside `active`/`maintenance`) until this round is done |

### Which product tier this is
This is **not** the EDU desk/classroom object. A rooftop unit at a home or a school —
weatherised, mains present, battery for ride-through, nobody handling it — is exactly
tier 2, *"powered outdoor site (field)"*, in
`../iesh-production-reference/01-hardware/04-power-architecture.md`, and it maps onto
`CONFIG-SCI-BUILDING` rather than `CONFIG-EDU-BASE`. That matters for three reasons:

- **No OLED window, no demonstrative cutaway, no handling affordances.** The sealed SCI
  variant has no display for a reason; the OLED stays on the sled for bench work only.
- **Field ≠ remote.** Grid is present, so there is no solar sizing problem and no large
  LiFePO₄ pack — a modest UPS ride-through is the whole battery requirement.
- The learning portal still runs and is still reachable on the LAN; it just isn't what
  the *enclosure* is designed around.

---

## 3. The six faults, with their evidence

Referenced as F1–F6 throughout. **F1 is the root cause and F2 is its main symptom — those
two are what the rebuild is for. F3 is fixed in firmware (§4).** F5 is the one that matters
to anyone outside this document: the station has never run a full day.

| # | Fault | Evidence |
|---|---|---|
| **F1** | **Undervoltage, continuously** | `vcgencmd get_throttled` = `0x50005` → *under-voltage NOW · currently THROTTLED*. `dmesg`: `hwmon2: Undervoltage detected!`. Present on the power bank **and** on the replacement plug adapter, both measured on a 2-minute-old boot — so it is not stale history. Pi **3B+** wants a solid 5 V/2.5 A. |
| **F2** | **Sensors drop off their buses and come back** — [see the as-built photo](docs/reference-photos/01-circuit-as-built-cardboard.jpg) | BMP280 `[Errno 121]`, OLED `[Errno 5]`, DS18B20 absent from `/sys/bus/w1/devices/` then present as `28-062261761e24` minutes later. Downstream of F1, and of ~40 dupont crimp + friction joints. |
| **F3** | **A dead sensor logged its last value forever** | v0.1 initialised every reading to `0.0` and overwrote only on success. Measured in the station DB: `soil_temp` = **441 rows of 0.0** + **15 rows of 85.0** (the DS18B20 power-on-reset sentinel); `pressure` = **416 rows frozen at 800.647395954495** (bit-identical to 12 dp) + 26 rows of 0.0, against only **5** plausible rows. ~46 % of the soil column was garbage indistinguishable from data. |
| **F4** | **No working clock** | No `dtoverlay=i2c-rtc,ds3231`, so `/dev/rtc0` does not exist and the OS never reads the DS3231. The chip itself reads **2000-01-05** — coin cell dead or never set. Boot time came from systemd's saved clock, which is why services claimed "started Jun 13" on a 14-minute uptime. Every power cut mints rows with a wrong timestamp, and the server dedups on `(station, timestamp)` — so bad timestamps are **permanent**. |
| **F5** | **Never ran a full day** | Rows/day: Jun 11 → 598, Jun 12 → 35, Jun 13 → 101, Sep 3 → 26. A full day is 1440. There is no time series to speak of. |
| **F6** | Camera dead | `ov5647: i2c read error, reg: 300a = -5`; `config.txt` carries **both** `camera_auto_detect=1` and `dtoverlay=ov5647`. Camera has since been physically removed. |

---

## 4. What changed this session — firmware, committed

Commit `2acdd13` on `master`. **Synced to the Pi but not yet running** — the services were
never restarted (`deploy.sh --restart` can't do it; the `sudo` step needs a TTY password).
That is *not* a loose end to chase: the station is being torn down and rebuilt, so the
restart happens naturally during bench bring-up (§14 step 4). It matters only that you know
the code on disk is newer than the code in the running process, so **the log you see before
a restart is v0.1's behaviour, not the fixed behaviour.**

| File | Change |
|---|---|
| `sensors/health.py` **(new)** | A `Channel` logs a value only if it is *fresh* (a reading arrived within `max_age`, default 180 s) **and** *physically plausible*; otherwise `NULL`. Bounds mirror `_QUALITY_BOUNDS` in the website's `instruments/api.py`, so anything the server would flag `suspect` is dropped at the edge — which catches `85.0` (above the 80 °C ceiling) and `0.0` hPa (below the 300 hPa floor) for free. Also detects a **frozen register** (bit-identical raw reads N times running) and recovers when it moves again. |
| `core_dash.py` | Values flow through a `ChannelSet` instead of floats initialised to `0.0`. Downed BMP280/OLED are re-initialised every 60 s, so a device that drops off and returns recovers without a service restart. Unhealthy channels are named in the log and on the OLED. Altitude no longer feeds 0.0 hPa into the barometric formula to display 44 330 m. |
| `sensors/ds18b20.py` | Rescans the 1-Wire bus on failed reads; rejects the 85.0 sentinel; checks CRC; calls `modprobe` by absolute path (it had been silently printing `modprobe: not found` — `/usr/sbin` isn't on a login user's `PATH`). |
| `sensors/bmp280_sensor.py`, `sensors/oled.py` | Added `reinit()`. BMP280 exposes `last_raw_p` for frozen detection. |
| `data/uploader.py` | The `_online()` probe socket was never closed — **one leaked fd per upload cycle, ~288/day**. Timestamps now sent as explicit UTC per `docs/INGEST_CONTRACT.md`; **verified instant-identical** to what Django was already storing via `TIME_ZONE`, so **no existing data shifts**. Floats rounded. |
| `sensors/__init__.py` | Driver re-exports made lazy (PEP 562). They were eager, so `sensors.config` and `sensors.health` — which need no hardware — could not be imported off-Pi or in CI. |
| `tests/test_health.py` **(new)** | 21 checks, every case a value found in the live DB. Runs anywhere: `python3 tests/test_health.py`. Passing on dev **and** on the station. |

**The design principle, if you change nothing else:** `NULL` is honest, a stale number is
not. `data/database.py` already declared every sensor column nullable; v0.1 simply never
wrote one.

### Second pass, same evening — audit of the above, committed

| File | Change |
|---|---|
| `sensors/health.py` | **Bug in the frozen-register gate.** It compared the *compensated value* when no raw word was given, so a DS18B20 buried in still soil (identical 0.0625 °C reads for minutes) or a DHT22 at a steady 0.1 °C would be declared *frozen* and logged `NULL` — the 24 h bench gate (§14 step 6) would have failed on healthy sensors. Frozen detection now runs **only** when the caller supplies `raw` (the BMP280 does). Two regression tests added; 23 checks pass. |
| `core_dash.py` | Removed the BMP280-as-`air_temp` fallback: the BMP280 sits inside a box that runs 45–55 °C in sun (§7), so that fallback would log the *box* temperature as air temperature whenever the DHT22 dropped out — exactly the plausible-looking garbage the gating exists to stop. ADC channels are handed `None` (not 0) when SPI never opened. |
| `tests/test_all.py` | `--skip camera` / `--only bmp280,oled,rtc`; test order is now the §14 step 5 bring-up order. |
| `scripts/pi_config.sh` **(new)** | Applies §11.1–11.3 to `config.txt` idempotently (`--dry-run` shows the diff). Backs up first. |
| `scripts/gate_check.py` **(new)** | The §14 gates as one command on the station: throttle flags, `config.txt`, RTC vs system clock, I²C scan, 1-Wire (with a 3 s re-scan to catch F2), services + the `| NULL:` log note, rows/day and today's NULL share. |
| `scripts/gen_drawings.py` | Schematic re-routed (no line crosses a rail or a label); terminals carry the **CAT5e core colour**; new sheets **3** (header pinout + cable map) and **4** (lid layout, dimensioned, read from the CAD). Mast cable core map changed — see §10. DHT22 moved to the 3.3 V pair. |
| `docs/cad/` **(moved here)** | `roofbox.scad` + `roofbox_check.py` + `render.sh` now live in this repo (§6). Design revised: camera **tower** through the hood, **free-standing hood table**, **no lid holes**, lens under a lip, PG7 hole size corrected (12.5 mm, not 7). §16.8 says why. |

---

## 5. Reference photographs and the parts inventory

### Photographs
In `docs/reference-photos/` (1400 px, ~850 KB total) so the docs don't depend on paths
outside the repo. **Several assumptions in §17 were read off these images — which is exactly
why they need calipers.**

**[`01-circuit-as-built-cardboard.jpg`](docs/reference-photos/01-circuit-as-built-cardboard.jpg)
— fault F2, visually.** The cardboard build as taken to the AIT selection pitch: dupont
plugged into dupont, joints held with masking-tape flags, no strain relief anywhere, sensor
boards hanging off unsupported leads. The black power bank at left was the original supply
(F1). This is the thing being replaced.

**[`02-container-exterior.jpg`](docs/reference-photos/02-container-exterior.jpg) — the found
enclosure.** *Re-measured 2026-09-11: **130 × 130 mm base, 170 × 170 mm top, 230 mm tall,
internal** — materially bigger than the 120 × 120 × 180 first recorded (§5 table).* The taper,
rim width and wall thickness in `roofbox.scad` were **estimated from this image** — U1.

**[`03-container-interior-gasket.jpg`](docs/reference-photos/03-container-interior-gasket.jpg)
— the red silicone gasket** in the lid channel. This is the reason the container is usable
at all, and the reason the lid is the chassis plate. The lid seats on a moulded rim, not on
the wall edge.

**[`04-camera-and-clipon-fisheye.jpg`](docs/reference-photos/04-camera-and-clipon-fisheye.jpg)
— the constraint that shaped the enclosure.** OV5647 "Raspberry Pi Camera Rev 1.3", board
**25 × 24 mm**, with its ribbon at **~110 mm — and that is what forces lid-up (§16.1)**.
Also the clip-on phone fisheye: a knurled-ring lens element on a hinged clip, which is what
`cam_tower` seats. `FE_RING_D`, `FE_RING_H` and `FE_BACK` (U2, U3) were all guessed from
this photo.

### Dimensions on record

| Item | Dimension | Source |
|---|---|---|
| Container body | **130 × 130 mm base, 170 × 170 mm top, 230 mm tall — all internal** | **re-measured 2026-09-11.** Supersedes the 120 × 120 × 180 previously recorded here as *measured* |
| Container taper / rim / wall | rim ≈8 mm, wall ≈1.8 mm | **still estimated — U1** |
| Camera board (OV5647 Rev 1.3) | 25 × 24 mm, M2 holes on a 12.5 mm grid | datasheet + photo |
| Camera ribbon | **≈110 mm** | measured |
| Fisheye knurled ring | ≈Ø23 × 9 mm | **estimated — U2** |
| Fisheye back-focal gap | ≈3 mm | **guess, needs trial — U3** |
| Raspberry Pi 3B+ | 85 × 56 mm, M2.5 on a 58 × 49 grid, ports 17 mm tall | datasheet |
| Protoboard in use | **100 × 150 mm** (`PY-10CM*15CM`), **uncut** | measured. The corrected box holds it flat in its top ~115 mm, so it is *not* trimmed to the 65 × 70 `carrier-hat-v1` footprint |
| Protoboard spares | 1 × 100 × 150 mm blank, 2 × 50 × 70 mm blank | measured |
| Verified stack height | ~~80.5 mm in 178 mm~~ | **stale — computed against the old box. Recompute once `roofbox.scad` is corrected** |

> ⚠ **The CAD has not caught up with the corrected box.** `roofbox.scad`, every render, both
> 1:1 templates and all of `roofbox_check.py` still model 120 × 120 × 180. Do not cut, drill or
> print from them until they are regenerated. The hood plate and leg lengths in §13 are
> likewise sized for the old box — ≈250 mm plate and ≈280 mm legs are the arithmetic for the
> real one, unconfirmed by the CAD.

### Parts inventory — transcribed from the three supplier bills
Supplier: **Supreme Light Technology Pvt. Ltd.**, Sanepa-2, Lalitpur · 9860563506 ·
sitech.com.np. Bill images are deliberately not committed; this transcription is the record.

**Bill 724 — 22 May 2026 — ₨7,095**

| Item | Qty | Rate | Item | Qty | Rate |
|---|---|---|---|---|---|
| DHT22 | 2 | 550 | LED | 5 | 2 |
| BMP280 | 1 | 350 | Resistors | 30 | 1 |
| Raindrop sensor | 2 | 250 | LDR | 4 | 15 |
| Soil moisture sensor | 1 | 165 | Multimeter + battery | 1 | 475 |
| Jumper wires | 2 sets | 150 | PIR sensor | 1 | 200 |
| MQ-7 | 2 | 370 | RTC module | 1 | 350 |
| MQ-135 | 2 | 300 | Matrix board 10×15 cm | 2 | 85 |
| OLED 1.3" | 1 | 750 | Matrix board 5×7 cm | 2 | 25 |
| TP4056 | 1 | 90 | 3.7 V Li-ion | 2 | 180 |
| MCP3208 | 1 | 625 | Li battery holder | 1 | 150 |

**Bill 745 — ~7 Jun 2026 — ₨3,885**

| Item | Qty | Rate | Item | Qty | Rate |
|---|---|---|---|---|---|
| Waterproof ultrasonic sensor | 1 | 950 | 2-channel relay | 2 | 250 |
| Ultrasonic sensor | 1 | 165 | Terminal block, 3-pin | 2 | 15 |
| Heatshrink tube 6 mm | 2 m | 30 | Raspberry Pi camera | 1 | 900 |
| Crocodile clips | 5 sets | 30 | Switch | 10 | 30 |
| Mic module | 1 | 150 | Buzzer | 1 | 30 |
| "Boom/boost module" | 1 | 650 | | | |

**Bill 884 — 11 Sep 2026 (083-5-26) — ₨890**

| Item | Qty | Rate | Item | Qty | Rate |
|---|---|---|---|---|---|
| Female header | 4 | 15 | MCP3208 | 1 | 650 |
| Capacitor (1000 µF) | 2 | 15 | Terminal block, 3-pin | 6 | 20 |
| Resistor (4k7) | 20 | 1 | Ceramic cap (100 nF) | 10 | 1 |

⚠ **₨15 each is single-row pricing** — a 2×20 dual-row female header is normally ₨50–80.
These are most likely 1×40 single-row strips, which work: two 1×20 pieces in adjacent
perfboard rows sit 2.54 mm apart and *are* a 2×20 header. Test that two strips seat
shoulder-to-shoulder in adjacent rows before soldering — some bodies are wider than 2.54 mm.

**Not stocked at SLT (11 Sep 2026):** CR2032/LIR2032 cell, and the 15-pin camera FFC.
The cell is available anywhere; the ribbon needs an online order (§16.1).

**What the inventory changes:**
- **Spares exist** for MQ-7, MQ-135, DHT22 and — since bill 884 — **MCP3208**. There is still
  **no spare BMP280** (U7).
- **Two 10 × 15 cm matrix boards, plus two 5 × 7 cm.** The corrected box takes a 100 × 150
  board flat, so **neither needs cutting** — build on the blank one and keep the rest.
- **A multimeter is on hand**, so F1 can be settled by measurement, not inference.
- ✅ **Terminals settled.** Bill 884 adds 6× 3-pin to the 2 on hand — 24 ways against the 14
  needed (8 + 4 + 2). Off the shopping list.
- **Unused and worth fitting:** raindrop ×2 (CH3 free), LDR ×4 (CH4 free).
- **Unused, no role here:** PIR, mic, buzzer, relays, switches. The *waterproof ultrasonic*
  is interesting later as a **snow-depth or water-level** channel — a Himalayan-transect
  story, not a Lalitpur-rooftop one.
- ✅ **U4 closed by purchase.** Rather than sort 30 unknown resistors, bill 884 buys 20
  known 4k7 at ₨1 each. Still meter them, and pick *matched pairs* for the MQ dividers —
  `MQ_DIVIDER_RATIO` (`sensors/config.py:26`) is `(R1+R2)/R2`, so put the measured value in
  rather than assuming 2.0.
- ❌ **U5 RE-OPENED 2026-09-13: it is NOT a buck.** The chip reads **`LM2587S`** — a *boost*
  (step-up) regulator. On the bench with 12 V in, it read 30 V and could not be trimmed below
  ~11.2 V (input minus a diode drop), which is boost behaviour. The 2026-09-11 "LM2596"
  identification was wrong and was never measured. **It cannot make 5 V from 9 or 12 V.**
  So 12 V→5 V is available on the bench already. **Set its output to 5.00 V on the meter
  before connecting anything** — these ship at arbitrary voltages, often 15–20 V, which would
  destroy both MQ modules. Honest rating is ~2 A; fit a heatsink.
- **Power needs no purchase.** A 5 V 2 A adapter feeds the Pi; a 9 V adapter through the
  LM2596 at 5.00 V feeds the MQ heaters alone, grounds common at the board. That is §8.3's
  split rail, built from parts on hand.

### Generated drawings and renders

Index with thumbnails: [`docs/README.md`](docs/README.md).

| Sheet | Path |
|---|---|
| 1 · Wiring schematic | [`docs/drawings/schematic.svg`](docs/drawings/schematic.svg) |
| 2 · Perfboard placement | [`docs/drawings/perfboard.svg`](docs/drawings/perfboard.svg) |
| 3 · Header pinout + cable map | [`docs/drawings/pinout.svg`](docs/drawings/pinout.svg) |
| 4 · Lid layout, dimensioned | [`docs/drawings/lid-layout.svg`](docs/drawings/lid-layout.svg) |
| Whole station on the roof | [`docs/cad/renders/site.png`](docs/cad/renders/site.png) |
| Box as it stands (hood table, tower) | [`docs/cad/renders/service.png`](docs/cad/renders/service.png) |
| Section through the tower (exact, 2D) | [`docs/cad/renders/section2d.png`](docs/cad/renders/section2d.png) |
| Exploded / plan / mast / tower / pod / shield | `docs/cad/renders/*.png` |
| Lid placement template (1:1) | [`docs/cad/templates/roofbox_lid.svg`](docs/cad/templates/roofbox_lid.svg) |
| Side-wall gland template (1:1) | [`docs/cad/templates/roofbox_drill_wall.svg`](docs/cad/templates/roofbox_drill_wall.svg) |

---

## 6. Artifacts and how to regenerate them

Everything generated lives under `docs/` and is indexed in [`docs/README.md`](docs/README.md).

| Artifact | Path | What it is |
|---|---|---|
| Build sheet | this document | faults, power, protoboard rework, CAT5e cabling, sensor placement, commissioning gates |
| Sheets 1–4 | `docs/drawings/*.svg` | schematic · perfboard placement · pinout + cable map · lid layout. **One net list feeds all of them** |
| Drawing generator | `scripts/gen_drawings.py` | **Edit the net list here, not the SVGs.** Sheet 4 reads its positions from the CAD file |
| Box + site CAD | `docs/cad/roofbox.scad` | the real container, Pi 3B+, HAT, buck, camera tower, hood table, mast, vase, cable runs. Parts listed in its header |
| Numeric checks | `docs/cad/roofbox_check.py` | XY clash, usable field, stack height, sky clearance, ribbon reach, lid penetrations, gland spacing, **cable cut lengths** |
| Renders + templates | `docs/cad/renders/`, `docs/cad/templates/` | PNG views; 1:1 SVG templates in mm |
| Bench page | `docs/bench.html` | all four sheets + the key renders + the §14 gates on one page for a phone at the bench |
| Station-side tools | `scripts/pi_config.sh`, `scripts/gate_check.py` | apply §11 · run the §14 gates |

Regenerate:
```bash
python3 scripts/gen_drawings.py      # sheets 1-4 + docs/bench.html
docs/cad/render.sh                   # every render + template, then the checks (~2 min)
```

> The CAD was moved here from `../iesh-production-reference/03-enclosure/cad/` (which is
> **not a git repository** — a pointer file `ROOFBOX-MOVED.md` was left there). `edu.scad`
> / `sci.scad` there are the product enclosures and stay put. That folder's
> `render_views.py` had a stale absolute path; fixed on disk 2026-09-03, unversioned.

---

## 7. The one design decision everything follows from

> **The box is a dry electronics vault. Every environmental sensor lives outside it.**

A sealed 170 mm box on a Lalitpur rooftop in September sun runs 45–55 °C inside. A
DHT22 in there measures *the box*, not the air — that single mistake is what makes most
DIY weather stations produce numbers that look fine and mean nothing. The MQ heaters
would also be reading their own exhaust.

So the unit is three physically separate things, not one box:

```
      [ radiation shield ]          hood (sun + rain)
       DHT22 air T / RH          ╔══════════════════╗
              │                  ║  ▲ fisheye sees  ║
   ┌──────────┴──────────┐       ╚═══════▲══════════╝
   │  SENSOR MAST        │           ┌───┴───┐  ← lid = chassis plate
   │   [ gas pod, MQ×2 ] │           │ Pi+HAT│     camera bolted under it
   │   [ LDR + raindrop ]│           │ buck  │     (110 mm ribbon reaches)
   └──────────┬──────────┘           │  BOX  │  130 base / 170 top × 230, LID UP
              │  CAT5e ─────────────▶│       │
              └──────────────────────│ ▣ glands in the SIDE WALL, low
                                     └───┬───┘
                        [ vase: DS18B20 + capacitive probe ]
```

**Orientation is forced by the camera ribbon, not chosen.** The ribbon on hand is
**110 mm** ([photo](docs/reference-photos/04-camera-and-clipon-fisheye.jpg)). An all-sky camera must look up, and the Pi must be within a ribbon's length
of it — so the camera sits in the lid with the Pi bolted directly beneath. Mounting the
box inverted (lid down) would put the Pi 180 mm from the sky-facing end and the ribbon
would not reach. A 300–500 mm FFC would free the choice; with this one, **lid up** is the
only layout that works.

**The hood is therefore mandatory, not a nice-to-have.** Lid-up means rain can sit on the
gasket, so the hood keeps direct rain off the seal. It is needed for solar gain anyway — a
sealed box in Kathmandu sun runs 45–55 °C inside — so one part solves both. It stands off
on legs: an air gap is what makes a shade work, and a hood touching the lid just conducts
the heat straight in. **The legs stand on the paving tile, not on the lid** (§16.8) — a
198 mm plate on four 20 mm PVC legs straddling the box, so nothing bolts through the seal
and the box lifts straight out from under it.

**The camera rides a printed tower up through the hood.** A fisheye flush in the lid under
a 32 mm hood sees a ~75° cone, not the sky. `cam_tower` (`docs/cad/`) carries the lens
6 mm proud of the hood plate; the ribbon path is ~90 mm of the 110 mm on hand.

**Cable glands move off the lid into the box side wall, low down**, so nothing faces the
sky. Drip loops below each.

**The fisheye lens is the window.** It's a [clip-on phone lens](docs/reference-photos/04-camera-and-clipon-fisheye.jpg): the element with its
knurled ring unscrews from the clip arm, and that ring beds into a sealed boss in the lid.
This is better than cutting an acrylic window — the camera isn't also shooting through an
extra sheet that would add reflections and haze. Vignetting into a circular image is
exactly what an all-sky camera wants.

**Build on a removable sled.** A flat plate (3 mm acrylic, ply, or ABS offcut) carrying
Pi + HAT + terminal strip, which drops into the box as a unit. Assembling inside a
box is miserable; assembling on the bench and then inserting is not. This is the
single biggest buildability win available.

---

## 8. Power — fix this before anything else

F1 is upstream of F2. Rebuilding the wiring on a sagging 5 V rail just produces
better-looking intermittency.

### Measure first, don't infer
You have a multimeter. With the station running and both MQ heaters on, measure between
**GPIO pin 2 or 4 (+5 V)** and **pin 6 (GND)**:

| Reading | Verdict |
|---|---|
| ≥ 5.00 V | supply fine — look elsewhere |
| 4.75–5.00 V | marginal; will fail under camera/WiFi peaks |
| < 4.75 V | this is F1. Fix the supply. |

The Pi's own flag is the other half of the same test:
```bash
vcgencmd get_throttled     # want 0x0 — anything with bit 0 or 2 set is live undervoltage
```

### The likely culprit is the cable, not the adapter
A thin micro-USB lead drops 0.5 V+ at 2 A no matter what the brick is rated for. In
order of what actually fixes it:

1. **Short, thick micro-USB cable** (≤ 1 m, 20 AWG power conductors). Cheapest test, and
   often the whole answer.
2. **A genuine 5 V / 3 A supply.** Not a power bank — a power bank's regulator sags under
   the MQ heater step load and many cut out at low draw.
3. **Feed the MQ heaters from their own 5 V rail, not through the Pi.** MQ-7 + MQ-135
   heaters are ~300–400 mA continuously and they switch; that step load on a shared rail
   is exactly what tips a marginal supply over. Common ground, separate +5 V. This is
   also what `../iesh-production-reference/01-hardware/04-power-architecture.md` does.

### Roof mains, and where the adapter goes
A wall-socket line is being run up to the roof, so there is mains at the station. That
settles the topology, with one caution: **no mains inside the instrument box.** A 240 V
adapter in a sealed plastic food container on a roof is not something to sign off.

So:

```
  indoor UPS (12 V lead-acid) ──AC──▶ roof socket ──▶ adapter in its OWN
                                                       small junction box
                                                            │ low voltage
                                                            ▼
                                                      gland ─▶ instrument box
```

- **Adapter lives outside the instrument box** — its own small weatherproof junction box,
  or under the hood, or in whatever housing the roof socket already has.
- **Only low voltage crosses into the vault.** Either 5 V on a short thick run, or 12 V
  into a small buck module on the chassis plate. Prefer **12 V + buck** if the adapter
  ends up more than about a metre away: 12 V draws ~2.4× less current for the same power,
  so the run loses far less voltage — and voltage drop *is* fault F1.
- **The UPS stays indoors**, feeding the roof circuit. That gives ride-through through
  Nepal's grid with no lead-acid battery sitting on a hot roof, which is where you want
  it: heat is what kills lead-acid.

> Do **not** wire the LT3652 power-mgmt-v1 board into this deployment. Its input is
> **18–24 V**, not 12 V, and it belongs to the production build.

---

## 9. Wiring — the protoboard HAT

> 🔧 **At the bench, work from [`BOARD-BUILD.md`](BOARD-BUILD.md)** — the live working doc for
> this build: the board's own A–Z/A′–J′ × 48→1 coordinates, the orientation anchors, the
> layout map, the power topology as settled, and the steps with their gates and tick boxes.
> This section is the reasoning behind it; that one is what you hold the iron next to.

Chosen over hardened jumpers because F2 *is* the joint count. Every dupont pair is a
crimp plus a friction fit; soldering replaces each with one joint. Off-board sensors keep
one deliberate, serviceable connection each, via screw terminals.

### Keep what is already soldered
The existing board already has the **MCP3208 soldered with its power lines** — that part is
already the right thing and there is no reason to redo it. The rework is *not* a rebuild:

| Keep | Replace |
|---|---|
| The soldered MCP3208 and its 3.3 V / GND / VREF lines | The **jumper-to-jumper chains between modules** — dupont plugged into dupont, held with masking tape. This is the F2 mechanism. |
| Any decoupling already fitted | Bare-wire twists and taped joints, wherever they carry a bus signal |
| The board outline, if it fits the sled | Unlabelled connections — every terminal gets an indelible-pen label |

So the job is: **cut the inter-module jumper chains out and replace each with a single
soldered run**, then terminate every *off-board* sensor at a screw terminal so it stays
serviceable. Nothing that is already a solder joint needs touching.

**The board does not need cutting.** The corrected box (§5: 170 mm across the top) takes a
full **100 × 150 mm** board flat in its upper ~115 mm, and a HAT is allowed to overhang the
Pi. Build on the *blank* 10 × 15 board rather than reworking the old one — stripping 25 wire
stubs and a field of solder blobs off heat-cycled pads is more work than starting clean.

To recover the MCP3208 from the old board without risking the IC: cut the old board into a
small island around it (the old board is disposable), then snip the island *between* the two
pin rows. Each pin is then near-free-standing and lifts with one touch of the iron.

The 65 × 70 `carrier-hat-v1` footprint is therefore **not** matched by this build. The zone
layout still transfers to the real PCB; the outline does not. That is the right trade for a
DIY station (§16.7).

### Pin map (from `sensors/config.py` — the single source of truth)

| Signal | GPIO | Header pin | Goes to |
|---|---|---|---|
| 3.3 V | — | 1, 17 | MCP3208 VDD+VREF, BMP280, OLED, DS3231, pull-ups, **DHT22**, soil probes, raindrop |
| 5 V | — | 2, 4 | MQ heaters only *(prefer a separate rail — §8)*. The DHT22 runs on 3.3 V on purpose: keeps its DATA at 3.3 V logic and off the heater rail |
| GND | — | 6, 9, 14, 20, 25, 30, 34, 39 | everything |
| I2C SDA | GPIO2 | 3 | BMP280 `0x76`, OLED `0x3C`, DS3231 `0x68` |
| I2C SCL | GPIO3 | 5 | same three |
| 1-Wire | GPIO4 | 7 | DS18B20 data (+ 4.7 kΩ to 3.3 V) |
| DHT22 data | GPIO23 | 16 | DHT22 (+ 4.7–10 kΩ to 3.3 V) |
| SPI MOSI | GPIO10 | 19 | MCP3208 pin 11 (Din) |
| SPI MISO | GPIO9 | 21 | MCP3208 pin 12 (Dout) |
| SPI SCLK | GPIO11 | 23 | MCP3208 pin 13 (CLK) |
| SPI CE0 | GPIO8 | 24 | MCP3208 pin 10 (CS/SHDN) |

### MCP3208 (16-pin DIP)
```
 CH0  1 ─┬─ 16  VDD    → 3.3 V
 CH1  2  │   15  VREF   → 3.3 V
 CH2  3  │   14  AGND   → GND
 CH3  4  │   13  CLK    → GPIO11 / pin 23
 CH4  5  │   12  Dout   → GPIO9  / pin 21
 CH5  6  │   11  Din    → GPIO10 / pin 19
 CH6  7  │   10  CS     → GPIO8  / pin 24
 CH7  8 ─┴─   9  DGND   → GND

 CH0 ← MQ-7 divider      CH1 ← MQ-135 divider      CH2 ← soil moisture AOUT
```

### The passives that are not optional

| Part | Where | Why |
|---|---|---|
| **4.7 kΩ** | DS18B20 DATA → 3.3 V | 1-Wire does not work without it. Its absence is a candidate cause of the DS18B20 dropping off the bus (F2). |
| **4.7 kΩ ×2 per MQ** | AOUT → node → GND, node → CHx | The 2:1 divider that keeps the MQ's 0–5 V out of a 3.3 V ADC input. `MQ_DIVIDER_RATIO = 2.0` in config depends on both being equal — measure them, don't trust the band. |
| **4.7–10 kΩ** | DHT22 DATA → 3.3 V | Bare DHT22 modules need one; 3-pin breakout boards already have it. Check yours before adding a second. |
| **100 nF** | across each sensor's supply pins | Local decoupling. |
| **470–1000 µF** | on the 5 V rail beside the MQ sensors | Absorbs the heater step load that destabilises the rail (F1/F2). |

> **Do not add I2C pull-ups.** The Pi 3B+ already has 1.8 kΩ on GPIO2/GPIO3. More
> resistors in parallel over-pull the bus. The right I2C fix is **shorter wires and a
> slower clock** — see §11.1.

### Layout discipline on the board
- Keep the I2C run **as short as physically possible** and route SDA/SCL side by side
  with a ground trace between or beside them.
- Solid ground: bond every ground pad into one continuous strip, tied to at least two Pi
  GND pins. A shared thin ground return is a classic source of exactly F2.
- Analogue apart from digital: put MCP3208 and the MQ dividers at the opposite end of the
  board from the DHT22 and the I2C header.
- **Label every screw terminal on the board itself** with an indelible pen. The masking
  tape flags on the cardboard version are the reason a rebuild is needed at all.

### Screw terminals
Needed: mast cable (8), soil cable (4), power in (2) — **14 ways**. Bill 884 adds 6× 3-pin
to the 2 on hand, so **24 ways are available** — settled.
Sheet 3 ([`pinout.svg`](docs/drawings/pinout.svg)) traces every way to its CAT5e core and
to the sensor pin it is soldered to at the far end.

---


## 10. How the sensors actually connect

The rule: **no sensor gets its own cable run.** Two multi-core cables leave the box — one
up the mast, one down to the vase — and each sensor taps the cable at its own end. That
takes the box from six penetrations to **two**, which is the difference between a box that
stays dry and one that doesn't.

### Use CAT5e for both runs
Cheap, sold on every corner in Kathmandu, 8 conductors, and the twisted pairs are exactly
what you want: each supply travels twisted with its own return, which is what keeps a
switching MQ heater from injecting noise into an analogue line running beside it. You
already have a length of it (the yellow cable in the bench photo).

Convention on both cables: the **solid** core of a pair carries supply or signal, the
**white-striped** core is that pair's return — so every current travels twisted with its
own return. Terminal way numbers match sheets 1 and 3.

**Mast cable — 8 conductors, all 8 used:**

| Way | Core | Carries | Solder to, at the mast end |
|---|---|---|---|
| 1 | orange | **+5 V** | MQ-7 VCC + MQ-135 VCC |
| 2 | orange-white | GND | MQ-7 GND + MQ-135 GND |
| 3 | green | **+3.3 V** | DHT22 VCC + raindrop VCC |
| 4 | green-white | GND | DHT22 GND + raindrop GND |
| 5 | blue | **DHT22 DATA** → GPIO23 | DHT22 DATA |
| 6 | blue-white | **raindrop AO** → MCP3208 CH3 | raindrop board AO *(optional)* |
| 7 | brown | **MQ-7 AOUT** → CH0 (via R3/R4) | MQ-7 AOUT |
| 8 | brown-white | **MQ-135 AOUT** → CH1 (via R5/R6) | MQ-135 AOUT |

The heaters get their own pair because they are the only real current (~150 mA each). The
raindrop board at 3.3 V already outputs 0–3.3 V, so CH3 needs no divider. An **LDR** would
need a ninth core: if you fit one, run a second short CAT5e rather than doubling up a
conductor. Cable is cheaper than a debugging trip to the roof.

**Soil cable — 4 of 8 conductors to the vase:**

| Way | Core | Carries | Solder to, at the vase |
|---|---|---|---|
| 1 | orange | **+3.3 V** | DS18B20 red + soil probe VCC |
| 2 | orange-white | GND | DS18B20 black + soil probe GND |
| 3 | blue | **DS18B20 DATA** → GPIO4 | DS18B20 yellow |
| 4 | green | **soil moisture AOUT** → MCP3208 CH2 | soil probe AOUT |

Cut lengths, from the site layout in the CAD (`roofbox_check.py` prints them): **mast
2.4 m · soil 1.4 m · power 0.8 m**, slack and drip loops included.

Both probes sit in the same vase, so one cable is correct — and it keeps soil temperature
and soil moisture describing the same body of soil.

### Where the joints are allowed to be
Every cable has exactly **two** joint locations, and nothing in between:

```
  sensor ──[solder + heatshrink]── CAT5e ──[gland]── screw terminal ── protoboard
           ^                                         ^
           at the sensor, potted                     inside the dry vault
```

- **At the sensor end: solder, then heatshrink.** You have 2 m of 6 mm heatshrink. This
  end is outdoors and gets weather, so it must not be a connector — solder it and seal it.
  Slide the heatshrink on *before* you solder.
- **At the box end: a screw terminal.** This is the one connection meant to be undone, for
  servicing. It lives inside the vault where it's dry.
- **Nothing taped, nowhere.** The masking-tape joints in the bench photo are the fault.

### Strain relief and drip loops — not optional
- **Clamp each cable** with a zip tie on an **adhesive tie mount** bonded to the lid
  underside (positions on sheet 4). Pull on the cable and the tie takes the load, never
  the screw terminal. No holes in the lid for this.
- **Drip loop below every gland**: the cable must go *down* out of the gland and hang below
  it before rising. Water runs to the bottom of the loop and drips off. The glands are
  low in the side wall (§7), 32 mm above the box base, so the loop hangs on the tile.
- Leave ~200 mm of slack inside the box. Tight cabling makes servicing on a roof
  unpleasant and pulls joints apart.

### One thing to check with the multimeter before closing the box
With the mast cable connected and everything running, measure **+5 V at the MQ sensor end
of the cable**, not at the Pi. If it reads below 4.8 V there, the heaters are running cold
and the MQ readings drift — double up pair 1's conductors or shorten the run.

---

## 11. Pi configuration changes

All three are edits on the device; none is optional. **`sudo scripts/pi_config.sh` applies
11.1–11.3 in one go** (`--dry-run` first to see the diff; it backs up `config.txt`), and
`python3 scripts/gate_check.py` confirms them afterwards.

### 11.1 Slow the I2C bus — 400 kHz over unshielded wire is the F2 mechanism
`/boot/firmware/config.txt` currently has `dtparam=i2c_arm_baudrate=400000`. Nothing on
this bus needs 400 kHz; a 60-second log interval is happy at 100 kHz, and the noise
margin roughly quadruples.
```
dtparam=i2c_arm_baudrate=100000
```

### 11.2 Give the OS a real clock (fixes F4)
```
dtoverlay=i2c-rtc,ds3231
```
Then, **and this is the part v0.1 missed** — fit a fresh CR2032/LIR2032 in the DS3231
(the current cell is flat: the chip reads 2000-01-05), and seed it once from NTP:
```bash
sudo hwclock -w          # system (NTP-correct) -> DS3231
sudo hwclock -r          # read back; must show real local time
```
With the overlay loaded, `/dev/rtc0` exists and the kernel restores time at boot *before*
`hics-core` starts — so rows logged during a post-outage, pre-NTP window carry correct
timestamps instead of poisoning the server's dedup key forever.

> Note the ordering hazard: `hics-*.service` already start after `network.target`, but the
> RTC must be read before them. The kernel overlay handles this; the userspace
> `RTC.sync_from_system()` in `sensors/rtc.py` does not and never did.

### 11.3 Resolve the camera overlay conflict (F6)
`config.txt` carries both `camera_auto_detect=1` and `dtoverlay=ov5647`. Keep one. With
the camera physically removed, **comment out `dtoverlay=ov5647`** so the driver stops
retrying a chip that isn't there and filling the log with `i2c read error`. Restore it (or
rely on auto-detect alone) when the camera goes into its own housing.

### 11.4 Interface config that is now wrong for this board
`sensors/config.py` says `INTERNET_IFACE = 'wlan1'` and `HOTSPOT_IFACE = 'wlan0'`. A Pi
3B+ has **one** wlan. There is no `wlan1`, so the `IESH_Hub` hotspot the README describes
does not exist on this unit. For the Lalitpur deployment the station joins home WiFi on
`wlan0` (currently `liverpool08_2.4`, signal 70) and that is sufficient — but the README's
hotspot section does not describe this station and should say so.

---

## 12. Sensor placement, one by one

| Sensor | Where it goes | Why / gotcha |
|---|---|---|
| **DHT22** air T/RH | Mast, inside a **radiation shield**, ≥ 300 mm clear of the box and ≥ 1 m above the roof deck | Non-negotiable. In the box it reads the box; in direct sun it reads the sun. Shield = 4–6 stacked plates with air gaps — cheap plastic plant-pot saucers, inverted and spaced on a bolt, work genuinely well and cost almost nothing. |
| **BMP280** pressure | **Inside**, on the HAT | Pressure equalises through any small opening, so it can stay in the vault — but the vault must not be *perfectly* sealed or thermal swing gives a false offset. One 2 mm hole on the **downward** face, behind a scrap of PTFE tape or foam, is enough. Currently **absent from the I2C bus (`0x76`)** — reconnect it and re-scan; you have no spare, so if it stays dead it needs replacing. |
| **MQ-7** CO, **MQ-135** gas | Mast, in a **downward-facing vented pod** | Must see ambient air, and they self-heat ~350 mW each — in the vault they'd read their own exhaust and cook the Pi. Down-facing vents keep rain out. Stay a **labelled proxy**, not a calibrated measurement (hics-docs G9). |
| **DS18B20** soil T | **Buried in the planter**, 100 mm deep | Waterproof stainless probe version is already suitable. Needs the 4.7 kΩ pull-up. |
| **Capacitive soil moisture** | **Buried in the planter**, blade vertical | Only meaningful *if there is soil* — see the note below. **Pot the top ~25 mm of the board in epoxy or silicone**; the v1.2 boards leave their electronics exposed above the blade and die within weeks outdoors. Re-run `scripts/calibrate_soil.py` in the actual planter soil — the current `SOIL_DRY = 4021` / `SOIL_WET = 1673` came from a different medium. |
| **DS3231** RTC | Inside, on the HAT | **Fit a fresh coin cell.** The one in it is flat (§11.2). |
| **OLED** | Inside, or omit | A classroom feature with no outdoor purpose. Keep it on the sled for bench commissioning; don't cut a window for it. |
| **Pi camera** (all-sky) | **On a printed tower through the hood**, fisheye ring under a lip at the top, board on a ledge just behind it | The tower is the only lid penetration and the camera is deferred (F6) — so **do not cut the lid yet.** When it comes: print `cam_tower` from `docs/cad/roofbox.scad`, test-fit the real fisheye (U2/U3 — `FE_BACK` is found by trial, so print the ledge shimmable), then cut the bore on sheet 4. The lens is the window (§7). |
| **Raindrop ×2** *(unused)* | Mast, plate angled ~30° | Genuinely useful, and rain is the one channel a Kathmandu monsoon story wants. Needs an ADC channel — **CH3 is free**. |
| **LDR ×4** *(unused)* | Mast, facing up | Cheap daylight/cloud proxy, and it pairs with the sky camera later. **CH4 free.** |
| **PIR, ultrasonic, relay, mic, buzzer** | Not in this build | Real parts, no role in a rooftop climate station. The waterproof ultrasonic is interesting later as a **snow-depth or water-level** channel — that is a Himalayan-transect story, not a Lalitpur-rooftop one. |

### The soil question — settled
The concern was that soil sensors are pointless outdoors. They are pointless *without
soil*, and the ADC confirms the probe is currently in air: raw **4021** is precisely the
`SOIL_DRY` calibration point.

**There are planted vases on the roof, so this resolves itself:** put both probes into one
of them and the channels become real. Choose the **largest vase** available — a small pot
dries out and re-wets far faster than ground soil, so a shallow one produces a
spiky, unrepresentative moisture trace. Bury the DS18B20 at ~100 mm and the capacitive
blade vertically alongside it, in the same vase, so soil temperature and soil moisture
describe the same body of soil.

This turns the two dead channels into the richest pair on the station — soil moisture
against rainfall against air temperature is a genuine agronomy dataset, it directly serves
the AIT framing, and it demos far better than a flatlined channel. It also means the
raindrop sensors (mast, way 6) are worth fitting: rain → soil moisture response is the one
relationship on this station that is visible within a single afternoon.

What would not be defensible is leaving a probe in air and logging the number it produces.

---

### CAD, and the one part that needs printing

`docs/cad/roofbox.scad` models the **real container with the real Pi 3B+** (the product
library models a 4B), the HAT, the buck, the camera tower, the hood table, and — at 1:1 —
the whole site: tile, mast with shield and gas pod, vase with probes, junction box and the
three cable runs. It exists to fit-check, place the sensors, argue about distances, and
emit the templates — not to be a production enclosure.

```bash
docs/cad/render.sh                                          # every view + template + checks
openscad -o tower.stl -D 'part="cam_tower"' docs/cad/roofbox.scad   # the one printed part
```

Views: `site` · `service` · `exploded` · `plan` · `mast` · `cam_tower` · `gas_pod` ·
`shield` · `container`; exact 2D sections `section2d` · `tower2d`; 1:1 templates `lid` ·
`drill_wall`. Renders in `docs/cad/renders/`, templates in `docs/cad/templates/`.

**Almost nothing is fabricated.** The scope is a working station, not a production build:

| Part | How |
|---|---|
| Chassis plate | **The actual lid, with nothing drilled.** Standoffs for Pi and buck are **bonded** to its underside (epoxy or neutral-cure silicone on M2.5 brass standoffs); cable ties go on adhesive mounts. Sheet 4 / `templates/roofbox_lid.svg` give the positions. |
| `cam_tower` | **Print this one — later.** It holds the fisheye-to-sensor spacing, the only dimension that needs accuracy, and it is the only thing that ever cuts the lid. |
| Hood | A 198 mm square of aluminium or corrugated plastic on four 20 mm PVC legs standing on the tile — a table over the box. Aperture for the tower. `hood` is the reference geometry. |
| Gas pod | Any small vented tub, open downward, big enough for two 32 × 20 mm MQ modules side by side. `gas_pod` is printable if convenient. |
| Radiation shield | **Five inverted ~100 mm plant-pot saucers on a bolt** with spacers. Works genuinely well. `shield` is printable if preferred. |
| Stand | A 300 mm concrete paving tile. Heavy, flat, off the deck; box and hood legs stand on it, so the whole unit moves as one. |

**Fit is verified numerically, not by eye.** `roofbox_check.py` asserts: no two lid
footprints overlap; everything inside the ±58 mm usable field; stack 44.5 mm in 178 mm;
fisheye lip 6 mm proud of the hood; the 110 mm ribbon reaches (~90 mm path); hood legs
clear the lid; the tower bore is the lid's only through-cut; gland spacing; and it prints
the cable cut lengths. It has already caught a real overlap, a tie mount outside the field
and hood legs 2 mm into the lid.

Three dimensions in the file are marked **ASSUMPTION** and read off photographs. Measure
them before printing `cam_tower`, or it will not fit:

- `FE_RING_D` / `FE_RING_H` — the fisheye's knurled ring, est. Ø23 × 9 mm
- `FE_BACK` — lens rear to sensor front, est. 3 mm. **This is the one to find by trial**;
  clip-on fisheyes expect 2–4 mm off a phone lens. Print the ledge shimmable.
- `BOX_TOP` / `RIM_W` — the container's taper and flange

---

## 13. Shopping list

Everything not already in the inventory — transcribed in
§5.

| Item | Qty | Why | Where |
|---|---|---|---|
| ~~Short thick micro-USB cable~~ | — | ✅ **F1 reported resolved 2026-09-11.** The board, not the Pi, is now the power entry — no micro-USB in the low-voltage path at all | — |
| 5 V / 3 A supply | *optional* | **not needed:** a 5 V 2 A adapter feeds the Pi and a 9 V adapter through the LM2596 at 5.00 V feeds the MQ heaters alone, grounds common — §8.3's split rail from parts on hand. Buy only to simplify to one supply | SLT |
| Hook-up wire, 22 AWG stranded, 3–4 colours | 1 spool ea | you have jumper sets but no bulk wire | SLT |
| ~~Screw terminal blocks~~ | — | ✅ **bought, bill 884** — 6× 3-pin | — |
| ~~Resistors 4.7 kΩ~~ | — | ✅ **bought, bill 884** — 20 off | — |
| ~~Capacitors 100 nF / 1000 µF~~ | — | ✅ **bought, bill 884** — 10 / 2 | — |
| **2×20 female header (or 2× 1×20 strips)** | 1–2 | ✅ **bought, bill 884** — 4 strips. **This was missing from this list and is the one part that blocks the build**: without it, board-to-Pi is a wire bundle, which is fault F2 | SLT |
| PG7 or PG9 cable glands | 3 | sealed entries — drilled in the box **side wall**, low down, never the lid. **PG7 needs a 12.5 mm hole, PG9 15.2 mm** (the *thread*, not the cable). Rubber grommet + neutral-cure silicone is an acceptable substitute | hardware shop |
| Small weatherproof junction box | 1 | houses the mains adapter **outside** the instrument box | electrical shop |
| ~~12 V→5 V buck module (LM2596)~~ | ~₨150–200 | **Not buying — decided 2026-09-13.** The module on hand is an LM2587S boost (U5). The build runs on 5 V adapters only; see `BOARD-BUILD.md` §2. Revisit only if F1 cannot be closed without it | SLT |
| Neutral-cure silicone | 1 tube | **neutral-cure, not acetoxy** — acetoxy silicone corrodes copper and pins | hardware shop |
| M2.5 brass standoffs + screws | 1 set | Pi and buck to the lid underside — **bonded**, not bolted through | SLT |
| Adhesive zip-tie mounts, 19 mm | 4 | cable strain relief on the lid underside, no holes | SLT / hardware |
| Concrete paving tile | 1 | the stand: box and hood legs sit on it. **≈400 mm for the corrected box** — the legs straddle a wider body now | hardware shop |
| 15-pin camera FFC, 300–500 mm | 1 | frees the lid-up constraint entirely (§16.1). **Not stocked at SLT — order online.** Must be a Pi camera cable: 15-pin, 1.0 mm pitch, contacts on *opposite* faces at the two ends | online |
| Aluminium or corrugated-plastic sheet | 1 | the hood plate. **≈250 mm sq for the corrected 170 mm box — buy 300 mm and cut to fit** once the CAD is regenerated | hardware shop |
| Plant-pot saucers ~100 mm | 5 | radiation shield plates | any nursery |
| — | — | *planter not needed: the roof already has planted vases* | — |
| **CR2032 / LIR2032** | 1 | the DS3231's cell is flat — **§14 gate 2 is blocked without it.** **Not stocked at SLT**; any general shop has them | any |
| 20 mm PVC pipe + clamps | **~3 m** | 1.5 m sensor mast + 4 hood legs. **Legs ≈280 mm, not 220** — the box is 230 mm tall, not 180. Buy long and cut | hardware shop |
| Desiccant sachets | 2–3 | condensation inside the vault | any |
| Epoxy or potting compound | small | pot the soil probe's exposed top | hardware shop |

---

## 14. Build order

Each step is gated: don't proceed while the previous one fails. The gates exist because
F2's symptoms are intermittent, and an intermittent fault found *after* the box is closed
costs a rooftop trip.

1. **Fix power. Verify `vcgencmd get_throttled` reads `0x0`** and stays there for an hour
   with both MQ heaters running. *Nothing below is meaningful until this passes.*
2. **Apply the `config.txt` changes** — `sudo scripts/pi_config.sh` (§11.1–11.3) — fit the
   DS3231 coin cell, reboot, `sudo hwclock -w`, confirm `hwclock -r` reads correct local
   time and `/dev/rtc0` exists. `python3 scripts/gate_check.py` checks G2/G3.
3. **Rework the protoboard** (§9). Keep the soldered MCP3208; cut out the jumper-to-jumper
   chains; add R1–R6, C1, C2; fit the screw terminals. Work from the
   [placement sheet](docs/drawings/perfboard.svg) and the
   [schematic](docs/drawings/schematic.svg). Do the Pi header, ground strip and 3.3 V/5 V
   distribution first; **continuity-check every net with the multimeter before fitting any
   IC or plugging it onto the Pi.** A shorted rail on a soldered board is much less
   forgiving than on a breadboard.
4. **Restart the services** — `sudo systemctl restart hics-core hics-web` — so the fixed
   firmware from §4 is finally the code that runs. Confirm the log shows
   `Logged to DB (… rows)` with a `| NULL:` note naming exactly the channels you know are
   disconnected. **That note appearing is the gate**: it is the freshness/plausibility
   gating doing its job, and its absence means you are still running v0.1.
   `gate_check.py` G6 reads it for you.
5. **Bring up one sensor at a time on the bench**, HAT on the Pi, running
   `python3 tests/test_all.py --skip camera` after each (or `--only bmp280,oled,rtc` for
   the trio). Order: I2C trio (BMP280 / OLED / DS3231) → MCP3208 + soil → DS18B20 → DHT22
   → MQ pair. Adding them one at a time is what makes an intermittent fault attributable.
6. **Run 24 h on the bench.** Gate: `sqlite3 ~/hics-data/hics.db "SELECT date(timestamp),
   COUNT(*) FROM telemetry GROUP BY 1"` shows **~1440 rows** for a full day, and
   `get_throttled` is still `0x0`. This directly closes F5 — the station has never yet
   done this.
7. **Bond the standoffs to the lid** (sheet 4), fit the stack, **drill the three gland
   holes and the vent in one side wall** (`templates/roofbox_drill_wall.svg`, 1:1), fit
   the glands, seal. Silicone needs 24 h to cure. The lid itself gets no holes.
8. **Assemble the mast**, radiation shield and gas pod; wire to the terminals.
9. **Deploy to the roof.** Box inverted, off the deck, shaded if possible. Drip loops on
   every cable *below* the gland.
10. **Re-register the station public** on the website only after 48 h of clean data (§15).

---

## 15. Website — before going public again

The station is deliberately not in the public list right now (`/api/v1/stations/` returns
`[]`, `status` outside `active`/`maintenance`); it goes back after this round of work.
Two things to do first, both in `../../himalayansciences-web`:

**Purge the existing readings for `IESH-KMC-001`.** The garbage from F3 is already stored
server-side — the live API returns `pressure_hpa: 0.0` — and because ingest is
`get_or_create` on `(station, timestamp)`, re-POSTing corrected rows will **not** overwrite
them. Starting the public series clean is the only honest option.
⚠️ **Destructive, and it is a decision, not a step — confirm before running.**

**Then set `status = 'active'`** so it appears in the public list and on the map.

Worth knowing and leaving alone: every reading is stamped `quality_flag = 'suspect'`
because the server flags any `v0.*` firmware that way, regardless of value. That is correct
and intended for a prototype — uncalibrated sensors, an MQ proxy, unverifiable timestamps
(hics-docs G9). Do not bump `FIRMWARE_VERSION` past `v0.` to make the flag go away; it
should only move when the data is genuinely calibration-grade.

---

## 16. The rethink — what to question rather than inherit

This is the part worth reading. Everything above is defensible; some of it is only
defensible *given constraints that a small purchase would remove*.

### 16.1 The camera ribbon is driving the entire enclosure design. Buy a longer one.
The ribbon on hand is **110 mm**. That single fact forced: camera in the lid → lid must
face up → rain can sit on the gasket → a hood becomes mandatory → glands must move to the
side wall. **Lid-*down* is strictly better weatherproofing** (every penetration faces the
ground, gravity loads the seal correctly), and it was rejected only because the Pi would
then sit 180 mm from the sky-facing end.

**A 300–500 mm 15-pin FFC costs almost nothing.** Buy it, then revisit the orientation
from scratch. Do not inherit lid-up as though it were a design decision; it is a
workaround. (The tower of §16.8 makes lid-up *work*; a long ribbon would make it
*unnecessary*.)

### 16.2 Question the container itself before designing further around it
A food container is a genuinely defensible proof-of-concept housing, and "we built it with
what we had" is an honest story. But a proper **IP65 ABS junction box** is cheap in
Kathmandu, arrives with a real gasket, moulded gland bosses and mounting lugs, needs no
hood improvisation — and will photograph far better for Swiss Week. Spend thirty minutes
pricing one at Supreme Light Technology (Sanepa-2) before committing. If the container
wins on cost or timing, fine — but make it a decision, not a default.

Related: **five container dimensions in `roofbox.scad` are estimates read off photographs**
(§5). Measure before printing anything.

### 16.3 The perfboard drawing is deliberately incomplete, and you should finish it differently
`perfboard.svg` is a **zoned placement** drawing, not a hole-exact route. That was a
judgement call: the physical board already has the MCP3208 and its power lines soldered,
and authoring a hole-by-hole route without that board in hand produces a drawing that is
wrong in detail *and trusted anyway* — the worst outcome.

**The right way to finish it:** photograph the existing board top and bottom, count the
actual occupied holes, and *then* extend `scripts/gen_drawings.py` with the real routing.
The generator is structured for this — `ZONES` is already data.

### 16.4 Do not build on a sagging rail, and do not trust "it worked before"
F1 is live. "It worked fine on the power bank at the AIT pitch" and "the Pi reports
under-voltage" are **both true simultaneously** — the Pi runs while throttled, and marginal
peripherals drop off. That *is* F2. Order of attack:

1. **Short thick micro-USB cable** (≤ 1 m, 20 AWG). Often the entire answer; a thin lead
   drops 0.5 V+ at 2 A regardless of the brick's rating.
2. A genuine **5 V/3 A** supply — not a power bank.
3. **Feed the MQ heaters from their own 5 V rail**, not through the Pi. Two heaters are
   ~300–400 mA of switching load, which is what tips a marginal supply over.

Then measure with the multimeter you already have: **GPIO pin 2 or 4 (+5 V) to pin 6 (GND)**,
under load. Below 4.75 V is the fault.

### 16.5 Mains is now going to the roof — keep it out of the instrument box
A wall-socket line is being run up. That settles the topology, but **no 240 V inside a
plastic food container on a roof.** Adapter in its own small junction box; only low voltage
crosses the gland. Prefer **12 V + a small buck module** over 5 V if the adapter ends up
more than about a metre away — 12 V draws ~2.4× less current for the same power, so the run
loses far less voltage, and voltage drop *is* F1. Keep the lead-acid UPS **indoors**: heat
kills lead-acid, and a hot roof is the worst place for it.

### 16.6 What actually earns a render, and what doesn't
A 3D render of a food container told us almost nothing we didn't already know — that steer
was correct. What paid off was the **2D schematic** (it caught nothing, but it is what you
solder from) and, unexpectedly, the **numeric checks**: an XY clash test caught a real
camera-over-Pi overlap that two rounds of eyeballing renders had missed, and a unit test
caught a bug in the frozen-register gate that looked right in code review.

**Generalise that.** Prefer a computed assertion over a picture. Reserve renders for the
pitch deck, where communication is the actual job, and for verifying that a *mechanism* is
what you think it is.

The second pass confirmed it twice more: the unit test that "caught a bug in the frozen
gate" had itself enshrined a wrong rule (a steady sensor is not a frozen one — §4), and
`roofbox_check.py` caught three placement errors that the renders showed and nobody saw.
And OpenSCAD 2021's *preview* paints cut faces flat over hollows, so 3D section renders
were quietly lying; the sections are now exact 2D projections instead (§19).

### 16.8 What the audit changed in the enclosure, and why
Four things in the first CAD draft would have been built wrong:

1. **The hood blinded the camera.** A fisheye flush in the lid under a 32 mm hood with a
   49 mm aperture sees a ~75° cone. Now a printed **tower** carries the lens up through
   the hood, 6 mm proud of it.
2. **Hood legs bolted through the lid at ±65 mm — on the gasket channel.** The hood is
   now a **free-standing table** on the paving tile; nothing bolts to the lid.
3. **The lid had ~20 holes, all facing the sky**: hood legs, six zip-tie slots, eight
   standoff screws. Now: standoffs **bonded**, ties on **adhesive mounts**, and the only
   penetration is the tower bore — which waits for the camera. **Today the lid is not
   drilled at all.**
4. **`GLAND_ID = 7` was the cable size, not the hole.** A PG7 gland needs a **12.5 mm**
   hole. It would have been drilled at 7.
5. The fisheye seat was a cup open to the sky — a water trap. The ring now goes in from
   inside under a 2 mm **lip**, bedded in silicone.

### 16.7 Scope honestly: this is a robust DIY build, not a production one
The two routed PCBs (`carrier-hat-v1`, `power-mgmt-v1`) and the printed EDU/SCI enclosures
already exist in `../iesh-production-reference/` and **are** the product. This deployment is
the working proof that logs real data. Show both at Swiss Week; don't let a render imply the
container is the product, or the container imply the renders are vapour.

---

## 17. ⚠ UNVERIFIED — measure or confirm before relying on any of these

| # | Assumption | Where | How to settle it |
|---|---|---|---|
| U1 | `RIM_W = 8`, `RIM_T = 6`, `BOX_WALL = 1.8` | `roofbox.scad` | Calipers. **The body is now measured: 130 base / 170 top / 230 tall, internal (§5) — the CAD still has the old 120 × 120 × 180 and must be corrected.** Rim and wall remain estimates |
| U2 | `FE_RING_D = 23`, `FE_RING_H = 9` — the fisheye's knurled ring | `roofbox.scad` | Calipers, before printing `cam_tower` |
| U3 | `FE_BACK = 3` — fisheye rear to sensor front | `roofbox.scad` | **Trial and error.** Clip-on phone fisheyes expect 2–4 mm off a phone lens. Print the seat shimmable |
| ~~U4~~ | ~~The 30 resistors on bill 724 include 4.7 kΩ~~ | — | **Closed 2026-09-11** by buying 20 known 4k7 (bill 884). Still meter them and match the MQ pairs |
| U5 | The ₨650 "boom/boost module" | — | **Re-opened 2026-09-13: chip is `LM2587S`, a BOOST.** The 2026-09-11 "LM2596 buck" closure was wrong — it was never measured. Buy a real LM2596 |
| U6 | DHT22 breakout already carries its own pull-up | schematic R2 | Inspect the module before adding a second |
| U7 | BMP280 is merely disconnected, not dead | §2 | Reconnect and re-scan `0x76`. **There is no spare** — if dead it needs buying |
| U8 | `PSU`/`BUCK` module dimensions in the CAD | `roofbox.scad` | Measure the actual module — the buck to be bought (U5 — the module on hand is an LM2587S boost) |
| U9 | Whether the new firmware behaves correctly on real hardware | §4 | **It has not run yet.** Restart the services and watch the log; `gate_check.py` G6 |
| U10 | Tower ledge / ribbon fold geometry (`TOWER_IX/IY`, `LIP_T`, ledge width) | `roofbox.scad` | Only meaningful once the camera board and fisheye are in hand. Print one, test-fit, adjust |
| U11 | The buck module is 25 × 45 × 16 and mounts on M2 standoffs | `roofbox.scad` (U8) | Measure the module on bill 745 (U5) — the lid layout moves if it is bigger |
| U12 | The container lid accepts bonded standoffs (PP surface) | §12 | Scuff + epoxy on a test patch first; PP is a poor glue surface. Fallback: through-bolt with sealed heads |

---

## 18. Open decisions — not for an agent to make alone

1. **Purge the existing website readings for `IESH-KMC-001`?** The F3 garbage is already
   stored server-side (the live API returns `pressure_hpa: 0.0`), and because ingest is
   `get_or_create` on `(station, timestamp)`, re-POSTing corrected rows **will not**
   overwrite them. Starting the public series clean looks like the only honest option — but
   it is **destructive and irreversible. Confirm with Pawan before running anything.**
2. **`git init` the `iesh-production-reference` folder?** See §6 — the roofbox CAD no longer depends on it, but the product CAD there is still unversioned.
3. **Container or IP65 junction box?** See §16.2.
4. **Buy the longer camera ribbon and redo the orientation?** See §16.1.
5. **Bump `FIRMWARE_VERSION` past `v0.`?** **No — leave it.** The server flags every `v0.*`
   reading `suspect` deliberately: uncalibrated sensors, an MQ proxy, unverifiable
   timestamps (`hics-docs` G9). It should move only when the data is genuinely
   calibration-grade. Do not "fix" the suspect flag.

---

## 19. Things that will waste your time if you don't know them

- **`deploy.sh --restart` cannot restart the services** — the `sudo` step needs a TTY
  password. Sync works; the restart must be run by hand on the Pi.
- **`sensors/config.py` is never synced** by `deploy.sh` (it holds the API key) and is
  `--assume-unchanged` on the Pi. The local copy has `API_KEY = ''`; the device's is set.
- **`i2cdetect` is not installed** on the station. Scan with `smbus2` from Python instead —
  there is a working snippet in this session's history, or just loop `read_byte`/`write_quick`.
- **`sudo` needs a password** for everything on the station.
- **ImageMagick silently ignores `fill-opacity`** on `<rect>` and cannot parse quoted
  multi-family `font-family` stacks. `gen_drawings.py` works around both — don't
  "modernise" the fonts or the tint helper without re-rasterising to check.
- **OpenSCAD's PNG backend ignores alpha**, so a transparent shell renders opaque and hides
  everything. That's why `roofbox.scad` has `exploded` and `section` views rather than one
  transparent assembly.
- **The `else if` chain in `roofbox.scad` used to fall through to `assembly()`** — five
  parts once "compiled fine" while actually rendering the assembly. It now ends in
  `assert(false, "unknown part")`, so a typo fails loudly.
- **OpenSCAD 2021's preview cannot be trusted for section views**: on a nested cut it
  paints the cut face flat across hollows (verified: the STL volume of the half-tower is
  exactly half the hollow tower, yet every preview showed it solid). `render.sh` therefore
  emits sections as exact 2D `projection(cut=true)` SVGs. Trust `roofbox_check.py` over
  any picture.
- **STL-exporting the `site` assembly takes minutes** (CGAL on the whole roof). Preview
  PNGs are seconds. `render.sh` only exports STL for small parts.
- **`quality_flag = 'suspect'` on every reading is correct**, not a bug. See §18.5.

---

## 20. What this deployment does *not* claim

Written down so the Swiss Week material doesn't overstate it.

- **It is not calibrated.** MQ-7 and MQ-135 are labelled proxies; soil moisture is a
  relative index against a two-point calibration. `quality_flag` says `suspect` and that
  is accurate.
- **It is one station, on one rooftop, at 1350 m.** The 4000 m validation environment in
  the AIT pitch is an argument about *where HICS can work*, not a place data has come from.
- **The interim enclosure is a food container.** That is a deliberate, honest
  proof-of-concept step — the printed EDU/SCI enclosures and the two routed PCBs in
  `../iesh-production-reference/` are the product, and they exist. Show both; don't let a
  render imply the container is the product, or the container imply the renders are vapour.
- **No all-sky camera data yet.** Deferred this round (F6, §2).

---

*Diagnosis, firmware fixes and drawings: 2026-09-03, from a live session against
`iesh.local`; audited, corrected and extended the same evening (§4 second pass, §16.8).
Firmware is committed and tested (23 checks). **The hardware rebuild is not started** —
the circuit is part-disassembled on the bench and the camera is out. Next session starts
at `docs/README.md`, then §14 step 1 with the multimeter.*
