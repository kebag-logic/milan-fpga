#!/usr/bin/env python3
"""Run the committed crossing bench and its five mutations outside the checkout."""
from pathlib import Path
import os, subprocess, sys
P=Path(__file__).resolve().parent; R=Path(sys.argv[1]).resolve(); S=P/'scratch'
sys.dont_write_bytecode=True
os.environ['VERILATOR']=os.environ.get('VERILATOR','verilator')
os.environ['VBUILD_JOBS']='1'; os.environ['TMPDIR']=str(S)
sys.path.insert(0,str(R/'tb/verilator/mbx'))
import cdc_pub_mutants as c
cmd=[*c.vflags(),'--Mdir',str(S/'cdc-baseline'),*map(str,c.SOURCES),str(c.HERE/'tb_cdc_pub.sv'),'-o','Vtb_cdc_pub']
with (P/'cdc-build.log').open('w') as f:
    subprocess.run(cmd,check=True,stdout=f,stderr=subprocess.STDOUT)
with (P/'cdc-baseline.log').open('w') as f:
    rc=subprocess.run([str(S/'cdc-baseline/Vtb_cdc_pub')],stdout=f,stderr=subprocess.STDOUT).returncode
(P/'cdc-baseline.rc').write_text(str(rc)+'\n')
if rc:sys.exit(rc)
with (P/'cdc-mutants.log').open('w') as f:
    rc=subprocess.run(['python3','-B',str(c.HERE/'cdc_pub_mutants.py'),'--jobs','4','--keep',str(S/'cdc-mutants')],stdout=f,stderr=subprocess.STDOUT).returncode
(P/'cdc-mutants.rc').write_text(str(rc)+'\n')
print('cdc baseline and mutations',rc)
sys.exit(rc)
