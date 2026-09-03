#!/usr/bin/env python3
"""Numeric checks on roofbox.scad — the assertions a render cannot make.

    python3 roofbox_check.py          # exit 1 on any FAIL

Reads the top-level constants straight out of the .scad (so it cannot drift
from the geometry), then checks what two rounds of eyeballing renders missed
the first time: XY clashes on the plate, the usable field, the stack height,
whether the fisheye actually clears the hood, and whether the ribbon reaches.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, 'roofbox.scad')).read()

# ── pull constants ─────────────────────────────────────────────────────────
ns = {'sqrt': math.sqrt}
CLEAN = re.sub(r'//[^\n]*', '', SRC)          # comments off, so '=' in prose is ignored
for m in re.finditer(r'(?<![\w.])([A-Z][A-Z0-9_]*)\s*=\s*([^;{}]+?);', CLEAN):
    name, expr = m.group(1), m.group(2).strip()
    try:
        ns[name] = eval(expr, {'__builtins__': {}}, ns)
    except Exception:
        pass   # strings / module-level expressions we don't need

V = lambda k: ns[k]   # noqa: E731
fails = []


def check(desc, ok, detail=''):
    print(f"  {'PASS' if ok else 'FAIL'}  {desc}" + (f'   [{detail}]' if detail else ''))
    if not ok:
        fails.append(desc)


def rect(name, x0, y0, w, h):
    return (name, x0, y0, x0 + w, y0 + h)


def overlap(a, b):
    return not (a[3] <= b[1] or b[3] <= a[1] or a[4] <= b[2] or b[4] <= a[2])


# ── plate items, XY, in build coordinates (plate centred on the origin) ─────
pi   = rect('Pi',    *V('PI_ORG'),   V('PI_W'),   V('PI_D'))
buck = rect('buck',  *V('BUCK_ORG'), V('BUCK_W'), V('BUCK_D'))
fx = V('TOWER_OX') + 2 * V('FLANGE_W')
fy = V('TOWER_OY') + 2 * V('FLANGE_W')
tower = rect('tower flange', V('CAM_ORG')[0] - fx / 2, V('CAM_ORG')[1] - fy / 2, fx, fy)
tm = V('TIE_MOUNT')
lugs = [rect(f'tie mount y={y}', V('CLAMP_X') - tm / 2, y - tm / 2, tm, tm) for y in V('CLAMP_YS')]
items = [pi, buck, tower] + lugs

print('XY clash (no two plate items may overlap):')
for i, a in enumerate(items):
    for b in items[i + 1:]:
        check(f'{a[0]} vs {b[0]}', not overlap(a, b))

print('usable field (+/-%.0f mm, inside the seal channel):' % (V('USABLE') / 2))
half = V('USABLE') / 2
for it in items:
    inside = it[1] >= -half and it[2] >= -half and it[3] <= half and it[4] <= half
    check(f'{it[0]} inside', inside, f'x {it[1]:.1f}..{it[3]:.1f}  y {it[2]:.1f}..{it[4]:.1f}')

print('height:')
stack = V('Z_HAT') + V('HAT_T') + 16          # tallest HAT part: the 1000 uF cap
avail = V('BOX_H') - V('BOX_WALL')
check('stack fits the interior', stack + 10 < avail, f'{stack:.1f} mm in {avail:.1f} mm')

print('sky view:')
proud = V('Z_TOWER_TOP') - (V('Z_HOOD') + V('HOOD_T'))
check('fisheye lip is proud of the hood', proud >= 3, f'{proud:.1f} mm above the hood plate')
ap = V('FE_RING_D') - 4
check('lip aperture clears a fisheye rear element', ap >= 14, f'aperture {ap:.1f} mm (U2: measure the ring)')
bore_ok = V('TOWER_IX') >= V('CAM_W') + 1 and V('TOWER_IY') >= V('CAM_D') + 1
check('tower bore passes the OV5647 board', bore_ok,
      f'bore {V("TOWER_IX")} x {V("TOWER_IY")} vs board {V("CAM_W")} x {V("CAM_D")}')

print('ribbon:')
csi, cam = V('CSI_XY'), V('CAM_ORG')
xy = math.hypot(csi[0] - cam[0], csi[1] - cam[1])
# connector is on top of the Pi (interior side); ribbon drops to the lid,
# through the bore, and up the tower to the board. 20 mm for the two folds.
path = xy + (V('Z_PI') + V('PI_T') + 8) + (-V('Z_PCB')) + 20
check('110 mm FFC reaches the tower', path <= V('RIBBON_LEN'),
      f'path ~{path:.0f} mm of {V("RIBBON_LEN"):.0f}')

print('hood table:')
check('legs clear the lid', V('LEG_CLEAR') >= 2, f'{V("LEG_CLEAR"):.1f} mm between leg and lid edge')
check('legs stand on the tile', V('LEG_XY') + V('LEG_D') / 2 <= V('TILE') / 2 - 10,
      f'leg at {V("LEG_XY"):.0f}, tile half {V("TILE")/2:.0f}')
check('hood wider than the lid on every side', (V('HW') - V('LID_W')) / 2 >= 15,
      f'{(V("HW") - V("LID_W"))/2:.0f} mm overhang')

print('lid penetrations:')
holes = SRC.count('cylinder(d=2.2')   # blind threads only; nothing else may cut the plate through
plate_cuts = [l for l in SRC.splitlines() if 'linear_extrude(LID_T + 2)' in l]
check('the only through-cut in chassis() is the tower bore', len(plate_cuts) == 1, f'{len(plate_cuts)} through-cut(s)')

print('cable lengths (site layout, CABLE_SLACK included):')
mast_run = (math.hypot(V('MAST_XY')[0] - V('BOX_BASE') / 2, V('MAST_XY')[1]) + V('SHIELD_Z') + V('CABLE_SLACK'))
soil_run = (math.hypot(V('VASE_XY')[0] + V('BOX_BASE') / 2, V('VASE_XY')[1]) + V('VASE_H') + 100 + V('CABLE_SLACK'))
pwr_run  = (math.hypot(V('JBOX_XY')[0], V('JBOX_XY')[1] + V('BOX_BASE') / 2) + V('STAND_H') + V('CABLE_SLACK'))
for name, mm in (('mast CAT5e', mast_run), ('soil CAT5e', soil_run), ('power 2-core', pwr_run)):
    print(f'  INFO  {name:<13} cut {math.ceil(mm / 100) / 10:.1f} m')

print('side-wall glands:')
edge = V('GLAND_PITCH') + V('GLAND_HOLE') / 2
check('outer glands clear the plan corner radius', edge <= V('BOX_BASE') / 2 - V('BOX_R'),
      f'{edge:.1f} <= {V("BOX_BASE")/2 - V("BOX_R"):.1f}')
check('nut clearance between glands', V('GLAND_PITCH') >= 19 + 4, f'pitch {V("GLAND_PITCH")}')
check('PG7 hole is the THREAD size, not the cable size', V('GLAND_HOLE') >= 12.5)

print()
if fails:
    print(f'{len(fails)} FAILED: {fails}')
    sys.exit(1)
print('all roofbox checks pass')
