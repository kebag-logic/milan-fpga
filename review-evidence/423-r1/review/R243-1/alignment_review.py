import concurrent.futures, hashlib, itertools, json, os, subprocess, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
cases=[]
# A bounded independent population: all binary five-line originals, all pairs,
# replacement/deletion/insertion edits, either one-edit reversal, a far suffix.
for bits in itertools.product((b'a\n',b'b\n'),repeat=5):
 original=b''.join(bits)+b'end\n'
 for i,j in itertools.combinations(range(5),2):
  for mode in ('replace','delete','insert'):
   def edit(line,pos,locations):
    if pos not in locations:return line
    return b'NEW\n' if mode=='replace' else b'' if mode=='delete' else line+b'NEW\n'
   branch=b''.join(edit(line,k,(i,j)) for k,line in enumerate(bits))+b'end\n'
   for retained in (i,j):
    tip=b''.join(edit(line,k,(retained,)) for k,line in enumerate(bits))+b'end\nLATER\n'
    cases.append(dict(original=original,branch=branch,tip=tip,positions=[i,j],retained=retained,mode=mode))

def job(pair):
 index,c=pair
 with tempfile.TemporaryDirectory(prefix='r243-align-',dir=root) as directory:
  paths=[Path(directory)/name for name in ('tip','base','branch')]
  for p,data in zip(paths,(c['tip'],c['original'],c['branch'])):p.write_bytes(data)
  r=subprocess.run(['rtk','proxy','git','--no-replace-objects','-c','merge.conflictStyle=merge','merge-file','-p','-q',*map(str,paths)],capture_output=True,
    env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull))
  return dict(index=index,rc=r.returncode,equals_tip=r.stdout==c['tip'],stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),**{k:v.decode() if isinstance(v,bytes) else v for k,v in c.items()})
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(job,enumerate(cases)))
false=[row for row in rows if row['rc']==0 and row['equals_tip']]
(root/'alignment-review-data.json').write_text(json.dumps(dict(count=len(rows),counterexamples=false,rows=rows),indent=2)+'\n')
print('bounded alignment partial-revert probes:',len(rows),'no-op acceptances:',len(false));print(json.dumps(false[:5],indent=2))
raise SystemExit(bool(false))
