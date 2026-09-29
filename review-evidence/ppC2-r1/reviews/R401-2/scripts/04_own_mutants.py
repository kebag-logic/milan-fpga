#!/usr/bin/env python3
"""R401-2 reviewer-owned mutants against KL_pp_maap at the exact head.

Each mutant is an exact, unique string replacement in a scratch copy of the head
export's hdl/maap/KL_pp_maap.sv (refused if the anchor is absent or not unique).
The unmodified head tb/maap suite must finish red (rc != 0, a tally line with
failures) with at least one FAIL line whose check starts with one of the
expected prefixes. A build failure, a missing tally or a clean run is UNPROVEN.

Environment: PKT (packet root), VLT (Verilator 5.050 launcher). The head export
must already exist at $PKT/scratch/head (01_export_and_suites.sh).
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PKT = Path(os.environ["PKT"])
VLT = os.environ["VLT"]
HEAD = PKT / "scratch" / "head"
OUT = PKT / "receipts" / "own-mutants"
RTL = "hdl/maap/KL_pp_maap.sv"

# name, commit judged, anchor, replacement, expected FAIL prefixes
MUTANTS = [
    # round-1 reviewer mutants on the W_ADDR draw-mark fix, re-run at this head
    ("r401-release-clears-mark-after-request-only", "15de8b5",
     "            draw_act_r <= 1'b0;\n            w_st_r     <= W_OFF;",
     "            if (!draw_req_r) draw_act_r <= 1'b0;\n            w_st_r     <= W_OFF;",
     ("U17b:",)),
    ("r401-release-keeps-mark-on-coincident-answer", "15de8b5",
     "            draw_act_r <= 1'b0;\n            w_st_r     <= W_OFF;",
     "            if (!prng_draw_valid_i) draw_act_r <= 1'b0;\n            w_st_r     <= W_OFF;",
     ("U17b:",)),
    # 4de2c60 / d0acc9b: W_RX processes a record after the fall (sDefend after it)
    ("r401-rx-serves-record-after-fall", "4de2c60/d0acc9b",
     "          if (!eng_w) begin\n            // Release!: torn down from here",
     "          if (1'b0) begin\n            // Release!: torn down from here",
     ("U28:", "U26:")),
    # 4de2c60: a fall seen while the frame waits for the lane is not latched
    ("r401-lane-not-latched", "4de2c60",
     "W_WRITE, W_COMMIT,\n                                    W_LANE})",
     "W_WRITE, W_COMMIT})",
     ("U25:", "U24:", "U23:")),
    # 4de2c60: W_POST honours only the latch, not a fall first seen in W_POST
    ("r401-post-ignores-a-fall-seen-in-post", "4de2c60",
     "          if (!eng_w || rel_pend_r) begin",
     "          if (rel_pend_r) begin",
     ("U23:", "U28:")),
    # d0acc9b: the teardown never cancels probe_timer
    ("r401-teardown-keeps-probe-timer", "d0acc9b",
     "        W_TEARDOWN: begin\n          arm_v_r       <= 1'b1;",
     "        W_TEARDOWN: begin\n          arm_v_r       <= teardown_ph_r;",
     ("U28:",)),
    # 4f6affc: the drained frame reaches the lane one cycle later than the window
    ("r401-drain-one-cycle-late", "4f6affc",
     "          if (32'(bld_idx_r) == FRAME_BYTES_C - 1) begin",
     "          if (32'(bld_idx_r) == FRAME_BYTES_C - 1 + (rel_pend_r ? 1 : 0)) begin",
     ("U23:",)),
    # 2c11d6f / 4de2c60: a fall in W_IVAL leaves the interval draw's mark set
    ("r401-ival-keeps-draw-mark", "2c11d6f/4de2c60",
     "            draw_act_r    <= 1'b0;\n            pstate_r      <= P_INITIAL;\n"
     "            teardown_ph_r <= 1'b0;\n            w_st_r        <= W_TEARDOWN;\n"
     "          end else if (draw_act_r) begin",
     "            pstate_r      <= P_INITIAL;\n"
     "            teardown_ph_r <= 1'b0;\n            w_st_r        <= W_TEARDOWN;\n"
     "          end else if (draw_act_r) begin",
     ("U17c:", "U28:", "U23:")),
    # 8ae76ee: the seed is re-armed in the teardown only (the W_ADDR arc skips it)
    ("r401-seed-rearmed-in-teardown-only", "8ae76ee",
     ["          seed_used_r <= 1'b0;\n          rel_pend_r  <= 1'b0;",
      "            pend_ann_exp_r <= 1'b0;\n            w_st_r         <= W_OFF;"],
     ["          rel_pend_r  <= 1'b0;",
      "            pend_ann_exp_r <= 1'b0;\n            seed_used_r    <= 1'b0;\n"
      "            w_st_r         <= W_OFF;"],
     ("U27:",)),
    # fa21c58: the seed clamp lands one below the boundary
    ("r401-seed-clamp-target-minus-one", "fa21c58",
     "                        ? (POOL_SIZE_C - {8'd0, cfg_count_i})\n",
     "                        ? (POOL_SIZE_C - {8'd0, cfg_count_i} - 16'd1)\n",
     ("U18b:", "U18:")),
]

TALLY = re.compile(r"^(\d+) checks: \d+ PASS, (\d+) FAIL", re.M)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    src = (HEAD / RTL).read_text()
    lines = []
    killed = 0
    for name, commit, anchors, repls, prefixes in MUTANTS:
        if isinstance(anchors, str):
            anchors, repls = [anchors], [repls]
        counts = [src.count(a) for a in anchors]
        if counts != [1] * len(anchors):
            lines.append(f"{name} [{commit}]: anchor counts {counts} REFUSED")
            continue
        mutated = src
        for a, r in zip(anchors, repls):
            mutated = mutated.replace(a, r)
        tree = PKT / "scratch" / "mut" / name
        shutil.rmtree(tree, ignore_errors=True)
        (tree / "tb").mkdir(parents=True)
        shutil.copytree(HEAD / "hdl", tree / "hdl")
        for suite in ("maap", "common"):
            shutil.copytree(HEAD / "tb" / suite, tree / "tb" / suite,
                            ignore=shutil.ignore_patterns("obj_dir"))
        (tree / RTL).write_text(mutated)
        log = OUT / f"{name}.log"
        with log.open("w") as fh:
            rc = subprocess.run(["make", "-C", str(tree / "tb" / "maap"), f"VERILATOR={VLT}", "run"],
                                stdout=fh, stderr=subprocess.STDOUT, check=False).returncode
        text = log.read_text()
        t = TALLY.findall(text)
        fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
        named = [l for l in fails if l[5:].strip().startswith(prefixes)]
        ok = rc != 0 and bool(t) and int(t[-1][1]) > 0 and bool(named)
        killed += ok
        tally = f"{t[-1][0]} checks, {t[-1][1]} FAIL" if t else "no tally"
        lines.append(f"{name} [{commit}]: rc={rc} {tally} named={len(named)} "
                     f"{'KILLED' if ok else 'UNPROVEN'}")
        lines += ["    " + l for l in fails[:4]]
    lines.append(f"{killed} of {len(MUTANTS)} KILLED")
    (OUT / "summary.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if killed == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())
