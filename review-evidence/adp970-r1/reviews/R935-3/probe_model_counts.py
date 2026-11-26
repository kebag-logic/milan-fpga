"""In-memory probes of tb/verilator/ctrl_service_budget/model_counts.py; edits no file.

Usage: python3 -I probe_model_counts.py <repo root>
Each probe plants one count (or one header bound) in memory and reports whether model_counts.findings() sees it.
"""
import json
import sys
from dataclasses import replace
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import model_counts as mc  # noqa: E402
import scenario  # noqa: E402

counts = mc.bounds(mc.HEADER.read_text(encoding='utf-8'))
print('header bounds:', dict(sorted(counts.items())))
base = json.loads(mc.ORACLE.read_text(encoding='utf-8'))['point']


def plant(groups, path, value):
    n = 0
    for g in groups:
        new = []
        for pr in g.probes:
            if mc.path_of(pr) == path:
                pr = replace(pr, accesses=value)
                n += 1
            new.append(pr)
        g.probes = new
    return n


for ifs in (1, 2):
    p = scenario.Point(**dict(base, interfaces=ifs))
    # every ADP-channel probe in the full scenario, with its path and count
    allg = scenario.groups(p) if hasattr(scenario, 'groups') else None
    checked = {(g.name, pr.name) for g in mc.groups_at(p) for pr in g.probes}
    adp_all = set()
    src = [*mc.groups_at(p), *scenario.shutdown_groups(p)]
    for g in src:
        for pr in g.probes:
            if pr.channel == 'adp' if hasattr(pr, 'channel') else False:
                adp_all.add((mc.path_of(pr), pr.accesses))
    paths = sorted({(mc.path_of(pr), pr.accesses, mc.PATHS.get(mc.path_of(pr), '-'))
                    for g in src for pr in g.probes if mc.path_of(pr).startswith(('adp.', 'control.discover'))})
    print(f'--- {ifs} interface(s); ADP paths seen (path, count, checked-as):')
    for row in paths:
        print('   ', row)
    for path, value, label in (('adp.link_up', 11, 'LINK_UP stale 11 (planted)'),
                               ('adp.gm_change', 12, 'GM_CHANGE 12 (planted)'),
                               ('adp.discover', 30, 'DISCOVER 30 (planted)'),
                               ('adp.tmr_delay', 40, 'TMR_DELAY 40 (planted)'),
                               ('adp.tmr_advertise', 10, 'TMR_ADVERTISE 10 (planted)'),
                               ('adp.link_down', 8, 'LINK_DOWN 8 (planted)'),
                               ('adp.shutdown', 28, 'SHUTDOWN 28 (planted, shutdown_groups)')):
        gs = [*mc.groups_at(p), *scenario.shutdown_groups(p)]
        n = plant(gs, path, value)
        found = mc.findings(gs, counts)
        print(f'  {label}: planted in {n} probe(s), findings {len(found)} -> {"DETECTED" if found else "MISSED"}')
    # header-side: the adapter's LINK bound back at 11, real scenario counts
    c2 = dict(counts, LINK=11)
    found = mc.findings(mc.groups_at(p), c2)
    print(f'  header LINK=11 vs real scenario: findings {len(found)} -> {"DETECTED" if found else "MISSED"}')
    c3 = dict(counts, SHUTDOWN=30)
    found = mc.findings([*mc.groups_at(p), *scenario.shutdown_groups(p)], c3)
    print(f'  header SHUTDOWN=30 vs real scenario: findings {len(found)} -> {"DETECTED" if found else "MISSED"}')
