"""Build round 8's PR body from round 7's, with exact-text replacements; each must match once."""
import sys
SRC = "$MANAGEMENT/2026-09-23/640-a720g/PR-BODY.md"
OUT = "$MANAGEMENT/2026-09-23/640-a720h/PR-BODY.md"
HEAD = "20933ef48a9b174e58a9d17ddd59078a072024af"
D = "https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030"
s = open(SRC, encoding="utf-8").read()

def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected one match, got {n}: {old[:80]!r}")
    s = s.replace(old, new)

sub("[A720g]\n\n## Contents", "[A720h]\n\n## Contents")
sub("and the round-6 residue closed.\n",
    "and the round-6 residue closed.\n"
    "- **[Round 8](#round-8)** -- No fewer-reservations maximum is derived: the pass rule and the reached cases corrected.\n")
sub("clean clone of head `e7310e94fff7188c5800a94c03a3f0e4c7c1c024`", f"clean clone of head `{HEAD}`")

# Status and the talker statement.
sub("Round 7 applies the [owner decisions of 2026-11-01]",
    "Round 8 answers R757-7 (NEGATIVE at `e7310e94`, one MINOR) and R758-7 (POSITIVE at `e7310e94`, one residue item). Round 7 applied the [owner decisions of 2026-11-01]")
sub("With mixed channel counts, or with fewer reservations, it does not; the owner accepted those derived bounds, which stay published. No connection is refused because of them, and no restriction to one base format applies.",
    "With mixed channel counts it does not; the owner accepted those derived bounds, which stay published. With fewer reservations it does not either, and no maximum is derived: the largest figure reached is 143.347 µs, quoted as reached, not as a limit. No connection is refused because of these figures, and no restriction to one base format applies.")
sub("Fewer reservations are worse: with three co-phased eight-channel streams the bound is 123.337 µs. The owner accepted both cases' bounds on 2026-11-01.",
    "Fewer reservations are worse, and no maximum is derived for them. The largest figure reached is 143.347 µs at 48 kHz, with six co-phased one-channel streams; it is quoted as reached, not as a limit. The owner's decision of 13:35 on 2026-11-01 was taken on a figure of 123.337 µs. The reached figure is now 143.347 µs, and the manager has told the owner.")

# Executor and commits.
sub("Executor: `[A720g]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`; round 5: `[A720e]`; round 6: `[A720f]`)",
    "Executor: `[A720h]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`; round 5: `[A720e]`; round 6: `[A720f]`; round 7: `[A720g]`)")
sub("| `7b3121d2` | FR_NFR.md, stream engines, area plan | NFR-LAT-03 restated as a 65 µs target, with the bounds accepted and what the bench records;",
    "| `7b3121d2` | FR_NFR.md, stream engines, area plan | NFR-LAT-03 restated as a 65 µs target, with the bounds accepted and what the bench records (round 8 corrects this for fewer reservations);")
sub("the threshold carries the conversion error. |\n",
    "the threshold carries the conversion error. |\n"
    "| `210c3eb6` | FR_NFR.md, stream engines, area plan | No fewer-reservations maximum is derived; 143.347 µs quoted as reached; a case graded only against a derived bound; the reached cases tabled as examples; open design item 4 for lane 6; the area plan's rows and lane 6 evidence agree. |\n"
    "| `20933ef4` | stream engines | The fixed-terms line kept within the sentence limit; the probe pointer says it reports the reached cases. |\n")

# Round 7 rows that would otherwise read as current.
sub("a case above 65 µs that stays inside its published bound is not a failure.\" |",
    "a case above 65 µs that stays inside its published bound is not a failure.\" Round 8 replaces those sentences. |")
sub("| Area plan | The target row and D14 agree: a target, those bounds accepted and published, no connection refused. |",
    "| Area plan | The target row and D14 agree: a target, those bounds accepted and published, no connection refused. Round 8 narrows \"those bounds\" to mixed formats. |")

sub("## Authoritative references\n", f"""## Round 8

R757-7 is NEGATIVE at `e7310e94` with one MINOR, R757-7-F1: round 7 made "inside its published bound" the pass rule, but no bound is published for fewer reservations. R758-7 is POSITIVE at `e7310e94` with one residue item, R758-7-R1. The manager ruled on the fix. No mechanism and no new derivation are added, and no existing figure changes. The lane handoff carries file, line and verification.

| Item | Closure |
|---|---|
| R757-7-F1, NFR-LAT-03 | 123.337 µs is gone from the row. It reads "Those 16-reservation bounds are accepted and published." and "With fewer reservations no maximum is derived". It quotes 143.347 µs as reached, not as a limit, and says no connection is refused because of these figures. Its last sentences read "The bench measures every case against the target and reports it; a case above 65 µs is reported, not failed." and "A case is graded against a bound only where one is derived, which is the 16-reservation table; there, a measurement above its bound contradicts the analysis and is a finding." |
| R757-7-F1, stream engines | The decision's statement under "Talker latency budget" says the same. "Fewer reservations on a port" gains a second table of four cases reached under the exact phase rule, each with its starts and stops: 143.347 µs and 111.635 µs at 48 kHz, 125.426 µs at 96 kHz, at least 102.034 µs at 192 kHz before the packetizer term. The page says the rows of both tables are examples and none is a maximum. The k-co-phased form now names equal frames, gives no largest k and does not cover unequal frames. The first table is unchanged. |
| R757-7-F1, the maximum | Open design item 4, for lane 6: derive the fewer-reservations maximum with the model at every rate, and verify it against the reached cases and on the bench. |
| R757-7-F1, area plan | The target row and D14 say the mixed-format bounds are accepted, and that with fewer reservations no maximum is derived and 143.347 µs is reached, not a limit. |
| R758-7-R1, R757-7 RR12 | Lane 6's evidence reads "Talker latency taps on all talker streams, measured against the 65 µs target". |
| Owner | The decision of 13:35 was taken on a figure of 123.337 µs. The reached figure is now 143.347 µs, and the manager has told the owner. |
| Witnesses | The 48 kHz six-stream and 96 kHz four-stream sequences are the reviewer's. The probe's walks print only the placement for the two unequal-stream rows, so the author wrote the short sequences on the page. The published model's phase rule reaches all four placements. Its queue recursion and event-exact shaper simulation both give each wait. |
| 192 kHz | The table's row is R757-7's, and that search left out eight-channel streams, as the page says. R758-7's S1 reaches at least 106.927 µs at 192 kHz with an eight-channel stream, before the packetizer term; the author's run of the published model gives the same. This round adds only the assigned cases, so no row carries that figure. It is below 143.347 µs, and open design item 4 covers eight-channel streams at 192 kHz. |
| Not taken | R758-7 S2 and S3, and R757-7-S2, are outside the assigned text. R757-7 RR13 is the manager's, on the issue body. R757-7-S1's bench case enters only through item 4's verification. |

## Authoritative references
""")
sub("and the owner decisions of 2026-11-01;", "the owner decisions of 2026-11-01, and R757-7-F1 with the manager's ruling on it;")

sub("thirty-eight commits: one per file group or finding group, and the dev merge", "forty commits: one per file group or finding group, and the dev merge")
sub("Recorded at `e7310e94` (every step", "Recorded at `20933ef4` (every step")
sub("em dash (0 over 1,754 added lines in 7 pages)", "em dash (0 over ADDED added lines in 7 pages)")

# Known limitations.
sub("The owner decided on 2026-11-01 that 65 µs is a target: the derived bounds are accepted and stay published, no connection is refused because of them, and no restriction to one base format applies. The bench reports each case against the target; a case above 65 µs that stays inside its published bound is not a failure.",
    "The owner decided on 2026-11-01 that 65 µs is a target: no connection is refused because of these figures, and no restriction to one base format applies. The 16-reservation bounds are accepted and stay published. With fewer reservations no maximum is derived; 143.347 µs is the largest figure reached, not a limit, and open design item 4 gives the derivation to lane 6. The bench measures every case against the target and reports it; a case above 65 µs is reported, not failed. A case is graded only against a derived bound, which is the 16-reservation table; there, a measurement above its bound contradicts the analysis and is a finding.")
if len(sys.argv) > 1:
    s = s.replace("ADDED added lines", sys.argv[1] + " added lines")
open(OUT, "w", encoding="utf-8").write(s)
