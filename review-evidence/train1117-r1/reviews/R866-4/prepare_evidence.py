#!/usr/bin/env python3
"""Extract only the public author packet and manifest from the fixed archive commit."""
from pathlib import Path
import io
import subprocess
import tarfile

OUT = Path(__file__).resolve().parent / 'scratch/evidence'
OUT.mkdir(parents=True, exist_ok=True)
prefix = 'review-evidence/train1117-r1/'
data = subprocess.check_output(['git', 'archive', '563c16e5f62152a2ff1c9722e23208e1fbad0e88',
                                prefix + 'author-r6', prefix + 'MANIFEST.json'])
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    archive.extractall(OUT, filter='data')
print('Public author packet and checksum manifest extracted; no reviewer reports extracted')
