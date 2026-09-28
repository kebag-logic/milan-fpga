"""Base RTL (16be6768) + head srp_top testbench, with the head-only probe
taps mapped to their base equivalents (the expiry pulse is the action)."""
import pathlib, shutil, sys
base = pathlib.Path(sys.argv[1]); head = pathlib.Path(sys.argv[2]); dst = pathlib.Path(sys.argv[3])
shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
shutil.copytree(base / "hdl", dst / "hdl"); shutil.copytree(head / "tb", dst / "tb")
w = dst / "tb/srp_top/srp_top_wrap.sv"; s = w.read_text()
rep = {
 "assign dbg_la_pending_o = u_dut.la_msrp_pend_r;": "assign dbg_la_pending_o = 1'b0;",
 "assign dbg_prepare_done_o = u_dut.la_done_w;": "assign dbg_prepare_done_o = u_dut.p_la_msrp_r;",
 "assign dbg_la_action_o = u_dut.p_la_msrp_w;": "assign dbg_la_action_o = u_dut.p_la_msrp_r;",
 "assign dbg_la_wait_o = u_dut.la_wait_r;": "assign dbg_la_wait_o = 1'b0;",
 "assign dbg_enc_state_o = u_dut.u_encoder.st_r;": "assign dbg_enc_state_o = {1'b0, u_dut.u_encoder.st_r};",
 "assign dbg_join_tick_o = u_dut.join_fsm_w;": "assign dbg_join_tick_o = u_dut.p_join_fsm_r;",
}
for a, b in rep.items():
    assert s.count(a) == 1, a
    s = s.replace(a, b)
w.write_text(s)
