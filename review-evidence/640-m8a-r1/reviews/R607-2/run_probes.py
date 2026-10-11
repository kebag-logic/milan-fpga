#!/usr/bin/env python3
"""Run independent probes after run_focused.py, awaiting every foreground child."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--litex-python', required=True)
ap.add_argument('--label', default='independent')
a = ap.parse_args()
p = Path(__file__).resolve().parent
env = json.loads((p/'scratch/run-environment.json').read_text())
tree = p/'scratch/test-tree'
work = p/'scratch'/a.label
work.mkdir(exist_ok=True)
jobs = {
    a.label+'-elf': ('probe_elf_loads.py', [tree, work/'elf']),
    a.label+'-soc': ('probe_load_soc.py', [tree, work/'soc']),
    a.label+'-bus': ('probe_memory_bus.py', [tree]),
}

def run(item):
    name,(script,args) = item
    with (p/'receipts'/(name+'.log')).open('w') as log:
        rc = subprocess.run([a.litex_python,str(p/script),*map(str,args)], env=env,
                            stdout=log,stderr=subprocess.STDOUT).returncode
    (p/'receipts'/(name+'.rc')).write_text(str(rc)+'\n')
    return name,rc

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run,jobs.items()))
for result in results:
    print(*result)
raise SystemExit(int(any(rc for _,rc in results)))
