[R801] POSITIVE - exact head 03862f75c89e5c1d84baa4735eff1c1c6f796e25

# R801-4 independent review: processor issue #216 / PR #218, round 4 (PR-body-only delta)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #218, branch `216-mrp-applicant`.
- Exact head `03862f75c89e5c1d84baa4735eff1c1c6f796e25`, tree `dec0f2f79439b89af8686f87bd1db6653a0585fd`. This is the same head R801-3 reviewed. The remote branch ref and the PR's `headRefOid` both still read `03862f7` (`receipts/remote-branch-sha.txt`, `receipts/pr218-view.json`).
- Scope: R801-3-F01 only. Everything else in R801-3 (issuecomment-6754863630) stands and is not re-done.
- Delta since R801-3: no commit. The manager edited the PR body. Body sha256 at this review: `db5586c9…065a` (`receipts/pr218-body.txt`).

## Verdict

**POSITIVE.** R801-3-F01 is resolved at its cause. No MINOR, MAJOR or BLOCKER is open. All five lenses are CLEAN. The one new item is a RESIDUE in the PR body (R801-4-R01).

## R801-3-F01: resolved

- **Required outcome (R801-3):** replace "LINK_DOWN leaves the Applicants as they are (Flush! is a Registrar event, 10.7.5.2)." with "LINK_DOWN leaves the Applicants as they are (Table 10-3 has no Flush! row); it signals no leavealltimer! to either LeaveAll state machine (GAP-19)."
- **What I see in `gh pr view 218 --json body`** (`receipts/pr218-body.txt`, `receipts/f01-check.txt`, `receipts/check-f01-run.txt`):
  - Line 38 ends "… LINK_DOWN leaves the Applicants". Line 39 reads exactly: "  as they are (Table 10-3 has no Flush! row); it signals no leavealltimer! to either LeaveAll state machine (GAP-19)."
  - Joined across the line wrap, the required sentence appears once, word for word. The replaced text "Flush! is a Registrar event, 10.7.5.2" does not appear anywhere in the body.
  - Line 39 is 117 characters, the same width as its neighbours (lines 30 to 40 run 108 to 117, apart from a 67-character paragraph end at line 31), so the edit adds no layout residue.
- **No line cites 10.7.5.2 as the reason LINK_DOWN leaves the Applicants.** The body has four lines with 10.7.5.2. I read each one:
  - `:99-102`: "Table 10-3 has no Flush! row, so the Applicants keep their state", then 10.7.5.2 is cited for the leavealltimer! that the engine does not signal. That is the ruled basis plus the GAP-19 disclosure.
  - `:193`: 10.7.5.2 appears inside the quoted text that was replaced ("in place of 'Flush! is a Registrar event only (§10.7.5.2)'"). It is cited as the old text, not as a basis.
  - `:194`: 10.7.5.2 is cited for leavealltimer! at a Flush!.
  - `:196`: GAP-19's basis list (10.7.5.2, 10.7.5.22, Table 10-5).
- **Only that line changed.** I diffed the body's per-file summary (lines 1 to 90) against the published round-2 body (`author-r2/PR-BODY.md` at evidence commit `6c2007ae`, sha256 `44c4eb9a…f22c`). There are two hunks: the head and commit history at `:6-8` (updated for `03862f7` in round 3) and `:39`. Nothing else changed (`receipts/body-diff-vs-r2-first90.txt`).
- **GAP-19 owner:** issue #221 is OPEN (`receipts/issue221.json`). It covers LINK_DOWN (10.7.5.2, leavealltimer!, Table 10-5) and LINK_UP (10.7.5.1, Tables 10-5 and 10-6), and its done-means includes linking it from GAP-19's owner cell. That answers R801-3-S01. R801-3-S02 (link #221 from the F00.2 owner cell) and R801-3-R01 (re-flow 10 §6.2) are residue at merge, as the manager stated.

## Findings

### R801-4-R01 - RESIDUE - Docs - the PR body still says GAP-19 is "owed and not filed"

- **Where:** PR #218 body, lines 101-102: "Recorded as GAP-19 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`, owed and not filed."
- **Evidence:** issue #221 was created at 2026-11-10T00:03:38Z as GAP-19's owner (`receipts/issue221.json`). The manager's comment 6754877300 says so too.
- **Impact:** wording only. The sentence is a stale status note in PR text. It changes no measurement, figure, test, code, generated artifact, clause claim or verdict. Line 198, "(owner: owed, not filed)", correctly describes the F00.2 row as it reads at this head, so leave it alone until R801-3-S02 lands.
- **Exact fix:** replace "Recorded as GAP-19 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`, owed and not filed." with "Recorded as GAP-19 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`; its owner is #221." Do this in the body, or in the merge commit message if the body is used there.
- **Verification:** read body lines 99-102 and confirm they name #221 and no longer say "not filed".

### Prior findings at this head

| Finding | Severity | Status at `03862f7` | Evidence |
|---|---|---|---|
| R801-3-F01: PR body `:39` cites 10.7.5.2 as the Applicants' basis | MINOR | **RESOLVED** (PR body, no head change) | `receipts/check-f01-run.txt`, `receipts/body-diff-vs-r2-first90.txt` |
| R801-3-R01: ragged wrap, `10_srp_engine.md:530` | RESIDUE | retained; manager's residue checklist at merge | unchanged head |
| R801-3-S01: GAP-19 issue should cover both link edges | SUGGESTION | **ANSWERED** by #221 | `receipts/issue221.json` |
| R801-3-S02: link the GAP-19 issue from the F00.2 owner cell | SUGGESTION | retained; residue checklist at merge (owner now #221) | unchanged head |
| R802-2-F1 and all earlier findings resolved in R801-3 | — | stand as R801-3 recorded; the head is unchanged | issuecomment-6754863630 |

## Lens results

- **Conformance: CLEAN.** The only clause defect at this head was the PR-body copy of the replaced basis. It now gives the ruled basis (Table 10-3 has no Flush! row) and discloses the leavealltimer! omission as GAP-19. GAP-19's owner, #221, covers both link edges.
- **RTL: CLEAN** (carried from R801-2 at `84f6d6a`, via R801-3). No commit since R801-3. A PR-body edit changes nothing that RTL depends on.
- **Robustness: CLEAN** (carried, same reason).
- **Tests: CLEAN** (carried, same reason). Exact-head hosted runs 42710764142 (push) and 42710776954 (pull_request) have `head_sha` `03862f7`. Their `docs-gates` and `portability` jobs passed, and their `suites` jobs were still in progress when I checked (`receipts/hosted-runs.txt`, `receipts/pr218-checks.txt`). I make no claim about the suites jobs. The manager owns hosted acceptance.
- **Docs: CLEAN** (R801-3-R01 and R801-4-R01 are residue). The PR body's per-file summary now agrees with 10 §6.2, GAP-19 and the body's own round-3 section.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PR body `:33-39`, `:99-102`, `:187-200`; R801-3-F01 required text; issue #221 body; GAP-19 basis as recorded in R801-3 | R801-4 (F01); R801-3 for the rest | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| RTL | CLEAN | no change since R801-3; RTL verdict carried from R801-2 at `84f6d6a` (docs-only `03862f7` reviewed in R801-3) | R801-2 / R801-3 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Robustness | CLEAN | as RTL | R801-2 / R801-3 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Tests | CLEAN | as RTL; exact-head hosted job states (docs-gates and portability passed, suites in progress) | R801-2 / R801-3; R801-4 spot-check | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Docs | CLEAN (R801-3-R01 and R801-4-R01 are residue) | full PR body (219 lines, sha256 `db5586c9…065a`); diff against the round-2 published body; widths of lines 30-40 | R801-4 (PR body); R801-3 (repository docs) | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |

## Clone integrity

- The clone is at `03862f7`, tree `dec0f2f7…6fd`, with an empty `git status --porcelain=v2`. sha256 of the `git ls-files -s` index listing: `20af147e…94a6` (`receipts/clone-integrity.txt`).
- The repository has no `.gitmodules` and no submodule gitlinks.
- I ran no probes, edited no file and changed no bytes, so there was nothing to restore.

## Real limits

- This round reads the PR body and issue #221 only. No probe, build or simulation was run, because none of the claims in scope needed falsifying. All execution evidence is still what R801-2 and R801-3 cite.
- I did not read the 802.1Q text for 10.7.5.1 or Tables 10-5 and 10-6. #221 rightly leaves the LINK_UP half to "confirm against the clause text".
- No manager source bank runs at this head, and I claim none. Hosted `suites` jobs were in progress and are not used as evidence. Physical calibration NOT RUN; no hardware proof.
- The PR body can still be edited after this review. This verdict covers the body with sha256 `db5586c9…065a`.

## Pending manager duties

- Merge needs two independent POSITIVE reviews at `03862f7`. Listing comment headers showed that R802-3 is published (issuecomment-6755056010). I did not read its findings before writing this verdict.
- Hosted and act acceptance at the exact head, including the in-progress `suites` jobs.
- Build and validate the current-dev merge candidate (source base `044cb25f`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`) with the builder and native banks, and link the receipts on the PR.
- Residue checklist at merge: R801-3-R01 (re-flow 10 §6.2 `:529-539`), R801-3-S02 (link #221 from GAP-19's F00.2 owner cell), R801-4-R01 (PR body `:101-102`, "its owner is #221").

R801-4 FINISHED
