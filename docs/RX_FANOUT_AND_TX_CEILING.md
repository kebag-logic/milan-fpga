# RX fan-out & the TX throughput ceiling (2026-07-07)

Campaign to raise best-effort TCP throughput on the fully-FPGA dual-VexiiRiscv Milan NIC
(Alinx AX7101, 2×RV64 @100 MHz, 50 MHz datapath, MTU 1500 everywhere). Three efforts:
hardware TSO, a profiled single-flow ceiling investigation, and a two-queue RX fan-out.

**Outcome:** TX 58 → 186 single-flow; **RX −P2 = 223 Mbit/s (goal ≥200 met)**; TX capped at
186 by the TX datapath (CBS shaper + reader DRAM latency), *not* the CPU — and located exactly.

All numbers were measured on silicon over a clean SSH path, with the driver identity verified
(`MODULE_VERSION`) and the `milan_tlm` HW counters read alongside the CPU profile — no blind
measurements. iperf3, MTU 1500. Zerocopy = `iperf3 -Z` (sendfile).

## Throughput ladder (Mbit/s)

| Path                 | baseline | soft-TSO | HW-TSO | RX fan-out | bound by                |
|----------------------|:-------:|:--------:|:------:|:----------:|-------------------------|
| TX single, copy      |   58    |   120    | **143**|     —      | sender CPU              |
| TX single, zerocopy  |   —     |   166    | **186**|     —      | ACK-NAPI (1 hart)       |
| TX −P2, zerocopy     |   —     |   136    |   186  |   **186**  | **TX datapath (shaper)**|
| RX single            |   203   |   200    |   200  |     —      | app recv (1 hart)       |
| RX −P2               |   —     |    —     |    —   |  **223**   | **scales — goal met**   |

## Effort 01 — Hardware header-generation TSO

The driver posts one template header (coherent arena, at slot **+2** = NET_IP_ALIGN) + a
2-entry descriptor (MSS, payload len, flag bytes, P-checksum seeds) + frag payload BDs. The
`RingDMAReader` loops the segments in HW: template replay via synthesized windows, constant-
offset field patches (seq@38, flags@47, last-seg tot_len@16 / ip.check@24), P-seeded csum
pre-pass + BD-ring rewind. One skb walks the stack per 64 KB; the wire gets ~45 correct frames.

**The +2 alignment lesson:** headers first landed at +0, putting iph/tcph at 2 mod 4. Every
misaligned u32 store trapped to SBI emulation on VexiiRiscv — **≈56 µs/header = 69% of the whole
TSO cost.** Moving to slot +2 took single-flow TX 42 → 88. The continuity engine reads any source
alignment, so +2 is free downstream.

Validated: sim `test_tx_bd.py::test_tso_hw` (4 cases, classical-checksum reference, suite 9/9);
silicon 0 retransmissions; +12–19% over soft-TSO. Enabled via `hwtso=1` (rsc8+ gateware).

## Effort 02 — the single-flow ceiling (profiled)

**Methodology correction (important):** an apparent "gateware regression" (TX → 57) was a
*measurement artifact* — the 1.5 Mbaud console garbled driver-swap commands, so the stale rootfs
driver kept running while a new one was assumed loaded. Fixed by (1) verifying the driver via
`MODULE_VERSION`, (2) measuring over dropbear **SSH**, (3) rebuilding the gateware at **115200 baud**.
The gateware was never guilty: `rsc8 + hwtso=0` == `rsc7` (both 120 soft-TSO).

At 186 zerocopy, one hart pins ~95% processing incoming ACKs; the other sits ~40% idle. Top cost
(`/proc/profile`): the **socket lock at 15%** — it ping-pongs between the app core and the NAPI core
because a single TCP flow is serial on its ACK clock. Two harts can't accelerate one flow while
sharing one socket lock and one RX queue/NAPI.

Eight runtime levers, each profiled HW+SW — all flat or worse:

| lever | Mbit/s | why it failed |
|---|:---:|---|
| baseline single flow | 186 | ACK-NAPI on one hart |
| RPS → other hart | 145 | IPI cost > benefit on a 2-hart core |
| RFS flow-steer | 157 | steering overhead, still one queue |
| 2-flow pinned | 160 | single NAPI caps both flows |
| rx-usecs 20→1000 | 188 | NAPI runs continuously; poll period moot |
| peer ACK-coalesce | 183 | i210 igb ignores it |

**Exploitable asymmetry:** RX and TX pin *opposite* harts (RX→hart1 app-recv, TX→hart0 ACK-NAPI),
each leaving the other idle. The RX DMA writer shows **0 stalls** at 200 → the datapath is never the
receive limit, so 1 Gbit is a CPU wall not a wire wall. The opposite-core asymmetry is what the
fan-out exploits.

## Effort 03 — the RX fan-out (RX −P2 = 223)

`RxSteer` (milan_soc.py) buffers each frame's head, hashes the IPv4/TCP 4-tuple (parity of src/dst
IP + ports), and routes the whole frame — flow-consistently, no reorder — to q0/q1; non-IP/TCP → q0.
Two `RingDMAWriter`s: q0 = `milan_dma_rx` @0xf0003024, q1 = `milan_dma_rx1` @0xf0003084; q1 IRQ
reuses the unused `ev.tx` line. Driver refactored to per-queue `struct kl_rxq[2]`, 2 threaded NAPI
(pinned to 2 harts from userspace), shared IRQ schedules both with q0 owning the re-enable (gated on
q1-empty). `hash_sel` CSR @0xf0003080 (1 = force all→q0 bypass); telemetry q0/q1_frames @0x…78/…7c.
q0/TX CSR ABI unchanged. Sim: `test_rx_steer.py`.

```
RX fan-out (wire → memory):
  MAC → PTP-ts → TCAM filter → RxSteer →↓ hash(4-tuple)
                                   q0 → RingDMAWriter → ring0 → IRQ → NAPI0 → hart 0
                                   q1 → RingDMAWriter → ring1 → IRQ → NAPI1 → hart 1
```

Verified on silicon: steering splits flows (even ~26k/24k frame split); both harts ~85% (were
1-idle); **socket-lock 15% → 4.5%** (flows core-local); **RX −P2 = 113 + 110 = 223 Mbit/s** — the
fan-out scales past 200 where the HW isn't the wall.

**TX −P2 stayed 186** — no CPU fix moves it. At 186 the system is **22.8% idle** (not CPU-bound), the
TX reader is **52% stalled** (traffic-shaper backpressure) + **45% idle** (DRAM read latency). The
fan-out removed the CPU ceiling and exposed the TX-datapath wall underneath.

## Where the 4 queues live (and why TX ≠ RX)

The four queues are **802.1Qav CBS traffic-class queues on the TX egress path only** (AVB QoS:
class A/B audio, best-effort, control), inside `traffic_controller_802_1q` — a transient fan-out:
single stream in → classify by PCP into 4 shaped queues → CBS credit → arbitrate → **back to one
stream** before the MAC. They are **not** RX DMA channels.

```
TX (memory → wire):  RingDMAReader → [traffic_controller_802_1q: 4 CBS queues → 1] → PTP → arbiter → MAC
                                       ^^^ TX throughput ceiling ~186 lives here
RX (wire → memory):  MAC → PTP → TCAM filter → RingDMAWriter → ring   (single stream, no shaper → 200)
```

Every TX frame passes the CBS shaper; RX has no equivalent. That is why RX reaches 200 and TX caps
at 186, and why the RX fan-out (CPU-side) helps RX cleanly but leaves TX against the datapath wall.

## Direct proof the datapath is the TX limit (datapath-input probe)

Effort 03 *inferred* the TX-datapath ceiling from reader-side counters. To prove it directly,
a counter (`MilanDebug.dp_in_probe`, bitstream `vexii_dpin.bit`) was placed on the TX datapath
**input** — the `traffic_controller_802_1q` `s_axis`, in the 50 MHz `milan_cd` domain —
counting `busy` (valid&ready), `stall` (valid&~ready → the reader offers a beat and the
datapath *refuses* it) and `starve` (~valid → the reader has nothing to offer). The three
sum to `cyc` exactly, so the percentages are self-consistent.

Measured on silicon (MTU 1500, single zerocopy TX flow, 8 s window):

| rate | driver | busy | stall | starve | reading |
|---|---|:---:|:---:|:---:|---|
| 62.7 Mbit/s | rootfs, no TSO | 2% | 26% | **71%** | datapath starved — has headroom |
| 145 Mbit/s | rxfan1 HW-TSO | 4% | **60%** | 34% | datapath stalled — it is the wall |
| 138 Mbit/s | rxfan1 −P2 | 4% | **59%** | 36% | same as single flow |

Three findings settle it:
1. As offered load rises 62 → 145 Mbit/s the datapath input flips **starve-dominated (71%) →
   stall-dominated (60%)** — the textbook signature of a stage becoming the bottleneck.
2. **−P2 (2 flows on 2 harts) matches single-flow** (138 vs 145 total, stall 59 ≈ 60%). A
   CPU-bound TX would gain from the second hart; it does not → the *shared* TX datapath caps
   both flows.
3. It is **not raw bandwidth**: the datapath is 64-bit @ 50 MHz = 3.2 Gbit/s but only **4%
   busy** at the ceiling. The 60% stall is the shaper's per-frame grant/serialization latency
   (`classifier → per-queue FIFO → traffic_shaping_core` CBS grant); the 34% starve is the
   reader's residual DRAM read latency (secondary). This is exactly what a best-effort
   passthrough fast-path (below) would remove.

(Rates here are unpinned, hence below the pinned-SSH 186 above; the stall-vs-starve conclusion
is the invariant. `hash_sel=1` bypass must be set before any TCP so the flow is not split onto
q1 and dropped by a single-queue driver — otherwise SSH/iperf hang, ICMP notwithstanding.)

## To take TX past 200 (next, independent of the above)

Ordered by the datapath-input measurement (stall 60% ≫ starve 34%):

1. **Trim the shaper per-frame overhead (primary)** — a passthrough fast-path in
   `traffic_controller_802_1q` when no CBS shaping is enabled, or raising `milan_cd` 50 → 100 MHz.
   This attacks the dominant **60% datapath-input stall** and is the only lever that moves the wall.
2. **Hide the reader's DRAM latency (secondary)** — larger AXI read bursts / prefetch to cut the
   34% starve. Note `burst_beats` 16 → 64 (cf98505) did **not** move end-to-end TX — consistent
   with the probe: the reader is not the dominant limit, so amortizing its DRAM reads can't raise
   a datapath-bound ceiling. Only worth revisiting after the shaper stall is removed.

## Artifacts

| item | id |
|---|---|
| Gateware HW-TSO | `vexii_hwtso.bit` · milan-fpga `78633ed` · WNS +0.123 · 115200 |
| Gateware RX fan-out | `vexii_rxfan.bit` · milan-fpga `d1bbed7` · WNS +0.135 · 70% LUT |
| Gateware datapath-input probe | `vexii_dpin.bit` · milan-fpga `064485a` (probe) + `cf98505` (burst-64) |
| Datapath-input probe | `MilanDebug.dp_in_probe` (txdp_in) · CSRs busy/stall/starve/cyc @0xf0004060–6c |
| Driver HW-TSO | kl-eth `tso1` · milan-tests-avb `151032d` |
| Driver RX fan-out | kl-eth `rxfan1` · milan-tests-avb `01a484c` |
| Sim HW-TSO | `sw/litex/test_tx_bd.py::test_tso_hw` |
| Sim RX steering | `sw/litex/test_rx_steer.py` |

## Ops notes

- rxfan gateware steers RX to 2 queues — the **single-queue rootfs driver only reads q0**, dropping
  ~half the frames (SSH SYN lost → timeout). Unblock: `devmem 0xf0003080 32 1` (hash_sel bypass) via
  console → deploy `rxfan1` → `devmem 0xf0003080 32 0`.
- iperf3 serves one test/port → use 2 peer ports for −P2. Split flows across queues with
  `iperf3 --cport` (5201/5202 share parity, so cport parity picks the queue: 30000→q0, 30001→q1).
  Pin the napi threads (`ps` → `[napi/eth%d-N]`) with the static `pin` helper.
- Board rootfs bakes the peer's **id_rsa.pub** (567 B) in authorized_keys → SSH with the peer's
  default key (no `-i`).
