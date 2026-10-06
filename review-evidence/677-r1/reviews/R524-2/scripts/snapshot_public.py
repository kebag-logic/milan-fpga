#!/usr/bin/env python3
"""Read only the assigned public scope and correction artifacts."""
import argparse
import json
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('packet', type=Path)
args = ap.parse_args()
out = args.packet / 'receipts'
out.mkdir(parents=True, exist_ok=True)

def read(endpoint):
    return json.loads(subprocess.check_output(['rtk', 'proxy', 'gh', 'api', 'repos/kebag-logic/milan-fpga/' + endpoint]))

def save(name, obj):
    (out / name).write_text(json.dumps(obj, indent=2) + '\n')

for number, filename in [(677, 'issue-body.json'), (678, 'issue-678-body.json')]:
    obj = read(f'issues/{number}')
    save(filename, {k: obj[k] for k in ['number', 'title', 'body', 'html_url', 'updated_at']})
obj = read('pulls/684')
pr = {k: obj[k] for k in ['number', 'title', 'body', 'html_url', 'updated_at']}
for k in ['head', 'base']:
    pr[k] = {f: obj[k][f] for f in ['sha', 'ref']}
save('pr-body.json', pr)
for number in [6021510152, 6021539044, 6024328677, 6024757146, 6024758039]:
    obj = read(f'issues/comments/{number}')
    save(f'comment-{number}.json', {k: obj[k] for k in ['id', 'body', 'html_url', 'created_at', 'updated_at']})
print('PASS: public scope and correction artifacts captured; no write requests')
