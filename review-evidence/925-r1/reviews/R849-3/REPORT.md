[R849] POSITIVE - exact head 0fdfdba72192003ea27ff831628fd9c124963df1

# R849-3: internal independent review of PR #932 (issue #925), round 4, narrow delta

- **Head:** `0fdfdba72192003ea27ff831628fd9c124963df1`, tree `8b3a953b65c712198b2fb279fd9c66e895d22036`. PR #932 reports the same head (`receipts/hosted-checks.txt`).
- **Delta:** `5f625090..0fdfdba7`, one commit. It touches two files, +5 -4: `docs/design/SPLIT_CONTROL_MEMORY.md` (lines 145, 173 and 174) and `sw/litex/ctrl_memory.py` (one `#:` comment, lines 250-251).
- **Prior verdicts at the base:** R850-2 POSITIVE at `5f625090`. R849-2 NEGATIVE at `5f625090`, on F1 (MINOR, Docs) only, with R1 (RESIDUE) and suggestions S1 and S2.
- **Author evidence:** packet `review-evidence/925-r1/author-r4` (archive `fc2f4678`) and REVIEW READY #925 issuecomment-6942378185.

## Summary

All five lenses were applied to the delta. R849-2 F1 is resolved, and so is R849-2 R1. Nothing in the delta changes code behaviour:

- `ctrl_memory.py`'s AST, with comments ignored, is identical to the base's.
- The tree changes only the two blobs named above, and no gitlink moves.
- The author's image-identity receipt shows all 24 images byte-identical between `5f625090` and `0fdfdba7`.

There is no new MINOR, MAJOR or BLOCKER finding. I record one wording residue (R2) and two optional suggestions (S3, S4). R849-2's S1 and S2 are still open as suggestions, which the author chose not to take.

## Prior findings at this head

| Prior finding | Status at `0fdfdba7` | Evidence |
|---|---|---|
| R849-2 F1, MINOR, Docs: `SPLIT_CONTROL_MEMORY.md:145` and `:173-174` gave the old cap and the old planted ledgers | **Resolved** | `:145` now gives the 59.0 and 60.5 caps as the state until #925. It cites the owner's decision of 2026-11-15 (#665 issuecomment-6892332745) and gives the entries as they stand: 59.0 and 61.0, refused at 59.5 and 61.5. That matches `ctrl_memory.LEDGERED` (`ctrl_memory.py:257` 59.0, `:268` 61.0) and `ctrl_memory_ledger.py` `REFUSED` (`:58` 59.5, `:65` 61.5). `:173` now reads "plans 61.5" and `:174` "plans the platform's 61.0". These match `planted()` (`ctrl_memory_ledger.py:128` `{"tiles": 61.5}`, `:130` `{"tiles": 61.0}`). The decision text matches the paraphrase: caps no longer stop conditions for the flip lanes, and an entry raised to the measured size at the next half tile (`receipts/owner-decision-6892332745.md`). `:145` no longer contradicts `:138` or `:148`. The author's `test_ctrl_memory.log` at `0fdfdba7` shows both planted ledgers caught and rc 0. |
| R849-2 R1, RESIDUE, Docs: lane name in the `ctrl_memory.py:250` comment | **Resolved** | `:250-251` now read "as debt owed to the hybrid XIP work (#665 decision D3))", which is the exact fix R849-2 asked for. No `#` comment in `ctrl_memory.py` at head carries `S14`, a reviewer ID or a round label (`receipts/f1-r1-check.txt`). The `owed` string literals (`:257-266`, `:269-281`) are data and are unchanged, as R1 stated. |
| R849-2 S1, SUGGESTION, Tests | Open, optional | Not taken (REVIEW READY). The delta does not touch its scope. |
| R849-2 S2, SUGGESTION, RTL and Robustness | Open, optional | Not taken. The delta does not touch its scope. |
| R850-1 F1 and F2, R849-1 F1 to F4 | Resolved at `5f625090` (R849-2) | The delta does not touch the firmware, so these stay resolved. |

## Findings

### R2 - RESIDUE - Docs - `sw/litex/ctrl_memory.py:251`: the re-worded comment leaves a one-word line

- **Where:** the R1 fix wrapped the comment as `...as debt owed to the hybrid XIP work (#665` / `#: decision D3)). The` / `#: platform's image is linked...`. Line 251 holds 21 characters, inside a block wrapped at about 115.
- **Authority:** wording and layout only. It changes no code, figure, test or claim, and it passes the Python idiom gate (`receipts/py_idiom.log`: over-long line 0).
- **Exact fix:** reflow lines 250-253 so that "The platform's image is linked at every point..." continues on full-width lines.
- **Status:** RESIDUE. It does not make the verdict negative.

### S3 - SUGGESTION - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:148`: a durable document cites "#925's round-3 head"

- **Where:** `:148` says "`plat_ledger.py` at #925's round-3 head". This line predates the delta (`git blame`: `44265574`).
- **Why:** after merge, the review-round label means nothing to a cold reader of the design document. A commit (`5f625090`) or "#925's head" would stay true. This is not a source comment, so the owner's comment rule does not apply, and the figures are right.
- **Optional change:** replace "round-3 head" with the commit or with "head".

### S4 - SUGGESTION - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:132`: the list of authorities omits the decision of 2026-11-15

- **Where:** `:132`, "Two images may plan past the budget ... (#665 rulings 6412739248, 6425357821 and 6505997821, and the owner's decision of 2026-11-12)". The platform's current 61.0 now rests on the decision of 2026-11-15, which `:145` and `:148` cite but `:132` does not. This line predates the delta.
- **Optional change:** add the decision of 2026-11-15 to `:132`'s list.

## Lens results at `0fdfdba7`

```text
[R849] PASS Conformance - docs/design/SPLIT_CONTROL_MEMORY.md:145,:173-174 against ctrl_memory.py:257,:268 (LEDGERED), ctrl_memory_ledger.py:58,:65,:128,:130 and #665 issuecomment-6892332745 - the stated entries, refusals and plants equal the ledger contract and the owner decision; no code in the delta (AST identical, receipts/ast_ctrl_memory.txt), so R849-2's Conformance at 5f625090 carries
[R849] PASS RTL - receipts/delta-identity.txt, receipts/restore-check.txt - only two blobs changed, no HDL, firmware, mailbox or build file, all six gitlinks unchanged; author identity receipt identity/images-5f625090-vs-0fdfdba7.txt (hash verified) shows 24 images byte-identical; R849-2's RTL at 5f625090 carries
[R849] PASS Robustness - receipts/delta-identity.txt; ctrl_memory.py AST identical - the delta adds no behaviour, input path or state; R849-2's Robustness at 5f625090 carries
[R849] PASS Tests - author-r4 receipts/ledger/test_ctrl_memory.log (hash verified; rc 0, PLANTED ledger rows at 61.5 and 61.0 caught, section 3 register row passes) and sw/litex/test_ctrl_memory.py, ctrl_memory_ledger.py unchanged in the delta - the doc now describes the plants the test holds; no test changed or weakened
[R849] PASS Docs - SPLIT_CONTROL_MEMORY.md:132-148,:165-178; ctrl_memory.py:231-253; receipts/{docs_check,doc_style,doc_style_self,em_dash_5f62,em_dash_16ba,doc_map,py_idiom,feature_status,solution_docs}.log all rc 0 - F1 and R1 resolved; R2 residue and S3/S4 suggestions only
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | SPLIT_CONTROL_MEMORY.md:145,:173-174; LEDGERED; `planted()`/`REFUSED`; owner decision 6892332745; firmware coverage from R849-2 | R849-3 (delta) on R849-2 | `0fdfdba72192003ea27ff831628fd9c124963df1` (firmware scope last changed at ancestor `5f625090`) |
| RTL | CLEAN | tree delta, gitlinks, image-identity receipt; R849-2's held-table and bound review | R849-3 (delta) on R849-2 | `0fdfdba72192003ea27ff831628fd9c124963df1` (scope unchanged since `5f625090`) |
| Robustness | CLEAN | AST identity of the only code file touched; R849-2's paths and probes | R849-3 (delta) on R849-2 | `0fdfdba72192003ea27ff831628fd9c124963df1` (scope unchanged since `5f625090`) |
| Tests | CLEAN | author `test_ctrl_memory.log` at head; test files unchanged; R849-2's plant campaigns | R849-3 (delta) on R849-2 | `0fdfdba72192003ea27ff831628fd9c124963df1` (test files unchanged since `5f625090`) |
| Docs | CLEAN | SPLIT_CONTROL_MEMORY.md sections 3 and 5 lines 132-178; ctrl_memory.py comment; nine docs gates run by me; author docs.yml replay | R849-3 | `0fdfdba72192003ea27ff831628fd9c124963df1` |

## What I ran and checked

- **Delta identity:**
  - `git ls-tree -r` at base and head differ in the two blobs alone.
  - `scripts/ast_same.py` reports `ctrl_memory.py` as SAME with comments ignored.
  - The changed lines in the author's `diff/0fdfdba7.diff` equal `git diff 5f625090..0fdfdba7`.
- **Author packet:**
  - All six receipts in `author-r4/receipts/INDEX.md` match their listed sha256 prefixes and byte sizes (`receipts/author_index_check.txt`).
  - The archive commit carries no cryptographic signature (`%G?` = N). The packet's integrity rests on its index hashes and on the archive commit id.
- **Docs gates at head, run by me with the pinned Markdown renderer in a scratch venv:** `docs_check.py`, `check_doc_style.py` and its `--selftest`, `check_em_dash.py --base` against both `5f625090` and `16ba667d`, `DOC_MAP.gen.py --check`, `check_py_idiom.py`, `check_feature_status.py` and `check_solution_docs.py`. All are rc 0.
- **`test_ctrl_memory.py`:** I could not run it here. It imports migen/LiteX, which this host's Python does not have (`receipts/test_ctrl_memory.log`, rc 1 on import). I rely on the author's hash-verified rc 0 log at `0fdfdba7`. With an identical AST and the test files untouched, the delta cannot change its result.
- **Restore:** the worktree and index match HEAD, with no untracked or modified files. The six gitlinks are as recorded (`receipts/restore-check.txt`).

## Real limits

- **No exact-head hosted evidence.** At review time `0fdfdba7` has 0 check runs (`receipts/hosted-checks.txt`). The manager owns hosted and act acceptance.
- **The ledger test is the author's receipt, not my run**, because LiteX is absent here. The image-identity, `plat_ledger.py` and full `docs.yml` replay results are also the author's receipts. I verified their hashes but did not re-run them.
- **Firmware, RTL-adjacent and test lens coverage carry from R849-2 at the ancestor `5f625090`.** Nothing in their scope changed, and this round did not re-execute their campaigns.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate: source base `16ba667d`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`. The PR's recorded base branch is `dev-soft-core`.
- Accept hosted and act evidence at the exact head.
- Run the bench gate: Listener Ready within 1 s of the Talker Advertise.
- Obtain the external review of this head.
- Carry R2 to the residue checklist. R849-2's R1 is now fixed and can come off it.
- Publish this report and the files in `MANIFEST.sha256`.

## Receipts

Listed in `MANIFEST.sha256`: `scripts/ast_same.py` and `receipts/*`.

R849-3 FINISHED
