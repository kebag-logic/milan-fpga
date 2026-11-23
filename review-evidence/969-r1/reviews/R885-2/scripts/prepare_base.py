#!/usr/bin/env python3
"""Extract only the prior adapter tree for the differential probes, inside the packet scratch directory.
Usage: python3 -I prepare_base.py CHECKOUT PACKET
"""
import io
from pathlib import Path
import subprocess
import sys
import tarfile

root, packet = (Path(p).resolve() for p in sys.argv[1:])
out = packet/'scratch/f863'
out.mkdir(parents=True, exist_ok=True)
data = subprocess.check_output(['git', '-C', str(root), 'archive', 'f863258d', 'sw/firmware/ctrl'])
with tarfile.open(fileobj=io.BytesIO(data)) as tar:
    tar.extractall(out, filter='data')
print('Prior adapter extracted at f863258d into scratch/f863')
