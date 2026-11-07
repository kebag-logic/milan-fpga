#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gen_flash_port.py - the flash port's map, generated from a split SoC's csr.csv (#665).

nvm_flash_litespi.c reaches three devices: the LiteSPI command master, timer0
and the memory-mapped flash window. On the target their addresses are the
split SoC's (sw/litex/milan_soc.py --ctrl-mailbox --ctrl-firmware), which
LiteX writes into the export's csr.csv. This generator reads them from there
and writes the two headers the port includes, so the port never compiles
against a hand-written address:

  OUT/generated/csr.h   the command master's and timer0's registers, their
                        accessors and the master's field offsets;
  OUT/generated/mem.h   the flash window's base and size;
  OUT/flash_port.json   the same map, the clock and the journal, for the
                        builds that place or check the devices.

LiteX's own csr.h cannot be compiled into the freestanding image: it includes
libbase's <system.h> and <hw/common.h>. Its field offsets are still read, from
the same export's csr.h, because csr.csv carries no fields. Every register
address the two files share is compared, and a difference is refused.

THE RULES, each a named refusal (RULES below):

  data width     each register is one 32-bit word (config_csr_data_width);
  registers      every register the port uses is in csr.csv once, one word
                 wide, with the access the port needs;
  header         csr.h names each of those registers at csr.csv's address,
                 and defines each field the port writes or tests;
  fields         each value the port writes into phyconfig fits its field,
                 the fields do not overlap, and the two status bits are one
                 bit each and distinct;
  flash window   the window is mapped once, at the size of the part and of
                 the device milan_soc.py describes (FLASH_SIZE);
  journal        the SoC publishes the journal milan_soc.py reserves
                 (FLASHBOOT_RESERVED), and the store is built with that
                 journal (nvm_bench.py reads the same literal). It is two
                 slots, each one erase block, the A/B geometry
                 scripts/check_nvm_record_space.py sizes every container
                 against (check 5), aligned and inside the device;
  slots          the journal overlaps no image slot (FLASHBOOT_LAYOUT: the
                 bitstream and the AEM), no other reserved slot, and no image
                 the SoC publishes (milan_flashboot_*_offset/_size);
  clock          the SoC publishes the clock timer0 counts.

The port's own guard (ls_in_journal) refuses a program or an erase outside
MILAN_FLASH_JOURNAL_OFFSET/SIZE; these rules are why those constants, in the
image that links the port, are the journal of the SoC the image runs on.

Usage:
    python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv EXPORT/csr.csv \\
        --csr-h EXPORT/software/include/generated/csr.h --out DIR
    python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --self-test

Exit 0 = written (or every self-test check passed); 1 = refused; 2 = an input
could not be read.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "sw/litex"))
sys.path.insert(0, str(ROOT / "scripts"))

from flash_map import literal  # noqa: E402
from nvm_contract import FIXED  # noqa: E402

PORT = HERE / "nvm_flash_litespi.c"
#: Each register the port uses: its csr.csv name and the access it needs.
REGISTERS = {
    "spiflash_master_cs": "rw", "spiflash_master_phyconfig": "rw", "spiflash_master_rxtx": "rw",
    "spiflash_master_status": "ro",
    "timer0_load": "rw", "timer0_reload": "rw", "timer0_en": "rw", "timer0_update_value": "rw",
    "timer0_value": "ro",
}
#: The phyconfig fields and the value nvm_flash_litespi.c's ls_open() writes into each.
PHYCONFIG = {"LEN": 8, "WIDTH": 1, "MASK": 1}
#: The status bits the port tests.
STATUS = ("TX_READY", "RX_READY")
#: The devices whose CSR banks the harness places, by csr_base name.
BANKS = ("spiflash", "timer0")
#: The flash window's memory region in csr.csv.
WINDOW = "spiflash"
DATA_WIDTH = 32


class Unreadable(Exception):
    """An input could not be read: exit 2."""


@dataclass
class Export:
    """What one split SoC export says, parsed."""

    bases: dict[str, int] = field(default_factory=dict)
    registers: dict[str, tuple[int, int, str]] = field(default_factory=dict)
    duplicates: set[str] = field(default_factory=set)
    constants: dict[str, str] = field(default_factory=dict)
    regions: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    header_addr: dict[str, int] = field(default_factory=dict)
    header_fields: dict[str, tuple[int, int]] = field(default_factory=dict)


def field_name(register: str, name: str) -> str:
    """LiteX's csr.h name of one field of a register, without _OFFSET or _SIZE."""
    return f"CSR_{register.upper()}_{name}"


def parse_csv(text: str, export: Export) -> None:
    """csr.csv's rows into `export`: bases, registers (a name seen twice is kept in duplicates), constants and
    memory regions."""
    rows = csv.reader(line for line in io.StringIO(text) if not line.startswith("#"))
    for row in rows:
        if not row:
            continue
        kind, name, *rest = row + [""] * (5 - len(row))
        if kind == "csr_base":
            export.bases[name] = int(rest[0], 16)
        elif kind == "csr_register":
            if name in export.registers:
                export.duplicates.add(name)
            export.registers[name] = (int(rest[0], 16), int(rest[1]), rest[2])
        elif kind == "constant":
            export.constants[name] = rest[0]
        elif kind == "memory_region":
            export.regions.setdefault(name, []).append((int(rest[0], 16), int(rest[1])))


def parse_header(text: str, export: Export) -> None:
    """LiteX csr.h's register addresses and field offsets into `export`."""
    base = re.findall(r"^#define CSR_BASE (0x[0-9a-fA-F]+)L?$", text, re.M)
    if len(base) != 1:
        raise Unreadable(f"csr.h defines CSR_BASE {len(base)} times, not once")
    for name, offset in re.findall(r"^#define (CSR_\w+)_ADDR \(CSR_BASE \+ (0x[0-9a-fA-F]+)L\)$", text, re.M):
        export.header_addr[name] = int(base[0], 16) + int(offset, 16)
    sizes = dict(re.findall(r"^#define (CSR_\w+)_SIZE (\d+)$", text, re.M))
    for name, offset in re.findall(r"^#define (CSR_\w+)_OFFSET (\d+)$", text, re.M):
        if name in sizes:
            export.header_fields[name] = (int(offset), int(sizes[name]))


def read_export(csr_csv: Path, csr_h: Path) -> Export:
    """Both files of one export, parsed; Unreadable when either cannot be."""
    export = Export()
    try:
        parse_csv(csr_csv.read_text(), export)
        parse_header(csr_h.read_text(), export)
    except (OSError, ValueError, IndexError) as exc:
        raise Unreadable(f"{exc}") from exc
    return export


def number(export: Export, name: str) -> int | None:
    """A constant of the export as an integer; None when it is absent or not a number."""
    value = export.constants.get(name)
    return int(value, 0) if value is not None and re.fullmatch(r"\d+|0x[0-9a-fA-F]+", value) else None


def rule_data_width(export: Export) -> list[str]:
    """Each CSR register is one 32-bit word."""
    width = number(export, "config_csr_data_width")
    return [] if width == DATA_WIDTH else [f"config_csr_data_width is {width}, not {DATA_WIDTH}"]


def rule_registers(export: Export) -> list[str]:
    """Every register the port uses is in csr.csv once, one word wide, with its access."""
    found = []
    for name, access in REGISTERS.items():
        if name not in export.registers:
            found.append(f"{name} is not in csr.csv")
            continue
        _addr, size, kind = export.registers[name]
        if name in export.duplicates:
            found.append(f"{name} is in csr.csv more than once")
        if size != 1:
            found.append(f"{name} is {size} words, not one")
        if kind != access:
            found.append(f"{name} is {kind}, the port needs {access}")
    return found


def rule_header(export: Export) -> list[str]:
    """csr.h names each register at csr.csv's address and defines each field the port uses."""
    found = []
    for name in REGISTERS:
        if name not in export.registers:
            continue
        want, got = export.registers[name][0], export.header_addr.get(f"CSR_{name.upper()}")
        if got != want:
            found.append(f"csr.h puts {name} at {got if got is None else hex(got)}, csr.csv at {want:#x}")
    for name in [*(field_name("spiflash_master_phyconfig", f) for f in PHYCONFIG),
                 *(field_name("spiflash_master_status", s) for s in STATUS)]:
        if name not in export.header_fields:
            found.append(f"csr.h does not define {name}_OFFSET and _SIZE")
    return found


def rule_fields(export: Export) -> list[str]:
    """The values the port writes fit their fields, the fields are disjoint, the status bits single and
    distinct."""
    found, used = [], 0
    for name, value in PHYCONFIG.items():
        at = export.header_fields.get(field_name("spiflash_master_phyconfig", name))
        if at is None:
            continue
        offset, size = at
        if value >> size:
            found.append(f"phyconfig {name} is {size} bits; the port writes {value}")
        bits = ((1 << size) - 1) << offset
        if bits & used:
            found.append(f"phyconfig {name} overlaps another field")
        used |= bits
    status = [export.header_fields.get(field_name("spiflash_master_status", s)) for s in STATUS]
    if None not in status:
        if any(size != 1 for _offset, size in status):
            found.append(f"a status bit the port tests is not one bit: {dict(zip(STATUS, status))}")
        if status[0][0] == status[1][0]:
            found.append(f"TX_READY and RX_READY are the same bit ({status[0][0]})")
    return found


def rule_window(export: Export) -> list[str]:
    """The flash window is mapped once, at the size of the part and of the device milan_soc.py describes."""
    regions = export.regions.get(WINDOW, [])
    if len(regions) != 1:
        return [f"memory region {WINDOW} is mapped {len(regions)} times, not once"]
    base, size = regions[0]
    part, device = number(export, "spiflash_module_total_size"), literal("FLASH_SIZE")
    found = [] if size == part == device else [
        f"the window is {size} bytes, the part {part}, the device (FLASH_SIZE) {device}"]
    if base % size:
        found.append(f"the window at {base:#x} is not aligned to its {size} bytes")
    return found


def journal(export: Export) -> tuple[int | None, int | None]:
    """The journal the SoC publishes: its offset and size, None where absent."""
    return number(export, "milan_flash_journal_offset"), number(export, "milan_flash_journal_size")


def rule_journal(export: Export) -> list[str]:
    """The SoC's journal is milan_soc.py's, two one-erase-block slots, aligned and inside the device."""
    offset, size = journal(export)
    reserved = literal("FLASHBOOT_RESERVED")["journal"]
    if offset is None or size is None:
        return ["csr.csv publishes no milan_flash_journal_offset and _size"]
    found = []
    if (offset, size) != (reserved["offset"], reserved["size"]):
        found.append(f"the SoC's journal {offset:#x}+{size:#x} is not milan_soc.py's "
                     f"{reserved['offset']:#x}+{reserved['size']:#x}, which the store is built with")
    if size != 2 * FIXED.ERASE_BLOCK:
        found.append(f"the journal is {size:#x} bytes, not two {FIXED.ERASE_BLOCK:#x}-byte slots")
    if offset % literal("FLASH_ERASE_BLOCK"):
        found.append(f"the journal at {offset:#x} is not erase-block aligned")
    if offset + size > literal("FLASH_SIZE"):
        found.append(f"the journal ends at {offset + size:#x}, past the device")
    return found


def published_images(export: Export) -> dict[str, tuple[int, int]]:
    """Each image the SoC publishes (milan_flashboot_<name>_offset and _size), by name."""
    images = {}
    for name in export.constants:
        match = re.fullmatch(r"milan_flashboot_(\w+)_offset", name)
        size = number(export, f"milan_flashboot_{match.group(1)}_size") if match else None
        if match and size is not None:
            images[f"published {match.group(1)}"] = (number(export, name), size)
    return images


def rule_slots(export: Export) -> list[str]:
    """The journal overlaps no image slot, no other reserved slot and no image the SoC publishes."""
    offset, size = journal(export)
    if offset is None or size is None:
        return []
    others = {name: (e["offset"], e["size"]) for name, e in literal("FLASHBOOT_LAYOUT").items()}
    others.update((name, (e["offset"], e["size"])) for name, e in literal("FLASHBOOT_RESERVED").items()
                  if name != "journal")
    others.update(published_images(export))
    return [f"the journal {offset:#x}+{size:#x} overlaps {name} {start:#x}+{length:#x}"
            for name, (start, length) in sorted(others.items())
            if start < offset + size and offset < start + length]


def rule_clock(export: Export) -> list[str]:
    """The SoC publishes the clock timer0 counts."""
    hz = number(export, "config_clock_frequency")
    return [] if hz else ["csr.csv publishes no config_clock_frequency"]


RULES: dict[str, Callable[[Export], list[str]]] = {
    "data width": rule_data_width, "registers": rule_registers, "header": rule_header, "fields": rule_fields,
    "flash window": rule_window, "journal": rule_journal, "slots": rule_slots, "clock": rule_clock,
}


def findings(export: Export, rules: dict[str, Callable[[Export], list[str]]] = RULES) -> list[tuple[str, str]]:
    """Every (rule, finding) the export fails."""
    return [(name, text) for name, rule in rules.items() for text in rule(export)]


def accessors(name: str, access: str) -> list[str]:
    """One register's address and its accessors, as LiteX names them: a read for each, a write where it is
    writable."""
    upper = name.upper()
    lines = [f"static inline uint32_t {name}_read(void) {{ return flash_port_rd(CSR_{upper}_ADDR); }}"]
    if access == "rw":
        lines.append(f"static inline void {name}_write(uint32_t v) {{ flash_port_wr(CSR_{upper}_ADDR, v); }}")
    return lines


def csr_header(export: Export) -> str:
    """generated/csr.h for the port: the fields, the register addresses and their accessors."""
    lines = ["/* Generated by sw/firmware/ctrl_nvm/plat/gen_flash_port.py from the split SoC's csr.csv",
             " * (#665); never edited or committed. */",
             "#ifndef GENERATED_CSR_H", "#define GENERATED_CSR_H", "#include <stdint.h>"]
    names = [*(field_name("spiflash_master_phyconfig", f) for f in PHYCONFIG),
             *(field_name("spiflash_master_status", s) for s in STATUS)]
    for name in names:
        offset, size = export.header_fields[name]
        lines += [f"#define {name}_OFFSET {offset}", f"#define {name}_SIZE {size}"]
    lines += [f"#define CSR_{name.upper()}_ADDR 0x{export.registers[name][0]:08x}u" for name in REGISTERS]
    lines += ["static inline uint32_t flash_port_rd(uint32_t a) { return *(volatile uint32_t *)(uintptr_t)a; }",
              "static inline void flash_port_wr(uint32_t a, uint32_t v) { *(volatile uint32_t *)(uintptr_t)a = v; }"]
    for name, access in REGISTERS.items():
        lines += accessors(name, access)
    return "\n".join([*lines, "#endif", ""])


def mem_header(export: Export) -> str:
    """generated/mem.h for the port: the flash window."""
    base, size = export.regions[WINDOW][0]
    return "\n".join(["/* Generated by sw/firmware/ctrl_nvm/plat/gen_flash_port.py from the split SoC's csr.csv",
                      " * (#665); never edited or committed. */",
                      "#ifndef GENERATED_MEM_H", "#define GENERATED_MEM_H",
                      f"#define SPIFLASH_BASE 0x{base:08x}u", f"#define SPIFLASH_SIZE 0x{size:08x}u", "#endif", ""])


def port_map(export: Export, sources: dict[str, str]) -> dict:
    """flash_port.json: the map, the clock, the journal and the digests of the two files it came from."""
    offset, size = journal(export)
    base, length = export.regions[WINDOW][0]
    return {"source": sources, "registers": {n: export.registers[n][0] for n in REGISTERS},
            "fields": {n: list(v) for n, v in sorted(export.header_fields.items()) if "SPIFLASH_MASTER" in n},
            "banks": {n: export.bases[n] for n in BANKS if n in export.bases},
            "flash": {"base": base, "size": length}, "journal": {"offset": offset, "size": size},
            "clock_hz": number(export, "config_clock_frequency")}


def generate(csr_csv: Path, csr_h: Path, out: Path) -> list[tuple[str, str]]:
    """Write the port's headers and map from one export into `out`; the findings that refused it, if any."""
    export = read_export(csr_csv, csr_h)
    found = findings(export)
    if found:
        return found
    (out / "generated").mkdir(parents=True, exist_ok=True)
    (out / "generated/csr.h").write_text(csr_header(export))
    (out / "generated/mem.h").write_text(mem_header(export))
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (csr_csv, csr_h)}
    (out / "flash_port.json").write_text(json.dumps(port_map(export, sources), indent=2) + "\n")
    return []


# ---- the self-test --------------------------------------------------------------------------------------------

#: A passing export as the split SoC's 1x1 export has it at dev-soft-core f4c9ad4f: the spiflash bank, timer0 and the
#: constants the rules read. The self-test plants each defect in a copy of it.
GOOD_CSV = {
    "bases": {"spiflash": 0xF000_2800, "timer0": 0xF000_3000},
    "registers": {"spiflash_master_cs": (0xF000_2810, 1, "rw"), "spiflash_master_phyconfig": (0xF000_2814, 1, "rw"),
                  "spiflash_master_rxtx": (0xF000_2818, 1, "rw"), "spiflash_master_status": (0xF000_281C, 1, "ro"),
                  "timer0_load": (0xF000_3000, 1, "rw"), "timer0_reload": (0xF000_3004, 1, "rw"),
                  "timer0_en": (0xF000_3008, 1, "rw"), "timer0_update_value": (0xF000_300C, 1, "rw"),
                  "timer0_value": (0xF000_3010, 1, "ro")},
    "constants": {"config_clock_frequency": "100000000", "config_csr_data_width": "32",
                  "spiflash_module_total_size": "16777216", "milan_flash_journal_offset": "15597568",
                  "milan_flash_journal_size": "131072", "milan_flashboot_aem_offset": "4194304",
                  "milan_flashboot_aem_size": "65536"},
    "regions": {"spiflash": [(0x0100_0000, 16_777_216)], "csr": [(0xF000_0000, 65_536)]},
    "fields": {"PHYCONFIG_LEN": (0, 8), "PHYCONFIG_WIDTH": (8, 4), "PHYCONFIG_MASK": (16, 8),
               "STATUS_TX_READY": (0, 1), "STATUS_RX_READY": (1, 1)},
}


def render(spec: dict) -> tuple[str, str]:
    """csr.csv and csr.h text, in LiteX's formats, for one export spec."""
    rows = ["#" + "-" * 80, "# Auto-generated by LiteX", "#" + "-" * 80]
    rows += [f"csr_base,{n},0x{a:08x},," for n, a in spec["bases"].items()]
    rows += [f"csr_register,{n},0x{a:08x},{s},{k}" for n, (a, s, k) in spec["registers"].items()]
    rows += [f"constant,{n},{v},," for n, v in spec["constants"].items()]
    rows += [f"memory_region,{n},0x{b:08x},{s},io" for n, regions in spec["regions"].items() for b, s in regions]
    header = ["#ifndef CSR_BASE", "#define CSR_BASE 0xf0000000L", "#endif /* ! CSR_BASE */"]
    header += [f"#define CSR_{n.upper()}_ADDR (CSR_BASE + 0x{a - 0xF000_0000:x}L)\n#define CSR_{n.upper()}_SIZE {s}"
               for n, (a, s, _k) in spec.get("header", spec["registers"]).items()]
    header += [f"#define CSR_SPIFLASH_MASTER_{n}_OFFSET {o}\n#define CSR_SPIFLASH_MASTER_{n}_SIZE {s}"
               for n, (o, s) in spec["fields"].items()]
    return "\n".join(rows) + "\n", "\n".join(header) + "\n"


def planted(edit: Callable[[dict], None]) -> dict:
    """A copy of GOOD_CSV with one edit applied."""
    spec = json.loads(json.dumps(GOOD_CSV))
    spec["registers"] = {n: tuple(v) for n, v in spec["registers"].items()}
    spec["regions"] = {n: [tuple(r) for r in v] for n, v in spec["regions"].items()}
    spec["fields"] = {n: tuple(v) for n, v in spec["fields"].items()}
    edit(spec)
    return spec


def _set(path: tuple[str, ...], value: object) -> Callable[[dict], None]:
    """An edit that sets one nested key."""
    def apply(spec: dict) -> None:
        """Set the key in spec."""
        node = spec
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
    return apply


def _drop(path: tuple[str, ...]) -> Callable[[dict], None]:
    """An edit that removes one nested key."""
    def apply(spec: dict) -> None:
        """Remove the key from spec."""
        node = spec
        for key in path[:-1]:
            node = node[key]
        del node[path[-1]]
    return apply


def _moved_in_header(spec: dict) -> None:
    """csr.h puts the master's status register one word further than csr.csv does."""
    spec["header"] = dict(spec["registers"])
    addr, size, kind = spec["header"]["spiflash_master_status"]
    spec["header"]["spiflash_master_status"] = (addr + 4, size, kind)


def _twice(spec: dict) -> None:
    """The master's chip-select register is listed twice."""
    spec["duplicate"] = True


#: Each planted defect: its name, the rule that must refuse it, and the edit.
PLANTS: tuple[tuple[str, str, Callable[[dict], None]], ...] = (
    ("eight-bit CSR data width", "data width", _set(("constants", "config_csr_data_width"), "8")),
    ("the master's status register missing", "registers", _drop(("registers", "spiflash_master_status"))),
    ("the master's chip select listed twice", "registers", _twice),
    ("timer0's value register two words wide", "registers", _set(("registers", "timer0_value"),
                                                                  (0xF000_3010, 2, "ro"))),
    ("the master's status register writable", "registers", _set(("registers", "spiflash_master_status"),
                                                                 (0xF000_281C, 1, "rw"))),
    ("csr.h and csr.csv disagree on an address", "header", _moved_in_header),
    ("csr.h without the RX_READY field", "header", _drop(("fields", "STATUS_RX_READY"))),
    ("a LEN field too narrow for 8", "fields", _set(("fields", "PHYCONFIG_LEN"), (0, 3))),
    ("WIDTH overlapping LEN", "fields", _set(("fields", "PHYCONFIG_WIDTH"), (4, 4))),
    ("TX_READY two bits wide", "fields", _set(("fields", "STATUS_TX_READY"), (0, 2))),
    ("both status bits at bit 0", "fields", _set(("fields", "STATUS_RX_READY"), (0, 1))),
    ("no flash window", "flash window", _drop(("regions", "spiflash"))),
    ("an 8 MiB flash window", "flash window", _set(("regions", "spiflash"), [(0x0100_0000, 8_388_608)])),
    ("a window off its alignment", "flash window", _set(("regions", "spiflash"), [(0x0180_0000, 16_777_216)])),
    ("no journal published", "journal", _drop(("constants", "milan_flash_journal_size"))),
    ("the journal one block lower than milan_soc.py's", "journal",
     _set(("constants", "milan_flash_journal_offset"), str(0xED_0000))),
    ("no clock published", "clock", _drop(("constants", "config_clock_frequency"))),
)


def export_of(spec: dict, tmp: Path, label: str) -> Export:
    """The Export a spec renders to, through the files the generator reads."""
    csv_text, header = render(spec)
    if spec.get("duplicate"):
        csv_text += "csr_register,spiflash_master_cs,0xf0002810,1,rw\n"
    stem = tmp / re.sub(r"\W+", "-", label)
    stem.mkdir(parents=True)
    (stem / "csr.csv").write_text(csv_text)
    (stem / "csr.h").write_text(header)
    return read_export(stem / "csr.csv", stem / "csr.h")


class Tally:
    """The self-test's checks and failures."""

    def __init__(self) -> None:
        self.checks = 0
        self.failures = 0

    def check(self, ok: bool, what: str) -> None:
        """One named check."""
        self.checks += 1
        self.failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} {what}")


#: Journals milan_soc.py could reserve, each with the rules that must refuse it: the SoC publishes the same
#: journal, so only the geometry and the overlaps can refuse it. The user slot runs to the end of the device, so
#: a journal past the device overlaps it too.
RESERVED_PLANTS = (
    ("a one-slot journal", 0xEE_0000, 0x1_0000, {"journal"}),
    ("a journal off its erase block", 0xED_8000, 0x2_0000, {"journal"}),
    ("a journal past the device", 0xFF_0000, 0x2_0000, {"journal", "slots"}),
    ("a journal over the AEM slot", 0x40_0000, 0x2_0000, {"slots"}),
    ("a journal over the bitstream", 0x3F_0000, 0x2_0000, {"slots"}),
    ("a journal over the user slot", 0xF0_0000, 0x2_0000, {"slots"}),
)


def doctored_literal(real: Callable[[str], object], offset: int, size: int) -> Callable[[str], object]:
    """milan_soc.py's literals as `real` reads them, with FLASHBOOT_RESERVED's journal moved."""
    def read(name: str) -> object:
        """One literal; FLASHBOOT_RESERVED with the journal at offset, size."""
        value = real(name)
        return {**value, "journal": {"offset": offset, "size": size}} if name == "FLASHBOOT_RESERVED" else value
    return read


def reserved_plants(tally: Tally, work: Path) -> None:
    """The rules that read milan_soc.py's literals, against a doctored FLASHBOOT_RESERVED the SoC publishes
    unchanged; and an image the SoC publishes over the journal."""
    real = literal
    for label, offset, size, expected in RESERVED_PLANTS:
        constants = {"milan_flash_journal_offset": str(offset), "milan_flash_journal_size": str(size)}
        export = export_of(planted(lambda spec, c=constants: spec["constants"].update(c)), work, label)
        globals()["literal"] = doctored_literal(real, offset, size)
        try:
            rules = {name for name, _text in findings(export)}
            without = findings(export, {n: r for n, r in RULES.items() if n not in expected})
        finally:
            globals()["literal"] = real
        tally.check(rules == expected and not without,
                    f"{label} is refused by {sorted(expected)} and by no other rule ({sorted(rules)})")
    spec = planted(_set(("constants", "milan_flashboot_spare_offset"), str(0xEF_0000)))
    spec["constants"]["milan_flashboot_spare_size"] = str(0x1_0000)
    rules = {name for name, _text in findings(export_of(spec, work, "published"))}
    tally.check(rules == {"slots"}, f"a published image over the journal is refused by rule 'slots' ({sorted(rules)})")


def port_values(tally: Tally) -> None:
    """PHYCONFIG holds the values nvm_flash_litespi.c writes, and STATUS the bits it tests."""
    source = PORT.read_text()
    writes = {name: int(value) for value, name in
              re.findall(r"\((\d+)u << CSR_SPIFLASH_MASTER_PHYCONFIG_(\w+)_OFFSET\)", source)}
    tests = set(re.findall(r"CSR_SPIFLASH_MASTER_STATUS_(\w+)_OFFSET", source))
    tally.check(writes == PHYCONFIG, f"PHYCONFIG is what ls_open() writes ({writes})")
    tally.check(tests == set(STATUS), f"STATUS is what the port tests ({sorted(tests)})")


def compiled(tally: Tally, out: Path) -> None:
    """The generated headers compile, C11, every warning an error, and carry csr.csv's addresses."""
    probe = out / "probe.c"
    asserts = [f"_Static_assert(CSR_{n.upper()}_ADDR == 0x{a:08x}u, \"{n}\");"
               for n, (a, _s, _k) in GOOD_CSV["registers"].items()]
    probe.write_text("#include <generated/csr.h>\n#include <generated/mem.h>\n" + "\n".join(asserts) +
                     "\n_Static_assert(SPIFLASH_BASE == 0x01000000u && SPIFLASH_SIZE == 0x01000000u, \"window\");"
                     "\nuint32_t probe(void) { spiflash_master_cs_write(1u); return timer0_value_read(); }\n")
    result = subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-pedantic", f"-I{out}", "-c",
                             str(probe), "-o", str(out / "probe.o")], capture_output=True, text=True, check=False)
    tally.check(result.returncode == 0, f"the generated headers compile and hold csr.csv's addresses "
                                        f"({result.stderr.strip()[:300] or 'cc rc 0'})")


def self_test() -> int:
    """Every planted defect refused by its own rule, and by no rule once that rule is removed; the passing export
    generated, compiled and mapped as csr.csv says."""
    tally = Tally()
    with tempfile.TemporaryDirectory(prefix="gen-flash-port-") as tmp:
        work = Path(tmp)
        good = export_of(planted(lambda spec: None), work, "good")
        tally.check(findings(good) == [], f"the passing export passes every rule ({findings(good)})")
        for label, rule, edit in PLANTS:
            export = export_of(planted(edit), work, label)
            rules = {name for name, _text in findings(export)}
            without = {name for name, _text in findings(export, {n: r for n, r in RULES.items() if n != rule})}
            tally.check(rule in rules and not without,
                        f"{label} is refused by rule '{rule}', and by no other ({sorted(rules)})")
        out = work / "out"
        csv_text, header = render(GOOD_CSV)
        (work / "csr.csv").write_text(csv_text)
        (work / "csr.h").write_text(header)
        tally.check(generate(work / "csr.csv", work / "csr.h", out) == [], "the passing export is written")
        written = json.loads((out / "flash_port.json").read_text())
        tally.check(written["registers"] == {n: a for n, (a, _s, _k) in GOOD_CSV["registers"].items()} and
                    written["banks"] == GOOD_CSV["bases"] and written["flash"] == {"base": 0x0100_0000,
                                                                                    "size": 16_777_216},
                    "flash_port.json holds csr.csv's registers, banks and window")
        compiled(tally, out)
        bad = work / "bad"
        tally.check(main(["--csr-csv", str(work / "csr.csv"), "--csr-h", str(work / "missing.h"),
                          "--out", str(bad)]) == 2, "an unreadable csr.h exits 2, never 0")
        twice = planted(_twice)
        export_of(twice, work, "refused")
        tally.check(main(["--csr-csv", str(work / "refused/csr.csv"), "--csr-h", str(work / "refused/csr.h"),
                          "--out", str(bad)]) == 1, "a refused export exits 1")
        tally.check(not bad.exists(), "a refused or unread export writes nothing")
        reserved_plants(tally, work)
    port_values(tally)
    print(f"checks: {tally.checks}   failures: {tally.failures}")
    return 0 if tally.failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    """Generate one export's port map, or run the self-test."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--csr-csv", type=Path)
    ap.add_argument("--csr-h", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not (args.csr_csv and args.csr_h and args.out):
        ap.error("--csr-csv, --csr-h and --out are required")
    try:
        found = generate(args.csr_csv, args.csr_h, args.out)
    except Unreadable as exc:
        print(f"UNREADABLE: {exc}")
        return 2
    for rule, text in found:
        print(f"REFUSED {rule}: {text}")
    if not found:
        print(f"WROTE {args.out / 'generated/csr.h'}, {args.out / 'generated/mem.h'}, {args.out / 'flash_port.json'}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
