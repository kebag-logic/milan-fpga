<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# AECP firmware owner

Lane F5 of [#665](https://github.com/kebag-logic/milan-fpga/issues/665) adds
an opt-in AECP owner beside ADP, ACMP, MAAP and SRP. The default fabric build
and shipping image continue to use their existing owners. The normative
references are IEEE 1722.1-2021 7.4, 7.5 and 9.3, Milan v1.2 5.4, and
[NFR-SCOUT-02/03/08](../../../../docs/reference/FR_NFR.md).

## Contents

- **[Contract and integration](#contract-and-integration)** -- Portable ownership, observations, callback boundaries and application boot order.
- **[Non-AEM message contract](#non-aem-message-contract)** -- Clause-based handling of address access, AV/C, vendor, HDCP and reserved types.
- **[Verification and limits](#verification-and-limits)** -- Reproducible wire comparisons, timing evidence and linked-image limits.

## Contract and integration

[`aecp.h`](aecp.h) is a portable C11 API over caller-owned storage and typed
environment ports. The core has no register, mailbox, image-file, heap, thread
or operating-system dependency. [`aecp_image.c`](aecp_image.c) validates the
generated AEM image and exposes descriptor spans; [`aecp_entity.py`](aecp_entity.py)
uses the existing builder generators and derives capacities from their output.
Every advertised descriptor is served by READ_DESCRIPTOR. Names and scalar
changes are reflected in subsequent descriptor reads. ENTITY available_index is
observed from the current ADP owner on the ingress interface (IEEE 7.2.1 and
6.2.2.15). The application and mailbox adapters pass this observation without
copying it into the image. The fabric reference serves the image constant; the
wire fixture has no advertisements and uses zero on both sides. The composed
application test emits N advertisements and requires a subsequent read to see N.

The command owner implements entity availability, acquisition refusal and locks;
configuration, names, stream formats and information; rates and clock sources;
IDENTIFY control; START/STOP; registration; AVB information, AS path, counters,
audio mappings and dynamic information. MVU implements Milan information and
system unique ID. Other AEM commands return NOT_IMPLEMENTED, except the required
BAD_ARGUMENTS response to a solicited IDENTIFY_NOTIFICATION. The command model
consolidation remains owed while
[processor #73](https://github.com/kebag-logic/protocol-processor/issues/73)
is open.

Each AVB interface has its own registration table, controller liveness timers,
source MAC and transmit destination. Locks, entity configuration, descriptor
values and system ID belong to the entity. Physical observations use the
stream descriptor's AVB interface. The API accepts one or two interfaces, with
16 controller registrations per interface. This preserves the ingress contract
of [processor #69](https://github.com/kebag-logic/protocol-processor/issues/69).

Ports must return without calling a core entry point synchronously, including
on another instance. Read ports answer a snapshot or explicitly report its
absence. The start port queues work; `aecp_start_done()` is delivered from a
later loop pass. Reentry is asserted in diagnostic builds and counted/refused
otherwise. One response remains owed through backpressure. Notifications follow
that response, exclude its requester, and advance each recipient's own sequence.
Counter notifications are limited per descriptor from the latest recipient's
completed transmission. Under the [2026-10-12 #726 ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685),
FRAMES_TX/RX snapshots carry per-AVTPDU 32-bit totals.
TX resets at talker start; RX resets on not-bound to bound and retains unbind totals.
The observation port supplies those values; the protocol core does not recount packets.
Every counter update, including healthy traffic, must call `aecp_changed()` with the COUNTERS event (bit 3, value 8).
The [gap check](../../../../tb/verilator/milan_dp/stream_counter_f5.py)
uses this unchanged core and mailbox adapter, two registered recipients,
and a two-millisecond transmit stall at both descriptor shapes.
See the [counter evidence](../../../../docs/testing/726_STREAM_COUNTERS.md) for measurements.
Milan 5.4.5.2 Table 5.22 remains the notification rate limit.
Controller probes use a 30-60 s monitor interval,
250 ms retry and eventual targeted deregistration. Locks expire after 60 s.

The guard covers every public protocol and saved-state input.
It is shared across AECP instances on the event loop.
Queries refuse without writing output parameters.
Initialization checks before touching potentially uninitialized destination storage.
Its refusal increments the active caller's counter; others increment the destination's.
The diagnostic build defines `CTRL_REENTRY_ASSERT`.

Unavailable notification snapshots retain their event and retry after 1, 2, 4, then every 8 ms (`AECP_RETRY_MAX_MS`, #665).
The first failure of a round schedules the next round; a delivered notice resets the wait.
Solicited responses never wait on a retry, so their 240 ms bound (IEEE 1722.1-2021 9.3.2.6) is untouched.
Other eligible snapshots continue during that wait.
The retry timer permits the event loop to sleep.
Backpressure retains the completed snapshot and its remaining recipients.
The event scans walk only the events holding a notice or a retry, linked in descriptor order through their rows (`aecp.live`), and the registry scans visit only the used registrations (`aecp.used`), so a record's pass no longer walks every descriptor (#665).
`aecp_open` relinks every row, so what was set before the open is seen.
`aecp_find` answers from an index of the model's keys that `aecp_init` builds (`aecp.runs`, `aecp_index`): a configuration's descriptors of one type, held as one run from index 0, are found at their position, and a key outside the indexed configurations and types of IEEE 1722.1-2021 Table 7-1, or placed otherwise, is scanned for as before (#665). The firmware never changes a key after `aecp_init`; the self-test's cases that do rebuild the index with the change, and its fixture fails any case that leaves `aecp_find` answering differently from a scan.

[`aecp_mbx.c`](aecp_mbx.c) attaches the AECP channel and one timer slot. Accepted
TX_HEAD publication and completed TX_TAIL retirement are separate events. The
adapter retains completion cookies until the final frame words retire and reads
the clock then. A stale clock observation cannot move the completion time back.

[`ctrl_app_aecp.h`](../app/ctrl_app_aecp.h) composes the owner with the existing
application without changing its default entry point. The platform supplies the
physical observation/apply ports and static descriptor, map and event storage.
Boot in this order: generate/load the model, compose AECP, initialize its NVM
adapter, boot/service the saved-state store, settle restored values and maps,
then open AECP and attach SRP. The bridge restores the combined channel filter
and interrupts after SRP attaches. Its poll service forwards ACMP bindings,
START/STOP, persistence and deferred notifications. An UNBIND_RX response must
be accepted before the corresponding MEDIA_UNLOCKED notification is eligible
([#653](https://github.com/kebag-logic/milan-fpga/issues/653)). START/STOP
applies through `acmp_set_started`, which writes the sink's started level to
the mailbox's [publication block](../../../../docs/design/MAILBOX_SPLIT.md#the-publication-block)
before it returns; the response leaves on a later pass (#665).

[`aecp_state.c`](aecp_state.c), [`aecp_maps.c`](aecp_maps.c) and
[`aecp_nvm.c`](aecp_nvm.c) implement
[#637](https://github.com/kebag-logic/milan-fpga/issues/637). Saved scalars use
the live validators. A saved map is accepted atomically or refused as a whole.
Absent maps start from generated identity defaults, clipped to a restored input
format. A refused saved map retains the default map and rolls its input format
back when required to preserve that map. An emptied map is saved as a framed
record whose entries are all UNUSED, never as an erased record, so an empty list
and a non-default one each come back across the store's power cycle
([#763](https://github.com/kebag-logic/milan-fpga/issues/763); Milan v1.2
5.3.9.1, 5.3.10.1). Live format changes cannot orphan
existing mappings. Map partitioning follows advertised geometry and output
stream/channel ownership is global across output ports. An accepted default-valued
SET still establishes a persistent override. Store dirty marks are queued for
later polling. The reserved system-ID/media-clock-reference saved spans remain
erased; system unique ID is volatile until a record-format decision is made.

## Non-AEM message contract

| Message type | Decision and clause | Reference wire difference |
|---|---|---|
| AA_COMMAND (2) | AA_RESPONSE / NOT_IMPLEMENTED; IEEE 9.4.4/9.4.5. Type-specific body is retained. | None. |
| AVC_COMMAND (4) | AVC_RESPONSE / NOT_IMPLEMENTED; IEEE 9.5.4/9.5.5. Type-specific body is retained. | None. |
| VENDOR_UNIQUE_COMMAND (6) | Milan MVU commands as above; other protocols/commands return NOT_IMPLEMENTED under IEEE 9.6.4. | System-ID difference recorded below. |
| HDCP_APM_COMMAND (8) | HDCP_APM_RESPONSE / NOT_IMPLEMENTED with zero data length, preserved sequence, flags and fragment offset; IEEE 9.7.4. | The reference echoes the HDCP data and length; the core sends no HDCP data. |
| Reserved (10, 12), EXTENDED_COMMAND (14) | Ignore: IEEE Table 9-1 and 9.2.2.4 assign no defined protocol handling to these values. | The reference returns an odd message type with status 1; the core emits nothing. |
| Response types | Ignore unsolicited responses, except matching AEM availability responses (IEEE 9.3.2.5). | No additional response generated. |

`Core.NonAemMessageTypesFollowTheirOwnContracts` checks these decisions,
including the complete HDCP fixed header, transmit stalls and both interfaces.
No reserved message type is interpreted as an AEM command.

## Verification and limits

The [firmware bank](../test/test_ctrl_firmware.py) includes the composed AECP
tests at one and two interfaces, all five generated shapes and the reentry
guard. [`aecp_mutants.py`](../test/aecp_mutants.py) names every test and requires
each source defect to fail its named assertion in a completed run. It plants into
a copy of this tree and of the saved-state store beside it, so a store defect that
reads an all-UNUSED map payload as erased is graded against the AECP owner's
power-cycle test, which no store suite catches (#763). The full
[coverage gate](../../gtest/README.md) measures the eight new production files
at 100% lines and branches without a new exclusion.

[`aecp_wire.py`](../test/aecp_wire.py) builds unchanged processor RTL in scratch,
feeds the same commands to that model and the portable core, and independently
grades the resulting bytes. The single-interface reference is
`2ad2f845dd583f8310075fa2380cb60a04fd091a`, the processor pin when F5 was
measured; #708 later moved the pin, so its command takes a checkout of that
revision. The two-interface reference is the merged #69 revision
`c9f74b6866a63dd3c0e4534724bfc07a86ad142b`.
Both source inventories are content-pinned. The core is built with the
[TSN stack](../README.md#the-tsn-stack-submodule)'s wire layer, whose pin check
runs first (`--stack`, the submodule by default). The wrapper's name capacity follows
the generated shape. Only the bench's external observation/format/map providers
are adapted to that shape. A generated verification-only second sampling rate
exercises a real rate change. No product configuration or RTL is edited.

```sh
python3 -B sw/firmware/ctrl/test/aecp_wire.py --reference "$PROCESSOR_F5_REFERENCE" \
  --interfaces 1 --output "$F5_SCRATCH/wire-one" --verilator "$PINNED_VERILATOR"
python3 -B sw/firmware/ctrl/test/aecp_wire.py --reference "$PROCESSOR_69_REFERENCE" \
  --interfaces 2 --output "$F5_SCRATCH/wire-two" --verilator "$PINNED_VERILATOR"
```

`--every` runs both, each against its pinned revision, whose tree it takes
from the `protocol-processor` submodule's own objects without changing the
submodule; a revision the submodule does not hold is refused by name. The
[TSN stack boundary](../README.md#the-tsn-stack-submodule) runs it this way,
so it judges what both configurations compile:

```sh
python3 -B sw/firmware/ctrl/test/aecp_wire.py --every --output "$F5_SCRATCH/wire" \
  --verilator "$PINNED_VERILATOR"
```

Each ingress grades every generated descriptor, the implemented command set and
every mandatory notification type, including lock expiry, controller departure
and START/STOP. The two-interface case also registers the same controller on both
interfaces, removes one registration, and checks the remaining notification and
firmware egress index. The processor wrapper exposes ingress but no egress index;
its wire count proves registration isolation, not a physical dual-port output.
Sequences are checked independently before comparing payloads. Eleven planted
observation defects prove the oracle rejects missing records, altered payloads,
lengths, status, sequences, extra frames and requested-latency echo without a
latency sub-command. That request uses a different value from the stored latency.
No-subcommand refusals cover flags 0, 4, 8 and 12.
Stream Inputs return NOT_SUPPORTED (Milan 5.4.2.9).
Streaming outputs return STREAM_IS_RUNNING (Milan 5.4.2.9; IEEE 7.4.15.2).
The wire fixture establishes streaming through PROBE_TX and Listener Ready.
It observes streaming before sending the refused commands.
Controls replace each refusal with success and remove each case.
Each control must produce its named refusal or census diagnostic.

| Observed difference | Clause and disposition |
|---|---|
| Root descriptor reads ignore the received configuration index; the reference refuses nonzero indices. | IEEE 7.4.5.1/2 requires ignoring it and responding with zero. |
| SET_STREAM_INFO returns current fields; the reference echoes the command. The core also accepts no sub-command and ignores SAVED_STATE/STREAMING_WAIT. | IEEE 7.4.15.1 defines current fields and ignored flags. Milan 5.4.2.9 echoes requested latency on success only when MSRP_ACC_LAT_VALID is set. Without it, the response reports current latency; stored latency, saved override and change notifications remain unchanged. Unsupported sub-commands still fail atomically. |
| The reference refuses SET/GET_SYSTEM_UNIQUE_ID; the core implements both. | Milan 5.4.4.2/3 require these commands. |
| The first default-valued format/rate SET creates a saved override and notifies in the core; the reference emits no notification. | Milan 5.4.5.2 associates notification with a state change. Persistent override intent is state; repeat identical SETs do not notify again. |
| Both emit START/STOP responses and their command notifications, but only the core emits the additional GET_STREAM_INFO notice for changed started state. | Milan 5.4.5.2 Table 5.22 requires this notice; IEEE 7.5.2 covers the command notification. |
| An unlock notification uses flag 1 in the core and flag 0 in the reference. | IEEE 7.4.2.1 permits these flag alternatives; the owner is zero in both. |

The service tests count mailbox accesses from one original arrival/due time,
including fanout, stalls and deferred failure, then add fixed CPU/observation
allowances. The measured endpoint is response acceptance by the transmit ring.
They compare against IEEE 9.3.2.6 and Milan 5.4.3.4's 240 ms response timeout
and the 10 ms local service target. The HDCP refusal path also checks the
15 ms response deadline from IEEE 9.7.2.7. START/STOP failure is due at 8 ms to leave
service and clock-quantization allowance. These are desk bounds using explicit
100 ns access/observation and 1 ms CPU allowances. Target calibration, complete
call-chain stack bounds and physical timing remain integration obligations.

[`ctrl_srp_image.py --with-aecp`](../test/ctrl_srp_image.py) links the complete
F0-F5/F1 composition at shipping/largest shapes and one/two interfaces. The
fixture retains saved-state restore and application service but uses explicit
unavailable physical observation callbacks. It is a size/ABI fixture, not a
board image. The revised F5 budget is 224 KB
([ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916)).
The later default flip still requires routed memory fit and the owner's reserve.
