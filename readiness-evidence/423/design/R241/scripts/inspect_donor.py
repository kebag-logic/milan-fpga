from pathlib import Path
import subprocess,json,hashlib,os
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT/'fixtures/donor.git'
TRUSTED=Path('$VALIDATION_STORAGE/reviews/r241-423-design/scripts/check_merge_containment.py')
def git(*args): return subprocess.check_output(['rtk','proxy','git','--no-replace-objects','-C',str(REPO),*args])
branch='3db86812096830fada2f5f276fa5f4d9f37d1d14';original='f0f1c055ee5226f08e656c27cb1bf4c355be11ae';live=git('rev-parse','refs/heads/main').decode().strip()
record={'branch':branch,'original':original,'live':live,'pairs':[],'topology':[],'cases':[]}
for old,new in [('9790ac736e6d10301ad814ffdf73dbe37b59768b','20927af74752620b2ad0f973e8be3203994b5547'),(branch,'5602e70bb4cf70c2e0e39e846e26925e27659e32')]:
 patches=[]
 for oid in (old,new):
  patch=git('show','--format=','--no-ext-diff','--no-textconv','--ignore-submodules=none','--binary','--full-index','--no-renames',oid)
  (ROOT/'logs'/f'{oid}.patch').write_bytes(patch);patches.append(patch)
 names=git('diff-tree','--no-commit-id','--name-only','--no-renames','-r','-z',old).split(b'\0');names=[n.decode() for n in names if n]
 q=subprocess.run(['rtk','proxy','git','--no-replace-objects','-C',str(REPO),'--literal-pathspecs','diff','--no-ext-diff','--no-textconv','--ignore-submodules=none','--quiet',old,new,'--',*names])
 record['pairs'].append({'old':old,'new':new,'raw_patch_sha256':hashlib.sha256(patches[0]).hexdigest(),'patch_equal':patches[0]==patches[1],'postimage_diff_exit':q.returncode,'paths':names,'whole_tree_equal':git('rev-parse',old+'^{tree}')==git('rev-parse',new+'^{tree}')})
for oid in [branch,'9790ac736e6d10301ad814ffdf73dbe37b59768b','f27b45500cb02a5277b5cb32cef408658c1f914e','377b8c428b226a796adde099fe07152151fd6c5d','676d2f6be46b2775b8a008800d394c9855a5efc3',original,live]:
 record['topology'].append({'oid':oid,'parents':git('show','-s','--format=%P',oid).decode().split(),'tree':git('rev-parse',oid+'^{tree}').decode().strip()})
for label,target in [('original',original),('live',live)]:
 for name,cmd in [('baseline',['rtk','proxy','python3','-B',str(TRUSTED),'--no-fetch','--base',target,branch]),('historical',['rtk','proxy','python3','-B',str(ROOT/'scripts/predicate.py'),str(REPO),branch,target,'--historical']),('retention',['rtk','proxy','python3','-B',str(ROOT/'scripts/predicate.py'),str(REPO),branch,target])]:
  p=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True)
  (ROOT/'logs'/f'donor-{label}-{name}.log').write_text('COMMAND '+repr(cmd)+'\nEXIT '+str(p.returncode)+'\n'+p.stdout+p.stderr)
  record['cases'].append({'target_label':label,'target':target,'predicate':name,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 paths=sorted(set(p for pair in record['pairs'] for p in pair['paths']))
 (ROOT/'logs'/f'donor-{label}-touched-paths.diff').write_bytes(git('--literal-pathspecs','diff','--no-ext-diff','--no-textconv','--ignore-submodules=none',branch,target,'--',*paths))
record['source_unique']=git('rev-list','--parents',live+'..'+branch).decode()
(ROOT/'logs/donor-evidence.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
