<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# gtest: the host unit tests of the bare-metal firmware (#665 lane FT)

The bare-metal control-plane firmware ([`ctrl`](../ctrl/README.md)) and its
saved-state store ([`ctrl_nvm`](../ctrl_nvm/README.md)) are tested on the host
with GoogleTest and GoogleMock. The firmware stays C11 with no heap; the tests
are C++ and include its C headers through `extern "C"`. This directory holds
what both host gates share: the `main()` and tally listener every test binary
links, the build and grading helpers, the coverage gate and its ratchet.

The gates are unchanged in name and exit status:
`sw/firmware/ctrl/test/test_ctrl_firmware.py` and
`sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py`. Both now build GoogleTest
binaries and grade each one by the tally it prints.

## Contents

- **[Layout](#layout)** -- The shared harness here, and the tests beside each firmware module.
- **[The tally](#the-tally)** -- The listener's summary line, what counts as a failure, and the planted cases that prove a failing or crashing test fails the tally.
- **[The seams and their mocks](#the-seams-and-their-mocks)** -- The four ports the firmware already has, and the GoogleMock object for each.
- **[The port](#the-port)** -- Every hand-rolled check moved onto GoogleTest, arm by arm, with the counts.
- **[Coverage](#coverage)** -- Line and branch coverage of the firmware's sources with gcc's gcov, the ratchet that refuses a drop, and each branch no input can reach, with its proof.
- **[Run](#run)** -- The commands, and what each needs.
- **[CI](#ci)** -- The hosted job, the arms it leaves to the local gates, and the versions it runs with.
- **[Not in this lane](#not-in-this-lane)** -- lwSRP's own suites.

## Layout

| Path | What it holds |
|---|---|
| [`fw_gtest.hpp`](fw_gtest.hpp), [`fw_gtest_main.cpp`](fw_gtest_main.cpp) | `main()` of every firmware test binary: GoogleTest, GoogleMock and the tally listener |
| [`fw_gtest.py`](fw_gtest.py) | the build (C11 firmware, C++ tests, the harness's main), the run and the grade both gates use |
| [`tally_cases.cpp`](tally_cases.cpp), [`tally_selftest.py`](tally_selftest.py) | the listener's planted cases and their self-test |
| [`fw_coverage.py`](fw_coverage.py), [`fw_coverage_selftest.py`](fw_coverage_selftest.py) | the coverage gate and its planted cases |
| [`coverage.ratchet`](coverage.ratchet) | per-file line and branch coverage the gate refuses to fall below |
| [`../ctrl/test`](../ctrl/test) | the control-plane tests, its mocks and its arms |
| [`../ctrl_nvm/test`](../ctrl_nvm/test) | the saved-state store's tests, its rig and fixture writer, and its mocks |

## The tally

Each binary names its tally once, `FW_TALLY_LABEL("...")`, and the listener
prints the one shape [`scripts/suite_tally.py`](../../../scripts/suite_tally.py)
reads:

```text
== ctrl port, driver and loop (host model): checks: 30   failures: 0 ==
RESULT: PASS
```

`checks` is the tests run and `failures` the tests that failed, were skipped,
or crashed. One more is added for each test suite whose set-up or tear-down
failed, one for a failure outside every test (a global environment's), and
one for each disabled test, alone or in a disabled suite, which runs nothing.
Every failed assertion also prints `[FAIL] <Suite.Test>: <its last line>`,
which is the marker `suite_tally.py --verdict` reads and the line the
planted-defect campaigns match a test by. An assertion's last line is the
check's own words wherever the hand-rolled suite had them.

A run that does not finish still leaves a verdict. A fatal signal (SIGSEGV,
SIGBUS, SIGFPE, SIGILL, SIGABRT) prints a `[FAIL]` line naming the test it was
in and a tally counting that test failed, then dies of the same signal.
`exit()` before the run ended does the same through an `atexit` handler. A
process that leaves with neither (`_exit()`, `SIGKILL`) prints no tally, which
the reader refuses as `NOCOUNT`. A binary passes only when it exits 0 AND its
log reads as a pass: one tally, no `NOCOUNT`, no failure in it, no `[FAIL]`
line (`fw_gtest.grade`).

`tally_selftest.py` proves each of those with a planted case run through the
same grade, and through `suite_tally.py` itself: every count above, every
fatal signal the handler is installed for, the `atexit` path and `NOCOUNT`. Each case proves two things
apart. Its tally line, read with `suite_tally.scan`, the sweep's own
scanner, must carry exactly the `checks` and `failures` below, with
`RESULT: FAIL` under it whenever `failures` is not 0: so the tally line
itself fails, not only the `[FAIL]` marker or the exit status. And its
verdict must be the one below, through `fw_gtest.grade` and through
`suite_tally.py --verdict` or the sweep's `NOCOUNT`:

| Planted case | Exit | Tally line: checks, failures | Verdict |
|---|---|---|---|
| one passing test (the control) | 0 | 1, 0 (`RESULT: PASS`) | passes |
| a failing assertion | 1 | 1, 1 | fails, `[FAIL] Fail.Expect` |
| SIGSEGV inside a test | -11 | 1, 1, from the signal handler | fails, `[FAIL] Crash.Segv` |
| `abort()` inside a test | -6 | 1, 1, from the signal handler | fails, `[FAIL] Crash.Abort` |
| SIGBUS inside a test | -7 | 1, 1, from the signal handler | fails, `[FAIL] Crash.Bus` |
| SIGFPE inside a test | -8 | 1, 1, from the signal handler | fails, `[FAIL] Crash.Fpe` |
| SIGILL inside a test | -4 | 1, 1, from the signal handler | fails, `[FAIL] Crash.Ill` |
| `exit(0)` inside a test | 0 | 1, 1, from the `atexit` handler | fails, `[FAIL] Exit.Zero` |
| a skipped test | 0 | 1, 1 | fails, `[FAIL] Skip.Silent: skipped: ...` |
| an uncaught exception | 1 | 1, 1 | fails, GoogleTest's own catch, `[FAIL] Throw.Uncaught` |
| a disabled test | 0 | 0, 1 | fails, `[FAIL] Disabled.DISABLED_NeverRuns` |
| a disabled suite | 0 | 0, 1 | fails, `[FAIL] DISABLED_Suite.NeverRuns` |
| a failure in a suite's set-up | 1 | 1, 2: the suite's test and its set-up | fails, `[FAIL] SetUpFails` |
| a failure in a suite's tear-down | 1 | 1, 1: the tear-down, its test passed | fails, `[FAIL] TearDownFails` |
| a failure in the global environment's set-up | 1 | 1, 1: the program's, its test passed | fails, `[FAIL] (program)` |
| `_exit(0)` inside a test | 0 | none | `NOCOUNT` |
| no test selected | 0 | 0, 0 | `NOCOUNT` |
| a disabled test, `GTEST_ALSO_RUN_DISABLED_TESTS=1` in the environment | 0 | 0, 1 | fails, as above: the gates drop `GTEST_*` from each binary's environment, so a shell's GoogleTest controls cannot narrow or reshape a gate's run |

`tally_selftest.py --mutants` plants eighteen defects into copies of the
listener and requires each to turn the cases it names red, through the
tally line wherever the defect falsifies it: a skipped test, a suite's
set-up or tear-down failure, a crashed test or an early exit left out of
the failures; a crashed test left out of the checks; disabled tests left
out of the failures; a test disabled by its suite's name not seen as
disabled; a failure outside every test not counted; `RESULT: PASS` printed whatever the
failures; no test counted; no `[FAIL]` line; no `atexit` handler; no
signal handler; and each of the five signals left out of the handler's
list. A suite's tear-down failure or the program's, left out, prints
`RESULT: PASS` on the tally line. A copy that does not build, or a case
that still reads as planted, is an escape.

A binary still running after `fw_gtest.RUN_TIMEOUT_S` (600 s) is killed and
graded `NOCOUNT`, with what it printed before the kill.

## The seams and their mocks

GoogleMock mocks the ports the firmware already has. No seam was added for a
test.

| Seam | Kind | Mock | Used by |
|---|---|---|---|
| `ctrl/mbx/mbx_hal.h`, the bus port | link seam: three C functions a platform defines | [`MockMbxHal`](../ctrl/test/mock_mbx_hal.hpp) | the composition, the contract check, the driver's refusals and `ctrl_loop_run` (`test_unit_seams.cpp`, `test_unit_driver.cpp`) |
| `ctrl/port/shlan_port.h`, lwSRP's port layer | link seam: the four `shlan_*` calls and the pool binding | [`MockShlanPort`](../ctrl/test/mock_shlan_port.hpp) | the composition binding lwSRP's allocator to the app's pool (`test_unit_seams.cpp`) |
| `ctrl_nvm/nvm_flash.h`, the media port | function-pointer port | [`MockNvmFlash`](../ctrl_nvm/test/mock_nvm_flash.hpp) | the boot read's agreement rule (`test_nvm_flashmock.cpp`) |
| `<generated/csr.h>`, the LiteSPI port's CSR accessors | link seam: the host stubs' `litespi_model_*` calls | [`MockLitespiCsr`](../ctrl_nvm/test/mock_litespi_csr.hpp) | the on-chip flash port alone (`test_nvm_litespi.cpp`) |

A link-seam mock forwards to the one mock object alive in the test, and a
call with none alive fails the test that made it. `MockMbxHal` can also leave
a loop that never returns: `escape_after(n, &jmp)` jumps back to the test's
`setjmp` from the n-th `mbx_hal_wait()`.

The models the hand-rolled suites ran on stay, and stay the main stimulus:
the mailbox model (`ctrl/host`), and the flash, state and LiteSPI models
(`ctrl_nvm/host`). A mock is used where a model cannot answer as a test needs:
a window laid out word by word, a medium that answers each read differently,
a command master that outlasts a deadline.

## The port

Every F0 and F1 host check now runs on GoogleTest. Each check's meaning is
kept: it is an assertion carrying the check's own words, inside a test named
after its labelled step or scenario. What changed is the count unit: the
hand-rolled tally counted assertions, the listener counts tests, so the
numbers below are not the same kind of number. The lane FT pull request on
#665 maps every hand-rolled check, by its words, to the test that now holds
it.

| Arm | Hand-rolled source | Checks before | GoogleTest source | Tests now |
|---|---|---:|---|---:|
| `model` | `model_suite.cpp` (one `Checker`) | 134 | `model_suite.cpp`: one test per group of `tb/verilator/mbx/suite.hpp` | 14 |
| `port` | `test_port_loop.c` | 81 | `test_port_loop.cpp`: P0 to P9, S0 to S3, D0 to D5, L0 to L9 | 30 |
| `adp` | `test_adp.c` | 163 | `test_adp.cpp`: A0 to A24, B1, C0 to C6, E0 to E5, F0 to F7 | 26 |
| `walk` | `adp_walk.cpp` (one `Checker`) | 320 | `adp_walk.cpp`: one test per walked Table 5.51 cell, and four scenarios | 41 |
| `entity` | `entity_probe.c` and the arm's own compare | 45 | `entity_fields.cpp`: one test per field per shipped config | 45 |
| `lwsrp` | `lwsrp_port.c` | 13 | `lwsrp_port.cpp`: one application for the run, as a boot has | 1 |
| `unit` | (new) | 0 | `test_unit_seams.cpp`, `test_unit_driver.cpp`, `test_mmio.cpp` | 23 |
| `rv32` | the arm's symbol check | 1 | unchanged: a cross build, not a host test | 1 |
| `ctrl_nvm`, per shape | `nvm_test.c` with `nvm_checks.py`, `nvm_checks_write.py` | 42 checks | `test_nvm_boot.cpp`, `test_nvm_write.cpp`, `test_nvm_vector.cpp`: one test per check per port it runs on | 71 (69 at a shape with no recorded vector) |
| `ctrl_nvm`, per shape | (new) | 0 | `test_nvm_codec.cpp`, `test_nvm_more.cpp`, `test_nvm_flashmock.cpp` | 16 |
| `ctrl_nvm`, 1x1 shape | (new) | 0 | `test_nvm_shapes.cpp` (two doctored builds), `test_nvm_litespi.cpp` | 5 |

The table records the port as FT landed it. Lane FC (the full-tuple ingress
filter) then added eight `model` groups, D12 to `port`, and D11 and U4 to
`unit`, so those arms run 22, 31 and 25 tests.

The saved-state store's checks kept their names: a check that ran on both
flash ports is two tests, `Ports/NvmBoth.<check>/model` and `.../litespi`.
Their oracle did not move. [`nvm_fixture.py`](../ctrl_nvm/test/nvm_fixture.py)
writes, per shape, every container a test loads or compares with and every
payload set a restore must leave, from `scripts/nvm_klj2.py`; the tests read
that fixture and never assemble or decode a container themselves. The
scenario runner is now [`nvm_rig.cpp`](../ctrl_nvm/test/nvm_rig.cpp), the same
script words run in the test's own process. Where the hand-rolled check
decoded a slot to find one changed value, the test compares the whole slot
with the container the reference encoder assembles for the same records.

`test_check.h` and `test_check.c`, the hand-rolled framework, are gone:
nothing used them once the port was done.

Every planted defect of `ctrl_mutants.py` and `nvm_mutants.py` is now killed
by a named GoogleTest test: a mutant names the test (and, for `ctrl`, the
check's words) whose `[FAIL]` line must appear. Each test added here has a
planted defect of its own.

## Coverage

[`fw_coverage.py`](fw_coverage.py) measures line and branch coverage of the
firmware's own sources under `sw/firmware/ctrl` and `sw/firmware/ctrl_nvm`:
not the tests, not the host models, not the host stubs.

**How.** Each gate's `--coverage DIR` mode builds the firmware and the tests
at `-O0` with gcc's `--coverage`, leaves the host models and stubs
uninstrumented, and runs every binary that executes the firmware: every arm of
`ctrl`, the lwSRP arm when a checkout is given (the measurement reads the
same without it), and every shipped shape of the store with the unit
binaries. The reader is gcc's own `gcov` in its JSON
intermediate format (`gcov --json-format --branch-probabilities`, gcc 9 and
later), read by the small reader in `fw_coverage.py`. No other coverage
tool is involved, so there is nothing else to pin: the coverage is gcc's, and
the gate's first line, `toolchain:`, names the gcc, gcov and GoogleTest it
ran with. A source built into several objects
(each arm, each shape) is merged line by line: a line is covered when any run
executed it, an arc when any run took it. Where builds of one line differ in
their arcs (a shape constant folds a condition), the build with the most arcs
is the line's measure. Exception edges are not counted; the firmware is C.

**The ratchet.** [`coverage.ratchet`](coverage.ratchet) records, per file,
covered over total lines and branch arcs after the exclusions. `--check`
refuses a file whose line or branch coverage falls below its record, a
measured file the ratchet does not record, and a recorded file nothing
measured. `--write` records the measurement and refuses to record a drop.

**The target** is 100 % branch coverage of the protocol and saved-state code,
and every file here is at 100 % of its lines and branches once the exclusions
below are taken out. Each exclusion is a branch no sequence of calls through
the module's public header reaches, with the ports keeping the contract their
header states; a static function is judged through the public functions that
call it. A row's proof does not rest on what today's callers happen to pass.
Where it rests on a generated constant of the contract, the row says so, and
the row stops matching (so the gate fails) when the constant changes. Nine
rows meet that standard through their headers as they stand. The five
`adp.c` rows do not yet: they rest on a port rule that `adp.h` does not
state, which #678 has ruled and will add to it (see below the gate's rules).

### Coverage exclusions

Each row names its file, its function, a fragment of the statement's first
line that occurs once in the function, the items it leaves uncovered, and
why no input reaches them. The statement runs from that line to the line
where its parentheses close and it ends with `;`, opens a block with `{`, or
closes a control header with `)`. The Uncovered cell names its items
exactly:

- `arcs 2, 4 of 4`: the statement has four arcs, counted in gcov's order
  line by line through the statement, and the second and the fourth are
  uncovered. The count runs over the whole statement because gcc at `-O0`
  files the arcs of a condition that spans lines under one line of it, and
  not always the operand's own (the `ls_in_journal` row).
- ``line `a->stray_expiries++;` ``: the first line from the statement's on
  that holds the fragment is unexecuted.

**What the gate enforces**, row by row and function by function:

- the row has a reason, and its function is in the measurement;
- its fragment occurs exactly once in the function, and its statement ends
  inside the function;
- the statement has exactly the number of arcs the row states, and the
  uncovered ones are exactly those it names, no more and no fewer;
- every line it names is a line gcov measures, and is unexecuted;
- no arc or line is named by two rows;
- every uncovered arc and every unexecuted line of a function that has rows
  is named by one of them.

Only the named items are taken out of the measurement; anything else
uncovered stays in its file's tally, where the ratchet refuses it. So a row
fails when what it names becomes covered, when anything else in its
function goes uncovered, and when an uncovered item moves, to another arc
of the same statement, another statement or another line, even with the
function's totals unchanged. An arc is identified by its position in gcov's
order, which is the compiler's: both versions in [the version
table](#ci) number every row's arcs the same, and a compiler that numbered
them differently would fail the gate, not pass it. `fw_coverage.py
--selftest` plants each of these refusals, two of them on gcc's own output
(a compensating swap and a condition over two lines).

**The five `adp.c` rows rest on #678's rule, not on `adp.h` as it
stands.** They assume two things of the ports. `adp.h` states the first:
the timer port calls `adp_timer_expired` once, `delay_ms` after
`timer_start`, which the rows read as after `timer_start` has returned.
`adp.h` does not state the second: no port calls into the core while the
core is calling it. [#678](https://github.com/kebag-logic/milan-fpga/issues/678)
rules that ports never call back into the core synchronously, and its
follow-up to the F0 code states the rule in `adp.h` and the port headers
and guards it in the core. Until that lands, the rows rest on the ruling.
The adapter (`adp_mbx.c`) keeps the rule today: its ports call no core
function, and the core is called only from the loop's handlers. A port
that breaks the rule reaches every item the five rows name. Each of these
was measured alone with gcov:

- **Rows 1 and 2** (`adp_link_change`, arc 2 of 2 each): a send port that
  reports the link down (`adp_link_change(false)`) from inside a send.
  From inside the ENTITY_AVAILABLE send, it leaves the machine in WAITING
  with the link recorded down and TMR_ADVERTISE running. The next link-up
  then reaches row 1 and enters no DELAY. From inside SHUTDOWN's
  ENTITY_DEPARTING send, the nested call reaches row 2.
- **Rows 3 and 4** (`adp_timer_expired`: row 3's arc 4 of 4, row 4's arcs
  2 and 4 of 4 and its stray-count line): a timer port that expires a
  timer from inside `timer_start`. Expiring TMR_ADVERTISE that way reaches
  row 3's arc and row 4's arc 2, and leaves the machine in WAITING with no
  timer running. Expiring TMR_DELAY on a grandmaster change reaches row 4's
  arc 4, and leaves it in DELAY with none. Each counts one stray.
- **Row 5** (`adp_poll`, arcs 2 and 4 of 4 and its line): a link port that
  calls back twice from inside `adp_set_enable(true)`. It reports the link
  up, expires the TMR_DELAY that starts while the send port has no room,
  then answers down. The machine is left in DOWN with an ENTITY_AVAILABLE
  owed. The next `adp_poll` reaches arc 4, or arc 2 after
  `adp_set_enable(false)`.

So `adp.c`'s 100 % holds for ports that keep #678's rule, and not for a
port that breaks it.

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

The two rows a public caller reaches were tested and taken out:
`ctrl_pool_alloc`'s `bin->free_head != NULL`, a client writing into a block
after freeing it (`Pool.P9`), and `nvm_klj2_check_body`'s refusal of a loaded
prefix that ends before a record header (`NvmCodec.codec_loaded_prefix`,
which pins that guard and the payload's at their exact ends).
Each has a planted defect that removes it.

## Run

```sh
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP checkout>
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 16
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp <lwSRP checkout> --jobs 16
python3 sw/firmware/gtest/fw_coverage.py --selftest
```

They need a C11 and a C++20 compiler (gcc), `gcov`, GoogleTest and
GoogleMock with their pkg-config files (`libgtest-dev` and `libgmock-dev` on
Debian and Ubuntu, `gtest` on Arch), PyYAML, and for the RV32 arms an RV32
compiler. The store's arm builds with the pinned SDK
(`scripts/ci_rv32_sdk.py`). The ctrl arm compiles against the SDK's C
headers for `-mabi=ilp32`, and that SDK is `ilp32d` with no
`gnu/stubs-ilp32.h`, so the ctrl arm needs an `ilp32` SDK at
`~/br-milan-rv32/host` or a bare-metal compiler. The ctrl gate, the store's
gate, the coverage gate and the tally's self-test each print a `toolchain:`
line first: the C and C++ compilers, gcov and GoogleTest and GoogleMock
they ran with. A gate's coverage mode does not; the coverage gate that
drives it prints the line for the run.

## CI

`rtl-fast`'s `firmware-unit` job
([CI workflow policy](../../../docs/testing/CI_WORKFLOWS.md#fast-feedback))
runs on every change the classifier calls relevant (`scripts/ci_scope.py`;
every path under `sw/firmware/` is). It installs `libgtest-dev` and
`libgmock-dev` from the runner's distribution, prints their versions and the
gcc and gcov it measures with, then runs the tally's planted cases, the ctrl
gate, the store's gate at every shape with its RV32 build on the pinned SDK,
and this coverage gate with its planted cases. `scripts/ci_events.py` pins
the job's steps and the `rtl-fast` aggregate's verdict on it, and
`scripts/act_ci.py` replays it with the rest of `rtl-fast.yml`.

Three arms stay with the local gates, and the job names each:

- the ctrl gate's `rv32` arm, for the SDK reason above: the job runs that
  gate before it installs the SDK, so the arm reports SKIPPED;
- the ctrl gate's `lwsrp` arm: lwSRP is a private repository the workflow's
  token cannot read. The coverage ratchet reads the same with and without
  it;
- both gates' planted-defect campaigns (`--self-test`) and the tally
  listener's (`tally_selftest.py --mutants`).

The versions this harness was built and measured with:

| Where | gcc and gcov | GoogleTest and GoogleMock |
|---|---|---|
| the development host | 16.2.1 | 1.18.0 |
| `ubuntu-24.04` (`ubuntu-latest`), as the job installs them | 13.3.0 | 1.14.0 (`libgtest-dev` and `libgmock-dev` 1.14.0-1) |

Both measure the same per-file coverage, and every row of
[the exclusion table](#coverage-exclusions) matches under both.

## Not in this lane

lwSRP's own upstream suites are not run here. They run with lane F4, when
lwSRP is vendored at its pin, and a coverage gap in lwSRP is fixed upstream.
The `lwsrp` arm covers only this firmware's port layer under lwSRP's MRP
core. lwSRP's timer port keeps every timer it was given in one list with no
removal, so an application destroyed and created again leaves its timers, in
freed blocks, on the list `shlan_timer_tick` walks; the arm creates one
application for its run, as a boot does, and F4 inherits that constraint.
