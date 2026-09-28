"""Reviewer-planted RTL mutants. Usage: r374_mutants.py <src_tree> <dst_root> [names...]
Each mutant: a fresh copy of hdl/ + tb/ with exactly one textual edit (each
replacement must match exactly once), then the full srp_top suite plus the
reviewer probe group(s) run with the pinned simulator."""
import pathlib, shutil, subprocess, sys, hashlib, json
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
VER = "$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator"
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
    r = subprocess.run([str(HERE / "run_suite.sh"), str(d), "srp_top", ""], stdout=open(log, "w"), stderr=subprocess.STDOUT, timeout=3000)
    txt = log.read_text()
    ok_build = "Vsrp_top_sim" in txt and (d / "tb/srp_top/obj_dir/Vsrp_top_sim").exists()
    tally = [l for l in txt.splitlines() if " checks: " in l]
    fails = [l for l in txt.splitlines() if l.startswith("FAIL: ")]
    names_failed = sorted({l[6:].split(":")[0] for l in fails})
    probes = {}
    for g in ("r374r3", "r374r4"):
        pr = subprocess.run([str(d / "tb/srp_top/obj_dir/Vsrp_top_sim"), g], cwd=d / "tb/srp_top", capture_output=True, text=True, timeout=1200) if ok_build else None
        probes[g] = (pr.returncode, [l for l in pr.stdout.splitlines() if "R374" in l or "checks:" in l or l.startswith("FAIL")]) if pr else None
    res[n] = dict(build=ok_build, tally=tally[-1:] , suite_exit=[l for l in txt.splitlines() if l.startswith("EXIT=")], fail_lines=len(fails), failed_names=names_failed[:40], probes=probes)
    print(n, json.dumps(res[n]), flush=True)
out = DST / ("results-" + "-".join(names) + ".json")
json.dump(res, open(out, "w"), indent=1)
