<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# AECP firmware owner

Lane F5 of [#665](https://github.com/kebag-logic/milan-fpga/issues/665) adds
an opt-in AECP owner beside ADP, ACMP, MAAP and SRP. The default fabric build
and shipping image continue to use their existing owners. The normative
references are IEEE 1722.1-2021 7.4, 7.5 and 9.3, Milan v1.2 5.4, and
[NFR-SCOUT-02/03/08](../../../../docs/reference/FR_NFR.md).

## Contract and integration

[`aecp.h`](aecp.h) is a portable C11 API over caller-owned storage and typed
environment ports. The core has no register, mailbox, image-file, heap, thread
or operating-system dependency. [`aecp_image.c`](aecp_image.c) validates the
generated AEM image and exposes descriptor spans; [`aecp_entity.py`](aecp_entity.py)
uses the existing builder generators and derives capacities from their output.
Every advertised descriptor is served by READ_DESCRIPTOR. Names and scalar
changes are reflected in subsequent descriptor reads.

The command owner implements entity availability, acquisition refusal and locks;
configuration, names, stream formats and information; rates and clock sources;
IDENTIFY control; START/STOP; registration; AVB information, AS path, counters,
audio mappings and dynamic information. MVU implements Milan information and
system unique ID. Other commands return NOT_IMPLEMENTED, except the required
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
completed transmission. Controller probes use a 30-60 s monitor interval,
250 ms retry and eventual targeted deregistration. Locks expire after 60 s.

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
([#653](https://github.com/kebag-logic/milan-fpga/issues/653)).

[`aecp_state.c`](aecp_state.c), [`aecp_maps.c`](aecp_maps.c) and
[`aecp_nvm.c`](aecp_nvm.c) implement
[#637](https://github.com/kebag-logic/milan-fpga/issues/637). Saved scalars use
the live validators. A saved map is accepted atomically or refused as a whole.
Absent maps start from generated identity defaults, clipped to a restored input
format. A refused saved map retains the default map and rolls its input format
back when required to preserve that map. Live format changes cannot orphan
existing mappings. Map partitioning follows advertised geometry and output
stream/channel ownership is global across output ports. An accepted default-valued
SET still establishes a persistent override. Store dirty marks are queued for
later polling. The reserved system-ID/media-clock-reference saved spans remain
erased; system unique ID is volatile until a record-format decision is made.

## Verification and limits

The [firmware bank](../test/test_ctrl_firmware.py) includes the composed AECP
tests at one and two interfaces, all five generated shapes and the reentry
guard. [`aecp_mutants.py`](../test/aecp_mutants.py) names every test and requires
each source defect to fail its named assertion in a completed run. The full
[coverage gate](../../gtest/README.md) measures the eight new production files
at 100% lines and branches without a new exclusion.

[`aecp_wire.py`](../test/aecp_wire.py) builds unchanged processor RTL in scratch,
feeds the same commands to that model and the portable core, and independently
grades the resulting bytes. The single-interface reference is the pinned
`2ad2f845dd583f8310075fa2380cb60a04fd091a`; the two-interface reference is
the merged #69 revision `c9f74b6866a63dd3c0e4534724bfc07a86ad142b`.
Both source inventories are content-pinned. The wrapper's name capacity follows
the generated shape. Only the bench's external observation/format/map providers
are adapted to that shape. A generated verification-only second sampling rate
exercises a real rate change. No product configuration or RTL is edited.

```sh
python3 -B sw/firmware/ctrl/test/aecp_wire.py --reference protocol-processor \
  --interfaces 1 --output "$F5_SCRATCH/wire-one" --verilator "$PINNED_VERILATOR"
python3 -B sw/firmware/ctrl/test/aecp_wire.py --reference "$PROCESSOR_69_REFERENCE" \
  --interfaces 2 --output "$F5_SCRATCH/wire-two" --verilator "$PINNED_VERILATOR"
```

Each ingress grades every generated descriptor, the implemented command set and
every mandatory notification type, including lock expiry, controller departure
and START/STOP. The two-interface case also registers the same controller on both
interfaces, removes one registration, and checks the remaining notification and
firmware egress index. The processor wrapper exposes ingress but no egress index;
its wire count proves registration isolation, not a physical dual-port output.
Sequences are checked independently before comparing payloads. Six planted
observation defects prove the oracle rejects missing records, altered payloads,
lengths, status, sequences and extra frames.

| Observed difference | Clause and disposition |
|---|---|
| The reference refuses SET/GET_SYSTEM_UNIQUE_ID; the core implements both. | Milan 5.4.4.2/3 require these commands. |
| The first default-valued format/rate SET creates a saved override and notifies in the core; the reference emits no notification. | Milan 5.4.5.2 associates notification with a state change. Persistent override intent is state; repeat identical SETs do not notify again. |
| Both emit START/STOP responses and their command notifications, but only the core emits the additional GET_STREAM_INFO notice for changed started state. | Milan 5.4.5.2 Table 5.22 requires this notice; IEEE 7.5.2 covers the command notification. |
| An unlock notification uses flag 1 in the core and flag 0 in the reference. | IEEE 7.4.2.1 permits these flag alternatives; the owner is zero in both. |

The service tests count mailbox accesses from one original arrival/due time,
including fanout, stalls and deferred failure, then add fixed CPU/observation
allowances. The measured endpoint is response acceptance by the transmit ring.
They compare against IEEE 9.3.2.6 and Milan 5.4.3.4's 240 ms response timeout
and the 10 ms local service target. START/STOP failure is due at 8 ms to leave
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
