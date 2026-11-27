#!/usr/bin/env python3
"""Copy execution receipts only; redact host paths, keeping disposable trees private.

Usage: collect_receipts.py CHECKOUT TOOL_ROOT
"""
import hashlib
import json
from pathlib import Path
import sys

p = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
tools = Path(sys.argv[2]).resolve()
scratch = p/'scratch'
q = scratch/'quality'
selected = list(q.glob('*.log')) + list(q.glob('*.rc')) + [q/'gates.json',q/'mutations/results.json',q/'mutations/message-markers.json']
names = [r['name'] for r in json.loads((root/'tests/mutations.json').read_text())
         if r['name'].startswith(('record-omit','record-drop','walk-publish-no','walk-admit-no','view-drop'))]
for name in names:
    selected += list((q/'mutations'/name).glob('*.xml')) + list((q/'mutations'/name).glob('*.log'))
selected += list((q/'mutations/baseline').glob('*.xml'))
selected += [scratch/'rv32/results.json',scratch/'octet-probes/results.json']
for name in ('debug','release'):
    selected += list((scratch/'rv32'/name).glob('*.log')) + list((scratch/'rv32'/name).glob('*.map'))
selected += list((scratch/'octet-probes').glob('*/*.xml')) + list((scratch/'octet-probes').glob('*/*.log'))
redactions = [(str(scratch),'<scratch>'),(str(root),'<checkout>'),(str(p),'<packet>'),(str(tools),'<tool-root>')]
def redact(text):
    for old,new in redactions:
        text=text.replace(old,new)
    return text
records=[]
for src in sorted(set(selected)):
    dest=p/'receipts'/src.relative_to(scratch)
    data=src.read_bytes()
    cooked=redact(data.decode()).encode()
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(cooked)
    records.append({'file':dest.relative_to(p).as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest(),
                    'published_sha256':hashlib.sha256(cooked).hexdigest(),'path_redacted':data!=cooked})
for name in ('jobs.json','rv32.log','quality.log'):
    f=p/name
    f.write_text(redact(f.read_text()))
(p/'receipt-export.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(records)} execution receipts exported; only paths redacted')
