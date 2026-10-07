#!/usr/bin/env python3
"""R530-2 reviewer-planted RTL defects for the adp channel's bound-talker term.

Independent of the lane's own mutants.py arms: it reuses only that file's
plant/build/run machinery (the Makefile's recipe, a copy of the RTL per arm,
the two-interface variant written by the generator into the copy), and plants
the reviewer's own substitutions.  Each probe records whether the suite at the
head reddens (rc 1 with at least one [FAIL]) and which check failed first.
A probe that is semantically equivalent to the head is labelled so up front
and is expected to stay green.

Usage (from a copy of the exact head, Verilator 5.050 first on PATH):
    python3 r530_2_rtl_probes.py --tree <copy-of-head> [--jobs 2]
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--tree", type=Path, required=True)
ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--only", default="")
args = ap.parse_args()
sys.path.insert(0, str(args.tree / "tb" / "verilator" / "mbx"))
import mutants as M  # noqa: E402  (the lane's machinery at the head, never modified)

RX = "KL_mbx_rx.sv"
TOP = "KL_mbx.sv"


def arm(name, path, old, new, ifs=1, host=0, equivalent=False):
    return (M.Arm(name, path, old, new, host, "", ifs), equivalent)


PROBES = [
    # --- wrong byte index -------------------------------------------------
    arm("X1-copy-words-swapped", RX, "RW_C'(2 * int'(cp_k_r) + int'(cp_b_r[2]))",
        "RW_C'(2 * int'(cp_k_r) + int'(!cp_b_r[2]))"),
    arm("X2-armed-at-second-identity-byte", RX, "(cnt_r == 11'(BO_C) || match_r[e])",
        "(cnt_r == 11'(BO_C + 1) || match_r[e])"),
    arm("X3-tap-index-from-cnt-low-bits", RX, "assign cmp_b_w   = 3'(cnt_r - 11'(BO_C));",
        "assign cmp_b_w   = 3'(cnt_r);"),
    arm("X4-copy-byte-lane-rotated", RX, "rb_q_w[8 * int'(cp_b_r[1:0]) +: 8]",
        "rb_q_w[8 * int'(cp_b_r[1:0] + 2'd1) +: 8]"),
    # --- stale match flag across frames ------------------------------------
    arm("X5-flag-kept-on-unequal-byte", RX,
        "if (cmp_w) match_r[e] <= live_w[e] && eq_w[e] && (cnt_r == 11'(BO_C) || match_r[e]);",
        "if (cmp_w && eq_w[e]) match_r[e] <= live_w[e] && eq_w[e] && (cnt_r == 11'(BO_C) || match_r[e]);"),
    arm("X6-eq-bound-field-length-unchecked", RX,
        "MBX_TEST_EQ_BOUND_C:      if (field_ok && bound_hit_w)", "MBX_TEST_EQ_BOUND_C:      if (bound_hit_w)"),
    arm("X7-flag-not-cleared-by-reset", RX, "      match_r   <= '0;\n", ""),
    # --- off-by-one entry ---------------------------------------------------
    arm("X8-copier-reads-next-entry", RX, "RW_C'(2 * int'(cp_k_r) + int'(cp_b_r[2]))",
        "RW_C'(2 * int'(cp_k_r) + 2 + int'(cp_b_r[2]))"),
    arm("X9-scan-wraps-past-entry-0", RX, "(32'(cp_k_r) == NE_C - 1) ? '0 :",
        "(32'(cp_k_r) == NE_C - 1) ? KW_C'(1) :"),
    arm("X10-last-entry-never-live", RX, "for (int e = 0; e < int'(NB_C); e++) begin\n      live_w[e]",
        "for (int e = 0; e < int'(NB_C) - 1; e++) begin\n      live_w[e]"),
    arm("X11-valid-flag-of-next-word", RX, "if (rb_a_w == RW_C'(2 * k)) rb_vld_w = vlo_r[k];",
        "if (rb_a_w == RW_C'(2 * k)) rb_vld_w = vhi_r[k];"),
    arm("X12-entry-decode-bound-relaxed-equivalent", TOP, "&& entry < AW2_C'(MBX_N_BOUND_C)",
        "&& entry <= AW2_C'(MBX_N_BOUND_C)", equivalent=True),
    # --- interface mix-up ---------------------------------------------------
    arm("X13-frame-table-from-live-if-input", RX,
        "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
        "assign {fok_w, fif_w} = (int'(rx_if_i) < int'(MBX_N_IF_C)) ? {1'b1, rx_if_i} : '0;"),
    arm("X13-frame-table-from-live-if-input-if2", RX,
        "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
        "assign {fok_w, fif_w} = (int'(rx_if_i) < int'(MBX_N_IF_C)) ? {1'b1, rx_if_i} : '0;", ifs=2),
    arm("X14-host-entry-interface-transposed-if2", RX,
        "assign hk_w   = KW_C'(int'(bnd_if_i) * int'(NB_C) + int'(bnd_entry_i));",
        "assign hk_w   = KW_C'(int'(bnd_entry_i) * int'(MBX_N_IF_C) + int'(bnd_if_i));", ifs=2),
    arm("X15-copy-into-other-interface-if2", RX, "c_sh_w[k] = cp_step_w && int'(cp_k_r) == k;",
        "c_sh_w[k] = cp_step_w && (int'(cp_k_r) + int'(NB_C)) % int'(NE_C) == k;", ifs=2),
    arm("X16-out-of-range-index-uses-table-0", RX,
        "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
        "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : {1'b1, MBX_IF_W_C'(0)};"),
    arm("X17-live-of-other-interface-if2", RX,
        "live_w[e] = fok_w && en_r[int'(fif_w) * int'(NB_C) + e] && !owed_r[int'(fif_w) * int'(NB_C) + e];",
        "live_w[e] = fok_w && en_r[int'(fif_w) * int'(NB_C) + e] && !owed_r[e];", ifs=2),
    # --- AXI4-Lite host for two of them -----------------------------------
    arm("X5-flag-kept-on-unequal-byte-axil", RX,
        "if (cmp_w) match_r[e] <= live_w[e] && eq_w[e] && (cnt_r == 11'(BO_C) || match_r[e]);",
        "if (cmp_w && eq_w[e]) match_r[e] <= live_w[e] && eq_w[e] && (cnt_r == 11'(BO_C) || match_r[e]);",
        host=1),
    arm("X14-host-entry-interface-transposed-if2-axil", RX,
        "assign hk_w   = KW_C'(int'(bnd_if_i) * int'(NB_C) + int'(bnd_entry_i));",
        "assign hk_w   = KW_C'(int'(bnd_entry_i) * int'(MBX_N_IF_C) + int'(bnd_if_i));", ifs=2, host=1),
    # --- positive controls: the head's RTL unchanged (expected green) -----
    arm("CTRL-if1-wb", RX, "assign cp_step_w = cp_busy_r && !bnd_req_i;", "assign cp_step_w = cp_busy_r && !bnd_req_i;",
        equivalent=True),
    arm("CTRL-if1-axil", RX, "assign cp_step_w = cp_busy_r && !bnd_req_i;",
        "assign cp_step_w = cp_busy_r && !bnd_req_i;", host=1, equivalent=True),
    arm("CTRL-if2-wb", RX, "assign cp_step_w = cp_busy_r && !bnd_req_i;", "assign cp_step_w = cp_busy_r && !bnd_req_i;",
        ifs=2, equivalent=True),
    arm("CTRL-if2-axil", RX, "assign cp_step_w = cp_busy_r && !bnd_req_i;",
        "assign cp_step_w = cp_busy_r && !bnd_req_i;", ifs=2, host=1, equivalent=True),
]


def run(p):
    a, eq = p
    try:
        copy = M.plant(a, ROOT)
    except ValueError as exc:
        return a, eq, 2, f"FIXTURE: {exc}"
    rc, log = M.build_and_run(copy, ROOT / a.name, a.host, a.ifs)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    tally = [ln.strip() for ln in log.splitlines() if "checks:" in ln]
    first = fails[0] if fails else (tally[-1] if tally else (log.strip().splitlines() or ["no output"])[-1])
    return a, eq, rc, f"{len(fails)} failed; {first}"


with tempfile.TemporaryDirectory(prefix="r530-2-probes-") as tmp:
    ROOT = Path(tmp)
    sel = [p for p in PROBES if not args.only or p[0].name in args.only.split(",")]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(run, sel))
    bad = 0
    for a, eq, rc, detail in results:
        caught = rc == 1 and "[FAIL]" in detail
        if eq:
            verdict = "equivalent-green" if rc == 0 else f"equivalent-but-rc{rc}"
        else:
            verdict = "CAUGHT" if caught else ("FIXTURE" if rc == 2 else "ESCAPED")
            bad += not caught
        print(f"[{verdict}] {a.name} (ifs {a.ifs}, host {a.host}) rc={rc}: {detail}")
    print(f"r530-2 probes: {sum(1 for a, eq, rc, d in results if not eq and rc == 1 and '[FAIL]' in d)} of "
          f"{sum(1 for _a, eq, _r, _d in results if not eq)} non-equivalent caught")
sys.exit(1 if bad else 0)
