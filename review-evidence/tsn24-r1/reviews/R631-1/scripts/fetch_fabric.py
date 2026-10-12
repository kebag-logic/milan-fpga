#!/usr/bin/env python3
"""Fetch only the pinned fabric authority and focused talker build inputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

p=argparse.ArgumentParser()
p.add_argument('packet',type=Path)
a=p.parse_args()
packet=a.packet.resolve()
repo='Mister-M-alt/protocol-processor-control-plane-avb-milan'
pin='2ad2f845dd583f8310075fa2380cb60a04fd091a'
fabric='c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'
def api(path,raw=False):
    args=['gh','api',path]
    if raw:args+=['-H','Accept: application/vnd.github.raw+json']
    return subprocess.check_output(args)
parent=json.loads(api(f'repos/kebag-logic/milan-fpga/git/trees/{fabric}?recursive=1'))
link=next(row for row in parent['tree'] if row['path']=='protocol-processor')
assert link['mode']=='160000' and link['sha']==pin
tree=json.loads(api(f'repos/{repo}/git/trees/{pin}?recursive=1'))
entries={row['path']:row for row in tree['tree']}
files=['hdl/common/pp_pkg.sv','hdl/srp/srp_pkg.sv','hdl/acmp/KL_acmp_talker.sv',
       'tb/acmp_talker/Makefile','tb/acmp_talker/sim_main.cpp','tb/acmp_talker/retry_cases.hpp',
       'tb/common/verilator_harness.hpp']
def get(path):
    data=api(f'repos/{repo}/contents/{path}?ref={pin}',True)
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob==entries[path]['sha']
    target=packet/'scratch/pp'/path
    target.parent.mkdir(exist_ok=True,parents=True)
    target.write_bytes(data)
    return {'path':path,'git_blob':blob,'mode':entries[path]['mode'],'sha256':hashlib.sha256(data).hexdigest()}
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(get,files))
(packet/'receipts/fabric-inputs.json').write_text(json.dumps({'fabric_head':fabric,'processor_gitlink':pin,'files':rows},indent=2)+'\n')
print('PASS pinned processor gitlink and seven focused build input blobs')
