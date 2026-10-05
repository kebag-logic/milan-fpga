#!/usr/bin/env python3
"""Independent ID controls and parser mutations; edits disposable trees only."""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('packet', type=Path)
ap.add_argument('--jobs', type=int, default=4)
a = ap.parse_args()
assert 1 <= a.jobs <= 16
root, packet = a.root.resolve(), a.packet.resolve()
scratch = packet / 'scratch' / 'ids'
scratch.mkdir(parents=True, exist_ok=True)
src = (root / 'scripts/check-ids.py').read_text()
spec = importlib.util.spec_from_file_location('gate', root / 'scripts/check-ids.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
cases = [
 ('minus-one-missing', 'P-MISSING-1', 1, 'P-MISSING-1'),
 ('minus-one-valid', 'P-RX-SLOTS-1', 0, None),
 ('minus-two-invalid', 'P-RX-SLOTS-2', 1, 'P-RX-SLOTS-2'),
 ('optional-newline-missing', 'T-ADP-DELAY(-\n// STRT)', 1, 'T-ADP-DELAY-STRT'),
 ('composition-missing', 'T-ADP-\n// DELAY(-STRT)', 1, 'T-ADP-DELAY-STRT'),
 ('composition-double-missing', 'T-ADP-\n// DELAY(-\n// STRT)', 1, 'T-ADP-DELAY-STRT'),
 ('composition-valid', 'T-ADP-\n// DELAY(-START)', 0, None),
 ('composition-double-valid', 'T-ADP-\n// DELAY(-\n// START)', 0, None),
 ('successive-valid', 'T-ADP-\n// DELAY-\n// START', 0, None),
 ('braced-hyphen-missing', 'T-NVM-{RS-DEADLINE, RS-AGREGATE}', 1, 'T-NVM-RS-AGREGATE'),
 ('continued-brace', 'T-NVM-\n// RS-{DEADLINE, TYPO}', 1, 'T-NVM-RS-TYPO'),
 ('continued-sibling', 'T-BUDGET-\n// AECP-TYP / -XX', 1, 'T-BUDGET-AECP-XX'),
 ('continued-family', 'T-NO-\n// FAMILY-*', 1, 'T-NO-FAMILY-*'),
 ('malformed-optional', 'T-ADP-\n// DELAY(-start)', 1, 'T-ADP-DELAY(-...)'),
]
for leader in ('', '// ', '# ', '-- ', '* ', '; ', '> '):
 cases.append(('leader-'+str(len(cases)), 'T-ADP-\r\n'+leader+'DELAY(-STRT)', 1, 'T-ADP-DELAY-STRT'))

def run_case(c):
 name, body, expected, token = c
 tree = scratch / name
 tree.mkdir(exist_ok=True)
 subprocess.run(['git', 'init', '-q', str(tree)], check=True)
 for rel, value in {str(gate.PARAMS):gate.SELFTEST_PARAMS, str(gate.TIMING):gate.SELFTEST_TIMING, 'tb/probe.md':body}.items():
  f=tree/rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(value)
 p=subprocess.run([sys.executable, str(root/'scripts/check-ids.py'), '--root', str(tree)], capture_output=True,text=True)
 ok=p.returncode==expected and (token is None or gate.findings(p.stdout)==[token])
 return dict(name=name,rc=p.returncode,expected_rc=expected,token=token,ok=ok,stdout=p.stdout,stderr=p.stderr)

with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
 results=list(pool.map(run_case,cases))
mutants={
 'any-minus-one': src.replace('(token.endswith("-1") and token[:-2] in rows)', 'token.endswith("-1")'),
 'skip-linebroken-optional': src.replace('if optional:\n                yield line, f"{token}-{optional.group(1)}", "id"', 'if optional:\n                if "\\n" not in optional.group(0):\n                    yield line, f"{token}-{optional.group(1)}", "id"'),
}
old=subprocess.check_output(['git','-C',str(root),'show','80588cdc43ca5605a1d3748d13dd8ed7f22f7000:scripts/check-ids.py'],text=True)
mutants['previous-parser-new-plants']=src[:src.index('def uses(')]+old[old.index('def uses('):old.index('def resolves(')]+src[src.index('def resolves('):]
for name, mutated in mutants.items():
 assert mutated != src, name
 f=scratch/(name+'.py'); f.write_text(mutated)
 p=subprocess.run([sys.executable,str(f),'--selftest'],capture_output=True,text=True)
 results.append(dict(name=name,rc=p.returncode,expected_rc=1,ok=p.returncode==1 and 'SELFTEST FAIL:' in p.stdout,stdout=p.stdout,stderr=p.stderr))
(packet/'receipts/ids-probes.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results:
 print(r['name'], 'PASS' if r['ok'] else 'FAIL', 'rc',r['rc'])
 print(r['stdout'],end='')
assert all(r['ok'] for r in results)
