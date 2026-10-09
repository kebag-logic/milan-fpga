#!/usr/bin/env python3
"""R580-2 probe P5: per-case fuzz statuses of one gate implementation on the head's fixtures.

Usage: probe_fuzz_cases.py <syn/ooc directory> <cases> <seed> <output tsv>
Imports pp_resource_gate from the given directory, records every per-case digest line the
fuzz driver hashes ("<number> <name> <label> <broken> <statuses>"), and writes them as TSV.
"""
import contextlib
import hashlib
import io
import sys
from pathlib import Path

folder, cases, seed, output = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
sys.path.insert(0, str(folder))
import pp_resource_gate as gate  # noqa: E402

recorded = []


class Recorder:
    def __init__(self, *args):
        self.inner = hashlib.sha256(*args)

    def update(self, data):
        recorded.append(data.decode(errors="replace"))
        self.inner.update(data)

    def hexdigest(self):
        return self.inner.hexdigest()

    def digest(self):
        return self.inner.digest()


class Shim:
    def __getattr__(self, name):
        return Recorder if name == "sha256" else getattr(hashlib, name)


gate.hashlib = Shim()
out = io.StringIO()
with contextlib.redirect_stdout(out):
    status = gate.fuzz(cases, seed, None, None, gate.BASELINE, gate.BUDGET)
lines = [line for line in recorded if line.count(" ") >= 3 and line.split(" ", 1)[0].lstrip("-").isdigit()]
output.write_text("".join(lines))
print(out.getvalue().splitlines()[-1], f"| status {status} | {len(lines)} case lines")
