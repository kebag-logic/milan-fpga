#!/usr/bin/env python3
"""[R383] Run ONLY the builder-bank arm test_builder.test_clock_crossing_constraints
(the #607 arm) from a tree, as the bank's own interpreter would, and report rc,
the interpreter it discovered, and the shipping markers it printed.
Usage: bank_arm.py <tree>   (run with the bank's interpreter, e.g. /usr/bin/python3)"""
import contextlib, io, os, subprocess, sys, time
tree = os.path.abspath(sys.argv[1])
os.chdir(tree)
sys.path.insert(0, os.path.join(tree, "sw/builder"))
real_run = subprocess.run
seen = []
def spy(cmd, *a, **k):
    seen.append((list(map(str, cmd)), k.get("timeout")))
    k.setdefault("capture_output", True); k.setdefault("text", True)
    r = real_run(cmd, *a, **{x: y for x, y in k.items() if x != "check"})
    seen[-1] += (r.returncode, [l for l in r.stdout.splitlines() if l.startswith("[constraints] shipping ")])
    if k.get("check") and r.returncode:
        raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
    return r
import test_builder as tb
subprocess.run = spy
t0 = time.monotonic()
try:
    tb.test_clock_crossing_constraints(); rc = 0; err = ""
except BaseException as e:
    rc = 1; err = f"{type(e).__name__}: {str(e)[:200]}"
finally:
    subprocess.run = real_run
arm = [s for s in seen if any("test_clock_constraints.py" in c for c in s[0])]
print(f"arm rc={rc} {err} elapsed={time.monotonic()-t0:.1f}s")
for cmd, timeout, sub_rc, markers in arm:
    print(f"  child={os.path.basename(cmd[0])} script={cmd[1].replace(tree, '<TREE>')} timeout={timeout} rc={sub_rc} shipping_markers={len(markers)}")
    for m in markers: print("   ", m[:150])
print(f"skips={getattr(tb, 'SKIPS', getattr(tb, '_SKIPS', 'n/a'))}")
