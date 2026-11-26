"""Every LINK_UP / ADP probe count the full scenario emits at 1x1/1if and 8x8/1if; edits no file.
Usage: python3 -I probe_emitted_counts.py <repo root>"""
import json, sys
from collections import Counter
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import scenario, model_counts as mc
base = json.loads(mc.ORACLE.read_text(encoding='utf-8'))['point']
for label, shape, srcs in (('1x1-1if', 'endstation_ax7101_1x1_tdm8', base['sources']), ('8x8-1if', 'endstation_ax7101_8x8', 8)):
    p = scenario.Point(**dict(base, shape=shape, interfaces=1, sources=srcs, sinks=srcs))
    for build, ctor in (('build-free constructors', lambda: [*scenario.acmp_groups(p), *scenario.adp_groups(p),
                              *scenario.maap_groups(p), *scenario.srp_groups(p), *scenario.backlog_groups(p),
                              *scenario.control_groups(p), *scenario.fixture_groups(p)]),
                        ('shutdown-entry', lambda: scenario.all_groups(p, {'variant': 'shutdown-entry'}))):
        try:
            gs = ctor()
        except Exception as e:  # report and continue
            print(label, build, 'error:', type(e).__name__, e); continue
        c = Counter((mc.path_of(pr), pr.accesses) for g in gs for pr in g.probes if pr.family == 'adp')
        print(label, build, sorted(c.items()))
        print('   checker findings over all_groups:', len(mc.findings(gs, mc.bounds(mc.HEADER.read_text(encoding="utf-8")))))
