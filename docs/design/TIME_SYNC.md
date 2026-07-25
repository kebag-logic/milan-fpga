<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# Time synchronization — gPTP, the PHC, and the media clock

How time works in this system, top to bottom: what 802.1AS (gPTP) gives us,
where hardware timestamps are made and how they reach `ptp4l`, and how the
gPTP-disciplined clock becomes the 48 kHz media clock that the DACs and ADCs
actually run on. Register offsets follow
[`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) (the CSR ABI
authority); status claims carry their in-repo evidence. Written 2026-07-25.

![The time-sync clock chain](../diagrams/timesync_chain.png)

> The picture above is generated (editable
> [timesync_chain.drawio](../diagrams/timesync_chain.drawio); regenerate with
> `python3 docs/diagrams/timesync_chain.gen.py docs/diagrams/timesync_chain &&
> rsvg-convert -w 2000 docs/diagrams/timesync_chain.svg -o
> docs/diagrams/timesync_chain.png`).

## 1. Concept — the three clocks

gPTP gives every device on the AVB segment one shared nanosecond timeline.
One node is elected grandmaster (GM); everyone else measures its link delay to
its neighbor (pdelay) and steers a local hardware clock until the shared
timeline agrees to nanoseconds. Milan requires this (it is what makes
presentation times meaningful), and everything below the protocol runs in our
fabric.

Three clocks exist on each board, chained in one direction:

1. **The network clock — the PHC** (PTP Hardware Clock). A 64-bit
   nanosecond counter in the fabric
   (`hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv`). This is the clock
   gPTP disciplines and the clock every hardware timestamp is drawn from.
   When the board is GM, the PHC free-runs and everyone else follows it.
2. **The system clock** — Linux `CLOCK_REALTIME` on the softcore. `phc2sys`
   copies the PHC into it so userland timestamps and timers agree with
   network time ([`../ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md)
   "PHC clock ops": *ptp4l disciplines it, phc2sys mirrors it to
   CLOCK_REALTIME*). Nothing in the media path depends on it.
3. **The media clock** — the 24.576 MHz audio MMCM output, divided to the
   48 kHz sample grid that the I2S/TDM front-ends run on. It is a *physical*
   clock (a DAC cannot consume "nanoseconds"), so it cannot be written like
   the PHC — it is *steered*: the CRF stream carries the talker's media clock
   as gPTP timestamps, and the MMCM-DRP servo trims our MMCM until the local
   rate matches (section 3).

The chain, in one sentence: gPTP disciplines the PHC; the PHC timestamps
frames and dates every AVTP/CRF timestamp; CRF plus the servo turn that shared
timeline into an actual audio clock edge.

## 2. Mechanism — the hardware timestamp path

### 2.1 The PHC counter and its CSR group (0x500)

`timestamp_counter.sv` is a fractional-nanosecond phase accumulator
`{ns[63:0], frac[23:0]}`. Each tick adds `PTP_INCR + PTP_ADJ`, both Q8.24
nanoseconds, which gives software the full linuxptp clock-ops set
(REQ-PTP-01..04):

* **rate** (`adjfine`): `PTP_ADJ` (0x508) is a signed per-tick addend;
* **settime**: `PTP_TOD_WR_*` + `PTP_CMD[0]` loads an absolute time;
* **adjtime**: `PTP_OFFSET_*` + `PTP_CMD[1]` adds a signed delta once;
* **gettime**: `PTP_CMD[2]` latches a snapshot into `PTP_TOD_RD_*`
  (64-bit reads on the 32-bit bus are not atomic — the snapshot latch is the
  coherent-read mechanism, [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md)
  "Notes").

The CSR plane and the PHC live in different clock domains;
`ptp_csr_sync.sv` carries values plus toggle-synchronized apply strobes
across (REQ-CSR-03).

On the fully-FPGA LiteX SoCs the PHC clock (`gtx_clk`) is tied to the
datapath clock (`sw/litex/milan_soc.py`, the
`i_gtx_clk = ClockSignal(milan_cd)` instantiation) — 50 MHz Arty, 100 MHz
AX7101 — and `PTP_INCR` carries the matching ns-per-tick (its reset value
`0x0800_0000` = 8.0 ns assumes the recommended 125 MHz reference,
REQ-PTP-07).

The tie also satisfies the timestamping core's one hard requirement:
`ts_in` synchronous to the AXIS domain (`ptp_ts_core.sv` header,
2026-07-13 redesign note).

### 2.2 Where frames get stamped

`ptp_ts_top.sv` sits in-line in `milan_datapath.sv`: the TX tap between the
CBS shaper and the TX arbiter to the MAC, the RX tap directly after MAC
ingress, before the destination-MAC filter (instance `ptp_timestamp`,
streams `tx_axis_shaper_to_ts -> tx_axis_dp_to_arb` and
`rx_axis_to_ts -> rx_axis_ptp_to_filt`). Both taps are pure pass-throughs —
they never stall a frame. Per direction, `ptp_ts_core.sv`:

* latches the live PHC value at the frame's **first beat** (SOP);
* parses ethertype (`0x88F7`), PTP `messageType` and `sequenceId` at their
  fixed untagged-gPTP offsets;
* **qualifies at TLAST**: ethertype match AND an **event** message
  (`msgType[3] == 0` — Sync, Delay_Req, Pdelay_Req, Pdelay_Resp). General
  messages (Announce, Follow_Up, Signaling) are never recorded — stamping
  them would only burn record slots and invite seq collisions
  ([`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) row AS-5).

Qualify-at-TLAST is the load-bearing part. The original core decided the
record when a timestamp CDC handshake returned, which raced the ingress beat
rate both ways — first record never emitted on slow MII beats, stale
one-frame-late pairing after, records lost on fast back-to-back frames.

The full root cause, the synchronous redesign, and the netlist-forensics
fallout (LUTRAM-inferred record queues mis-wired by the cross-hierarchy
optimizer, rebuilt as explicit flops) are recorded in
[`../findings/PTP_TS_METADATA_FIX.md`](../findings/PTP_TS_METADATA_FIX.md).

Both exchanges, as this design stamps them:

![gPTP timelines: peer delay and Sync/Follow_Up with the PHC latch points](../diagrams/wd_gptp_pdelay.png)

> Generated chronogram (master
> [wd_gptp_pdelay.json](../diagrams/wd_gptp_pdelay.json); regenerate with
> `~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py
> docs/diagrams/wd_gptp_pdelay.json`). Each tap's `ptp_ts_core` latches the
> PHC at SOP and qualifies the record at TLAST (event messages only), so
> `t1`/`t4` come from hardware records while the peer's `t2`/`t3` arrive
> inside `Pdelay_Resp`/`Pdelay_Resp_Follow_Up`; `ptp4l` computes
> `meanLinkDelay = ((t4 - t1) - (t3 - t2)) / 2` (802.1AS 11.2.19) and the
> result is published at CSR 0x6E4 (section 4). Cadences per
> [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) rows
> AS-7/AS-8: pdelay 1/s, Sync+Follow_Up 8/s.

### 2.3 How stamps reach the driver — the record contract

Each qualified frame emits a two-beat, 16-byte metadata record
(`ptp_ts_core.sv` output FSM; contract v2.1 in
[`../findings/PTP_TS_METADATA_FIX.md`](../findings/PTP_TS_METADATA_FIX.md)):

| beat | content |
|------|---------|
| 0 | `ns[63:0]` — the disciplined PHC value at SOP (same epoch as `/dev/ptp0`) |
| 1 | `{40'0, seq[15:0], msgType[3:0], 2'0, marker=1, dir}` — `seq` is the frame's big-endian sequenceId verbatim (no byte swap anywhere), `dir` 0=RX 1=TX |

The always-1 **marker** (bit 1) is the driver's race-free slot sentinel: DMA
lands word 0 before word 1, so "marker set" proves the timestamp word is
complete.

TX and RX records pass per-direction 16-deep `axis_fifo`s, a
round-robin mux, and a final FIFO (`ptp_ts_top.sv`), then the **dma-ts**
engine (a LiteX simple-mode DMA writer in loop mode, register block in
[`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) "DMA
registers"; its absolute address is build-generated — `build/csr.csv` is the
authority, stale device trees have burned three generations of addresses)
writes them into a coherent DRAM ring.

`tlast` is deliberately **not** forwarded to the DMA writer — forwarded,
LiteX treated every record as end-of-transfer and each record overwrote
slot 0 (the "lossy mailbox", found on silicon).

The kl-eth driver (the-private-test-repo) drains the ring: TX records
complete the one pending timestamp-requested skb via `skb_tstamp_tx`
(`SO_TIMESTAMPING`), RX records ride a small wire-order FIFO matched by
order with `seq` as the consistency check.

`o_tx_ts_ready` pulses `IRQ_STATUS[0]` (0x010) at core emission — which
precedes the DMA landing by microseconds, so the driver pairs the IRQ drain
with a NAPI-poll fallback and `ptp4l` runs `tx_timestamp_timeout` raised
well above default (500 on the current images,
[`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md)
section 8).

One RX-path prerequisite is easy to forget: gPTP frames must arrive
*unpadded*. The RX DMA originally reported 8-byte-rounded lengths and `ptp4l`
rejected every pdelay_req as a bad message (trailing zeros parse as a bogus
TLV). Root cause and the true-length gateware fix:
[`../findings/GPTP_RXPAD_ROOTCAUSE.md`](../findings/GPTP_RXPAD_ROOTCAUSE.md).

### 2.4 The ingress/egress latency constants

The taps stamp at the MAC-side AXIS boundary, not at the wire (802.1AS
8.4.3's "reference plane"), so each board carries a constant correction in
its `ptp4l` config.

The values are **tap-measured** (ProfiShark, inline):
**ingressLatency 3511 ns on the Arty, 1490 ns on the AX7101, egressLatency
0**, provisioned by `S50milan` at boot
([`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md) section 8;
[`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) section 4).

Uncompensated, the late RX stamps kept `asCapable` permanently false — the
single biggest gPTP field bug of this project
([`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) row AS-3).

Two honest caveats, tracked as traceability rows: the constants are
bench-calibrated per board *type*, with no per-unit calibration procedure,
and the ingress/egress split was never measured separately — only the sum
(row AS-4, MISSING). The fabric does expose `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT`
CSRs (0x540/0x544) for a future in-fabric correction, but today the exported
wires terminate unused in `milan_datapath.sv` — the compensation lives
entirely in the `ptp4l` config.

### 2.5 Who runs where

The split is deliberate and normative
([`../ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md);
[`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) header):
**protocol in software, time in fabric.**

| Agent | Where | Job |
|-------|-------|-----|
| `timestamp_counter` + `ptp_csr_sync` | fabric | the PHC: rate/offset/absolute set, snapshot reads |
| `ptp_ts_top` / `ptp_ts_core` | fabric | per-frame event-message timestamps, both directions |
| dma-ts ring + kl-eth | fabric + driver | records to DRAM; `/dev/ptp0` clock ops; `SO_TIMESTAMPING` |
| `ptp4l` | softcore | BMCA, Announce/Sync/Pdelay state machines, the clock servo |
| `phc2sys` | softcore | PHC -> `CLOCK_REALTIME` |
| `gptp2csr.sh` | softcore daemon | publishes gPTP state into fabric CSRs: GM id 0x624/0x628 (the LOCAL clock id when we are GM), measured pdelay 0x6E4, AS_PATH parent bridge 0x730/0x734 from `PARENT_DATA_SET` — so ADP/AEM answer with wire truth ([`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md) section 8) |
| `stream_phc_sync.sh` | softcore daemon | media/PHC watchdog; dormant while `ptp4l` holds SLAVE or MASTER |

The fabric never builds a PTP message (row AS-10 marks that N/A for RTL);
`ptp4l` never sees a raw timestamp race — the fabric guarantees exact
pairing by construction.

## 3. The media clock

### 3.1 The audio MMCM — a clean, integer-derived 24.576 MHz

Sample clocks are made from a dedicated MMCM, not from logic dividers of the
datapath clock: fractional-N edge jitter on MCLK measurably wrecked the
converters (analog THD+N collapsed to -4.5 dB; history in
`hdl/ieee1722/aaf/KL_i2s_playback.sv`'s header).

The chain is two-stage and **integer-only** (`sw/litex/milan_soc.py`,
`_CRG`): 100 MHz -> PLL /2 x23 /37 -> 31.081081 MHz -> MMCM x34 /43 ->
**24.575739 MHz = 24.576 MHz -10.6 ppm**.

Integer dividers are a servo prerequisite: UG472 forbids fractional divide
in fine-phase-shift mode, and the best single-stage integer alternative
lands -186 ppm — beyond the servo's trim budget
([`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) section 2).

`/512` of this clock is the 48 kHz sample grid; I2S (`MCLK/SCLK/LRCK`) and
TDM front-ends are plain registered dividers of it.

### 3.2 CRF out — `KL_crf_tx`, the media-clock talker

`hdl/ieee1722/crf/KL_crf_tx.sv` emits the Milan CRF Media Clock Stream
(Milan v1.2 7.3.1 / IEEE 1722-2016 Clause 10): subtype 4, type
CRF_AUDIO_SAMPLE, pull 0, base_frequency 48000, one 64-bit timestamp per
PDU, timestamp_interval 96 — one PDU per 96 sample events = 500 PDU/s.

The timestamp grid is the **real media clock**: an own `/512` divider of
`clk_audio` counts sample ticks, and every 96th event crosses into the
datapath domain where the live PHC value is latched as that event's gPTP
time. The wire therefore carries the actual audio-MMCM rate as the PHC sees
it — not a synthetic 2 ms accumulator.

Milan applies the stream **presentation time offset to CRF exactly as to
media streams**: every emitted timestamp is `event gPTP time + transit_ns`,
from the same offset source as the AAF framer (SET_STREAM_INFO
accumulated-latency field; reset 2 ms) — see the `transit_ns_i` wiring in
`hdl/milan/milan_datapath.sv`.

A PDU that would collide with a busy serializer is skipped whole, so emitted
timestamps stay truthful and only the cadence stretches. The stream leaves
untagged on the low-rate control lane until a second lwSRP talker
declaration exists (section 5).

### 3.3 CRF in — `KL_crf_rx`, the measurement half

`hdl/ieee1722/crf/KL_crf_rx.sv` validates every CRF PDU of the selected
stream against the Milan 7.3.2 profile constants (wrong pull/base/dlen/
interval/type increments `fmt_err`) and produces the two servo inputs:

* **phase**: `delta = crf_ts - ptp_now` at each accepted PDU (CSR 0x744,
  same signed-delta contract as the AAF `ts_delta` at 0x6EC);
* **frequency**: `rate` (CSR 0x748) = accumulated timestamp advance across a
  256-PDU ring (512 ms) minus the nominal 512 ms — signed ns per window,
  i.e. the talker's media clock measured against gPTP. Implementation
  (2026-07-25): the ring is a 256×32 **single-port READ_FIRST BRAM** —
  storing the truncated 32-bit timestamp is bit-exact because the window
  subtraction is congruent mod 2^32, and one same-port access reads the
  oldest entry and overwrites it in place. `rate` updates one clock after
  the accepted PDU (invisible at any CSR poll rate; pinned by the
  `tb/verilator/crf_rx` regression). The previous 256×64 flop file was
  the exact placer-overflow victim of the first 8×8+chmap build;
* **lock**: 8 clean consecutive PDUs to lock, 100 ms of silence (or a
  validation error) to unlock — mirroring the AAF media-lock contract —
  with lock/unlock event counters feeding CLOCK_DOMAIN GET_COUNTERS when
  `clock_source` = CRF.

The followed stream comes from the CRF sink bind (ACMP listener sink 1 —
the bind wins) with the CSR pair 0x738/0x73C/0x740 as the manual bench
lever (`milan_datapath.sv`, `crf_rx` instance).

### 3.4 The MMCM-DRP servo — `KL_mmcm_drp_servo` (MCSRV 0x8F8/0x8FC)

`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` closes the loop when
`clock_source == 2` (the CRF CLOCK_SOURCE descriptor); in every other mode
it is IDLE with zero DRP/PS activity.

The loop error is **differential rate**, not phase: `e = local_rate -
crf_rate`, both in gPTP-ns per 512 ms of media events (the module measures
our own audio clock against the PHC over a matching 512 ms window; 1 ppm =
512 units). `CRF_DELTA` (0x744) is deliberately NOT a loop input — it
contains the arbitrary talker+transit phase constant.

A PI controller (integrator halves the error per window, bounded slew
+-100 ppm/window, bounded authority +-200 ppm) drives two actuators:

* **fine (the real one)**: MMCME2 dynamic fine phase shift — UG472-linear
  steps of `1/(56*F_VCO)` = 16.9 ps, glitch-free, wrap-around — so a
  sustained step *rate* is a permanent frequency trim of the live audio
  clock. The 200 MHz PS clock gives a 260 ppm slew ceiling, > 2x the
  10.6 ppm base + 100 ppm talker budget (`milan_soc.py` `_CRG` comment).
* **coarse (DRP, XAPP888)**: on every activation the engine read-verifies
  the CLKOUT0 divider registers; only with `auto_repair` set (MCSRV_CTRL
  0x8FC bit 1, reset 0, bench-gated) and a mismatch does it reprogram them
  through the full reset-sequenced read-modify-write. DRP fractional fields
  have 1/8 resolution (>= 1953 ppm/LSB) — three orders too coarse for a ppm
  servo, which is exactly why the fine-PS actuator exists.

Hardening from the silicon rounds:

* a **step guard** discards any window whose error exceeds ~1024 ppm (a
  local PHC step — GM reboot — used to wind the integrator to the clamp and
  stick there);
* **HOLDOVER** on CRF unlock freezes the trim but keeps stepping at the
  held rate;
* `ps_invert` (0x8FC bit 0) is the bench polarity knob from the mf51
  bring-up where silicon stepped opposite the TB's UG472 reading.

`MCSRV_STAT` (0x8F8) exposes state
(IDLE/VERIFY/REPAIR/ACQUIRE/LOCKED/HOLDOVER/FAULT), the DRP
verify/mismatch and fault flags, and the **signed applied trim in 1/16 ppm
units** in bits [31:16].

### 3.5 The coherent chain and the media-lock rule

**Coherent chain** means: one audio-MMCM lineage carries every media-rate
element — the ADC capture front-end, the CRF talker's timestamp grid, and
(through the servo) the listener's playback clock.

There is no software resampler and no NCO anywhere in the path; the old
playback NCO was removed by the exact-recovery rule and its trim output
reads 0 (`KL_i2s_playback.sv` header). When the servo locks, talker and
listener run at the *same* frequency, so the playback FIFO neither drains
nor fills and the drift-glitch class (underrun repeats / overrun drops) ends.

The chain was measured end to end 2026-07-23 at **-83.9 dB loop THD+N — the
CS4344+CS5343 converter datasheet floor**
([`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) roadmap item 6;
[`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md) section 2).

The **media-lock rule** (`hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`, the
MEDIA_LOCKED engine): with an **internal** clock source
(`clock_source_index == 0`) the stream locks on the first valid PDU — lock
means "buffer position established", and slips are accepted as
underrun/overrun rail events.

With an **external** source (CRF) the stream locks **only once the
recovered clock has converged near nominal** (`servo_conv` — the
playback-FIFO convergence flag: fill inside the mid-window sustained for
100 ms, `KL_i2s_playback.sv`), and losing convergence while locked is an
immediate MEDIA_UNLOCKED event. Internal locks immediately; external must
earn it.

### 3.6 AAF presentation time against the PHC

The same PHC dates the audio itself: the AAF packetizer latches
`avtp_timestamp = ptp_now + transit_ns` at each PDU's first sample pair
(`hdl/ieee1722/aaf/KL_aaf_packetizer.sv`, `tsw_val_r` assignment), and the
listener-side monitor computes `ts_delta = avtp_timestamp - ptp_now` on
every accepted PDU (CSR 0x6EC), counting LATE (delta < 0) and EARLY (delta
beyond offset + margin) per Milan Table 5.6.

This is the number the latency-equals-pto work steers by, and the per-stage
breakdown of where the time goes lives in
[`../AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md) (the 0x870 tap block
latches `ptp_now` epochs per measured frame).

## 4. Time-related CSRs — quick table

Rows below `PTP_EGRESS_LAT` marked (*) are live in `milan_csr.sv` and
documented in [`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md)
section 8, but have no row in
[`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) yet — the map
is the ABI authority and closing that gap is listed in section 5. Meanings
are quoted from the map where a row exists, from the RTL localparam docs
otherwise.

| Offset | Name | One line |
|--------|------|----------|
| `0x008` | `CAP[9]` | PTP capability present |
| `0x010` | `IRQ_STATUS[0]` | `tx_ts_ready` — TX egress timestamp record emitted |
| `0x500` | `PTP_CTRL` | `[0]` PHC counter enable |
| `0x504` | `PTP_INCR` | nominal Q8.24-ns increment per tick |
| `0x508` | `PTP_ADJ` | signed Q8.24-ns adjfine addend added each tick |
| `0x510/0x514` | `PTP_TOD_WR_LO/HI` | settime target (ns) |
| `0x518/0x51C` | `PTP_OFFSET_LO/HI` | adjtime signed delta (ns) |
| `0x520` | `PTP_CMD` | W1S strobes: `[0]` load, `[1]` adjust, `[2]` snapshot |
| `0x530/0x534` | `PTP_TOD_RD_LO/HI` | latched TOD from the snapshot round trip |
| `0x540` | `PTP_INGRESS_LAT` | ingress latency correction, ns (fabric hook — unused today, section 2.4) |
| `0x544` | `PTP_EGRESS_LAT` | egress latency correction, ns (same status) |
| `0x624/0x628` | `ADP_GPTP_GM_LO/HI` | gptp_grandmaster_id published into ADP/AEM (`gptp2csr.sh`) |
| `0x62C` | `ADP_GPTP_DOMAIN` | `[7:0]` gptp_domain_number |
| `0x6C8` | `PCMRX_TS` | avtp_timestamp of the last ring-accepted PDU |
| `0x6E4` (*) | `A_GPTP_PDELAY` | measured neighbor propagation delay, ns (daemon-written) |
| `0x6EC` (*) | `A_AVTPRX_TSD` | signed ts_delta at the last accepted AVTP PDU |
| `0x730/0x734` (*) | `A_AS2_LO/HI` | AS_PATH parent bridge clock id (0 = none/unknown) |
| `0x738` (*) | `A_CRF_CTRL` | `[0]` CRF sink enable; RO `[31]` locked |
| `0x73C/0x740` (*) | `A_CRF_SIDLO/HI` | CRF sink stream_id |
| `0x744` (*) | `A_CRF_DELTA` | RO signed `crf_ts - ptp_now` (phase) |
| `0x748` (*) | `A_CRF_RATE` | RO signed ns error per 512 ms window (frequency) |
| `0x74C` (*) | `A_CRF_STATUS` | RO `{pdu16, fmt_err8, seq_err8}` |
| `0x750` (*) | `A_CRFT_CTRL` | `[0]` CRF talker enable |
| `0x754/0x758` (*) | `A_CRFT_SIDLO/HI` | CRF talker stream_id |
| `0x75C/0x760` (*) | `A_CRFT_DMLO/HI` | CRF talker destination MAC |
| `0x764` (*) | `A_CRFT_COUNT` | RO CRF PDUs emitted |
| `0x874` / `0x894` | `LTAP_TX_EPOCH` / `LTAP_RX_EPOCH` | gPTP ns latched at the latency-tap reference frames |
| `0x8F8` | `MCSRV_STAT` | servo state/flags + signed trim in 1/16 ppm (`[31:16]`) |
| `0x8FC` | `MCSRV_CTRL` | `[0]` ps_invert (bench sign knob); `[1]` auto_repair enable per `milan_csr.sv` — the map row documents `[0]` only (drift noted in section 5) |
| LiteX `dma-ts` | `base/length/enable/loop/offset` | the timestamp record ring engine (address from `build/csr.csv`) |

## 5. Status (2026-07-25)

Proven, with the evidence next to each claim:

* **PHC + clock ops**: RTL-proven against a 128-bit accumulator model
  (201 k checks) — [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md)
  rows AS-1/AS-2.
* **Per-frame HW timestamps under interference**: RTL interference suite
  green (`tb/verilator/ptp_ts`, event frames inside line-rate floods) and
  silicon green 2026-07-13 (hwts5): 0 tx-timestamp timeouts steady-state,
  offset rms 2-5 ns *through* RX/TX/bidirectional floods, **peer delay
  600 us (SW stamps) -> 1.3 us (HW)** —
  [`../findings/PTP_TS_METADATA_FIX.md`](../findings/PTP_TS_METADATA_FIX.md)
  "Validation status".
* **asCapable + full sync through the reference AVB switch**: pdelay
  handshake both ways, board-as-GM relayed to a hardware-timestamped slave
  at rms 2-4 ns (2026-07-13) —
  [`../findings/GPTP_RXPAD_ROOTCAUSE.md`](../findings/GPTP_RXPAD_ROOTCAUSE.md).
  Both boards have since run hardware timestamps with zero config overrides
  (row AS-7).
* **CRF end to end**: sink lock on a bound stream proven on silicon (mf40);
  board-to-board CRF locked at **rate +6.7 ppm** (2026-07-21) —
  [`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md) section 9.
* **Media-clock servo silicon-proven**: coherent chain measured **-83.9 dB
  loop THD+N = the converter floor** (2026-07-23) —
  [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) item 6;
  [`../traceability/milan-v12.md`](../traceability/milan-v12.md) row M-DEV-15.

Partial or missing, each with its row id:

* **AS-4 — MISSING**: latency constants are bench-calibrated (3511/1490 ns);
  no per-unit calibration procedure exists and the ingress/egress split was
  never measured separately —
  [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) row AS-4,
  [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) section 4. Any
  new PHY/board is wrong by an unknown amount — silently degrading, not
  failing.
* **AS-6 — partial**: the DUT-wins-BMCA recreation is blocked on the bench:
  the reference AVB switch claims priority1 246 / clockClass 248 /
  clockAccuracy 0x20 and outranks every Milan-legal end-station value. The
  shipping priority1 must be 246; the bench 100 override is bench-only —
  row AS-6; [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md)
  section 4; [`../traceability/milan-v12.md`](../traceability/milan-v12.md)
  row M-DEV-1.
* **M-DEV-2/3/4 — partial**: the Milan pdelay edge-case deltas (multiple
  responses to one request, turnaround bound, negative pdelay handling) ride
  on `ptp4l` and were never explicitly recreated; only the normal path is
  wire-proven — [`../traceability/milan-v12.md`](../traceability/milan-v12.md)
  section 1.
* **M-CLK-2 — MISSING**: the CRF stream rides untagged best-effort (an
  SR-tagged unregistered stream would be pruned to zero ports); it needs the
  second lwSRP listener/talker attribute — row M-CLK-2;
  [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) section 2.
* **M-CLK-3 — row upgrade pending**: the actuator the row calls MISSING is
  now built and silicon-proven; the matrix row awaits the 1:1 review before
  its status flips — [`../traceability/milan-v12.md`](../traceability/milan-v12.md)
  row M-CLK-3.
* **M-CLK-5 — MISSING**: Milan 7.6 media-clock reference election /
  domain propagation logic on top of the (implemented) command layer —
  row M-CLK-5.
* **AS-10 — tooling gap**: no tsn_gen gPTP frame model; building one is the
  enabler for replaying the blocked AS-6 BMCA variant without the bench
  switch — [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md).
* **Servo residuals**: `auto_repair` stays 0 until the one-shot ClkReg
  readback is blessed on the bench, and the winning `ps_invert` polarity is
  still a CSR knob rather than the RTL default —
  [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) item 6.
* **Doc drift (this doc's own findings)**: the 0x6E4/0x6EC/0x730-0x764
  time CSRs and `MCSRV_CTRL[1]` are live in `milan_csr.sv` but missing from
  [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) (section 4
  table, rows marked *); `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` exist in the map
  but their fabric wires are unconsumed (section 2.4).
