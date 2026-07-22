# Spec ↔ test traceability matrix

**Purpose.** For every implemented module: what SHOULD be tested per the
governing standard clause, how that requirement IS verified today (Verilator
TB / CERT bench feature / silicon finding / tsn_gen wire model), or an
explicit **MISSING** / **N/A** verdict. This is roadmap item 3's spec-test
subtask. Every row is meant to be human peer-reviewed and then turned into a
behave feature — clause references are the load-bearing content; they were
verified against the PDFs in `/home/alex/standards/` (pdftotext extraction,
2026-07-22).

Companion documents: [`testing/PROTOCOL_VALIDATION_MATRIX.md`](testing/PROTOCOL_VALIDATION_MATRIX.md)
(protocol → test inventory, status-focused), [`MILAN_COMPLIANCE_GAPS.md`](MILAN_COMPLIANCE_GAPS.md)
(what is still missing, narrative), [`reference/FR_NFR.md`](reference/FR_NFR.md)
(requirement text), [`ENDSTATION_BUILDER.md`](ENDSTATION_BUILDER.md)
(roadmap item 4: clause-anchored builder design decisions + config-schema →
descriptor mapping, same PDF-verification rule as this matrix). This matrix
is the clause-anchored join between them.

## Family files

| Family | File | Rows | ✅ verified | 🟡 partial | ❌ MISSING | ➖ N/A |
|--------|------|------|------------|-----------|-----------|--------|
| IEEE 1722.1-2021 (ADP/ACMP/AECP+AEM) | [`traceability/ieee1722_1-2021.md`](traceability/ieee1722_1-2021.md) | 72 | 59 | 3 | 0 | 10 |
| IEEE 1722-2016 (AVTP/AAF/CRF/MAAP) | [`traceability/ieee1722-2016.md`](traceability/ieee1722-2016.md) | 38 | 33 | 2 | 1 | 2 |
| IEEE 802.1Q-2022 (VLAN/CBS/MRP/MSRP/MVRP) | [`traceability/ieee8021q.md`](traceability/ieee8021q.md) | 31 | 24 | 3 | 1 | 3 |
| IEEE 802.1AS-2020 (gPTP HW-assist scope) | [`traceability/ieee8021as.md`](traceability/ieee8021as.md) | 11 | 8 | 1 | 1 | 1 |
| Milan v1.2 profile deltas | [`traceability/milan-v12.md`](traceability/milan-v12.md) | 52 | 38 | 9 | 4 | 1 |
| **Total** | | **204** | **162** | **18** | **7** | **17** |

Legend: **✅** requirement has a specific self-checking verification today
(named TB / CERT feature / silicon wire proof). **🟡** partially verified —
the cell says exactly which leg is missing. **❌ MISSING** — no verification
(or no implementation where the clause is claimed). **➖ N/A** — clause
deliberately out of scope, with the reason in the row. A ✅ row may still
carry a `tsn_gen NO MODEL` note: the behavior is verified, but not yet
wire-generatable/fuzzable by tsn_gen.

## Why rows are N/A (taxonomy)

**N/A never means "skipped".** It means the clause imposes no positive
obligation on this device in this role/profile — and wherever a residual
obligation remains, that residual is a separate ✅ row. The 17 N/A rows fall
into exactly four categories; a reviewer disputing an N/A should attack the
category claim, not the row in isolation:

1. **Wrong role — controller/bridge obligations** (ADP-15, ACMP-11, AECP-7,
   Q-13): the clause binds ATDECC controllers or 802.1Q bridges. We are an
   end-station entity; the counterpart behavior is provided by the bench
   (Hive, `avdecc_l2`, the certified switch) — which is what the entity is
   tested *against*, not what it implements.
2. **Superseded by Milan** (ACMP-12, ACMP-13): Milan v1.2 5.5.3/5.5.4
   replaces the 1722.1 8.2.4/8.2.5 state machines wholesale. Asserting the
   base SM literally would test for behavior that is *wrong* on a Milan
   device; these rows redirect to M-ACMP-1..8, where the replacement is
   fully verified.
3. **Optional feature — only the refusal code is owed** (AEM-9, CMD-4,
   CMD-18, CMD-21, CMD-23): 1722.1 makes these optional; the testable
   residual is the exact NO_SUCH_DESCRIPTOR / NOT_IMPLEMENTED status, which
   *is* verified (RTL aecp negative reads + unknown-cmd path) and slated for
   an exhaustive tsn_gen full-range sweep.
4. **Profile/scope exclusion** (AAF-11, CRF-9, MRP-8, Q-14, AS-11,
   M-DEV-16): the Milan profile restricts the format/type set (AES3,
   non-audio CRF), the architecture fulfills the function another way
   (MMRP → MAAP + TCAM), the feature is outside Milan (Qbv TAS), the medium
   does not exist on this hardware (802.11/EPON/CSN), or the project
   recorded an explicit exclusion (redundancy — dependency-matrix decision).
   Residuals (e.g. "must not advertise AES3 / a secondary interface") are
   carried by ✅ rows (AEM-4, M-FMT-1, M-DEV-16's note).

## Module → family map

| `hdl/` module(s) | Family file section |
|------------------|---------------------|
| `adp/` (advertiser, parser, tx_arbiter) | 1722.1 §1 (ADP-1..17), Milan §2 |
| `acmp/` (listener, responder) | 1722.1 §2 (ACMP-1..14), Milan §3 |
| `aecp/` (top + 9 submodules, AEM ROM) | 1722.1 §3a–3c, Milan §4 |
| `1722/` (parsers, rx_monitor, crf_rx/tx) | 1722-2016 §1, §3; Milan §5–6 |
| `avtp/` (aaf talker, depacketizer, playback, lpf, tone, media_adv) | 1722-2016 §2; Milan §6 |
| `maap/KL_maap` | 1722-2016 §4 (MAAP-1..6) |
| `802_1q_traffic_shaper/` (classifier, class_map, queues, shaping core, CBS, controller) | 802.1Q §1 (Q-1..14) |
| `lwsrp/` (9 modules) | 802.1Q §2–3 (MRP/SRP rows), Milan §1 (M-DEV-5..10) |
| `ptp_timestamp/` (counter, ts core/top, csr_sync) | 802.1AS (AS-1..5) |
| `common/` (tcam, rx_mac_filter, link_guard, ifg gasket, cdc, datapath, csr) | supporting rows inside each family (filtering, link qualification, integration) |

## tsn_gen (wire-test engine) — model inventory and gaps

tsn_gen (`/home/alex/tsn-gen`) generates, fuzzes and decodes wire frames from
YAML protocol models (`protocols/`); packet_gen is the engine the matrix's
"would be verified with tsn_gen" statements refer to.

**Models that exist today:** `application/1722_1/adp/1722_1_adp.yaml`,
23 AECP yamls (`application/1722_1/aecp/`: 20 AEM commands + address access
+ vendor unique + no-payload), `data_link/1722/1722_avtp_common_stream.yaml`,
`data_link/1722/1722_avtp_control.yaml`, `data_link/ethernet/mac_frame.yaml`.

**Models to author (highest value first):**

1. **ACMP** (`1722_1_acmp.yaml`) — unlocks fuzz for all 14 ACMP + 10 M-ACMP
   rows; length fuzz reproduces the field 68-byte-frame trap.
2. **MSRP/MVRP MRPDU** (`802_1q/mrpdu_*.yaml`) — systematic Milan 4.2.7.1.2
   malformed-MRPDU sweeps; replaces hand-hexed frames in `lwsrp_rx` /
   `lwsrp_switchpdu`; class-B vectors for SRP-8.
3. **MAAP** (Annex B PDU) — conflict/defend fuzz (MAAP-1..6).
4. **CRF** (Clause 10 PDU) — off-profile and mr/fs-toggle vectors (CRF-5,
   M-CLK-1).
5. **AAF-PCM payload** — sparse/format-mutation streams (AAF-2, AVTP-3).
6. **gPTP message set** — packet_gen as adjustable-priority BMCA claimant;
   the enabler for the blocked es-1.1 DUT-wins variant (AS-6).
7. **VLAN tag fields in `mac_frame.yaml`** — Q-1..Q-4 tag fuzz.
8. **GET_DYNAMIC_INFO (0x4B) batch model** — record-level fuzz of the one
   command whose silicon diverged from TB four times (CMD-22).

## Top MISSING rows (attack-order preview)

1. **M-ACMP-9** — Milan 5.5.1.4/5.5.2.6 saved-state fast-connect: binds do
   not survive reboot (caused the overnight-lapse incident). Roadmap item 9.
2. **M-CLK-2** — Milan 7.3.3: the CRF stream has no SRP reservation (rides
   untagged best-effort); needs the 2nd lwSRP listener attribute.
3. **CRF-8 / M-CLK-3** — 1722 10.6/10.8 + Milan 7.2.2: clock-recovery
   actuator absent (MMCM-DRP servo); measurement half is done. Roadmap 5.
4. **M-AECP-9 / M-CLK-5** — Milan 5.4.4.4/5.4.4.5 + 7.6:
   SET/GET_MEDIA_CLOCK_REFERENCE_INFO and media clock management layer
   unimplemented.
5. **SRP-9** — 802.1Q 35.2.7: single-stream lwSRP engine; NxN AAF streams
   (AX 8x8 / Arty 4x4) need per-stream registrar/declaration instances.
   Roadmap 4.
6. **SRP-8** — 802.1Q 35.1.4/34.5: SR class B never *declared/used* (bench
   is class A only). The incoming half is now walker-TB-proven (lwsrp_rx
   8b, packed B-first Domain vectors) — which also FOUND the walker's
   stale-`dom_a_evt_r` defect (class-A event lags one Domain PDU; RTL fix
   pending, see the SRP-8 row).
7. **AS-4** — 802.1AS 8.4.3: ingress/egress latency constants are
   bench-calibrated with no per-board calibration procedure; the
   ingress/egress split was never measured separately.
8. **AVTP-5 + M-CNT-4** — 1722 4.4.4.3 mr (media clock restart) toggle has
   no listener response: the parser does not extract mr, so it can never
   tick MEDIA_RESET (gap TB-pinned, avtp_rxmon [30]; the counter's
   servo-rail semantics are now asserted). M-CNT-4's talker-side
   MEDIA_RESET is still unasserted.
9. **AS-6 (variant)** — Milan es-1.1 DUT-wins-BMCA: blocked on the bench
   switch's gPTP claim (USER-ordered to the bottom of the attack list); a
   tsn_gen gPTP model is the unblocking path.
10. **ACMP tsn_gen model** — verification-infrastructure gap: every ACMP row
    is TB-verified but nothing can generate/fuzz ACMP on the wire today.

## Review workflow

Each family file is a table meant for row-by-row peer review; the intended
lifecycle per row is: review clause ref → confirm/adjust required-behavior
wording → promote to a behave feature (CERT suite) and/or a tsn_gen sweep →
flip the row's status. When a TB or module changes, the row citing it must
change in the same commit (same rule as `tb/verilator/README.md`).
