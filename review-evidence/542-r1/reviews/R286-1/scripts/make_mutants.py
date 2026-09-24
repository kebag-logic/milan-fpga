#!/usr/bin/env python3
"""R286-1 disposable mutants of tb/verilator/milan_dp/sim_nxn.cpp at the head.
usage: make_mutants.py <bench dir>. Writes sim_nxn_mut_*.cpp beside the source."""
import sys, pathlib
tb = pathlib.Path(sys.argv[1]); src = (tb / "sim_nxn.cpp").read_text()
def sub(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)
# M1: the lever compiled in but its move made dead -> its liveness check must fail
m1 = sub(src, "        if (!kForceRealloc) return;\n", "        if (kForceRealloc || !kForceRealloc) return;   // R286 M1\n")
(tb / "sim_nxn_mut_nolever.cpp").write_text(m1)
# M2: a reference into uns_log held across drain_tx (the lever's second hook);
# the N2 bar reads it after a one-cycle drain. Under the lever it must dangle.
m2 = sub(src,
  "        const std::vector<uint8_t> nB1 = notify_last(0x0010, CTL_B);\n",
  "        size_t k_r286 = uns_log.size();\n"
  "        for (size_t i = 0; i < uns_log.size(); i++)\n"
  "            if (aecp_is_unsolicited(uns_log[i]) && notify_cmd(uns_log[i]) == 0x0010\n"
  "                && notify_to(uns_log[i], CTL_B)) k_r286 = i;\n"
  "        static const std::vector<uint8_t> none_r286;\n"
  "        const std::vector<uint8_t>& nB1 = k_r286 < uns_log.size() ? uns_log[k_r286] : none_r286;\n"
  "        drain_tx(1);   // R286 M2: a hold across the drain_tx hook\n")
(tb / "sim_nxn_mut_drainhold.cpp").write_text(m2)
print("ok")
# M3: every notify_last() lookup absent -> the copy's empty path must fail its
# checks cleanly (no crash, no out-of-range read), as the old null pointer did
m3 = sub(src, "        return last < uns_log.size() ? uns_log[last] : std::vector<uint8_t>();\n",
              "        (void)last; return std::vector<uint8_t>();   // R286 M3\n")
(tb / "sim_nxn_mut_absent.cpp").write_text(m3)
print("ok m3")
