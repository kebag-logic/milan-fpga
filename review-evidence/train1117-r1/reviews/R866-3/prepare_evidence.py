#!/usr/bin/env python3
"""Extract only the public author packet and manifest into the review scratch directory."""
import io
from pathlib import Path
import subprocess
import sys
import tarfile

out = Path(sys.argv[1]).resolve()
archive = '33c82526d5f62e39b1324b5dd3e34b63602f8c03'
data = subprocess.check_output(['git', 'archive', archive,
    'review-evidence/train1117-r1/author-r5', 'review-evidence/train1117-r1/MANIFEST.json'])
scratch = out / 'scratch'
scratch.mkdir(parents=True, exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(data)) as stream:
    stream.extractall(scratch, filter='data')
print('Extracted public author-r5 and its manifest at', archive)
