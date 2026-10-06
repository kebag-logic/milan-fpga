#!/usr/bin/env python3
"""Verify unchanged coverage exclusions and the scope of the source delta."""
import sys,subprocess
from pathlib import Path
root=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'sw/firmware/gtest'))
import fw_coverage
base='6714181d0c8a16e2983f85b724f4d688f5111835'
def old(path): return subprocess.check_output(['git','-C',str(root),'show',base+':'+path],text=True)
path='sw/firmware/gtest/README.md'
a=fw_coverage.exclusions(old(path)); b=fw_coverage.exclusions((root/path).read_text())
assert a==b
print('Coverage exclusions:',len(a),'unchanged parsed rows')
for path in ('sw/firmware/gtest/fw_coverage.py','sw/litex/milan_soc.py',
             'hdl/milan/mailbox/KL_mbx_wb.sv','hdl/milan/mailbox/KL_mbx_axil.sv',
             'hdl/milan/mailbox/KL_mbx_ring.sv','hdl/milan/mailbox/KL_mbx_tx.sv','hdl/milan/mailbox/KL_mbx_evt.sv'):
 assert old(path)==(root/path).read_text(),path
 print('Unchanged:',path)
subprocess.run(['git','-C',str(root),'diff','--check',base,'HEAD'],check=True)
print('PASS unchanged contracts and whitespace')
