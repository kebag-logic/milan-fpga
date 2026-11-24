[A828] REVIEW READY
Commit: 300da99beed5bb1c77e4b04af0bb4f9369856e0d (branch pf-train-1123, tree 3b1a7562a4d6f954df7cd8f32c5c6e96f049d465; one commit on adc13dbdd1241b124c8877f1dda5318c1095e0df)

Changed (2 files, harness grader and its README only; `git diff --stat adc13dbd..300da99b -- sw hdl configs third_party protocol-processor` is empty):
- `tb/verilator/ctrl_service_budget/kept_grade.py`, R911-2-N1: `transmit_slices` no longer classifies the pass itself.
  - It reuses `whole_grade.held`'s classification. A THE TRANSMIT build slice over `CTRL_LOOP_SLICE_US` is `build-one` only where `whole_grade.held(log, shape)['over']` holds a pass of kind `build-one` (`BOUND_OWED_BUILDS`) at the same start (`kept_grade.py:213`).
  - So every condition `held` applies is inherited, not restated: the round idle (`round_idle`), not an aged step, a build entry inside, and at most one SRP frame.
  - Every other build slice over the slice is `build` and stays a failure. That covers a pass given whole to the build, a build of one whose AECP round did work, and an aged step's.
  - The docstring states this. It also states why matching only `held`'s over-cost passes loses nothing: at every shape `ctrl_loop.h` lists, `CTRL_LOOP_SLICE_US` >= `CTRL_LOOP_BUILD_ONE_PASS_US` (950/735, 1475/1475, 1300/1215, 1300/1215). So a build of one over the slice is over its cost too, and one that were not would fail closed.
- `kept_grade.py` self-test: 29 checks before, 32 after. The three new checks are in `selftest_transmit` (`kept_grade.py:474`), with the five existing THE TRANSMIT checks moved in beside them, output order unchanged:
  - N1: srp-bound's build of one over the slice (95,001 against 95,000), its AECP round at 1,001 cycles (one past `whole_grade.ROUND_IDLE_CYCLES`). There is no build-one pass line, and its slice line FAILS, never owed.
  - N1: the same pass as an aged step's (`step=1 aged=1`). Its slice line FAILS, never owed.
  - N2: a srp-bound build of one and a pass given whole, both 98,000 cycles. The build-one pass line is owed, and both slice lines FAIL (the equal-length clause, `kept_grade.py:264`).
  - The move into `selftest_transmit`, with `disposed` and `unowed` at module level, keeps `selftest_files` under the Python idiom gate's 100-line function limit (long function 9 <= 9).
- `README.md:790-806`: states the classification the code applies, the busy-round, aged-step and equal-length cases, the shape inequality, and 32 checks. The paragraph is re-wrapped within 120 columns (R911-2-S3).
- Design page: not changed. It states no check count, and its "only the build of one's slice is owed" stays true.

Validation (receipts in round4/receipts/, INDEX.md):
- `kept_grade.py --selftest`: PASS, 32 checks (`budget/kept-grade-selftest-r4.txt`).
- The new checks against round 3's rule:
  - The head's `selftest_transmit` run against adc13dbd's own `Disposition` (blob 6a81cad0): 2 of 7 fail, the busy-round and aged-step checks (`budget/new-checks-on-adc13dbd-r4.txt`).
  - The head file with `transmit_slices` replaced, text for text, by adc13dbd's: `--selftest` rc 1, the same 2 FAIL (`budget/kept-grade-source-mutants-r4.txt`, `r3-rule`).
- N2: the head file with `and cycles not in self.slices['build']` deleted: `--selftest` rc 1, and the equal-length check FAILS (`no-closed`, same receipt).
- Planted defects (scratch monkeypatches): 8 of 8 caught, and the unpatched run PASSES (`budget/kept-grade-planted-r4.txt`).
  - Round 3's six: the prefix-only owes (5 fail), whole slices owed too (5), no slice owed (3), every slice a build of one (5), strict `<` (1) and a 6 % margin (2).
  - Round 3's rule (2 fail).
  - The deleted clause (1 fail).
- R911-2's tools, unmodified (sha256 matching their MANIFEST):
  - `probe_owes_edges.py`: idle-one OWED, busy-one FAILS, aged-one FAILS, equal FAILS (`harness/probe_owes_edges-r4.txt`).
  - `mutants_r911_2.py`: drop-fail-closed is caught, 1 of 32 checks failing. idle-filtered, the reviewer's own implementation of the stricter reading, makes 0 of 32 fail, as an equivalent of the fix should (`harness/mutants_r911_2-r4.txt`).
  - R911-1's `probe_whole_slice.py`: both whole-pass slice lines are failures (`harness/probe_whole_slice-r4.txt`).
- Re-grade of the four formal legs, with no simulation (round 1's logs, sha256 in `budget/regrade-summary-r4.txt`; images unchanged):

  | Leg | kept_grade | Owed | run.py --regrade |
  |---|---|---|---|
  | 1x1/1if arm A | PASS, 0 findings | 4 | rc 0, 9 OWED, 0 STATED, 0 REFUSED |
  | 1x1/1if answering-ports | PASS, 0 findings | 4 | rc 0, 9 OWED, 0 STATED, 0 REFUSED |
  | 8x8/1if arm A | PASS, 0 findings | 5 | rc 0, 12 OWED, 0 STATED, 0 REFUSED |
  | 8x8/1if answering-ports | PASS, 0 findings | 6 | rc 0, 13 OWED, 0 STATED, 0 REFUSED |

  - The 171,645-cycle build-one pass and its THE TRANSMIT slice are still OWED #977 (`budget/run-regrade-8x8-1if-answering-ports-r4.txt:14,15,21`).
  - All 8 outputs are byte-identical to round 3's below the header (`budget/regrade-identity-r4.txt`, with sha256 prefixes).
- plat_ledger at 300da99b: PASS, 0 findings, the same POINT lines. All 24 (path, sha256) image lines are identical to adc13dbd's (`ledger/image-hashes-vs-adc13dbd.txt`).
- Harness tree checks and self-tests: rc 0 throughout. Load 0.512 at 1x1/1if. run.py --self-test reports 0 failures, 295 MUTANT caught and 0 escaped. test_ctrl_memory passes.
  - The full log is identical to round 3's apart from kept_grade's three new `[ok]` lines and its count, 29 to 32 (`gates/tree-log-diff-vs-adc13dbd.txt`).
- ctrl_boundary --require-rv32 --selftest: PASS, 0 findings, 117 boundary, 192 pin and 4 figure controls, 0 misbehaved, 313 `[ok]` and 0 FAIL.
  - The full log is identical to round 3's once temporary directory names are normalized (`gates/ctrl-boundary-log-diff-vs-adc13dbd.txt`).
- Docs workflow steps (5 jobs, fresh clone, em-dash base aa30d77f): 56 rc 0, 24 SKIP and 3 rc 1 (the RV32 SDK install-verify, an environment limit as before). Every step's name and rc is identical to round 3's.
  - docs_check: 0 findings over 223 pages.
  - em-dash: 0 over 772 added lines.
  - The SV, C/C++, Python (54/54) and Shell idiom gates PASS.

Acceptance criteria:
- R911-2-N1's required outcome is met. The slice line is owed only where `whole_grade.held` classes the pass `build-one`, and busy-round and aged-step passes stay failures. There are self-test checks for both, the docstring and README state the rule, and the verification is met: the probe gives busy-one and aged-one FAILS and idle-one OWED, round 3's rule fails the self-test, and the re-grades are unchanged.
- R911-2-N2's required outcome is met. The equal-length check makes both slice lines fail, and the `drop-fail-closed` mutant is caught.
- R911-2-S3 is taken.

Open risks/questions:
1. The classification now depends on `whole_grade.held`'s over-cost list. A build of one over the slice but within `CTRL_LOOP_BUILD_ONE_PASS_US` would fail rather than be owed. No listed shape allows that (slice >= build-one at all four), and the failure is the closed direction.
2. Unchanged from round 3, outside this scope: when a finding holds, `Disposition.owed` still carries `held`'s owed lines.
