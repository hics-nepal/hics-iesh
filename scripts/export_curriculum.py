#!/usr/bin/env python3
"""Export the curriculum package to curriculum/curriculum.json.

The curriculum/ package is the single source of truth for learning content
(see the website repo: docs/CURRICULUM_PIPELINE.md). This script produces the
committed JSON artefact that the website's `manage.py sync_curriculum` imports
and from which printable PDFs are generated. The device portal keeps importing
the Python modules directly.

Run from the repo root after any curriculum edit, bump CURRICULUM_VERSION in
curriculum/__init__.py, and commit the regenerated JSON:

    python3 scripts/export_curriculum.py

Equipment tiers: an activity may declare `equipment: 'none' | 'common' |
'iesh'` in its source dict ('none' = paper/observation only, 'common' =
everyday materials, 'iesh' = needs live station data). Activities without the
field are exported as 'iesh' when they use live sensors — which today is all
of them. Authoring non-station variants is pending content work, not an
exporter concern.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from curriculum import CURRICULUM_VERSION, all_modules  # noqa: E402

OUTPUT = REPO_ROOT / 'curriculum' / 'curriculum.json'

EQUIPMENT_TIERS = ('none', 'common', 'iesh')


def equipment_tier(activity):
    explicit = activity.get('equipment')
    if explicit:
        if explicit not in EQUIPMENT_TIERS:
            raise ValueError(
                f"{activity['id']}: equipment must be one of {EQUIPMENT_TIERS}, "
                f"got {explicit!r}"
            )
        return explicit
    if activity.get('live_sensors'):
        return 'iesh'
    return 'common' if activity.get('materials') else 'none'


def export():
    modules = []
    activity_count = 0
    for module in all_modules():
        out = dict(module)
        out['activities'] = []
        for activity in module['activities']:
            a = dict(activity)
            a['equipment'] = equipment_tier(activity)
            out['activities'].append(a)
            activity_count += 1
        modules.append(out)

    payload = {
        'schema': 'hics-curriculum/1',
        'version': CURRICULUM_VERSION,
        'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'source': 'https://github.com/hics-nepal/hics-iesh',
        'locales': ['en'],  # 'ne' joins once title_ne/description_ne land in source
        'module_count': len(modules),
        'activity_count': activity_count,
        'modules': modules,
    }

    OUTPUT.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}: "
          f"v{CURRICULUM_VERSION}, {len(modules)} modules, {activity_count} activities")


if __name__ == '__main__':
    export()
