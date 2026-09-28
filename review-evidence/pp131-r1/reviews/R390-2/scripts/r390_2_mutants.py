#!/usr/bin/env python3
"""Reviewer mutants, R390-2, at the exact head. Each mutant is planted in a
fresh git-archive copy, the pp_top bench is built with the given Verilator
and its D3 section is run (--d3-only). KILLED = build ok and the run fails
(the FAIL lines name the checks); SURVIVED = build ok and every D3 check
passes; REFUSED = an anchor did not occur exactly once or the build failed.
Usage: r390_2_mutants.py <clone> <scratch> <verilator> [name ...]"""
import subprocess, sys, pathlib, shutil, concurrent.futures as cf

HEAD = "2b38d68e704e8a62fbeae8171c9195ca93728488"
W = "hdl/aecp/KL_aecp_nvm_writer.sv"
T = "hdl/top/protocol_processor_top.sv"
V = "hdl/packet_engine/KL_pp_rx_validator.sv"
HOLD = "  assign aecp_rx_hold_w = !d3_done_w && ((aecp_rx_res_r != '0) || aecp_rx_in_w);"
MUTANTS = {
    # ---- round 1 (R390-1 F3), re-run at this head
    "backoff_holds_dispatch": [(W,
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w;",
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w || (ss_r == S_BACKOFF);")],
    "disagree_one_direction": [(W,
        "&& (rd_whole_w != whole0_r[rec_r]);",
        "&& (!rd_whole_w && whole0_r[rec_r]);")],
    "rollback_one_cycle": [(W,
        "if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;",
        "if (!desc_debt_i) ws_r <= W_RELOC;")],
    "backoff_derivation": [(T,
        "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2),",
        "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd200),")],
    # ---- round 2: the DR3a aggregate
    "agg_removed": [(W,
        "assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P - 1))",
        "assign agg_expire_w = 1'b0 && (agg_r >= 32'(RS_AGG_CYC_P - 1))")],
    "agg_one_late": [(W,
        "assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P - 1))",
        "assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P))"),
        (W, "if (agg_live_w && (agg_r < 32'(RS_AGG_CYC_P - 1))) agg_r <= agg_r + 32'd1;",
            "if (agg_live_w && (agg_r < 32'(RS_AGG_CYC_P))) agg_r <= agg_r + 32'd1;")],
    "agg_restarts_on_go": [(W,
        "      if (agg_live_w && (agg_r < 32'(RS_AGG_CYC_P - 1))) agg_r <= agg_r + 32'd1;",
        "      if (rs_go_i) agg_r <= 32'd0;\n"
        "      else if (agg_live_w && (agg_r < 32'(RS_AGG_CYC_P - 1))) agg_r <= agg_r + 32'd1;")],
    "agg_ignores_in_hand": [(W,
        "                        && (stall_w || !wait_w);",
        "                        && 1'b1;")],
    "agg_not_in_rollback": [(W,
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r && !done_r && !closed_r;",
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r && !done_r && !closed_r"
        " && (ws_r != W_RB) && (ws_r != W_RELOC);")],
    # ---- round 2: the AECP hold admission
    "hold_unbounded": [(T, HOLD,
        "  assign aecp_rx_hold_w = 1'b0 && ((aecp_rx_res_r != '0) || aecp_rx_in_w);")],
    "hold_until_any_terminal": [(T, HOLD,
        "  assign aecp_rx_hold_w = !d3_done_w && !d3_closed_w && ((aecp_rx_res_r != '0) || aecp_rx_in_w);")],
    "hold_admits_two": [(T, HOLD,
        "  assign aecp_rx_hold_w = !d3_done_w && (aecp_rx_res_r > 1);")],
    "hold_after_release": [(T, HOLD,
        "  assign aecp_rx_hold_w = ((aecp_rx_res_r != '0) || aecp_rx_in_w);")],
    "residency_counts_acmp": [(T,
        "                         && (v_hdr_protocol_w != 3'(PP_PROTO_ACMP))\n", "")],
    "held_gate_ignores_da": [(V,
        "&& (rx_data_i == SUB_AECP_C) && (da_own_r | da_mcast_r);",
        "&& (rx_data_i == SUB_AECP_C);")],
}

def run(name, clone, scratch, vl):
    out = pathlib.Path(scratch) / name
    shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", clone, "archive", HEAD], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(out)], input=tar, check=True)
    for path, old, new in MUTANTS[name]:
        f = out / path; s = f.read_text()
        if s.count(old) != 1:
            return f"{name}: REFUSED anchor count {s.count(old)} in {path}"
        f.write_text(s.replace(old, new))
    tb = out / "tb/pp_top"
    b = subprocess.run(["make", "gsi-build", f"VERILATOR={vl}"], cwd=tb, capture_output=True, text=True)
    (out / "build.log").write_text(b.stdout + b.stderr)
    if b.returncode != 0:
        return f"{name}: REFUSED build rc={b.returncode}"
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--d3-only"], cwd=tb, capture_output=True, text=True)
    (out / "run.log").write_text(r.stdout + r.stderr)
    fails = [l[len("FAIL: "):][:90] for l in r.stdout.splitlines() if l.startswith("FAIL: ")]
    tally = [l for l in r.stdout.splitlines() if l.startswith("D3:")]
    verdict = "KILLED" if (r.returncode != 0 and tally) else ("SURVIVED" if r.returncode == 0 else "CRASHED")
    return f"{name}: {verdict} rc={r.returncode} {tally} failing: {fails}"

if __name__ == "__main__":
    clone, scratch, vl = sys.argv[1:4]
    names = sys.argv[4:] or list(MUTANTS)
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for line in ex.map(lambda n: run(n, clone, scratch, vl), names):
            print(line, flush=True)
