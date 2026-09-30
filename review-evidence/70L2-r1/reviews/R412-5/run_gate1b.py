#!/usr/bin/env python3
"""Run ONLY test_baremetal_profile_contract (gate 1b) from a probe tree.

Usage: run_gate1b.py <tree> [stop]
  stop: set R412_STOP=1, so the run ends right after the verdict controls
        (the hook in probe_lib.py prints kept/refused/interior bytes).
Prints GATE1B PASS / GATE1B STOP / GATE1B REFUSED: <first 700 chars>.
The SDK selector is required (--require-rv32 in argv), so the census uses
the provisioned RV32 compiler and nothing stands down.
"""
import os
import sys
import time
import traceback
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
if len(sys.argv) > 2 and sys.argv[2] == "stop":
    os.environ["R412_STOP"] = "1"
sys.argv = [str(tree / "sw/builder/test_builder.py"), "--require-rv32"]
sys.path.insert(0, str(tree / "sw/builder"))
os.chdir(tree)
started = time.time()
import test_builder  # noqa: E402
assert Path(test_builder.__file__).resolve().is_relative_to(tree), \
    test_builder.__file__
try:
    test_builder.test_baremetal_profile_contract()
except SystemExit as exc:
    print(f"GATE1B STOP rc={exc.code} ({time.time() - started:.0f} s)")
    sys.exit(0)
except AssertionError as exc:
    print(f"GATE1B REFUSED ({time.time() - started:.0f} s): "
          f"{str(exc)[:700]}")
    sys.exit(3)
except Exception:
    traceback.print_exc()
    print("GATE1B ERROR")
    sys.exit(4)
print(f"GATE1B PASS ({time.time() - started:.0f} s)")
