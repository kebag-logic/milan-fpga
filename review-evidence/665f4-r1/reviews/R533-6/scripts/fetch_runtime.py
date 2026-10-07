#!/usr/bin/env python3
"""Recover public runtime inputs and require every published source digest."""
import concurrent.futures
import hashlib
import json
import urllib.request
from pathlib import Path

packet=Path(__file__).resolve().parents[1]
manifest=packet/'scratch/ROUND2-RUNTIME.json'
if not manifest.exists():
    url='https://raw.githubusercontent.com/kebag-logic/milan-fpga/0fc49330/review-evidence/665f4-r1/author-r2/ROUND2-RUNTIME.json'
    manifest.write_bytes(urllib.request.urlopen(url).read())
roots={
 '${PICOLIBC}':('litex-hub/picolibc','16ff442da4b92e28d0753fabed18ad4a15254498','', 'picolibc'),
 '${COMPILER_RT}':('litex-hub/pythondata-software-compiler_rt','6eb76609c9627bf26635e57c63fb22cda7115887','pythondata_software_compiler_rt/data/','compiler-rt'),
 '${LITEX_SOFTWARE}':('enjoy-digital/litex','a1e1c3652ec2f1346ebaea7663d2867f393ae2c4','litex/soc/software/','litex-software'),
}
def fetch(entry):
    token,rel=entry['path'].split('/',1)
    if token not in roots:return None
    repo,rev,prefix,local=roots[token]
    url=f'https://raw.githubusercontent.com/{repo}/{rev}/{prefix}{rel}'
    data=urllib.request.urlopen(url,timeout=60).read()
    actual=hashlib.sha256(data).hexdigest()
    assert actual==entry['sha256'],(entry['path'],actual,entry['sha256'])
    dest=packet/'scratch/runtime-inputs'/local/rel
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    return {'input':entry['path'],'url':url,'sha256':actual}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    entries=[r for r in pool.map(fetch,json.loads(manifest.read_text())['files']) if r]
(packet/'receipts/runtime-inputs.json').write_text(json.dumps(entries,indent=2)+'\n')
print('Verified public runtime input files:',len(entries))
