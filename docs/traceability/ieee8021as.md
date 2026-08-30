# Traceability — IEEE 802.1AS-2020 (gPTP) — hardware-assist scope

Clause numbers in the table are verified against the local standards PDF
`$STANDARDS_DIR/802.1AS-2020.pdf`. Current implementation coverage is in the
[generated module matrix](MODULE_MATRIX.md), and the current hardware/software
boundary is in the [architecture guide](../overview/ARCHITECTURE.md).

**Two scopes, two editions.** This table is the hardware-assist scope: the PTP
hardware clock and event-message timestamping the **fabric** provides, traced
against 802.1AS-2020. At VERSION `0x0002_0056` the fabric plane is the sole
product gPTP owner (#259). The option-OFF elaboration is an ownerless proof
target: it emits no gPTP protocol messages; GM, parent, path and pdelay are
zero; sync/asCapable are zero; `tu` is one; and all legacy writes are inert.
Pre-#259 wire captures remain labelled only as historical evidence and do not
describe that current option-OFF boundary. With `GPTP_PLANE_EN_P` on, the fabric
gPTP plane ([GPTP_PLANE.md](../design/GPTP_PLANE.md), the `gptp-processor`
submodule) runs the protocol and builds the messages itself, and its wire
formats and state machines follow the Milan v1.2 profile (section 4.2.6) of
IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015, not 802.1AS-2020: the
controlField carries the 802.1AS-2011 11.4.2.7 / Table 11-7 value per message
(Sync 0x0, Follow_Up 0x2, Announce and Pdelay 0x5) where 802.1AS-2020
10.6.2.2.13 says 0; receivers ignore the byte in both editions (IEEE 1588-2008
13.3.2.10, IEEE 1588-2019 13.3.2.13). The decision is recorded on #139 and in
[REQUIREMENTS.md](../../REQUIREMENTS.md) section 2. The plane's own
transmissions are graded field-by-field by the tsn-gen 802.1AS models in
[`tb/verilator/tsn_fuzz`](../../tb/verilator/tsn_fuzz) (row AS-10). The current
Milan verdict, including gPTP blockers, is in the
[Milan v1.2 audit](../testing/MILAN_V12_AUDIT_2026-08-16.md).

Modules: [`hdl/ieee8021as/ptp_timestamp/`](../../hdl/ieee8021as/ptp_timestamp) (`timestamp_counter`, `ptp_ts_core`,
`ptp_ts_top`, `ptp_csr_sync`), `hdl/common/cdc_*`.

| # | Clause | Required behavior | Module / agent | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|----------------|------------------------------|----------------|
| AS-1 | 8.2 (timescale) | PTP timescale: monotonic ns clock, settable epoch, frequency-adjustable | timestamp_counter (PHC: settime/adjtime/adjfine w/ fractional carry, gettime snapshot) | ✅ RTL ptp (201 k vs 128-bit accumulator model) | 8.2: every timestamp, AVTP presentation time and CRF value inherits this counter's correctness. |
| AS-2 | Annex B.1 (LocalClock) | LocalClock frequency accuracy within ±100 ppm, adjustable with fine granularity | timestamp_counter on the fixed 125 MHz reference (REQ-PTP-07) | ✅ RTL ptp (adjfine granularity vs model); 🟩 board: PHC readback + measured lock quality | B.1.1: a reference outside ±100 ppm can be unservoable by peers even with a perfect protocol. |
| AS-3 | 8.4.3 (timestamp measurement plane) | Timestamps captured at the reference plane; deviation compensated via ingressLatency/egressLatency | ptp_ts_top/core capture; latency constants applied in the historical bench profile | ✅ RTL ptp_ts (golden delta model: any ts↔frame mis-pairing shifts a delta by a whole frame time); SILICON tap-measured constants (3511 ns Arty / 1490 ns AX) — the asCapable breakthrough | 8.4.3: uncompensated RX-stamp lateness made asCapable *never* true — the single biggest gPTP field bug of this project. |
| AS-4 | 8.4.3 (per-unit calibration) | Latency constants valid per instance/board, not per bench | -- procedure gap | ❌ MISSING -- constants are bench-calibrated; ingress/egress split never measured separately (gaps Section 4); no calibration procedure exists | 8.4.3: on any new PHY/board the current constants are wrong by an unknown amount -- silently degrading, not failing. |
| AS-5 | 11.3 / 8.4.3 | Only PTP **event** messages timestamped (Sync, Pdelay_Req, Pdelay_Resp); general messages never capture | ptp_ts_core (msgType[3]==0 rule, seq echoed verbatim) | ✅ RTL ptp_ts (interference suite: event frames inside line-rate floods, general-storms, runts, VLAN lookalikes) | 11.3: stamping a general message mis-pairs seq→timestamp and poisons the pdelay math with whole-frame errors. |
| AS-6 | 10.2 / 10.3 (BMCA, port states) | Best-master selection, Announce handling | option OFF: ownerless, with no BMCA participant; option ON (`GPTP_PLANE_EN_P`): the fabric plane's BTCA in the `gptp-processor` engine ([GPTP_PLANE.md](../design/GPTP_PLANE.md)) | ✅ option ON: donor engine suite plus `fuzz_ptp.py` BTCA legality, PathTrace and GM transmission assertions, tallied in generated [`TEST_RESULTS.md`](../../hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md); ✅ option OFF: engine absent, GM/parent/path zero and retained writes inert; ✅ historical pre-#259 wire BENCH ALINX-GM half; ❌ DUT-wins-BMCA physical variant remains #117 | 10.3: Milan requires the PAAD to be a *capable* GM. The ownerless option is a verification boundary, not an alternate product implementation. |
| AS-7 | 11.1 / 11.2 (MD sync SMs) | Sync/Follow_Up generation & receipt, rateRatio | option OFF: ownerless, with no Sync/Follow_Up state machine; option ON: the fabric plane's state machines and servo (`gptp-processor`) on the hardware timestamps | ✅ option ON: donor engine suite, `fuzz_ptp.py` clean-pair/malformed-pair and byte-exact GM transmit grading, plus [`tb/verilator/gptp_plane`](../../tb/verilator/gptp_plane) closed-loop PHC steering; ✅ option OFF: sync zero and `tu=1`; ✅ historical pre-#259 wire sync cadence and hardware-timestamp evidence | 11.2: sync cadence + correct timestamps are what the whole media clock chain stands on. |
| AS-8 | 11.2.19 (MDPdelayReq) | Peer delay measurement; asCapable determination | option OFF: ownerless, with no Pdelay exchange and pdelay/asCapable zero; option ON: the fabric plane's MDPdelayReq/MDPdelayResp state machines (`gptp-processor`) | ✅ option ON: donor pdelay ladder plus `fuzz_ptp.py` boot request, response-pair identity/sequence/domain qualification, replay refusal, negative-delay and drought/recovery checks; ✅ option OFF: zero publication despite retained writes; ✅ historical pre-#259 wire pdelay cadence and stable asCapable evidence | 11.2.19: asCapable=false silently removes the port from the gPTP domain — no error, just no sync. |
| AS-9 | 8.1 / 10.6 (domain, intervals) | Single gPTP domain 0, standard message intervals | option OFF: ownerless, with no protocol configuration or transmissions; option ON: fabric-plane microcode, domain-0 parser enforcement and generated intervals | ✅ option ON: `fuzz_ptp.py` foreign-domain drops, multiple-responder behavior, per-message `logMessageInterval`, and unlisted-message refusal; ✅ option OFF: quiescent protocol boundary; ✅ historical pre-#259 wire cadence record | 10.6: wrong intervals violate the Milan profile even when sync converges. |
| AS-10 | 11.4 (message formats; for the fabric plane 802.1AS-2011 11.4 per the Milan v1.2 profile, see the header) | Correct on-the-wire PTP message encoding | option OFF: ownerless and emits no PTP messages; option ON (`GPTP_PLANE_EN_P`): the fabric plane builds Sync, Follow_Up, Announce, Pdelay_Req, Pdelay_Resp and Pdelay_Resp_Follow_Up ([`hdl/ieee8021as/gptp_plane/`](../../hdl/ieee8021as/gptp_plane), `gptp-processor`) | ✅ option ON: fabric TX graded field-by-field against tsn-gen by [`fuzz_ptp.py`](../../tb/verilator/tsn_fuzz/fuzz_ptp.py), including controlField, minimum/trailing-TLV length acceptance and request/response identity rules; current tally in [`TEST_RESULTS.md`](../../hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md); ✅ option OFF: no protocol output; ✅ historical pre-#259 tap dissection retained only as history | 11.4: a wrong header byte is visible to every capture-based conformance check even where peers ignore it. |
| AS-11 | 12–16 (other media) | 802.11 / EPON / CSN media-dependent layers | — | ➖ N/A — full-duplex 802.3 only (Clause 11 applies) | Media out of scope. |
| AS-12 | 10.3 (PortAnnounceInformation / ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES) + 10.6 (intervals) | Product announce/sync/pdelay cadence remains independent of bulk traffic; a grandmaster that stops for `announceReceiptTimeout` × `announceInterval` is correctly deposed by every peer | option ON: the fabric plane is timer-driven and independent of softcore load (`gptp-processor`, [GPTP_PLANE.md](../design/GPTP_PLANE.md)); option OFF: ownerless and intentionally has no cadence | ✅ option ON simulation: donor boot-cadence/cease-countdown phases and `fuzz_ptp.py` storm/recovery canaries; 🟡 product physical load repetition remains #117 | 10.3: fabric timers and bounded handshakes keep protocol cadence independent of other fabric traffic; option OFF is not an alternate product implementation. |

**tsn_gen status: models present.** The `protocols/data_link/ptp/8021as_*`
family (Sync, Follow_Up, Announce, Pdelay_Req, Pdelay_Resp,
Pdelay_Resp_Follow_Up and the Ethernet header) exists at the CI-pinned tsn-gen
revision and is consumed by `tb/verilator/tsn_fuzz/fuzz_ptp.py`, which grades
the fabric plane's own transmissions and drives its BTCA probes in simulation
(row AS-10). What the models do not yet replace is the bench-side recreation of
the blocked AS-6 DUT-wins-BMCA variant: packet_gen as the adjustable-priority
claimant instead of the bench switch remains to be wired into a BENCH feature.
