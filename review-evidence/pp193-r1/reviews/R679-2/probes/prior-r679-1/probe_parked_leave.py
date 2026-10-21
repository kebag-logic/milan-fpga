#!/usr/bin/env python3
"""Reviewer probe (R679-1, issue #193): a parked owed Leave for a stream_id
meeting a new group on the same stream_id.

Usage: probe_parked_leave.py <exported-tree>
Inserts PR* probe cases into <tree>/tb/srp_stream_fsms/sim_main.cpp of a
DISPOSABLE exported copy (never the review clone). The probe lines print
"PROBE:" with the Listener words each tick pushes for the shared stream_id,
in walk order, as "<event>/<fourpacked>" (event 1 = New, 2 = JoinIn, 3 = JoinMt,
5 = Lv; fourpacked 2 = Ready). Each PR case is also a CHECK named "PRn:"
requiring at most one VectorAttribute for the value per tick and no Lv in a
tick in which a settled, registered sink still wants the value.
"""
import pathlib
import sys

tree = pathlib.Path(sys.argv[1])
f = tree / "tb" / "srp_stream_fsms" / "sim_main.cpp"
src = f.read_text()

decl_anchor = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl_anchor) == 1
src = src.replace(decl_anchor, decl_anchor + "  void probe_parked_leave_meets_a_new_group(int parker, int joiner, bool via_a8);\n")

body = r'''
// ==== reviewer probe: parked owed Leave vs a new group on the same value ====
void SrpStreamFsmsSuite::probe_parked_leave_meets_a_new_group(int parker,
                                                              int joiner,
                                                              bool via_a8) {
  constexpr uint64_t SIDB = 0x02AABBCCDDEE0002ull;
  constexpr uint64_t DAB  = 0x91E0F0001235ull;
  h.reset();
  // parker alone on SID0, registered Ready, ticked to QA
  h.ctl(true, parker, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  for (int k = 0; k < 4; ++k) h.tick();
  const int parker_qa = h.l_app(parker);
  // parker re-binds to SIDB (optionally A8 first): the applicant owes Lv for
  // SID0 and is parked (#188), no other sink being on SID0 at that time
  if (via_a8) h.ctl(false, parker, SID0, DA0, VID0);
  h.ctl(true, parker, SIDB, DAB, VID0);
  const int parker_after = h.l_app(parker);
  // before the next tx!: the joiner settles on SID0 and its talker registers
  h.ctl(true, joiner, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  const int joiner_decl = h.l_decl(joiner);
  h.clear_logs();
  h.tick();
  const std::string w = listener_words(h.l_push, SID0);
  int n = 0;
  bool lv = false;
  for (const Push& p : h.l_push) {
    uint64_t got = 0;
    for (int i = 0; i < 8; ++i) got = (got << 8) | p.val[i];
    if (p.type == 3 && got == SID0) { ++n; if (p.code == 5) lv = true; }
  }
  printf("PROBE: parker %d joiner %d via_a8 %d: parker %s -> %s, joiner decl %d, "
         "tick SID0 words '%s' (%d VectorAttributes for SID0)\n", parker, joiner,
         via_a8, SN[parker_qa], SN[parker_after], joiner_decl, w.c_str(), n);
  CHECK(n <= 1 && !(lv && joiner_decl != 0),
        "PR%d: parker %d joiner %d via_a8 %d: one VectorAttribute for SID0 per "
        "tick and no Lv while sink %d wants it (got '%s')",
        1 + (parker > joiner ? 1 : 0) + (via_a8 ? 2 : 0), parker, joiner, via_a8,
        joiner, w.c_str());
  // the following ticks, for the record
  for (int k = 0; k < 2; ++k) {
    h.clear_logs();
    h.tick();
    printf("PROBE:   next tick SID0 words '%s', joiner app %s decl %d\n",
           listener_words(h.l_push, SID0).c_str(), SN[h.l_app(joiner)],
           h.l_decl(joiner));
  }
}

'''
run_anchor = "int SrpStreamFsmsSuite::run() {\n"
assert src.count(run_anchor) == 1
src = src.replace(run_anchor, body + run_anchor)

call_anchor = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call_anchor) == 1
src = src.replace(call_anchor,
                  "  ready_with_asking_failed_declares_ready_failed();\n"
                  "  probe_parked_leave_meets_a_new_group(1, 0, false);\n"
                  "  probe_parked_leave_meets_a_new_group(0, 1, false);\n"
                  "  probe_parked_leave_meets_a_new_group(1, 0, true);\n"
                  "  probe_parked_leave_meets_a_new_group(0, 1, true);\n"
                  "\n  printf(")
f.write_text(src)
print("probe inserted into", f)
