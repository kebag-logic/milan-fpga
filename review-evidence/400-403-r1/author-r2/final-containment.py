import hashlib, json, subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
def git(*args):
 return subprocess.check_output(['git',*args],text=True)
expected=json.loads((p/'validated-inputs.json').read_text())
assert git('rev-parse','HEAD').strip()==expected['head']
assert git('branch','--show-current').strip()=='400-403-declaration-truth'
assert git('remote','get-url','origin').strip()=='https://github.com/kebag-logic/milan-fpga.git'
assert git('rev-parse','origin/dev').strip()==expected['base']
assert not git('status','--porcelain','--untracked-files=all')
for row in expected['files']:
 assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
print('All 25 changed-file fingerprints match the final committed head; root working tree clean')
for line in git('submodule','status','--recursive').splitlines():
 assert line.startswith(' '),line
 path=line.split()[1]
 assert not git('-C',path,'status','--porcelain','--untracked-files=all'),path
 print('Clean pinned submodule:',line.strip())
same=['protocol-processor','gptp-processor','syn/yosys/rom_digests.tsv',
      'docs/diagrams/submodule_boundaries.drawio','docs/diagrams/submodule_boundaries.svg',
      'docs/diagrams/submodule_boundaries.png','docs/diagrams/PNG_MANIFEST.json']
subprocess.run(['git','diff','--exit-code',expected['base'],'--',*same],check=True)
print('Dev pins, ROM ledger and regenerated submodule diagram assets match required dev')
subprocess.run(['git','diff','--check'],check=True)
subprocess.run(['git','diff','--check',expected['base']],check=True)
print('Both working-tree and full bundle diff checks pass')
rows=[json.loads(x) for x in (p/'gate-results.jsonl').read_text().splitlines()]
last={r['name']:r for r in rows}
for name in ['builder-sdk-final','builder-absent-final']+[f'milan-dp-{i:02}' for i in range(46)]:
 assert name in last and last[name]['exit']==0,(name,last.get(name))
print('Both full builder modes and all 46 default sweep entries have zero exit receipts')
print('FINAL HEAD:',expected['head'])
