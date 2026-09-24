#!/usr/bin/env python3
"""[A261] scratch: run the WHOLE sw/builder/test_builder.py suite (its
`__main__` block, unmodified) under test_firmware_compiler.CompilerAudit.

  whole_suite.py <lane> sdk <sdk-host-dir> <audit.jsonl>   selector mapped to
      the verified disposable SDK (sdk.verify first), argv gets --require-rv32
  whole_suite.py <lane> absent <audit.jsonl>               every cross
      candidate hidden; a host compiler may only answer --version or probe.c

Exit status is the suite's own; the audit's compile count is printed last.
"""
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

lane = Path(sys.argv[1]).resolve()
mode = sys.argv[2]
destination = Path(sys.argv[3]).resolve() if mode == "sdk" else None
audit_path = Path(sys.argv[4] if mode == "sdk" else sys.argv[3])
sys.path[:0] = [str(lane / "sw/builder"), str(lane / "scripts")]
import test_firmware_compiler as tfc  # noqa: E402

if destination is not None:
    tfc.sdk.verify(destination)
script = str(lane / "sw/builder/test_builder.py")
argv = [script] + (["--require-rv32"] if destination is not None else [])
status = 0
with audit_path.open("w") as stream:
    audit = tfc.CompilerAudit(stream, destination)
    with patch.object(subprocess, "run", side_effect=audit.invoke), \
            patch.object(sys, "argv", argv):
        try:
            runpy.run_path(script, run_name="__main__")
        except SystemExit as exc:
            status = exc.code if isinstance(exc.code, int) else 1
print(f"WHOLE SUITE ({'mapped disposable SDK' if destination else 'absent'}):"
      f" exit {status}; {audit.compiles} actual firmware compiler invocations;"
      f" hidden {sorted(audit.hidden)}", flush=True)
sys.exit(status)
