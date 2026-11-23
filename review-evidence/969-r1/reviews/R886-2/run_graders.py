#!/usr/bin/env python3
"""Repeat the lightweight graders: CHECKOUT PACKET. No timing simulations."""
import concurrent.futures as cf
import json
from pathlib import Path
import subprocess
import sys
root, packet = (Path(x).resolve() for x in sys.argv[1:3])
commands = [('kept-selftest', 'kept_grade.py', ['--selftest']),
            ('flip-1x1', 'flip_grade.py', ['--check','--point','1x1/1if']),
            ('flip-8x8', 'flip_grade.py', ['--check','--point','8x8/1if']),
            ('load', 'load_grade.py', ['--check']),
            ('shape', 'shape_costs.py', ['--check'])]
def run(item):
    name, script, args = item
    command = [sys.executable, '-B', str(root/'tb/verilator/ctrl_service_budget'/script), *args]
    r = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (packet/(name+'.log')).write_text(r.stdout.replace(str(root),'<checkout>').replace(str(packet),'<packet>'))
    (packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
    return dict(name=name, rc=r.returncode)
with cf.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, commands))
print(json.dumps(results, indent=2))
sys.exit(any(r['rc'] for r in results))
