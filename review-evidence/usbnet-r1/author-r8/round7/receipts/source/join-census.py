"""Join disjoint completed partitions only after all per-case replay receipts exist."""
import hashlib,json,sys
from pathlib import Path
root=Path.cwd();scratch=Path('$VALIDATION_STORAGE/usbnet-a855/round7')
a=scratch/'census';b=scratch/'census-supplemental'
packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'));import build
part=json.loads((packet/'census-partition.json').read_text())
left=json.loads((a/'completed.json').read_text());right=json.loads((b/'completed.json').read_text())
keys=lambda rows:{(r['variant'],r['group']) for r in rows}
assert keys(left)=={tuple(x) for x in part['original']}
assert keys(right)=={tuple(x) for x in part['supplemental']}
assert not keys(left)&keys(right)
rows=left+right
manifest=json.loads((a/'manifest.json').read_text())
expected={(v,g) for v,gs in manifest['groups'].items() for g in gs}
assert keys(rows)==expected and len(rows)==len(expected)==159
assert {(f.parent.name,f.stem) for f in (packet/'egress-cases').glob('*/*.json')}==expected
moves=[];scripts=[]
for variant in manifest['groups']:
 old,new=build.reused(a/variant),build.reused(b/variant)
 assert old['executable_sha256']==new['executable_sha256']
 for f in (b/variant/'results').iterdir():
  assert f.is_file()
  target=a/variant/'results'/f.name;assert not target.exists(),target
  digest=hashlib.sha256(f.read_bytes()).hexdigest();f.rename(target)
  moves.append(dict(source=str(f),target=str(target),sha256=digest))
for r in rows:
 path=a/r['variant']/'results'/(r['group']+'.log')
 assert hashlib.sha256(path.read_bytes()).hexdigest()==r['trace_sha256']
 script=path.with_suffix('.txt')
 prior=Path('$VALIDATION_STORAGE/artysplit-a829/r10/final-census')/r['variant']/'results'/script.name
 assert script.read_bytes()==prior.read_bytes(),script
 scripts.append(dict(case=r['variant']+'/'+r['group'],sha256=hashlib.sha256(script.read_bytes()).hexdigest(),baseline_identical=True))
(a/'completed.json').write_text(json.dumps(rows,indent=2)+'\n')
findings=[r for r in rows if r['native_status'] or any(r[k] for k in ('refusals','share','late','forbidden'))]
(a/'findings.json').write_text(json.dumps(findings,indent=2)+'\n')
manifest.update(status='NATIVE MEASUREMENTS COMPLETE; FINAL COST AND CLASS CHECKS REQUIRED',completed=len(rows),partition=part,max_native_legs=96,assigned_cpu_count=32)
(a/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
import shutil
shutil.copyfile(a/'window-stop.json',packet/'partition-boundary.json')
(a/'window-stop.json').rename(a/'partition-boundary.json')
(packet/'census-join.json').write_text(json.dumps(dict(moves=moves,stimulus_identity=scripts,completed=len(rows),findings=len(findings)),indent=2)+'\n')
print('JOINED',len(rows),'cases; every stimulus byte-identical to baseline;',len(findings),'finding cases')
