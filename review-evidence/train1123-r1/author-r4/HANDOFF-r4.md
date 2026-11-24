# HANDOFF r4: [A828], the post-flip composition lane (pf-train-1123 -> dev-soft-core), round 4

**Status: REVIEW READY (05:25 CET, 2026-11-24). ETA: none, no work remains in this lane.**

- R911-2-N1 is fixed. `transmit_slices` reuses `whole_grade.held`'s own classification, matched by the pass's start, so a srp-bound build of one whose AECP round did work, or that is an aged step's, keeps its THE TRANSMIT slice line failing.
- R911-2-N2 is fixed. A self-test check pins the equal-length fail-closed clause.
- R911-2-S3 is taken.
- The four formal legs re-graded with no simulation: 0 findings, with 4, 4, 5 and 6 owed. The 171,645-cycle build of one is still owed. Every output is byte-identical to round 3's below its header.
- Every final-head gate passes. All 24 plat_ledger image hashes are identical to adc13dbd's.

- Final head **`300da99beed5bb1c77e4b04af0bb4f9369856e0d`** (tree `3b1a7562`), branch `pf-train-1123`. It is one commit on `adc13dbd` and is **committed locally, not pushed** (the manager pushes). The worktree is clean (porcelain 0).
- No issue or PR comment was posted. [REVIEW-READY.md](REVIEW-READY.md) holds the delta from `adc13dbd`, for the manager to post.
- Receipts are in [receipts/INDEX.md](receipts/INDEX.md): 34 files, each under 200 KB, with host paths replaced.

## The commit (adc13dbd..300da99b)

"Owe srp-bound's THE TRANSMIT slice line only where whole_grade.held itself classes its pass a build of one, a busy-round or aged-step pass staying a failure, and pin the equal-length fail-closed clause in the self-test". It is one line, with no trailer.

| File | Change |
|---|---|
| `kept_grade.py` | **N1, the rule.** `transmit_slices` (`:207-218`) takes the starts of `whole_grade.held(log, shape)['over']`'s `build-one` passes (`BOUND_OWED_BUILDS`). A THE TRANSMIT build slice over the slice is `build-one` only at one of those starts, and `build` (a failure) otherwise. The frame count is no longer restated here. **N1 and N2, the self-test**, 29 to 32 checks: a build of one with its AECP round at `ROUND_IDLE_CYCLES + 1` fails; the same as an aged step fails; a build of one and a whole pass of equal length both fail, with the build-one pass owed. The THE TRANSMIT checks now sit in `selftest_transmit` (`:474`), with `disposed` and `unowed` at module level and the output order unchanged, which keeps `selftest_files` under the idiom gate's 100 lines. The module docstring names the new cases |
| harness `README.md:790-806` | The classification the code applies, the busy, aged and equal-length cases, the shape inequality, and 32 checks. Re-wrapped within 120 columns (S3) |

`Disposition.owes` (`:255-266`) is unchanged; it keeps the clause at `:264`.

## Evidence

| Gate (head 300da99b) | Result | Receipt |
|---|---|---|
| kept_grade --selftest | **PASS**, 32 checks | `budget/kept-grade-selftest-r4.txt` |
| The new checks against round 3's rule | The head's `selftest_transmit` against **adc13dbd's own `Disposition`** (blob 6a81cad0): **2 of 7 fail**, busy and aged. The head file with `transmit_slices` spliced back to adc13dbd's text: `--selftest` **rc 1**, the same 2 FAIL | `budget/new-checks-on-adc13dbd-r4.txt`, `budget/kept-grade-source-mutants-r4.txt` |
| The clause deleted (N2) | The head file without `and cycles not in self.slices['build']`: `--selftest` **rc 1**, and the equal-length check FAILS | `budget/kept-grade-source-mutants-r4.txt` |
| Planted defects (scratch monkeypatches) | **8 of 8 caught**, and the unpatched run PASSES. Round 3's six are caught by 5, 5, 3, 5, 1 and 2 checks. Round 3's rule is caught by 2 and the deleted clause by 1 | `budget/kept-grade-planted-r4.txt` |
| R911-2's tools, unmodified (sha256 = MANIFEST) | `probe_owes_edges`: idle-one OWED, **busy-one FAILS, aged-one FAILS**, equal FAILS. `mutants_r911_2`: **drop-fail-closed caught (1 of 32)**. idle-filtered makes 0 of 32 fail, as an equivalent implementation of the fix should. R911-1's `probe_whole_slice`: both whole slices fail | `harness/*-r4.txt` |
| Re-grade of the 4 formal legs (no simulation; round 1's logs, with their sha256) | kept_grade PASS with 0 findings at every leg: 4 owed (1x1/1if arm A), 4 (1x1/1if answering-ports), 5 (8x8/1if arm A) and 6 (8x8/1if answering-ports). `run.py --regrade` gives rc 0, 0 STATED and 0 REFUSED at all four, with 9/9/12/13 OWED. 171,645 is OWED as a pass and as THE TRANSMIT's slice. **All 8 outputs are byte-identical to round 3's below the header** | `budget/kept-grade-*-r4.txt`, `budget/run-regrade-*-r4.txt`, `budget/regrade-identity-r4.txt`, `budget/regrade-summary-r4.txt` |
| Harness tree checks and self-tests (load_grade, flip_grade 1x1/8x8 and shape_costs `--check`; record_classes, flip_grade, kept_grade, load_grade and shape_costs `--selftest`; run.py --self-test; test_ctrl_memory) | **PASS**, every rc 0. Load 0.512. run.py reports 0 failures, 295 MUTANT caught and 0 escaped. Porcelain 0 after. **The full log diff against round 3 is only kept_grade's 3 new `[ok]` lines and 29 to 32** | `gates/tree-checks-300da99b.txt`, `gates/tree-log-diff-vs-adc13dbd.txt` |
| ctrl_boundary --require-rv32 --selftest | **PASS**: 0 findings, 117 boundary, 192 pin and 4 figure controls, 0 misbehaved. 313 `[ok]` and 0 FAIL, with 16 "stopped at its link". **The normalized full log is identical to round 3's** | `gates/ctrl-boundary-300da99b.txt`, `gates/ctrl-boundary-log-diff-vs-adc13dbd.txt` |
| plat_ledger | **PASS**, 0 findings, with the same POINT lines. **24 of 24 (path, sha256) lines identical to adc13dbd's.** No image input changed | `ledger/image-hashes-vs-adc13dbd.txt`, `ledger/plat-ledger-300da99b.txt` |
| Docs workflow steps (5 jobs, fresh clone, em-dash base aa30d77f) | 56 steps rc 0, 24 SKIP and 3 rc 1 (the RV32 SDK install-verify, an environment limit). **Every step's name and rc is identical to round 3's.** docs_check 0 findings over 223 pages, em-dash 0 over 772 added lines, and the SV, C/C++, Python (54/54) and Shell gates PASS | `docs/docs-workflow-steps-300da99b.txt` |
| Firmware gate, routes | **Not re-run.** No firmware, RTL or configuration input changed | rounds 1 and 2 |

## The gate that caught the first commit

- The first round-4 commit, `6ab79cf6` (never pushed), put the new checks inline in `selftest_files`.
- The docs run on it failed the **Python idiom gate: long function 10 > ratchet 9**. Every other step matched round 3.
- I amended the commit, moving the THE TRANSMIT checks into `selftest_transmit` with the self-test output unchanged, and re-ran every receipt and gate at `300da99b`.
- The `6ab79cf6` gate receipts are kept, labelled, in `receipts/superseded-6ab79cf6/`. None of them is evidence for the final head.

## Open risks and observations

1. The slice line's pass is now found through `whole_grade.held`'s over-cost list. A build of one over the slice but within its stated cost would fail, not be owed. That is the closed direction, and no shape `ctrl_loop.h` lists allows it: slice >= build-one at all four (950/735, 1475/1475, 1300/1215, 1300/1215).
2. This is unchanged from rounds 2 and 3, and outside this scope. When a finding holds, `Disposition.owed` still carries `held`'s owed lines, so run.py prints them as OWED beside the failing findings. The run still fails on the findings.

## Notes

- **CPU.** plat_ledger ran as unit `milan-train1123-a828-ledger-r4` on CPUs 56-63, booked through `cpu_ranges.py`. The tree checks, ctrl_boundary and docs ran as units `-tree-r4`, `-cb-r4` and `-docs-r4` on the session pool 64-95. The self-tests, mutants, probes and re-grades are pure-Python log reads. No Vivado was used.
- **Scratch.** Everything is under `$VALIDATION_STORAGE/train1123-a828`:
  - `r4/`: `bin/kept_mutants_r4.py`, `splice_r4.py`, `new_checks_on_adc13dbd.py`, `regrade_r4.sh`, adc13dbd's `kept_grade.py` copy, the re-grade outputs and the spliced mutants;
  - `ledger/300da99b/`, `docs-300da99b/`;
  - the clones `tc`, `cb` and `lg`, now at 300da99b.
  - The `6ab79cf6` unit logs are kept as `units/*-r4a-6ab79cf6.*`.
  - The measurement clone `clones/cpu` was restored to c2b2ba1a with porcelain 0.
- No bench, board or test-machine access was used. No push, and no issue or PR comment.

REVIEW READY 300da99beed5bb1c77e4b04af0bb4f9369856e0d
