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
          map (not its discarded input sections).

ctrl_srp_image.py applies both to every split image it links. --check applies
ORDER to the tree's two files, and LINKED too with --map. --self-test plants
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


def findings(script: str, order: str, link_map: str | None = None) -> list[str]:
    """ORDER, then LINKED when a map is given: each finding one line."""
    out = []
    have = listed(script)
    want = recorded(order)
    if have is None:
        return [f"ORDER: ctrl_split.ld holds no hot list of entries alone between {START} and {END}"]
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


def written_map(entries: list[Entry], discarded: list[Entry] = ()) -> str:
    """A link map in the toolchain's layout holding these entries' sections, and these discarded ones."""
    def path(n: int, stem: str) -> str:
        """The object a section came from, as the toolchain names it in the map."""
        archive, _, member = stem.partition(":")
        return f"/scratch/{archive}({member}.o)" if member else f"/scratch/{n}-{stem}.o"

    def rows(chosen: list[Entry], base: int) -> str:
        """One input section a line, from base, as the map lays it out."""
        return "".join(f" .text.{name}\n                0x{base + 16 * n:08x}       0x10 {path(n, stem)}\n"
                       for n, (stem, name) in enumerate(chosen))
    return ("Discarded input sections\n\n" + rows(list(discarded), 0) + "\nMemory Configuration\n\n"
            "Linker script and memory map\n\n .text           0x00000000     0x1000\n *(.text.start)\n"
            + rows(entries, 0x8c))


def plants(script: str, order: str) -> list[tuple[str, str, str, str, str]]:
    """Each planted defect: its name, the rule that must refuse it, and the script, order and map it makes."""
    want = recorded(order)
    first, second = want[0], want[1]
    good_map = written_map(want)
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
    ]


def self_test(script: str, order: str) -> int:
    """The tree's files pass both rules on a map written from the order; every plant is refused by its rule."""
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
