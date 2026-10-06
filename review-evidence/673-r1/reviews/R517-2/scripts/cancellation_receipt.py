#!/usr/bin/env python3
"""Run the focused driver fixture and redact only the disposable root path."""
import os
from pathlib import Path
import subprocess
import sys

repo, packet = (Path(p).resolve() for p in sys.argv[1:])
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(packet / "scratch"))
result = subprocess.run([sys.executable, "scripts/test_suite_cancellation.py"],
                        cwd=repo, env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, timeout=300)
(packet / "scratch/suite-cancellation-raw.log").write_bytes(result.stdout)
public = result.stdout.replace(str(packet / "scratch").encode(), b"$SCRATCH")
(packet / "receipts/suite-cancellation.log").write_bytes(public)
(packet / "receipts/suite-cancellation.rc").write_text(str(result.returncode) + "\n")
print(public.decode())
sys.exit(result.returncode)
