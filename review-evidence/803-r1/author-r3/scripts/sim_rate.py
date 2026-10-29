"""sim_rate.py <out.json> <seconds> <label>=<cpu>:<run-dir>:<binary> ...: run each physical gPTP simulation binary at
once, each pinned to its own CPU (taskset) with line-buffered output (stdbuf -oL), for the same wall-clock window;
timestamp every `PROGRESS simulated_seconds=` line and report, per binary, the wall seconds it took over the
simulated interval both reached, so two heads' per-cycle cost is compared under one host load. The runs are
stopped by SIGTERM at the window's end; nothing they write is read except their stdout."""
import json
import re
import subprocess
import sys
import threading
import time

out, window = sys.argv[1], float(sys.argv[2])
specs = []
for arg in sys.argv[3:]:
    label, rest = arg.split('=', 1)
    cpu, run_dir, binary = rest.split(':', 2)
    specs.append((label, cpu, run_dir, binary))
marks = {label: [] for label, *_ in specs}
pat = re.compile(r'^PROGRESS simulated_seconds=([0-9.]+)')


def reader(label, proc, t0):
    for line in proc.stdout:
        m = pat.match(line)
        if m:
            marks[label].append((round(time.monotonic() - t0, 3), float(m.group(1))))


procs = []
t0 = time.monotonic()
for label, cpu, run_dir, binary in specs:
    p = subprocess.Popen(['taskset', '-c', cpu, 'stdbuf', '-oL', binary], cwd=run_dir, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, errors='replace')
    th = threading.Thread(target=reader, args=(label, p, t0), daemon=True)
    th.start()
    procs.append((p, th))
time.sleep(window)
for p, _ in procs:
    p.terminate()
for p, th in procs:
    p.wait(timeout=60)
    th.join(timeout=10)
common = min(m[-1][1] for m in marks.values() if m)
first = 0.25
result = {'window_s': window, 'interval_sim_s': [first, common], 'runs': {}}
for label, *_ in specs:
    pts = dict((s, t) for t, s in marks[label])
    wall = pts[common] - pts[first]
    result['runs'][label] = {'marks': len(marks[label]), 'last_sim_s': marks[label][-1][1],
                             'wall_s_over_interval': round(wall, 3),
                             'wall_s_per_sim_s': round(wall / (common - first), 3)}
labels = [s[0] for s in specs]
if len(labels) == 2:
    a, b = (result['runs'][x]['wall_s_per_sim_s'] for x in labels)
    result[f'{labels[1]}_over_{labels[0]}'] = round(b / a, 4)
open(out, 'w').write(json.dumps(result, indent=1) + '\n')
print(json.dumps(result, indent=1))
