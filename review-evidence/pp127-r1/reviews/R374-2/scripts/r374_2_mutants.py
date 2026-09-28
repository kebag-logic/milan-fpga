"""Round 2 reviewer mutants. Usage: r374_2_mutants.py <head_tree> <dst_root> [names...]
The edits are the round-1 reviewer edits verbatim (textual, each must match
exactly once). Each mutant: fresh copy of hdl/ + tb/, one edit, reviewer
probes installed, then the FULL default srp_top suite (the committed entry
point, all groups) and probes r374r3..r374r5. Simulator: $VERILATOR
(default: pinned wrapper capped at 8 jobs)."""
import pathlib, shutil, subprocess, sys, json, os
SRC = pathlib.Path(sys.argv[1]).resolve(); DST = pathlib.Path(sys.argv[2]).resolve()
HERE = pathlib.Path(__file__).resolve().parent
T = "hdl/srp/KL_srp_top.sv"; E = "hdl/srp/KL_srp_encoder.sv"; TK = "hdl/srp/KL_srp_talker_fsm.sv"
MUT = {
 # restore the timer-expiry registrar pulse (in addition to sLA)
 "my-expiry-pulse": [(T, "  logic       la_msrp_pend_r;  // timer intent, not a registrar event\n",
                        "  logic       la_msrp_pend_r;  // timer intent, not a registrar event\n  logic       my_exp_r;\n"),
                     (T, "      la_msrp_pend_r    <= 1'b0;\n      join_msrp_pend_r  <= 1'b0;\n",
                         "      la_msrp_pend_r    <= 1'b0;\n      my_exp_r <= 1'b0;\n      join_msrp_pend_r  <= 1'b0;\n"),
                     (T, "      p_la_mvrp_r  <= 1'b0;\n      enc_join_r   <= 2'b00;\n",
                         "      p_la_mvrp_r  <= 1'b0;\n      my_exp_r <= 1'b0;\n      enc_join_r   <= 2'b00;\n"),
                     (T, "            la_msrp_pend_r <= 1'b1;  // wait for a supported sLA opportunity\n",
                         "            la_msrp_pend_r <= 1'b1;  // wait for a supported sLA opportunity\n            my_exp_r <= 1'b1;\n"),
                     (T, "      .leaveall_own_i      (p_la_msrp_w),\n", "      .leaveall_own_i      (p_la_msrp_w || my_exp_r),\n"),
                     (T, "      .leaveall_own_i          (p_la_msrp_w),\n", "      .leaveall_own_i          (p_la_msrp_w || my_exp_r),\n")],
 # peer LeaveAll on the join-cadence clock no longer blocks the prepared round
 "my-join-edge-peer": [(T, "        if (la_msrp_pend_r && !(|dec_la_msrp_w)) begin\n", "        if (la_msrp_pend_r) begin\n")],
 # a canceled preparation also consumes a newer timer intent
 "my-cancel-eats-new-intent": [(T, "        if (!la_cancel_r) la_msrp_pend_r <= 1'b0;\n", "        la_msrp_pend_r <= 1'b0;\n")],
 # same-edge peer does not block the sLA strobe
 "my-edge-cancel-lost": [(E, "&& ((st_r == E_COLLECT) || la_act_r) && !la_cancel_i;", "&& ((st_r == E_COLLECT) || la_act_r);")],
 # registrar: own/peer LeaveAll outranks a same-edge Listener Leave
 "my-la-outranks-leave": [(TK, "        end else if (reg_rx_hit_w[s] && (evt_mrp_event_i == 3'(SRP_EV_LV))) begin\n",
                              "        end else if (reg_rx_hit_w[s] && !leaveall_any_w && (evt_mrp_event_i == 3'(SRP_EV_LV))) begin\n")],
 # join cadence during la_wait is dropped instead of coalesced
 "my-drop-join-during-wait": [(T, "            if (rnd_act_r || la_wait_r) join_msrp_pend_r <= 1'b1;\n",
                                  "            if (rnd_act_r) join_msrp_pend_r <= 1'b1;\n")],
 # accepted preparation does not start the applicant walks
 "my-no-walk-at-sLA": [(T, "  assign join_fsm_w = p_join_fsm_r || la_done_w;\n", "  assign join_fsm_w = p_join_fsm_r;\n")],
 # reuse of a canceled reservation keeps LeaveAll flags despite a same-edge cancel
 "my-reuse-flags-ignore-cancel": [(E, "          if (la_prepare_i) begin\n            la_act_r <= !la_cancel_i;\n",
                                      "          if (la_prepare_i) begin\n            la_act_r <= 1'b1;\n")],
}
names = sys.argv[3:] or list(MUT)
res = {}
for n in names:
    d = DST / n
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    for sub in ("hdl", "tb"): shutil.copytree(SRC / sub, d / sub)
    for f, a, b in MUT[n]:
        p = d / f; s = p.read_text()
        assert s.count(a) == 1, (n, f, a)
        p.write_text(s.replace(a, b))
    subprocess.run(["python3", str(HERE / "install_probe.py"), str(d)], check=True)
    log = d / "suite.log"
    with open(log, "w") as fh:
        subprocess.run([str(HERE / "run_suite.sh"), str(d), "srp_top", ""], stdout=fh, stderr=subprocess.STDOUT)
    txt = log.read_text()
    binp = d / "tb/srp_top/obj_dir/Vsrp_top_sim"
    tally = [l for l in txt.splitlines() if " checks: " in l]
    fails = [l for l in txt.splitlines() if l.startswith("FAIL: ")]
    probes = {}
    for g in ("r374r3", "r374r4", "r374r5"):
        if binp.exists():
            pr = subprocess.run([str(binp), g], cwd=d / "tb/srp_top", capture_output=True, text=True)
            probes[g] = [pr.returncode] + [l for l in pr.stdout.splitlines() if "checks:" in l or l.startswith("FAIL")]
    res[n] = dict(build=binp.exists(), tally=tally[-1:], exit=[l for l in txt.splitlines() if l.startswith("EXIT=")],
                  fail_lines=fails, probes=probes)
    print(n, json.dumps(dict(tally=tally[-1:], fails=len(fails), names=sorted({l[6:].split(":")[0] for l in fails}), probes={k: v[:2] for k, v in probes.items()})), flush=True)
    shutil.copyfile(log, DST / (n + ".suite.log"))
json.dump(res, open(DST / ("results-" + "-".join(names) + ".json"), "w"), indent=1)
