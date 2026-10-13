#!/usr/bin/env python3
"""Join four bounded offline mutation/control children; edit scratch copies only."""
import ast,concurrent.futures,json,shutil,subprocess,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent.parent;repo=Path(sys.argv[1]).resolve();base=p/'scratch/pristine'
source=(base/'scripts/act_ci.py').read_text()
controls=json.loads((p/'scripts/signal-controls.json').read_text())
# Closing defects are independently planted in the exact production function.
boundary=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='execute_act_boundary')
lines=source.splitlines(keepends=True);prefix=''.join(lines[:boundary.lineno-1]);body=''.join(lines[boundary.lineno-1:boundary.end_lineno]);suffix=''.join(lines[boundary.end_lineno:])
closing=[
 ('C01','primary never captured','            primary = exc','            primary = None'),
 ('C02','later signal replaces primary','        if primary is None or primary is delivered:','        if True:'),
 ('C03','first signal swallowed','        if primary is None or primary is delivered:\n            raise','        if primary is None or primary is delivered:\n            return 0'),
 ('C04','diagnostic prefix variation (retains required meaning)','f"act-ci: act boundary closing was interrupted','f"act-ci: omitted closing signal'),
]
cases=[]
for ident,mode,old,new in controls:
 assert source.count(old)==1,(ident,source.count(old));cases.append((ident,mode,source.replace(old,new)))
for ident,why,old,new in closing:
 assert body.count(old)==1,(ident,body.count(old));cases.append((ident,'closing',prefix+body.replace(old,new)+suffix))
# Genuine preceding production boundary, retaining this head's new standing controls.
previous=subprocess.check_output(['git','show','ede700b0:scripts/act_ci.py'],cwd=repo,text=True)
node=next(n for n in ast.parse(previous).body if isinstance(n,ast.FunctionDef) and n.name=='execute_act_boundary')
oldbody=''.join(previous.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
cases.append(('C05','closing',prefix+oldbody+suffix))
cases.append(('C00','closing',source))
oldprint=next(n for n in ast.walk(boundary) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='print')
mutlines=source.splitlines(keepends=True)
mutlines[oldprint.lineno-1:oldprint.end_lineno]=[' ' * oldprint.col_offset + 'pass\n']
cases.append(('C06','closing',''.join(mutlines)))
if '--only' in sys.argv:
 selected=set(sys.argv[sys.argv.index('--only')+1].split(','));cases=[c for c in cases if c[0] in selected]
def run(case):
 ident,mode,contents=case;tree=p/'scratch/signal-controls'/ident
 tree.mkdir(parents=True,exist_ok=True);(tree/'scripts').mkdir(exist_ok=True)
 (tree/'scripts/act_ci.py').write_text(contents)
 cmd=['sh',str(p/'scripts/reviewer_sandbox.sh'),str(tree),str(p),'python3','-I',
 '/packet/scripts/run_closing_arms.py' if mode=='closing' else '/packet/scripts/run_masked_arms.py','/work/scripts/act_ci.py']
 if mode!='closing':cmd.append(mode)
 start=time.monotonic()
 with (p/'receipts'/f'signal-{ident}.log').open('w') as f:
  try:rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=120).returncode
  except subprocess.TimeoutExpired:rc=124
 (p/'receipts'/f'signal-{ident}.rc').write_text(str(rc)+'\n')
 row=dict(id=ident,mode=mode,rc=rc,seconds=round(time.monotonic()-start,3));print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(run,cases))
(p/'receipts'/('signal-controls-extra.json' if '--only' in sys.argv else 'signal-controls.json')).write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(int(any(r['rc']!=0 if r['id'] in ('C00','C04') else r['rc']==0 or r['rc']==124 for r in rows)))
