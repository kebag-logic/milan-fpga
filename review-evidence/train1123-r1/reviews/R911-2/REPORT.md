[R911] NEGATIVE - exact head adc13dbdd1241b124c8877f1dda5318c1095e0df

Round R911-2, an internal cleared-context review of PR #988 (pf-train-1123 -> dev-soft-core) for issue #665.

- **Head and tree:** head `adc13dbdd1241b124c8877f1dda5318c1095e0df`, tree `cd1b498839072753c29811c7ef5a048d223b36de`.
- **Scope:** a narrow re-review of the delta `43076d0f..adc13dbd`: one commit, 5 files.
  - `git diff --stat 43076d0f..adc13dbd -- sw hdl configs third_party protocol-processor` is empty.
  - Round 1 and round 2 content is not re-reviewed. R912-1 was POSITIVE at `43076d0f`.

## Summary

- **The named case is fixed.** R911-1's F1 asked that a `srp-bound` pass given whole to THE TRANSMIT's build (two MRPDUs), over the slice, stay a failure.
  - It does now. R911-1's probe, run unmodified (sha256 `b7172b3e…`), prints "a failure" for both groups.
  - The self-test passes its 29 checks, including the exact 105,000 / 105,001 control.
  - The author's 6 planted defects are all caught.
  - The four re-grades match round 2, and every comment and citation residue from round 1 is resolved.
- **The cause is not fully fixed.** `transmit_slices` does not use `whole_grade.held`'s classification, which its own docstring claims it does.
  - It classes any build slice with at most one SRP frame as a build of one. That includes passes `whole_grade.held` never classes a build of one:
    - a pass whose AECP round did work;
    - an aged step.
  - So the THE TRANSMIT slice line of such a `srp-bound` pass is OWED #977 and fails nothing, with no build-one pass line beside it.
  - That is wider than the ruling, which owes only the bound path's build-of-one pass (N1, MINOR).
  - The self-test also never pins the clause that makes an ambiguous equal length fail closed (N2, MINOR).
- **No current figure changes.** Across the four legs, the only owed `srp-bound` slice line is the 171,645-cycle one, and it sits beside a `whole_grade` build-one pass line of the same length.

## Findings

### N1: MINOR, lenses `Conformance`, `Robustness`, `Tests`, `Docs`: a slice line is owed for passes `whole_grade.held` does not class a build of one

**Where:**
- `tb/verilator/ctrl_service_budget/kept_grade.py:206-217` (`transmit_slices`, line 216 classes by frame count only);
- `kept_grade.py:254-263` (`Disposition.owes`);
- `tb/verilator/ctrl_service_budget/README.md:790-792`.

**Authority and evidence:**
- **The ruling.** #969's ruling of 2026-11-23 (issuecomment-7116192252, item 2) owes to #977 only "the bound path's build-of-one pass and its pass over THE SHARE".
- **The focus of this round.** It asks that `owes` owe srp-bound's THE TRANSMIT slice line only for a build of one, by `whole_grade.held`'s classification.
- **`whole_grade.held`** (`whole_grade.py:52-75`) classes a pass `build-one` only under all of these conditions:
  - its round is idle (`round_idle`, at most 1,000 cycles of AECP modules);
  - it is not an aged step, which it classes `step`;
  - it holds a build and at most one SRP frame.
- **`transmit_slices` skips both of the first two filters.** It takes every `slice_grade` `build` slice over the limit and labels it `build-one` whenever it holds at most one SRP frame. Its docstring (`kept_grade.py:207-209`) says "by the pass's kind as whole_grade.held tells it", which is not what the code does for those passes.

**Probe** (`tools/probe_owes_edges.py`, receipt `receipts/probe-owes-edges.txt`):
- The probe uses the harness's own `Synthetic` logs at 1x1/1if, with `slice_grade.held`, `whole_grade.held`, `run.stated_misses` and `Disposition`.
- **`idle-one`** (the self-test's case, as a control): `whole_grade` reports `build-one` 95,001. The build-one line and the slice line are both owed. This is correct.
- **`busy-one`**: the same pass with `mods=aecp:5000`.
  - `whole_grade` over: `[]`, so run.py prints no build-one pass line.
  - The slice line "srp-bound: a tier-2 slice of THE TRANSMIT's build of 95,001 CPU cycles" is **OWED #977** and nothing fails.
- **`aged-one`**: the same pass marked `step=1 aged=1`. `whole_grade` over: `[]`. The slice line is **OWED** and nothing fails.
- **`equal`**: a build of one and a whole pass, both 98,000 cycles. Both slice lines **FAIL**. This is correct: the ambiguous case fails closed.

**Mutant** (`tools/mutants_r911_2.py`, receipt `receipts/mutants-r911-2.txt`):
- A `transmit_slices` restricted to `whole_grade.held`'s filters (round idle, not aged) leaves all 29 checks passing ("idle-filtered: 0 of 29 checks fail").
- So the self-test cannot tell the head's classification from the one the ruling describes.

**Impact:**
- No figure moves at this head. In the four published re-grades, the only owed srp-bound slice line is 171,645. It sits beside the owed build-one pass line of 171,645 (`run-regrade-8x8-1if-answering-ports-r3.txt:15,21`).
- A later image, though, could carry one of two `srp-bound` passes that overruns `CTRL_LOOP_SLICE_US`:
  - a pass whose AECP round did work, which is the round's cost and not registration cost;
  - an aged step.
- Either would be graded OWED #977 and pass the formal measurement silently. This is the same shape as F1, for a smaller set of passes.

**Required outcome:**
- Owe a `srp-bound` THE TRANSMIT slice line only where `whole_grade.held` classes that pass `build-one`. Every other `srp-bound` build slice over the limit stays a failure, including busy-round and aged-step passes.
  - One route is to derive the classification from `whole_grade.held`'s own span or kind, in place of re-counting frames over every build slice.
  - Alternatively, publish a ruling that extends item 2 to those passes, and cite it.
- Add self-test checks that a busy-round pass and an aged-step pass with one build, over the slice in `srp-bound`, keep their slice line failing.
- Make `transmit_slices`' docstring and README:790-792 state the classification the code applies.

**Verification:**
- `tools/probe_owes_edges.py` reports `busy-one` and `aged-one` FAILS, and `idle-one` OWED.
- The head's frame-count-only rule, applied as a mutant against the fixed code, makes at least one self-test check fail.
- The four re-grades are unchanged: 0 findings, owed 4/4/5/6, and 171,645 still OWED.

### N2: MINOR, lens `Tests`: the fail-closed clause for ambiguous equal lengths is not pinned

**Where:**
- `kept_grade.py:263` (`cycles not in self.slices['build']`);
- `kept_grade.py:445-537` (`selftest_files`).

**Evidence:**
- The clause is what makes a build of one and a whole pass of the same length both fail. That behaviour is correct at this head: `probe_owes_edges.py` case `equal` gives FAILS.
- Deleting the clause still leaves all 29 checks passing ("drop-fail-closed: 0 of 29 checks fail", `receipts/mutants-r911-2.txt`).
- The in-one-log check (`kept_grade.py:480,506`) uses lengths that differ (95,001 and 98,000), so it never reaches the clause.
- AGENTS.md section 5 asks for self-checking tests of changed behaviour. This is new behaviour, and one of the properties this round was asked to verify.

**Impact:** A later edit could drop the clause, owe the whole pass's slice whenever its length equals a build of one's, and keep the self-test green.

**Required outcome:** Add a self-test check with a build of one and a whole pass of equal cycles in `srp-bound`. Both slice lines must fail.

**Verification:** The `drop-fail-closed` mutant in `tools/mutants_r911_2.py` makes at least one check fail.

### S3: SUGGESTION (lens `Docs`)

- **What:** `README.md:792` is 128 characters wide, against about 120 for the rest of its re-wrapped paragraph (784-800).
- **Fix:** Re-wrap the paragraph. This is cosmetic only.

### S1, retained as optional (lens `Docs`)

- **Where:** the PR body still cites the stated-cost rule as "#665 ruling item 4" in two places:
  - the statement table row for `EIGHT_ONE['aecp_long']`;
  - the references bullet "ruling item 4 of 2026-11-20".
- The same citation also appears at `poll_grade.py:107`, which this delta does not touch.
- The governing 2026-11-23 rulings cite it the same way, so it stays a suggestion.

## Prior public findings on this PR, resolved or retained at this head

These were read only after the findings above were written.

| ID (round) | Status at `adc13dbd` | Evidence |
|---|---|---|
| F1 (R911-1, MINOR) | **Named case RESOLVED; cause partly open as N1** | R911-1's probe, unmodified, sha256 `b7172b3e8ee2eafc…` (matches the published copy at `8d71efcb`), gives "RESULT srp-bound: the whole build pass's slice line is a failure" (`receipts/probe-whole-slice.txt`). The self-test check "a srp-bound pass given whole … its slice line FAILS, never owed" passes. srp-kept is unchanged, and its slice line still fails. The author's planted defects: 6 of 6 caught (`author-r3/receipts/budget/kept-grade-planted-r3.txt`). F1's required outcome, "every other srp-bound build slice over the slice stays a failure", is not met for busy-round and aged-step passes (N1). |
| R1 (R911-1, RESIDUE) | RESOLVED | `poll_grade.py:135-137` carries the exact fix, and only comment lines changed. `EIGHT_ONE` is byte-unchanged at `poll_grade.py:138-139` (`receipts/delta.diff`). The new citation matches #665 issuecomment-7093949712, third bullet of "The ruling". |
| R2 (R911-1, RESIDUE) | RESOLVED | `kept_grade.py:71` reads `AMENDED = "#969's ruling of 2026-11-23"`. No `issuecomment` appears in `kept_grade.py`, `poll_grade.py` or `kept_window.py`. The link stays in `SPLIT_CONTROL_MEMORY.md:3312`, a doc. |
| R3 (R911-1, RESIDUE) | RESOLVED | The PR body reads "The six open PRs (#958, #959, #975, #971, #978, #974) are superseded … #961 merged on dev-soft-core at aa30d77f, which closed #950 and #954." |
| R4 / D1 (R911-1, R912-1, RESIDUE) | RESOLVED | The PR body reads "Its own commits after the merges make no RTL, mailbox-contract, lwSRP or owner-bound …". |
| S1 (R911-1, SUGGESTION) | RESOLVED in source, retained in the PR body | `SPLIT_CONTROL_MEMORY.md:3310`, `poll_grade.py:135-137`, `kept_grade.py:24,72` and `README.md:787` cite `record_classes.rule` and the 2026-11-23 ruling. The PR body still cites item 4 (see S1 above). |
| S2 (R911-1, SUGGESTION) | RESOLVED | `kept_window.py:33-35` now names srp-bound's whole builds as held. |
| T1 (R912-1, SUGGESTION) | RESOLVED | `kept_grade.py:369-370,392-394`: kept 105,000 against bound 100,000 holds, and 105,001 breaks. Both the `kept_within` arithmetic and `held` are checked. The mutation "kept <= bound strict (<)" is caught. |

## Evidence checked, by focus item

1. **The delta is confined.**
   - `git diff --stat 43076d0f..adc13dbd -- sw hdl configs third_party protocol-processor` is empty.
   - Five files change: `kept_grade.py`, `kept_window.py`, `poll_grade.py`, `README.md` and `SPLIT_CONTROL_MEMORY.md`.
2. **The self-test** (`receipts/selftest.log`, rc 0): `kept_grade selftest: PASS (29 checks)`. It matches the author's `kept-grade-selftest-r3.txt`. The checks this round needed:
   - the exact +5 % control;
   - the build of one owed;
   - the whole pass failing;
   - both in one log;
   - srp-kept's whole pass failing.
3. **The published packet** (`review-evidence/train1123-r1/author-r3` at `8d71efcb`): all 18 sha256 prefixes in `receipts/INDEX.md`, recomputed on the published bytes, match (`receipts/evidence-verify.txt`).
4. **The four re-grades.** Round 1's logs are not public, so they were not re-run here (see the limits section). Verified from the published receipts:
   - All four standalone `kept_grade` runs report `PASS (0 finding(s))`, with 4 (1x1 arm A), 4 (1x1 answering-ports), 5 (8x8 arm A) and 6 (8x8 answering-ports) owed.
   - `run.py --regrade` exits 0 with 0 STATED and 0 REFUSED in all four. It prints 9/9/12/13 OWED.
   - 171,645 is OWED both as a build-one pass and as THE TRANSMIT's slice (`run-regrade-8x8-1if-answering-ports-r3.txt:15,21`).
   - Log sha256 prefixes are printed per leg in `regrade-summary-r3.txt`.
   - Against round 2's receipts, all eight bodies are identical below the `#` header, except round 2's trailing wrapper line `rc=0`. Round 3 records that line in `regrade-summary-r3.txt` instead, so the tools' output is byte-identical (`receipts/evidence-verify.txt`).
5. **The ledger.**
   - The 24 `(sha256, path)` image lines extracted from `plat-ledger-43076d0f.txt` (round 2) and `plat-ledger-adc13dbd.txt` (round 3) are identical, 24 of 24, compared here independently.
   - `plat_ledger: PASS (0 finding(s))`, with all four POINT lines PASS.
6. **The comment rule, privacy and wording** over the 123 added lines (`receipts/delta.diff`). None of the following is present:
   - lane labels, round or reviewer IDs;
   - tool or model names;
   - host paths;
   - em dashes.
   - The one `issuecomment` in the added lines is the pre-existing link in `SPLIT_CONTROL_MEMORY.md:3312`, a doc, kept as R2's fix asked.
7. **Citations.**
   - `AMENDED` matches #969 issuecomment-7116192252 (2026-11-23, item 2).
   - The `poll_grade.py:135-137` and `SPLIT_CONTROL_MEMORY.md:3310` authority matches #665 issuecomment-7093949712 ("Any further statement over is raised the same way only if every owner bound holds").
8. **The doc claim "none arises at either point"** (`SPLIT_CONTROL_MEMORY.md:3312`) agrees with the 0 STATED lines in all four `run.py --regrade` receipts.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| `Conformance` | UNCLEAN (N1) | #969 issuecomment-7116192252 item 2 against `kept_grade.py:206-263`. `whole_grade.py:52-75`. `slice_grade.py:50-80`. `run.py:187-217,268`. `receipts/probe-owes-edges.txt`, `receipts/probe-whole-slice.txt`. | R911-2 | `adc13dbdd1241b124c8877f1dda5318c1095e0df` |
| `RTL` | CLEAN | The stat `43076d0f..adc13dbd -- sw hdl configs third_party protocol-processor` is empty, so no RTL, firmware or config is in the delta. The 24 image hashes are identical to `43076d0f`'s (`receipts/evidence-verify.txt`). The harness interface `run.py` uses is unchanged: the `Disposition(groups, out, spec)`, `.owes(line)` and `.stated(lines)` signatures, at `kept_grade.py:234-270`. The six submodule gitlinks are unchanged (`receipts/restore.txt`). | R911-2 | `adc13dbdd1241b124c8877f1dda5318c1095e0df` |
| `Robustness` | UNCLEAN (N1) | Busy-round, aged-step, equal-length, two-frame and srp-kept cases through `Disposition` (`tools/probe_owes_edges.py`, `tools/probe_whole_slice.py`). `stated_cycles` parsing at `kept_grade.py:220-224` against `run.py:215-217`'s format. | R911-2 | `adc13dbdd1241b124c8877f1dda5318c1095e0df` |
| `Tests` | UNCLEAN (N1, N2) | `kept_grade.py --selftest`: 29 checks PASS (`receipts/selftest.log`). The author's 6 of 6 planted defects (`kept-grade-planted-r3.txt`). The reviewer's mutants: 2 of 2 survive (`receipts/mutants-r911-2.txt`). | R911-2 | `adc13dbdd1241b124c8877f1dda5318c1095e0df` |
| `Docs` | UNCLEAN (N1: the `transmit_slices` docstring at `kept_grade.py:207-209` and `README.md:790-792` state a `whole_grade.held` classification the code does not apply) | `README.md:784-800`. `SPLIT_CONTROL_MEMORY.md:3310-3312`. The `kept_grade.py:11-43` docstring. `kept_window.py:30-35`. The `poll_grade.py:132-137` comment. The PR body at head `adc13dbd`. | R911-2 | `adc13dbdd1241b124c8877f1dda5318c1095e0df` |

Lenses the delta does not touch, covering round 1 and round 2 content, keep their prior verdicts at `43076d0f` (R912-1 POSITIVE).

## Real limits

- **The re-grades were not re-run here.** Round 1's measured `srp-kept` and `srp-bound` logs are in the author's private scratch and are not in the public packet, so this round has no copy.
  - Re-grade figures are checked from the author's published, hash-matched receipts, and against round 2's receipts. They are not independently re-executed.
  - The log sha256 prefixes in `regrade-summary-r3.txt` could not be recomputed.
- **No other source gates were run.** No simulation, firmware build, ledger build or docs gate was run here. The ledger and docs evidence is the author's published receipts.
- **No manager source bank runs at this head**, and none is claimed or inferred here.
- **Physical calibration was NOT RUN.** Field skips are not hardware proof.
- **Hosted checks were in flight at the time of reading** (`receipts/hosted-checks-adc13dbd.txt`): 10 success, 1 skipped, and 35 queued or in progress, including the Verilator shards and `yosys-elaboration`. They are not used as evidence here.
- **The clone was restored.** It was never edited. The ignored `__pycache__` directories created by this round's own self-test run were removed, and none held an older file.
  - After that, HEAD and tree are as above, porcelain is 0 (including ignored files), and the index matches HEAD's tree (`receipts/restore.txt`).

## Pending manager duties

- Carry N1 and N2 to the author. Both are MINOR and leave `Conformance`, `Robustness`, `Tests` and `Docs` unclean at this head.
- Carry S3 and the retained S1 to the suggestion list. Both are optional.
- Validate the current-dev merge candidate at the merge turn: source base `aa30d77f75cd97b3a29878ca0ed68010a7629266`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and native banks. Then link the receipts.
- Own the hosted and local-replica acceptance on the exact head.
- Physical calibration remains outstanding.

R911-2 FINISHED
