"""Additional same-name local b/d/r controls through both real firmware arms."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:])
sys.path[:0] = [str(root / p) for p in ("sw/firmware/ctrl/test", "sw/firmware/ctrl_nvm/test", "sw/firmware/gtest")]
import ctrl_arms
from ctrl_build import CTRL, Tree
import nvm_bench
import nvm_rv32

work = packet / "scratch/local-data"
work.mkdir()
cc = str(packet / "scratch/sdk/bin/riscv32-linux-gcc")
os.environ["MILAN_RV32_CC"] = cc
prefix = cc.removesuffix("gcc")
symbol = "__review_runtime_service"
call = f"\nextern void *{symbol}(__SIZE_TYPE__);\nvoid *review_call(void) {{ return {symbol}(16); }}\n"
for arm in ("ctrl", "nvm"):
    src, out = work / arm, work / (arm + "-out")
    shutil.copytree(CTRL if arm == "ctrl" else nvm_bench.TREE, src)
    if arm == "ctrl":
        caller, private = src / "port/shlan_port.c", src / "port/ctrl_debug.c"
    else:
        caller, private = src / "nvm_klj2.c", src / "nvm_store.c"
        inputs = nvm_bench.shape_inputs(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
        gen = work / "gen"
        nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
    caller.write_text(caller.read_text() + call)
    original = private.read_text()
    for kind, decl in (("b", f"static int {symbol} __attribute__((used));"),
                       ("d", f"static int {symbol} __attribute__((used)) = 1;"),
                       ("r", f"static const int {symbol} __attribute__((used)) = 1;")):
        private.write_text(original + "\n" + decl + "\n")
        if arm == "ctrl":
            result = ctrl_arms.arm_rv32(Tree(src, out, work / "reuse"), True)
            findings = [x for x in result.log.splitlines() if "[FAIL]" in x]
            assert result.rc == 1
            objects = sorted((out / "rv32").glob("*.o"))
        else:
            findings, _ = nvm_rv32.build(src, out, gen, cc)
            objects = sorted(out.glob("*.o"))
        assert len(findings) == 1 and "symbols outside the C library" in findings[0] and symbol in findings[0], findings
        names = subprocess.check_output([prefix + "nm", *map(str, objects)], text=True)
        rows = [x for x in names.splitlines() if x.split() and x.split()[-1] == symbol]
        assert {x.split()[-2] for x in rows} == {kind, "U"}, rows
        linked = work / f"{arm}-{kind}.o"
        subprocess.run([prefix + "ld", "-m", "elf32lriscv", "-r", *map(str, objects), "-o", str(linked)], check=True)
        undefined = subprocess.check_output([prefix + "nm", "-u", str(linked)], text=True)
        assert symbol in {x.split()[-1] for x in undefined.splitlines() if x.split()}
        print(json.dumps({"arm": arm, "local_binding": kind, "symbols": rows, "findings": findings,
                          "partial_link_rc": 0, "still_undefined": True}), flush=True)
print("PASS: all six local b/d/r cases rejected for the dependency, with successful partial links")
