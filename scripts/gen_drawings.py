#!/usr/bin/env python3
"""Generate the IESH v0.2 2D build drawings as SVG.

Why scripted rather than hand-drawn: the net list below is the single source of
truth for both sheets, so the schematic and the perfboard placement cannot drift
apart, and a pin change is one edit. Output is plain SVG — scalable, printable
at 1:1, editable in Inkscape, and usable directly in poster artwork.

    python3 scripts/gen_drawings.py
    -> docs/drawings/schematic.svg
    -> docs/drawings/perfboard.svg
    -> docs/drawings/pinout.svg
    -> docs/drawings/lid-layout.svg      (positions read from docs/cad/roofbox.scad)

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
# Grouped by function, not by pin number, so each bus leaves the header as a
# block: power, then the two single-wire signals, then SPI, then I2C last -
# the I2C pair runs straight to its device box below the ADC without crossing
# anything.
HEADER = [
    (1,  '3V3',    '+3.3 V',      RAIL3, 'MCP3208 VDD+VREF · I2C trio · pull-ups · DHT22 · soil probes'),
    (2,  '5V',     '+5 V',        RAIL5, 'MQ-7 + MQ-135 heaters only  (own rail preferred - §8)'),
    (6,  'GND',    'GND',         GND,   'ground bus - tie at least TWO Pi GND pins'),
    (7,  'GPIO4',  '1-WIRE',      SIG,   'DS18B20 data  (+4k7 pull-up to 3V3)'),
    (16, 'GPIO23', 'DHT-DATA',    SIG,   'DHT22 data  (+4k7 pull-up to 3V3)'),
    (19, 'GPIO10', 'MOSI',        SPI,   'MCP3208 pin 11  Din'),
    (21, 'GPIO9',  'MISO',        SPI,   'MCP3208 pin 12  Dout'),
    (23, 'GPIO11', 'SCLK',        SPI,   'MCP3208 pin 13  CLK'),
    (24, 'GPIO8',  'CE0',         SPI,   'MCP3208 pin 10  CS/SHDN'),
    (3,  'GPIO2',  'SDA',         I2C,   'BMP280 0x76 · OLED 0x3C · DS3231 0x68'),
    (5,  'GPIO3',  'SCL',         I2C,   'same three devices'),
]

# The full 40-pin header, physical layout (odd pins left column, even right).
PI40 = [
    '3V3', '5V', 'GPIO2 SDA', '5V', 'GPIO3 SCL', 'GND', 'GPIO4', 'GPIO14 TXD',
    'GND', 'GPIO15 RXD', 'GPIO17', 'GPIO18', 'GPIO27', 'GND', 'GPIO22', 'GPIO23',
    '3V3', 'GPIO24', 'GPIO10 MOSI', 'GND', 'GPIO9 MISO', 'GPIO25', 'GPIO11 SCLK',
    'GPIO8 CE0', 'GND', 'GPIO7 CE1', 'ID_SD', 'ID_SC', 'GPIO5', 'GND', 'GPIO6',
    'GPIO12', 'GPIO13', 'GND', 'GPIO19', 'GPIO16', 'GPIO26', 'GPIO20', 'GND', 'GPIO21',
]
# Spare rail pins worth using: a second GND bond and the second 3V3/5V pins.
PI40_RAIL_SPARES = {4: '5V spare', 17: '3V3 spare', 9: 'GND spare', 14: 'GND spare', 20: 'GND spare', 25: 'GND spare'}

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

# CAT5e conductor colours. Convention on BOTH cables: the SOLID conductor of a
# pair carries supply or signal, the WHITE-STRIPED one carries that pair's
# return, so a twisted pair is always a current and its own return.
WIRE = {
    'or': ('#f28c28', False), 'or/wh': ('#f28c28', True),
    'gn': ('#2e9e4f', False), 'gn/wh': ('#2e9e4f', True),
    'bl': ('#2f6fd6', False), 'bl/wh': ('#2f6fd6', True),
    'br': ('#8b5a2b', False), 'br/wh': ('#8b5a2b', True),
    'red': ('#d32f2f', False), 'blk': ('#222222', False),
}

# Screw terminals: (label, [(way, net, colour, conductor, sensor-end)])
# The mast cable uses all 8 conductors. Rain gets the 8th; the LDR (also
# optional) needs a second cable - never double up a conductor.
TERMINALS = [
    ('MAST  CAT5e  8-way', [
        ('1', '+5 V',       RAIL5, 'or',    'MQ-7 VCC + MQ-135 VCC'),
        ('2', 'GND',        GND,   'or/wh', 'MQ-7 GND + MQ-135 GND'),
        ('3', '+3.3 V',     RAIL3, 'gn',    'DHT22 VCC + raindrop VCC'),
        ('4', 'GND',        GND,   'gn/wh', 'DHT22 GND + raindrop GND'),
        ('5', 'DHT-DATA',   SIG,   'bl',    'DHT22 DATA'),
        ('6', 'RAIN-AOUT',  SIG,   'bl/wh', 'raindrop AO   (optional - CH3)'),
        ('7', 'MQ7-AOUT',   SIG,   'br',    'MQ-7 AOUT'),
        ('8', 'MQ135-AOUT', SIG,   'br/wh', 'MQ-135 AOUT')]),
    ('SOIL  CAT5e  4 of 8', [
        ('1', '+3.3 V',     RAIL3, 'or',    'DS18B20 red + soil probe VCC'),
        ('2', 'GND',        GND,   'or/wh', 'DS18B20 black + soil probe GND'),
        ('3', '1-WIRE',     SIG,   'bl',    'DS18B20 yellow (DATA)'),
        ('4', 'SOIL-AOUT',  SIG,   'gn',    'soil probe AOUT')]),
    ('POWER  2-way', [
        ('1', '+5 V in',    RAIL5, 'red',   'from the buck / adapter, OUTSIDE the box'),
        ('2', 'GND',        GND,   'blk',   '')]),
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


def swatch(x, y, wire, w=26, h=10):
    """A CAT5e conductor: solid colour, or white with a colour stripe."""
    col, striped = WIRE[wire]
    if not striped:
        return rect(x, y, w, h, col, '#555', 0.6, 2)
    o = [rect(x, y, w, h, '#fff', '#555', 0.6, 2)]
    o.append(f'<line x1="{x+2:.1f}" y1="{y+h/2:.1f}" x2="{x+w-2:.1f}" y2="{y+h/2:.1f}" '
             f'stroke="{col}" stroke-width="3.2" stroke-dasharray="5 3"/>')
    return '\n'.join(o)


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
    A, B, C, D = 60, 430, 670, 1070
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

    # ── zone B: bus rails. They end just below the GND row: every stub and
    # signal drawn lower down then crosses nothing, instead of running through
    # three rails it is not connected to.
    RAIL_BOT = rowy['GND'] + 30
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
                     ('SCLK', 'CLK 13'), ('CE0', 'CS 10')):   # short labels: they
        # must end before the ADC's left-hand net labels begin
        y = rowy[net]
        o.append(line(A + 326, y, B + 128, y, SPI, 2))
        o.append(f'<path d="M {B+128:.0f} {y-4:.0f} l 9 4 l -9 4 z" fill="{SPI}"/>')
        o.append(txt(B + 146, y + 3.5, pin, 8.5, SPI, weight='700'))

    # I2C bus block: positioned so the SDA/SCL header rows land straight on
    # its left edge - no vertical drop through the stub labels.
    iy = rowy['SDA'] - 34
    assert iy > my + mh + 12, 'I2C block would overlap the ADC - move SDA/SCL lower in HEADER'
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
    for net in ('SDA', 'SCL'):
        y = rowy[net]
        o.append(line(A + 326, y, mx - 40, y, I2C, 2))
        o.append(dot(mx - 40, y, 3, I2C))

    # Single-ended signals cross the board untouched (bar their pull-up) and
    # land on a terminal. Drawn as short labelled stubs rather than lines run
    # across the whole sheet through the ADC - the terminal block already names
    # them, and a wire drawn over a chip reads as a connection to it.
    for net, dest in (('1-WIRE', 'SOIL 3'),
                      ('DHT-DATA', 'MAST 5')):
        y = rowy[net]
        o.append(line(A + 326, y, B + 128, y, SIG, 2))
        o.append(f'<path d="M {B+128:.0f} {y-4:.0f} l 9 4 l -9 4 z" fill="{SIG}"/>')
        o.append(txt(B + 146, y + 3.5, dest, 8.5, SIG, weight='700'))

    # ── zone D: terminals ───────────────────────────────────────────────────
    o.append(sans(D, TOP - 22, 'Screw terminals  ->  CAT5e', 15, INK, weight='700'))
    o.append(txt(D, TOP - 6, 'two cables leave the box, not six', 9, MUTE))
    y = TOP + 6
    for i, (label, ways) in enumerate(TERMINALS):
        bh2 = 34 + len(ways) * 22
        o.append(rect(D, y, 480, bh2, '#fff', INK, 1.5, 3))
        o.append(txt(D + 14, y + 22, label, 11, INK, weight='700'))
        if i == 0:
            o.append(txt(D + 150, y + 22, 'CAT5e', 8, MUTE, 'middle', '700'))
            o.append(txt(D + 232, y + 22, 'at the sensor end  (solder + heatshrink)', 8, MUTE, weight='700'))
        for k, (w, net, col, wire, dest) in enumerate(ways):
            yy = y + 40 + k * 22
            o.append(rect(D + 14, yy - 9, 19, 17, col, 'none', 0, 2))
            o.append(txt(D + 23.5, yy + 3.5, w, 9.5, '#fff', 'middle', '700'))
            o.append(txt(D + 42, yy + 3.5, net, 10, col, weight='700'))
            o.append(swatch(D + 137, yy - 5, wire))
            o.append(txt(D + 168, yy + 3.5, wire, 8.5, INK, weight='600'))
            o.append(line(D + 208, yy, D + 226, yy, col, 1.8))
            o.append(txt(D + 232, yy + 3.5, dest, 8.5, MUTE))
        y += bh2 + 16
    o.append(txt(D, y + 2, 'solid conductor = supply/signal · striped = that pair\'s return. '
                 'Rain takes the 8th core; an LDR needs a second cable.', 8.5, MUTE))

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
# HONEST SCOPE: a ZONED PLACEMENT drawing for the BLANK 100 x 150 mm board, not
# a hole-exact route. What is fixed and knowable is what matters: which block
# sits where, which edge the terminals are on, the separation rules and the
# order of work. Count holes off the printed grid; adjust by a hole or two to
# suit your own board without asking.
#
# Board: PY-10CM*15CM phenolic matrix board, nominally 57 x 37 holes at 2.54 mm.
# COUNT YOUR OWN before committing - vendors vary by a hole or two at the edges.
#
# The old demo board is NOT reworked: bill 884 bought a second MCP3208, so that
# board is set aside intact and everything below is built fresh.
HOLES_X, HOLES_Y = 57, 37          # 145 x 94 mm of grid on a 100 x 150 board
PITCH_MM = 2.54

ZONES = [
    # (col0, row0, cols, rows, label, sub, colour)
    (2,  0,  20, 2,
     '2 x  1x20 FEMALE HEADER STRIPS   ->  Pi GPIO',
     'BODIES ON THE UNDERSIDE, tails soldered on top - it seats DOWN onto the Pi.   '
     'upper row = Pi ODD pins 1-39,  lower row = Pi EVEN pins 2-40.   MARK PIN 1.',
     '#37474f'),

    (1,  4,  55, 1,
     'GND RAIL          flood one continuous strip  -  tie to at least TWO Pi GND pins '
     '(6, 9, 14, 20, 25, 30, 34, 39)', '', GND),
    (1,  6,  55, 1,
     '+3.3 V RAIL       from Pi pins 1 and 17  -  MCP3208 VDD+VREF, I2C trio, pull-ups, '
     'DHT22, soil, raindrop', '', RAIL3),
    (1,  8,  55, 1,
     '+5 V RAIL         from the POWER terminal via the LM2596 @ 5.00 V  -  MQ HEATERS ONLY.  '
     'do NOT wire this rail to Pi pins 2/4', '', RAIL5),

    # ---- analogue end (left) ----
    (3,  11, 10, 9,
     'MCP3208   DIP-16',
     'pin 1 top-left.   16->3V3 VDD   15->3V3 VREF   14+9->GND   '
     '13->pin23 CLK   12->pin21 Dout   11->pin19 Din   10->pin24 CS',
     SPI),
    (15, 11, 6,  2,
     'C1  100 nF', 'across the ADC supply pins, as close as it will go', MUTE),
    (3,  22, 17, 4,
     'MQ DIVIDERS   R3 R4  (MQ-7 -> CH0)    R5 R6  (MQ-135 -> CH1)',
     'AOUT -> node -> GND, node -> CHx.   USE MATCHED PAIRS and put the measured '
     '(R1+R2)/R2 into sensors/config.py:26', SIG),
    (22, 22, 7,  3,
     'C2  1000 uF', 'on the 5 V rail beside the MQ feed.   WATCH POLARITY', MUTE),

    # ---- digital end (right) ----
    (32, 11, 21, 4,
     'I2C BREAKOUT   BMP280 0x76  ·  OLED 0x3C  ·  DS3231 0x68',
     'shortest run on the board.   route SDA and SCL side by side with a GND between them.   '
     'do NOT add pull-ups - the Pi 3B+ already has 1k8', I2C),
    (32, 17, 9,  2,
     'R1  4k7', '1-WIRE pull-up:  GPIO4 (pin 7) -> 3V3', RAIL3),
    (43, 17, 10, 2,
     'R2  4k7', 'DHT22 pull-up: GPIO23 (pin 16) -> 3V3.  CHECK the module first - U6', RAIL3),
    (32, 22, 21, 3,
     'FREE ADC CHANNELS   CH3  CH4  CH5  CH6  CH7',
     'raindrop x2 and LDR x4 are owned and unfitted - leave room, fit after gate 6', MUTE),

    # ---- terminals along the bottom edge ----
    (1,  29, 55, 5,
     'SCREW TERMINALS   14 ways   -   MAST 8   |   SOIL 4   |   POWER 2',
     'cables leave the board at this edge, nearest the glands.   '
     'LABEL EVERY WAY ON THE BOARD IN INDELIBLE PEN', ACC),
]

RULES = [
    ('Analogue apart from digital',
     'MCP3208 and the MQ dividers on the left; I2C and the DHT22 pull-up on the right. A switching MQ heater beside an ADC input is a measurable error, not a theoretical one.'),
    ('One continuous ground',
     'Flood the GND row into a single strip and tie it to at least TWO Pi GND pins. A thin shared return is a classic cause of fault F2.'),
    ('I2C as short as physically possible',
     'Plus 100 kHz instead of 400 kHz in config.txt. Do NOT add pull-ups - the Pi 3B+ already has 1k8 on GPIO2/GPIO3.'),
    ('Rails before components, and buzz them',
     'Header, ground strip and supply rails first. Then meter GND/3V3/5V against each other - ALL THREE MUST READ OPEN - before the board ever meets the Pi.'),
    ('Label every terminal on the board itself',
     'The masking-tape flags on the demo build are the reason a rebuild was needed at all.'),
    ('Iron under three seconds per pad',
     'Cheap phenolic board lifts pads if you dwell. ~350 C, in and out.'),
]


def perfboard():
    W, H = 1860, 1040
    o = header_block(W, 'Perfboard placement',
                     'BLANK PY-10CM*15CM board, 57 x 37 holes at 2.54 mm.   '
                     'Zoned placement, separation rules and order of work - not a hole-exact route.')

    # ---- the hole grid, drawn to scale ----
    S = 19.0                                    # px per hole
    gx, gy = 70, 205
    bw, bh = (HOLES_X - 1) * S, (HOLES_Y - 1) * S
    o.append(rect(gx - S * 0.7, gy - S * 0.7, bw + S * 1.4, bh + S * 1.4,
                  BOARD, '#8a6a2a', 1.8, 4))
    for r in range(HOLES_Y):
        for c in range(HOLES_X):
            o.append(f'<circle cx="{gx + c * S:.1f}" cy="{gy + r * S:.1f}" '
                     f'r="1.9" fill="none" stroke="#a8926f" stroke-width="0.7"/>')
    for c in range(0, HOLES_X, 5):
        o.append(txt(gx + c * S, gy - S * 1.25, str(c + 1), 8, MUTE, 'middle'))
    for r in range(0, HOLES_Y, 5):
        o.append(txt(gx - S * 1.25, gy + r * S + 3, str(r + 1), 8, MUTE, 'end'))

    # ---- the analogue | digital divide ----
    dx = gx + 30.5 * S
    o.append(line(dx, gy + 10 * S, dx, gy + 27 * S, ACC, 1.4, '6 4'))
    o.append(txt(dx - 8, gy + 9.4 * S, 'ANALOGUE', 8.5, ACC, 'end', '700'))
    o.append(txt(dx + 8, gy + 9.4 * S, 'DIGITAL', 8.5, ACC, 'start', '700'))

    # ---- zones over the grid ----
    for c0, r0, cw, rh, label, sub, col in ZONES:
        x = gx + c0 * S - S * 0.45
        y = gy + r0 * S - S * 0.45
        w = (cw - 1) * S + S * 0.9
        h = (rh - 1) * S + S * 0.9
        o.append(rect(x, y, w, h, tint(col, 0.16), col, 2.0, 3))
        o.append(txt(x + 7, y + 13, label, 9.5, col, weight='700'))
        if sub:
            # wrap the sub-label to the zone width, then place it INSIDE the zone
            # if it fits and immediately BELOW it if it does not - a short zone
            # must still show its true hole count, so the text moves, not the box.
            cap = max(28, int(w / 4.55))
            lines, ln = [], ''
            for wd in sub.split():
                if len(ln) + len(wd) + 1 > cap:
                    lines.append(ln); ln = wd
                else:
                    ln = (ln + ' ' + wd).strip()
            lines.append(ln)
            needed = 25 + 11 * (len(lines) - 1) + 3
            inside = needed <= h
            yy = y + 25 if inside else y + h + 11
            if not inside:
                # a backing panel, or the text fights the hole grid underneath
                tw = max(len(l) for l in lines) * 4.25 + 14
                o.append(f'<rect x="{x+2:.1f}" y="{yy-9:.1f}" width="{tw:.1f}" '
                         f'height="{11*len(lines)+4:.1f}" fill="{PAPER}" '
                         f'fill-opacity="0.93" stroke="{tint(col,0.45)}" '
                         f'stroke-width="0.7" rx="2"/>')
            for l in lines:
                o.append(txt(x + 7, yy, l, 7.6, MUTE)); yy += 11

    o.append(txt(gx, gy + bh + S * 2.0,
                 f'grid {(HOLES_X-1)*PITCH_MM:.0f} x {(HOLES_Y-1)*PITCH_MM:.0f} mm  '
                 f'({HOLES_X} x {HOLES_Y} holes @ {PITCH_MM} mm) on a 150 x 100 mm board.   '
                 'COUNT YOUR OWN BOARD - vendors vary by a hole or two at the edges.',
                 9, MUTE))
    o.append(txt(gx, gy + bh + S * 2.0 + 15,
                 'The 65 x 70 carrier-hat-v1 footprint is deliberately NOT matched: the corrected '
                 'box takes the full board flat, and a HAT may overhang the Pi. Zones transfer to '
                 'the real PCB; the outline does not.',
                 9, MUTE))

    # ---- rules column ----
    rx = gx + bw + 95
    o.append(sans(rx, gy - 22, 'LAYOUT RULES', 12.5, INK, weight='700'))
    y = gy + 6
    for i, (t, why) in enumerate(RULES):
        o.append(txt(rx, y, f'{i+1}.  {t}', 10.5, ACC, weight='700'))
        words, ln = why.split(), ''
        yy = y + 16
        for wd in words:
            if len(ln) + len(wd) > 56:
                o.append(txt(rx + 16, yy, ln, 8.8, MUTE)); ln = wd; yy += 13
            else:
                ln = (ln + ' ' + wd).strip()
        o.append(txt(rx + 16, yy, ln, 8.8, MUTE))
        y = yy + 30

    o.append(sans(rx, y + 8, 'ORDER OF WORK', 12.5, INK, weight='700'))
    steps = [
        ('1',    'both header strips, all 40 tails soldered. Mark pin 1', '#37474f'),
        ('2',    'GND rail, flooded, to >= 2 Pi GND pins', GND),
        ('3',    '+3.3 V rail from Pi pins 1 and 17', RAIL3),
        ('4',    '+5 V rail - NOT connected to Pi pins 2/4', RAIL5),
        ('GATE', 'GND / 3V3 / 5V all OPEN to each other, board OFF the Pi', ACC),
        ('5',    'MCP3208 + C1', SPI),
        ('6',    'R1 R2 pull-ups, R3-R6 dividers, C2', SIG),
        ('7',    'screw terminals, every way labelled in pen', ACC),
        ('8',    'onto the Pi. tests/test_all.py, one sensor at a time', SIG),
    ]
    for i, (verb, what, col) in enumerate(steps):
        yy = y + 32 + i * 19
        o.append(rect(rx, yy - 10, 40, 15, col, 'none', 0, 2))
        o.append(txt(rx + 20, yy + 1.5, verb, 8.5, '#fff', 'middle', '700'))
        o.append(txt(rx + 50, yy + 1.5, what, 9.2, INK))

    o.append(txt(70, H - 28,
                 'Generated by scripts/gen_drawings.py - edit ZONES there, not this SVG.   '
                 'Placement is deliberate; hole-exact routing is yours to finish on the board.',
                 9, MUTE))
    body = '\n'.join(o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
            f'{body}\n</svg>\n')


# ════════════════════════════════════════════════════════════════════════════
#  SHEET 3 — Pi header pinout and the two cables end to end
# ════════════════════════════════════════════════════════════════════════════
# The thing to have beside you while soldering: the 40-pin header as it sits on
# the Pi (pin 1 top-left, odd pins in the left column), used pins in their net
# colour, and each CAT5e conductor traced from its screw-terminal way to the
# sensor pin it is soldered to at the far end.
def pinout():
    W, H = 1620, 1120
    o = header_block(W, 'Header pinout and cable map',
                     'Pi 3B+ 40-pin header, looking down on the board with pin 1 at the '
                     'SD-card end.   Every used pin in its net colour; every CAT5e core '
                     'traced terminal -> sensor.')
    used = {pin: (net, col) for pin, _g, net, col, _d in HEADER}

    # ---- the header ----
    hx, hy, P = 170, 212, 42          # column x, first-row y, row pitch
    o.append(rect(hx - 96, hy - 58, 340, 20 * P + 52, '#eef3ee', '#2f6b46', 1.6, 6))
    o.append(sans(hx - 84, hy - 38, 'Pi 3B+ header', 11.5, '#2f6b46', weight='700'))
    o.append(txt(hx - 84, hy - 24, 'board edge to the RIGHT (even pins), SD-card end at the top', 8, MUTE))
    for row in range(20):
        for colm in range(2):
            pin = row * 2 + colm + 1
            x = hx + colm * 80
            y = hy + row * P
            name = PI40[pin - 1]
            if pin in used:
                net, col = used[pin]
                o.append(f'<rect x="{x-14:.1f}" y="{y-14:.1f}" width="28" height="28" rx="4" fill="{col}"/>')
                o.append(txt(x, y + 4, str(pin), 10, '#fff', 'middle', '700'))
                lab, lcol, wt = net, col, '700'
            elif pin in PI40_RAIL_SPARES:
                net = PI40_RAIL_SPARES[pin]
                col = {'5V': RAIL5, '3V3': RAIL3, 'GND': GND}[net.split()[0]]
                o.append(f'<rect x="{x-14:.1f}" y="{y-14:.1f}" width="28" height="28" rx="4" '
                         f'fill="{tint(col, 0.25)}" stroke="{col}" stroke-width="1.4" stroke-dasharray="3 2"/>')
                o.append(txt(x, y + 4, str(pin), 10, col, 'middle', '700'))
                lab, lcol, wt = net, col, '600'
            else:
                o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#fff" stroke="#b9bec6" stroke-width="1.2"/>')
                o.append(txt(x, y + 4, str(pin), 9.5, '#8a9099', 'middle'))
                lab, lcol, wt = name, '#8a9099', '400'
            # label: left column reads outward to the left, right column to the right
            if colm == 0:
                o.append(txt(x - 20, y + 3.5, lab, 8.5, lcol, 'end', wt))
            else:
                o.append(txt(x + 20, y + 3.5, lab, 8.5, lcol, 'start', wt))
    o.append(txt(hx - 84, hy + 20 * P + 6,
                 'square = wired on the HAT · dashed = spare rail pin worth bonding', 8.5, MUTE))
    o.append(txt(hx - 84, hy + 20 * P + 20,
                 'Pi 3B+ has 1k8 pull-ups on pins 3/5 already - add none.', 8.5, ACC, weight='700'))

    # ---- cables end to end ----
    cx = 560
    o.append(sans(cx, hy - 16, 'Cables, terminal -> sensor', 15, INK, weight='700'))
    o.append(txt(cx, hy, 'Two joints per conductor and nothing between: screw terminal in the box, '
                 'solder + heatshrink at the sensor. Cable is cheaper than a roof trip.', 8.5, MUTE))
    cols = [(cx, 'WAY'), (cx + 60, 'NET'), (cx + 175, 'CORE'), (cx + 300, 'SOLDER TO AT THE FAR END')]
    y = hy + 30
    for x, h in cols:
        o.append(txt(x, y - 14, h, 7.5, MUTE, weight='700', ls='1'))
    for label, ways in TERMINALS:
        o.append(rect(cx - 12, y - 6, 1000, 30 + len(ways) * 24, '#fff', INK, 1.3, 3))
        o.append(txt(cx, y + 12, label, 10.5, INK, weight='700'))
        for k, (w, net, col, wire, dest) in enumerate(ways):
            yy = y + 36 + k * 24
            o.append(rect(cx, yy - 9, 19, 17, col, 'none', 0, 2))
            o.append(txt(cx + 9.5, yy + 3.5, w, 9.5, '#fff', 'middle', '700'))
            o.append(txt(cx + 60, yy + 3.5, net, 10, col, weight='700'))
            o.append(swatch(cx + 175, yy - 5, wire))
            o.append(txt(cx + 206, yy + 3.5, wire, 8.5, INK, weight='600'))
            o.append(line(cx + 250, yy, cx + 290, yy, col, 1.8))
            o.append(txt(cx + 300, yy + 3.5, dest, 9.5, INK))
        y += 30 + len(ways) * 24 + 18

    # what each sensor's pins are, so the far end can be soldered without a datasheet
    o.append(sans(cx, y + 10, 'Sensor pins at the far end', 12.5, INK, weight='700'))
    pins = [
        ('DHT22 (3-pin breakout)', 'VCC -> gn   DATA -> bl   GND -> gn/wh.   3.3 V supply on purpose: keeps DATA at 3.3 V logic and off the heater rail.'),
        ('MQ-7 / MQ-135 modules',  'VCC -> or   GND -> or/wh   AOUT -> br (MQ-7) / br/wh (MQ-135).   DOUT unused.   Heaters ~150 mA each - hence their own pair.'),
        ('Raindrop board',         'VCC -> gn   GND -> gn/wh   AO -> bl/wh.   At 3.3 V its AO is already 0-3.3 V: straight into CH3, no divider.'),
        ('DS18B20 waterproof',     'red -> or   black -> or/wh   yellow -> bl.   R1 4k7 DATA->3V3 lives on the HAT, not at the probe.'),
        ('Capacitive soil v1.2',   'VCC -> or   GND -> or/wh   AOUT -> gn.   Pot the top 25 mm. Calibrated at 3.3 V (SOIL_DRY 4021) - keep it on 3.3 V.'),
    ]
    for i, (nm, what) in enumerate(pins):
        yy = y + 34 + i * 22
        o.append(txt(cx, yy, nm, 9.5, INK, weight='700'))
        o.append(txt(cx + 190, yy, what, 8.5, MUTE))

    o.append(txt(hx - 84, H - 30,
                 'Generated by scripts/gen_drawings.py from the same net list as sheets 1 and 2.',
                 9, MUTE))
    body = '\n'.join(o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
            f'{body}\n</svg>\n')


# ════════════════════════════════════════════════════════════════════════════
#  SHEET 4 — lid layout, dimensioned, from the CAD constants
# ════════════════════════════════════════════════════════════════════════════
# Reads the numbers straight out of docs/cad/roofbox.scad (same parser as
# roofbox_check.py) so this sheet cannot disagree with the CAD. It is the
# sheet to have on the bench when bonding standoffs to the lid: every position
# as a distance from the lid centre, in mm.
import math
import re

SCAD = os.path.join(os.path.dirname(OUT), 'cad', 'roofbox.scad')


def scad_constants():
    src = re.sub(r'//[^\n]*', '', open(SCAD).read())
    ns = {'sqrt': math.sqrt}
    for m in re.finditer(r'(?<![\w.])([A-Z][A-Z0-9_]*)\s*=\s*([^;{}]+?);', src):
        try:
            ns[m.group(1)] = eval(m.group(2).strip(), {'__builtins__': {}}, ns)
        except Exception:
            pass
    return ns


def lid_layout():
    V = scad_constants()
    W, H = 1620, 1120
    o = header_block(W, 'Lid layout',
                     'The container lid as chassis plate, seen from INSIDE the box (the side the parts bond to).   '
                     'Positions in mm from the lid centre. Nothing is drilled today: standoffs are bonded, '
                     'the tower bore waits for the camera.')
    K = 4.7                                  # px per mm
    cx, cy = 470, 600                        # lid centre on the sheet
    lid = V['LID_W']

    def X(x): return cx + x * K
    def Y(y): return cy - y * K             # +y up on the sheet

    def box(x0, y0, w, h, col, label, sub='', fill=None, dash=None):
        o.append(rect(X(x0), Y(y0 + h), w * K, h * K, fill or tint(col, 0.18), col, 1.8, 3,
                      f'stroke-dasharray="{dash}"' if dash else ''))
        o.append(txt(X(x0) + 6, Y(y0 + h) + 14, label, 9.5, col, weight='700'))
        if sub:
            o.append(txt(X(x0) + 6, Y(y0 + h) + 26, sub, 8, MUTE))

    # lid, wall line, gasket band
    o.append(rect(X(-lid / 2), Y(lid / 2), lid * K, lid * K, '#dfe6ef', INK, 1.6, 14 * K))
    bt = V['BOX_TOP']
    o.append(rect(X(-bt / 2), Y(bt / 2), bt * K, bt * K, 'none', MUTE, 1, 14 * K, 'stroke-dasharray="4 3"'))
    inner = bt - 2 * V['BOX_WALL'] - 6
    o.append(rect(X(-inner / 2), Y(inner / 2), inner * K, inner * K, 'none', ACC, 1.2, 12 * K, 'stroke-dasharray="4 3"'))
    o.append(txt(X(0), Y(inner / 2) - 6, 'GASKET BAND - nothing through the lid outside this line', 8, ACC, 'middle', '700'))
    o.append(txt(X(0), Y(lid / 2) - 8, f'lid {lid:.0f} x {lid:.0f} mm (assumed, U1)', 8.5, MUTE, 'middle'))

    # parts
    px, py = V['PI_ORG']
    box(px, py, V['PI_W'], V['PI_D'], '#2f6b46', '', '')
    o.append(txt(X(px) + 6, Y(py) - 22, 'Raspberry Pi 3B+  85 x 56', 9.5, '#2f6b46', weight='700'))
    o.append(txt(X(px) + 6, Y(py) - 10, f'corner at ({px:+.0f}, {py:+.0f})  -  M2.5 standoffs on a 58 x 49 grid, BONDED', 8, MUTE))
    for hx, hy in V['PI_MH']:
        o.append(dot(X(px + hx), Y(py + hy), 3.2, '#2f6b46'))
        o.append(txt(X(px + hx) + 6, Y(py + hy) + 12, f'({px + hx:+.1f}, {py + hy:+.1f})', 7, '#2f6b46'))
    bx, by = V['BUCK_ORG']
    box(bx, by, V['BUCK_W'], V['BUCK_D'], '#0b6e4f', 'buck 12V->5V',
        f'({bx:+.0f}, {by:+.0f})  {V["BUCK_W"]:.0f} x {V["BUCK_D"]:.0f} - U8, measure')
    cxx, cyy = V['CAM_ORG']
    tw, td = V['TOWER_OX'] + 0.6, V['TOWER_OY'] + 0.6
    box(cxx - tw / 2, cyy - td / 2, tw, td, '#b03a2e', 'TOWER BORE',
        f'centre ({cxx:+.0f}, {cyy:+.0f})  {tw:.1f} x {td:.1f} - witness only', fill='#fff', dash='5 3')
    sx, sy = V['CSI_XY']
    o.append(dot(X(sx), Y(sy), 3.5, '#e0b000'))
    o.append(txt(X(sx) + 7, Y(sy) + 3, 'CSI (ribbon leaves the Pi here)', 7.5, '#8a6d00', weight='700'))
    tm = V['TIE_MOUNT']
    for y in V['CLAMP_YS']:
        box(V['CLAMP_X'] - tm / 2, y - tm / 2, tm, tm, '#546e7a', 'tie', f'({V["CLAMP_X"]:+.0f}, {y:+.0f})')

    # centre lines + scale
    o.append(line(X(-lid / 2 - 6), Y(0), X(lid / 2 + 6), Y(0), MUTE, 0.8, '6 4'))
    o.append(line(X(0), Y(-lid / 2 - 6), X(0), Y(lid / 2 + 6), MUTE, 0.8, '6 4'))
    for v in range(-70, 71, 10):
        o.append(line(X(v), Y(-lid / 2 - 8), X(v), Y(-lid / 2 - 14), MUTE, 0.8))
        o.append(txt(X(v), Y(-lid / 2 - 20), f'{v:+d}', 7, MUTE, 'middle'))
        o.append(line(X(-lid / 2 - 8), Y(v), X(-lid / 2 - 14), Y(v), MUTE, 0.8))
        o.append(txt(X(-lid / 2 - 18), Y(v) + 2.5, f'{v:+d}', 7, MUTE, 'end'))
    o.append(txt(X(0), Y(-lid / 2 - 34), 'mm from the lid centre  ·  +x to the right, +y up  ·  '
                 'the Pi USB stack faces +x, its CSI edge faces -y', 8.5, MUTE, 'middle'))

    # right-hand notes
    nx = 1010
    o.append(sans(nx, 190, 'What this settles', 15, INK, weight='700'))
    notes = [
        ('No holes today.',
         'Standoffs (Pi, buck) bond to the lid underside with epoxy or neutral-cure silicone. '
         'Cable ties go on adhesive mounts. The gasket band stays untouched.'),
        ('One hole, later.',
         f'The camera tower bore, {tw:.1f} x {td:.1f} mm, cut only when the camera is verified '
         'and the printed tower has been test-fitted to the real fisheye (U2/U3).'),
        ('Ribbon.',
         f'CSI connector at ({sx:+.0f}, {sy:+.0f}); tower centre at ({cxx:+.0f}, {cyy:+.0f}). '
         f'roofbox_check.py puts the FFC path at ~90 mm of the 110 mm on hand.'),
        ('Field.',
         f'Everything sits inside +/-{V["USABLE"]/2:.0f} mm - clear of the seal channel - '
         'and no two footprints overlap. Checked numerically, not by eye.'),
        ('Stack.',
         f'Lid -> Pi standoff {V["STANDOFF_LID"]:.0f} -> Pi -> {V["SOCKET_GAP"]:.1f} socket -> HAT: '
         f'{V["Z_HAT"] + V["HAT_T"] + 16:.1f} mm to the tallest part, in {V["BOX_H"] - V["BOX_WALL"]:.0f} mm of box.'),
        ('Glands.',
         f'Not on the lid. Three PG7 ({V["GLAND_HOLE"]} mm holes) in one side wall, '
         f'{V["GLAND_Z"]:.0f} mm up, {V["GLAND_PITCH"]:.0f} mm apart - templates/roofbox_drill_wall.svg.'),
    ]
    y = 222
    for head, body in notes:
        o.append(txt(nx, y, head, 10.5, INK, weight='700'))
        words, ln, yy = body.split(), '', y + 16
        for wd in words:
            if len(ln) + len(wd) > 66:
                o.append(txt(nx, yy, ln, 9, MUTE)); ln = wd; yy += 14
            else:
                ln = (ln + ' ' + wd).strip()
        o.append(txt(nx, yy, ln, 9, MUTE))
        y = yy + 30

    o.append(txt(nx, H - 30, 'Generated by scripts/gen_drawings.py from docs/cad/roofbox.scad - '
                 'change the CAD, not this sheet.', 9, MUTE))
    body = '\n'.join(o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
            f'{body}\n</svg>\n')


# ════════════════════════════════════════════════════════════════════════════
#  bench.html — the four sheets, the key renders and the gates on one page
# ════════════════════════════════════════════════════════════════════════════
import base64

GATES = [
    ('1', 'Power', '`vcgencmd get_throttled` reads `0x0` and stays there for an hour with both MQ heaters on. Meter pins 2/6: below 4.75 V is the fault.'),
    ('2', 'Config + clock', '`sudo scripts/pi_config.sh` · fit the CR2032 · reboot · `sudo hwclock -w` · `/dev/rtc0` exists · `hwclock -r` is right.'),
    ('3', 'Protoboard', 'Header, ground strip and rails first; continuity-check every net before any IC goes on. Then R1-R6, C1, C2, terminals, labels.'),
    ('4', 'Services', '`sudo systemctl restart hics-core hics-web`; the log shows `Logged to DB ... | NULL: ...` naming exactly the disconnected channels. `gate_check.py` G6.'),
    ('5', 'One sensor at a time', 'I2C trio -> ADC + soil -> DS18B20 -> DHT22 -> MQ pair, `tests/test_all.py --skip camera` after each.'),
    ('6', '24 h on the bench', '~1440 rows for a day, throttled still `0x0`. Closes F5 - the station has never done this.'),
    ('7', 'Lid, glands, seal', 'Bond standoffs (sheet 4); three PG7 holes + vent in one side wall (wall template); silicone cures 24 h. The lid is not drilled.'),
    ('8', 'Mast and pod', 'Shield, pod, rain plate on the PVC; solder + heatshrink at every sensor; drip loops.'),
    ('9', 'Roof', 'Box on the tile under the hood table, mast clamped, probes in the biggest vase. 48 h clean data before going public.'),
]


def _svg_inline(name):
    with open(os.path.join(OUT, f'{name}.svg')) as f:
        return f.read().split('?>', 1)[-1]


def _img(path):
    full = os.path.join(os.path.dirname(OUT), 'cad', 'renders', path)
    if not os.path.exists(full):
        return ''
    with open(full, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()


def bench_html():
    css = """
    :root{--ink:#1a1d21;--mute:#6b7280;--ground:#f3f1ec;--paper:#fbfaf8;--card:#ffffff;--acc:#b03a2e;--sig:#2e8b6f;--line:#d9d4cc;--code:#ece7dd}
    @media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#e6e2da;--mute:#9aa0a8;--ground:#14171b;--paper:#1b1f24;--card:#1f2429;--acc:#d9664f;--sig:#4fb08f;--line:#343a42;--code:#2a3037}}
    :root[data-theme="dark"]{--ink:#e6e2da;--mute:#9aa0a8;--ground:#14171b;--paper:#1b1f24;--card:#1f2429;--acc:#d9664f;--sig:#4fb08f;--line:#343a42;--code:#2a3037}
    body{margin:0;background:var(--ground);color:var(--ink);font:15px/1.55 "IBM Plex Sans",system-ui,sans-serif}
    header{padding:30px 24px 14px;border-bottom:2px solid var(--ink);background:var(--paper)}
    header .eyebrow{font:600 11px/1 "IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin-bottom:8px}
    header h1{margin:0;font-size:28px;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
    header p{margin:6px 0 0;color:var(--mute);max-width:65ch}
    nav{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--line);padding:8px 24px;display:flex;gap:18px;flex-wrap:wrap;font:600 12.5px/1.6 "IBM Plex Mono",monospace;z-index:2}
    nav a{color:var(--ink);text-decoration:none}nav a:hover,nav a:focus-visible{color:var(--acc);outline:none;text-decoration:underline}
    section{padding:22px 24px 26px;border-bottom:1px solid var(--line)}
    h2{font-size:18px;font-weight:600;margin:0 0 12px;text-wrap:balance}
    .sheet{overflow-x:auto;background:#fbfaf8;border:1px solid var(--line);border-radius:4px}
    .sheet svg{display:block;min-width:900px;width:100%;height:auto}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
    figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:8px}
    figure img{width:100%;height:auto;display:block;border-radius:2px;background:#f7f7f7}
    figcaption{font-size:12.5px;color:var(--mute);margin-top:6px}figcaption b{color:var(--ink)}
    ol.gates{list-style:none;padding:0;margin:0}
    ol.gates li{display:grid;grid-template-columns:34px 160px 1fr;gap:12px;padding:11px 0;border-bottom:1px dashed var(--line);align-items:start}
    ol.gates li span.n{font:600 13px/1 "IBM Plex Mono",monospace;background:var(--ink);color:var(--ground);border-radius:3px;text-align:center;padding:6px 0;font-variant-numeric:tabular-nums}
    ol.gates li b{font-size:14px;font-weight:600}
    code{font-family:"IBM Plex Mono",monospace;background:var(--code);padding:1px 5px;border-radius:3px;font-size:12.5px}
    .warn{border-left:4px solid var(--acc);padding:10px 14px;background:var(--card);margin:0 0 14px;max-width:72ch}
    footer{padding:18px 24px;color:var(--mute);font-size:12.5px;max-width:80ch}
    @media (max-width:640px){ol.gates li{grid-template-columns:30px 1fr}ol.gates li div{grid-column:2}}
    @media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
    """
    def md(t):  # backticks -> code
        return re.sub(r'`([^`]+)`', r'<code>\1</code>', esc(t))
    gates = ''.join(f'<li><span class="n">{n}</span><b>{esc(t)}</b><div>{md(d)}</div></li>' for n, t, d in GATES)
    renders = [
        ('site', 'Whole station on the roof', 'tile, box under the hood table, mast with shield / rain plate / gas pod, vase, junction box, the three cable runs'),
        ('service', 'The box as it stands', 'hood table on four PVC legs, tower proud of the hood, nothing bolted to the lid'),
        ('section2d', 'Exact section through the tower', '2D cut on the tower centre plane: lip, ring, board, ribbon, Pi + HAT under the lid, hood gap'),
        ('exploded', 'Hood plate / lid stack / body', 'what bonds to the lid: Pi on standoffs, HAT on the header, buck, tower, tie mounts'),
        ('plan', 'Lid from the inside', 'the footprints that roofbox_check.py keeps apart'),
        ('mast', 'Mast', 'shield at 1.4 m, rain plate, gas pod open downward'),
        ('tower2d', 'Tower section', 'the one printed part - print after measuring U2/U3'),
        ('drill_wall', 'Side-wall template', 'three 12.5 mm PG7 holes 32 mm up, vent high; print at 100 %'),
    ]
    figs = ''.join(
        f'<figure><img src="{_img(n + ".png")}" alt="{esc(t)}"><figcaption><b>{esc(t)}</b> - {esc(d)}</figcaption></figure>'
        for n, t, d in renders if _img(n + '.png'))
    sheets = ''.join(
        f'<section id="{n}"><h2>Sheet {i} - {esc(t)}</h2><div class="sheet">{_svg_inline(n)}</div></section>'
        for i, (n, t) in enumerate([('schematic', 'Wiring schematic'), ('perfboard', 'Perfboard placement'),
                                    ('pinout', 'Header pinout and cable map'), ('lid-layout', 'Lid layout')], 1))
    return f"""<title>IESH Bench Sheet</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap">
<style>{css}</style>
<header><div class="eyebrow">HICS · IESH v0.2 · Lalitpur rooftop</div><h1>Bench sheet</h1><p>The four drawing sheets, the CAD views and the commissioning gates, generated from one net list and one CAD file. HANDOFF.md is the narrative; this is what sits next to the soldering iron.</p></header>
<nav><a href="#gates">Gates</a><a href="#schematic">1 Schematic</a><a href="#perfboard">2 Perfboard</a><a href="#pinout">3 Pinout + cables</a><a href="#lid-layout">4 Lid</a><a href="#views">Views</a></nav>
<section id="gates"><h2>Build order - each step gated (HANDOFF section 14)</h2>
<div class="warn"><b>Nothing below step 1 is meaningful until <code>get_throttled</code> reads <code>0x0</code>.</b> F1 is the root cause; rebuilding wiring on a sagging rail just produces better-looking intermittency.</div>
<ol class="gates">{gates}</ol></section>
{sheets}
<section id="views"><h2>Views</h2><div class="grid">{figs}</div></section>
<footer>HICS - Himalayan Institute for Contextual Sciences - IESH v0.2. Not calibrated; one station, one rooftop, 1350 m; the container is the proof-of-concept housing, not the product.</footer>
"""


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('schematic', schematic), ('perfboard', perfboard),
                     ('pinout', pinout), ('lid-layout', lid_layout)):
        with open(os.path.join(OUT, f'{name}.svg'), 'w') as f:
            f.write(fn())
        print(f'wrote docs/drawings/{name}.svg')
    with open(os.path.join(os.path.dirname(OUT), 'bench.html'), 'w') as f:
        f.write(bench_html())
    print('wrote docs/bench.html')
