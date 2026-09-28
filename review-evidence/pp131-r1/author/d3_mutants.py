#!/usr/bin/env python3
"""Negative controls for the D3 lane, kept out of the processor tree.

Each mutant copies the processor tree into a scratch directory, plants one
defect by exact text replacement (each old text must occur exactly once),
builds the named suite and runs its focused mode. A mutant is KILLED only when
the run completes (its tally line is printed), exits non-zero, and every check
named for it fails. A build failure or a crash never counts. The golden copy
runs first and must pass.

The driver rewrites HDL copies, so it lives in the evidence packet rather than
in the tree, where the parent classifier would count it as an unclassified
reader of production HDL.
"""
import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
from pathlib import Path

WRITER = "hdl/aecp/KL_aecp_nvm_writer.sv"
ENGINE = "hdl/aecp/KL_aecp_engine.sv"
DYN = "hdl/aecp/KL_aecp_dyn_state.sv"

PP_TOP = ("tb/pp_top", ["make", "gsi-build"], ["./obj_dir/Vpp_top_sim", "--d3-only"])
ACMP_NVM = ("tb/acmp_nvm", ["make", "ltn_rom.hex"], ["make", "run"])
SHADOW = "hdl/acmp/KL_acmp_nvm_shadow.sv"


def trg(sel: int) -> list[tuple[str, str, str]]:
    """Delete one group's trigger: its selector no longer sets a record."""
    old = "    if (chg_i && (chg_sel_i <= 13'd5)\n"
    new = f"    if (chg_i && (chg_sel_i <= 13'd5) && (chg_sel_i != 13'd{sel})\n"
    return [(WRITER, old, new)]


MUTANTS = {
    "hold_released_at_go": (PP_TOP, [(
        WRITER, "  assign own_o = !done_r || (ss_r == S_ACQ) || latch_w;\n",
        "  assign own_o = (ws_r == W_WAITGO) || (ss_r == S_ACQ) || latch_w;\n")],
        ["D3O1: released at"]),
    "dispatch_not_held": (PP_TOP, [
        (ENGINE, "                           && !amap_notify_busy_i && !d3_own_w;\n",
         "                           && !amap_notify_busy_i;\n"),
        (ENGINE, "  assign rsp_open_w     = (a_st_r == A_IDLE) && !rsp_busy_w && !d3_own_w\n",
         "  assign rsp_open_w     = (a_st_r == A_IDLE) && !rsp_busy_w\n"),
        (ENGINE, "          if (txn_valid_i && !rsp_busy_w && !amap_notify_busy_i\n"
                 "              && !d3_own_w) begin\n",
         "          if (txn_valid_i && !rsp_busy_w && !amap_notify_busy_i) begin\n")],
        ["D3O1: without the walk the writer owns every cycle"]),
    "TRG_cfg": (PP_TOP, trg(0), ["D3S1 cfg"]),
    "TRG_rate": (PP_TOP, trg(1), ["D3S1 rate"]),
    "TRG_clks": (PP_TOP, trg(2), ["D3S1 clks"]),
    "TRG_fmti": (PP_TOP, trg(3), ["D3S1 fmti"]),
    "TRG_fmto": (PP_TOP, trg(4), ["D3S1 fmto"]),
    "TRG_ptof": (PP_TOP, trg(5), ["D3S1 ptof"]),
    "taint_ignored": (PP_TOP, [(
        WRITER, "  assign done_ok_w   = (ss_r == S_WAIT) && m_done_i && !taint_r;\n",
        "  assign done_ok_w   = (ss_r == S_WAIT) && m_done_i;\n")],
        ["D3S4 taint"]),
    "clear_wins_same_edge": (PP_TOP, [(
        WRITER, "    else        dirty_r <= set_w | (dirty_r & ~clr_w);\n",
        "    else        dirty_r <= (set_w | dirty_r) & ~clr_w;\n")],
        ["D3S5 same edge"]),
    "clear_by_group": (PP_TOP, [(
        WRITER, "    if (done_ok_w || giveup_w) clr_w[hand_r] = 1'b1;\n",
        "    if (done_ok_w || giveup_w)\n"
        "      for (int unsigned i = 0; i < N_REC_C; i++)\n"
        "        if (rec_sel_f(RW_C'(i)) == hsel_w) clr_w[i] = 1'b1;\n")],
        ["D3S6 group"]),
    "clear_by_index": (PP_TOP, [(
        WRITER, "    if (done_ok_w || giveup_w) clr_w[hand_r] = 1'b1;\n",
        "    if (done_ok_w || giveup_w)\n"
        "      for (int unsigned i = 0; i < N_REC_C; i++)\n"
        "        if (16'(32'(i) - sel_off_f(rec_sel_f(RW_C'(i)))) == hidx_w)\n"
        "          clr_w[i] = 1'b1;\n")],
        ["D3S6 index"]),
    "identify_is_a_change": (PP_TOP, [
        (WRITER, "    if (chg_i && (chg_sel_i <= 13'd5)\n", "    if (chg_i && (chg_sel_i <= 13'd7)\n"),
        (DYN, "      default:           fmask_w = 64'd0;   // IDENTIFY is volatile\n",
         "      default:           fmask_w = 64'hFF;\n")],
        ["D3S7"]),
    "unchanged_compare_ignores_validity": (PP_TOP, [(
        DYN, "                    && (!vld_w[0] || ((st_wdata_i & fmask_w) != val_w));\n",
        "                    && ((st_wdata_i & fmask_w) != val_w);\n")],
        ["D3S8 validity"]),
    "latch_ignores_program": (PP_TOP, [(
        WRITER, "          if (!prog_busy_i) ss_r <= S_LATCH;\n",
        "          ss_r <= S_LATCH;\n")],
        ["D3S9"]),
    "fourth_attempt": (PP_TOP, [(
        WRITER, "  assign giveup_w    = write_err_w && (attempts_r >= 32'(1 + RETRY_MAX_P));\n",
        "  assign giveup_w    = write_err_w && (attempts_r >= 32'(2 + RETRY_MAX_P));\n")],
        ["D3S10 count"]),
    "alarm_forgiven_by_success": (PP_TOP, [(
        WRITER, "    else if (giveup_w) alarm_r <= 1'b1;            // sticky until reset\n",
        "    else if (giveup_w) alarm_r <= 1'b1;\n"
        "    else if (done_ok_w) alarm_r <= 1'b0;\n")],
        ["D3S10 revocation"]),
    "image_unproven_continues": (PP_TOP, [(
        WRITER, "    else if ((ws_r == W_IMGLOC) && sb_rvalid_i && sb_err_i)\n",
        "    else if (1'b0)\n")],
        ["D3O2: CLOSED at", "D3O3: CLOSED"]),
}

TOP = "hdl/top/protocol_processor_top.sv"
VERDICT_END = ("      W_JUDGE: begin accept_w = !jd_wait_i && jd_data_i[0];\n"
               "                     refuse_w = !jd_wait_i && !jd_data_i[0]; end\n"
               "      default: ;\n    endcase\n")


def rpl(sel: int) -> list[tuple[str, str, str]]:
    """Delete one group's replay: its framed, rule-accepted record is refused."""
    return [(WRITER, VERDICT_END, VERDICT_END + f"    if (rsel_w == 3'd{sel}) begin\n"
             "      refuse_w = accept_w || refuse_w;\n      accept_w = 1'b0;\n    end\n")]


MUTANTS.update({
    "RPL_cfg": (PP_TOP, rpl(0), ["D3R1 cfg"]),
    "RPL_rate": (PP_TOP, rpl(1), ["D3R1 rate"]),
    "RPL_clks": (PP_TOP, rpl(2), ["D3R1 clks"]),
    "RPL_fmti": (PP_TOP, rpl(3), ["D3R1 fmti"]),
    "RPL_fmto": (PP_TOP, rpl(4), ["D3R1 fmto"]),
    "RPL_ptof": (PP_TOP, rpl(5), ["D3R1 ptof"]),
    "rule_ignored": (PP_TOP, [(WRITER, VERDICT_END, VERDICT_END
        + "    if (refuse_w) begin\n      accept_w = 1'b1;\n      refuse_w = 1'b0;\n    end\n")],
        ["D3R2: COMPLETE"]),
    "passes_may_disagree": (PP_TOP, [(
        WRITER, "  assign pass_disagree_w = pass_r && (rd_whole_w || rd_blank_w)\n",
        "  assign pass_disagree_w = 1'b0 && (rd_whole_w || rd_blank_w)\n")],
        ["D3R4"]),
    "device_error_reads_as_blank": (PP_TOP, [
        (WRITER, "                      && (m_err_cause_i == PORT_UNFRAMED_C);\n", ";\n"),
        (WRITER, "                      && (m_err_cause_i != PORT_UNFRAMED_C);\n", " && 1'b0;\n")],
        ["D3R5 device error on the header", "D3R6: the one saved record"]),
    "unframed_reads_as_device_error": (PP_TOP, [
        (WRITER, "                      && (m_err_cause_i == PORT_UNFRAMED_C);\n", " && 1'b0;\n"),
        (WRITER, "                      && (m_err_cause_i != PORT_UNFRAMED_C);\n", ";\n")],
        ["D3R6: an erased device restores blank"]),
    "desc_error_is_a_refusal": (PP_TOP, [(
        WRITER, "    else if ((ws_r == W_LOC) && sb_rvalid_i && sb_err_i)\n",
        "    else if (1'b0)\n")],
        ["D3R7"]),
    "no_restore_watchdog": (PP_TOP, [(
        WRITER, "  assign expire_w = stall_w && (wd_r >= 32'(RS_TMO_CYC_P - 1));\n",
        "  assign expire_w = 1'b0 && (wd_r >= 32'(RS_TMO_CYC_P - 1));\n")],
        ["D3R8"]),
    "restore_writes_are_changes": (PP_TOP, [(
        ENGINE, "  assign d3_chg_w = dyn_chg_w && !d3_bus_w;\n",
        "  assign d3_chg_w = dyn_chg_w;\n")],
        ["D3R1: no restore write is a change"]),
    "enable_not_released_by_restore": (PP_TOP, [(
        TOP, "  assign adp_enable_w = entity_enable_i && restore_done_o;\n",
        "  assign adp_enable_w = entity_enable_i;\n")],
        ["D3R1: the enable requested from reset"]),
    "done_without_d3": (PP_TOP, [(
        TOP, "  assign restore_done_o   = nvm_walk_done_w && lsn_released_w && d3_done_w;\n",
        "  assign restore_done_o   = nvm_walk_done_w && lsn_released_w;\n")],
        ["D3R1: the enable requested from reset", "D3R1: COMPLETE"]),
    "blank_ignores_d3": (PP_TOP, [(
        TOP, "                            && nvm_walk_blank_w && d3_blank_w;\n",
        "                            && nvm_walk_blank_w;\n")],
        ["D3R1: COMPLETE"]),
    "own_taken_at_the_walk": (PP_TOP, [(
        WRITER, "  assign own_o = !done_r || (ss_r == S_ACQ) || latch_w;\n"
                "  assign bus_o = !done_r || latch_w;\n",
        "  assign own_o = ((ws_r != W_WAITGO) && !done_r) || (ss_r == S_ACQ) || latch_w;\n"
        "  assign bus_o = ((ws_r != W_WAITGO) && !done_r) || latch_w;\n")],
        ["D3R9: the held SET"]),
})

MUTANTS.update({
    "no_rollback": (PP_TOP, [(
        WRITER, "        rb_min_r <= 1'b0;\n        ws_r     <= W_RB;\n",
        "        done_r   <= 1'b1;\n        ws_r     <= W_DONE;\n")],
        ["D3R4"]),
    "dyn_not_rolled_back": (PP_TOP, [(
        ENGINE, "  ) u_dyn (\n      .clk_i           (clk_i),\n      .rst_n           (store_rst_n_w),\n",
        "  ) u_dyn (\n      .clk_i           (clk_i),\n      .rst_n           (rst_n),\n")],
        ["D3R4"]),
    "store_not_rolled_back": (PP_TOP, [(
        ENGINE, "  ) u_store (\n      .clk_i             (clk_i),\n      .rst_n             (store_rst_n_w),\n",
        "  ) u_store (\n      .clk_i             (clk_i),\n      .rst_n             (rst_n),\n")],
        ["D3R10 5000"]),
    "rollback_ignores_debt": (PP_TOP, [(
        WRITER, "          if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;\n",
        "          if (rb_min_r) ws_r <= W_RELOC;\n")],
        ["D3R10 16000"]),
    "closed_releases_the_entity": (PP_TOP, [(
        WRITER, "            closed_r <= 1'b1;             // the image walked again is not proven\n"
                "            ws_r     <= W_CLOSED;\n",
        "            done_r   <= 1'b1;\n            ws_r     <= W_DONE;\n")],
        ["D3R12"]),
})

MUTANTS.update({
    "no_backoff_d3": (PP_TOP, [(
        WRITER, "          if (bo_cnt_r <= 32'd1) ss_r <= S_ACQ;  // a fresh latch, attempts kept\n"
                "          else                   bo_cnt_r <= bo_cnt_r - 32'd1;\n",
        "          ss_r <= S_ACQ;\n")],
        ["D3S10 timing"]),
    "no_backoff_binding": (ACMP_NVM, [(
        SHADOW, "          if (fl_bo_r <= 32'd1) hs_r    <= H_FL_RD;\n"
                "          else                  fl_bo_r <= fl_bo_r - 32'd1;\n",
        "          hs_r <= H_FL_RD;\n")],
        ["E9 DR2c timing"]),
    "fourth_attempt_binding": (ACMP_NVM, [
        (SHADOW, "  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P);\n",
         "  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P + 1);\n"),
        (SHADOW, "          if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P) begin\n",
         "          if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P + 1) begin\n"),
        (SHADOW, "end else if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P) begin\n",
         "end else if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P + 1) begin\n")],
        ["E8 DR2c count"]),
    "alarm_forgiven_binding": (ACMP_NVM, [(
        SHADOW, "      alarm_r <= 1'b1;                             // sticky until reset\n    end\n",
        "      alarm_r <= 1'b1;\n    end else if (fl_done_w && !fl_taint_r) begin\n"
        "      alarm_r <= 1'b0;\n    end\n")],
        ["E11 DR2c revocation"]),
})

ARB = "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv"
MUTANTS.update({
    "store_not_cleared": (PP_TOP, [
        (DYN, "      rate_v_r   <= '0;\n", ""),
        (DYN, "      for (int unsigned i = 0; i < N_AUDIO_UNIT_P; i++) rate_r[i]   <= 32'd0;\n", "")],
        ["D3R1: every row at its reset value"]),
    "valid_not_cleared": (PP_TOP, [
        (DYN, "      rate_v_r   <= '0;\n", "")],
        ["D3R1: every row at its reset value"]),
    "quarantine_released_by_time": (PP_TOP, [(
        ARB, "  assign end_w  = (own_r != O_NONE) && (p_done_i || p_err_i);\n",
        "  logic [15:0] mut_dcnt_r;\n"
        "  always_ff @(posedge clk_i) mut_dcnt_r <= (!rst_n || !drain_r) ? 16'd0 : mut_dcnt_r + 16'd1;\n"
        "  assign end_w  = (own_r != O_NONE)\n"
        "                  && (p_done_i || p_err_i || (drain_r && (mut_dcnt_r == 16'd1000)));\n")],
        ["D3R5: once the device ends the drained read a later SET persists"]),
})

TALLY = re.compile(r"\d+ checks(, \d+ failures|: \d+ PASS, \d+ FAIL)")


def plant(tree: Path, edits: list[tuple[str, str, str]]) -> None:
    """Apply every exact replacement, refusing an old text that is not unique."""
    for rel, old, new in edits:
        path = tree / rel
        text = path.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"REFUSED: {rel}: the planted text occurs "
                             f"{text.count(old)} times")
        path.write_text(text.replace(old, new, 1))


def run_one(name: str, suite: tuple, edits: list, expect: list[str],
            source: Path, scratch: Path) -> dict:
    """Build and run one copy; report whether every named check failed."""
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(source, tree, ignore=shutil.ignore_patterns(".git", "obj_*"))
    try:
        plant(tree, edits)
    except SystemExit as refusal:
        shutil.rmtree(tree, ignore_errors=True)
        return {"mutant": name, "verdict": "REFUSED", "reason": str(refusal),
                "missing_expected": expect}
    where, build, run = suite
    cwd = tree / where
    log = scratch / f"{name}.log"
    with log.open("w") as out:
        b = subprocess.run(build, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                           check=False)
        r = subprocess.run(run, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                           check=False) if b.returncode == 0 else None
    text = log.read_text(errors="replace")
    fails = [ln[len("FAIL: "):] for ln in text.splitlines() if ln.startswith("FAIL: ")]
    completed = bool(TALLY.search(text))
    missing = [e for e in expect if not any(f.startswith(e) for f in fails)]
    rc = None if r is None else r.returncode
    if name == "golden":
        verdict = "PASS" if (rc == 0 and completed and not fails) else "BROKEN"
    else:
        verdict = "KILLED" if (rc not in (0, None) and completed and not missing) else "SURVIVED"
    shutil.rmtree(tree, ignore_errors=True)
    return {"mutant": name, "build_rc": b.returncode, "run_rc": rc,
            "completed": completed, "failing_checks": fails,
            "missing_expected": missing, "verdict": verdict, "log": str(log)}


def main() -> int:
    """Run the golden copy, then the selected mutants."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--summary", type=Path, required=True)
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    names = args.only or list(MUTANTS)
    suites = {MUTANTS[n][0][0]: MUTANTS[n][0] for n in names}
    results = [run_one("golden-" + where.split("/")[-1], suite, [], [],
                       args.tree, args.scratch)
               for where, suite in sorted(suites.items())]
    for r in results:
        r["verdict"] = "PASS" if (r["run_rc"] == 0 and r["completed"]
                                  and not r["failing_checks"]) else "BROKEN"
        print(json.dumps(r), flush=True)
    if any(r["verdict"] != "PASS" for r in results):
        args.summary.write_text(json.dumps(results, indent=1) + "\n")
        return 1
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(run_one, n, MUTANTS[n][0], MUTANTS[n][1],
                               MUTANTS[n][2], args.tree, args.scratch): n
                   for n in names}
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            results.append(res)
            print(json.dumps({k: res[k] for k in ("mutant", "verdict",
                                                  "missing_expected")}), flush=True)
    args.summary.write_text(json.dumps(results, indent=1) + "\n")
    return 0 if all(r["verdict"] in ("PASS", "KILLED") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
