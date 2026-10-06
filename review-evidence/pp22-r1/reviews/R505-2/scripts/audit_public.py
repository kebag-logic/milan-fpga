#!/usr/bin/env python3
"""Read pinned public receipts and replay the ordered adoption patches only."""
import argparse, base64, concurrent.futures, hashlib, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('packet',type=Path);a=p.parse_args()
parent='kebag-logic/milan-fpga'; evidence='2e889399824b70f9ed9a20c53d925e61a617a976'
base='28f9666feab2b2ba287643c63ed3a16b1e0bb863'
def api(path): return json.loads(subprocess.check_output(['gh','api',path]))
def fetch(path,ref):
    return base64.b64decode(api(f'repos/{parent}/contents/{path}?ref={ref}')['content'])
root=a.packet/'scratch/public-evidence';root.mkdir(parents=True,exist_ok=True)
manifest=api(f'repos/{parent}/contents/review-evidence/pp22-r1/MANIFEST.json?ref={evidence}')
raw=base64.b64decode(manifest['content']);(root/'MANIFEST.json').write_bytes(raw)
def get(row):
    data=fetch('review-evidence/pp22-r1/'+row['file'],evidence)
    assert hashlib.sha256(data).hexdigest()==row['published_sha256']
    f=root/row['file'];f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
    return dict(file=row['file'],sha256=row['published_sha256'])
with concurrent.futures.ThreadPoolExecutor(4) as ex: rows=list(ex.map(get,json.loads(raw)))
for name in ['KL_pp_originator','KL_pp_rx_validator','protocol_processor_top']:
    assert (root/f'author/base-{name}-stat.json').read_bytes()==(root/f'author/head-{name}-stat.json').read_bytes()
(a.packet/'receipts/public-evidence-verified.json').write_text(json.dumps(rows,indent=2)+'\n')
dest=a.packet/'scratch/adoption-replay';dest.mkdir(parents=True,exist_ok=True)
for path in ['scripts/xvlog.budget','tb/verilator/milan_dp/sim_nxn.cpp']:
    out=dest/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(fetch(path,base))
result=[]
for name in ['parent-adoption-148-6c22d3ca.patch','parent-adoption-22-28f9666f.patch']:
    patch=root/'author'/name
    subprocess.run(['git','apply','--check',str(patch)],cwd=dest,check=True)
    subprocess.run(['git','apply',str(patch)],cwd=dest,check=True)
    result.append(dict(patch=name,check_rc=0,apply_rc=0))
budget=(dest/'scripts/xvlog.budget').read_text()
assert 'section submodules: 0 finding(s)' in budget
assert not any(line and not line.startswith('#') for line in budget.splitlines())
result.append(dict(empty_budget=True,scope='static application at public 28f9666f only; not a consumer execution'))
(a.packet/'receipts/adoption-plant.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS {len(rows)} public checksums, three statistics pairs, two ordered patch applications')
