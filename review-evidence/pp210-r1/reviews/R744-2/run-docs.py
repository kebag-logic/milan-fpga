#!/usr/bin/env python3
"""Usage: python3 run-docs.py DISPOSABLE_SOURCE PACKET.

Place the disposable source under PACKET/scratch; documentation dependencies
must be available. The repository may bootstrap a local rendering environment.
"""
import os
from pathlib import Path
import subprocess
import sys

root, packet = (Path(x).resolve() for x in sys.argv[1:])
scratch = packet / 'scratch'
assert root.is_relative_to(scratch)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
with (packet / 'docs.log').open('w') as out:
    result = subprocess.run(['make', '-j16', 'check'], cwd=root, env=env,
                            stdout=out, stderr=subprocess.STDOUT)
(packet / 'docs.rc').write_text(str(result.returncode) + '\n')
print('documentation gates rc', result.returncode)
sys.exit(result.returncode)
