#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R299-2: run the reviewer's new admission mutants against the AUTHOR's
suites (tb/srp_admission N=2 and N=8, tb/srp_top), each in a private copy of
the exact-head tree. KILLED = non-zero exit with a 'checks:' tally.
Usage: mutants_r2_suites.py <head-tree> <work> <out-dir> [jobs]
"""
import concurrent.futures as cf
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mutants_r2 import MUTANTS as ALL  # noqa: E402

ADM = "hdl/srp/KL_srp_admission.sv"
PICK = ["control", "D-last-visit-ignored", "E-pend-not-accumulated", "I-aggregate-not-frozen"]
BENCHES = {
    "adm2": ("tb/srp_admission", ["make", "run", "N=2"]),
    "adm8": ("tb/srp_admission", ["make", "run", "N=8"]),
    "srp_top": ("tb/srp_top", ["make", "run"]),
}


def run(name, bench):
    tree = WORK / f"{name}-{bench}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(HEAD / "hdl", tree / "hdl")
    for sub in ("tb/common", "tb/srp_admission", "tb/srp_top"):
        shutil.copytree(HEAD / sub, tree / sub, ignore=shutil.ignore_patterns("obj_*"))
    for old, new, count in ALL[name]:
        p = tree / ADM
        s = p.read_text()
        if s.count(old) != count:
            raise RuntimeError(f"{name}: anchor count {s.count(old)} != {count}")
        p.write_text(s.replace(old, new))
    sub, cmd = BENCHES[bench]
    log = OUT / f"{name}-{bench}.log"
    with log.open("w") as f:
        r = subprocess.run(cmd, cwd=tree / sub, stdout=f, stderr=subprocess.STDOUT,
                           timeout=3600, check=False)
    text = log.read_text()
    tally = [l for l in text.splitlines() if "checks:" in l]
    names = sorted({l.split(" N=")[0] for l in text.splitlines() if l.startswith("FAIL: ")})
    if not tally:
        verdict = "BUILD-FAIL"
    elif name == "control":
        verdict = "PASS" if r.returncode == 0 else "CONTROL-FAIL"
    else:
        verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    shutil.rmtree(tree)
    return name, bench, r.returncode, verdict, tally[-1] if tally else "", names[:6]


if __name__ == "__main__":
    HEAD = Path(sys.argv[1]).resolve()
    WORK, OUT = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = [(m, b) for m in PICK for b in BENCHES]
    with cf.ThreadPoolExecutor(max_workers=JOBS) as ex:
        res = list(ex.map(lambda t: run(*t), tasks))
    for name, bench, rc, verdict, tally, names in sorted(res):
        print(f"{name:24s} {bench:8s} rc={rc:<3d} {verdict:10s} {tally} | {'; '.join(names)}")
