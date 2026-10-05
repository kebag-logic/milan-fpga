# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_build.py - the build helpers of the control-plane firmware's host test.

The firmware is compiled from a Tree: the checkout, or a copy a planted defect
was written into (ctrl_mutants.py), with every object and executable under the
tree's own output directory, never in the checkout.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
CTRL = HERE.parent
ROOT = CTRL.parents[2]
PP = ROOT / "protocol-processor"
PP_ADP_SIM = "tb/adp_engine/sim_main.cpp"
PP_ADP_PKG = PP / "hdl/adp/pp_adp_pkg.sv"
TB_MBX = ROOT / "tb/verilator/mbx"
TB_COMMON = ROOT / "tb/common"

#: The firmware every target links: the driver, the loop, the port layer, ADP, the app.
PORTABLE = ("mbx/mbx.c", "loop/ctrl_loop.c", "port/ctrl_pool.c", "port/ctrl_debug.c", "port/shlan_port.c",
            "adp/adp.c", "adp/adp_mbx.c", "app/ctrl_app.c")
#: The host side: the model, its mbx_hal.h, the checks.
HOST = ("host/mbx_model.c", "host/mbx_plat_host.c", "test/test_check.c")
INCLUDE_DIRS = ("mbx", "wire", "host", "port", "loop", "adp", "app", "test")
C_FLAGS = ("-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic")
CXX_FLAGS = ("-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror")

RV32_CANDIDATES = (str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"), "riscv32-unknown-elf-gcc",
                   "riscv64-elf-gcc")
RV32_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-fno-stack-protector", "-Os", "-std=c11", "-Wall",
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


@dataclass(frozen=True)
class Outcome:
    """One arm's verdict and its output."""

    arm: str
    rc: int
    log: str


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One subprocess, its output captured."""
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)


def includes(tree: Tree) -> list[str]:
    """The firmware's include path, from the tree being built."""
    return [f"-I{tree.src / d}" for d in INCLUDE_DIRS]


def compile_c(tree: Tree, sources: list[Path], tag: str, extra: tuple[str, ...] = ()) -> list[Path]:
    """Compile C sources to objects under out/<tag>; a compile error refuses the arm."""
    obj_dir = tree.out / tag
    obj_dir.mkdir(parents=True, exist_ok=True)
    objects = []
    for src in sources:
        obj = obj_dir / f"{src.parent.name}_{src.stem}.o"
        res = run([os.environ.get("CC", "gcc"), *C_FLAGS, *includes(tree), *extra, "-c", str(src), "-o", str(obj)])
        if res.returncode != 0:
            raise Refusal(f"{src.name} does not compile:\n{res.stderr}")
        objects.append(obj)
    return objects


def link(tree: Tree, name: str, objects: list[Path], cxx_main: Path | None = None,
         extra: tuple[str, ...] = ()) -> Path:
    """Link objects (and a C++ main) into out/<name>."""
    exe = tree.out / name
    if cxx_main is None:
        argv = [os.environ.get("CC", "gcc"), *map(str, objects), "-o", str(exe)]
    else:
        argv = [os.environ.get("CXX", "g++"), *CXX_FLAGS, *includes(tree), f"-I{TB_COMMON}", f"-I{TB_MBX}", *extra,
                str(cxx_main), *map(str, objects), "-o", str(exe)]
    res = run(argv)
    if res.returncode != 0:
        raise Refusal(f"{name} does not link:\n{res.stderr}")
    return exe


def execute(arm: str, exe: Path) -> Outcome:
    """Run one test binary."""
    res = run([str(exe)])
    return Outcome(arm, res.returncode, res.stdout + res.stderr)


def sources(tree: Tree, names: tuple[str, ...]) -> list[Path]:
    """Paths of firmware sources inside the tree."""
    return [tree.src / n for n in names]
