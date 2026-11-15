# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Shared freestanding RV32I and RV32IM object checks, without the SDK's hosted libc.

GCC supplies stdint/stddef/stdarg/stdbool under -ffreestanding. The
rv32_include headers declare the bare-metal runtime interfaces consumed by
the firmware. These checks compile objects, not a linked or bootable image.
"""

from __future__ import annotations

import os
import re
import shutil
import struct
from pathlib import Path

import fw_gtest

HERE = Path(__file__).resolve().parent
CANDIDATES = (str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"),
              "riscv32-linux-gcc", "riscv32-unknown-elf-gcc",
              "riscv64-unknown-elf-gcc", "riscv64-elf-gcc")
# Exact compiler arithmetic helpers, never an unrestricted double-underscore prefix.
HELPERS = frozenset({"__lshrdi3", "__ashldi3", "__ashrdi3", "__mulsi3", "__muldi3",
                     "__divsi3", "__udivsi3", "__modsi3", "__umodsi3",
                     "__divdi3", "__udivdi3", "__moddi3", "__umoddi3"})
#: Each ISA an object may be built for, as its name and its architecture attribute: RV32I, and
#: RV32IM for the split placement's hart (#665, owner decision 2026-10-27; NFR-SCOUT-01), whose
#: M implies Zmmul in the attribute.
ARCH = {"rv32i": ("RV32I", r"rv32i\d+p\d+"),
        "rv32im": ("RV32IM", r"rv32i\d+p\d+_m\d+p\d+_zmmul\d+p\d+")}
#: The multiply and divide helpers among HELPERS. RV32M makes the 32-bit ones and the 64-bit
#: multiply instructions, so no object built for the split placement's RV32IM hart calls them
#: (#665); a 64-bit divide still would, and stay a software loop on its path.
MULDIV_HELPERS = HELPERS - {"__lshrdi3", "__ashldi3", "__ashrdi3"}


def compiler() -> str | None:
    """Use an explicit compiler when requested; otherwise prefer the CI SDK."""
    requested = os.environ.get("MILAN_RV32_CC")
    choices = (requested,) if requested else CANDIDATES
    return next((found for name in choices if (found := shutil.which(name))), None)


def includes(cc: str) -> list[str]:
    """Exclude all hosted headers, retaining GCC's freestanding C headers."""
    result = fw_gtest.run([cc, "-print-file-name=include"])
    directory = Path(result.stdout.strip())
    if result.returncode or not directory.is_dir() or not (directory / "stdint.h").is_file():
        raise ValueError("RV32 compiler did not identify its freestanding headers")
    return ["-nostdinc", "-isystem", str(directory), "-I", str(HERE / "rv32_include")]


def object_findings(cc: str, objects: list[Path], isa: str = "rv32i") -> list[str]:
    """Every emitted object must use little-endian ELF32 RISC-V soft-float ABI, built for exactly `isa`."""
    name, attribute = ARCH[isa]
    found = []
    for obj in objects:
        data = obj.read_bytes()
        if (len(data) < 52 or data[:7] != b"\x7fELF\x01\x01\x01" or
                struct.unpack_from("<HH", data, 16) != (1, 243) or
                struct.unpack_from("<I", data, 36)[0] != 0):
            found.append(f"{obj.name}: expected {name} ILP32 relocatable object")
            continue
        attributes = fw_gtest.run([cc.removesuffix("gcc") + "readelf", "-A", str(obj)])
        arches = re.findall(r'Tag_RISCV_arch: "([^"]+)"', attributes.stdout)
        if attributes.returncode or len(arches) != 1 or not re.fullmatch(attribute, arches[0]):
            found.append(f"{obj.name}: expected {name} architecture attribute, got {arches}")
    return found


def muldiv_findings(cc: str, objects: list[Path]) -> list[str]:
    """Every object that calls a software multiply or divide helper (MULDIV_HELPERS), with the helpers it calls."""
    found = []
    for obj in objects:
        result = fw_gtest.run([cc.removesuffix("gcc") + "nm", "-u", str(obj)])
        called = sorted(MULDIV_HELPERS & {line.split()[-1] for line in result.stdout.splitlines() if line.strip()})
        if result.returncode or called:
            found.append(f"{obj.name}: calls software multiply or divide {called or result.stderr.strip()}")
    return found


def stack_frames(objects: list[Path]) -> int:
    """Largest compiler-reported static frame; not a call-chain stack bound."""
    maximum = 0
    for obj in objects:
        rows = obj.with_suffix(".su").read_text().splitlines()
        if not rows:
            raise ValueError(f"{obj.name}: missing stack usage rows")
        for row in rows:
            _, size, kind = row.split("\t")
            if kind != "static":
                raise ValueError(f"{obj.name}: non-static stack usage: {row}")
            maximum = max(maximum, int(size))
    return maximum
