#!/usr/bin/env python3
"""Materialize only pinned public author evidence; never reviewer reports."""
import subprocess, sys, tarfile
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
ref = '0cad829e1af15b9c96b0ef3d10d109b9721154c5'
base = 'review-evidence/artysplit-r1'
paths = [base + '/MANIFEST.json', base + '/author-r8/receipts', base + '/author-r8/REVIEW-READY.md', base + '/author-r8/PR-BODY.md']
out.mkdir(parents=True, exist_ok=True)
proc = subprocess.Popen(['git', '-C', str(repo), 'archive', ref, *paths], stdout=subprocess.PIPE)
count = size = 0
with tarfile.open(fileobj=proc.stdout, mode='r|') as archive:
    for member in archive:
        if not member.isfile():
            continue
        relative = Path(member.name).relative_to(base)
        assert '..' not in relative.parts
        target = out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.extractfile(member) as src, target.open('wb') as dst:
            while chunk := src.read(1024 * 1024):
                dst.write(chunk)
        count += 1
        size += member.size
assert proc.wait() == 0
print(f'PASS extracted {count} files, {size} bytes from {ref}')
