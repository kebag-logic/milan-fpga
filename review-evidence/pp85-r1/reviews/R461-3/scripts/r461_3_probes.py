#!/usr/bin/env python3
"""Reviewer fault probes of the round-3 two-sided noted-index check (R461-3).

usage: r461_3_probes.py --tree EXPORTED_HEAD_TREE --work SCRATCH_DIR --out RECEIPT_DIR [--jobs N]

Each probe copies hdl/, tb/adp_engine and tb/common of an exported tree into a
scratch directory of its own, applies one or more exact text substitutions
(refusing to run if an anchor is not found exactly once), runs
`make -C tb/adp_engine run` with whatever `verilator` is first on PATH, and
records rc, the tally line and every FAIL line. Nothing is written into the
exported tree.
"""
import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
from pathlib import Path

ENG = "hdl/adp/KL_adp_engine.sv"
SIM = "tb/adp_engine/sim_main.cpp"
FRESH = "            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n"
RESTART = ("            ev_disc_w   = 1'b1;\n"
           "            rec_wr_en_w = 1'b1;\n"
           "            iter_arm_w  = 1'b1;\n"
           "          end else begin\n")


def fresh_note(expr):
    return (ENG, FRESH, "            rec_wr_en_w = 1'b1;\n"
            f"            rec_wr_data_w = {expr};\n")


def restart_note(expr):
    return (ENG, RESTART, "            ev_disc_w   = 1'b1;\n"
            "            rec_wr_en_w = 1'b1;\n"
            f"            rec_wr_data_w = {expr};\n"
            "            iter_arm_w  = 1'b1;\n"
            "          end else begin\n")


Q1 = fresh_note("{rx_ifx_r, rx_aidx_r + 32'd1}")
R7 = (ENG, RESTART, "            ev_disc_w   = 1'b1;\n"
      "            iter_arm_w  = 1'b1;\n"
      "          end else begin\n")
NO_UPPER = (SIM,
            "  goto_disc(col, s);\n  apply_disc(col, row, s);\n  idle(20);\n"
            "  const size_t e2 = evts.size();\n",
            "  return;\n  const size_t e2 = evts.size();\n")
NO_REWALK = (SIM,
             "  goto_disc(col, s);\n  apply_disc(col, row, s);\n  idle(20);\n"
             "  const size_t e2 = evts.size();\n",
             "  const size_t e2 = evts.size();\n")
RESTART_AT_LAST = [
    (SIM, "    case V_STALE:  avail(col == D_DISC ? last - 1 : 3, gm, DOM0, 0); break;\n",
     "    case V_STALE:  avail(col == D_DISC ? last : 3, gm, DOM0, 0); break;\n"),
    (SIM, "  return row == V_STALE ? DISC_LAST - 1 : DISC_LAST + 1;\n",
     "  return row == V_STALE ? DISC_LAST : DISC_LAST + 1;\n"),
]
DISC_LAST_900 = (SIM, "constexpr uint32_t DISC_LAST = 700;\n",
                 "constexpr uint32_t DISC_LAST = 900;\n")

# name, [(file, anchor, replacement)], what it breaks
PROBES = [
    ("control", [], "no edit"),
    ("s1-restart-store-plus-one", [restart_note("{rx_ifx_r, rx_aidx_r + 32'd1}")],
     "restart branch notes the received index + 1"),
    ("s2-restart-store-max", [restart_note("{rx_ifx_r, 32'hFFFF_FFFF}")],
     "restart branch notes the maximum index"),
    ("s3-restart-store-minus-one", [restart_note("{rx_ifx_r, rx_aidx_r - 32'd1}")],
     "restart branch notes the received index - 1"),
    ("s4-fresh-store-minus-one", [fresh_note("{rx_ifx_r, rx_aidx_r - 32'd1}")],
     "fresh branch notes the received index - 1"),
    ("s5-fresh-store-wrong-ifx", [fresh_note("{rx_ifx_r ^ 16'd1, rx_aidx_r}")],
     "fresh branch notes the right index under another interface_index"),
    ("c1-no-upper-side-q1", [NO_UPPER, Q1],
     "TB: the upper side removed, RTL: q1 (does the upper side alone catch q1?)"),
    ("c2-no-rewalk-q1", [NO_REWALK, Q1],
     "TB: upper side asked straight after the repeat, without walking the cell again, RTL: q1"),
    ("c3-restart-at-last-r7", RESTART_AT_LAST + [R7],
     "TB: restart cell walked at the last index (700) as in round 2, RTL: r7"),
    ("c4-disc-last-900", [DISC_LAST_900],
     "TB: DISC_LAST moved to 900 (every site follows the constant), head RTL"),
    ("c5-disc-last-900-q1", [DISC_LAST_900, Q1], "TB: DISC_LAST 900, RTL: q1"),
    ("c6-disc-last-900-r7", [DISC_LAST_900, R7], "TB: DISC_LAST 900, RTL: r7"),
]


def one(args, probe):
    name, edits, what = probe
    work = Path(args.work) / name
    if work.exists():
        shutil.rmtree(work)
    src = Path(args.tree)
    shutil.copytree(src / "hdl", work / "hdl")
    for d in ("adp_engine", "common"):
        shutil.copytree(src / "tb" / d, work / "tb" / d,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    for path, anchor, repl in edits:
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
        arc5 = sum("arc DISCOVERED -> DISCOVERED (index <= last" in f for f in fails)
        print(f"{name}: rc={rc} {tally} | arc4-failed={arc4} arc5-failed={arc5} | {what}")
        for f in fails:
            print(f"    {f}")


if __name__ == "__main__":
    main()
