#!/usr/bin/env python3
"""Drive the committed mutants.run_units() with fake units whose durations are
random (so they finish in a random order), on 1, 3, 4 and 8 workers, with the
datapath flag set on a random subset; the printed lines and the returned
verdict list must be identical in every run and in list order. One unit raises,
in a final run, to show an exception is not swallowed as a pass.
Usage: order_probe.py <capture_coherence dir>"""
import contextlib, importlib.util, io, random, sys, time
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("m", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = ["mutants.py"]; spec.loader.exec_module(m)

def unit(i, dur, ok):
    def run():
        time.sleep(dur)
        return [(ok, [f"[{'PASS' if ok else 'FAIL'}] unit {i}"])] + ([(True, [f"[PASS] unit {i} second check"])] if i % 5 == 0 else [])
    return run

outs = set(); verdict_lists = set()
for trial, jobs in enumerate([1, 3, 4, 8, 4, 8]):
    rnd = random.Random(trial)
    units = [m.Unit(unit(i, rnd.uniform(0, 0.05), i % 7 != 3), rnd.random() < 0.3) for i in range(29)]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        v = m.run_units(units, jobs)
    body = [ln for ln in buf.getvalue().splitlines() if not ln.startswith("[i]")]
    outs.add(tuple(body)); verdict_lists.add(tuple(v))
    print(f"jobs={jobs}: {len(body)} lines, {sum(v)}/{len(v)} pass, first={body[0]!r} last={body[-1]!r}")
expected = []
for i in range(29):
    expected.append(f"[{'PASS' if i % 7 != 3 else 'FAIL'}] unit {i}")
    if i % 5 == 0: expected.append(f"[PASS] unit {i} second check")
print("identical output across runs:", len(outs) == 1, "| identical verdicts:", len(verdict_lists) == 1,
      "| in list order:", list(next(iter(outs))) == expected)
def boom(): raise RuntimeError("planted unit exception")
try:
    with contextlib.redirect_stdout(io.StringIO()):
        m.run_units([m.Unit(unit(0, 0, True), False), m.Unit(boom, False)], 2)
    print("exception probe: run_units returned normally (BAD)")
except RuntimeError as e:
    print("exception probe: run_units raised:", e, "(main() would exit non-zero with a traceback)")
