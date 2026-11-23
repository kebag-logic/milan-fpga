#!/usr/bin/env python3
"""group_summary.py RESULTS_JSON... : per group, its work passes, those over THE SHARE, the longest, and each probe's
ms, verdict, taking pass cycles and pass modules (aecp_maps, aecp_commands). Read only."""
import json
import sys

for path in sys.argv[1:]:
    data = json.load(open(path))
    for g in data['results']:
        passes = g.get('passes', {})
        share, worst = passes.get('share', {}), passes.get('worst', {})
        print(f"{path}: {g['group']}: work passes {share.get('passes')}, over {share.get('over')}, longest "
              f"{worst.get('cycles')} (aecp_maps {worst.get('modules', {}).get('aecp_maps')})")
        for p in g.get('probes', []):
            mods = p.get('pass_modules', {})
            print(f"  {p['probe']:<45} {p.get('ms', 0):7.3f} ms  {p.get('status')}  within {p.get('within_budget')}  "
                  f"pass {p.get('pass_cycles')}  maps {mods.get('aecp_maps')} commands {mods.get('aecp_commands')}")
