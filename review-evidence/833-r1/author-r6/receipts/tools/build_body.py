#!/usr/bin/env python3
"""Build round 6's PR body from round 5's and the round 6 section.

usage: python3 -I -B build_body.py <round 5 body> <round 6 section> <gates table> <head> <out>
"""
import sys
from pathlib import Path

base, section, gates, head, out = sys.argv[1:6]
text = Path(base).read_text()
round6 = Path(section).read_text().replace("HEAD_SHA", head).replace("GATES_TABLE", Path(gates).read_text().strip())


def swap(old: str, new: str) -> None:
    """Replace one exact passage of the body, which must occur once."""
    global text
    assert text.count(old) == 1, old[:80]
    text = text.replace(old, new)


swap("[A726e]\n", "[A726f]\n")
swap("- **[Round 5](#round-5)** — Round 4's one test gap and its class: every published mutant against every control, "
     "the stated behaviours each pinned, the list's home, and the gates.\n",
     "- **[Round 5](#round-5)** — Round 4's one test gap and its class: every published mutant against every control, "
     "the stated behaviours each pinned, the list's home, and the gates.\n"
     "- **[Round 6](#round-6)** — Round 5's findings with both review IDs: the shell-window hold bounded on both sides, "
     "the stated cleanup contract as a table with each row's control and mutants, the five gaps pinned, an own mutant per "
     "row, and the gates.\n")
swap("head `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` (round 5). Round 5's gates are in [Round 5](#round-5).",
     f"head `{head}` (round 6). Round 6's gates are in [Round 6](#round-6).")
swap("Rounds 2 to 5 change only files round 1 changed", "Rounds 2 to 6 change only files round 1 changed")
swap("`[A726e]` (round 5)\n", "`[A726e]` (round 5), `[A726f]` (round 6)\n")
swap("`owned-process mutants: PASS (43 mutants, 42 with a control that must fail)`; `mutant lifecycle: PASS`",
     "`owned-process mutants: PASS (74 mutants, 70 with a control that must fail)`; `mutant lifecycle: PASS`")
swap("as in [Round 5 gates](#round-5-gates)", "as in [Round 6 gates](#round-6-gates)")
swap("and round 5 adds about 1.5 s: 1.4 s to the shell-window control and 0.1 s for two new controls.",
     "round 5 adds about 1.5 s: 1.4 s to the shell-window control and 0.1 s for two new controls, and round 6 adds "
     "about 0.2 s: the report control's 0.1 s pause and the reused-identity control's second process.")
swap("### The class: every published mutant\n\n",
     "### The class: every published mutant\n\n"
     "Round 6 replaces this section's table with [the stated cleanup contract](#the-stated-cleanup-contract), which "
     "states every cleanup behaviour with its control. Line numbers in this section are `TESTING.md` at `a67eaf66`.\n\n")
start = text.index("### Round 5 mutation table\n")
end = text.index("### R764-4-S1: derived, not widened\n")
text = (text[:start] + "### Round 5 mutation table\n\n"
        "Round 5 ran every mutant at round 4's head and at its own, through one driver: 506 `--matrix` runs at "
        "`a67eaf66`, each in its own user and PID namespace. At `c1b29617`, the 10 named above were green on every "
        "control and on the whole test. Its table is `review-evidence/833-r1/author-r5/receipts/matrix/matrix-table.md` "
        "on branch `833-review-evidence`. The [Round 6 mutation table](#round-6-mutation-table) re-runs every row at "
        "this head.\n\n" + text[end:])
start = text.index("Per control, at this head (`ok` passes")
end = text.index("The new reds and their failing words:")
text = (text[:start] + "Both of round 2's tables, per control and through R764-1's driver, are in "
        "`review-evidence/833-r1/author-r2/PR-BODY.md` on branch `833-review-evidence`. The "
        "[Round 6 mutation table](#round-6-mutation-table) re-runs every mutant in them at this head.\n\n" + text[end:])
start = text.index("R764-1's driver, whole test per mutant:\n")
end = text.index("### Round 2 gates\n")
text = text[:start] + text[end:]
swap("## Definition of Done\n", round6.rstrip() + "\n\n## Definition of Done\n")
Path(out).write_text(text)
print(len(text), "characters")
