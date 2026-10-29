# [A697d] #665 S3 round 3: R733-1 and R734-1 on PR #811, handoff

STATUS: **REVIEW READY** at `ac105b158bb740a65e0154305377fd4a7d0f6f87`, posted on #665 as issuecomment-6511365175 (text in `REVIEW-READY-COMMENT.md`); the PR body for base `dev-soft-core` is `PR-BODY.md`. Every gate the change touches, and the firmware self-test, passed at that head, rc 0 (table below); no STOP condition holds.

- Lane: S3 of the Mark II split (#665). Round 3 under [A10] issuecomment-6508869822, answering R733-1
  (issuecomment-6508864388, two MINOR) and R734-1 (issuecomment-6508854695, one MAJOR, residue). Earlier rounds:
  `../665s3-a697/`, `../665s3-a697b/`, `../665s3-a697c/`.
- Branch `665-s3-platform`, start `99de3a02` (pushed, PR #811). Six commits on top, no rebase, nothing pushed.
  Base `origin/dev-soft-core` `f4c9ad4f`, an ancestor of the head; origin verified
  `https://github.com/kebag-logic/milan-fpga.git`. No submodule pin moved and no git command ran inside a submodule.
  No RTL, `milan_soc.py`, `.github/` or CI generator changed, so the full sweep and Vivado are not run.
- No issue or PR comment was edited; TAKEN was already posted for the lane.

## The assignment, item by item

| Item | Finding | Done |
|---|---|---|
| 1 | R734-F1 (MAJOR): the split boot driver accepts a failed native simulation | The run saves the model's exit status beside its log (`sim.status`); the grade's new NATIVE check fails on a nonzero or missing saved status and on a tally that failed, is missing or measured nothing, read with the sweep's own reader; the regrade reads the same saved status. Six native controls (a passing control, a nonzero exit, a failed tally, a missing tally, both, a status gone before the regrade) run with no build, under `--native-controls` and first in `--self-test`; each graded as required on its run and its regrade. R734's own probe now ends `DEFECT REJECTED`, rc 0. Both positive points and both plants re-run. |
| 2 | R733-F1 (MINOR): `is()` reads past the command literal on a NUL | `is()` stops at the command's terminator. K3 sends `milan_status\0XYZ\r` and `milan_gettime\0\r`. The `plat` arm builds and runs `test_plat` under AddressSanitizer (`abort_on_error=1`, so the harness names the test). The shipped mutant `plat-command-read-past-its-end` (the fix reverted) is caught by K3, `crashed on signal 6`, with ASan's `global-buffer-overflow ... in is`; the same mutant escapes with the sanitizer withheld (0 checks fail), so the sanitizer is what kills it. R733's probe is clean on the fix, and reports the overflow on the revert. |
| 3 | R733-F2 (MINOR): the boot tests miss the saved state after the mailbox and an unbound store service | B1 now stamps each flash media access with the mailbox's access count and requires every one before the mailbox's first access. B10 (new): a controller's BIND_RX_COMMAND arrives through the mailbox model after READY, and the store's service on the loop's centisecond tick commits it to the flash. R733's two plants are shipped mutants: `plat-saved-state-after-mailbox-open` (caught by B1, the boot-order check) and `plat-store-service-unbound` (caught by B10, the write-back check). |
| 4 | R734-R1 (residue): lane labels and comment IDs in new comments | Every line of `comment-residue.txt` cleaned, with R734's exact replacements, plus `ctrl_memory.py:210` (R734's exact fix). Executable strings (the boundary gate's classification texts in `ctrl_configs.py`, the ledger's reason strings in `ctrl_memory.py`) are left, as R734 scoped them out; `F0-F5` and `F1` are kept as functional names, as R734 classified them. |
| R-2 (both reviewers' residue) | `tb/verilator/ctrl_split_boot/README.md` "longer than any span here" | Deleted, as both reviewers' exact fix (the README changes this round anyway). |
| R-3 (R733 residue) | the PR body's timing figures carry no clock | Every timing figure in `PR-BODY.md` and in the boot README's results is labelled with the split CPU's 50 MHz and its bus's 100 MHz. |
| R-5 (R733 residue) | the `c787a3ce` row | `PR-BODY.md` says which six files it re-recorded that this PR does not change. |

R733's R-4 (`ctrl_plat.c:64-65` wording) and suggestions S-1 to S-3 are not changed (not in the round's items).

## Commits

| Commit | Subject |
|---|---|
| `18fa9a45` | Keep the new comments to behaviour, reason and #665's decision IDs, without lane labels, comment IDs or ruling numbers (#665) |
| `b8628704` | Stop the console's command compare at the command's terminator, so a line holding a NUL reads nothing past it, its test run under AddressSanitizer with the fix's revert planted (#665) |
| `07eba0fc` | Check in the platform's boot that the saved state is read before the mailbox opens and that a bind after ready reaches the flash through the loop's service, each with its planted defect (#665) |
| `6987b8d8` | Fail the split boot on the native model's own verdict, its exit status saved beside its log for the regrade, with six native controls of valid observations (#665) |
| `7b308437` | Spin the console plant only before milan_status's response, so its run ends inside the limit, and require each plant to be found in a run the model completes (#665) |
| `ac105b15` | Record the platform's figures at this head: its rom 8 B larger at every point from the console's compare, the boot and its spans at the 50 MHz CPU, and the console's coverage (#665) |

## Changes (file:line, reason)

### Item 2, the console (`b8628704`)

| Where | What | Why |
|---|---|---|
| `sw/firmware/ctrl/plat/ctrl_plat_console.c:129-140` | `is()`'s loop also stops at `command[n] == '\0'`; comment says why (a UART yields 0x00 on a break). | R733-F1: with a NUL where a name ends, the old loop compared `command[n]` past the literal (C11 6.5.6). Now the loop ends at the terminator and the return short-circuits on `n != len`. |
| `sw/firmware/ctrl/test/test_plat.cpp:160-164`, `:17-19` | K3 sends `milan_status\0XYZ\r` (R733's probe line) and `milan_gettime\0\r` (the NUL at the name's end, where the old return read `command[13]`); both answered `?`, refusals 5. | The probe, permanent. |
| `sw/firmware/ctrl/test/plat_arms.py:39-50`, `:6-7` | `arm_plat` builds the CSR window, the console and `test_plat` with `address_sanitizer=True` (a `dataclasses.replace` of the tree's build, so a coverage build keeps coverage) and runs it with `ASAN_OPTIONS=abort_on_error=1`. `test_plat_mmio` stays unsanitized. | A report aborts the run, and the harness's SIGABRT handler prints `[FAIL] <test>: crashed on signal 6`, as `nvm_bench` runs its prefix binary. The MMIO test's planted neighbour accesses stay inside its host array and must be caught by their words, which a sanitizer abort would replace. |
| `sw/firmware/ctrl/test/plat_mutants.py:92-97` | `plat-command-read-past-its-end`: the fix reverted; `plat`, `Plat.K3LinesEndOnceAndOthersAreRefused`, `crashed on signal 6`. | The planted defect. |
| `sw/firmware/ctrl/plat/README.md:72` | The console's compare stops at the terminator. | Docs. |

### Item 3, the boot tests (`07eba0fc`)

| Where | What | Why |
|---|---|---|
| `sw/firmware/ctrl/test/test_plat_boot.cpp:80-97`, `:140`, `:146`, `:155-157` | A flash port over the model whose read, program and erase record `mailbox.size()` (`media`); the fixture boots with it. | So a test reads the saved state's place among the mailbox's accesses, as the CSR and UART accesses already are. |
| `sw/firmware/ctrl/test/test_plat_boot.cpp:209-214` | B1: the boot read the flash, every flash access came before the mailbox's first access, and a blank flash ends BLANK. | R733-F2's first plant. `compose()` makes no mailbox access, so the bound is 0 at the shipping shape and at two interfaces (both arms pass). |
| `sw/firmware/ctrl/test/test_plat_boot.cpp:378-402` | B10: after READY, a BIND_RX_COMMAND (the stack's `acmpdu()`, IEEE 1722.1-2021 Figure 8-1) through `mbx_model_rx`; loop passes 10 ms of both clocks apart; sink 0 bound, one commit, a flash program. | R733-F2's second plant: the whole chain the platform composes (mailbox, loop, ACMP, the AECP bridge's persist, `nvm_store_changed`, the loop's tick, `nvm_store_service`, the flash). |
| `sw/firmware/ctrl/test/test_plat_boot.cpp:48-60`, `:4-16`, `:32-34` | `nvm_store.h` included in `extern "C"`; header text for B1 and B10. | The store's headers carry no `extern "C"` (as `test_acmp_nvm.cpp` includes them). |
| `sw/firmware/ctrl/test/plat_arms.py:22`, `:103-105` | The boot tests' compile adds `-I` the stack's tests (`STACK_TESTS`), last, for `acmp_fake.hpp`'s ACMPDU builder. | Last, so it shadows no firmware header; `compile_tests` already adds it for every other arm's tests. |
| `sw/firmware/ctrl/test/plat_mutants.py:36-41`, `:162-169` | `SAVED`, `SERVICE`, `OPEN` as `ctrl_plat.c` holds them; `plat-saved-state-after-mailbox-open` (R733's exact plant: `SAVED+SERVICE+OPEN` to `SERVICE+OPEN+SAVED`) named B1; `plat-store-service-unbound` (`SERVICE` removed) named B10. | The two plants, shipped. |
| `sw/firmware/ctrl/test/plat_mutants.py:3-22` | Module docstring: the new controls. | |
| `sw/firmware/ctrl/plat/README.md:102-109` | The `plat` arm under AddressSanitizer; `platboot`'s flash order and B10; 40 defects. | Docs. |

### Item 1, the boot driver (`6987b8d8`, `7b308437`)

| Where | What | Why |
|---|---|---|
| `tb/verilator/ctrl_split_boot/run.py:343-359` `point()` | Removes a stale `sim.status`, runs the model, writes its exit status to `sim.status`; grades with `saved_status(out)` on both paths; takes an optional `model` (a control's stand-in and spec) instead of `build()`. | R734-F1: the status was printed and discarded, and a regrade had none. |
| `run.py:335-340` `saved_status()` | The saved status, or None. | A regrade of a build directory without one is a finding, not a pass. |
| `run.py:248-269` `native()` | NATIVE findings: no saved status; a nonzero status; the tally read by `suite_tally.scan` / `is_nocount` (missing or zero: did not complete), an unparsed tally line, `log_reports_failure` (failed tally or `[FAIL]` line), with the model's `FAIL:` lines; a report line `NATIVE exit status N; <tally>`. | The model's own verdict, read as the sweep reads a suite log. |
| `run.py:272-277` `grade()` | Takes the status; NATIVE first, never returning early before it. | |
| `run.py:99-131` | `STATUS`, `PASSED`/`FAILED` (the checker's lines as `sim_main.cpp` prints them on a pass and on its time limit), `Control`, `NATIVE_CONTROLS` (six), `BANNER`, `ANSWERS`. | The controls. |
| `run.py:362-382` `stand_in()` | Writes a program that writes the boot transcript, prints `configure_fabric()`'s writes (the real host oracle) and MAAP's three, READY, the three commands answered as the grader passes them, then the control's end, and exits with its status; and the export's spec. | Valid earlier observations, so the only finding a control may give is NATIVE. |
| `run.py:385-406` `verdict()`, `native_controls()` | PASS / NATIVE / OTHER per path; a control is right only when both its run and its regrade give its required verdicts (OTHER is never right). | Both paths must reject. |
| `run.py:409-424` `self_test()`, `:433-441` `main()` | `--native-controls`; `--self-test` grades the controls first. A plant is caught only by a finding of its kind in a run with no NATIVE finding (`7b308437`). | |
| `run.py:84-95` `PLANTS` (`7b308437`) | `console-blocks` spins only before `milan_status`'s response. | The NATIVE check exposed that the plant spun before all three commands (about 2.1 s), so its run passed the 2,000 ms limit and the model failed; the old driver could not see it. Now the run ends inside the limit and the plant is caught by UART alone. |
| `run.py:4-40` | Docstring: NATIVE, the controls. | |
| `tb/verilator/ctrl_split_boot/README.md` | Run (`sim.status`, `--native-controls`), What is graded (NATIVE, the native controls, the plants in completed runs), Contents, R-2. | Docs. |

### Item 4, residue (`18fa9a45`)

24 files, comments and docstrings only: `(#665 S3)` to `(#665)`; `S3's` to `the platform's`; `S3: skipped, reordered, wrong` to `skipped, reordered, wrong`; `the measurement S3 owes` to `the platform measurement`; `S2's test-only split SoC` to `the CPU budget harness's test-only split SoC`; `D6 (#665, issuecomment-6409738976)` to `Decision D6`; `lane S14` to `hybrid XIP work (#665 decision D3)` (`ctrl_memory.py:210`); the ledger docstring's ruling numbers to `under #665's documented memory exceptions`. A scan of every added comment line in `f4c9ad4f..HEAD` finds no lane label, comment ID or ruling number left in a comment (`receipts/checks-at-ac105b15/residue_scan.txt`).

### Figures (`ac105b15`)

| Where | What |
|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:215-252` | Section 5 at the firmware of `b8628704`: platform `rom` 109,560 / 111,200 / 123,304 / 125,048 B (8 B more at each point, the console's compare), tiles unchanged 39.0 / 42.0 / 52.0 / 59.0; deltas +5,112 / +5,168 / +5,136 / +5,224; the cut 4,216 B of 5,224; console row +1,748; alignment +6 / +6 / +2 / +6. Measured: `receipts/measure-at-6987b8d8/images/`, `parts/`. |
| `tb/verilator/ctrl_split_boot/README.md:71-84` | Results at this firmware, each figure labelled with the split CPU 50 MHz and bus 100 MHz; NATIVE exit 0 on both runs. |
| `sw/firmware/gtest/coverage.ratchet:25` | `ctrl_plat_console.c` lines 119/119, branches 68/68, written by `fw_coverage.py --write` in a clone at `6987b8d8`; no other line changed. |

### Shared files touched this round

`docs/design/SPLIT_CONTROL_MEMORY.md` (section 5's platform rows only), `sw/firmware/gtest/coverage.ratchet` (one line, by its generator), `sw/litex/ctrl_memory.py` and `sw/litex/ctrl_memory_ledger.py` (one comment each), `ctrl_configs.py`, `ctrl_runs.py` (one comment each). All others are this lane's own files.

## New checks, planted defects and failing words

| Check | Planted defect | Failing words (receipt) |
|---|---|---|
| K3, NUL lines, under AddressSanitizer | `plat-command-read-past-its-end` (shipped) | `[FAIL] Plat.K3LinesEndOnceAndOthersAreRefused: crashed on signal 6`, ASan `global-buffer-overflow ... in is` (`checks-at-ac105b15/console_mutant_arm_log.log`); without the sanitizer it escapes, 0 checks failed (`console_mutant_without_asan.log`, rc 1 wanted) |
| B1, flash before the mailbox | `plat-saved-state-after-mailbox-open` (shipped, R733's plant) | `[FAIL] Boot.B1ReachesReadyInStepOrder: B1 the saved state is read before the mailbox's first access` (`new_mutants.log`, and shard 1) |
| B10, a bind's write-back through the loop | `plat-store-service-unbound` (shipped, R733's plant) | `[FAIL] Boot.B10ABindAfterReadyIsWrittenBackThroughTheLoop: B10 the bind is written back by the store's service on the loop's tick` (`new_mutants.log`, and shard 1) |
| NATIVE: nonzero exit | control `native-exits-nonzero` | `NATIVE: the model exited 1`, on the run and the regrade |
| NATIVE: failed tally | control `native-tally-failed` | `NATIVE: the model's log reports a failure: its tallies report 1 failure(s) across 1 checks; FAIL: simulation exceeded its time limit` |
| NATIVE: incomplete | control `native-incomplete` | `NATIVE: the model printed no tally: it did not complete` |
| NATIVE: both | control `native-fails-and-exits-nonzero` (R734's case) | both of the above |
| NATIVE: no saved status on regrade | control `native-status-not-saved` | run PASS; regrade `NATIVE: the run saved no exit status (sim.status), so how the model ended is unknown` |
| the NATIVE check itself | six planted copies of `run.py`'s check, in memory (`scripts/native_mutants.py`): exit status ignored; missing tally ignored; failed tally ignored; status not saved; regrade assumes success; missing status read as success | each grades at least one control WRONG: 6 of 6 caught (`checks-at-ac105b15/native_mutants.log`) |
| a plant must be found in a completed run | `console-blocks` as it was (spinning before every command) | before `7b308437`: `PLANT console-blocks: caught (UART)` beside `NATIVE: the model exited 1` and `FAIL: simulation exceeded its time limit` (`measure-at-6987b8d8/boot/split_boot-selftest.log`) |

## Gate table

Every gate at `ac105b15`, each in a fresh clone of the head (submodules at their gitlinks), each its own transient
unit (MemoryMax 10G, `systemd-run --wait`) pinned to one of two CPU ranges of the one free pick (32-39, 40-47), two
serial chains (`scripts/chain_a.sh`, `scripts/chain_b.sh`); the clone's tree was clean after every gate. Receipts:
`receipts/gates-at-ac105b15/`.

| Gate | Command | Result | rc | s | Receipt |
|---|---|---|---:|---:|---|
| firmware self-test, shard 0 (suites) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 8` | PASS; `plat` (test_plat under ASan, 10 tests), `platboot` x2 (10 tests each), `platrv32`, `plattrace` | 0 | 331 | `selftest-shard0.log` |
| shard 1 (control campaign) | `... --shard 1/4 --jobs 8` | 568 of 568 caught (565 + the 3 new platform defects); every platform test named | 0 | 1162 | `selftest-shard1.log` |
| shard 2 (AECP campaign) | `... --shard 2/4 --jobs 8` | 137 caught, as before | 0 | 460 | `selftest-shard2.log` |
| shard 3 (SRP campaigns, pin controls) | `... --shard 3/4 --jobs 8` | 278 caught and the 2 lwSRP pin controls, as before | 0 | 728 | `selftest-shard3.log` |
| firmware coverage | `python3 sw/firmware/gtest/fw_coverage.py --selftest && python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8` | 29 of 29 planted cases; `firmware coverage: PASS (35 files)`; console 119/119, 68/68 | 0 | 284 | `fw_coverage.log` |
| the memory test | `python3 sw/litex/test_ctrl_memory.py` | `RESULT: PASS` (47 mutants, 6 planted ledgers) | 0 | 69 | `test_ctrl_memory.log` |
| images at four points, both images; six refusals | `scripts/images.sh` | platform 39.0 / 42.0 / 52.0 / 59.0 (`rom` 109,560 / 111,200 / 123,304 / 125,048 B), fixture 37.0 / 40.5 / 50.5 / 57.5; the six refusals rc 2, wanted 2; every ELF byte-identical to `6987b8d8`'s | 0 | 62 | `images.log`, `images/`, `images/elf_digests.txt` |
| split boot, 1x1 | `python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <build>/boot-1x1` | PASS, 0 findings; NATIVE exit status 0, tally 1/0; 84.383 ms, 4,219,150 CPU cycles at 50 MHz | 0 | 39 | `boot/split_boot-1x1.log`, `boot/split_boot-1x1.sim.status` |
| its regrade | `... --regrade` | the same | 0 | 1 | `boot/split_boot-1x1-regrade.log` |
| split boot, 8x8 | `... --build-dir <build>/boot-8x8 --shape endstation_ax7101_8x8` | PASS, 0 findings; NATIVE exit 0; 184.647 ms, 9,232,360 CPU cycles at 50 MHz | 0 | 58 | `boot/split_boot-8x8.log` |
| its regrade | `... --shape endstation_ax7101_8x8 --regrade` | the same | 0 | 0 | `boot/split_boot-8x8-regrade.log` |
| native controls | `... --build-dir <build>/boot-native --native-controls` | 6 of 6 as required | 0 | 8 | `boot/split_boot-native-controls.log` |
| boot self-test | `... --build-dir <build>/boot-plants --self-test` | 6 of 6 native controls; `csr-write-skipped` caught (TRACE; the run completed), `console-blocks` caught (UART; the run completed; 742.670 ms span) | 0 | 196 | `boot/split_boot-selftest.log` |
| end-station builder | `python3 sw/builder/test_builder.py --require-rv32` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, the calibration report of a local Arty build, as at the base) | 0 | 1507 | `builder_require_rv32.log` |
| TSN stack boundary | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `ctrl_boundary: PASS`, 0 findings; 112 boundary, 167 pin and 4 figure controls | 0 | 1112 | `ctrl_boundary-without-verilator.log` |
| docs, scope, idiom, harness self-test, CPU options, `git diff --check`, rtl-fast's bdd-conformance | `scripts/docs_gates.sh` (`gates_s3.py`, 97 gates one at a time) | 0 of 97 nonzero; `behave` 14 features, 406 scenarios, 1977 steps | 0 | 1449 | `docs/runner.out`, one log per gate |
| CPU budget harness, 1x1 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <build>/budget-1x1 --record-budget-findings --jobs 4` | 18 groups graded, 0 refusals; 13 of 81 paths miss T_svc (34 of 141 instances), as at `5edbba1d`; CPU 50 MHz, bus 100 MHz (`s2_harness-clocks.txt`) | 0 | 2165 | `s2_harness-1x1.log` |
| CPU budget harness, 8x8 | `... --point 8x8 ...` | 17 groups graded, 0 refusals; 30 of 129 paths miss T_svc (62 of 182 instances), as at `5edbba1d`; CPU 50 MHz, bus 100 MHz | 0 | 2577 | `s2_harness-8x8.log` |

Lane checks at `ac105b15` (`receipts/checks-at-ac105b15/`, one clone, in the agent's unit):

| Check | Result | rc (wanted) | Receipt |
|---|---|---|---|
| the NATIVE check's six planted defects (`scripts/native_mutants.py`) | 6 of 6 caught | 0 (0) | `native_mutants.log` |
| R734's probe (a copy of `probe_boot_exit.py`) | `DEFECT REJECTED`: native exit 1 gives gate exit 1 on the run and the regrade | 0 (0) | `r734_probe_boot_exit.log` |
| R733's NUL probe under ASan (`scripts/asan_probe.sh`) | the fix: answered `?`, no report; the revert: `global-buffer-overflow ... ctrl_plat_console.c:135 in is` | 0 (0) | `r733_console_nul_asan.log` |
| the three new shipped defects through the campaign (`scripts/plat_quick.py mutants`) | 3 of 3 caught, each by its named test and words | 0 (0) | `new_mutants.log` |
| the console defect with the sanitizer withheld (`plat_quick.py noasan`) | escapes, 0 checks failed: the sanitizer is what catches it | 1 (1) | `console_mutant_without_asan.log` |
| the console defect's arm log (`plat_quick.py armlog`) | `[FAIL] Plat.K3...: crashed on signal 6`, the ASan report, `verdict: FAIL (... exit -6)`; caught | 0 (0) | `console_mutant_arm_log.log` |
| comment residue scan of the delta | 0 comment lines; 22 string or code lines (the boundary gate's classification texts, the ledger's reason strings, numeric literals) | | `residue_scan.txt` |

Measurement runs at `6987b8d8` (`receipts/measure-at-6987b8d8/`): the images and their by-part split (`parts/`), the
boot runs (the README's results), and `fw_coverage.py --write` (the ratchet line), each its own unit; the ELFs at the
head are byte-identical to these.

Not re-run this round, because nothing they read changed: the saved-state store gate and its planted defects
(`ctrl_nvm` is unchanged), the MAAP differential, the Verilator boundary leg, `fw_rv32_selftest.py` and
`tally_selftest.py`. [A697b]'s runs at `5edbba1d` are in `../665s3-a697b/receipts/`. The full sweep and Vivado: no
RTL changed; no route is owed by S3.

## Measurements

Boot simulation at `6987b8d8` (the same firmware and harness as the head's, `receipts/measure-at-6987b8d8/boot/`), split CPU 50 MHz, bus 100 MHz, simulated time:

| Point | Ready | CPU cycles at 50 MHz | `milan_status` span / first byte / gap | `milan_gettime` worst |
|---|---:|---:|---|---|
| 1x1, one interface | 84.383 ms | 4,219,150 | 21.531 / 1.962 / 1.265 ms | 2.523 / 1.238 / 1.265 ms |
| 8x8, one interface | 184.647 ms | 9,232,360 | 40.197 / 2.855 / 2.205 ms | 4.051 / 2.131 / 1.857 ms |

Both NATIVE exit status 0 with a passing tally; both regrades equal. VexiiRiscv netlist `VexiiRiscvLitex_903b010fc69f2a4188ee1b2191a0834e`, the one [A697b] built at `5edbba1d`.

## Other notes

- The NATIVE check exposed a plant run that never completed: before `7b308437` the console plant spun before all
  three commands, so its run passed the 2,000 ms limit (`FAIL: simulation exceeded its time limit`) while the old
  driver reported it caught. [A697b]'s self-test receipt at `5edbba1d` had the same hidden failure. The plant now
  spins only before `milan_status`'s response (its run ends at bus cycle 83,294,742, 832.9 ms of simulated time at the 100 MHz bus, 41,647,371 CPU cycles at 50 MHz; exit status 0), and a plant counts
  only in a completed run.
- `ctrl_plat_console.c` grows by 4 B of `.text` (the compare) and its alignment by 4 B: the platform's `rom` need is
  8 B larger at every point, the tiles unchanged; the 59.0 ledger entry keys on `ctrl_plat` and `nvm_stage`, whose
  sizes are unchanged, so it still recognises the image.
- Receipts: `receipts/INDEX.md` (generated from the files present by `scripts/finalize_receipts.py`, host paths
  replaced by placeholders); the two logs over 190 KB are kept as excerpts, their whole size and sha256 in
  `receipts/WHOLE-LOGS.txt`; the raw copies are on the lane's disk scratch, `$VALIDATION_STORAGE/665s3-a697d/raw-receipts`.
- Scratch on disk: `$VALIDATION_STORAGE/665s3-a697d` (the clones at `6987b8d8` and `ac105b15`, their builds, the copied
  runtime archives and boot-SoC maps). Nothing of this lane's is in tmpfs `/tmp`.
- Helper scripts (`scripts/`): `chain_a.sh`, `chain_b.sh`, `unitw.sh`, `gate.sh`, `env.sh`, `clone.sh`, `boot.sh`,
  `images.sh`, `docs_gates.sh`, `gates_s3.py`, `parts.py`, `finalize_receipts.py` (last round's, re-pointed);
  `plat_quick.py` (the platform arms or chosen defects through the campaign, the no-sanitizer control, one defect's
  arm log), `native_mutants.py`, `asan_probe.sh`, `stage_hunks.py` (stages chosen zero-context hunks, used to keep
  each finding's commit to its own hunks).
