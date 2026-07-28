# Traceability — IEEE 802.1AS-2020 (gPTP) — hardware-assist scope

Part of [`docs/SPEC_TRACEABILITY.md`](../SPEC_TRACEABILITY.md). Clause numbers
verified against the local standards PDFs (`$STANDARDS_DIR/802.1AS-2020.pdf`). Architecture split
(normative: [`docs/ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md)): the **protocol** (BMCA,
Announce/Sync/Pdelay state machines, servo) runs in `ptp4l`/linuxptp on the
softcore; the **fabric** provides the PTP hardware clock and event-message
timestamping. RTL rows therefore cover the timestamping/clock clauses; the
protocol rows are SW and verified on the wire (BENCH features at the
ProfiShark taps). Milan gPTP deltas (priority1, pdelay rules) are in
[`milan-v12.md`](milan-v12.md).

Modules: `hdl/ieee8021as/ptp_timestamp/` (`timestamp_counter`, `ptp_ts_core`,
`ptp_ts_top`, `ptp_csr_sync`), `hdl/common/cdc_*`.

| # | Clause | Required behavior | Module / agent | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|----------------|------------------------------|----------------|
| AS-1 | 8.2 (timescale) | PTP timescale: monotonic ns clock, settable epoch, frequency-adjustable | timestamp_counter (PHC: settime/adjtime/adjfine w/ fractional carry, gettime snapshot) | ✅ RTL ptp (201 k vs 128-bit accumulator model) | 8.2: every timestamp, AVTP presentation time and CRF value inherits this counter's correctness. |
| AS-2 | Annex B.1 (LocalClock) | LocalClock frequency accuracy within ±100 ppm, adjustable with fine granularity | timestamp_counter on the fixed 125 MHz reference (REQ-PTP-07) | ✅ RTL ptp (adjfine granularity vs model); 🟩 board: `ethtool -T` PHC + ptp4l lock quality | B.1.1: a reference outside ±100 ppm can be unservoable by peers even with a perfect protocol. |
| AS-3 | 8.4.3 (timestamp measurement plane) | Timestamps captured at the reference plane; deviation compensated via ingressLatency/egressLatency | ptp_ts_top/core capture; latency constants applied in ptp4l config | ✅ RTL ptp_ts (golden delta model: any ts↔frame mis-pairing shifts a delta by a whole frame time); SILICON tap-measured constants (3511 ns Arty / 1490 ns AX) — the asCapable breakthrough | 8.4.3: uncompensated RX-stamp lateness made asCapable *never* true — the single biggest gPTP field bug of this project. |
| AS-4 | 8.4.3 (per-unit calibration) | Latency constants valid per instance/board, not per bench | — procedure gap | ❌ MISSING — constants are bench-calibrated; ingress/egress split never measured separately (gaps §4); no calibration procedure exists | 8.4.3: on any new PHY/board the current constants are wrong by an unknown amount — silently degrading, not failing. |
| AS-5 | 11.3 / 8.4.3 | Only PTP **event** messages timestamped (Sync, Pdelay_Req, Pdelay_Resp); general messages never capture | ptp_ts_core (msgType[3]==0 rule, seq echoed verbatim) | ✅ RTL ptp_ts (interference suite: event frames inside line-rate floods, general-storms, runts, VLAN lookalikes) | 11.3: stamping a general message mis-pairs seq→timestamp and poisons the pdelay math with whole-frame errors. |
| AS-6 | 10.2 / 10.3 (BMCA, port states) | Best-master selection, Announce handling | ptp4l (SW) | ✅ wire: BENCH es-1.1 ALINX-GM half (announce 1.0001 s cadence, priority1/clockClass at tap); ❌ DUT-wins-BMCA variant blocked on bench-switch claim (gaps §4, attack-order bottom) | 10.3: Milan requires the PAAD to be a *capable* GM; the blocked variant is the only unproven leg. |
| AS-7 | 11.1 / 11.2 (MD sync SMs) | Sync/Follow_Up generation & receipt, rateRatio | ptp4l (SW) + HW timestamps | ✅ wire: BENCH es-1.1 half (sync 8/s at tap); SILICON both boards HW-ts green zero-overrides | 11.2: sync cadence + correct timestamps are what the whole media clock chain stands on. |
| AS-8 | 11.2.19 (MDPdelayReq) | Peer delay measurement; asCapable determination | ptp4l (SW); PDELAY forensics CSR 0x6E4 | ✅ wire: BENCH es-1.1 half (pdelay 1/s); SILICON asCapable stable post-AS-3 fix | 11.2.19: asCapable=false silently removes the port from the gPTP domain — no error, just no sync. |
| AS-9 | 8.1 / 10.6 (domain, intervals) | Single gPTP domain 0, standard message intervals | ptp4l config (S65 ships /usr/sbin prepend) | ✅ wire BENCH cadence checks | 10.6: wrong intervals violate the Milan profile even when sync converges. |
| AS-10 | 11.4 (message formats) | Correct on-the-wire PTP message encoding | ptp4l (SW) | ✅ wire (tap dissection); ➖ RTL N/A — fabric never builds PTP messages; ❌ tsn_gen NO gPTP MODEL | 11.4: a gPTP YAML model would let packet_gen replay GM behaviors (BMCA fixtures) without the 255-claimant test machine. |
| AS-11 | 12–16 (other media) | 802.11 / EPON / CSN media-dependent layers | — | ➖ N/A — full-duplex 802.3 only (Clause 11 applies) | Media out of scope. |
| AS-12 | 10.3 (PortAnnounceInformation / ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES) + 10.6 (intervals) | The announce/sync/pdelay cadence must hold **while the host is under load** — a grandmaster that stops transmitting for `announceReceiptTimeout` × `announceInterval` (3 × 1 s) is correctly deposed by every peer, so cadence is what keeps the BMCA from ever being provoked | `ptp4l` (SW) + `RxSteer` (`sw/litex/milan_soc.py`) — the ingress separation that keeps gPTP off the bulk ring | ✅ MODEL: `tests/features/gptp_announce_receipt_timeout.feature` (10 scenarios: timeout boundary both sides + cadence budget fed real `pmc PORT_STATS_NP` deltas, one window that holds and one that breaks); ✅ SILICON 2026-07-28 A/B/A: `rx_queues: 1` ALINX loses the GM under a 935 Mb/s RX flood, `rx_queues: 2` Arty holds it, and the Arty reproduces the loss when `RxSteer.hash_sel` bypasses steering on the same board — [`GPTP_GM_LOSS_UNDER_RX_LOAD.md`](../findings/GPTP_GM_LOSS_UNDER_RX_LOAD.md) | 10.3: this is defect **D7** ("when the device receives packets the gPTP GM changed for no reason"). The re-election is *conformant* — the defect is upstream, in a build where bulk RX and gPTP share one ring and one NAPI so `ptp4l` never gets the CPU. `configs/endstation_ax7101_8x8.yaml` still ships `rx_queues: 1` and its own comment says the USER's 2-ingress-queue directive "is simply not implemented on this build". |

**tsn_gen status: ❌ NO MODEL.** A `data_link/gptp/` family (Sync/Follow_Up/
Pdelay/Announce) is the enabler for the blocked AS-6 DUT-wins-BMCA
recreation: packet_gen as the adjustable-priority claimant instead of the
bench switch.
