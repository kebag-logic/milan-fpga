#!/usr/bin/env python3
"""Verify the explicitly permitted installed tool, without launching a container."""
import gzip
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

OUT = Path(__file__).resolve().parent
SELECTOR = Path('$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator')
selector = SELECTOR.read_text()
words = shlex.split(selector.splitlines()[1])
toolroot = Path(next(s.split('=',1)[1] for s in words if s.startswith('VERILATOR_ROOT=')))
install = toolroot.parents[2]
package = install / 'var/lib/pacman/local/verilator-5.050-1'
mtree = gzip.decompress((package/'mtree').read_bytes()).decode()
records = []
missing = []
for line in mtree.splitlines():
    if not line.startswith('./'):
        continue
    parts = shlex.split(line)
    fields = dict(p.split('=',1) for p in parts[1:] if '=' in p)
    if 'sha256digest' not in fields:
        continue
    relative = parts[0][2:]
    if relative in ('.BUILDINFO', '.PKGINFO', '.INSTALL'):
        continue
    path = install / relative
    if not path.exists():
        missing.append(relative)
        assert relative.startswith('usr/share/man/'), relative
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == fields['sha256digest'], relative
    records.append(dict(path=relative,sha256=digest))
version = subprocess.check_output(['rtk','proxy',str(SELECTOR),'--version'],text=True).strip()
assert version == 'Verilator 5.050 2026-07-01 rev v5.050'
result = dict(version=version, selector=selector, selector_sha256=hashlib.sha256(SELECTOR.read_bytes()).hexdigest(),
              mtree_sha256=hashlib.sha256((package/'mtree').read_bytes()).hexdigest(),
              package_description=(package/'desc').read_text(), files=records, missing_manuals=missing)
(OUT/'tool-identity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(version=version,matched_files=len(records),missing_manuals=missing)))
