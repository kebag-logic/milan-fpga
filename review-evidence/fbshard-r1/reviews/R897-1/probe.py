#!/usr/bin/env python3
"""Focused, disposable review checks. Usage: python3 probe.py CHECKOUT PACKET."""
import argparse
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
scratch = packet / "scratch" / "focused"
scratch.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(scratch)
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as cfg
import ctrl_boundary as boundary
import ctrl_capture as capture
import ctrl_runs as runs
import test_ctrl_firmware as driver
import test_ctrl_firmware_shards as dispatch
import yaml

BASE = "854bd7236792ce1adbd10c43b13a6a5002ad3bb6"

def old_module(name, path):
    module = ModuleType(name)
    module.__file__ = str(root / path)
    source = subprocess.check_output(["git", "-C", str(root), "show", f"{BASE}:{path}"], text=True)
    exec(compile(source, str(root / path), "exec"), module.__dict__)
    return module

old = old_module("baseline_driver", "sw/firmware/ctrl/test/test_ctrl_firmware.py")
old.aecp_arms = old_module("aecp_arms", "sw/firmware/ctrl/test/aecp_arms.py")
for phase in (None, (0, 1)):
    before = dispatch.inventory(old, build_part=phase)
    after = dispatch.inventory(driver, build_part=phase)
    assert before == after, "baseline/head ordered dispatch differs"
    print(f"PASS ordered baseline/head dispatch: {len(after)} calls, build-only={phase is not None}")
    (packet / ("build-inventory.json" if phase else "full-inventory.json")).write_text(json.dumps(after, indent=2) + "\n")

def aecp_trace(module, coverage):
    tree = driver.Tree(driver.CTRL, Path("out"), Path("reuse"), driver.fw_gtest.Build(jobs=4, coverage=coverage))
    calls = []
    def arm(*args, **kwargs):
        def norm(value):
            if isinstance(value, driver.Tree):
                return [str(value.src.relative_to(root)), str(value.out), str(value.reuse), str(value.build.coverage)]
            if isinstance(value, Path):
                return str(value.relative_to(root)) if value.is_relative_to(root) else str(value)
            return value
        calls.append(([norm(x) for x in args], {k: norm(v) for k, v in kwargs.items()}))
        return dispatch.Outcome("trace", 0, "")
    with patch.object(module, "core_arm", side_effect=arm), patch.object(module, "image_arm", side_effect=arm), \
            patch.object(module, "key_geometry", side_effect=lambda out, name, widths: out / f"keys-{name}.yaml"):
        module.all_arms(tree)
    return calls

for coverage in (None, scratch / "coverage"):
    before, after = aecp_trace(old.aecp_arms, coverage), aecp_trace(driver.aecp_arms, coverage)
    assert before == after
    print(f"PASS AECP ordered calls and arguments, including output paths: {len(after)}, coverage={coverage is not None}")

dispatch.run_cases(driver)
for count in (1, 2, 3, 4):
    parts = dispatch.build_part_cases(driver, count)
    assert Counter(x for part in parts for x in part) == Counter(dispatch.inventory(old, build_part=(0, 1)))
print("PASS build-part unions independently equal the pre-change dispatch")

known = cfg.units()
assert len(known) == 8 and not cfg.plan_findings()
commands = tuple({"argv": [w.format(python=sys.executable, work=scratch) for w in unit.words], "rc": 0, "cwd": str(root)} for unit in known)
assert not cfg.union_findings(commands)
for unit in known:
    dropped = tuple(tuple(n for n in shard if n != unit.name) for shard in cfg.SHARDS)
    duplicated = (*cfg.SHARDS[:-1], (*cfg.SHARDS[-1], unit.name))
    for label, table in (("dropped", dropped), ("duplicated", duplicated)):
        with patch.object(cfg, "SHARDS", table):
            findings = cfg.plan_findings()
            assert any(unit.name in f for f in findings)
            with patch.object(boundary.fw_rv32, "compiler", return_value="compiler-unused"), \
                    patch.object(boundary, "build_shard", side_effect=AssertionError("built before plan refusal")), \
                    redirect_stdout(io.StringIO()) as output:
                rc = boundary.main(["--require-rv32", "--without", "verilator", "--shard", "0/3", "--capture-out", str(scratch / "unused")])
            assert rc == 2 and unit.name in output.getvalue()
        print(f"PASS live table {label} refusal before building: {unit.name}")
    mine = next(c for c in commands if unit.runs(c["argv"]))
    for label, cmds in (("dropped", tuple(c for c in commands if c is not mine)), ("duplicated", (*commands, mine))):
        found = cfg.union_findings(cmds)
        assert len(found) == 1 and unit.name in found[0]
        print(f"PASS capture union {label} refusal: {unit.name}")
assert cfg.plan_findings((*cfg.SHARDS, ("unknown-unit",)))
assert cfg.union_findings((*commands, {"argv": ["unknown-command"]}))
assert boundary.shard_controls(commands) == (0, 4)

invalid = [["--shard", x, "--capture-out", "unused", "--without", "verilator"] for x in ("0/0", "3/3", "-1/3", "x/3", "0/2")]
invalid += [["--shard", "0/3"], ["--shards", "3", "--without", "verilator"], ["--capture-out", "unused"], ["--shards", "0", "--capture", "unused", "--without", "verilator"]]
for argv in invalid:
    with redirect_stderr(io.StringIO()):
        try:
            boundary.arguments(argv)
        except SystemExit as exc:
            assert exc.code == 2
        else:
            raise AssertionError(argv)
print(f"PASS {len(invalid)} invalid boundary argument combinations refused")

workflow = yaml.safe_load((root / ".github/workflows/rtl-fast.yml").read_text())
jobs = workflow["jobs"]
matrix = jobs["firmware-boundary-shards"]
assert matrix["strategy"]["matrix"] == {"shard": [0, 1, 2], "total": [3]}
assert matrix["timeout-minutes"] == jobs["firmware-boundary"]["timeout-minutes"] == 30
assert "firmware-boundary-shards" in jobs["firmware-boundary"]["needs"]
assert "firmware-boundary-shards" in jobs["rtl-fast"]["needs"]
verdict = next(s for s in jobs["rtl-fast"]["steps"] if "FIRMWARE_BOUNDARY_SHARDS_RESULT" in s.get("env", {}))
env = {**os.environ, **{key: "success" for key in verdict["env"]}}
for result in ("success", "failure", "cancelled", "timed_out", "", "in_progress", "unknown"):
    ran = subprocess.run(["bash", "-c", verdict["run"]], env={**env, "FIRMWARE_BOUNDARY_SHARDS_RESULT": result, "FIRMWARE_BOUNDARY_RESULT": "success" if result == "success" else "skipped"}, capture_output=True, text=True)
    assert (ran.returncode == 0) == (result == "success")
    print(f"PASS required rtl-fast shell: shard result {result!r}, rc={ran.returncode}")
ran = subprocess.run(["bash", "-c", verdict["run"]], env={**env, "FIRMWARE_BOUNDARY_RESULT": "failure"}, capture_output=True)
assert ran.returncode != 0
print("PASS successful shards with failed judgement cannot pass required rtl-fast")

# Real small capture, copied using precisely the upload's three selected paths.
source = scratch / "sample.c"
source.write_text("int review_sample(void) { return 7; }\n")
original, downloaded = scratch / "capture", scratch / "downloaded"
for path in (original, downloaded):
    if path.exists():
        shutil.rmtree(path)
result = capture.run(original, ["gcc", "-c", str(source), "-o", str(scratch / "sample.o")], cwd=root, capture_output=True, text=True)
assert result.returncode == 0, result.stderr
downloaded.mkdir()
for name in ("records.jsonl", "manifest.jsonl"):
    shutil.copy2(original / name, downloaded / name)
shutil.copytree(original / "text", downloaded / "text")
a, b = capture.load(original), capture.load(downloaded)
assert a.commands == b.commands and a.invocations == b.invocations
assert runs.captures([downloaded], scratch, cfg.Scope(cfg.SHARD_SCOPE_WITHOUT))
print("PASS real compile capture survives records/manifest/text-only artifact roundtrip")
manifest = (downloaded / "manifest.jsonl").read_bytes()
bad = json.loads(manifest)
bad["rc"] = 1
(downloaded / "manifest.jsonl").write_text(json.dumps(bad) + "\n")
try:
    runs.captures([downloaded], scratch, cfg.Scope(cfg.SHARD_SCOPE_WITHOUT))
except runs.Refusal:
    print("PASS failed builder manifest refused")
else:
    raise AssertionError("failed manifest escaped")
(downloaded / "manifest.jsonl").write_bytes(manifest)
for name in ("records.jsonl", "manifest.jsonl", "text"):
    path = downloaded / name
    hidden = downloaded / (name + ".hidden")
    path.rename(hidden)
    try:
        try:
            capture.load(downloaded)
        except capture.CaptureError:
            print(f"PASS incomplete artifact without {name} refused")
        else:
            raise AssertionError(f"missing {name} escaped")
    finally:
        hidden.rename(path)
print("PASS all focused checks")
