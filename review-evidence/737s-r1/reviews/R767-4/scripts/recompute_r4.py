"""Recompute run 41705989293's elaborate components from saved jobs-API JSON (attempts 1 and 2)."""
import json, sys, datetime as d
t = lambda s: d.datetime.fromisoformat(s.replace('Z', '+00:00'))
dur = lambda x: (t(x['completed_at']) - t(x['started_at'])).total_seconds()
for path in sys.argv[1:]:
    jobs = {j['name']: j for j in json.load(open(path))['jobs']}
    print('==', path)
    for name in sorted(jobs):
        j = jobs[name]
        steps = {s['name']: dur(s) for s in j['steps'] if s['started_at'] and s['completed_at'] and s['conclusion'] == 'success'}
        gate = sum(v for k, v in steps.items() if k.startswith('Elaboration gates') or k.startswith('Standalone LiteX'))
        ver = steps.get('Build Verilator from source on cache miss', 0)
        line = f'{name}: span {dur(j):.0f}'
        if name.startswith('elaborate-gates'):
            line += f' gate {gate:.0f} verilator {ver:.0f} setup {dur(j) - gate - ver:.0f} checkout {steps.get("Run actions/checkout@v4", 0):.0f}'
            line += f' litex-install {steps.get("Install LiteX at the pinned revisions", 0):.0f} vexii {steps.get("Place the VexiiRiscv source at the revision LiteX pins", 0):.0f}'
        elif 'Run actions/checkout@v4' in steps:
            line += f' checkout {steps["Run actions/checkout@v4"]:.0f}'
        print(line)
