#!/usr/bin/env python3
"""Reviewer probe: ctrl_memory.plan/read_elf on edge-case ELFs (no source change).

    python3 -I probe_elf_edges.py <repo> <scratch-dir>

Writes ELFs with the head test's own independent writer (test_ctrl_memory.write_elf
is not imported, to keep this probe free of LiteX; a copy of its layout is used)
and prints, per case, ACCEPTED / REFUSED <check>/<rule> / RAISED <type>.
"""
import struct
import sys
from pathlib import Path

repo, tmp = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/litex"))
import ctrl_memory as cm  # noqa: E402

RAM = cm.RAM.origin


def write_elf(entry, sections, symbols, shstrndx_override=None, symtab_link=None, symtab_entsize=16):
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
        symtab += struct.pack("<IIIBBH", strtab.index(name.encode() + b"\0"), RAM, size, 0x11, 0, 1)
    tables = {"symtab": base + len(body)}
    body += symtab
    tables["strtab"] = base + len(body)
    body += strtab
    tables["shstrtab"] = base + len(body)
    body += shstr + b"\0" * (-len(shstr) % 4)
    shoff = base + len(body)
    n = len(sections)
    shstrndx = n + 3 if shstrndx_override is None else shstrndx_override
    head = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 2, 243, 1, entry, 52, shoff,
                       0, 52, 32, n, 40, n + 4, shstrndx)
    programs, shdrs = b"", bytes(40)
    for (name, vma, lma, data, writable), offset in zip(sections, placed):
        loaded = isinstance(data, bytes)
        size = len(data) if loaded else data
        programs += struct.pack("<8I", 1, offset, vma, lma, size if loaded else 0, size, 6, 4)
        shdrs += struct.pack("<10I", shstr.index(name.encode() + b"\0"), 1 if loaded else 8,
                             0x2 | (0x1 if writable else 0x4), vma, offset, size, 0, 0, 4, 0)
    link = n + 2 if symtab_link is None else symtab_link
    shdrs += struct.pack("<10I", shstr.index(b".symtab\0"), 2, 0, 0, tables["symtab"], len(symtab), link, 1, 4,
                         symtab_entsize)
    shdrs += struct.pack("<10I", shstr.index(b".strtab\0"), 3, 0, 0, tables["strtab"], len(strtab), 0, 0, 1, 0)
    shdrs += struct.pack("<10I", shstr.index(b".shstrtab\0"), 3, 0, 0, tables["shstrtab"], len(shstr), 0, 0, 1, 0)
    return head + programs + body + shdrs


def good_sections(extra=()):
    return [(".text", 0, 0, bytes(range(256)) * 32, False),
            (".rodata", 8192, 8192, bytes(512), False),
            (".data", RAM, 8704, bytes(range(64)), True),
            (".bss", RAM + 64, RAM + 64, 4096, True),
            *extra,
            (".stack", RAM + 0x2000, RAM + 0x2000, 8192, True)]


def run(label, **kw):
    sections = kw.pop("sections", good_sections())
    path = tmp / (label.replace(" ", "_") + ".elf")
    path.write_bytes(write_elf(0, sections, {"_start": 4, "nvm_stage": 3344}, **kw))
    try:
        cm.plan(cm.read_elf(path))
        print(f"{label}: ACCEPTED")
    except cm.Refusal as exc:
        print(f"{label}: REFUSED {exc.check}/{exc.rule}")
    except Exception as exc:  # recorded, not a refusal
        print(f"{label}: RAISED {type(exc).__name__}: {exc}")


tmp.mkdir(parents=True, exist_ok=True)
run("control good image")
# A loaded writable section that runs in sram after .data, loaded from rom, but
# outside the [_fdata, _edata) range the reset entry copies: never initialised.
run("loaded sram section outside the startup copy",
    sections=good_sections([(".orphan_data", RAM + 0x1100, 8768, bytes(range(1, 33)), True)]))
run("shstrndx out of range", shstrndx_override=60)
run("symtab sh_link out of range", symtab_link=60)
run("symtab entsize zero", symtab_entsize=0)
