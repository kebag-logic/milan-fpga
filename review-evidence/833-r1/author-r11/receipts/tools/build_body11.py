"""Build round 11's PR body from round 10's published body, its edits listed here, and the round 11 section.

usage: python3 -I build_body11.py PUBLISHED ROUND11 OUT
"""
import re
import sys
from pathlib import Path

published, round11, out = (Path(a) for a in sys.argv[1:4])
s = published.read_text().rstrip("\n") + "\n"
parts = re.split(r"(?m)^(?=## )", s)
by = {p.splitlines()[0]: p for p in parts}
LINK = "https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r{n}/PR-BODY.md#round-{n}"


def edit(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:80]
    return text.replace(old, new)


head = edit(parts[0], "[A726j]", "[A726k]")
contents = by["## Contents"]
contents = edit(contents, "- **[Rounds 2 to 8](#rounds-2-to-8)** — Links to each round's published section.\n",
                "- **[Rounds 2 to 9](#rounds-2-to-9)** — Links to each round's published section.\n")
contents = re.sub(r"- \*\*\[Round 9\]\(#round-9\)\*\*.*\n", "", contents)
contents = edit(contents, "- **[Definition of Done]",
                "- **[Round 11](#round-11)** — Round 10's findings with both review IDs: a stubborn parent from the "
                "first census beside a shell never resumed and under it, with its mutant, and the room for them; "
                "the exact RESIDUE wording; both reviewers' round 10 probes and sweeps; the gates.\n"
                "- **[Definition of Done]")
status = edit(by["## Status"],
              "head `fce77f0efc1425ef7732a8d70c02addc108f7afe` (round 10). Round 10's gates are in [Round 10](#round-10).",
              "head `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea` (round 11). Round 11's gates are in [Round 11](#round-11).")
status = edit(status, "Rounds 2 to 10 change only files", "Rounds 2 to 11 change only files")
roles = edit(by["## Linked Issue / roles"], "`[A726j]` (round 10)", "`[A726j]` (round 10), `[A726k]` (round 11)")
validate = edit(by["## How to validate"], "`owned-process mutants: PASS (149 mutants, 146 with a control that must fail)`",
                "`owned-process mutants: PASS (150 mutants, 147 with a control that must fail)`")
validate = edit(validate, "as in [Round 10 gates](#round-10-gates)", "as in [Round 11 gates](#round-11-gates)")
limits = edit(by["## Known limitations / out of scope"], "round 9 adds about 11 ms, and round 10 about 12 ms.",
              "round 9 adds about 11 ms, round 10 about 12 ms, and round 11 about 2 ms.")
rounds = edit(by["## Rounds 2 to 8"], "## Rounds 2 to 8", "## Rounds 2 to 9")
rounds = rounds.rstrip("\n") + "\n- [Round 9](" + LINK.format(n=9) + ")\n\n"
body = "".join([head, contents, status, roles, by["## Description"], by["## Authoritative references"],
                by["## How to get into the same state"], validate, limits, rounds, by["## Round 10"],
                round11.read_text().rstrip("\n") + "\n\n", by["## Definition of Done"]])
out.write_text(body)
print(len(body), "characters")
