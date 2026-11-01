"""Build round 6's PR body from round 5's, with exact-text replacements; each must match once."""
import sys
SRC = "$MANAGEMENT/2026-09-23/640-a720e/PR-BODY.md"
OUT = "$MANAGEMENT/2026-09-23/640-a720f/PR-BODY.md"
HEAD = "3f5fea241e8dacd976798ca817c67e55096cf1aa"
EV = "https://github.com/kebag-logic/milan-fpga/blob/f9cfe08cd3f526acde88e0d2a1c48ed2740583df/review-evidence/640-m9-r1/reviews/R758-5"
s = open(SRC, encoding="utf-8").read()

def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected one match, got {n}: {old[:80]!r}")
    s = s.replace(old, new)

sub("[A720e]\n\n## Contents", "[A720f]\n\n## Contents")
sub("- **[Round 5](#round-5)** -- How each round-4 finding was closed: the tu merge reduced to requirements.\n",
    "- **[Round 5](#round-5)** -- How each round-4 finding was closed: the tu merge reduced to requirements.\n"
    "- **[Round 6](#round-6)** -- How R758-5-F1 and the round-5 residue were closed: the short-margin limit stated and owned.\n")
sub("clean clone of head `270866ecb95155ef48428ec3a049c357f7eae946`", f"clean clone of head `{HEAD}`")
sub("Round 5 answers R757-4 and R758-4 (both NEGATIVE at `22f3cedb`, MINOR findings only). ",
    "Round 6 answers R757-5 (POSITIVE at `270866ec`, residue only) and R758-5 (NEGATIVE at `270866ec`, one MINOR). ")
sub("Executor: `[A720e]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`)",
    "Executor: `[A720f]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`; round 5: `[A720e]`)")

# RR10.
sub("duplicates counted exactly; the merge registers. |",
    "duplicates counted exactly; the merge registers. The tu text left in round 5. |")
sub("| `270866ec` | stream engines | TU-2 says a clean copy renders as the rules place it, so a discarded duplicate breaks nothing; case B takes the model's latency. |\n",
    "| `270866ec` | stream engines | TU-2 says a clean copy renders as the rules place it, so a discarded duplicate breaks nothing; case B takes the model's latency. |\n"
    "| `872ff20e` | stream engines | A margin under 125 µs lapses the head every packet, so interleaved copies can land one sample apart; the placement and Annex D.2 claims hold under a valid head; open design item 3 for lane 6. |\n"
    "| `3f5fea24` | stream engines | Residue: TU-4 names a stream starting with tu, unpaired or on both networks; rule 2 restarts the map with only bit 0 set. |\n")

# The round-3 row states the placement claim the page now conditions.
sub("Samples are placed by count from the head, so the error never shifts a sample. A copy with tu set",
    "Samples are placed by count from the head, so the error never shifts a sample (round 6 conditions this on a valid head). A copy with tu set")

# RR8.
sub("TU-4 requires that an unpaired stream starting with tu still renders, with the lane stating how.",
    "TU-4 requires that a stream starting with tu still renders, unpaired or on both networks, with the lane stating how.")

sub("## Authoritative references\n", f"""## Round 6

R757-5 was POSITIVE with three residue items. R758-5 was NEGATIVE with one MINOR and one residue item. The manager took R758-5-F1's second outcome, which adds no mechanism: the merge rules do not change. No latency, save, area or Block RAM figure moves. The lane handoff carries file, line and verification.

| Finding | Closure |
|---|---|
| R758-5-F1 | The placement line reads "Under a valid head, conversion error never shifts a sample." After the "A new anchor" line the page adds "A margin under 125 µs lapses the head every packet." and "Interleaved copies can then land one sample apart." The Annex D.2 claim carries the same condition: "Under a valid head, clean copies keep that external behaviour." Open design item 3, for lane 6, states the requirement and its verification: clean copies on both networks 10 to 50 µs before their time, first arrival interleaved, at 48, 96 and 192 kHz, every grid phase; the test fails on a shift beyond what the lane states. The reviewer's [published probe]({EV}/scripts/probe_margin_r5.py) is the starting case. Its [output]({EV}/receipts/model/probe_margin_r5.out) (up to 766 shifts and 383 unwritten samples in 2,000 packets) is stated as the probe's result, not as a design figure. A re-run of the probe prints the same output. |
| R757-5 RR8, R758-5-R1 | TU-4 reads "A stream that starts with tu, unpaired or on both networks, still renders." The two reviews word this differently and mean the same; RR8's wording is the one applied, since it also gives the matching text for this body's Round 5 row. |
| R757-5 RR9 | Rule 2 reads "it anchors the head and restarts the map with only bit 0 set". |
| R757-5 RR10 | Commit row `07f8eb91` ends "The tu text left in round 5." |
| Suggestions | R757-5 S8 to S13 and R758-5 S1 to S4 are not taken: this round touches only the assigned text. R757-5 S9 is the one-network form of the same lapse, and R757-5 asks the manager to carry it to lane 6. Item 3 names both networks, as assigned. The page's "the pair loses no samples" is unchanged: R758-5 finds it holds, and S9 reads it as too strong in that regime. |

The Round 3 row above says "never shifts a sample"; it now notes the condition.

## Authoritative references
""")

sub("thirty-four commits: one per file group or finding group, and the dev merge", "thirty-six commits: one per file group or finding group, and the dev merge")
sub("Recorded at `270866ec` (every step", "Recorded at `3f5fea24` (every step")
sub("- The render-span edges are open design item 1 for the same lane.\n",
    "- The render-span edges are open design item 1 for the same lane.\n"
    "- **Short margin on both networks:** a margin under 125 µs lapses the head every packet, so interleaved clean copies can land one sample apart; open design item 3 for the same lane sets the allowed shift, and this PR states none.\n")
sub("em dash (0 over 1,748 added lines in 7 pages)", "em dash (0 over 1,754 added lines in 7 pages)")
open(OUT, "w", encoding="utf-8").write(s)
