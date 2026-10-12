import copy,json,shutil,subprocess,sys,tempfile
from pathlib import Path
root=Path('$LANES/pp73-command-model')
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
sys.path.insert(0,str(root/'scripts'))
from aecp_gate.inputs import load
from aecp_gate.gate import check
from aecp_gate.selftest import copy_inputs
base=load(root)
positive=[]
for name,explicit in [('TIZ4NS',False),('EAVL',True)]:
 inp=copy.deepcopy(base)
 inp.table['echo_entries'].append(name)
 if explicit:inp.table['shared_entries'][name]='declared shared program'
 found=check(inp)
 assert not found,found
 positive.append({'program':name,'explicit_shared':explicit,'findings':found})
(r/'membership-positive.json').write_text(json.dumps(positive,indent=2)+'\n')
changes=[
 ('membership','table.py','for e in echoes if e not in shared and (e in owners or uses[e] < 2)','for e in echoes if False','echo_entries names no shared program'),
 ('rom-success','rom.py','(s != 0 and e in echo_shared)','(e in echo_shared)','a shared echo cannot exempt ROM SUCCESS'),
 ('record-success','record.py','(int(s) != 0 and pn in echo_shared)','(pn in echo_shared)','a shared echo cannot exempt observed SUCCESS'),
]
records=[]
for name,filename,old,new,expected in changes:
 with tempfile.TemporaryDirectory(dir=r/'tmp',prefix='disabled-check-') as tmp:
  d=Path(tmp);copy_inputs(root,d)
  shutil.copytree(root/'scripts',d/'scripts',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
  p=d/'scripts/aecp_gate'/filename;s=p.read_text();assert s.count(old)==1
  p.write_text(s.replace(old,new))
  log=r/(name+'-disabled.log')
  with log.open('w') as stream:
   rc=subprocess.run([sys.executable,'-B','scripts/check_aecp_commands.py','--selftest'],cwd=d,stdout=stream,stderr=subprocess.STDOUT,check=False).returncode
  assert rc==1 and expected in log.read_text(),(name,rc)
  records.append({'check':name,'selftest_rc':rc,'named_failure':expected})
(r/'disabled-checks.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({'positive':positive,'disabled':records},indent=2))
