"""Build deterministic offline Git objects and execute the unchanged checker
and both SCRATCH predicates. No source checkout writes, no network, no builds.
"""
from pathlib import Path
import os,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT/'fixtures/counterexamples.git'
TRUSTED=Path('$VALIDATION_STORAGE/reviews/r241-423-design/scripts/check_merge_containment.py')
ENV={**os.environ,'GIT_AUTHOR_NAME':'R241 offline fixture','GIT_AUTHOR_EMAIL':'fixture@example.invalid','GIT_COMMITTER_NAME':'R241 offline fixture','GIT_COMMITTER_EMAIL':'fixture@example.invalid','GIT_AUTHOR_DATE':'2026-09-22T00:00:00+00:00','GIT_COMMITTER_DATE':'2026-09-22T00:00:00+00:00','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','PYTHONDONTWRITEBYTECODE':'1'}
commands=[]
def git(*args,data=None):
 p=subprocess.run(['rtk','proxy','git','--no-replace-objects','-C',str(REPO),*args],input=data,capture_output=True,env=ENV)
 commands.append({'argv':list(args),'exit':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')})
 p.check_returncode();return p.stdout.decode().strip()
if not REPO.exists():
 p=subprocess.run(['rtk','proxy','git','init','--bare','--quiet',str(REPO)],capture_output=True,env=ENV);p.check_returncode()
objects={};trees={}
def commit(name,files,parents=()):
 entries=[]
 for path,item in sorted(files.items()):
  mode,content=item if isinstance(item,tuple) else ('100644',item)
  oid=git('hash-object','-w','--stdin',data=content)
  entries.append(mode.encode()+b' blob '+oid.encode()+b'\t'+path.encode()+b'\0')
 tree=git('mktree','-z',data=b''.join(entries))
 args=['commit-tree',tree]
 for parent in parents: args+=['-p',parent]
 oid=git(*args,data=(name+'\n').encode());git('update-ref','refs/heads/'+name,oid)
 objects[name]=oid;trees[name]=files.copy();return oid
seed={'feature.txt':b'before\n','other.txt':b'before\n','third.txt':b'before\n'}
O=commit('origin',seed)
a={**seed,'feature.txt':b'after\n'};A=commit('source-A',a,[O]);M=commit('source-M',a,[O,A])
c={**a,'other.txt':b'after\n'};C=commit('source-C',c,[M])
AP=commit('replay-A',a,[O]);CP=commit('replay-C',c,[AP])
cases=[]
def case(name,source,target,baseline,historical,retention,note): cases.append({'case':name,'source':source,'target':target,'expected':{'baseline':baseline,'historical':historical,'retention':retention},'note':note})
case('exact-replay',C,CP,0,0,0,'Exact endpoint bytes, including mode/kind, are present.')
T=commit('unrelated-extension',{**c,'new.txt':b'later\n'},[CP]);case('unrelated-extension',C,T,0,0,0,'A later extension outside all source-touched paths is permitted.')
T=commit('published-same-path-extension',{**c,'feature.txt':b'after\nlater extension\n'},[CP]);case('published-same-path-extension',C,T,1,0,1,'Legitimate append retained the original bytes, but strict whole-entry equality is unresolved.')
T=commit('exact-revert-A',{**c,'feature.txt':seed['feature.txt']},[CP]);case('exact-revert-A',C,T,1,0,1,'A exact reverse tree delta after both replays, not just a revert message.')
T=commit('revert-plus-unrelated-extension',{**c,'feature.txt':seed['feature.txt'],'new.txt':b'later\n'},[CP]);case('revert-plus-unrelated-extension',C,T,1,0,1,'Aggregate later delta is not an exact inverse; lost work still refuses.')
T=commit('exact-revert-C',a,[CP]);case('exact-revert-C',C,T,1,0,1,'The final linear change can also be reverted.')
T=commit('missing-A',{**seed,'other.txt':b'after\n'},[O]);case('missing-linear-A',C,T,1,1,1,'The second linear patch alone cannot replace the missing first.')
case('missing-linear-C',C,AP,1,1,1,'The first linear patch alone cannot replace the missing second.')
T1=commit('whitespace-replay-A',{**seed,'feature.txt':b'after \n'},[O]);T=commit('whitespace-replay-C',{**c,'feature.txt':b'after \n'},[T1]);case('whitespace-different-replay',C,T,1,1,1,'Whitespace differs at replay time; exact patch/postimage proof fails.')
T=commit('later-whitespace-change',{**c,'feature.txt':b'after \n'},[CP]);case('later-whitespace-change',C,T,1,0,1,'Exact historical replay does not certify whitespace-different current bytes.')
T=commit('later-mode-change',{**c,'feature.txt':('100755',b'after\n')},[CP]);case('later-mode-change',C,T,1,0,1,'Blob bytes remain but executable mode changes.')
T=commit('later-kind-change',{**c,'feature.txt':('120000',b'after\n')},[CP]);case('later-kind-change',C,T,1,0,1,'Same blob bytes as a symlink cannot equal a regular file.')
MR=commit('merge-with-resolution',{**a,'resolution.txt':b'merge-only work\n'},[O,A]);CR=commit('tip-with-resolution',{**c,'resolution.txt':b'merge-only work\n'},[MR]);case('missing-merge-resolution',CR,CP,1,1,1,'Same parent shape but merge tree differs from incoming parent.')
OP=commit('unrelated-origin',seed);AU=commit('unrelated-incoming',a,[OP]);MU=commit('merge-unrelated',a,[O,AU]);CU=commit('tip-unrelated',c,[MU]);case('unrelated-parents-same-tree',CU,CP,0,1,1,'Existing exact endpoint proof passes independently; scratch topology rule refuses.')
UE=commit('unrelated-later-extension',{**c,'feature.txt':b'after\nlater\n'},[CP]);case('unrelated-parents-with-extension',CU,UE,1,1,1,'Endpoint differs: neither existing nor bounded topology proof admits unrelated parents.')
EX=commit('extra-incoming-parent',{**seed,'extra.txt':b'extra\n'},[O]);MO=commit('octopus',a,[O,A,EX]);CO=commit('tip-octopus',c,[MO]);case('octopus-same-incoming-tree',CO,CP,0,1,1,'Existing exact endpoint proof passes independently; scratch topology rule refuses.')
OE=commit('octopus-later-extension',{**c,'feature.txt':b'after\nlater\n'},[CP]);case('octopus-with-extension',CO,OE,1,1,1,'Endpoint differs: no permission to skip the octopus in a new proof.')
MM=commit('second-merge',c,[M,C]);CC=commit('tip-two-merges',{**c,'third.txt':b'after\n'},[MM]);TCP=commit('replay-two-merges-tail',{**c,'third.txt':b'after\n'},[CP]);TE=commit('two-merges-later-extension',{**trees['replay-two-merges-tail'],'feature.txt':b'after\nnext\n'},[TCP]);case('multiple-source-merges',CC,TE,1,1,1,'Multiple source merges are deliberately outside the bounded rule.')
L=commit('incoming-intermediate',{**seed,'third.txt':b'after\n'},[O]);AL=commit('incoming-not-immediate',{**a,'third.txt':b'after\n'},[L]);ML=commit('merge-long-incoming',{**a,'third.txt':b'after\n'},[O,AL]);CL=commit('tip-long-incoming',{**c,'third.txt':b'after\n'},[ML]);case('omitted-linear-incoming-work',CL,CP,1,1,1,'Ancestor-only first-parent condition must not silently omit intermediate work.')
DROP=commit('target-discarding-merge',{**c,'feature.txt':seed['feature.txt']},[CP,EX]);case('target-merge-discards-work',C,DROP,1,0,1,'Replay in a second-parent/history path is insufficient at the target tip.')
TM=commit('target-retaining-merge',{**c,'extra.txt':b'extra\n'},[CP,EX]);case('target-merge-retains-work',C,TM,0,0,0,'Target integration topology is allowed when current protected entries agree.')
# Existing linear and ancestry semantics are measured, not changed.
linear=commit('pure-linear-C',c,[A]);case('existing-linear-policy-revert',linear,objects['exact-revert-A'],0,1,1,'Existing linear historical fallback passes; the scratch rule refuses as out of scope.')
anc=commit('ancestry-revert-A',{**c,'feature.txt':seed['feature.txt']},[C]);case('existing-ancestry-policy-revert',C,anc,0,1,1,'Existing ancestry proof passes; no global retention-policy change is proposed.')
# An append-only proposal also fails: undoing a tail deletion appends the deleted bytes.
ds={**seed,'feature.txt':b'keep\ndeleted tail\n'};DO=commit('delete-origin',ds);da={**ds,'feature.txt':b'keep\n'};DA=commit('delete-A',da,[DO]);DM=commit('delete-M',da,[DO,DA]);dc={**da,'other.txt':b'after\n'};DC=commit('delete-C',dc,[DM]);DAP=commit('delete-replay-A',da,[DO]);DCP=commit('delete-replay-C',dc,[DAP]);DT=commit('append-is-exact-revert',{**dc,'feature.txt':ds['feature.txt']},[DCP]);case('append-is-deletion-revert',DC,DT,1,0,1,'Current file starts with the full branch postimage, yet exactly reverts the source deletion.')
# Explicit partial revert retaining the other change in a source commit.
pa={**seed,'feature.txt':b'after\n','third.txt':b'after\n'};PA=commit('partial-A',pa,[O]);PM=commit('partial-M',pa,[O,PA]);pc={**pa,'other.txt':b'after\n'};PC=commit('partial-C',pc,[PM]);PAP=commit('partial-replay-A',pa,[O]);PCP=commit('partial-replay-C',pc,[PAP]);PT=commit('partial-revert',{**pc,'feature.txt':b'before\n'},[PCP]);case('partial-revert',PC,PT,1,0,1,'One path of a multi-path source patch is undone; no whole-commit inverse is required.')
failures=[]
for row in cases:
 row['actual']={}
 for name in ('baseline','historical','retention'):
  if name=='baseline': cmd=['rtk','proxy','python3','-B',str(TRUSTED),'--no-fetch','--base',row['target'],row['source']]
  else:
   cmd=['rtk','proxy','python3','-B',str(ROOT/'scripts/predicate.py'),str(REPO),row['source'],row['target']]
   if name=='historical':cmd+=['--historical']
  p=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True,env=ENV)
  (ROOT/'logs'/f"fixture-{row['case']}-{name}.log").write_text('COMMAND '+repr(cmd)+'\nEXIT '+str(p.returncode)+'\n'+p.stdout+p.stderr)
  row['actual'][name]=p.returncode
  if p.returncode!=row['expected'][name]:failures.append((row['case'],name,row['expected'][name],p.returncode))
 print(row['case'],row['actual'])
(ROOT/'logs/fixture-results.json').write_text(json.dumps({'objects':objects,'cases':cases,'failures':failures},indent=2)+'\n')
(ROOT/'logs/fixture-construction.json').write_text(json.dumps(commands,indent=2)+'\n')
assert not failures,failures
print(f'{len(cases)} cases x 3 actual process exits agree with expectations')
