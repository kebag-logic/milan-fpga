# HANDOFF: #665 lane FT, the GoogleTest/GoogleMock harness ([A547])

Status: REVIEW READY (round 3) at `6ca834a782a1bd5574d44998c8e214cf16df3441` (local branch `665-ft-gtest`, not pushed), posted on #665 as comment 6015346011. Round 2's REVIEW READY at `e7e0c10f` was comment 6013685269.

- Issue: kebag-logic/milan-fpga#665. Assignment: comment 6009234414. Round 1: TAKEN 6009299837, REVIEW READY 6011410375 at `27433e47`.
- Round 2: assignment 6012062072, on R506-1 (6011948437) and R507-1 (6012056114), both NEGATIVE at `27433e47`. TAKEN (round 2): 6012112514.
- Round 3: assignment 6014362247, on R506-2 (6014356451), NEGATIVE on three MINORs at `e7e0c10f`; R507-2 (6014209924) POSITIVE at `e7e0c10f`. TAKEN (round 3): 6014399613.
- Base: dev `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`. Round-1 commits: `bd5c89695`, `1b3cca0d0`, `ddd1adfb5`, `36014e0b4`, `4e6f0c46d`, `4018e3260`, `27433e47c` (subjects in the branch log). Round-2 commits on top of `27433e47c`, one-line subjects, no rebase, no amend:
  - `8387d18fe` Test the pool's free list cut short and the codec's loaded prefix that ends before a record header, each with planted defects, and drop both coverage exclusions (#665 FT)
  - `341ea77e3` Bind each coverage exclusion to its statement's exact uncovered arcs and lines, refuse one whose items move even with the function's totals unchanged, and print the toolchain the gate measured with (#665 FT)
  - `7412748eb` Hold every planted case of the tally self-test to its tally line, plant listener defects it must catch, keep GTEST_ variables away from test binaries, and print the ctrl gate's toolchain (#665 FT)
  - `e7e0c10f4` Say which state the ADP machine is left in by a timer port that calls back from inside timer_start, as the two probes show (#665 FT)
- Round-3 commits on top of `e7e0c10f4`, one-line subjects, no rebase, no amend:
  - `7a2686aee` Pin the loaded-prefix guards at their exact ends: a record header claiming a payload past the container gets its own VD_LEN only once the header guard passes, with both guards planted one byte off either way (#665 FT)
  - `89b02c7f4` Plant SIGBUS, SIGFPE and SIGILL, a suite's tear-down, the global environment and a disabled suite in the tally self-test, each held to its tally line, and a listener defect for each path (#665 FT)
  - `6ca834a78` Say that the five ADP coverage exclusions rest on the no-callback rule #678 rules, not on adp.h as it stands, and which port call reaches each row's items (#665 FT)
- Dev moved to `30e3c018` during round 2 (20 commits, PR #658's dynmap work) and is still there at round 3 (`git fetch`, 2026-10-06). None of its files is one this lane changed, so nothing was merged in either round, as the instructions direct. A scratch merge of it into the head is clean, and the contract gates pass on it (section 7); that is not the candidate-merge validation, which stays with the manager.
- Roles: executor [A547]; reviewers [R506] (internal), [R507] (external).
- Receipts: every `gates/...` and `hosted/...` file named below (round 2 and earlier) and every `r3/...` file (round 3) is kept in the lane's scratch directory, not here (its logs carry local paths). `RECEIPTS.sha256` beside this file lists each one's SHA-256 and size.
- No RTL change, no change to the default build or the shipping image. Round 2 changes tests, the harness, the coverage gate and its ratchet, docs, and two comment lines of `sw/firmware/ctrl_nvm/nvm_klj2.c` (the comment above the guard the new codec test reaches; no code, the line count unchanged). Nothing under `hdl/`, `syn/`, `configs/`, `sw/litex/`, `sw/builder/` or `.github/` changed in round 2. Round 3 changes two tests, the planted-defect list, the tally cases and self-test, and two READMEs; no firmware source at all.

## Contents

R3. Round 3: every finding, the change, the evidence
0. Round 2: every finding, the change, the evidence
1. Harness layout
2. The tally listener, with its planted failure and crash cases
3. Port table: old check -> new test, with counts
4. Mutation arms and the test that kills each
5. Coverage per file, every exclusion and its reason
6. CI wiring: hosted and act evidence
7. Gate table
8. Open risks and questions

## R3. Round 3: every finding, the change, the evidence

Assignment 6014362247, on R506-2 (6014356451, NEGATIVE on three MINORs at `e7e0c10f`) with R507-2
(6014209924) POSITIVE at the same head. Three one-line commits on `e7e0c10f4`, one per finding; no
firmware source, RTL, workflow, classifier, builder or shipping-image file changed
(`git diff --stat e7e0c10f4 HEAD`: `test_nvm_codec.cpp`, `nvm_mutants.py`, `ctrl_nvm/README.md`,
`tally_cases.cpp`, `tally_selftest.py`, `gtest/README.md`). Lens labels below are the reviewer's.

| Finding | Lenses | Change | Evidence at the head |
|---|---|---|---|
| R506-2-F1 MINOR: `codec_loaded_prefix` did not pin the record-header guard at its exact end; the guard written `>=` passed every test and the coverage gate | Conformance, Robustness, Tests | `NvmCodec.codec_loaded_prefix` (`test_nvm_codec.cpp`), for every record of the shape: a copy of `golden@5` whose record header claims a payload one byte past the container's end, resealed (the CRC-32 recomputed, so `nvm_klj2_check` gives that header's `NVM_VD_LEN`, not `NVM_VD_CRC`). One byte short of the header's end it is refused `NVM_VD_REC` (the guard); at the header's exact end it gets `NVM_VD_LEN`, the header's own verdict, which only a guard that passes there can reach. On the last record, the payload's guard the same way: one byte short of the payload's end `NVM_VD_REC`, at its exact end `NVM_VD_OK`. Four planted defects in `nvm_mutants.py`, each named on `codec_loaded_prefix`: `header_guard_early` (`>=`), `header_guard_late` (`> loaded + 1u`), `payload_guard_early` (`>=`), `payload_guard_late` (`> loaded + 1u`). The payload's pair goes past what F1 asked; it is the same test's other guard and is stated here. S1 taken: the test comment names the erased-record case left out and #677. No firmware change; the public contract is unchanged; coverage is unchanged (`nvm_klj2.c` 195/196 lines, 104/108 branches raw). | store gate `--require-rv32 --self-test --jobs 8`: 434 tests, `all 106 planted defects reddened`, each new one by its intended assertion: `header_guard_early` "at record 0's header's exact end, the guard passes and the header is VD_LEN", `header_guard_late` "one byte short of record 0's header, the guard refuses it VD_REC", `payload_guard_early` "a prefix that ends at the last record's payload's exact end is accepted", `payload_guard_late` "a prefix one byte short of the last record's payload is refused VD_REC" (`r3/gates/nvm-self.log`). R506-2's `guard_ge_probe.sh`, unchanged, against the head: rc 1: at each of the 5 shapes the boot-and-write binary fails 1 test of 85, `NvmCodec.codec_loaded_prefix`, with `[FAIL] NvmCodec.codec_loaded_prefix: at record N's header's exact end, the guard passes and the header is VD_LEN` for every record (`r3/gates/probe-r506-guard-ge.log`) |
| R506-2-F2 MINOR: the README stated the exclusion standard as met while the ADP rows rest on a premise `adp.h` does not state, and named only the timer port and two rows | Conformance, Tests, Docs | `sw/firmware/gtest/README.md`: the standard paragraph now says nine rows meet it through their headers as they stand and the five `adp.c` rows do not yet, resting on a rule `adp.h` does not state, which #678 has ruled. The premise paragraph is headed "The five `adp.c` rows rest on #678's rule, not on `adp.h` as it stands", cites #678 (ports never call back into the core synchronously; its F0 follow-up adds the rule to `adp.h` and the port headers and guards it in the core), says the adapter keeps the rule today (its ports call no core function; the core is called only from the loop's handlers), and lists, measured, which port call reaches which row's items: a send port calling `adp_link_change(false)` from inside a send reaches rows 1 and 2 (arc 2 of 2 each); a timer port expiring a timer from inside `timer_start` reaches row 3 (arc 4 of 4) and row 4 (arcs 2 and 4 of 4 and its stray-count line); a link port calling back twice from inside `adp_set_enable(true)` (link up, then the TMR_DELAY expiry, while the send port has no room) reaches row 5 (arcs 2 and 4 of 4 and its line). It closes: `adp.c`'s 100 % holds for ports that keep #678's rule, and not for a port that breaks it. No firmware change. The PR body's decision bullet now cites #678 and the same reach. | my probe `adp_reentry_rows.py` (scratch `r3/probes/adp/`): `adp.c` built for gcov with ports that call back, six scenarios each measured alone, the README's rows applied with the gate's own parser: every named arc and line of the five rows reached, each by the scenario the README names (`r3/gates/probe-adp-reentry-rows.log`). R506-2's `adp_reentry_probe.py`, unchanged: rows 1 to 4 reached, row 5 not, as it reported (`r3/gates/probe-r506-adp-reentry.log`) |
| R506-2-F3 MINOR: the tally self-test did not plant four listener behaviours the README says it proves; four listener defects escaped, one leaving the tally line at `RESULT: PASS` | Tests, Docs | `tally_cases.cpp`: six planted cases, `Crash.Bus`, `Crash.Fpe` and `Crash.Ill` (the signal raised inside a test), `TearDownFails` (a suite's tear-down fails), `ProgramFails` (a global environment whose set-up fails only in the run whose filter selects that suite, so the failure is outside every test) and `DISABLED_Suite.NeverRuns` (a disabled suite). `tally_selftest.py` holds each to its tally line: 1/1 for each signal and for the tear-down and the program (their test passed, so the listener's count is the only failure, and a listener that drops it prints `RESULT: PASS`), 0/1 for the disabled suite. Listener defects 11 -> 18: each of the five signals dropped from the handler's list, `program-failure-not-counted`, `disabled-suite-not-counted`; `setup-failure-not-counted` renamed `suite-failure-not-counted` and now names the tear-down case too; both crash-tally defects and `no-signal-handler` name all five signal cases; `disabled-not-counted` names the disabled suite; `result-always-pass` names the tear-down and program cases. README: the counting sentence names the suite's set-up or tear-down, the program's failure and the disabled suite; the table has the six rows; the `--mutants` paragraph lists the eighteen. | `tally_selftest.py --mutants`: 18 of 18 cases, 18 of 18 defects, gcc 16.2.1 / GoogleTest 1.18.0 (`r3/gates/tally-mutants.log`), and 18 of 18 and 18 of 18 with gcc 13.3.0 / GoogleTest 1.14.0 (`r3/gates/tally-mutants-gcc13.log`). R506-2's `tally_extra_plants.py`, unchanged, against the head: its six cases read as planted, and each of its four defects (`sigfpe-unhandled`, `sigbus-unhandled`, `program-failure-not-counted`, `disabled-suite-not-counted`) now reddens the head's own planted cases (`r3/gates/probe-r506-tally-extra.log`) |
| R506-2-S1 SUGGESTION: say in the tree that `codec_loaded_prefix` leaves out the erased record whose header ends at `loaded` | Docs | the test comment: "Left out: an erased record whose header ends exactly at `loaded`. Its verdict is right, but nvm_klj2_record reads its erased payload past `loaded` to reach it, which a buffer holding the whole container cannot show; the fix and its test are #677's." | `test_nvm_codec.cpp` |
| R506-2-R1 and R507-2-R1 RESIDUE: PR body's hosted status stale | Docs | PR-BODY.md Status and Known limitations: dated, at `e7e0c10f`, `rtl-fast` run 37445962183 passed with `firmware-unit` (job 112210865722); no hosted run at the round-3 head (this lane does not push); the manager owns the remaining hosted contexts and the act replica. This lane does not edit the PR. | `r3/gates/hosted-checks-e7e0c10f.txt` |

The Issues the round-2 handoff proposed now exist and are cited: #677 (the erased-record read), #678
(the ADP no-callback rule, ruled), #679 (the ctrl `rv32` arm against the CI-pinned SDK); and #673
(hosted shard 2's `milan_dp_mclk` timeout).

## 0. Round 2: every finding, the change, the evidence

| Finding | Lenses (the reviewer's) | Change | Evidence at the head |
|---|---|---|---|
| R507-1-F1 MAJOR: `nvm_klj2_check_body`'s refusal of a loaded prefix shorter than the next record header is reachable through `nvm_klj2.h` and was excluded | Conformance, Robustness, Tests, Docs | New test `NvmCodec.codec_loaded_prefix` (`test_nvm_codec.cpp`): the blank container with only its 40-byte header loaded, and one byte short of the first record header (47), each `NVM_VD_REC`; then, for every record of a container of frames (`golden@5`), one byte short of its header and its header whole without its payload, each `NVM_VD_REC`; the whole container `NVM_VD_OK`. Each buffer holds the whole container, so a walk that read past `loaded` finds valid bytes and accepts the blank one. Two planted defects in `nvm_mutants.py`: `short_prefix_read_on` (the guard removed) and `short_prefix_as_len` (refused `NVM_VD_LEN`), both named on `codec_loaded_prefix`. The exclusion row is gone; `coverage.ratchet` records `nvm_klj2.c` at lines 195/195, branches 104/104. The comment above the guard said "unreachable"; it now says what the test shows. The public contract and the refusal are unchanged. | `test_ctrl_nvm.py --require-rv32 --self-test`: 434 tests (one more per shape), all 102 defects reddened, both new ones by `codec_loaded_prefix` (`gates/nvm-self.log`); coverage PASS with the row gone (`gates/cov-check.log`) |
| R507-1-F2 MAJOR and R506-1-S1: an exclusion matched only per-function totals, so an uncovered branch could move inside a function unseen | Conformance, Robustness, Tests, Docs | `fw_coverage.py`: a row now names its statement (a fragment of its first line, once in the function; the statement runs to where its parentheses close and it ends) and exactly the uncovered items it permits: `arcs K, L of N` (positions among the statement's N arcs in gcov's order, counted over the statement's lines) and `line \`frag\`` (the first line from the statement's on that holds the fragment). The gate refuses a statement with another arc count, any other uncovered arc of it, a named arc or line that is covered, an item named twice, and any uncovered arc or line of a function with rows that no row names; it removes only the named items, so anything else stays in the file's tally for the ratchet. The README states exactly this guarantee. `fw_coverage_selftest.py` goes from 18 to 28 cases: R506-1-S1's fixture swap, an arc moved within its statement, a statement with another arc count, a line fragment found nowhere, two rows on one arc, a stale row whose named line runs, and on the real compiler a compensating swap (control passes, swap refused with the function's totals unchanged) and a condition over two lines (control passes, the other operand's arc refused). The multi-line, shorter-arc-vector, stale-row, missing-file and per-file-drop cases are kept. | gcc 16.2.1: `--selftest` 28 of 28, `--check` PASS; gcc 13.3.0 (the `ubuntu:24.04` replay of `firmware-unit`): 28 of 28 and PASS with the same per-file table. Both compilers give every one of the 14 rows the same arc count and the same uncovered positions (section 5). R507-1's probe, its row written in the new form: the control passes and the swap is refused; R506-1's swap probe is refused (`gates/probe-r507-coverage-newrow.log`, `gates/probe-r506-swap.log`) |
| R506-1-F1 MINOR: `ctrl_pool_alloc`'s `bin->free_head != NULL` is reachable (a client writing into a freed block) and was excluded | Conformance, Tests, Robustness, Docs | New test `Pool.P9AFreeListShorterThanItsCountIsExhausted` (`test_port_loop.cpp`): two blocks freed, the head block's link overwritten with NULL as a client's write after free would, then the head is handed out, the small class counts three free blocks and no list, the next class serves two allocations, and the next is refused and counted. Two planted defects in `ctrl_mutants.py`: `pool-follows-a-cut-free-list` (the guard removed; the NULL is dereferenced and the crash report names P9) and `pool-cut-list-refuses-outright` (a cut class refuses instead of passing to the next class). The row is gone; the ratchet records `ctrl_pool.c` at branches 60/60. | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <pin>`: `mutants: 76 of 76 caught`, `[FAIL] Pool.P9AFreeListShorterThanItsCountIsExhausted: crashed on signal 11` and `... P9 a class whose list ends before its count is exhausted, not followed: the next class serves` (`gates/ctrl-self.log`) |
| Assignment item 3: every remaining exclusion re-judged against its module's public header, not today's callers | (assignment) | Each of the 14 remaining rows was judged against `adp.h`, `adp_mbx.h`, `ctrl_app.h`, `nvm_klj2.h`, `nvm_store.h` and the `struct nvm_flash` port (section 5 table). All 14 hold. The ADP rows rest on two premises about the ports, now stated in the README: `adp.h`'s "delay_ms later" for the timer, and a no-callback rule `adp.h` does not state. Under a timer port that calls back from inside `timer_start`, the third and fourth ADP rows are reached and the machine is left with no timer running (probes; section 8, question 2). | `gates/probe-adp-reentry.log`, `gates/probe-adp-reentry2.log` |
| R506-1-F2 MINOR: the tally self-test never asserted the tally line, so listener defects that falsified it survived | Tests, Conformance (R507-1 adds Robustness, Docs) | `tally_selftest.py`: every planted case now reads its tally line with `suite_tally.scan` and must carry exactly its `checks` and `failures` (control 1/0; failing, crashing, aborting, exiting, skipped and throwing tests 1/1; disabled 0/1; suite set-up 1/2; empty 0/0; `_exit` none), one listener line with the cases' label, and `RESULT: FAIL` exactly when `failures` is not 0. New `--mutants` mode: 11 listener defects planted into copies of `fw_gtest_main.cpp` (skip, set-up, crash, early-exit and disabled failures not counted; a crashed test not counted as a check; `RESULT: PASS` always; no test counted; no `[FAIL]` line; no `atexit`; no signal handler), each required to turn the cases it names red. | 12 of 12 cases and 11 of 11 defects caught with GoogleTest 1.18.0 (`gates/tally-mutants.log`) and with 1.14.0 in the gcc 13 image (`gates/tally-mutants-gcc13.log`). R506-1's own seven plants (`tally_mutants.sh`) are all caught now; the first `disabled-not-counted` plant does not build, as in R506-1's run (`gates/probe-r506-tally-mutants.log`) |
| R506-1-F3 MINOR: the README said each gate prints the toolchain; only the store gate did | Docs | The coverage gate (every mode), the ctrl gate and the tally self-test now print a `toolchain:` line first, as the store gate does; the README names which gates print it and that a gate's coverage mode leaves it to the coverage gate. | first lines of `gates/ctrl-self.log`, `gates/cov-check.log`, `gates/tally-mutants.log`, and of steps 03, 04, 07 and 08 of the replay |
| R506-1-S2 SUGGESTION: the gates inherited `GTEST_*` | Robustness | `fw_gtest.run` drops `GTEST_*` from every child's environment. A planted case runs the disabled test with `GTEST_ALSO_RUN_DISABLED_TESTS=1` set and requires the 0/1 tally. | the case passes; with the filter removed from a scratch copy it fails (`tally 1/0`, `RESULT: PASS`, graded PASS; `gates/envprobe.log`, rc 1) |
| R506-1-R1 RESIDUE: the PR body said no hosted run exists | Docs | PR-BODY.md names the hosted run at `27433e47` and its result (section 6). This lane does not edit the PR. | PR-BODY.md |

Two things found while doing this, published here and not changed (both firmware behaviour, outside a test lane):

1. **`nvm_klj2_record` reads an erased record's payload past `loaded`.** The erased-record branch (`nvm_klj2.c:298`, `nvm_all_erased(p + NVM_REC_HDR, r.plen)`) checks the payload against `end`, not against `loaded`, while the framed branch refuses a payload past `loaded` before reading it. A caller holding exactly the first 48 bytes of a CRC-closed blank container (header loaded, payload not), as `nvm_klj2.h` allows, gets an out-of-bounds read: AddressSanitizer reports a heap-buffer-overflow at `nvm_klj2.c:298` (`gates/probe-overread.log`). With the whole container in the buffer the verdict is `NVM_VD_REC` either way, and the store's own calls cannot reach it (they load the whole stage). `codec_loaded_prefix` tests the blank container at 40 and 47 bytes, where the header guard refuses before any read, and the adjacent header boundary (the header whole, its payload not) on framed records, where the framed branch refuses before reading. It leaves out the erased record at that boundary, which is where the read happens. Proposed Issue: refuse an erased record whose span passes `loaded` before reading it, and test it with a buffer of exactly `loaded` bytes.
2. **The ADP rows' premise about the ports.** See section 8, question 2.

## 1. Harness layout

The authoritative description is `sw/firmware/gtest/README.md` (linked from `docs/README.md`,
`docs/design/MAILBOX_SPLIT.md`, both firmware READMEs and `docs/testing/CI_WORKFLOWS.md`).

| Path | What it holds |
|---|---|
| `sw/firmware/gtest/fw_gtest.hpp`, `fw_gtest_main.cpp` | `main()` of every firmware test binary: GoogleTest, GoogleMock, the tally listener, the crash and early-exit handlers |
| `sw/firmware/gtest/fw_gtest.py` | the build (C11 firmware with the target's flags, C++20 tests, the harness main), the run with a timeout, the grade (`grade`), the toolchain banner |
| `sw/firmware/gtest/tally_cases.cpp`, `tally_selftest.py` | the listener's planted cases and their self-test |
| `sw/firmware/gtest/fw_coverage.py`, `fw_coverage_selftest.py`, `coverage.ratchet` | the gcov JSON reader, the exclusion matcher, the ratchet, and their planted cases |
| `sw/firmware/ctrl/test/` | `test_port_loop.cpp`, `test_adp.cpp`, `adp_walk.cpp`, `model_suite.cpp`, `entity_fields.cpp`, `lwsrp_port.cpp` (ported); `test_unit_seams.cpp`, `test_unit_driver.cpp`, `test_mmio.cpp` (new `unit` arm); mocks `mock_mbx_hal.*`, `mock_shlan_port.*`, `unit_window.hpp`, `mmio_window.h` |
| `sw/firmware/ctrl_nvm/test/` | `test_nvm_boot.cpp`, `test_nvm_write.cpp`, `test_nvm_vector.cpp` (ported); `test_nvm_more.cpp`, `test_nvm_codec.cpp`, `test_nvm_flashmock.cpp`, `test_nvm_shapes.cpp`, `test_nvm_litespi.cpp` (new); the in-process rig `nvm_rig.*`, the suite fixture `nvm_suite.*`, the C shim `nvm_c.hpp`, the fixture writer `nvm_fixture.py` (oracle: `scripts/nvm_klj2.py`), mocks `mock_nvm_flash.hpp`, `mock_litespi_csr.*` |
| retired | `test_check.h/.c`, `test_adp.c`, `test_port_loop.c`, `lwsrp_port.c`, `entity_probe.c`, `nvm_test.c`, `nvm_checks.py`, `nvm_checks_write.py`: nothing uses them |

Firmware stays C11, bare metal, no heap; tests are host C++ including the C headers through `extern "C"`.
Seams mocked are only the ones the firmware already has: `mbx_hal.h` (link seam), `shlan_port.h`
(link seam), `nvm_flash.h` (function-pointer port) and the LiteSPI port's `<generated/csr.h>` accessors
(link seam onto the host stubs). No seam was added; no STOP condition arose.

GoogleTest and GoogleMock come from the distribution (`libgtest-dev`, `libgmock-dev`), found through
pkg-config. Versions recorded: development host gcc/gcov 16.2.1, GoogleTest/GoogleMock 1.18.0;
`ubuntu-24.04` runner (as the job installs them) gcc/gcov 13.3.0, `libgtest-dev`/`libgmock-dev`
1.14.0-1. The ctrl gate, the store's gate, the coverage gate (every mode) and the tally self-test
print a `toolchain:` line first (round 2: the ctrl gate, the coverage gate and the tally self-test
did not before; R506-1-F3). A gate's `--coverage` mode leaves it to the coverage gate that drives
it. The CI job also prints `dpkg-query`, `g++ --version` and `gcov --version`. `fw_gtest.run` drops
`GTEST_*` from every child's environment (R506-1-S2).


## 2. The tally listener

Every binary prints exactly the shape `scripts/suite_tally.py` reads,
`== <label>: checks: N   failures: M ==` then `RESULT: PASS|FAIL`, where checks = tests run and
failures = tests failed, skipped or crashed, plus one per test suite whose set-up or tear-down
failed, one for a failure outside every test (a global environment's), and one per disabled test,
alone or in a disabled suite. Every failed assertion prints `[FAIL] <Suite.Test>: <its last line>`
(the `--verdict` marker and the campaigns' match). A fatal signal (SIGSEGV, SIGBUS, SIGFPE, SIGILL,
SIGABRT) prints the `[FAIL]` line and a failing tally from an async-signal-safe handler, then
re-raises; `exit()` inside a test is caught by `atexit`; `_exit()` and SIGKILL leave no tally, which
the reader refuses as `NOCOUNT`. `fw_gtest.grade` passes a binary only when it exits 0 AND its log
reads as a pass.

Round 2 (R506-1-F2): each planted case also holds the tally line itself, read with
`suite_tally.scan`, to its exact `checks` and `failures`, the cases' own label, and `RESULT: FAIL`
exactly when `failures` is not 0. So a listener that falsifies the line fails the self-test even
while the `[FAIL]` marker or the exit status still refuses the run. A case runs the disabled test
with `GTEST_ALSO_RUN_DISABLED_TESTS=1` in the environment, which the gates drop (R506-1-S2).

Round 3 (R506-2-F3): every listener path the README names now has a planted case, 18 in all: the
five fatal signals (SIGBUS, SIGFPE and SIGILL added), a suite's set-up and tear-down failure (the
tear-down added), a failure in the global environment (added; `ProgramFails`, whose environment
fails only in the run that selects it), a disabled test and a disabled suite (added). `--mutants`
plants 18 listener defects into copies of `fw_gtest_main.cpp` and requires each to turn the cases it
names red; a copy that does not build is an escape. The tear-down and program cases are the two
where a listener that drops its count prints `RESULT: PASS` on the tally line itself: their test
passed, so the listener's count is the only failure (`suite-failure-not-counted`,
`program-failure-not-counted`).

| Listener defect | Planted cases it must turn red |
|---|---|
| `skip-not-counted` | `Skip.*` |
| `suite-failure-not-counted` (round 2's `setup-failure-not-counted`) | `SetUpFails.*`, `TearDownFails.*` |
| `crash-tally-passes`, `crashed-test-not-counted`, `no-signal-handler` | `Crash.Segv`, `Crash.Abort`, `Crash.Bus`, `Crash.Fpe`, `Crash.Ill` |
| `early-exit-tally-passes`, `no-atexit` | `Exit.Zero` |
| `disabled-not-counted` | `Disabled.*`, `DISABLED_Suite.*` |
| `result-always-pass` | `Fail.*`, `Crash.Segv`, `Exit.Zero`, `Skip.*`, `Disabled.*`, `TearDownFails.*`, `ProgramFails.*` |
| `tests-not-counted` | `Pass.*`, `Fail.*` |
| `fail-line-dropped` | `Fail.*` |
| `sigsegv-unhandled`, `sigbus-unhandled`, `sigfpe-unhandled`, `sigill-unhandled`, `sigabrt-unhandled` (one signal dropped from the handler's list) | `Crash.Segv`, `Crash.Bus`, `Crash.Fpe`, `Crash.Ill`, `Crash.Abort` respectively |
| `program-failure-not-counted` | `ProgramFails.*` |
| `disabled-suite-not-counted` (the suite's `DISABLED_` prefix not read) | `DISABLED_Suite.*` |

`python3 sw/firmware/gtest/tally_selftest.py --mutants` at the head (rc 0, 65 s; GoogleTest 1.18.0;
`r3/gates/tally-mutants.log`):

```text
toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1 20260810', 'gtest': '1.18.0', 'gmock': '1.18.0'}
[ok] a passing test (the control): exit 0, tally 1/0, 1 tests, 0 failures
[ok] a failing assertion: exit 1, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a crash on SIGSEGV: exit -11, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] an abort: exit -6, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a crash on SIGBUS: exit -7, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a crash on SIGFPE: exit -8, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a crash on SIGILL: exit -4, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] exit(0) inside a test: exit 0, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a skipped test: exit 0, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] an uncaught exception: exit 1, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a disabled test: exit 0, tally 0/1, its tallies report 1 failure(s) across 0 checks
[ok] a disabled suite: exit 0, tally 0/1, its tallies report 1 failure(s) across 0 checks
[ok] a failure in a suite's set-up: exit 1, tally 1/2, its tallies report 2 failure(s) across 1 checks
[ok] a failure in a suite's tear-down: exit 1, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] a failure in the global environment: exit 1, tally 1/1, its tallies report 1 failure(s) across 1 checks
[ok] _exit(0) inside a test: exit 0, no tally, NOCOUNT: no tally, or a tally of nothing (the run did not finish)
[ok] no test selected: exit 0, tally 0/0, NOCOUNT: no tally, or a tally of nothing (the run did not finish)
[ok] a disabled test, GTEST_ALSO_RUN_DISABLED_TESTS=1 in the environment: exit 0, tally 0/1, its tallies report 1 failure(s) across 0 checks
tally self-test: 18 of 18 planted cases read as planted
[caught] skip-not-counted: Skip.* (tally checks 1 failures 0, want checks 1 failures 1); also SetUpFails.*
[caught] suite-failure-not-counted: SetUpFails.*, TearDownFails.* (tally checks 1 failures 1, want checks 1 failures 2)
[caught] crash-tally-passes: Crash.Segv, Crash.Abort, Crash.Bus, Crash.Fpe, Crash.Ill (tally checks 1 failures 0, want checks 1 failures 1)
[caught] crashed-test-not-counted: Crash.Segv, Crash.Abort, Crash.Bus, Crash.Fpe, Crash.Ill (tally checks 0 failures 1, want checks 1 failures 1)
[caught] early-exit-tally-passes: Exit.Zero (tally checks 1 failures 0, want checks 1 failures 1)
[caught] disabled-not-counted: Disabled.*, DISABLED_Suite.* (tally checks 0 failures 0, want checks 0 failures 1)
[caught] result-always-pass: Fail.*, Crash.Segv, Exit.Zero, Skip.*, Disabled.*, TearDownFails.*, ProgramFails.* (RESULT lines ['PASS'], want ['FAIL']); also Crash.Abort, Crash.Bus, Crash.Fpe, Crash.Ill, DISABLED_Suite.*, SetUpFails.*, Throw.*
[caught] tests-not-counted: Pass.*, Fail.* (tally checks 0 failures 0, want checks 1 failures 0); also ProgramFails.*, SetUpFails.*, Skip.*, TearDownFails.*, Throw.*
[caught] fail-line-dropped: Fail.* (no [FAIL] line names Fail.Expect); also Throw.*
[caught] no-atexit: Exit.Zero (not one listener tally line: [])
[caught] no-signal-handler: Crash.Segv, Crash.Abort, Crash.Bus, Crash.Fpe, Crash.Ill (not one listener tally line: [])
[caught] sigsegv-unhandled: Crash.Segv (not one listener tally line: [])
[caught] sigbus-unhandled: Crash.Bus (not one listener tally line: [])
[caught] sigfpe-unhandled: Crash.Fpe (not one listener tally line: [])
[caught] sigill-unhandled: Crash.Ill (not one listener tally line: [])
[caught] sigabrt-unhandled: Crash.Abort (not one listener tally line: [])
[caught] program-failure-not-counted: ProgramFails.* (tally checks 1 failures 0, want checks 1 failures 1)
[caught] disabled-suite-not-counted: DISABLED_Suite.* (tally checks 0 failures 0, want checks 0 failures 1)
listener defects: 18 of 18 caught
```

The same with GoogleTest 1.14.0 and gcc 13.3.0, the runner's packages, in the `ubuntu:24.04` image
(`r3/gates/tally-mutants-gcc13.log`, rc 0): `tally self-test: 18 of 18 planted cases read as
planted`, `listener defects: 18 of 18 caught`, each defect caught on the same cases. R506-2's
`tally_extra_plants.py`, unchanged, against the head: its six cases read as planted on the head's
listener, and each of its four defects now reddens the head's own planted cases
(`r3/gates/probe-r506-tally-extra.log`).

## 3. Port table: old check -> new test, with counts

The count unit changed: the hand-rolled tally counted assertions, the listener counts tests. Every
check's meaning is kept as an assertion carrying the same words, inside a test named after its
labelled step or scenario. Splits and merges, arm by arm:

| Arm | Before (unit: assertions) | After (unit: tests) | Split or merge |
|---|---:|---:|---|
| `model` | 134 (one `Checker`) | 14 | merged by group: one test per group of `tb/verilator/mbx/suite.hpp` (`Suite/MbxModelGroup.PassesOnTheModel/<Group>`), every check of the group an assertion inside it; the RTL bench still counts 134/179/13 at head as at base |
| `port` | 81 | 30 | merged by labelled step: P0 to P9, S0 to S3, D0 to D5, L0 to L9 (P5 to P9, S3, L9 new; P9 in round 2) |
| `adp` | 163 | 26 | merged by labelled step: A0 to A24, B1, C0 to C6, E0 to E5 (E5 split into 6 parameterised cases), F0 to F7 (A22 to A24 new) |
| `walk` | 320 (one `Checker`) | 41 | merged by cell: one test per walked Table 5.51 cell (`Table551/AdpWalkCell.Graded/<ROW_x_COL>`) and the scenario tests (P11 and the frame checks) |
| `entity` | 45 | 45 | one test per field per shipped config (`Fabric/EntityField.MatchesTheFabric/<field>`) |
| `lwsrp` | 13 | 1 | merged: one application for the run, as a boot has (lwSRP's timer list keeps every timer it was given; see `sw/firmware/gtest/README.md`, Not in this lane) |
| `unit` | 0 | 23 | new: the seams on GoogleMock and the MMIO platform |
| `rv32` | 1 | 1 | unchanged: a cross build, not a host test |
| `ctrl_nvm`, per shape | 42 checks | 71 tests (69 at a shape without a recorded vector) | kept by name: a check on both ports is two tests `Ports/NvmBoth.<check>/model` and `.../litespi` |
| `ctrl_nvm`, per shape, new | 0 | 16 | `test_nvm_more.cpp`, `test_nvm_codec.cpp` (`codec_loaded_prefix` in round 2), `test_nvm_flashmock.cpp` |
| `ctrl_nvm`, 1x1 shape, new | 0 | 5 | `test_nvm_shapes.cpp` (two doctored builds) and `test_nvm_litespi.cpp` |

### 3.1 ctrl `port` and `adp`: every check by its words

Generated from the base's `check()`, `check_eq()` and `bound()` call sites, each found at head by
its exact words.

#### `test_port_loop.c` -> `test_port_loop.cpp` (81 call sites)

| Check (its words at base) | GoogleTest test at head |
|---|---|
| P0 an arena one byte short is refused | `Pool.P0Refusals` |
| P0 a misaligned arena is refused | `Pool.P0Refusals` |
| P0 classes that do not grow are refused | `Pool.P0Refusals` |
| P0 an empty class is refused | `Pool.P0Refusals` |
| P0 the exact arena is accepted | `Pool.P0Refusals` |
| P1 four 24-byte blocks come from the 32-byte class, aligned | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 an exhausted class spills into the next larger one | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 a size no class holds is refused | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 a zero-byte allocation is refused | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 refusals are counted | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 the last block of the large class | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 then nothing is left | `Pool.P1ClassesExhaustionAndRefusals` |
| P1 every block is in use | `Pool.P1ClassesExhaustionAndRefusals` |
| P2 a released block is the next one handed out | `Pool.P2ReleaseAndBadFrees` |
| P2 a double free is refused and counted | `Pool.P2ReleaseAndBadFrees` |
| P2 a free into the middle of a block is refused | `Pool.P2ReleaseAndBadFrees` |
| P2 a free of a pointer the pool never handed out is refused | `Pool.P2ReleaseAndBadFrees` |
| P2 a free of NULL is a no-op | `Pool.P2ReleaseAndBadFrees` |
| P2 the high-water mark of the small class | `Pool.P2ReleaseAndBadFrees` |
| P3 calloc hands out a zeroed block, even a reused one | `Pool.P3CallocZeroesAndRefusesAWrap` |
| P3 calloc refuses a count times size that wraps to a small size | `Pool.P3CallocZeroesAndRefusesAWrap` |
| P4 shlan_malloc before the pool is bound refuses | `Pool.P4ShlanFunctionsDrawOnTheBoundPool` |
| P4 shlan_malloc and shlan_calloc draw on the bound pool | `Pool.P4ShlanFunctionsDrawOnTheBoundPool` |
| P4 shlan_free returns both blocks | `Pool.P4ShlanFunctionsDrawOnTheBoundPool` |
| S0 with no sink bound shlan_printf emits nothing | `DebugSink.S0NoSinkDiscardsAndCounts` |
| S0 and counts the discard | `DebugSink.S0NoSinkDiscardsAndCounts` |
| S1 shlan_printf reaches the bound sink formatted | `DebugSink.S1FormattedToTheSink` |
| S2 a line over the buffer is truncated to it | `DebugSink.S2TruncatedToTheLine` |
| S2 and the sink receives that many bytes | `DebugSink.S2TruncatedToTheLine` |
| S2 in one call | `DebugSink.S2TruncatedToTheLine` |
| S2 the truncation is counted | `DebugSink.S2TruncatedToTheLine` |
| D0 mbx_open accepts the model's contract | `Driver.D0RxRecordByteForByte` |
| D0 the model commits a DISCOVER | `Driver.D0RxRecordByteForByte` |
| D0 mbx_rx_take returns it | `Driver.D0RxRecordByteForByte` |
| D0 byte for byte, with its length, interface and arrival | `Driver.D0RxRecordByteForByte` |
| D0 the release moved RX_TAIL to RX_HEAD | `Driver.D0RxRecordByteForByte` |
| D0 an empty ring | `Driver.D0RxRecordByteForByte` |
| D1 a record with the wrong KIND is refused | `Driver.D1MalformedRecordResynchronises` |
| D1 and the ring is resynchronised to RX_HEAD, the next record included | `Driver.D1MalformedRecordResynchronises` |
| D1 bad channel | `Driver.D1MalformedRecordResynchronises` |
| D2 a frame becomes a TX record | `Driver.D2TxRecordAndRefusals` |
| D2 and leaves the merge byte for byte | `Driver.D2TxRecordAndRefusals` |
| D2 a 13-byte frame is refused | `Driver.D2TxRecordAndRefusals` |
| D2 a frame over max_frame_bytes is refused | `Driver.D2TxRecordAndRefusals` |
| D2 an unknown interface is refused | `Driver.D2TxRecordAndRefusals` |
| D3 a held merge fills the ring to its last whole record | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` |
| D3 once drained every record leaves | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` |
| D3 and none was refused | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` |
| D3 ACMP, ACMP, AECP committed by the driver behind a held merge leave in that order | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` |
| D4 a LINK event | `Driver.D4EveryEventTypeDecoded` |
| D4 a GM event with the identity and domain | `Driver.D4EveryEventTypeDecoded` |
| D4 a TIMER event with slot, tag and deadline | `Driver.D4EveryEventTypeDecoded` |
| D4 a cancelled timer posts nothing | `Driver.D4EveryEventTypeDecoded` |
| D4 TICK events count the centiseconds | `Driver.D4EveryEventTypeDecoded` |
| D5 the grandmaster read is coherent | `Driver.D5CoherentGrandmasterRead` |
| L0 bindings fit their tables | `LoopBring.L0BindingsFitTheirTables` |
| L0 an unknown channel cannot be bound | `LoopBring.L0BindingsFitTheirTables` |
| L1 ctrl_loop_open brings the mailbox up | `LoopBring.L1OpenOrder` |
| L1 OWN_EID is written before any channel opens | `LoopBring.L1OpenOrder` |
| L1 only the bound channel opens | `LoopBring.L1OpenOrder` |
| L1 the tick starts because a centisecond consumer is bound | `LoopBring.L1OpenOrder` |
| L1 IRQ_ENABLE holds the bound channel and the event ring | `LoopBring.L1OpenOrder` |
| L2 a pass takes at most CTRL_LOOP_RX_PER_PASS records of a channel | `Loop.L2PerPassRxBound` |
| L2 and polls every module once | `Loop.L2PerPassRxBound` |
| L2 the rest follow in later passes | `Loop.L2PerPassRxBound` |
| L3 a pass takes at most CTRL_LOOP_EVENTS_PER_PASS events | `Loop.L3PerPassEventBound` |
| L3 the rest follow in the next pass | `Loop.L3PerPassEventBound` |
| L4 (a late firmware: the ring is full while three ticks pass) | `Loop.L4TickFanOut` |
| L4 every centisecond reaches the first consumer | `Loop.L4TickFanOut` |
| L4 and the second | `Loop.L4TickFanOut` |
| L4 in registration order, tick by tick (a b a b a b) | `Loop.L4TickFanOut` |
| L5 a malformed record is counted, not handed out | `Loop.L5MalformedRecordCounted` |
| L5 and no handler saw it | `Loop.L5MalformedRecordCounted` |
| L6 a pass after which a module still owes output asks for the next pass at once | `Loop.L6OwedOutputKeepsPassing` |
| L6 a pass that handled nothing and owes nothing lets the loop sleep | `Loop.L6OwedOutputKeepsPassing` |
| L7 every one of 40 coalesced centiseconds reaches the consumer | `Loop.L7TickSlices` |
| L7 at most CTRL_LOOP_TICKS_PER_PASS of them per pass | `Loop.L7TickSlices` |
| L7 and the loop keeps passing until the last is dispatched | `Loop.L7TickSlices` |
| L8 (centiseconds are carried when the second TICK record is posted, alone in the ring) | `Loop.L8TickRecordWhileCarried` |
| L8 a TICK record taken while centiseconds are carried adds to them: all 41 reach the consumer | `Loop.L8TickRecordWhileCarried` |
| L8 and none is left owed | `Loop.L8TickRecordWhileCarried` |

81 of 81 literal call sites found at head by their words, and 0 formatted at run time mapped by hand.

#### `test_adp.c` -> `test_adp.cpp` (121 call sites)

| Check (its words at base) | GoogleTest test at head |
|---|---|
| A0 enabled with the link down: DOWN (5.6.3.5.1) | `AdpCore.A0toA2Schedule` |
| A0 and no timer | `AdpCore.A0toA2Schedule` |
| A0 LINK_UP: DELAY with a 0..4 s draw (5.6.3.5.3) | `AdpCore.A0toA2Schedule` |
| A1 TMR_DELAY: ENTITY_AVAILABLE, WAITING, TMR_ADVERTISE 5 s (5.6.3.5.9) | `AdpCore.A0toA2Schedule` |
| A1 valid_time 10, control_data_length 56 | `AdpCore.A0toA2Schedule` |
| A1 the first available_index is 0 | `AdpCore.A0toA2Schedule` |
| A1 available_index is incremented after the send (6.2.2.15) | `AdpCore.A0toA2Schedule` |
| A2 the next cycle carries index 1 and the grandmaster sampled at build | `AdpCore.A0toA2Schedule` |
| A2 GM_CHANGE in WAITING re-advertises (5.6.3.5.7) | `AdpCore.A0toA2Schedule` |
| A2 with the new current_configuration_index (6.2.2.18) | `AdpCore.A0toA2Schedule` |
| A2 and the entity's identify_control_index (6.2.2.19) | `AdpCore.A0toA2Schedule` |
| A3 enabled with the link up: DELAY with a 0..2 s draw (5.6.3.5.2) | `AdpCore.A3toA5DiscoverAndDiscard` |
| A3 RCV_ADP_DISCOVER in DELAY is ignored (Table 5.51) | `AdpCore.A3toA5DiscoverAndDiscard` |
| A4 a foreign DISCOVER, an AVAILABLE and a truncated ADPDU are discarded (5.6.3.1) | `AdpCore.A3toA5DiscoverAndDiscard` |
| A4 and leave WAITING alone | `AdpCore.A3toA5DiscoverAndDiscard` |
| A4 a DISCOVER for this entity stops TMR_ADVERTISE and enters DELAY (5.6.3.5.4) | `AdpCore.A3toA5DiscoverAndDiscard` |
| A5 an expiry with no timer running is a stray, counted | `AdpCore.A3toA5DiscoverAndDiscard` |
| A5 and sends nothing | `AdpCore.A3toA5DiscoverAndDiscard` |
| A6 a refused send keeps ENTITY_AVAILABLE owed in DELAY | `AdpCore.A6toA8DeferredSends` |
| A6 a poll without room retries and keeps it | `AdpCore.A6toA8DeferredSends` |
| A6 a poll with room sends it and completes 5.6.3.5.9 | `AdpCore.A6toA8DeferredSends` |
| A7 a link loss drops an owed ENTITY_AVAILABLE and departs nothing (5.6.3.5.10) | `AdpCore.A6toA8DeferredSends` |
| A8 SHUTDOWN with no room keeps ENTITY_DEPARTING owed, index reset | `AdpCore.A6toA8DeferredSends` |
| A8 a link loss does not drop it; the next poll sends it with the index current at SHUTDOWN | `AdpCore.A6toA8DeferredSends` |
| A8 SHUTDOWN in DOWN sends nothing (Table 5.51) | `AdpCore.A6toA8DeferredSends` |
| A10 the first ENTITY_AVAILABLE carries 0 | `AdpCore.A10toA14DepartingIndex` |
| A10 the second carries 1 | `AdpCore.A10toA14DepartingIndex` |
| A10 SHUTDOWN is taken in WAITING | `AdpCore.A10toA14DepartingIndex` |
| A10 SHUTDOWN in WAITING, sent at once: ENTITY_DEPARTING carries the current index, 2 | `AdpCore.A10toA14DepartingIndex` |
| A11 the first ENTITY_AVAILABLE after a restart carries 0 | `AdpCore.A10toA14DepartingIndex` |
| A12 SHUTDOWN is taken in DELAY | `AdpCore.A10toA14DepartingIndex` |
| A12 SHUTDOWN in DELAY, sent at once: ENTITY_DEPARTING carries the current index, 1 | `AdpCore.A10toA14DepartingIndex` |
| A13 SHUTDOWN with no room leaves ENTITY_DEPARTING owed | `AdpCore.A10toA14DepartingIndex` |
| A13 sent from a later poll, it carries the index current at SHUTDOWN, 2 | `AdpCore.A10toA14DepartingIndex` |
| A13 and the restart's first ENTITY_AVAILABLE carries 0 | `AdpCore.A10toA14DepartingIndex` |
| A14 available_index 0xFFFFFFFF goes on the wire | `AdpCore.A10toA14DepartingIndex` |
| A14 the next ENTITY_AVAILABLE carries 0, modulo 2^32 | `AdpCore.A10toA14DepartingIndex` |
| A14 SHUTDOWN after the wrap: ENTITY_DEPARTING carries the current index, 1 | `AdpCore.A10toA14DepartingIndex` |
| A15 advertised once, SHUTDOWN behind a full ring: ENTITY_DEPARTING owed with index 1 | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 the restart runs while it is owed: DELAY, the startup TMR_DELAY armed | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 that TMR_DELAY expires before the ring has room: ENTITY_AVAILABLE owed behind it, no timer | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 a poll without room keeps both owed | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 with room, the next poll sends the owed ENTITY_DEPARTING first, with its SHUTDOWN index 1 | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 and the one after it the restart's ENTITY_AVAILABLE, with index 0 | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 then WAITING with TMR_ADVERTISE armed 5 s, available_index 1 | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 and nothing stranded: nothing owed, a further poll sends nothing | `AdpCore.A15OwedDepartingAcrossARestart` |
| A15 the schedule runs on: the next ENTITY_AVAILABLE carries 1 | `AdpCore.A15OwedDepartingAcrossARestart` |
| A16 a SHUTDOWN while one is owed queues its own ENTITY_DEPARTING and drops the owed AVAILABLE | `AdpCore.A16SecondShutdownQueuesItsOwn` |
| A16 each leaves in order with its SHUTDOWN's index: 1, then 0 (that run sent nothing) | `AdpCore.A16SecondShutdownQueuesItsOwn` |
| A16 the restart running meanwhile is untouched: DELAY, its TMR_DELAY armed | `AdpCore.A16SecondShutdownQueuesItsOwn` |
| A16 its ENTITY_AVAILABLE, with index 0, leaves at its TMR_DELAY expiry; WAITING | `AdpCore.A16SecondShutdownQueuesItsOwn` |
| A17 room back and TMR_DELAY expiring before a poll: the ENTITY_AVAILABLE does not pass the owed DEPARTING | `AdpCore.A17RoomBackBeforeAPoll` |
| A17 the polls then send DEPARTING with index 1 and AVAILABLE with index 0, in that order | `AdpCore.A17RoomBackBeforeAPoll` |
| A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING, index 1 | `AdpCore.A18LinkLossKeepsTheOwedDeparting` |
| A18 the link's return starts a new run with the ENTITY_DEPARTING still owed (5.6.3.5.3) | `AdpCore.A18LinkLossKeepsTheOwedDeparting` |
| A18 a link loss with that run's ENTITY_AVAILABLE owed drops the AVAILABLE and keeps the DEPARTING | `AdpCore.A18LinkLossKeepsTheOwedDeparting` |
| A18 with room the ENTITY_DEPARTING leaves, index 1 | `AdpCore.A18LinkLossKeepsTheOwedDeparting` |
| A18 then the new run's ENTITY_AVAILABLE, index 0, at its TMR_DELAY expiry; WAITING | `AdpCore.A18LinkLossKeepsTheOwedDeparting` |
| A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed, no timer started | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` |
| A19 so does an ENTITY_DISCOVER | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` |
| A19 and a stray expiry, which is counted | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` |
| A19 the next poll with room sends it, index 0, then WAITING with TMR_ADVERTISE 5 s | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` |
| A20 a link loss drops the owed ENTITY_AVAILABLE at once, before any poll (5.6.3.5.10) | `AdpCore.A20LinkLossDropsTheOwedAvailable` |
| A20 after the link's return a poll sends nothing: the new run waits for its TMR_DELAY (5.6.3.5.3) | `AdpCore.A20LinkLossDropsTheOwedAvailable` |
| A20 whose expiry sends the ENTITY_AVAILABLE, index 0; WAITING | `AdpCore.A20LinkLossDropsTheOwedAvailable` |
| A21 a second SHUTDOWN takes the last place: two owed, the oldest with index 1, none coalesced | `AdpCore.A21DepartingCapacity` |
| A21 the next SHUTDOWN is coalesced into the queued one and counted; its run's owed AVAILABLE is dropped | `AdpCore.A21DepartingCapacity` |
| A21 and so are 100000 more, each counted, the two owed unchanged | `AdpCore.A21DepartingCapacity` |
| A21 with room the wire carries DEPARTING 1, then one DEPARTING 0, and nothing more is owed | `AdpCore.A21DepartingCapacity` |
| A21 then the running restart's ENTITY_AVAILABLE, index 0, at its TMR_DELAY expiry; WAITING | `AdpCore.A21DepartingCapacity` |
| A9 every startup draw is 0..2 s and every other draw 0..4 s | `AdpCore.A9DrawKinds` |
| A9 the two kinds are distinct: the 0..4 s draws pass 2 s | `AdpCore.A9DrawKinds` |
| A9 and both reach near their maxima | `AdpCore.A9DrawKinds` |
| B0 the app starts on the model | `the set-up of every adapter test (boot(): B1, C0 to C6, E0 to E5, F0 to F7)` |
| B1 the model reaches WAITING | `AdpAdapter.B1StaleTagDiscarded` |
| B1 an expiry of the arm a GM_CHANGE replaced is discarded by its tag | `AdpAdapter.B1StaleTagDiscarded` |
| B1 and the replacing TMR_DELAY stands | `AdpAdapter.B1StaleTagDiscarded` |
| C0 LINK_UP -> TMR_DELAY armed, one pass | `AdpLatency.C0toC6EveryResponsePath` |
| C0 LINK_UP -> TMR_DELAY armed | `AdpLatency.C0toC6EveryResponsePath` |
| C1 TMR_DELAY -> ENTITY_AVAILABLE committed and TMR_ADVERTISE armed, one pass | `AdpLatency.C0toC6EveryResponsePath` |
| C1 TMR_DELAY -> ENTITY_AVAILABLE, TMR_ADVERTISE | `AdpLatency.C0toC6EveryResponsePath` |
| C2 RCV_ADP_DISCOVER -> TMR_DELAY armed, one pass | `AdpLatency.C0toC6EveryResponsePath` |
| C2 RCV_ADP_DISCOVER -> TMR_DELAY armed | `AdpLatency.C0toC6EveryResponsePath` |
| C3 TMR_ADVERTISE -> TMR_DELAY armed, one pass | `AdpLatency.C0toC6EveryResponsePath` |
| C3 TMR_ADVERTISE -> TMR_DELAY armed | `AdpLatency.C0toC6EveryResponsePath` |
| C4 GM_CHANGE -> TMR_DELAY armed, one pass | `AdpLatency.C0toC6EveryResponsePath` |
| C4 GM_CHANGE -> TMR_DELAY armed | `AdpLatency.C0toC6EveryResponsePath` |
| C5 LINK_DOWN -> timer cancelled, one pass | `AdpLatency.C0toC6EveryResponsePath` |
| C5 LINK_DOWN -> timer cancelled | `AdpLatency.C0toC6EveryResponsePath` |
| C6 SHUTDOWN -> ENTITY_DEPARTING committed | `AdpLatency.C0toC6EveryResponsePath` |
| C6 SHUTDOWN -> ENTITY_DEPARTING committed | `AdpLatency.C0toC6EveryResponsePath` |
| E0 LINK_UP takes the machine to DELAY | `AdpOwed.E0toE3PendingWake` |
| E0 TMR_DELAY expires behind a full transmit ring: ENTITY_AVAILABLE is owed | `AdpOwed.E0toE3PendingWake` |
| E0 and nothing else can wake the core: no RX, no event, TICK off | `AdpOwed.E0toE3PendingWake` |
| E1 the loop does not sleep while a frame is owed | `AdpOwed.E0toE3PendingWake` |
| E2 once the ring drains, the next pass sends the owed ENTITY_AVAILABLE | `AdpOwed.E0toE3PendingWake` |
| E2 and restarts its timer: TMR_ADVERTISE armed 5 s after the frame left, the machine in WAITING | `AdpOwed.E0toE3PendingWake` |
| E3 then the loop sleeps, and the TMR_ADVERTISE expiry wakes it | `AdpOwed.E0toE3PendingWake` |
| E4 advertised once: the first ENTITY_AVAILABLE left with index 0, the machine in WAITING | `AdpOwed.E4OwedDepartingWake` |
| E4 SHUTDOWN behind the full ring leaves ENTITY_DEPARTING owed with index 1; the restart arms TMR_DELAY | `AdpOwed.E4OwedDepartingWake` |
| E4 its TMR_DELAY expires before the ring drains: ENTITY_AVAILABLE owed behind the DEPARTING, no arm | `AdpOwed.E4OwedDepartingWake` |
| E4 the loop does not sleep while both are owed | `AdpOwed.E4OwedDepartingWake` |
| E4 once the ring drains: ENTITY_DEPARTING with index 1, then ENTITY_AVAILABLE with index 0 | `AdpOwed.E4OwedDepartingWake` |
| E4 then WAITING with TMR_ADVERTISE armed 5 s after the ENTITY_AVAILABLE left | `AdpOwed.E4OwedDepartingWake` |
| E4 nothing stranded: no frame owed, the loop sleeps, and the TMR_ADVERTISE expiry wakes it | `AdpOwed.E4OwedDepartingWake` |
| F0 the F0 composition with a centisecond consumer comes up | `AdpBacklog.F0toF7FullBacklogs` |
| F0 the event ring is full, ADP's TMR_DELAY expiry its 16th record | `AdpBacklog.F0toF7FullBacklogs` |
| F0 the receive ring is full: it refuses the next frame | `AdpBacklog.F0toF7FullBacklogs` |
| F0 30 centiseconds wait coalesced behind the full event ring | `AdpBacklog.F0toF7FullBacklogs` |
| F0 and holds no more records than A1 assumes | `AdpBacklog.F0toF7FullBacklogs` |
| F1 events first: no event-ring access follows a receive-ring access in a pass | `AdpBacklog.F0toF7FullBacklogs` |
| F2 all 16 event records are taken by pass CTRL_LOOP_EVT_PASSES | `AdpBacklog.F0toF7FullBacklogs` |
| F2 the TMR_DELAY expiry, posted 16th, has its ENTITY_AVAILABLE committed in the pass that takes it | `AdpBacklog.F0toF7FullBacklogs` |
| F2 within ADP_MBX_EVT_ACCESSES of the backlog's first access | `AdpBacklog.F0toF7FullBacklogs` |
| F3 the receive backlog is taken by pass ceil(records / CTRL_LOOP_RX_PER_PASS) | `AdpBacklog.F0toF7FullBacklogs` |
| F3 within CTRL_LOOP_RX_PASSES(256) passes and ADP_MBX_RX_ACCESSES accesses | `AdpBacklog.F0toF7FullBacklogs` |
| F4 every coalesced centisecond reaches the consumer | `AdpBacklog.F0toF7FullBacklogs` |
| F4 at most CTRL_LOOP_TICKS_PER_PASS of them in a pass | `AdpBacklog.F0toF7FullBacklogs` |
| F5 the costliest pass of the backlog | `AdpBacklog.F0toF7FullBacklogs` |
| F6 the loop passes until the backlog is gone, then may sleep | `AdpBacklog.F0toF7FullBacklogs` |
| F7 the backlog left exactly one frame, the ENTITY_AVAILABLE | `AdpBacklog.F0toF7FullBacklogs` |
| E5 %u SHUTDOWNs behind a full ring, %s: five checks per case (owed, the AVAILABLE behind, the pass it is committed in, the wire, WAITING after), for 1, 2 and 64 SHUTDOWNs with the expiry before and after the room | `Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/0 to /5 (one test per case)` |

121 of 121 literal call sites found at head by their words, and 1 formatted at run time mapped by hand.

### 3.2 ctrl_nvm: every check by name

Generated from the base's `BOOT_CHECKS`/`WRITE_CHECKS` and their ports, each found at head by name.

| Check at base | Ports at base | GoogleTest test(s) at head | Tests |
|---|---|---|---:|
| `blank_boot` | model, litespi | `Ports/NvmBoth.blank_boot/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `golden_restore` | model, litespi | `Ports/NvmBoth.golden_restore/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `erased_records` | model, litespi | `Ports/NvmBoth.erased_records/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `newer_wins` | model, litespi | `Ports/NvmBoth.newer_wins/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `torn_falls_back` | model, litespi | `Ports/NvmBoth.torn_falls_back/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `both_torn_blank` | model, litespi | `Ports/NvmBoth.both_torn_blank/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `verdict_parity` | model, litespi | `Ports/NvmBoth.verdict_parity/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `wrong_version_falls_back` | model, litespi | `Ports/NvmBoth.wrong_version_falls_back/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `read_flip_at_stage` | model | `NvmModel.read_flip_at_stage` (test_nvm_boot.cpp) | 1 |
| `read_flip_boot` | model | `NvmModel.read_flip_boot` (test_nvm_boot.cpp) | 1 |
| `read_alias_at_stage` | model | `NvmModel.read_alias_at_stage` (test_nvm_boot.cpp) | 1 |
| `read_fail_boot` | model | `NvmModel.read_fail_boot` (test_nvm_boot.cpp) | 1 |
| `fallback_restage` | model | `NvmModel.fallback_restage` (test_nvm_boot.cpp) | 1 |
| `apply_fault_rolls_back` | model, litespi | `Ports/NvmBoth.apply_fault_rolls_back/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `settle_fault_rolls_back` | model, litespi | `Ports/NvmBoth.settle_fault_rolls_back/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `binding_walk` | model, litespi | `Ports/NvmBoth.binding_walk/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `rollback_fault_closes` | model, litespi | `Ports/NvmBoth.rollback_fault_closes/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `model_unproven_closes` | model, litespi | `Ports/NvmBoth.model_unproven_closes/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `refused_keeps_default` | model, litespi | `Ports/NvmBoth.refused_keeps_default/model`, `.../litespi` (test_nvm_boot.cpp) | 2 |
| `first_commit_bytes` | model, litespi | `Ports/NvmBoth.first_commit_bytes/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `change_commit_bytes` | model, litespi | `Ports/NvmBoth.change_commit_bytes/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `debounce` | model, litespi | `Ports/NvmBoth.debounce/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `unchanged_no_erase` | model, litespi | `Ports/NvmBoth.unchanged_no_erase/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `failed_commit_not_skipped` | model, litespi | `Ports/NvmBoth.failed_commit_not_skipped/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `media_failures` | model, litespi | `Ports/NvmBoth.media_failures/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `recovers_after_failure` | model, litespi | `Ports/NvmBoth.recovers_after_failure/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `dr2c_unchanged_set` | model, litespi | `Ports/NvmBoth.dr2c_unchanged_set/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `dr2c_console` | model, litespi | `Ports/NvmBoth.dr2c_console/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `verify_tail` | model, litespi | `Ports/NvmBoth.verify_tail/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `blankcheck_tail` | model, litespi | `Ports/NvmBoth.blankcheck_tail/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `media_verdicts` | model | `NvmModel.media_verdicts` (test_nvm_write.cpp) | 1 |
| `refused_slot_kept` | model, litespi | `Ports/NvmBoth.refused_slot_kept/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `service_bound` | model, litespi | `Ports/NvmBoth.service_bound/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `powercut` | model, litespi | `Ports/NvmBoth.powercut/model`, `.../litespi` (test_nvm_write.cpp) | 2 |
| `vector_round_trip` | model, litespi | `Ports/NvmBoth.vector_round_trip/model`, `.../litespi` (test_nvm_vector.cpp) | 2 |
| `time_base` | litespi | `NvmLitespi.time_base` (test_nvm_write.cpp) | 1 |
| `port_clock` | litespi | `NvmLitespi.port_clock` (test_nvm_write.cpp) | 1 |
| `port_stall` | litespi | `NvmLitespi.port_stall` (test_nvm_write.cpp) | 1 |
| `port_deadline` | litespi | `NvmLitespi.port_deadline` (test_nvm_write.cpp) | 1 |
| `port_guard` | litespi | `NvmLitespi.port_guard` (test_nvm_write.cpp) | 1 |
| `authority_unknown` | model | `NvmModel.authority_unknown` (test_nvm_write.cpp) | 1 |
| `read_disagreement` | model | `NvmModel.read_disagreement` (test_nvm_write.cpp) | 1 |

42 checks at base, 42 found at head by name, 71 tests.

Checks added at head (#665 lane FT), each with a planted defect of its own:

| Check | GoogleTest test(s) | Tests |
|---|---|---:|
| `capture_window_edges` | `Ports/NvmBoth.capture_window_edges/model`, `.../litespi` (test_nvm_more.cpp) | 2 |
| `change_unknown_record` | `NvmModel.change_unknown_record` (test_nvm_more.cpp) | 1 |
| `codec_loaded_prefix` | `NvmCodec.codec_loaded_prefix` (test_nvm_codec.cpp) | 1 |
| `codec_lookups` | `NvmCodec.codec_lookups` (test_nvm_codec.cpp) | 1 |
| `codec_parity` | `NvmCodec.codec_parity` (test_nvm_codec.cpp) | 1 |
| `codec_room` | `NvmCodec.codec_room` (test_nvm_codec.cpp) | 1 |
| `console_commit_unchanged` | `Ports/NvmBoth.console_commit_unchanged/model`, `.../litespi` (test_nvm_more.cpp) | 2 |
| `first_commit_no_blank_slot` | `Ports/NvmBoth.first_commit_no_blank_slot/model`, `.../litespi` (test_nvm_more.cpp) | 2 |
| `long_container_reads` | `NvmModel.long_container_reads` (test_nvm_more.cpp) | 1 |
| `nothing_to_save` | `Ports/NvmBoth.nothing_to_save/model`, `.../litespi` (test_nvm_more.cpp) | 2 |
| `port_drain_deadline` | `NvmLitespiPort.port_drain_deadline` (test_nvm_litespi.cpp) | 1 |
| `port_read_range` | `NvmLitespiPort.port_read_range` (test_nvm_litespi.cpp) | 1 |
| `port_write_refusals` | `NvmLitespiPort.port_write_refusals` (test_nvm_litespi.cpp) | 1 |
| `reads_agree_in_digest_not_length` | `NvmFlashMock.reads_agree_in_digest_not_length` (test_nvm_flashmock.cpp) | 1 |
| `reads_differ_in_verdict` | `NvmFlashMock.reads_differ_in_verdict` (test_nvm_flashmock.cpp) | 1 |
| `settle_after_the_last_record` | `NvmModel.settle_after_the_last_record` (test_nvm_shapes.cpp) | 1 |
| `shape_mismatch_disables_persistence` | `NvmModel.shape_mismatch_disables_persistence` (test_nvm_shapes.cpp) | 1 |

## 4. Mutation arms and the test that kills each

Both campaigns at the round-3 head `6ca834a7`, rc 0 (`r3/gates/ctrl-self.log`, `r3/gates/nvm-self.log`):

- ctrl: `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <pin>`: `mutants: 76 of 76 caught`, both lwSRP pin arms refusing, `test_ctrl_firmware: PASS`. A defect is
  caught only when its arm fails AND a `[FAIL]` line names the test with the check's words; a broken
  build or only other tests failing is an escape. The 51 base defects are all still killed, now by the
  named GoogleTest test; the 25 defects added for the new checks are killed too (round 2's two on
  P9: `pool-follows-a-cut-free-list`, killed by the crash report that names P9, and
  `pool-cut-list-refuses-outright`), `rx-no-resync` gained a `unit`-arm kill (D7), and the `unit` arm
  joined the campaign.
- ctrl_nvm adds 24 defects to the base's 82 (one or more per new check, and `codec_parity` and the two
  read-agreement checks named on existing defects that must also redden them; round 2's two are
  `short_prefix_read_on` and `short_prefix_as_len`, and round 3's four are `header_guard_early`,
  `header_guard_late`, `payload_guard_early` and `payload_guard_late`, all on `codec_loaded_prefix`).
- ctrl_nvm: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`: `saved-state store gate (#665 F1): OK across 5 shape(s), 434 tests, and all 106 planted defects reddened`. `unnamed_checks`
  proves every check of the suite is named by at least one defect before any is planted.

One test was strengthened because its planted defect showed it could not fail:
`NvmLitespiPort.port_drain_deadline` now bounds the drain below LS_POLL_MAX, so a drain bounded by
its poll count alone (`drain_deadline_ignored`) fails it.

#### ctrl: `sw/firmware/ctrl/test/ctrl_mutants.py` (76 defects)

| Defect | Planted in | Arm | Test that must fail, on these words |
|---|---|---|---|
| `departing-keeps-index` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/` on "available_index" |
| `departing-sends-zero` | `adp/adp.c` | adp | `AdpCore.A10toA14DepartingIndex` on "A10 SHUTDOWN in WAITING" |
| `available-replaces-owed-departing` | `adp/adp.c` | adp | `AdpCore.A15OwedDepartingAcrossARestart` on "A15 with room, the next poll sends the owed ENTITY_DEPARTING first" |
| `available-passes-owed-departing` | `adp/adp.c` | adp | `AdpCore.A17RoomBackBeforeAPoll` on "A17 room back and TMR_DELAY expiring before a poll" |
| `second-departing-dropped` | `adp/adp.c` | adp | `AdpCore.A16SecondShutdownQueuesItsOwn` on "A16 a SHUTDOWN while one is owed queues its own" |
| `second-shutdown-overwrites-index` | `adp/adp.c` | adp | `AdpCore.A16SecondShutdownQueuesItsOwn` on "A16 a SHUTDOWN while one is owed queues its own" |
| `link-loss-drops-owed-departing` | `adp/adp.c` | adp | `AdpCore.A18LinkLossKeepsTheOwedDeparting` on "A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING" |
| `gm-change-drops-owed-available` | `adp/adp.c` | adp | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` on "A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed" |
| `discover-drops-owed-available` | `adp/adp.c` | adp | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` on "A19 so does an ENTITY_DISCOVER" |
| `stray-expiry-drops-owed-available` | `adp/adp.c` | adp | `AdpCore.A19IgnoredInputsKeepTheOwedAvailable` on "A19 and a stray expiry, which is counted" |
| `link-loss-keeps-owed-available` | `adp/adp.c` | adp | `AdpCore.A20LinkLossDropsTheOwedAvailable` on "A20 a link loss drops the owed ENTITY_AVAILABLE at once" |
| `departing-queue-unbounded` | `adp/adp.c` | adp | `Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/` on "E5 64 SHUTDOWNs behind a full ring, expiry taken before the room: the ENTITY_AVAILABLE is committed" |
| `coalesced-departing-uncounted` | `adp/adp.c` | adp | `AdpCore.A21DepartingCapacity` on "A21 the next SHUTDOWN is coalesced into the queued one and counted" |
| `coalesce-drops-queued-departing` | `adp/adp.c` | adp | `AdpCore.A21DepartingCapacity` on "A21 the next SHUTDOWN is coalesced into the queued one and counted" |
| `coalesce-overwrites-oldest-index` | `adp/adp.c` | adp | `AdpCore.A21DepartingCapacity` on "A21 the next SHUTDOWN is coalesced into the queued one and counted" |
| `own-discover-discarded` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_own_eid_x_WAITING` on "RCV_ADP_DISCOVER(own eid) x WAITING" |
| `down-answers-discover` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_eid_0_x_DOWN` on "RCV_ADP_DISCOVER(eid 0) x DOWN" |
| `link-down-departs` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/LINK_DOWN_x_WAITING` on "LINK_DOWN x WAITING: frames committed" |
| `gm-change-ignored` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING` on "GM_CHANGE x WAITING" |
| `delay-ignores-link-down` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/LINK_DOWN_x_DELAY_timer_armed` on "LINK_DOWN x DELAY" |
| `shutdown-in-down-departs` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/SHUTDOWN_x_DOWN` on "SHUTDOWN x DOWN" |
| `advertise-expiry-skips-delay` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/TMR_ADVERTISE_x_WAITING` on "TMR_ADVERTISE x WAITING" |
| `advertise-period-wrong` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/TMR_DELAY_x_DELAY_timer_armed` on "TMR_DELAY x DELAY(timer armed)" |
| `link-up-draws-startup-kind` | `adp/adp.c` | walk | `Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN` on "LINK_UP x DOWN" |
| `draw-kinds-merged` | `adp/adp.c` | adp | `AdpCore.A9DrawKinds` on "A9 every startup draw" |
| `foreign-discover-answered` | `adp/adp.c` | adp | `AdpCore.A3toA5DiscoverAndDiscard` on "A4 a foreign DISCOVER" |
| `frame-misses-config-index` | `adp/adp.c` | walk | `AdpWalk.P11ConfigurationIndexBytes` on "P11" |
| `stale-tag-accepted` | `adp/adp_mbx.c` | adp | `AdpAdapter.B1StaleTagDiscarded` on "B1 an expiry of the arm a GM_CHANGE replaced" |
| `latency-extra-read` | `adp/adp_mbx.c` | adp | `AdpLatency.C0toC6EveryResponsePath` on "C0 LINK_UP -> TMR_DELAY armed" |
| `pool-free-leaks` | `port/ctrl_pool.c` | port | `Pool.P2ReleaseAndBadFrees` on "P2 a released block" |
| `calloc-overflow-unchecked` | `port/ctrl_pool.c` | port | `Pool.P3CallocZeroesAndRefusesAWrap` on "P3 calloc refuses" |
| `pool-double-free-accepted` | `port/ctrl_pool.c` | port | `Pool.P2ReleaseAndBadFrees` on "P2 a double free" |
| `debug-truncation-uncounted` | `port/ctrl_debug.c` | port | `DebugSink.S2TruncatedToTheLine` on "S2 the truncation" |
| `tick-count-ignored` | `loop/ctrl_loop.c` | port | `Loop.L4TickFanOut` on "L4 every centisecond" |
| `rx-pass-unbounded` | `loop/ctrl_loop.c` | port | `Loop.L2PerPassRxBound` on "L2 a pass takes at most" |
| `poll-owes-nothing` | `adp/adp_mbx.c` | adp | `AdpOwed.E0toE3PendingWake` on "E1 the loop does not sleep while a frame is owed" |
| `events-halved` | `loop/ctrl_loop.c` | adp | `AdpBacklog.F0toF7FullBacklogs` on "F2 all 16 event records are taken by pass" |
| `rx-before-events` | `loop/ctrl_loop.c` | adp | `AdpBacklog.F0toF7FullBacklogs` on "F1 events first" |
| `carried-ticks-overwritten` | `loop/ctrl_loop.c` | port | `Loop.L8TickRecordWhileCarried` on "L8 a TICK record taken while centiseconds are carried" |
| `tick-slice-unbounded` | `loop/ctrl_loop.c` | port | `Loop.L7TickSlices` on "L7 at most CTRL_LOOP_TICKS_PER_PASS" |
| `owed-ticks-let-it-sleep` | `loop/ctrl_loop.c` | port | `Loop.L7TickSlices` on "L7 and the loop keeps passing" |
| `filter-opened-before-eid` | `loop/ctrl_loop.c` | port | `LoopBring.L1OpenOrder` on "L1 OWN_EID is written before" |
| `rx-no-resync` | `mbx/mbx.c` | port | `Driver.D1MalformedRecordResynchronises` on "D1 and the ring is resynchronised"; `Records/DriverMalformed.D7RefusedAndResynchronised/` on "and the ring is resynchronised to RX_HEAD" (unit) |
| `tx-overfills` | `mbx/mbx.c` | port | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` on "D3 a held merge fills the ring" |
| `lanes-big-endian` | `mbx/mbx_wire.h` | model | `Suite/MbxModelGroup.PassesOnTheModel/` on "F1 frame byte k is ring word" |
| `frame-sources-from-sinks` | `adp/adp.c` | entity | `Fabric/EntityField.MatchesTheFabric/talker_stream_sources` on "talker_stream_sources" |
| `pool-falls-back-to-heap` | `port/shlan_port.c` | port | `Pool.P4ShlanFunctionsDrawOnTheBoundPool` on "P4 shlan_malloc and shlan_calloc draw on the bound pool"; `(the symbol check)` on "symbols outside the C library" (rv32) |
| `model-rate-unlimited` | `host/mbx_model.c` | model | `Suite/MbxModelGroup.PassesOnTheModel/RateLimit` on "T0 the frames past it count in RATE_DROP" |
| `seq-not-stamped` | `mbx/mbx.c` | port | `Driver.D3HeldMergeFillsAndOrderAcrossChannels` on "D3 ACMP, ACMP, AECP committed by the driver" |
| `model-round-robin` | `host/mbx_model.c` | model | `Suite/MbxModelGroup.PassesOnTheModel/TxCommitOrder` on "X2 ACMP, ACMP, then AECP committed behind a stalled ACMP frame" |
| `model-gm-hi-live` | `host/mbx_model.c` | model | `Suite/MbxModelGroup.PassesOnTheModel/GmSnapshot` on "G0 GM_HI reads the snapshot" |
| `zero-byte-class-accepted` | `port/ctrl_pool.c` | port | `Pool.P5ClassTablesAndArenasRefused` on "P5 a class of zero-byte blocks is refused" |
| `zero-size-refusal-uncounted` | `port/ctrl_pool.c` | port | `Pool.P6CallocOfNothingAndOnAnExhaustedPool` on "P6 and both refusals are counted" |
| `foreign-free-uncounted` | `port/ctrl_pool.c` | port | `Pool.P7FreeBelowTheArenaRefused` on "P7 a free below the first class is refused and counted" |
| `port-pool-unreported` | `port/shlan_port.c` | port | `Pool.P8PortLayerUnbound` on "P8 the bound pool is the one reported" |
| `pool-follows-a-cut-free-list` | `port/ctrl_pool.c` | port | `Pool.P9AFreeListShorterThanItsCountIsExhausted` on "crashed on signal 11" |
| `pool-cut-list-refuses-outright` | `port/ctrl_pool.c` | port | `Pool.P9AFreeListShorterThanItsCountIsExhausted` on "P9 a class whose list ends before its count" |
| `encoding-failure-swallowed` | `port/ctrl_debug.c` | port | `DebugSink.S3UnencodablePrintDiscarded` on "S3 an encoding failure is returned" |
| `rx-binds-no-function` | `loop/ctrl_loop.c` | port | `LoopBring.L9TablesRefuseNullAndOverflow` on "L9 a channel bound to no function is refused" |
| `seed-left-at-zero` | `adp/adp.c` | adp | `AdpCore.A22GeneratorNeverStuckAtZero` on "A22 an entity id whose words cancel the seed constant" |
| `enable-not-idempotent` | `adp/adp.c` | adp | `AdpCore.A23RepeatedEnableOrDisableChangesNothing` on "A23 an enable while enabled draws and arms nothing" |
| `other-subtype-accepted` | `adp/adp.c` | adp | `AdpCore.A24OtherEtherTypeOrSubtypeDiscarded` on "A24 a DISCOVER under another EtherType or subtype is discarded" |
| `app-binds-pool-after-the-mailbox` | `app/ctrl_app.c` | unit | `AppComposition.U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox` on "unsatisfied and active" |
| `app-starts-on-an-uncarved-pool` | `app/ctrl_app.c` | unit | `AppComposition.U1AnUncarvablePoolStartsNothing` on "over-saturated and active" |
| `major-unchecked` | `mbx/mbx.c` | unit | `AppComposition.U1AnotherContractOpensNothing` on "U1 a bitstream carrying another contract is refused"; `IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/major` on "U2 major differs" |
| `evt-words-unchecked` | `mbx/mbx.c` | unit | `IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/evt_words` on "U2 evt_words differs" |
| `step-waits-twice` | `loop/ctrl_loop.c` | unit | `LoopRun.U3TurnsForEverAndSleepsWhenNothingIsOwed` on "U3 every turn is one pass" |
| `maap-base-shifted` | `mbx/mbx.c` | unit | `DriverUnit.D6MaapRangeWritten` on "D6 MAAP_BASE_LO holds the base's low word" |
| `tx-negative-fill` | `mbx/mbx.c` | unit | `DriverUnit.D8TransmitRefusals` on "D8 a TX_TAIL more than a ring behind TX_HEAD is no room" |
| `unknown-event-decoded-as-tick` | `mbx/mbx.c` | unit | `DriverUnit.D9UnknownEventTypeGrandmasterAndInterrupt` on "D9 an event of a type the contract does not define" |
| `whole-field-loses-its-top-bit` | `mbx/mbx_wire.h` | unit | `DriverUnit.D10LanesAndFieldsAtTheirBounds` on "D10 and reads whole" |
| `slots-past-the-bank` | `adp/adp_mbx.c` | unit | `AdpAdapterUnit.B2SlotsPastTheTimerBankRefused` on "B2 slots past the fabric's timer bank" |
| `foreign-frame-uncounted` | `adp/adp_mbx.c` | unit | `AdpAdapterUnit.B3ForeignInterfaceCounted` on "B3 a record, a LINK and a GM" |
| `attach-ignores-poll-room` | `adp/adp_mbx.c` | unit | `AdpAdapterUnit.B4LoopWithNoRoomRefused` on "B4 a loop with no room for the poll is refused" |
| `mmio-offset-as-index` | `plat/mbx_plat_mmio.c` | unit | `MmioPlatform.M1OneWordAtBasePlusOffset` on "M1 a write lands in the word at base + offset" |
| `wait-without-wfi` | `plat/mbx_plat_mmio.c` | unit | `MmioPlatform.M2WaitIsThePlatformWfi` on "M2 each mbx_hal_wait() waits once" |

#### ctrl_nvm: `sw/firmware/ctrl_nvm/test/nvm_mutants.py` (106 defects)

A check is every GoogleTest test of that name, on each port it runs on. Graded at `endstation_ax7101_1x1_tdm8` unless a shape is named.

| Defect | Planted in | Checks that must fail |
|---|---|---|
| `no_crc_check` | `nvm_store.c` | `torn_falls_back`, `verdict_parity` |
| `no_crc_anywhere` | `nvm_klj2.c`, `nvm_store.c` | `powercut` |
| `pick_older` | `nvm_store.c` | `newer_wins` |
| `pick_no_wrap` | `nvm_store.c` | `newer_wins` |
| `tie_picks_b` | `nvm_store.c` | `newer_wins` |
| `erased_header_only` | `nvm_klj2.c` | `verdict_parity`, `codec_parity` |
| `no_ascending` | `nvm_klj2.c` | `verdict_parity`, `codec_parity` |
| `overrun_as_rec` | `nvm_klj2.c` | `verdict_parity`, `codec_parity` |
| `incomplete_accepted` | `nvm_klj2.c` | `verdict_parity`, `codec_parity` |
| `room_unchecked` | `nvm_klj2.c` | `codec_room` |
| `short_prefix_read_on` | `nvm_klj2.c` | `codec_loaded_prefix` |
| `short_prefix_as_len` | `nvm_klj2.c` | `codec_loaded_prefix` |
| `header_guard_early` | `nvm_klj2.c` | `codec_loaded_prefix` |
| `header_guard_late` | `nvm_klj2.c` | `codec_loaded_prefix` |
| `payload_guard_early` | `nvm_klj2.c` | `codec_loaded_prefix` |
| `payload_guard_late` | `nvm_klj2.c` | `codec_loaded_prefix` |
| `lookup_index_unbounded` | `nvm_klj2.c` | `codec_lookups` |
| `long_crc_unchecked` | `nvm_store.c` | `long_container_reads` |
| `unread_not_counted` | `nvm_store.c` | `long_container_reads` |
| `no_version_check` | `nvm_klj2.c` | `wrong_version_falls_back` |
| `no_blank_verdict` | `nvm_klj2.c` | `blank_boot` |
| `pad_not_zero` | `nvm_klj2.c` | `blank_boot` |
| `header_n_rec` | `nvm_klj2.c` | `blank_boot`, `first_commit_bytes` |
| `frame_crc_init` | `nvm_klj2.c` | `vector_round_trip`, `change_commit_bytes` |
| `no_blank_stage` | `nvm_store.c` | `blank_boot` |
| `verdict_not_named` | `nvm_store.c` | `both_torn_blank` |
| `stage_not_rechecked` | `nvm_store.c` | `read_flip_at_stage` |
| `stage_seq_unchecked` | `nvm_store.c` | `read_alias_at_stage` |
| `select_on_unchecked_reread` | `nvm_store.c` | `read_flip_boot` |
| `slot_read_fail_ignored` | `nvm_store.c` | `read_fail_boot` |
| `unread_not_held` | `nvm_store.c` | `authority_unknown`, `fallback_restage`, `read_disagreement` |
| `read_not_retried` | `nvm_store.c` | `read_fail_boot`, `authority_unknown` |
| `refusal_unconfirmed` | `nvm_store.c` | `authority_unknown`, `read_disagreement`, `reads_differ_in_verdict`, `reads_agree_in_digest_not_length` |
| `blank_unconfirmed` | `nvm_store.c` | `authority_unknown` |
| `refusal_by_verdict` | `nvm_store.c` | `read_disagreement` |
| `agreement_by_digest` | `nvm_store.c` | `reads_agree_in_digest_not_length` |
| `disagreement_not_counted` | `nvm_store.c` | `reads_differ_in_verdict`, `reads_agree_in_digest_not_length` |
| `restage_not_retried` | `nvm_store.c` | `read_flip_at_stage`, `read_alias_at_stage`, `read_fail_boot` |
| `fallback_restage_unchecked` | `nvm_store.c` | `fallback_restage` |
| `no_rollback` | `nvm_store.c` | `apply_fault_rolls_back`, `settle_fault_rolls_back` |
| `rollback_failure_ignored` | `nvm_store.c` | `rollback_fault_closes` |
| `release_on_closed` | `nvm_store.c` | `rollback_fault_closes` |
| `fault_as_refusal` | `nvm_store.c` | `apply_fault_rolls_back`, `binding_walk` |
| `refusal_aborts` | `nvm_store.c` | `refused_keeps_default` |
| `settle_fault_ignored` | `nvm_store.c` | `settle_fault_rolls_back` |
| `settle_after_names` | `nvm_store.c` | `golden_restore` |
| `no_settle_without_names` | `nvm_store.c` | `settle_after_the_last_record` |
| `shape_not_checked` | `nvm_store.c` | `shape_mismatch_disables_persistence` |
| `shape_mismatch_released_unproven` | `nvm_store.c` | `shape_mismatch_disables_persistence` |
| `release_before_apply` | `nvm_store.c` | `golden_restore` |
| `apply_erased` | `nvm_store.c` | `erased_records` |
| `model_ready_ignored` | `nvm_store.c` | `model_unproven_closes` |
| `bindings_skipped_unproven` | `nvm_store.c` | `model_unproven_closes` |
| `d3_rollback_takes_bindings` | `nvm_store.c` | `apply_fault_rolls_back`, `settle_fault_rolls_back` |
| `bindings_in_d3_walk` | `nvm_store.c` | `binding_walk`, `golden_restore` |
| `binding_fault_aborts_d3` | `nvm_store.c` | `binding_walk` |
| `binding_fault_keeps_preloads` | `nvm_store.c` | `binding_walk` |
| `quiet_period` | `nvm_store.c` | `debounce` |
| `no_debounce` | `nvm_store.c` | `debounce` |
| `capture_leaves_window_armed` | `nvm_store.c` | `debounce` |
| `taken_off_by_one` | `nvm_store.c` | `debounce` |
| `taken_while_capturing` | `nvm_store.c` | `capture_window_edges` |
| `taken_after_last_latch` | `nvm_store.c` | `capture_window_edges` |
| `change_of_no_record` | `nvm_store.c` | `change_unknown_record` |
| `nothing_to_save_framed` | `nvm_store.c` | `nothing_to_save` |
| `dr2b_ignores_durability` | `nvm_store.c` | `failed_commit_not_skipped` |
| `no_dr2b` | `nvm_store.c` | `unchanged_no_erase` |
| `console_force_ignored` | `nvm_store.c` | `console_commit_unchanged` |
| `no_backoff` | `nvm_store.c` | `media_failures` |
| `unbounded_attempts` | `nvm_store.c` | `media_failures` |
| `budget_rearmed_by_change` | `nvm_store.c` | `dr2c_unchanged_set` |
| `budget_rearmed_by_capture` | `nvm_store.c` | `dr2c_unchanged_set` |
| `commit_now_overrides_exhaustion` | `nvm_store.c` | `dr2c_console` |
| `commit_now_ignores_backoff` | `nvm_store.c` | `dr2c_console` |
| `success_forgives_exhaustion` | `nvm_store.c` | `recovers_after_failure`, `dr2c_unchanged_set` |
| `stale_kept` | `nvm_store.c` | `recovers_after_failure` |
| `dr2b_keeps_stale` | `nvm_store.c` | `recovers_after_failure` |
| `no_blankcheck` | `nvm_store.c` | `media_failures` |
| `blankcheck_first_stretch_only` | `nvm_store.c` | `blankcheck_tail` |
| `blankcheck_read_fail_ignored` | `nvm_store.c` | `media_verdicts` |
| `no_verify` | `nvm_store.c` | `media_failures`, `failed_commit_not_skipped` |
| `verify_skips_last_stretch` | `nvm_store.c` | `verify_tail` |
| `verify_read_fail_ignored` | `nvm_store.c` | `media_verdicts` |
| `program_refusal_ignored` | `nvm_store.c` | `media_verdicts` |
| `no_timeout` | `nvm_store.c` | `media_failures` |
| `same_sequence` | `nvm_store.c` | `change_commit_bytes` |
| `refused_slot_overwritten` | `nvm_store.c` | `refused_slot_kept` |
| `no_blank_slot_takes_b` | `nvm_store.c` | `first_commit_no_blank_slot` |
| `erase_authoritative` | `nvm_store.c` | `change_commit_bytes`, `powercut` |
| `descending_pages` | `nvm_store.c` | `first_commit_bytes` |
| `capture_in_one_step` | `nvm_store.c` | `service_bound` |
| `spin_wait` | `nvm_store.c` | `service_bound` |
| `litespi_no_wren` | `plat/nvm_flash_litespi.c` | `first_commit_bytes` |
| `litespi_status_ignored` | `plat/nvm_flash_litespi.c` | `first_commit_bytes` |
| `litespi_no_guard` | `plat/nvm_flash_litespi.c` | `port_guard` |
| `phc_time` | `plat/nvm_flash_litespi.c` | `time_base` |
| `clock_not_accumulated` | `plat/nvm_flash_litespi.c` | `time_base` |
| `ticks_per_us_truncated` (at `endstation_arty_current`) | `plat/nvm_flash_litespi.c` | `port_clock`, `time_base` |
| `xfer_unbounded` | `plat/nvm_flash_litespi.c` | `port_stall` |
| `open_unbounded` | `plat/nvm_flash_litespi.c` | `port_stall` |
| `call_deadline_ignored` | `plat/nvm_flash_litespi.c` | `port_deadline`, `port_drain_deadline` |
| `drain_deadline_ignored` | `plat/nvm_flash_litespi.c` | `port_drain_deadline` |
| `read_runs_past_device` | `plat/nvm_flash_litespi.c` | `port_read_range` |
| `program_across_page` | `plat/nvm_flash_litespi.c` | `port_write_refusals` |
| `deadline_per_wait` | `plat/nvm_flash_litespi.c` | `port_deadline` |
| `stall_ignored` | `plat/nvm_flash_litespi.c` | `port_stall` |

## 5. Coverage per file, every exclusion and its reason

Method: each gate's `--coverage DIR` builds the firmware and tests at -O0 with `--coverage` (host
models and stubs uninstrumented) and runs every binary that executes the firmware; `fw_coverage.py`
runs gcc's own `gcov --json-format --branch-probabilities` on each `.gcda` and reads the gzipped JSON
(no other tool, nothing else to pin; the gate prints a `toolchain:` line first). Merged per line
across builds (the builds with the most arcs on a line are its measure); exception edges not
counted. Exclusions are the README's table, bound to their statements and exact items (section 0
and the README's "What the gate enforces").

Measured at the head on the host (gcc 16.2.1) with and without the lwsrp arm, and in the
`ubuntu:24.04` replay (gcc 13.3.0): the same table each time, and `coverage.ratchet` records the
after-exclusion figures:

| File | Lines (raw) | Branches (raw) | After exclusions |
|---|---:|---:|---|
| `sw/firmware/ctrl/adp/adp.c` | 168/170 | 73/80 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/app/ctrl_app.c` | 12/13 | 6/8 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 93/93 | 54/54 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/mbx/mbx.c` | 162/162 | 60/60 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 195/196 | 104/108 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | lines 100.00 %  branches 100.00 % |

Round 3 changes no figure here: the new assertions of `codec_loaded_prefix` pin the guards at
their exact ends and take no arc the round-2 test did not (`r3/gates/cov-check.log`,
`r3/gates/cov-check-lwsrp.log`, the same table). Changed from round 1: `ctrl_pool.c` branches 59/60 raw, 59/59 after, to 60/60 (P9 takes the arc);
`nvm_klj2.c` lines 194/196 and branches 103/108 raw (after 194/194, 103/103) to 195/196 and 104/108
raw (after 195/195, 104/104): `codec_loaded_prefix` takes the guard's arc and runs its return.

Exclusions: 14 rows over 11 functions in 6 files (round 1: 16 rows, 13 functions, 7 files), verbatim
from the README:

| File | Function | Statement | Uncovered | Why no input reaches it |
|---|---|---|---|---|
| `sw/firmware/ctrl/adp/adp.c` | `adp_link_change` | `if (a->state == ADP_STATE_DOWN) {` | arc 2 of 2 | A link coming up while the machine is out of DOWN. The machine leaves DOWN only through `enter_delay`, after the link was recorded up: from `adp_set_enable` with the port's level up, or from `adp_link_change(up)`. While enabled, a link recorded down has put the machine in DOWN (the branch below). So an enabled machine with the link recorded down is in DOWN. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_link_change` | `if (a->state != ADP_STATE_DOWN) {` | arc 2 of 2 | A link going down while the machine is already DOWN. An enabled machine reaches DOWN only by a link going down, or by `adp_set_enable(true)` finding the port's link down. So an enabled machine with the link recorded up is out of DOWN. `shutdown` puts it in DOWN but runs only from `adp_set_enable(false)`, which then clears `enabled`, and this function returns early for a disabled machine. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_timer_expired` | `if (a->state == ADP_STATE_DELAY && kind == ADP_TIMER_DELAY) {` | arc 4 of 4 | DELAY with TMR_ADVERTISE held (`kind == ADP_TIMER_DELAY` false). `timer_start(ADVERTISE)` is called only by `advertise`, which then enters WAITING. Every way back into DELAY (`enter_delay`) starts TMR_DELAY, and every way into DOWN stops the timer. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_timer_expired` | `} else if (a->state == ADP_STATE_WAITING && kind == ADP_TIMER_ADVERTISE) {` | arcs 2, 4 of 4; line `a->stray_expiries++;` | The final `else` and its stray count (each operand false): a timer held in DOWN, or WAITING with TMR_DELAY held. DOWN is entered only with the timer stopped (`shutdown`, `adp_link_change(down)`, and `adp_set_enable` with the link down, from a stopped machine). TMR_DELAY is started only by `enter_delay`, which enters DELAY. The function sets the timer to NONE before acting, and a NONE timer returns earlier. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_poll` | `if (a->enabled && a->state == ADP_STATE_DELAY) {` | arcs 2, 4 of 4; line `a->available_owed = false;` | An owed ENTITY_AVAILABLE outside an enabled DELAY (each operand false). `available_owed` is set only by `advertise`, in DELAY: from the TMR_DELAY expiry, which only an enabled machine can hold, or from this poll. It is cleared by `shutdown`, by a link loss (each leaving DELAY), and by the send that enters WAITING. Nothing else leaves DELAY. |
| `sw/firmware/ctrl/adp/adp_mbx.c` | `on_poll` | `owed = adp_poll(&m->ifs[k].adp)` | arc 3 of 4 | The second operand true. `owed` starts false and the loop runs `MBX_N_IF` times, 1 in the generated contract (`mbx_contract.h`), so the operand is read once, while still false. A contract of two interfaces makes it reachable, and the row stops matching. |
| `sw/firmware/ctrl/adp/adp_mbx.c` | `adp_mbx_attach` | `ctrl_loop_bind_rx(l, MBX_CH_ADP, on_frame, m)` | arc 2 of 6 | The channel bind failing. `ctrl_loop_bind_rx` refuses only a channel past `MBX_N_CH` or no function, whatever the loop holds. `MBX_CH_ADP` is a channel of the contract and `on_frame` is a function. Both table-full refusals after it are tested (B4). |
| `sw/firmware/ctrl/app/ctrl_app.c` | `ctrl_app_start` | `if (!adp_mbx_init(` | arcs 2, 3 of 4; line `return false;` | The adapter refusing the app (either operand true). `adp_mbx_init` refuses only `first_slot + MBX_N_IF > MBX_N_TIMERS`: here 0 + 1 > 16, constants of the contract. `adp_mbx_attach` refuses a full sink or poll table, and the app's loop was initialised empty two calls before, its channel bind as above. |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | `nvm_shape_consistent` | `(int)r.id <= last` | arcs 2, 4, 5 of 6; line `return 0;` | The walk out of order, an offset off its sum, or a payload past `NVM_PAYLOAD_MAX` (each operand true). The function takes no argument: it walks the shape the build was generated for. Ids ascend: the walk takes the groups in `nvm_blocks` order, and the `_Static_assert`s at the top of the file keep every block inside its id range. `nvm_rec_next` adds each record's framed length to the offset, as `bytes` does. `NVM_PAYLOAD_MAX` is the largest of the same lengths, a map's from its entry count, and the walk's map length is that count through a byte table that can only be smaller. The refusal this function exists for, the walk's bytes against the sizes, is tested by a doctored build (`test_nvm_shapes.cpp`). |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | `nvm_shape_consistent` | `return count == NVM_N_REC && bytes == NVM_AREA_RAW;` | arc 2 of 4 | The record count off. `NVM_N_REC` sums the group counts the walk visits, each from the same `MILAN_NVM_N_*` constant. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_idle` | `due = nvm.dirty_armed && nvm_any(nvm.dirty) &&` | arc 4 of 6 | The first-dirty window open with nothing dirty (`nvm_any(nvm.dirty)` false). `nvm_store_changed` opens the window only with the bit it sets, and returns before both for a record the shape does not have. Every capture start closes the window, and only a capture clears a dirty bit, after that start. A change behind the capture's cursor reopens the window, and its bit stays set because the capture does not go back. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_framed_as` | `return rec[0] == (uint8_t)(NVM_REC_MAGIC >> 8)` | arcs 2, 4, 6, 10, 12 of 12 | A staged record span that starts with the magic but is not a frame of its record (each compare after the first false). The stage holds only the blank container (`nvm_klj2_blank`, every span erased), a container the boot proved (`nvm_klj2_record` checked each framed span's magic, layout, id and length against the shape; an erased span is all `0xff`), or frames `nvm_rec_frame` wrote; `nvm_store.h` hands the stage out read-only. Only the first byte of an erased span can differ. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_erase_start` | `nvm.target == nvm.st.auth` | arc 2 of 4 | Erasing the authoritative slot. `nvm_target_slot` returns `!auth` while a slot is authoritative, and 0 or 1 while `auth` is -1. |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | `ls_in_journal` | `return addr >= MILAN_FLASH_JOURNAL_OFFSET &&` | arc 2 of 6 | A length longer than the journal (`len <= MILAN_FLASH_JOURNAL_SIZE` false). The port's public entry points are the `struct nvm_flash` calls: `ls_program` refuses a length past `LS_PAGE` before this call, and `ls_erase` passes `LS_BLOCK`. The journal is two 64 KiB slots (`nvm_shape.h` asserts the slot size). gcov files this operand's arcs under the statement's first line, as arcs 1 and 2, and the first operand's under its second. |

How each row's items read on both compilers (gcc 16.2.1 on the host, gcc 13.3.0 in the image the
runner's packages make; arc counts per line, 0 an uncovered arc). The two compilers give every row
the same statement lines, the same arc count per line and the same uncovered positions
(`gates/explore-gcc16.log`, `gates/explore-gcc13.log`, compared position by position):

```text
sw/firmware/ctrl/adp/adp.c adp_link_change() [1 arc] statement 208-208
   208: [417, 0]  if (a->state == ADP_STATE_DOWN) {
   uncovered arcs [(208, 1), (213, 1)]; lines []
sw/firmware/ctrl/adp/adp.c adp_link_change() [1 arc] statement 213-213
   213: [405, 0]  if (a->state != ADP_STATE_DOWN) {
   uncovered arcs [(208, 1), (213, 1)]; lines []
sw/firmware/ctrl/adp/adp.c adp_timer_expired() [1 arc] statement 236-236
   236: [57, 11, 57, 0]  if (a->state == ADP_STATE_DELAY && kind == ADP_TIMER_DELAY) {
   uncovered arcs [(236, 3), (238, 1), (238, 3)]; lines [(241, 'a->stray_expiries++;')]
sw/firmware/ctrl/adp/adp.c adp_timer_expired() [2 arcs, 1 line] statement 238-238
   238: [11, 0, 11, 0]  } else if (a->state == ADP_STATE_WAITING && kind == ADP_TIMER_ADVERTISE) {
   uncovered arcs [(236, 3), (238, 1), (238, 3)]; lines [(241, 'a->stray_expiries++;')]
sw/firmware/ctrl/adp/adp.c adp_poll() [2 arcs, 1 line] statement 274-274
   274: [30, 0, 30, 0]  if (a->enabled && a->state == ADP_STATE_DELAY) {
   uncovered arcs [(274, 1), (274, 3)]; lines [(277, 'a->available_owed = false;')]
sw/firmware/ctrl/adp/adp_mbx.c on_poll() [1 arc] statement 131-131
   131: [8402, 56, 0, 8402]  owed = adp_poll(&m->ifs[k].adp) || owed;
   uncovered arcs [(131, 2)]; lines []
sw/firmware/ctrl/adp/adp_mbx.c adp_mbx_attach() [1 arc] statement 138-139
   138: [40, 0, 40, 1, 40, 1]  return ctrl_loop_bind_rx(l, MBX_CH_ADP, on_frame, m) && ctrl_loop_add_sink(l, on
   139: []  ctrl_loop_add_poll(l, on_poll, m);
   uncovered arcs [(138, 1)]; lines []
sw/firmware/ctrl/app/ctrl_app.c ctrl_app_start() [2 arcs, 1 line] statement 18-19
   18: [40, 0]  if (!adp_mbx_init(&app->adp, cfg->entity, CTRL_APP_ADP_FIRST_SLOT, cfg->current_
   19: [0, 40]  !adp_mbx_attach(&app->adp, &app->loop)) {
   uncovered arcs [(18, 1), (19, 0)]; lines [(20, 'return false;')]
sw/firmware/ctrl/port/ctrl_pool.c ctrl_pool_alloc() [1 arc] statement 115-115
   115: [30, 6, 23, 7, 23, 0]  if (bin->stride >= bytes && bin->free_count > 0u && bin->free_head != NULL) {
   uncovered arcs [(115, 5)]; lines []
sw/firmware/ctrl_nvm/nvm_klj2.c nvm_shape_consistent() [3 arcs, 1 line] statement 195-195
   195: [699952, 0, 699952, 0, 0, 699952]  if ((int)r.id <= last || r.off != bytes || r.plen > NVM_PAYLOAD_MAX)
   uncovered arcs [(195, 1), (195, 3), (195, 4), (202, 1)]; lines [(196, 'return 0;')]
sw/firmware/ctrl_nvm/nvm_klj2.c nvm_shape_consistent() [1 arc] statement 202-202
   202: [4268, 0, 4268, 3]  return count == NVM_N_REC && bytes == NVM_AREA_RAW;
   uncovered arcs [(195, 1), (195, 3), (195, 4), (202, 1)]; lines [(196, 'return 0;')]
sw/firmware/ctrl_nvm/nvm_klj2.c nvm_klj2_check_body() [1 arc, 1 line] statement 348-350
   348: -  /* unreachable for any position the walk can reach (see the
   349: -  * stage size); kept so no read leaves the loaded bytes */
   350: [0, 1341026]  if (pos + NVM_REC_HDR > loaded)
   uncovered arcs [(350, 0)]; lines [(351, 'return NVM_VD_REC;')]
sw/firmware/ctrl_nvm/nvm_store.c nvm_idle() [1 arc] statement 479-480
   479: [28033710, 4948169, 28033710, 0]  due = nvm.dirty_armed && nvm_any(nvm.dirty) &&
   480: [2803, 28030907]  nvm.now_us - nvm.dirty_since_us >= NVM_US(MILAN_NVM_DEBOUNCE_MS);
   uncovered arcs [(479, 3)]; lines []
sw/firmware/ctrl_nvm/nvm_store.c nvm_framed_as() [5 arcs] statement 489-491
   489: [22083, 0]  return rec[0] == (uint8_t)(NVM_REC_MAGIC >> 8) && rec[1] == (uint8_t)NVM_REC_MAG
   490: [22083, 0, 22083, 0]  rec[2] == (uint8_t)MILAN_NVM_REC_LAYOUT && rec[3] == r.id &&
   491: [22083, 10228, 22083, 0, 22083, 0]  rec[4] == (uint8_t)(r.plen >> 8) && rec[5] == (uint8_t)r.plen;
   uncovered arcs [(489, 1), (490, 1), (490, 3), (491, 3), (491, 5)]; lines []
sw/firmware/ctrl_nvm/nvm_store.c nvm_erase_start() [1 arc] statement 627-627
   627: [2846, 0, 11, 2835]  if (nvm.target == nvm.st.auth || f->erase(f->ctx, nvm_slot_addr(nvm.target))) {
   uncovered arcs [(627, 1)]; lines []
sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c ls_in_journal() [1 arc] statement 180-182
   180: [54993, 0]  return addr >= MILAN_FLASH_JOURNAL_OFFSET &&
   181: [54993, 3]  len <= MILAN_FLASH_JOURNAL_SIZE &&
   182: [54992, 1]  addr - MILAN_FLASH_JOURNAL_OFFSET <= MILAN_FLASH_JOURNAL_SIZE - len;
   uncovered arcs [(180, 1)]; lines []
```

(This listing was taken before the round-2 rows were written and the two reachable rows tested: the
bracketed cell is round 1's Uncovered form, and the `ctrl_pool_alloc` and `nvm_klj2_check_body`
entries show the arcs those rows used to exclude. The positions it shows are the ones the round-2
rows name.)

Every remaining row re-judged against its module's public header (round-2 assignment item 3). Round 3
(R506-2-F2): nine rows hold through their headers as they stand; the five `adp.c` rows hold only under
#678's no-callback rule, which `adp.h` does not state yet, and every item they name is reached by a port
that breaks it. The README says so.

Every remaining row re-judged against its module's public header:

| Row | Public surface judged | Judgement |
|---|---|---|
| `adp_link_change`, both rows | `adp.h`: `adp_init`, `adp_set_enable`, `adp_set_current_configuration`, `adp_rx`, `adp_timer_expired`, `adp_link_change`, `adp_gm_change`, `adp_poll` in any order with any argument, and any answers from the ports (`link_up`, `send`, `seed`) | holds under #678's rule (no port calls back into the core synchronously), which `adp.h` does not state yet: the state leaves DOWN only through `enter_delay`, after the link was recorded up; a disabled machine is DOWN (`adp_init`, and `shutdown` on disable), and `adp_set_enable(true)` samples the port's level again. A send port that calls `adp_link_change(false)` from inside a send breaks the rule and reaches both rows' arc 2 (round 3, `r3/gates/probe-adp-reentry-rows.log`) |
| `adp_timer_expired`, DELAY with TMR_ADVERTISE | the same, with the timer port keeping "delay_ms later" | holds under #678's rule. A timer port that expires TMR_ADVERTISE from inside `timer_start` reaches its arc 4, and leaves the machine in WAITING with no timer (`gates/probe-adp-reentry2.log`; round 3, `r3/gates/probe-adp-reentry-rows.log`) |
| `adp_timer_expired`, the final `else` | the same | holds under #678's rule. A timer port that expires a timer from inside `timer_start` reaches it: TMR_ADVERTISE takes arc 2, TMR_DELAY on a grandmaster change arc 4, each with the stray line, leaving WAITING or DELAY with no timer (`gates/probe-adp-reentry.log`; round 3, `r3/gates/probe-adp-reentry-rows.log`) |
| `adp_poll`, owed outside an enabled DELAY | the same | holds under #678's rule: `available_owed` is set only by `advertise` in DELAY and cleared on every way out of DELAY. Round 3 found that a port breaking the rule reaches it too, which round 2 had not shown: a link port that calls back twice from inside `adp_set_enable(true)` (link up, then the TMR_DELAY expiry, while the send port has no room) and then answers down leaves DOWN with an ENTITY_AVAILABLE owed; the next `adp_poll` takes arc 4 and the line, or arc 2 after `adp_set_enable(false)` (`r3/gates/probe-adp-reentry-rows.log`) |
| `on_poll` (static; the loop's poll from `adp_mbx_attach`) | `adp_mbx.h`, `mbx_contract.h` | holds for the generated contract, `MBX_N_IF` 1; the row says so and stops matching at two interfaces |
| `adp_mbx_attach`, the bind | `adp_mbx.h`, `ctrl_loop.h` | holds for any loop the caller passes: `ctrl_loop_bind_rx` refuses only a channel past `MBX_N_CH` or no function |
| `ctrl_app_start`, the adapter's refusal | `ctrl_app.h` | holds for any configuration: the refusals depend only on contract constants and a loop the call itself initialises |
| `nvm_shape_consistent`, both rows | `nvm_klj2.h` (no argument; the generated shape) | holds for every shipped shape; the refusal it exists for is tested by the doctored build |
| `nvm_idle` (static; `nvm_store_service`) | `nvm_store.h`: `nvm_store_boot`, `nvm_store_service`, `nvm_store_changed` (any group and index), `nvm_store_commit_now` | holds: `nvm_store_changed` returns before arming for a record the shape lacks, sets the bit with the window, and only a capture that first closes the window clears a bit |
| `nvm_framed_as` (static) | `nvm_store.h`; the stage is handed out `const` | holds: only the store writes the stage |
| `nvm_erase_start` (static) | `nvm_store.h` | holds for any authority, including -1 |
| `ls_in_journal` (static) | the `struct nvm_flash` calls the LiteSPI port exports | holds: `ls_program` refuses a length past `LS_PAGE` before the call, `ls_erase` passes `LS_BLOCK` |

`fw_coverage.py --selftest`: 28 of 28 planted cases (`gates/cov-selftest.log`). Kept from round 1
(18): the control, a branch drop, a line drop, the record as a floor, a file in one table only
either way, an exclusion with no reason, a statement missing from or repeated in its function, an
unknown function, a stale row (its arc covered now), an under-named row, an unreadable cell, two
builds merged, a shorter build covering none of a longer build's arcs, tests and host models and
outside sources not measured, a throw edge not a branch, and a real gcc+gcov build read as planted
(now also holding the planted row on it). New (10): a stale row whose named line runs now, an arc
moved within its statement, the arc and line moved to another statement with the function's totals
unchanged (R506-1-S1's fixture), a statement with another arc count, a line fragment found nowhere,
two rows on one arc, and on the real compiler a compensating swap (the control, and the swap
refused) and a condition over two lines (the control, and the other operand's arc refused).

## 6. CI wiring: hosted and act evidence

No workflow or classifier file changed in round 2 or round 3 (`git diff 27433e47c..HEAD -- .github
scripts` is empty at the round-3 head too); the job's steps run the round-3 tally cases (18) unchanged.
Round 2's wording: `.github/workflows/rtl-fast.yml`,
`scripts/ci_events.py`, `scripts/ci_scope.py` and `scripts/act_ci.py` are as round 1 left them
(`git diff 27433e47c..HEAD -- .github scripts` is empty). `firmware-unit` runs `tally_selftest.py`
(now 12 planted cases holding each tally line), the ctrl gate, the RV32 SDK, the store's gate, and
`fw_coverage.py --selftest` (now 28 cases) and `--check`. The listener's defects (`--mutants`) join
the two planted-defect campaigns as local arms; `docs/testing/CI_WORKFLOWS.md` and the harness README
say so.

Round 1 as wired (unchanged): job `firmware-unit` in `rtl-fast`, gated on `needs.changes.outputs.rtl`,
in the aggregate's `needs`, env and verdict loop; distribution `libgtest-dev`/`libgmock-dev` with
`dpkg-query`, `g++ --version` and `gcov --version` printed; the ctrl gate run before the SDK install
so its `rv32` arm reports SKIPPED by name; the store's gate with `--require-rv32`; `ci_events.py`
pins the step list, `FIRMWARE_UNIT_RESULT` and the RV32 provenance arms; `ci_scope.py` files every
path under `sw/firmware/` into the job, with cases and mutations.

**Hosted evidence (round-1 head `27433e47`, pushed by the manager as PR #675).** Read-only API,
2026-10-06:

- `rtl-fast` run 37429204550, `pull_request`, head `27433e47`: success. Its `firmware-unit` job
  112155948905: success, 07:22:25 to 07:26:31 UTC, every step executed (GoogleTest and GoogleMock
  1.14.0-1, gcc and gcov 13.3.0).
- `rtl-full` run 37429204551 at the same head: failure. `Verilator shard 2/5` (job 112155955407)
  failed with `TIMEOUT milan_dp_mclk (1800s wall clock)`, which the sweep refuses as `NOCOUNT`
  (exit 92); its 12 other suites passed, `mbx` (the bench whose `suite.hpp` round 1 refactored)
  among them; the `verilator-suites` aggregate failed on that shard. This is not this lane's: the
  same suite times out the same way at the base, in dev's own push run 37412878143 at `423ac5d9`
  (job 112105271160, `TIMEOUT milan_dp_mclk`, NOCOUNT) and in the scheduled run 37430728685 at
  `423ac5d9` (shard 2 failed, job 112160880744). Round 2 changes no RTL and no bench. Receipts:
  `hosted/shard2.log`, `hosted/base-push-shard2.log` (escape sequences removed).
- **Round-2 head `e7e0c10f`** (pushed by the manager to PR #675). Read-only API, snapshots
  2026-10-06 10:47:24 and 11:07:55 UTC (`r3/gates/hosted-checks-e7e0c10f.txt`, `-1108.txt`): `rtl-fast`
  run 37445962183 success; its `firmware-unit` job 112210865722 success, 09:52:59 to 09:57:57 UTC,
  every step executed (checkout, RTL dependencies, GoogleTest packages, the tally's planted cases, the
  ctrl suites, the SDK cache and install, the store's suites with RV32, the coverage ratchet).
  `elaborate` 37445962098 and `docs` 37445962303 success. `rtl-full` 37445962113 still in progress at
  11:07:55: every Verilator and Yosys shard success except `Verilator shard 1/5`, still running;
  `Verilator shard 2/5` passed at this head (job 112210929579), unlike at `27433e47` and at base
  (#673 tracks that timeout); `Physical gPTP` skipped, which is not hardware evidence.
- No hosted run exists at the round-3 head `6ca834a7`: this lane does not push.

**act evidence.** `act_ci.py --pr 675` is the manager's (it records and rechecks the exact remote
head, and this account cannot reach the Docker socket). In its place, at the round-2 head, the job's
own `run:` steps were extracted verbatim from `rtl-fast.yml` and replayed in `ubuntu:24.04`
(podman, `--memory 8g`, each step under `taskset -c 0-3` so `nproc` is 4, `bash --noprofile --norc
-eo pipefail`, `RUNNER_TEMP` set, the checkout a clone of the head with a snapshot commit, the cache
step a miss; `replay.sh` in scratch records the exact command): rc 0 in 300 s, `::job firmware-unit
PASS`. Steps: 01 submodules 5 s; 02 packages 3 s (`libgmock-dev 1.14.0-1`, `libgtest-dev 1.14.0-1`,
`g++ 13.3.0`, `gcov 13.3.0`); 03 tally 3 s, `tally self-test: 12 of 12`; 04 ctrl gate 34 s, rv32
SKIPPED by name, `test_ctrl_firmware: PASS`; 06 SDK 21 s, verified (`d42680e9...`); 07 store 89 s,
`OK across 5 shape(s), 434 tests`; 08 coverage 128 s, `coverage self-test: 28 of 28` and `firmware
coverage: PASS (14 files)` with the table of section 5. Every gate printed its `toolchain:` line.
This is a replay, not act and not hosted evidence.

Round 3, the same replay at `6ca834a7` (`r3/gates/replay.log`, the snapshot commit empty on top of
it): rc 0 in 273 s, `::job firmware-unit PASS`. Steps: 01 submodules 4 s; 02 packages 4 s
(`libgmock-dev 1.14.0-1`, `libgtest-dev 1.14.0-1`); 03 tally 3 s, `tally self-test: 18 of 18`; 04
ctrl gate 28 s, rv32 SKIPPED by name, `test_ctrl_firmware: PASS`; 06 SDK 19 s; 07 store 82 s, `OK
across 5 shape(s), 434 tests`; 08 coverage 110 s, `coverage self-test: 28 of 28` and `firmware
coverage: PASS (14 files)` with the same per-file table as gcc 16 (compared line by line). Every gate
printed its `toolchain:` line (gcc 13.3.0, GoogleTest 1.14.0). A replay, not act and not hosted
evidence.

## 7. Gate table

Final head `6ca834a782a1bd5574d44998c8e214cf16df3441`. Every gate below ran at that exact commit, from a clean tree (`git status` empty), each with its own log, rc and time file, none piped, each run's temporary directory removed after it. Batch 1 (both firmware campaigns, the coverage gate and its self-test, the tally self-test) ran concurrently, then batch 2 (the builder set, R506-2's guard probe, the gcc 13 tally run), then the `firmware-unit` replay. Receipts: `r3/gates/` in scratch, hashed in `RECEIPTS.sha256`.

### The 48-command builder set at `6ca834a78`

Each command as the F1 receipts list it, with the pinned Verilator 5.050 and the pinned Markdown interpreter on PATH; the em-dash and `git diff --check` bases are `423ac5d9`, and command 48 is the full builder with the RV32 SDK mapping, its argv records kept in scratch. The docs gates are commands 13 to 20, 36 and 41 to 43.

| # | Command | rc | Last line |
|---:|---|---:|---|
| 1 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | gen_aem_store self-test: PASS |
| 2 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | prose    tests/steps/aecp_engine_steps.py: BDD steps citing the RTL they mirror |
| 3 | `python3 scripts/lint_rtl.py --check --self-test` | 0 | LINT GATE: PASS (90 violation(s) <= ratchet 90; 18 waived, 0 justified lint_off) |
| 4 | `python3 scripts/suite_shards.py --selftest` | 0 | selftest: PASS |
| 5 | `python3 scripts/ci_events.py --check` | 0 | ci_events: OK (1741 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md) |
| 6 | `python3 scripts/ci_scope.py --selftest` | 0 | selftest: PASS |
| 7 | `python3 scripts/ci_events.py --selftest` | 0 | selftest: PASS (1741 contract items, 2352 arms) |
| 8 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | traceability matrix up to date (77 modules, 0 untested <= ratchet 0, 0 archived) |
| 9 | `python3 scripts/check_feature_status.py` | 0 | feature_status: 0 finding(s) |
| 10 | `python3 scripts/check_submodule_docs.py` | 0 | submodule documentation: OK (4 exact gitlinks) |
| 11 | `python3 scripts/check_cpp_idiom.py` | 0 | build without warnings: 0 <= 0 |
| 12 | `python3 scripts/check_py_idiom.py` | 0 | over-long line: 0 <= 0 |
| 13 | `python3 scripts/docs_check.py` | 0 | docs_check: 0 finding(s) across 196 md files + 1111 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| 14 | `python3 scripts/check_doc_style.py` | 0 | documentation style: OK (22 current documents) |
| 15 | `python3 scripts/check_doc_style.py --selftest` | 0 | documentation style selftest: OK |
| 16 | `python3 scripts/check_solution_docs.py` | 0 | solution documentation: OK (product recipe, 3 memory faces, 13 exhaustive port groups) |
| 17 | `python3 scripts/check_doc_paths.py` | 0 | doc path gate: OK (927 cited paths all resolve; 10 line anchor(s) within their file) |
| 18 | `python3 scripts/check_archive.py` | 0 | archive gate: OK (21 historical page(s), each indexed with metadata and a current successor) |
| 19 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | anchor check: 345 existing cross-page fragment links reproduced |
| 20 | `python3 scripts/gen_toc.py --check` | 0 | TOC gate: OK (136 page(s) carry an annotated contents list, 17 below the 3-section threshold) |
| 21 | `python3 scripts/check_hygiene.py --check` | 0 | HYGIENE RATCHET: PASS (3 population(s), 992 file(s)) |
| 22 | `python3 scripts/check_todo_ownership.py` | 0 | TODO ownership gate: OK (0 owned marker(s), 0 unowned; 37 near-miss occurrence(s) on 30 line(s) correctly not treated as markers; 1049 first-party fil |
| 23 | `python3 scripts/check_sv_idiom.py` | 0 | SystemVerilog idiom gate: OK (137 first-party HDL file(s) across the superproject and both processor submodules, every one .sv/.svh; 0 generic `always |
| 24 | `python3 scripts/check_sh_idiom.py` | 0 | top-heavy long script: 0 <= 0 |
| 25 | `python3 scripts/check_rtl_source_lists.py` | 0 | RTL source-list gate: OK (108 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them; protocol-processor 42/42 tops, 0 recorde |
| 26 | `python3 scripts/check_soc_sources.py` | 0 | SoC source gate: OK (43 instantiated modules all registered, 77 sources all present) |
| 27 | `python3 scripts/check_port_contracts.py` | 0 | review inventory: 93 open and 49 literal-bound named connection(s), 59 without a local rationale (all recorded; none may be added); 317 test-only hier |
| 28 | `python3 scripts/check_nvm_record_space.py` | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set the shape requires with no key claimed twice, every persist |
| 29 | `python3 scripts/check_baremetal_only.py --check` | 0 | baremetal-only: OK (0 findings across 1109 tracked first-party file(s)) |
| 30 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | baremetal-only selftest: PASS (700 arm(s)) |
| 31 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| 32 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | [self-test] OK: 1 drift(s) reported |
| 33 | `python3 scripts/xvlog_gate.py --check` | 0 | xvlog gate: PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors) |
| 34 | `python3 scripts/measure_control_flow.py --selftest` | 0 | 45 checks: 45 PASS, 0 FAIL |
| 35 | `python3 scripts/measure_cohesion.py --selftest` | 0 | 18 checks: 18 PASS, 0 FAIL |
| 36 | `python3 scripts/check_em_dash.py --base 423ac5d9` | 0 | check_em_dash: 0 finding(s) over 494 added line(s) in 6 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [423ac5d9..HEAD] |
| 37 | `python3 scripts/measure_fail_fast.py --check` | 0 | the ratchets can be lowered to 80, 4 and 0 |
| 38 | `python3 scripts/measure_test_evidence.py --check` | 0 | the mutation ratchet can be lowered to 72 |
| 39 | `python3 scripts/measure_naming.py --check` | 0 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| 40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 101 checks: 101 PASS, 0 FAIL |
| 41 | `python3 scripts/gen_toc.py --selftest` | 0 | TOC selftest: PASS (1501/1501 arm(s)) |
| 42 | `python3 scripts/check_em_dash.py --selftest` | 0 | check_em_dash selftest: PASS (339 arm(s)) |
| 43 | `python3 scripts/docs_check.py --selftest` | 0 | docs_check selftest: PASS (23 scrub + 4 routing arm(s)) |
| 44 | `git diff --check 423ac5d9 6ca834a78` | 0 | $ git diff --check 423ac5d910d09ab189b3acc39ae3ae1d10d50b19 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| 45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| 46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | RESULT: PASS |
| 47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | [selftest] OK: 1 drift(s) reported |
| 48 | `python3 -u full-builder-sdk-head.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN |

Command 48 says of itself "ALL GATES PASS EXCEPT 1 NOT RUN": its gate 11, a calibration gate, reads the placement report of an Arty build tree that is not on this host, and this lane runs no Vivado. That arm covers none of this lane's files; it is reported as the gate reports it, not as a pass. Total 1316 s, six at a time.

### The firmware gates, the campaigns and the replay

| Head | Command | rc | Time | Evidence |
|---|---|---:|---|---|
| `6ca834a78` | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <pin>` | 0 | 528 s | mutants: 76 of 76 caught; test_ctrl_firmware: PASS |
| `6ca834a78` | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | 0 | 988 s | saved-state store gate (#665 F1): OK across 5 shape(s), 434 tests, and all 106 planted defects reddened |
| `6ca834a78` | `tally_selftest.py --mutants` | 0 | 65 s | tally self-test: 18 of 18 planted cases read as planted; listener defects: 18 of 18 caught |
| `6ca834a78` | `tally_selftest.py --mutants (gcc 13.3.0, GoogleTest 1.14.0 image, a clone of the head)` | 0 | 70 s | tally self-test: 18 of 18 planted cases read as planted; listener defects: 18 of 18 caught |
| `6ca834a78` | `fw_coverage.py --selftest` | 0 | 1 s | coverage self-test: 28 of 28 planted cases read as planted |
| `6ca834a78` | `fw_coverage.py --check --jobs 4 (as firmware-unit runs it)` | 0 | 126 s | firmware coverage: PASS (14 files) |
| `6ca834a78` | `fw_coverage.py --check --lwsrp <pin> --jobs 4` | 0 | 133 s | firmware coverage: PASS (14 files) |
| `6ca834a78` | `firmware-unit run: steps replayed in ubuntu:24.04` | 0 | 273 s | ::job firmware-unit PASS |


### Probes (evidence, not gates)

R506-2's probes ran from copies in scratch (`r3/probes/r506-2/`, byte-identical to the packet's), never
from the packet's own directory.

| Probe | Head | rc | Result | Receipt |
|---|---|---:|---|---|
| R506-2 `guard_ge_probe.sh`, unchanged: the store gate, all 5 shapes, on a clone with the header guard written `>=` | `6ca834a7` | 1 (the expected result) | each of the 5 shapes fails 1 test of 85, `NvmCodec.codec_loaded_prefix`, `[FAIL] ... at record N's header's exact end, the guard passes and the header is VD_LEN` for every record; at `e7e0c10f` it exited 0 (R506-2's receipt) | `r3/gates/probe-r506-guard-ge.log` |
| R506-2 `tally_extra_plants.py`, unchanged | `6ca834a7` | 0 | its 6 extra cases read as planted on the head's listener; each of its 4 defects reddens the head's own planted cases (`a crash on SIGFPE`, `a crash on SIGBUS`, `a failure in the global environment`, `a disabled suite`) | `r3/gates/probe-r506-tally-extra.log` |
| R506-2 `adp_reentry_probe.py`, unchanged | `6ca834a7` | 0 | rows 1 to 4 reached, row 5 not, as R506-2 reported | `r3/gates/probe-r506-adp-reentry.log` |
| `adp_reentry_rows.py` (scratch `r3/probes/adp/`): `adp.c` for gcov with ports that call back, six scenarios each measured alone, the README's rows applied with `fw_coverage`'s own parser | `6ca834a7` | 0 | row 1: send port, link down in the ENTITY_AVAILABLE send, then link up (WAITING, TMR_ADVERTISE running, no DELAY drawn); row 2: the same in SHUTDOWN's ENTITY_DEPARTING send; rows 3 and 4: TMR_ADVERTISE expired in its `timer_start` (WAITING, no timer, a stray); row 4: TMR_DELAY expired in its `timer_start` on a GM change (DELAY, no timer, a stray); row 5: a link port calling back twice in `adp_set_enable(true)` with the send refused (DOWN with ENTITY_AVAILABLE owed), then `adp_poll` (arc 4) or `adp_set_enable(false)` and `adp_poll` (arc 2) | `r3/gates/probe-adp-reentry-rows.log` |
| the store gate's own self-test with only the six loaded-prefix defects, at 1x1 (`r3/probes/nvm_focus.py`) | working tree that became `7a2686ae` | 0 | 6 of 6, each by its intended assertion | `r3/gates/focus-nvm-guards.log` |
| quick checks before the commits: the store gate at one shape (92 tests), `tally_selftest.py --mutants` (18 and 18), `check_cpp_idiom.py`, `check_py_idiom.py`, `clang-format` of both changed C++ files (no diff) | working tree | 0 each | superseded by the runs above at the head | `r3/gates/dev-nvm-1x1.log`, `dev-tally.log`, `pre-cpp-idiom.log`, `pre-py-idiom.log` |
| hosted checks at `e7e0c10f`, read-only API | `e7e0c10f` | - | section 6 | `r3/gates/hosted-checks-e7e0c10f.txt`, `-1108.txt` |

### Not run in round 3

- The base gate reruns (round 1 has them at `423ac5d9`). Round 3 changes nothing they cover at base.
- The mailbox RTL bench `make -C tb/verilator/mbx`: no bench changed since round 1 (R506-2 reran it at
  `e7e0c10f`: 134/179/13, 4 of 4).
- A scratch merge with dev: dev is still `30e3c018`, as in round 2, whose scratch merge was clean; the
  candidate-merge validation is the manager's.
- `act_ci.py`: there is no pushed round-3 head, and this account cannot reach the Docker socket; the
  replay above is the substitute and is labelled as one.
- R506-2's `klj2_boundary_probe.sh`: its F1 half is what `codec_loaded_prefix` now asserts, and its
  S1 half is #677's.
- No Vivado, hardware, bench access or flashing (none in this lane).

## 8. Open risks and questions

1. **`nvm_klj2_record`'s erased branch reads past `loaded`: #677** (open). A caller of
   `nvm_klj2_check_body` holding only the bytes `nvm_klj2.h` says it must hold gets an out-of-bounds
   read at `nvm_klj2.c:298` when an erased record's header ends exactly at `loaded`. The verdict is
   right; the read is not. The store's own calls are safe. Not fixed here (firmware behaviour; a test
   lane). Round 3: `codec_loaded_prefix`'s comment names the case it leaves out and #677 (R506-2-S1).
2. **The ADP no-callback rule: ruled in #678, not yet in `adp.h`.** The manager ruled that ports never
   call back into the core synchronously; #678's F0 follow-up states it in `adp.h` and the port
   headers and guards it in the core. Until that lands, the five `adp.c` exclusion rows rest on the
   ruling, and the README says so. Round 3 measured that a port breaking the rule reaches every item
   they name, row 5 included (a link port calling back twice from inside `adp_set_enable(true)`),
   which round 2 had not shown. #678's guard asserts on such a call in debug and test builds and
   ignores and counts it in release; once it lands, the rows' proofs rest on the header, and the
   README's premise paragraph should then point at the header, not at the ruling.
3. **The ctrl `rv32` arm and the CI-pinned SDK: #679** (open, pre-existing). The arm fails against
   `scripts/ci_rv32_sdk.py`'s `ilp32d` SDK (no `gnu/stubs-ilp32.h` for `-mabi=ilp32`), at base as at
   the head; `firmware-unit` skips it by name. Locally it ran on an `ilp32` SDK.
4. **lwSRP in CI.** The lwsrp arm stays local while lwSRP is private; the ratchet reads the same with
   and without it (round 3 again: `r3/gates/cov-check.log`, `r3/gates/cov-check-lwsrp.log`).
5. **`milan_dp_mclk` on hosted shard 2: #673** (open). It timed out at the base and at `27433e47`, and
   passed at `e7e0c10f` (job 112210929579), so it depends on the runner. Not this lane's.
6. **Arc identity is gcov's order.** Both recorded compilers agree on every row (section 5). A
   compiler that numbers a row's arcs differently fails the gate, and the row then needs its
   positions rewritten from that compiler's output. A compiler that renumbered a row's arcs and, at
   the same time, changed which branch the tests leave uncovered, so that the uncovered arc landed on
   the same position, would pass unnoticed. That needs a compiler change and a test change at once.
7. **Count unit.** Tallies count tests, not assertions (section 3), as in round 1.
8. **Beyond the letter of F1.** Round 3 also pins the payload guard (`pos + NVM_REC_HDR + plen >
   loaded`) at its exact end, with two planted defects. F1 asked for the header guard; the payload
   guard is the same test's other boundary, and the change is test-only.
