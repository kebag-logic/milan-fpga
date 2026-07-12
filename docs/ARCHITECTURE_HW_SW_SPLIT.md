# Architecture — what runs on the softcore, what does not

Status: 2026-07-12. Diagram: `hdl/aecp/doc/atdecc_architecture.drawio` page
`9-hw-sw-split` (rendered PNG alongside). This document is the normative
delimitation; the diagram mirrors it.

## The dividing principle

Everything that must stay correct **per frame, at line rate, or while the CPU
is busy/absent** lives in the fabric. Everything that is **negotiation,
policy, or long-lived state** lives on the softcore under Linux. The fabric
*answers*; the softcore *decides*.

Concretely, a function goes to the FPGA fabric when it needs any of:
- per-frame work at line rate (filter, classify, shape, timestamp, coalesce);
- protocol liveness with deadlines independent of CPU load (ADP re-advertise,
  AECP response before the controller's 250 ms retry, byte-exact fixed-format
  replies);
- wire-format truth that must never drift from the advertised identity
  (the 0x600 CSR group feeds ADP and AEM from the same wires).

A function goes to the softcore when it is:
- a state machine with policy or configuration input (gPTP BMCA, SRP
  registration/bandwidth math, ACMP connection acceptance);
- media production (PipeWire graph, AAF payload assembly);
- provisioning that runs once per boot (identity programming).

## Per-function delimitation

| Function | Where | Status | Notes |
|---|---|---|---|
| MAC RX/TX (RGMII/GMII), 1G | fabric | silicon | eth_mac_1g_rgmii |
| Dest-MAC TCAM filter | fabric | silicon | rx_mac_filter |
| 802.1Q classify + CBS shaper + queues | fabric | silicon | never removed (user rule); sequential slope engine |
| PTP timestamp counter + RX/TX capture | fabric | silicon | DMA ts window; the raw gPTP ingredient |
| RX DMA: RSC coalescing, header-split, multi-slot | fabric | silicon | driver-paired (hsplit16/mslot60) |
| HW-TSO header generation | fabric | silicon | TX 143/186 zc validated |
| **ADP advertiser** (available/depart/discover, available_index) | fabric | silicon | la_avdecc-clean; index +1 every ADPDU |
| **AECP/AEM entity** (5 descriptors, Milan §5.4.4 command set, LOCK) | fabric | silicon | zero-CPU responder; ROM+overlay store |
| **ACMP stateless responder** (GET_TX_STATE / GET_TX_CONNECTION, count=0) | fabric | **next** | the Milan=1 gate; same ingress/merge pattern as AECP |
| ACMP connection handling (CONNECT/DISCONNECT_TX policy) | softcore | future | CSR mailbox + IRQ: SW accepts/refuses, writes the connection table back; fabric keeps answering state queries from that table |
| kl-eth driver (rings, NAPI, ethtool, CSR) | softcore | silicon | Linux 6.x, kl,dma-ether |
| kl-eth PHC (`/dev/ptpN`) + SO_TIMESTAMPING | softcore | **next** | exposes the fabric counter/timestamps to linuxptp |
| gPTP protocol (BMCA, servo, pdelay) | softcore | present, unvalidated | linuxptp ptp4l + phc2sys in the rootfs; needs the PHC to be real |
| gPTP → entity bridge (GM id/domain into CSR 0x624/0x628 on change) | softcore | future | tiny daemon or ptp4l hook; fabric already has gm_change → re-advertise + index bump + AS_PATH/AVB_INFO truth |
| SRP/MSRP (talker advertise, bandwidth) | softcore | future | pipewire module-avb carries the MRP state machines; fabric provides class-A shaping already |
| AVTP media (AAF talker payloads) | softcore | future | PipeWire module-avb crafts frames → kl-eth → CBS class-A queue; a fabric AAF framer is an optional later offload, not the plan of record |
| Identity provisioning (0x600 group, caps 0x8588) | softcore | silicon | once per boot (avdecc/aecp_csr_setup.sh); after that the fabric is autonomous |

## Boundary contracts (the only crossings)

1. **CSR 0x600 group** — identity + control, written by SW once (then only on
   real changes: GM change, name-affecting config). ADP and AEM read the same
   wires, so wire truth cannot diverge. Status readback: 0x644 (live
   available_index), 0x648/0x64C (locked, cmd/resp counters).
2. **DMA rings + timestamp window** — the data plane crossing; all media and
   host traffic, with per-frame HW timestamps landing in descriptors.
3. **PHC clock ops** (next) — the fabric counter exposed as `/dev/ptpN`;
   ptp4l disciplines it, phc2sys mirrors it to CLOCK_REALTIME.
4. **Event mailbox + IRQ** (future, with ACMP connections) — fabric posts
   CONNECT_TX_COMMANDs it cannot answer alone; SW replies via the connection
   table; fabric answers all subsequent state queries without SW.

## Rationale anchors (paid-for evidence)

- The AECP/ADP-in-fabric choice is validated: la_avdecc enumerates the entity
  with the CPU fully idle, and the available_index/ADP coherence rules are
  enforceable exactly because one HW counter feeds both protocols.
- The 50→100 MHz datapath and reader-bound TX ceiling work showed the softcore
  is the scarce resource; anything periodic or per-frame that can leave the
  CPU, should.
- gPTP's BMCA/servo is policy with OS timers and config — the reference
  practice (linuxptp) stays; only timestamps and the clock itself are HW.

## Open decisions (flagged, not blocking)

- **ACMP connection table location** once real connections land: proposed
  fabric-owned table written via mailbox (keeps state queries zero-CPU).
  Alternative (all-SW responder via tap+inject) rejected for liveness.
- **Fabric AAF framer** (media offload): revisit only if PipeWire-crafted
  frames cannot hold class-A cadence at target channel counts.
