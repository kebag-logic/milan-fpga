#!/usr/bin/env python3
"""Reconcile public findings only after the independent verdict is written."""
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
draft = (packet / 'independent-verdict.md').read_text()
assert draft.startswith('[R526] POSITIVE - exact head af5be4710c3516cc247c353213d6939fa8d23f57')
assert '| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |' in draft
out = packet / 'public'
for suffix, fields in [('issues/683/comments', ('id','html_url','body')), ('pulls/683/reviews', ('id','html_url','body','state','commit_id')), ('pulls/683/comments', ('id','html_url','body','path','line','commit_id'))]:
    data = json.loads(subprocess.check_output(['gh','api',f'repos/kebag-logic/milan-fpga/{suffix}?per_page=100']))
    if suffix.startswith('issues'):
        data = [c for c in data if c['body'].startswith(('[R526]', '[R527]'))]
    kept = [{k:c.get(k) for k in fields} for c in data]
    name = suffix.replace('/', '-') + '.json'
    (out / name).write_text(json.dumps(kept, indent=2) + '\n')
    print(suffix, len(kept), 'public records')
    for c in kept:
        print(c['id'], c['body'].splitlines()[0] if c['body'] else c.get('state'))
