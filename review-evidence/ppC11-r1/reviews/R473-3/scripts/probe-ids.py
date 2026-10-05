#!/usr/bin/env python3
"""Independent ID fault and self-test-sensitivity checks in disposable trees."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

source, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
scratch, receipts = packet/'scratch', packet/'receipts'
os.environ['TMPDIR'] = str(scratch)
tempfile.tempdir = str(scratch)
sys.dont_write_bytecode = True
checker = source/'scripts/check-ids.py'
spec = importlib.util.spec_from_file_location('ids', checker)
ids = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ids)
cases = [
 ('continued-optional-good', 'T-ADP-\nDELAY(-START)', []),
 ('continued-optional-bad', 'T-ADP-\nDELAY(-STRT)', ['T-ADP-DELAY-STRT']),
 ('optional-break-good', 'T-ADP-DELAY(-\n// START)', []),
 ('optional-break-bad', 'T-ADP-DELAY(-\n// STRT)', ['T-ADP-DELAY-STRT']),
 ('both-breaks-good', 'T-ADP-\n// DELAY(-\n// START)', []),
 ('both-breaks-bad', 'T-ADP-\n// DELAY(-\n// STRT)', ['T-ADP-DELAY-STRT']),
 ('missing-minus-one-base', 'P-MISSING-1', ['P-MISSING-1']),
 ('registered-minus-one', 'P-RX-SLOTS-1', []),
 ('minus-two', 'P-RX-SLOTS-2', ['P-RX-SLOTS-2']),
 ('continued-braces-bad', 'T-NVM-\n// RS-{DEADLINE, TYPO}', ['T-NVM-RS-TYPO']),
 ('continued-family-good', 'T-MRP-\n// JOIN-*', []),
 ('successive-break-good', 'T-ADP-\n// DELAY-\n// START', []),
 ('successive-break-bad', 'T-ADP-\n// DELAY-\n// STRT', ['T-ADP-DELAY-STRT']),
 ('continued-sibling-bad', 'T-BUDGET-\n// AECP-TYP / -XX', ['T-BUDGET-AECP-XX']),
 ('optional-malformed', 'T-ADP-\n// DELAY(-start)', ['T-ADP-DELAY(-...)']),
 ('braced-hyphen-bad', 'T-NVM-{RS-DEADLINE,RS-TYPO}', ['T-NVM-RS-TYPO']),
]
records=[]
for n,(name,body,expected) in enumerate(cases):
 with tempfile.TemporaryDirectory(prefix='ids-probe-',dir=scratch) as tmp:
  root=Path(tmp)
  subprocess.run(['git','init','-q',str(root)],check=True)
  for path,text in {str(ids.PARAMS):ids.SELFTEST_PARAMS,
                    str(ids.TIMING):ids.SELFTEST_TIMING,
                    ids.CASE:body}.items():
   p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
  cp=subprocess.run([sys.executable,str(checker),'--root',str(root)],text=True,capture_output=True)
  got=ids.findings(cp.stdout)
  record={'name':name,'input':body,'rc':cp.returncode,'stdout':cp.stdout,
          'expected':expected,'got':got}
  records.append(record)
  assert cp.returncode == bool(expected) and got == expected,record

text=checker.read_text()
mutants={
 'any-minus-one':('token.endswith("-1") and token[:-2] in rows','token.endswith("-1")'),
 'skip-line-broken-optional':(
     'if optional:\n                yield line, f"{token}-{optional.group(1)}", "id"',
     'if optional:\n                if "\\n" not in optional.group(0):\n                    yield line, f"{token}-{optional.group(1)}", "id"'),
}
for name,(old,new) in mutants.items():
 assert text.count(old)==1,(name,text.count(old))
 path=scratch/(name+'.py');path.write_text(text.replace(old,new))
 cp=subprocess.run([sys.executable,str(path),'--selftest'],text=True,capture_output=True)
 (receipts/(name+'.log')).write_text(cp.stdout+cp.stderr)
 (receipts/(name+'.rc')).write_text(str(cp.returncode)+'\n')
 records.append({'name':name,'rc':cp.returncode,'stdout':cp.stdout})
 assert cp.returncode==1 and 'SELFTEST FAIL:' in cp.stdout

# Regression control: execute the previous parser with the new test cases.
old=subprocess.check_output(['git','-C',str(source),'show','80588cdc:scripts/check-ids.py'],text=True)
for name,(before,after) in mutants.items():
 assert old.count(before)==1
 path=scratch/('round2-'+name+'.py');path.write_text(old.replace(before,after))
 cp=subprocess.run([sys.executable,str(path),'--selftest'],text=True,capture_output=True)
 (receipts/('round2-'+name+'.log')).write_text(cp.stdout+cp.stderr)
 (receipts/('round2-'+name+'.rc')).write_text(str(cp.returncode)+'\n')
 assert cp.returncode==0,cp.stdout
 records.append({'name':'round2-'+name,'rc':cp.returncode,'stdout':cp.stdout})
start=text.index('SELFTEST_CASES = (');end=text.index('\nUSE_FAIL =',start)
o_start=old.index('SELFTEST_CASES = (');o_end=old.index('\nUSE_FAIL =',o_start)
path=scratch/'previous-parser-new-tests.py'
path.write_text(old[:o_start]+text[start:end]+old[o_end:])
cp=subprocess.run([sys.executable,str(path),'--selftest'],text=True,capture_output=True)
(receipts/'previous-parser-new-tests.log').write_text(cp.stdout+cp.stderr)
(receipts/'previous-parser-new-tests.rc').write_text(str(cp.returncode)+'\n')
assert cp.returncode==1 and 'T-ADP-DELAY-STRT' in cp.stdout
records.append({'name':'previous-parser-new-tests','rc':cp.returncode,'stdout':cp.stdout})
(receipts/'id-probes.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(cases)} independent forms passed; both weakened parsers and previous parser rejected')
