#!/usr/bin/env python3
"""Reviewer probe: insert group `r488join` into a scratch copy of tb/srp_top/sim_main.cpp.

It reuses the head's own collision calibration and snapshot replay, but the
event decoded across the expiry clock is a registering JoinIn instead of Lv.
Required (802.1Q-2014 Table 10-4, expiry first, then rJoinIn! at MT -> IN):
every k ends IN with the registration published. Decoded before or on the
expiry clock: no ACTIVE edge / no TK (UN)REGISTERED pulse (renewal). Decoded
after it: one close then one re-registration. For the same-clock case only,
the run continues T-MRP-LEAVE + 200 ms to show the cancel of an already-fired
slot leaves no stale expiry. usage: probe_join_collision.py <tree>
"""
import sys
from pathlib import Path

METHOD = r'''
  void r488_join_collisions() {
    for (bool listener : {false, true}) for (bool own : {false, true})
      for (int fp : {DECL_READY, DECL_READYFAIL}) for (int target : {0, 7}) {
        collision_setup(own, fp, target);
        const uint64_t origin = h.t;
        const uint32_t limit = d->now_ms_o + LEAVE_TIME_MS + 10;
        while ((listener ? sink_reg(target) : source_reg(target)) != 0 && d->now_ms_o < limit)
          h.cycle();
        const uint64_t close_offset = h.t - origin;
        collision_setup(own, fp, target);
        const uint64_t calibrated_close = h.t + close_offset;
        while (h.t + 401 < calibrated_close) h.cycle();
        const H saved = h;
        const std::string snapshot = save_collision_state();
        int same = 0, before = 0, after = 0;
        for (int k = 0; k <= 400; ++k) {
          const uint64_t total = h.t;
          VerilatedRestore restore;
          restore.open(snapshot.c_str());
          restore >> *d;
          restore.close();
          h = saved;
          h.t = total;
          h.accept_cycle += total - saved.t;
          const uint64_t close = h.t + 401;
          const int stops = h.stop_cnt[target], starts = h.start_cnt[target];
          const int unregs = h.unreg_cnt[target], regs = h.reg_cnt[target];
          const int lrcs = h.lrc_cnt[target];
          const uint32_t end_ms = d->now_ms_o + 20;
          while (h.t + k < close) h.cycle();
          h.rx_cycles.clear();
          if (listener) talker_event(target, EV_JOININ);
          else listener_event(target, EV_JOININ, fp);
          long rel = 9999;
          for (uint64_t cycle : h.rx_cycles) rel = long(cycle + 1) - long(close);
          until_ms(end_ms);
          const int ds = h.stop_cnt[target] - stops, dst = h.start_cnt[target] - starts;
          const int du = h.unreg_cnt[target] - unregs, dr = h.reg_cnt[target] - regs;
          const int dl = h.lrc_cnt[target] - lrcs;
          const int want_type = target == 0 ? 1 : 2;
          bool in_ok = listener ? (sink_reg(target) == 1 && h.tk_reg(target) == want_type)
                                : (source_reg(target) == 1 && h.lstn_reg(target) == fp
                                   && h.active(target));
          bool edges_ok;
          if (h.rx_cycles.size() != 1) edges_ok = false;
          else if (rel <= 0) edges_ok = listener ? (du == 0 && dr == 0) : (ds == 0 && dst == 0 && dl == 0);
          else edges_ok = listener ? (du == 1 && dr == 1) : (ds == 1 && dst == 1 && dl == 2);
          (rel == 0 ? same : rel < 0 ? before : after)++;
          bool stale_ok = true;
          if (rel == 0) {
            until_ms(end_ms + LEAVE_TIME_MS + 200);
            stale_ok = listener ? (sink_reg(target) == 1 && h.unreg_cnt[target] == unregs)
                                : (source_reg(target) == 1 && h.active(target)
                                   && h.stop_cnt[target] == stops);
          }
          CHECK(in_ok && edges_ok && stale_ok, "PJ1: plane=%s cause=%s fp=%d target=%d k=%d rel=%ld "
                "in=%d edges=%d stale=%d stop=%d start=%d unreg=%d reg=%d lrc=%d",
                listener ? "listener" : "talker", own ? "own" : "peer", fp, target, k, rel,
                in_ok, edges_ok, stale_ok, ds, dst, du, dr, dl);
          if (rel >= -1 && rel <= 1)
            printf("R488_JOIN plane=%s cause=%s fp=%d target=%d k=%d rel=%ld in=%d edges=%d stale=%d "
                   "stop=%d start=%d unreg=%d reg=%d lrc=%d\n", listener ? "listener" : "talker",
                   own ? "own" : "peer", fp, target, k, rel, in_ok, edges_ok, stale_ok, ds, dst, du, dr, dl);
        }
        unlink(snapshot.c_str());
        CHECK(same == 1, "PJ2: plane=%s cause=%s fp=%d target=%d one JoinIn on the expiry clock "
              "(same=%d before=%d after=%d)", listener ? "listener" : "talker",
              own ? "own" : "peer", fp, target, same, before, after);
      }
  }
'''

tree = Path(sys.argv[1])
src = tree / "tb" / "srp_top" / "sim_main.cpp"
text = src.read_text()
anchor = "  // L: move slot acceptance across one decoded Listener Lv."
assert text.count(anchor) == 1
text = text.replace(anchor, METHOD + "\n" + anchor)
disp = '    if (!*group || !strcmp(group,"lvcoll")) check_leave_expiry_collisions();\n'
assert text.count(disp) == 1
text = text.replace(disp, disp + '    if (!strcmp(group,"r488join")) r488_join_collisions();\n')
gate = '&& strcmp(group,"lvcoll")) return 2;'
assert text.count(gate) == 1
text = text.replace(gate, '&& strcmp(group,"lvcoll") && strcmp(group,"r488join")) return 2;')
src.write_text(text)
print("probe inserted into", src)
