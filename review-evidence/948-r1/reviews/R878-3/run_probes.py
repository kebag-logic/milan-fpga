#!/usr/bin/env python3
"""Focused review probes. Usage: run_probes.py SOURCE PINNED_EXECUTABLE.

All children are waited for by this foreground driver. Four concurrent builds,
four compiler jobs each. Disposable source/build files stay under scratch.
"""
import concurrent.futures as cf
import hashlib
import os
from pathlib import Path
import subprocess as sp
import sys

source = Path(sys.argv[1]).resolve()
exe = Path(sys.argv[2]).resolve()
out = Path(__file__).resolve().parent
scratch = out / 'scratch'
head = '64117b77cb9e5c421717835b5be032b5905c447d'
def run(args, **kw):
    return sp.run(args, check=True, **kw)
def git(*args):
    return sp.check_output(['git', '-C', str(source), *args])
assert git('rev-parse', 'HEAD').decode().strip() == head
(out/'tool-identity.txt').write_text(sp.check_output([str(exe), '--version']).decode() + 'Executable SHA256 ' + hashlib.sha256(exe.read_bytes()).hexdigest()+'\n')
trees = {}
for name in ('control', 'bubbles'):
    tree = scratch / name
    if not tree.exists():
        run(['git','clone','--quiet','--shared',str(source),str(tree)])
        run(['git','-C',str(tree),'checkout','--quiet','--detach',head])
        run(['git','-C',str(tree),'-c','protocol.file.allow=always','-c',f'submodule.third_party/verilog-axis.url={source}/third_party/verilog-axis','submodule','update','--init','third_party/verilog-axis'],stdout=sp.DEVNULL)
    trees[name] = tree
# Reproduce the original probe with its original bench, current production RTL.
bubble = trees['bubbles']
for name in ('sim_depkt.cpp', 'sim_fanout.cpp'):
    rel = 'tb/verilator/avtp_rxmon/'+name
    (bubble/rel).write_bytes(git('show','64e55a59:'+rel))
plant = out/'plant_tap_bubbles.py'
run([sys.executable,str(plant),str(bubble)],stdout=sp.DEVNULL)
mon = source/'hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv'
for width in (3,6):
    text=mon.read_text().replace('        depkt_urg_w = 1\'b1;', '        depkt_urg_w = 1\'b0;')
    if width==3: text=text.replace('DEPKT_PEND_W_C = 6;', 'DEPKT_PEND_W_C = 3;')
    (scratch/f'monitor-{width}.sv').write_text(text)
flags = '--cc --exe --build -j 4 --top-module avtp_rxmon_nx_wrap -GCLK_FREQ_HZ_P=100000 +incdir+../../../hdl/common +incdir+../../../hdl/ieee1722/avtp -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
def campaign(name, tree, override=None):
    build = scratch/('build-'+name)
    args=['make','-j4','-C',str(tree/'tb/verilator/avtp_rxmon'),'fanout-build',f'VERILATOR={exe}',f'FO_MDIR={build}',f'NXFLAGS={flags}']
    if override: args.append('RXMON_SRC='+str(override))
    with (out/(name+'-build.log')).open('w') as log:
        rc=sp.run(args,stdout=log,stderr=sp.STDOUT).returncode
    assert rc==0,(name,'build',rc)
    with (out/(name+'.log')).open('w') as log:
        rc=sp.run([str(build/'Vavtp_rxmon_fanout')],stdout=log,stderr=sp.STDOUT).returncode
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    text=(out/(name+'.log')).read_text()
    fails=[x for x in text.splitlines() if '[FAIL]' in x]
    if name=='control': assert rc==0
    elif name=='bubbles':
        assert not any('[FO10]' in x for x in fails),fails
        assert all('[FO4]' in x for x in fails),fails
    else:
        assert rc==1 and any('[FO15] every accepted PDU is delivered' in x for x in fails)
    return name,rc,fails
jobs=[('control',trees['control'],None),('bubbles',bubble,None),('plant3',trees['control'],scratch/'monitor-3.sv'),('plant6',trees['control'],scratch/'monitor-6.sv')]
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(lambda a:campaign(*a),jobs))
with (out/'probe-summary.txt').open('w') as f:
    for name,rc,fails in results:
        f.write(f'{name}: rc={rc}, failed checks={len(fails)}\n')
        f.write('\n'.join(fails)+'\n')
        print(name,rc,len(fails),flush=True)
print('All foreground-owned probes completed.',flush=True)
