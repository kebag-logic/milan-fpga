#!/usr/bin/env python3
"""Run `python3 sw/builder/test_builder.py` -- its own __main__ block,
unchanged -- with every RV32 cross compiler hidden, through the CompilerAudit
that sw/builder/test_firmware_compiler.py --absent (the CI compiler-absent
control) uses: a cross candidate raises FileNotFoundError, and any attempt
to compile firmware with a host compiler is an error.

usage: suite_absent.py <lane> <audit.jsonl>"""
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

lane, audit_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path.insert(0, str(lane / "scripts"))
sys.path.insert(0, str(lane / "sw/builder"))
import test_firmware_compiler as tfc  # noqa: E402

builder = lane / "sw/builder/test_builder.py"
with audit_path.open("w") as stream:
    audit = tfc.CompilerAudit(stream, None)
    with patch.object(subprocess, "run", side_effect=audit.invoke), \
            patch.object(sys, "argv", [str(builder)]):
        runpy.run_path(str(builder), run_name="__main__")
    assert audit.hidden == audit.cross, audit.hidden
    assert audit.compiles == 0, "absent mode compiled firmware"
print(f"suite-absent: cross candidates hidden {sorted(audit.hidden)}; "
      f"{audit.compiles} firmware compiles")
