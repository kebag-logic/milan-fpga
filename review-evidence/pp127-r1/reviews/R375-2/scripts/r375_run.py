#!/usr/bin/env python3
"""Reviewer (R375-2) probe and mutant runner for processor PR #130.

Round 2: re-targeted at exact head 00b5c6c9 (its sim_main.cpp already records
join_cycles, gates event history on rst_n, and adds the guards group), and the
full-suite run of each mutant now includes the committed O1..O7 guards.

Builds disposable trees under <packet>/scratch/runs/<label>/ from extracted
exact-head (and base) sources, patches a scratch copy of tb/srp_top/sim_main.cpp
with scripts/r375_probes.inc, optionally applies one RTL mutant, builds once
with the pinned simulator and runs the requested groups. Never touches the
review clone.

usage: r375_run.py LABEL[,LABEL...] [--jobs N]
  LABEL: head | base | <mutant name from MUTANTS>
"""
import argparse
import concurrent.futures as cf
import os
from pathlib import Path
import shutil
import subprocess

PKT = Path(__file__).resolve().parents[1]
HEAD = PKT / "scratch" / "head"
BASE = PKT / "scratch" / "base"
RUNS = PKT / "scratch" / "runs"
RCPT = PKT / "receipts" / "runs"
VERILATOR = os.environ.get(
    "R375_VERILATOR",
    "$VALIDATION_STORAGE/pp127-manager-00b5c6c9/pinned-tool-bin/verilator")
INC = (PKT / "scripts" / "r375_probes.inc").read_text()
INC2 = (PKT / "scripts" / "r375_probes2.inc").read_text()

TOP = "hdl/srp/KL_srp_top.sv"
ENC = "hdl/srp/KL_srp_encoder.sv"
LS = "hdl/srp/KL_srp_listener_fsm.sv"

# name -> (edits, groups to run). Groups: "" = full existing suite,
# phases/edge/peer/congestion = author groups, r375 = reviewer probes.
MUTANTS = {
    # Restore the timer-expiry registrar/applicant pulse IN ADDITION to the
    # new acceptance path (the pre-fix behaviour for aging at expiry).
    "r-expiry-pulse-restored": ([
        (TOP, "  assign join_fsm_w = p_join_fsm_r || la_done_w;",
              "  assign join_fsm_w = p_join_fsm_r || la_done_w;\n  logic r375_exp_w;"),
        (TOP, ".leaveall_own_i      (p_la_msrp_w),", ".leaveall_own_i      (p_la_msrp_w || r375_exp_w),"),
        (TOP, ".leaveall_own_i          (p_la_msrp_w),", ".leaveall_own_i          (p_la_msrp_w || r375_exp_w),"),
        (TOP, "  assign tf_pop_w[0] =",
              "  assign r375_exp_w = cad_hit_w && (cad_exp_ix_w == CAD_LA_MSRP_C);\n  assign tf_pop_w[0] ="),
    ], ["", "r375"]),
    # Cancel only on the decode strobe, dropping the latched cancellation.
    "r-cancel-latch-dropped": ([
        (TOP, ".la_cancel_i    (la_cancel_r || (|dec_la_msrp_w)),", ".la_cancel_i    ((|dec_la_msrp_w)),"),
    ], ["", "r375"]),
    # A canceled acceptance consumes a newer timer intent.
    "r-cancel-consumes-new-intent": ([
        (TOP, "        if (!la_cancel_r) la_msrp_pend_r <= 1'b0;", "        la_msrp_pend_r <= 1'b0;"),
    ], ["", "r375"]),
    # Join-start ignores a same-cycle peer LeaveAll.
    "r-join-start-guard-dropped": ([
        (TOP, "if (la_msrp_pend_r && !(|dec_la_msrp_w)) begin", "if (la_msrp_pend_r) begin"),
    ], ["", "r375"]),
    # Sink plane: own LeaveAll outranks a same-edge received Talker event.
    "r-sink-receive-priority-lost": ([
        (LS, "        if (reg_rx_hit_w[s] && rx_registering_w) begin\n          // registering event",
             "        if (leaveall_any_w[s] && (reg_r[s] == R_IN_C)) begin\n          reg_r[s] <= R_LV_C; tpend_r[s] <= T_ARM_C;\n"
             "        end else if (reg_rx_hit_w[s] && rx_registering_w) begin\n          // registering event"),
    ], ["", "r375"]),
    # Cadence ticks during a blocked round are dropped instead of coalesced.
    "r-join-coalesce-dropped": ([
        (TOP, "            if (rnd_act_r || la_wait_r) join_msrp_pend_r <= 1'b1;", "            // tick dropped"),
    ], ["", "r375"]),
    # LeaveAll-only emission for an empty accepted round removed.
    "r-la-only-emission-lost": ([
        (ENC, "            else if (la_act_r) begin\n              run_type_r <= ATTR_TALKER_ADV_C;",
              "            else if (1'b0) begin\n              run_type_r <= ATTR_TALKER_ADV_C;"),
    ], ["", "r375"]),
    # Walk pushes blocked while collecting (collect state counted as busy).
    "r-collect-blocks-pushes": ([
        (ENC, "  assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)",
              "  assign busy_app_w  = (st_r != E_IDLE)"),
    ], ["", "r375"]),
    # Interim drain not requested on the acceptance edge.
    "r-accept-edge-drain-lost": ([
        (TOP, "if ((rnd_act_r || la_done_w) && enc_msrp_full_w", "if (rnd_act_r && enc_msrp_full_w"),
    ], ["", "r375"]),
    # Reuse of a reserved slot does not raise the action.
    "r-reuse-without-action": ([
        (ENC, "assign la_tx_o = la_prepare_done_o && ((st_r == E_COLLECT) || la_act_r) && !la_cancel_i;",
              "assign la_tx_o = la_prepare_done_o && la_act_r && !la_cancel_i;"),
    ], ["", "r375"]),
    # MVRP drain may start on the same cycle as an own preparation.
    "r-mvrp-start-during-prepare": ([
        (ENC, "assign start1_w = (st_r == E_IDLE) && !la_prepare_i && !start0_w",
              "assign start1_w = (st_r == E_IDLE) && !start0_w"),
    ], ["", "r375"]),
}


def patch_tb(dest, base_rtl):
    sim = dest / "tb" / "srp_top" / "sim_main.cpp"
    s = sim.read_text()
    reps = [
        ("  std::vector<uint32_t> la_times;\n",
         "  std::vector<uint32_t> la_times;\n  std::vector<uint64_t> wait_cycles;\n  std::vector<uint64_t> fin_cycles;\n"),
        ("      if (d->dbg_rx_event_o) rx_cycles.push_back(t);\n",
         "      if (d->dbg_rx_event_o) rx_cycles.push_back(t);\n"
         "      if (d->dbg_la_wait_o) wait_cycles.push_back(t);\n"),
        ("        finished = true;\n", "        finished = true; fin_cycles.push_back(t);\n"),
        ("rx_cycles.clear();\n    d->block_alloc_i = 0;",
         "rx_cycles.clear(); wait_cycles.clear(); fin_cycles.clear();\n    d->block_alloc_i = 0;"),
        ("  void bring_up_the_port() {\n", INC + INC2 + "\n  void bring_up_the_port() {\n"),
        ('    if (!*group || !strcmp(group,"guards")) check_leaveall_guards();\n',
         '    if (!*group || !strcmp(group,"guards")) check_leaveall_guards();\n'
         '    if (!strcmp(group,"r375")) r375_all(false);\n'
         '    if (!strcmp(group,"r375base")) r375_all(true);\n'
         '    if (!strcmp(group,"r375b")) r375_parked_bounds();\n'),
        ('      && strcmp(group,"guards")) return 2;',
         '      && strcmp(group,"guards")\n      && strcmp(group,"r375") && strcmp(group,"r375base")'
         '\n      && strcmp(group,"r375b")) return 2;'),
    ]
    for a, b in reps:
        assert s.count(a) == 1, ("tb anchor", a[:60], s.count(a))
        s = s.replace(a, b)
    sim.write_text(s)
    if base_rtl:
        w = dest / "tb" / "srp_top" / "srp_top_wrap.sv"
        t = w.read_text()
        for a, b in [
            ("assign dbg_la_pending_o = u_dut.la_msrp_pend_r;", "assign dbg_la_pending_o = 1'b0;"),
            ("assign dbg_prepare_done_o = u_dut.la_done_w;", "assign dbg_prepare_done_o = 1'b0;"),
            ("assign dbg_la_action_o = u_dut.p_la_msrp_w;", "assign dbg_la_action_o = u_dut.p_la_msrp_r;"),
            ("assign dbg_la_wait_o = u_dut.la_wait_r;", "assign dbg_la_wait_o = 1'b0;"),
            ("assign dbg_enc_state_o = u_dut.u_encoder.st_r;", "assign dbg_enc_state_o = 5'(u_dut.u_encoder.st_r);"),
            ("assign dbg_join_tick_o = u_dut.join_fsm_w;", "assign dbg_join_tick_o = u_dut.p_join_fsm_r;"),
        ]:
            assert t.count(a) == 1, ("wrap anchor", a)
            t = t.replace(a, b)
        w.write_text(t)


def build_tree(label):
    dest = RUNS / label
    if dest.exists():
        shutil.rmtree(dest)
    base_rtl = label == "base"
    shutil.copytree((BASE if base_rtl else HEAD) / "hdl", dest / "hdl")
    for suite in ("common", "srp_top"):
        shutil.copytree(HEAD / "tb" / suite, dest / "tb" / suite,
                        ignore=shutil.ignore_patterns("obj_*"))
    patch_tb(dest, base_rtl)
    # build parallelism is already capped at 2 by prepare_trees.sh
    mk = dest / "tb" / "srp_top" / "Makefile"
    assert mk.read_text().count("--build -j 2") == 1
    if label in MUTANTS:
        for path, anchor, repl in MUTANTS[label][0]:
            f = dest / path
            src = f.read_text()
            assert src.count(anchor) == 1, (label, anchor[:60], src.count(anchor))
            f.write_text(src.replace(anchor, repl))
    return dest


def groups_for(label):
    if label == "head":
        return ["r375", "r375b"]
    if label == "base":
        return ["r375base"]
    return MUTANTS[label][1]


def run_label(label):
    dest = build_tree(label)
    RCPT.mkdir(parents=True, exist_ok=True)
    tbdir = dest / "tb" / "srp_top"
    blog = RCPT / f"{label}.build.log"
    with blog.open("w") as out:
        rc = subprocess.run(["make", "-C", str(tbdir), f"VERILATOR={VERILATOR}",
                             "RUN_ARGS=--build-only-marker"], stdout=out,
                            stderr=subprocess.STDOUT, timeout=3000).returncode
    exe = tbdir / "obj_dir" / "Vsrp_top_sim"
    if not exe.exists():
        return f"{label}: BUILD FAILED (see {blog.name})"
    lines = []
    for g in groups_for(label):
        tag = g or "full"
        log = RCPT / f"{label}.{tag}.log"
        with log.open("w") as out:
            r = subprocess.run([str(exe)] + ([g] if g else []), cwd=tbdir, stdout=out,
                               stderr=subprocess.STDOUT, timeout=5400)
        txt = log.read_text()
        summ = [l for l in txt.splitlines() if " checks: " in l]
        fails = sorted({l.split(":", 2)[1].strip() for l in txt.splitlines() if l.startswith("FAIL:")})
        lines.append(f"{label} [{tag}] rc={r.returncode} {summ[-1] if summ else 'NO SUMMARY'} "
                     f"failing_ids={','.join(fails)}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("labels")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    labels = list(MUTANTS) if a.labels == "all-mutants" else a.labels.split(",")
    with cf.ThreadPoolExecutor(max_workers=min(a.jobs, 4)) as ex:
        for res in ex.map(run_label, labels):
            print(res, flush=True)


if __name__ == "__main__":
    main()
