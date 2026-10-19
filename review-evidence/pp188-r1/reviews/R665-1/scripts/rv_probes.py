#!/usr/bin/env python3
"""Run the reviewer RV section (rv_section.cpp) of tb/srp_stream_fsms on the
head and on each surviving RTL probe of probes.py.

Usage: rv_probes.py HEAD_TREE OUT_DIR [--jobs N]

Each arm copies hdl/ and tb/ of HEAD_TREE to OUT_DIR/work/<arm>, inserts the RV
section into tb/srp_stream_fsms/sim_main.cpp (exact anchors, each once), plants
the arm's RTL edit if any, and runs `make run` (the suite, not the walk arms).
The head arm must pass every RV check; a probe arm shows which RV checks fail.
"""
import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probes  # noqa: E402

SIM = "tb/srp_stream_fsms/sim_main.cpp"
DECL = "  void settle_keeps_the_owed_listener_leave();\n"
CALL = "  settle_keeps_the_owed_listener_leave();\n\n  printf("
DEF_AT = "// SC1: independently compose Table 10-4's LV/leavetimer row with each\n"
ARMS = ["head", "U1-lo-not-owed", "U2-park-retires-on-txla", "U3-parked-applies-rx",
        "U5-csid-ignores-park", "U6-retire-keeps-fourpack", "U7-same-ignores-rec-valid"]
TALLY = re.compile(r"^\d+ checks: \d+ PASS, \d+ FAIL$", re.M)


def arm(name, head, out):
    work = out / "work" / name
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copytree(head / "hdl", work / "hdl")
    shutil.copytree(head / "tb", work / "tb", ignore=shutil.ignore_patterns("obj*", "__pycache__"))
    edits = [(SIM, DECL, DECL + "  void reviewer_rv_probes();\n"),
             (SIM, CALL, "  settle_keeps_the_owed_listener_leave();\n  reviewer_rv_probes();\n\n  printf("),
             (SIM, DEF_AT, (HERE / "rv_section.cpp").read_text() + DEF_AT)]
    if name != "head":
        edits += probes.PROBES[name][1]
    for rel, old, new in edits:
        p = work / rel
        t = p.read_text()
        if t.count(old) != 1:
            return {"arm": name, "verdict": "INCONCLUSIVE", "reason": f"{rel}: {t.count(old)} matches of {old[:40]!r}"}
        p.write_text(t.replace(old, new, 1))
    log = out / f"rv-{name}.log"
    with log.open("w") as f:
        rc = subprocess.run(["make", "run", "VERILATOR=" + os.environ.get("VERILATOR", "verilator")],
                            cwd=work / "tb/srp_stream_fsms", stdout=f, stderr=subprocess.STDOUT).returncode
    text = log.read_text(errors="replace")
    fails = [l for l in text.splitlines() if l.startswith("FAIL")]
    rv_fails = [l for l in fails if l.startswith("FAIL: RV")]
    other = [l for l in fails if not l.startswith("FAIL: RV")]
    shutil.rmtree(work)
    return {"arm": name, "rc": rc, "tally": TALLY.findall(text)[-1:], "rv_fail_lines": rv_fails,
            "other_fail_lines": other[:5], "n_other_fail": len(other)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda n: arm(n, a.head, a.out), ARMS))
    for r in res:
        print(json.dumps(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
