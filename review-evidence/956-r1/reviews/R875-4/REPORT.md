[R875] POSITIVE - exact head 1825ba4eaccfe40788391b7af5533fae8c910a85

This is internal cleared-context review R875-4 of #956 and #957, PR #958, at tree
`450fc60a4ae5c1259afe9b487d5593e31e8fa8ee`. It is a narrow re-check of the live PR body, at the same head as R875-3.
All five lenses were applied to the delta. The delta is the PR body only; the tree has not changed.

**R875-3-F1 is resolved, and so are its S1, W1 and W2.** The live body (updated `2026-11-22T03:20:51Z`, sha256
`1ec149e3...`) differs from the body R875-3 read (sha256 `56143d39...`) in exactly four places, plus one trailing blank
line. Each of the four edits gives the outcome R875-3 required, and each matches the receipts. A fresh pass over the
whole body found no figure stated as current that the final head's receipts contradict. This round has **no
findings**.

## Contents

- **[Findings](#findings)**: none.
- **[The three checks in the brief](#the-three-checks-in-the-brief)**
- **[Prior findings at this head](#prior-findings-at-this-head)**
- **[Clean results by lens](#clean-results-by-lens)**
- **[Ledger](#ledger)**
- **[Limits and pending manager duties](#limits-and-pending-manager-duties)**

## Findings

None: no BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION.

Two notes, neither of which is a finding:

- Line 148 says the step "leaves 8x8/1if's `rom` 112 B smaller than at round 1's head (128 B smaller than at
  `04819246`)". The receipt (`rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt:24`) attributes the final 139,136 B to the
  compile-time interface and the refused slice's due together. With both bases named, the sentence's figures are
  correct as it stands. It is also the exact wording R875-3 required, so it is not reopened.
- The S1 sentence names only 1x1/1if. That is correct: the 8x8/1if receipt's compare-long section
  (`cpu-8x8-1if-legs-...md:216-218`) holds no measured notice, and its `item.aecp_long` row (`:187`) is 0 of 320.

## The three checks in the brief

### 1. The four edits against R875-3's required outcomes and the receipts

The source for this table is `receipts/evidence-and-delta.log`, which holds the diff of the R875-3 body against the
live body.

| Item | Live body now | Required outcome (R875-3) | Receipt | Result |
|---|---|---|---|---|
| F1 (MINOR) | `:253` "`item.acmp_declined`: 1,476 cycles, 20 of 20 us at 1x1/1if; 2,386 cycles, 30 of 30 us at 8x8/1if." | each point's own figure, 20/20 at 1x1/1if and 30/30 at 8x8/1if; the count of three still correct | 1x1 `:153-155` give 1,476, 20, 20 (three rows); 8x8 `:178-180` give 2,386, 30, 30 (three rows) | **resolved**. The count of three (acmp_declined at two points, plus record.srp at 8x8/1if `:209-210`, 375/375) still equals every nonzero statement-equal row (`receipts/check-body.log`). |
| S1 (SUGGESTION) | `:256-257` "`item.aecp_long` at 1x1/1if (29,554 cycles, 315 of 315 us) also sits at its statement, but it is the largest legal notice by construction ...; it is not counted among the three." | optional half sentence saying it also sits at its statement, and why it is excluded | 1x1 `:194-195` give 29,554 CPU cycles, 315 us, against aecp_long 315 us | **taken, correct** |
| W1 (RESIDUE) | `:66` "The reviewers' probes at `b4a1dde2`: pass; each is listed with its finding in the round's `[A809] REVIEW READY` on #956." | exact fix text | (wording) | **resolved**, verbatim |
| W2 (RESIDUE) | `:148-149` "... which leaves 8x8/1if's `rom` 112 B smaller than at round 1's head (128 B smaller than at `04819246`)." | exact fix text | rom-ledger `:20` 139,248 at `0d80f0ed` (round 1's images); `:23` 139,264 at `04819246`; `:24` 139,136 at `b4a1dde2`. 139,248 − 139,136 = 112 and 139,264 − 139,136 = 128. | **resolved**, verbatim |

Where the receipts come from:

- The three receipts were copied from the R875-3 packet.
- They were checked again against the published evidence tree `362a3039`:
  - Each git blob id matches the tree entry under `review-evidence/956-r1/author-r2/receipts/`.
  - `MANIFEST.json` matches `review-evidence/956-r1/MANIFEST.json`, blob `75b0e7ce`.
  - Each receipt's sha256 matches `MANIFEST.json`.
- The evidence for all three checks is in `receipts/check-body.log` and `receipts/evidence-and-delta.log`.

### 2. `scripts/check_body.sh` against the live body, and a whole-body pass

- **The script:** `scripts/check_body.sh <packet> <clone>` exited with rc 0 (`receipts/check-body.log`). The script is
  unchanged from R875-3.
  - Head and tree: `1825ba4e` / `450fc60a`, with 0 dirty lines.
  - Live `headRefOid`: `1825ba4e`. The PR is not a draft.
  - Every body line that names one of the costs, the rom, the roles, "each finding above" or "112 B" agrees with
    the receipt rows that the script prints.
  - "each finding above" no longer occurs in the body.
- **The whole-body pass** covered all 291 lines, once. These are the figures stated as current and their receipts:
  - Status rom points 126,360 / 128,112 / 139,136 / 140,864 B, and 128 B left (16 at `0d80f0ed`): rom-ledger
    `:11-14`, `:17`.
  - Image deltas `transmit` −116 / +40 / −112 / +36 B and `reset_interface` +4 B at 8x8: rom-ledger `:29`, `:35`,
    `:41`, `:47`.
  - Probes paired: 71 at 1x1/1if (50 + 14 + 7) and 95 at 8x8/1if (45 + 36 + 14), with 7 misses each side.
  - 66 of 66 stated costs within, at each point.
  - Build of one 52,531 cycles (735 us) and 126,644 cycles in `srp-talker-held` (1,475 us).
  - `centisecond` 14,213 cycles, 150 of 170 us.
  - `record.srp` 35,507 cycles in `srp-talker-held`, 375 of 375 us (35,273 before).
  - `record.maap` 17,014 cycles, 180 of 185 us (17,259 before, at 185).
  - `item.acmp_declined` 20/20 at 1x1/1if and 30/30 at 8x8/1if, at both `:59` and `:62` and at `:253`.
  - The rom paragraph's 139,208 / 56 B, 139,248 / 16 B, 139,280 B and 139,136 / 128 B: rom-ledger `:20-24`, and the
    train-head figure as R875-3 read it.
  - The limitations at `:253-263`.

  **Result: no instance contradicts the receipts.** Round 1's figures appear only where they are labelled history
  or "before".
- **Lines this check does not reach.** The figures in the body's description are not in these three receipts. They
  are the hold-off table (2,977 / 2,973 / 2,970 cs), 29,770 / 29,700 / 29,995 / 29,997 ms, and the plant counts
  826 / 389 / 574. They are unchanged since R875-3, which accepted them on R875-2's tree review. This round did not
  verify them again.

### 3. Head unchanged; earlier verdicts stand

- Local `HEAD` is `1825ba4eaccfe40788391b7af5533fae8c910a85` and its tree is `450fc60a`. This equals the live PR
  `headRefOid`.
- `git status --porcelain` is empty.
- The submodule gitlinks are the recorded ones, with none modified (`git submodule status`).
- No probe, build or edit was made in the clone.
- R875-2's tree verdicts for Conformance, RTL, Robustness and Tests, as re-confirmed by R875-3, therefore stand. The
  body delta changes nothing they depend on.

## Prior findings at this head

- **R875-3-F1 (MINOR, Docs): resolved** (check 1).
- **R875-3-S1 (SUGGESTION): taken.**
- **R875-3-W1 and W2 (RESIDUE): resolved** in the body (check 1).
- **R875-2-D1 = R876-2-F1 (MINOR, Docs): resolved.** Its last wrong figure was F1.
- **R875-2-W2 = R876-2-R1 (RESIDUE, roles): resolved.** This was confirmed by R875-3 and is unchanged.
- **Carried unchanged, outside a body-only delta:**
  - R875-2-W1 (RESIDUE, the design page's "112 bytes smaller" names no base). It stays on the manager's residue
    checklist.
  - R875-2-S1, S2 and S3 (SUGGESTION, Tests). These are optional.
- **R875-1-F1/F2/F3 and R876-1-F1/F2/F3:** resolved, as R875-2 and R876-2 found. The tree has not changed.

## Clean results by lens

[R875] PASS Conformance - `pr958-body.md:83-114`, `:203-209`, `:264-274` at tree `450fc60a` - the delta touches no protocol or clause claim; the hold-off figures, the behaviour claims and the references are unchanged since R875-3 and agree with R875-2's tree review of the owner decision.

[R875] PASS RTL - `receipts/check-body.log` (HEAD/tree `1825ba4e`/`450fc60a`, 0 dirty, live headRefOid `1825ba4e`) and `pr958-body.md:26-27` - no tree change since R875-2's RTL PASS; the body still states no RTL change.

[R875] PASS Robustness - `pr958-body.md:262-274` against rom-ledger `:13`, `:17` and the unchanged tree - the rom margin (128 B), the DA gate, the link reset, the mid-centisecond request and the T_egress limitations are current and unchanged in meaning.

[R875] PASS Tests - `pr958-body.md:32-67`, `:249-261` against `cpu-1x1-legs-...md:153-155`, `:194-195` and `cpu-8x8-1if-legs-...md:178-180`, `:209-210`, `:215` - the probe tallies, the 66-row tallies and the at-statement set (three, plus the separately justified compare-long) match the receipts; the tree's tests are unchanged.

[R875] PASS Docs - the whole live body (`pr958-body.md`, 291 lines, sha256 `1ec149e3...`) against the three receipts, which match the evidence tree `362a3039` by blob id - F1, W1 and W2 are fixed as R875-3 required, S1 is taken, and no figure stated as current is contradicted.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | live body `:83-114`, `:203-209`, `:264-274`; tree unchanged (R875-2's examination at this tree) | R875-2, re-confirmed R875-3 and R875-4 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| RTL | CLEAN | head/tree identity, live headRefOid, clean index, gitlinks; R875-2's examination at this tree | R875-2, re-confirmed R875-3 and R875-4 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Robustness | CLEAN | body limitations `:262-274`, rom-ledger; tree unchanged | R875-2, re-confirmed R875-3 and R875-4 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Tests | CLEAN | body gate evidence `:32-67` and limitations `:249-261` against both CPU legs receipts; tree unchanged | R875-2, re-confirmed R875-3 and R875-4 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Docs | CLEAN | whole live body (sha256 `1ec149e3...`), rom-ledger and both CPU legs receipts (blob-verified at `362a3039`); repository docs unchanged since R875-2 | R875-4 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |

## Limits and pending manager duties

- **What I did:**
  - Fetched the live PR body read-only.
  - Diffed it against the body R875-3 read.
  - Checked the published receipts again by blob id and sha256 against evidence tree `362a3039`.
  - Ran `scripts/check_body.sh`.
  - Read the whole body once.
- **What I did not do:**
  - I re-ran no suite, build or probe. None was needed for a body-only check.
  - I did not review the tree again.
  - I did not inspect the hosted gates or act; the manager owns them.
  - There is no manager source bank at this head, and I claim none.
  - Physical calibration has not been run, and field skips are not hardware proof.
  - The figures in the description that are not in the three receipts were not checked again (see check 2).
- **Owed to the manager:**
  - Carry R875-2-W1 (the design page's base) to the residue checklist.
  - R875-2-S1 to S3 are optional.
  - Build and validate the current-dev merge candidate (source base `15168e14`, live dev `e275d795`) at the merge
    turn, and link its receipts.
  - Hosted and act acceptance.
  - Merge only with maintainer authorization.
- **What this round changed:** none of: source, commits, pushes, GitHub writes, author contact, other checkouts. The
  clone's tracked bytes, index and gitlinks are untouched.

R875-4 FINISHED
