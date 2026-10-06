# HANDOFF: #665 lane FT, the GoogleTest/GoogleMock harness ([A547])

Status: REVIEW READY at `27433e47c6d7805376547a91b418cf6aa9d95d2a` (local branch `665-ft-gtest`, not pushed), posted on #665 as comment 6011410375.

- Issue: kebag-logic/milan-fpga#665. Assignment: comment 6009234414. TAKEN: comment 6009299837.
- Base: dev `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`. Commits on top: `bd5c89695` Run the control-plane firmware's host checks on GoogleTest under a tally listener, and retire test_check (#665 FT); `1b3cca0d0` Port the saved-state store's checks onto GoogleTest, mock the firmware's own seams, and add the tests branch coverage needs, each with a planted defect (#665 FT); `ddd1adfb5` Measure the firmware's line and branch coverage with gcov and refuse any per-file drop below a ratchet (#665 FT); `36014e0b4` Run the firmware's GoogleTest suites and coverage ratchet in rtl-fast's firmware-unit job (#665 FT); `4e6f0c46d` Declare the store tests' sequence tables as std::array, wrap the fixture's long line, and spell the coverage gate's README name so the classifier does not read it as the top-level page (#665 FT); `4018e3260` Point the harness page's port section at the pull request that maps every hand-rolled check (#665 FT); `27433e47c` Take a line's arcs from the builds with the most arcs only, as the coverage gate states, and plant the case that a shorter build covers none of them (#665 FT).
- Roles: executor [A547]; reviewers [R506] (internal), [R507] (external).
- No RTL change, no change to the default build or the shipping image: the diff touches
  `sw/firmware/**` tests, harness and docs, `tb/verilator/mbx/suite.hpp` (a template parameter, same
  checks), `scripts/ci_events.py`, `scripts/ci_scope.py`, `.github/workflows/rtl-fast.yml` and docs.
  Outside `test/`, the firmware diff is the two READMEs and three comment lines of
  `sw/firmware/ctrl/adp/adp_mbx.h` that name the C++ test file; nothing under `hdl/`, `syn/`,
  `configs/`, `sw/litex/` or `sw/builder/` changed.

## Contents

1. Harness layout
2. The tally listener, with its planted failure and crash cases
3. Port table: old check -> new test, with counts
4. Mutation arms and the test that kills each
5. Coverage per file, every exclusion and its reason
6. CI wiring: hosted and act evidence
7. Gate table
8. Open risks and questions

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
1.14.0-1. Each gate prints the versions it ran with (`toolchain:` line), and the CI job prints
`dpkg-query`, `g++ --version` and `gcov --version`.

## 2. The tally listener

Every binary prints exactly the shape `scripts/suite_tally.py` reads,
`== <label>: checks: N   failures: M ==` then `RESULT: PASS|FAIL`, where checks = tests run and
failures = tests failed, skipped or crashed (plus one per failure outside a test and per disabled
test). Every failed assertion prints `[FAIL] <Suite.Test>: <its last line>` (the `--verdict`
marker and the campaigns' match). A fatal signal prints the `[FAIL]` line and a failing tally from an
async-signal-safe handler, then re-raises; `exit()` inside a test is caught by `atexit`; `_exit()` and
SIGKILL leave no tally, which the reader refuses as `NOCOUNT`. `fw_gtest.grade` passes a binary only
when it exits 0 AND its log reads as a pass.

`python3 sw/firmware/gtest/tally_selftest.py` at the head (rc 0):

```text
[ok] a passing test (the control): exit 0, 1 tests, 0 failures
[ok] a failing assertion: exit 1, its tallies report 1 failure(s) across 1 checks
[ok] a crash on SIGSEGV: exit -11, its tallies report 1 failure(s) across 1 checks
[ok] an abort: exit -6, its tallies report 1 failure(s) across 1 checks
[ok] exit(0) inside a test: exit 0, its tallies report 1 failure(s) across 1 checks
[ok] a skipped test: exit 0, its tallies report 1 failure(s) across 1 checks
[ok] an uncaught exception: exit 1, its tallies report 1 failure(s) across 1 checks
[ok] a disabled test: exit 0, its tallies report 1 failure(s) across 0 checks
[ok] a failure in a suite's set-up: exit 1, its tallies report 2 failure(s) across 1 checks
[ok] _exit(0) inside a test: exit 0, NOCOUNT: no tally, or a tally of nothing (the run did not finish)
[ok] no test selected: exit 0, NOCOUNT: no tally, or a tally of nothing (the run did not finish)
tally self-test: 11 of 11 planted cases read as planted
```

## 3. Port table: old check -> new test, with counts

The count unit changed: the hand-rolled tally counted assertions, the listener counts tests. Every
check's meaning is kept as an assertion carrying the same words, inside a test named after its
labelled step or scenario. Splits and merges, arm by arm:

| Arm | Before (unit: assertions) | After (unit: tests) | Split or merge |
|---|---:|---:|---|
| `model` | 134 (one `Checker`) | 14 | merged by group: one test per group of `tb/verilator/mbx/suite.hpp` (`Suite/MbxModelGroup.PassesOnTheModel/<Group>`), every check of the group an assertion inside it; the RTL bench still counts 134/179/13 at head as at base |
| `port` | 81 | 29 | merged by labelled step: P0 to P8, S0 to S3, D0 to D5, L0 to L9 (P5 to P8, S3, L9 new) |
| `adp` | 163 | 26 | merged by labelled step: A0 to A24, B1, C0 to C6, E0 to E5 (E5 split into 6 parameterised cases), F0 to F7 (A22 to A24 new) |
| `walk` | 320 (one `Checker`) | 41 | merged by cell: one test per walked Table 5.51 cell (`Table551/AdpWalkCell.Graded/<ROW_x_COL>`) and the scenario tests (P11 and the frame checks) |
| `entity` | 45 | 45 | one test per field per shipped config (`Fabric/EntityField.MatchesTheFabric/<field>`) |
| `lwsrp` | 13 | 1 | merged: one application for the run, as a boot has (lwSRP's timer list keeps every timer it was given; see `sw/firmware/gtest/README.md`, Not in this lane) |
| `unit` | 0 | 23 | new: the seams on GoogleMock and the MMIO platform |
| `rv32` | 1 | 1 | unchanged: a cross build, not a host test |
| `ctrl_nvm`, per shape | 42 checks | 71 tests (69 at a shape without a recorded vector) | kept by name: a check on both ports is two tests `Ports/NvmBoth.<check>/model` and `.../litespi` |
| `ctrl_nvm`, per shape, new | 0 | 15 | `test_nvm_more.cpp`, `test_nvm_codec.cpp`, `test_nvm_flashmock.cpp` |
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

Both campaigns at the head, rc 0:

- ctrl: `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <pin>`: `mutants: 74 of 74 caught`, both lwSRP pin arms refusing, `test_ctrl_firmware: PASS`. A defect is
  caught only when its arm fails AND a `[FAIL]` line names the test with the check's words; a broken
  build or only other tests failing is an escape. The 51 base defects are all still killed, now by the
  named GoogleTest test; the 23 defects added for the new checks are killed too, `rx-no-resync` gained
  a `unit`-arm kill (D7), and the `unit` arm joined the campaign.
- ctrl_nvm adds 18 defects to the base's 82 (one or more per new check, and `codec_parity` and the two
  read-agreement checks named on existing defects that must also redden them).
- ctrl_nvm: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 16`: `saved-state store gate (#665 F1): OK across 5 shape(s), 429 tests, and all 100 planted defects reddened`. `unnamed_checks`
  proves every check of the suite is named by at least one defect before any is planted.

One test was strengthened because its planted defect showed it could not fail:
`NvmLitespiPort.port_drain_deadline` now bounds the drain below LS_POLL_MAX, so a drain bounded by
its poll count alone (`drain_deadline_ignored`) fails it.

#### ctrl: `sw/firmware/ctrl/test/ctrl_mutants.py` (74 defects)

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

#### ctrl_nvm: `sw/firmware/ctrl_nvm/test/nvm_mutants.py` (100 defects)

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
with about a hundred lines of Python (no other tool, nothing else to pin). Merged per line across
builds; exception edges not counted. Exclusions are the table in the README, matched per function
(exact arc and line counts, statement fragment unique in the function, a reason required).

Measured at the head, on the host (gcc 16.2.1) and in the `ubuntu-24.04` replay (gcc 13.3.0), with
and without the lwsrp arm: identical, and the ratchet `coverage.ratchet` records the after-exclusion
figures:

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
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 59/60 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 194/196 | 103/108 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | lines 100.00 %  branches 100.00 % |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | lines 100.00 %  branches 100.00 % |

Exclusions (16 rows over 13 functions in 7 files), each with its proof, verbatim from the README:

| File | Function | Statement | Uncovered | Why no input reaches it |
|---|---|---|---|---|
| `sw/firmware/ctrl/adp/adp.c` | `adp_link_change` | `if (a->state == ADP_STATE_DOWN) {` | 1 arc | A link coming up while the machine is out of DOWN. The machine leaves DOWN only through `enter_delay`, after the link was recorded up: from `adp_set_enable` with the port's level up, or from `adp_link_change(up)`. While enabled, a link recorded down has put the machine in DOWN (the branch below). So an enabled machine with the link recorded down is in DOWN. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_link_change` | `if (a->state != ADP_STATE_DOWN) {` | 1 arc | A link going down while the machine is already DOWN. An enabled machine reaches DOWN only by a link going down, or by `adp_set_enable(true)` finding the port's link down. So an enabled machine with the link recorded up is out of DOWN. `shutdown` puts it in DOWN but runs only from `adp_set_enable(false)`, which then clears `enabled`, and this function returns early for a disabled machine. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_timer_expired` | `if (a->state == ADP_STATE_DELAY && kind == ADP_TIMER_DELAY) {` | 1 arc | DELAY with TMR_ADVERTISE held. `timer_start(ADVERTISE)` is called only by `advertise`, which then enters WAITING. Every way back into DELAY (`enter_delay`) starts TMR_DELAY, and every way into DOWN stops the timer. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_timer_expired` | `} else if (a->state == ADP_STATE_WAITING && kind == ADP_TIMER_ADVERTISE) {` | 2 arcs, 1 line | The final `else` and its stray count: a timer held in DOWN, or WAITING with TMR_DELAY held. DOWN is entered only with the timer stopped (`shutdown`, `adp_link_change(down)`, and `adp_set_enable` with the link down, from a stopped machine). TMR_DELAY is started only by `enter_delay`, which enters DELAY. The function sets the timer to NONE before acting, and a NONE timer returns earlier. |
| `sw/firmware/ctrl/adp/adp.c` | `adp_poll` | `if (a->enabled && a->state == ADP_STATE_DELAY) {` | 2 arcs, 1 line | An owed ENTITY_AVAILABLE outside an enabled DELAY. `available_owed` is set only by `advertise`, in DELAY: from the TMR_DELAY expiry, which only an enabled machine can hold, or from this poll. It is cleared by `shutdown`, by a link loss (each leaving DELAY), and by the send that enters WAITING. Nothing else leaves DELAY. |
| `sw/firmware/ctrl/adp/adp_mbx.c` | `on_poll` | `owed = adp_poll(&m->ifs[k].adp)` | 1 arc | The second operand true. `owed` starts false and the loop runs `MBX_N_IF` times, 1 in the contract, so the operand is read once, while still false. |
| `sw/firmware/ctrl/adp/adp_mbx.c` | `adp_mbx_attach` | `ctrl_loop_bind_rx(l, MBX_CH_ADP, on_frame, m)` | 1 arc | The channel bind failing. `ctrl_loop_bind_rx` refuses only a channel past `MBX_N_CH` or no function. `MBX_CH_ADP` is a channel of the contract and `on_frame` is a function. Both table-full refusals after it are tested (B4). |
| `sw/firmware/ctrl/app/ctrl_app.c` | `ctrl_app_start` | `if (!adp_mbx_init(` | 2 arcs, 1 line | The adapter refusing the app. `adp_mbx_init` refuses only `first_slot + MBX_N_IF > MBX_N_TIMERS`: here 0 + 1 > 16, constants of the contract. `adp_mbx_attach` refuses a full sink or poll table, and the app's loop was initialised empty two calls before, its channel bind as above. |
| `sw/firmware/ctrl/port/ctrl_pool.c` | `ctrl_pool_alloc` | `bin->free_head != NULL` | 1 arc | A class counting free blocks with an empty list. `free_count` and the free list move together: `bin_carve` builds a list of `blocks` entries and sets the count to `blocks`; `bin_take` pops one and decrements; `ctrl_pool_free` pushes one and increments, after its range and double-free checks. |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | `nvm_shape_consistent` | `(int)r.id <= last` | 3 arcs, 1 line | The walk out of order, an offset off its sum, or a payload past `NVM_PAYLOAD_MAX`. Ids ascend: the walk takes the groups in `nvm_blocks` order, and the `_Static_assert`s at the top of the file keep every block inside its id range. `nvm_rec_next` adds each record's framed length to the offset, as `bytes` does. `NVM_PAYLOAD_MAX` is the largest of the same lengths, a map's from its entry count, and the walk's map length is that count through a byte table that can only be smaller. The refusal this function exists for, the walk's bytes against the sizes, is tested by a doctored build (`test_nvm_shapes.cpp`). |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | `nvm_shape_consistent` | `return count == NVM_N_REC && bytes == NVM_AREA_RAW;` | 1 arc | The record count off. `NVM_N_REC` sums the group counts the walk visits, each from the same `MILAN_NVM_N_*` constant. |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | `nvm_klj2_check_body` | `if (pos + NVM_REC_HDR > loaded)` | 1 arc, 1 line | A header past the loaded bytes, which the comment above it already calls unreachable. With the whole container loaded, `loaded` is `img_len` and the test before it refused `pos + NVM_REC_HDR > img_len - 4`. With only `NVM_STAGE_BYTES` loaded, `pos` advances only past accepted records of this shape, so `pos + NVM_REC_HDR <= NVM_KLJ2_HDR + NVM_AREA_RAW + NVM_REC_HDR < NVM_IMG_LEN + NVM_REC_HDR = NVM_STAGE_BYTES`. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_idle` | `due = nvm.dirty_armed && nvm_any(nvm.dirty) &&` | 1 arc | The first-dirty window open with nothing dirty. `nvm_store_changed` opens the window only with the bit it sets. Every capture start closes the window, and only a capture clears a dirty bit, after that start. A change behind the capture's cursor reopens the window, and its bit stays set because the capture does not go back. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_framed_as` | `return rec[0] == (uint8_t)(NVM_REC_MAGIC >> 8)` | 5 arcs | A staged record span that starts with the magic but is not a frame of its record. The stage holds only the blank container (`nvm_klj2_blank`, every span erased), a container the boot proved (`nvm_klj2_record` checked each framed span's magic, layout, id and length against the shape; an erased span is all `0xff`), or frames `nvm_rec_frame` wrote. Only the first byte of an erased span can differ. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_erase_start` | `nvm.target == nvm.st.auth` | 1 arc | Erasing the authoritative slot. `nvm_target_slot` returns `!auth` while a slot is authoritative, and 0 or 1 while `auth` is -1. |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | `ls_in_journal` | `len <= MILAN_FLASH_JOURNAL_SIZE` | 1 arc | A length longer than the journal. `ls_program` passes at most `LS_PAGE`, checked just before the call, and `ls_erase` passes `LS_BLOCK`. The journal is two 64 KiB slots (`nvm_shape.h` asserts the slot size). gcov files this arc under the expression's first line. |

`fw_coverage.py --selftest`: 18 of 18 planted cases (control, a branch drop, a line drop, the record
as a floor, a file in one table only either way, an exclusion with no reason, missing or repeated
statement, unknown function, stale, under-stated, unreadable count, two builds merged, a shorter build covering none of a longer build's arcs, tests and host
models and outside sources not measured, a throw edge not a branch, and a real gcc+gcov build read as
planted). Six mutations of the reader in scratch were each caught by a case, and so is the reader's
first merge, which mixed a shorter build's arcs into a longer build's by position (found and fixed
before handoff; no line measured today differs in arc count across builds, so the figures did not
move).

## 6. CI wiring: hosted and act evidence

- `.github/workflows/rtl-fast.yml`: new job `firmware-unit`, gated on `needs.changes.outputs.rtl`
  like the other RTL fast jobs, in the `rtl-fast` aggregate's `needs`, env and verdict loop. Steps:
  checkout; submodules; `apt-get install libgtest-dev libgmock-dev` (+ pyyaml) with
  `dpkg-query`/`g++ --version`/`gcov --version`; the tally self-test; the ctrl gate; the pinned RV32
  SDK (the docs job's cache and install); the store's gate with `--require-rv32` at every shape; the
  coverage self-test and `--check`.
- `scripts/ci_events.py`: the job's whole step list recorded in `RTL_STEP_LISTS` (sequence, keys,
  scripts), `FIRMWARE_UNIT_RESULT` in the aggregate's env, the RV32 provenance arms extended to the
  job (wrong cache key/path/fallback, installation removed, verification skipped, `--require-rv32`
  dropped). At the head: `ci_events: OK (1741 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)`; `selftest: PASS (1741 contract items, 2352 arms)` (95 of the caught arms are
  planted in the new job: its scripts, its keys and its RV32 provenance).
- `scripts/ci_scope.py`: decision recorded in its docstring: `firmware-unit` gates on the same
  conservative answer (every path under `sw/firmware/` is relevant; the job's gates also read the
  builder, configs, scripts/ and the processor submodule, so no narrower list decides it). Four new
  classification cases (`sw/firmware` sources, tests, the gtest README, the ratchet) and two new
  mutations (`sw/firmware/` and `sw/firmware/gtest/` filed as documentation), both caught. At the head:
  `selftest: PASS`.
- `scripts/act_ci.py`: no change needed. It replays `rtl-fast.yml` whole, and the new job passes its
  sandbox rules (literal `ubuntu-latest`, only trusted actions, no container or service);
  `validate_workflow_sandbox` accepts the file.
- `docs/testing/CI_WORKFLOWS.md`: the job in Fast feedback (with the three arms left local and why)
  and the local commands.

Hosted evidence: none. The branch is not pushed (pushing and PR creation are outside this lane), so
no hosted run exists.

act evidence: `act_ci.py --pr <n>` needs a pushed PR (it records and rechecks the exact remote head)
and this host's Docker socket is not accessible to this account, so it was not run. In its place,
the job's own `run:` steps were extracted verbatim from `rtl-fast.yml` at the head and replayed in an
`ubuntu:24.04` container (podman, 16 GB, each step pinned to 4 CPUs like a hosted runner, run as
`bash --noprofile --norc -eo pipefail`, the checkout replaced by a clone of the snapshot, the cache a
miss): every step rc 0 (step 01: 4 s, step 02: 5 s, step 03: 4 s, step 04: 56 s, step 06: 32 s, step 07: 161 s, step 08: 210 s), `::job firmware-unit PASS`; versions libgmock-dev:amd64 1.14.0-1; libgtest-dev:amd64 1.14.0-1; g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; gcov (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; the ctrl rv32 arm SKIPPED by name, the store gate "saved-state store gate (#665 F1): OK across 5 shape(s), 429 tests", and "firmware coverage: PASS (14 files)" with every exclusion matching.

The replay found two things the job now handles, and one this lane fixed:

1. lwSRP is a private repository (anonymous `git ls-remote` refused; HTTPS 404), so a hosted runner's
   token cannot clone it. The ctrl gate's lwsrp arm is opt-in; the job omits it, and the coverage
   ratchet was measured both ways and reads the same (section 5).
2. The ctrl gate's `rv32` arm compiles against the SDK's glibc headers with `-mabi=ilp32`; the
   CI-pinned bootlin SDK is `ilp32d` and has no `gnu/stubs-ilp32.h`. This fails at base `423ac5d9`
   exactly as at the head (pre-existing, F0; measured by pointing the gate at the pinned SDK). The
   job runs the ctrl gate before installing the SDK, so that arm reports SKIPPED by name; the store's
   RV32 arm builds with the pinned SDK and runs with `--require-rv32`. See section 8.
3. `fw_gtest.run` raised on a missing program (`pkg-config` absent in the bare image); it now returns
   a failed run (rc 127) naming the program.

## 7. Gate table

All at the head `27433e47c6d7805376547a91b418cf6aa9d95d2a` unless marked base (`423ac5d9`). Each command ran with its own log and rc
file; none was piped.

### The 48-command builder set (at the head)

Each command as the F1 receipts list it, with the pinned Verilator 5.050 and Markdown venv on PATH; the em-dash and `git diff --check` bases are `423ac5d9`, and command 48 is the full builder with the RV32 SDK mapping, its argv records kept in scratch.

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
| 36 | `python3 scripts/check_em_dash.py --base 423ac5d9` | 0 | check_em_dash: 0 finding(s) over 375 added line(s) in 6 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [423ac5d9..HEAD] |
| 37 | `python3 scripts/measure_fail_fast.py --check` | 0 | the ratchets can be lowered to 80, 4 and 0 |
| 38 | `python3 scripts/measure_test_evidence.py --check` | 0 | the mutation ratchet can be lowered to 72 |
| 39 | `python3 scripts/measure_naming.py --check` | 0 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| 40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 101 checks: 101 PASS, 0 FAIL |
| 41 | `python3 scripts/gen_toc.py --selftest` | 0 | TOC selftest: PASS (1501/1501 arm(s)) |
| 42 | `python3 scripts/check_em_dash.py --selftest` | 0 | check_em_dash selftest: PASS (339 arm(s)) |
| 43 | `python3 scripts/docs_check.py --selftest` | 0 | docs_check selftest: PASS (23 scrub + 4 routing arm(s)) |
| 44 | `git diff --check 423ac5d9 27433e47c` | 0 | $ git diff --check 423ac5d910d09ab189b3acc39ae3ae1d10d50b19 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| 45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| 46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | RESULT: PASS |
| 47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | [selftest] OK: 1 drift(s) reported |
| 48 | `python3 -u full-builder-sdk-head.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN |

### The firmware gates, the campaigns and the replay

| Where | Command | rc | Time | Evidence |
|---|---|---:|---|---|
| head | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <pin>` | 0 | 553 s | mutants: 74 of 74 caught; test_ctrl_firmware: PASS |
| base | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <pin>` | 0 | 72 s | mutants: 51 of 51 caught; test_ctrl_firmware: PASS |
| head | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 16` | 0 | 623 s | saved-state store gate (#665 F1): OK across 5 shape(s), 429 tests, and all 100 planted defects reddened |
| base | `test_ctrl_nvm.py --require-rv32 --self-test (the base gate has no --jobs)` | 0 | 198 s | saved-state store gate (#665 F1): OK across 5 shape(s), 42 checks, and all 82 planted defects reddened |
| base | `nvm_hosttest/test_nvm_firmware.py --self-test (head: command 31 above)` | 0 | 81 s | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| head | `sw/firmware/gtest/tally_selftest.py` | 0 | 5 s | tally self-test: 11 of 11 planted cases read as planted |
| head | `fw_coverage.py --selftest` | 0 | 0 s | coverage self-test: 18 of 18 planted cases read as planted |
| head | `fw_coverage.py --check --lwsrp <pin> --jobs 16` | 0 | 136 s | firmware coverage: PASS (14 files) |
| head | `fw_coverage.py --check --jobs 16 (as firmware-unit runs it)` | 0 | 121 s | firmware coverage: PASS (14 files) |
| head | `make -C tb/verilator/mbx -j16 (Verilator 5.050, an export of the head)` | 0 | 16 s | mbx mutants: 4 of 4 caught |
| base | `make -C tb/verilator/mbx -j16 (Verilator 5.050)` | 0 | 19 s | mbx mutants: 4 of 4 caught |
| head | `firmware-unit run: steps replayed in ubuntu:24.04` | 0 | 492 s | ::job firmware-unit PASS; ::step 08.sh rc=0 elapsed=210 s |

Evidence runs that are not gates (each fails by design, to show the pre-existing ctrl `rv32` finding; section 8):

| Where | Command | rc | Evidence |
|---|---|---:|---|
| base | `test_ctrl_firmware.py --require-rv32` with the CI-pinned SDK | 1 | 8 / # include <gnu/stubs-ilp32.h> |
| head | `test_ctrl_firmware.py --require-rv32` with the CI-pinned SDK | 1 | 8 / # include <gnu/stubs-ilp32.h> |

Command 48 exits 0 and says of itself "ALL GATES PASS EXCEPT 1 NOT RUN": its gate 11, a calibration
gate, reads the placement report of an Arty build tree that is not on this host, and this lane runs no
Vivado. That arm covers none of this lane's files; it is reported here as the gate reports it, not as
a pass.

## 8. Open risks and questions

- **The ctrl `rv32` arm and the CI-pinned SDK (pre-existing, needs its own Issue).** At base and head
  the arm fails against `scripts/ci_rv32_sdk.py`'s SDK (no `gnu/stubs-ilp32.h` for `-mabi=ilp32`). It
  passes locally with an `ilp32` Buildroot SDK. Fixing it is an F0 decision (the arm's flags, a
  freestanding header set, or another SDK pin), not this lane's; `firmware-unit` skips the arm by
  name until then. A maintainer may want this filed as a new Issue.
- **lwSRP in CI.** The lwsrp arm stays local while lwSRP is private. Running it hosted needs a
  read credential for that repository (a maintainer decision), or the vendoring F4 plans.
- **Count unit.** Tallies now count tests, not assertions (section 3). Any page quoting an old
  assertion count for these suites would be stale; the firmware READMEs were updated.
- **gcov version drift.** gcc 13 and 16 agree today. A future runner gcc that attributes arcs
  differently changes per-function counts; the exclusion matcher is per function to absorb line
  attribution, and a real disagreement fails the gate rather than passing silently.
- **No hosted or act run yet.** The first hosted `rtl-fast` run on the pushed head is the first
  real evidence for the job; the container replay is the closest local substitute available here.
