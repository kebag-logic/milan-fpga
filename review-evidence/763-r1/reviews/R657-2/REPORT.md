[R657] POSITIVE - exact head 07c6c72fce79e705bcf28a70071497d0ce7040e4

# R657-2: narrow internal re-review of PR #766 (Closes #763)

- Head `07c6c72fce79e705bcf28a70071497d0ce7040e4`, tree `c70d7afe29d34724474bfc05053fe3cb43801026`, on dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. The source base and live dev are the same commit.
- This is the same head that R657-1 reviewed. `git log e9cbb676..HEAD` still shows the same two one-line commits, and the diff is the same four files (+65/-3). No byte of source, test, docs or CI input changed between rounds. Only the PR body and the public evidence branch changed.
- Scope:
  - my round-1 findings (F1, R1, S1, S2);
  - the R658-1 findings the manager assigned me to confirm (F2, and the F3 residue);
  - the manager's ruling on F1: PR #766 comment 6259476788, option (c).
- Read in this order:
  - AGENTS.md;
  - the round-2 assignment (6259259419);
  - the author's STOP on #763 (6259463748);
  - the ruling (6259476788);
  - the #737 tracking comment (6259477028);
  - the delta, the live PR body, and the evidence tree `687310c8…/review-evidence/763-r1` (author-r2).
  - I read R658-1's findings only after my own pass, and only to confirm F2 and F3. I did not read the R658-2 report.
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR is open. One RESIDUE (RS1, PR body wording) and two carried SUGGESTIONs (S1, S2) remain. None of them affects the verdict or any lens.

## Prior findings at this head

| Finding | Round-1 severity / lenses | Status at this head | Evidence |
|---|---|---|---|
| R657-1-F1 (inventory digests) | MINOR / Conformance, Tests | **Discharged by outcome (b) of my round-1 required outcome** | See F1 below. |
| R658-1-F1 (same defect) | MINOR | Discharged by the same ruling and tracking | Same as above. |
| R658-1-F2 (overstated count) | MINOR / Tests, Docs | **Resolved** | See F2 below. |
| R657-1-R1 (status line) | RESIDUE / Docs | **Applied** | Live body line 16 reads "two commits at published head `07c6c72f`". |
| R658-1-F3 (status and roles) | RESIDUE / Docs | **Applied** | Line 16 as above. The roles name `[R657]` (6258585761) and `[R658]` (6258590845). |
| R657-1-S1 (scope the README sentence) | SUGGESTION / Docs | Not taken. Optional, carried below. | README:105-109 is unchanged. |
| R657-1-S2 (writer-side mutant) | SUGGESTION / Tests | Not taken. Optional, carried below. | aecp_mutants.py:358-371 is unchanged. |

### F1: discharged by a public decision plus a tracking issue that names the rows

My round-1 required outcome offered two routes. Route (b) was: "a public maintainer or manager decision that assigns the refresh of these rows to the inventory's owner, with a tracking issue that names both lane-owned rows." That is what happened:

- **Ruling** (`receipts/pr766_ruling_option_c.txt`, PR #766 comment 6259476788):
  - option (c) is chosen, and the refresh stays out of this PR;
  - all four rows go to #737's adoption work, as one inventory refresh plus a lock re-record from two cold builds;
  - `exec-audit-receipt.json` stays as committed.
- **Tracking** (`receipts/issue737_tracking_comment.txt`, #737 comment 6259477028). It names the four `inputs` rows exactly:
  - `sw/firmware/ctrl/test/aecp_arms.py` and `aecp_mutants.py` (PR #766);
  - `scripts/check_doc_style.py` (#753);
  - `scripts/measure_test_evidence_readers.py` (#754).

  It also names the fix: `--write` once on the dev that includes #766, then re-record `image.lock.json` from two byte-identical cold builds (the recipe digest moves from `712f7b38`), then add `--check` to the gate set. #737 is OPEN.
- **The four rows are exactly the drift** (`scripts/ci_input_scope.py`, `receipts/ci_input_scope.txt`, `receipts/ci_input_scope_base.txt`):
  - at base `e9cbb676`, exactly 2 in-tree inventory rows are stale: `check_doc_style.py` and `measure_test_evidence_readers.py`;
  - at head, exactly 4 are stale: those two plus `aecp_arms.py` (`33c3c60a…` committed, `277a41b9…` at head) and `aecp_mutants.py` (`b3f94ef0…` committed, `bb4fe6f2…` at head);
  - the #737 comment lists the same four, no more and no fewer.
- **The PR changes no CI image input beyond the two AECP scripts** (`receipts/ci_input_scope.txt`):
  - Of the four changed files, only `aecp_arms.py` and `aecp_mutants.py` are inventory `inputs`. `README.md` and `test_aecp.cpp` are not.
  - None of the four is among the literal files of `ci/image/build.py` `recipe_inputs()` (`build.py:143-156`). The diff does not touch `ci/image/`.
  - Of every `ci/image/*.json`, only `tool-inventory.json` and `exec-audit-receipt.json` name a changed file, and both name only the two AECP scripts. By the ruling, `exec-audit-receipt.json` stays as a committed observation of one traced run.

### F2: the corrected count matches the gate log

The published blobs were fetched and every git blob id was verified (`receipts/evidence_fetch.txt`, all OK).

- **Author-r2 receipt summary.** `author-r2/receipts/round-b/gates/test_ctrl_firmware/summary.txt` (blob `da1896b8`) now reads: "876 source-mutant executions caught (520 control-source, 78 AECP, 278 SRP), 2 dependency-pin refusal controls passed, 61 normal arm outcomes passed. The 939 lines are not 939 planted controls." `round-2/count/classify.json` gives the same split (`classify.rc` is 0, and `unclassified` is empty).
- **My independent split** of the published extract (blob `72562576`, the same bytes as round B), using `scripts/count_check.py` (`receipts/count_check.txt`):
  - 939 top-level `[ok]` lines, and 0 `ESCAPED`;
  - 2 lines are `[ok] lwSRP pin …` refusal controls;
  - all 78 names in the head's `aecp_mutants.py` defect table have an `[ok]` line, for 79 hits over 78 distinct names. The extra hit is `reentry-uncounted`, which is a name in both the AECP and SRP tables. The author's `resolved_by_campaign_order` resolves it the same way.
  - So 939 − 61 − 78 − 2 = 798 = 520 + 278. This agrees with my own R657-1 four-shard bank: 61 + 520 + 78 + 280, where my "280 SRP" included the two pin lines.
  - Both #763 mutants are `[ok]` on their named tests.
- **PR body.** The live body's Status paragraph (lines 18-20) states the same split, and the Round 2 table row "R658-1-F2 (count)" repeats it.
- **What remains in history.** The round-B REVIEW READY comment on #763 (6258557430) and the superseded `author/…/summary.txt` (blob `49c71528`) still carry the older wording. Both are immutable history. The STOP (6259463748) corrects the claim publicly, and the author-r2 tree supersedes the old summary. This is not a finding.
- **The live PR body matches the published draft.** It equals `author-r2/PR-BODY.md` (blob `1bb5f908`) except for two differences: "Relates to #763" became "Closes #763", as the ruling directed, and there is one trailing newline (`receipts/pr766_body_live.md`). GitHub lists #763 as a closing reference.

## Findings this round

### RS1: RESIDUE (Docs): the PR body still describes the F1 decision as pending

- **Where:** the PR #766 body (`receipts/pr766_body_live.md`, sha256 `cd1cd280…`), lines 16, 21-23, 30-31, 114, 125 and 146.
- **Problem:** after ruling 6259476788, these lines still say that the PR is blocked, or that it only relates to #763, pending a decision that has now been made. The text is wording only. It changes no measurement, figure, test, code, generated artifact or clause claim, and the closing keyword "Closes #763" is already correct.
- **Exact fix:**
  - **Line 16:** replace "BLOCKED on a decision (Round 2 STOP, below)." with "Round 2 answered; the inventory refresh is out of this PR by ruling option (c) (PR #766 comment 6259476788)."
  - **Lines 21-23:** replace "is generated and verified but not committed. Committing it makes the image-lock recipe check refuse, which needs a decision." with "is left out of this PR by that ruling; all four stale rows and the lock re-record are tracked on #737 (comment 6259477028)."
  - **Lines 30-31:** replace "Until the Round 2 decision lands, its "every touched gate rc 0" item is not met, so this PR only relates to #763 for now." with "By the Round 2 ruling, the inventory refresh is tracked on #737, so this PR closes #763."
  - **Line 114:** replace "The refresh is ready but is held for the Round 2 decision." with "By ruling option (c), the refresh and the image-lock re-record belong to #737."
  - **Line 125:** in the F1 row, replace "STOP for a decision." with "Out of this PR by ruling option (c); tracked on #737."
  - **Line 146:** replace "Decision needed on F1, one of:" with "Decided: option (c). The options were:".

### S1: SUGGESTION (Docs), carried from R657-1

- **Where:** `sw/firmware/ctrl/aecp/README.md:105-109`.
- **Suggestion:** optionally add "in this opt-in owner; the shipping image writes no channel-map record until #637". README:4-6 and `docs/design/SAVED_STATE_MATERIALIZATION.md:17` already bound the sentence, so this is optional.

### S2: SUGGESTION (Tests), carried from R657-1

- **Where:** `sw/firmware/ctrl/test/aecp_mutants.py:358-371`.
- **Suggestion:** optionally add the writer-side defect (`nvm_latch` skips an all-UNUSED payload) as a third named mutant. My R657-1 probe showed that the new test catches it and the rest of the arm does not.

Comment rule: the delta is unchanged since R657-1, which found no lane label, lane name, round, reviewer ID or comment ID in the new source comments. No new instance, so no residue.

## Lens results at this head

Every lens was applied this round to what round 2 changed (the PR body, the evidence branch, the ruling and the tracking). The source delta is byte-identical to R657-1, so the source-dependent results of R657-1 carry unchanged. Nothing they depend on moved.

```text
[R657] PASS Conformance — PR #766 comment 6259476788; #737 comment 6259477028; receipts/ci_input_scope.txt, ci_input_scope_base.txt; live PR body (Closes #763) — R657-1-F1 discharged by its outcome (b): the ruling plus a tracking issue that names exactly the four stale rows (2 inherited at base, 2 from this lane). The PR touches no other CI image input. The narrowed #763 acceptance (ruling 6257040042) stands as verified in R657-1 at this head.
[R657] PASS RTL — git diff --name-status e9cbb676..07c6c72f (unchanged four files; no HDL, firmware or store source); R657-1 RTL evidence carries — no delta since R657-1. The harness store-path change (aecp_arms.py:20) is as reviewed.
[R657] PASS Robustness — test_aecp.cpp:250-286 and R657-1 probe receipts (unchanged bytes) — no delta. The R657-1 probes (both directions, writer-side, non-empty-ignored, 25 shuffled + 10 isolated repeats) still apply.
[R657] PASS Tests — author-r2/receipts/round-b/gates/test_ctrl_firmware/extract.log (blob 72562576), summary.txt (blob da1896b8), round-2/count/classify.json; receipts/count_check.txt; hosted firmware-* contexts at exact head — R658-1-F2 resolved: 876 + 2 + 61 = 939 reproduced independently, 0 ESCAPED, both #763 mutants [ok]. R657-1-F1's Tests half is discharged as under Conformance.
[R657] PASS Docs — live PR #766 body vs author-r2/PR-BODY.md (blob 1bb5f908); sw/firmware/ctrl/aecp/README.md:101-141 (unchanged) — R657-1-R1 and R658-1-F3 applied. RS1 is wording residue only. S1 is optional.
```

## Execution and evidence used

- **No firmware bank re-run.** No source byte changed since my own R657-1 four-shard self-test bank and gate runs at this exact head, which all exited 0 and are published under `reviews/R657-1/receipts/`. The author's published round-B gate run (rc 0, `test_ctrl_firmware: PASS`) is the source-head execution evidence.
- **Probes this round:** read-only scripts only. `scripts/ci_input_scope.py` classifies the changed files against the CI image inputs and lists the stale inventory rows at base and head. `scripts/count_check.py` splits the gate log independently. `scripts/fetch_blobs.py` fetches the published blobs and verifies their git blob ids.
- **Hosted checks** are observational only. The manager owns hosted and act acceptance. A snapshot of the exact-head check runs (`receipts/hosted_check_runs_snapshot.tsv`, taken 2026-10-19T04:35:34Z) shows 63 completed/success and 1 skipped: "Physical gPTP (nightly and manual)", which was not run and is not evidence. Every firmware and docs context completed successfully.
- **Clone integrity** (`receipts/head_integrity.txt`):
  - HEAD, tree and `write-tree` all equal `c70d7afe…`;
  - the worktree and index equal HEAD, and the porcelain output, including ignored files, is empty;
  - `ls-files -s` equals `ls-tree -r` on mode, blob and path;
  - all five required submodule gitlinks match HEAD. The unused `external` gitlink is uninitialized.
  - No tracked byte was modified this round.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 6259476788; #737 comment 6259477028; ci_input_scope receipts (base and head); live PR body closing reference; R657-1 acceptance evidence (unchanged bytes) | R657-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| RTL | CLEAN | diff name-status (unchanged); R657-1 RTL artifacts: aecp_nvm.c:52-104, nvm_store.c:288-310 and 494-517, aecp_arms.py:13-90 | R657-1, unchanged at R657-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Robustness | CLEAN | test_aecp.cpp:250-286; aecp_state.c:71-86; R657-1 probe and repeat receipts | R657-1, unchanged at R657-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Tests | CLEAN | gate extract (blob 72562576); author-r2 summary.txt and classify.json; count_check.txt; aecp_mutants.py defect table at head; hosted firmware-* contexts | R657-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Docs | CLEAN (RS1 residue, S1 optional) | live PR #766 body vs author-r2/PR-BODY.md; aecp/README.md:101-141 | R657-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |

## Real limits

- **F1 is discharged by tracking, not by a change in the tree.** At merge, `ci/image/tool-inventory.json` keeps four stale `inputs` rows, two of them caused by this lane. `ci_tool_inventory.py --check` stays red until #737 lands the refresh and the lock re-record. AGENTS.md section 7 says that a finding moved to another Issue is not resolved. I accept the discharge for these reasons:
  - my round-1 required outcome explicitly allowed this route;
  - the refresh cannot be made rc 0 inside this PR without moving the image lock, so the conflict was published and decided rather than chosen privately;
  - no PR workflow runs `--check`;
  - the two rows are provenance digests, not shipped behaviour.

  The manager should treat the #737 refresh as the place where these two script changes are reviewed against the inventory.
- **In-tree rows only.** `ci_input_scope.py` hashes only the inventory rows present in the parent tree object. Rows inside submodules are skipped, and the delta does not touch any submodule.
- **No firmware bank re-run** this round (see above). Host only: the power cycle is the flash model, not a board cold cycle. Board acceptance belongs to #637. Physical calibration NOT RUN, and no hardware was used.
- **No manager source bank** ran at this head, and I claim none.

## Pending manager duties

- Carry RS1 to the residue checklist.
- Carry R657-1-F1 and R658-1-F1 to #737: the inventory refresh, the image-lock re-record and adding `--check` to the gates.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and own hosted and act acceptance.
- Confirm the second independent positive review before any authorized merge.

R657-2 FINISHED
