#!/usr/bin/env python3
"""Reproduce the focused review without changing tracked source files."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--sim',required=True)
a=p.parse_args()
packet=Path(__file__).resolve().parents[1]
scratch=packet/'scratch'
receipts=packet/'receipts'
def run(name,argv):
    return subprocess.run(['python3',str(packet/'scripts/run_receipt.py'),'--cwd',str(a.repo),name,'--',*map(str,argv)],check=True)
def build(suite,name,extra=()):
    return run(name+'-build',['make','-j16','-C','tb/verilator/'+suite,'build','VERILATOR='+a.sim,'VERILATOR_JOBS=8','MDIR='+str(scratch/name),*extra])
with ThreadPoolExecutor(max_workers=2) as pool:
    fs=[pool.submit(build,'chmap_capture','chmap'),pool.submit(build,'follow_ring','fine',('CLK_HZ=25000000','FRAME_DIV=64'))]
    for f in fs:f.result()
build('follow_ring','coarse')
run('controller',['python3','tb/verilator/follow_ring/settle_control.py','--sim',a.sim,'--out',scratch/'control','--jobs','1'])
with ThreadPoolExecutor(max_workers=3) as pool:
    fs=[pool.submit(run,'chmap-run',[scratch/'chmap/Vchmap_wrap']),
        pool.submit(run,'fine-campaign',['python3','tb/verilator/follow_ring/small_pulls.py','--exe',scratch/'fine/Vfollow_ring','--out',receipts/'fine','--jobs','4']),
        pool.submit(run,'pullin-campaign',['python3','tb/verilator/follow_ring/sweep.py','pullin','--exe',scratch/'coarse/Vfollow_ring','--out',receipts/'pullin','--jobs','4','--hold-us','52','56','--phases','16'])]
    for f in fs:f.result()
run('own-faults',['python3',packet/'scripts/fault_probes.py','--repo',a.repo,'--sim',a.sim,'--jobs','2'])
run('traceability',['python3','docs/traceability/gen_module_matrix.py','--check'])
run('public-independent-audit',['python3',packet/'scripts/audit_public.py','--repo',a.repo])
run('final-tree',['python3',packet/'scripts/verify_tree.py','--repo',a.repo])
