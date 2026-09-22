from pathlib import Path
import random, subprocess, tempfile, json, time
rng=random.Random(4232026)
out=Path(__file__).parent
started=time.monotonic();tested=0;hits=[]
with tempfile.TemporaryDirectory(prefix='423-retention-') as td:
 paths=[Path(td)/x for x in ['tip','base','branch']]
 for n in range(6000):
  base=[rng.choice('abc') for _ in range(rng.randrange(5,12))]
  i,j=rng.sample(range(len(base)),2)
  branch=base.copy()
  branch[i]=rng.choice([x for x in 'abcX' if x!=base[i]])
  branch[j]=rng.choice([x for x in 'abcY' if x!=base[j]])
  tip=branch.copy();tip[i]=base[i]
  suffix=[rng.choice('abcXY') for _ in range(rng.randrange(1,6))]
  tip+=suffix
  data=[('\n'.join(x)+'\n').encode() for x in [tip,base,branch]]
  for path,value in zip(paths,data):path.write_bytes(value)
  r=subprocess.run(['git','merge-file','-p','-q',*[str(x) for x in paths]],capture_output=True)
  tested+=1
  if r.returncode==0 and r.stdout==data[0]:
   hit={'case':n,'base':base,'branch':branch,'tip':tip,'changed_positions':[i,j],'reverted_position':i,'suffix':suffix,'exit':r.returncode,'output':r.stdout.decode()}
   hits.append(hit)
   if len(hits)>=3:break
record={'seed':4232026,'tested':tested,'seconds':time.monotonic()-started,'hits':hits,'meaning':'Bounded design probe of raw no-op merge; no production verdict or fixture expectation changed'}
(out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
