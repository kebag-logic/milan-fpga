#!/usr/bin/env python3
"""srpcmp_arm_probe.py - the firmware gate's srpcmp arm against doctored comparator reports.

Runs ctrl_arms.arm_srpcmp() once on the tracked comparator, then again with
ctrl_arms.run replaced so the comparator's real --self-test report reaches the
arm edited: one plant dropped, all but one dropped, a plant renamed, a control
dropped, a control failed, a plant added, and an empty plant list. Expected:
the tracked report and the added plant pass (rc 0); every other edit fails (rc 1).

Usage: srpcmp_arm_probe.py <checkout>
"""
import copy
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
    import ctrl_arms

    real = ctrl_arms.run
    base = real([sys.executable, "-I", "-B", str(ctrl_arms.SRP_COMPARE), "--self-test"])
    report = json.loads(base.stdout)

    def edited(fn):
        r = copy.deepcopy(report)
        fn(r["controls"])
        return subprocess.CompletedProcess(base.args, 0, json.dumps(r), "")

    def drop_first(c): c["plants"].pop(0)
    def keep_one(c): del c["plants"][1:]
    def rename(c): c["plants"][0]["plant"] = c["plants"][0]["plant"] + "-renamed"
    def drop_control(c): c.pop(sorted(k for k in c if k != "plants")[0])
    def fail_control(c): c[sorted(k for k in c if k != "plants")[0]] = "FAIL"
    def add_plant(c): c["plants"].append({**c["plants"][0], "plant": "an-added-plant"})
    def no_plants(c): c["plants"] = []

    cases = [("tracked report", None, 0), ("one plant dropped", drop_first, 1), ("all plants but one dropped", keep_one, 1),
             ("a plant renamed", rename, 1), ("a control dropped", drop_control, 1), ("a control failed", fail_control, 1),
             ("a plant added", add_plant, 0), ("no plants", no_plants, 1)]
    bad = 0
    for what, fn, want in cases:
        ctrl_arms.run = real if fn is None else (lambda argv, cwd=None, fn=fn: edited(fn))
        out = ctrl_arms.arm_srpcmp()
        ok = out.rc == want
        bad += not ok
        last = out.log.strip().splitlines()[-1] if out.log.strip() else ""
        print(f"[{'ok' if ok else 'BAD'}] {what}: rc {out.rc} (want {want}); {last[:150]}")
    print(f"srpcmp arm probe: {len(cases) - bad} of {len(cases)} as expected")
    return int(bad != 0)


if __name__ == "__main__":
    sys.exit(main())
