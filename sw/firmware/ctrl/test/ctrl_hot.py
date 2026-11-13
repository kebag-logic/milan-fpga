#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split image's hot list (#665, NFR-SCOUT-01).

plat/ctrl_split.ld places the functions a service pass runs ahead of the rest of
the text, each as `*-<stem>.o(.text.<function>)`, in the order
plat/ctrl_split_hot.txt records with the traces it was learned from. A pattern
that matches no section places nothing, so a renamed or removed function would
silently keep its place among the rest. Two rules, each a finding:

  ORDER   the script's list is the recorded one, entry for entry;
  LINKED  every entry names a section of the linked image, read from its link
          map (not its discarded input sections);
  SETS    the script opens .bss with SRP's state and then the store's (#908),
          and where the image links both as their own sections (the size
          fixture's image_srp and nvm_store's nvm) they share no line set of
          the split CPU's 8 KiB direct-mapped data cache, read from the map.

ctrl_srp_image.py applies the three to every split image it links. --check applies
ORDER and SETS' order to the tree's two files, and LINKED and SETS' sets too with --map. --self-test plants
each defect of PLANTS into copies of the two files and of a map written from
the recorded order, and requires its rule to refuse it; the unplanted copies
must pass both.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_hot.py --check [--map ctrl_app.map]
    python3 sw/firmware/ctrl/test/ctrl_hot.py --self-test

Exit 0 = no finding (with --self-test, every plant refused by its own rule);
1 = a finding.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PLAT = Path(__file__).resolve().parents[1] / "plat"
SCRIPT = PLAT / "ctrl_split.ld"
ORDER = PLAT / "ctrl_split_hot.txt"
START = "_ctrl_hot_start = .;"
END = "_ctrl_hot_end = .;"
# An entry selects a firmware object by its stem (`*-<stem>.o`) or a runtime archive's member
# (`*<archive>:<member>.o`); either is named here as its object: `<stem>` or `<archive>:<member>`.
ENTRY = re.compile(r"\*(?:-([A-Za-z0-9_]+)|([A-Za-z0-9_.]+\.a):([A-Za-z0-9_]+))\.o\(\.text\.([A-Za-z0-9_.]+)\)")
# One input section of the link map: its name, address and size, and the object it came from, on one line or,
# for a long name, on two.
SECTION = re.compile(r"^ \.text\.(\S+)\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+\S*/"
                     r"(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)

Entry = tuple[str, str]
#: SETS (#908): the two lines that open the script's .bss, SRP's state then the store's, and the split CPU's data
#: cache (docs/design/SPLIT_CONTROL_MEMORY.md section 9: 128 sets of 64-byte lines, one way).
BSS_START = "_fbss = .;"
PLACED = ("*(.bss.image_srp)", "*-nvm_store.o(.bss.nvm)")
CACHE_SETS, CACHE_LINE = 128, 64
# Each of the two as an input section of the link map: its address and size, on one line or, for a long name, two.
STATE = re.compile(r"^ \.bss\.(image_srp|nvm)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s", re.M)


def listed(script: str) -> list[Entry] | None:
    """The script's hot list in order, or None when its block is missing or holds anything else."""
    if script.count(START) != 1 or script.count(END) != 1 or script.index(START) > script.index(END):
        return None
    rows = [row.strip() for row in script[script.index(START) + len(START):script.index(END)].splitlines()]
    entries = [ENTRY.fullmatch(row) for row in rows if row]
    return [(m[1] or f"{m[2]}:{m[3]}", m[4]) for m in entries] if all(entries) else None


def recorded(order: str) -> list[Entry]:
    """The recorded order: one `<stem> <function>` a line, `#` lines and blank lines aside."""
    rows = [row.split() for row in order.splitlines() if row.strip() and not row.lstrip().startswith("#")]
    return [(row[0], row[1]) if len(row) == 2 else ("?", " ".join(row)) for row in rows]


def linked(link_map: str) -> set[Entry]:
    """Every text section the image links, by its object's stem: the map past its discarded sections."""
    marker = "Linker script and memory map"
    body = link_map[link_map.index(marker):] if marker in link_map else ""
    return {(stem or f"{archive}:{member}", name) for name, stem, archive, member in SECTION.findall(body)}


def entry(e: Entry) -> str:
    """An entry as the script spells it."""
    return f"*{e[0]}.o(.text.{e[1]})" if ":" in e[0] else f"*-{e[0]}.o(.text.{e[1]})"


def placed(script: str) -> bool:
    """Whether the script's .bss opens with PLACED, in its order, its comment lines aside."""
    rows = [row.strip() for row in script.splitlines()]
    k = next((n for n, row in enumerate(rows) if row == BSS_START), None)
    rows = [row for row in rows[k + 1:] if row and not row.startswith(("/*", "* ", "*/"))] if k is not None else []
    return rows[:2] == list(PLACED)


def shared_sets(link_map: str) -> list[int]:
    """The data-cache sets SRP's state and the store's state share in a linked image, but for a line both hold;
    none where the map links either inside another section."""
    found = {name: (int(a, 16), int(s, 16)) for name, a, s in STATE.findall(link_map)}
    if set(found) != {"image_srp", "nvm"}:
        return []
    lines = {name: set(range(a // CACHE_LINE, (a + s + CACHE_LINE - 1) // CACHE_LINE))
             for name, (a, s) in found.items()}
    return sorted({x % CACHE_SETS for x in lines["image_srp"] for y in lines["nvm"]
                   if x != y and x % CACHE_SETS == y % CACHE_SETS})


def findings(script: str, order: str, link_map: str | None = None) -> list[str]:
    """ORDER and SETS' order, then LINKED and SETS' sets when a map is given: each finding one line."""
    out = [] if placed(script) else [f"SETS: ctrl_split.ld does not open .bss with {PLACED[0]} and then {PLACED[1]}"]
    if link_map is not None and shared_sets(link_map):
        out.append(f"SETS: SRP's state and the store's state share the data cache's sets "
                   f"{', '.join(map(str, shared_sets(link_map)))}")
    have = listed(script)
    want = recorded(order)
    if have is None:
        return out + [f"ORDER: ctrl_split.ld holds no hot list of entries alone between {START} and {END}"]
    if have != want:
        k = next((n for n, (a, b) in enumerate(zip(have, want)) if a != b), min(len(have), len(want)))
        found = entry(have[k]) if k < len(have) else "the end"
        expected = entry(want[k]) if k < len(want) else "the end"
        out.append(f"ORDER: the hot list is not the order ctrl_split_hot.txt records: entry {k + 1} is {found}, "
                   f"recorded {expected}")
    if link_map is not None:
        names = linked(link_map)
        out += [f"LINKED: hot-list name {entry(e)} is no section of the linked image" for e in have if e not in names]
    return out


def written_map(entries: list[Entry], discarded: list[Entry] = (), state: tuple[int, int] | None = None) -> str:
    """A link map in the toolchain's layout holding these entries' sections, and these discarded ones; and SRP's
    state and the store's at these two addresses, at their sizes at 1x1/1if, where `state` is given."""
    def path(n: int, stem: str) -> str:
        """The object a section came from, as the toolchain names it in the map."""
        archive, _, member = stem.partition(":")
        return f"/scratch/{archive}({member}.o)" if member else f"/scratch/{n}-{stem}.o"

    def rows(chosen: list[Entry], base: int) -> str:
        """One input section a line, from base, as the map lays it out."""
        return "".join(f" .text.{name}\n                0x{base + 16 * n:08x}       0x10 {path(n, stem)}\n"
                       for n, (stem, name) in enumerate(chosen))
    data = "" if state is None else (
        f" .bss.image_srp\n                0x{state[0]:08x}      0xd10 /scratch/3-ctrl_srp_image.o\n"
        f" .bss.nvm       0x{state[1]:08x}      0x228 /scratch/27-nvm_store.o\n")
    return ("Discarded input sections\n\n" + rows(list(discarded), 0) + "\nMemory Configuration\n\n"
            "Linker script and memory map\n\n .text           0x00000000     0x1000\n *(.text.start)\n"
            + rows(entries, 0x8c) + data)


def plants(script: str, order: str) -> list[tuple[str, str, str, str, str]]:
    """Each planted defect: its name, the rule that must refuse it, and the script, order and map it makes."""
    want = recorded(order)
    first, second = want[0], want[1]
    good_map = written_map(want, state=(0x10000040, 0x10000d50))
    swapped = script.replace(entry(first), "\0").replace(entry(second), entry(first)).replace("\0", entry(second))
    renamed = (first[0], first[1] + "_old")
    extra = ("mbx", "mbx_open")
    return [
        ("stale-name", "LINKED", script.replace(entry(first), entry(renamed)),
         order.replace(f"{first[0]} {first[1]}\n", f"{renamed[0]} {renamed[1]}\n", 1), good_map),
        ("absent-from-image", "LINKED", script, order, written_map(want[1:])),
        ("only-discarded", "LINKED", script, order, written_map(want[1:], [first])),
        ("reordered", "ORDER", swapped, order, good_map),
        ("dropped", "ORDER", script.replace(f"\t\t{entry(second)}\n", ""), order, good_map),
        ("unrecorded", "ORDER", script.replace(END, f"{entry(extra)}\n\t\t{END}"), order, written_map([*want, extra])),
        ("recorded-elsewhere", "ORDER", script, order.replace(f"{second[0]} {second[1]}\n", "", 1), good_map),
        ("no-end-marker", "ORDER", script.replace(END, ""), order, good_map),
        ("state-unplaced", "SETS", script.replace(f"\t\t{PLACED[0]}\n", "").replace(f"\t\t{PLACED[1]}\n", ""),
         order, good_map),
        ("state-reordered", "SETS", script.replace(PLACED[0], "\0").replace(PLACED[1], PLACED[0]).replace(
            "\0", PLACED[1]), order, good_map),
        ("state-aliased", "SETS", script, order, written_map(want, state=(0x10007530, 0x1000b520))),
    ]


def self_test(script: str, order: str) -> int:
    """The tree's files pass the three rules on a map written from the order, with SRP's state and the store's at
    1x1/1if's sizes one after the other; every plant is refused by its rule."""
    failures = 0
    control = findings(script, order, written_map(recorded(order)))
    print(f"control: the tree's script and order, linked: {'PASS' if not control else control}")
    failures += bool(control)
    for name, rule, planted_script, planted_order, planted_map in plants(script, order):
        found = findings(planted_script, planted_order, planted_map)
        caught = bool(found) and all(f.startswith(rule + ":") for f in found)
        print(f"[{'caught' if caught else 'ESCAPED'}] {name}: {found[0] if found else 'no finding'}")
        failures += not caught
    print(f"self-test: {failures} failure(s)")
    return 1 if failures else 0


def main() -> int:
    """--check or --self-test on the tree's script and order."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--map", type=Path, help="with --check: the linked split image's map")
    args = parser.parse_args()
    script = SCRIPT.read_text()
    order = ORDER.read_text()
    if args.self_test:
        return self_test(script, order)
    found = findings(script, order, args.map.read_text() if args.map else None)
    print("\n".join(found) or f"hot list: {len(recorded(order))} entries, "
                               f"{'linked and ' if args.map else ''}in the recorded order")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
