"""Build round 5's PR-BODY.md from round 4's. Usage: python3 -I make_pr_body.py <r4 body> <out> <head> <r4 head> <steps>"""
import sys
from pathlib import Path

src, out, head, r4head, steps = sys.argv[1:6]
t = Path(src).read_text(encoding="utf-8")


def sub(a, b):
    global t
    assert t.count(a) == 1, a[:70]
    t = t.replace(a, b)


sub("[A720n]\n", "[A720o]\n")
sub("- **[Round 4](#round-4)** -- The answer to R765-3-F1, one commit.\n",
    "- **[Round 4](#round-4)** -- The answer to R765-3-F1, one commit.\n"
    "- **[Round 5](#round-5)** -- The answer to R765-4-F1 / R766-4-F1 and three residues, one commit each.\n")
sub(f"clean clone of head `{r4head}`, including both builder legs (55 recorded steps, all rc 0)",
    f"clean clone of head `{head}`, including both builder legs ({steps} recorded steps, all rc 0)")
sub("then `[A720n]` for round 4\n", "then `[A720n]` for round 4, then `[A720o]` for round 5\n")
sub("and none of the 29 belongs to a stage 3 row:",
    "and none of the 29 RAMB36 belongs to a stage 3 row:")
sub('The cell now reads "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block", linked to the census. |',
    'The cell read "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block", linked to the census; round 5 narrows it to the 29 RAMB36. |')
sub("## Authoritative references\n", """## Round 5

R765-4 (issuecomment-6584004136) and R766-4 (issuecomment-6582620684) were both NEGATIVE on the same MINOR, R765-4-F1 / R766-4-F1. Stage 3's "Removes" cell said every generated FIFO leaves before stage 3. The census places the UART's FIFOs and the CSR crossing `milan_axil_cdc`'s (two RAMB18) at stage 3. One page changes: `docs/design/MARK_II_AREA_PLAN.md`, five lines, one commit each.

| # | Findings | What changed |
|---|---|---|
| 15 | R765-4-F1 / R766-4-F1 | Stage 3's "Removes" cell takes R766-4-F1's exact fix: "Wishbone and CSR-bank glue; the FIFOs of stage 3 blocks. The 29 generated FIFO RAMB36 leave earlier, each with its block", linked to the census. Neither the stage table nor the census now says stage 3 removes no generated FIFO. |
| 16 | R766-3-RESIDUE-2 / R765-3-R1 | The note under the stage table reads "Until stage 3, `ctrl_memory`'s banks hold both regions." "Them" no longer takes the BIOS as its object. |
| 17 | R765-2-RESIDUE-1 | The console UART text reads "Taking 10 ms as the gap gives 128 bytes." |
| 18 | R765-2-RESIDUE-2 | The split build's census fate reads "From stage 1, `rom` is filled from the flash copy, not the configuration image." |
| 19 | R765-4-S1 | Stage 1's "Removes" cell names the link's target: "(M8a-1, Mark I ledger)", with "Mark I ledger" linked to the firmware and block RAM ledger. M8a-1's -18 RAMB36 row exists only in the Mark I history ledger, and the page also has a current Mark II Block RAM ledger. |

No figure moves. The census coverage check is unchanged (PASS), and every fragment link in the stage table and its note resolves.

Not taken, optional: R765-3-S1 (where stage 1's loader runs), R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3 and R765-2-S4.

## Authoritative references
""")
sub("- PR #835's round 3 reviews: R765-3 (issuecomment-6580969269) and R766-3 (issuecomment-6580971431).\n",
    "- PR #835's round 3 reviews: R765-3 (issuecomment-6580969269) and R766-3 (issuecomment-6580971431).\n"
    "- PR #835's round 4 reviews: R765-4 (issuecomment-6584004136) and R766-4 (issuecomment-6582620684).\n")
sub(f"git rev-parse HEAD        # {r4head}", f"git rev-parse HEAD        # {head}")
Path(out).write_text(t, encoding="utf-8")
