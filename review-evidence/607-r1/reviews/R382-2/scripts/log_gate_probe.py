#!/usr/bin/env python3
"""Apply the exact-head check_implementation_log to COPIES of real implementation logs.

The gate renames adjacent *.bit files on refusal, so it is never pointed at an evidence
directory: each log is hash-verified against its public index entry, copied into a fresh
scratch directory next to a decoy `alinx_ax7101.bit`, and the gate runs there.

Usage: log_gate_probe.py <clone> <scratch> <index.json>:<ROOTVAR>=<root> ...
Each index is a public JSON list of {path, size, sha256}; only entries ending in vivado.log
are used. Also exercises synthetic 12-5201 lines at each severity and at INFO level.
"""
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

clone, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "sw/litex"))
from clock_constraints import check_implementation_log  # noqa: E402

ID = re.compile(r"\[(Vivado 12-4739|Vivado 12-5201|Designutils 20-1307)\]")


def run(label: str, log_bytes: bytes) -> None:
    work = scratch / f"gate-{label}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    (work / "vivado.log").write_bytes(log_bytes)
    (work / "alinx_ax7101.bit").write_bytes(b"decoy")
    try:
        check_implementation_log(work / "vivado.log")
        verdict = "ACCEPTED"
    except RuntimeError as exc:
        ids = Counter(ID.search(line).group(1) for line in str(exc).splitlines()[1:])
        verdict = f"REFUSED findings={sum(ids.values())} {dict(sorted(ids.items()))}"
    left = sorted(p.name for p in work.iterdir() if p.name != "vivado.log")
    print(f"{label}: {verdict}; files after gate: {left}")
    shutil.rmtree(work)


for spec in sys.argv[3:]:
    index, root = spec.split(":", 1)
    var, value = root.split("=", 1)
    for item in json.load(open(index)):
        if not item["path"].endswith("vivado.log"):
            continue
        path = Path(item["path"].replace(var, value))
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != item["sha256"] or len(data) != item["size"]:
            print(f"{item['path']}: HASH MISMATCH, not used")
            continue
        run(path.parent.parent.name, data)

for severity in ("WARNING", "CRITICAL WARNING", "ERROR", "INFO"):
    run(f"synthetic-12-5201-{severity.replace(' ', '_')}",
        f"{severity}: [Vivado 12-5201] set_clock_groups: cannot set the clock group "
        "when only one non-empty group remains.\n".encode())
