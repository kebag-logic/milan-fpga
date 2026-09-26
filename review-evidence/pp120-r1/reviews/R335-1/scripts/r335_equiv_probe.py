#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Instrument a COPY of KL_aecp_desc_store with display-only monitors and
report, over a whole suite run, how often (a) a write request is held while
the store is not ready, (b) a non-name write is accepted by the store,
(c) the boot walk writes the name RAM, (d) the export pulses.
Usage: r335_equiv_probe.py <tree-copy>   (edits the copy in place)"""
import sys
from pathlib import Path
f = Path(sys.argv[1]) / "hdl/aecp/KL_aecp_desc_store.sv"
t = f.read_text()
anchor = "  assign name_wr_o = take_wr_w && st_name_i;"
assert t.count(anchor) == 1
probe = anchor + """
  // reviewer probe: display only, no state visible to the design
  always_ff @(posedge clk_i) if (rst_n) begin
    if (st_req_i && st_we_i && !st_ready_o)
      $display("R335PROBE held_write_not_ready name=%0d st=%0d", st_name_i, st_r);
    if (take_wr_w && !st_name_i) $display("R335PROBE non_name_store_write");
    if (name_we_w && !name_wr_o) $display("R335PROBE boot_name_load");
    if (name_wr_o) $display("R335PROBE export_pulse");
  end"""
f.write_text(t.replace(anchor, probe))
print("probe inserted in", f)
