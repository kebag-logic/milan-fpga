<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Bare-metal MSRP and MVRP

F4 implements SRP on the mailbox using the pinned lwSRP submodule.
The firmware owns interface identity, static storage, admission and output ports.
lwSRP owns the MRP parser, Applicant, Registrar and timers.
The default fabric build and shipping image are unchanged.

## Contents

- **[Composition](#composition)** -- Boot order, allocation and asynchronous ports.
- **[Protocol commitments](#protocol-commitments)** -- Declarations, timers and output ordering.
- **[Evidence](#evidence)** -- Host, freestanding, coverage, mutation and timing checks.
- **[Processor comparison](#processor-comparison)** -- Reused stimuli and normative differences.
- **[Integration still owed](#integration-still-owed)** -- Application wiring and target release evidence.

## Composition

Generate `srp_entity_gen.h` with `srp_entity.py` from the selected builder config.
Force-include it in every SRP translation unit; there is no fallback shape.
The source and sink counts equal the entity's advertised counts, including CRF.
The shape tests independently compare them with the builder's fabric constants.

Statically allocate `srp_mbx`, `ctrl_pool`, an aligned `SRP_POOL_ARENA_BYTES`
arena and one `srp_source` array per interface.
Initialize the pool with `srp_pool_classes`, then bind it with
`shlan_port_bind_pool` before creating SRP.
Do not rebind or destroy the pool while any participant owns storage.
`shlan_printf` uses the existing optional debug sink.
There is no firmware heap or operating-system dependency.

The pool has two small and two large blocks per interface, plus
`16 + 3 * sources + 4 * sinks` medium blocks per interface.
The arena includes conservative allocator overhead for each block.
Receive-interest filters retain every valid Class A Domain value, output Listener
IDs, bound input Talker IDs and required VLANs.
Quiescent, undeclared MT attributes are reclaimed under Table 10-3 note 11.
`refused` counts unsuccessful attempts, including retries, rather than records.
Exhaustion is counted and refused; it cannot overwrite another reservation.
The pool is a finite capacity, not a claim that arbitrary peer churn always fits.

Initialize the adapter with interface MACs, source TSpecs/allocation state,
link rate, and a licence output callback.
The explicit application composition starts with `ctrl_app_start_maap`.
Initialize SRP on that application's pool using the same interface MACs.
Then call `ctrl_app_attach_srp` before servicing the loop.
Supply ACMP through the application configuration when composing all four modules.
Attachment follows ADP, ACMP and MAAP, retaining each receive and event enable.
It opens SRP reception and its interrupt, and enables centisecond delivery.
SRP owns no one-shot fabric timer slot: lwSRP timers use the shared tick.
The other three modules retain disjoint runs of `MBX_N_IF` slots.
The isolated adapter uses `srp_mbx_attach` before opening its loop.
Only one adapter may own the library's global centisecond dispatch.
Each fabric TICK record counts elapsed centiseconds; NOW_MS is a separate
millisecond timestamp. Coalesced ticks are drained without dropping elapsed time.
Destroy detaches the adapter, releases all participants and revokes active licences.
Destroy before reinitializing an already initialized instance.
Attach reads each interface's current mailbox link level.
Polling reconciles that level even without another LINK record.
A held DOWN record can disappear when the level recovers.

`ctrl_app_attach_srp` wires the ACMP environment's SRP port into a static
latest-request slot per sink. It refuses a sink count beyond the generated
SRP shape or insufficient loop-poll capacity before attaching anything.
The callback copies bind/unbind intent and forwards it to the original observer.
The observer must not deliver the binding itself or reenter a protocol.
Other ACMP environment callbacks keep their original context.
After SRP's poll returns, a composition poll calls
`srp_mbx_bind(interface, sink, identity, destination, VID)` for pending requests.
The sink index and its configured interface are preserved independently.
An accepted request retires; a refusal stays pending and keeps the loop awake.
Unbind or replacement supersedes that sink's previous pending request.
Keep both objects alive until loop service stops, then destroy SRP and the pool.
Recompose the application before attaching another adapter.
A null identity removes a binding; false leaves the old binding unchanged.
Retry after owed transmission commits and retained reception completes or expires.
Bindings may share a StreamID while differing in destination or VID.
The interface reconciles one Listener declaration from all eligible bindings:
Ready contributes 2, AskingFailed contributes 1, and their union is ReadyFailed.
An ineligible binding contributes nothing and cannot withdraw another's request.
Ready contributes only after its own VLAN membership commits.
Shared bindings retain their Listener and VLAN until the final user leaves.
Replacement preserves the shared Applicant state until reconciliation.
Consecutive replacements before service preserve that state too.
Reconciliation withdraws Ready when its last eligible binding disappears.
The final binding preserves the current Domain VID.
Otherwise, it releases its VID regardless of prior eligibility.
All ports are serialized. Output callbacks must enqueue work and return;
they must not synchronously call an input port or advance the loop.
The adapter asserts on reentry in debug builds and counts/refuses it in release.

## Protocol commitments

Each physical interface has independent MSRP and MVRP participants.
The adapter accepts the FC SRP mailbox channel's untagged Ethernet records,
validates destination, EtherType, length and interface, and preserves interface
identity on transmission. The library validates a whole PDU before applying events.
Malformed PDUs increment `malformed`; local allocation refusals increment `refused`.
A refusal retains the complete record in one static buffer.
Its interface, arrival timestamp and payload remain unchanged.
Later SRP records and binding changes wait behind it.
Each poll retries after pending events, ticks and owed output.
Earlier applied attributes remain applied; replay includes every later attribute.
Each poll attempts reception once.
The fabric centisecond event supplies another service opportunity.
Storage recovery completes the payload on the next eligible poll.
A continuing allocation refusal expires after 1000 ms from the original arrival.
This local recovery policy allows one periodic interval.
It is checked at each eligible receive attempt.
A record already delayed in the RX ring gets no fresh retry window.
A failed participant recreation checks the same deadline.
A successful retry takes precedence over expiration; pending events and owed
output still precede that retry.
Expired refusal clears the retained record and increments `rx_discarded` once,
without incrementing `received` or `malformed`.
Earlier applied attributes remain; MRP refresh and aging recover the lost suffix.
Later input on every interface and binding calls can then proceed.
This recovery limit does not enlarge the 10 ms service budget.
Destroy cancels it; link reset cancels only its interface's record.

Every output starts with Talker Advertise or Talker Failed (Milan 5.5.2.7).
Admission charges Ethernet overhead and a 75% link-rate ceiling.
Unallocated outputs report insufficient resources; bandwidth failures report
insufficient bandwidth. A registered Ready or ReadyFailed Listener can enable
an admitted output only after the applicable MVRP Join commits (Milan 4.3.2).
A binding declares Ready for a matching Advertise, AskingFailed for a matching
Failed, and withdraws when its retained registration expires.
Ready follows the accepted MVRP membership request (802.1Q 35.1.2.2).

Startup declares Domain class 6, priority 3, VID 2 and MVRP membership in VID 2.
A valid peer Class A Domain changes the priority and VID; link restart restores
the defaults. A changed VID is reserved before old declarations are withdrawn.
A bound sink retains an old VID it still needs.

| Timer | Configured value | Authority |
|---|---|---|
| JoinTime | 20 centiseconds | IEEE 802.1Q-2018 10.7.11; Milan Table 4.3 |
| LeaveTime | 500 centiseconds | Milan Table 4.3 |
| Periodic | 100 centiseconds | IEEE 802.1Q-2018 10.7.11; Milan Table 4.3 |
| LeaveAll | Integer draw strictly between 1000 and 1500 centiseconds | IEEE 802.1Q-2018 10.7.11 |

Build lwSRP with `LWSRP_MILAN=1` for Milan v1.2 4.2.7.2.2.
Only MSRP opts in: IN/rLv issues Lv and enters MT immediately.
The corresponding Talker licence or Listener request is revoked in that pass.
MVRP retains the generic IEEE 802.1Q Table 10-4 Registrar behavior.
A withdrawal in LV does not restart LeaveTime (#608 and processor #134).
The original five-second deadline revokes the Talker licence.
Temporary storage refusal defers application until capacity returns or the
receive recovery limit expires.
Timer withdrawals retry at each centisecond; retained RX retries at polls.
That delay is measured from the original deadline or arrival.
Exhaustion never grants a fresh service or protocol timing budget.
An over-budget recovery remains a timing failure.
Expiry processing precedes later RX, including a tick still in the event ring.
A subsequent same-pass registration cannot erase the owed stop notification.

An accepted `TX_HEAD` write commits the complete frame and Applicant transition.
A refused send retains identical bytes and interface until accepted.
SRP RX waits behind that owed record; Registrar clocks continue to run.
Each LINK event preserves the lifecycle, including down/up between service passes.
Observed level changes apply the same reset and receive fence.
A repeated UP also recreates state because event coalescing may hide the down edge.
Reset cancels only that interface's owed output and restores the default Domain.
It fences that interface's already published RX prefix at the current RX_HEAD.
Those records are consumed without registration; other interfaces keep their input.
Frames published before lifecycle service are conservatively discarded for that
interface, including frames received after the physical recovery.
Fresh declarations after that fence are required before a licence can restart.
A failed recreation owns neither participant, counts a refusal and retries later;
the surviving interface continues service.

## Evidence

Run the common firmware gate from the repository root:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
```

The gate requires the exact lwSRP gitlink and compiled source bytes.
The pinned SDK distribution is named `ilp32d`; the cacheless core build uses
`-march=rv32i -mabi=ilp32`, as required by #679.
Minimal freestanding headers and ELF/runtime checks prevent hosted-libc leakage.
Object totals include the library and adapter; compiler stack frames are reported
separately and do not establish a whole call-chain bound.
`ctrl_srp_image.py` also links a size fixture containing the reachable control loop,
ADP, ACMP, MAAP, mailbox, SRP, binding-delivery queue and their static storage.
`ctrl_image_runtime.py` builds its memory primitives and integer helpers with the
same compiler from externally provisioned Picolibc, compiler-rt and LiteX sources.
Their hashes, commands, ELF sections and symbol sizes accompany the measurement.
The fixture has no board reset entry and observes licences in static storage.
It is size evidence, not a boot or routed-resource result.

```sh
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py --picolibc "$PICOLIBC" \
  --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --output "$RUNTIME"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py \
  --config configs/endstation_ax7101_1x1_tdm8.yaml --interfaces 1 --output "$IMAGE" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

Repeat for `endstation_ax7101_8x8.yaml` and two interfaces.
For the base comparison, export its control sources and pass `--without-srp`
with `--ctrl-source "$BASE_CTRL"` to the same fixture and runtime.
The report separates text, read-only data, initialized data, BSS, reserved stack
and alignment; the arena is already in BSS and must not be added twice.
The reserved 8192-byte stack is a measurement assumption, not a call-chain proof.

GoogleTest/GoogleMock exercise one and two interfaces, every shipped entity shape,
allocation failures, malformed inputs, declaration changes, reset, reentry,
backpressure and timer ordering. The adapter has no coverage exclusions.
`srp_mutants.py` ties each named case to a defect and its failed observable;
build failures do not count as catches.
`srp_binding.hpp` feeds real BIND_RX and PROBE_TX_RESPONSE records through
all four modules, checks deferred delivery, refusal/recovery, expiry, unbind,
replacement and interface/sink isolation, with named plants at both interface counts.
`srp_app.cpp` counts actual mailbox accesses in the event, refused-receive,
retained-receive poll, transmitting poll, maximum RX/TX record and full-pass paths.
Each bound term has a named planted understatement at one and two interfaces.
Poll-allocation tests exhaust storage after successful reception.
Separate receive tests exhaust it before accepting a mailbox record.
They cover mixed attributes, partial completion, repeated refusal and recovery.
They also cover interface ordering, link fences and destruction.
The retry-removal plant must fail the retained-payload regressions.
Wire-valid Domain floods exceed the actual pool without artificial exhaustion.
They check later withdrawal and binding progress at one and two interfaces.
Boundary, clock-wrap and failed-recreation cases grade the original deadline.
The bound-removal plant must fail the oversized-record regression.
Higher-version messages and atomic invalid-value rejection have wire cases.

The published lwSRP [Applicant tests](https://github.com/kebag-logic/lwSRP/pull/15)
merged as PR #15 at `9197193e`.
That public pin includes branch `f4-applicant-notes`.
`applicant_receive_conditions_follow_link_mode` tests Table 10-3 notes 4/5.
`pending_applicant_joinin_obeys_note_four` adds both link modes in VP.
The `point-to-point-condition`, `pending-point-to-point-condition` and
`shared-in-condition` reversals must fail their named tests.

The H-SRP desk test timestamps the actual mailbox access path at 100 ns per access.
It adds one aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty per
action. It records full elapsed time and subtracts only the applicable normative
Join wait; periodic and Leave expiry start at their original deadlines.
All overhead shares the single 10 ms service allowance in
[FR_NFR 3.4.1](../../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing).
An 11 ms full-ring stall deliberately fails that budget predicate without
restarting the origin when space becomes available.
These are explicit host-envelope assumptions, not measured target execution or
wire-departure latency. Target scheduling, ingress, egress and arbitration must
validate those assumptions and the remaining normative margin before release.

## Processor comparison

`srp_reuse.py` verifies each source blob against the processor gitlink before
extracting the SRP-top wire builders and stream-FSM Applicant tables.
`srp_walk.cpp` applies their two-class Domain vector, stream near misses,
Advertise/Failed replacement, Run-B LeaveAll lanes, Applicant startup/received
rows, per-interface Listener registration and truncated frames through the
firmware mailbox. This is a selected wire differential, not an exhaustive walk
of every processor state. The complete original processor suites run separately.

| Difference | Processor stimulus/expectation | Firmware result and authority |
|---|---|---|
| D1, resolved | `srp_stream_fsms` section E expects immediate loss on Talker Lv from IN | Firmware agrees under Milan v1.2 4.2.7.2.2. A later Lv in LV retains the original LeaveTime deadline; the #608 cases remain covered. |
| D2 | Sections B/E encode Listener withdrawal with FourPackedEvent Ignore (0) | Retain the last declaration subtype on Lv. IEEE 802.1Q-2018 35.2.2.7.2: Ignore is not a Listener declaration to register or withdraw. |

Milan v1.2 4.2.7.2.2 governs D1; IEEE 802.1Q-2018 35.2.2.7.2 governs D2.
JoinIn/JoinMt replacing Advertise with Failed or the reverse uses 35.2.6;
conflicting New registrations retain Failed precedence until replacement/expiry.

## Integration still owed

F3 is present in the Round 8 merge base.
The explicit composition now runs ADP, ACMP, MAAP and SRP.
The composition owns ACMP binding-port delivery, cancellation and retries.
Target integration still supplies live stream configuration and MAAP allocation changes.
It also connects the existing fabric licence output.
The desk callback proves output ordering, not a connected target licence register.
The mailbox SoC skeleton also needs its separate target integration and timing
validation. No register-map change is made here.

The lwSRP pin is public `main` at `9197193e`.
Round 6 adapts to its recoverable receive-allocation contract.
The earlier claim that production needed no adaptation was incorrect.
Two independent reviews, candidate-merge gates and deployment
remain separate obligations; this lane changes neither shipping ownership nor RTL.
