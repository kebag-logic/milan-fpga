# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_rv32.py - the store cross-compiled freestanding for RV32I, and its sizes.

The portable set (the codec and the store) and the LiteSPI port are compiled
with the pinned SDK's compiler for RV32I, freestanding, against MMIO stand-ins
for the LiteX-generated CSR and memory headers (test/rv32/) and the shape's
own generated/soc.h, which the bench writes from its config's system clock,
so each shape is built at the clock it ships. The arm fails on any undefined
symbol that is not a C-library memory function or a libgcc helper, so a heap
allocator, a stdio call or an OS service cannot enter the store; and it
reports the store's text, data and bss and each static buffer, which is the
size of the store as the shape fixes it.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from nvm_bench import Refusal

RV32_CANDIDATES = (str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"),
                   "riscv32-linux-gcc", "riscv32-unknown-elf-gcc", "riscv64-unknown-elf-gcc")
RV32_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-Os", "-std=c11", "-ffreestanding",
              "-Wall", "-Wextra", "-Werror")
PORTABLE = ("nvm_klj2.c", "nvm_store.c", "plat/nvm_flash_litespi.c")
LIBC_OK = frozenset({"memcpy", "memset", "memmove", "memcmp"})
#: The store's static buffers and state, and the port's counters: its clock
#: and its per-call deadline.
BUFFERS = ("nvm_stage", "nvm_payload", "nvm_chunk", "nvm", "ls_ticks", "ls_tick_last",
           "ls_call_start", "ls_waited")
CLOCK = ("ls_ticks", "ls_tick_last", "ls_call_start", "ls_waited")


def compiler() -> str | None:
    """The first RV32 compiler present, the pinned SDK's first."""
    for cand in RV32_CANDIDATES:
        found = shutil.which(cand)
        if found is not None:
            return found
    return None


def _tool(cc: str, name: str, *args: str) -> str:
    """Run a binutils tool of the same toolchain; its output."""
    r = subprocess.run([cc.removesuffix("gcc") + name, *args], capture_output=True, text=True,
                       check=False)
    if r.returncode:
        raise Refusal(f"{name}: {r.stderr.strip()}")
    return r.stdout


def build(tree: Path, work: Path, gen: Path, cc: str) -> tuple[list[str], dict[str, int]]:
    """Compile the portable set for RV32I into `work`: (findings, sizes)."""
    work.mkdir(parents=True, exist_ok=True)
    objs = []
    for src in PORTABLE:
        obj = work / (Path(src).stem + ".o")
        r = subprocess.run([cc, *RV32_FLAGS, f"-I{gen}", f"-I{tree / 'test/rv32'}", "-c",
                            str(tree / src), "-o", str(obj)], capture_output=True, text=True,
                           check=False)
        if r.returncode:
            return [f"rv32: {src} does not build freestanding for RV32I:\n{r.stderr}"], {}
        objs.append(str(obj))
    undefined = {ln.split()[-1] for ln in _tool(cc, "nm", "-u", *objs).splitlines()
                 if ln.strip() and not ln.endswith(":")}
    defined = {ln.split()[-1] for ln in _tool(cc, "nm", "--defined-only", *objs).splitlines()
               if ln.strip() and not ln.endswith(":")}
    stray = sorted(s for s in undefined - defined if s not in LIBC_OK and not s.startswith("__"))
    total = _tool(cc, "size", "-t", *objs).strip().splitlines()[-1].split()
    sizes = {"text": int(total[0]), "data": int(total[1]), "bss": int(total[2])}
    for line in _tool(cc, "nm", "-S", "--defined-only", *objs).splitlines():
        parts = line.split()
        if len(parts) == 4 and parts[3] in BUFFERS:
            sizes[parts[3]] = int(parts[1], 16)
    found = [f"rv32: symbols outside the C library and libgcc: {', '.join(stray)}"] if stray else []
    return found, sizes
