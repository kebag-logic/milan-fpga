#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reviewer probes: plant one Table 10-3 note 4/5 defect per copy, both profiles.

Each probe copies CMakeLists.txt, src and tests from the checkout into a new
scratch directory, requires exactly one occurrence of the target text, builds
the unit runner, runs it, and records which named tests failed.
Usage: probes.py <checkout> <scratch-dir> <cgreen-prefix> <out-json> [--jobs N]
"""
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAD = "src/core/mrp_mad.c"
NOTE4 = "pending_applicant_joinin_obeys_note_four"
LINK = "applicant_receive_conditions_follow_link_mode"
GUARD = "(ai->appl == MRP_APPL_STATE_VO || ai->appl == MRP_APPL_STATE_VP)"
RIN_ROW = "[MRP_EVENT_RIN] = {\n        _X, _X, _X,\n        _X, _S(TX_MSG_NONE, MRP_APPL_STATE_QA), _X,"
JOININ_ROW = "_S(TX_MSG_NONE, MRP_APPL_STATE_AO), _S(TX_MSG_NONE, MRP_APPL_STATE_AP), _X,"

# label, old, new, tests that must fail ([] = control / observation only)
PROBES = [
    ("control-unmodified", None, None, []),
    # The three upstream reversals that name these tests, replayed exactly.
    ("upstream-point-to-point-condition", "if ((p2p && ev == MRP_EVENT_RJOININ &&",
     "if ((false && p2p && ev == MRP_EVENT_RJOININ &&", [LINK, NOTE4]),
    ("upstream-pending-point-to-point-condition",
     "ai->appl == MRP_APPL_STATE_VO || ai->appl == MRP_APPL_STATE_VP",
     "ai->appl == MRP_APPL_STATE_VO", [NOTE4]),
    ("upstream-shared-in-condition", "(!p2p && ev == MRP_EVENT_RIN)",
     "(false && !p2p && ev == MRP_EVENT_RIN)", [LINK]),
    # Reviewer-designed independent faults.
    ("vo-dropped-from-note4-guard", GUARD, "(ai->appl == MRP_APPL_STATE_VP)", [LINK]),
    ("note4-applied-on-shared-links", "if ((p2p && ev == MRP_EVENT_RJOININ &&",
     "if ((ev == MRP_EVENT_RJOININ &&", [LINK, NOTE4]),
    ("vp-rjoinin-cell-ignored", JOININ_ROW,
     "_S(TX_MSG_NONE, MRP_APPL_STATE_AO), _X, _X,", [NOTE4]),
    ("vp-rjoinin-cell-to-qp", JOININ_ROW,
     "_S(TX_MSG_NONE, MRP_APPL_STATE_AO), _S(TX_MSG_NONE, MRP_APPL_STATE_QP), _X,", [NOTE4]),
    ("vo-rjoinin-cell-ignored", JOININ_ROW,
     "_X, _S(TX_MSG_NONE, MRP_APPL_STATE_AP), _X,", [LINK]),
    ("note5-inverted", "(!p2p && ev == MRP_EVENT_RIN)", "(p2p && ev == MRP_EVENT_RIN)", [LINK]),
    ("note5-applied-on-p2p-links", "(!p2p && ev == MRP_EVENT_RIN)", "(ev == MRP_EVENT_RIN)", [LINK]),
    ("aa-rin-cell-ignored", RIN_ROW,
     "[MRP_EVENT_RIN] = {\n        _X, _X, _X,\n        _X, _X, _X,", [LINK]),
    # Out-of-scope observation: note 4 over-applied to every state (AA rJoinIn! is unconditional).
    ("note4-guard-all-states", GUARD, "(true)", []),
]

FAIL_RE = re.compile(r"Failure: (?:[A-Za-z_]+ -> )*([A-Za-z0-9_]+)")


def run(cmd, cwd, env, log):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    log.write_text(r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


def probe(root, scratch, prefix, label, old, new, must_fail, profile):
    work = scratch / f"{label}-{profile}"
    if work.exists():
        shutil.rmtree(work)
    src = work / "source"
    src.mkdir(parents=True)
    shutil.copy2(root / "CMakeLists.txt", src / "CMakeLists.txt")
    for d in ("src", "tests"):
        shutil.copytree(root / d, src / d, ignore=shutil.ignore_patterns("__pycache__"))
    rec = {"label": label, "profile": profile, "must_fail": must_fail}
    if old is not None:
        path = src / MAD
        text = path.read_text()
        rec["occurrences"] = text.count(old)
        if rec["occurrences"] != 1:
            rec["verdict"] = "TARGET-NOT-UNIQUE"
            return rec
        path.write_text(text.replace(old, new))
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = str(prefix / "lib") + os.pathsep + env.get("LD_LIBRARY_PATH", "")
    build = work / "build"
    rec["configure_rc"], _ = run(["cmake", "-S", str(src), "-B", str(build), "-DCMAKE_BUILD_TYPE=Release",
                                  f"-DCMAKE_PREFIX_PATH={prefix}", f"-DLWSRP_MILAN={profile}"],
                                 src, env, work / "configure.log")
    rec["build_rc"], _ = run(["cmake", "--build", str(build), "--parallel", "2"], src, env, work / "build.log")
    if rec["build_rc"]:
        rec["verdict"] = "BUILD-FAILED"
        return rec
    rec["unit_rc"], out = run([str(build / "unit_tests")], src, env, work / "unit.log")
    summary = [l for l in out.splitlines() if "Completed" in l or "passes" in l]
    rec["summary"] = summary[-1].strip() if summary else ""
    rec["failed_tests"] = sorted(set(FAIL_RE.findall(out)))
    if label == "control-unmodified":
        rec["verdict"] = "PASS" if rec["unit_rc"] == 0 and not rec["failed_tests"] else "CONTROL-FAILED"
    elif not must_fail:
        rec["verdict"] = "OBSERVED-KILLED" if rec["unit_rc"] else "OBSERVED-SURVIVED"
    else:
        ok = rec["unit_rc"] != 0 and all(t in rec["failed_tests"] for t in must_fail)
        rec["verdict"] = "KILLED" if ok else "SURVIVED"
    return rec


def main():
    root, scratch, prefix, out = (Path(a).resolve() for a in sys.argv[1:5])
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
    scratch.mkdir(parents=True, exist_ok=True)
    tasks = [(p, prof) for p in PROBES for prof in ("OFF", "ON")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = [ex.submit(probe, root, scratch, prefix, *p, prof) for p, prof in tasks]
        results = [f.result() for f in futs]
    out.write_text(json.dumps(results, indent=2) + "\n")
    bad = 0
    for r in results:
        print(f"{r['verdict']:18} {r['profile']:3} {r['label']:42} failed={r.get('failed_tests')} {r.get('summary', '')}")
        bad += r["verdict"] in ("SURVIVED", "TARGET-NOT-UNIQUE", "BUILD-FAILED", "CONTROL-FAILED")
    print(f"probes={len(results)} bad={bad}")
    return int(bad != 0)


if __name__ == "__main__":
    raise SystemExit(main())
