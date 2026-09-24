#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe P2: pp_top BW3 at the top level. Patches a COPY of
tb/pp_top/sim_main.cpp (argv[1]). After BW3's held GET_RX_STATE of sink 0
(whose saved record was read and stored before the device went silent) is
answered on the default and the device serves the abandoned read, the probe
lets every debounce and flush run out BEFORE the case's own BIND, then grades
that no write reached sink 0's region and its bytes are the saved record.
With R278_PROBE set, the bench stops after BW3 (the probe's section)."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
snap_anchor = """    h.reset();
    h.flush_all();
    const size_t ops3 = h.nvm_ops.size();
    d->restore_go_i = 1;"""
assert s.count(snap_anchor) == 1
s = s.replace(snap_anchor, """    h.reset();
    h.flush_all();
    const size_t ops3 = h.nvm_ops.size();
    const std::vector<uint8_t> r278_saved(h.nv_mem[0x20].begin(),
                                          h.nv_mem[0x20].begin() + 28);
    d->restore_go_i = 1;""")
drain_anchor = """    while (bw_ops(ops3, 0, 0x21) == 0 && guard--) h.step();
    h.feed(acmp_frame(CTLR_MAC, 6,"""
assert s.count(drain_anchor) == 1
s = s.replace(drain_anchor, """    while (bw_ops(ops3, 0, 0x21) == 0 && guard--) h.step();
    h.run_ms(1500);
    {
      const std::vector<uint8_t> now(h.nv_mem[0x20].begin(),
                                     h.nv_mem[0x20].begin() + 28);
      printf("  [i] PROBE BW3: sink-0 region writes %d erases %d since the boot; "
             "saved byte8 %02x now byte8 %02x\\n", bw_ops(ops3, 1, 0x20),
             bw_ops(ops3, 2, 0x20), r278_saved[8], now[8]);
      CHECK(bw_ops(ops3, 1, 0x20) == 0 && bw_ops(ops3, 2, 0x20) == 0
                && now == r278_saved,
            "PROBE BW3: the held read-only GET, served after the failed walk, "
            "left sink 0's saved record in NVM untouched");
      if (getenv("R278_PROBE")) { fflush(stdout); std::exit(0); }
    }
    h.feed(acmp_frame(CTLR_MAC, 6,""")
open(p, "w", encoding="utf-8").write(s)
print("patched", p)
