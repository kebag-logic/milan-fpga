"""Retain bounded evidence copies and hash the full reports in place."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path('$LANES/395-timing-grade')
OUT = Path('$MANAGEMENT/2026-09-23/395-a390')
WORK = Path('$VALIDATION_STORAGE/395-a390-work')
SHIPPING = Path('$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9')
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
reports = WORK/('final-'+head[:9])

def fingerprint(path):
    with path.open('rb') as stream:
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}

rows=[]
for path in sorted(reports.iterdir()):
    if not path.is_file() or path.suffix not in ('.rpt','.txt','.tcl','.log'):
        continue
    row={'source':str(path),**fingerprint(path)}
    if row['bytes']<=200000:
        target=OUT/'reports'/path.name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(path,target)
        row['copy']=str(target.relative_to(OUT))
    rows.append(row)
(OUT/'report-artifacts.json').write_text(json.dumps(rows,indent=2)+'\n')
gates=json.loads((OUT/'gate-results.json').read_text())
assert len(gates)==19 and all(r['returncode']==0 and r['head']==head for r in gates),gates
for row in gates:
    path=Path(row['log'])
    assert fingerprint(path)=={'bytes':row['bytes'],'sha256':row['sha256']},row
    if row['bytes']<=200000:
        target=OUT/'gates'/path.name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(path,target)
inputs=json.loads((OUT/'shipping-inputs-before.json').read_text())
after={name:fingerprint(SHIPPING/name) for name in inputs}
assert inputs==after,'shipping inputs changed'
(OUT/'shipping-inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
for mode in ('present','absent'):
    text=(WORK/('gates-'+head[:9])/('builder-'+mode+'.log')).read_text()
    selected=[line for line in text.splitlines() if '[timing grade]' in line or re.search(r'\[gate [^]]+\] SKIP:',line) or 'GATE ARM(S) DID NOT RUN' in line or line.startswith(('ALL GATES','Full builder bank completed'))]
    (OUT/('builder-'+mode+'-summary.txt')).write_text('\n'.join(selected)+'\n')
print('All 19 gates rc 0 at',head)
print('Seven shipping input size/hash pairs unchanged.')
print('Retained',len(rows),'report fingerprints; copied only files at most 200000 bytes.')
