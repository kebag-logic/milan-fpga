#!/usr/bin/env python3
"""Plant one named control into a copy of the candidate listener. Usage: mutate.py FILE NAME"""
import sys

REC_READ = "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[sink_r]);\n"
REC_WRITE = "      rec_ram_r[recwr_addr_w] <= recwr_data_w;\n"
MUTANTS = {
    "read_sink_zero": (REC_READ, "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[0]);\n"),
    "read_sampled_in_idle": (REC_READ,
        "  logic [ACMP_REC_W_C-1:0] rec_idle_r;\n"
        "  always_ff @(posedge clk_i) if (xs_r == X_IDLE) rec_idle_r <= rec_ram_r[sink_r];\n"
        "  assign rec_rd_w     = acmp_rec_t'(rec_idle_r);\n"),
    "started_bit_unstored": (REC_WRITE,
        "      rec_ram_r[recwr_addr_w] <= recwr_data_w & ~(ACMP_REC_W_C'(1) << 12);\n"),
    "settled_vlan_bit_unstored": (REC_WRITE,
        "      rec_ram_r[recwr_addr_w] <= recwr_data_w & ~(ACMP_REC_W_C'(1) << 305);\n"),
    "sweep_misaddressed": (REC_WRITE, "      rec_ram_r[sink_r] <= recwr_data_w;\n"),
    # reviewer's own probe (expected equivalent: no record is written in a consuming cycle):
    # a write-first bypass on the read
    "probe_write_first_bypass": (REC_READ,
        "  assign rec_rd_w     = acmp_rec_t'((recwr_en_w && (recwr_addr_w == sink_r))"
        " ? recwr_data_w : rec_ram_r[sink_r]);\n"),
    # reviewer's own probe (expected equivalent outside X_INIT): read on the write address
    "probe_read_on_write_addr": (REC_READ,
        "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[recwr_addr_w]);\n"),
}

path, name = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8").read()
needle, repl = MUTANTS[name]
assert text.count(needle) == 1, (name, text.count(needle))
open(path, "w", encoding="utf-8").write(text.replace(needle, repl))
