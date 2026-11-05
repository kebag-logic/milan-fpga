#!/usr/bin/env python3
"""Probe (disposable): add one check to tb/srp_stream_fsms at the end of section
PS. Every port Talker registrar holds another value; sink 0 is bound to V and
registers V itself (V arrives after the settle); the sink unbinds and binds
again to V before the talker re-declares (acceptance 2, the same stream).
Usage: probe_rebind_same_full_table.py <tree>"""
import sys, pathlib
f = pathlib.Path(sys.argv[1]) / "tb/srp_stream_fsms/sim_main.cpp"
t = f.read_text()
anchor = """        "no EVT_TK_UNREGISTERED (reg %d, unreg %d, state %d, tk %d, %zu ops)",
        h.l_reg[0], h.l_unreg[0], h.l_regst(0), h.l_tkreg(0), h.l_arm.size());
}
"""
assert t.count(anchor) == 1
probe = """        "no EVT_TK_UNREGISTERED (reg %d, unreg %d, state %d, tk %d, %zu ops)",
        h.l_reg[0], h.l_unreg[0], h.l_regst(0), h.l_tkreg(0), h.l_arm.size());
  for (const bool lv_first : {false, true}) {
    h.reset();
    fill_port_registrars();                       // every port registrar held
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);   // sink 0 registers V
    for (int k = 0; k < 3; ++k) h.tick();
    const bool in0 = h.l_tkreg(0) == 1 && h.l_decl(0) == 2;
    h.ctl(false, 0, SID0, DA0, VID0);             // unbind
    if (lv_first) { h.clear_logs(); h.tick(); }   // its Lv goes out
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);              // bind again, the same stream
    const bool at_once = h.l_reg[0] == 1 && h.l_tkreg(0) == 1;
    h.clear_logs();
    h.tick();
    const bool new_ready = listener_pushes(h.l_push, {{app_msg(VN, false, false), 2, SID0}});
    CHECK(in0 && at_once && new_ready,
          "PROBE-R1%s: every port registrar held by other values, sink 0 bound to "
          "V and registered on it, unbind, bind again to V: registered at the "
          "settle and New Ready on the next tx! (in %d, at once %d, new %d, tk %d, "
          "%zu pushes: %s)", lv_first ? "b" : "a", in0, at_once, new_ready,
          h.l_tkreg(0), h.l_push.size(), push_words(h.l_push).c_str());
  }
}
"""
f.write_text(t.replace(anchor, probe))
print("probe planted", f)
