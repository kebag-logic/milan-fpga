#!/usr/bin/env python3
"""R425-5: open-trace one analysis tool run with a Python audit hook.

Usage (from the extracted review-evidence/b5-r1 directory):
  r425_5_trace.py <tool.py> <args...>
Writes the tool's stdout unchanged; prints every file the tool opens, once,
relative to the current directory, on stderr prefixed with OPEN.
"""
import os, runpy, sys

seen = []
cwd = os.getcwd()

def hook(event, args):
    if event == 'open' and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        p = os.path.relpath(os.path.abspath(p), cwd)
        if p not in seen and not p.startswith('..'):
            seen.append(p)

tool = sys.argv[1]
sys.argv = sys.argv[1:]
sys.addaudithook(hook)
try:
    runpy.run_path(tool, run_name='__main__')
except SystemExit as e:
    if e.code not in (None, 0):
        raise
finally:
    sys.stdout.flush()
    for p in seen:
        if not p.endswith('.pyc') and '__pycache__' not in p:
            print('OPEN', p, file=sys.stderr)
