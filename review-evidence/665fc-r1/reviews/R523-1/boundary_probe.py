#!/usr/bin/env python3
"""Build the independent probe in a disposable exact-head archive already used by mbx-suite.
Arguments: scratch source root, simulator executable. All compiler commands remain foreground.
"""
import sys,subprocess,shutil
from pathlib import Path
packet=Path(__file__).resolve().parent
root=Path(sys.argv[1]).resolve(); exe=Path(sys.argv[2]).resolve()
bench=root/'tb/verilator/mbx'; gen=bench/'obj_if2/gen'
shutil.copy2(packet/'boundary_probe.cpp',bench/'boundary_probe.cpp')
fw=root/'sw/firmware/ctrl'; rtl=root/'hdl/milan/mailbox'
files=[gen/'KL_mbx_pkg.sv',*[rtl/(x+'.sv') for x in ('KL_mbx_ring','KL_mbx_rx','KL_mbx_tx','KL_mbx_evt')],gen/'KL_mbx.sv',rtl/'KL_mbx_wb.sv',rtl/'KL_mbx_axil.sv',bench/'tb_mbx_top.sv']
def run(cmd):
 print('COMMAND',*map(str,cmd),flush=True)
 subprocess.run(list(map(str,cmd)),cwd=bench,check=True)
for host in (0,1):
 out=bench/('probe-'+str(host))
 run([exe,'--cc','--exe','--build','-j','2','--top-module','tb_mbx_top','-Wall','-Wno-fatal','-Werror-USERERROR','-Werror-PINMISSING','-Werror-UNDRIVEN','-Wno-DECLFILENAME','-Wno-UNUSEDPARAM','-Wno-UNUSEDSIGNAL','-CFLAGS','-std=c++17 -O2 -I'+str(gen),'-GHOST_P='+str(host),'--Mdir',out,*files,bench/'boundary_probe.cpp','-o','probe'])
 run([out/'probe',str(host)])
run(['c++','-std=c++17','-O2','-DPROBE_MODEL','-I'+str(gen),'-I'+str(bench),'-I'+str(fw/'test'),'-I'+str(fw/'host'),bench/'boundary_probe.cpp',bench/'obj_if2/mbx_model.o','-o',bench/'probe-model'])
run([bench/'probe-model'])
