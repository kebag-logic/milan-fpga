"""Build round 7's PR body from round 6's, with exact-text replacements; each must match once."""
import sys
SRC = "$MANAGEMENT/2026-09-23/640-a720f/PR-BODY.md"
OUT = "$MANAGEMENT/2026-09-23/640-a720g/PR-BODY.md"
HEAD = "e7310e94fff7188c5800a94c03a3f0e4c7c1c024"
D = "https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030"
s = open(SRC, encoding="utf-8").read()

def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected one match, got {n}: {old[:80]!r}")
    s = s.replace(old, new)

sub("[A720f]\n\n## Contents", "[A720g]\n\n## Contents")
sub("the short-margin limit stated and owned.\n",
    "the short-margin limit stated and owned.\n"
    "- **[Round 7](#round-7)** -- The owner's 2026-11-01 decisions applied, and the round-6 residue closed.\n")
sub("clean clone of head `3f5fea241e8dacd976798ca817c67e55096cf1aa`", f"clean clone of head `{HEAD}`")

# The approval, and the talker statement.
sub("Round 6 answers R757-5 (POSITIVE at `270866ec`, residue only) and R758-5 (NEGATIVE at `270866ec`, one MINOR). The requirement text (NFR-RES-01, NFR-LAT-03, NFR-REL-03, the NFR-SCOUT-02/03/05 amendments and the REQUIREMENTS.md scoping) needs owner approval before merge.",
    f"Round 7 applies the [owner decisions of 2026-11-01]({D}) and the residue of R757-6 and R758-6 (both POSITIVE at `3f5fea24`). The owner approved the requirement text (NFR-RES-01, NFR-LAT-03, NFR-REL-03, the NFR-SCOUT-02/03/05 amendments and the REQUIREMENTS.md scoping) as reviewed at `3f5fea24`, with NFR-LAT-03's \"MUST be below 65 µs\" restated as a target by the same decision.")
sub("The talker latency target is met by the design only when each port carries 16 reservations of one base format. With mixed channel counts, or with fewer reservations, it is not met; that is an open owner question, not a claim.",
    "65 µs is a target; it does not bind every legal stream setup. The design meets it when each port carries 16 reservations of one base format. With mixed channel counts, or with fewer reservations, it does not; the owner accepted those derived bounds, which stay published. No connection is refused because of them, and no restriction to one base format applies.")
sub("- **Talker latency at 16 reservations per port** (derived bound, pin to first bit, one interfering 1522-octet frame):",
    "- **Talker latency at 16 reservations per port** (derived bound against the 65 µs target, pin to first bit, one interfering 1522-octet frame):")
sub("with three co-phased eight-channel streams the bound is 123.337 µs. Both cases are open owner question 1.",
    "with three co-phased eight-channel streams the bound is 123.337 µs. The owner accepted both cases' bounds on 2026-11-01.")

# Executor and commits.
sub("Executor: `[A720f]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`; round 5: `[A720e]`)",
    "Executor: `[A720g]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`; round 5: `[A720e]`; round 6: `[A720f]`)")
sub("| `872ff20e` | stream engines | A margin under 125 µs lapses the head every packet, so interleaved copies can land one sample apart; the placement and Annex D.2 claims hold under a valid head; open design item 3 for lane 6. |",
    "| `872ff20e` | stream engines | A margin under 125 µs lapses the head every packet, so interleaved copies can land one sample apart (round 7 rewords this: about 125 µs, on both networks); the placement and Annex D.2 claims hold under a valid head; open design item 3 for lane 6. |")
sub("rule 2 restarts the map with only bit 0 set. |\n",
    "rule 2 restarts the map with only bit 0 set. |\n"
    "| `7b3121d2` | FR_NFR.md, stream engines, area plan | NFR-LAT-03 restated as a 65 µs target, with the bounds accepted and what the bench records; open question 1 removed and the decision stated once on the design page; the D14 and target rows agree. |\n"
    "| `e7310e94` | stream engines | Residue: a margin under about 125 µs on both networks lapses the head; the threshold carries the conversion error. |\n")

# History rows that would otherwise read as current.
sub('| R757-2 RR1 | This body: "(open questions 1 and 7)". |',
    '| R757-2 RR1 | This body: "(open questions 1 and 7)". Round 7 answers question 1 and renumbers question 7 to 6. |')
sub("S5 and S1 ask for one clause in NFR-REL-03, which waits for the owner's requirement approval.",
    "S5 and S1 ask for one clause in NFR-REL-03, which waited for the owner's requirement approval (round 7: approved as reviewed, without that clause).")
sub('the page adds "A margin under 125 µs lapses the head every packet." and "Interleaved copies can then land one sample apart."',
    'the page adds "A margin under 125 µs lapses the head every packet." (round 7 rewords this line) and "Interleaved copies can then land one sample apart."')

sub("## Authoritative references\n", f"""## Round 7

R757-6 and R758-6 were both POSITIVE at `3f5fea24`, with one residue item each. The [owner decisions of 2026-11-01]({D}) answer the talker question and approve the requirement text. Nothing else changes, and no latency, save, area or Block RAM figure moves. The lane handoff carries file, line and verification.

| Item | Closure |
|---|---|
| Owner: 65 µs is a target | NFR-LAT-03 reads "SHOULD be below 65 µs, and as short as possible", cites the decision and takes priority S, the file's mark for SHOULD. Its interval, derivation pointer, figures and verification method stay. Its last sentences read "Those derived bounds are accepted and published, and no connection is refused because of them." and "The bench measures against the target and reports each case; a case above 65 µs that stays inside its published bound is not a failure." |
| Owner: open question 1 is answered | The question is gone from the design's list, and the remaining six are numbered 1 to 6. The decision is stated once, under "Talker latency budget". The bounds tables are unchanged. The pointer after them now reads "the owner's decision accepts their bounds". The pointer under the save bound stays as it was: it names a burst beyond S1, which is still open, now as question 1. |
| Owner: requirement text approved | The Status section records the approval. |
| Area plan | The target row and D14 agree: a target, those bounds accepted and published, no connection refused. |
| R757-6 RR11, R758-6-R1 | The design's line reads "Both copies' margins under about 125 µs lapse every head." and "The threshold carries the conversion error, so it is approximate." Open design item 3 reads "A margin under about 125 µs on both networks lapses the head before the next packet" and "within that error of 125 µs, only some packets lapse". The limitation below says the same. The two reviews' exact texts differ, so the closure carries both points. |
| Suggestions | R757-6 S14 to S16 and R758-6 S1 to S4 are not taken: this round touches only the assigned text. |

## Authoritative references
""")
sub("- #640 body (\"Updated 2026-10-31\") and comments of 2026-10-31;", "- #640 body (\"Updated 2026-10-31\"), comments of 2026-10-31 and the owner decisions of 2026-11-01;")

sub("thirty-six commits: one per file group or finding group, and the dev merge", "thirty-eight commits: one per file group or finding group, and the dev merge")
sub("Recorded at `3f5fea24` (every step", "Recorded at `e7310e94` (every step")
sub("em dash (0 over 1,754 added lines in 7 pages)", "em dash (0 over ADDED added lines in 7 pages)")

# Known limitations.
sub("- **Open owner question 1: talker latency with mixed formats or fewer reservations.** The phase rule",
    "- **Talker latency with mixed formats or fewer reservations is above the 65 µs target, by accepted decision.** The phase rule")
sub("The owner called 65 µs ideal; the choices include accepting the derived bounds, one base format per port, re-phasing with an audio gap, or another stagger or shape.",
    "The owner decided on 2026-11-01 that 65 µs is a target: the derived bounds are accepted and stay published, no connection is refused because of them, and no restriction to one base format applies. The bench reports each case against the target; a case above 65 µs that stays inside its published bound is not a failure.")
sub("- At 192 kHz the shared engines reach 93.18 % load, and mixed formats reach 84.319 µs, at most 100.825 µs (open questions 1 and 7).",
    "- At 192 kHz the shared engines reach 93.18 % load (open question 6), and mixed formats reach 84.319 µs, at most 100.825 µs (accepted, as above).")
sub("a margin under 125 µs lapses the head every packet, so interleaved clean copies",
    "a margin under about 125 µs on both networks lapses the head every packet (the threshold carries the conversion error, so it is approximate), so interleaved clean copies")
if len(sys.argv) > 1:
    s = s.replace("ADDED added lines", sys.argv[1] + " added lines")
open(OUT, "w", encoding="utf-8").write(s)
