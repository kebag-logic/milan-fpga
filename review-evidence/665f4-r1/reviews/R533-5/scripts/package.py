#!/usr/bin/env python3
"""Finalize publishable diagnostics, path-only provenance and SHA-256 manifest."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

packet=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
receipts=packet/'receipts'
campaign=receipts/'campaign';campaign.mkdir(exist_ok=True)
for log in (packet/'scratch/campaign').glob('*.log'):
    shutil.copyfile(log,campaign/log.name)
setup=packet/'scratch/probes-setup.log'
if setup.exists():
    shutil.copyfile(setup,receipts/'probe-setup-failure.log')
    (receipts/'probe-setup-failure.rc').write_text('1\n')
raw=packet/'scratch/original-receipts';raw.mkdir(exist_ok=True)
def sha(data):return hashlib.sha256(data).hexdigest()
entries=[]
for path in sorted(receipts.rglob('*')):
    if not path.is_file() or path.name=='receipt-provenance.json':continue
    rel=path.relative_to(receipts)
    original=raw/rel;original.parent.mkdir(parents=True,exist_ok=True)
    if not original.exists():shutil.copyfile(path,original)
    data=original.read_bytes()
    text=data.decode()
    text=text.replace(str(repo),'$REPO').replace(str(packet),'$PACKET')
    text=text.replace('$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz','$SDK_ARCHIVE')
    normalized=text.encode();path.write_bytes(normalized)
    entries.append({'path':str(path.relative_to(packet)),'raw_sha256':sha(data),
                    'published_sha256':sha(normalized),'path_normalization_only':data!=normalized})
(receipts/'receipt-provenance.json').write_text(json.dumps(entries,indent=2)+'\n')
publish=[packet/'REPORT.md',packet/'REPRODUCE.md',*sorted((packet/'scripts').glob('*.py')),
         *sorted((packet/'scripts').glob('*.cpp')),
         *sorted(x for x in receipts.rglob('*') if x.is_file())]
lines=[sha(p.read_bytes())+'  '+p.relative_to(packet).as_posix() for p in publish]
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print('Manifest files:',len(lines))
print('Report SHA-256:',sha((packet/'REPORT.md').read_bytes()))
assert 'SKELETON' not in (packet/'REPORT.md').read_text()
assert (packet/'REPORT.md').read_text().splitlines()[0]=='[R533] NEGATIVE - exact head 500b8f64443777685e6a54049d933476710d26f0'
assert (packet/'REPORT.md').read_text().splitlines()[-1]=='R533-5 FINISHED'
