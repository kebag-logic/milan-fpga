#!/usr/bin/env python3
"""Capture the documented and elaborated counter-stamp dimensions."""
import argparse,pathlib,re
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args()
for name,pattern in [('docs/architecture/06_aecp_engine.md','GET_COUNTERS stamps'),('hdl/aecp/KL_aecp_notify.sv','localparam int unsigned N_CTR_DESC_C ='),('hdl/aecp/KL_aecp_notify.sv','logic [31:0] ctr_last_r')]:
 for n,line in enumerate((a.source/name).read_text().splitlines(),1):
  if pattern in line:print(f'{name}:{n}: {line}')
f=a.packet/'scratch/depth16/obj_dir/VKL_aecp_notify___024root.h'
for line in f.read_text().splitlines():
 if 'ctr_last_r' in line:print('Generated two-interface, 1-in/1-out model: '+line.strip())
print('Documented expression at 1-in/1-out: (1 + 1 + 2) * 32 = 128 bits.')
print('Elaborated expression at 1-in/1-out and two interfaces: (1 + 1 + 1 + 2) * 32 = 160 bits.')
print('At 8-in/8-out and two interfaces: documented 18 stamps, actual 19 stamps; difference 32 bits.')
