#!/usr/bin/env python3
"""Prove each echo check is load bearing without editing the source checkout."""
import concurrent.futures
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
os.environ["TMPDIR"] = str(packet / "scratch/tmp")
sys.dont_write_bytecode = True
sys.path.insert(0, str(source / "scripts"))
from aecp_gate.table import check_schema

table = json.loads((source / "hdl/aecp/ucode/aecp_commands.json").read_text())
positives = []
for program, shared in (("TIZ4NS", False), ("EAVL", True)):
    trial = copy.deepcopy(table)
    trial["echo_entries"].append(program)
    if shared:
        trial["shared_entries"][program] = "review control: explicit shared program"
    result = check_schema(trial)
    assert result == [], result
    positives.append(dict(program=program, explicit_shared=shared, findings=result))

variants = [
    ("membership", "table.py", "for e in echoes if e not in shared and (e in owners or uses[e] < 2)", "for e in echoes if False", "echo_entries names no shared program"),
    ("rom-success", "rom.py", "(s != 0 and e in echo_shared)", "(e in echo_shared)", "a shared echo cannot exempt ROM SUCCESS"),
    ("record-success", "record.py", "(int(s) != 0 and pn in echo_shared)", "(pn in echo_shared)", "a shared echo cannot exempt observed SUCCESS"),
]

def run(variant):
    name, filename, old, new, words = variant
    tree = packet / "scratch" / ("disabled-" + name)
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(source, tree, ignore=shutil.ignore_patterns(".git", "obj*", "__pycache__", ".venv*"))
    path = tree / "scripts/aecp_gate" / filename
    text = path.read_text()
    assert text.count(old) == 1
    path.write_text(text.replace(old, new))
    log = packet / "receipts" / ("disabled-" + name + ".log")
    with log.open("w") as stream:
        result = subprocess.run([sys.executable, "-B", "scripts/check_aecp_commands.py", "--selftest"],
                                cwd=tree, stdout=stream, stderr=subprocess.STDOUT)
    (log.with_suffix(".rc")).write_text(str(result.returncode)+"\n")
    diagnostics = [line for line in log.read_text().splitlines() if "SELFTEST FAIL" in line and words in line]
    assert result.returncode == 1 and diagnostics, (name, result.returncode, diagnostics)
    return dict(disabled=name, rc=result.returncode, expected_failure=diagnostics)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    disabled = list(pool.map(run, variants))
(packet / "receipts/round4-controls.json").write_text(json.dumps(dict(positive=positives, disabled=disabled), indent=2)+"\n")
print("PASS: both allowed membership forms accepted; disabling each of the three echo checks fails its standing control by name.")
