#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant header, ABI and runtime-dependency defects in RV32 object checks (#679)."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import fw_gtest
import fw_rv32

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "sw/firmware/ctrl/test"), str(ROOT / "sw/firmware/ctrl_nvm/test")]

import ctrl_arms  # noqa: E402
import nvm_bench  # noqa: E402
import nvm_rv32  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402


def header_and_abi_cases(cc: str, work: Path) -> int:
    """A hostile hosted include tree cannot affect the freestanding build."""
    poison = work / "sysroot/usr/include"
    poison.mkdir(parents=True)
    for header in ("stdint.h", "string.h", "stdio.h"):
        (poison / header).write_text('#error "hosted header reached"\n')
    source = work / "interfaces.c"
    source.write_text("""#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
_Static_assert(sizeof(uintptr_t) == 4, "RV32 pointers");
_Static_assert(sizeof(long) == 4, "ILP32 long");
_Static_assert(sizeof(uint64_t) == 8, "64-bit wire fields");
int format(char *dst, size_t n, const char *fmt, va_list ap) {
    memset(dst, 0, n);
    return vsnprintf(dst, n, fmt, ap);
}
""")
    flags = ["-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-fno-stack-protector",
             "-fstack-usage", "-Os", "-std=c11", "-Wall", "-Werror",
             f"--sysroot={work / 'sysroot'}"]
    obj = work / "interfaces.o"
    inc = fw_rv32.includes(cc)
    command = [cc, *flags, *inc, "-c", str(source), "-o", str(obj)]
    built = fw_gtest.run(command)
    assert built.returncode == 0, built.stderr
    assert not fw_rv32.object_findings(cc, [obj])
    assert fw_rv32.stack_frames([obj]) >= 0
    print("PASS: freestanding headers, ILP32 types, ELF ABI and static frame with hostile sysroot")
    for name, bad, reason in (
            ("hosted headers restored", [cc, *flags, "-c", str(source), "-o", str(obj)], "hosted header reached"),
            ("freestanding disabled", [x for x in command if x != "-ffreestanding"], "include_next")):
        result = fw_gtest.run(bad)
        assert result.returncode != 0 and reason in result.stderr, (name, result.stderr)
        print(f"PASS: caught {name}")
    source.write_text("int identity(int value) { return value; }\n")
    for name, arch, abi in (("RV64", "rv64i", "lp64"), ("hard-float", "rv32imafd", "ilp32d"),
                            ("compressed ISA", "rv32ic", "ilp32"), ("multiply ISA", "rv32im", "ilp32")):
        result = fw_gtest.run([cc, f"-march={arch}", f"-mabi={abi}", "-ffreestanding",
                               "-c", str(source), "-o", str(obj)])
        assert result.returncode == 0, result.stderr
        assert fw_rv32.object_findings(cc, [obj]), name
        print(f"PASS: caught {name} object")
    obj.write_bytes(b"not an ELF object")
    assert fw_rv32.object_findings(cc, [obj])
    obj.with_suffix(".su").write_text("probe.c:1:1:probe\t16\tdynamic\n")
    try:
        fw_rv32.stack_frames([obj])
    except ValueError as exc:
        assert "non-static stack usage" in str(exc)
    else:
        raise AssertionError("dynamic stack report was accepted")
    print("PASS: caught malformed object and dynamic stack report")
    return 9


def runtime_cases(cc: str, work: Path) -> int:
    """Real firmware arms must reject heap and unrecognised __ dependencies."""
    import shutil

    ctrl = work / "ctrl"
    shutil.copytree(CTRL, ctrl)
    tree = Tree(ctrl, work / "ctrl-build", work / "reuse")
    with patch.dict(os.environ, MILAN_RV32_CC=cc):
        assert ctrl_arms.arm_rv32(tree, True).rc == 0
        source = ctrl / "port/shlan_port.c"
        original = source.read_text()
        for symbol in ("malloc", "__unexpected_service"):
            source.write_text(f"extern void *{symbol}(__SIZE_TYPE__);\n" + original.replace(
                "return ctrl_pool_alloc(port_pool, size);", f"return {symbol}(size);"))
            got = ctrl_arms.arm_rv32(tree, True)
            assert got.rc and "symbols outside the C library" in got.log and symbol in got.log, got.log
            print(f"PASS: ctrl rejects {symbol}")
        source.write_text(original)
    cfg = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    inputs = nvm_bench.shape_inputs(cfg, work / "inputs")
    gen = work / "gen"
    nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
    nvm = work / "nvm"
    shutil.copytree(nvm_bench.TREE, nvm)
    findings, _ = nvm_rv32.build(nvm, work / "nvm-build", gen, cc)
    assert not findings, findings
    source = nvm / "nvm_klj2.c"
    original = source.read_text()
    for symbol in ("malloc", "__unexpected_service"):
        source.write_text(original + f"\nextern void *{symbol}(__SIZE_TYPE__);\n"
                          f"void *runtime_probe(void) {{ return {symbol}(16); }}\n")
        findings, _ = nvm_rv32.build(nvm, work / "nvm-build", gen, cc)
        assert any("symbols outside the C library" in f and symbol in f for f in findings), findings
        print(f"PASS: ctrl_nvm rejects {symbol}")
    source.write_text(original + """
extern void use_buffer(char *);
void stack_probe(void) { char bytes[64]; use_buffer(bytes); }
""")
    with patch.object(nvm_rv32, "RV32_FLAGS", (*nvm_rv32.RV32_FLAGS, "-fstack-protector-all")):
        findings, _ = nvm_rv32.build(nvm, work / "nvm-build", gen, cc)
    assert any("__stack_chk_fail" in f for f in findings), findings
    print("PASS: ctrl_nvm rejects restored stack-protector dependency")
    return 5


def main() -> int:
    """Compile positive controls and require every planted defect caught."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-rv32", action="store_true")
    args = parser.parse_args()
    cc = fw_rv32.compiler()
    if cc is None:
        print("REFUSED: no RV32 compiler" if args.require_rv32 else "SKIPPED: no RV32 compiler")
        return 2 if args.require_rv32 else 0
    with tempfile.TemporaryDirectory(prefix="fw-rv32-") as tmp:
        work = Path(tmp)
        with patch.dict(os.environ, MILAN_RV32_CC=str(work / "absent-compiler")):
            assert fw_rv32.compiler() is None, "explicit absent compiler fell back"
            try:
                ctrl_arms.arm_rv32(Tree(CTRL, work, work), True)
            except ctrl_arms.Refusal:
                pass
            else:
                raise AssertionError("required ctrl compiler was skipped")
        print("PASS: explicit absent compiler is refused without fallback")
        checks = 1 + header_and_abi_cases(cc, work) + runtime_cases(cc, work)
    print(f"RV32 build self-test: {checks} checks PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
