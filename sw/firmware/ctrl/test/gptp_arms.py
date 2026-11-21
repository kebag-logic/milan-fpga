# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gptp_arms.py - the firmware gPTP end station port's arms of the control firmware gate (#665 F6, #884).

  gptp       the port (gptp/gptp.c) on the host: its GoogleTest suite (test_gptp.cpp), scripted frames and a
             two-port network over simulated PHCs, each test naming its IEEE 802.1AS-2020 or Milan v1.2 clause;
  gptp_rv32  the same source built freestanding for the split placement's RV32IM hart with the image's flags:
             no float, no libm, nothing open but the C library's memory functions and libgcc's helpers, and its
             size, which the memory plan reads.
"""

from __future__ import annotations

from pathlib import Path

from ctrl_arms import rv32_compiler, symbols
from ctrl_build import (RV32_LIBC, SPLIT_RV32_FLAGS, Outcome, Refusal, Tree, compile_c, compile_tests, execute,
                        link, run, sources)
import fw_rv32

#: The port's source and its test, inside the ctrl tree.
SOURCES = ("gptp/gptp.c",)
TESTS = ("test_gptp.cpp",)
#: The tally label test_gptp.cpp names (FW_TALLY_LABEL).
LABEL = "ctrl gPTP end station port (host)"
#: Soft-float and libm symbols: the port must reference none (the split hart has no FPU).
FLOAT_SYMBOLS = ("__adddf3", "__subdf3", "__muldf3", "__divdf3", "__addsf3", "__mulsf3", "__divsf3",
                 "__fixdfdi", "__floatdidf", "__extendsfdf2", "__truncdfsf2", "exp", "log2", "llround")


def include(tree: Tree) -> tuple[str, ...]:
    """The port's include directory, for the host and the RV32 builds."""
    return (f"-I{tree.src / 'gptp'}",)


def arm_gptp(tree: Tree) -> Outcome:
    """The port's GoogleTest suite on the host."""
    objs = compile_c(tree, sources(tree, SOURCES), "gptp", include(tree))
    tests = compile_tests(tree, TESTS, "gptp/tests", include(tree))
    return execute("gptp", link(tree, "test_gptp", objs + tests))


def arm_gptp_rv32(tree: Tree, require: bool) -> Outcome:
    """The port for the split hart (RV32IM, the image's flags): only memory functions and libgcc helpers open."""
    cc = rv32_compiler()
    if cc is None:
        if require:
            raise Refusal("no RV32 compiler (the pinned SDK's riscv32-linux-gcc or a bare-metal one)")
        return Outcome("gptp_rv32", 0, "  SKIPPED: no RV32 compiler; --require-rv32 refuses instead")
    obj_dir = tree.out / "gptp_rv32"
    obj_dir.mkdir(parents=True, exist_ok=True)
    try:
        runtime_inc = fw_rv32.includes(cc)
    except ValueError as exc:
        raise Refusal(str(exc)) from exc
    objs: list[Path] = []
    for src in sources(tree, SOURCES):
        obj = obj_dir / f"{src.stem}.o"
        res = run([cc, *SPLIT_RV32_FLAGS, *runtime_inc, *include(tree), "-c", str(src), "-o", str(obj)])
        if res.returncode != 0:
            return Outcome("gptp_rv32", 1, f"  [FAIL] {src.name} does not build for RV32IM:\n{res.stderr}")
        objs.append(obj)
    tool = cc.removesuffix("gcc")
    open_syms = symbols(tool + "nm", objs, True)
    stray = sorted(open_syms - RV32_LIBC - {"memcmp"} - fw_rv32.HELPERS)
    floats = sorted(open_syms & set(FLOAT_SYMBOLS))
    # the split image's own rule (ctrl_srp_image.py's object audit): RV32M makes the 32-bit helpers and the 64-bit
    # multiply instructions, so an object for the split hart calls no multiply or divide helper (#665)
    muldiv = sorted(open_syms & fw_rv32.MULDIV_HELPERS)
    findings = fw_rv32.object_findings(cc, objs, "rv32im")
    size = run([tool + "size", "-t", *map(str, objs)])
    if size.returncode:
        raise Refusal(f"RV32 size failed: {size.stderr.strip()}")
    total = size.stdout.strip().splitlines()[-1].split()[:4]
    lines = [f"  {cc.rsplit('/', 1)[-1]} {' '.join(SPLIT_RV32_FLAGS[:4])}: {len(objs)} object(s)",
             f"  size (text data bss dec): {' '.join(total)}",
             f"  undefined: {', '.join(sorted(open_syms))}"]
    failed = 0
    for what, names in (("soft-float or libm", floats), ("other runtime", stray),
                        ("software multiply or divide", muldiv)):
        if names:
            failed = 1
            lines.append(f"  [FAIL] GptpRv32.NoStrayRuntime: the port references {what} symbols: {', '.join(names)}")
    for finding in findings:
        failed = 1
        lines.append(f"  [FAIL] GptpRv32.ObjectChecks: {finding}")
    checks = 4
    lines.append(f"== {LABEL}, RV32IM objects: checks: {checks}   failures: {failed} ==")
    return Outcome("gptp_rv32", failed, "\n".join(lines))


def all_arms(tree: Tree, require_rv32: bool = False) -> list[Outcome]:
    """Both arms; require_rv32 refuses a tree with no RV32 compiler instead of skipping its arm."""
    return [arm_gptp(tree), arm_gptp_rv32(tree, require_rv32)]
