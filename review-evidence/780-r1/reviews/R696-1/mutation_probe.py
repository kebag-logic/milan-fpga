#!/usr/bin/env python3
"""Revert only the adopted dispatch constant in the disposable probe tree.

The fixed head expectations must reject the old status. Restore source bytes
even if the build or observation fails. Run after run_focused.py.
"""
from pathlib import Path
import os
import subprocess

PACKET=Path(__file__).resolve().parent
TREE=PACKET/'scratch/probe-tree'
ENGINE=TREE/'protocol-processor/hdl/aecp/KL_aecp_engine.sv'
VERILATOR=os.environ.get('REVIEW_VERILATOR','verilator')
original=ENGINE.read_bytes()
old=b"else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin\n                upc_r  <= UPC_NSUPPE_C;"
new=old.replace(b'UPC_NSUPPE_C',b'UPC_NOTIMPL_C')
assert original.count(old)==1
env=dict(os.environ,TMPDIR=str(PACKET/'scratch'),PYTHONDONTWRITEBYTECODE='1')
try:
    ENGINE.write_bytes(original.replace(old,new))
    with (PACKET/'parent-mutant.log').open('w') as log:
        log.write('Mutation: wrong-type GET_AVB_INFO dispatch UPC_NSUPPE_C -> UPC_NOTIMPL_C\n')
        log.flush()
        command=['make','-j16','-C','tb/verilator/pp_shadow','run-base',
                 f'VERILATOR={VERILATOR}','VERILATOR_JOBS=8']
        p=subprocess.run(command,cwd=TREE,env=env,stdout=log,stderr=subprocess.STDOUT)
    (PACKET/'parent-mutant.rc').write_text(str(p.returncode)+'\n')
    text=(PACKET/'parent-mutant.log').read_text()
    assert p.returncode!=0 and 'adoption probe: 160 checks, 30 failures' in text
    assert text.count('expected=11 actual=1')==15
    print('PASS: old-status mutant rejected by 15 status checks and 15 byte-exact echoes.')
finally:
    ENGINE.write_bytes(original)
    assert ENGINE.read_bytes()==original
    print('Disposable donor source restored byte-exactly.')
