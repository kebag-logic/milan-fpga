#!/usr/bin/env python3
"""Foreground bounded concurrent review; disposable builds only under scratch."""
import concurrent.futures
import hashlib
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import time

root = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(sys.argv[2]).resolve()
simulator = pathlib.Path(sys.argv[3]).resolve()
scratch = packet / "scratch"
receipts = packet / "receipts"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch / "tmp"))
(scratch / "tmp").mkdir(exist_ok=True)

def raw(argv, cwd=root):
    return subprocess.check_output(["rtk", "proxy", *map(str, argv)], cwd=cwd, env=env)

def run(label, argv, cwd=root, expected=0, words=()):
    start = time.monotonic()
    with (receipts / (label + ".log")).open("w") as log:
        result = subprocess.run(["rtk", "proxy", *map(str, argv)], cwd=cwd, env=env,
                                stdout=log, stderr=subprocess.STDOUT, timeout=570)
    (receipts / (label + ".rc")).write_text(str(result.returncode) + "\n")
    (receipts / (label + ".json")).write_text(json.dumps(dict(
        argv=list(map(str, argv)), cwd=str(cwd), rc=result.returncode,
        expected=expected, elapsed_seconds=round(time.monotonic()-start, 3)), indent=2) + "\n")
    text = (receipts / (label + ".log")).read_text()
    assert result.returncode == expected, (label, result.returncode, text[-3000:])
    assert all(w in text for w in words), (label, words, text[-3000:])
    print(f"{label}: rc={result.returncode} expected={expected}", flush=True)

def snapshot(ref, name):
    dest = scratch / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    archive = raw(["git", "archive", ref])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(dest, filter="data")
    return dest

def gate_checks():
    run("gate-selftest", ["python3", "-B", "scripts/check_aecp_commands.py", "--selftest"])
    run("gate-optimized", ["python3", "-B", "-O", "scripts/check_aecp_commands.py", "--selftest"])
    run("gate-pr-reference", ["python3", "-B", "scripts/check_aecp_commands.py", "--pr-body", receipts / "PR-BODY.md"])
    run("focused-doc-checks", ["make", "-j16", "links", "matrix", "modmatrix", "params", "ids", "figures"])

def boundary_checks():
    run("independent-echo-probes", ["python3", "-B", packet / "scripts/probe_echo.py", root])
    src = snapshot("HEAD", "regeneration")
    before = {p: (src / p).read_bytes() for p in (
        "scripts/check_aecp_commands.py", "docs/architecture/06_aecp_engine.md",
        "docs/architecture/09_verification.md", "docs/00_MILAN_COMPLIANCE_REVIEW.md")}
    run("regenerated-references", ["python3", "-B", "scripts/check_aecp_commands.py", "--write"], src)
    assert all((src / p).read_bytes() == data for p, data in before.items())
    (receipts / "regeneration-identity.txt").write_text("All four generated references are byte-identical after --write.\n")
    # Revert each new guard separately in disposable copies. The standing tests must object.
    mutations = (
        ("membership", "scripts/aecp_gate/table.py", "for e in echoes if e not in shared", "for e in [] if e not in shared", "echo_entries names no shared program"),
        ("rom-success", "scripts/aecp_gate/rom.py", "(s != 0 and e in echo_shared)", "(e in echo_shared)", "a shared echo cannot exempt ROM SUCCESS"),
        ("record-success", "scripts/aecp_gate/record.py", "(int(s) != 0 and pn in echo_shared)", "(pn in echo_shared)", "a shared echo cannot exempt observed SUCCESS"),
    )
    for name, path, old, new, token in mutations:
        target = src / path
        original = target.read_text()
        assert original.count(old) == 1
        target.write_text(original.replace(old, new))
        try:
            run("guard-disabled-" + name, ["python3", "-B", "scripts/check_aecp_commands.py", "--selftest"], src,
                expected=1, words=("SELFTEST FAIL", token))
        finally:
            target.write_text(original)

def suite_checks():
    src = snapshot("HEAD", "suite")
    cwd = src / "tb/aecp_cmds"
    vflags = ('--cc --exe --build -j 12 --top-module aecp_cmds_wrap '
              '-Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL '
              '-Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY '
              '-CFLAGS "-std=c++17 -O2 -Wall -Wextra"')
    run("suite-baseline", ["make", "-j16", "VERILATOR=" + str(simulator), "VFLAGS=" + vflags], cwd,
        words=("176 checks: 176 PASS, 0 FAIL",))
    shutil.copyfile(cwd / "obj_dir/observed.json", receipts / "observed-baseline.json")
    # The three ENTITY_AVAILABLE body fields, edited directly, with exact match checks.
    path = src / "hdl/aecp/ucode/gen_ucode.py"
    text = path.read_text()
    fields = [
        "    u('BUILD_FLD', ra=3, fmt=FMT_D),             # flags                  @24",
        "    u('BUILD_FLD', ra=2, fmt=FMT_Q),             # acquired_controller_id @28",
        "    u('BUILD_FLD', ra=1, fmt=FMT_Q),             # locked_controller_id   @36",
    ]
    for field in fields:
        assert text.count(field) == 1
        text = text.replace(field, "    u('NOP'),")
    path.write_text(text)
    table_path = src / "hdl/aecp/ucode/aecp_commands.json"
    table = json.loads(table_path.read_text())
    table["echo_entries"].append("EAVL")
    table_path.write_text(json.dumps(table, indent=2) + "\n")
    run("echo-hide-gate", ["python3", "-B", "scripts/check_aecp_commands.py"], src,
        expected=1, words=("schema: echo_entries: EAVL", "nor listed in shared_entries"))
    # Explicit sharing permits membership but cannot exempt a SUCCESS size.
    table["shared_entries"]["EAVL"] = "Reviewer disposable shared-program probe"
    table_path.write_text(json.dumps(table, indent=2) + "\n")
    run("echo-shared-rom-gate", ["python3", "-B", "scripts/check_aecp_commands.py"], src,
        expected=1, words=("rom: ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12",))
    run("echo-shared-generate", ["python3", "-B", "../../hdl/aecp/ucode/gen_ucode.py", "-o", "ucode.hex"], cwd)
    run("echo-shared-sweep", ["./obj_dir/Vaecp_cmds", "obj_dir/echo-shared.json"], cwd,
        words=("0 timeouts",))
    shutil.copyfile(cwd / "obj_dir/echo-shared.json", receipts / "observed-echo-shared.json")
    run("echo-shared-observed", ["python3", "-B", "scripts/check_aecp_commands.py", "--observed",
                                "tb/aecp_cmds/obj_dir/echo-shared.json"], src,
        expected=1, words=("decode: ENTITY_AVAILABLE: EAVL answered SUCCESS",))
    run("echo-shared-rerecord", ["python3", "-B", "scripts/check_aecp_commands.py", "--observed",
                                "tb/aecp_cmds/obj_dir/echo-shared.json", "--write-record"], src,
        expected=1, words=("decode: ENTITY_AVAILABLE: EAVL answered SUCCESS",))
    run("echo-shared-fresh-gate", ["python3", "-B", "scripts/check_aecp_commands.py"], src,
        expected=1, words=("decode: ENTITY_AVAILABLE: EAVL answered SUCCESS",
                          "rom: ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12"))

def rom_checks():
    rows = []
    for ref, name in (("2cbed0a987c1e68402658d69459ab7e5aa571adc", "base-rom"),
                      ("15981b511370a8cfb58ec023fae27f8a800c058c", "resume-rom"),
                      ("HEAD", "head-rom")):
        src = snapshot(ref, name)
        for kind, path in (("ucode", "hdl/aecp/ucode/gen_ucode.py"), ("ltn", "hdl/acmp/rom/gen_ltn_rom.py")):
            dest = src / (kind + ".hex")
            run(name + "-" + kind, ["python3", "-B", path, "-o", dest], src)
            rows.append(dict(ref=ref, kind=kind, size=dest.stat().st_size,
                             sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
    for kind in ("ucode", "ltn"):
        assert len({r["sha256"] for r in rows if r["kind"] == kind}) == 1
    (receipts / "rom-identity.json").write_text(json.dumps(rows, indent=2) + "\n")
    paths = raw(["git", "diff", "--name-only", "2cbed0a987c1e68402658d69459ab7e5aa571adc", "HEAD", "--", "hdl/**/*.sv"]).decode()
    assert not paths, paths
    (receipts / "production-rtl-identity.txt").write_text("No production SystemVerilog changes from original base to exact head.\n" +
        "New testbench wrapper is outside production HDL.\n")

version = raw([simulator, "--version"]).decode()
assert "Verilator 5.050" in version
(receipts / "simulator-identity.txt").write_text(version + "wrapper_sha256=" + hashlib.sha256(simulator.read_bytes()).hexdigest() + "\n")
# Foreground supervisor owns all children and waits for completion. No detached jobs.
campaigns = {"gates": gate_checks, "boundaries": boundary_checks,
             "suite": suite_checks, "rom": rom_checks}
selected = sys.argv[4:] or list(campaigns)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(campaigns[name]) for name in selected]
    errors = []
    for f in concurrent.futures.as_completed(futures):
        try:
            f.result()
        except Exception as exc:
            errors.append(repr(exc))
            print("CHECK ERROR:", repr(exc), flush=True)
if errors:
    raise SystemExit("\n".join(errors))
print("Review validation complete: all expected outcomes matched.", flush=True)
