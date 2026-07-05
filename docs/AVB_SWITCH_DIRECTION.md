# Direction: from the 1-NIC endpoint to an 8-port AVB switch (MTU fixed at 1500)

*Design note, 2026-07-05. One-picture summary below (source `AVB_SWITCH_DIRECTION.gen.py`,
editable `.drawio`). Companion to [`RX_RING_DMA.md`](RX_RING_DMA.md) (the endpoint ring
DMA work this builds on).*

![endpoint -> switch direction](AVB_SWITCH_DIRECTION.svg)

## The constraint set

* **MTU stays 1500** (interop; AVB frames are small anyway) — so all large-MTU levers are
  off the table, and at 1 Gbps that means **81,274 packets/s ≈ 1,230 CPU cycles/packet**
  on the 100 MHz RV64. No software per-packet path fits in that. Every design below is a
  way of taking the CPU out of the per-packet path.
* **Target platform role: an 8-port AVB switch.** Forwarding 8×1G must not touch the CPU
  at all — the CPU is the control plane (gPTP servo, MSRP/MVRP, AVDECC, management).

## The three endpoint hooks (panel ①/②)

* **A — AVTP stream engine** (the mission-critical one): taps the classifier; matched
  stream IDs bypass ring/driver/stack entirely. RX: strip AVTP, write raw samples +
  presentation timestamps into per-stream sample rings that PipeWire mmaps — the CPU
  wakes **per audio period (~375/s)** instead of per packet (8,000/s/stream). TX mirror:
  sample ring → hardware AVTP framing + gPTP timestamps → CBS. Media cost on the CPU ≈ 0,
  independent of stream count up to line rate.
* **T — TSO** (TCP Segmentation Offload, TX): the stack hands ONE ≤64 KB super-packet
  through TCP/IP/qdisc/driver once; the TX ring reader slices it into 1500-byte wire
  frames (cloned headers, per-slice IP len/id, TCP seq/flags, checksums). Per-packet
  stack cost ÷ ~43 at unchanged wire MTU.
* **R — RSC/LRO** (Receive Segment Coalescing, RX): the ingress drop-FIFO merges
  consecutive in-order segments of one TCP flow into a single large ring frame (flush on
  gap/PSH/FIN/interleave/timer) — the hardware twin of GRO, so the stack pays per-64 KB.

T+R restore (and exceed) the measured large-MTU throughput while the wire never carries
anything but 1500-byte frames. They are classic, bounded, protocol-aware RTL — medium
risk. A is simpler RTL than either and is the Milan roadmap.

## The switch data plane (panel ③)

Per-port MAC + PTP timestamping → per-port ingress (PCP classification + **TCAM** dst-MAC
lookup + SRP policing) → an **output-queued shared-BRAM fabric** → per-port egress with
**8 CBS-shaped queues** → MACs. The existing endpoint (rings, datapath, AVTP engine)
attaches to the fabric as the internal CPU port. Blocks already in the repo and verified:
`tcam.sv`, `credit_based_shaper.sv`, `traffic_classifier.sv`, the PTP timestampers, the
ring DMA engines.

## Memory: "would a wider bus help?" (panel ④)

* **Endpoint, today: no.** The socket path is CPU-bound; at 92 Mbit/s the DMA uses <2 %
  of DDR3-800 x16 (~1.2 GB/s effective). Telemetry: 0 RX stalls across 35 M frames.
* **Switch: the question inverts.** 8×1G in + 8×1G out ≈ **2 GB/s sustained** — above the
  DDR3 ceiling and hostage to refresh/CPU arbitration jitter (AVB latency guarantees
  die). The answer is not a wider DRAM bus but **keeping forwarding on-chip**: 2 GB/s is
  one 128-bit @ 125-200 MHz internal path into a 256-512 KB segmented BRAM buffer. CBS
  bounds AVB queue depth by construction, so BRAM suffices; best-effort overflow drops
  (counted) rather than spilling to DRAM. DRAM remains CPU/control-plane only.

## Hardware reality

The AX7101 has **one** PHY. 8 external ports need new I/O: the xc7a100t's 4 GTP
transceivers can carry 8×1G as **2 lanes of QSGMII** into two quad PHYs (daughter
board), or move to a bigger carrier (Artix-200T/Kintex) — 8 MACs + fabric + 64 CBS
queues will crowd the 100T. Prototype path: 2-3 SGMII ports on the GTPs first, with the
current board as the CPU/endpoint port.

## Suggested phasing

1. **A** (AVTP engine) on the current 1-port endpoint — Milan roadmap value immediately,
   and it is the switch's CPU-port media path unchanged.
2. 2-3-port switch prototype on GTP SGMII: fabric + TCAM + per-port CBS, gPTP
   transparent-clock residence-time correction.
3. Scale to 8 ports on the target carrier; T/R (TSO/RSC) only if bulk socket throughput
   at MTU 1500 turns out to be a real product requirement rather than a benchmark.
