#!/usr/bin/env python3
"""Reviewer fault probes of the ADP fresh-arc noted index (round R461-2).

usage: r461_probes.py --tree EXPORTED_HEAD_TREE --work SCRATCH_DIR --out RECEIPT_DIR [--jobs N]

Each probe copies hdl/, tb/adp_engine and tb/common of an exported tree into a
scratch directory of its own, applies one exact text substitution (refusing to
run if the anchor is not found exactly once), runs `make -C tb/adp_engine run`
with whatever `verilator` is first on PATH, and records rc, the tally line and
every FAIL line. Nothing is written into the exported tree.
"""
import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
from pathlib import Path

ENG = "hdl/adp/KL_adp_engine.sv"
SIM = "tb/adp_engine/sim_main.cpp"
FRESH = ("            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n")
RESTART = ("            ev_disc_w   = 1'b1;\n"
           "            rec_wr_en_w = 1'b1;\n"
           "            iter_arm_w  = 1'b1;\n"
           "          end else begin\n")

# name, file, anchor, replacement, what it breaks
PROBES = [
    ("control", None, None, None, "no edit"),
    ("q0-fresh-no-store", ENG, FRESH, "",
     "fresh branch does not note the index (same edit as arc-fresh-no-store)"),
    ("q1-fresh-store-plus-one", ENG, FRESH,
     "            rec_wr_en_w = 1'b1;\n"
     "            rec_wr_data_w = {rx_ifx_r, rx_aidx_r + 32'd1};\n",
     "fresh branch notes the received index + 1 (over-notes)"),
    ("q2-fresh-store-max", ENG, FRESH,
     "            rec_wr_en_w = 1'b1;\n"
     "            rec_wr_data_w = {rx_ifx_r, 32'hFFFF_FFFF};\n",
     "fresh branch notes the maximum index"),
    ("q3-fresh-store-gm-only", ENG, FRESH,
     "            rec_wr_en_w = gm_dom_ok_w;\n",
     "fresh branch notes the index only when grandmaster and domain match"),
    ("q4-restart-no-store", ENG, RESTART,
     "            ev_disc_w   = 1'b1;\n"
     "            iter_arm_w  = 1'b1;\n"
     "          end else begin\n",
     "restart branch does not note the index"),
    ("q5-tb-no-followup", SIM, "  if (!notes_fresh_index(row, col)) return;\n",
     "  return;\n",
     "TB control: the round-2 follow-up step removed (vacuity of the walk without it)"),
]


def one(args, probe):
    name, path, anchor, repl, what = probe
    work = Path(args.work) / name
    if work.exists():
        shutil.rmtree(work)
    src = Path(args.tree)
    shutil.copytree(src / "hdl", work / "hdl")
    for d in ("adp_engine", "common"):
        shutil.copytree(src / "tb" / d, work / "tb" / d,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    if path is not None:
        f = work / path
        text = f.read_text()
        if text.count(anchor) != 1:
            return name, what, "ANCHOR", "", []
        f.write_text(text.replace(anchor, repl))
    log = Path(args.out) / f"probe-{name}.log"
    with log.open("w") as stream:
        rc = subprocess.run(["make", "-C", str(work / "tb" / "adp_engine"), "run"],
                            stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text()
    tally = next((ln for ln in text.splitlines() if re.match(r"\d+ checks:", ln)), "NO TALLY")
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL:")]
    return name, what, rc, tally, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    Path(args.out).mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(lambda p: one(args, p), PROBES))
    for name, what, rc, tally, fails in results:
        arc4 = sum("arc DISCOVERED -> DISCOVERED (index > last)" in f for f in fails)
        print(f"{name}: rc={rc} {tally} | arc4-check-failed={arc4} | {what}")
        for f in fails:
            print(f"    {f}")


if __name__ == "__main__":
    main()
