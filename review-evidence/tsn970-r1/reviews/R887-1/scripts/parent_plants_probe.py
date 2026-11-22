#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: plant each #970 defect of the parent's adp_first_mutants.py (and gm-change-ignored from
ctrl_mutants.py) into a copy of the pinned stack, run the parent's adp and walk arms, and require every named
kill's words on a failing line of its arm. Usage: parent_plants_probe.py PARENT_ROOT STACK_HEAD_DIR OUT JOBS"""
import sys, json, shutil, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root, head, out, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import adp_first_mutants, ctrl_mutants
plants = list(adp_first_mutants.MUTANTS) + [m for m in ctrl_mutants.MUTANTS if m.name in ("gm-change-ignored",)]
probe = Path(__file__).with_name("parent_adp_probe.py")
def one(m):
    d = out / m.name; shutil.rmtree(d, ignore_errors=True); shutil.copytree(head, d / "stack")
    f = d / "stack" / m.path.removeprefix("tsn-c-stack/"); s = f.read_text()
    if s.count(m.old) != 1:
        return {"plant": m.name, "verdict": "NOT-APPLICABLE", "count": s.count(m.old)}
    f.write_text(s.replace(m.old, m.new))
    arms = sorted({k[0] for k in m.kills()})
    r = subprocess.run([sys.executable, str(probe), str(root), m.name, str(d / "stack"), str(d / "build"), ",".join(arms)],
                       capture_output=True, text=True)
    try:
        res = json.loads(r.stdout)
    except ValueError:
        return {"plant": m.name, "verdict": "ERROR", "stderr": r.stderr[-800:]}
    kills = []
    for arm, test, words in m.kills():
        lines = res.get(arm, {}).get("fail_lines", [])
        kills.append({"arm": arm, "test": test, "words": words,
                      "seen": any(test.split("/")[-1].split(".")[-1] in l and words in l for l in lines) or
                              any(words in l for l in lines if l.startswith("[FAIL]"))})
    return {"plant": m.name, "verdict": "CAUGHT" if all(k["seen"] for k in kills) else "ESCAPED", "kills": kills,
            "arm_rc": {a: res.get(a, {}).get("rc") for a in arms}}
with ThreadPoolExecutor(jobs) as ex:
    results = list(ex.map(one, plants))
print(json.dumps(results, indent=1))
print("SUMMARY", {v: sum(r["verdict"] == v for r in results) for v in ("CAUGHT", "ESCAPED", "ERROR", "NOT-APPLICABLE")})
