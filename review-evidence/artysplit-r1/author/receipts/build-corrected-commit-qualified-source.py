"""Freeze exactly the tested source, plus its final qualified documentation."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
assert git('branch','--show-current')=='pf-arty-split-1'
before=git('rev-parse','HEAD');assert before=='4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2'
snapshot=json.loads((r/'source-before-qualification.json').read_text())
docs=json.loads((r/'final-service-documentation.json').read_text())
assert docs['status']=='PASS' and len(docs['results'])==11
qualified=json.loads((r/'final-census/qualification.json').read_text())
assert qualified['status']=='PASS' and qualified['groups']==145
assert docs['qualification_sha256']==hashlib.sha256((r/'final-census/qualification.json').read_bytes()).hexdigest()
doc_changes={row['file']:row for row in docs['changes']}
rows=[]
for row in snapshot['files']:
    name=row['file'];data=(root/name).read_bytes();sha=hashlib.sha256(data).hexdigest()
    if name in doc_changes:
        assert row['sha256']==doc_changes[name]['before_sha256'],name
        assert sha==doc_changes[name]['after_sha256'],name
    else:assert sha==row['sha256'],name
    rows.append(dict(file=name,bytes=len(data),sha256=sha))
expected={row['file'] for row in rows}
actual=set(git('diff','--name-only','HEAD').splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines())
assert actual==expected,(actual-expected,expected-actual)
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'));import build
assert build.tree_digest([root/p for p in build.FIRMWARE_TREES])==docs['firmware_tree']
old=r.parent/'old-row-identity.json'
(r/'old-row-before-final.json').write_bytes(old.read_bytes())
subprocess.run([sys.executable,'-B',str(r.parent/'check-old-rows.py')],cwd=root,check=True,timeout=120)
(r/'old-row-final.json').write_bytes(old.read_bytes())
subprocess.run(['git','diff','--check'],cwd=root,check=True,timeout=120)
subprocess.run(['git','add','--',*sorted(expected)],cwd=root,check=True,timeout=120)
subprocess.run(['git','diff','--cached','--check'],cwd=root,check=True,timeout=120)
assert set(git('diff','--cached','--name-only').splitlines())==expected
subprocess.run(['git','commit','-m','Add qualified 80 MHz Arty split image configuration'],cwd=root,check=True,timeout=1200)
head=git('rev-parse','HEAD');assert head!=before
assert not git('status','--porcelain')
patch=subprocess.check_output(['git','show','--format=fuller','--binary',head],cwd=root)
(r/'qualified-source.patch').write_bytes(patch)
record=dict(status='PASS',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    branch='pf-arty-split-1',base='854bd7236792ce1adbd10c43b13a6a5002ad3bb6',previous_head=before,
    head=head,files=rows,firmware_tree=docs['firmware_tree'],qualification_sha256=docs['qualification_sha256'],
    patch_sha256=hashlib.sha256(patch).hexdigest(),pushed=False)
(r/'qualified-source.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='files'}))
