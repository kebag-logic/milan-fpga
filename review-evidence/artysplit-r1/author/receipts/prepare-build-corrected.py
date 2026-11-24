"""Prepare fresh qualification helpers without changing the running calibration."""
import ast,datetime,hashlib,json,shutil
from pathlib import Path
old=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined');new=old.parent/'build-corrected'
assert not new.exists();new.mkdir();(new/'work-tmp').mkdir()
names=(*json.loads((old/'preparation.json').read_text())['copied_helpers'],'run-pipeline.py')
for name in names:
 text=(old/name).read_text().replace(str(old),str(new))
 (new/name).write_text(text)
for name in ('identity-before','native-optimization'):
 (new/name).symlink_to((old/name).resolve(),target_is_directory=True)
shutil.copy2(old/'identity-compare.json',new/'identity-compare.json')
(new/'docs').mkdir();shutil.copy2(old/'docs/results.json',new/'docs/results.json')
path=new/'run-final-census.py';text=path.read_text()
before="first={('none','backlog-adp'),('none','backlog-owed'),\n       ('declaring-outputs','aecp-largest-notice'),('valid-destinations','srp-talker-held')}"
after="first={('none','srp'),('none','backlog-adp'),('none','backlog-owed'),\n       ('declaring-outputs','aecp-largest-notice'),('valid-destinations','srp-talker-held'),\n       ('answering-every-port','notice-every-3'),('answering-every-port','notice-burst-5')}"
assert text.count(before)==1;text=text.replace(before,after)
text=text.replace('# Complete the four scheduling/held-load cases before admitting long cases.',
                  '# Complete the build, held-load and maximum-pass cases before the long cases.')
assert text.count('list(pool.map(one,jobs[:4]))')==1
text=text.replace('list(pool.map(one,jobs[:4]))','list(pool.map(one,jobs[:len(first)]))')
text=text.replace('list(pool.map(one,jobs[4:]))','list(pool.map(one,jobs[len(first):]))')
text=text.replace("jobs.sort(key=lambda pair:","assert first <= {(v,g.name) for v,g in jobs}\njobs.sort(key=lambda pair:")
path.write_text(text)
# Only admission order changes. Native scripts, limits, and grading stay exact.
def functions(path):
 return {node.name:ast.dump(node,include_attributes=False) for node in ast.parse(path.read_text()).body
         if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
a,b=functions(old/path.name),functions(path)
assert a==b
for name in names:compile((new/name).read_text(),str(new/name),'exec')
record=dict(status='PREPARED; CALIBRATION STILL RUNNING; SOURCE UNCHANGED',
 time=datetime.datetime.now(datetime.timezone.utc).isoformat(),copied_helpers=list(names),
 old_evidence=str(old),new_evidence=str(new),
 changes='Seven initial sensitivity cases; unchanged full coverage, native functions, four-slot cap and owner/SHARE/ledger tests',
 helper_sha256={name:hashlib.sha256((new/name).read_bytes()).hexdigest() for name in names})
(new/'preparation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='helper_sha256'},indent=2))
