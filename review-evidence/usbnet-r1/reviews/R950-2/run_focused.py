#!/usr/bin/env python3
"""Run bounded review checks in the foreground; all disposable outputs stay in scratch."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))
compiler = Path(os.environ['REVIEW_VERILATOR'])
version = subprocess.check_output([str(compiler), '--version'], text=True).strip()
assert 'Verilator 5.050 ' in version, version
runtime = subprocess.check_output([str(compiler), '-getenv', 'VERILATOR_ROOT'], text=True).strip()
(packet / 'compiler-identity.json').write_text(json.dumps({'version': version, 'sha256': hashlib.sha256(compiler.read_bytes()).hexdigest()}, indent=2)+'\n')
env['PATH'] = str(compiler.parent) + os.pathsep + env['PATH']
commands = {
    'rtl-focused': ['make', '-j16', '-C', 'tb/verilator/usbnet', 'JOBS=2', 'tap', 'leds', 'truth', 'local', 'wait', f'VERILATOR={compiler}', f'OBJ={scratch / "rtl"}'],
    'ledger-controls': ['python3', '-B', 'tb/verilator/ctrl_service_budget/egress_ledger.py', '--selftest'],
    'injection-controls': ['python3', '-B', 'tb/verilator/usbnet/egress_controls.py'],
    'inventory-check': ['python3', '-B', 'scripts/docs_inventory.py', '--check'],
    'suite-registration': ['python3', '-B', 'scripts/suite_shards.py', '--selftest'],
}
def run(item):
    name, command = item
    result = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    text = result.stdout.replace(str(root), '$REVIEW_ROOT').replace(str(packet), '$REVIEW_PACKET').replace(str(compiler.parent), '$SCOPED_COMPILER').replace(runtime, '$COMPILER_RUNTIME')
    (packet / (name + '.log')).write_text(text)
    (packet / (name + '.rc')).write_text(str(result.returncode)+'\n')
    return {'name':name, 'command':[str(x).replace(str(packet), '$REVIEW_PACKET').replace(str(compiler), '$SCOPED_COMPILER/verilator') for x in command], 'returncode':result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,commands.items()))
(packet/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
sys.exit(any(r['returncode'] for r in results))
