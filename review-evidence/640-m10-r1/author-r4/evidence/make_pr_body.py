"""Build round 4's PR-BODY.md from round 3's. Usage: python3 -I make_pr_body.py <r3 body> <out> <head> <r3 head> <steps>"""
import sys
from pathlib import Path

src, out, head, r3head, steps = sys.argv[1:6]
t = Path(src).read_text(encoding="utf-8")


def sub(a, b):
    global t
    assert t.count(a) == 1, a[:70]
    t = t.replace(a, b)


sub("[A720m]\n", "[A720n]\n")
sub("- **[Round 3](#round-3)** -- The answer to R766-2-F1, one commit.\n",
    "- **[Round 3](#round-3)** -- The answer to R766-2-F1, one commit.\n"
    "- **[Round 4](#round-4)** -- The answer to R765-3-F1, one commit.\n")
sub(f"clean clone of head `{r3head}`, including both builder legs (55 recorded steps, all rc 0)",
    f"clean clone of head `{head}`, including both builder legs ({steps} recorded steps, all rc 0)")
sub("then `[A720m]` for round 3\n", "then `[A720m]` for round 3, then `[A720n]` for round 4\n")
sub("## Authoritative references\n", """## Round 4

R766-3 (issuecomment-6580971431) was POSITIVE. R765-3 (issuecomment-6580969269) was NEGATIVE on one MINOR, R765-3-F1: the stage table's stage 1 "Removes" cell still credited stage 1 with the BIOS ROM and SRAM and their measured 18 RAMB36, which the note, the census rows, lane 2's scope, the Block RAM ledger (M8a-1) and `AREA_BUDGET.md` book to the switch-over. One page changes: `docs/design/MARK_II_AREA_PLAN.md`, three lines.

| # | Findings | What changed |
|---|---|---|
| 14 | R765-3-F1 | Stage 1's "Removes" cell reads "LiteDRAM controller and PHY. The BIOS ROM and SRAM, 18 RAMB36 measured, already left at the switch-over (M8a-1)", linked to the firmware and block RAM ledger. Stage 1's "Change" cell keeps the owner's words, and the note now names it: "Stage 1's Change cell keeps the owner's words." |
| 14 | R765-3-F1, same cause | Stage 3's "Removes" cell credited stage 3 with "the generated FIFOs". The census says each leaves with the block that owns it, and none of the 29 belongs to a stage 3 row: 16 are DDR3's (stage 1), 5 the Ethernet MAC's (stage 2) and 8 the processor's memory-path crossings (switch-over), by the basis build's synthesis mapping. The cell now reads "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block", linked to the census. |

Every other per-stage RAMB36 or LUT credit was re-read and books nothing twice: stage 1's "Lever 1, ~1.0k LUTs" is lever 1's DDR3 drop, with no BIOS figure; stage 2's and stage 3's LUT credits split the -1.75k "beyond levers 1 and 2"; the lane table's savings match the stage table; the Block RAM ledger books the BIOS's 18 at the switch-over (M8a-1) and credits no generated FIFO to any stage; and "all 47 are gone once LiteX stage 3 ends" states a bound, not a stage credit. The census coverage check maps the same objects to the same rows as round 3 (PASS).

Not taken this round, by the round's limit: R765-3-R1 ("hold them" takes the BIOS as its object) and R765-3-S1 (where stage 1's loader runs). R765-2-RESIDUE-1 and -2 stay as residue.

## Authoritative references
""")
sub("- PR #835's round 2 reviews: R765-2 (issuecomment-6579373754) and R766-2 (issuecomment-6579449561).\n",
    "- PR #835's round 2 reviews: R765-2 (issuecomment-6579373754) and R766-2 (issuecomment-6579449561).\n"
    "- PR #835's round 3 reviews: R765-3 (issuecomment-6580969269) and R766-3 (issuecomment-6580971431).\n")
sub(f"git rev-parse HEAD        # {r3head}", f"git rev-parse HEAD        # {head}")
Path(out).write_text(t, encoding="utf-8")
