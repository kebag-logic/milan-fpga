# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Shared freestanding RV32I object checks, without the SDK's hosted libc.

GCC supplies stdint/stddef/stdarg/stdbool under -ffreestanding. The two
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


def object_findings(cc: str, objects: list[Path]) -> list[str]:
    """Every emitted object must use little-endian ELF32 RISC-V soft-float ABI."""
    found = []
    for obj in objects:
        data = obj.read_bytes()
        if (len(data) < 52 or data[:7] != b"\x7fELF\x01\x01\x01" or
                struct.unpack_from("<HH", data, 16) != (1, 243) or
                struct.unpack_from("<I", data, 36)[0] != 0):
            found.append(f"{obj.name}: expected RV32I ILP32 relocatable object")
            continue
        attributes = fw_gtest.run([cc.removesuffix("gcc") + "readelf", "-A", str(obj)])
        arches = re.findall(r'Tag_RISCV_arch: "([^"]+)"', attributes.stdout)
        if attributes.returncode or len(arches) != 1 or not re.fullmatch(r"rv32i\d+p\d+", arches[0]):
            found.append(f"{obj.name}: expected RV32I architecture attribute, got {arches}")
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
