#!/usr/bin/env python3
"""Reviewer-planted mutants of KL_acmp_talker.sv, each run in a fresh scratch
copy of an exported processor tree. Never edits a checkout.

Usage: own_mutants.py <exported-tree> <scratch-dir> <receipt> [suite ...]
Needs PINNED_VERILATOR; builds through verilator_j8.sh (at most 8 jobs).
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    "m01_conflict_keeps_wait": [(
        "if (!cfg_src_en_i[i] || !en_q_r[i] || set_conflict_w[i])",
        "if (!cfg_src_en_i[i] || !en_q_r[i])")],
    "m02_enable_keeps_wait": [(
        "if (!cfg_src_en_i[i] || !en_q_r[i] || set_conflict_w[i])",
        "if (set_conflict_w[i])")],
    "m03_no_accept_kill": [(
        "maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]",
        "maap_kill_r <= 1'b0 && pe_off_r[mreq_src_r]")],
    "m04_grant_kill_reg_only": [(
        "if (maap_kill_r || maap_kill_w)", "if (maap_kill_r)")],
    "m05_init_ignores_pending_off_conflict": [(
        "&& !pe_off_r[ev_src_r] && !pe_conflict_r[ev_src_r]) begin", ") begin")],
    "m06_turn_never_returns": [(
        "        txn_turn_r <= 1'b1;\n        if (disp_code_w == EVC_INIT)",
        "        if (disp_code_w == EVC_INIT)")],
    "m07_eligible_ignores_rel": [(
        "|| |pe_tmr_r || |pe_lsn_r || |pe_rel_r", "|| |pe_tmr_r || |pe_lsn_r")],
    "m08_release_sets_wait": [(
        "ev_to_maap_w && !ev_maap_rel_w)\n        retry_wait_r",
        "ev_to_maap_w)\n        retry_wait_r")],
    "m09_ready_ignores_turn": [(
        "assign txn_ready_o = (state_r == S_IDLE) && !gp_valid_r && txn_eligible_w",
        "assign txn_ready_o = (state_r == S_IDLE) && !gp_valid_r")],
    "m10_kill_ignores_conflict_strobe": [(
        "|| pe_conflict_r[maap_src_r]\n                       || (maap_conflict_valid_i\n"
        "                           && maap_conflict_src_i == maap_src_r);",
        "|| pe_conflict_r[maap_src_r];")],
    "m11_kill_ignores_disable": [(
        "assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]",
        "assign maap_kill_w = pe_off_r[maap_src_r]")],
    "m12_sticky_kill_off": [(
        "if (!maap_accept_w && (maap_busy_r || gp_valid_r) && maap_kill_w)",
        "if (1'b0)")],
    "m13_init_no_enable_check": [(
        "if ((rec_w.gstate == GS_NO_DA_C) && cfg_src_en_i[ev_src_r]",
        "if ((rec_w.gstate == GS_NO_DA_C)")],
    "m14_round_skips_rotation": [(
        "retry_next_r <= (disp_src_w == SRC_W_C'(N_STREAM_OUT_P - 1))\n"
        "                          ? '0 : disp_src_w + SRC_W_C'(1);",
        "retry_next_r <= retry_next_r;")],
    "m15_eligible_ignores_init": [(
        "|| (maap_avail_w && |init_ready_w));", ");")],
    "m16_tick_keeps_wait": [(
        "        retry_t0_r   <= now_ms_i;\n        retry_wait_r <= '0;",
        "        retry_t0_r   <= now_ms_i;")],
    "m19_init_elig_no_avail": [(
        "|| (maap_avail_w && |init_ready_w));", "|| (|init_ready_w));")],
    "m20_no_probe_initset": [(
        "if ((state_r == S_TXN_ACT) && txn_initset_w) set_init_w[tsrc_w]   = 1'b1;",
        "if (1'b0) set_init_w[tsrc_w]   = 1'b1;")],
    "m21_no_lsn_initset": [(
        "ev_initset_w = 1'b1;    // a listener appeared: retry allocation",
        "ev_initset_w = 1'b0;    // a listener appeared: retry allocation")],
    "m22_no_backoff_exit_initset": [(
        "ev_initset_w     = 1'b1;   // re-allocate, then re-declare",
        "ev_initset_w     = 1'b0;   // re-allocate, then re-declare")],
    "m18_no_round": [("retry_tick_w ? cfg_src_en_i : '0", "'0")],
    "m17_eligible_only_init": [(
        "|| !(|pe_off_r || |pe_conflict_r || |pe_pcp_r\n"
        "                              || |pe_tmr_r || |pe_lsn_r || |pe_rel_r\n"
        "                              || (maap_avail_w && |init_ready_w));",
        "|| !(maap_avail_w && |init_ready_w);")],
}


def main() -> int:
    src, scratch, receipt = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    suites = sys.argv[4:] or ["acmp_talker"]
    wrapper = Path(__file__).resolve().parent / "verilator_j8.sh"
    rtl_rel = Path("hdl/acmp/KL_acmp_talker.sv")
    original = (src / rtl_rel).read_text()
    lines = []
    only = [n for n in os.environ.get("ONLY_MUTANTS", "").split(",") if n]
    for name, reps in MUTANTS.items():
        if only and name not in only:
            continue
        text = original
        for old, new in reps:
            if text.count(old) != 1:
                raise SystemExit(f"{name}: anchor not unique ({text.count(old)})")
            text = text.replace(old, new)
        tree = scratch / name
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(src, tree, ignore=shutil.ignore_patterns("obj_dir"))
        (tree / rtl_rel).write_text(text)
        verdicts = []
        for suite in suites:
            r = subprocess.run(["make", "-C", str(tree / "tb" / suite),
                                f"VERILATOR={wrapper}"], capture_output=True,
                               text=True, timeout=3000, check=False)
            out = r.stdout + r.stderr
            tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", out)
            fails = [l for l in out.splitlines() if l.startswith("FAIL")][:3]
            state = "KILLED" if r.returncode else "SURVIVED"
            verdicts.append(f"{suite}:{state} rc={r.returncode} "
                            f"{tally[-1] if tally else 'no-tally'} "
                            + " | ".join(fails))
        line = f"{name}: " + " ; ".join(verdicts)
        print(line, flush=True)
        lines.append(line)
        shutil.rmtree(tree)
    receipt.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
