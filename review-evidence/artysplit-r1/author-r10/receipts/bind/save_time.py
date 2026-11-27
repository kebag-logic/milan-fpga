"""The Arty's whole save as the census models it: each save of each bind group, from the seal's first stretch to
durable (bind_save.phase_of's edges), with the part's modelled erase and page times."""
import glob, json, math, sys
from pathlib import Path
sys.path.insert(0, 'tb/verilator/ctrl_service_budget')
import bind_save, grade, run, save_burst, save_window, scenario
bind_save.FLIGHT_MS.setdefault('arty-1x1', 10**9); bind_save.BURST_SAVES.setdefault('arty-1x1', 10**6)
D = Path('$VALIDATION_STORAGE/r9/final-census/none')
spec = json.loads((D / 'build.json').read_text())
groups = {g.name: g for g in run.all_groups(scenario.point('arty-1x1', spec), spec) if g.name.startswith('save-bind')}
out = []
for name, g in sorted(groups.items()):
    image = g.save['bind']['image']
    log = grade.parse((D / 'results' / (name + '.log')).read_text(errors='replace'), spec['sys_hz'], spec['cpu_hz'])
    stretches = math.ceil((image - save_window.TRAILER) / save_window.PAGE)
    prev = 0
    for s in save_burst.saves(log, image):
        seals = sorted(int(t[1]) for t in log.traced if t[0] == 'CALL' and t[3] == bind_save.SEAL_CALL and prev < int(t[1]) < s['erase'])
        if s['durable'] is not None and seals:
            start = seals[-stretches:][0]
            out.append(dict(group=name, image=image, seal_start=start, erase=s['erase'], durable=s['durable'],
                            save_ms=(s['durable'] - start) * 1000 / spec['sys_hz']))
        prev = s['erase']
json.dump(out, open('$VALIDATION_STORAGE/r10/save-times.json', 'w'), indent=1)
ms = [r['save_ms'] for r in out]
print(len(out), 'saves; image', sorted({r['image'] for r in out}), 'pages', math.ceil(out[0]['image'] / save_window.PAGE))
print('whole save ms: min %.3f max %.3f' % (min(ms), max(ms)))
