"""Build the head parser harness against another RTL tree and run it.

usage: head_harness_on_base.py <parser tb dir> <rtl src dir> <work dir>
"""
import sys
from pathlib import Path

tb = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tb))
import mutants  # noqa: E402

exe = mutants.build(Path(sys.argv[2]).resolve(), Path(sys.argv[3]), "base")
rc, out = mutants.run_harness(exe)
print(out, end="")
print(f"rc {rc}")
