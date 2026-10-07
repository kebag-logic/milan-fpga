#!/usr/bin/env python3
"""Independent disposable RTL faults; compile each before judging its rejection."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--sim', required=True)
p.add_argument('--jobs', type=int, default=2)
a = p.parse_args()
assert 1 <= a.jobs <= 2
packet = Path(__file__).resolve().parents[1]
scratch = packet / 'scratch' / 'faults'
receipts = packet / 'receipts' / 'faults'
receipts.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('controller', a.repo / 'tb/verilator/follow_ring/settle_control.py')
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
dp = (a.repo / 'hdl/milan/milan_datapath.sv').read_text()
begin = dp.index('  localparam int unsigned SRC_SETTLE_ERR_C')
end = dp.index('  end : g_settle_recentre', begin) + len('  end : g_settle_recentre')
control_source = dp[begin:end]
capture = (a.repo / 'hdl/ieee1722/aaf/KL_chan_map_capture.sv').read_text()

def run(name, kind, old, new, expected):
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    source = capture if kind == 'capture' else control_source
    assert source.count(old) == 1, (name, source.count(old))
    planted = source.replace(old, new)
    (receipts / (name + '.mutation.json')).write_text(json.dumps({'kind':kind,'old':old,'new':new,'expected':expected}, indent=2)+'\n')
    if kind == 'capture':
        path = work / 'capture.sv'
        path.write_text(planted)
        cwd = a.repo
        build = ['make','-j16','-C','tb/verilator/chmap_capture','build',f'VERILATOR={a.sim}', 'VERILATOR_JOBS=8',f'MDIR={work}',f'CMAP_SRC={path}']
        exe = work / 'Vchmap_wrap'
    else:
        path = work / 'settle_control.sv'
        path.write_text(controller.HEADER.replace('AXIS_RATE','25000000')+planted+controller.DRIVER)
        cwd = work
        build = [a.sim,'--binary','--timing','-j','8','-Wno-fatal','--top-module','settle_control',str(path)]
        exe = work / 'obj_dir/Vsettle_control'
    for leg,cmd in [('build',build),('run',[str(exe)])]:
        stem = receipts / (name + '-' + leg)
        stem.with_suffix('.command.json').write_text(json.dumps({'cwd':str(cwd),'argv':cmd},indent=2)+'\n')
        with stem.with_suffix('.log').open('w') as f:
            rc = subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT).returncode
        stem.with_suffix('.rc').write_text(str(rc)+'\n')
        if leg == 'build':
            assert rc == 0, name+' did not compile'
        else:
            output = stem.with_suffix('.log').read_text()
            killed = rc != 0 and expected in output
            print(name, 'KILLED' if killed else 'SURVIVED', 'rc', rc, flush=True)
            return {'name':name,'rc':rc,'killed':killed,'expected':expected}

cases = [
 ('one-sided','capture',"? LB_DROPW_C'(32'(rc_left_w) - LB_LEFT_C) : '0;", "? LB_DROPW_C'(0) : '0;", '[FAIL] LRC: ten left drops five excess events on both pairs'),
 ('settle-counted','capture',"17'(lb_dup_cnt_o) + 17'(pop_dup_w)", "17'(lb_dup_cnt_o) + 17'(pop_dup_w || pop_hold_w)", '[FAIL] LRC: no recentre moved the dup counter'),
 ('high-band','control','SETTLE_EXC_ERR_C   = 2;', 'SETTLE_EXC_ERR_C   = 10;', 'excursion did not arm'),
 ('quiet-band','control','SETTLE_EXC_ERR_C   = 2;', 'SETTLE_EXC_ERR_C   = 0;', 'quiet noise armed'),
 ('early-rearm','control',"settle_run_ticks_r >= SETTLE_RUN_W_C'(SRC_SETTLE_TICKS_C)", "settle_run_ticks_r >= SETTLE_RUN_W_C'(1024)", 're-armed before quiet dwell'),
]
with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results = list(pool.map(lambda c:run(*c),cases))
(receipts / 'summary.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(0 if all(r['killed'] for r in results) else 1)
