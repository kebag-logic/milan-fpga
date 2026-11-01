"""Build round 9's PR body from round 8's, with exact-text replacements; each must match once."""
import sys
SRC = "$MANAGEMENT/2026-09-23/640-a720h/PR-BODY.md"
OUT = "$MANAGEMENT/2026-09-23/640-a720i/PR-BODY.md"
HEAD = "d63b378d27c1c663034744a5b48a99c190271f58"
s = open(SRC, encoding="utf-8").read()

def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected one match, got {n}: {old[:80]!r}")
    s = s.replace(old, new)

sub("[A720h]\n\n## Contents", "[A720i]\n\n## Contents")
sub("the pass rule and the reached cases corrected.\n",
    "the pass rule and the reached cases corrected.\n"
    "- **[Round 9](#round-9)** -- Pages this PR had not touched brought into line with it, with a docs-tree sweep.\n")
sub("clean clone of head `20933ef48a9b174e58a9d17ddd59078a072024af`", f"clean clone of head `{HEAD}`")
sub("Round 8 answers R757-7 (NEGATIVE at `e7310e94`, one MINOR) and R758-7 (POSITIVE at `e7310e94`, one residue item). Round 7 applied",
    "Round 9 answers [R757-9](https://github.com/kebag-logic/milan-fpga/pull/828#issuecomment-6563425814) (NEGATIVE, two MINOR findings on pages this PR had not touched). Round 8 answered R757-7 (NEGATIVE at `e7310e94`, one MINOR) and R758-7 (POSITIVE at `e7310e94`, one residue item). Round 7 applied")
sub("With fewer reservations it does not either, and no maximum is derived:",
    "With fewer reservations some cases exceed it, and no maximum is derived:")
sub("Executor: `[A720i]`" if False else "Executor: `[A720h]` (round 1:", "Executor: `[A720i]` (round 1:")
sub("round 7: `[A720g]`)", "round 7: `[A720g]`; round 8: `[A720h]`)")
sub("| `20933ef4` | stream engines | The fixed-terms line kept within the sentence limit; the probe pointer says it reports the reached cases. |\n",
    "| `20933ef4` | stream engines | The fixed-terms line kept within the sentence limit; the probe pointer says it reports the reached cases. |\n"
    "| `2515b51f` | area budget | R757-9-F1: NFR-RES-01's Mark II ceiling is the target row and the active acceptance bar; 60 percent and 38,040 stay only as marked history; the shipping image shows no other LUT bound. |\n"
    "| `7e10647c` | 14 pages | R757-9-F2 and the sweep: each page states the transition and end state or points at the split contract; today's facts stay, scoped until the switch-over or F6. |\n"
    "| `26885333` | stream engines | R758-8-R1: the 192 kHz row is low, and why. |\n"
    "| `d63b378d` | area plan | R758-8-R2: only some fewer-reservations cases exceed the target. |\n")
sub("  Fewer reservations are worse, and no maximum is derived for them.",
    "  Some cases with fewer reservations are worse, and no maximum is derived for them.")
sub("## Authoritative references\n\n- #640 body",
"""## Round 9

[R757-9](https://github.com/kebag-logic/milan-fpga/pull/828#issuecomment-6563425814) is NEGATIVE with two MINOR findings. PR #828 amends requirements, and pages it had not touched still stated the old contract. The charter's own decisions and figures do not change, and no measured or gate-read figure moves. The lane handoff carries file, line and verification.

| Item | Closure |
|---|---|
| R757-9-F1, area budget | The target statement and the target row give the Mark II ceiling, fewer than 20,000 LUTs. The active #640 acceptance bar reads the same. The shipping row reads "fits; no other LUT bound on this image". 60 percent, 38,040, 37,659, 13,972 and 10,521 survive only in passages marked as replaced. The Mark II planning ledger is marked as the Mark I plan, as the area plan marks its own copy. The M9 row and re-record rule name the Mark II ceiling. |
| R757-9-F1, gates | The resource gate's `check-baseline` reads only the budget's endpoint policy table, which is unchanged, and it passes. No gate reads the figures this round re-marked. |
| R757-9-F2, listed pages | README.md, the solution overview, the AXI-Stream boundary page and the budget's ledger state the transition and end state as the architecture overview does. The glossary row says firmware serves AECP after the switch-over. The six pages that shared one header point at the split contract, keeping "stays the shipping default until F2 to F5 acceptance". |
| Sweep, same claim on other lines or pages | `docs/ENDSTATION_BUILDER.md` and `docs/integration/INTEGRATION_GUIDE.md` (selectable placement; gPTP interfaces); `docs/design/GPTP_PLANE.md` and the glossary's gPTP row (sole owner, now until F6); `docs/traceability/ieee8021q.md`'s "permits firmware placement"; the boundary page's "gPTP progress" line; the budget's "Unqualified functions retain fabric placement", which is removed. |
| Sweep, left unchanged | Dated records (`docs/history`, `docs/findings`, `CHANGELOG.md`); the area plan's marked Mark I history; lines already bounded "until" or "before the default changes", such as the mailbox page and the compliance matrix; "both placements" lines that hold until the switch-over; today's build facts such as the `--fabric-gptp` option. The handoff lists each with its reason. |
| R758-8-R1 | The stream-engine page reads "Its 192 kHz search was a random walk." "It left out eight-channel streams." and "Larger cases exist, so that row is low." |
| R758-8-R2 | The area plan's two rows and this body's status read "some cases". This body's key results and known limitation say the same, beyond the three lines the residue names. |
| Not taken | R757-9 S1 and S2, and R757-8-R1 and R757-8-R2, are outside this assignment. R757-8-R1's point on the 96 kHz row stays open: the page's general "None is a maximum" covers that row. R757-7 RR13 is the manager's, on the issue body. |
| CI scope | This head now changes `docs/design/AREA_BUDGET.md`, a gate-read page. So `scripts/ci_scope.py` classifies the PR as relevant rather than docs-only, and the exact-head long gates apply to it. The local candidate's "Only Markdown" reason for jobs not run needs review. |

## Authoritative references

- R757-9-F1 and F2; `docs/reference/FR_NFR.md` NFR-RES-01, `REQUIREMENTS.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md` and `docs/overview/ARCHITECTURE.md`, which the changed pages follow.
- #640 body""")
sub("# forty commits: one per file group or finding group, and the dev merge",
    "# forty-four commits: one per file group or finding group, and the dev merge")
sub("Recorded at `20933ef4` (every step", "Recorded at `d63b378d` (every step")
sub("em dash (0 over 1,792 added lines in 7 pages)", "em dash (0 over 1,906 added lines in 21 pages)")
sub("over every changed block of the 7 touched pages: 0 findings", "over every changed block of the 21 touched pages: 0 findings")
sub("- **Talker latency with mixed formats or fewer reservations is above the 65 µs target, by accepted decision.**",
    "- **Talker latency with mixed formats, and in some cases with fewer reservations, is above the 65 µs target, by accepted decision.**")
open(OUT, "w", encoding="utf-8").write(s)
