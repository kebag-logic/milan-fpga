#!/usr/bin/env python3
"""Parse the documented shell and trace Tcl arguments without executing synthesis."""
from pathlib import Path
import os
import re
import subprocess
import sys

repo=Path(sys.argv[1]).resolve()
scratch=Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True,exist_ok=True)
text=(repo/'docs/design/MARK_II_AREA_PLAN.md').read_text()
blocks=re.findall(r'```sh\n(.*?)\n```',text,re.S)
for i,block in enumerate(blocks):
    result=subprocess.run(['bash','-n'],input=block,text=True,capture_output=True)
    assert result.returncode==0,result.stderr
print('PASS shell syntax:',len(blocks),'documented blocks')
tcl=text.split("<<'TCL'\n",1)[1].split('\nTCL',1)[0]
header='''
proc set_param {args} {puts [linsert $args 0 set_param]}
proc read_verilog {args} {puts [linsert $args 0 read_verilog]}
proc synth_design {args} {puts [linsert $args 0 synth_design]}
proc report_utilization {args} {puts [linsert $args 0 report_utilization]}
'''
script=scratch/'trace.tcl'
script.write_text(header+tcl)
env=dict(os.environ,CPU_VEXII_DIR='/sources/vexii',CPU_VEXMIN_DIR='/sources/vexmin',CPU_PICO_DIR='/sources/pico')
for core in ['vexii','vexmin','pico']:
    result=subprocess.run(['tclsh',str(script),core],env=env,text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    assert 'synth_design -mode out_of_context -directive AreaOptimized_high -part xc7a100t-fgg484-2' in result.stdout
    assert 'PRICED '+core in result.stdout
    print(result.stdout,end='')
print('PASS three argument traces; no synthesis, source netlist lookup or hardware execution')
