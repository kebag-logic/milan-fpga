#!/usr/bin/env python3
"""Prepare three public parent sources and apply only the immutable handover patch."""
import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT/'scratch/parent'
REPO='repos/kebag-logic/milan-fpga/'
commit=json.loads(subprocess.check_output(['gh','api',REPO+'commits/e76a755a']))['sha']
records=[]
for rel in ['hdl/ieee1722/aaf/KL_aaf_packetizer.sv','hdl/milan/KL_pp_shadow.sv','hdl/milan/milan_datapath.sv']:
    data=subprocess.check_output(['gh','api',REPO+'contents/'+rel+'?ref='+commit,'-H','Accept: application/vnd.github.raw+json'])
    path=ROOT/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    records.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest(),git_blob=subprocess.check_output(['git','hash-object','--stdin'],input=data,text=False).decode().strip()))
patch=OUT/'scratch/public/author/parent-src-stream-id-wiring.patch'
subprocess.run(['git','apply','--check',str(patch)],cwd=ROOT,check=True)
subprocess.run(['git','apply',str(patch)],cwd=ROOT,check=True)
for r in records:r['patched_sha256']=hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()
(OUT/'parent-source-verification.json').write_text(json.dumps(dict(base=commit,patch_sha256=hashlib.sha256(patch.read_bytes()).hexdigest(),files=records),indent=2)+'\n')
print('Parent patch applies cleanly:',commit)
