# Traceability — IEEE 802.1AS-2020 (gPTP) — fabric-default scope

Clause numbers are verified against the local standards PDF
`$STANDARDS_DIR/802.1AS-2020.pdf`. Current implementation coverage is in the
[generated module matrix](MODULE_MATRIX.md), and the current hardware/software
boundary is in the [architecture guide](../overview/ARCHITECTURE.md). Since
VERSION `0x0002_0055`, `KL_gptp_shadow` and the pinned `gptp-processor` own
BMCA/BTCA, Announce, Sync, Pdelay, the PHC servo and atomic publication in the
default build. `ptp4l`/linuxptp is retained only by explicit
`--no-fabric-gptp` profiles. Processor and parent RTL evidence is recorded
below; #117 owns the still-open two-board acceptance. The current Milan
verdict, including gPTP blockers, is in the
[Milan v1.2 audit](../testing/MILAN_V12_AUDIT_2026-08-16.md).

Modules: [`hdl/ieee8021as/ptp_timestamp/`](../../hdl/ieee8021as/ptp_timestamp)
(`timestamp_counter`, `ptp_ts_core`, `ptp_ts_top`, `ptp_csr_sync`),
[`hdl/ieee8021as/gptp_plane/`](../../hdl/ieee8021as/gptp_plane), and the pinned
[`gptp-processor`](../../gptp-processor).

| # | Clause | Required behavior | Module / agent | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|----------------|------------------------------|----------------|
| AS-1 | 8.2 (timescale) | PTP timescale: monotonic ns clock, settable epoch, frequency-adjustable | timestamp_counter (PHC: settime/adjtime/adjfine w/ fractional carry, gettime snapshot) | ✅ RTL ptp (201 k vs 128-bit accumulator model) | 8.2: every timestamp, AVTP presentation time and CRF value inherits this counter's correctness. |
| AS-2 | Annex B.1 (LocalClock) | LocalClock frequency accuracy within ±100 ppm, adjustable with fine granularity | timestamp_counter on the profile-derived fixed Milan clock (REQ-PTP-07) | ✅ RTL ptp (adjfine granularity vs model); 🟩 historical option-off board evidence: `ethtool -T` PHC + `ptp4l` lock quality; ⚠️ default fabric board acceptance #117 | B.1.1: a reference outside ±100 ppm can be unservoable by peers even with a perfect protocol. |
| AS-3 | 8.4.3 (timestamp measurement plane) | Timestamps captured at the reference plane; deviation compensated via ingressLatency/egressLatency | default: `KL_gptp_shadow` RX tap + `KL_gptp_txstamp`; option-off metadata: `ptp_ts_top/core`, with live 0x540/0x544 correction | ✅ RTL `ptp_ts` golden delta/correction model and `gptp_shadow` timestamp pairing; historical silicon constants 3511 ns Arty / 1490 ns AX; ⚠️ default-plane board acceptance remains #117 | 8.4.3: uncompensated RX-stamp lateness made asCapable *never* true — the single biggest gPTP field bug of this project. |
| AS-4 | 8.4.3 (per-unit calibration) | Latency constants valid per instance/board, not per bench | -- procedure gap | ❌ MISSING -- constants are bench-calibrated; ingress/egress split never measured separately (gaps Section 4); no calibration procedure exists | 8.4.3: on any new PHY/board the current constants are wrong by an unknown amount -- silently degrading, not failing. |
| AS-5 | 11.3 / 8.4.3 | Only PTP **event** messages are paired with protocol timestamps; general messages never consume an event record | default: direct `KL_gptp_shadow` RX timestamps plus sequence-matched `KL_gptp_txstamp`; option-off: `ptp_ts_core` (`msgType[3]==0`, seq echoed verbatim) | ✅ default `gptp_shadow` event pairing/TX-sequence checks; ✅ option-off `ptp_ts` interference suite (event frames inside line-rate floods, general storms, runts, VLAN lookalikes) | 11.3: pairing a general message as an event poisons the pdelay or sync math with an unrelated frame time. |
| AS-6 | 10.2 / 10.3 (BMCA, port states) | Best-master selection, Announce handling | default `KL_gptp_shadow` + processor full-compare BTCA; option-off `ptp4l` | ✅ processor engine mutation suite covers stored-vector comparison, parent degradation and tie-breaks; ✅ historical option-off wire ALINX-GM half; ⚠️ default two-board acceptance #117 | 10.3: Milan requires the PAAD to be a capable GM; processor conformance evidence does not substitute for the parent wire campaign. |
| AS-7 | 11.1 / 11.2 (MD sync SMs) | Sync/Follow_Up generation & receipt, rateRatio | default processor engine + fabric timestamps; option-off `ptp4l` | ✅ processor sequence/source pairing, timeout, neighborRateRatio and closed-loop servo tests; ✅ parent `gptp_shadow` frame/timestamp integration; ⚠️ #117 wire acceptance open | 11.2: sync cadence + correct timestamps are what the whole media clock chain stands on. |
| AS-8 | 11.2.19 (MDPdelayReq) | Peer delay measurement; asCapable determination | default processor Pdelay roles and published 0x6E4/asCapable; option-off `ptp4l` | ✅ processor normal roles and multiple-responder cease-rule mutations; ✅ parent atomic publication; ⚠️ #117 turnaround/negative-pdelay board campaign open | 11.2.19: asCapable=false silently removes the port from the gPTP domain — no error, just no sync. |
| AS-9 | 8.1 / 10.6 (domain, intervals) | Single gPTP domain 0, standard message intervals | default processor profile constants/timers; option-off `ptp4l` config | ✅ processor timer/profile checks; ✅ historical option-off wire cadence; ⚠️ default board cadence #117 | 10.6: wrong intervals violate the Milan profile even when sync converges. |
| AS-10 | 11.4 (message formats) | Correct on-the-wire PTP message encoding | default `KL_gptp_engine` TX slot/µcode; option-off `ptp4l` | ✅ processor engine byte-exact message checks; ✅ parent TX gearing/sequence timestamp tests; ⚠️ default wire acceptance #117; ❌ tsn_gen NO gPTP MODEL | 11.4: a gPTP YAML model would let packet_gen replay GM behaviors (BMCA fixtures) without the 255-claimant test machine. |
| AS-11 | 12–16 (other media) | 802.11 / EPON / CSN media-dependent layers | — | ➖ N/A — full-duplex 802.3 only (Clause 11 applies) | Media out of scope. |
| AS-12 | 10.3 (PortAnnounceInformation / ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES) + 10.6 (intervals) | The announce/sync/pdelay cadence must hold **while the host is under load** -- a grandmaster that stops transmitting for `announceReceiptTimeout` × `announceInterval` (3 × 1 s) is correctly deposed by every peer | default fabric engine/timer/FIFOs; option-off `ptp4l` + `RxSteer` ([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py)) | ✅ processor timeout/timer tests and parent FIFO/drop observability; ✅ 10-scenario model; ✅ historical option-off 2026-07-28 A/B/A host-load evidence; ⚠️ default fabric board-load campaign #117 | Default ownership removes daemon scheduling from the timing loop, but #117 must still prove the integrated FIFOs and MAC path sustain cadence under load. Historical details: [`GPTP_GM_LOSS_UNDER_RX_LOAD.md`](../findings/GPTP_GM_LOSS_UNDER_RX_LOAD.md). |

**tsn_gen status: ❌ NO MODEL.** A `data_link/gptp/` family (Sync/Follow_Up/
Pdelay/Announce) is the enabler for the blocked AS-6 DUT-wins-BMCA
recreation: packet_gen as the adjustable-priority claimant instead of the
bench switch.
