# IESH v0.2 — handoff

> **For the next agent or person picking this up.** Read this file, then
> [`LALITPUR-DEPLOYMENT.md`](LALITPUR-DEPLOYMENT.md) (the build sheet). Everything below was
> established on **2026-09-03** against the live station at `pawan@iesh.local`.
>
> Institute context: `~/Documents/HICS/hics-docs/` (start at its `README.md`; folder map in
> `HICS-MAP.md`). Productisation truth: `../iesh-production-reference/` (decisions D1–D29).
> **This file does not restate facts owned by those repos** — it links them.
>
> House rule from `hics-docs/WORKING-AGREEMENT.md` applies here: *if this file and reality
> disagree, this file is the bug.* Sections marked **⚠ UNVERIFIED** were never confirmed.

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

---

## 1. What is physically true right now

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

### The six faults, with their evidence
Referenced as F1–F6 throughout both documents.

- **F1 — undervoltage.** As above. Everything else is downstream.
- **F2 — devices drop off buses.** BMP280 `[Errno 121]`, OLED `[Errno 5]`, DS18B20 vanishing.
  Downstream of F1 *and* of ~40 dupont crimp+friction joints and a 400 kHz I²C clock over
  unshielded wire.
- **F3 — a dead sensor logged its last value forever.** `soil_temp`: **441 rows of `0.0`**
  plus **15 rows of `85.0`** (the DS18B20 power-on-reset sentinel). `pressure`: **416 rows
  frozen at `800.647395954495`**, bit-identical to 12 decimal places, plus 26 rows of `0.0`,
  against only **5** plausible rows (869.8/870.7 hPa; Lalitpur at 1350 m ≈ 862 hPa).
  **FIXED IN FIRMWARE — see §2.**
- **F4 — no working clock.** No RTC overlay, flat coin cell. Post-outage boots mint rows
  with wrong timestamps, and since ingest dedups on `(station, timestamp)`, those are
  **permanent**.
- **F5 — never ran 24 h.** See rows/day above. This is the real headline.
- **F6 — camera dead.** `ov5647: i2c read error, reg: 300a = -5`, plus the overlay conflict.
  Now moot until the camera goes back in.

---

## 2. What changed this session — firmware, committed

Commit `2acdd13` on `master`. **Synced to the Pi but ⚠ NOT YET RESTARTED** — it needs
`sudo systemctl restart hics-core hics-web`, which needs a password this session couldn't
supply. **The new code is therefore not yet running.** That is the first thing to do.

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

---

## 3. Artifacts produced

| Artifact | Path | What it is |
|---|---|---|
| Build sheet | [`LALITPUR-DEPLOYMENT.md`](LALITPUR-DEPLOYMENT.md) | 600-line rooftop build: faults, power, protoboard rework, CAT5e cabling, sensor placement, commissioning gates |
| Wiring schematic | `docs/drawings/schematic.svg` | Pi ↔ protoboard ↔ MCP3208 ↔ terminals. Every net named; the net name is the wire label |
| Perfboard placement | `docs/drawings/perfboard.svg` | 25 × 27 hole grid to scale, zoned placement, separation rules, keep/cut/add list |
| Drawing generator | `scripts/gen_drawings.py` | **Edit the net list here, not the SVGs.** One source feeds both sheets so they cannot drift |
| Box CAD | `../iesh-production-reference/03-enclosure/cad/roofbox.scad` | Third variant beside `edu.scad`/`sci.scad`. Parts: `exploded` `section` `chassis` `cam_mount` `hood` `gas_pod` `shield` `container` `drill` |
| Renders | `../iesh-production-reference/03-enclosure/cad/_roofbox/` | `exploded.png`, `section.png`, `cam_mount.png`, `roofbox_drill.svg` |

Regenerate:
```bash
python3 scripts/gen_drawings.py                                     # both SVG sheets
cd ../iesh-production-reference/03-enclosure/cad
openscad -o out.stl  -D 'part="cam_mount"' roofbox.scad             # the one printed part
openscad -o drill.svg -D 'part="drill"'    roofbox.scad             # 1:1 drilling template
```

> ⚠ `../iesh-production-reference/` **is not a git repository.** The CAD is on disk,
> uncommitted and unversioned. Decide whether to `git init` it — this session did not, on
> the grounds that initialising someone's repo uninvited is not a call to make silently.
>
> ⚠ `03-enclosure/cad/render_views.py` has a **stale hardcoded path**
> (`~/Documents/HICS/iesh-production-reference`, missing the `hics-iesh/` segment). It will
> fail until fixed. Not touched this session.

---

## 3b. Reference photographs and the parts inventory

### Photographs
In `docs/reference-photos/` (1400 px, ~850 KB total) so the docs don't depend on paths
outside the repo. **Several assumptions in §5 were read off these images — which is exactly
why they need calipers.**

**[`01-circuit-as-built-cardboard.jpg`](docs/reference-photos/01-circuit-as-built-cardboard.jpg)
— fault F2, visually.** The cardboard build as taken to the AIT selection pitch: dupont
plugged into dupont, joints held with masking-tape flags, no strain relief anywhere, sensor
boards hanging off unsupported leads. The black power bank at left was the original supply
(F1). This is the thing being replaced.

**[`02-container-exterior.jpg`](docs/reference-photos/02-container-exterior.jpg) — the found
enclosure.** *Measured: **120 × 120 mm base, 180 mm tall**, excluding the rim.* The taper,
rim width and wall thickness in `roofbox.scad` were **estimated from this image** — U1.

**[`03-container-interior-gasket.jpg`](docs/reference-photos/03-container-interior-gasket.jpg)
— the red silicone gasket** in the lid channel. This is the reason the container is usable
at all, and the reason the lid is the chassis plate. The lid seats on a moulded rim, not on
the wall edge.

**[`04-camera-and-clipon-fisheye.jpg`](docs/reference-photos/04-camera-and-clipon-fisheye.jpg)
— the constraint that shaped the enclosure.** OV5647 "Raspberry Pi Camera Rev 1.3", board
**25 × 24 mm**, with its ribbon at **~110 mm — and that is what forces lid-up (§4.1)**.
Also the clip-on phone fisheye: a knurled-ring lens element on a hinged clip, which is what
`cam_mount` seats. `FE_RING_D`, `FE_RING_H` and `FE_BACK` (U2, U3) were all guessed from
this photo.

### Dimensions on record

| Item | Dimension | Source |
|---|---|---|
| Container body | **120 × 120 mm base, 180 mm tall** (excl. rim) | measured |
| Container taper / rim / wall | top ≈130 mm, rim ≈8 mm, wall ≈1.8 mm | **estimated — U1** |
| Camera board (OV5647 Rev 1.3) | 25 × 24 mm, M2 holes on a 12.5 mm grid | datasheet + photo |
| Camera ribbon | **≈110 mm** | measured |
| Fisheye knurled ring | ≈Ø23 × 9 mm | **estimated — U2** |
| Fisheye back-focal gap | ≈3 mm | **guess, needs trial — U3** |
| Raspberry Pi 3B+ | 85 × 56 mm, M2.5 on a 58 × 49 grid, ports 17 mm tall | datasheet |
| Protoboard target | 65 × 70 mm = 25 × 27 holes @ 2.54 mm | `carrier-hat-v1` footprint |
| Verified stack height | **80.5 mm in 178 mm** interior depth (98 mm spare) | computed |

### Parts inventory — transcribed from the two supplier bills
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

**What the inventory changes:**
- **Spares exist** for MQ-7, MQ-135 and DHT22 — a suspect part can be swapped rather than
  debugged. There is **no spare BMP280** (U7).
- **Two 10 × 15 cm matrix boards** — cut one to 65 × 70 mm and a whole spare remains.
- **A multimeter is on hand**, so F1 can be settled by measurement, not inference.
- **Only 2× 3-pin terminals** — about 16 ways are needed. On the shopping list.
- **Unused and worth fitting:** raindrop ×2 (CH3 free), LDR ×4 (CH4 free).
- **Unused, no role here:** PIR, mic, buzzer, relays, switches. The *waterproof ultrasonic*
  is interesting later as a **snow-depth or water-level** channel — a Himalayan-transect
  story, not a Lalitpur-rooftop one.
- ⚠ **U4:** "Resistors ×30" does not say the values. R1–R6 all need **4k7**.
- ⚠ **U5:** the ₨650 "boom/boost module" is unidentified. If it is a 12 V→5 V buck it may
  serve the power design directly (§4.5).

### Generated drawings and renders

| Sheet | Path |
|---|---|
| Wiring schematic | [`docs/drawings/schematic.svg`](docs/drawings/schematic.svg) |
| Perfboard placement | [`docs/drawings/perfboard.svg`](docs/drawings/perfboard.svg) |
| Box exploded view | `../iesh-production-reference/03-enclosure/cad/_roofbox/exploded.png` |
| Box section view | `../iesh-production-reference/03-enclosure/cad/_roofbox/section.png` |
| Camera mount | `../iesh-production-reference/03-enclosure/cad/_roofbox/cam_mount.png` |
| Lid drilling template (1:1) | `../iesh-production-reference/03-enclosure/cad/_roofbox/roofbox_drill.svg` |

---

## 4. The rethink — what to question rather than inherit

This is the part worth reading. Everything above is defensible; some of it is only
defensible *given constraints that a small purchase would remove*.

### 4.1 The camera ribbon is driving the entire enclosure design. Buy a longer one.
The ribbon on hand is **110 mm**. That single fact forced: camera in the lid → lid must
face up → rain can sit on the gasket → a hood becomes mandatory → glands must move to the
side wall. **Lid-*down* is strictly better weatherproofing** (every penetration faces the
ground, gravity loads the seal correctly), and it was rejected only because the Pi would
then sit 180 mm from the sky-facing end.

**A 300–500 mm 15-pin FFC costs almost nothing.** Buy it, then revisit the orientation
from scratch. Do not inherit lid-up as though it were a design decision; it is a
workaround.

### 4.2 Question the container itself before designing further around it
A food container is a genuinely defensible proof-of-concept housing, and "we built it with
what we had" is an honest story. But a proper **IP65 ABS junction box** is cheap in
Kathmandu, arrives with a real gasket, moulded gland bosses and mounting lugs, needs no
hood improvisation — and will photograph far better for Swiss Week. Spend thirty minutes
pricing one at Supreme Light Technology (Sanepa-2) before committing. If the container
wins on cost or timing, fine — but make it a decision, not a default.

Related: **five container dimensions in `roofbox.scad` are estimates read off photographs**
(§5). Measure before printing anything.

### 4.3 The perfboard drawing is deliberately incomplete, and you should finish it differently
`perfboard.svg` is a **zoned placement** drawing, not a hole-exact route. That was a
judgement call: the physical board already has the MCP3208 and its power lines soldered,
and authoring a hole-by-hole route without that board in hand produces a drawing that is
wrong in detail *and trusted anyway* — the worst outcome.

**The right way to finish it:** photograph the existing board top and bottom, count the
actual occupied holes, and *then* extend `scripts/gen_drawings.py` with the real routing.
The generator is structured for this — `ZONES` is already data.

### 4.4 Do not build on a sagging rail, and do not trust "it worked before"
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

### 4.5 Mains is now going to the roof — keep it out of the instrument box
A wall-socket line is being run up. That settles the topology, but **no 240 V inside a
plastic food container on a roof.** Adapter in its own small junction box; only low voltage
crosses the gland. Prefer **12 V + a small buck module** over 5 V if the adapter ends up
more than about a metre away — 12 V draws ~2.4× less current for the same power, so the run
loses far less voltage, and voltage drop *is* F1. Keep the lead-acid UPS **indoors**: heat
kills lead-acid, and a hot roof is the worst place for it.

### 4.6 What actually earns a render, and what doesn't
A 3D render of a food container told us almost nothing we didn't already know — that steer
was correct. What paid off was the **2D schematic** (it caught nothing, but it is what you
solder from) and, unexpectedly, the **numeric checks**: an XY clash test caught a real
camera-over-Pi overlap that two rounds of eyeballing renders had missed, and a unit test
caught a bug in the frozen-register gate that looked right in code review.

**Generalise that.** Prefer a computed assertion over a picture. Reserve renders for the
pitch deck, where communication is the actual job, and for verifying that a *mechanism* is
what you think it is.

### 4.7 Scope honestly: this is a robust DIY build, not a production one
The two routed PCBs (`carrier-hat-v1`, `power-mgmt-v1`) and the printed EDU/SCI enclosures
already exist in `../iesh-production-reference/` and **are** the product. This deployment is
the working proof that logs real data. Show both at Swiss Week; don't let a render imply the
container is the product, or the container imply the renders are vapour.

---

## 5. ⚠ UNVERIFIED — measure or confirm before relying on any of these

| # | Assumption | Where | How to settle it |
|---|---|---|---|
| U1 | `BOX_TOP = 130`, `RIM_W = 8`, `RIM_T = 6`, `BOX_WALL = 1.8` | `roofbox.scad` | Calipers. Only base 120 × 120 and height 180 were actually measured |
| U2 | `FE_RING_D = 23`, `FE_RING_H = 9` — the fisheye's knurled ring | `roofbox.scad` | Calipers, before printing `cam_mount` |
| U3 | `FE_BACK = 3` — fisheye rear to sensor front | `roofbox.scad` | **Trial and error.** Clip-on phone fisheyes expect 2–4 mm off a phone lens. Print the seat shimmable |
| U4 | The 30 resistors on bill 724 include **4.7 kΩ** | shopping list | Read the bands / measure. R1–R6 all need 4k7 |
| U5 | The ₨650 "boom/boost module" on bill 745 is a buck/boost converter | shopping list | Look at it. If it is a 12 V→5 V buck, it may serve directly |
| U6 | DHT22 breakout already carries its own pull-up | schematic R2 | Inspect the module before adding a second |
| U7 | BMP280 is merely disconnected, not dead | §1 | Reconnect and re-scan `0x76`. **There is no spare** — if dead it needs buying |
| U8 | `PSU`/`BUCK` module dimensions in the CAD | `roofbox.scad` | Measure the actual module |
| U9 | Whether the new firmware behaves correctly on real hardware | §2 | **It has not run yet.** Restart the services and watch the log |

---

## 6. Open decisions — not for an agent to make alone

1. **Purge the existing website readings for `IESH-KMC-001`?** The F3 garbage is already
   stored server-side (the live API returns `pressure_hpa: 0.0`), and because ingest is
   `get_or_create` on `(station, timestamp)`, re-POSTing corrected rows **will not**
   overwrite them. Starting the public series clean looks like the only honest option — but
   it is **destructive and irreversible. Confirm with Pawan before running anything.**
2. **`git init` the `iesh-production-reference` folder?** See §3.
3. **Container or IP65 junction box?** See §4.2.
4. **Buy the longer camera ribbon and redo the orientation?** See §4.1.
5. **Bump `FIRMWARE_VERSION` past `v0.`?** **No — leave it.** The server flags every `v0.*`
   reading `suspect` deliberately: uncalibrated sensors, an MQ proxy, unverifiable
   timestamps (`hics-docs` G9). It should move only when the data is genuinely
   calibration-grade. Do not "fix" the suspect flag.

---

## 7. Do these in this order

Gated deliberately: F2's symptoms are intermittent, and an intermittent fault found *after*
the box is closed costs a rooftop trip.

1. **`sudo systemctl restart hics-core hics-web`.** The fixed firmware is synced but not
   running. Then confirm the log shows `Logged to DB (… rows)` with a `| NULL:` note naming
   exactly the channels you know are disconnected — that is the gating working.
2. **Fix power. Get `vcgencmd get_throttled` to `0x0` and hold it for an hour** with both MQ
   heaters running. §4.4. *Nothing below is meaningful until this passes.*
3. **`config.txt`:** `i2c_arm_baudrate=100000`, add `dtoverlay=i2c-rtc,ds3231`, comment out
   `dtoverlay=ov5647`. Fit a **fresh coin cell**, `sudo hwclock -w`, reboot, confirm
   `hwclock -r` and `/dev/rtc0`.
4. **Measure U1–U8.** Cheap, and it unblocks everything physical.
5. **Rework the protoboard** — cut the jumper chains, keep the soldered MCP3208, add R1–R6
   / C1 / C2, fit screw terminals. Continuity-check **every** net before fitting any IC.
6. **Bring up one sensor at a time** on the bench, `python3 tests/test_all.py` after each.
   Order: I²C trio → MCP3208 + soil → DS18B20 → DHT22 → MQ pair.
7. **Run 24 h on the bench.** Gate: ~1440 rows for a full day *and* `get_throttled` still
   `0x0`. **This closes F5, which has never been closed.**
8. Drill the lid from the template, seal, assemble the mast, deploy.
9. **48 h of clean data**, then purge + set `status = 'active'` (§6.1).

---

## 8. Things that will waste your time if you don't know them

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
- **An `else if` chain in `roofbox.scad` silently falls through to `assembly()`.** Five
  parts once "compiled fine" while actually rendering the assembly. If you add a part,
  verify the geometry differs (`md5sum` the STLs).
- **`quality_flag = 'suspect'` on every reading is correct**, not a bug. See §6.5.

---

*Written 2026-09-03 by Claude Opus 5, from a live diagnosis of `iesh.local`. Firmware fixes
are committed and tested; the hardware rebuild is not started.*
