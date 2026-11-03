"""Build round 10's PR body from round 9's published body, its edits listed here, and the round 10 section.

usage: python3 -I build_body10.py PUBLISHED ROUND10 OUT
"""
import re
import sys
from pathlib import Path

published, round10, out = (Path(a) for a in sys.argv[1:4])
s = published.read_text().rstrip("\n") + "\n"
parts = re.split(r"(?m)^(?=## )", s)
by = {p.splitlines()[0]: p for p in parts}
LINK = "https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r{n}/PR-BODY.md#round-{n}"


def edit(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:80]
    return text.replace(old, new)


head = edit(by["[A726i]\n\n"] if "[A726i]\n\n" in by else parts[0], "[A726i]", "[A726j]")
contents = by["## Contents"]
contents = edit(contents, "- **[Rounds 2 to 7](#rounds-2-to-7)** — Links to each round's published section.\n",
                "- **[Rounds 2 to 8](#rounds-2-to-8)** — Links to each round's published section.\n")
contents = re.sub(r"- \*\*\[Round 8\]\(#round-8\)\*\*.*\n", "", contents)
contents = edit(contents, "- **[Definition of Done]",
                "- **[Round 10](#round-10)** — Round 9's findings with both review IDs: `owner_report`'s child asleep "
                "with no timer; early listings, which list a new descendant a tick after the first pass; a live new "
                "descendant beside a shell never resumed; R764-9-S1's three listings; the listing-time domain; the "
                "residue, the sweeps and the gates.\n- **[Definition of Done]")
status = edit(by["## Status"],
              "head `e803d94b3a11921a293cf036a8eda333d23828f9` (round 9). Round 9's gates are in [Round 9](#round-9).",
              "head `fce77f0efc1425ef7732a8d70c02addc108f7afe` (round 10). Round 10's gates are in [Round 10](#round-10).")
status = edit(status, "Rounds 2 to 9 change only files", "Rounds 2 to 10 change only files")
roles = edit(by["## Linked Issue / roles"], "`[A726i]` (round 9)", "`[A726i]` (round 9), `[A726j]` (round 10)")
description = edit(by["## Description"],
                   "the starved owner's clock that `owner_stated_seconds` runs on (round 8), with its matrix's classes "
                   "and its stated window (round 9) |",
                   "the starved owner's clock that `owner_stated_seconds` runs on (round 8), with its matrix's classes "
                   "and its stated window (round 9), a census a listing states, and the reused-identity control's "
                   "child script (round 10) |")
validate = edit(by["## How to validate"], "`owned-process mutants: PASS (142 mutants, 139 with a control that must fail)`",
                "`owned-process mutants: PASS (149 mutants, 146 with a control that must fail)`")
validate = edit(validate, "as in [Round 9 gates](#round-9-gates)", "as in [Round 10 gates](#round-10-gates)")
limits = edit(by["## Known limitations / out of scope"], "rounds 7 and 8 add no measurable time, and round 9 adds about 11 ms.",
              "rounds 7 and 8 add no measurable time, round 9 adds about 11 ms, and round 10 about 12 ms.")
rounds = edit(by["## Rounds 2 to 7"], "## Rounds 2 to 7", "## Rounds 2 to 8")
rounds = rounds.rstrip("\n") + "\n- [Round 8](" + LINK.format(n=8) + ")\n\n"
body = "".join([head, contents, status, roles, description, by["## Authoritative references"],
                by["## How to get into the same state"], validate, limits, rounds, by["## Round 9"],
                round10.read_text().rstrip("\n") + "\n\n", by["## Definition of Done"]])
out.write_text(body)
print(len(body), "characters")
