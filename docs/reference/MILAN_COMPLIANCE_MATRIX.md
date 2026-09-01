<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Milan v1.2 compliance matrix — all five standards, one page

The per-clause compliance position of this end-station against its five
normative specifications, at firmware VERSION `0x0002_0056`. The overall
verdict is the audit's:
[not fully compliant with Milan v1.2](../testing/MILAN_V12_AUDIT_2026-08-16.md)
— the open rows below are why, and the ordered plan through them is
[`../MILAN_V12_ROADMAP.md`](../MILAN_V12_ROADMAP.md).

Machine-checked anchors from the
[Milan feature status ledger](MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gateware.current-version` | `implemented` | `0x0002_0056` |
| `aem.served-command-set` | `implemented` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `gptp.fabric-product-owner` | `implemented` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
<!-- milan-feature-status:end -->

Normative editions — clause numbers below were re-verified against these exact
texts (grep over the extracted PDFs, 2026-09-01), not recalled and not taken
from a later edition:

| Standard | Edition | Scope here |
|---|---|---|
| Milan Specification, Consolidated | **v1.2** (Final, 2023-11-30) | the profile: non-redundant PAAD-AE, talker + listener |
| IEEE Std 1722.1 | **-2021** | ATDECC: ADP, ACMP, AECP/AEM |
| IEEE Std 1722 | **-2016** | AVTP: common header, AAF audio, CRF |
| IEEE Std 802.1AS | **-2011** (+Cor1-2013, +Cor2-2015) | gPTP as Milan Section 4.2.6 profiles it — the fabric plane's edition of record (decision #139; [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) keeps the 802.1AS-2020 hardware-assist cross-trace) |
| IEEE Std 802.1Q | **-2014** | VLAN tag, FQTSS/CBS, MRP/MVRP/MSRP (the cited clause numbers are identical in the 2018/2022 editions — [`../traceability/ieee8021q.md`](../traceability/ieee8021q.md) traces against 2022) |

**Status vocabulary** — the ledger's, so a row here can never contradict a
marked row elsewhere: `implemented` (a runnable gate exists and is green),
`partial` (the cell says which leg is missing), `missing` (the function is
absent — a conformant refusal or echo never moves this), `not-supported`
(refusal IS the compliant behavior), `n/a` (outside the declared profile).

Owners: **fabric** = RTL in [`hdl/`](../../hdl); **processor** = the pinned
`protocol-processor` submodule via
[`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv); **gPTP plane**
= the pinned `gptp-processor` submodule
([`../design/GPTP_PLANE.md`](../design/GPTP_PLANE.md)); **firmware** = the
bare-metal boot/provisioning software. Evidence tokens: `RTL <dir>` =
[`tb/verilator/<dir>`](../../tb/verilator), `PP <dir>` =
`protocol-processor/tb/<dir>`, `BDD` = [`tests/`](../../tests) behave,
`SILICON` = dated on-board measurement, `BENCH` = the bench suite.

## Contents

- **[1. Milan v1.2 — the profile](#1-milan-v12--the-profile)** — The governing layer: gPTP profile numbers, SRP duties, the complete Section 5.4.2 AEM command table (every subclause served), MVU, notifications and liveness, ACMP/ADP, the persistence list (the largest open block), streaming formats and media clocking.
- **[2. IEEE 1722.1-2021 — ATDECC base](#2-ieee-17221-2021--atdecc-base)** — What the base standard adds under the profile: ADP fields, the descriptor set served from the entity-model image, the counter tables, the response-contract duties, ACMP timeouts and the originated CONTROLLER_AVAILABLE probe.
- **[3. IEEE 1722-2016 — AVTP](#3-ieee-1722-2016--avtp)** — The media plane field by field: common stream header, AAF PCM encapsulation, CRF, presentation time.
- **[4. IEEE 802.1AS-2011 — gPTP](#4-ieee-8021as-2011--gptp)** — The time plane: the fabric gPTP plane against the Milan Section 4.2.6 profile of the 2011 edition, and the PHC/timestamping hardware assists beneath it.
- **[5. IEEE 802.1Q-2014 — VLAN / FQTSS / SRP](#5-ieee-8021q-2014--vlan--fqtss--srp)** — Tag handling, queuing, the credit-based shaper, and the MSRP/MVRP endpoint duties the processor owns.
- **[6. How a row moves](#6-how-a-row-moves)** — The evidence rule that keeps this page honest, and the counter-layout trap every peer implementer hits.

## 1. Milan v1.2 — the profile

### 1.1 gPTP profile (Section 4.2.6)

The product gPTP owner is the **fabric plane** (`gptp-processor`), which
implements the Milan v1.2 profile of IEEE 802.1AS-2011 (+Cor1/Cor2); the
decision record for the one deliberate 2011-vs-2020 wire difference
(controlField values) is issue #139 and
[the reference-standards register](../../REQUIREMENTS.md#2-reference-standards).

| Clause | Requirement | Status / evidence |
|---|---|---|
| 4.2.6.1 | BTCA support per 802.1AS Section 10.3 | implemented — plane BTCA; RTL gptp_shadow + milan_dp `obj_gptp`; SILICON: elections won and lost against real peers (plane bench records) |
| 4.2.6.1.1 | neighborPropDelayThresh default 800 ns (copper) | partial — threshold in the plane; the per-unit ingress/egress latency calibration procedure is still open ([`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) AS-4) |
| 4.2.6.2.1 | priority1 default 248 for a GM-capable PAAD | implemented — station config through the builder; graded on the wire by the tsn-gen 802.1AS models (RTL tsn_fuzz `fuzz_ptp`) |
| 4.2.6.2.2 / 4.2.6.2.3 | Table 4.1 interval and Table 4.2 timeout tolerances | partial — cadences graded field-by-field in simulation (RTL tsn_fuzz); tolerance *edges* and long-duration holds are unproven (audit B11) |
| 4.2.6.2.4 | asCapable after 2–5 Pdelay responses | implemented — plane state machine; RTL gptp_shadow |
| 4.2.6.2.5 | cease Pdelay TX on multiple responses | implemented — plane rule (multi-response teardown guarded) |
| 4.2.6.2.6 | Pdelay turnaround ≤ 15 ms | implemented — plane timer service; SILICON turnaround well inside the relaxed bound |

### 1.2 SRP duties (Section 4.2.7, Section 4.3.3, Section 4.4.1)

| Clause | Requirement | Status / evidence |
|---|---|---|
| 4.2.7.1 | MRP support + Table 4.3 timer tolerances | implemented — PP srp_top / timer_service |
| 4.2.7.1.2 / .3 | malformed-MRPDU tolerance; EndMark 0x0000 | implemented — PP srp_decoder / srp_encoder |
| 4.2.7.2.1 | Domain: SR class A, priority 3, VID 2 | implemented — PP srp_top; SILICON reservation against a real bridge; the adopted {priority, VID} pair tags every emitted frame |
| 4.2.7.2.2 | instantaneous IN→MT registrar transition | implemented — PP srp_stream_fsms |
| 4.2.7.3 / 4.4.1 | MVRP (talker + listener) | implemented — PP srp suites; SILICON join |
| 4.3.3 | talker attribute declaration + Table 4.4 bandwidth | implemented — TSpec derived from real frame geometry (`milan_datapath`), declared by the processor; RTL milan_dp |

### 1.3 AECP AEM command set (Section 5.4.2)

**Thirty AEM opcodes are served with real state** — every command of Milan
Section 5.4.2.1–5.4.2.29 plus the Section 5.4.5.4 `IDENTIFY_NOTIFICATION`
path — and MVU `GET_MILAN_INFO` beside them; the inventory is machine-gated
([`aecp_response_contract.feature`](../../tests/features/aecp_response_contract.feature)
parses the engine's own opcode constants, and the ledger's served-set row is
checked against
[`tests/steps/aecp_engine_steps.py`](../../tests/steps/aecp_engine_steps.py)).
Unknown commands draw a correctly sized `NOT_IMPLEMENTED` echo (IEEE
Section 9.3.5.3.3); a command for another entity, and any AECP response arriving as
input, are silently refused.

| Clause | Command | Status | Note / evidence |
|---|---|---|---|
| 5.4.2.1 | ACQUIRE_ENTITY | not-supported | Milan's required refusal, `owner_id` 0 — PP pp_top; RTL pp_shadow |
| 5.4.2.2 | LOCK_ENTITY (+ auto-unlock push) | implemented | PP pp_top + aecp_notify |
| 5.4.2.3 | ENTITY_AVAILABLE | implemented | RTL milan_dp `[AECP-MODEL]` |
| 5.4.2.4 | READ_DESCRIPTOR | implemented | RTL milan_dp — walks every generated descriptor + absent-descriptor oracle |
| 5.4.2.5 / .6 | SET/GET_CONFIGURATION | implemented | lock-guarded; `STREAM_IS_RUNNING` reduction — PP dyn_state + pp_top |
| 5.4.2.7 / .8 | SET/GET_STREAM_FORMAT | implemented | landed 0x0053 with the bound/streaming interlocks |
| 5.4.2.9 / .10 | SET/GET_STREAM_INFO (Milan 80-byte form) | implemented | `MSRP_ACC_LAT` presentation-offset leg included — PP pp_top byte-exact |
| 5.4.2.11 / .12 | SET/GET_NAME | implemented | landed 0x0054; nonvolatile restore stays with persistence (Section 1.7) |
| 5.4.2.13 / .14 | SET/GET_SAMPLING_RATE | implemented | stored + served; media-plane adoption open (Section 1.8, audit B3) |
| 5.4.2.15 / .16 | SET/GET_CLOCK_SOURCE | implemented | stored + served + exported to root; nothing consumes it yet (Section 1.8, audit B3) |
| 5.4.2.17 / .18 | SET/GET_CONTROL (Identify, 0/255, volatile) | implemented | PP dyn_state; no public indication output yet (audit B7) |
| 5.4.2.19 / .20 | START/STOP_STREAMING (inputs; `NOT_SUPPORTED` on outputs) | implemented | binding-record interlock (issue #78); started-state persistence open (audit B12) |
| 5.4.2.21 / .22 | REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION | implemented | PP aecp_notify |
| 5.4.2.23 | GET_AVB_INFO | implemented | propagation delay served from the measured word since 0x0055 (audit B8 closed) |
| 5.4.2.24 | GET_AS_PATH | implemented | staged publish/cutover contract; option-off aliasing recorded in audit B6 |
| 5.4.2.25 | GET_COUNTERS — AAF Stream Input, Stream Output (Table 5.17), AVB Interface, Clock Domain | partial | served + pushed for those four; **the declared CRF Stream Input returns an empty mask** — its Table 5.16 counters are unconnected (audit B4) |
| 5.4.2.26 | GET_AUDIO_MAP (both directions) | implemented | PP pp_top |
| 5.4.2.27 / .28 | ADD/REMOVE_AUDIO_MAPPINGS | implemented | atomic validation, live datapath projection, lock checks, unsolicited updates (2026-08-17) |
| 5.4.2.29 | GET_DYNAMIC_INFO (IEEE Section 7.4.76) | implemented | completed 2026-08-17; never answers `IN_PROGRESS`, satisfying Section 7.4.76's support rule |

### 1.4 Milan Vendor Unique (Section 5.4.4)

| Clause | Command | Level | Status |
|---|---|---|---|
| 5.4.4.1 | GET_MILAN_INFO | SHALL | implemented |
| 5.4.4.2 / .3 | SET/GET_SYSTEM_UNIQUE_ID | RECOMMENDED | n/a — tracked, not a gap |
| 5.4.4.4 / .5 | SET/GET_MEDIA_CLOCK_REFERENCE_INFO | RECOMMENDED | n/a — tracked, not a gap |

### 1.5 Unsolicited notifications and controller liveness (Section 5.4.5)

| Clause | Requirement | Status |
|---|---|---|
| 5.4.5.1 / .2 | registry, fan-out, per-controller sequencing, the full Table 5.22 trigger set, GET_COUNTERS push ≤ 1/descriptor/second | implemented at 0x0055 (issue #69) — every state-changing command pushes to every registered controller except the requester; the timed `milan_dp` leg (`obj_notify`) measures the one-second limit. Open corner: the CRF Stream Input has no served counters, so no counter push (audit B4) |
| 5.4.5.3 | departing-controller monitor: random 30–60 s timer, CONTROLLER_AVAILABLE probe + one retry, targeted auto-deregister | implemented at 0x0055 — `KL_aecp_ca_originator` on the processor's shared originator; PP ca_originator; timed leg measures probe, 250 ms retry, deregistration |
| 5.4.5.4 | identification notification | SHOULD — n/a as a gap; the Identify *indication* output is the open half (audit B7) |

### 1.6 ACMP (Section 5.5) and ADP (Section 5.6)

| Clause | Requirement | Status / evidence |
|---|---|---|
| 5.5.2 / 5.5.3 | sink binding/unbinding, Table 5.26 timeouts, settlement, the Section 5.5.3.5 event ladder | implemented — PP acmp_listener + pp_top; RTL pp_shadow; SILICON binds against a Milan-validated peer |
| 5.5.1.4 / 5.5.2.6 | Auto Connect (saved-state fast connect) | missing — blocked by persistence (Section 1.7): the flag path exists, the saved binding does not survive a power cycle |
| 5.5.4 | talker treatment of PROBE_TX / DISCONNECT_TX / GET_TX_* | implemented — PP acmp_talker; SILICON streaming licences open/close |
| 5.6.3 / 5.6.4 | advertise + discovery state machines, valid_time | implemented — PP adp_engine; SILICON discovery by controllers; the available_index increment-policy divergence stays recorded in the processor's docs |

### 1.7 Dynamic state and persistence (Section 5.3) — the largest open block

The dynamic-state store serves every settable field below;
**nothing survives a power cycle** — the root integration still answers as
blank flash (`nvm_backed = 0`, audit B2), which also voids saved-state fast
connect and the started-state restore (audit B12).

| Clause | State | Live (set/served) | Persisted |
|---|---|---|---|
| 5.3.5.1 | sampling rate per Audio Unit | implemented (adoption by the media plane open — B3) | missing |
| 5.3.7.1 / 5.3.7.6 | Stream Output format · presentation-time offset (2 ms default) | implemented | missing |
| 5.3.8.1 / .2 / .3 / .7 | Stream Input format · bound state · binding params · started/stopped | implemented | missing |
| 5.3.9.1 / 5.3.10.1 | channel mappings (both directions) | implemented | missing |
| 5.3.11.1 | clock source per Clock Domain | implemented (consumption open — B3) | missing |
| 5.3.12 | Identify control (volatile by rule) | implemented | n/a — must NOT persist |
| 5.3.13 | user names | implemented (0x0054) | missing |

### 1.8 Streaming (Section 6) and media clocking (Section 7)

| Clause | Requirement | Status / evidence |
|---|---|---|
| 6.2–6.5 | Base Formats: AAF/PCM 32-bit, {48/96/192 kHz} × {1,2,4,6,8} ch, SR class A | partial — full family declared per configuration (gate: `check_wire_accountability.py`); fabric proven at 48 kHz (RTL aaf; SILICON audio E2E); 96/192 kHz unproven on silicon |
| 5.3.7.6 / 4.4.2.1 | 2 ms default presentation-time offset, settable via SET_STREAM_INFO | implemented |
| 5.3.7.3 | talker transmit licence (bound listener + reservation) | partial — the admission composition is graded (BDD `milan_streaming_licence.feature`), but the writable debug bypass `AAF_CTRL[1]` can defeat it (audit B9) |
| 7.2.2 | media clock inputs — the CRF sink can drive the media clock | missing — the stored clock-source selection reaches the root and stops there: `CRF_CLK_SELECTED_C` is a compile-time zero, the servo path idle (audit B3); grid alignment consequently unproven (audit B10) |
| 7.2.3 / 7.3.2–7.3.4 | CRF Media Clock Output, Pro Audio CRF format (48 kHz base, SR class A) | implemented — RTL crf_tx; format fields byte-verified |
| 7.4 | media clock source quality ± 50 ppm | partial — board-oscillator property; measured 10.6 ppm offset vs the exact grid, no closed loop yet (audit B10) |
| 8.x | seamless redundancy | n/a — single-AVB_INTERFACE PAAD |

## 2. IEEE 1722.1-2021 — ATDECC base

| Clause | Requirement | Status / evidence |
|---|---|---|
| 6.2.2 | ADPDU format; valid_time (2 s units) | implemented — PP adp_engine; RTL pp_shadow wire checks |
| 7.2.x | descriptor set: ENTITY 7.2.1, CONFIGURATION 7.2.2, AUDIO_UNIT 7.2.3, STREAM_IN/OUT 7.2.6, AVB_INTERFACE 7.2.8, CLOCK_SOURCE 7.2.9, LOCALE 7.2.11, STRINGS 7.2.12, STREAM_PORT 7.2.13, AUDIO_CLUSTER 7.2.16, AUDIO_MAP 7.2.19, CONTROL 7.2.22, CLOCK_DOMAIN 7.2.32 | implemented — generated into the entity-model image by the builder, loaded and verified before enable; RTL milan_dp `[AECP-MODEL]` walks every emitted descriptor |
| 7.4.x | AEM commands | see Section 1.3 — Milan's profile governs each |
| 7.4.42.2 | counter tables: AVB_INTERFACE Table 7-152, CLOCK_DOMAIN 7-154, STREAM_INPUT 7-156, STREAM_OUTPUT 7-158 | partial — served per Milan's sets (Section 1.3 GET_COUNTERS row); **Table 7-158 deliberately diverges from Milan Table 5.17** (Section 6 trap) |
| 7.5.2 | unsolicited notification duty | implemented — Section 1.5 |
| 8.2.1 | ACMPDU message types (Table 8-2), status codes (8-3), command timeouts (Table 8-1: CONNECT_TX 2000 ms … GET_RX_STATE 200 ms) | implemented — PP acmp suites drive the timers |
| 9.3.2.5 | AEM status codes (Table 7-141) | implemented — every refusal carries a defined code; PP pp_top |
| 9.3.2.6 | 250 ms command timeout — answer within 240 ms | implemented — fabric answers at wire speed, independent of any host |
| 9.3.5.3.3 | unimplemented commands answered `NOT_IMPLEMENTED`, correctly sized | implemented — BDD `aecp_response_contract.feature`, gated against the engine's opcode constants |
| 9.3.6 | command retry as originator (CONTROLLER_AVAILABLE, one retry) | implemented — PP ca_originator; timed milan_dp leg |

## 3. IEEE 1722-2016 — AVTP

| Clause | Requirement | Status / evidence |
|---|---|---|
| 4.4.3.2–.4 | subtype, h, version — a non-zero-version PDU is discarded whole | implemented — RTL avtp_parser (version gate closed 2026-08-08) |
| 4.4.4.2 / .8 | sv, stream_id match | implemented — RTL avtp_parser at five shapes |
| 4.4.4.3 | mr — toggled on media-clock change, held ≥ 8 AVTPDUs | implemented — `KL_media_clock_restart`; RTL tkdiag + milan_dp |
| 4.4.4.5 / .9 | tv + avtp_timestamp (mod-2³² gPTP ns) | implemented — RTL avtp_stream, aaf; SILICON latency = presentation offset |
| 4.4.4.6 | sequence_num increment/wrap | implemented — RTL aaf; the SEQ_NUM_MISMATCH counter proves the observer |
| 4.4.4.7 | tu on gPTP discontinuity | implemented — `KL_ptp_clock_validity` + the plane's clock-validity lease; RTL clkvalid; the BDD leg left with the retired host plane |
| 4.3.2 | AVTP presentation time semantics | implemented — RTL aaf_latency_taps / aaf_latency_tap_bank; SILICON E2E = offset |
| 7.2.3–.5 / 7.3.2–.4 | AAF PCM: format, sp, evt · nsr, channels_per_frame, bit_depth | implemented — RTL aaf + the advertised-vs-emitted wire-accountability gate |
| 10.4.x | CRF: type `CRF_AUDIO_SAMPLE`, pull, base_frequency, timestamp_interval, mr | implemented — RTL crf_rx / crf_tx |

## 4. IEEE 802.1AS-2011 — gPTP

The Milan-normative edition (Section 4.2.6 profiles 802.1AS-2011 + Cor1-2013 +
Cor2-2015). The product gPTP owner is the fabric plane; the 2011-edition
clause numbers below differ from 802.1AS-2020's in places (MDPdelayReq is
**11.2.15** here, not 11.2.19 —
[`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) keeps the
2020 cross-trace for the hardware-assist scope).

| Clause | Requirement | Owner | Status / evidence |
|---|---|---|---|
| 8.2 | PTP timescale: monotonic, settable, frequency-adjustable | fabric (`timestamp_counter`) | implemented — RTL ptp (201 k checks vs a 128-bit model) |
| 8.4.2.2 / 8.4.3 | event messages timestamped at the reference plane; general messages never | fabric (`ptp_ts_core/top`) | implemented — RTL ptp_ts interference suite |
| Annex B.1.1 | LocalClock within ± 100 ppm, finely adjustable | fabric + board oscillator | implemented — RTL ptp adjfine granularity |
| 10.2 / 10.3 | time-sync state machines + BTCA | gPTP plane | implemented — RTL gptp_shadow, milan_dp `obj_gptp`; SILICON elections both ways |
| 10.5.3 | Announce format | gPTP plane | implemented — RTL tsn_fuzz `fuzz_ptp` field-by-field |
| 10.6.2.2 / 10.6.3.1–.2 | announce interval 0; sync/announce receipt timeout 3 | gPTP plane | implemented — plane microcode; cadence graded in simulation |
| 11.2.2 | asCapable conditions (threshold, multi-response, no loopback) | gPTP plane | implemented — plane state machine |
| 11.2.13–.16 | MD sync + pdelay state machines | gPTP plane + fabric timestamps | implemented — RTL gptp_shadow; SILICON exchanges against real peers |
| 11.4.x | message formats (Sync, Follow_Up, Pdelay trio) — controlField per 2011 Table 11-7, decision #139 | gPTP plane | implemented — RTL tsn_fuzz models at the CI pin |
| 11.5.2.2 / .3 | log intervals: pdelay 0, sync −3 (125 ms) | gPTP plane | implemented — cadence graded in simulation |
| 10.1 / 11.1 | two-step operation (2011 has no one-step) | gPTP plane | implemented — two-step Sync + Follow_Up on the wire |
| 12–13 | other media (802.11, EPON) | — | n/a — full-duplex 802.3 only |

Open in this section: the per-unit ingress/egress latency calibration
procedure (AS-4), long-duration holds, and every SILICON claim's currency —
[audit B11](../testing/MILAN_V12_AUDIT_2026-08-16.md).

## 5. IEEE 802.1Q-2014 — VLAN / FQTSS / SRP

| Clause | Requirement | Owner | Status / evidence |
|---|---|---|---|
| 9.4 / 9.6 | C-TAG TPID 0x8100; TCI = PCP·DEI·VID | fabric | implemented — RTL cls / classifier |
| 6.9.3 / 6.9.4 | PCP encoding on transmit; priority regeneration on receive | fabric | implemented — RTL aaf/crf_tx TCI bytes; RTL cls |
| 8.6.6 + Table 8-4 | queue per traffic class | fabric | implemented — RTL queues / classifier |
| 8.6.8.1 | strict priority (non-CBS queues) | fabric | implemented — RTL shaper_core (all priority pairs) |
| 8.6.8.2 | credit-based shaper: idleSlope/sendSlope, transmitAllowed (hiCredit/loCredit per informative Annex L.1) | fabric | implemented — RTL cbs, bit-exact vs a cycle-accurate replica |
| 34.3 / 34.6.1 | per-class idleSlope from reservations; class measurement interval 125 µs (A) / 250 µs (B) | fabric + processor | implemented — granted slope drives the class-A queue's idleSlope; TSpec from real frame geometry |
| 35.2.2.4 | MSRP attributes: Talker Advertise/Failed, Listener, Domain | processor | implemented — PP srp_decoder / srp_encoder / srp_stream_fsms |
| 35.2.2.8.6 | accumulated latency per hop | processor | implemented — PP srp suites; consumed by stream info |
| 35.2.2.9.3 + Table 6-5 / Table 9-2 | SRclassPriority defaults A=3, B=2; SR_PVID default 2 | processor + fabric adoption | implemented — defaults in force; adopted pair tags every emitted frame |
| Table 35-6 | reservation failure codes | processor | implemented — decoded and surfaced on the talker-failed path |
| 10.7.11 | MRP timers: JoinTime 200 ms, LeaveTime, LeaveAllTime | processor | implemented — PP timer_service, Milan Table 4.3 tolerances |
| 11.2 | MVRP | processor | implemented — PP srp suites |
| 8.6.1–8.6.5 (bridge relay) | forwarding, filtering DB | — | n/a — end station, not a bridge |

## 6. How a row moves

- A row moves to `implemented` **only** with a named, runnable gate (a
  Verilator suite, a behave feature, a generator gate) or a dated silicon
  measurement. Reading code is not evidence.
- A `NOT_IMPLEMENTED` echo satisfies IEEE Section 9.3.5.3.3 and nothing else; a
  `not-supported` row is different — there, refusal is the compliant behavior.
- Status claims that repeat ledger values are machine-judged
  ([`MILAN_FEATURE_STATUS.md`](MILAN_FEATURE_STATUS.md)); keep this page's
  embedded block, and this page, in step with the ledger.
- **The STREAM_OUTPUT counter trap:** Milan Table 5.17 ≠ IEEE Table 7-158 —
  Milan drops STREAM_INTERRUPTED, TIMESTAMP_VALID and TIMESTAMP_NOT_VALID and
  compacts the offsets, and flags the divergence itself in Section 5.4.2.25. This
  device implements Milan's layout; a peer decoding by the IEEE table will
  mis-read the talker counters.
- When an RTL module or TB changes, the row citing it changes **in the same
  commit** ([CONTRIBUTING](../../CONTRIBUTING.md)).
- The open rows, ordered: [`../MILAN_V12_ROADMAP.md`](../MILAN_V12_ROADMAP.md)
  and the audit's B-items.
