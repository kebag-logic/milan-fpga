#!/usr/bin/env python3
"""Run a tool and list the packet files it opens (Python audit hook, read-only probe).

usage: trace_opens.py <packet-root> <tool.py> <args...>
Prints each opened path relative to <packet-root>, to stderr, once; the tool's
stdout is left untouched.
"""
import os, runpy, sys

root = os.path.realpath(sys.argv[1])
seen = set()
def hook(ev, args):
    if ev == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.path.realpath(os.fsdecode(args[0]))
        if p.startswith(root) and p not in seen:
            seen.add(p)
            sys.stderr.write("OPEN " + os.path.relpath(p, root) + "\n")
sys.addaudithook(hook)
sys.argv = sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
