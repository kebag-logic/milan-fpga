[R911] POSITIVE - exact head 300da99beed5bb1c77e4b04af0bb4f9369856e0d

# R911-3: internal cleared-context re-review of PR #988 (issue #665), narrow delta `adc13dbd..300da99b`

## Summary

- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. All five lenses were applied and are covered clean at `300da99beed5bb1c77e4b04af0bb4f9369856e0d` (tree `3b1a7562a4d6f954df7cd8f32c5c6e96f049d465`).
- **Scope.** The scope is one commit, `adc13dbd..300da99b`, touching two files:
  - `tb/verilator/ctrl_service_budget/kept_grade.py`: +79/-43;
  - `tb/verilator/ctrl_service_budget/README.md`: +13/-3.
- **No product change.** `git diff --stat adc13dbd..300da99b -- sw hdl configs third_party protocol-processor` is empty, and no gitlink moved (`receipts/restore.txt`).
- **N1 (R911-2, MINOR): RESOLVED.** `transmit_slices` now takes its build-of-one classification from `whole_grade.held`'s own `over` list, matched by kind and by pass start. It restates no conditions.
  - My R911-2 probe, unmodified, gives `idle-one` OWED, and `busy-one`, `aged-one` and `equal` FAIL.
  - The prior head's frame-count-only rule, applied as a mutant, makes 2 of 32 checks fail.
- **N2 (R911-2, MINOR): RESOLVED.** Deleting the equal-length fail-closed clause now makes 1 of 32 checks fail.
- **S3 (R911-2, SUGGESTION): RESOLVED.**
- **New this round:**
  - **S4** (SUGGESTION, `Tests`): the kind filter inside `transmit_slices` is not pinned by the self-test. Removing it cannot change any run's verdict at a listed shape.
  - **R5** (RESIDUE, `Docs`): one stale clause in the `Disposition.owes` docstring.
- **Retained from earlier rounds:** S1, optional.
- **Order of work.** I wrote my verdict and ledger to `receipts/verdict-before-prior-findings.txt` before reading any prior public finding. R5 was found afterwards. It is wording only and does not change the verdict.

## Findings

### S4: SUGGESTION, lens `Tests`: the `BOUND_OWED_BUILDS` kind filter in `transmit_slices` is not pinned

- **Where:** `tb/verilator/ctrl_service_budget/kept_grade.py:213`, the clause `if o['kind'] in BOUND_OWED_BUILDS`, and `selftest_transmit` at `kept_grade.py:474-512`.
- **Evidence:**
  - **The mutant survives.** `scripts/mutants_r911_3.py` mutant `any-over-kind` owes the slice of any pass in `whole_grade.held`'s `over` list, whatever its kind. It leaves 0 of 32 checks failing (`receipts/mutants-r911-3.txt`).
  - **Why the self-test misses it.** The self-test's aged-step pass is 95,001 cycles. That is inside the step's stated 97,500 at 1x1/1if, so `whole_grade.held` never lists it as `over`.
  - **The probe** (`scripts/probe_aged_over_step.py`, `receipts/probe-aged-over-step.txt`) plants an aged step of 97,501 cycles, which is over both the slice and the step cost:
    - At the head, the slice line FAILS. This is correct.
    - With the filter removed, the slice line is printed OWED #977.
- **Impact:** None on any verdict.
  - In that case the step's own STATED line ("a step pass of 97,501 CPU cycles, over its stated 97,500") still fails, because it is not in `OWED_KINDS`.
  - A `build` over its stated cost is a `held` finding, and a finding stops `Disposition` from owing anything at all.
  - At every listed shape, a step over the slice is either within the step cost (not in `over`) or over it (its own STATED line fails). At 8x8/1if the slice is 1,475 us and the step cost 975 us; at 1x1/1if they are 950 us and 975 us.
  - So a later edit that drops the filter would only mislabel one line of a run that already fails. That is why this is a suggestion.
- **Suggested outcome:** Add a self-test check with an aged step in `srp-bound` over both the slice and `CTRL_LOOP_STEP_PASS_US`. Its THE TRANSMIT slice line must stay failing.
- **Verification:** The `any-over-kind` mutant in `scripts/mutants_r911_3.py` makes at least one check fail.

### R5: RESIDUE, lens `Docs`: `Disposition.owes`' docstring describes the `'build'` set by its old meaning

- **Where:** `tb/verilator/ctrl_service_budget/kept_grade.py:256-258`. These lines are unchanged in the delta, but the delta changes what the docstring describes.
- **Evidence:**
  - The docstring says the slice line is owed only where its cycles are a build of one's "and none given whole to the build is".
  - At this head, `transmit_slices` (`kept_grade.py:209-211,217`) puts every other over-slice build into `'build'`: a pass given whole to the build, one whose round did work, and an aged step's.
  - The code checks `cycles not in self.slices['build']` (`kept_grade.py:264`), so a busy-round or aged-step slice of equal cycles also blocks the owing. The docstring omits this.
- **Impact:** Wording only. No figure, check, verdict or claim moves.
- **Exact fix:** In `kept_grade.py:257-258`, replace "and none given whole to the build is" with "and no other build slice of those cycles is (a pass given whole to the build, one whose round did work, an aged step's)".

### S1: retained as optional, lens `Docs` (from R911-1, retained by R911-2)

- The PR body still cites the stated-cost rule as "#665 ruling item 4" in two places: line 96, the `EIGHT_ONE['aecp_long']` row, and line 122.
- `poll_grade.py:107` also still cites "ruling item 4 of 2026-11-20".
- Neither is in this delta. It stays a suggestion for the reasons R911-2 gave.

## Prior public findings on this PR, resolved or retained at this head

I read these only after writing `receipts/verdict-before-prior-findings.txt`. The PR comments read were R912-1, R911-1 and R911-2. The PR has no review objects.

| Finding | Status at `300da99b` | Evidence |
|---|---|---|
| N1 (R911-2, MINOR; `Conformance`, `Robustness`, `Tests`, `Docs`) | **RESOLVED** | The classification now comes from `whole_grade.held` itself: `kept_grade.py:213` builds `ones` from its `over` entries of kind `build-one`, keyed by `start_sys`, and line 217 classes each over-slice build slice by its own start.<br>The starts match exactly, because `slice_grade.slices` gives a build slice its pass's `start_sys` and `cycles` (`slice_grade.py:58-62`), and `whole_grade.held` spans the same `p.start_sys` (`whole_grade.py:60`).<br>`scripts/probe_owes_edges.py` (sha256 `6c61c36c…`, identical to R911-2's published copy) gives idle-one OWED and busy-one, aged-one and equal FAIL (`receipts/probe-owes-edges.txt`).<br>The prior head's frame-count-only rule as a mutant fails 2/32 checks, and each single filter removed fails 1/32 (`receipts/mutants-r911-3.txt`).<br>The new self-test checks are at `kept_grade.py:501-506`, the docstrings at `kept_grade.py:40-46,208-212`, and the README at `README.md:790-797`. |
| N2 (R911-2, MINOR; `Tests`) | **RESOLVED** | `drop-fail-closed: 1 of 32 checks fail`. The equal-length check at `kept_grade.py:507-512` kills the mutant (`receipts/mutants-r911-2.txt`; `scripts/mutants_r911_2.py` is unmodified, sha256 `2acf7e5d…`). |
| S3 (R911-2, SUGGESTION) | **RESOLVED** | `README.md:782-805` are all 119 columns or fewer. The widest line in that paragraph is 119, and no added line is over 120 (`receipts/residue-scan.txt`). |
| S1 (R911-1/R911-2, SUGGESTION) | Retained, optional | See above. |
| F1, R1-R4, S2 (R911-1) | Resolved at `adc13dbd` per R911-2; not re-opened | The delta touches none of their artifacts. F1's named case, a whole build pass over the slice, still fails: `scripts/probe_whole_slice.py` (unmodified) gives FAIL in both groups (`receipts/probe-whole-slice.txt`). |
| D1 (R912-1, RESIDUE) | Resolved per R911-2; unchanged | The delta does not touch the PR body text that D1 concerned. |
| T1 (R912-1, SUGGESTION) | Resolved; still present | The self-test still checks that 105,000 against 100,000 holds and one cycle more breaks (`receipts/selftest.log`). |

## Evidence checked, by focus item

1. **N1: `transmit_slices` takes build-of-one from `whole_grade.held`.**
   - Code: `kept_grade.py:207-218`. It restates no conditions (round idle, not aged, at most one SRP frame). It takes the pass kinds `whole_grade.held` puts in `over` and filters them by `BOUND_OWED_BUILDS` (`kept_grade.py:85`).
   - My R911-2 probe and mutants, unmodified, produce what the focus requires:
     - idle-one OWED; busy-one, aged-one and equal FAIL;
     - drop-fail-closed caught;
     - idle-filtered equivalent (0/32, because the head now applies that classification).
2. **N2: the equal-length clause has a check that dies when it is deleted.** Yes, 1/32 (see the table above).
3. **The docstring's claim that the slice is at least the build-of-one cost at every listed shape is true.** From `ctrl_loop.h:361-391` (`receipts/shapes-slice-vs-build-one.txt`):

   | Shape | `CTRL_LOOP_SLICE_US` | `CTRL_LOOP_BUILD_ONE_PASS_US` |
   |---|---:|---:|
   | 1x1/1if | 950 | 735 |
   | 8x8/1if | 1475 | 1475 (equal) |
   | 1x1/2if | 1300 | 1215 |
   | 8x8/2if | 1300 | 1215 |

   - Both limits convert to CPU cycles by the same `us * cpu_hz // 1_000_000`, and both comparisons are strict.
   - A build slice's cycles are its whole pass's (`slice_grade.py:62`). So a build of one over the slice is over its build-one cost, and lands in `whole_grade.held`'s `over` list.
   - The fallback the docstring states also holds by construction: a pass not in `ones` is classed `'build'` and fails.
4. **The self-test runs 32 checks.** `python3 -I -B tb/verilator/ctrl_service_budget/kept_grade.py --selftest` gives rc 0, 32 `[ok]` lines and "PASS (32 checks)" (`receipts/selftest.log`, `receipts/selftest.rc`). This matches the author's `kept-grade-selftest-r4.txt`, the README (`README.md:800`) and the PR body (line 178).
5. **The four re-grades match round 3 byte for byte below the header.**
   - All 8 receipts (4 `kept_grade` and 4 `run.py --regrade`) are identical to the `author-r3` ones below the `#` lines (`receipts/regrade-compare.txt`).
   - The 8x8/1if `answering-ports` re-grade still prints "OWED srp-bound: a tier-2 slice of THE TRANSMIT's build of 171,645 CPU cycles … owed to #977" (line 21), beside the owed build-one pass of 171,645 at bus cycle 606660065 (lines 14-15).
   - `kept_grade` reports 0 findings in all four, with 4/4/5/6 owed, and `run.py` reports 0 STATED and 0 REFUSED (`regrade-summary-r4.txt`).
6. **The `plat_ledger` image hashes are identical to `adc13dbd`'s.** All 24 (sha256, path) lines and every POINT and verdict line of `plat-ledger-300da99b.txt` equal `plat-ledger-adc13dbd.txt` (`receipts/ledger-hashes-compare.txt`). The ledger is PASS with 0 findings.
7. **The `ctrl_boundary` log is identical.** I compared the full receipt with the head SHA, durations, clock times, temp-dir suffixes and unit names normalized: 363 against 363 lines, no differing hunk (`receipts/ctrl-boundary-compare.txt`). The author's own normalized full-log diff is empty. The gate reports PASS.
8. **The evidence packet is intact.**
   - All 34 `author-r4/receipts/INDEX.md` rows match their published bytes, by sha256 prefix and byte count.
   - All 37 `MANIFEST.json` entries under `author-r4/` match `published_sha256`.
   - Only `HANDOFF-r4.md` is path-redacted.
   - Source: evidence commit `f2c9d42524ec5ddee9d602789bf15ff5ac912407` (`receipts/evidence-verify.txt`, `scripts/verify_evidence.py`).
9. **Docs gates.** Every `docs.yml` gate step at `300da99b` has rc 0 (`docs-workflow-steps-300da99b.txt`). This includes the Python idiom gate (54/54) and `docs_check` (0 findings). The exceptions:
   - 3 SDK install-verify steps fail with rc 1. The cause is the environment (no SDK provenance receipt on that host), the same as in rounds 2 and 3.
   - 24 steps are skipped.
   - The superseded first commit, `6ab79cf6`, failed the Python idiom gate. It was amended to `300da99b`, which passes.
10. **Public-text rules.**
    - None of the 92 added lines contains a bench lane label, lane name, review round, reviewer ID, issue-comment ID, or tool or model name (`receipts/residue-scan.txt`).
    - The PR body names no private host, user or tool. The only pattern hit was the `gptp-processor` submodule name.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| `Conformance` | CLEAN | `kept_grade.py:207-218` against `whole_grade.py:52-75`. #969's 2026-11-23 amendment item 2 owes only srp-bound's build-of-one pass (as R911-2 reconstructed it; `kept_grade.py:71` `AMENDED`). `ctrl_loop.h:361-391` slice against build-one. The 171,645 owed line in `run-regrade-8x8-1if-answering-ports-r4.txt:14-15,21`. | R911-3 | `300da99beed5bb1c77e4b04af0bb4f9369856e0d` |
| `RTL` | CLEAN | `git diff --stat adc13dbd..300da99b -- sw hdl configs third_party protocol-processor` is empty, and the gitlinks are unchanged (`receipts/restore.txt`). The 24 image hashes are identical to `adc13dbd`'s (`receipts/ledger-hashes-compare.txt`). The `ctrl_boundary` receipt is identical after normalization (`receipts/ctrl-boundary-compare.txt`). The delta has no RTL or firmware scope, so the prior verdict (R911-2) carries. | R911-3 | `300da99beed5bb1c77e4b04af0bb4f9369856e0d` |
| `Robustness` | CLEAN | Cases run through `Disposition`: busy-round, aged-step, equal-length, two-frame whole pass, srp-kept, and an aged step over its step cost (`receipts/probe-owes-edges.txt`, `probe-whole-slice.txt`, `probe-aged-over-step.txt`). The `start_sys` keying between `slice_grade.py:58-62` and `whole_grade.py:60`. | R911-3 | `300da99beed5bb1c77e4b04af0bb4f9369856e0d` |
| `Tests` | CLEAN (S4 SUGGESTION) | Self-test 32/32 (`receipts/selftest.log`). `kept_grade.py:453-512` (`disposed`, `unowed`, `selftest_transmit`). Mutants `mutants_r911_2.py` (drop-fail-closed caught, idle-filtered equivalent) and `mutants_r911_3.py` (frame-count-only, no-round-filter, no-aged-filter and all-build-one caught; any-over-kind survives, S4). The author's `new-checks-on-adc13dbd-r4.txt` (2 of the 7 new checks fail on `adc13dbd`). | R911-3 | `300da99beed5bb1c77e4b04af0bb4f9369856e0d` |
| `Docs` | CLEAN (R5 RESIDUE, S1 SUGGESTION) | `README.md:788-806`. Docstrings at `kept_grade.py:40-46,208-212,255-258,453-476`. PR body lines 86 and 178-181. `docs-workflow-steps-300da99b.txt`. `receipts/residue-scan.txt`. | R911-3 | `300da99beed5bb1c77e4b04af0bb4f9369856e0d` |

## Real limits

- **No measurement re-run.** The four re-grades re-grade round 1's measurement logs with the head's harness. The delta changes grading only, so this is the right evidence, but no new image was measured.
- **No source bank by me.** I ran only the `kept_grade` self-test and in-memory probes and mutants. I did not re-run `plat_ledger`, `ctrl_boundary`, the tree checks or the docs gates; I relied on the author's published receipts, verified by hash against `MANIFEST.json` and `INDEX.md`. No manager source bank exists at this head, and I claim none.
- **Evidence integrity rests on hashes.** The evidence commit `f2c9d425` carries no cryptographic signature. Integrity rests on the published `MANIFEST.json` and the `INDEX.md` sha256 prefixes (16 hex digits).
- **Hosted checks were still running.** When I read them (`receipts/hosted-checks-300da99b.txt`), 7 contexts had passed and one was skipped (Physical gPTP, nightly and manual). Another 44 were queued or in progress, among them the Verilator shards, the Yosys shards, the firmware jobs and `docs-gates`. These are not evidence for this report. The manager owns hosted and act acceptance.
- **Physical calibration was NOT RUN.** Field skips are not hardware proof.
- **Mutants are in-memory monkeypatches.** No source file was changed, and the tree is byte-identical to the head (`receipts/restore.txt`).

## Pending manager duties

- Validate the current-dev merge candidate (source base `aa30d77f`, live dev `e275d795`) with the builder and native banks at the merge turn, and link the receipts on the PR.
- Accept the exact-head hosted `verilator-suites` and `yosys-portability` contexts, and the act replica, at `300da99b`. They were in flight when this review read them.
- Carry R5's exact fix to the residue checklist, and S4 and S1 to the author as optional.
- Merge only with explicit maintainer authorization and the second independent positive review the bar requires.

R911-3 FINISHED
