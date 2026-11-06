#!/usr/bin/env python3
"""Reviewer fault probes on a scratch copy of the hook harness (never the checkout).

Each probe replaces one exact text (found exactly once) in a copy of tb/verilator/ctrl_service_hooks, runs the
harness's portable self-test in that copy, and records whether the self-test fails (CAUGHT) or passes
(ESCAPED). The copy is restored from the pristine archive between probes.

Usage: python3 -I probes.py <pristine tree> <work tree> <out dir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

pristine, work, out = (Path(a).resolve() for a in sys.argv[1:4])
H = 'tb/verilator/ctrl_service_hooks'
PROBES = [
    ('P1 summary picks the best path, not the worst', 'run.py',
     "top = max(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))",
     "top = min(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))"),
    ('P2 H-DISC counts a PROBE_TX on any interface', 'hooks.py',
     "if ch == CH['acmp'] and inter == i and c1 < c < until", "if ch == CH['acmp'] and c1 < c < until"),
    ('P3 H-SRP accepts an SR_DOMAIN publication made before the Domain record', 'hooks.py',
     "if w == word and c > rx and adopted(v)), None)", "if w == word and adopted(v)), None)"),
    ('P4 the loaded fan-out group is dropped', 'hooks.py',
     "out += [loaded_notify_group(p), order_adp_group(p)", "out += [order_adp_group(p)"),
    ('P5 a plant is caught by any finding of its kind (LATE/ORDER), not its own hook', 'run.py',
     "caught = [x for x in graded['findings'] if x.startswith(words + ':')]",
     "caught = [x for x in graded['findings'] if x.startswith(words.split()[0])]"),
    ('P6 the composed window opens after burst x refill_ms, without the extra period', 'hooks.py',
     'return max((ch.burst + 1) * ch.refill_ms', 'return max(ch.burst * ch.refill_ms'),
    ('P7 counter spacing of exactly 1 s is reported', 'hooks.py',
     'if b - a < COUNTERS_SPACING_MS * BUS_MS:', 'if b - a <= COUNTERS_SPACING_MS * BUS_MS:'),
    ('P8 every bound relaxed by 1 ms', 'run.py',
     "within=not unbounded and row['ms'] <= bound,", "within=not unbounded and row['ms'] <= bound + 1.0,"),
    ('P9 H-MAAP: a gate publication counts for every later report', 'hooks.py',
     "                                f'{since}')\n        since = c\n", "                                f'{since}')\n"),
    ('P10 the late groups are counted as under the composed load', 'run.py',
     'loaded=group in LOADED,', "loaded=group in LOADED or group.startswith('hooks-'),"),
    ('P11 a run with a check that applied to nothing exits 1 (control: changes no rule the self-test reads)',
     'run.py', "    if graded['refusals'] or orders or", "    if graded['refusals'] or orders or unapplied or"),
    ('P12 the ALL push is graded per descriptor (only its first descriptor ends it)', 'hooks.py',
     "'pad:CTR:0', [notify_end(k, n) for k, n in others], recipients=everyone, path='counters.all'),",
     "'pad:CTR:0', [notify_end(k, n) for k, n in others][:1], recipients=everyone, path='counters.all'),"),
]


def restore() -> None:
    shutil.rmtree(work / H, ignore_errors=True)
    shutil.copytree(pristine / H, work / H)


def selftest() -> tuple[int, str]:
    r = subprocess.run([sys.executable, '-B', f'{H}/run.py', '--self-test'], cwd=work, capture_output=True,
                       text=True, timeout=1200)
    return r.returncode, r.stdout + r.stderr


out.mkdir(parents=True, exist_ok=True)
restore()
rc, text = selftest()
(out / 'probe_control.log').write_text(text + f'rc={rc}\n')
print(f'control (unmodified copy): rc={rc}; {text.strip().splitlines()[-1]}')
for name, path, old, new in PROBES:
    restore()
    target = work / H / path
    src = target.read_text()
    if src.count(old) != 1:
        print(f'{name}: ANCHOR {src.count(old)} times, not run')
        continue
    target.write_text(src.replace(old, new))
    rc, text = selftest()
    tag = name.split()[0]
    (out / f'probe_{tag}.log').write_text(text + f'rc={rc}\n')
    fails = [ln for ln in text.splitlines() if ln.startswith('FAIL ') or 'ESCAPED' in ln]
    print(f"{name}: {'CAUGHT' if rc else 'ESCAPED'} (rc={rc}){'; ' + fails[0][:150] if fails else ''}")
restore()
print('work copy restored to the pristine harness')
