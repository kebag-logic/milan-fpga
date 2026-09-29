#!/usr/bin/env python3
"""Disposable probe (R399-1): can the talker streaming licence's MVRP term
(KL_srp_talker_fsm vid_ok_w) stick closed? Adds a read-only wrapper output for
vid_ok_w and one probe group to a scratch copy of tb/srp_top; no RTL change.
Usage: probe_licence.py <pristine tree> <work dir>"""
import pathlib, shutil, subprocess, sys

src, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

PROBE = r'''
  // R399 probe: the MVRP licence term across the events that could strand it
  bool vok(int s) const { return ((d->dbg_vid_ok_o >> s) & 1) != 0; }
  // run until vid_ok[s] rises (bounded); ms waited, or -1
  int await_vok(int s, int guard_ms) {
    const uint32_t t0 = d->now_ms_o;
    for (long n = long(guard_ms) * MS_CYC; n > 0 && !vok(s); n--) h.cycle();
    return vok(s) ? int(d->now_ms_o - t0) : -1;
  }
  // hold for ms; false if vid_ok[s] ever drops
  bool holds(int s, int ms) {
    bool ok = true;
    for (long n = long(ms) * MS_CYC; n > 0; n--) { h.cycle(); ok &= vok(s); }
    return ok;
  }
  void probe_licence() {
    h.reset(); d->link_up_i = 1; h.idle(10);
    h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 2, 29, 1);
    int w = await_vok(0, 400);
    printf("LICPROBE S0 first_declare_wait_ms=%d\n", w);
    CHECK(w >= 0 && w <= 240, "S0: VID 2 term rises within one join tick (%d ms)", w);
    // S1: 45 s of own MSRP/MVRP LeaveAll cycles plus a peer MVRP LeaveAll every 3 s
    bool s1 = true;
    for (int k = 0; k < 15; k++) { h.feed(peer_mvrp_leaveall(2), false); s1 &= holds(0, 3000); }
    printf("LICPROBE S1 held_through_leavealls=%d mvrp_actions=%zu\n", int(s1), h.mvrp_action_cycles.size());
    CHECK(s1, "S1: the term never drops through own and peer LeaveAll cycles");
    // S2: a sink shares VID 2 and leaves again: the talker's term stays
    h.op(OP_DECL_LS, 0, peer_sid(0), peer_da(0), 2, 0, 0, DECL_READY);
    bool s2 = holds(0, 500);
    h.op(OP_WDRW_LS, 0);
    s2 &= holds(0, 1500);
    CHECK(s2, "S2: a co-user joining and leaving VID 2 never drops the term");
    // S3: withdraw + immediate re-declare on the same VID
    h.op(OP_WDRW_TK, 0);
    h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 2, 29, 1);
    w = await_vok(0, 1500);
    printf("LICPROBE S3 redeclare_same_vid_wait_ms=%d\n", w);
    CHECK(w >= 0 && w <= 240, "S3: withdraw/re-declare on the same VID recovers within one join tick (%d ms)", w);
    // S4: VID 2 -> 7 -> 2
    for (int vid : {7, 2}) {
      h.op(OP_WDRW_TK, 0); h.run_ms(50);
      h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, vid, 29, 1);
      w = await_vok(0, 1500);
      printf("LICPROBE S4 move_to_vid=%d wait_ms=%d\n", vid, w);
      CHECK(w >= 0 && w <= 240, "S4: a VID move to %d recovers within one join tick (%d ms)", vid, w);
    }
    // S5: TX arbiter refuses for 1 s right at a fresh declaration: waits, then recovers
    h.op(OP_WDRW_TK, 0); h.run_ms(50);
    h.pause_tx = true;
    h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 5, 29, 1);
    bool closed = true;
    for (long n = 1000L * MS_CYC; n > 0; n--) { h.cycle(); closed &= !vok(0); }
    h.pause_tx = false;
    w = await_vok(0, 1500);
    printf("LICPROBE S5 closed_while_tx_refused=%d wait_after_release_ms=%d\n", int(closed), w);
    CHECK(closed && w >= 0 && w <= 240, "S5: no term while the arbiter refuses; recovers after (%d ms)", w);
    // S6: link down/up with the declaration held
    d->link_up_i = 0; h.run_ms(300); const bool down = vok(0);
    d->link_up_i = 1; w = await_vok(0, 1500);
    printf("LICPROBE S6 term_during_link_down=%d after_up_wait_ms=%d\n", int(down), w);
    CHECK(w >= 0, "S6: the term is present after link up (%d ms)", w);
    // S7 (behaviour record): four sinks on four other VIDs fill the table first
    h.reset(); d->link_up_i = 1; h.idle(10);
    for (int s = 0; s < 4; s++) h.op(OP_DECL_LS, s, peer_sid(s), peer_da(s), 10 + s, 0, 0, DECL_READY);
    h.run_ms(300);
    const unsigned errs0 = 0;
    (void)errs0;
    h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 2, 29, 1);
    w = await_vok(0, 1000);
    h.op(OP_WDRW_LS, 3); h.run_ms(300);
    const int w2 = await_vok(0, 3000);
    h.op(OP_WDRW_TK, 0); h.run_ms(50);
    h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 2, 29, 1);
    const int w3 = await_vok(0, 1000);
    printf("LICPROBE S7 table_full wait_ms=%d after_slot_freed_wait_ms=%d after_redeclare_wait_ms=%d vid_active=0x%x\n",
           w, w2, w3, unsigned(d->dbg_vid_active_o));
  }
'''

t = work / "tree"
if t.exists(): shutil.rmtree(t)
(t / "tb").mkdir(parents=True)
shutil.copytree(src / "hdl", t / "hdl")
shutil.copytree(src / "tb" / "common", t / "tb" / "common")
shutil.copytree(src / "tb" / "srp_top", t / "tb" / "srp_top", ignore=shutil.ignore_patterns("obj_*"))
cpp = t / "tb/srp_top/sim_main.cpp"
s = cpp.read_text()
s = s.replace("  // P: issue #108.", PROBE + "\n  // P: issue #108.", 1)
s = s.replace('if (!*group || !strcmp(group,"join")) check_mvrp_join_before_the_stream();',
              'if (!*group || !strcmp(group,"join")) check_mvrp_join_before_the_stream();\n'
              '    if (!strcmp(group,"licprobe")) probe_licence();', 1)
s = s.replace('&& strcmp(group,"timers") && strcmp(group,"join")) return 2;',
              '&& strcmp(group,"timers") && strcmp(group,"join") && strcmp(group,"licprobe")) return 2;', 1)
assert "probe_licence();" in s and '"licprobe")) return 2' in s
cpp.write_text(s)
w = t / "tb/srp_top/srp_top_wrap.sv"
v = w.read_text()
anchor = "    output logic [3:0]  dbg_vid_active_o,"
assert anchor in v
v = v.replace(anchor, "    output wire  [7:0]  dbg_vid_ok_o,\n" + anchor, 1)
v = v.replace("  assign dbg_la_redraw_o = draw_req_w;",
              "  assign dbg_la_redraw_o = draw_req_w;\n  assign dbg_vid_ok_o = u_dut.u_talker.vid_ok_w;", 1)
assert "dbg_vid_ok_o = u_dut" in v
w.write_text(v)
log = work / "licprobe.log"
with log.open("w") as f:
    rc = subprocess.run(["make", "-C", str(t / "tb/srp_top"), "RUN_ARGS=licprobe"],
                        stdout=f, stderr=subprocess.STDOUT).returncode
print("rc", rc)
