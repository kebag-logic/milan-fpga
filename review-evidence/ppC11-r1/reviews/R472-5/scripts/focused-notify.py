#!/usr/bin/env python3
"""Run only the three imported notification block controls, plus their golden."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

from review import PACKET, RECEIPTS, SCRATCH, run

repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
pinned = Path(os.environ.get('REVIEW_PINNED_SIM', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'))
env = os.environ.copy()
env.update(TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1', MAKEFLAGS='-j16')
version = run(repo, 'simulator-identity', [pinned, '--version'], env)
assert '5.050' in version
(RECEIPTS/'simulator-wrapper.sha256').write_text(hashlib.sha256(pinned.read_bytes()).hexdigest()+'  '+str(pinned)+'\n')
# Each of three concurrent arms gets at most four compiler jobs. The original
# Makefile asks for all CPUs; cap only the command line, without editing sources.
wrapper = SCRATCH/'sim-bounded'
wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\na=sys.argv[1:]\n'
                   'for i in range(len(a)-1):\n'
                   '    if a[i] == "-j": a[i+1] = "4"\n'
                   f'os.execv({str(pinned)!r}, [{str(pinned)!r}]+a)\n')
wrapper.chmod(0o755)
run(repo, 'notify-focused', [sys.executable, 'tb/pp_top/notify_mutants.py',
    '--output', RECEIPTS/'notify-focused', '--verilator', wrapper,
    '--jobs', '3', '--only', 'counter_spacing_from_selection_tw',
    'counter_stamp_at_send_only', 'counter_stamp_first_job_only'], env)
