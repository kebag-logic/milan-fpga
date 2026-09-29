#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned mutation probes for KL_pp_maap (R400-2).

Each arm is an exact string replacement in hdl/maap/KL_pp_maap.sv, planted in a
fresh scratch export of the reviewed commit. The unit suite (tb/maap, make run)
is built and run; the verdict reads only the simulation log's tally and FAIL
lines. A build failure or a missing tally is UNPROVEN, never a kill.

usage: r400_mutants.py --repo CLONE --rev SHA --out DIR --work SCRATCH --verilator VERILATOR
                       [--only a,b]
"""
import argparse
import difflib
import re
import shutil
import subprocess
from pathlib import Path

RTL = "hdl/maap/KL_pp_maap.sv"

TX_SET = ("      if (!eng_w && (w_st_r inside {W_ALLOC, W_GWAIT, W_WRITE, W_COMMIT,\n"
          "                                    W_LANE})) begin\n")


def tx_set_without(state: str) -> str:
    states = [s for s in ("W_ALLOC", "W_GWAIT", "W_WRITE", "W_COMMIT", "W_LANE")
              if s != state]
    return "      if (!eng_w && (w_st_r inside {" + ", ".join(states) + "})) begin\n"


ARMS = [
    # the Release! latch in the TX path, one state at a time
    ("tx-set-omits-alloc", TX_SET, tx_set_without("W_ALLOC")),
    ("tx-set-omits-gwait", TX_SET, tx_set_without("W_GWAIT")),
    ("tx-set-omits-write", TX_SET, tx_set_without("W_WRITE")),
    ("tx-set-omits-commit", TX_SET, tx_set_without("W_COMMIT")),
    ("tx-set-omits-lane", TX_SET, tx_set_without("W_LANE")),
    # the TX-path fall latches rel_pend but keeps the claim published
    ("tx-fall-keeps-claim",
     "        pstate_r   <= P_INITIAL;\n        rel_pend_r <= 1'b1;\n",
     "        rel_pend_r <= 1'b1;\n"),
    # W_OFF forgets to clear the latched Release!
    ("off-keeps-rel-pend",
     "          seed_used_r <= 1'b0;\n          rel_pend_r  <= 1'b0;\n",
     "          seed_used_r <= 1'b0;\n"),
    # W_IVAL's fall keeps the draw mark (the round-1 wedge, new arc)
    ("ival-fall-keeps-draw-mark",
     "            draw_act_r    <= 1'b0;\n            pstate_r      <= P_INITIAL;\n"
     "            teardown_ph_r <= 1'b0;\n            w_st_r        <= W_TEARDOWN;\n"
     "          end else if (draw_act_r) begin\n",
     "            pstate_r      <= P_INITIAL;\n"
     "            teardown_ph_r <= 1'b0;\n            w_st_r        <= W_TEARDOWN;\n"
     "          end else if (draw_act_r) begin\n"),
    # W_POST's Release! keeps a pending probeCount! chain
    ("post-teardown-keeps-chain",
     "            pstate_r      <= P_INITIAL;\n            chain_ann_r   <= 1'b0;\n",
     "            pstate_r      <= P_INITIAL;\n"),
    # W_IVAL's fall skips the teardown (goes straight to W_OFF)
    ("ival-fall-skips-teardown",
     "            draw_act_r    <= 1'b0;\n            pstate_r      <= P_INITIAL;\n"
     "            teardown_ph_r <= 1'b0;\n            w_st_r        <= W_TEARDOWN;\n",
     "            draw_act_r    <= 1'b0;\n            pstate_r      <= P_INITIAL;\n"
     "            teardown_ph_r <= 1'b0;\n            w_st_r        <= W_OFF;\n"),
    # the seed clamp with >= (equivalence probe: seed == fit clamps to itself)
    ("seed-clamp-ge",
     "offset_r <= (cfg_seed_offset_i > (POOL_SIZE_C",
     "offset_r <= (cfg_seed_offset_i >= (POOL_SIZE_C"),
    # the seed clamp lands one below the fit
    ("seed-clamp-value-minus-one",
     "                        ? (POOL_SIZE_C - {8'd0, cfg_count_i})\n"
     "                        : cfg_seed_offset_i;\n",
     "                        ? (POOL_SIZE_C - {8'd0, cfg_count_i} - 16'd1)\n"
     "                        : cfg_seed_offset_i;\n"),
]

TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def export(repo: Path, rev: str, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    archive = subprocess.run(["git", "-C", str(repo), "archive", rev],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    summary = []
    for label, old, new in ARMS:
        if only and label not in only:
            continue
        tree = a.work / label
        export(a.repo, a.rev, tree)
        rtl = tree / RTL
        src = rtl.read_text()
        n = src.count(old)
        if n != 1:
            summary.append(f"{label}: ANCHOR-{n} UNPROVEN")
            print(summary[-1], flush=True)
            continue
        mut = src.replace(old, new)
        rtl.write_text(mut)
        (a.out / f"{label}.patch").write_text("".join(difflib.unified_diff(
            src.splitlines(True), mut.splitlines(True),
            fromfile="a/" + RTL, tofile="b/" + RTL)))
        log = a.out / f"{label}.log"
        with log.open("w") as fh:
            rc = subprocess.run(["make", "-C", str(tree / "tb" / "maap"), "run",
                                 f"VERILATOR={a.verilator}"],
                                stdout=fh, stderr=subprocess.STDOUT).returncode
        text = log.read_text()
        t = TALLY.findall(text)
        fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
        if not t:
            verdict = "UNPROVEN(no tally)"
        elif rc != 0 and int(t[-1][2]) > 0:
            verdict = "KILLED"
        elif rc == 0 and int(t[-1][2]) == 0:
            verdict = "SURVIVED"
        else:
            verdict = "UNPROVEN"
        first = fails[0] if fails else ""
        summary.append(f"{label}: rc={rc} tally={t[-1] if t else None} {verdict} | {first}")
        print(summary[-1], flush=True)
        shutil.rmtree(tree / "tb" / "maap" / "obj_dir", ignore_errors=True)
    (a.out / "SUMMARY.txt").write_text("\n".join(summary) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
