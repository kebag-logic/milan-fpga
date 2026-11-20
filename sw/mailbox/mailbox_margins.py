# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""FR_NFR.md 3.4.1's response-margin table: the columns the contract decides (#917).

Each row of the table between the page's ``response-margins`` markers states a
numeric response deadline, the mailbox channel its command arrives on, its
timeout, the path's bound and ``T_egress``; the header states the proposal's
bound ("At the N ms proposal"). The rest is arithmetic on the contract, so
gen_mailbox.py writes it: ``T_ingress`` for a record that finds a token
(``T_INGRESS_MS``, as the channel table states it), the margin left for
``T_network`` at the bound and at the proposal's bound, and the same three for a
record its channel's bucket holds, whose ``T_ingress`` is its channel's
``refill_ms`` and ``T_INGRESS_MS``. ``--write`` rewrites those cells; ``--check``
names every row whose cells differ, and every margin that is not positive, since
FR_NFR requires ``T_ingress + T_svc + T_egress + T_network < timeout``.
"""

from __future__ import annotations

import re

from mailbox_emit import T_INGRESS_MS
from mailbox_model import Contract

#: The page, and the markers around its table.
PAGE = "docs/reference/FR_NFR.md"
START = "<!-- response-margins:start -->\n"
END = "\n<!-- response-margins:end -->"

PROPOSAL = re.compile(r"At the (\d+) ms proposal")
MS = re.compile(r"^(\d+) ms$")
CHANNEL = re.compile(r"^`(\w+)`$")
#: The cells a row states: its deadline, channel, timeout, bound and T_egress; the six after them are written.
STATED, WRITTEN = 5, 6


class MarginError(ValueError):
    """The page's table cannot be read: no markers, an unknown channel, a cell that is not whole milliseconds."""


def row_cells(line: str) -> list[str]:
    """A table row's cells."""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _ms(cell: str, what: str, label: str) -> int:
    """A cell of whole milliseconds."""
    m = MS.match(cell)
    if not m:
        raise MarginError(f"{PAGE}: '{label}': its {what} {cell!r} is not a whole number of ms")
    return int(m[1])


def _row(contract: Contract, proposal: int, line: str) -> list[str]:
    """One row, its written cells computed from its stated ones and the contract."""
    cells = row_cells(line)
    if len(cells) != STATED + WRITTEN:
        raise MarginError(f"{PAGE}: a margin row has {len(cells)} cells, want {STATED + WRITTEN}: {line[:60]}")
    label, channel = cells[0], cells[1]
    m = CHANNEL.match(channel)
    rates = {ch.name: ch.refill_ms for ch in contract.channels}
    if not m or m[1] not in rates:
        raise MarginError(f"{PAGE}: '{label}': {channel!r} names no channel of the contract")
    timeout, bound, egress = (_ms(c, w, label) for c, w in zip(cells[2:5], ("timeout", "bound", "T_egress")))
    held = rates[m[1]] + T_INGRESS_MS
    figures = [T_INGRESS_MS, timeout - bound - egress - T_INGRESS_MS, timeout - proposal - egress - T_INGRESS_MS,
               held, timeout - bound - egress - held, timeout - proposal - egress - held]
    return cells[:STATED] + [f"{v} ms" for v in figures]


def split_page(page: str) -> tuple[str, list[str], str]:
    """The page before its table, the table's lines, and the page after it."""
    head, found, rest = page.partition(START)
    body, closed, tail = rest.partition(END)
    if not found or not closed:
        raise MarginError(f"{PAGE}: no table between {START.strip()} and {END.strip()}")
    return head, body.split("\n"), tail


def splice(contract: Contract, page: str) -> str:
    """The page with its margin table's written cells as the contract gives them."""
    head, lines, tail = split_page(page)
    m = PROPOSAL.search(lines[0])
    if not m:
        raise MarginError(f"{PAGE}: the margin table's header states no 'At the N ms proposal'")
    rows = ["| " + " | ".join(_row(contract, int(m[1]), line)) + " |" for line in lines[2:]]
    return head + START + "\n".join(lines[:2] + rows) + END + tail


def findings(contract: Contract, page: str) -> list[str]:
    """Every row whose written cells differ from the contract's, by its deadline, and every margin it leaves
    that is not positive; a table that cannot be read is one finding."""
    try:
        want = split_page(splice(contract, page))[1][2:]
    except MarginError as exc:
        return [str(exc)]
    out = []
    for got, new in zip(split_page(page)[1][2:], want):
        label, cells = row_cells(new)[0], row_cells(new)[STATED:]
        if got != new:
            out.append(f"{PAGE}: '{label}' reads {' / '.join(row_cells(got)[STATED:])}, the contract gives "
                       f"{' / '.join(cells)}; run gen_mailbox.py --write")
        out += [f"{PAGE}: '{label}' leaves no margin: {cell}" for cell in (cells[1], cells[2], cells[4], cells[5])
                if int(cell.split()[0]) <= 0]
    return out
