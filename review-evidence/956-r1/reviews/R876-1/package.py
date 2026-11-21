#!/usr/bin/env python3
"""Hash the explicit publishable packet; scratch is always excluded."""
import hashlib
from pathlib import Path
packet=Path(__file__).resolve().parent
files=['REPORT.md','focused.py','reset_probe.cpp','rerun.py','checks.py','audit.py','package.py','public-review-state.json']
stems=['srp-1x1-if1','srp-8x8-if1','srp-8x8-if2-existing','composed-8x8-if2',
       'aecp-1x1-if1','aecp-1x1-if2-existing','aecp-8x8-if1-existing',
       'reset-1x1-if1','reset-8x8-if2','phases-1x1-if1','phases-8x8-if1','phases-8x8-if2',
       'load','flip-1x1','flip-8x8','shape','harness-selftest','audit']
files += [s+ext for s in stems for ext in ('.log','.rc')]
report=(packet/'REPORT.md').read_text()
assert 'SKELETON' not in report
assert report.startswith('[R876] NEGATIVE - exact head 0d80f0ed2a880c3a3b2429c669f104801203ec05\n')
assert report.rstrip().endswith('R876-1 FINISHED')
lines=[]
for name in sorted(files):
    data=(packet/name).read_bytes()
    lines.append(hashlib.sha256(data).hexdigest()+'  '+name)
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print(f'{len(files)} publishable files hashed; scratch excluded')
