<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ctrl: the bare-metal control-plane firmware (#665)

Portable C11 for the on-chip RISC-V, and for a hard core, behind the packet
mailbox ([design](../../../docs/design/MAILBOX_SPLIT.md),
[contract](../../../docs/reference/MAILBOX_CONTRACT.md)). No OS, no heap, no
threads: one event loop, static state, and a static pool behind lwSRP's
allocation port. Lane F0 carries the mailbox driver, the HAL, lwSRP's port
layer, the loop and the ADP slice; F2 adds the opt-in [MAAP owner](maap/README.md),
F3 the ACMP module, and F4 the [SRP adapter](srp/README.md) on pinned lwSRP.
Each protocol has its own core and mailbox adapter.

`python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`
is the gate: exit 0 = every arm passed and every planted defect was caught.

The [split verification contract](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#6-verification-boundary)
requires FT before F2 to F5.
FT ports these checks to GoogleTest/GoogleMock and adds coverage gates.
Existing mutation arms remain required.
The [service budget](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)
is an integration obligation, not a target-time result established here.

## Contents

- **[Layout](#layout)** -- One directory per layer: wire, driver and HAL, lwSRP's port layer, loop, ADP, MAAP, ACMP, the app, the MMIO platform, the host model, the tests.
- **[The ACMP module](#the-acmp-module)** -- The core, its mailbox adapter with the ADP channel's tap, and the binding owner on the saved-state store; per-interface keying, the response before its notification, the adp filter's bound-talker term, TMR_NO_RESP from the accepted send, and the boot order.
- **[The composition](#the-composition)** -- ADP, ACMP and MAAP in one app: the attach order, the channels the open enables, the timer slots, the refusals and the pass bound.
- **[The host test](#the-host-test)** -- The sixteen arms and lwSRP's, how the processor's ADP and ACMP stimulus is cut from the pinned submodule and walked, and the planted defects.
- **[Run](#run)** -- The four invocations and what each needs.
- **[Linked size](#linked-size)** -- The composed app linked with the pinned SDK and no library, audited as RV32I, at the shipping and the largest shape, against the block-RAM budget and dev.

## Layout

| Directory | What it holds |
|---|---|
| [`wire/`](wire) | the big-endian wire layer every protocol shares |
| [`mbx/`](mbx) | the generated contract header, the three-function bus port (`mbx_hal.h`), the ring lanes and the driver |
| [`port/`](port) | lwSRP's port layer: `shlan_malloc`/`calloc`/`free` on the static block pool, `shlan_printf` on the debug sink |
| [`loop/`](loop) | the event loop: events first, bounded passes, the TICK fan-out in slices, sleep only when nothing is owed, the bring-up order, and the latency bound's assumptions |
| [`adp/`](adp) | the ADP core (no mailbox), its mailbox adapter with the latency bounds, and `adp_entity.py` |
| [`maap/`](maap) | the Annex B core, per-interface mailbox adapter, allocation CSR output and H-MAAP evidence |
| [`srp/`](srp) | per-interface MSRP/MVRP adapter, generated static shape, admission and the binding port |
| [`acmp/`](acmp) | the ACMP core (no mailbox), its mailbox adapter with the latency bounds and the ADP channel's tap, and the binding owner on lane F1's store |
| [`app/`](app) | the static composition a platform starts: compose, then open, then `ctrl_app_attach_srp` for SRP |
| [`plat/`](plat) | `mbx_hal.h` on a memory-mapped window (`CTRL_MBX_BASE`, from the SoC's generated `mem.h`) |
| [`host/`](host) | the mailbox model and `mbx_hal.h` on it |
| [`test/`](test) | the host tests and their driver |

## The ACMP module

Milan v1.2 5.5 (connection management) and 5.6.4 (the listener's discovery
machine), in three units, each stating its clauses in its header:

| Unit | What it is |
|---|---|
| [`acmp.h`](acmp/acmp.h), [`acmp.c`](acmp/acmp.c) | the core, with no mailbox: every listener transition of Table 5.30, the talker's answers of 5.5.4, the discovery machine of Table 5.54, the timers of Tables 5.26 and 5.29, the lock, the saved binding record, and the no-callback guard of #678 |
| [`acmp_mbx.h`](acmp/acmp_mbx.h), [`acmp_mbx.c`](acmp/acmp_mbx.c) | the mailbox adapter: the acmp channel, one fabric timer slot per AVB interface armed at the earliest deadline of its sinks, the tap that hands the adp channel's ENTITY_AVAILABLE and ENTITY_DEPARTING to discovery and everything else to ADP, the adp channel's bound-talker table kept equal to the bindings, and the service-latency figures per path |
| [`acmp_nvm.h`](acmp/acmp_nvm.h), [`acmp_nvm.c`](acmp/acmp_nvm.c) | the binding group on lane F1's state port (`ctrl_nvm/nvm_state.h`), every other group forwarded to the integrator's owners |

The protocol state is keyed per AVB interface: a sink's probes leave on its
interface, a source answers only probes that arrived on its own, and a sink
takes ADPDUs only from its own interface. A change of a sink's Table 5.22
items is reported through the env's `changed` port only once the response of
the command that caused it has been taken by the transmit ring (#653).

The adp channel's term is decided on #665 (6029368753): ENTITY_AVAILABLE and
ENTITY_DEPARTING of a talker bound on the receiving interface; F3 round 2 adds
the term. The contract's `eq_bound` term reads a per-interface bound-talker
table in the mailbox block, which the core's `admit` port keeps equal to each
bound sink's talker (sink k is entry k), and which `ctrl_app_open()` fills
with the bindings the store restored
([design page](../../../docs/design/MAILBOX_SPLIT.md#discovery-and-the-adp-channels-filter)).
Only AVTP version 0 is read: the core discards an ACMPDU or ADPDU of another
version before decoding it (IEEE 1722-2016 4.4.3.4). TMR_NO_RESP runs from
the send the transmit ring accepts, so a probe owed behind other frames
holds its timer until it leaves, and its deadline comes from a clock read
after that send returns, never from one read before it.

A platform that restores bindings boots in this order: `ctrl_app_compose()`,
`acmp_nvm_init()` on the app's ACMP core, `nvm_store_boot()` with its port,
`nvm_store_service()` added as a centisecond consumer, then `ctrl_app_open()`;
the ACMP env's `persist` port calls `nvm_store_changed(NVM_G_BIND, sink)`.

## The composition

`ctrl_app` composes ADP always, and ACMP and lane F2's
[MAAP owner](maap/README.md) when the configuration supplies them: `acmp`
and `acmp_env` for ACMP; `maap_allocation`, the stream-address port
(`maap_csr_allocation` on the datapath CSR window), with `maap_ctx` and
`maap_preferred` for MAAP. Lane F2's `ctrl_app_start_maap()` is
`ctrl_app_start()` with those three fields given, and refuses a missing port.

- **The attach order.** `ctrl_app_compose()` attaches ADP, then ACMP (its
  tap stands in front of ADP's handler of the adp channel), then MAAP, and
  touches no mailbox register. `ctrl_app_open()` then opens every bound
  channel at the filter and enables each one's receive interrupt with the
  events' (`ctrl_loop_open()`): with all three, the adp, acmp and maap
  channels and no other. ACMP writes the restored bindings, ADP is enabled,
  and MAAP reads each interface's link and begins.
- **The timer slots.** ADP holds slots 0 to `MBX_N_IF` - 1, ACMP the next
  `MBX_N_IF` and MAAP the next: three disjoint runs, which a
  `_Static_assert` keeps inside the fabric's bank of `MBX_N_TIMERS` (16).
- **The refusals.** The composition is refused, with nothing opened, for a
  pool that cannot be carved, a configuration its module refuses (MAAP
  refuses an entity with no talker source), and a preferred MAAP range
  that starts outside the B.4 pool (IEEE 1722-2016 Table B.9) or runs past
  its end. A refusal stops the composition before the later modules attach.
- **The pass bound.** A pass of the three costs at most `CTRL_APP_THREE_PASS_MAX`
  mailbox accesses: the pass of ADP and ACMP (`ACMP_MBX_PASS_MAX`, 1,012 at
  one interface) plus MAAP's share of 568, its costliest action on each of
  the 8 events (48), its 2 records of the maap channel (20 + 48) and its
  poll on each interface (48). That is 1,580 at one interface and 1,659 at
  two. It is also the two modules' own pass bounds less what both count:
  `ACMP_MBX_PASS_MAX` plus `MAAP_MBX_PASS_MAX` (616 at one interface, 664
  at two) less the 6 accesses of each of the 8 event records. Every pass
  count of `acmp_mbx.h` and of the MAAP page holds in the composed loop
  with this pass in place of its own
  ([design page](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)).

After the open, initialize SRP on the application's static pool and call
`ctrl_app_attach_srp()` before entering the loop. This fourth attachment retains
ADP, ACMP and MAAP receive/filter bits, adds SRP's receive interrupt, and enables
the centisecond tick. SRP uses no one-shot timer slot. Its participant timers
share the tick; the three runs of fabric slots above remain disjoint.
A failed attachment preserves the running three-module composition.
With ACMP present, attachment also installs a composition-owned request per sink.
The ACMP callback copies the latest bind or unbind, preserving its sink index.
A fifth poll delivers requests after SRP service returns, using each sink's
configured interface. Transient refusal keeps the request pending and the loop awake.
VID 0 or VID >= 4095 sets the readable per-request `parked` state.
A parked request permits sleep until ACMP replaces or withdraws it.
Unbind and replacement supersede the prior request; no callback enters SRP.
The supplied ACMP SRP callback observes intent; it must not deliver it itself.
After SRP returns, the same poll reports matching per-sink Talker registration
to ACMP: Advertise or Failed enters SETTLED_RSV_OK; withdrawal reprobes.
The snapshot uses the configured interface and only the accepted binding.
Repeated registration is not a new event under Milan Table 5.30.
Both directions obey #678: no protocol entry occurs inside a port callback.
Other environment callbacks retain their original context.
Keep application and adapter storage alive until loop service stops.

`CTRL_APP_PASS_MAX` bounds all four modules: `ACMP_MBX_PASS_MAX` already
includes ADP, then add `MAAP_MBX_PASS_MAX` and `SRP_MBX_PASS_MAX`, subtracting
two copies of the shared event reads, then adding `CTRL_APP_SRP_FEEDBACK_MAX`.
Feedback costs at most four accesses per configured sink: clock, seed and
one timer re-arm on withdrawal; registration only stops or re-arms a timer.
The static maximum of 16 sinks contributes 64 accesses.
The result is 3,192 accesses at one interface and 4,041 at two. The SRP bound counts one maximum-size frame per
library transmit call, at most two calls per interface, receive readiness and
retry clocks, plus link/reset work. Binding delivery itself adds no mailbox access.
The feedback allowance covers the same poll's ACMP registration entries.
It excludes CPU work and external ports.
The SRP arm also builds U6/F6 with all four modules at each interface count:
exact interrupt mask, an idle HAL awakened by SRP alone, ordered attachment,
disjoint timer slots, full receive backlogs and the algebraic pass bound.
The exact-mask, SRP-only wake and algebraic-bound checks have named planted defects.

MAAP's allocation reaches ACMP's talker only through the integrator's
`source` port (`acmp.h`): the port reports `dest_mac_valid` and the stream's
destination, and the app does not connect it to the stream-address port.

`test_acmp_mbx.cpp` holds the composition's checks, in both ACMP arms: U6
(the attach order, every channel and its interrupt, disjoint slots each
holding its own module's arm, MAAP acquiring its range beside the other
two over four seconds, every MAAP frame sent from its interface's own
unicast MAC, where the maap row admits a DEFEND (IEEE 1722-2016 B.2.1)),
U7 (the refusals) and F6 (events and the acmp and maap rings backlogged:
the worst pass 231 accesses at one interface and 233 at two, and the bound
against the two modules' own).

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
| `reentry_debug`, `reentry_release` | `test_adp_reentry.cpp` | Every port/core entry pair, same and cross instance; both inline-expiry regressions. Assertions in debug, counted refusal in release. |
| `walk` | `adp_walk.cpp` | the processor's own ADP walk, reused: 36 cells of its Table 5.51 transcription and its frame builder, on the firmware and the model |
| `acmp` | `test_acmp.cpp`, `test_acmp_mbx.cpp` | the ACMP core over fake ports (every listener command, response, timer and SRP event in every state Table 5.30 gives it, each response field by field; the talker's answers; the lock; responses keyed on the consumer's unique ID; sequence IDs; one timer per interface; owed frames and the response before its notification; the discovery machine cell by cell; the saved record; the no-callback guard), then the adapter on the model: the channel and its filter, the timer slot and the tag rule, the ADP channel's tap, the gPTP pair, the adapter's refusals, every path's service cost (the H-ACMP and H-DISC hooks), an owed response behind a full ring under a HAL that sleeps, full backlogs and the composition, with ADP, ACMP and MAAP composed together ([The composition](#the-composition)) |
| `acmpwalk` | `acmp_walk.cpp` | the processor's own ACMP expectations, reused: its F05.3 matrix model of Table 5.30 in lock step with the firmware (88 cells), its Table 5.54 transcription (33 cells) and its talker suite's F05.11 constants, each difference between the two asserted to be what it is |
| `acmpnvm` | `test_acmp_nvm.cpp` | the core and its binding owner on lane F1's store over the host flash model, at the shipping 1x1 shape: a bind saved and fast-connected after a power cycle, an unbind saved, the started flags, an unread slot refusing persistence, a refused record, the roll-back and every other group forwarded, and a D3 roll-back (at the port and at a boot) leaving the bindings applied |
| `acmpif2` | `test_acmp_mbx.cpp`, `acmp_if2.cpp` | the adapter's tests again with the firmware and the model compiled against the contract elaborated for two AVB interfaces (written into the build by `gen_mailbox.py`): each interface's timer slot, tag, gPTP pair, bound-talker table and every latency path, and the three-way composition |
| `entity` | `entity_fields.cpp` | every shipped config's ADPDU fields, against the fabric's own sources |
| `maap`, `maap_if2`, `maap_debug` | `test_maap.cpp`, `test_maap_mbx.cpp`, `test_maap_debug.cpp` | Annex B, stream CSR output, H-MAAP at one/two interfaces, and synchronous reentry refusal |
| `rv32` | the portable set | a freestanding RV32I build whose only open symbols are C-library string, format and assertion functions and libgcc helpers |
| `lwsrp` | `lwsrp_port.cpp` | the pinned submodule, or `--lwsrp DIR`: lwSRP's own MRP core on the port layer, through the SRP channel, timed by the fabric's ticks; DIR must be lwSRP at the pinned revision with `src/` unmodified |

The [SRP evidence](srp/README.md#evidence) adds declaration, lifecycle, latency,
debug, shape and processor-wire arms at one and two interfaces.

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
SRP start and stop, discovery, the store's mark and the notification. Three
differences are asserted, field for field, to be exactly what they are:
UNBIND_RX_RESPONSE's talker fields (the processor echoes them; Milan Table
5.36 gives 0), the ACMP status after a TMR_RETRY with the talker discovered
(the processor zeroes it; 5.5.3.5.30 step 2 sets none), and the lock's refusal
status (the processor sends 13, TALKER_MISBEHAVING in IEEE 1722.1-2021 Table
8-3; the firmware 16, CONTROLLER_NOT_AUTHORIZED). A fourth, DISCONNECT_TX of
an unknown source, is asserted on the firmware's half only (TALKER_UNKNOWN_ID,
Milan 5.5.4.2 step 1); the processor's SUCCESS is read from source
(`KL_acmp_talker.sv:1301-1306`), not walked. Milan 5.5.2.7 says DISCONNECT_TX
"always returns SUCCESS"; 5.5.4.2 governs, since 5.5.2.7 is an overview that
defers to 5.5.4 and 5.5.4.2 is the "shall" procedure. The four are processor
issue #168.

### Planted defects

`--self-test` writes each defect of `ctrl_mutants.py` (with lane F3's
`acmp_mutants.py` and lane F2's `maap_mutants.py` appended) into a copy of
this tree and requires the arm it
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
own MAC not the entity's (`unit`). Lane F3 adds 273 defects for the
`acmp`, `acmpwalk`, `acmpnvm` and `acmpif2` arms (with the driver's and the
model's for the bound-talker table in `unit` and `model`): a defect in each clause step, each
response field, each guard term, each timer, the owed queue and the #653
release, discovery's every guard, each port's re-entry flag, the saved
record, the adapter's slot, tag and tap, extra mailbox accesses on each
measured path, each backlog figure understated, and the binding owner's
forwarding; round 2's AVTP version check, TMR_NO_RESP from the accepted send,
the slot range, the per-interface wiring at two interfaces, the binding
record's flags and length, the D3 roll-back, each timer across the
millisecond wrap and the bound-talker table; round 4's TMR_NO_RESP from a
clock read before the probe's send; round 6's for the composition with
MAAP: each overlap of MAAP's slots with ACMP's or ADP's, MAAP attached after
the open, before ACMP, started in the compose or never, its channel left
unbound, each refusal dropped or moved off its boundary, lane F2's entry
taking no port or dropping its range, and a MAAP handler overrunning the
three-way pass bound; round 7's: MAAP's source MAC or the filter's own MAC
keyed by interface (`acmpif2`), and the three-way bound without MAAP's
share or with MAAP's poll on one interface only; and eight wrong numbers in
`acmp.h` itself, which the tests
catch because they spell the standards' values (`acmp_fake.hpp`, `spec`),
never the header's. They are `acmp_mutants.py`'s table, rounds 2, 4, 6 and 7's
in `acmp_review_mutants.py`. Round 6 re-plants four defects whose text the
composition moved, each with its test and words: the pool bound after the
mailbox (F0) and ACMP never composed read the compose's ACMP block, and lane
F2's MAAP receive interrupt and filter bit, which the app no longer writes,
are dropped where `ctrl_loop_open()` writes them. Lane F2's own defects
(96, `maap_mutants.py`) grade the `maap`, `maap_if2` and `maap_debug` arms;
its README lists them. Every test of those
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

Needs host C/C++ compilers, GoogleTest, GoogleMock, and PyYAML (the
`acmpnvm` arm also runs the builder for its shape, as lane F1's gate does).
RV32 checks use the SDK from `scripts/ci_rv32_sdk.py`.
Both firmware gates require RV32 in `firmware-unit`.
Freestanding declarations avoid the SDK's hosted C headers.
GCC supplies its own freestanding integer and varargs headers.
`MILAN_RV32_CC` selects an explicit compiler for local validation.
See [the harness](../gtest/README.md#rv32-object-builds) for evidence limits.
The SDK distribution is `ilp32d`; the core uses RV32I/ILP32.
The CI firmware step also requires the control mutation campaign.

Initialize `third_party/lwSRP` at its recorded gitlink before running the gate.
An alternate `--lwsrp` checkout must match `ctrl_arms.LWSRP_REV`, currently
`9197193e47a6bb1c45a56d90a18c1784123aba44`, with every compiled source unchanged.
Moving either pin requires a reviewed change.
The pin is published on public lwSRP `main`, including PR #12 and PR #15.
Anonymous HTTPS checkout needs no repository credentials.

## Linked size

Two independent measurement fixtures survive the F3/F4 merge.
`ctrl_image.py` retains F3's ADP/ACMP/MAAP and saved-state composition below.
`ctrl_srp_image.py` measures ADP/ACMP/MAAP/SRP with the entity-sized pool,
verified bare-metal runtime archives and an 8192-byte stack reservation;
see the [SRP recipe](srp/README.md#evidence).
Neither fixture is a shipping or booted image, and neither connects the
integrator's live stream, persistence and media owners completely.


`ctrl_image.py` links the firmware as a Mark II platform composes it
([`rv32_image/image_main.c`](test/rv32_image/image_main.c)): the app with
ADP, ACMP and MAAP, the binding owner, MAAP's allocation output on the
datapath CSR window, and lane F1's store on the LiteSPI port at the shape's
container, booted in the order above, every source compiled with its gate's
RV32I flags plus `-DNDEBUG`, one section per function and object, and linked
at `--gc-sections` into one 128 KB block-RAM region
([`image.ld`](test/rv32_image/image.ld)), so only what the composition
reaches counts (#665, acceptance addition 6030870481). The integrator's
owners (the lock, the sources, SRP, the notifier, every other saved group,
the CSR window's two accesses) are stubs; the C runtime the SoC's libbase supplies is linked from byte-loop
stand-ins, reported apart (64 bytes: `memset` and `memcpy`, the only ones the
composition reaches); lwSRP's pool is the host tests' 256 bytes in this fixture; `ctrl_srp_image.py` measures the entity-sized pool; the stack is not counted. `--base REV` measures another revision's
firmware with the same harness.

No library is linked. The pinned SDK's `libgcc.a` is built for its one
multilib, `rv32imafd` with the `ilp32d` ABI, so it cannot link into a
soft-float RV32I image. The arithmetic helpers GCC calls on RV32I come from
[`rv32_image/image_arith.c`](test/rv32_image/image_arith.c) instead: every
helper the `rv32` arm admits (none is a floating-point one), each a
shift-and-add or shift-and-subtract loop that must be a leaf. A helpers
object that leaves a symbol open or calls a helper is refused, since GCC
lowers a `*` inside `__mulsi3` into a call to `__mulsi3`. In the SoC image
LiteX's `libcompiler_rt` supplies them. They are reported apart: 508 bytes,
`__lshrdi3`, `__muldi3`, `__mulsi3`, `__udivdi3`, `__umoddi3` and
`__umodsi3` (the only ones the composition reaches; MAAP's code brings
`__umodsi3`) and their two divide loops.

Before any figure is read, the linked ELF is audited, and any finding
refuses the measurement:

- a little-endian ELF32 RISC-V executable whose `e_flags` are 0: no RVC, the
  soft-float ILP32 ABI, not RVE or Ztso;
- one architecture attribute, `rv32i` and its version alone;
- every word of every executable section an RV32I base instruction (no M,
  A, F, D, C, Zicsr, Zifencei or privileged instruction);
- no symbol the linked objects reference and none defines. A weak one links
  to address 0 and leaves no trace in the image, so the inputs are read.

```sh
python3 sw/firmware/ctrl/test/ctrl_image.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
```

The self-test holds the controls, 33 checks: the helpers against the host's
own arithmetic (the edges, every shift count and 200,000 random pairs), the
leaf rule and two helpers it refuses, a probe linked as the image is and
every RV32I instruction form passing, eleven foreign instruction words, an
RV32IM attribute, ten foreign header fields and a weak symbol refused, and
the measurement itself at the shipping shape: passing, and refusing a helper
library built for RV32IM with the soft-float ABI (by the audit), one built
for the pinned SDK's own multilib (at the link) and a helper that calls
itself.

`ctrl_image.py` prints the compiler's identity first: its version line and
the sha256 of its `libgcc.a`, which is not linked. That is what names the
toolchain of a table. Another build at the SDK's path prints another
identity.

At lane F3 round 6, with the pinned SDK of `scripts/ci_rv32_sdk.py`
(`riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256
`d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`), whose
compiler's version line reports GCC 14.3.0 from the SDK build
`2021.11-18033-g83947c7bb6` (`ctrl_image.py` prints the line in full) and
whose `libgcc.a` has sha256
`d8ebca8cf6ad31cd50695f79e91e86a716d3b1761fbbefd5ee7b0627a2d0af58`, against
dev `e21c1ca0` (the app with ADP and MAAP through `ctrl_app_start_maap()`,
no ACMP, the same store):

| Shape | STREAM_INPUTs / OUTPUTs | text | rodata | data | bss | total | of 128 KB |
|---|---:|---:|---:|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8` (shipping) | 2 / 2 | 33,444 (+10,768) | 748 (+32) | 0 (+0) | 12,416 (+4,848) | 46,608 (+15,648) | 35.6 % |
| `endstation_ax7101_8x8` (largest) | 9 / 9 | 33,448 (+10,768) | 748 (+32) | 0 (+0) | 22,784 (+4,848) | 56,980 (+15,648) | 43.5 % |

Every image passes the audit (`rv32i2p1`, 8,361 and 8,362 words at the
head, 5,669 and 5,670 at the base). The text includes the 64 bytes of
runtime stand-ins and the 508 bytes of helpers, at the head and the base.

The static objects: the app, 7,904 bytes at every shape (ACMP's state 4,720
at its maxima of 16 sinks, 16 sources and four interfaces, the loop 1,748,
MAAP's 1,104, the pool's header 204, ADP's 124), the store's stage (3,344 at the shipping
shape, 13,264 at the largest), its payload buffer (136, 576), chunk (256)
and state (288), and the pool's arena (256). ACMP's state does not follow
the shape: the sinks and sources it serves are a run-time configuration
within those maxima, so the shape moves only the store's buffers and a few
bytes of code.
