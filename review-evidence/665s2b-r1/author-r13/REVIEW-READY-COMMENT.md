[A683p] REVIEW READY
Commit: `4f58214f457e963243a1fe6b86c6af161e97f26f` on `665-s2b-cycles`, local; 23 commits on round 12's `c954b8a9`, which contains `dev-soft-core` `a68536fa`. No rebase, no force, no merge; nothing pushed by this lane. The PR targets `dev-soft-core`.

Changed:
- **THE STEP** (`ctrl_loop.h`, `ctrl_loop.c`, `nvm_store.c/.h`). The saved-state store's centisecond consumer only owes a step. The loop reads the store's clock as a pass starts and, after the polls of a pass that took no event and no record, hands the step the clock's value at which the pass has spent its 2.0 ms share. The step is taken only while `NVM_STEP_US`, 1.0 ms, is left; otherwise it stays owed, once. THE SHARE names it. With the room gate alone, the last 8x8 SRP record reached 18.02 to 18.21 ms in four blank-check windows, so the step now waits for a pass that took no input; that first attempt is kept as a receipt.
- **SRP builds one interface a pass** (`srp_mbx.c`, `srp_bounds.h`); the other is built on the next pass, first. The interface reset clears `listener_present` (S1).
- **The harness** (`grade.py`, `save_window.py`, `sim_main.cpp`, `build.py`, `run.py`) holds every pass to the share, including passes that write nothing to the mailbox (each run's longest). It stages `backlog-adp`'s window in each flash phase of a save (blank check, program, verify) at eight tick phases. `grade.save_phase` refuses a window outside its phase. The planted store step `--mutation store-step-unbounded` is judged per window.
- **The boot simulation** builds the product's uncached flash window (`milan_soc.ctrl_uncached_flash`), refuses any other, and its self-test plants the call's removal.
- **Docs.** The three stale lines (SRP README share 2.0 ms, AECP README 20 ms bound, the store README's cadence) and the platform image's 58.5 tiles. `SPLIT_CONTROL_MEMORY.md` section 13 gains "A save in a composed window, and both links at once"; section 14 restates the 32x32 estimate and the gPTP additions from their units, each a mean or a bound. The boot, store and harness READMEs and `MAILBOX_SPLIT.md` are updated.

Validation, each on a clean clone of the commit, each rc 0:
- **docs.yml**: every `run:` step, 64 ran; 31 hosted-only steps not run, each with its reason.
- **The full sweep**, four native shards (`scripts/run_all_suites.sh --wait --shard k/4`): 65 of 65 suites, 2,613,655 checks, 0 failures. The first attempt stopped in every shard's preflight, `test_suite_cancellation.py`'s SIGINT case ("owned descendants remain"); the script alone passed, and the second attempt is the result given here. No gptp_shadow failure (#833).
- **Firmware**: `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --shard k/4`, all four PASS, 612 of 612 mutants in shard 1. `python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`: 445 tests, 116 plants. `python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP`: PASS.
- **Harness and boot**: `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 0 failures. `python3 -B tb/verilator/ctrl_split_boot/run.py` at both shapes: 25.515 and 64.885 ms to ready. Its `--self-test`: 3 of 3 plants caught, `flash-window-cached` among them.
- **Builder**: `python3 sw/builder/test_builder.py --require-rv32`: PASS, except the same two arms that need another host.
- **behave**: `cd tests && behave`: 508 scenarios passed.
- **`git diff --check`** against `a68536fa`: clean.
- **Images**: the harness images rebuilt at the commit equal the measured legs' (5 of 5).

Acceptance criteria:
1. **Met.** At `c954b8a9` the review's windows reproduce exactly (x-save 2.388 ms, y-save 2.716 ms). At this head they take 1.628 and 1.978 ms.
   - Each store step's cost, flash port and store, CPU cycles at 1x1 / 8x8: blank-check read-back 73,491 / 72,841, page program issue 95,373 / 95,386, verify read-back 76,234 / 76,737, busy poll 3,994 / 4,710.
   - The 24 save windows, at both points, in both arms, with and without the drafts: 0 of 99,289 passes over the share; a pass carrying a step is at most 1.02 ms at 8x8. The planted store step prints `CONTROL store-step-unbounded caught`: 5 windows over the share with every row in bound.
   - A save from the change to durable at 8x8: 4,697.1 ms before, 4,697.4 ms after; 2,018.4 ms at 1x1. #823's 0.5 s belongs to the append-only design and is not claimed.
2. **Met.** `y-links`: 1.761 / 1.817 ms, arm A / arm B. `x-links-same`: 1.543 / 1.560 ms. No pass over. The plant `joint-reset-builds-both` fails `Srp.JointLinkChangeBuildsOneInterfaceAPass` ("a pass builds one interface at most").
3. **Met.** As under Validation; the README's figures are the final head's runs exactly.
4. **Met.** The three lines are fixed. The gPTP additions now come from the table's own units: a row mean of 0.45 ms, a row bound of 8.0 ms and a pass bound of 1.6 ms. Against the 8x8/2if worst, 17.29 ms, the mean leaves 0.26 ms and the bound is 7.29 ms over.
5. **Met.** The save time in absolute terms is in the PR body and at `SPLIT_CONTROL_MEMORY.md:1304`; the harness README's arm B line is fixed; S1 is done.
- **Exit:** every measured row and every pass fits at 100 MHz, a save in progress included. The least margin is the 8x8 last SRP record's, 0.71 ms (17.29 ms against 18, arm B, in a save's window). The 32x32 estimate is restated, since its figures moved.

Open risks/questions:
- **Thin margins.** The heaviest 8x8 pass is 1.98 ms, carrying no step. The longest step is 0.954 ms of the 1.0 ms `NVM_STEP_US` allows.
- **A save's progress is not bounded.** A step waits for a pass that takes no input: at most 16.95 ms in the heaviest window, costing the save one tick. Nothing bounds the wait under input that never leaves a pass empty.
- **The 8x8 backlog last SRP record rose** from 15.88 / 15.96 to 16.56 / 16.46 ms. Each drain pass runs 68 more instructions, and about half of its 3,300 extra cycles are instruction-fetch waits.
- The PR body, HANDOFF and receipts are with the manager, who pushes.
