#!/usr/bin/env python3
import argparse,fnmatch,hashlib,json,pathlib,re,xml.etree.ElementTree as ET
ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();p=a.packet.resolve();src=a.source.resolve();public=p/'scratch/public-author-r3';hosted=p/'scratch/hosted/quality-evidence';plants=json.loads((src/'tests/mutations.json').read_text())
report={}
snapshot=json.loads((public/'source-snapshot.json').read_text());bad=[e['file'] for e in snapshot if hashlib.sha256((src/e['file']).read_bytes()).hexdigest()!=e['sha256'] or (src/e['file']).stat().st_size!=e['size']];assert not bad;report['author_source_snapshot']={'files':len(snapshot),'mismatches':bad}
for name,d in [('author',public/'validation'),('hosted',hosted)]:
 gates=json.loads((d/'gates.json').read_text());assert len(gates)==28 and all(r['rc']==0 for r in gates);report[name+'_gates']={'count':len(gates),'nonzero':[]}

def parse(files):
 cases={};failures={};counts=0
 for f in files:
  root=ET.parse(f).getroot();cs=root.findall('.//testcase');assert int(root.get('tests'))==len(cs) and cs
  for c in cs:
   name=c.get('classname')+'.'+c.get('name');assert c.get('status')=='run' and c.get('result')=='completed' and c.find('skipped') is None
   cases[f.name+'::'+name]=True;counts+=1
   fs=c.findall('failure')
   if fs:failures[name]=failures.get(name,'')+'\n'+'\n'.join(x.get('message','')+' '+(x.text or '') for x in fs)
 return cases,failures,counts

def check_kills(m,failures):
 for k in m['kills']:
  matches=[v for name,v in failures.items() if (name.startswith(k['test']) if k['test'].endswith('/') else fnmatch.fnmatchcase(name,k['test']))]
  assert matches,(m['name'],k['test'])
  assert any(k['needle'] in chunk for msg in matches for chunk in re.findall(r'TSN_MESSAGE_BEGIN_[0-9a-f]+\n(.*?)\nTSN_MESSAGE_END_[0-9a-f]+',msg,re.S)),(m['name'],k['needle'])
rows=json.loads((hosted/'mutations/results.json').read_text());assert len(rows)==len(plants)==367
for m,r in zip(plants,rows):
 assert m['name']==r['name'] and r['status']=='CAUGHT' and r['rc']!=0
 _,failures,_=parse(sorted((hosted/'mutations'/m['name']).glob('*.xml')));check_kills(m,failures)
report['hosted_campaign']={'plants':len(rows),'named_needles':sum(len(m['kills']) for m in plants),'all_regraded':True,'escapes':0,'errors':0}
local=p/'scratch/validation-sdk/mutations'
if (local/'results.json').exists():
 rows=json.loads((local/'results.json').read_text());assert len(rows)==len(plants)
 for m,r in zip(plants,rows):
  assert m['name']==r['name'] and r['status']=='CAUGHT' and r['rc']!=0
  _,failures,_=parse(sorted((local/m['name']).glob('*.xml')));check_kills(m,failures)
 report['independent_campaign']={'plants':len(rows),'named_needles':sum(len(m['kills']) for m in plants),'all_regraded':True,'escapes':0,'errors':0}
author_missing=[];graded=0
for m in plants:
 files=list((public/'validation/mutations'/m['name']).glob('*.xml'))
 if not files:author_missing.append(m['name']);continue
 _,failures,_=parse(files);check_kills(m,failures);graded+=1
report['author_campaign']={'named_plants_regraded':graded,'omitted_large_xml':author_missing,'summary_count':len(json.loads((public/'mutation-summary.json').read_text()))}
rows=json.loads((public/'complete-suite/results.json').read_text());closures=[]
for r in rows:
 d=public/'complete-suite'/r['plant'];full,ff,fc=parse(sorted((d/'full/xml').glob('*.xml')));removed,rf,rc=parse(sorted((d/'removed/xml').glob('*.xml')))
 assert fc==420 and rc==419 and len(full)-len(removed)==1 and set(ff)=={r['killer']} and not rf
 assert r['killer_needle'] in ff[r['killer']]
 closures.append({'plant':r['plant'],'full_instances':fc,'removed_instances':rc,'escapes':True})
report['author_complete_suites']=closures
identities=[]
for role in ['R630-1','R630-2']:
 for f in (p/'scripts'/role).glob('*.py'):
  b=f.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();path='review-evidence/tsn24-r1/reviews/'+role+'/scripts/'+f.name
  expect=next(e['sha'] for e in json.loads((p/'scratch/evidence-tree-correct.json').read_text())['tree'] if e['path']==path);assert blob==expect
  identities.append(dict(file=str(f.relative_to(p)),blob=blob,sha256=hashlib.sha256(b).hexdigest(),unchanged=True))
report['unchanged_scripts']=identities
(p/'receipts/public-evidence-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
