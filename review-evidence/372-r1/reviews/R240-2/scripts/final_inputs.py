#!/usr/bin/env python3
"""Prove every exported build input still equals its reviewed tracked blob."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parents[1]
scratch = out/'scratch'
rows = []
entries = subprocess.check_output(['rtk','proxy','git','-C',str(repo),'ls-tree','-rz','HEAD'])
for entry in entries.split(b'\0')[:-1]:
    metadata,name=entry.split(b'\t',1)
    mode,kind,oid=metadata.decode().split()
    name=name.decode()
    if kind!='blob' or not (scratch/name).exists():
        continue
    content=(scratch/name).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
    assert actual==oid,name
    rows.append(dict(path=name,blob=oid))
fifo='third_party/verilog-axis/rtl/axis_fifo.v'
assert (repo/fifo).read_bytes()==(scratch/fifo).read_bytes()
models=[]
for width in [8,64]:
    obj=scratch/f'tb/verilator/ptp_ts/obj_dir_mux_sva_w{width}'
    for name in ['Vaxis_mux_rr_2in_1out___024root__0.cpp',
                 'Vaxis_mux_rr_2in_1out__Syms__Slow.cpp']:
        content=(obj/name).read_bytes()
        models.append(dict(path=str((obj/name).relative_to(out)),sha256=hashlib.sha256(content).hexdigest()))
print(json.dumps(dict(result='PASS',exported_parent_files=len(rows),files=rows,
                     pinned_fifo_matches=True,generated_models=models),indent=2))
