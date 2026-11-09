#!/usr/bin/env python3
"""Add a reviewer probe group 'probe216' to tb/srp_top/sim_main.cpp (disposable copy only).
Scenario: a peer's MVRP JoinIn of VID 2 arrives before the first user's join of VID 2;
the probe prints the VID 2 messages this participant then sends."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "tb/srp_top/sim_main.cpp"
s = p.read_text()
method = r'''
  void probe_early_registrar() {
    h.reset(); d->link_up_i = 1; h.run_ms(300);
    const size_t f0 = h.archive.size();
    h.feed(mrpdu_body(false, {Msg{1, 2, false, {Vec{false, 1, fv_vid(2), {EV_JOININ}, {}}}}}), false);
    h.run_ms(500);
    const uint32_t decl = d->now_ms_o;
    const auto r = h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 2, 29, 1);
    h.run_ms(3000);
    const auto v = messages_of(false, 1, 2, f0);
    printf("PROBE216 early-registrar: peer JoinIn VID 2 at ~300 ms, declared at %u ms (ok %d), VID 2 sent %s\n",
           decl, (int)(r.got && r.status == ST_OK), shown216(v, 12).c_str());
    const size_t f1 = h.archive.size();
    h.feed(mrpdu_body(false, {Msg{1, 2, false, {Vec{false, 1, fv_vid(2), {EV_JOININ}, {}}}}}), false);
    h.run_ms(2500);
    printf("PROBE216 after a second peer JoinIn: VID 2 sent %s\n", shown216(messages_of(false, 1, 2, f1), 12).c_str());
  }
'''
anchor = "  const milan::tb::Model<Vsrp_top_wrap> model;"
assert s.count(anchor) == 1
s = s.replace(anchor, method + "\n" + anchor)
a2 = '    if (!*group || !strcmp(group,"applicant")) check_each_applicant_follows_table_10_3();'
assert s.count(a2) == 1
s = s.replace(a2, a2 + '\n    if (!strcmp(group,"probe216")) probe_early_registrar();')
a3 = '&& strcmp(group,"applicant")) return 2;'
assert s.count(a3) == 1
s = s.replace(a3, '&& strcmp(group,"applicant") && strcmp(group,"probe216")) return 2;')
p.write_text(s)
print("probe group added")
