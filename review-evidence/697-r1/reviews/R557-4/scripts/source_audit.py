#!/usr/bin/env python3
"""Compare core tokens, planted programs and the exact Round 5 mutation mapping."""
import argparse,hashlib,io,json,pathlib,re,subprocess,tarfile
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve();p=a.packet.resolve();base=p/'scratch/base';base.mkdir(parents=True,exist_ok=True)
def git(*cmd):return subprocess.check_output(['git','-C',str(r),*cmd])
if not (base/'src/adp.c').exists():
 with tarfile.open(fileobj=io.BytesIO(git('archive','ae982af85ec97286bd35b39403926d8f0eaec81d'))) as t:t.extractall(base,filter='data')
pattern=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/|//[^\n]*|[a-zA-Z_]\w*|\d[\w.]*|[^\s]',re.S)
def tokens(text):return [m[0] for m in pattern.finditer(text) if not m[0].startswith(('//','/*'))]
rows=[]
for d in ['src','include']:
 for f in sorted((r/d).glob('*')):
  if f.suffix not in ['.c','.h']:continue
  old=(base/f.relative_to(r)).read_text();new=f.read_text();rows.append({'file':str(f.relative_to(r)),'tokens_equal':tokens(old)==tokens(new),'line_count_equal':len(old.splitlines())==len(new.splitlines())})
old={x['name']:x for x in json.loads((base/'tests/mutations.json').read_text())};new={x['name']:x for x in json.loads((r/'tests/mutations.json').read_text())};plantrows=[]
for name,x in old.items():
 y=new[name];before=(base/x['path']).read_text();after=(r/y['path']).read_text()
 if before.count(x['old'])!=1 or after.count(y['old'])!=1:raise RuntimeError('ambiguous mutation anchor '+name)
 before=before.replace(x['old'],x['new']);after=after.replace(y['old'],y['new']);plantrows.append({'name':name,'program_tokens_equal':tokens(before)==tokens(after)})
round4=json.loads(git('show','3c350014:tests/mutations.json'));round5=list(new.values());delta=[];changed_needles=0
for x,y in zip(round4,round5):
 x=json.loads(json.dumps(x));y=json.loads(json.dumps(y))
 for k,l in zip(x['kills'],y['kills']):
  if k['needle']!=l['needle']:changed_needles+=1
  k.pop('needle');l.pop('needle')
 if x!=y:delta.append(x['name'])
result={'core_files':rows,'planted_programs':plantrows,'round5_non_needle_changes':delta,'round5_changed_needles':changed_needles,'round5_killers':sum(len(x['kills']) for x in round5)}
(p/'receipts/source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('core equal',sum(x['tokens_equal'] for x in rows),'of',len(rows),'programs equal',sum(x['program_tokens_equal'] for x in plantrows),'of',len(plantrows),'round5 changed needles',changed_needles,'other table changes',delta)
raise SystemExit(not all(x['tokens_equal'] for x in rows) or not all(x['program_tokens_equal'] for x in plantrows) or bool(delta))
