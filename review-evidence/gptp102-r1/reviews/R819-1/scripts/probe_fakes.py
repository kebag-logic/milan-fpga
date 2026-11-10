#!/usr/bin/env python3
"""Power of tb/mutation_jobs_test.py against planted fake drivers.

usage: probe_fakes.py <tree> <workdir>

Each fake driver defines MUTATIONS and takes --jobs, like the real arm, and
plants one way the --jobs 1 and --jobs 4 runs can differ (or agree while
both are wrong). Only `good` may pass. Prints one line per fake and a tally.
"""
import subprocess
import sys
from pathlib import Path

tree, work = Path(sys.argv[1]), Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)
test = tree / "tb/mutation_jobs_test.py"

COMMON = '''
import sys
MUTATIONS = [("m1",), ("m2",), ("m3",)]
def body(jobs):
    lines = ["[PASS] control"] + [f"[PASS] mutant caught: {m[0]}" for m in MUTATIONS]
    tally = f"\\n{len(lines)} checks: {len(lines)} PASS, 0 FAIL"
    rc = 0
    err = ""
    %s
    print("\\n".join(lines)); print(tally); sys.stderr.write(err); return rc
if __name__ == "__main__":
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1])
    sys.exit(body(jobs))
'''
FAKES = {
    "good": ("pass", 0),
    "order": ("if jobs > 1: lines = lines[:1] + lines[1:][::-1]", 1),
    "abort_alike": ("lines = lines[:1]; tally = ''; rc = 1", 1),
    "stderr_diff": ("err = 'warn\\n' if jobs > 1 else ''", 1),
    "rc_diff": ("rc = 1 if jobs > 1 else 0", 1),
    "tally_wrong": ("tally = '\\n3 checks: 3 PASS, 0 FAIL'", 1),
    "extra_verdict": ("lines = lines + ['[FAIL] mutant SURVIVED: m3']", 1),
    "named_line_diff": ("if jobs > 1: lines.insert(2, 'FAIL extra named line')", 1),
}
ok_all = 0
for name, (plant, want_rc) in FAKES.items():
    d = work / name
    d.mkdir(exist_ok=True)
    drv = d / "mutants.py"
    drv.write_text(COMMON % plant)
    r = subprocess.run([sys.executable, str(test), str(drv)],
                       capture_output=True, text=True)
    fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL ")]
    good = r.returncode == want_rc
    ok_all += good
    print(f"{'OK ' if good else 'BAD'} fake {name}: rc {r.returncode} "
          f"(want {want_rc}); failed checks: {fails}")
print(f"{len(FAKES)} fakes: {ok_all} as expected, {len(FAKES) - ok_all} not")
sys.exit(0 if ok_all == len(FAKES) else 1)
