#!/usr/bin/env python3
"""R376-2 reviewer mutants of KL_acmp_talker.sv at head cc7c911e.

m01..m22 are the R376-1 reviewer mutants re-anchored to this head (only m01
and m02 needed new anchors, because round 2 removed the redundant !en_q_r[i]
term). m23..m31 are new round-2 reviewer mutants. Each mutant runs in a fresh
scratch copy of an exported processor tree; a checkout is never edited. A run
with no simulation tally is reported as NO-TALLY and never counted as a kill.

Usage: own_mutants_r2.py <exported-tree> <scratch-dir> <receipt> [suite ...]
Needs PINNED_VERILATOR; builds through verilator_j8.sh (at most 8 jobs).
ONLY_MUTANTS=a,b restricts the set. MUTANTS is importable by other probes.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    # ---- R376-1 set, head anchors ----
    "m01_conflict_keeps_wait": [(
        "if (!cfg_src_en_i[i] || set_conflict_w[i])",
        "if (!cfg_src_en_i[i])")],
    "m02_enable_keeps_wait": [(
        "if (!cfg_src_en_i[i] || set_conflict_w[i])",
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
    "m17_eligible_only_init": [(
        "|| !(|pe_off_r || |pe_conflict_r || |pe_pcp_r\n"
        "                              || |pe_tmr_r || |pe_lsn_r || |pe_rel_r\n"
        "                              || (maap_avail_w && |init_ready_w));",
        "|| !(maap_avail_w && |init_ready_w);")],
    "m18_no_round": [("retry_tick_w ? cfg_src_en_i : '0", "'0")],
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
    # ---- new in R376-2 ----
    # command turn never handed back to events after a command
    "m23_turn_never_cleared": [(
        "if (state_r == S_TXN_ACT) txn_turn_r <= 1'b0;",
        "if (1'b0) txn_turn_r <= 1'b0;")],
    # rotation restarts AT the last visited source instead of after it
    "m24_rotate_restarts_at_last": [(
        "? '0 : disp_src_w + SRC_W_C'(1);", "? '0 : disp_src_w;")],
    # single-term: EVC_INIT ignores only a pending OFF
    "m25_init_ignores_pending_off": [(
        "&& !pe_off_r[ev_src_r] && !pe_conflict_r[ev_src_r]) begin",
        "&& !pe_conflict_r[ev_src_r]) begin")],
    # single-term: EVC_INIT ignores only a pending CONFLICT
    "m26_init_ignores_pending_conflict": [(
        "&& !pe_off_r[ev_src_r] && !pe_conflict_r[ev_src_r]) begin",
        "&& !pe_off_r[ev_src_r]) begin")],
    # the round pacing bit is set only for accepted, not offered, requests
    "m27_wait_only_on_accept": [(
        "if ((state_r == S_EV_ACT) && ev_to_maap_w && !ev_maap_rel_w)\n"
        "        retry_wait_r[ev_src_r] <= 1'b1;",
        "if (maap_accept_w && !mreq_rel_r)\n"
        "        retry_wait_r[mreq_src_r] <= 1'b1;")],
    # retry tick re-arms only owned-less sources' INIT bits: tick sets nothing
    # for sources already pending (should be equivalent: OR is idempotent)
    "m28_init_ready_drops_enable": [(
        "assign init_ready_w = pe_init_r & cfg_src_en_i & ~retry_wait_r;",
        "assign init_ready_w = pe_init_r & ~retry_wait_r;")],
    # sticky kill set also on the accept edge (term !maap_accept_w removed)
    "m29_sticky_kill_ignores_accept": [(
        "if (!maap_accept_w && (maap_busy_r || gp_valid_r) && maap_kill_w)",
        "if ((maap_busy_r || gp_valid_r) && maap_kill_w)")],
    # PROBE_TX demand arc sets INIT for every enabled source (demand storm)
    "m30_probe_sets_all": [(
        "if ((state_r == S_TXN_ACT) && txn_initset_w) set_init_w[tsrc_w]   = 1'b1;",
        "if ((state_r == S_TXN_ACT) && txn_initset_w) set_init_w = cfg_src_en_i;")],
    # retry round clock restarted by every EVC_INIT dispatch (round drifts)
    "m31_round_restarts_on_init": [(
        "      if (retry_tick_w) begin\n        retry_t0_r   <= now_ms_i;\n",
        "      if (retry_tick_w || ((state_r == S_EV_ACT) && ev_to_maap_w)) begin\n"
        "        retry_t0_r   <= now_ms_i;\n")],
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
        for d in ("hdl", "tb/common", *(f"tb/{s}" for s in suites)):
            shutil.copytree(src / d, tree / d, ignore=shutil.ignore_patterns("obj_dir"))
        (tree / rtl_rel).write_text(text)
        verdicts = []
        for suite in suites:
            r = subprocess.run(["make", "-C", str(tree / "tb" / suite),
                                f"VERILATOR={wrapper}"], capture_output=True,
                               text=True, check=False)
            out = r.stdout + r.stderr
            tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", out)
            fails = [l for l in out.splitlines() if l.startswith("FAIL")]
            if not tally:
                state = "NO-TALLY"
            else:
                state = "KILLED" if (r.returncode and fails) else "SURVIVED"
            verdicts.append(f"{suite}:{state} rc={r.returncode} "
                            f"{tally[-1] if tally else 'no-tally'} "
                            f"nfail={len(fails)} first=" + " | ".join(fails[:2]))
        line = f"{name}: " + " ; ".join(verdicts)
        print(line, flush=True)
        lines.append(line)
        shutil.rmtree(tree)
    receipt.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
