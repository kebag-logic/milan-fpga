#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate lk_top.sv: the reference (main's KL_aecp_notify, renamed) and the
candidate side by side, same inputs, one mismatch bit per output.

Usage: gen_wrapper.py CANDIDATE.sv OUT.sv
The port list is read from the candidate file; the reference must have the
same ports (checked by the compiler: every port is connected by name).
"""
import re
import sys

src = open(sys.argv[1]).read()
body = src[src.index("module KL_aecp_notify"):]
plist = body[body.index(") (") + 3: body.index(");\n")]
ports = []
for line in plist.splitlines():
    line = line.split("//")[0].strip().rstrip(",")
    if not line:
        continue
    m = re.match(r"(input|output)\s+(wire|logic)\s*(\[[^\]]+\])?\s*(\w+)$", line)
    if not m:
        sys.exit(f"unparsed port line: {line!r}")
    ports.append((m.group(1), m.group(3) or "", m.group(4)))

ins = [p for p in ports if p[0] == "input" and p[2] != "clk_i"]
outs = [p for p in ports if p[0] == "output"]

o = []
o.append("`default_nettype none")
o.append("module lk_top import pp_pkg::*; #(")
o.append("  parameter int unsigned N_CTRL_P = 16,")
o.append("  parameter int unsigned N_STREAM_IN_P = 8,")
o.append("  parameter int unsigned N_STREAM_OUT_P = 8,")
o.append("  parameter bit EN_IDENTIFY_NOTIF_P = 1'b0,")
o.append("  parameter int unsigned TMR_SLOTS_P = 89,")
o.append("  localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 1) ? $clog2(TMR_SLOTS_P) : 1,")
o.append("  localparam int unsigned CIX_W_C  = (N_CTRL_P > 1) ? $clog2(N_CTRL_P) : 1")
o.append(") (")
o.append("  input  wire clk_i,")
for _, w, n in ins:
    o.append(f"  input  wire {w} {n},")
for _, w, n in outs:
    o.append(f"  output logic {w} {n},   // the reference's")
o.append(f"  output logic [{len(outs)}-1:0] mism_o,")
o.append("  output logic [N_CTRL_P-1:0] hit_dut_o, hit_ref_o,")
o.append("  output logic cov_clr_o, cov_set_o, cov_wr_en_o, cov_idchg_o,")
o.append("  output logic [CIX_W_C-1:0] cov_wr_ix_o, cov_rd_ix_o,")
o.append("  output logic [3:0] cov_st_o,")
o.append("  output logic cov_ctr_sent_any_o,")
o.append("  output logic [63:0] cov_old_eid_o, cov_new_eid_o,")
o.append("  output logic [47:0] cov_old_mac_o, cov_new_mac_o")
o.append(");")
for tag in ("d", "r"):
    for _, w, n in outs:
        o.append(f"  logic {w} {tag}_{n};")
for tag, mod in (("d", "KL_aecp_notify"), ("r", "KL_aecp_notify_ref")):
    o.append(f"  {mod} #(.N_CTRL_P(N_CTRL_P), .N_STREAM_IN_P(N_STREAM_IN_P),"
             " .N_STREAM_OUT_P(N_STREAM_OUT_P), .EN_IDENTIFY_NOTIF_P(EN_IDENTIFY_NOTIF_P),"
             f" .TMR_SLOTS_P(TMR_SLOTS_P)) u_{tag} (")
    conns = ["    .clk_i(clk_i)"]
    conns += [f"    .{n}({n})" for _, _, n in ins]
    conns += [f"    .{n}({tag}_{n})" for _, _, n in outs]
    o.append(",\n".join(conns))
    o.append("  );")
for k, (_, _, n) in enumerate(outs):
    o.append(f"  assign mism_o[{k}] = (d_{n} != r_{n});")
for _, _, n in outs:
    o.append(f"  assign {n} = r_{n};")
o.append("  assign hit_dut_o = u_d.rx_cmd_hit_w;")
o.append("  assign hit_ref_o = u_r.rx_cmd_hit_w;")
o.append("  assign cov_clr_o = u_d.ix_clr_r;")
o.append("  assign cov_set_o = u_d.ix_set_r;")
o.append("  assign cov_wr_en_o = u_d.wr_en_r;")
o.append("  assign cov_idchg_o = (u_d.wr_row_r[127:16] != u_d.ix_wr_row_w[127:16]);")
o.append("  assign cov_wr_ix_o = u_d.wr_ix_r;")
o.append("  assign cov_rd_ix_o = u_d.rd_ix_w;")
o.append("  assign cov_st_o = 4'(u_d.n_st_r);")
o.append("  assign cov_ctr_sent_any_o = |u_d.ctr_sent_r;")
o.append("  assign cov_old_eid_o = u_d.ix_wr_row_w[127:64];")
o.append("  assign cov_old_mac_o = u_d.ix_wr_row_w[63:16];")
o.append("  assign cov_new_eid_o = u_d.wr_row_r[127:64];")
o.append("  assign cov_new_mac_o = u_d.wr_row_r[63:16];")
o.append("endmodule")
o.append("`default_nettype wire")
open(sys.argv[2], "w").write("\n".join(o) + "\n")
with open(sys.argv[2] + ".outputs", "w") as f:
    for _, _, n in outs:
        f.write(n + "\n")
print(f"{len(ins)} inputs, {len(outs)} outputs")
