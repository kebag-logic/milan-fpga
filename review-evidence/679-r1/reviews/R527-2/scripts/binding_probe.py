#!/usr/bin/env python3
"""Compiled cross-object binding controls for both real RV32 arms.

Usage: python3 binding_probe.py CHECKOUT PACKET
Every plant and object lives under PACKET/scratch/binding-probe.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.path[:0] = [str(root / path) for path in
               ("sw/firmware/gtest", "sw/firmware/ctrl/test", "sw/firmware/ctrl_nvm/test")]
import ctrl_arms
from ctrl_build import CTRL, Tree
import nvm_bench
import nvm_rv32

cc = str(packet / "scratch/sdk/bin/riscv32-linux-gcc")
os.environ["MILAN_RV32_CC"] = cc
work = packet / "scratch/binding-probe"
work.mkdir(parents=True, exist_ok=True)
symbol = "__r527_runtime_dependency"

def tool(name, *args):
    result = subprocess.run([cc.removesuffix("gcc") + name, *map(str, args)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    return result.stdout

inputs = nvm_bench.shape_inputs(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
gen = work / "gen"
nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)

for arm in ("ctrl", "nvm"):
    original = CTRL if arm == "ctrl" else nvm_bench.TREE
    copy = work / arm
    shutil.copytree(original, copy, dirs_exist_ok=True)
    callfile = copy / ("port/shlan_port.c" if arm == "ctrl" else "nvm_klj2.c")
    deffile = copy / ("port/ctrl_debug.c" if arm == "ctrl" else "nvm_store.c")
    call_original, def_original = callfile.read_text(), deffile.read_text()
    for binding in ("none", "t", "d", "b", "r", "T", "W"):
        if binding in ("d", "b", "r"):
            caller = f"\nextern const int {symbol};\nint r527_probe(void) {{ return {symbol}; }}\n"
            definition = {"d": f"static int {symbol} = 7;", "b": f"static int {symbol};",
                          "r": f"static const int {symbol} = 7;"}[binding]
        else:
            caller = f"\nextern int {symbol}(void);\nint r527_probe(void) {{ return {symbol}(); }}\n"
            prefix = "static " if binding == "t" else "__attribute__((weak)) " if binding == "W" else ""
            definition = f"{prefix}int {symbol}(void) {{ return 7; }}"
        callfile.write_text(call_original + caller)
        deffile.write_text(def_original + ("\n__attribute__((used)) " + definition + "\n" if binding != "none" else ""))
        out = work / (arm + "-" + binding)
        if arm == "ctrl":
            got = ctrl_arms.arm_rv32(Tree(copy, out, work / "reuse"), True)
            rc, diagnostic = got.rc, got.log
            objects = sorted((out / "rv32").glob("*.o"))
        else:
            found, sizes = nvm_rv32.build(copy, out, gen, cc)
            rc, diagnostic = bool(found), "\n".join(found)
            objects = sorted(out.glob("*.o"))
        assert len(objects) == (9 if arm == "ctrl" else 3), (arm, binding, diagnostic)
        symbols = [line for line in tool("nm", *objects).splitlines() if line.split() and line.split()[-1] == symbol]
        types = [line.split()[-2] for line in symbols]
        assert "U" in types and (binding == "none" or binding in types), (arm, binding, symbols)
        merged = work / f"{arm}-{binding}-partial.o"
        tool("ld", "-r", "-o", merged, *objects)
        unresolved = symbol in tool("nm", "-u", merged)
        if binding in ("T", "W"):
            assert not rc and not unresolved, (arm, binding, diagnostic)
        else:
            assert rc and "symbols outside the C library" in diagnostic and symbol in diagnostic, diagnostic
            assert "does not build" not in diagnostic and unresolved, diagnostic
        print(f"PASS {arm} binding={binding} nm_types={types} partial_link=0 unresolved={unresolved} arm_rc={int(rc)}")
        for line in diagnostic.splitlines():
            if "symbols outside the C library" in line:
                print(line)
    callfile.write_text(call_original)
    deffile.write_text(def_original)
print("PASS: 14 compiled binding controls; local t/d/b/r stay unresolved; global T and weak W resolve")
