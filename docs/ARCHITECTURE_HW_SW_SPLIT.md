# Architecture — what runs on the softcore, what does not

Status: 2026-07-12 (rev 2 — USER DIRECTIVE: **everything goes FPGA; use
lwSRP**. The media plane, SRP and ACMP connections move to fabric; PipeWire
is out of the plan of record. The softcore keeps provisioning, gPTP protocol
(linuxptp), the PCM producer and ops.) Diagram: `hdl/ieee17221/aecp/doc/atdecc_architecture.drawio` page
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
- a state machine with policy or configuration input where deadlines are
  soft (gPTP BMCA/servo — OS timers, config files);
- sample *production* (filling a PCM ring at millisecond cadence — the
  per-frame 125 us work is NOT this);
- provisioning that runs once per boot (identity programming) and ops.

The cadence anchor that forced rev 2: class-A AAF = one frame every 125 us;
the measured softcore wakeup is 340-560 us per leg (R1 campaign). Userspace
cannot hold the media cadence on this silicon — by our own first principle
the framer, the reservation gate and connection liveness are fabric work.

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
| **ACMP stateless responder** (GET_TX_STATE / GET_TX_CONNECTION, count=0) | fabric | silicon | la_avdecc Milan=1 CLEAN (2026-07-12, eto_acmp2); CSR 0x650 |
| ACMP connection handling (CONNECT/DISCONNECT_TX, PROBE_TX fast-connect) | **fabric** | silicon | in-fabric connection table + acceptance (resource check against lwSRP grant); CSR mailbox demoted to telemetry/override; ACMP listener SM + PROBE_TX activation SM silicon-proven |
| kl-eth driver (rings, NAPI, ethtool, CSR) | softcore | silicon | Linux 6.x, kl,dma-ether |
| kl-eth PHC (`/dev/ptpN`) + SO_TIMESTAMPING | softcore | silicon | exposes the fabric counter/timestamps to linuxptp; HW-ts green zero-overrides |
| gPTP protocol (BMCA, servo, pdelay) | softcore | present, silicon-validated | linuxptp ptp4l + phc2sys in the rootfs; the PHC is real; media-clock MMCM-DRP servo silicon-proven (−83.9 dB) |
| gPTP → entity bridge (GM id/domain into CSR 0x624/0x628 on change) | softcore | present | `gptp2csr.sh` daemon publishes GM id/domain (0x624/0x628) on change; fabric already has gm_change → re-advertise + index bump + AS_PATH/AVB_INFO truth |
| **lwSRP** — lightweight SRP in fabric (MSRP Talker Advertise TX, Listener Ready RX, MVRP VLAN reg, ≤75 % SR-class bandwidth gate) | **fabric** | silicon | RTL (`hdl/lwsrp`, 9 modules, CSR 0x680) + harness, silicon-validated; the grant drives the CBS idleSlope and GATES tx (FR-SRP-03) |
| MAAP (multicast MAC allocation) | **fabric** | silicon | `KL_maap` probe/defend/announce, silicon-proven (CSR 0x6CC-0x6D4) |
| **AAF framer** (AVTP talker payloads) | **fabric** | silicon | PCM via a DMA audio ring -> fabric packetizer stamps presentation time from the PTP counter -> class-A CBS queue; zero per-frame CPU; RTL + harness, silicon-validated |
| PCM producer (fills the audio ring, ms-cadence) | softcore | present (ALSA record) | any Linux source (ALSA app, test tone); ALSA record byte-exact on silicon (playback scaffold pending); PipeWire optional as a source, NOT in the datapath |
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
4. **DMA audio ring** (next, with the AAF framer) — the PCM crossing: SW
   fills samples at millisecond cadence; the fabric framer consumes, stamps
   presentation time (PTP counter + offset), packetizes, and feeds class A.
5. **Telemetry mailbox** (demoted from policy mailbox) — fabric-owned
   connection/reservation tables report events; SW may override, never
   gates liveness.

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

- **lwSRP scope**: proposed architecture in docs/LWSRP_FPGA_ARCHITECTURE.md
  (streaming vector walker, always-declare applicant, gate-before-slope).
  MSRP talker-side + MVRP first (talker endpoint); the
  listener half (Listener Ready TX) lands with STREAM_INPUT. Domain/SR-class
  discovery stays minimal per Milan (fixed class A defaults).
- **gPTP in fabric**: explicitly NOT now — linuxptp on the softcore is the
  plan (task: Arty+Milan pair), with fabric timestamps + INCR/ADJ discipline
  hooks. Revisit only if servo jitter proves blocking.
- **Audio source**: DMA PCM ring from Linux first; a native I2S/TDM codec
  input to the fabric is the later fully-FPGA option.
