[OBSOLETE + 2026-08-16]

# Architecture — what runs on the softcore, what does not

Status: **rev 3, 2026-08-13** (USER DIRECTIVE: *"remove the old code AECP/ACMP/ADP
the lwSRP shall be removed as well. Only use the uCPU code"*). Rev 2's verdict
stands — everything per-frame goes FPGA — but the fabric that implements the
IEEE 1722.1 / SRP control plane is no longer this repository's own engines: it
is [`hdl/milan/KL_pp_shadow.sv`](../hdl/milan/KL_pp_shadow.sv), wrapping the
pinned `protocol-processor` submodule, instantiated **unconditionally** by
[`hdl/milan/milan_datapath.sv`](../hdl/milan/milan_datapath.sv) with no
parameter, no fallback and no shadow arm. It owns ADP, ACMP (talker and
listener) and SRP. MAAP stays in this fabric (`KL_maap` +
[`hdl/milan/KL_pp_maap_shim.sv`](../hdl/milan/KL_pp_maap_shim.sv)) because the
processor implements none by design. The rev-2 ADP advertiser, AECP/AEM engine,
ACMP talker/listener and lwSRP applicant are **deleted**. This document is the
normative delimitation; the rev-2 `atdecc_architecture.drawio` page
`9-hw-sw-split` that used to mirror it was deleted with the plane it drew.

**The AECP row is the one to read first: this entity serves the processor's
declared command inventory, including `READ_DESCRIPTOR` and `GET_COUNTERS`.**
The responder is the processor's AECP uCPU in fabric. No software responder was
added because a controller's 250 ms retry deadline is independent of CPU load.
`READ_DESCRIPTOR` provides its three standard status paths. GET_COUNTERS serves
every declared Stream Output with the Milan Table 5.17 mask and compact
five-counter layout. Unsupported commands receive a conformant
`NOT_IMPLEMENTED` response with the correct message type, length and control
data length. `IDENTIFY_NOTIFICATION` (0x0026) as a command receives
`BAD_ARGUMENTS`. A command for another entity and an AECP response arriving as
input are silently refused, freed and counted.

**The remaining boundary is explicit.** The Milan Table 5.22 unsolicited
counter-change producer, saved-state persistence and commands outside the
served inventory remain open. Milan Delta 7 `ACQUIRE_ENTITY` is not
distinguished from the generic fallback response.

**The entity model lives in DDR3.** The processor's descriptor store fetches it
over a read-only master at a **compile-time base** (no base register), surfaced
by `milan_datapath` as `o_desc_mem_*`/`i_desc_mem_*` and bridged to DRAM by the
LiteX SoC. Software must load the image before the entity is enabled — see the
boot sequence below.

## Contents

- **[The dividing principle](#the-dividing-principle)** -- The test for "fabric or softcore", plus the measurement that forced rev 2: class-A AAF wants a frame every 125 us and the measured softcore wakeup is 340–560 us, so the framer cannot live in userspace.
- **[Per-function delimitation](#per-function-delimitation)** -- The normative table names which side owns each function, the served AECP inventory and the remaining gaps.
- **[What rev 3 costs, named](#what-rev-3-costs-named)** -- The remaining losses include unavailable media-clock selection, the pinned presentation offset and the missing Table 5.22 producer. Solicited Stream Output counters are live.
- **[Boundary contracts (the only crossings)](#boundary-contracts-the-only-crossings)** -- The interfaces that are allowed to cross: the 0x600 identity CSRs, the DMA rings + timestamp window, the read-only descriptor-memory master into DRAM, the PHC, the DMA audio ring, and the mailbox -- now telemetry-and-override, explicitly not a liveness gate.
- **[Rationale anchors (paid-for evidence)](#rationale-anchors-paid-for-evidence)** -- Why the split is believed rather than asserted: la_avdecc enumerated the rev-2 entity with the CPU idle (evidence that must now be re-taken against the uCPU and its DDR3 image), one hardware counter fed both ADP and AEM so wire truth could not diverge, and the TX-ceiling work showed the CPU is the scarce resource.
- **[Open decisions (flagged, not blocking)](#open-decisions-flagged-not-blocking)** -- Three things deliberately left unsettled: how far the AECP uCPU is taken past READ_DESCRIPTOR, gPTP staying on the softcore (linuxptp, revisit only if servo jitter blocks), and whether audio ever arrives from a native I2S/TDM input instead of the DMA ring.

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
| **ADP** (available/depart/discover, available_index) | fabric | rev 3 | the protocol processor's ADP engine, via `KL_pp_shadow`; `available_index` is published on its class-D face and stays live at CSR `0x644`. The rev-2 `adp_advertiser`/`KL_adp_parser` are deleted, and the `0x600` diagnostic words they fed read structural zeros |
| **AECP/AEM entity** | fabric | rev 3, **partial** | The protocol processor's AECP uCPU, via `KL_pp_shadow`, serves its declared command inventory. `READ_DESCRIPTOR` provides SUCCESS, NO_SUCH_DESCRIPTOR and BAD_ARGUMENTS. GET_COUNTERS serves every declared Stream Output counter bank. Unsupported commands receive a conformant fallback, and `IDENTIFY_NOTIFICATION` as a command receives BAD_ARGUMENTS. Descriptors are fetched from DDR3 at a compile-time base. Remaining gaps include the Table 5.22 unsolicited producer, persistence and Milan Delta 7 ACQUIRE_ENTITY semantics |
| **ACMP** (CONNECT_TX / PROBE_TX / GET_TX_STATE, the BIND_RX ladder) | fabric | rev 3 | the processor's talker + listener pair; the result is republished as a **bind record** on the class-D face, which is what every consumer in `milan_datapath` reads. `ACMPL_STATE` no longer tracks PROBING/SETTLED — take `bound` as the truth |
| **The talker DA gate** | fabric | rev 3 | `acmp_declaring_o` asserts only after a MAAP `ALLOC_DA` success through `KL_pp_maap_shim`, so AAF admission is still "a destination address exists AND the source is declaring" |
| kl-eth driver (rings, NAPI, ethtool, CSR) | softcore | silicon | Linux 6.x, kl,dma-ether |
| kl-eth PHC (`/dev/ptpN`) + SO_TIMESTAMPING | softcore | silicon | exposes the fabric counter/timestamps to linuxptp; HW-ts green zero-overrides |
| gPTP protocol (BMCA, servo, pdelay) | softcore | present, silicon-validated | linuxptp ptp4l + phc2sys in the rootfs; the PHC is real. The media-clock MMCM-DRP servo was silicon-proven at −83.9 dB, but rev 3 leaves it **structurally off** — see the losses below |
| Media clock **source selection** | **neither** | **NOT IMPLEMENTED** | `SET_CLOCK_SOURCE` was the only writer of the live CLOCK_DOMAIN `clock_source_index`; pinned at 0 = the INTERNAL media clock for the life of the build |
| Saved-state / fast-connect persistence | **neither** | **NOT IMPLEMENTED** | the journal is deleted; the processor's NVM face is answered by a blank-flash responder, so a restore walk always completes with zero records. Milan v1.2 5.3.8.2 wants saved state; this build does not have it and says so structurally |
| gPTP → entity bridge (GM id/domain into CSR 0x624/0x628 on change) | softcore | present | `gptp2csr.sh` daemon publishes GM id/domain (0x624/0x628) on change; fabric already has gm_change → re-advertise + index bump + AS_PATH/AVB_INFO truth |
| **SRP** (MSRP Talker Advertise TX, Listener Ready RX, MVRP VLAN registration, ≤75 % SR-class bandwidth gate) | **fabric** | rev 3 | the protocol processor's, consumed as **wires**: `srp_active_o` + `srp_granted_slope_bps_o` drive the CBS idleSlope and gate TX (FR-SRP-03). The 11-module `lwSRP` engine is deleted; at `0x680` the domain word, granted slope and over-limit bit are repointed and live, while the MRPDU counters read structural zeros. Ordering note: the processor asserts activity and slope in the SAME cycle where `KL_lwsrp_bw_gate` staged them — at worst equal on the opening edge, briefly conservative on the closing one; neither edge lets a stream transmit against an un-budgeted slope |
| MAAP (multicast MAC allocation) | **fabric** | silicon | `KL_maap` probe/defend/announce (CSR 0x6CC-0x6D4), now also serving the processor's per-source ALLOC/RELEASE face through [`hdl/milan/KL_pp_maap_shim.sv`](../hdl/milan/KL_pp_maap_shim.sv) out of the same block claim |
| **AAF framer** (AVTP talker payloads) | **fabric** | silicon | PCM via a DMA audio ring -> fabric packetizer stamps presentation time from the PTP counter -> class-A CBS queue; zero per-frame CPU; RTL + harness, silicon-validated |
| PCM producer (fills the audio ring, ms-cadence) | softcore | present (ALSA record) | any Linux source (ALSA app, test tone); ALSA record byte-exact on silicon (playback scaffold pending); PipeWire optional as a source, NOT in the datapath |
| **Descriptor-image load into DDR3** | softcore | rev 3 | the entity model is no longer a fabric ROM: the processor's descriptor store fetches it from main memory over a read-only master at a **compile-time base**, so there is no base register and software cannot relocate it at runtime. The image **must be written at that base before the entity is enabled** — a zeroed region reads as "image not loaded" through its header magic/version/checksum, and every `READ_DESCRIPTOR` then answers **`BAD_ARGUMENTS`**, because an invalid image reports a configuration count of zero and the microprogram's `configuration_index` check runs before the locate. That is a clean refusal, not a hang: the store's watchdog abandons a stalled burst. **The code discriminates:** `BAD_ARGUMENTS` on every read = no image; `NO_SUCH_DESCRIPTOR` = image loaded, that descriptor absent from the model |
| Identity provisioning (0x600 group) | softcore | silicon | once per boot ([avdecc/aecp_csr_setup.sh](../avdecc/aecp_csr_setup.sh)), **after** the descriptor image is in place; after that the fabric is autonomous. `ADP_CTRL.en` (`0x600` bit 0) is ORed with `PP_CTRL[0]` (`0x920`): **either** bit enables the entity, which is why every existing bring-up script still works. Note that five of that group's words — entity_capabilities, valid_time, association_id, controller_capabilities, interface_index — plus the advertise/depart strobes are now **write-only scratch**: the processor holds those as internal constants and exposes no port, so writing them reads back but changes nothing observable |

## What rev 3 costs, named

Three losses are functional, not paperwork, and each is where a bench meets it:

1. **The CRF media clock can never be SELECTED.** AECP `SET_CLOCK_SOURCE` was
   the only writer of the live CLOCK_DOMAIN `clock_source_index`, so it is
   pinned at 0 — the INTERNAL media clock — for the life of the build.
   Consequence: `KL_mmcm_drp_servo` and the `KL_media_nco` packet-grid servo are
   **structurally off** and `A_MCSRV_STAT` (`0x8F8`) reads its idle. The CRF
   Media Clock Input engine (`KL_crf_rx`) still parses, counts and reports — it
   just cannot steer anything.
2. **Presentation-time offset is pinned at the Milan 2 ms DEFAULT** for every
   Stream Output, because `SET_MAX_TRANSIT_TIME` / `SET_STREAM_INFO(ACC_LAT)`
   was its only writer. That is a *default*, not a zero: 0 ns would be a
   presentation time in the past and every listener would drop every frame as
   late.
3. **Milan Table 5.4 per-STREAM_OUTPUT diagnostic counters are live.**
   `KL_talker_diag_ctx` is instantiated for every declared AAF output and the
   CRF output. Solicited GET_COUNTERS reads the compact five-counter Milan
   layout. The Table 5.22 unsolicited change notification remains open because
   its producer is not connected to the processor's unsolicited TX lane.

## Boundary contracts (the only crossings)

1. **CSR 0x600 group** — identity + control, written by SW once (then only on
   real changes: GM change, name-affecting config). The processor's ADP engine
   reads those wires, so what is advertised cannot diverge from what was
   provisioned. Status readback: 0x644 (live available_index, still published by
   the processor); 0x648/0x64C carried the AECP lock and cmd/resp counters and
   now read **structural zeros** — with the one exception that ACMP
   `talker_active` is live, being the processor's `acmp_declaring_o`.
2. **DMA rings + timestamp window** — the data plane crossing; all media and
   host traffic, with per-frame HW timestamps landing in descriptors.
2b. **The descriptor-memory master** — `milan_datapath`'s
   `o_desc_mem_*`/`i_desc_mem_*`, bridged to DRAM by the LiteX SoC. Read-only,
   fabric-initiated, at a compile-time base. Software's whole share of this
   crossing is placing the image there before enabling the entity; there is no
   handshake and no register to point it somewhere else.
3. **PHC clock ops** (next) — the fabric counter exposed as `/dev/ptpN`;
   ptp4l disciplines it, phc2sys mirrors it to CLOCK_REALTIME.
4. **DMA audio ring** (next, with the AAF framer) — the PCM crossing: SW
   fills samples at millisecond cadence; the fabric framer consumes, stamps
   presentation time (PTP counter + offset), packetizes, and feeds class A.
5. **Telemetry mailbox** (demoted from policy mailbox) — fabric-owned
   connection/reservation state reports events; SW may observe, never gates
   liveness. Under rev 3 the state itself comes from the processor's class-D
   face, and several of the old mailbox-adjacent ports are now write-accepted
   and discarded: the `0x7A0` bind-restore (ack never asserts, nothing is
   restored), the `0x7B8`-`0x7C4` journal, the `0x7C8`-`0x7D4` AEM patch port
   and the `0x7DC` AS_PATH staging.

## Rationale anchors (paid-for evidence)

- The ADP/ACMP-in-fabric choice is validated by the rev-2 build it was measured
  on: la_avdecc enumerated the entity with the CPU fully idle, and the
  available_index/ADP coherence rules were enforceable exactly because one HW
  counter fed both protocols. Rev 3 keeps the fabric placement and changes the
  implementation; the enumeration half of that evidence has to be **re-taken
  against the processor's AECP uCPU and its DDR3 descriptor image**, which is a
  different responder answering the same `READ_DESCRIPTOR` walk.
- The 50→100 MHz datapath and reader-bound TX ceiling work showed the softcore
  is the scarce resource; anything periodic or per-frame that can leave the
  CPU, should. That is also why the remaining AECP gaps are not being filled in
  software.
- gPTP's BMCA/servo is policy with OS timers and config — the reference
  practice (linuxptp) stays; only timestamps and the clock itself are HW.

## Open decisions (flagged, not blocking)

- **How far the AECP uCPU is taken.** The engine serves the inventory recorded
  in `tests/steps/aecp_engine_steps.py`, including GET_COUNTERS. Commands outside
  that inventory are upstream work in the submodule. The Table 5.22 producer
  and Milan Delta 7 ACQUIRE_ENTITY semantics remain open; do not plan around a
  date.
- **gPTP in fabric**: explicitly NOT now — linuxptp on the softcore is the
  plan (task: Arty+Milan pair), with fabric timestamps + INCR/ADJ discipline
  hooks. Revisit only if servo jitter proves blocking.
- **Audio source**: DMA PCM ring from Linux first; a native I2S/TDM codec
  input to the fabric is the later fully-FPGA option.
