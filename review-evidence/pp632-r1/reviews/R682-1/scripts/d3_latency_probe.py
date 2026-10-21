#!/usr/bin/env python3
"""Disposable probe: measure each arm and repeat the unchanged D3S5 assertions."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
p = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve()
tree = p/'scratch/d3-latency'
skip = shutil.ignore_patterns('obj*', '*.hex', '__pycache__')
for d in ('hdl','tb/common','tb/pp_top'):
    shutil.copytree(root/d, tree/d, ignore=skip)
main = tree/'tb/pp_top/sim_main.cpp'
s = main.read_text()
start = s.index('  D3OwnershipPhase{h, image}.run();', s.index('static void run_d3'))
end = s.index('  printf("D3:', start)
s = s[:start] + '''  D3ServicePhase phase{h, image};
  phase.power_up();
  const long unset = phase.write_latency(D3ServicePhase::pl_ptof(0, 4000000));
  phase.settle(3 * D3ServicePhase::WINDOW);
  const long set = phase.write_latency(D3ServicePhase::pl_ptof(0, 4000001));
  printf("LATENCY_PROBE unset=%ld set=%ld delta(set-unset)=%ld\\n", unset, set, set-unset);
  phase.s5_a_change_on_the_done_edge_wins();
''' + s[end:]
main.write_text(s)
env = dict(os.environ, TMPDIR=str(p/'scratch'), PYTHONDONTWRITEBYTECODE='1')
def run(tag, argv):
    with (p/'receipts'/f'{tag}.log').open('w') as f:
        rc=subprocess.run(argv,cwd=tree/'tb/pp_top',env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (p/'receipts'/f'{tag}.rc').write_text(str(rc)+'\n')
    return rc
assert run('d3-latency-build',['make','-j16','gsi-build','VERILATOR='+str(p/'scripts/limited-simulator.py')])==0
assert run('d3-latency',['./obj_dir/Vpp_top_sim','--d3-only'])==0
hpp=tree/'tb/pp_top/d3_phases.hpp'
txt=hpp.read_text()
old='    const bool primed = set_ok(AEM_SET_STREAM_INFO, pl_ptof(0, 3999999));'
assert txt.count(old)==1
hpp.write_text(txt.replace(old, '    const bool primed = true; // probe: reproduce pre-fix setup'))
assert run('d3-unprimed-build',['make','-j16','gsi-build','VERILATOR='+str(p/'scripts/limited-simulator.py')])==0
rc=run('d3-unprimed',['./obj_dir/Vpp_top_sim','--d3-only'])
assert rc != 0
log=(p/'receipts/d3-unprimed.log').read_text()
assert 'FAIL: D3S5 premise:' in log
print((p/'receipts/d3-latency.log').read_text())
print(log)
