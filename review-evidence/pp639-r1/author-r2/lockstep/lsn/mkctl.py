#!/usr/bin/env python3
"""mkctl.py <head listener.sv>: one planted copy per control (exact edits, each once)."""
import sys
src = open(sys.argv[1], encoding="utf-8").read()
CTL = {
    "read_sink_zero": [("assign rec_rd_w     = acmp_rec_t'(rec_ram_r[sink_r]);",
                        "assign rec_rd_w     = acmp_rec_t'(rec_ram_r[0]);")],
    "read_sampled_in_idle": [("assign rec_rd_w     = acmp_rec_t'(rec_ram_r[sink_r]);",
                              "logic [ACMP_REC_W_C-1:0] ctl_q;\n"
                              "  always_ff @(posedge clk_i) if (xs_r == X_IDLE) ctl_q <= rec_ram_r[sink_r];\n"
                              "  assign rec_rd_w     = acmp_rec_t'(ctl_q);")],
    "started_bit_unstored": [("      rec_ram_r[recwr_addr_w] <= recwr_data_w;",
                              "      rec_ram_r[recwr_addr_w] <= recwr_data_w & ~(ACMP_REC_W_C'(1) << 12);")],
    "settled_vlan_bit_unstored": [("      rec_ram_r[recwr_addr_w] <= recwr_data_w;",
                                   "      rec_ram_r[recwr_addr_w] <= recwr_data_w & ~(ACMP_REC_W_C'(1) << 305);")],
    "sweep_misaddressed": [("      rec_ram_r[recwr_addr_w] <= recwr_data_w;",
                            "      rec_ram_r[sink_r] <= recwr_data_w;")],
}
for name, edits in CTL.items():
    s = src
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            sys.exit(f"{name}: edit text occurs {n} times")
        s = s.replace(old, new)
    open(f"ctl_{name}.sv", "w", encoding="utf-8").write(s)
    print("wrote", f"ctl_{name}.sv")
