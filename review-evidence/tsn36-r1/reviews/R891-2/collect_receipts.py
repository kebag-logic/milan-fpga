#!/usr/bin/env python3
"""Copy text receipts for publication, redacting only local path prefixes."""
import hashlib
import html
import json
import os
from pathlib import Path
import sys

repo,packet=(Path(x).resolve() for x in sys.argv[1:])
scratch=packet/'scratch'
sources=[]
for pattern in ('validate/*.log','validate/*.rc','validate/gates.json',
                'validate/mutations/results.json','validate/mutations/message-markers.json',
                'validate/mutations/gm-change-draws-startup-kind/*',
                'validate/mutations/gm-change-rearms-without-a-draw/*',
                'baremetal/results.json','baremetal/*/*.log','old-*.log'):
    for src in scratch.glob(pattern):
        if src.is_file() and src.suffix in ('.log','.json','.xml','.rc'):
            sources.append(src)
records=[]
for src in sorted(set(sources)):
    original=src.read_bytes()
    try: text=original.decode()
    except UnicodeDecodeError: continue
    replacements=[(str(repo),'<checkout>'),(str(packet),'<packet>')]
    dependency_root=os.environ.get('REVIEW_DEPENDENCY_ROOT')
    if dependency_root:
        replacements.append((dependency_root,'<dependencies>'))
    replacements.append((str(Path.home()),'<user>'))
    for old,new in replacements:
        text=text.replace(old,html.escape(new) if src.suffix=='.xml' else new)
    dst=packet/'receipts'/src.relative_to(scratch)
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(text)
    records.append({'file':str(dst.relative_to(packet)),
                    'raw_sha256':hashlib.sha256(original).hexdigest(),
                    'published_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
                    'path_redacted':original!=dst.read_bytes()})
(packet/'receipt-copy-record.json').write_text(json.dumps(records,indent=2)+'\n')
print('Collected',len(records),'text receipts; disposable trees remain excluded.')
