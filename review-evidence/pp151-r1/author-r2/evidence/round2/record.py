#!/usr/bin/env python3
"""Record a foreground command and its status without piping its output."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

out = Path(sys.argv[1])
cwd = Path(sys.argv[2]).resolve()
cmd = sys.argv[3:]
out.parent.mkdir(parents=True, exist_ok=True)
out.with_suffix('.cmd').write_text(shlex.join(cmd) + '\n')
env = os.environ.copy()
env['PATH'] = '<scratch>/tools/bin:' + env['PATH']
if env.get('PP151_SV2V') == '013':
    env['PATH'] = '<scratch>/r2/hostbin:' + env['PATH']
env['VERILATOR'] = '<tools>/pinned-verilator-5.050/verilator'
env['MAKEFLAGS'] = '-j16'
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['TMPDIR'] = '<scratch>/r2/tmp'
Path(env['TMPDIR']).mkdir(exist_ok=True)
started = time.time()
with out.with_suffix('.log').open('w') as stream:
    rc = subprocess.run(cmd, cwd=cwd, env=env, stdout=stream,
                        stderr=subprocess.STDOUT, check=False).returncode
out.with_suffix('.rc').write_text(str(rc) + '\n')
out.with_suffix('.seconds').write_text(f'{time.time() - started:.1f}\n')
print(f'{out.name}: rc={rc}', flush=True)
