# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_rv32.py - the store cross-compiled freestanding for RV32I, and its sizes.

The portable set (the codec and the store) and the LiteSPI port are compiled
with the pinned SDK's compiler for RV32I, freestanding, against MMIO stand-ins
for the LiteX-generated CSR and memory headers (test/rv32/) and the shape's
own generated/soc.h, which the bench writes from its config's system clock,
so each shape is built at the clock it ships. The arm fails on any undefined
symbol outside named memory interfaces and arithmetic helpers, so a heap
allocator, a stdio call or an OS service cannot enter the store; and it
reports the store's text, data and bss and each static buffer, which is the
size of the store as the shape fixes it. These are object sizes, not a
linked image; the maximum static frame is not a call-chain bound.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from nvm_bench import Refusal
import fw_rv32

RV32_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-Os", "-std=c11", "-ffreestanding",
              "-fno-stack-protector", "-fstack-usage", "-Wall", "-Wextra", "-Werror")
PORTABLE = ("nvm_klj2.c", "nvm_store.c", "plat/nvm_flash_litespi.c")
LIBC_OK = frozenset({"memcpy", "memset", "memmove", "memcmp"})
#: The store's static buffers and state, and the port's counters: its clock
#: and its per-call deadline.
BUFFERS = ("nvm_stage", "nvm_payload", "nvm_chunk", "nvm", "ls_ticks", "ls_tick_last",
           "ls_call_start", "ls_waited")
CLOCK = ("ls_ticks", "ls_tick_last", "ls_call_start", "ls_waited")


def compiler() -> str | None:
    """The explicit compiler, or the first available SDK candidate."""
    return fw_rv32.compiler()


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
    try:
        runtime_inc = fw_rv32.includes(cc)
    except ValueError as exc:
        raise Refusal(str(exc)) from exc
    objs = []
    for src in PORTABLE:
        obj = work / (Path(src).stem + ".o")
        r = subprocess.run([cc, *RV32_FLAGS, *runtime_inc, f"-I{gen}", f"-I{tree / 'test/rv32'}", "-c",
                            str(tree / src), "-o", str(obj)], capture_output=True, text=True,
                           check=False)
        if r.returncode:
            return [f"rv32: {src} does not build freestanding for RV32I:\n{r.stderr}"], {}
        objs.append(str(obj))
    undefined = {ln.split()[-1] for ln in _tool(cc, "nm", "-u", *objs).splitlines()
                 if ln.strip() and not ln.endswith(":")}
    defined = {ln.split()[-1] for ln in _tool(cc, "nm", "--extern-only", "--defined-only", *objs).splitlines()
               if ln.strip() and not ln.endswith(":")}
    stray = sorted(undefined - defined - LIBC_OK - fw_rv32.HELPERS)
    total = _tool(cc, "size", "-t", *objs).strip().splitlines()[-1].split()
    sizes = {"text": int(total[0]), "data": int(total[1]), "bss": int(total[2])}
    found = fw_rv32.object_findings(cc, [Path(obj) for obj in objs])
    try:
        sizes["stack_frame"] = fw_rv32.stack_frames([Path(obj) for obj in objs])
    except ValueError as exc:
        found.append(str(exc))
    for line in _tool(cc, "nm", "-S", "--defined-only", *objs).splitlines():
        parts = line.split()
        if len(parts) == 4 and parts[3] in BUFFERS:
            sizes[parts[3]] = int(parts[1], 16)
    if stray:
        found.append(f"rv32: symbols outside the C library and libgcc: {', '.join(stray)}")
    return found, sizes
