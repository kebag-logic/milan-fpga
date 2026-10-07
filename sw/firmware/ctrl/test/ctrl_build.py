# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_build.py - the build helpers of the control-plane firmware's host test.

The firmware is compiled from a Tree: the checkout, or a copy a planted defect
was written into (ctrl_mutants.py), with every object and executable under the
tree's own output directory, never in the checkout. The tests are GoogleTest
(sw/firmware/gtest/README.md): always compiled from the checkout's test
sources against the tree's headers, so a defect planted in a .c file reuses
every test object and one planted in a header rebuilds the tests that see it.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
CTRL = HERE.parent
ROOT = CTRL.parents[2]
HARNESS = ROOT / "sw/firmware/gtest"
sys.path.insert(0, str(HARNESS))

import fw_gtest  # noqa: E402

PP = ROOT / "protocol-processor"
PP_ADP_SIM = "tb/adp_engine/sim_main.cpp"
PP_ADP_PKG = PP / "hdl/adp/pp_adp_pkg.sv"
TB_MBX = ROOT / "tb/verilator/mbx"
TB_COMMON = ROOT / "tb/common"

#: The firmware every target links: the driver, the loop, the port layer, ADP, the app.
PORTABLE = ("mbx/mbx.c", "loop/ctrl_loop.c", "port/ctrl_pool.c", "port/ctrl_debug.c", "port/shlan_port.c",
            "adp/adp.c", "adp/adp_mbx.c", "app/ctrl_app.c")
#: The host side: the model and mbx_hal.h on it. Test equipment, never measured.
HOST = ("host/mbx_model.c", "host/mbx_plat_host.c")
INCLUDE_DIRS = ("mbx", "wire", "host", "port", "loop", "adp", "app", "test")
C_FLAGS = ("-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic")

RV32_CANDIDATES = (str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"), "riscv32-unknown-elf-gcc",
                   "riscv64-elf-gcc")
RV32_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-fno-stack-protector", "-fstack-usage",
              "-Os", "-std=c11", "-Wall",
              "-Wextra", "-Werror", "-pedantic", "-DCTRL_MBX_BASE=0x80000000u")
#: What a freestanding RV32I build may leave undefined, besides libgcc's `__` helpers.
RV32_LIBC = frozenset({"memset", "memcpy", "vsnprintf"})


class Refusal(Exception):
    """The gate cannot run as asked; exit 2, never a pass."""


@dataclass(frozen=True)
class Tree:
    """Where the firmware sources come from and where its builds go."""

    src: Path
    out: Path
    reuse: Path
    build: fw_gtest.Build = field(default_factory=fw_gtest.Build)


@dataclass(frozen=True)
class Outcome:
    """One arm's verdict and its output."""

    arm: str
    rc: int
    log: str


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One subprocess, its output captured."""
    return fw_gtest.run(argv, cwd=cwd)


def includes(tree: Tree) -> list[str]:
    """The firmware's include path, from the tree being built, then the harness."""
    return [f"-I{tree.src / d}" for d in INCLUDE_DIRS] + [f"-I{HARNESS}"]


def compile_c(tree: Tree, sources: list[Path], tag: str, extra: tuple[str, ...] = (),
              measured: bool = True) -> list[Path]:
    """Compile C sources to objects under out/<tag>; a compile error refuses the arm."""
    try:
        return fw_gtest.compile_c(tree.build, C_FLAGS, [*includes(tree), *extra], sources, tree.out / tag, measured)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def firmware(tree: Tree, names: tuple[str, ...], tag: str) -> list[Path]:
    """The firmware sources `names` (measured) and the host model (not) as objects."""
    return (compile_c(tree, sources(tree, names), tag) +
            compile_c(tree, sources(tree, HOST), f"{tag}/host", measured=False))


def compile_tests(tree: Tree, names: tuple[str, ...], tag: str, extra: tuple[str, ...] = ()) -> list[Path]:
    """The GoogleTest sources `names` (from the checkout's test/) against the tree's headers."""
    try:
        return fw_gtest.compile_tests(tree.build, [*includes(tree), *extra], [HERE / n for n in names],
                                      tree.out / tag)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def link(tree: Tree, name: str, objects: list[Path]) -> Path:
    """Link objects with the harness's main into out/<name>."""
    try:
        main = fw_gtest.main_object(tree.build, tree.out / "harness")
        return fw_gtest.link(tree.build, [*objects, main], tree.out / name)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def execute(arm: str, exe: Path) -> Outcome:
    """Run one test binary and grade it as the sweep grades a suite log."""
    ok, log = fw_gtest.run_binary(exe)
    return Outcome(arm, 0 if ok else 1, log)


def sources(tree: Tree, names: tuple[str, ...]) -> list[Path]:
    """Paths of firmware sources inside the tree."""
    return [tree.src / n for n in names]
