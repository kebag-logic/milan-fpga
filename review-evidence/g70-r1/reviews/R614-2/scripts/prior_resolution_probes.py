#!/usr/bin/env python3
"""Confirm prior-public-finding dispositions only after the independent verdict.

Usage: prior_resolution_probes.py REPO PACKET
"""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
assert (packet / "receipts/independent_verdict.md").is_file()
root = packet / "scratch" / "prior_probes"
root.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(root), PYTHONDONTWRITEBYTECODE="1")
source = (repo / "syn/ooc/check_ooc_clock.py").read_text()
mutants = [
    ("two-clocks-rule", "if len(clocks) != 1 or clocks[0] is None:", "if len(clocks) < 1 or clocks[0] is None:", "XDC with two create_clock lines escaped"),
    ("echo-anywhere-rule", "first(lines, LOG_READ_RE, 0, command)", "first(lines, LOG_READ_RE, 0, len(lines))", "read_xdc echoed after synth_design escaped"),
]
for label, old, new, expected in mutants:
    assert source.count(old) == 1
    target = root / (label + ".py")
    target.write_text(source.replace(old, new))
    p = subprocess.run([sys.executable, str(target), "--selftest"], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(label, "rc=" + str(p.returncode), p.stdout.strip())
    assert p.returncode != 0 and expected in p.stdout

for label, extra in (("extra-generated-clock", "create_generated_clock -name extra -source [get_ports clk_i] [get_ports rst_n]\n"), ("extra-timing-exception", "set_false_path -from [get_ports rx_valid_i]\n"), ("malformed-period", None), ("missing-xdc", None), ("missing-ucpu", None), ("missing-engine", None)):
    case = root / label
    case.mkdir(exist_ok=True)
    for name in ("check_ooc_clock.py", "ooc_clock.xdc", "ucpu_ooc.tcl", "engine_ooc.tcl"):
        shutil.copy2(repo / "syn/ooc" / name, case / name)
    xdc = case / "ooc_clock.xdc"
    if extra:
        xdc.write_text(xdc.read_text() + extra)
    elif label == "malformed-period":
        xdc.write_text(xdc.read_text().replace("10.000", "10.0.0"))
    else:
        (case / {"missing-xdc":"ooc_clock.xdc", "missing-ucpu":"ucpu_ooc.tcl", "missing-engine":"engine_ooc.tcl"}[label]).unlink()
    p = subprocess.run([sys.executable, str(case / "check_ooc_clock.py")], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(label, "rc=" + str(p.returncode))
    print(p.stdout)
    assert (p.returncode == 0) == bool(extra)
print("PASS: both prior mutation survivors now killed; optional XDC grammar/message hardening remains")
