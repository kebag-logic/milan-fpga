#!/usr/bin/env python3
"""Fetch selected immutable public receipts, proving their Git blob identities."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

REV='cf851544c2071f6edc611bf5600e81aec1356541'
PREFIX='review-evidence/726-r1/author-r3/'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);a=ap.parse_args()
    p=a.packet.resolve();(p/'scratch').mkdir(parents=True,exist_ok=True)
    treefile=p/'scratch/evidence-tree.json'
    if not treefile.is_file():
        treefile.write_bytes(subprocess.check_output(['gh','api',
            'repos/kebag-logic/milan-fpga/git/trees/'+REV+'?recursive=1']))
    tree=json.loads(treefile.read_text())['tree']
    selected=[]
    for item in tree:
        path=item['path']
        if not path.startswith(PREFIX) or item['type']!='blob':continue
        rel=path[len(PREFIX):]
        if (rel in ('ROUND3-GATES.tsv','ROUND3-DOCS-GATES.md','evidence/implementation-inputs.json')
            or (rel.startswith('review-round3/') and (Path(rel).name.startswith(('docs-', 'image-input-audit','pinned-builder-complete','pinned-builder-all','pinned-inputs-final','standing-before-', 'head-', 'lint-current','tkdiag-mutants','avtp-mutants','crf-mutants','native.'))))
            or (rel.startswith('evidence/alinx_ax7101') and any(s in rel for s in ('utilization_route','signoff_', '.tcl')))):
            selected.append(item)
    def fetch(item):
        src=item['path'];dst=p/'receipts/public'/src[len(PREFIX):]
        dst.parent.mkdir(parents=True,exist_ok=True)
        data=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json',
             'repos/kebag-logic/milan-fpga/contents/'+src+'?ref='+REV])
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==item['sha'],src
        dst.write_bytes(data)
        return dict(source=src,local=str(dst.relative_to(p)),git_blob=blob,sha256=hashlib.sha256(data).hexdigest())
    with ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(fetch,selected))
    (p/'receipts/public-provenance.json').write_text(json.dumps(dict(revision=REV,files=result),indent=2)+'\n')
    print('Verified public receipts:',len(result))

if __name__=='__main__':main()
