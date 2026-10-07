<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ctrl: the bare-metal control-plane firmware (#665)

Portable C11 for the on-chip RISC-V, and for a hard core, behind the packet
mailbox ([design](../../../docs/design/MAILBOX_SPLIT.md),
[contract](../../../docs/reference/MAILBOX_CONTRACT.md)). No OS, no heap, no
threads: one event loop, static state, and a static pool behind lwSRP's
allocation port. Lane F0 carries the mailbox driver, the HAL, lwSRP's port
layer, the loop and the ADP slice; lane F3 the ACMP module; the other
protocols follow in F2, F4 and F5, each as its own ports-and-adapters module.

`python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`
is the gate: exit 0 = every arm passed and every planted defect was caught.

The [split verification contract](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#6-verification-boundary)
requires FT before F2 to F5.
FT ports these checks to GoogleTest/GoogleMock and adds coverage gates.
Existing mutation arms remain required.
The [service budget](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)
is an integration obligation, not a target-time result established here.

## Contents

- **[Layout](#layout)** -- One directory per layer: wire, driver and HAL, lwSRP's port layer, loop, ADP, ACMP, the app, the MMIO platform, the host model, the tests.
- **[The ACMP module](#the-acmp-module)** -- The core, its mailbox adapter with the ADP channel's tap, and the binding owner on the saved-state store; per-interface keying, the response before its notification, the filter term discovery still waits for, and the boot order.
- **[The host test](#the-host-test)** -- The ten arms, how the processor's ADP and ACMP stimulus is cut from the pinned submodule and walked, and the planted defects.
- **[Run](#run)** -- The four invocations and what each needs.

## Layout

| Directory | What it holds |
|---|---|
| [`wire/`](wire) | the big-endian wire layer every protocol shares |
| [`mbx/`](mbx) | the generated contract header, the three-function bus port (`mbx_hal.h`), the ring lanes and the driver |
| [`port/`](port) | lwSRP's port layer: `shlan_malloc`/`calloc`/`free` on the static block pool, `shlan_printf` on the debug sink |
| [`loop/`](loop) | the event loop: events first, bounded passes, the TICK fan-out in slices, sleep only when nothing is owed, the bring-up order, and the latency bound's assumptions |
| [`adp/`](adp) | the ADP core (no mailbox), its mailbox adapter with the latency bounds, and `adp_entity.py` |
| [`acmp/`](acmp) | the ACMP core (no mailbox), its mailbox adapter with the latency bounds and the ADP channel's tap, and the binding owner on lane F1's store |
| [`app/`](app) | the static composition a platform starts, in two calls: compose, then open |
| [`plat/`](plat) | `mbx_hal.h` on a memory-mapped window (`CTRL_MBX_BASE`, from the SoC's generated `mem.h`) |
| [`host/`](host) | the mailbox model and `mbx_hal.h` on it |
| [`test/`](test) | the host tests and their driver |

## The ACMP module

Milan v1.2 5.5 (connection management) and 5.6.4 (the listener's discovery
machine), in three units, each stating its clauses in its header:

| Unit | What it is |
|---|---|
| [`acmp.h`](acmp/acmp.h), [`acmp.c`](acmp/acmp.c) | the core, with no mailbox: every listener transition of Table 5.30, the talker's answers of 5.5.4, the discovery machine of Table 5.54, the timers of Tables 5.26 and 5.29, the lock, the saved binding record, and the no-callback guard of #678 |
| [`acmp_mbx.h`](acmp/acmp_mbx.h), [`acmp_mbx.c`](acmp/acmp_mbx.c) | the mailbox adapter: the acmp channel, one fabric timer slot per AVB interface armed at the earliest deadline of its sinks, the tap that hands the adp channel's ENTITY_AVAILABLE and ENTITY_DEPARTING to discovery and everything else to ADP, and the service-latency figures per path |
| [`acmp_nvm.h`](acmp/acmp_nvm.h), [`acmp_nvm.c`](acmp/acmp_nvm.c) | the binding group on lane F1's state port (`ctrl_nvm/nvm_state.h`), every other group forwarded to the integrator's owners |

The protocol state is keyed per AVB interface: a sink's probes leave on its
interface, a source answers only probes that arrived on its own, and a sink
takes ADPDUs only from its own interface. A change of a sink's Table 5.22
items is reported through the env's `changed` port only once the response of
the command that caused it has been taken by the transmit ring (#653).

The tree's contract passes no ENTITY_AVAILABLE or ENTITY_DEPARTING into the
adp channel, so until it carries the term the
[design page](../../../docs/design/MAILBOX_SPLIT.md#the-acmp-module) records
as an open decision, the tap's discovery half receives nothing from the
fabric, and a restored binding waits in PRB_W_AVAIL.

A platform that restores bindings boots in this order: `ctrl_app_compose()`,
`acmp_nvm_init()` on the app's ACMP core, `nvm_store_boot()` with its port,
`nvm_store_service()` added as a centisecond consumer, then `ctrl_app_open()`;
the ACMP env's `persist` port calls `nvm_store_changed(NVM_G_BIND, sink)`.

## The host test

The driver compiles the firmware for the host exactly as the target
compiles it (`-std=c11 -Wall -Wextra -Werror -pedantic`), into a temporary
directory, and runs these arms. Every arm but `rv32` is a GoogleTest binary
graded by the tally it prints; the harness, its mocks, the port from the
hand-rolled checks and the coverage ratchet are described in
[the harness page](../gtest/README.md).

| Arm | Source | What it shows |
|---|---|---|
| `model` | `model_suite.cpp` | the mailbox suite's checks, which the RTL passes through both adapters, pass on the model too |
| `port` | `test_port_loop.cpp` | the pool, the debug sink, the driver on the model (TX commit order across channels included, and the own MAC the filter matches with the FILTER_MISMATCH it counts), the loop's order (every interface's own MAC before a channel opens), bounds, owed work and tick slices, and a TICK record taken while centiseconds are carried |
| `unit` | `test_unit_seams.cpp`, `test_unit_driver.cpp`, `test_mmio.cpp` | the firmware's own seams on GoogleMock: the app's composition order over the mailbox window (`mbx_hal.h`) and lwSRP's port layer (`shlan_port.h`), the entity's MAC as every interface's own MAC, the contract check field by field, the driver's refusals and bounds, each interface's own MAC block and the FILTER_MISMATCH read, the adapter's slot, interface and loop-room refusals, and the MMIO platform over a host window |
| `adp` | `test_adp.cpp` | the ADP core over fake ports (deferred sends, strays, discards, the two draw kinds, the available_index every DEPARTING and restart carries on the wire, an owed DEPARTING across a restart and a second SHUTDOWN, owed frames across a link loss, a GM change, a DISCOVER and a stray expiry, and the bound of two owed DEPARTINGs with the SHUTDOWNs beyond it coalesced and counted), the tag race, the latency bound of every path, an owed frame behind a full transmit ring under a HAL that sleeps, the owed DEPARTING across a restart through the mailbox, the pass an AVAILABLE behind owed DEPARTINGs is committed in, and the bound with both rings full and ticks coalesced |
| `walk` | `adp_walk.cpp` | the processor's own ADP walk, reused: 36 cells of its Table 5.51 transcription and its frame builder, on the firmware and the model |
| `acmp` | `test_acmp.cpp`, `test_acmp_mbx.cpp` | the ACMP core over fake ports (every listener command, response, timer and SRP event in every state Table 5.30 gives it, each response field by field; the talker's answers; the lock; responses keyed on the consumer's unique ID; sequence IDs; one timer per interface; owed frames and the response before its notification; the discovery machine cell by cell; the saved record; the no-callback guard), then the adapter on the model: the channel and its filter, the timer slot and the tag rule, the ADP channel's tap, the gPTP pair, the adapter's refusals, every path's service cost (the H-ACMP and H-DISC hooks), an owed response behind a full ring under a HAL that sleeps, full backlogs and the composition |
| `acmpwalk` | `acmp_walk.cpp` | the processor's own ACMP expectations, reused: its F05.3 matrix model of Table 5.30 in lock step with the firmware (88 cells), its Table 5.54 transcription (33 cells) and its talker suite's F05.11 constants, each difference between the two asserted to be what it is |
| `acmpnvm` | `test_acmp_nvm.cpp` | the core and its binding owner on lane F1's store over the host flash model, at the shipping 1x1 shape: a bind saved and fast-connected after a power cycle, an unbind saved, the started flags, an unread slot refusing persistence, a refused record, the roll-back and every other group forwarded |
| `entity` | `entity_fields.cpp` | every shipped config's ADPDU fields, against the fabric's own sources |
| `rv32` | the portable set | a freestanding RV32I build whose only open symbols are C-library string and format functions and libgcc helpers |
| `lwsrp` | `lwsrp_port.cpp` | with `--lwsrp DIR`: lwSRP's own MRP core on the port layer, through the SRP channel, timed by the fabric's ticks; DIR must be lwSRP at the pinned revision with `src/` unmodified |

### Reusing the processor's stimulus

`ctrl_reuse.py` cuts three things out of the pinned
`protocol-processor/tb/adp_engine/sim_main.cpp` at build time: the fixed
entity configuration, the independent 82-byte `model_frame` builder and the
`ADV` table of Milan v1.2 Table 5.51. It first proves the submodule is one
stage-0 gitlink, checked out at that commit, and that the file's bytes are the
blob the pin records; a marker that is missing or repeated refuses the run.

`adp_walk.cpp` drives the firmware into each cell's state through the
mailbox, applies the row's event as the fabric delivers it, and grades the
cell's end state, draws, arms, cancel rule, frame (byte for byte against
`model_frame`) and available_index. The processor's "DELAY, draw in flight"
column has no firmware counterpart (the firmware draws and arms in one call)
and is reported as not applicable. A stray ('S') is an expiry posted with a
tag the firmware did not issue.

For ACMP the same module cuts three more slices, each from its pinned file:
`tb/acmp_listener/sim_main.cpp`'s constants, ACMPDU builder, stimulus and
independent F05.3 matrix model (`pp_acmp_reuse.inc`),
`tb/adp_engine/sim_main.cpp`'s Table 5.54 transcription (`pp_disc_reuse.inc`)
and `tb/acmp_talker/sim_main.cpp`'s F05.11 constants
(`pp_talker_reuse.inc`). `acmp_walk.cpp` runs the processor's model and the
firmware's core in lock step through every Table 5.30 cell a stimulus can
reach, and grades the frames byte for byte, the sink's timer, its record, the
SRP start and stop, discovery, the store's mark and the notification. Four
differences are asserted, field for field, to be exactly what they are:
UNBIND_RX_RESPONSE's talker fields (the processor echoes them; Milan Table
5.36 gives 0), the ACMP status after a TMR_RETRY with the talker discovered
(the processor zeroes it; 5.5.3.5.30 step 2 sets none), the lock's refusal
status (the processor sends 13, TALKER_MISBEHAVING in IEEE 1722.1-2021 Table
8-3; the firmware 16, CONTROLLER_NOT_AUTHORIZED), and DISCONNECT_TX of an
unknown source (the processor answers SUCCESS; Milan 5.5.4.2 step 1,
TALKER_UNKNOWN_ID).

### Planted defects

`--self-test` writes each defect of `ctrl_mutants.py` (with lane F3's
`acmp_mutants.py` appended) into a copy of this tree and requires the arm it
names to exit 1 with a `[FAIL]` line naming the
GoogleTest test and carrying the check's own words; a defect that breaks the
build, or reddens only other tests, is an escape. The arms: ADP clause defects caught by the walk (one per walked
Table 5.51 row but the foreign DISCOVER, which the fabric filter drops and
`adp`'s A4 catches), adapter, latency, owed-output (an owed DEPARTING
replaced, passed or dropped, an owed AVAILABLE dropped or kept wrongly, and
the bound on owed DEPARTINGs included), events-first and available_index
defects by `adp`, pool, sink, loop, tick-slice, tick-carry and driver
defects (TX commit order included) by `port`, lane, model and model
commit-order defects by `model`, a wrong ADPDU field source by `entity`, a
heap call by `rv32`, and a defect in each seam the `unit` arm mocks (the
composition order, the contract fields, the driver's refusals, the
adapter's bounds and the MMIO platform) by `unit`; each check written for
branch coverage (P5 to P9, S3, L9, A22 to A24) has a defect of its own; P9's
free list cut short, followed to its end, is caught by the crash report
that names P9. Each rule of the full-tuple filter (lane FC) has a defect in
the model caught by `model` (a tag stripped or taken for an EtherType, a
destination, EtherType or subtype ignored, any unicast or interface 0's MAC
taken for own, the AECP response term dropped, FILTER_MISMATCH never, wrongly
or ERR-less counted; for the MAAP DEFEND to own unicast, the message_type read
a byte early, a tuple's message types ignored, a message_type refusal left
uncounted, a DEFEND taken to any unicast), and the firmware's side has its
own: the own MAC unguarded or halved, FILTER_MISMATCH read from another register (`unit` and
`port`), the own MACs written after the channels open (`port`) and the app's
own MAC not the entity's (`unit`). Lane F3 adds 195 defects for the
`acmp`, `acmpwalk` and `acmpnvm` arms: a defect in each clause step, each
response field, each guard term, each timer, the owed queue and the #653
release, discovery's every guard, each port's re-entry flag, the saved
record, the adapter's slot, tag and tap, extra mailbox accesses on each
measured path, each backlog figure understated, and the binding owner's
forwarding; and seven wrong numbers in `acmp.h` itself, which the tests
catch because they spell the standards' values (`acmp_fake.hpp`, `spec`),
never the header's. They are `acmp_mutants.py`'s table. Every test of those
arms is named by at least one defect, which `unnamed_tests` proves before any is planted, as lane F1's
store suite does. Some FC filter defects in the host model also name
lane F3's own-unicast and FILTER_MISMATCH checks. With
`--lwsrp` it also requires the pin to refuse a
scratch clone with one compiled source edited, and the same clone at
another revision. `--slice K/N` plants slice K of N of the table, so the
campaign runs as N commands.

## Run

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice 1/6
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --lwsrp <lwSRP checkout>
```

Needs a host C and C++ compiler, GoogleTest and GoogleMock (`libgtest-dev`
and `libgmock-dev`), PyYAML (the `acmpnvm` arm also runs the builder for its
shape, as lane F1's gate does), and for `rv32` an RV32 compiler for
`-mabi=ilp32` with its C headers (the CI-pinned SDK of
`scripts/ci_rv32_sdk.py` is `ilp32d` and carries no `gnu/stubs-ilp32.h`, so
`firmware-unit` runs this gate with the arm skipped). lwSRP is referenced, never vendored, at the
revision `ctrl_arms.LWSRP_REV` records,
`19f5796b63652eb1151906de73cb827d4980a53f`:

```sh
git clone https://github.com/kebag-logic/lwSRP lwSRP
git -C lwSRP checkout 19f5796b63652eb1151906de73cb827d4980a53f
```

The `lwsrp` arm refuses another HEAD, and a checkout whose `src/` (every
source and header it compiles) differs from that revision. Moving the pin is
a reviewed change to `LWSRP_REV`.
