#!/usr/bin/env python3
"""Install the pinned test dependency only inside PACKET/scratch.

Usage: python3 setup_gtest.py PACKET
"""
from pathlib import Path
import subprocess as sp
import sys

packet = Path(sys.argv[1]).resolve()
scratch = packet / 'scratch'
scratch.mkdir(parents=True, exist_ok=True)
src, build, prefix = (scratch / p for p in ('googletest', 'gtest-build', 'gtest-install'))
pin = 'f8d7d77c06936315286eb55f8de22cd23c188571'
if not src.exists():
    sp.run(['git', 'clone', '--depth', '1', '--branch', 'v1.14.0',
            'https://github.com/google/googletest.git', str(src)], check=True)
assert sp.check_output(['git', '-C', str(src), 'rev-parse', 'HEAD'], text=True).strip() == pin
sp.run(['cmake', '-S', str(src), '-B', str(build), '-DCMAKE_BUILD_TYPE=Release',
        '-DCMAKE_INSTALL_PREFIX=' + str(prefix)], check=True)
sp.run(['cmake', '--build', str(build), '-j16'], check=True)
sp.run(['cmake', '--install', str(build)], check=True)
print('Pinned dependency:', pin)
