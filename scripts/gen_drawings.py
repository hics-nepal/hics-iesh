#!/usr/bin/env python3
"""Generate the IESH v0.2 2D build drawings as SVG.

Why scripted rather than hand-drawn: the net list below is the single source of
truth for both sheets, so the schematic and the perfboard placement cannot drift
apart, and a pin change is one edit. Output is plain SVG — scalable, printable
at 1:1, editable in Inkscape, and usable directly in poster artwork.

    python3 scripts/gen_drawings.py
    -> docs/drawings/schematic.svg
    -> docs/drawings/perfboard.svg

Pin assignments are read from the same values as sensors/config.py; if you change
one there, change it here. The header pin numbers are physical (1-40).
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'docs', 'drawings')

# ── palette: readable printed, and on a dark poster ─────────────────────────
INK   = '#1a1d21'   # main linework / text
MUTE  = '#6b7280'   # secondary text, dimensions
RAIL5 = '#d94f3d'   # 5 V
RAIL3 = '#e0932f'   # 3.3 V
GND   = '#3f4650'   # ground
I2C   = '#2f7fb5'   # I2C bus
SPI   = '#6a4fa3'   # SPI bus
SIG   = '#2e8b6f'   # single-ended signals
PAPER = '#fbfaf8'
BOARD = '#e8ded0'   # perfboard substrate
ACC   = '#b03a2e'

# ── the net list: (pin, gpio, net, colour, destination) ─────────────────────
HEADER = [
    (1,  '3V3',    '+3.3 V',      RAIL3, 'MCP3208 VDD+VREF · I2C trio · pull-ups · soil probe'),
    (2,  '5V',     '+5 V',        RAIL5, 'DHT22 · MQ-7 + MQ-135 heaters'),
    (3,  'GPIO2',  'SDA',         I2C,   'BMP280 0x76 · OLED 0x3C · DS3231 0x68'),
    (5,  'GPIO3',  'SCL',         I2C,   'same three devices'),
    (6,  'GND',    'GND',         GND,   'ground bus'),
    (7,  'GPIO4',  '1-WIRE',      SIG,   'DS18B20 data  (+4k7 pull-up to 3V3)'),
    (16, 'GPIO23', 'DHT-DATA',    SIG,   'DHT22 data  (+4k7 pull-up to 3V3)'),
    (19, 'GPIO10', 'MOSI',        SPI,   'MCP3208 pin 11  Din'),
    (21, 'GPIO9',  'MISO',        SPI,   'MCP3208 pin 12  Dout'),
    (23, 'GPIO11', 'SCLK',        SPI,   'MCP3208 pin 13  CLK'),
    (24, 'GPIO8',  'CE0',         SPI,   'MCP3208 pin 10  CS/SHDN'),
]

MCP = [  # (pin, name, net)
    (1,  'CH0',  'MQ7-DIV'),   (16, 'VDD',  '+3.3 V'),
    (2,  'CH1',  'MQ135-DIV'), (15, 'VREF', '+3.3 V'),
    (3,  'CH2',  'SOIL-AOUT'), (14, 'AGND', 'GND'),
    (4,  'CH3',  'RAIN-AOUT'), (13, 'CLK',  'SCLK'),
    (5,  'CH4',  'LDR-DIV'),   (12, 'Dout', 'MISO'),
    (6,  'CH5',  '—'),         (11, 'Din',  'MOSI'),
    (7,  'CH6',  '—'),         (10, 'CS',   'CE0'),
    (8,  'CH7',  '—'),         (9,  'DGND', 'GND'),
]

# Screw terminals: (label, ways, [(way, net, colour)])
TERMINALS = [
    ('MAST  CAT5e  8-way', [
        ('1', '+5 V',      RAIL5), ('2', 'GND',        GND),
        ('3', '+3.3 V',    RAIL3), ('4', 'GND',        GND),
        ('5', 'DHT-DATA',  SIG),   ('6', 'MQ7-AOUT',   SIG),
        ('7', 'MQ135-AOUT',SIG),   ('8', 'RAIN/LDR',   SIG)]),
    ('SOIL  CAT5e  4-way', [
        ('1', '+3.3 V',    RAIL3), ('2', 'GND',        GND),
        ('3', 'DS18B20',   SIG),   ('4', 'SOIL-AOUT',  SIG)]),
    ('POWER  2-way', [
        ('1', '+5 V in',   RAIL5), ('2', 'GND',        GND)]),
]

PASSIVES = [
    ('R1', '4k7',   '1-WIRE (GPIO4) -> +3.3 V',      'mandatory - 1-Wire will not work without it'),
    ('R2', '4k7',   'DHT-DATA (GPIO23) -> +3.3 V',   'omit if your DHT22 breakout already has one'),
    ('R3', '4k7',   'MQ7-AOUT -> MQ7-DIV',           'divider upper leg'),
    ('R4', '4k7',   'MQ7-DIV -> GND',                'divider lower leg'),
    ('R5', '4k7',   'MQ135-AOUT -> MQ135-DIV',       'divider upper leg'),
    ('R6', '4k7',   'MQ135-DIV -> GND',              'divider lower leg'),
    ('C1', '100nF', 'MCP3208 VDD -> GND',            'local decoupling, close to the chip'),
    ('C2', '1000uF','+5 V -> GND, at the MQ feed',   'absorbs the heater step load'),
]


def tint(hexcol, amount=0.13, toward=PAPER):
    """Blend a colour toward the paper. Used instead of fill-opacity, which
    several SVG rasterisers silently ignore - the zones came out fully opaque
    and buried their own labels."""
    def parts(h):
        h = h.lstrip('#')
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    a, b = parts(hexcol), parts(toward)
    m = [round(a[i] * amount + b[i] * (1 - amount)) for i in range(3)]
    return '#%02x%02x%02x' % tuple(m)


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# Plain font names, deliberately: quoted multi-family stacks break several SVG
# rasterisers (ImageMagick among them), and these two are present everywhere.
def txt(x, y, s, size=11, fill=INK, anchor='start', weight='400',
        family='monospace', ls='0'):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" letter-spacing="{ls}">{esc(s)}</text>')


def sans(x, y, s, size=11, fill=INK, anchor='start', weight='400', ls='0'):
    return txt(x, y, s, size, fill, anchor, weight, 'sans-serif', ls)


def rect(x, y, w, h, fill='none', stroke=INK, sw=1.2, rx=2, extra=''):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def line(x1, y1, x2, y2, stroke=INK, sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d} stroke-linecap="round"/>')


def dot(x, y, r=2.6, fill=INK):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"/>'


def header_block(W, title, sub):
    o = [rect(0, 0, W, 999999, PAPER, 'none', 0, 0)]
    o.append(sans(38, 52, 'HICS  IESH v0.2', 13, MUTE, weight='600', ls='2.5'))
    o.append(sans(38, 84, title, 27, INK, weight='700'))
    o.append(sans(38, 106, sub, 12.5, MUTE))
    o.append(line(38, 122, W - 38, 122, INK, 1.6))
    return o


def legend(x, y):
    items = [('+5 V', RAIL5), ('+3.3 V', RAIL3), ('GND', GND),
             ('I2C', I2C), ('SPI', SPI), ('signal', SIG)]
    o = [sans(x, y - 10, 'NETS', 9.5, MUTE, weight='700', ls='1.5')]
    for i, (n, c) in enumerate(items):
        yy = y + i * 17
        o.append(line(x, yy, x + 22, yy, c, 3))
        o.append(txt(x + 29, yy + 3.5, n, 10, MUTE))
    return o


# ════════════════════════════════════════════════════════════════════════════
#  SHEET 1 — system wiring schematic
# ════════════════════════════════════════════════════════════════════════════
# Layout is ZONED into non-overlapping bands so nothing can collide:
#   A x 60-370   Pi header          B x 420-560   bus rails
#   C x 610-1010 MCP3208 + I2C      D x 1060-1560 terminals + destinations
#   bottom band y 690-1120          passives, legend, notes
def schematic():
    W, H = 1620, 1120
    A, B, C, D = 60, 430, 620, 1070
    TOP, ROW = 190, 38
    o = header_block(W, 'Wiring schematic',
                     'Raspberry Pi 3B+ - protoboard HAT - MCP3208 - six sensor channels.   '
                     'Every net is named, and the net name is what you write on the wire.')

    # ── zone A: Pi header ───────────────────────────────────────────────────
    ph = TOP + len(HEADER) * ROW + 26
    o.append(rect(A, TOP - 46, 310, ph - TOP + 46, '#eef3ee', '#2f6b46', 1.6, 4))
    o.append(sans(A + 16, TOP - 22, 'Raspberry Pi 3B+', 15, '#2f6b46', weight='700'))
    o.append(txt(A + 16, TOP - 6, '40-pin header, physical pin numbers', 9, MUTE))

    rowy = {}
    for i, (pin, gpio, net, col, _d) in enumerate(HEADER):
        y = TOP + 22 + i * ROW
        rowy[net] = y
        o.append(rect(A + 16, y - 12, 32, 23, col, 'none', 0, 3))
        o.append(txt(A + 32, y + 4, str(pin), 11, '#fff', 'middle', '700'))
        o.append(txt(A + 58, y + 4, gpio, 10.5, INK, weight='600'))
        o.append(txt(A + 124, y + 4, net, 10.5, col, weight='700'))

    # ── zone B: bus rails, each in its own lane, ending above the bottom band
    RAIL_BOT = ph - 14
    railx = {}
    for i, (nm, col) in enumerate([('+5 V', RAIL5), ('+3.3 V', RAIL3), ('GND', GND)]):
        x = B + i * 46
        railx[nm] = x
        o.append(line(x, TOP - 4, x, RAIL_BOT, col, 3.6))
        o.append(txt(x, TOP - 16, nm, 8.5, col, 'middle', '700'))
        y = rowy[nm]
        o.append(line(A + 326, y, x, y, col, 2.2))
        o.append(dot(x, y, 3.4, col))

    def to_rail(nm, y, side=1):
        """Stub from a rail to something at height y."""
        x = railx[nm]
        return [line(x, y, x + side * 26, y, railx and {'+5 V': RAIL5, '+3.3 V': RAIL3,
                                                        'GND': GND}[nm], 2), dot(x, y, 3.4,
                {'+5 V': RAIL5, '+3.3 V': RAIL3, 'GND': GND}[nm])]

    # ── zone C: MCP3208 ─────────────────────────────────────────────────────
    PITCH = 26                      # tightened so the I2C block clears the
    mw, mh = 250, 62 + 8 * PITCH + 18   # bottom band divider
    mx, my = C + 66, TOP + 6
    o.append(rect(mx, my, mw, mh, '#fff', INK, 1.5, 3))
    o.append(txt(mx + mw / 2, my + 24, 'MCP3208', 13, INK, 'middle', '700'))
    o.append(txt(mx + mw / 2, my + 40, 'DIP-16   8-channel 12-bit ADC', 8.5, MUTE, 'middle'))
    left = [q for q in MCP if q[0] <= 8]
    right = sorted([q for q in MCP if q[0] >= 9], key=lambda q: -q[0])
    for i, (pin, name, net) in enumerate(left):
        y = my + 62 + i * PITCH
        o.append(txt(mx + 10, y + 4, f'{pin:>2}  {name}', 9.5, INK))
        if net != '—':
            o.append(txt(mx - 14, y + 4, net, 9, SIG, 'end', '700'))
            o.append(line(mx - 8, y, mx, y, SIG, 1.6))
    for i, (pin, name, net) in enumerate(right):
        y = my + 62 + i * PITCH
        o.append(txt(mx + mw - 10, y + 4, f'{name}  {pin:>2}', 9.5, INK, 'end')) 
        col = {'+3.3 V': RAIL3, 'GND': GND}.get(net, SPI)
        o.append(txt(mx + mw + 10, y + 4, net, 9, col, 'start', '700'))
        o.append(line(mx + mw, y, mx + mw + 6, y, col, 1.6))

    # SPI: stubs, not routed lines. The ADC's right-hand pins are already
    # labelled with these net names, so drawing four wires looping around the
    # chip restates the connection while reading as dangling ends.
    for net, pin in (('MOSI', 'Din 11'), ('MISO', 'Dout 12'),
                     ('SCLK', 'CLK 13'), ('CE0', 'CS 10')):
        y = rowy[net]
        o.append(line(A + 326, y, B + 128, y, SPI, 2))
        o.append(f'<path d="M {B+128:.0f} {y-4:.0f} l 9 4 l -9 4 z" fill="{SPI}"/>')
        o.append(txt(B + 146, y + 3.5, f'ADC {pin}', 8.5, SPI, weight='700'))

    # I2C bus block, below the ADC
    iy = my + mh + 76
    o.append(rect(mx - 40, iy, mw + 90, 112, '#fff', I2C, 1.5, 3))
    o.append(txt(mx - 28, iy + 22, 'I2C bus   @ 100 kHz  (was 400 kHz - fault F2)',
                 10.5, I2C, weight='700'))
    for i, (nm, addr, note) in enumerate([
            ('BMP280', '0x76', 'pressure - the only sensor kept inside'),
            ('DS3231', '0x68', 'RTC - fit a FRESH coin cell'),
            ('OLED',   '0x3C', 'bench commissioning only')]):
        y = iy + 44 + i * 22
        o.append(txt(mx - 28, y + 4, f'{nm:<8} {addr}', 9.5, INK, weight='600'))
        o.append(txt(mx + 74, y + 4, note, 8.5, MUTE))
    for k, net in enumerate(('SDA', 'SCL')):
        y = rowy[net]
        xg = C + 4 + k * 10
        o.append(line(A + 326, y, xg, y, I2C, 2))
        o.append(line(xg, y, xg, iy + 8 + k * 8, I2C, 2))
        o.append(line(xg, iy + 8 + k * 8, mx - 40, iy + 8 + k * 8, I2C, 2))

    # Single-ended signals cross the board untouched (bar their pull-up) and
    # land on a terminal. Drawn as short labelled stubs rather than lines run
    # across the whole sheet through the ADC - the terminal block already names
    # them, and a wire drawn over a chip reads as a connection to it.
    for net, dest in (('1-WIRE', 'SOIL way 3'),
                      ('DHT-DATA', 'MAST way 5')):
        y = rowy[net]
        o.append(line(A + 326, y, B + 128, y, SIG, 2))
        o.append(f'<path d="M {B+128:.0f} {y-4:.0f} l 9 4 l -9 4 z" fill="{SIG}"/>')
        o.append(txt(B + 146, y + 3.5, dest, 8.5, SIG, weight='700'))

    # ── zone D: terminals ───────────────────────────────────────────────────
    o.append(sans(D, TOP - 22, 'Screw terminals  ->  CAT5e', 15, INK, weight='700'))
    o.append(txt(D, TOP - 6, 'two cables leave the box, not six', 9, MUTE))
    y = TOP + 6
    for label, ways in TERMINALS:
        bh2 = 34 + len(ways) * 22
        o.append(rect(D, y, 480, bh2, '#fff', INK, 1.5, 3))
        o.append(txt(D + 14, y + 22, label, 11, INK, weight='700'))
        for k, (w, net, col) in enumerate(ways):
            yy = y + 40 + k * 22
            o.append(rect(D + 14, yy - 9, 19, 17, col, 'none', 0, 2))
            o.append(txt(D + 23.5, yy + 3.5, w, 9.5, '#fff', 'middle', '700'))
            o.append(txt(D + 42, yy + 3.5, net, 10, col, weight='700'))
            o.append(line(D + 156, yy, D + 186, yy, col, 1.8))
        y += bh2 + 16

    # ── bottom band ─────────────────────────────────────────────────────────
    BY = 724
    o.append(line(A, BY - 24, W - 38, BY - 24, INK, 1.4))

    o.append(sans(A, BY, 'PASSIVES   none of these are optional', 11.5, ACC, weight='700'))
    for i, (ref, val, where, why) in enumerate(PASSIVES):
        yy = BY + 24 + i * 19
        o.append(txt(A, yy, f'{ref:<3} {val:<7}', 9.5, INK, weight='700'))
        o.append(txt(A + 84, yy, where, 9.5, INK))
        o.append(txt(A + 320, yy, why, 8.5, MUTE))
    o.append(txt(A, BY + 24 + len(PASSIVES) * 19 + 16,
                 'Do NOT add I2C pull-ups: the Pi 3B+ already has 1k8 on GPIO2/GPIO3.',
                 9, ACC, weight='700'))

    dx = 700
    o.append(sans(dx, BY, 'WHERE EACH CHANNEL PHYSICALLY LIVES', 11.5, INK, weight='700'))
    dests = [
        ('DHT22',          'mast, in a radiation shield', 'NOT in the box - it would read the box'),
        ('MQ-7 / MQ-135',  'mast, downward vented pod',   'self-heating; a labelled proxy, not calibrated'),
        ('DS18B20',        'buried in a roof vase',       '100 mm deep'),
        ('Soil capacitive','same vase, blade vertical',   'pot the top 25 mm or it dies in weeks'),
        ('Raindrop',       'mast, plate at ~30 deg',      'optional - CH3 is free'),
        ('LDR',            'mast, facing up',             'optional - CH4 is free'),
        ('BMP280',         'inside, on the HAT',          'equalises through a 2 mm side-wall vent'),
        ('Pi camera',      'in the lid, fisheye sealed',  'forced by the 110 mm ribbon'),
    ]
    for i, (nm, where, note) in enumerate(dests):
        yy = BY + 24 + i * 19
        o.append(txt(dx, yy, nm, 9.5, INK, weight='700'))
        o.append(txt(dx + 130, yy, where, 9.5, SIG))
        o.append(txt(dx + 330, yy, note, 8.5, MUTE))

    o += legend(A, BY + 236)
    o.append(txt(A + 190, BY + 246,
                 'Generated by scripts/gen_drawings.py - edit the net list there, not this SVG.',
                 9, MUTE))
    o.append(txt(A + 190, BY + 262,
                 'HICS - Himalayan Institute for Contextual Sciences   -   IESH v0.2   -   Lalitpur rooftop',
                 9, MUTE))
    body = '\n'.join(o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
            f'{body}\n</svg>\n')


# ════════════════════════════════════════════════════════════════════════════
#  SHEET 2 — perfboard placement
# ════════════════════════════════════════════════════════════════════════════
# HONEST SCOPE: this is a ZONED PLACEMENT drawing, not a hole-exact routing
# diagram. The real board already has the MCP3208 and its power lines soldered,
# and authoring a hole-by-hole route without that board in hand would produce a
# drawing that is wrong in detail and trusted anyway. What is fixed here is what
# matters and can be known: which functional block sits where, which edge the
# terminals are on, and the separation rules. Count holes off the printed grid.
HOLES_X, HOLES_Y = 25, 27          # 65 x 70 mm at 2.54 mm pitch
PITCH_MM = 2.54

ZONES = [
    # (col0, row0, cols, rows, label, sub, colour)
    (2,  0,  21, 2,  '2x20 FEMALE HEADER  ->  Pi GPIO', 'SOLDER ON THE UNDERSIDE - it seats down onto the Pi', '#37474f'),
    (1,  3,  23, 2,  'POWER BUSES   +5 V / +3.3 V / GND', 'three continuous rails, each tied to two Pi GND/supply pins', RAIL5),
    (2,  6,  10, 8,  'MCP3208  DIP-16', 'ALREADY SOLDERED - keep it, do not redo', SPI),
    (13, 6,  10, 8,  'MQ DIVIDERS  R3-R6  +  C2 1000uF', 'analogue: keep at the opposite end from the DHT/I2C lines', SIG),
    (2,  15, 21, 3,  'I2C BREAKOUT  -  BMP280 / DS3231 / OLED', 'shortest possible run; route SDA+SCL side by side with a GND between', I2C),
    (2,  19, 8,  2,  'R1 / R2  4k7 PULL-UPS', '1-Wire + DHT22', RAIL3),
    (12, 19, 11, 2,  'C1 100nF', 'decoupling, right at the ADC', MUTE),
    (1,  22, 23, 4,  'SCREW TERMINALS   14 ways', 'MAST 8  -  SOIL 4  -  POWER 2      label every way in indelible pen', ACC),
]

RULES = [
    ('Analogue apart from digital',
     'MCP3208 and the MQ dividers at one end; DHT22 and I2C at the other. A switching MQ heater beside an ADC input is a measurable error.'),
    ('One continuous ground',
     'Bond every ground pad into a single strip and tie it to at least TWO Pi GND pins. A thin shared return is a classic cause of fault F2.'),
    ('I2C as short as physically possible',
     'Plus 100 kHz instead of 400 kHz in config.txt. Do NOT add pull-ups - the Pi 3B+ already has 1k8 on GPIO2/GPIO3.'),
    ('Continuity-check before fitting any IC',
     'Do the header, ground strip and supply rails first, then buzz every net with the multimeter. A shorted rail on a soldered board is far less forgiving than on a breadboard.'),
    ('Label every terminal on the board itself',
     'The masking-tape flags on the cardboard build are the reason a rebuild was needed.'),
]


def perfboard():
    W, H = 1620, 1120
    o = header_block(W, 'Perfboard placement',
                     '65 x 70 mm matrix board, 25 x 27 holes at 2.54 mm.   '
                     'Zoned placement and separation rules - not a hole-exact route.')

    # ---- the hole grid, drawn to scale ----
    S = 21.0                                    # px per hole
    gx, gy = 70, 200
    bw, bh = (HOLES_X - 1) * S, (HOLES_Y - 1) * S
    o.append(rect(gx - S * 0.7, gy - S * 0.7, bw + S * 1.4, bh + S * 1.4,
                  BOARD, '#8a6a2a', 1.8, 4))
    for r in range(HOLES_Y):
        for c in range(HOLES_X):
            o.append(f'<circle cx="{gx + c * S:.1f}" cy="{gy + r * S:.1f}" '
                     f'r="2.1" fill="none" stroke="#a8926f" stroke-width="0.8"/>')
    # column / row rulers, so holes can be counted off the print
    for c in range(0, HOLES_X, 5):
        o.append(txt(gx + c * S, gy - S * 1.25, str(c + 1), 8, MUTE, 'middle'))
    for r in range(0, HOLES_Y, 5):
        o.append(txt(gx - S * 1.25, gy + r * S + 3, str(r + 1), 8, MUTE, 'end'))

    # ---- zones over the grid ----
    for c0, r0, cw, rh, label, sub, col in ZONES:
        x = gx + c0 * S - S * 0.45
        y = gy + r0 * S - S * 0.45
        w = (cw - 1) * S + S * 0.9
        h = (rh - 1) * S + S * 0.9
        o.append(rect(x, y, w, h, tint(col, 0.16), col, 2.0, 3))
        o.append(txt(x + 7, y + 14, label, 9.5, col, weight='700'))
        o.append(txt(x + 7, y + 26, sub, 7.8, MUTE))
        # leader out to the right-hand notes column
        o.append(line(x + w, y + h / 2, gx + bw + S * 1.4, y + h / 2, col, 1, '3 3'))

    o.append(txt(gx, gy + bh + S * 2.2,
                 f'{(HOLES_X-1)*PITCH_MM + PITCH_MM:.0f} mm  x  '
                 f'{(HOLES_Y-1)*PITCH_MM + PITCH_MM:.0f} mm   '
                 f'({HOLES_X} x {HOLES_Y} holes @ {PITCH_MM} mm)   '
                 '- the carrier-hat-v1 footprint, so this layout transfers to the real PCB',
                 9, MUTE))

    # ---- rules column ----
    rx = gx + bw + 120
    o.append(sans(rx, gy - 22, 'LAYOUT RULES', 12.5, INK, weight='700'))
    y = gy + 6
    for i, (t, why) in enumerate(RULES):
        o.append(txt(rx, y, f'{i+1}.  {t}', 10.5, ACC, weight='700'))
        # wrap the explanation
        words, ln = why.split(), ''
        yy = y + 17
        for wd in words:
            if len(ln) + len(wd) > 62:
                o.append(txt(rx + 16, yy, ln, 9, MUTE)); ln = wd; yy += 14
            else:
                ln = (ln + ' ' + wd).strip()
        o.append(txt(rx + 16, yy, ln, 9, MUTE))
        y = yy + 34

    o.append(sans(rx, y + 6, 'WHAT TO KEEP FROM THE EXISTING BOARD', 12.5, INK, weight='700'))
    keep = [
        ('KEEP', 'the soldered MCP3208 and its 3.3 V / GND / VREF lines', SIG),
        ('KEEP', 'any decoupling already fitted', SIG),
        ('CUT',  'every jumper-to-jumper chain between modules - this is fault F2', ACC),
        ('CUT',  'bare-wire twists and taped joints on any bus signal', ACC),
        ('ADD',  'screw terminals for everything that leaves the box', RAIL3),
        ('ADD',  'the passives on sheet 1 - R1-R6, C1, C2', RAIL3),
    ]
    for i, (verb, what, col) in enumerate(keep):
        yy = y + 30 + i * 19
        o.append(rect(rx, yy - 10, 38, 15, col, 'none', 0, 2))
        o.append(txt(rx + 19, yy + 1.5, verb, 8.5, '#fff', 'middle', '700'))
        o.append(txt(rx + 48, yy + 1.5, what, 9.5, INK))

    o.append(txt(70, H - 30,
                 'Generated by scripts/gen_drawings.py.   Placement is deliberate; hole-exact '
                 'routing is left to the physical board, whose MCP3208 is already soldered.',
                 9, MUTE))
    body = '\n'.join(o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
            f'{body}\n</svg>\n')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('schematic', schematic), ('perfboard', perfboard)):
        with open(os.path.join(OUT, f'{name}.svg'), 'w') as f:
            f.write(fn())
        print(f'wrote docs/drawings/{name}.svg')
