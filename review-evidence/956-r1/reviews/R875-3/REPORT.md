[R875] NEGATIVE - exact head 1825ba4eaccfe40788391b7af5533fae8c910a85

Internal cleared-context review R875-3 of #956 and #957, PR #958. Tree `450fc60a4ae5c1259afe9b487d5593e31e8fa8ee`.
This is a narrow re-check of the live PR body at the same head as R875-2 and R876-2. All five lenses were applied
to the delta, which is the PR body only. The tree did not change.

**The rewrite fixes nearly all of R875-2-D1 / R876-2-F1.** The rom margin, `centisecond`, `record.srp` and
`record.maap` are now the final head's figures, and round 1's figures are labelled history. The roles are filled in.

**But the rewrite brings in one new wrong figure, so the verdict is NEGATIVE.** The limitations say
`item.acmp_declined` is "30 of 30 us" at 1x1/1if. The receipt, and the same body's line 59, give **20 of 20 us**
there. The cost does sit at its statement, so that part of the claim holds, but the figure is wrong. The brief for
this round has the same "30/30 at both points" figure, and the receipt contradicts it. A wrong figure is not purely
wording, so this is F1, MINOR.

## Contents

- **[Findings](#findings)**: F1 (MINOR); S1 (SUGGESTION); W1, W2 (RESIDUE).
- **[The four checks in the brief](#the-four-checks-in-the-brief)**
- **[Prior findings at this head](#prior-findings-at-this-head)**
- **[Clean results by lens](#clean-results-by-lens)**
- **[Ledger](#ledger)**
- **[Limits and pending manager duties](#limits-and-pending-manager-duties)**

## Findings

### F1: MINOR, Docs: the limitations put 1x1/1if's `item.acmp_declined` at 30 of 30 us; the receipt gives 20 of 20

- **Where:** PR #958 live body, "Known limitations / out of scope", line 253 of `pr958-body.md`:
  "`item.acmp_declined` at 1x1/1if and at 8x8/1if: 30 of 30 us."
- **Evidence:**
  - `author-r2/receipts/cpu-1x1-legs-0d80f0ed-vs-b4a1dde2.md:153-155` gives 1,476 cycles, **20 of 20 us**, for
    every statement of `item.acmp_declined` at 1x1/1if.
  - `cpu-8x8-1if-legs-0d80f0ed-vs-b4a1dde2.md:178-180` gives 2,386 cycles, 30 of 30 us, at 8x8/1if.
  - The same body's Status, line 59, says "20 of 20 us" at 1x1/1if.
  - R875-2-D1's required outcome spelled out both values ("20 of 20 at 1x1/1if, 30 of 30 at 8x8/1if").
  - Each receipt's sha256 matches the published evidence `MANIFEST.json` (`receipts/check-body.log`).
- **Authority:** AGENTS.md section 6, Docs lens ("The PR and Issue contain enough evidence for another cold
  reviewer"). The owner rule of 2026-10-02 says a defect that changes a figure is not RESIDUE.
- **Impact:** One review object gives two different current figures for one cost. A reader of the limitations alone
  would take 1x1/1if's statement for `acmp_declined` to be 30 us. The real statement is 20 us. The implementation and
  the budget are not affected.
- **Required outcome:** Line 253 gives each point's own figure, for example "`item.acmp_declined`: 20 of 20 us at
  1x1/1if and 30 of 30 us at 8x8/1if." The count of three costs at their statement is then still correct.
- **Verification:** Compare the revised line with the two receipt lines above, or fetch the body again and re-run
  `scripts/check_body.sh <packet-dir> <clone-dir>` against it.

### S1: SUGGESTION, Docs: the largest-notice comparison at 1x1/1if also sits at its statement

`cpu-1x1-legs-0d80f0ed-vs-b4a1dde2.md:194-195` gives `item.aecp_long` (the largest legal notice, run in the
`aecp-largest-notice` leg) as 29,554 cycles, 315 of 315 us at 1x1/1if. This is the separate compare-long check, not
one of the 66 stated-cost rows. Its bound is the largest legal notice by construction, so no group that was not run
can push it over. The limitations' "three measured costs" are therefore defensible. Optional: add half a sentence
saying that this cost also sits at its statement and why it is excluded. That would stop a cold reader recounting
to four.

### W1: RESIDUE, Docs: the Status bullet "see each finding above" points at nothing in the PR body

Line 66 of the live body reads "The reviewers' probes at `b4a1dde2`: see each finding above." No findings appear
above it in the PR body; the sentence was copied from the round's `[A809] REVIEW READY` comment on #956, where the
findings do come first. Exact fix: "The reviewers' probes at `b4a1dde2`: pass; each is listed with its finding in
the round's `[A809] REVIEW READY` on #956."

### W2: RESIDUE, Docs: "gives back 112 B" names no base

Line 148 of the live body says fixing one interface's build at compile time "gives back 112 B of 8x8/1if's `rom`".
The receipt (`rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt:20-24`) shows the following:

- 112 B is the round's net change against round 1's head (139,248 to 139,136 B).
- That step, together with the refused slice's due, gave back 128 B against `04819246` (139,264 to 139,136).
- Commit `b4a1dde2`'s own subject says "128 bytes ... back".

This is the same kind of defect as R875-2-W1 on the design page. Exact fix: "... which leaves 8x8/1if's `rom` 112 B
smaller than at round 1's head (128 B smaller than at `04819246`)."

## The four checks in the brief

1. **The limitations give the final head's figures, with round 1's labelled history.** I verified each one against
   the published receipts. Their sha256 matches `MANIFEST.json` and their git blob ids match tree `362a3039`.

   | Claim in the live limitations | Receipt | Result |
   |---|---|---|
   | rom 128 B left, aligned `rom_end` 139,136 of 139,264 B, 58 RAMB36 | rom-ledger `:13`, `:17`, `:24` | match |
   | `centisecond` 1x1/1if 14,213 cycles, 150 of 170 us | 1x1 `:132-133` | match |
   | `record.srp` 8x8/1if 35,507 cycles, 375 of 375 us | 8x8 `:209-210` | match |
   | `record.maap` 8x8/1if 17,014 cycles, 180 of 185 us | 8x8 `:207-208` | match |
   | `item.acmp_declined` 30 of 30 us at 8x8/1if | 8x8 `:178-180` | match |
   | `item.acmp_declined` 30 of 30 us at 1x1/1if | 1x1 `:153-155`: **20 of 20** | **F1** |
   | Round 1: `centisecond` 16,064 (170/170), `record.srp` 35,273, `record.maap` 17,259 (185/185), labelled "history, superseded" | base columns of the same rows | match; labelled |
   | Round 1's head had 16 B of rom left (labelled) | rom-ledger `:7`, `:17` | match; labelled |
   | "three measured costs sit at their statement" | every nonzero row with rule = statement: acmp_declined at both points, record.srp at 8x8/1if (`check-body.log`) | match (see S1) |

2. **Roles.** Lines 75-77 now read Executor `[A809]`, Internal cleared-context reviewer R875, External reviewer R876.
   This matches the review sessions that have published on this PR. R875-2-W2 / R876-2-R1 is **resolved**. The issue
   body still says "as the maintainer assigns it". That is issue text, outside this check, and does not contradict
   the PR body.
3. **One pass over the whole live body** (288 lines, sha256 `56143d39...`) for figures and claims stated as current:
   - The Status figures match the receipts:
     - rom points 126,360 / 128,112 / 139,136 / 140,864;
     - 71 and 95 probes paired, 7 misses each side;
     - 66 of 66 stated costs within at each point;
     - build-one 52,531 (735 us) and 126,644 (1,475 us);
     - lines 58-63.
   - The rom paragraph's history (139,208, 56 B, 139,248, 16 B, 139,280) and its final 139,136 / 128 B match
     rom-ledger `:20-24`.
   - The commit count of 20 matches `git rev-list --count 15168e14..1825ba4e`.
   - The live PR head is `1825ba4e`.
   - The only contradiction found is F1. W1 and W2 are wording.
4. **Head and tree unchanged.** Local `HEAD` and the live PR `headRefOid` are both
   `1825ba4eaccfe40788391b7af5533fae8c910a85`, tree `450fc60a`. The working tree and index are clean. No probe or edit
   was made in the clone. So R875-2's and R876-2's lens verdicts on the tree stand at this head. Their only open
   non-wording finding was the PR-body finding re-checked here.

## Prior findings at this head

- **R875-2-D1 = R876-2-F1 (MINOR, Docs): resolved except for one figure.**
  - The rom margin, `centisecond`, `record.srp` and `record.maap` are current.
  - Round 1's figures are labelled history.
  - The costs at their statement are listed.
  - The formal-measurement limitation is kept.
  - The rewrite's 1x1/1if `acmp_declined` figure is wrong. That is recorded as F1 rather than retaining D1, because
    D1's stated defect, round 1's figures given as current, is gone.
- **R875-2-W2 = R876-2-R1 (RESIDUE): resolved** (check 2).
- **R875-2-S1, S2, S3 (SUGGESTION, Tests) and R875-2-W1 (RESIDUE, design page "112 bytes smaller"):** These are
  unchanged and carried. They are not touched by a body-only delta, and W2 above is the same kind of defect in the
  body.
- **R876-1-F1/F2/F3 and R875-1-F1/F2/F3:** The tree did not change, so R875-2's and R876-2's "resolved" stands.

## Clean results by lens

[R875] PASS Conformance - `pr958-body.md:81-199` against #956's owner decision as R875-2 read it at tree `450fc60a` - the body's hold-off figures (2,977 / 2,973 / 2,970 cs), its behaviour claims and its scope match; the tree is unchanged, so R875-2's Conformance PASS stands; F1 is a cost figure, not a protocol claim.

[R875] PASS RTL - `git rev-parse HEAD HEAD^{tree}` = `1825ba4e` / `450fc60a`, live `headRefOid` `1825ba4e` (`receipts/check-body.log`) - no tree change since R875-2's RTL PASS; the body still states no RTL change (line 26), which matches the diff R875-2 read.

[R875] PASS Robustness - `receipts/check-body.log` (head, clean status) and `pr958-body.md:262-272` - the tree is unchanged; the limitations on robustness (DA gate, link reset, mid-centisecond request, T_egress) match what R875-2 checked in the tree.

[R875] PASS Tests - `pr958-body.md:32-67`, `:238-245` against `cpu-*-legs-0d80f0ed-vs-b4a1dde2.md` probe tallies - the paired-probe counts, misses and the 66-row tallies stated as gate evidence match; the tree's tests are unchanged since R875-2.

Docs: **UNCLEAN (F1).** I applied it to the whole live body against the three receipts and the head.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | live PR body `:81-199`; tree unchanged (R875-2's examination at this tree) | R875-2, re-confirmed R875-3 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| RTL | CLEAN | head/tree identity, live headRefOid; R875-2's examination at this tree | R875-2, re-confirmed R875-3 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Robustness | CLEAN | body limitations `:262-272`; tree unchanged | R875-2, re-confirmed R875-3 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Tests | CLEAN | body gate evidence `:32-67` against both CPU legs receipts; tree unchanged | R875-2, re-confirmed R875-3 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Docs | UNCLEAN (F1) | live PR body (sha256 `56143d39...`), rom-ledger and both CPU legs receipts; repository docs unchanged since R875-2 | R875-3, applied, not clean | `1825ba4eaccfe40788391b7af5533fae8c910a85` |

## Limits and pending manager duties

- **What I did:**
  - Read the live PR body (fetched 2026-11-22, updated `03:14:24Z`).
  - Downloaded three published receipts and `MANIFEST.json` from evidence tree `362a3039`, and verified their hashes.
  - Ran one portable check script, `scripts/check_body.sh`.
- **What I did not do:**
  - I re-ran no suite, build or probe. None was needed for a body-only check.
  - I did not review the tree again.
  - I did not inspect the hosted gates or act; the manager owns them.
  - There is no manager source bank at this head, and I claim none.
  - Physical calibration has not been run.
- **Owed to the manager:**
  - Correct F1 in the PR body. A Docs re-check of that line clears it.
  - Carry W1, W2 and R875-2-W1 to the residue checklist.
  - S1 and R875-2-S1 to S3 are optional.
  - Build and validate the current-dev merge candidate (source base `15168e14`, live dev `e275d795`) at the merge
    turn.
  - Hosted and act acceptance.
  - Merge only with maintainer authorization.
- **What this round changed:** none of: source, commits, pushes, GitHub writes, author contact, other checkouts. The
  clone's tracked bytes are untouched (`git status --porcelain` is empty).

R875-3 FINISHED
