#!/usr/bin/env python3
"""Run a repository script under an audit hook; record every file it opens or imports under the repository root.

usage: trace_reads.py <repo_root> <log_out> <script> [args...]
"""
import os, runpy, sys
root = os.path.realpath(sys.argv[1]); out = sys.argv[2]; script = sys.argv[3]
seen = set()
def hook(event, args):
    if event in ('open', 'import') and args:
        p = args[0]
        if event == 'import':
            return
        if isinstance(p, (str, bytes, os.PathLike)):
            try:
                rp = os.path.realpath(os.fsdecode(p))
            except Exception:
                return
            if rp.startswith(root + os.sep):
                seen.add(os.path.relpath(rp, root))
sys.addaudithook(hook)
sys.argv = [script] + sys.argv[4:]
rc = 0
try:
    runpy.run_path(script, run_name='__main__')
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
finally:
    for m in list(sys.modules.values()):
        f = getattr(m, '__file__', None)
        if f:
            rp = os.path.realpath(f)
            if rp.startswith(root + os.sep):
                seen.add(os.path.relpath(rp, root))
    with open(out, 'w') as fh:
        for s in sorted(seen):
            if '__pycache__' not in s:
                fh.write(s + '\n')
sys.exit(rc)
