#!/usr/bin/env python3
"""Reviewer probe (R679-1, issue #193), wire level: a parked owed Leave for a
stream_id meeting a new sink settled on the same stream_id, through the real
decoder, listener FSMs, encoder and slot pool of tb/srp_top, with the suite's
own Milan v1.2 4.2.7.2.2 PeerRegistrar model fed every DUT MSRP frame.

Usage: probe_parked_leave_wire.py <exported-tree>
Edits <tree>/tb/srp_top/sim_main.cpp of a DISPOSABLE exported copy only; run
`make RUN_ARGS=share` there. Prints "PROBE-W:" lines with every DUT frame
carrying the value (hex) and a CHECK "PW<n>:" requiring that the peer
registrar never deregisters the value while the joiner sink wants it.
"""
import pathlib
import sys

tree = pathlib.Path(sys.argv[1])
f = tree / "tb" / "srp_top" / "sim_main.cpp"
src = f.read_text()

call_anchor = "      check_ready_with_asking_failed_is_ready_failed_on_the_wire();\n    }\n"
assert src.count(call_anchor) == 1
src = src.replace(call_anchor,
                  "      check_ready_with_asking_failed_is_ready_failed_on_the_wire();\n"
                  "      probe_parked_leave_then_new_sink(1, 0);\n"
                  "      probe_parked_leave_then_new_sink(0, 1);\n"
                  "    }\n")

body = r'''
  // ==== reviewer probe: parked owed Leave vs a new sink on the value ====
  void probe_parked_leave_then_new_sink(int parker, int joiner) {
    static constexpr uint64_t SIDY = 0x1122334455660009ULL;
    static constexpr uint64_t DAY  = 0x91E0F0112239ULL;
    h.reset();
    d->link_up_i = 1; h.idle(10);
    (void)h.wait_any(true, 1000);
    h.op(OP_DECL_LS, parker, SIDX, DAX, 2, 0, 0, DECL_READY);
    h.sync();
    Msg adv{1, 25, false, {Vec{false, 1,
            fv_talker(SIDX, DAX, 2, 0x0100, 1, 3, 1, 0x00012345),
            {EV_JOININ}, {}}}};
    const size_t from0 = h.archive.size();
    h.feed(mrpdu_body(true, {adv}), true);
    h.idle(10);
    h.run_ms(1500);
    PeerRegistrar peer;
    size_t from = from0;
    peer_sees(peer, from);
    const int st_before = peer.st;
    h.sync();
    const size_t at_rebind = h.archive.size();
    // the parker alone re-binds to another stream: its applicant owes Lv for
    // SIDX and is parked (issue #188); then, before the next tx!, the joiner
    // settles on SIDX and the talker's next Advertise registers it
    h.op(OP_DECL_LS, parker, SIDY, DAY, 2, 0, 0, DECL_READY);
    h.op(OP_DECL_LS, joiner, SIDX, DAX, 2, 0, 0, DECL_READY);
    h.feed(mrpdu_body(true, {adv}), true);
    h.idle(10);
    const int joiner_decl_early = h.ls_decl(joiner);
    h.run_ms(2500);
    peer_sees(peer, from);
    int n_frames = 0;
    for (size_t i = at_rebind; i < h.archive.size(); i++) {
      const auto& fr = h.archive[i];
      if (fr.size() <= 13 || ((fr[12] << 8) | fr[13]) != 0x22EA) continue;
      if (listener_values(fr, SIDX) == 0) continue;
      if (n_frames++ >= 3) continue;
      printf("PROBE-W: parker %d joiner %d frame at %u ms, %d values for SIDX:",
             parker, joiner, static_cast<unsigned>(h.archive_ms[i]),
             listener_values(fr, SIDX));
      for (auto b : fr) printf(" %02x", b);
      printf("\n");
    }
    printf("PROBE-W: parker %d joiner %d: peer before %d, after %d, deregs %d, "
           "Lv %d, joiner decl early %d now %d\n", parker, joiner, st_before,
           peer.st, peer.deregs, peer.lvs, joiner_decl_early, h.ls_decl(joiner));
    CHECK(st_before == PeerRegistrar::kIn && peer.deregs == 0
          && peer.st == PeerRegistrar::kIn && h.ls_decl(joiner) == DECL_READY,
          "PW%d: parker %d re-binds away, joiner %d settles on the value before "
          "the next tx!: a Milan peer Registrar never deregisters it while the "
          "joiner wants it (before %d, after %d, deregs %d, Lv %d)",
          1 + parker, parker, joiner, st_before, peer.st, peer.deregs, peer.lvs);
  }
'''
anchor = "  // Ready (sink 0, VLAN 2) with AskingFailed (sink 1, VLAN 3, its talker\n"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)
f.write_text(src)
print("wire probe inserted into", f)
