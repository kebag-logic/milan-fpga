# Integrating `milan_datapath`

`hdl/milan/milan_datapath.sv` is the single supported RTL boundary. The LiteX
integration in `sw/litex/milan_soc.py` is the executable reference.

These integration-boundary claims are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

Use this contract when wiring `milan_datapath`.

## Contents

- **[1. Boundary model](#1-boundary-model)** — The clocks, streams, CSRs, descriptor reads, status, and physical audio supplied or consumed by the datapath.
- **[2. Clocks and resets](#2-clocks-and-resets)** — Destination-domain reset release and the required packet or AXI-Lite crossings.
- **[3. Source files and includes](#3-source-files-and-includes)** — How to consume the checked transitive source closure and generated headers.
- **[4. MAC stream](#4-mac-stream)** — The 64-bit wire-order data, keep, packet-boundary, backpressure, and timestamp convention.
- **[5. CSR and descriptor memory](#5-csr-and-descriptor-memory)** — The register window and builder-generated AEM image contract.
- **[6. Fabric audio](#6-fabric-audio)** — How configured capture and render pins connect directly to the AAF fabric paths.
- **[7. Time ownership](#7-time-ownership)** — The fabric gPTP plane's sole ownership of PHC discipline and published time state.
- **[8. Acceptance](#8-acceptance)** — The structural, simulation, synthesis, timing, UART, and wire checks required after integration.

## 1. Boundary model

The integrator supplies clocks/resets, a MAC RX/TX stream, AXI-Lite CSRs,
descriptor-memory reads, station/MAC status, and physical audio pins. The
datapath supplies fabric packet protocols, time synchronization, media routing,
filtering, counters, and interrupts. Product packet payload does not cross into
CPU memory.

## 2. Clocks and resets

- `axis_clk` runs the packet and CSR datapath.
- `gtx_clk` runs the PHC/timestamp counter.
- Ethernet TX/RX clocks terminate at the MAC adapter.
- the configured audio clock and media tick pace capture/render.

Each reset is synchronized to its destination domain. If CSR or MAC adapters
run in another domain, use explicit AXI-Lite or complete-packet stream
crossings; do not synchronize payload buses bit by bit.

## 3. Source files and includes

Do not maintain a hand-copied source subset. Use `add_milan_datapath()` or the
closure emitted by `scripts/check_rtl_source_lists.py --files`. Packages must
precede modules, processor sources must match the superproject pins, and
include directories must cover generated CSR/shape headers.

Run `python3 scripts/check_soc_sources.py` and
`python3 scripts/check_rtl_source_lists.py` whenever a child module is added or
moved.

## 4. MAC stream

The datapath uses 64-bit AXI-Stream with eight keep bits and wire byte zero in
`tdata[7:0]`. The adapter must preserve packet boundaries, keep masks, and
backpressure. Timestamp capture is tied directly to the MAC-side
start-of-frame event and fabric flow control.

## 5. CSR and descriptor memory

Expose the 64 KiB AXI-Lite window without reinterpreting register ownership.
The current contract is the [register map](../reference/REGISTER_MAP.md). The protocol
processor's descriptor read port addresses the builder-generated AEM image;
firmware must validate and install that image before entity enable.

## 6. Fabric audio

Map capture and render pins from the end-station configuration. Capture feeds
the AAF talker map; accepted listener payload feeds direct and mapped physical
render. Unused physical interfaces are elaboration-time omissions or safe
ties, never target-memory detours.

## 7. Time ownership

Release images enable the fabric gPTP plane. It owns PHC adjustment and all
published synchronization state. Firmware may establish an epoch but must not
mirror or overwrite fabric-owned publication fields. The option-OFF shape is a
non-flashable negative test.

## 8. Acceptance

Elaborate the exact source closure, run focused and `milan_dp` suites, synthesize
with Yosys, close timing on the destination device, and run the UART plus
external-wire campaign. Preserve the exact pins, config, generated artifacts,
tool versions, and hashes with the evidence.
