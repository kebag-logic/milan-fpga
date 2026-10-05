#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #652: the design page's section 4.2 allocation table, read against
the inventory `check_nvm_record_space.py` derives (its check 14).

The page states the record allocation at two shipped shapes. Every figure in
its two shape columns is compared with the census the gate derives for those
shapes, every block with `ALLOC`, and a row that does not carry one cell per
header column is a finding of its own. The page text passes through
`SEAM.ALLOCATION_PAGE_EDIT`, the seam the gate's allocation-table negative
controls plant through.
"""

from __future__ import annotations

import re

from nvm_contract import ALLOC, ROOT, SEAM


#: Section 4.2 of the design page states the allocation at two shipped shapes.
#: Its columns are these configurations, and every figure in them is checked
#: against the inventory the gate derives for them, so the page cannot carry a
#: count the shapes no longer have (#652).
ALLOCATION_PAGE = ROOT / "docs" / "design" / "SAVED_STATE_FASTCONNECT.md"
ALLOCATION_HEAD = "| ids | group | block | index | 1x1 | 8x8 |"
ALLOCATION_COLUMNS = {"1x1": "endstation_ax7101_1x1_tdm8",
                      "8x8": "endstation_ax7101_8x8"}


def _allocation_cells(line: str) -> list[str]:
    """One table line's cells, without emphasis or code marks."""
    return [cell.strip().replace("*", "").replace("`", "")
            for cell in line.strip().strip("|").split("|")]


def _allocation_rows(page: str) -> list[list[str]]:
    """The allocation table's body rows, as cells; none when the page has no
    single table under ALLOCATION_HEAD."""
    lines = page.splitlines()
    if lines.count(ALLOCATION_HEAD) != 1:
        return []
    rows = []
    for line in lines[lines.index(ALLOCATION_HEAD) + 2:]:
        if not line.startswith("|"):
            break
        rows.append(_allocation_cells(line))
    return rows


def _allocation_width(where: str, head: list[str], row: list[str]) -> str:
    """The finding for a body row without one cell per header column: the
    columns it has no figure for, or the cells it carries past the last."""
    what = " ".join(cell for cell in row[:2] if cell) or "a blank row"
    shape = f"{len(row)} cells under a {len(head)}-column header"
    if len(row) < len(head):
        return f"{where}: {what} has no {', '.join(head[len(row):])} figure ({shape})"
    return (f"{where}: {what} has {len(row) - len(head)} cell(s) past the "
            f"{head[-1]} column ({shape})")


def _allocation_want(census: dict, ids: str, group: str | None) -> str:
    """The figure one allocation-table cell must read at one shape."""
    if group is not None:
        return str(census["counts"][group])
    if ids == "records":
        return str(census["records"])
    if ids == "highest id":
        return f"0x{census['top']:02X}"
    return "--"


def allocation_findings(census: dict, base: int) -> list[str]:
    """Every figure of the design page's section 4.2 allocation table that is
    not the derived one: each group's block, its record count at each
    column's shape, the record total and the highest id. A row without one
    cell per header column is a finding of its own, never a shorter
    comparison: a figure dropped from the table is not a figure checked."""
    where = f"{ALLOCATION_PAGE.relative_to(ROOT)} section 4.2"
    absent = [s for s in ALLOCATION_COLUMNS.values() if s not in census]
    if absent:
        return [f"{where}: no inventory for {absent}, the shapes its columns state"]
    page = ALLOCATION_PAGE.read_text(encoding="utf-8")
    if SEAM.ALLOCATION_PAGE_EDIT is not None:
        page = SEAM.ALLOCATION_PAGE_EDIT(page)
    rows = _allocation_rows(page)
    if not rows:
        return [f"{where}: no single allocation table headed {ALLOCATION_HEAD!r}"]
    by_base = {(base if group == "BINDING" else b): group
               for group, (b, _block) in ALLOC.items()}
    head = _allocation_cells(ALLOCATION_HEAD)
    findings, seen = [], set()
    for row in rows:
        first = re.match(r"0x([0-9A-Fa-f]{2})", row[0])
        group = by_base.get(int(first.group(1), 16)) if first else None
        if group is not None:
            seen.add(group)
        if len(row) != len(head):
            findings.append(_allocation_width(where, head, row))
            continue
        ids, label, block, _index, *cells = row
        for (column, stem), cell in zip(ALLOCATION_COLUMNS.items(), cells,
                                        strict=True):
            want = _allocation_want(census[stem], ids, group)
            if cell != want:
                findings.append(f"{where}: {column} {label or ids} reads "
                                f"{cell}, the {stem} inventory derives {want}")
        if group is not None and block != str(ALLOC[group][1]):
            findings.append(f"{where}: {label} block reads {block}, the "
                            f"allocation holds {ALLOC[group][1]}")
    if set(ALLOC) - seen:
        findings.append(f"{where}: no row for {sorted(set(ALLOC) - seen)}")
    return findings
