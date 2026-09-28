"""Publish a compact final evidence index without copying generated trees."""
from pathlib import Path
import hashlib
import json
import subprocess
out = Path(__file__).parent
root = Path.cwd()
head = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
artifacts = []
for name in ('capture-artifacts-final.json', 'service-artifacts-final.json',
             'final-gates.json', 'final-builder-gates.json', 'final-target-gates.json', 'control-artifacts-final.json'):
    rows=json.loads((out/name).read_text())
    for row in rows:
        p=Path(row['path'])
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
        artifacts.append(dict(path=str(p),size=row['size'],sha256=row['sha256']))
artifacts=list({r['path']:r for r in artifacts}.values())
text='# Final evidence artifacts\n\nThe final firmware measurements use `final3` build directories. Earlier runs and their receipts are historical.\nThe following generated files remain outside this packet; their exact size and digest are retained.\n\n| Path | Bytes | SHA-256 |\n| --- | --- | --- |\n'
text+=''.join('| `'+r['path']+'` | '+str(r['size'])+' | `'+r['sha256']+'` |\n' for r in artifacts)
(out/'ARTIFACTS.md').write_text(text)
for p in out.rglob('*'):
    if p.is_file(): assert p.stat().st_size <= 200000, str(p)
files={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.iterdir())
       if p.is_file() and p.name!='EVIDENCE.json'}
fw=root/'sw/firmware/milan_baremetal/milan_baremetal.c'
(out/'EVIDENCE.json').write_text(json.dumps(dict(head=head,committed=True,
    firmware_sha256=sha(fw),firmware_bytes=fw.stat().st_size,
    processor_pin='16be6768f710e79450aace277abacd6c2c3336e5',
    final_measurement_generation='final3', historical_generations=['initial','final2'],
    capture_arms=6,captures_per_arm=16,service_plans=10,
    physical_acceptance_599_4='deferred to the later bench lane', files=files),indent=2)+'\n')
print('Final packet indexed',head,len(files),'files')
