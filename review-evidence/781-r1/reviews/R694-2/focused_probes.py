import collections, hashlib, json, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parent
root=Path(sys.argv[1]).resolve()
clone=P/'scratch/probe-clone'
head='41f4a53cc0b12f143fa3e61a5339a11e79806ce9'
old='8a4fa2f971427b1deb1f20a4b456a8a4d94bf008'
def run(args,cwd):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
 assert r.returncode==0,(args,r.stdout,r.stderr)
 return r.stdout
clone.parent.mkdir(parents=True,exist_ok=True)
if not clone.exists():
 run(['git','clone','--quiet','--shared','--no-checkout',str(root),str(clone)],root)
rows=[]; lists={}
for ref in (old,head):
 run(['git','checkout','--quiet','--detach',ref],clone)
 got={}
 for name,args in [('serial',[]),('pieces',['--ci-pieces'])]+[(f'shard-{k}',['--ci-pieces','--shard',f'{k}/17']) for k in range(17)]:
  value=run(['bash','scripts/run_all_suites.sh',*args,'--list'],clone)
  got[name]=value
  rows.append({'head':ref,'name':name,'sha256':hashlib.sha256(value.encode()).hexdigest(),'lines':len(value.splitlines())})
 lists[ref]=got
assert lists[old]==lists[head]
owned=[x for k in range(17) for x in lists[head][f'shard-{k}'].splitlines()]
assert collections.Counter(owned)==collections.Counter(lists[head]['pieces'].splitlines())
assert len(set(owned))==81
assert len(lists[head]['serial'].splitlines())==64
assert 'media_phase' in lists[head]['shard-4'].splitlines()
assert lists[head]['shard-16'].splitlines()==['milan_dp_mclk__0']
(P/'ownership-verification.json').write_text(json.dumps({'byte_identical':True,'exactly_once':True,'lists':rows},indent=2)+'\n')
print('Ownership: 64 suites, 81 units; all 19 listings byte-identical; every unit exactly once')
script=clone/'scripts/suite_shards.py'; baseline=script.read_text()
probes=[('measured-582',baseline.replace('"media_phase": 1400,','"media_phase": 582,'),0),('disabled-provisional-guard',baseline.replace('elif seconds[suite] != expected:', 'elif False:'),1)]
for name,source,expected in probes:
 try:
  script.write_text(source)
  r=subprocess.run(['python3','scripts/suite_shards.py','--selftest'],cwd=clone,capture_output=True,text=True)
  (P/(name+'.log')).write_text(r.stdout+r.stderr+'\nreturncode='+str(r.returncode)+'\n')
  assert r.returncode==expected,(name,r.returncode)
  assert 'skip head arms' not in r.stdout
  print(name,'rc',r.returncode,'expected',expected)
 finally: script.write_text(baseline)
assert run(['git','diff','--exit-code'],clone)==''
