#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Collect text receipts; normalize machine-specific prefixes without changing outcomes."""
import argparse
import hashlib
import json
from pathlib import Path
import re

p=argparse.ArgumentParser()
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--repo',type=Path,required=True)
a=p.parse_args()
packet=a.packet.resolve()
scratch=packet/'scratch'
receipt=packet/'receipts'
rows=[]

def copy(source,target):
    original=source.read_bytes()
    text=original.decode()
    text=text.replace(str(scratch),'${SCRATCH}').replace(str(a.repo.resolve()),'${SOURCE}').replace(str(packet),'${PACKET}')
    text=re.sub(r'/data/[^/\s]+/tools/gtest-1\.14\.0','${GTEST_PREFIX}',text)
    text=re.sub(r'/data/[^/\s]+/tools/clang-18/root','${CLANG18_SDK}',text)
    text=re.sub(r'/data/[^/\s]+/tools/pinned-verilator-5\.050/verilator','${RTL_SIMULATOR}',text)
    text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff','${RTL_SDK}',text)
    text=re.sub(r'<home-path>/work/tsn-c-stack/tsn-c-stack','${HOSTED_SOURCE}',text)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text)
    rows.append(dict(receipt=str(target.relative_to(packet)),raw_sha256=hashlib.sha256(original).hexdigest(),
                     published_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),prefix_normalized=text.encode()!=original))

for name in ['validation','initial','probes','rtl','base-run']:
    for f in (scratch/name).glob('*'):
        if f.is_file() and f.suffix in ('.log','.rc','.json'):
            copy(f,receipt/name/f.name)
for directory in ['complete-suites','rtl-edges']:
    for f in (scratch/directory).rglob('*'):
        rel=f.relative_to(scratch/directory)
        if f.is_file() and 'processor' not in rel.parts and f.suffix in ('.log','.rc','.json','.xml'):
            copy(f,receipt/directory/rel)
for f in (scratch/'validation/mutations').rglob('*'):
    if f.is_file() and f.suffix in ('.xml','.json'):
        copy(f,receipt/'mutations'/f.relative_to(scratch/'validation/mutations'))
for directory in ['escape','physical-0']:
    for f in (scratch/directory).rglob('*'):
        rel=f.relative_to(scratch/directory)
        if f.is_file() and not any(x in rel.parts for x in ['tree','build','b','selftest']) and f.suffix in ('.log','.rc','.json'):
            copy(f,receipt/directory/rel)
for name in ['rv32','rv32-base']:
    for f in (scratch/name).rglob('*'):
        rel=f.relative_to(scratch/name)
        if len(rel.parts)<=2 and f.is_file() and f.suffix in ('.log','.json'):
            copy(f,receipt/name/rel)
for name in ['base-static','static-analysis-18','static-analysis-18-complete-sdk','complete-suites']:
    for suffix in ['.log','.rc']:
        copy(scratch/(name+suffix),receipt/'additional'/(name+suffix))
for name in ['gates.json','coverage.log','static-analysis.log','gcc-test.log','clang-sanitizers-test.log','graphs.log']:
    copy(scratch/'hosted-quality'/name,receipt/'hosted'/name)
copy(scratch/'hosted-rv32/results.json',receipt/'hosted/rv32-results.json')
(receipt/'receipt-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Collected',len(rows),'receipts; original bytes remain in unpublished scratch; result contents unchanged.')
