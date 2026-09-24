#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer mutant runner. Every mutant runs in its own disposable copy of
the reviewed commit (git archive), never in a checkout, so no restore step is
needed and jobs run in parallel.

usage: mutants.py <repo> <commit> <scratch> <receipts> [NAME ...]

Each row: NAME, suite, file, OLD, NEW. OLD must occur exactly once. The
acmp_nvm and lsn_admit suites run their `run` target; pp_top runs only its
first (full-section) build, the one that carries the BW cases. A mutant is
KILLED when the bench exits non-zero with at least one completed-scenario
FAIL line and a tally; a build failure is reported as such, never as killed.
"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys

SH = "hdl/acmp/KL_acmp_nvm_shadow.sv"
AD = "hdl/acmp/KL_pp_acmp_lsn_admit.sv"
AR = "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv"
TOP = "hdl/top/protocol_processor_top.sv"

MUTANTS = [
    # --- the published failing arms, re-run independently -----------------
    ("LG01", "acmp_nvm", AD, "      own_r <= 1'b1;", "      own_r <= 1'b0;"),
    ("LG02", "acmp_nvm", AD, "assign l_txn_valid_o  = p_txn_valid_i  && !own_r;",
     "assign l_txn_valid_o  = p_txn_valid_i;"),
    ("LG03", "acmp_nvm", AD, "assign p_txn_ready_o  = l_txn_ready_i  && !own_r;",
     "assign p_txn_ready_o  = l_txn_ready_i;"),
    ("LG02t", "acmp_nvm", AD, "assign l_tk_valid_o   = p_tk_valid_i   && !own_r;",
     "assign l_tk_valid_o   = p_tk_valid_i;"),
    ("LG03t", "acmp_nvm", AD, "assign p_tk_ready_o   = l_tk_ready_i   && !own_r;",
     "assign p_tk_ready_o   = l_tk_ready_i;"),
    ("LG04", "acmp_nvm", AD, "assign l_exp_valid_o = p_exp_valid_i && !own_r;",
     "assign l_exp_valid_o = p_exp_valid_i;"),
    ("LG05", "acmp_nvm", AD, "assign l_strm_valid_o = p_strm_valid_i && !own_r;",
     "assign l_strm_valid_o = p_strm_valid_i;"),
    ("LRdone", "acmp_nvm", AD, "assign drained_w = walk_done_i && !pre_valid_i",
     "assign drained_w = 1'b1 && !pre_valid_i"),
    ("B01", "acmp_nvm", SH,
     "assign rs_tmo_w   = rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1));",
     "assign rs_tmo_w   = 1'b0;"),
    ("B02", "acmp_nvm", SH, "&& (nvm_err_cause_i != CAUSE_UNFRAMED_C);", "&& 1'b0;"),
    ("B03", "acmp_nvm", AR, "      drain_r <= 1'b1;", "      drain_r <= 1'b0;"),
    ("BA1", "acmp_nvm", SH, "assign nvm_abort_o = rs_tmo_w && (hs_r == H_RS_STREAM);",
     "assign nvm_abort_o = 1'b0;"),
    ("BC1", "acmp_nvm", SH, "rs_cause_r <= rs_tmo_w  ? RS_CAUSE_DEADLINE_C",
     "rs_cause_r <= 1'b1      ? RS_CAUSE_TORN_C"),
    ("A01", "acmp_nvm", AR, "assign m0_busy_o      = p_busy_i || (own_r == O_M1) || iss1_w;",
     "assign m0_busy_o      = p_busy_i || (own_r == O_M1);"),
    ("LG01-top", "pp_top", AD, "      own_r <= 1'b1;", "      own_r <= 1'b0;"),
    ("B01-top", "pp_top", SH,
     "assign rs_tmo_w   = rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1));",
     "assign rs_tmo_w   = 1'b0;"),
    ("B03-top", "pp_top", AR, "      drain_r <= 1'b1;", "      drain_r <= 1'b0;"),
    # --- reviewer-owned extra mutants ---------------------------------------
    ("X-rel-busy", "acmp_nvm", AD, "&& !lsn_busy_i && !lsn_arm_i;", "&& !lsn_arm_i;"),
    ("X-rel-arm", "acmp_nvm", AD, "&& !lsn_busy_i && !lsn_arm_i;", "&& !lsn_busy_i;"),
    ("X-rel-busy-lsn", "lsn_admit", AD, "&& !lsn_busy_i && !lsn_arm_i;", "&& !lsn_arm_i;"),
    ("X-rel-pre-lsn", "lsn_admit", AD,
     "assign drained_w = walk_done_i && !pre_valid_i", "assign drained_w = walk_done_i"),
    ("X-drain-leak", "acmp_nvm", AR,
     "assign m0_rvalid_o    = (own_r == O_M0) && !drain_r && p_rvalid_i;",
     "assign m0_rvalid_o    = (own_r == O_M0) && p_rvalid_i;"),
    ("X-drain-done-leak", "acmp_nvm", AR,
     "assign m0_done_o      = (own_r == O_M0) && !drain_r && p_done_i;",
     "assign m0_done_o      = (own_r == O_M0) && p_done_i;"),
    ("X-tmo-off-by-one", "acmp_nvm", SH, "(rs_wd_r >= 32'(RS_TMO_CYC_P - 1))",
     "(rs_wd_r >= 32'(RS_TMO_CYC_P))"),
    ("X-no-req-stall", "acmp_nvm", SH,
     "assign rs_stall_w = ((hs_r == H_RS_REQ) && (nvm_busy_i || nvm_done_i || nvm_err_i))",
     "assign rs_stall_w = 1'b0"),
    ("X-top-done-no-release", "pp_top", TOP,
     "assign restore_done_o = nvm_walk_done_w && lsn_released_w;",
     "assign restore_done_o = nvm_walk_done_w;"),
    ("X-top-busy-gap", "pp_top", TOP,
     "  assign restore_busy_o = nvm_walk_busy_w\n                          || (nvm_walk_done_w && !lsn_released_w);",
     "  assign restore_busy_o = nvm_walk_busy_w;"),
    ("X-rel-busy-top", "pp_top", AD, "&& !lsn_busy_i && !lsn_arm_i;", "&& !lsn_arm_i;"),
    ("B04", "acmp_nvm", SH, "&& (nvm_err_cause_i != CAUSE_UNFRAMED_C);", ";"),
    ("B04b", "acmp_nvm", SH, "&& (nvm_err_cause_i == CAUSE_UNFRAMED_C))", "&& 1'b0)"),
    ("X-rel-arm-lsn", "lsn_admit", AD, "&& !lsn_busy_i && !lsn_arm_i;", "&& !lsn_busy_i;"),
    ("X-rel-both", "acmp_nvm", AD, "&& !lsn_busy_i && !lsn_arm_i;", ";"),
    ("X-rel-both-top", "pp_top", AD, "&& !lsn_busy_i && !lsn_arm_i;", ";"),
]

PP_TOP_PROBE = ("\nr278-first: fixture-guards ltn_rom.hex ucode.hex\n"
                "\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n"
                "\t./obj_dir/Vpp_top_sim\n")


def run_one(repo, commit, scratch, receipts, row, verilator):
    name, suite, rel, old, new = row
    d = os.path.join(scratch, "mut", name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    subprocess.run(f"git -C {repo} archive {commit} | tar -x -C {d}", shell=True, check=True)
    if name != "BASELINE":
        path = os.path.join(d, rel)
        text = open(path).read()
        if text.count(old) != 1:
            return f"{name}: ANCHOR occurs {text.count(old)} times"
        open(path, "w").write(text.replace(old, new))
    tdir = os.path.join(d, "tb", suite)
    target = "run"
    if suite == "pp_top":
        with open(os.path.join(tdir, "Makefile"), "a") as f:
            f.write(PP_TOP_PROBE)
        target = "r278-first"
    p = subprocess.run(["make", target, f"VERILATOR={verilator}"], cwd=tdir,
                       capture_output=True, text=True, timeout=3600)
    out = p.stdout + p.stderr
    log = os.path.join(receipts, f"mutant-{suite}-{name}.log")
    with open(log, "w") as f:
        f.write(f"# mutant {name} on {rel} at {commit}\n# - {old!r}\n# + {new!r}\n")
        f.write(f"# make {target} in tb/{suite}: exit {p.returncode}\n")
        f.write(out)
    tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL|\d+ checks, \d+ failures?", out)
    fails = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
    verdict = ("KILLED" if p.returncode != 0 and fails and tally else
               "SURVIVED" if p.returncode == 0 else "BUILD/OTHER")
    first = fails[0][:150] if fails else ""
    return (f"{name:22s} {suite:9s} exit {p.returncode} "
            f"{tally[-1] if tally else 'NO TALLY':32s} {len(fails):4d} FAIL  {verdict}  {first}")


def main():
    repo, commit, scratch, receipts = sys.argv[1:5]
    only = set(sys.argv[5:])
    verilator = os.environ.get("VERILATOR", "verilator")
    rows = [r for r in MUTANTS if not only or r[0] in only]
    if not only or "BASELINE" in only:
        rows = [("BASELINE", s, "", "", "") for s in ("pp_top",)] + rows
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(run_one, repo, commit, scratch, receipts, r, verilator)
                for r in rows]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
