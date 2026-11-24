# HANDOFF r3: [A828], the post-flip composition lane (pf-train-1123 -> dev-soft-core), round 3

**Status: REVIEW READY (03:06 CET, 2026-11-24). No ETA: no work remains in this lane.**

- R911-1-F1 is fixed. `kept_grade` now owes srp-bound's THE TRANSMIT slice line only where its pass is a build of one.
- R1 and R2 are applied with the exact fixes. R911-1-S1, R911-1-S2 and R912-1-S1 are taken.
- The four formal legs were re-graded with no simulation: 0 findings, with 4, 4, 5 and 6 owed. The 171,645-cycle build of one is still owed.
- Every final-head gate passes. All 24 plat_ledger image hashes are identical to 43076d0f's.

- Final head **`adc13dbdd1241b124c8877f1dda5318c1095e0df`**, branch `pf-train-1123`. It is one commit on `43076d0f` and is **committed locally, not pushed** (the manager pushes). The worktree is clean.
- No issue or PR comment was posted. [REVIEW-READY.md](REVIEW-READY.md) holds the delta from `43076d0f`, for the manager to post.
- Receipts are in [receipts/INDEX.md](receipts/INDEX.md): 18 files, each under 200 KB, with host paths replaced.

## The commit (43076d0f..adc13dbd)

`adc13dbd` "Owe srp-bound's THE TRANSMIT slice line only where its pass is a build of one, a pass given whole to the build staying a failure over the slice, and hold kept exactly bound + 5 % inclusive in the self-test". It changes five files:

| File | Change |
|---|---|
| `kept_grade.py` | **F1.** `Disposition.owes` owes `srp-bound: a tier-2 slice of THE TRANSMIT's build of N` only if srp-bound's log has a build slice of N cycles over the slice that makes at most one SRP frame (`transmit_slices`: `slice_grade.held`'s build slices, classed by `whole_grade.held`'s frame rule), and no slice of N given whole to the build. If the cycles are ambiguous, the line fails. Every other STATED prefix is unchanged. **R2:** `AMENDED = "#969's ruling of 2026-11-23"`. **S1:** "#665's ruling item 4" is replaced by `record_classes.rule`. The self-test goes from 24 checks to 29 (below) |
| `poll_grade.py:135-137` | **R1**, verbatim: "...325 us by the rule (record_classes.rule), raised with every owner bound still held (#665's ruling of 2026-11-23 on the #958 sync's STOP: a further statement over is raised by the same rule while every owner bound holds)". This is a comment only |
| `kept_window.py` docstring | **S2:** srp-bound's whole builds are held within their stated cost, and its build of one is owed as a pass and as THE TRANSMIT's slice |
| harness `README.md` | The narrowed disposition, the S1 citation, and 29 checks with what they hold. The ruling's link is kept here |
| `SPLIT_CONTROL_MEMORY.md` | Line 3310 (S1): `record_classes.rule`, by #665's ruling of 2026-11-23. Line 3312: only the build of one's slice is owed, a whole pass over the slice stays a failure, and none arises at either point |

The five new self-test checks:
- srp-bound's build of one over the slice (95,001 against 95,000): run.py's build-one and slice lines are both owed, and nothing fails.
- **A srp-bound pass given whole to THE TRANSMIT's build, over the slice and within `CTRL_LOOP_BUILD_PASS_US` (98,000 against 95,000 and 101,000): its slice line FAILS.**
- Both kinds of pass in one log: the build of one is owed, and the whole pass fails.
- srp-kept's whole pass over the slice fails.
- R912-1-S1: 105,000 against 100,000 holds and 105,001 breaks.

The Disposition checks run on run.py's own `stated_misses` lines.

## Evidence

| Gate (head adc13dbd) | Result | Receipt |
|---|---|---|
| kept_grade --selftest | **PASS**, 29 checks | `budget/kept-grade-selftest-r3.txt` |
| Planted defects (scratch, not committed) | **6 of 6 caught**, and the unpatched run PASSES. Round 2's prefix-only `owes` is caught by 2 checks. Owing whole slices too, owing no slice, and classing every slice as a build of one are each caught. `<` in place of `<=` is caught only by the new integral control | `budget/kept-grade-planted-r3.txt` |
| R911-1's `probe_whole_slice.py`, unmodified | **"RESULT srp-bound: the whole build pass's slice line is a failure"** (OWED []). srp-kept is a failure as before | `harness/probe-whole-build-slice-r3.txt` |
| Re-grade of the 4 formal legs (no simulation; round 1's logs, with their sha256) | kept_grade PASS with 0 findings at every leg: 4 owed at 1x1/1if arm A, 4 at 1x1/1if answering-ports, 5 at 8x8/1if arm A and 6 at 8x8/1if answering-ports. `run.py --regrade` gives rc 0, 0 refusals, 0 budget misses and 0 STATED at all four. The 171,645 build-one pass and its THE TRANSMIT slice are OWED #977. **Every output is byte-identical to round 2's below its header** | `budget/kept-grade-*-r3.txt`, `budget/run-regrade-*-r3.txt`, `budget/regrade-summary-r3.txt`, `budget/regrade_r3.sh.txt` |
| Harness tree checks: load_grade, flip_grade (1x1/1if, 8x8/1if) and shape_costs `--check`; record_classes, flip_grade, kept_grade, load_grade and shape_costs `--selftest`; run.py --self-test; test_ctrl_memory | **PASS**, every rc 0. Load 0.512 at 1x1/1if. run.py --self-test reports 0 failures, 295 MUTANT caught and 0 escaped, as in round 2. test_ctrl_memory 0 failures. Porcelain 0 before and after | `gates/tree-checks-adc13dbd.txt` |
| ctrl_boundary --require-rv32 --selftest | **PASS**: 0 findings, 117 boundary, 192 pin and 4 figure controls, 0 misbehaved. 313 `[ok]` and 0 FAIL, the same as round 2. The 16 "stopped at its link" builder lines match round 2's | `gates/ctrl-boundary-adc13dbd.txt` |
| plat_ledger | **PASS**, 0 findings, with the same POINT lines. **24 of 24 (path, sha256) lines identical to 43076d0f's**, by diff. `git diff --stat 43076d0f..adc13dbd -- sw hdl configs third_party protocol-processor` is empty | `ledger/image-hashes-vs-43076d0f.txt`, `ledger/plat-ledger-adc13dbd.txt` |
| Docs workflow steps (5 jobs, fresh clone, em-dash base aa30d77f) | 56 steps rc 0, 24 SKIP and 3 rc 1. The rc 1 steps are the RV32 SDK install-verify, an environment limit as in round 2. **Every step's name and rc is identical to round 2's.** docs_check 0 findings over 223 pages, em-dash 0 over 766 added lines, and the SV, C/C++, Python and Shell idiom gates PASS | `docs/docs-workflow-steps-adc13dbd.txt` |
| Firmware gate, routes | **Not re-run.** No firmware, RTL or configuration input changed (the diff above). Earlier passes: the firmware gate at f5a1585e, the routes at c2b2ba1a | round 1/2 |

## Residues

| Residue | Disposition |
|---|---|
| R911-1-R1 | Applied, with the exact text |
| R911-1-R2 | Applied: `AMENDED = "#969's ruling of 2026-11-23"`, and the link stays in the README |
| R911-1-R3, R4 (PR body) | Already applied by the manager, so not touched here |
| R911-1-S1 | Taken in kept_grade.py, poll_grade.py, the README and SPLIT_CONTROL_MEMORY.md:3310. The PR body's own "item 4" reference is the manager's to edit, if wanted |
| R911-1-S2 | Taken |
| R912-1-S1 (T1) | Taken. The control fails under a strict `<` (planted) |

## Open risks and observations

1. The STATED slice line carries no pass start, so matching uses the line's cycle figure against srp-bound's own log. It fails closed when a build of one and a whole pass have equal lengths.
2. An observation, outside F1's scope and not changed: when a finding holds, `Disposition.owed` still carries `held`'s owed lines, so `run.py` prints them as OWED beside the failing findings. The run still fails on the findings. This behaviour is unchanged since round 2. It is for the manager to decide whether it needs an Issue.

## Notes

- **CPU.** plat_ledger ran as unit `milan-train1123-a828-ledger-r3` on CPUs 8-15, booked through `cpu_ranges.py`; only one 8-CPU range was free. The tree checks, ctrl_boundary and docs ran as units `-tree-r3`, `-cb-r3` and `-docs-r3` on the session pool 64-95. The re-grades and self-tests are pure-Python log reads. No Vivado was used.
- **Scratch.** Everything is under `$VALIDATION_STORAGE/train1123-a828`:
  - `r3/`: the re-grade copies and outputs, `bin/kept_mutants_r3.py` and `bin/regrade_r3.sh`;
  - `ledger/adc13dbd/` and `docs-adc13dbd/`;
  - the clones `tc`, `cb` and `lg`, now at adc13dbd.
  The measurement clone `clones/cpu` was restored to c2b2ba1a with porcelain 0.
- No bench, board or test-machine access was used. No push, and no issue or PR comment.

REVIEW READY adc13dbdd1241b124c8877f1dda5318c1095e0df
