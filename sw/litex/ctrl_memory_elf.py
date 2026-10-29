# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The memory test's ELF32 writer, independent of `ctrl_memory.read_elf`, and its byte edits."""

from __future__ import annotations

import struct
from collections.abc import Callable

import ctrl_memory


def write_elf(entry: int, sections: list[tuple[str, int, int, bytes | int, bool]],
              symbols: dict[str, int], machine: int = 243) -> bytes:
    """A little-endian ELF32 executable, one PT_LOAD per section.

    A section is (name, address, load address, initial bytes or a NOBITS
    size, writable); a symbol is a name and the size of the object it names.
    """
    shstr = b"\0" + b"".join(n.encode() + b"\0" for n, *_ in sections) + b".symtab\0.strtab\0.shstrtab\0"
    strtab = b"\0" + b"".join(n.encode() + b"\0" for n in symbols)
    body, placed = b"", []
    base = 52 + 32 * len(sections)
    for _, _, _, data, _ in sections:
        payload = data if isinstance(data, bytes) else b""
        placed.append(base + len(body))
        body += payload + b"\0" * (-len(payload) % 4)
    symtab = bytes(16)
    for name, size in symbols.items():
        symtab += struct.pack("<IIIBBH", strtab.index(name.encode() + b"\0"), ctrl_memory.RAM.origin, size,
                              0x11, 0, 1)
    tables = {"symtab": base + len(body)}
    body += symtab
    tables["strtab"] = base + len(body)
    body += strtab
    tables["shstrtab"] = base + len(body)
    body += shstr + b"\0" * (-len(shstr) % 4)
    shoff = base + len(body)
    head = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 2, machine, 1, entry, 52, shoff,
                       0, 52, 32, len(sections), 40, len(sections) + 4, len(sections) + 3)
    programs = b""
    shdrs = bytes(40)
    for (name, vma, lma, data, writable), offset in zip(sections, placed):
        loaded = isinstance(data, bytes)
        size = len(data) if loaded else data
        programs += struct.pack("<8I", 1, offset, vma, lma, size if loaded else 0, size, 6, 4)
        shdrs += struct.pack("<10I", shstr.index(name.encode() + b"\0"), 1 if loaded else 8,
                             0x2 | (0x1 if writable else 0x4), vma, offset, size, 0, 0, 4, 0)
    n = len(sections)
    shdrs += struct.pack("<10I", shstr.index(b".symtab\0"), 2, 0, 0, tables["symtab"], len(symtab), n + 2, 1, 4, 16)
    shdrs += struct.pack("<10I", shstr.index(b".strtab\0"), 3, 0, 0, tables["strtab"], len(strtab), 0, 0, 1, 0)
    shdrs += struct.pack("<10I", shstr.index(b".shstrtab\0"), 3, 0, 0, tables["shstrtab"], len(shstr), 0, 0, 1, 0)
    return head + programs + body + shdrs


def truncate(size: Callable[[int], int]) -> Callable[[bytearray], None]:
    """An edit that cuts the file to `size(len)` bytes."""
    def cut(data: bytearray) -> None:
        """Drop everything past the new end."""
        del data[size(len(data)):]
    return cut


def poke(offset: Callable[[bytearray], int], value: int) -> Callable[[bytearray], None]:
    """An edit that overwrites the 32-bit field at `offset(data)` with `value`."""
    def write(data: bytearray) -> None:
        """Pack the field in place."""
        struct.pack_into("<I", data, offset(data), value)
    return write


def splice(at: int, value: bytes) -> Callable[[bytearray], None]:
    """An edit that overwrites the bytes at `at` with `value`."""
    def write(data: bytearray) -> None:
        """Overwrite in place."""
        data[at:at + len(value)] = value
    return write
