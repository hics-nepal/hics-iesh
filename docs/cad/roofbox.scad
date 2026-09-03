// ============================================================================
// IESH-ROOFBOX — interim rooftop variant, Lalitpur proof-of-concept
//
//   The enclosure is a FOUND OBJECT: a 120 x 120 x 180 mm gasketed square food
//   container with a snap lid (red silicone seal). It is not printed and not the
//   product — the printed EDU/SCI shells in edu.scad / sci.scad remain that.
//   SCOPE: a working deployment, not a production build. So almost nothing here
//   is fabricated — the real lid is a placement job (see lid_layout()), the gas
//   pod can be any small vented tub, and the radiation shield can be five
//   inverted plant-pot saucers on a bolt. The ONE part that genuinely wants
//   printing is cam_tower(), because the fisheye-to-sensor spacing has to be
//   held accurately. Everything else is a found object.
//
//   This file exists to (a) fit-check the real electronics in the real
//   container, (b) place the sensors, and (c) emit the drilling template.
//
//   Product tier: powered outdoor site (home / school roof), i.e. tier 2 in
//   01-hardware/04-power-architecture.md -> closer to CONFIG-SCI-BUILDING than
//   to CONFIG-EDU-BASE. No display window, no demonstrative cutaway.
//
//   THE CENTRAL DECISION: the LID IS THE CHASSIS PLATE. Everything bolts to it;
//   the box body is just a cover that closes over the assembly onto the gasket.
//   Lid off = the whole instrument lifts out as a unit for bench work, and
//   nothing is ever assembled inside a 120 mm box.
//
//   ORIENTATION: LID UP, and this is forced by the camera, not chosen.
//   The Pi camera ribbon on hand is only 100-120 mm. An all-sky camera must
//   look up; the Pi must be within a ribbon's length of it. So the camera sits
//   in the lid and the Pi hangs directly beneath it — about 60 mm of ribbon.
//   Inverting the box (lid down) would put the Pi 180 mm from the sky-facing
//   end and the ribbon would not reach. Buying a 300-500 mm FFC would free the
//   choice; with this ribbon, lid-up is the only layout that works.
//
//   The cost of lid-up is that rain can sit on the lid gasket, so the hood()
//   part is NOT optional — it keeps direct rain off the seal. It is needed for
//   solar-gain reasons anyway (a sealed box in Kathmandu sun runs 45-55 C
//   inside), so one part solves both problems.
//
//   Cable glands therefore move OFF the lid and into the box side wall, low
//   down, so no penetration faces the sky. Drip loops below each one.
//
//   Environmental sensors do NOT live in here. A sealed box on a Kathmandu roof
//   runs 45-55 C inside; a DHT22 in it measures the box. See gas_pod() and
//   rad_shield() for where they go, and ../../HANDOFF.md §7 / §12.
//
//   LIVES IN hics-iesh-v0.1/docs/cad/ (versioned with the deployment it serves),
//   not beside edu.scad/sci.scad in iesh-production-reference - those are the
//   product; this is one rooftop. ./render.sh regenerates every view below
//   into renders/ and templates/, and runs roofbox_check.py.
//
//   THE CAMERA MUST CLEAR THE HOOD. The first draft seated the fisheye flush in
//   the lid, under a 32 mm-high hood with a 49 mm aperture: an "all-sky" camera
//   that could see a 75 degree cone. cam_tower() now carries the lens up THROUGH
//   the hood so it sits proud of it and sees the whole hemisphere. The ribbon
//   still reaches: the tower sits directly under the Pi's CSI connector.
//
//   THE LID GETS NO HOLES IT DOES NOT NEED. Second-pass audit: the first draft
//   bolted the hood legs through the lid at +/-65 mm - on the gasket channel -
//   and put six zip-tie slots through it. Now: the hood is a free-standing
//   table over the box (legs to the paving tile, not the lid); cable ties go
//   on adhesive mounts; Pi and buck standoffs are BONDED to the lid underside.
//   The only lid penetration is the camera tower, and the camera is deferred -
//   so today's build drills the lid NOWHERE. lid_layout() is a placement
//   template, not a drilling template.
//
//   THE LENS SITS UNDER A LIP, NOT IN A CUP. A pocket facing the sky is a water
//   trap; the ring now goes in from inside the tube and beds in silicone under a
//   2 mm lip, so the lip sheds water and the silicone is never the first line.
//
//   Section views are 2D (projection(cut=true)) because OpenSCAD 2021's preview
//   cannot be trusted to show a nested cut - it paints cut faces flat. The 2D
//   sections are exact; roofbox_check.py measures what a picture cannot.
//
//   render:  part = "site"      the whole station on the roof: box, mast, vase, cables
//                 | "service"   the box as it stands: hood table, tower, body
//                 | "exploded"  hood plate / plate stack / body, pulled apart
//                 | "plan"      plate layout from the interior side
//                 | "mast"      shield + gas pod + rain plate on the PVC
//                 | "chassis" | "cam_tower" | "hood" | "gas_pod" | "shield" | "container"
//            2D:  | "section2d"  service orientation, cut on the tower's centre plane
//                 | "tower2d"    the tower alone, same cut
//                 | "lid"        1:1 lid PLACEMENT template (bond standoffs; witness only)
//                 | "drill_wall" 1:1 side-wall template: 3 gland holes + vent
//   check:   python3 roofbox_check.py     (XY clash, field, height, sky, ribbon, cable lengths)
// ============================================================================

part = "assembly";
$fn = 48;

// ---- the found container ---------------------------------------------------
// MEASURED: 120 x 120 base, 180 tall (excluding the rim).
// ASSUMPTION: the taper and the rim flange are estimated from photographs.
// TODO: measure BOX_TOP and RIM_W with calipers and correct these two lines.
BOX_BASE   = 120.0;   // outer, at the closed (moulded) end
BOX_TOP    = 130.0;   // ASSUMPTION - outer, at the lid opening
BOX_H      = 180.0;   // excluding rim
RIM_W      = 8.0;     // ASSUMPTION - flange width beyond BOX_TOP
RIM_T      = 6.0;     // ASSUMPTION - flange thickness
BOX_WALL   = 1.8;     // ASSUMPTION - typical PP food container
BOX_R      = 14.0;    // corner radius
GASKET_T   = 2.0;     // red silicone seal in the lid channel

LID_T      = 2.5;     // lid panel thickness
LID_W      = BOX_TOP + 2*RIM_W;

// Interior clear space, at the lid end (the widest point, where we mount).
IN_AT_LID  = BOX_TOP - 2*BOX_WALL;      // ~126
USABLE     = IN_AT_LID - 10;            // ~116 - keep clear of the seal channel

// ---- real electronics ------------------------------------------------------
// Raspberry Pi 3B+ (this station), NOT the 4B modelled in iesh_lib.scad.
PI_W = 85.0;  PI_D = 56.0;  PI_T = 1.6;
PI_MH = [[3.5,3.5],[3.5,52.5],[61.5,3.5],[61.5,52.5]];   // M2.5, 58 x 49 grid
PI_PORTS_H = 17.0;                       // USB/Ethernet stack

// Protoboard HAT — 10 x 15 cm matrix board cut to the carrier-hat-v1 footprint,
// so the layout transfers when 02-pcb/carrier-hat-v1 is fabbed.
HAT_W = 65.0;  HAT_D = 70.0;  HAT_T = 1.6;

STANDOFF_LID = 10.0;                     // lid inner face -> Pi PCB bottom
SOCKET_GAP   = 12.8;                     // Pi top -> HAT bottom (40-pin socket)

Z_PI   = LID_T + STANDOFF_LID;
Z_HAT  = Z_PI + PI_T + SOCKET_GAP;

// POWER: a 12 V -> 5 V 3 A buck module, NOT a mains adapter.
// Three reasons this is the right call for a rooftop box:
//   1. no mains inside a plastic food container on a roof;
//   2. 12 V up the cable draws ~2.4x less current than 5 V for the same power,
//      so the run loses far less voltage — and voltage drop IS fault F1;
//   3. it feeds straight off the 12 V lead-acid UPS with no double conversion.
// The 5 V adapter stays indoors, or is replaced by the UPS entirely.
BUCK_W = 25; BUCK_D = 45; BUCK_H = 16;   // ASSUMPTION - measure yours (U8).
                                         // Mounted long side along Y.
Z_BUCK = LID_T + 6;                      // its own short standoffs

// ---- plate layout ----------------------------------------------------------
// SIGN CONVENTION, stated once because getting it wrong put the camera on the
// far side of the lid from the Pi in the first draft:
//   MODELLED in build orientation - plate at z=0, +z is the INTERIOR (where
//   every board lives), -z is the EXTERIOR (where the fisheye boss protrudes).
//   IN SERVICE the assembly is flipped, so +z hangs down inside the box and the
//   fisheye faces the sky.
// Positions are lower-left corners, plate centred on the origin. Usable field
// is +/-58 mm (LID_W/2 minus the seal channel). No two items may overlap in XY
// - verified by the clash check, not by eye.
PI_ORG   = [-50, -12];    // Pi 85 x 56  -> x -50..35,  y -12..44
BUCK_ORG = [16, -58];     // buck 25x45  -> x  16..41,  y -58..-13
// Adhesive zip-tie mounts (19 mm square, self-adhesive + a dab of silicone)
// for the three cables, on the free left-hand strip of the lid underside.
// Strain relief lives here, not at a gland, and it puts NO hole in the lid.
CLAMP_X  = -45;
CLAMP_YS = [-46, -24];       // two mounts carry three cables comfortably
TIE_MOUNT = 19;

// Only TWO sensor penetrations: one CAT5e up the mast, one down to the vase.
// Plus power in. Six sensors, three holes. See HANDOFF.md §10.
// They go in the BOX SIDE WALL, low down, NOT in the lid - nothing faces the
// sky. drill_wall() is their template. A PG7 gland (cable 3-6.5 mm, CAT5e is
// ~5.5) needs a 12.5 mm hole; PG9 (4-8 mm) needs 15.2. The first draft had
// GLAND_ID = 7 - that is the CABLE size, and would have been drilled.
GLAND_HOLE = 12.5;   // PG7 thread. Use 15.2 for PG9.
GLAND_PITCH = 34;    // centre spacing: a PG7 nut is ~19 mm across flats
GLAND_Z     = 32;    // hole centre above the box base (service orientation) -
                     // clear of the base corner radius, low enough for drip loops
GLANDS = ["mast CAT5e", "soil CAT5e", "power in"];

// BMP280 breathing hole: pressure equalises through anything, but a PERFECTLY
// sealed vault gives a false offset as the box heats. One 2 mm hole, backed by
// PTFE tape, in the same side wall as the glands, up under the hood's shadow.
VENT_D = 2.0;
VENT_Z = 120;

// ---- camera + clip-on fisheye ----------------------------------------------
// OV5647 board (Pi Camera Rev 1.3), measured from the board in hand.
CAM_W = 25.0; CAM_D = 24.0; CAM_T = 1.0;
CAM_MH = 12.5;                 // M2 mount holes, 12.5 mm square grid
CAM_LENS_H = 6.0;              // stock lens barrel height above the PCB
RIBBON_LEN = 110.0;            // AS MEASURED - the constraint that sets layout

// The clip-on phone fisheye. It is held in a hinged clip; the lens element with
// its knurled ring unscrews from the clip arm and is what we actually mount.
// THE LENS IS THE WINDOW: sealing its barrel into a boss in the lid means the
// camera is not also shooting through a sheet of acrylic, which would add
// reflections and haze for no benefit.
// TODO: measure these three with calipers before printing. Values are estimates
// read off the photograph and WILL need correcting.
FE_RING_D  = 23.0;   // ASSUMPTION - knurled ring outer diameter
FE_RING_H  = 9.0;    // ASSUMPTION - ring height
FE_BACK    = 3.0;    // ASSUMPTION - lens rear face -> OV5647 lens front.
                     // Clip-on fisheyes expect ~2-4 mm off a phone lens; this
                     // is the one dimension to find by trial. Print the boss
                     // with a threaded or shimmable seat so it can be adjusted.
CAM_ORG    = [-6, -35];        // tower centre: directly below the Pi's CSI
                               // connector (3B+: ~45 mm from the SD edge, on
                               // the -y long edge), clear of the Pi footprint,
                               // the buck and the clamp lugs. ~35 mm of ribbon.
CSI_XY     = [PI_ORG[0] + 45, PI_ORG[1] + 1];   // where the ribbon leaves the Pi

// The tower: a square tube through the lid and the hood, fisheye ring seated
// at the sky end, OV5647 board on a three-sided ledge just behind it, ribbon
// down the tube. The bore is deeper in Y than X so the FFC can fold without a
// hard crease where it leaves the connector.
HOOD_T     = 2.5;
HOOD_GAP   = 32;               // lid top face -> hood underside (air gap)
TOWER_IX   = 27;  TOWER_IY = 32;            // bore: passes the 25 x 24 board
TOWER_WALL = 2.5;
TOWER_OX   = TOWER_IX + 2*TOWER_WALL;       // 32
TOWER_OY   = TOWER_IY + 2*TOWER_WALL;       // 37
TOWER_H    = HOOD_GAP + HOOD_T + 6;         // ring top 6 mm proud of the hood
FLANGE_W   = 4;                             // sealing flange each side, outside

// ============================================================================
//  reference geometry - the found container
// ============================================================================
module rrsq(w, r) offset(r=r) offset(r=-r) square([w,w], center=true);

// Drawn in BUILD orientation: the lid opening is at z=0 (where the chassis
// plate sits) and the closed moulded end is up at z=BOX_H. In SERVICE the whole
// thing is flipped — lid down — so every gland points at the ground.
module container() {
  color([1,1,1,0.16]) difference() {
    hull() {
      linear_extrude(0.01) rrsq(BOX_TOP, BOX_R);
      translate([0,0,BOX_H]) linear_extrude(0.01) rrsq(BOX_BASE, BOX_R);
    }
    // hollow, closed at the far (moulded) end
    translate([0,0,-1]) hull() {
      linear_extrude(0.01) rrsq(BOX_TOP - 2*BOX_WALL, BOX_R);
      translate([0,0,BOX_H - BOX_WALL + 1])
        linear_extrude(0.01) rrsq(BOX_BASE - 2*BOX_WALL, BOX_R);
    }
  }
  // rim flange at the open (lid) end — sits just below the chassis plate
  color([1,1,1,0.16])
    translate([0,0,-RIM_T]) linear_extrude(RIM_T)
      difference() { rrsq(LID_W, BOX_R); rrsq(BOX_TOP - 2*BOX_WALL, BOX_R); }
  // the red silicone gasket, compressed between rim and chassis plate
  color([0.75,0.12,0.12,0.55])
    translate([0,0,-GASKET_T]) linear_extrude(GASKET_T)
      difference() { rrsq(BOX_TOP+1, BOX_R); rrsq(BOX_TOP-5, BOX_R); }
}

// ============================================================================
//  the part we FABRICATE - the lid used as a chassis plate
// ============================================================================
module tie_mounts() {
  for (y = CLAMP_YS) color("#eceff1")
    translate([CLAMP_X - TIE_MOUNT/2, y - TIE_MOUNT/2, LID_T]) cube([TIE_MOUNT, TIE_MOUNT, 4]);
}

module chassis() {
  difference() {
    union() {
      // the lid panel itself
      linear_extrude(LID_T) rrsq(LID_W, BOX_R);
      // Pi standoff posts, BONDED to the lid underside (epoxy / neutral-cure
      // silicone on M2.5 brass standoffs) - no screw heads outside, no holes.
      // The Pi carries the HAT on its own 40-pin socket, so only the Pi needs
      // tall posts.
      translate(PI_ORG)
        for (h = PI_MH) translate([h[0], h[1], 0])
          cylinder(d=6, h=STANDOFF_LID+LID_T);
      // buck module posts
      translate(BUCK_ORG)
        for (x=[3, BUCK_W-3], y=[3, BUCK_D-3]) translate([x,y,0])
          cylinder(d=5, h=Z_BUCK);
    }
    // threads in the posts (blind - they do not break the lid's outer face)
    translate(PI_ORG)
      for (h = PI_MH) translate([h[0], h[1], LID_T + 1])
        cylinder(d=2.2, h=STANDOFF_LID+2);
    translate(BUCK_ORG)
      for (x=[3, BUCK_W-3], y=[3, BUCK_D-3]) translate([x,y,LID_T + 1])
        cylinder(d=2.2, h=Z_BUCK);
    // camera bore: the tower passes through the plate here - the ONLY hole,
    // and only once the camera is fitted
    translate([CAM_ORG[0], CAM_ORG[1], -1])
      linear_extrude(LID_T + 2) square([TOWER_OX + 0.6, TOWER_OY + 0.6], center=true);
  }
}

// ============================================================================
//  electronics, for fit-checking only
// ============================================================================
module pi3bplus() {
  translate([PI_ORG[0], PI_ORG[1], Z_PI]) {
    color("#1a6b3c") cube([PI_W, PI_D, PI_T]);
    // 3B+: two USB stacks + Ethernet on the SHORT (x = 85) edge, overhanging 2 mm
    color("#9aa0a6") translate([PI_W-17, 2,  PI_T]) cube([19, 15, PI_PORTS_H]);
    color("#9aa0a6") translate([PI_W-17, 20, PI_T]) cube([19, 15, PI_PORTS_H]);
    color("#9aa0a6") translate([PI_W-21, 38, PI_T]) cube([23, 16, 13.5]);
    // long -y edge: micro-USB power, HDMI, CSI (the camera connector), audio
    color("#9aa0a6") translate([6,  -1, PI_T]) cube([8, 6, 3]);
    color("#9aa0a6") translate([25, -1, PI_T]) cube([15, 12, 6]);
    color("#e0b000") translate([42, 0.5, PI_T]) cube([4, 22, 5.5]);    // CSI socket
    color("#9aa0a6") translate([50, -1, PI_T]) cube([7, 12, 6]);
    // 40-pin header, SoC
    color("#222") translate([3.5, PI_D-6.5, PI_T]) cube([51, 5, 8.5]);
    color("#b0b0b0") translate([28, 22, PI_T]) cube([15,15,3]);
  }
}

module proto_hat() {
  // Seated on the Pi's 40-pin header, aligned to it as a real HAT is.
  translate([PI_ORG[0] + 3.5, PI_ORG[1] + PI_D - HAT_D + 3.0, Z_HAT]) {
    color("#8a6a2a") cube([HAT_W, HAT_D, HAT_T]);
    // MCP3208 DIP-16 - already soldered on the existing board, kept as-is
    color("#111") translate([8, 30, HAT_T]) cube([20, 8, 4]);
    // screw terminals along the free edge: mast(8) soil(4) power(2)
    color("#1e88e5") translate([2, 2, HAT_T]) cube([HAT_W-4, 8, 10]);
    // DS3231 RTC module (needs a FRESH coin cell - the fitted one is flat)
    color("#0d47a1") translate([38, 44, HAT_T]) cube([22, 15, 4]);
    color("#ccc")    translate([44, 48, HAT_T+4]) cylinder(d=12, h=3);
    // BMP280 - the only environmental sensor allowed inside
    color("#4a148c") translate([8, 46, HAT_T]) cube([11, 15, 3]);
    // bulk cap on the 5 V rail, next to the MQ feed
    color("#212121") translate([26, 12, HAT_T]) cylinder(d=10, h=16);
  }
}

module buck() {
  translate([BUCK_ORG[0], BUCK_ORG[1], Z_BUCK]) {
    color("#0b6e4f") cube([BUCK_W, BUCK_D, 1.6]);
    color("#37474f") translate([4, 5, 1.6]) cylinder(d=10, h=BUCK_H-1.6);  // inductor
    color("#1e88e5") translate([BUCK_W-9, 3, 1.6]) cube([7, BUCK_D-6, 9]); // terminals
  }
}

// ============================================================================
//  printable mast parts - where the environmental sensors actually live
// ============================================================================

// Downward-facing vented pod for MQ-7 + MQ-135. They must see ambient air and
// they self-heat ~350 mW each; inside the vault they would read their own
// exhaust and warm the Pi. Vents face down so rain cannot drive in.
POD_W = 78; POD_D = 42; POD_H = 46; POD_WALL = 2.2;   // two 32 x 20 MQ modules side by side
module gas_pod() {
  difference() {
    union() {
      linear_extrude(POD_H) offset(r=3) offset(r=-3) square([POD_W,POD_D], center=true);
      // mast saddle for 20 mm PVC
      translate([0, POD_D/2+6, POD_H/2]) rotate([0,90,0])
        difference() {
          cylinder(d=28, h=30, center=true);
          cylinder(d=20.5, h=32, center=true);
          translate([0,-16,0]) cube([34,32,32], center=true);
        }
    }
    // hollow, open at the BOTTOM
    translate([0,0,-1]) linear_extrude(POD_H-POD_WALL+1)
      offset(r=3) offset(r=-3) square([POD_W-2*POD_WALL, POD_D-2*POD_WALL], center=true);
    // downward louvres in the skirt
    for (i=[0:4]) translate([0, 0, 4 + i*7])
      for (s=[-1,1]) translate([s*(POD_W/2-POD_WALL/2), 0, 0])
        rotate([0,35,0]) cube([POD_WALL*4, POD_D-14, 3], center=true);
    // cable gland into the top
    translate([0,0,POD_H-POD_WALL-1]) cylinder(d=GLAND_HOLE, h=POD_WALL+2);
  }
  // two MQ modules, shown for fit: 32 x 20 boards, 17 mm sensor can
  for (s=[-1,1]) color("#1565c0")
    translate([s*18, 0, 6]) {
      cube([32, 20, 1.6], center=true);
      color("#9e9e9e") translate([0,0,1]) cylinder(d=17, h=10);
    }
}

// Stacked-plate radiation shield for the DHT22. THIS IS THE ONE THAT MATTERS:
// a DHT22 in sun, or in the box, produces numbers that look fine and mean
// nothing. Print these, or invert and space five ~100 mm plant-pot saucers -
// which works genuinely well and costs almost nothing.
SH_D = 104; SH_PLATES = 5; SH_GAP = 13; SH_T = 2.0;
module rad_shield() {
  for (i=[0:SH_PLATES-1]) translate([0,0,i*SH_GAP])
    difference() {
      // shallow cone: sheds rain, and each plate shades the one below
      cylinder(d1=SH_D - i*6, d2=SH_D - i*6 - 12, h=SH_T+3);
      translate([0,0,-1]) cylinder(d1=SH_D-i*6-14, d2=SH_D-i*6-26, h=SH_T+5);
      // three spacer bolt holes
      for (a=[0:120:359]) rotate([0,0,a]) translate([SH_D/2-i*3-9, 0, -1])
        cylinder(d=3.4, h=SH_T+6);
    }
  // DHT22, hanging in the shaded, ventilated middle
  color("#e0e0e0") translate([-12.5,-9, SH_GAP*2])
    cube([25, 18, 10]);
  // mast saddle
  translate([0, 0, -14]) rotate([0,90,0])
    difference() {
      cylinder(d=28, h=26, center=true);
      cylinder(d=20.5, h=28, center=true);
    }
}

// ============================================================================
//  camera tower - printed, the ONE part that must be printed
// ============================================================================
// Carries the fisheye up through the hood so it sees the whole sky, seals the
// lid bore with a flange bedded in neutral-cure silicone (NOT acetoxy), and
// holds the OV5647 FE_BACK behind the lens on a three-sided ledge - open on
// the -y side where the ribbon leaves the connector. Print sky-end down.
// The ring goes in FROM INSIDE the tube and beds in silicone under a 2 mm lip:
// the lip sheds water; a sky-facing pocket would have collected it.
// Build orientation: -z is outside (sky), so the tower hangs to -z here.
LIP_T  = 2;
Z_SKY  = -TOWER_H;                                   // lip top
Z_RING = Z_SKY + LIP_T;                              // ring top, under the lip
Z_PCB  = Z_RING + FE_RING_H + FE_BACK + CAM_LENS_H;  // lens-side face of the PCB
module cam_tower(show_parts=true) {
  difference() {
    union() {
      translate([0,0,Z_SKY]) linear_extrude(TOWER_H)
        offset(r=3) offset(r=-3) square([TOWER_OX, TOWER_OY], center=true);
      // sealing flange on the OUTSIDE face of the lid
      translate([0,0,-3]) linear_extrude(3)
        offset(r=3) offset(r=-3) square([TOWER_OX + 2*FLANGE_W, TOWER_OY + 2*FLANGE_W], center=true);
    }
    // bore
    translate([0,0,Z_SKY - 1]) linear_extrude(TOWER_H + 2)
      square([TOWER_IX, TOWER_IY], center=true);
    // lens seat is cut out of the cap below; here just keep the bore
  }
  // sky-end cap: a LIP with the optical aperture, and beneath it the ring
  // pocket, open toward the inside of the tube (+z). Ring in from below.
  translate([0,0,Z_SKY]) difference() {
    linear_extrude(LIP_T + FE_RING_H)
      offset(r=3) offset(r=-3) square([TOWER_OX, TOWER_OY], center=true);
    translate([0,0,-1]) cylinder(d=FE_RING_D - 4, h=LIP_T + 2);                  // aperture
    translate([0,0,LIP_T]) cylinder(d=FE_RING_D + 0.4, h=FE_RING_H + 1);         // pocket
  }
  // PCB ledge: three sides, 2.5 mm wide, on the +z (back) side of the board
  translate([0,0,Z_PCB + CAM_T]) linear_extrude(2) difference() {
    square([TOWER_IX + 0.2, TOWER_IY + 0.2], center=true);
    translate([0, 2.5]) square([TOWER_IX - 5, TOWER_IY + 5], center=true);
    translate([-TOWER_IX, -TOWER_IY/2 - 5]) square([2*TOWER_IX, 5 + 6]);  // -y side open
  }
  // two M2 posts at the +y holes: the board screws to these, the ledge locates it
  for (x=[-CAM_MH/2, CAM_MH/2]) translate([x, CAM_MH/2, Z_PCB + CAM_T])
    difference() { cylinder(d=4.6, h=4); translate([0,0,-1]) cylinder(d=1.8, h=6); }
  if (show_parts) {
    color("#1a6b3c") translate([-CAM_W/2, -CAM_D/2, Z_PCB]) cube([CAM_W, CAM_D, CAM_T]);
    color("#37474f") translate([0,0,Z_PCB - CAM_LENS_H]) cylinder(d=8.5, h=CAM_LENS_H);
    // FFC: out of the connector toward -y, fold, down the bore, out under the lid
    color("#e8e4d8") translate([-8, -TOWER_IY/2 + 1, Z_PCB + CAM_T + 1]) cube([16, 0.3, -Z_PCB + 4]);
    color("#1a1a1a") translate([0,0,Z_RING]) cylinder(d=FE_RING_D, h=FE_RING_H);
  }
}

// ============================================================================
//  sun / rain hood - mandatory, and FREE-STANDING
// ============================================================================
// Two jobs: keep direct rain off the lid gasket (the cost of lid-up), and keep
// the sun off a sealed box that would otherwise run 45-55 C inside. It stands
// on its own four legs on the paving tile, straddling the box: nothing bolts
// to the lid, the legs clear the lid by LEG_CLEAR, and the box lifts straight
// out from under it for service. Air gap HOOD_GAP above the lid - an air gap
// is what makes a shade work.
HW       = LID_W + 52;            // hood plate: 198 square - legs clear the lid by 4 mm
LEG_D    = 20;                    // 20 mm PVC, same stock as the mast
LEG_XY   = HW/2 - LEG_D/2 - 2;    // leg centres
LEG_CLEAR = LEG_XY - LEG_D/2 - LID_W/2;   // must be > 0 - checked
// service-orientation heights, tile top = 0
Z_LID_TOP = BOX_H + RIM_T + LID_T;
Z_HOOD    = Z_LID_TOP + HOOD_GAP;         // underside of the hood plate
Z_TOWER_TOP = Z_LID_TOP + TOWER_H;

// the plate alone, build orientation (used by exploded())
module hood_plate() {
  difference() {
    linear_extrude(HOOD_T) rrsq(HW, BOX_R + 6);
    // the tower passes through here and stands proud: 2 mm clearance all round
    translate([CAM_ORG[0], -CAM_ORG[1], -1])      // y mirrored: service view is flipped
      linear_extrude(HOOD_T + 2) square([TOWER_OX + 4, TOWER_OY + 4], center=true);
    for (sx=[-1,1], sy=[-1,1]) translate([sx*LEG_XY, sy*LEG_XY, -1]) cylinder(d=4.2, h=HOOD_T+2);
  }
}

// the whole table, SERVICE orientation, standing on z = 0
module hood_frame() {
  color("#78909c") translate([0,0,Z_HOOD]) hood_plate();
  for (sx=[-1,1], sy=[-1,1]) color("#eceff1")
    translate([sx*LEG_XY, sy*LEG_XY, 0]) difference() {
      cylinder(d=LEG_D, h=Z_HOOD);
      translate([0,0,-1]) cylinder(d=LEG_D - 4, h=Z_HOOD + 2);
    }
}

// ============================================================================
//  templates - 1:1, exported as SVG in mm
// ============================================================================
//   openscad -o roofbox_lid.svg        -D 'part="lid"'        roofbox.scad
//   openscad -o roofbox_drill_wall.svg -D 'part="drill_wall"' roofbox.scad
// LID: a PLACEMENT template. Tape it on the lid's underside and mark through
// it. Standoff positions are 2.8 mm marks - they are where to BOND standoffs,
// or where to drill only if you choose screws (then seal each head). The
// tower bore is a witness outline: cut it only when the camera is verified
// working and the printed tower fits the real fisheye (U2/U3). The gasket
// channel band is outlined: nothing goes through the lid there, ever.
module _outline(w, h, t=0.4) { difference() { square([w, h]); translate([t, t]) square([w-2*t, h-2*t]); } }
// Witness lines are CUT into the plate as 0.4 mm slots: a 2D union would
// otherwise swallow anything drawn on top of the solid lid square.
module lid_layout() {
  difference() {
    square([LID_W, LID_W], center=true);                  // lid outline
    translate(PI_ORG) for (h = PI_MH) translate(h) circle(d=2.8);          // Pi standoffs
    translate(BUCK_ORG)
      for (x=[3, BUCK_W-3], y=[3, BUCK_D-3]) translate([x,y]) circle(d=2.8);  // buck standoffs
    translate(CSI_XY) circle(d=1.5);                      // where the ribbon leaves the Pi
    translate(PI_ORG) _outline(PI_W, PI_D);
    translate(BUCK_ORG) _outline(BUCK_W, BUCK_D);
    translate(CAM_ORG) difference() {                     // tower bore - witness only
      square([TOWER_OX + 0.6, TOWER_OY + 0.6], center=true);
      square([TOWER_OX - 0.2, TOWER_OY - 0.2], center=true);
    }
    for (y = CLAMP_YS) translate([CLAMP_X - TIE_MOUNT/2, y - TIE_MOUNT/2]) _outline(TIE_MOUNT, TIE_MOUNT);
    // gasket channel band: between the wall line and the rim - keep out
    difference() { rrsq(BOX_TOP, BOX_R); rrsq(BOX_TOP - 0.5, BOX_R); }
    difference() { rrsq(BOX_TOP - 2*BOX_WALL - 6, BOX_R); rrsq(BOX_TOP - 2*BOX_WALL - 6.5, BOX_R); }
  }
}

// One side wall, unrolled, service orientation: base at the bottom. The wall
// tapers (BOX_BASE at the bottom, BOX_TOP at the lid) so it is a trapezium.
// Three PG7 holes low down for the glands, the 2 mm vent high up under the
// hood. Pick the wall that faces AWAY from the prevailing rain.
module drill_wall_template() {
  difference() {
    polygon([[-BOX_BASE/2, 0], [BOX_BASE/2, 0], [BOX_TOP/2, BOX_H], [-BOX_TOP/2, BOX_H]]);
    for (i = [0:2]) translate([(i-1)*GLAND_PITCH, GLAND_Z]) circle(d=GLAND_HOLE);
    translate([0, VENT_Z]) circle(d=VENT_D);
  }
  // witness: the base corner radius zone the glands must stay clear of
  difference() {
    translate([-BOX_BASE/2, 0]) square([BOX_BASE, BOX_R]);
    translate([-BOX_BASE/2 + 0.4, 0.4]) square([BOX_BASE - 0.8, BOX_R - 0.8]);
  }
}


// ============================================================================
//  the site - the whole station on the roof, to think with
// ============================================================================
// Not a fabrication drawing. It fixes the distances that decide cable lengths
// and sensor exposure, and lets the mast / vase / box relationship be argued
// about before anything is cut. Change a distance here and the cable lengths
// in roofbox_check.py change with it.
DECK_W = 1400; DECK_D = 900; DECK_T = 60;   // roof slab shown
MAST_D = 20; MAST_H = 1500;                 // 20 mm PVC, HANDOFF §13
MAST_XY = [600, 0];                         // mast foot, from the box centre
SHIELD_Z = 1400;                            // DHT22 shield centre: >= 1 m up, >= 300 clear
POD_Z = 1050;                               // gas pod, below the shield, open downward
RAIN_Z = 1250;                              // raindrop plate, tilted ~30 deg
LDR_Z  = 1330;
VASE_XY = [-650, 150]; VASE_D = 260; VASE_H = 280;   // the largest vase on the roof
JBOX_XY = [0, -420]; JBOX = [100, 100, 60];          // mains adapter, in its own box
CABLE_SLACK = 400;                                   // drip loop + service slack, each run

module deck() { color("#c9c2b6") translate([-DECK_W/2, -DECK_D/2, -DECK_T]) cube([DECK_W, DECK_D, DECK_T]); }
// a 300 mm concrete paving tile: heavy, flat, off the deck, and the hood legs
// stand on it too - so box and hood move as one unit
TILE = 300; STAND_H = 40;
module stand() { color("#9e9e9e") translate([-TILE/2, -TILE/2, 0]) cube([TILE, TILE, STAND_H]); }

module mast() {
  color("#d9d9d9") cylinder(d=MAST_D, h=MAST_H);
  translate([0,0,SHIELD_Z]) rotate([0,0,90]) rad_shield();
  translate([0,0,POD_Z]) rotate([180,0,90]) gas_pod();        // opens downward
  // raindrop plate: 60 x 40 board, ~30 deg so drops run off
  color("#2f6fd6") translate([0, -30, RAIN_Z]) rotate([30,0,0]) cube([60, 40, 1.6], center=true);
  color("#ffd54f") translate([0, 25, LDR_Z]) cylinder(d=6, h=3);   // LDR, facing up
}

module vase() {
  color("#b5651d") difference() {
    cylinder(d1=VASE_D*0.8, d2=VASE_D, h=VASE_H);
    translate([0,0,15]) cylinder(d1=VASE_D*0.8-16, d2=VASE_D-16, h=VASE_H);
  }
  color("#5d4037") translate([0,0,15]) cylinder(d1=VASE_D*0.8-16, d2=VASE_D-20, h=VASE_H-40); // soil
  // DS18B20 stainless probe buried 100 mm; capacitive blade vertical beside it
  color("#cfd8dc") translate([-30, 0, VASE_H-25-100]) cylinder(d=6, h=50);
  color("#111") translate([20, -12, VASE_H-25-98]) cube([23, 3, 98]);
}

module jbox() { color("#607d8b") translate([JBOX_XY[0]-JBOX[0]/2, JBOX_XY[1]-JBOX[1]/2, 0]) cube(JBOX); }

// a cable as straight runs between waypoints (drip loops not drawn)
module cable(pts, d=5.5, col="#f2c94c") {
  for (i=[0:len(pts)-2]) color(col) hull() {
    translate(pts[i]) sphere(d=d);
    translate(pts[i+1]) sphere(d=d);
  }
}

BOX_GLAND_PT = [BOX_BASE/2, -GLAND_PITCH, STAND_H + GLAND_Z];   // +x wall, low
module site() {
  deck();
  stand();
  translate([0,0,STAND_H]) service();
  translate([MAST_XY[0], MAST_XY[1], 0]) mast();
  translate([VASE_XY[0], VASE_XY[1], 0]) vase();
  jbox();
  // mast cable: gland -> drip loop -> up the mast -> pod -> shield
  cable([BOX_GLAND_PT, BOX_GLAND_PT + [30, 0, -25], [MAST_XY[0]-15, MAST_XY[1], 20],
         [MAST_XY[0]-15, MAST_XY[1], POD_Z], [MAST_XY[0]-15, MAST_XY[1], SHIELD_Z]]);
  // soil cable: gland -> along the deck -> over the vase rim -> down into the soil
  cable([[-BOX_BASE/2, 0, STAND_H + GLAND_Z], [-BOX_BASE/2 - 30, 0, STAND_H + GLAND_Z - 25],
         [VASE_XY[0] + VASE_D/2 + 10, VASE_XY[1], 20],
         [VASE_XY[0] + VASE_D/2 - 10, VASE_XY[1], VASE_H], [VASE_XY[0], VASE_XY[1], VASE_H - 60]],
        col="#4caf50");
  // power: junction box -> gland on the -y wall
  cable([[JBOX_XY[0], JBOX_XY[1] + JBOX[1]/2, JBOX[2]/2], [0, -BOX_BASE/2 - 30, STAND_H + GLAND_Z - 25],
         [0, -BOX_BASE/2, STAND_H + GLAND_Z]], d=4, col="#d32f2f");
}

// ============================================================================
//  assembly
// ============================================================================
// Stack only — no shell. The PNG backend renders solids opaque regardless of
// the alpha in color(), so including the container hides everything behind it.
module stack() {
  chassis();
  pi3bplus();
  proto_hat();
  buck();
  translate([CAM_ORG[0], CAM_ORG[1], 0]) cam_tower();
  tie_mounts();
  // camera bore through the plate itself is cut in chassis()
}

module assembly()       { stack(); }

// ---- views built to be LEGIBLE ---------------------------------------------
// The PNG backend ignores alpha, so a transparent shell just hides everything.
// These two views solve that honestly: lift the shell off, or cut it open.

// Service orientation: lid plate at z=0, box body hanging BELOW it, hood above.
// Container drawn opening-toward-the-plate, enclosing the +z interior side.
module box_below() { container(); }

module exploded() {
  translate([0,0,-40-HOOD_T]) hood_plate();   // hood plate OUTSIDE (-z) in build orientation
  stack();
  translate([0,0,46]) box_below();            // box closes over the interior side
}

// As it stands on the tile: base at z = 0, lid up, tower proud of the hood.
// rotate() not mirror(), so the geometry keeps its handedness.
module box_service() {
  translate([0,0,Z_LID_TOP]) rotate([180,0,0]) { stack(); box_below(); }
}
module service() { box_service(); hood_frame(); }

// Exact 2D sections: the material at the plane x = CAM_ORG.x (through the
// tower centre, the CSI connector and the Pi), service orientation, drawn in
// the y-z plane with z up. Voids are voids; nothing is painted over.
// (rotate(-90) so that +z ends up UP on the page: R_y(-90) puts (-z, y) on the
// plane, and a -90 turn maps that to (y, z).)
module section2d() {
  rotate(-90) projection(cut=true) rotate([0,-90,0]) translate([-CAM_ORG[0],0,0]) service();
}
module tower2d() {
  rotate(-90) projection(cut=true) rotate([0,-90,0]) translate([0,0,-Z_SKY]) rotate([180,0,0]) cam_tower();
}

// Service orientation, cut on the plane x = CAM_ORG.x so ONE view shows the
// tower with its lens and board, the ribbon path, the Pi + HAT stack hanging
// under the lid, and the hood gap above it.
module section() {
  rotate([180,0,0]) difference() {
    union() { stack(); box_below(); hood(); }
    translate([CAM_ORG[0] - 400, -400, -300]) cube([400, 800, 600]);
  }
}

module cam_tower_section() {
  rotate([180,0,0]) difference() {
    cam_tower();
    translate([-400, -400, -300]) cube([400, 800, 600]);
  }
}

module plan() { stack(); }
module assembly_boxed() { stack(); container(); }

if      (part == "assembly")       assembly();
else if (part == "assembly_boxed") assembly_boxed();
else if (part == "exploded")      exploded();
else if (part == "service")       service();
else if (part == "plan")          plan();
else if (part == "site")          site();
else if (part == "mast")          mast();
else if (part == "chassis")       chassis();
else if (part == "cam_tower")     cam_tower();
else if (part == "hood")          hood_frame();
else if (part == "section2d")     section2d();
else if (part == "tower2d")       tower2d();
else if (part == "lid")           lid_layout();
else if (part == "drill_wall")    drill_wall_template();
else if (part == "gas_pod")       gas_pod();
else if (part == "shield")        rad_shield();
else if (part == "container")     container();
else assert(false, str("unknown part: ", part));
