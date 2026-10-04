#!/usr/bin/env python3
"""Generate a lockstep wrapper: reference and candidate KL_aecp_notify, same inputs, outputs compared."""
import re, sys
src = open(sys.argv[1]).read()
hdr = src[src.index('module KL_aecp_notify'):]
ports_txt = hdr[hdr.index(') (') + 3: hdr.index(');')]
ports = []
for line in ports_txt.splitlines():
    line = line.split('//')[0].strip().rstrip(',')
    if not line:
        continue
    m = re.match(r'(input|output)\s+(?:wire|logic)\s*(\[[^\]]+\])?\s*(\w+)$', line)
    assert m, line
    ports.append((m.group(1), m.group(2) or '', m.group(3)))
params = """    parameter int unsigned N_CTRL_P          = 16,
    parameter int unsigned N_STREAM_IN_P     = 8,
    parameter int unsigned N_STREAM_OUT_P    = 8,
    parameter int unsigned TL_TIMEOUT_MS_P   = 300_000,
    parameter int unsigned LOCK_TIMEOUT_MS_P = 60_000,
    parameter int unsigned TMR_SLOTS_P       = 89,
    parameter int unsigned TMR_REGMON_BASE_P = 25,
    parameter int unsigned TMR_LOCK_SLOT_P   = 61,
    parameter int unsigned TMR_IDENT_SLOT_P  = 62,
    parameter bit          EN_IDENTIFY_NOTIF_P = 1'b0,
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 1) ? $clog2(TMR_SLOTS_P) : 1"""
plist = ['N_CTRL_P','N_STREAM_IN_P','N_STREAM_OUT_P','TL_TIMEOUT_MS_P','LOCK_TIMEOUT_MS_P','TMR_SLOTS_P','TMR_REGMON_BASE_P','TMR_LOCK_SLOT_P','TMR_IDENT_SLOT_P','EN_IDENTIFY_NOTIF_P']
out = ['`default_nettype none', 'module lockstep_top', '  import pp_pkg::*;', '#(', params, ') (']
lines = []
for d, w, n in ports:
    if d == 'input':
        lines.append(f'    input  wire {w} {n}')
outs = [(w, n) for d, w, n in ports if d == 'output']
for w, n in outs:
    lines.append(f'    output logic {w} {n}')
lines.append('    output logic [N_CTRL_P-1:0] hit_r_o')
lines.append('    output logic [N_CTRL_P-1:0] hit_c_o')
lines.append('    output logic busy_o')
lines.append('    output logic mism_o')
lines.append('    output logic [31:0] mism_ix_o')
out.append(',\n'.join(lines))
out.append(');')
for w, n in outs:
    out.append(f'  logic {w} r_{n}, c_{n};')
pmap = ', '.join(f'.{p}({p})' for p in plist)
for inst, pre, mod in (('u_ref', 'r_', 'KL_aecp_notify_ref'), ('u_cand', 'c_', 'KL_aecp_notify')):
    conns = []
    for d, w, n in ports:
        conns.append(f'.{n}({n})' if d == 'input' else f'.{n}({pre}{n})')
    out.append(f'  {mod} #({pmap}) {inst} (' + ', '.join(conns) + ');')
for w, n in outs:
    out.append(f'  assign {n} = r_{n};')
out.append('  assign hit_r_o = u_ref.rx_cmd_hit_w;')
out.append('  assign hit_c_o = u_cand.rx_cmd_hit_w;')
out.append('  assign busy_o = u_cand.IXBUSY;')
out.append('  always_comb begin')
out.append('    mism_o = 1\'b0; mism_ix_o = 32\'d0;')
out.append('    if (hit_r_o !== hit_c_o) begin mism_o = 1\'b1; mism_ix_o = 32\'d999; end')
for k, (w, n) in enumerate(outs):
    out.append(f'    if (r_{n} !== c_{n}) begin mism_o = 1\'b1; if (mism_ix_o == 0) mism_ix_o = 32\'d{k+1}; end')
out.append('  end')
out.append('endmodule')
out.append('`default_nettype wire')
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
open(sys.argv[3], 'w').write('\n'.join(n for w, n in outs) + '\n')
