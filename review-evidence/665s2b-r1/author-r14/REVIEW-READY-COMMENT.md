[A683q] REVIEW READY
Commit: `a3f23bbabdd9800177224432361fcd41b53bf882` on `665-s2b-cycles`, local; 11 commits on round 13's `4f58214f`, which contains `dev-soft-core` `a68536fa`. No rebase, no force, no merge; nothing pushed by this lane. The PR targets `dev-soft-core`.

Changed:
- **THE STEP's age limit** (`ctrl_loop.h`, `ctrl_loop.c`). Once more than `CTRL_LOOP_STEP_AGE` centiseconds (two) have been dispatched since the store's step last ran or owed nothing, the next pass is the step's alone. It runs before any input, with the deadline read as the pass starts, and returns one, so the input it held off is taken by the next pass. `Loop.L13AnAgedStepIsAPassOfItsOwn` covers it, with ten new planted defects. `ctrl_plat` is ledgered at 19,968 B.
- **A save's worst case** (`nvm_store.h`, `save_window.bound_ms`): 1,000 ms (DR2a) + S × 3 ticks + 10 ms from the change. A SET_NAME of the entity marks both its names, so S = 370 and the bound is 12,110 ms at 8x8/2if, S = 102 and 4,070 ms at 1x1, on a flash with no busy time.
- **The harness** has two new save groups, `save-held` and `save-starved`. `save-held` holds every receive channel at its contract refill rate with its bursts through a whole save. `save-starved` adds a grandmaster change as every pass starts, so no pass is empty. Every save is timed to durable against its bound, and a late save fails the run. Every pass that carries a step is printed, idle or work. `save_phase` ends the verify phase at the read-backs. The native control `store-step-ageless` removes the age limit.
- **SRP one build a pass either way** (`srp_mbx.c`): the poll reads whether the interface with the turn builds before it visits either. `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal` covers it, with the plant `build-turn-read-after-its-visit`.
- **Found on the way and fixed:**
  - A record is marked by its id without walking the records (`nvm_rec_id_of`, `nvm_store_changed_id`; AECP marks so). AECP's mark of a SET_NAME's two names walked them twice, 22,088 cycles, and put one 8x8 pass at 2.135 ms beside the held load's first bursts.
  - The `srp-poll-extra-read` plant is re-anchored at the link reads the poll now makes before its visits.
- **Residue:** R712-3 RESIDUE-1 and R711-3's RESIDUE (section 14's S slope) and R712-3 RESIDUE-2 (the read-back step's cost), all with their exact texts. S1 (`step_room` at exactly `NVM_STEP_US`) and the unrounded 1.116 ms are taken.
- **Docs:** `SPLIT_CONTROL_MEMORY.md` section 13 gains "A save's worst case, and one build a pass either way", and `:1435` is replaced. Section 14 is restated. The loop, store, SRP, harness and boot READMEs and `MAILBOX_SPLIT.md` are updated.

Validation, each on a clean clone of the commit, each rc 0:
- Every `run:` step of `.github/workflows/docs.yml`, each job on its own fresh clone: 64 steps ran, 0 bad. The 31 hosted-only steps were not run, each with its reason recorded.
- `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0 to 3, `MAKEFLAGS="-j4 --no-print-directory"`: 65 of 65 suites, 2,613,655 checks, 0 failures; each shard's counts equal round 13's. The first attempt stopped in every shard's preflight, in `test_suite_cancellation.py` (#833), and was re-run once; both results are kept. In the re-run, shards 0, 1 and 3 passed. Shard 2 was killed by the out-of-memory killer in `capture_coherence` on 8 CPUs, and again when run alone on 16, because that suite's mutant driver builds one datapath per CPU. Run alone on four CPUs, with the same command at the same head, it passed.
- `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard k/4`, k = 0 to 3: `test_ctrl_firmware: PASS` in each. Shard 1 caught 622 of 622 mutants, and every AECP and SRP campaign plant was caught in shards 2 and 3.
- `python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`: 455 tests, all 121 planted defects reddened.
- `python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8`: PASS (38 files).
- `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 0 failures, 124 of 124 grader mutants caught.
- `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <b> --record-budget-findings --record-share-findings --jobs 8`: 45 groups, 0 refusals, 0 of 66,819 passes over the share. The three saves (alone / held / starved) took 2,019.2 / 2,019.0 / 4,049.0 ms, against a stated worst case of 4,070.
- The same at `--point 8x8`: 44 groups, 0 refusals, 0 of 88,204 passes over. The saves took 4,697.4 / 4,696.9 / 12,087.0 ms against 12,110, and the longest step-carrying pass was 1.292 ms. Each point's table is byte for byte its measured leg's.
- `python3 sw/builder/test_builder.py --require-rv32`: "ALL GATES PASS EXCEPT 2 NOT RUN"; the same two arms that need another host as before.
- `cd tests && behave --no-capture -f plain`: 508 scenarios passed, 0 failed.
- `git diff --check a68536fa4cf8ce65c513874722de2e3ba83c2d00 HEAD`: clean.
- Also rc 0:
  - the boot simulation at both shapes (25.477 and 64.584 ms to ready), its native controls, and its self-test (3 of 3 plants caught);
  - the Python and C++ idiom gates;
  - `gen_mailbox.py --check --crosscheck` and `--selftest`;
  - the publication census;
  - `lint_rtl.py --check` (89, within its ratchet);
  - `test_soc_options.py` and `test_ctrl_memory.py`;
  - both halves of `ctrl_boundary.py`.
- The six measured images, rebuilt at the head through the harness's own build, are the legs' (6 of 6).

Acceptance criteria:
1. **Met.** N = 2, chosen by measurement. In every window of every leg, at most two centiseconds were posted between two step-carrying passes (one at 1x1), so no aged step lands among a window's records. At N = 1 one would at 8x8. Every row and every pass is within its bound. The least margin is 0.77 ms, the 8x8 last SRP record at 17.23 ms, arm A, in a save's window.
2. **Met.** At 8x8/2if, `save-starved` was durable 12,087.0 to 12,088.0 ms after its change, against 12,110 ms, in both arms with and without the drafts. At 1x1 it took 4,047.9 to 4,049.0 ms against 4,070 ms. `save-held` was 4,696.7 to 4,731.1 ms at 8x8. Neither group had a pass over the share, and each channel's longest record was within its bound. `CONTROL store-step-ageless caught`: without the age limit the save was not durable 12,618.4 ms after its change.
3. **Met.** The mirrored test and its plant are caught. The review's link groups at 8x8: `y-links` 1.741 / 1.809 ms, `x-links-same` 1.531 / 1.556 ms (arm A / arm B).
4. **Met.** The longest step-carrying pass over every group was 1.218 / 1.231 ms at 1x1 and 1.292 / 1.266 ms at 8x8 (arm A / arm B), and 1.182 / 1.177 and 1.246 / 1.249 ms with the drafts. The longest step's own time was 0.966 ms.
5. **Met.** The self-test's phase check holds the case and catches its mutant. Every leg's 24 windows were graded with 0 refusals.
6. **Met.** As under Changed.
- **Exit:** every measured row and every pass fits at 100 MHz with the share not amended, so there is no STOP.

Open risks/questions:
- **N = 2 has a margin of about 3.6 ms.** The heaviest window holds a step off for at most 26.4 ms; a third centisecond in that gap would put an aged step among its records. N = 3 would add 3.7 s to the worst case.
- **The step's room is 0.034 ms:** the longest step is 0.966 ms of the 1.0 ms `NVM_STEP_US`. The figure is reported but no gate holds it.
- **The worst case is this image's.** 12.11 s at 8x8/2if on a flash with no busy time; a part's erase time adds to it. #823's 0.5 s is the append-only design's and is not met here.
- **The walk-free mark is a store change beyond the items.** Item 1 needs every pass within its bound; it is disclosed in the PR body.
- The PR body, HANDOFF and receipts are with the manager, who pushes.
