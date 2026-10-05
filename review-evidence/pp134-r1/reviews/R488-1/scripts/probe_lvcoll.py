#!/usr/bin/env python3
"""R488-1 probe: insert a reviewer-only group `lvcoll` into a scratch copy of
tb/srp_top/sim_main.cpp (PR #160 head 5ab43bd9).

lvcoll <fp> <target> <kmin> <kmax> [hold_ms]: after a peer LeaveAll ages the target's
Listener registrar to LV, a calibration run finds the clock at which the
leave timer closes it with no Lv. Each sweep run then repeats the case and
starts the target's Lv frame k clocks before that close, k in [kmin, kmax],
and reports whether the registration and ACTIVE closed at the expiry.
Usage: probe_lvcoll.py <scratch-tree>
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
src = tree / "tb" / "srp_top" / "sim_main.cpp"
text = src.read_text()

METHOD = r'''
 public:
  void probe_lvcoll(int fp, int target, int kmin, int kmax, uint32_t hold_ms) {
    auto peer_la = [&]() -> uint64_t {
      leaveall_setup(fp);
      Msg ta{1, 25, false, {Vec{true, 1, fv_talker(peer_sid(0), peer_da(0), 2, 29, 1, 3, 1, 500),
                                {EV_JOININ}, {}}}};
      Msg tf{2, 34, false, {Vec{true, 1, fv_failed(peer_sid(7), peer_da(7), 2, 29, 1, 3, 1, 500,
                                                   0x1234, 1), {EV_JOININ}, {}}}};
      h.peer_la_times.clear();
      h.feed(mrpdu_body(true, {listener_rejoins(fp, target, true), ta, tf,
                               la_only(4, 4, false)}), true);
      return h.t;
    };
    const uint64_t c0 = peer_la();
    const uint32_t la0 = h.peer_la_times.empty() ? 0 : h.peer_la_times[0];
    while (source_reg(target) != 0 && d->now_ms_o < la0 + 6000) h.cycle();
    const uint64_t close_off = h.t - c0;
    printf("PROBE_CAL fp=%d target=%d la_ms=%u close_ms=%u close_off_clocks=%llu reg=%d\n",
           fp, target, la0, d->now_ms_o, (unsigned long long)close_off, source_reg(target));
    for (int k = kmin; k <= kmax; k++) {
      const uint64_t c = peer_la();
      const uint32_t la_ms = h.peer_la_times.empty() ? 0 : h.peer_la_times[0];
      const int stops = h.stop_cnt[target];
      const uint64_t at = c + close_off - k;
      if (h.t > at) { printf("PROBE_SKIP k=%d\n", k); continue; }
      while (h.t < at) h.cycle();
      listener_event(target, EV_LV, fp);
      until_ms(la_ms + LEAVE_TIME_MS + hold_ms);
      const bool closed = source_reg(target) == 0 && !h.active(target)
                          && h.stop_cnt[target] == stops + 1;
      printf("PROBE_K k=%d la_ms=%u now_ms=%u own_la_actions=%zu reg=%d lstn=%d active=%d stops=%d %s\n", k, la_ms, d->now_ms_o, h.la_times.size(),
             source_reg(target), h.lstn_reg(target), int(h.active(target)),
             h.stop_cnt[target] - stops, closed ? "CLOSED" : "STUCK");
    }
  }
 private:
'''
anchor = "  // L: move slot acceptance across one decoded Listener Lv."
assert text.count(anchor) == 1
text = text.replace(anchor, METHOD + anchor)

old_main = "  const char* group = argc > 1 ? argv[1] : \"\";\n"
assert text.count(old_main) == 1
text = text.replace(old_main, old_main +
    "  if (!strcmp(group, \"lvcoll\") && argc > 5) {\n"
    "    harness.probe_lvcoll(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]),\n"
    "                         argc > 6 ? uint32_t(atoi(argv[6])) : 1000u);\n"
    "    return 0;\n  }\n")
src.write_text(text)
print("patched", src)
