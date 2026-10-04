#!/usr/bin/env python3
"""Reviewer feasibility check for finding R461-2-F1 (not a source fix; scratch only).

usage: r461_fixcheck.py --variant A|B --tree EXPORTED_HEAD_TREE --work SCRATCH_DIR
                        --out RECEIPT_DIR [--jobs N]

Adds, in a scratch copy only, one step before the round-2 repeat: an AVAILABLE
at the noted index + 1, which must give no event, and moves the repeat to that
index + 1 (it must still give the restart pair). Variant A sends the extra step
with grandmaster and domain matching; variant B with a foreign grandmaster, so a
noted value above the received one reads it as stale and foreign. Runs the
edited walk on the head RTL and under the probes of r461_probes.py (q0 to q3).
"""
import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
from pathlib import Path

import r461_probes as rp

SIM_ANCHOR = "  const uint32_t noted = 700 + 1;              // apply_disc's last + 1\n"
SIM_ADD = SIM_ANCHOR + (
    "  // reviewer probe: the noted index + 1 is fresh, so nothing above it was noted\n"
    "  const size_t e2 = evts.size();\n"
    "  load_remote(0, walk_talker(s), noted + 1, d->gm_id_i ^ GMX, DOM0, 0, 10, MSG_AVAIL);\n"
    "  CHECK(send_txn(adp_txn(MSG_AVAIL, walk_talker(s), 10, 0, now)),\n"
    "        \"%s: the AVAILABLE at index %u consumed\", tag, noted + 1);\n"
    "  idle(20);\n"
    "  CHECK(evts.size() == e2, \"%s: index %u noted, so index %u is fresh, got %zu events\",\n"
    "        tag, noted, noted + 1, evts.size() - e2);\n"
    "  const uint32_t again = noted + 1;\n")
# the repeat then uses the index just sent
SIM_REPEAT_OLD = ("  load_remote(0, walk_talker(s), noted, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);\n"
                  "  CHECK(send_txn(adp_txn(MSG_AVAIL, walk_talker(s), 10, 0, now)),\n"
                  "        \"%s: the AVAILABLE repeating index %u consumed\", tag, noted);\n")
SIM_REPEAT_NEW = ("  load_remote(0, walk_talker(s), again, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);\n"
                  "  CHECK(send_txn(adp_txn(MSG_AVAIL, walk_talker(s), 10, 0, now)),\n"
                  "        \"%s: the AVAILABLE repeating index %u consumed\", tag, again);\n")

RTL = {p[0]: p for p in rp.PROBES if p[1] == rp.ENG}


def set_variant(v):
    """Variant A: the step at noted + 1 matches grandmaster and domain (it then
    re-notes through the fresh arc). Variant B: it carries a foreign grandmaster,
    so an over-noted value reads it as stale and foreign (EVT_TK_DEPARTED)."""
    global SIM_ADD
    SIM_ADD = SIM_ADD.replace("GMX", "0ull" if v == "A" else "1ull")


def one(args, rtl_name):
    name = f"fix{args.variant}+{rtl_name}"
    work = Path(args.work) / name
    if work.exists():
        shutil.rmtree(work)
    src = Path(args.tree)
    shutil.copytree(src / "hdl", work / "hdl")
    for d in ("adp_engine", "common"):
        shutil.copytree(src / "tb" / d, work / "tb" / d,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    edits = [(rp.SIM, SIM_ANCHOR, SIM_ADD), (rp.SIM, SIM_REPEAT_OLD, SIM_REPEAT_NEW)]
    if rtl_name != "control":
        _, path, anchor, repl, _ = RTL[rtl_name]
        edits.append((path, anchor, repl))
    for path, anchor, repl in edits:
        f = work / path
        text = f.read_text()
        if text.count(anchor) != 1:
            return name, "ANCHOR", "", []
        f.write_text(text.replace(anchor, repl))
    log = Path(args.out) / f"fixcheck-{args.variant}-{rtl_name}.log"
    with log.open("w") as stream:
        rc = subprocess.run(["make", "-C", str(work / "tb" / "adp_engine"), "run"],
                            stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text()
    tally = next((ln for ln in text.splitlines() if re.match(r"\d+ checks:", ln)), "NO TALLY")
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL:")]
    return name, rc, tally, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--variant", choices=("A", "B"), default="A")
    args = ap.parse_args()
    set_variant(args.variant)
    Path(args.out).mkdir(parents=True, exist_ok=True)
    names = ["control", "q0-fresh-no-store", "q1-fresh-store-plus-one",
             "q2-fresh-store-max", "q3-fresh-store-gm-only"]
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(lambda n: one(args, n), names))
    for name, rc, tally, fails in results:
        arc4 = sum("arc DISCOVERED -> DISCOVERED (index > last)" in f for f in fails)
        print(f"{name}: rc={rc} {tally} | arc4-check-failed={arc4}")
        for f in fails:
            print(f"    {f}")


if __name__ == "__main__":
    main()
