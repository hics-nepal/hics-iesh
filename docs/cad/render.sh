#!/bin/bash
# Regenerate every roofbox view + template and run the numeric checks.
#   docs/cad/render.sh            (from anywhere; ~2 min)
# 3D views are OpenSCAD previews (fast, coloured). Sections are 2D and exact.
set -e
cd "$(dirname "$0")"
mkdir -p renders templates
r() {  # name part camera projection
  timeout 240 openscad -o "renders/$1.png" -D "part=\"$2\"" --imgsize=1500,1150 --camera="$3" \
           --projection="$4" --colorscheme=Tomorrow roofbox.scad 2>&1 | grep -iE "error|warning|assert" || true
  echo "renders/$1.png"
}
svg() {  # name part  -> templates/*.svg (mm, 1:1) and a PNG preview in renders/
  timeout 240 openscad -o "templates/roofbox_$1.svg" -D "part=\"$2\"" roofbox.scad 2>&1 | grep -iE "error|warning|assert" || true
  convert -density 150 -background white "templates/roofbox_$1.svg" "renders/$1.png"
  echo "templates/roofbox_$1.svg  renders/$1.png"
}
r site       site       0,0,650,68,0,32,4300   p
r service    service    0,0,120,62,0,32,800    p
r exploded   exploded   0,0,30,55,0,35,720     p
r plan       plan       0,0,0,0,0,0,420        o
r mast       mast       0,0,1200,80,0,25,1400  p
r cam_tower  cam_tower  0,0,-20,62,0,210,190   p
r gas_pod    gas_pod    0,0,20,60,0,30,260     p
r shield     shield     0,0,30,60,0,30,320     p
svg section2d  section2d
svg tower2d    tower2d
svg lid        lid
svg drill_wall drill_wall
rm -f renders/section.png renders/cam_tower_section.png templates/roofbox_drill.svg
python3 roofbox_check.py
