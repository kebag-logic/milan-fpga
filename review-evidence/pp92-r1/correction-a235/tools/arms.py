#!/usr/bin/env python3
"""Failing-arm runner. Each arm runs in its own disposable extract of a
tree-ish (git archive), never in the lane, so no restore step is needed.

usage: arms.py <repo> <tree-ish> <scratch> <logdir> [NAME ...]

Each row: NAME, suite, file, OLD, NEW. OLD must occur exactly once; a
tuple of OLDs and a tuple of NEWs make an arm of several edits, in order. The
acmp_nvm, lsn_admit and nvm_port suites run their `run` target; pp_top runs
its first (all-section) build only, the one that carries section BW. An arm
is KILLED when the bench exits non-zero with at least one FAIL line and a
tally; a build failure is reported as such, never as killed. VERILATOR names
the simulator.
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

FIX_NEW = ("  assign c1_diff_w  = (c1_vld_r != valid_r[c1_sink_r])\n"
           "                    || (c1_vld_r && (SHW_W_C'(c1_proj_r) != cmp_data_w));")
FIX_OLD = ("  assign c1_diff_w  = (SHW_W_C'(c1_proj_r) != cmp_data_w)\n"
           "                    || (c1_vld_r != valid_r[c1_sink_r]);")
DONE_NEW = "assign restore_done_o = nvm_walk_done_w && lsn_released_w;"
BUSY_NEW = ("  assign restore_busy_o = nvm_walk_busy_w\n"
            "                          || (nvm_walk_done_w && !lsn_released_w);")

ARMS = [
    # --- this round's corrections --------------------------------------------
    ("F1-compare", "acmp_nvm", SH, FIX_NEW, FIX_OLD),
    ("F1-compare-top", "pp_top", SH, FIX_NEW, FIX_OLD),
    ("F2-done-no-release", "pp_top", TOP, DONE_NEW,
     "assign restore_done_o = nvm_walk_done_w;"),
    ("F2-busy-gap", "pp_top", TOP, BUSY_NEW, "  assign restore_busy_o = nvm_walk_busy_w;"),
    # --- the arms published for #92/#93, re-run at this round's counts ----------
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
    ("B02", "acmp_nvm", SH,
     ("&& (nvm_err_cause_i != CAUSE_UNFRAMED_C);", "&& (nvm_err_cause_i == CAUSE_UNFRAMED_C))"),
     ("&& 1'b0;", ")")),
    ("B03", "acmp_nvm", AR, "      drain_r <= 1'b1;", "      drain_r <= 1'b0;"),
    ("BA1", "acmp_nvm", SH, "assign nvm_abort_o = rs_tmo_w && (hs_r == H_RS_STREAM);",
     "assign nvm_abort_o = 1'b0;"),
    ("BC1", "acmp_nvm", SH, "rs_cause_r <= rs_tmo_w  ? RS_CAUSE_DEADLINE_C",
     "rs_cause_r <= 1'b1      ? RS_CAUSE_TORN_C"),
    ("A01", "acmp_nvm", AR, "assign m0_busy_o      = p_busy_i || (own_r == O_M1) || iss1_w;",
     "assign m0_busy_o      = p_busy_i || (own_r == O_M1);"),
    ("B04", "acmp_nvm", SH,
     ("&& (nvm_err_cause_i != CAUSE_UNFRAMED_C);", "&& (nvm_err_cause_i == CAUSE_UNFRAMED_C))"),
     (";", "&& 1'b0)")),
    ("LG01-top", "pp_top", AD, "      own_r <= 1'b1;", "      own_r <= 1'b0;"),
    ("B01-top", "pp_top", SH,
     "assign rs_tmo_w   = rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1));",
     "assign rs_tmo_w   = 1'b0;"),
    ("B03-top", "pp_top", AR, "      drain_r <= 1'b1;", "      drain_r <= 1'b0;"),
]

PP_TOP_FIRST = ("\narm-first: fixture-guards ltn_rom.hex ucode.hex\n"
                "\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n"
                "\t./obj_dir/Vpp_top_sim\n")


def run_one(repo, rev, scratch, logdir, row, verilator):
    name, suite, rel, old, new = row
    d = os.path.join(scratch, "arm", name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    subprocess.run(f"git -C {repo} archive {rev} | tar -x -C {d}", shell=True, check=True)
    if rel:
        path = os.path.join(d, rel)
        text = open(path).read()
        olds = old if isinstance(old, tuple) else (old,)
        news = new if isinstance(new, tuple) else (new,)
        for o, n in zip(olds, news):
            if text.count(o) != 1:
                return f"{name}: ANCHOR occurs {text.count(o)} times"
            text = text.replace(o, n)
        open(path, "w").write(text)
    tdir = os.path.join(d, "tb", suite)
    target = "run"
    if suite == "pp_top":
        with open(os.path.join(tdir, "Makefile"), "a") as f:
            f.write(PP_TOP_FIRST)
        target = "arm-first"
    p = subprocess.run(["make", target, f"VERILATOR={verilator}"], cwd=tdir,
                       capture_output=True, text=True, timeout=3600)
    out = p.stdout + p.stderr
    log = os.path.join(logdir, f"arm-{suite}-{name}.log")
    with open(log, "w") as f:
        f.write(f"# arm {name} on {rel or '(none)'} at {rev}\n# - {old!r}\n# + {new!r}\n")
        f.write(f"# make {target} in tb/{suite}: exit {p.returncode}\n")
        f.write(out)
    tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL|\d+ checks, \d+ failures?", out)
    fails = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
    verdict = ("KILLED" if p.returncode != 0 and fails and tally else
               "PASSES" if p.returncode == 0 else "BUILD/OTHER")
    first = fails[0][:140] if fails else ""
    subprocess.run(["rm", "-rf", d], check=False)
    return (f"{name:20s} {suite:9s} exit {p.returncode} "
            f"{tally[-1] if tally else 'NO TALLY':30s} {len(fails):4d} FAIL  {verdict}  {first}")


def main():
    repo, rev, scratch, logdir = sys.argv[1:5]
    only = sys.argv[5:]
    verilator = os.environ.get("VERILATOR", "verilator")
    os.makedirs(logdir, exist_ok=True)
    rows = [r for r in ARMS if not only or r[0] in only]
    if "BASELINE-top" in only:
        rows.insert(0, ("BASELINE-top", "pp_top", "", "", ""))
    if "BASELINE" in only:
        rows.insert(0, ("BASELINE", "acmp_nvm", "", "", ""))
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("JOBS", "6"))) as ex:
        futs = [ex.submit(run_one, repo, rev, scratch, logdir, r, verilator) for r in rows]
        for f in futs:
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
