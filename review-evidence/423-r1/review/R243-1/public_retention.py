import hashlib,json,os,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
source=Path('$VALIDATION_STORAGE/reviews/r243-423-r1/gptp-processor');os.chdir(source)
history=json.loads((root/'public-history-data.json').read_bytes());rows=[]
def git(*args):
 p=subprocess.run(['rtk','proxy','git','--no-replace-objects',*args],capture_output=True,check=True);return p.stdout
for h in history:
 if h['kind']!='real-tip':continue
 for e in h['entries']:
  entries=[None if not e[k] else tuple(e[k].split('\t')[0].split()) for k in ('ancestor','tip','branch')]
  blobs=[b'' if ent is None else git('cat-file','blob',ent[2]) for ent in entries]
  row=dict(tip=h['tip'],path=e['path'],entries=entries,blob_sha256=[hashlib.sha256(x).hexdigest() for x in blobs],exact_identity=entries[1]==entries[2])
  if not row['exact_identity']:
   with tempfile.TemporaryDirectory(prefix='r243-public-merge-',dir=root) as folder:
    paths=[Path(folder)/n for n in ('tip','base','branch')]
    for path,data in zip(paths,(blobs[1],blobs[0],blobs[2])):path.write_bytes(data)
    r=subprocess.run(['rtk','proxy','git','--no-replace-objects','-c','merge.conflictStyle=merge','merge-file','-p','-q',*map(str,paths)],capture_output=True)
    row.update(raw_merge_exit=r.returncode,output_equals_tip=r.stdout==blobs[1],output_sha256=hashlib.sha256(r.stdout).hexdigest())
    output=root/'public-raw-merges'/h['tip']/e['path'];output.parent.mkdir(parents=True,exist_ok=True);output.with_suffix(output.suffix+'.merged').write_bytes(r.stdout)
  rows.append(row)
for tip in sorted({r['tip'] for r in rows}):
 unresolved=[r['path'] for r in rows if r['tip']==tip and not r['exact_identity'] and (r['raw_merge_exit']!=0 or not r['output_equals_tip'])]
 assert unresolved==['tb/tsngen/mutants.py','tb/verilator/gaskets/mutants.py']
(root/'public-retention-data.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
