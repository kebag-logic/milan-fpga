"""Reproduce the public runtime-binding probe plus global/weak positives.

Usage: python3 runtime-binding-probe.py CHECKOUT PACKET
All source changes are confined to disposable scratch copies.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:])
sys.path[:0] = [str(root / p) for p in ("sw/firmware/ctrl/test",
                 "sw/firmware/ctrl_nvm/test", "sw/firmware/gtest")]
import ctrl_arms
from ctrl_build import CTRL, Tree
import nvm_bench
import nvm_rv32
import fw_rv32_selftest

work = packet / "scratch/binding"
work.mkdir()
cc = str(packet / "scratch/sdk/bin/riscv32-linux-gcc")
os.environ["MILAN_RV32_CC"] = cc
prefix = cc.removesuffix("gcc")
symbol = "__review_runtime_service"
definition = f"void *{symbol}(__SIZE_TYPE__ n) {{ (void)n; return (void *)0; }}\n"
call = f"\nextern void *{symbol}(__SIZE_TYPE__);\nvoid *review_call(void) {{ return {symbol}(16); }}\n"
records = []


def command(args):
    result = subprocess.run(args, text=True, capture_output=True, check=False)
    assert result.returncode == 0, (args, result.returncode, result.stderr)
    return result.stdout


for arm in ("ctrl", "nvm"):
    src = work / arm
    out = work / (arm + "-out")
    shutil.copytree(CTRL if arm == "ctrl" else nvm_bench.TREE, src)
    if arm == "ctrl":
        caller, private = src / "port/shlan_port.c", src / "port/ctrl_debug.c"
    else:
        caller, private = src / "nvm_klj2.c", src / "nvm_store.c"
        inputs = nvm_bench.shape_inputs(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
        gen = work / "gen"
        nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
    original_caller, original_private = caller.read_text(), private.read_text()
    for kind, decl, expected_type in (("baseline", "", None), ("unresolved", "", "U"),
                ("local", "__attribute__((used)) static " + definition, "t"),
                ("global", definition, "T"), ("weak", "__attribute__((weak)) " + definition, "W")):
        caller.write_text(original_caller + ("" if kind == "baseline" else call))
        private.write_text(original_private + "\n" + decl)
        if arm == "ctrl":
            result = ctrl_arms.arm_rv32(Tree(src, out, work / "reuse"), True)
            findings = [line.strip() for line in result.log.splitlines() if "[FAIL]" in line]
            rc = result.rc
            objects = sorted((out / "rv32").glob("*.o"))
        else:
            findings, sizes = nvm_rv32.build(src, out, gen, cc)
            rc = int(bool(findings))
            objects = sorted(out.glob("*.o"))
        print(arm, kind, "rc", rc, "findings", findings, flush=True)
        reject = kind in ("unresolved", "local")
        assert bool(rc) == reject, (arm, kind, findings)
        if reject:
            assert len(findings) == 1 and "symbols outside the C library" in findings[0] and symbol in findings[0]
        names = command([prefix + "nm", *map(str, objects)])
        relevant = [line for line in names.splitlines() if line.split() and line.split()[-1] == symbol]
        if expected_type:
            assert expected_type in [line.split()[-2] for line in relevant], relevant
        linked = work / f"{arm}-{kind}.o"
        command([prefix + "ld", "-m", "elf32lriscv", "-r", *map(str, objects), "-o", str(linked)])
        undefined = command([prefix + "nm", "-u", str(linked)])
        remains = symbol in {line.split()[-1] for line in undefined.splitlines() if line.split()}
        assert remains == reject
        record = {"arm": arm, "case": kind, "gate_rc": rc, "findings": findings,
                  "symbols": relevant, "partial_link_rc": 0, "still_undefined": remains}
        print(json.dumps(record), flush=True)
        records.append(record)

# Independently remove each changed binding restriction in memory. The newly
# committed control must fail at its runtime diagnostic assertion, not setup.
for arm in ("ctrl", "nvm"):
    target = work / ("control-mutation-" + arm)
    target.mkdir()
    if arm == "ctrl":
        original = ctrl_arms.run
        def unfiltered(argv, **kwargs):
            return original([arg for arg in argv if arg != "--extern-only"], **kwargs)
        context = patch.object(ctrl_arms, "run", unfiltered)
    else:
        original = nvm_rv32._tool
        def unfiltered(compiler, name, *args):
            return original(compiler, name, *(arg for arg in args if arg != "--extern-only"))
        context = patch.object(nvm_rv32, "_tool", unfiltered)
    with context:
        try:
            fw_rv32_selftest.runtime_cases(cc, target)
        except AssertionError as exc:
            import traceback
            frames = traceback.extract_tb(exc.__traceback__)
            matching = [f for f in frames if Path(f.filename).name == "fw_rv32_selftest.py"]
            assert matching and "symbols outside the C library" in (matching[-1].line or ""), frames
            print(f"PASS: removing {arm} external filtering breaks its new runtime control at line {matching[-1].lineno}", flush=True)
            records.append({"arm": arm, "control_mutation": "caught", "assertion_line": matching[-1].lineno})
        else:
            raise AssertionError(f"{arm} binding restriction mutation escaped")
(packet / "receipts/runtime-binding-result.json").write_text(json.dumps(records, indent=2) + "\n")
print("Binding probe: both masked cases rejected for the dependency; global/weak positives pass; both controls kill filter removal")
