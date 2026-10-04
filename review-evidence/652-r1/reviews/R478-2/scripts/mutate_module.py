#!/usr/bin/env python3
"""Run a resmap module's self-test with one defect planted IN MEMORY: the
module's source is read from the review clone, exactly one occurrence of OLD
is replaced by NEW, and the result is executed under the module's own name and
path, so the clone's files are never written.
Usage: mutate_module.py <path to module .py> OLD NEW
Prints SELFTEST rc=<rc>; rc 0 means the planted defect survived the self-test."""
import contextlib
import importlib.util
import sys
from pathlib import Path

path = Path(sys.argv[1]).resolve()
old, new = (a.encode().decode("unicode_escape") for a in sys.argv[2:4])
sys.path.insert(0, str(path.parent))
source = path.read_text(encoding="utf-8")
if source.count(old) != 1:
    sys.exit(f"anchor occurs {source.count(old)} times")
spec = importlib.util.spec_from_file_location(path.stem, path)
module = importlib.util.module_from_spec(spec)
sys.modules[path.stem] = module
exec(compile(source.replace(old, new), str(path), "exec"), module.__dict__)
try:
    rc = module.selftest()
except BaseException as exc:  # a crash is a red self-test
    print(f"self-test raised {type(exc).__name__}: {exc}")
    rc = 1
print(f"SELFTEST rc={rc}")
