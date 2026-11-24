"""Fresh linked products and exact AX identity, within the shared four-leg pool."""
import hashlib,json,subprocess,sys
from pathlib import Path
from harness_slots import slot
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected');root=Path.cwd()
records=[]
for helper in ('identity-final-build.py','arty-product-final-build.py'):
 with slot(helper):
  with (r/(helper+'.log')).open('w') as sink:
   result=subprocess.run([sys.executable,'-B',str(r/helper)],stdout=sink,stderr=subprocess.STDOUT,timeout=10800)
 records.append(dict(helper=helper,returncode=result.returncode))
 (r/'final-products-commands.json').write_text(json.dumps(records,indent=2)+'\n')
 if result.returncode:raise SystemExit(result.returncode)
prior=json.loads((r/'identity-compare.json').read_text());rows=[]
for row in prior['rows']:
 old=r/'identity-before'/row['file'];new=r/'identity-final'/row['file']
 a,b=old.read_bytes(),new.read_bytes()
 assert hashlib.sha256(a).hexdigest()==row['sha256'],old
 rows.append(dict(file=row['file'],bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),identical=a==b))
result=dict(status='PASS' if all(x['identical'] for x in rows) else 'FAIL',baseline='4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2',
            scope=prior['scope'],rows=rows,changed=[x['file'] for x in rows if not x['identical']])
(r/'identity-final-compare.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],len(rows),'AX generated and product artifacts',flush=True)
raise SystemExit(result['status']!='PASS')
