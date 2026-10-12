#!/usr/bin/env python3
"""Recheck the exact echo-hide edit with fresh responses, and ROM identity."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
receipts = packet / "receipts/echo"
receipts.mkdir(exist_ok=True)
os.environ["TMPDIR"] = str(scratch / "tmp")
sys.dont_write_bytecode = True
sys.path.insert(0, str(source / "scripts"))
from aecp_gate.selftest import echo_hide

def run(name, argv, cwd):
    with (receipts / (name + ".log")).open("w") as log:
        log.write("command: " + repr(argv) + "\n")
        log.flush()
        rc = subprocess.run(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
    (receipts / (name + ".rc")).write_text(str(rc)+"\n")
    return rc, (receipts / (name + ".log")).read_text()

tree = scratch / "echo"
shutil.copytree(scratch / "observed", tree, ignore=shutil.ignore_patterns(".git"))
echo_hide(tree)
table_path = tree / "hdl/aecp/ucode/aecp_commands.json"
table = json.loads(table_path.read_text())
bench = tree / "tb/aecp_cmds"
rc, _ = run("generate", [sys.executable, "-B", "../../hdl/aecp/ucode/gen_ucode.py", "-o", "ucode.hex"], bench)
assert rc == 0
# Only ROM contents changed. The same head-built executable reads ucode.hex at startup.
exe = bench / "obj_dir/Vaecp_cmds"
exe_hash = hashlib.sha256(exe.read_bytes()).hexdigest()
rc, _ = run("fresh-sweep", [str(exe), "obj_dir/echo-observed.json"], bench)
assert rc == 0
results = []
for name in ("echo-control", "echo-hide", "echo-explicit-shared"):
    variant = copy.deepcopy(table)
    if name == "echo-control":
        variant["echo_entries"].remove("EAVL")
    if name == "echo-explicit-shared":
        variant["shared_entries"]["EAVL"] = "review control: explicit shared program"
    table_path.write_text(json.dumps(variant, indent=2)+"\n")
    gate = [sys.executable, "-B", "scripts/check_aecp_commands.py"]
    write_rc, _ = run(name + "-write", gate + ["--write"], tree)
    record_rc, record_log = run(name + "-record", gate + ["--observed", str(bench / "obj_dir/echo-observed.json"), "--write-record"], tree)
    gate_rc, gate_log = run(name + "-gate", gate, tree)
    assert gate_rc == 1 and record_rc == 1, (name, gate_rc, record_rc)
    words = (["schema: echo_entries: EAVL", "nor listed in shared_entries"] if name == "echo-hide" else
             ["decode: ENTITY_AVAILABLE: EAVL answered SUCCESS at cdl 12", "rom: ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12"])
    assert all(word in gate_log for word in words), (name, gate_log)
    assert write_rc == (1 if name == "echo-hide" else 0)
    results.append(dict(variant=name, write_rc=write_rc, record_rc=record_rc, gate_rc=gate_rc,
                        named_failures=[s for s in gate_log.splitlines() if any(w in s for w in words)]))
(receipts / "results.json").write_text(json.dumps(dict(executable_sha256=exe_hash, variants=results), indent=2)+"\n")

roms = []
for ref in ("2cbed0a987c1e68402658d69459ab7e5aa571adc", "6d536868ee2a4762ab307d5ed51ff09c01130942", "4bee75b2e647507a71ece50359fceb135c334757"):
    root = scratch / ("rom-" + ref[:8])
    root.mkdir(exist_ok=True)
    for rel in ("hdl/aecp/ucode/gen_ucode.py", "hdl/acmp/rom/gen_ltn_rom.py", "hdl/aecp/ucode/aecp_commands.json"):
        fetched = subprocess.run(["git", "-C", str(source), "show", ref+":"+rel], capture_output=True)
        if fetched.returncode:
            assert rel.endswith("aecp_commands.json") and ref != "4bee75b2e647507a71ece50359fceb135c334757"
            continue
        (root / Path(rel).name).write_bytes(fetched.stdout)
    digests = {}
    for gen, output in (("gen_ucode.py", "ucode.hex"), ("gen_ltn_rom.py", "ltn_rom.hex")):
        rc, _ = run(ref[:8] + "-" + output, [sys.executable, "-B", gen, "-o", output], root)
        assert rc == 0
        digests[output] = hashlib.sha256((root / output).read_bytes()).hexdigest()
    roms.append(dict(commit=ref, sha256=digests))
assert all(r["sha256"] == roms[0]["sha256"] for r in roms)
(packet / "receipts/rom-identity.json").write_text(json.dumps(roms, indent=2)+"\n")
print("PASS: fresh short EAVL response rejected for all three echo variants; both ROMs identical at original base, imported main and head.")
