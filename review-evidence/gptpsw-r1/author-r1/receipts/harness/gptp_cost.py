#!/usr/bin/env python3
"""gptp_cost.py LOG...: the gPTP modules' CPU cycles in a harness run, from its PASS lines (the work passes) and its
MODULES line (every cycle of the run): per work pass, their distribution, the run's span after link-up, the load."""
import re, sys
for path in sys.argv[1:]:
    text = open(path).read()
    passes = []
    for line in text.splitlines():
        if line.startswith('PASS '):
            f = line.split()
            start, cyc = int(f[2]), int(f[4])
            m = re.search(r'mods=(\S+)', line)
            mods = dict((k, int(v)) for k, v in (x.split(':') for x in m.group(1).split(',') if x)) if m else {}
            g = mods.get('gptp', 0) + mods.get('gptp_mbx', 0)
            passes.append((start, cyc, g, mods.get('gptp', 0), mods.get('gptp_mbx', 0)))
    link = next((int(l.split()[1]) for l in text.splitlines() if l.startswith('LINK ')), 0)
    summ = next(l for l in text.splitlines() if l.startswith('SUMMARY'))
    sys_end = int(re.search(r'sys=(\d+)', summ).group(1))
    mods = next(l for l in text.splitlines() if l.startswith('MODULES'))
    tot = dict((k, int(v)) for k, v in (x.split(':') for x in mods.split()[1:]))
    gtot = tot.get('gptp', 0) + tot.get('gptp_mbx', 0)
    span = sys_end - link
    work = [p for p in passes if p[0] >= link and p[2] > 0]
    steady = [p for p in work if p[0] >= link + 100_000_000]   # after the first second (asCapable, the first pair)
    def pct(v, q): v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))] if v else 0
    print(f'== {path.split("/")[-1]}')
    print(f'run: link up at sys {link}, end at {sys_end}: {span / 1e8:.3f} s of CPU time after link-up at 100 MHz')
    print(f'gPTP cycles in the run: gptp {tot.get("gptp", 0)}, gptp_mbx {tot.get("gptp_mbx", 0)}, together {gtot}: '
          f'{100 * gtot / span:.3f} % of the CPU after link-up (an upper bound: boot passes before link-up included)')
    print(f'work passes with gPTP work after link-up: {len(work)}; its cycles a pass: max {max((p[2] for p in work), default=0)}, '
          f'p95 {pct([p[2] for p in work], .95)}, median {pct([p[2] for p in work], .5)}')
    print(f'  after the first second: {len(steady)} passes, max {max((p[2] for p in steady), default=0)}, '
          f'median {pct([p[2] for p in steady], .5)}; the longest such pass, all modules: {max((p[1] for p in steady), default=0)}')
    top = sorted(work, key=lambda p: -p[2])[:5]
    print('  the five dearest: ' + ', '.join(f'sys {p[0]}: gptp {p[3]} + gptp_mbx {p[4]} of {p[1]}' for p in top))

# ---- the steady state: from a second after link-up to the run's end ----
for path in sys.argv[1:]:
    text = open(path).read()
    lines = text.splitlines()
    link = next((int(l.split()[1]) for l in lines if l.startswith('LINK ')), 0)
    sys_end = int(re.search(r'sys=(\d+)', next(l for l in lines if l.startswith('SUMMARY'))).group(1))
    t0 = link + 100_000_000
    work_g = work_n = 0
    for line in lines:
        if line.startswith('PASS '):
            f = line.split()
            if int(f[2]) < t0:
                continue
            m = re.search(r'mods=(\S+)', line)
            mods = dict((k, int(v)) for k, v in (x.split(':') for x in m.group(1).split(',') if x)) if m else {}
            work_g += mods.get('gptp', 0) + mods.get('gptp_mbx', 0)
            work_n += 1
    span = sys_end - t0
    print(f'== {path.split("/")[-1]} steady state, {span / 1e8:.3f} s from a second after link-up: work passes {work_n}, '
          f'their gPTP cycles {work_g}: {100 * work_g / span:.3f} % of the CPU, {work_g / (span / 1e8):.0f} cycles a second')
