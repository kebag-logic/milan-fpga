#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Write sim_nxn_arbprobe.cpp: the head harness with three added checks in
prove_the_bind_edge_wipes_the_crf_row_and_raises_its_dirty_bit(). All four
arbiter observation bitmaps are cleared before the lever edge, and the edge
must deliver no STREAM_OUTPUT, AVB_INTERFACE or CLOCK_DOMAIN tuple, which is
what "as {STREAM_INPUT, N} and as nothing else" states.
usage: gen_arbiter_probe.py <tb/verilator/milan_dp dir of a disposable tree>"""
import hashlib, pathlib, sys
d = pathlib.Path(sys.argv[1])
src = (d / "sim_nxn.cpp").read_text()
old = ("        pp_ctr_evt_sin_seen = 0;\n"
       "        crf_lever(true);\n"
       "        ck(\"[CTRS-CRF] the bind edge reached the arbiter as STREAM_INPUT N only\",\n")
new = ("        pp_ctr_evt_sin_seen = 0;\n"
       "        pp_ctr_evt_sout_seen = 0; pp_ctr_evt_avb_seen = false; pp_ctr_evt_ckd_seen = false;\n"
       "        crf_lever(true);\n"
       "        ck(\"[PROBE] the bind edge delivered no STREAM_OUTPUT tuple\", pp_ctr_evt_sout_seen, 0);\n"
       "        ck(\"[PROBE] ...no AVB_INTERFACE tuple\", pp_ctr_evt_avb_seen ? 1 : 0, 0);\n"
       "        ck(\"[PROBE] ...no CLOCK_DOMAIN tuple\", pp_ctr_evt_ckd_seen ? 1 : 0, 0);\n"
       "        ck(\"[CTRS-CRF] the bind edge reached the arbiter as STREAM_INPUT N only\",\n")
assert src.count(old) == 1
m = src.replace(old, new)
(d / "sim_nxn_arbprobe.cpp").write_text(m)
print("sim_nxn_arbprobe.cpp", hashlib.sha256(m.encode()).hexdigest())
