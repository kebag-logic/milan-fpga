# Fabric AXI-Stream cores on the bare-metal SoC

This page defines the packet-stream boundary used by the supported LiteX
integration.

## Contents

- **[Interface model](#interface-model)** -- The MAC-facing AXI-Stream byte, packet, and backpressure contract and the fabric-only product flow.
- **[CSR model](#csr-model)** -- How firmware initializes and observes the datapath through the AXI-Lite window.
- **[Descriptor-memory model](#descriptor-memory-model)** -- The protocol processor's read-only AEM image interface and boot-time provisioning rule.
- **[Verification](#verification)** -- The RTL, SoC, UART, and external-wire evidence that closes the boundary.

## Interface model

`milan_datapath` receives and emits 64-bit MAC streams. Byte lane zero carries
the first wire byte; `tkeep` is contiguous on the final beat; `tlast` closes a
packet; and backpressure is honored at every registered merge. The MAC adapter
may cross clock domains only with a complete-packet asynchronous FIFO.

The current shipping placement keeps control traffic in fabric.
Mark II passes selected control frames through filtered packet mailboxes.
ADP, ACMP, AECP, MAAP and SRP are selectable per function.
Its default is bare-metal control; all-fabric remains supported.
All-fabric stays the shipping default until F2 to F5 acceptance.
That acceptance covers all streams, counters and the audio soak.
The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md#packet-mailbox-interface) defines the mailbox boundary.
Framing, timestamps, gPTP and media remain fabric responsibilities.
The generic classifier/queue/CBS input remains inactive in today's shipping boundary.

## CSR model

Bare-metal firmware accesses the AXI-Lite Milan window for initialization,
policy, state snapshots, and diagnostics. Interrupt status remains available
in the CSR block. Media and gPTP progress remain firmware-independent.
Selected firmware control protocols require bounded mailbox service.
[NFR-SCOUT-03](../reference/FR_NFR.md#341-control-service-budget-and-normative-timing) defines that obligation.

## Descriptor-memory model

The protocol processor has a read-only memory request/response interface for
the AEM image. Firmware validates the generated raw image, copies it to the
reserved window, and only then enables the entity. This is a descriptor store,
not a packet path.

## Verification

`tb/verilator/milan_dp` checks packet byte order, arbitration, backpressure,
filter isolation, fabric audio, and protocol/time ownership. The SoC source
closure and elaboration gates check the Python-to-RTL wiring. Physical
acceptance additionally requires UART grading and an external packet capture.
