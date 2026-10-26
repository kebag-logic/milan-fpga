#!/usr/bin/env python3
"""Run source-level census fault probes. Usage: script TREE SCRATCH."""
import sys
from pathlib import Path
root, scratch = map(Path, sys.argv[1:])
sys.path.insert(0, str(root / 'sw/mailbox'))
import publication_census as p
import mailbox_model
from census_elab import RECIPE
scratch.mkdir(parents=True, exist_ok=True)
wrapper = (root/'hdl/milan/KL_pp_shadow.sv').read_text()
datapath = (root/'hdl/milan/milan_datapath.sv').read_text()
new = wrapper.replace('output logic [31:0] dbg_now_ms_o', 'output logic probe_new_o,\n    output logic [31:0] dbg_now_ms_o')
wp = scratch/'wrapper.sv'; wp.write_text(new)
new = datapath.replace('assign o_mac_tx_en    = cfg_mac_tx_en;', 'wire [31:0] probe_g_w;\n  assign o_mac_tx_en = cfg_mac_tx_en ^ probe_g_w[0];')
assert new != datapath
new = new.replace('.dbg_now_ms_o      ()', '.dbg_now_ms_o      (probe_g_w)')
dp = scratch/'datapath.sv'; dp.write_text(new)
known = p.fields(mailbox_model.load())
for label, d, w, words in [('unmapped',p.DATAPATH,wp,('unmapped port: probe_new_o',)),('G-wire',dp,p.WRAPPER_SV,('G port dbg_now_ms_o reaches the wire','o_mac_tx_en'))]:
    out, surveys = p.census(p.load(d,w),p.CENSUS,known,p.Plan(at=(RECIPE,)))
    print(label, '\n'.join(out), flush=True)
    assert all(any(word in finding for finding in out) for word in words)
print('Both source plants refused by their intended rule.')
