#!/usr/bin/env python3
"""Prepare the explicit public file list and redact only local install roots.

Usage: python3 package.py PACKET
The manifest is the publication allow-list; all other files stay unpublished.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

p=Path(sys.argv[1]).resolve()
summary=[]
for file in sorted((p/'receipts/focused').glob('*.log')):
    lines=file.read_text().splitlines()
    failures=[l for l in lines if l.startswith('FAIL:')]
    summary.append({'file':str(file.relative_to(p)),
                    'tallies':[l for l in lines if 'checks:' in l and 'PASS' in l],
                    'failure_tags':dict(collections.Counter(l.split(':')[1].strip() for l in failures)),
                    'clock_counts':[l for l in lines if l.startswith('TOTAL_CLOCKS')],
                    'closed_cases':sum(l.startswith('LV_COLLISION') and ' CLOSED ' in l for l in lines),
                    'stuck_cases':sum(l.startswith('LV_COLLISION') and ' STUCK ' in l for l in lines)})
(p/'receipts/test-analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
names=['matrix.log','matrix.rc','notify-composition.log','notify-composition.rc',
       'planting.json','planting.log','planting.rc','docs-checks.log','docs-checks.rc',
       'identity-and-merges.txt','format-audit.json','reverse-patch-identity.json',
       'bank-reconciliation.json','public-manifest-verification.json',
       'consumer-gitlinks.json','consumer-third-party.json','clone-integrity.json',
       'clone-integrity.rc','source-scope.txt','independent-verdict.txt',
       'hosted-summary.json','resource-usage.json','test-analysis.json']
files=[p/'REPORT.md']+[p/'receipts'/name for name in names]
files+=list((p/'receipts').glob('hosted-jobs-*.json'))
files+=list((p/'receipts/focused').glob('*.log'))+list((p/'receipts/focused').glob('*.rc'))
files+=[p/'receipts/focused/summary.json']
files+=list((p/'scripts').glob('*.py'))+list((p/'scripts').glob('*.cpp'))
redaction_file=p/'receipts/path-redactions.json'
records=json.loads(redaction_file.read_text()) if redaction_file.exists() else []
for file in files:
    original=file.read_bytes()
    text=original.decode()
    text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/share/verilator',
                '<SCOPED_SIMULATOR_ROOT>',text)
    text=re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff',
                '<SCOPED_SIMULATOR_IMAGE>',text)
    published=text.encode()
    if published!=original:
        rel=file.relative_to(p)
        saved=p/'scratch/unredacted'/rel
        saved.parent.mkdir(parents=True,exist_ok=True)
        if not saved.exists(): saved.write_bytes(original)
        file.write_bytes(published)
        records.append({'file':str(rel),'original_sha256':hashlib.sha256(original).hexdigest(),
                        'published_sha256':hashlib.sha256(published).hexdigest(),
                        'change':'local simulator installation root only'})
redaction_file.write_text(json.dumps(records,indent=2)+'\n')
files.append(redaction_file)
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R489] POSITIVE - exact head ffc3a8e5733202384e55ea9094569cca86b78261'
assert report.splitlines()[-1]=='R489-3 FINISHED'
assert 'SKELETON' not in report
entries=[]
for file in sorted(set(files)):
    rel=file.relative_to(p)
    assert not str(rel).startswith('scratch/')
    entries.append(hashlib.sha256(file.read_bytes()).hexdigest()+'  '+str(rel))
(p/'MANIFEST.sha256').write_text('\n'.join(entries)+'\n')
print(f'Publication manifest: {len(entries)} files; scratch excluded; {len(records)} path redactions.')
