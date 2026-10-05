# Board build — working doc

Live bench notes for the IESH v0.2 HAT, built **2026-09-11 onward**. This is the sheet you
work from at the desk. Narrative, faults and the wider build order stay in
[`HANDOFF.md`](HANDOFF.md); the generated sheets stay in [`docs/`](docs/README.md). Anything
decided here that changes a documented fact gets folded back into `HANDOFF.md`.

---

## ▶ NEXT SESSION — start here

**Done and verified:** header, three rails + rail gate, MCP3208 block + ADC gate (2026-09-13).
**Next: the first power-on** (table below). The ADC gate table is kept for reference.

**⛔ First: the ADC gate.** The MCP3208 block was soldered on 2026-09-12 but **never metered** —
the session ended before the checks. Nothing gets powered until these pass, board off the Pi.

| Probe | Must read |
|---|---|
| `(38,D)` → 3V3 rail | short — pin 16 VDD |
| `(37,D)` → 3V3 rail | short — pin 15 VREF |
| `(36,D)` → GND rail | short — pin 14 AGND |
| `(31,D)` → GND rail | short — pin 9 DGND |
| **3V3 rail ↔ GND rail** | **must NOT buzz** |
| `(35,D)` ↔ `(48,I)` · `(34,D)` ↔ `(48,J)` · `(33,D)` ↔ `(48,K)` · `(32,D)` ↔ `(47,I)` | short |
| each SPI pad ↔ the other three | open |
| each SPI pad ↔ either rail | open |
| every column G pad (CH0–CH7) ↔ either rail | open |

**Then the first power-on.** Do this before another component goes on — it proves the header,
the rails and the ADC in one go, while the board is still simple enough to debug.

| Do | Detail |
|---|---|
| 1 | **Board onto the Pi.** Micro-USB plugged in **first** — the board roofs that edge |
| 2 | Power up. **Measure 3V3 rail → GND rail: must be 3.3 V.** Then `(38,D)` → GND: same |
| 3 | `sudo raspi-config` → Interface Options → **SPI enabled**. Reboot |
| 4 | `ls /dev/spidev*` — expect `spidev0.0` |
| 5 | **Read a channel.** Any free one, CH3–CH7. Floating input should give a drifting number, not a hard 0 or 4095 |
| 6 | Ground that channel to the GND rail by hand → reading should drop to ~0. Touch it to 3V3 → ~4095. **That is the ADC proven end to end** |

If step 5 gives a stuck 0 or 4095, the fault is almost certainly **MOSI and MISO swapped** —
`Din` at `(33,D)` takes MOSI from `(48,K)`, `Dout` at `(34,D)` takes MISO to `(48,J)`.

Then, still outstanding and none of it blocking: **1d** meter the passives and set aside two
matched 4.7 kΩ pairs · **1e** buy a real LM2596 (the module on hand is an LM2587S *boost*) and trim it · **1f** test the CR2032.

---

## 0. What is being built, and on what

A fresh board. **The old demo board is not reworked** — bill 884 bought a second MCP3208, so
the old one is set aside intact as a reference and parts donor. No desoldering, no island
cutting, no risk to a part there is only one of.

| | |
|---|---|
| Board | blank `PY-10CM*15CM`, **150 × 100 mm**, **uncut** |
| Grid | **48 columns × 36 rows**, 2.54 mm (= 122 × 91 mm; the missing ~28 mm is the two oval-pad strips at the ends) |
| Oval edge pads | **isolated — metered 2026-09-11, no continuity.** Not usable as rails |
| Pi link | 2 × `1×20` female strips cut from `1×40` (bill 884), side by side = a 2×20 header. **Verified: both seat flat on all 40 Pi pins** |

---

## 1. Coordinates — read this before anything else

Read off the board's own silkscreen, confirmed from photographs 2026-09-11:

| Axis | Marking | Count | Length |
|---|---|---|---|
| **Long, 150 mm** | **numbers 1 – 48** | 48 | 122 mm of grid + a ~14 mm oval-pad strip at each end |
| **Short, 100 mm** | **letters A–Z then A′–J′** | 36 | 91 mm of grid + ~4.5 mm margin each side |

**Origin is the `48, A` corner.** The oval strips are isolated pads (metered) — not rails,
and not part of the grid. *Forgetting the 14 mm strip outside number 48 is what put an
early layout 12 mm over the Ethernet jack; the grid is not the board edge.*

### Orientation, anchored to the Pi

**The header lies across the LETTERS: numbers 48 and 47, letters A → T.**

```
         letter  A   B   C  …                     T  …  Y  …  J′
              ┌───────────────────────────────────────────────┐
   number 48  │▓▓▓▓▓▓▓▓▓▓▓▓ 2×20 HEADER ▓▓▓▓▓▓▓▓▓│            │
   number 47  │▓▓▓▓▓▓▓▓▓▓▓▓ letters A → T ▓▓▓▓▓▓▓│            │
              │                                               │
              │ ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐         │
   number 25  │ │        Pi 3B+  (under the board)   │         │
              │ └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘         │
              │   ↑ µUSB / HDMI edge                          │
              │                                               │
              │        FREE BOARD — over open air             │
   number  1  └───────────────────────────────────────────────┘
            ↑ USB/Ethernet                          microSD ↑
              stick out ~23 mm                    end is ~38 mm
              PAST this edge                      inside this edge
```

| Anchor | |
|---|---|
| **Pi header pin 1** | **letter T** |
| **Pi header pin 39/40** | **letter A** |
| USB / Ethernet | project **~23 mm past the board's A-edge** — fully accessible, cannot foul |
| microSD end | ~38 mm inside the board's J′ edge |
| Numbers 47 → 25 | the Pi, underneath |
| Numbers 24 → 1 | free board over open air — **the working area** |
| Assembly footprint | ~**150 × 123 mm**, fits the 170 mm box |

Note the pin order: **Pi pin numbers run from letter T up toward letter A**, because the Pi's
pin 1 is at its microSD end. Counter-intuitive; write it on the board.

> ⚠ **Plug the micro-USB in BEFORE lowering the board.** The board roofs that edge by ~75 mm
> at 8.5 mm height. It fits, but you do not want to be feeding a plug under it. This goes
> away at deployment when 5 V moves to pins 2/4 (§2).

---

## 2. Power topology — settled 2026-09-11

Both adapters on hand are used, as two rails with a common ground. This is §8.3 of
`HANDOFF.md` built from parts already owned.

```
  5 V 2 A adapter ──────────────────────────▶  Pi        (~1.3 A peak)
  9 V 1.5 A adapter ──▶ LM2596 @ 5.00 V ────▶  MQ heaters only  (~0.4 A)
                                                └─ grounds common at the board GND rail
```

**Why not one supply.** The 9 V 1.5 A is the bigger source once bucked (13.5 W vs 10 W) and
could run everything. It must not: the whole point of the split is keeping the MQ heaters'
switching step load off the Pi's rail. One supply rebuilds fault F1/F2 with a nicer
regulator in the middle. Split, each adapter runs at about half its rating.

**Set the LM2596 to 5.00 V on the meter before it is connected to anything.** These ship at
arbitrary voltages, often 15–20 V.

### Pi 5 V: micro-USB now, direct later

> ⚠ **Correction 2026-09-13 — the Pi's 5 V never goes through rail 41.** Rail 41 is the
> **MQ heater rail**, fed from the LM2596. An earlier version of this section said "at
> deployment, link rail 41 to Pi pins 2/4" — that would put the heaters' switching load back
> on the Pi's supply and undo the whole split. **The Pi's 5 V adapter lands directly on
> `(47,T)` and `(47,S)` via its own terminal. Rail 41 stays heater-only. Only the grounds join,
> at rail 45.**
>
> **First power-on, 2026-09-13:** rail 43 read **3.26 V** from the Pi — board working. The
> monitor showed the rainbow screen then "no signal", which looked like undervoltage on the
> long micro-USB cable **but was not**: red LED steady, green LED blinking (normal boot). It is
> an HDMI setting issue, not power. **Micro-USB stays for the bench.** Both remaining adapters
> are round barrel plugs, so a GPIO feed would need a barrel socket or cut lead — deferred to
> deployment, with the rules above (USB unplugged, polarity metered, 2 A fuse).
Feeding 5 V into Pi pins 2/4 is better for the deployed instrument — a micro-USB plug on a
rooftop works loose and corrodes, and this rebuild exists to delete fragile connections. But
it bypasses the Pi's 2.5 A polyfuse, and the USB is convenient on the bench. So:

- **Now:** Pi on micro-USB. **The 5 V rail's link to Pi pins 2/4 is left unmade.**
- **At deployment:** add those two joints, fit a **2 A inline fuse**, stop using micro-USB.
- **Label those two pads:** `PI 5V — LINK AT DEPLOY ONLY. NEVER WITH USB.` Two supplies
  fighting is the one way to damage something here.

---

## 3. Layout map

```
  letter   A   C   E   G   I   K   M   O   Q   S   U   W   Y   A′  C′  E′  G′  I′
        ┌────────────────────────────────────────────────────────────────────────┐
   48   │▓▓▓▓▓▓▓▓▓▓▓ HEADER  pin39/40 ◄── A … T ──► pin 1 ▓▓▓▓│                  │
   47   │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│                  │
   45   │══════════════════ GND RAIL ═══════════════════════════════════════════ │
   43   │────────────────── +3.3 V RAIL ───────────────────────────────────────  │
   41   │────────────────── +5 V RAIL ─────────────────────────────────────────  │
        │                                                                        │
   38   │   MCP3208                          │   I2C BREAKOUT                    │
   ..   │   pin 1 at (38, D)                 │   letters P → Y, numbers 38 → 33  │
   31   │   pins 1-8  letter D               │   BMP280 0x76 · OLED · DS3231     │
        │   pins 9-16 letter G               │                                   │
        │   C1 100nF  letter I, numbers 38-37│   R1 4k7  P → S  ┐ numbers 30-29  │
   28   │                                    │   R2 4k7  V → Y  ┘                │
   ..   │   MQ DIVIDERS R3-R6                │                                   │
   22   │   letters A → H                    │   free ADC: CH3 CH4 CH5 CH6 CH7   │
        │   C2 1000µF letters K → N, 28 → 25 │                                   │
        │          ANALOGUE ←────────────────┼────────────────→ DIGITAL          │
        │                                    divide at letter ~N                 │
    6   │══════ SCREW TERMINALS  MAST 8 │ SOIL 4 │ POWER 2 ══════════════════    │
    3   │══════ letters A → J′ along the number-1 edge, over air ═══════════     │
    1   └────────────────────────────────────────────────────────────────────────┘
```

Rails run **across the letters**, parallel to the header, so every tap from a header pin is a
short vertical hop. Drop spurs down the board where a component sits far from a rail.

**Which of numbers 48 / 47 is the odd Pi row is not predictable from here** — the Pi marks
pin 1 with a square pad. Identify it at dry-fit and write `ODD` / `EVEN` and a pin-1
triangle on the board before the Pi comes off.

### Which way round you are looking — READ THIS BEFORE ANY ASCII MAP

**The board is single-sided:** copper pads on one face, bare phenolic on the other. The header
bodies were fitted on the bare face and the tails soldered on the copper face, so **the copper
face points UP, away from the Pi, and the Pi sits under the bare face.** Components insert
from the bare side and are soldered from the copper side, as normal.

> ⚠ **Never take an orientation from "left" or "right" in a drawing.** The two faces are
> mirror images, so any ASCII map is correct on one face and backwards on the other. **Read
> the silkscreen letter printed beside the pad. That is the only statement that is true from
> both sides.** An attempt on 2026-09-12 to write down which face has letter A on which hand
> was wrong, and is deliberately not recorded here — the coordinate is the truth, the view is
> not.

**Consequence, found the same day:** inserting a DIP from the bare side with its notch toward
number 38 leaves you **no choice** about which column pin 1 lands in — the body must stay on
the bare face, so the chip cannot be flipped. The MCP3208 came out **pin 1 at (38, G)**, and
that is not an error to correct but the board's answer. The wiring was mirrored to suit.

### Component bodies: which side they mount on

The copper face is up and the **Pi is underneath the bare face**, so a part mounted the normal
way hangs *down into the Pi gap* — about 10 mm, less whatever the Pi has under that spot.

> **Rule: anything taller than ~6 mm mounts on the TOP (copper) side, standing up into the
> box's headroom.** Everything short mounts normally underneath.

- **Underneath (normal):** MCP3208 (~4 mm), resistors, ceramic caps.
- **On top:** **C2, the 1000 µF electrolytic** — that can is 15–20 mm tall and §3 currently
  places it at numbers 28→25, directly over the Pi, where it **cannot physically fit**. Also
  the screw terminals.

### Notation

**(number, letter)** — `(47, R)` is the pad in number-row **47**, letter-column **R**.
Numbers are the long 150 mm axis, letters the short 100 mm axis.

### The full 40-pad map — AS BUILT

Header soldered **2026-09-11** at **numbers 48 and 47, letters A → T**. Pi pin 1 is at
letter **T**; pin numbers run **T → A**, backwards from the letters. Number 48 carries the
ODD pins, number 47 the EVEN.

```
  letter    A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T
  num 48   39  37  35  33  31  29  27  25  23  21  19  17  15  13  11   9   7   5   3   1
  num 47   40  38  36  34  32  30  28  26  24  22  20  18  16  14  12  10   8   6   4   2

  GND ->    G   .   .   .   .   .   .   G   .   .   .   .   .   .   .   G   .   .   .   .      (number 48 row)
            .   .   .   G   .   G   .   .   .   .   G   .   .   G   .   .   .   G   .   .      (number 47 row)
```

`G` marks a Pi ground pin (6, 9, 14, 20, 25, 30, 34, 39). With the board seated, all eight
of those pads are continuous with the metal USB/Ethernet shells — which is how the map was
verified rather than assumed.

### Pin map — every pad you need, by board coordinate


**Number 48 = the Pi’s ODD pins (1,3…39). Number 47 = EVEN (2,4…40).** The Pi’s pin-1 row is
its outer row, and that is the one landing on number 48, away from the Pi body. **Confirm on
first seating** and write it on the board.

Pin numbers run **T → A** (pin 1 at T, pin 39/40 at A):

```
  letter    T  S  R  Q  P  O  N  M  L  K  J  I  H  G  F  E  D  C  B  A
  num 48    1  3  5  7  9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39   ODD
  num 47    2  4  6  8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40   EVEN
```

| Signal | Pi pin | Pad(s) | Goes to |
|---|---|---|---|
| +3.3 V | 1, 17 | **(48, T)** + **(48, L)** | rail at number 43 |
| GND | 6, 20 | **(47, R)** + **(47, K)** | rail at number 45 - at least TWO |
| +5 V | 2, 4 | **(47, T)** + **(47, S)** | **LEAVE UNCONNECTED** - see section 2 |
| SDA | 3 | **(48, S)** | I2C breakout |
| SCL | 5 | **(48, R)** | I2C breakout |
| 1-WIRE | 7 | **(48, Q)** | DS18B20 + R1 to 3V3 |
| DHT-DATA | 16 | **(47, M)** | DHT22 + R2 to 3V3 |
| MOSI | 19 | **(48, K)** | MCP3208 pin 11 Din |
| MISO | 21 | **(48, J)** | MCP3208 pin 12 Dout |
| SCLK | 23 | **(48, I)** | MCP3208 pin 13 CLK |
| CE0 | 24 | **(47, I)** | MCP3208 pin 10 CS |

### MCP3208 (DIP-16), pin 1 at (38, G) — AS BUILT 2026-09-12

Notch toward number 38. **Column G, numbers 38→31 = pins 1–8 = CH0–CH7** (all still bare).
**Column D, numbers 38→31 = pins 16 down to 9** — the whole working side.

| Pin | Pad | Net / goes to |
|---|---|---|
| 16 VDD | `(38, D)` | 3V3 rail |
| 15 VREF | `(37, D)` | 3V3 rail |
| 14 AGND | `(36, D)` | GND rail |
| 13 CLK | `(35, D)` | `(48, I)` — Pi pin 23, SCLK |
| 12 Dout | `(34, D)` | `(48, J)` — Pi pin 21, **MISO** |
| 11 Din | `(33, D)` | `(48, K)` — Pi pin 19, **MOSI** |
| 10 CS | `(32, D)` | `(47, I)` — Pi pin 24, CE0 |
| 9 DGND | `(31, D)` | GND rail |

`Din` takes MOSI and `Dout` takes MISO — the pair crosses over. This is the joint that gets
wired backwards.

```
  col   B    C    D         G
  43   ┃    ·   ═╤═ 3V3 tap enters column D
  41   ┃    ·    ┃  (both wires insulated across the 5 V rail)
  38   ┃    ●────● 16 VDD          1 CH0
  37   ┃    ·    ● 15 VREF         2 CH1
  36   ●────●────● 14 AGND         3 CH2
  35   ┃    ·    ● 13 CLK          4 CH3
  34   ┃    ·    ● 12 Dout         5 CH4
  33   ┃    ·    ● 11 Din          6 CH5
  32   ┃    ·    ● 10 CS           7 CH6
  31   ●────●────●  9 DGND         8 CH7
```

**Two insulated wires only** — `(43,D) → (38,D)` for 3.3 V, and `(45,B) → (36,B)` for ground.
Column B is a **ground spur**: one wire dropped from the GND rail past both other rails,
landing at 36, then bare from 36 down to 31. It exists so the chip's two ground pins need
**two** rail crossings between them instead of four.

**Bare staples:** `(38,D)–(37,D)` · `(36,B)–(36,C)–(36,D)` · `(36,B)→(31,B)` ·
`(31,B)–(31,C)–(31,D)`.

**C1** (100 nF ceramic, body marked `104`) stands in column C between numbers **38 and 36** —
5.08 mm, a standard 5 mm part. `(36,C)` is already ground from the staple; `(38,C)` staples
across to `(38,D)`. It sits ~3 mm from VDD and AGND, which is the only placement that works.

> **No socket was available, so the chip is soldered direct.** That means VDD↔GND can no
> longer be tested in isolation. The substitute check is that **3V3 rail ↔ GND rail must not
> buzz** — the chip's own leakage is megohms, so a buzz means a bridged staple or a shorted
> C1, never the chip.

## 4. Steps and gates

- [x] **1a** Header strips cut to 1×20, both seat flat on all 40 Pi pins
- [x] **1b** Micro-USB plug clears the overhang
- [x] **1c** Oval edge pads metered — isolated, not rails
- [ ] **1d** Passives metered: resistors ≈4.7 kΩ (two **matched pairs** set aside for the MQ
      dividers), ceramics marked `104`, electrolytics 1000 µF — note the polarity stripe
- [ ] **1e** LM2596 trimmed with nothing connected to its output — **module on hand is an
      LM2587S boost (2026-09-13); a real LM2596 must be bought first**
- [x] **1f** CR2032 reads **≥3.0 V** unloaded — **3.2 V, 2026-09-13.** Safe on the DS3231 module
      because it runs at 3.3 V: the module's charging path (diode + resistor from VCC) then sits
      below the cell voltage, so a non-rechargeable CR2032 is not charged

### Step 4 — the header
Use the Pi as the jig; it is the only thing that guarantees alignment.

- [x] Both strips on the Pi, board down on the tails, orientation per §1 — header across
      **letters A → T on numbers 48 and 47**
- [x] **Sight the Ethernet jack: it should stick out ~23 mm PAST the board’s A-edge.**
      If any board is over it, stop — the position is wrong
- [x] **Tack two pins only**, one at each far corner. 2 seconds each
- [x] **Pull the Pi off** — do not solder the other 38 with it attached
- [x] Check both strips sit flat and square; reheat a single tack to correct
- [x] Solder the remaining 38 tails. ~350 °C, **under 3 s per pad** (phenolic lifts pads)
- [x] Mark pin 1 with a triangle at **letter T**; write `ODD` / `EVEN` against numbers 48/47,
      and write `pin 1 → T,  pin 39/40 → A` on the board — the order is counter-intuitive
- [x] Re-seat on the Pi dry, confirm it still goes down clean

- [x] **2026-09-11 — bridge test PASSED.** Board off the Pi, every one of the 40 tails
      metered open against its neighbours in both rows. Do this *before* rails go on: with
      no rails fitted every pad is isolated, so a bridge is trivial to find. Afterwards it
      is not.
- [x] **2026-09-11 — map verified on the Pi.** Probed a metal USB shell against each pad;
      exactly the eight `G` pads beeped and nothing else. So **pin 1 is at letter T and
      number 48 is the ODD row** — measured, not assumed. Everything downstream depends on
      this, so it is recorded rather than re-derived.

### Step 5 — the rails
Order is **GND → 3.3 V → 5 V**. Solid core stripped from an old ethernet cable lies flat and
is ideal; failing that, drag solder pad to pad.

- [x] **Number 45, GND**, letters A → J′, one continuous flooded strip — **2026-09-12**
- [x] GND tied to Pi pins **6 and 20** — two pins, far apart. A thin shared return is a
      classic cause of F2
- [x] **Number 43, +3.3 V**, letters A → J′, tied to Pi pins **1 and 17** — **2026-09-12**
- [x] **Number 41, +5 V**, letters A → J′, tied to **nothing on the Pi**. Pads for pins 2/4
      left bare and labelled — **2026-09-12**

**Tap routing — decided 2026-09-12.** Both 3.3 V taps are *insulated*; they cross the GND
rail. The pin-1 tap leaves `(48,T)` and hops **sideways into column U** before going down,
landing on the rail at `(43,U)`. Letters U → J′ are empty board, so that route passes only
the GND rail — whereas straight down column T it would pass `(47,T)` = Pi pin 2 = **+5 V**,
and a 3V3↔5V short is the worst fault this board can carry. The pin-17 tap runs straight
down column L; it passes GPIO24 at `(47,L)`, a signal, harmless.

> **A rail's `A ↔ J′` continuity check proves the WIRE, not the JOINTS.** It passes with only
> the two end pads soldered. Walk one probe down every pad ring in the row against a fixed
> probe on the rail — a pad that is touching the wire but not bonded reads open, and will
> pass every bench test until vibration finds it. Caught on the GND rail, 2026-09-12.

### ⛔ GATE — board OFF the Pi, before it is ever powered

| Check | Must read |
|---|---|
| GND ↔ 3V3 | **open** |
| GND ↔ 5V | **open** |
| 3V3 ↔ 5V | **open** |
| each rail, letter A to letter J′ | **short** |
| Pi pin 6 pad ↔ pin 20 pad | **short** |
| Pi pin 1 pad ↔ pin 17 pad | **short** |

- [x] **All seven pass — 2026-09-12.** Board is now safe to power.

A shorted rail found with a meter costs nothing. Found after power-up it costs the Pi.

### Step 6 — components
- [x] MCP3208 pin 1 at **(38, G)**, notch toward number 38 + C1 in column C — soldered
      2026-09-12, **SPI wires fitted and ADC gate PASSED 2026-09-13**
- [ ] R1 (1-Wire → 3V3), R2 (DHT22 → 3V3 — **check the module isn't already fitted with one**, U6)
- [ ] R3–R6 MQ dividers, matched pairs; put the measured `(R1+R2)/R2` into `sensors/config.py:26`
- [ ] C2 1000 µF on the 5 V rail, polarity checked
- [ ] Every net buzzed against sheet 1 (`docs/drawings/schematic.svg`)

### Step 7 — terminals
- [ ] 14 ways fitted, **numbers 6 → 3**, along the number-1 edge
- [ ] **Every way labelled on the board in indelible pen.** The masking-tape flags on the
      demo build are why this rebuild exists

### Step 8 — bring-up
- [x] **ADC proven 2026-09-13** — CH0 swings 0 ↔ 4095 on a jumper, CH1/CH2 unaffected
- [ ] On the Pi. `python3 tests/test_all.py --skip camera`
- [ ] Sensors **one at a time**: I2C trio → MCP3208 + soil → DS18B20 → DHT22 → MQ pair

---

## 5. Session log

### 2026-09-13 (cont.) — GPIO power, undervoltage persists, "buck" is a boost
- **Pi now powered through its GPIO pins.** 5 V 2 A barrel adapter, red → `(47,W)`, black →
  `(45,Y)` on the GND rail; insulated `(47,W)→(47,T)` Pi pin 2, staple `(47,T)–(47,S)` pin 4.
  Cable taped for strain relief. All checks passed; `(47,T)` read 5.2 V; **micro-USB removed.**
  **Rail 41 is not involved** — it stays the heater rail.
- Pi boots, monitor and SSH work (`iesh.local` / `192.168.5.100`). SPI already enabled in
  `config.txt`; `/dev/spidev0.0` present.
- **Undervoltage NOT fixed.** `throttled=0x50005`, `hwmon: Undervoltage detected` flickering
  every few seconds **even at idle** — though `(47,T)` meters **5.17 V** under load. The meter
  shows an average; the Pi trips on millisecond dips. The long micro-USB cable was not the
  whole cause — **the adapter is.** F1 is still open.
- **U5 was wrong.** The module believed to be an LM2596 buck reads **`LM2587S`** — a boost. With
  12 V in it gave 30 V and would not trim below ~11.2 V. **Nothing was connected to its output.**
  Needs a real LM2596 (~₨150–200, SLT). Plan once bought: **12 V 2 A → LM2596 @ 5.20–5.25 V →
  Pi leads**, the buck's screw terminals becoming the point where the board unplugs for the box.
- **Decision: no buck converter will be bought.** Power is built from what is on hand:
  **5 V 2 A barrel adapter → Pi via GPIO**, with the 1000 µF capacitor at the feed to absorb the
  dips. If undervoltage persists, the next try is the known-good USB charger with its cable
  **cut short** and wired to the board, since the long cable — not that charger — was suspect.
  The MQ heaters (rail 41) will take whichever 5 V source is not feeding the Pi. The 9 V and
  12 V adapters and the LM2587S boost have no role in this build.
- **1000 µF capacitor fitted at the Pi feed**, + at `(46,W)` stapled to `(47,W)`, − at `(45,W)`.
  **Idle undervoltage gone** — only two dips during boot, then clean. **Under a 60 s 4-core
  load it still flags undervoltage continuously (`0x50005`).** The capacitor fixes transients,
  not a supply that cannot hold sustained current. F1 is improved, not closed.
- The Pi restarted once while `(47,T)` was being probed under load — no undervoltage showed in
  the samples just before it, so a probe slipping onto `(48,T)` (3.3 V) is the likely cause. A
  second restart was a deliberate unplug. **Rule: never probe the header pins with the Pi
  powered — measure the 5 V feed on the capacitor legs `(46,W)`→`(45,W)` instead.**
- **✅ ADC PROVEN END TO END** (`tests/test_mcp3208.py`). Floating, CH0–CH2 drift slowly
  0–420 (normal for unconnected inputs). **Jumper `(38,G)` → rail 43: CH0 = 4088–4095. → rail
  45: CH0 = 0000.** CH1 and CH2 did not follow, so the channels are isolated. This proves the
  header, both 3.3 V ties, the ground spur, C1, all four SPI wires and the chip together.

### 2026-09-13 — SPI wires in, ADC gate PASSED
- Started the ADC gate and found **group 3 (chip → header) all silent**: the four SPI wires
  had never been fitted. Continuity needs no power, so silence was a real open, not a quirk.
- **SPI wires fitted:** `(35,D)→(48,I)`, `(34,D)→(48,J)`, `(33,D)→(48,K)`, `(32,D)→(47,I)`.
- **The pin-17 3.3 V tap `(48,L)→(43,L)` pulled out** while working near the header.
  Re-soldered with slack in the wire, then re-ran every check near the header — including
  `(48,T)↔(47,T)` open and all SPI header pads open to their neighbours. All pass.
- **Meter lesson — readings of `600`–`800` in continuity mode are diodes, not shorts.** The
  meter shows millivolts across the path. Every MCP3208 pin has an internal protection diode
  to VDD (the 3.3 V rail), so SPI and CH pads read ~700 against rail 43. **Test: swap the
  probes.** A diode reads ~700 one way and `1` (open) the other; a real short reads near 0
  both ways. Confirmed on the bench.
- **ADC gate PASSED — all five groups.** Board is ready for first power-on.

### 2026-09-12 — all three rails in, MCP3208 fitted
- **GND rail soldered at number 45**, letters A → J′, bare solid copper laid on the pads.
  Tapped to Pi pin 6 at `(47,R)` and pin 20 at `(47,K)` — two ties, far apart, deliberately.
  Both pins are already one net inside the Pi; the second tie exists to halve the return
  resistance and survive a cracked joint, not to make a new connection.
- **Lesson, caught on this rail:** the `A ↔ J′` continuity check passes with only the two end
  pads soldered, because it measures the wire. Several mid-run pads were sitting on the wire
  unbonded. Re-flowed, then verified pad-by-pad. Recorded in §4 so it is not re-learned.
- **+3.3 V rail soldered at number 43**, letters A → J′, tapped to Pi pins 1 and 17 with
  *insulated* wire over the GND rail. Pin-1 tap routed via column U — see §4.
- Bare solid copper used throughout rather than stripped ethernet core; the board had plenty
  on hand. Solder is rosin-cored, so no flux pen was needed — the rule that replaced it is
  **fresh solder at every joint, never drag an old blob**, since remelted solder has no flux
  left and that is what makes the grey high-resistance joints that are fault F2.

### 2026-09-11 — header in, map verified
- Board chosen: blank `PY-10CM*15CM`, **uncut**. Old demo board set aside intact — bill 884
  bought a second MCP3208, so nothing has to be desoldered from it.
- Coordinates established from the silkscreen: **numbers 1–48 on the long 150 mm axis,
  letters A–Z/A′–J′ (36) on the short 100 mm axis**, origin at the `48, A` corner.
- **Two wrong turns worth remembering.** First, a layout put the board 12 mm over the
  Ethernet jack: the arithmetic used the 122 mm *grid* and ignored the ~14 mm oval-pad strip
  outside number 48 — *the grid is not the board edge.* Second, the fix proposed was to
  rotate the header; that was also wrong, and the right answer was the user's — run the
  header **across the letters**, which puts the USB and Ethernet ~23 mm clear of the board
  entirely and removes the collision rather than tuning around it.
- Female strips cut from `1×40` to `1×20`; both seat flat on all 40 Pi pins.
- **Header soldered: numbers 48 and 47, letters A → T.**
- **Bridge test PASSED** — all 40 tails open to their neighbours, done before any rail went
  on, while every pad was still isolated.
- **Map verified PASSED** — USB shell probed against each pad, exactly the eight `G` pads
  beeped. **Pin 1 is at letter T; number 48 is the ODD row.** Measured, not assumed.
- Power topology settled (§2): both adapters, split rail, Pi on micro-USB for now.

---

## 6. Open

- **Power accepted as-is for bench work (2026-09-13, user decision):** 5 V 2 A adapter via GPIO + 1000 µF. Idle clean, sustained load still undervolts. **Deferred:** trim the Pi's load in software — `arm_freq` cap, HDMI/Bluetooth/Wi-Fi off when unused, unused services disabled — and optionally try the 5 V 2 A mobile charger. Re-check `vcgencmd get_throttled` before the 24 h gate (F5).
- **No buck converter, by decision (2026-09-13).** Module on hand is an LM2587S boost; not buying an LM2596.
- **F1 undervoltage still present** on the 5 V 2 A adapter via GPIO (`0x50005`).
- **`docs/drawings/perfboard.svg` is stale** — generated for 57 × 37 ascending columns. This
  board is 48 × 36 descending. Regenerate `scripts/gen_drawings.py` to match §3.
- **The CAD is stale** — `roofbox.scad` and `roofbox_check.py` still model the old
  120 × 120 × 180 box. See the warning in `HANDOFF.md` §5.
- **No camera FFC** (not stocked at SLT), so the 110 mm ribbon still forces lid-up (§16.1).
- **Passives not yet metered** (1d) — resistors need two *matched pairs* picked out for the
  MQ dividers, and the measured `(R1+R2)/R2` written into `sensors/config.py:26`.
- **LM2596 not yet trimmed to 5.00 V** (1e). It must be set with nothing connected to its
  output — these ship at 15–20 V and would destroy both MQ modules.
