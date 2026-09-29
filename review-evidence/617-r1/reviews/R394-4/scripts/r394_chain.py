#!/usr/bin/env python3
"""R394-4: the make-4.3 chain. Run as the recipe of a `make -C <dir>` (so it inherits whatever
MAKEFLAGS that make hands a recipe), import the suite's committed mutants.py and call its own
build('dp') and makeflags_result() unchanged; print the inherited MAKEFLAGS and each result.

  python3 r394_chain.py <suite-dir> <workdir>
"""
import importlib.util
import os
import sys
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
print(f"inherited MAKEFLAGS={os.environ.get('MAKEFLAGS')!r}", flush=True)
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
sys.argv = [str(suite / "mutants.py")]
spec.loader.exec_module(m)
work.mkdir(parents=True, exist_ok=True)
src = work / "chain" / "milan_datapath.sv"
src.parent.mkdir(exist_ok=True)
src.write_text(m.DATAPATH.read_text())
exe = m.build("dp", src, work, "chain")
print(f"mutants.build('dp') -> {'built ' + exe.name if exe else 'None (did not compile)'}", flush=True)
if exe is None:
    print("\n".join(m.build_tail(m.build_log(work, "chain"))))
ok, lines = m.makeflags_result(work)
print("\n".join(lines))
sys.exit(0 if exe and ok else 1)
