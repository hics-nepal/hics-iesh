# IESH v0.2 — Lalitpur rooftop deployment

> **Photos:** [as-built circuit](docs/reference-photos/01-circuit-as-built-cardboard.jpg) ·
> [container](docs/reference-photos/02-container-exterior.jpg) ·
> [lid gasket](docs/reference-photos/03-container-interior-gasket.jpg) ·
> [camera + fisheye](docs/reference-photos/04-camera-and-clipon-fisheye.jpg)
>
> **Drawings:** [wiring schematic](docs/drawings/schematic.svg) ·
> [perfboard placement](docs/drawings/perfboard.svg)
>
> **Scope.** Take the station from the cardboard bench prototype to a rooftop unit in
> Kumaripati, Lalitpur that logs real, trustworthy data to himalayansciences.org
> continuously. Interim housing is a 120 × 120 × 180 mm gasketed food container; the
> 3D-printed EDU/SCI enclosures and the two routed PCBs in
> `../iesh-production-reference/` remain the product end state and are **not** replaced
> by anything here.
>
> **Start at [`HANDOFF.md`](HANDOFF.md)** if you are picking this up cold — it carries the
> current state of the hardware, what is unverified, the open decisions, and a rethink of
> the approach. This file is the *build sheet*: what to do with your hands.
>
> Institute context: `~/Documents/HICS/hics-docs/`. Productisation truth:
> `../iesh-production-reference/` (decisions D1–D29). This file is the truth for
> **this deployment only** — the physical build, what goes where, and how we know it works.

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

## 1. Why v0.1 produced no usable data

Diagnosed on the live station 2026-09-03. Recorded here because every design choice
below is a response to one of these, and a future session that doesn't know them will
undo the fixes.

| # | Fault | Evidence |
|---|---|---|
| **F1** | **Undervoltage, continuously** | `vcgencmd get_throttled` = `0x50005` → *under-voltage NOW · currently THROTTLED*. `dmesg`: `hwmon2: Undervoltage detected!`. Present on the power bank **and** on the replacement plug adapter, both measured on a 2-minute-old boot — so it is not stale history. Pi **3B+** wants a solid 5 V/2.5 A. |
| **F2** | **Sensors drop off their buses and come back** — [see the as-built photo](docs/reference-photos/01-circuit-as-built-cardboard.jpg) | BMP280 `[Errno 121]`, OLED `[Errno 5]`, DS18B20 absent from `/sys/bus/w1/devices/` then present as `28-062261761e24` minutes later. Downstream of F1, and of ~40 dupont crimp + friction joints. |
| **F3** | **A dead sensor logged its last value forever** | v0.1 initialised every reading to `0.0` and overwrote only on success. Measured in the station DB: `soil_temp` = **441 rows of 0.0** + **15 rows of 85.0** (the DS18B20 power-on-reset sentinel); `pressure` = **416 rows frozen at 800.647395954495** (bit-identical to 12 dp) + 26 rows of 0.0, against only **5** plausible rows. ~46 % of the soil column was garbage indistinguishable from data. |
| **F4** | **No working clock** | No `dtoverlay=i2c-rtc,ds3231`, so `/dev/rtc0` does not exist and the OS never reads the DS3231. The chip itself reads **2000-01-05** — coin cell dead or never set. Boot time came from systemd's saved clock, which is why services claimed "started Jun 13" on a 14-minute uptime. Every power cut mints rows with a wrong timestamp, and the server dedups on `(station, timestamp)` — so bad timestamps are **permanent**. |
| **F5** | **Never ran a full day** | Rows/day: Jun 11 → 598, Jun 12 → 35, Jun 13 → 101, Sep 3 → 26. A full day is 1440. There is no time series to speak of. |
| **F6** | Camera dead | `ov5647: i2c read error, reg: 300a = -5`; `config.txt` carries **both** `camera_auto_detect=1` and `dtoverlay=ov5647`. Camera has since been physically removed. |

**F3 is fixed in firmware** (§6) — it was the one that silently corrupted the record.
**F1 and F2 are what this rebuild is for.**

---

## 2. The one design decision everything follows from

> **The box is a dry electronics vault. Every environmental sensor lives outside it.**

A sealed 120 mm box on a Kumaripati rooftop in September sun runs 45–55 °C inside. A
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
   └──────────┬──────────┘           │  BOX  │  120 × 120 × 180, LID UP
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
the heat straight in.

**Cable glands move off the lid into the box side wall, low down**, so nothing faces the
sky. Drip loops below each.

**The fisheye lens is the window.** It's a [clip-on phone lens](docs/reference-photos/04-camera-and-clipon-fisheye.jpg): the element with its
knurled ring unscrews from the clip arm, and that ring beds into a sealed boss in the lid.
This is better than cutting an acrylic window — the camera isn't also shooting through an
extra sheet that would add reflections and haze. Vignetting into a circular image is
exactly what an all-sky camera wants.

**Build on a removable sled.** A flat plate (3 mm acrylic, ply, or ABS offcut) carrying
Pi + HAT + terminal strip, which drops into the box as a unit. Assembling inside a
120 mm box is miserable; assembling on the bench and then inserting is not. This is the
single biggest buildability win available.

---

## 3. Power — fix this before anything else

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

## 4. Wiring — the protoboard HAT

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

If the current board turns out to be too big for the sled, cut a fresh 10 × 15 cm matrix
board down to **~65 × 70 mm** — the `carrier-hat-v1` footprint, so the layout transfers
when the real PCB arrives — and move the MCP3208 section across. Score with a knife
against a steel rule and snap. You keep the offcut and a whole spare board.

### Pin map (from `sensors/config.py` — the single source of truth)

| Signal | GPIO | Header pin | Goes to |
|---|---|---|---|
| 3.3 V | — | 1, 17 | MCP3208 VDD+VREF, BMP280, OLED, DS3231, DS18B20 pull-up |
| 5 V | — | 2, 4 | DHT22, MQ heaters *(prefer a separate rail — §3)* |
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
> slower clock** — see §5.

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
You have only **2× 3-pin**. Needed: mast cable (8), soil cable (4), power in (2) — about
**4 blocks / 16 ways** with the cabling scheme below. Add to the shopping list (§8).

---

## 4b. How the sensors actually connect

The rule: **no sensor gets its own cable run.** Two multi-core cables leave the box — one
up the mast, one down to the vase — and each sensor taps the cable at its own end. That
takes the box from six penetrations to **two**, which is the difference between a box that
stays dry and one that doesn't.

### Use CAT5e for both runs
Cheap, sold on every corner in Kathmandu, 8 conductors, and the twisted pairs are exactly
what you want: each supply travels twisted with its own return, which is what keeps a
switching MQ heater from injecting noise into an analogue line running beside it. You
already have a length of it (the yellow cable in the bench photo).

**Mast cable — 8 conductors, all 8 used:**

| Pair | Conductor | Carries |
|---|---|---|
| 1 | orange / orange-white | **+5 V** / GND — MQ-7 + MQ-135 heaters, DHT22 |
| 2 | green / green-white | **+3.3 V** / GND — raindrop board, LDR divider |
| 3 | blue / blue-white | **DHT22 DATA** / GND |
| 4 | brown | **MQ-7 AOUT** → MCP3208 CH0 |
| 4 | brown-white | **MQ-135 AOUT** → MCP3208 CH1 |

That leaves the LDR and raindrop analogue outputs sharing pair 2's spare capacity — if you
fit both, run **a second short CAT5e** rather than doubling up a conductor. Cable is
cheaper than a debugging trip to the roof.

**Soil cable — 4 conductors to the vase:**

| Conductor | Carries |
|---|---|
| 1 | **+3.3 V** (both probes) |
| 2 | GND (both probes) |
| 3 | **DS18B20 DATA** → GPIO4 |
| 4 | **soil moisture AOUT** → MCP3208 CH2 |

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
- **Clamp each cable to the sled** with a zip tie through two holes, ~40 mm inside the
  gland. Pull on the cable and the tie takes the load, never the screw terminal.
- **Drip loop below every gland**: the cable must go *down* out of the gland and hang below
  it before rising. Water runs to the bottom of the loop and drips off. With the box
  inverted (§2) the glands already point down, so this costs nothing but a little slack.
- Leave ~200 mm of slack inside the box. Tight cabling makes servicing on a roof
  unpleasant and pulls joints apart.

### One thing to check with the multimeter before closing the box
With the mast cable connected and everything running, measure **+5 V at the MQ sensor end
of the cable**, not at the Pi. If it reads below 4.8 V there, the heaters are running cold
and the MQ readings drift — double up pair 1's conductors or shorten the run.

---

## 5. Pi configuration changes

All three are edits on the device; none is optional.

### 5.1 Slow the I2C bus — 400 kHz over unshielded wire is the F2 mechanism
`/boot/firmware/config.txt` currently has `dtparam=i2c_arm_baudrate=400000`. Nothing on
this bus needs 400 kHz; a 60-second log interval is happy at 100 kHz, and the noise
margin roughly quadruples.
```
dtparam=i2c_arm_baudrate=100000
```

### 5.2 Give the OS a real clock (fixes F4)
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

### 5.3 Resolve the camera overlay conflict (F6)
`config.txt` carries both `camera_auto_detect=1` and `dtoverlay=ov5647`. Keep one. With
the camera physically removed, **comment out `dtoverlay=ov5647`** so the driver stops
retrying a chip that isn't there and filling the log with `i2c read error`. Restore it (or
rely on auto-detect alone) when the camera goes into its own housing.

### 5.4 Interface config that is now wrong for this board
`sensors/config.py` says `INTERNET_IFACE = 'wlan1'` and `HOTSPOT_IFACE = 'wlan0'`. A Pi
3B+ has **one** wlan. There is no `wlan1`, so the `IESH_Hub` hotspot the README describes
does not exist on this unit. For the Lalitpur deployment the station joins home WiFi on
`wlan0` (currently `liverpool08_2.4`, signal 70) and that is sufficient — but the README's
hotspot section does not describe this station and should say so.

---

## 6. Firmware — done, deployed 2026-09-03

Fixes F3 and the two smaller defects found alongside it. Synced to the Pi;
**needs `sudo systemctl restart hics-core hics-web` to take effect.**

**`sensors/health.py` (new).** A `Channel` logs a value only if it is *fresh* (a reading
arrived within `max_age`, default 180 s) **and** *physically plausible*. Otherwise it logs
`NULL`. The bounds deliberately mirror `_QUALITY_BOUNDS` in the website's
`instruments/api.py`, so a value the server would flag `suspect` is dropped at the edge
instead of shipped. Two consequences fall out for free: the DS18B20's **85.0** sits above
the 80 °C ceiling, and **pressure 0.0** sits below the 300 hPa floor — both now `NULL`.

It also detects a **frozen register**: bit-identical raw readings `FROZEN_REPEATS` times
running mean a chip that browned out into sleep holding old data, which is how 416 rows of
`800.647395954495` were logged as valid. A real sensor always dithers in the low bits, and
the channel recovers automatically once the register moves again.

`NULL` is honest; a stale number is not. `data/database.py` already declared every sensor
column nullable — v0.1 simply never wrote one.

**`core_dash.py`.** Values flow through a `ChannelSet` instead of module-level floats
initialised to `0.0`. Adds automatic recovery: a downed BMP280 or OLED is re-initialised
every 60 s, so a device that drops off the bus and returns comes back on its own — v0.1
latched `ok=False` at init and stayed dead until someone restarted the service by hand.
Failing channels are now named in the service log (`| NULL: pressure=dead`) and on the
OLED System screen, so a dead sensor is visible instead of silent. Altitude no longer
feeds 0.0 hPa into the barometric formula and displaying 44 330 m.

**`sensors/ds18b20.py`.** Rescans the 1-Wire bus on every failed read, so a probe that
reappears is picked up without a restart. Rejects the 85.0 reset sentinel explicitly and
checks the CRC line. `modprobe` now uses an absolute path — v0.1's `os.system('modprobe …')`
printed `modprobe: not found`, because `/usr/sbin` is not on a login user's `PATH`.

**`sensors/bmp280_sensor.py`.** Gains `reinit()`, and exposes the uncompensated pressure
word as `last_raw_p` for the frozen-register check.

**`sensors/oled.py`.** Gains `reinit()`.

**`data/uploader.py`.** Two real bugs. The `_online()` probe socket was never closed —
one leaked file descriptor per upload cycle, ~288/day, for the service's lifetime; it now
uses a context manager. And timestamps are now sent as explicit **UTC**, as
`docs/INGEST_CONTRACT.md` requires; v0.1 sent naive local time and relied on Django
interpreting it in `TIME_ZONE`. That rescue happened to be correct — verified
instant-identical, `2026-09-03T19:15:45.687572` local → `2026-09-03T13:30:45.687572Z`,
matching what the server already stored — so **this change shifts no existing data**. It
removes a warned, settings-dependent fallback. Floats are also rounded (soil moisture was
going up with 17 significant figures).

**`sensors/__init__.py`.** Driver re-exports are now lazy (PEP 562). They were eager, so
touching anything under `sensors.` imported Adafruit `board`, `spidev` and `smbus2` — which
meant the hardware-free `sensors.config` and `sensors.health` could not be imported off-Pi
or in CI. Every consumer in the tree imports submodules directly anyway.

**`tests/test_health.py` (new).** Every case is a value actually found in the station's
own database. Runs anywhere, no hardware:
```bash
python3 tests/test_health.py     # 21 checks, passing on dev and on the station
```

---

## 7. Sensor placement, one by one

| Sensor | Where it goes | Why / gotcha |
|---|---|---|
| **DHT22** air T/RH | Mast, inside a **radiation shield**, ≥ 300 mm clear of the box and ≥ 1 m above the roof deck | Non-negotiable. In the box it reads the box; in direct sun it reads the sun. Shield = 4–6 stacked plates with air gaps — cheap plastic plant-pot saucers, inverted and spaced on a bolt, work genuinely well and cost almost nothing. |
| **BMP280** pressure | **Inside**, on the HAT | Pressure equalises through any small opening, so it can stay in the vault — but the vault must not be *perfectly* sealed or thermal swing gives a false offset. One 2 mm hole on the **downward** face, behind a scrap of PTFE tape or foam, is enough. Currently **absent from the I2C bus (`0x76`)** — reconnect it and re-scan; you have no spare, so if it stays dead it needs replacing. |
| **MQ-7** CO, **MQ-135** gas | Mast, in a **downward-facing vented pod** | Must see ambient air, and they self-heat ~350 mW each — in the vault they'd read their own exhaust and cook the Pi. Down-facing vents keep rain out. Stay a **labelled proxy**, not a calibrated measurement (hics-docs G9). |
| **DS18B20** soil T | **Buried in the planter**, 100 mm deep | Waterproof stainless probe version is already suitable. Needs the 4.7 kΩ pull-up. |
| **Capacitive soil moisture** | **Buried in the planter**, blade vertical | Only meaningful *if there is soil* — see the note below. **Pot the top ~25 mm of the board in epoxy or silicone**; the v1.2 boards leave their electronics exposed above the blade and die within weeks outdoors. Re-run `scripts/calibrate_soil.py` in the actual planter soil — the current `SOIL_DRY = 4021` / `SOIL_WET = 1673` came from a different medium. |
| **DS3231** RTC | Inside, on the HAT | **Fit a fresh coin cell.** The one in it is flat (§5.2). |
| **OLED** | Inside, or omit | A classroom feature with no outdoor purpose. Keep it on the sled for bench commissioning; don't cut a window for it. |
| **Pi camera** (all-sky) | **In the lid**, fisheye barrel sealed into a printed boss, board bolted beneath | Forced by the **110 mm ribbon** — it cannot go on the mast. The lens is the window (§2). Print `cam_mount` from `roofbox.scad`; the one dimension to find by trial is `FE_BACK`, the lens-to-sensor gap (~2–4 mm), so print the seat shimmable. Currently removed, so this is the last thing to fit. |
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
raindrop sensors (§7) are worth fitting: rain → soil moisture response is the one
relationship on this station that is visible within a single afternoon.

What would not be defensible is leaving a probe in air and logging the number it produces.

---

## 7b. CAD and the one part that needs printing

`../iesh-production-reference/03-enclosure/cad/roofbox.scad` — a third variant alongside
`edu.scad` and `sci.scad`, modelling the **real container with the real Pi 3B+** (the
existing library models a Pi 4B). It exists to fit-check, place the sensors, and emit the
drilling template — not to be a production enclosure.

```bash
cd ../iesh-production-reference/03-enclosure/cad
openscad -o out.stl -D 'part="cam_mount"' roofbox.scad     # the one printed part
openscad -o drill.svg -D 'part="drill"'   roofbox.scad     # 1:1 drilling template
```

Parts: `exploded` · `section` · `chassis` · `cam_mount` · `hood` · `gas_pod` · `shield` ·
`container` · `drill`. Renders in `cad/_roofbox/`.

**Almost nothing is fabricated.** The scope is a working station, not a production build:

| Part | How |
|---|---|
| Chassis plate | **The actual lid, drilled.** Print `drill` at 1:1, tape it on, centre-punch through. No plate to make. |
| `cam_mount` | **Print this one.** It holds the fisheye-to-sensor spacing, which is the only dimension that needs accuracy. |
| Hood | A sheet of aluminium, corrugated plastic, or a second container lid on four standoffs. `hood` is the reference geometry, not a required print. |
| Gas pod | Any small vented tub with downward holes. `gas_pod` is printable if convenient. |
| Radiation shield | **Five inverted ~100 mm plant-pot saucers on a bolt** with spacers. Works genuinely well. `shield` is printable if preferred. |

**Fit is verified, not assumed.** The stack is 80.5 mm tall in 178 mm of interior depth
(98 mm spare, which is where cable slack and desiccant go), and Pi / buck / camera boss are
clash-checked in XY — the first two layout drafts had a real overlap that only a numeric
check caught.

Three dimensions in the file are marked **ASSUMPTION** and read off photographs. Measure
them before printing `cam_mount`, or it will not fit:

- `FE_RING_D` / `FE_RING_H` — the fisheye's knurled ring, est. Ø23 × 9 mm
- `FE_BACK` — lens rear to sensor front, est. 3 mm. **This is the one to find by trial**;
  clip-on fisheyes expect 2–4 mm off a phone lens. Print the seat so it can be shimmed.
- `BOX_TOP` / `RIM_W` — the container's taper and flange

---

## 8. Shopping list

Everything not already in the inventory — transcribed in
[`HANDOFF.md` §3b](HANDOFF.md#3b-reference-photographs-and-the-parts-inventory).

| Item | Qty | Why | Where |
|---|---|---|---|
| Short thick micro-USB cable (≤ 1 m, 20 AWG) | 1 | **Top priority — likely the whole of F1** | any |
| 5 V / 3 A supply | 1 | if the cable alone doesn't clear the flag. Lives in the junction box, not the vault | Supreme Light Technology, Sanepa-2 |
| Hook-up wire, 22 AWG stranded, 3–4 colours | 1 spool ea | you have jumper sets but no bulk wire | SLT |
| Screw terminal blocks, 2- and 3-way | ~6 blocks | only 2× 3-pin on hand | SLT |
| Resistors 4.7 kΩ | 10 | 1-Wire + MQ dividers — **the 30 on bill 724 have unconfirmed values (U4)** | SLT |
| Capacitors 100 nF / 1000 µF | 10 / 2 | decoupling + MQ bulk | SLT |
| PG7 or PG9 cable glands | 3 | sealed entries — drilled in the box **side wall**, low down, never the lid. Rubber grommet + neutral-cure silicone is an acceptable substitute | hardware shop |
| Small weatherproof junction box | 1 | houses the mains adapter **outside** the instrument box | electrical shop |
| 12 V→5 V 3 A buck module | 1 | if the adapter is >1 m away. First identify the ₨650 "boom/boost module" on bill 745 — it may already be one (U5) | SLT |
| Neutral-cure silicone | 1 tube | **neutral-cure, not acetoxy** — acetoxy silicone corrodes copper and pins | hardware shop |
| M2.5 standoffs + screws | 1 set | Pi to sled | SLT |
| Aluminium or corrugated-plastic sheet ~170 mm sq | 1 | the hood | hardware shop |
| Plant-pot saucers ~100 mm | 5 | radiation shield plates | any nursery |
| — | — | *planter not needed: the roof already has planted vases* | — |
| CR2032 / LIR2032 | 1 | the DS3231's cell is flat | any |
| 20 mm PVC pipe + clamps | ~1 m | sensor mast | hardware shop |
| Desiccant sachets | 2–3 | condensation inside the vault | any |
| Epoxy or potting compound | small | pot the soil probe's exposed top | hardware shop |

---

## 9. Build order

Each step is gated: don't proceed while the previous one fails. The gates exist because
F2's symptoms are intermittent, and an intermittent fault found *after* the box is closed
costs a rooftop trip.

1. **Fix power. Verify `vcgencmd get_throttled` reads `0x0`** and stays there for an hour
   with both MQ heaters running. *Nothing below is meaningful until this passes.*
2. **Apply the `config.txt` changes** (§5.1–5.3), fit the DS3231 coin cell, `hwclock -w`,
   reboot, confirm `hwclock -r` reads correct local time and `/dev/rtc0` exists.
3. **Restart the services** so the new firmware is live:
   `sudo systemctl restart hics-core hics-web`. Confirm the log shows
   `Logged to DB (… rows)` with a `| NULL:` note naming exactly the channels you know are
   disconnected — that is the gating working.
4. **Cut and solder the protoboard HAT** (§4). Do the Pi header, ground strip and 3.3 V/5 V
   distribution first; **continuity-check every net with the multimeter before fitting any
   IC or plugging it onto the Pi.** A shorted rail on a soldered board is much less
   forgiving than on a breadboard.
5. **Bring up one sensor at a time on the bench**, HAT on the Pi, running
   `python3 tests/test_all.py` after each. Order: I2C trio (BMP280 / OLED / DS3231) →
   MCP3208 + soil → DS18B20 → DHT22 → MQ pair. Adding them one at a time is what makes an
   intermittent fault attributable.
6. **Run 24 h on the bench.** Gate: `sqlite3 ~/hics-data/hics.db "SELECT date(timestamp),
   COUNT(*) FROM telemetry GROUP BY 1"` shows **~1440 rows** for a full day, and
   `get_throttled` is still `0x0`. This directly closes F5 — the station has never yet
   done this.
7. **Mount on the sled, fit the box, seal the glands.** Silicone needs 24 h to cure.
8. **Assemble the mast**, radiation shield and gas pod; wire to the terminals.
9. **Deploy to the roof.** Box inverted, off the deck, shaded if possible. Drip loops on
   every cable *below* the gland.
10. **Re-register the station public** on the website only after 48 h of clean data (§10).

---

## 10. Website — before going public again

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

## 11. What this deployment does *not* claim

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

*Diagnosis and firmware fixes: 2026-09-03. Hardware rebuild: in progress.*
