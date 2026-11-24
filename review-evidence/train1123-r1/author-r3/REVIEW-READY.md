[A828] REVIEW READY
Commit: adc13dbdd1241b124c8877f1dda5318c1095e0df (branch pf-train-1123; the delta from 43076d0f8c87b5118f6f4317d000a7eebdefc967, one commit)

Changed (5 files, no RTL, firmware, configuration or owner-bound change; `git diff --stat 43076d0f..adc13dbd -- sw hdl configs third_party protocol-processor` is empty):
- `tb/verilator/ctrl_service_budget/kept_grade.py`, R911-1-F1: `Disposition.owes` owes srp-bound's STATED line "a tier-2 slice of THE TRANSMIT's build of N" only where srp-bound's own log has a build slice of those N cycles over the slice whose pass makes at most one SRP frame (a build of one, as `whole_grade.held` classifies it) and no slice of those cycles given whole to the build. Every other srp-bound THE TRANSMIT slice over `CTRL_LOOP_SLICE_US` stays a failure. srp-kept's stays a failure as before. This follows #969's ruling of 2026-11-23, item 2: the build-of-one pass and the pass over THE SHARE, nothing else. New helpers: `transmit_slices` (from `slice_grade.held` and the SRP frames in each pass) and `stated_cycles`. If the cycles are ambiguous (a build of one and a whole pass of the same length), the line stays a failure.
- `kept_grade.py` self-test: 24 checks before, 29 after.
  - srp-bound's build of one over the slice: run.py's build-one line and its THE TRANSMIT slice line are both owed, and nothing fails.
  - **A srp-bound pass given whole to THE TRANSMIT's build, over the slice and within `CTRL_LOOP_BUILD_PASS_US` (98,000 against 95,000 and 101,000 at 1x1/1if), FAILS.**
  - Both kinds of pass in one log: the build of one is owed, and the whole pass fails.
  - srp-kept's whole pass over the slice fails.
  - R912-1-S1: kept exactly bound + 5 % (105,000 against 100,000) holds, and 105,001 breaks. This runs through `held` and `kept_within`.
  - The new checks use run.py's own STATED lines (`run.stated_misses`), not restated copies.
- R911-1-R2: `AMENDED = "#969's ruling of 2026-11-23"`, so no issue-comment ID remains in the source. The link stays in the harness README and the PR.
- R911-1-R1: `poll_grade.py:135-137` now reads "325 us by the rule (record_classes.rule), raised with every owner bound still held (#665's ruling of 2026-11-23 on the #958 sync's STOP: a further statement over is raised by the same rule while every owner bound holds)". This is a comment only. `EIGHT_ONE` is unchanged.
- R911-1-S1 (taken): `kept_grade.py`, the harness README and `SPLIT_CONTROL_MEMORY.md`'s train section now cite `record_classes.rule` and the 2026-11-23 rulings in place of "#665's ruling item 4". Older, correct citations of item 4 were left alone (the notice-path restatement).
- R911-1-S2 (taken): `kept_window.py`'s docstring now says that each pass srp-bound gives whole to THE TRANSMIT's build is held within its stated cost, and that srp-bound's build of one is owed as a pass and as THE TRANSMIT's slice.
- The harness README and the design page record the narrowed disposition and the 29 checks.

Validation (receipts in round3/receipts/, INDEX.md):
- `kept_grade.py --selftest`: PASS, 29 checks (`budget/kept-grade-selftest-r3.txt`).
- Planted defects (scratch monkeypatches, nothing committed): 6 of 6 caught, and the unpatched run PASSES (`budget/kept-grade-planted-r3.txt`).
  - Round 2's prefix-only `owes` is caught by the new whole-pass checks.
  - Owing whole slices too, owing no slice, and classing every slice as a build of one are each caught.
  - A strict `<` in `kept_within` is caught only by the new integral control.
  - A 6 % margin is caught.
- R911-1's `tools/probe_whole_slice.py`, unmodified: "RESULT srp-bound: the whole build pass's slice line is a failure" (OWED: [], still failing: the 98,000-cycle line). srp-kept is a failure as before (`harness/probe-whole-build-slice-r3.txt`).
- Re-grade of the four formal legs, with no simulation (round 1's logs, sha256 in each receipt; images unchanged):

  | Leg | kept_grade | Owed |
  |---|---|---|
  | 1x1/1if arm A | PASS, 0 findings | 4 owed |
  | 1x1/1if answering-ports | PASS, 0 findings | 4 owed |
  | 8x8/1if arm A | PASS, 0 findings | 5 owed |
  | 8x8/1if answering-ports | PASS, 0 findings | 6 owed |

  - `run.py --regrade` of srp-kept and srp-bound exits rc 0 at all four legs, with 0 refusals, 0 budget misses and 0 STATED failures.
  - At 8x8/1if answering-ports, "srp-bound: a tier-2 slice of THE TRANSMIT's build of 171,645 CPU cycles, over the stated slice 147,500" is still OWED #977, and so is the 171,645-cycle build-one pass.
  - Every kept_grade and run.py output is byte-identical to round 2's below its header (`budget/kept-grade-*-r3.txt`, `budget/run-regrade-*-r3.txt`, `budget/regrade-summary-r3.txt`).
- plat_ledger at adc13dbd: PASS, 0 findings, with the same POINT lines. **All 24 (path, sha256) image lines are identical to 43076d0f's** (`ledger/image-hashes-vs-43076d0f.txt`, `ledger/plat-ledger-adc13dbd.txt`).
- Harness tree checks and self-tests, ctrl_boundary --require-rv32 --selftest, docs workflow steps: see the gate table in HANDOFF-r3.md (`gates/`, `docs/`).

Acceptance criteria:
- R911-1-F1's required outcome is met: only the build of one's slice is owed, with the self-test check and the probe as evidence.
- Its verification is met: the self-test passes, the probe reports a failure, and the four re-grades give 0 findings, 4/4/5/6 owed, with 171,645 owed.
- R1 and R2 are applied with the exact fixes. S1 and S2 are taken. R912-1-S1 is taken.

Open risks/questions:
1. Matching is by the STATED line's cycle figure against srp-bound's own log, because run.py's line does not carry the pass's start. A build of one and a whole pass of identical length in one log fail closed: the line stays a failure.
2. An observation, not changed (outside F1's scope): `Disposition.owed` also carries `held`'s owed lines when a finding holds, so run.py prints them as OWED beside the failing findings. The run still fails on the findings. Round 2's behaviour is unchanged.
