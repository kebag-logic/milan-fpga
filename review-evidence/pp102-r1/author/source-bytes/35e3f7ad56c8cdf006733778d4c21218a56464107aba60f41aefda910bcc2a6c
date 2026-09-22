<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Milan v1.2 Compliance Review — `IEEE_1722_1_Hardware_Protocol_Processor.md`

Review of the original concept document against the requirements of a **non-redundant
Milan v1.2 PAAD** built on IEEE 1722.1-2021. Companion architecture: [`architecture/`](architecture/01_overview.md).

## 1. Executive summary

The reviewed document proposes a sound **execution architecture** — shared packet
infrastructure, protocol-graded compute (tiny ADP FSM / medium ACMP engine / microcoded
AECP), hazard scoreboard, deadline engine, control-plane-only boundary. Those ideas
survive into the new architecture. It is, however, **not yet a Milan architecture**: it
models ACMP with IEEE semantics that Milan replaces, models ADP from a controller's
perspective, has no path for the ~40 % of PAAD behavior that the entity must *originate*
(probes, liveness checks, notifications), never defines the external-engine interfaces
that most mandatory commands depend on, and contains no requirement inventory to size
anything against.

Top findings: [GAP-02](#gap-02) (ACMP model), [GAP-16](#gap-16) (ADP model),
[GAP-17](#gap-17) (no self-originated traffic), [GAP-04](#gap-04) (external "Hardware
API" undefined), [GAP-01](#gap-01) (no clause-mapped requirement inventory).
Every finding is dispositioned into the new architecture — see [§7](#7-disposition-of-findings-f002).

## 2. Scope and compliance target

Target: **non-redundant PAAD**, Milan Specification Consolidated **v1.2** (Final,
2023-11-30). Milan chapter 8 (seamless redundancy) is wholly excluded; the architecture
keeps its structural seams parameterized ([01 §7](architecture/01_overview.md)).

Pinned base revisions (Milan §2):

| Standard | Revision |
|---|---|
| ATDECC | IEEE Std 1722.1-**2021** |
| AVTP | IEEE Std 1722-**2016** |
| gPTP | IEEE Std 802.1AS-**2011** + Cor1-2013 + Cor2-2015 (not -2020) |
| Bridging/SRP | IEEE Std 802.1Q-**2014** |
| AVB profile | IEEE Std 802.1BA-2011 |

Precedence rule: **where Milan differs from IEEE 1722.1 ACMP (or elsewhere), Milan takes
precedence** (Milan §5.5.2.1). The master delta list is
[F01.4](architecture/01_overview.md#fig-01-deltas).

Milan v1.2 contains **no PICS / conformance annex**; requirements are inline
shall/should/may prose. The compliance matrix in [§6](#6-compliance-matrix-f001) is therefore
built from clause extraction, not from a published proforma.

## 3. Methodology

- Sources: the reviewed document; Milan v1.2 consolidated PDF (printed page = PDF − 7);
  IEEE 1722.1-2021 PDF. Every requirement row carries its clause.
- Procedure: extract requirements → map onto the reviewed document (Covered / Partial /
  Absent / Incorrect) → derive findings → disposition each finding into the new
  architecture → attach a verification category.
- Severity scale: **Blocker** (architecture cannot express the required behavior) ·
  **Major** (required subsystem/behavior missing, structure permits adding) ·
  **Minor** (scoping/policy gap) · **Info** (documentation/convention risk).

> ⚠ Bit tables in Milan and IEEE 1722.1 are **MSB-first** (bit 31 ⇔ mask `0x00000001`).
> The **hex mask column is authoritative**; never derive shifts from bit-number columns.

## 4. What the document got right

| Strength (original §) | Retained as |
|---|---|
| Shared packet engine + normalized transaction (§2, §4, §5) | [03 §2–§5](architecture/03_packet_engine.md), record extended with `origin` |
| Compute gradation: ADP tiny / ACMP medium / AECP µcoded (§1, §3, §23) | [04](architecture/04_adp_engine.md)/[05](architecture/05_acmp_engine.md)/[06](architecture/06_aecp_engine.md); ACMP refined to table-driven record executor |
| 4-stage pipeline, variable-latency EXECUTE (§5) | [03 §4](architecture/03_packet_engine.md) with three amendments |
| Command scoreboard / "deterministic safe parallelism" (§13) | [03 §6](architecture/03_packet_engine.md), classes re-grounded ([F03.7](architecture/03_packet_engine.md#fig-03-hazards)) |
| Deadline engine, deadline from command reception (§20) | [08](architecture/08_timing.md) timer service + PRNG |
| TX arbiter merging all sources (§16) | [03 §8](architecture/03_packet_engine.md) |
| Control-plane-only boundary (§21) | [01 §2](architecture/01_overview.md); the "Hardware API" is now four concrete adapters ([02 §4](architecture/02_interfaces.md)) |
| 16-controller table (§15) | Controller registry + separate lock manager ([06 §7](architecture/06_aecp_engine.md)) |
| Configurable response buffer (§19) | TX slot classes incl. full-frame oversize slot ([03 §7](architecture/03_packet_engine.md)) |
| µcode extensibility; single-source command model & toolchain vision (§9, §26) | [06 §8](architecture/06_aecp_engine.md), [09 §1](architecture/09_verification.md) |
| Implementation options analysis A–D (§22) | Rationale retained in [01 §3](architecture/01_overview.md) |

## 5. Gap findings

#### <a id="gap-01"></a>GAP-01 [Blocker] — No clause-mapped requirement inventory
The document names protocols, not requirements: no mandatory AEM/MVU command list, no
descriptor set, no per-command Milan behavior (direction rules, status codes, response
sizes). Nothing can be sized (µcode ROM, RAMs, timers) or verified against it.
Evidence: Milan mandates ~24 AEM commands with per-command deviations (Milan §5.4.2.1–.29),
Milan-extended GET_STREAM_INFO 80-byte response (§5.4.2.10, Fig 5.1), direction
prohibitions (SET_STREAM_INFO input → `NOT_SUPPORTED`, START/STOP_STREAMING output →
`NOT_SUPPORTED`; §5.4.2.9/.19/.20), SET_STREAM_INFO all-or-nothing sub-flag rule
(§5.4.2.9), GET_DYNAMIC_INFO execution rules (IEEE §7.4.76), correctly-sized
`NOT_IMPLEMENTED` responses for **all** opcodes (IEEE §9.3.5.3.3).
**Disposition**: command master table [F06.14](architecture/06_aecp_engine.md#fig-06-cmdtable);
matrix §6 below is the inventory.

#### <a id="gap-02"></a>GAP-02 [Blocker] — ACMP modeled with IEEE semantics Milan replaces
Original §7 keeps CONNECT/DISCONNECT_TX as talker state operations with talker-side
connection records. Milan (ch. 5.5): the talker is **stateless** (PROBE_TX is a pure
query; DISCONNECT_TX responds SUCCESS with no effect; GET_TX_CONNECTION →
`NOT_SUPPORTED`); all connection intelligence is the **listener's 8-state
binding/probing state machine** per Stream Input, driven by ADP discovery and SRP
registration events; messages are renamed (BIND_RX/UNBIND_RX/PROBE_TX); the ACMPDU is
truncated to 56 bytes; **all five command timeouts are 200 ms** (Table 5.26); binding
persists across power cycles (§5.3.8.2). "Milan as additive profile" (original §17)
understates this: Milan *replaces* ACMP semantics (§5.5.2.1).
**Disposition**: [05](architecture/05_acmp_engine.md) — stateless talker rules + listener
SM package (F05.2–F05.6).

#### <a id="gap-03"></a>GAP-03 [Major] — Milan Vendor Unique protocol absent
"Milan MVU" appears only as a label. Missing: MVU framing (protocol_id
`00-1B-C5-0A-C1-00`, 15-bit command_type, padding excluded from cdl; §5.4.3.2),
mandatory **GET_MILAN_INFO** (protocol_version = 1, features flags, certification_version;
§5.4.4.1), recommended SET/GET_SYSTEM_UNIQUE_ID (§5.4.4.2/.3) and
SET/GET_MEDIA_CLOCK_REFERENCE_INFO (§5.4.4.4/.5), MVU timing 250 ms / respond ≤ 240 ms
(§5.4.3.4).
**Disposition**: [06 §6.9](architecture/06_aecp_engine.md), feature-flag parameters in
[F01.5](architecture/01_overview.md#fig-01-params).

#### <a id="gap-04"></a>GAP-04 [Blocker] — External-engine "Hardware API" never defined
Original §21 draws arrows to AVTP/gPTP/TSN engines but defines no interface. Mandatory
behavior depends on those interfaces: GET_AVB_INFO / GET_AS_PATH (gPTP data; §5.4.2.23/.24),
GET_STREAM_INFO (SRP declaration/registration state, failure code+bridge, accumulated
latency; §5.4.2.10), GET_COUNTERS (link/gPTP/media-clock/stream events; §5.4.2.25),
talker DA-validity gate (MAAP + 15 s probe freshness **or** listener registered;
§4.3.3.1), MAAP-conflict recovery (withdraw → 2×LeaveAll → new DA; Table 5.3),
MSRP domain adopt/re-declare (§4.2.7.2.1), unsolicited notifications on all of the above
(Table 5.22).
**Disposition**: interface classes and the four adapters in
[02](architecture/02_interfaces.md); status dictionary [F02.10](architecture/02_interfaces.md#fig-02-statusdict);
the `srp` contract is served in scope by the SRP engine ([10](architecture/10_srp_engine.md),
§6.9 REQ-SRP rows, §8 item 9).

#### <a id="gap-05"></a>GAP-05 [Major] — Counters/diagnostics subsystem absent
GET_COUNTERS is mandatory for every AVB_INTERFACE, CLOCK_DOMAIN, STREAM_INPUT and
STREAM_OUTPUT of the current configuration (§5.4.2.25), with defined 32-bit wrapping
counters, invariant pairs (LINK_UP/DOWN, LOCKED/UNLOCKED, START/STOP), ≤ 1 s observation
intervals, and reset rules (input bank cleared on not-bound→bound; three output counters
cleared on stream start). Milan's STREAM_OUTPUT mask layout **differs from IEEE**
(Milan Table 5.17: MEDIA_RESET `0x4`, TIMESTAMP_UNCERTAIN `0x8`, FRAMES_TX `0x10`) —
Milan takes precedence (Δ-tagged).
**Disposition**: counters subsystem [06 §6.6](architecture/06_aecp_engine.md), banks in
[07 §4](architecture/07_memory_maps.md).

#### <a id="gap-06"></a>GAP-06 [Major] — Notification/registry/lock machinery underspecified
Original §15/§16 sketch a table and a TX mux. Required: registry tuples {controller EID,
MAC, **port**, per-controller next sequence_id} with no-duplicate rule, ≥ 16 per AVB
interface, cleared on power cycle (§5.3.4.2); fan-out to all registered controllers
**excluding the requester**, per-entry DA/EID/seq on the recorded port (§5.4.5.1);
trigger set = every successful state-changing command + non-ATDECC changes while
unlocked + async triggers of Table 5.22 with **≤ 1 notification per descriptor per
second** for counters; departing-controller detection (random 30–60 s monitor,
CONTROLLER_AVAILABLE probe + one retry, removal + targeted DEREGISTER; §5.4.5.3);
optional registration-overflow probing before mandatory `NO_RESOURCES` (§5.4.2.21); TIME_LIMITED
registrations with 300 s expiry (IEEE §7.4.37.2). The original conflates lock ownership
with this table: the **lock manager** is a separate object (ENTITY scope only, UNLOCK
flag, 60 s auto-unlock → notification; §5.4.2.2). Identify machinery (CONTROL 0/255,
multicast notification 3× @150 ms; §5.3.12, §5.4.5.4, IEEE §7.5.1) is absent.
**Disposition**: [06 §7](architecture/06_aecp_engine.md); records in [07 §4](architecture/07_memory_maps.md).

**Landed 2026-08-18**: registry (16 rows, duplicates refreshed, NO_RESOURCES on
overflow), TIME_LIMITED 300 s expiry with targeted u=1 DEREGISTER, the per-entry
sequence emission walk, successful state-changing command triggers with requester
exclusion and no-op suppression, the per-descriptor GET_COUNTERS limiter, and the
§5.4.5.3 random monitor with CONTROLLER_AVAILABLE, one retry, any-status rearm, and
targeted removal. The optional overflow eviction sweep is not attempted. Identify
notification machinery remains open.

#### <a id="gap-07"></a>GAP-07 [Major] — Timing model incomplete
Original §20 has one AECP number (250 ms, with a 187.5 ms internal target). The real
constant set is ~22 entries: ADP valid_time 10 → advertise every 5 s, delay 0–4 s
(0–2 s at startup — two distinct constants), ACMP 200 ms ×5 with exact-duplicate retry
then 4 s backoff, listener delay 0–1 s, TMR_NO_TK 10 s, AEM/MVU 250/240 ms, monitor
30–60 s, lock 60 s, TIME_LIMITED 300 s, identify 3×150 ms, observation ≤ 1 s, DA
freshness 15 s, MAAP backoff 2×LeaveAll. Randomized draws require an IEEE-seeded PRNG.
The 187.5 ms figure is not spec-derived; budgets replace it.
**Disposition**: master table [F08.1](architecture/08_timing.md#fig-08-constants), timer
service + PRNG [08 §3](architecture/08_timing.md), budgets [08 §4](architecture/08_timing.md).

#### <a id="gap-08"></a>GAP-08 [Major] -- Entity-model memory architecture incomplete
"Descriptor RAM" is named but not designed. Needed: static descriptor image + dynamic
overlay split; **IEEE 1722.1-2021 Table 7-8** STREAM descriptor layout (formats_offset =
138, N ≤ 47 formats, redundancy tail emitted with R = 0 even when non-redundant, per
Milan §5.3.3.4 which binds the descriptor to [ATDECC, Clause 7.2.6] and leaves Annex C
Table C.1 a **may**); name table for all
named descriptors; per-configuration index maps; READ_DESCRIPTOR assembly
incl. the 4-byte failure stub (IEEE §7.4.5). Response buffering must anticipate Milan
**oversize responses** (no cdl cap for six commands; §5.4.1) — a full-Ethernet-frame TX
slot, not `MAX_AECP_RESPONSE_SIZE` guesswork.
The live audio-map transaction is implemented: the engine stages a full page,
the root validates every row, and commit is all-or-nothing. Persisting and
restoring mappings remains part of GAP-09 and issue #70.
The static descriptor image, per-configuration index map, writable name table,
and coherent READ_DESCRIPTOR name patching are implemented. Name updates now
emit the persistence trigger, but replay after power loss remains in GAP-09.
**Disposition**: [07 §3](architecture/07_memory_maps.md), TX slots [03 §7](architecture/03_packet_engine.md).

#### <a id="gap-09"></a>GAP-09 [Major] — Persistence requirements absent
Milan mandates non-volatile storage of eleven state groups: sampling rate (§5.3.5.1),
stream formats in/out (§5.3.7.1/§5.3.8.1), presentation-time offset (§5.3.7.6), bound
state + binding parameters (§5.3.8.2/.3), started/stopped (§5.3.8.7), input and output
mappings (§5.3.10.1/§5.3.9.1), current clock source (§5.3.11.1), all user names
(§5.3.13). Explicitly volatile: lock state, controller registry, identify (reset to 0).
Boot must restore **before** entity enable, and a restored binding starts the listener
SM in `PRB_W_AVAIL` (§5.5.3.5.2). Persistence of the current configuration index is
*not* stated by Milan — recorded as an open decision (§8).
**Disposition**: NVM manager + records + flows [07 §5](architecture/07_memory_maps.md).

#### <a id="gap-10"></a>GAP-10 [Major] — Reusability substance missing
"Reusable FPGA IP" is claimed without the artifacts that make IP reusable: no clock/
reset/CDC strategy, no bus-agnostic interface contracts (signal tables + handshakes), no
parameter table, no profile mechanism, ungrounded scoreboard classes.
**Disposition**: [02 §2](architecture/02_interfaces.md) (CDC), interface classes A–F
(02), parameters [F01.5](architecture/01_overview.md#fig-01-params), profile-ROM strategy
[01 §7](architecture/01_overview.md), hazard classes [03 §6](architecture/03_packet_engine.md).

#### <a id="gap-11"></a>GAP-11 [Minor] — No verification/compliance strategy
One sentence on co-simulation (§26). Needed: requirement↔test traceability, listener-SM
matrix walking, malformed/tolerance suite, timing verification with compressed timers,
notification-storm and NVM power-cut tests, doc-sync regression.
**Disposition**: [09](architecture/09_verification.md); Verification column in §6.

#### <a id="gap-12"></a>GAP-12 [Minor] — Non-redundant scoping not explicit
The document never states the redundancy position. For a non-redundant PAAD: Milan ch. 8
excluded; GET_MILAN_INFO `REDUNDANCY` flag = 0; STREAM descriptors emitted with R = 0 and
Annex C Table C.1 declined (§5.3.3.4 makes it a **may** absent a redundant pair);
per-interface keying kept parameterized as the redundancy seam; gPTP-as-media-clock
(§7.5) is *only* legal non-redundant single-AVB_INTERFACE.
**Disposition**: [01 §1/§7](architecture/01_overview.md).

#### <a id="gap-13"></a>GAP-13 [Minor] — Firmware/REBOOT scope ambiguity
Milan v1.2 mandates **no** firmware-update mechanism, no REBOOT, no MEMORY_OBJECT
operations, no AEM checksum (verified by full-text search). These are IEEE-optional
(Annex D informative). Leaving them implied bloats the control plane.
**Disposition**: optional side-port assist behind `P-EN-FIRMWARE-ASSIST`
([02 §7](architecture/02_interfaces.md)); EFU_MODE capability = 0.

#### <a id="gap-14"></a>GAP-14 [Info] — All diagrams ASCII
Violates the project requirement that every figure be an editable artifact.
**Disposition**: Mermaid/WaveDrom/draw.io per [docs/README.md](README.md) §3; regeneration
+ lint via `Makefile`.

#### <a id="gap-15"></a>GAP-15 [Info] — Spec-literalism traps unaddressed
Traps that silently break interop if unknown: MSB-first bit tables (masks authoritative);
PDU length = cdl + 12 (IEEE figures printing +8 are an erratum) and padding excluded
from cdl → parser trusts cdl; mandatory short-PDU tolerance (2013 ACMPDU, 2013
ENTITY_AVAILABLE response, REGISTER_UNSOLICITED without flags); ACQUIRE_ENTITY must be
implemented but **never succeed** (→ `NOT_SUPPORTED`, §5.4.2.1) so no acquire/contention
machinery; IN_PROGRESS is incompatible with GET_DYNAMIC_INFO (IEEE §7.4.76.2) → policy:
**never emit IN_PROGRESS**, always respond ≤ 240 ms; AECP unicast vs ACMP/ADP multicast
`91-E0-F0-01-00-00` and identify multicast `91-E0-F0-01-00-01`.
**Disposition**: conventions ([docs/README.md](README.md) §4), parser rules
[F03.6](architecture/03_packet_engine.md#fig-03-valrules), policy notes in 06.

#### <a id="gap-16"></a>GAP-16 [Blocker] — ADP engine modeled from the controller side
Original §6 designs an "entity table + timer/aging" — that is what a *controller* keeps.
A PAAD needs: an **advertise SM per AVB interface** (DOWN/WAITING/DELAY; 5 s advertise;
0–4 s random delay, 0–2 s at startup; re-advertise on **GM change**; ENTITY_DEPARTING
only on shutdown, never on link-down; §5.6.3), ADP gating (start only when ready to
accept AECP + bind/probe; §5.6.1), `available_index` TX semantics (increment after each
ENTITY_AVAILABLE; reset on departing/power-up; IEEE §6.2.2.9), and a **per-bound-sink
talker-discovery SM** (GM-id + domain match, `available_index` restart detection,
TMR_NO_ADP aging; §5.6.4) feeding the ACMP listener SM.
**Disposition**: [04](architecture/04_adp_engine.md) (F04.2/F04.3).

#### <a id="gap-17"></a>GAP-17 [Blocker] — Purely reactive pipeline
The RX→process→TX pipeline has no path for traffic the entity must **originate**:
periodic/triggered ADP, listener PROBE_TX commands (with exact-duplicate retry),
CONTROLLER_AVAILABLE liveness probes (with one-retry inflight tracking), unsolicited
responses to ≥ 16 controllers, IDENTIFY_NOTIFICATION multicasts. These need an
originator with an inflight table so returning responses route back to their owners.
**Disposition**: originator + inflight [03 §5/§8](architecture/03_packet_engine.md);
pipeline origins {RX, TIMER, SELF, MGMT} [03 §4](architecture/03_packet_engine.md).

## 6. Compliance matrix (F00.1)

<a id="fig-00-matrix"></a>
Column key — **Cov**: original-document coverage (C = Covered, P = Partial, A = Absent,
I = Incorrect). **Mand**: shall / should / may / rec (Milan "recommendation, future
requirement") / design (architecture-imposed) / — (informative). **Arch**: element of the new architecture. **Doc**: architecture document
section. **Ver**: verification category per [09 §3](architecture/09_verification.md)
(DIR directed · MTXW matrix walker · TOL malformed/tolerance · TIM timing · RND
randomized multi-controller · STORM notification storm · NVM power-cut restore ·
lint = CI gate, [09 §7](architecture/09_verification.md) · — = no dynamic
verification).

### 6.1 Discovery (ADP)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-ADP-001 | Milan §5.6.2 | valid_time = 10 (20 s); advertise every 5 s | shall | A | [GAP-07](#gap-07) | advertise SM | 04 §6.1 | TIM |
| REQ-ADP-002 | Milan §5.6.2 | entity_capabilities: AEM, VU, CLASS_A, GPTP =1; PERSISTENT_ACQUIRE, GENERAL_CONTROLLER_IGNORE, ENTITY_NOT_READY, ACMP_ACQUIRE_WITH_AEM =0; AEM_IDENTIFY_CONTROL_INDEX_VALID, AEM_INTERFACE_INDEX_VALID =1 | shall | A | [GAP-16](#gap-16) | ADPDU sourcing table | 04 §3 | DIR |
| REQ-ADP-003 | Milan §5.6.2, §5.3.1 | entity_model_id valid EUI-64 (≠0, ≠all-1s); changes when static model changes | shall | A | [GAP-01](#gap-01) | config/ID regs + model lint | 07 §3 | DIR |
| REQ-ADP-004 | Milan §5.3.3.1 | talker_stream_sources / listener_stream_sinks = max across **all** configurations | shall | A | [GAP-16](#gap-16) | ADPDU sourcing | 04 §3 | DIR |
| REQ-ADP-005 | Milan §5.6.2 note | ADPDU fields independent of current configuration | shall | A | [GAP-16](#gap-16) | ADPDU sourcing | 04 §3 | DIR |
| REQ-ADP-006 | Milan §5.6.1 | Start ADP only when ready to accept AECP commands and bind/probe requests | shall | A | [GAP-16](#gap-16) | boot sequencer gate | 01 §5, 04 §6.1 | DIR |
| REQ-ADP-007 | Milan §5.6.3 | Advertise SM per AVB interface: DOWN/WAITING/DELAY; events DISCOVER(0/own), TMR, LINK, GM_CHANGE, SHUTDOWN | shall | I | [GAP-16](#gap-16) | F04.2 | 04 §6.1 | MTXW |
| REQ-ADP-008 | Milan §5.6.3.5.2/.3 | Random delay 0–2 s at startup-link-up; 0–4 s otherwise | shall | A | [GAP-07](#gap-07) | T-ADP-DELAY-START / T-ADP-DELAY | 08 §2 | TIM |
| REQ-ADP-009 | Milan §5.6.3.5.7 | GM change ⇒ re-advertise (via DELAY) | shall | A | [GAP-16](#gap-16) | GPTP adapter event | 04 §6.1 | DIR |
| REQ-ADP-010 | Milan §5.6.3.5.6/.8/.11 | ENTITY_DEPARTING only on SHUTDOWN; never on link-down | shall | A | [GAP-16](#gap-16) | F04.2 | 04 §6.1 | DIR |
| REQ-ADP-011 | IEEE §6.2.2.9 | available_index: 0 at init; ++ after each ENTITY_AVAILABLE tx; 0 on DEPARTING/power-up | shall | A | [GAP-16](#gap-16) | available_index mgr | 04 §5 | DIR |
| REQ-ADP-012 | Milan §5.6.4 | Talker-discovery SM per bound Stream Input (not a general entity table) | shall | I | [GAP-16](#gap-16) | F04.3 | 04 §6.2 | MTXW |
| REQ-ADP-013 | Milan §5.6.4.5.1/.2 | Ignore ENTITY_AVAILABLE whose gptp_grandmaster_id or domain ≠ local port state; available_index ≤ last ⇒ talker-restart handling | shall | A | [GAP-16](#gap-16) | F04.3 guards | 04 §6.2 | DIR |
| REQ-ADP-014 | Milan §5.6.4.5.1 | TMR_NO_ADP from received valid_time; expiry ⇒ EVT_TK_DEPARTED | shall | A | [GAP-07](#gap-07) | T-ADP-NOADP | 04 §6.2, 08 §2 | TIM |

### 6.2 Connection management (ACMP)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-ACMP-001 | Milan §5.5.2.2 | Send truncated 56-B ACMPDU; accept 56-B and longer | shall | A | [GAP-15](#gap-15) | parser + builder | 03 §3, 05 §3 | TOL |
| REQ-ACMP-002 | Milan §5.5.2.2 | BIND_RX/UNBIND_RX/PROBE_TX usage; unique_id = STREAM_OUTPUT/INPUT descriptor index of current config; CL_ENTRIES_VALID = 0 | shall | I | [GAP-02](#gap-02) | F05.13 + rules | 05 §3 | DIR |
| REQ-ACMP-003 | Milan Table 5.26 | All five command timeouts = 200 ms | shall | A | [GAP-07](#gap-07) | T-ACMP-CMD | 08 §2 | TIM |
| REQ-ACMP-004 | Milan §5.5.2.7, §5.5.4 | Talker stateless: no bound/settled listener state; SRP (never ACMP) tells the talker about listeners | shall | I | [GAP-02](#gap-02) | stateless responder | 05 §6bis | DIR |
| REQ-ACMP-005 | Milan §5.5.4.1 | PROBE_TX responses: TALKER_UNKNOWN_ID / ignore-or-INCOMPATIBLE_REQUEST (wrong interface) / TALKER_DEST_MAC_FAILED / SUCCESS{cc=0, echo flags, stream params} | shall | A | [GAP-02](#gap-02) | F05.11 | 05 §6bis | DIR |
| REQ-ACMP-006 | Milan §5.5.4.1 | Talker ignores STREAMING_WAIT; streams whenever bandwidth is reserved | shall | A | [GAP-02](#gap-02) | F05.11 note | 05 §6bis | DIR |
| REQ-ACMP-007 | Milan §5.5.4.2/.4 | DISCONNECT_TX → SUCCESS no-op; GET_TX_CONNECTION → NOT_SUPPORTED | shall | I | [GAP-02](#gap-02) | responder rules | 05 §6bis | DIR |
| REQ-ACMP-008 | Milan §5.5.4.3 | GET_TX_STATE: REGISTERING_FAILED = registering Listener Asking Failed; stream fields = declared values | shall | A | [GAP-02](#gap-02) | responder rules | 05 §6bis | DIR |
| REQ-ACMP-009 | Milan §4.3.3.1 | Talker DA valid ⇔ MAAP-allocated ∧ (PROBE_TX ≤ 15 s ∨ matching listener attr registered) | shall | A | [GAP-04](#gap-04) | F05.12, SRP adapter | 05 §6bis, 02 §4 | TIM |
| REQ-ACMP-010 | Milan Table 5.3 | MAAP conflict / PCP change ⇒ withdraw attr, wait 2×LeaveAll, new DA, re-declare | shall | A | [GAP-04](#gap-04) | F05.12 | 05 §6bis | DIR |
| REQ-ACMP-011 | Milan §5.5.3.2/.5 | Listener SM: 8 states with normative transition set | shall | I | [GAP-02](#gap-02) | F05.2–F05.6 | 05 §6 | MTXW |
| REQ-ACMP-012 | Milan §5.5.3.1 | Dispatch: LISTENER_UNKNOWN_ID on bad unique_id; silently ignore bad PROBE_TX_RESPONSE; ignore all other ACMP | shall | A | [GAP-02](#gap-02) | RX classifier | 05 §4 | TOL |
| REQ-ACMP-013 | Milan §5.5.3.5.3 | Canonical bind: lock check, NVM store, response SUCCESS{cc=1}, start discovery, PROBE_TX{FAST_CONNECT=1}, save copy | shall | A | [GAP-02](#gap-02) | A-ID actions | 05 §6.3 | MTXW |
| REQ-ACMP-014 | Milan §5.5.3.5.6/… (v1.2) | Re-bind same talker+source ⇒ update controller EID + STREAMING_WAIT only | shall | A | [GAP-02](#gap-02) | matrix cells | 05 §6.3 | MTXW |
| REQ-ACMP-015 | Milan §5.5.3.5.16/.23 | Probe retry = exact duplicate once (200 ms), then 4 s backoff with acmpsta = LISTENER_TALKER_TIMEOUT (7) | shall | A | [GAP-07](#gap-07) | F05.4 | 05 §6.4 | TIM |
| REQ-ACMP-016 | Milan §5.5.3.5.18/.36/.42/.48 | Settle: latch {stream_id, DA, VLAN}; SRP reservation; TMR_NO_TK 10 s; register/unregister events on exact match | shall | A | [GAP-02](#gap-02) | F05.5 | 05 §6.5 | MTXW |
| REQ-ACMP-017 | Milan §5.3.8.9 | Settled SRP params must equal last PROBE_TX_RESPONSE; divergent talker attr ignored → re-probe | shall | A | [GAP-02](#gap-02) | F05.5 guard | 05 §6.5 | DIR |
| REQ-ACMP-018 | Milan §5.3.8.5 | Declare Listener Ready iff matching Talker Advertise registered; Asking Failed optional | shall | A | [GAP-04](#gap-04) | SRP adapter ops | 02 §4 | DIR |
| REQ-ACMP-019 | Milan §5.5.3.5.41/.47 | Talker departure while settled ⇒ note only (keep reservation) | shall | A | [GAP-02](#gap-02) | matrix cells | 05 §6.3 | MTXW |
| REQ-ACMP-020 | Milan §5.5.2.4/.5 | BIND/UNBIND from non-lock-owner ⇒ CONTROLLER_NOT_AUTHORIZED | shall | C | [GAP-06](#gap-06) | listener A1 on the notify lock (landed) | 06 §6.8 | DIR |
| REQ-ACMP-021 | Milan §5.3.8.2/.3, §5.5.3.5.2 | Binding (talker EID, source idx, controller EID, started) persists; boot with saved binding → PRB_W_AVAIL | shall | A | [GAP-09](#gap-09) | NVM records | 07 §5 | NVM |
| REQ-ACMP-022 | Milan §5.5.3.5.4 etc. | GET_RX_STATE always SUCCESS; three content forms (unbound/probing/settled) | shall | A | [GAP-02](#gap-02) | F05.14 | 05 §6.7 | DIR |
| REQ-ACMP-023 | Milan §5.3.8.6 | pbsta (3-bit) / acmpsta (5-bit; valid only while PROBING_ACTIVE) exposure | shall | A | [GAP-02](#gap-02) | sink record | 05 §5, 07 §4 | DIR |

### 6.3 Control (AECP/AEM)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-AEM-001 | Milan §5.4.1 | Responses may exceed the 524-octet cdl cap (READ_DESCRIPTOR, GET_AVB_INFO, GET_AS_PATH, GET_AUDIO_MAP, ADD/REMOVE_AUDIO_MAPPINGS) up to a max Ethernet frame | may | A | [GAP-08](#gap-08) | oversize TX slot | 03 §7 | DIR |
| REQ-AEM-002 | Milan §5.4.2.1 | ACQUIRE_ENTITY implemented but never SUCCESS; respond NOT_SUPPORTED | shall | C | [GAP-15](#gap-15) | E_NSUPPE echo (landed) | 06 §6.8 | DIR |
| REQ-AEM-003 | Milan §5.4.2.2 | LOCK_ENTITY: UNLOCK flag; ENTITY descriptor only; 60 s auto-unlock ⇒ unsolicited | shall | C | [GAP-06](#gap-06) | KL_aecp_notify lock (landed) | 06 §6.8 | TIM |
| REQ-AEM-004 | Milan §5.4.2.3 / IEEE §7.4.3 | ENTITY_AVAILABLE: 2021 response with flags + acquired/locked IDs | shall | A | [GAP-01](#gap-01) | F06.14 row | 06 §6 | DIR |
| REQ-AEM-005 | Milan §5.4.2.21/§5.4.5.3 | Entity originates CONTROLLER_AVAILABLE for the departing-controller monitor with one retry; overflow probing remains optional | shall | A | [GAP-17](#gap-17) | originator + inflight (landed for monitor) | 03 §5, 06 §7 | RND |
| REQ-AEM-006 | Milan §5.4.2.4 / IEEE §7.4.5 | READ_DESCRIPTOR: allowed while locked/acquired; 4-byte stub on failure | shall | P | [GAP-01](#gap-01) | model store assembly | 07 §3 | DIR |
| REQ-AEM-007 | Milan §5.4.2.5 | SET_CONFIGURATION rejected with STREAM_IS_RUNNING if any input bound or output streaming; lock-protected | shall | A | [GAP-01](#gap-01) | CFG_BARRIER + guard | 03 §6, 06 §6.4 | DIR |
| REQ-AEM-008 | Milan §5.4.2.7 | SET_STREAM_FORMAT: STREAM_IS_RUNNING / BAD_ARGUMENTS (mapping refs channel absent in new format) | shall | A | [GAP-01](#gap-01) | validation chain | 06 §6.4 | DIR |
| REQ-AEM-009 | Milan §5.4.2.9 | SET_STREAM_INFO: OUTPUT only (INPUT → NOT_SUPPORTED); MSRP_ACC_LAT_VALID sets presentation offset 0..0x7FFFFFFF ns; any unsupported sub-flag ⇒ whole command NOT_SUPPORTED | shall | A | [GAP-01](#gap-01) | F06.14 row | 06 §6.3 | DIR |
| REQ-AEM-010 | Milan §5.4.2.10 | GET_STREAM_INFO: Milan 80-B extended response (flags_ex, pbsta, acmpsta); renamed flags; full validity matrix | shall | C | [GAP-01](#gap-01) | E_GSTRI + gsi face (landed; validity matrix = integrator serving the face) | 06 §6.2 | DIR |
| REQ-AEM-011 | Milan §5.4.2.11/.12 | SET/GET_NAME for all names of implemented descriptors; persisted | shall | C | live commands and coherent descriptor overlay implemented; persistence in [GAP-09](#gap-09) | name table + NVM trigger | 06 §6.2.1, 07 §3/§5 | DIR |
| REQ-AEM-012 | Milan §5.4.2.13/.14 | SET/GET_SAMPLING_RATE per Audio Unit; may NOT_SUPPORTED when mappings mismatch and no SRC ("UNSUPPORTED" in spec text is a typo) | shall | A | [GAP-01](#gap-01) | validation chain | 06 §6.4 | DIR |
| REQ-AEM-013 | Milan §5.4.2.15/.16 | SET/GET_CLOCK_SOURCE per Clock Domain; persisted | shall | A | [GAP-09](#gap-09) | CLOCK_CFG class | 06 §6, 07 §5 | NVM |
| REQ-AEM-014 | Milan §5.4.2.17/.18, §5.3.12 | SET/GET_CONTROL for Identify (0 / 255; reset default 0) | shall | A | [GAP-06](#gap-06) | identify handler | 06 §7 | DIR |
| REQ-AEM-015 | Milan §5.4.2.19/.20 | START/STOP_STREAMING: INPUT only (OUTPUT → NOT_SUPPORTED); bound+stopped→started semantics; persisted | shall | A | [GAP-01](#gap-01) | F06.14 rows | 06 §6.3 | DIR |
| REQ-AEM-016 | Milan §5.4.2.21, §5.3.4.2 | REGISTER_UNSOLICITED: tuple {EID, MAC, port}, no duplicates, ≥16/interface, seq init 0; overflow ⇒ NO_RESOURCES (eviction probe is a MAY — not attempted); never deregister a responder | shall | C | [GAP-06](#gap-06) | KL_aecp_notify registry (landed) | 06 §7, 07 §4 | RND |
| REQ-AEM-017 | IEEE §7.4.37.2 | TIME_LIMITED flag: 300 s expiry ⇒ auto-DEREGISTER unsolicited to that controller; accept 2013 no-flags form | shall | C | [GAP-06](#gap-06) | KL_aecp_notify TL timers (landed) | 06 §7 | TIM |
| REQ-AEM-018 | Milan §5.4.2.25 | GET_COUNTERS for every AVB_INTERFACE/CLOCK_DOMAIN/STREAM_IN/STREAM_OUT of current config; Milan mask set takes precedence over IEEE for STREAM_OUTPUT | shall | P | [GAP-05](#gap-05) | E_GCTRS locate-first + type gate (landed; the integrator serves every declared STREAM_OUTPUT counter bank) | 06 §6.6 | DIR |
| REQ-AEM-019 | Milan Tables 5.1/5.4/5.6/5.7 | Counter semantics: invariant pairs; ≤1 s observation intervals; input bank reset on not-bound→bound; output MEDIA_RESET/TS_UNCERTAIN/FRAMES_TX reset on stream start | shall | A | [GAP-05](#gap-05) | counter banks | 06 §6.6, 07 §4 | DIR |
| REQ-AEM-020 | Milan §5.4.2.26 | GET_AUDIO_MAP: fixed partition, subsets ≤176 channels, number_of_maps = N always | shall | C | [GAP-08](#gap-08) | E_GAMAP + E_GAMAPO, both port directions off the integrator's map stores (landed) | 06 §6.5, 07 §3 | DIR |
| REQ-AEM-021 | Milan §5.4.2.27/.28 | ADD/REMOVE_AUDIO_MAPPINGS: all-or-nothing BAD_ARGUMENTS; input conflict rules; REMOVE ignores duplicates; streaming-output changes gated by TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING; input maps changeable any time | shall | C | live transaction implemented; persistence in [GAP-09](#gap-09) | staged `MAP_VALID` transaction plus root projector | 06 §6.5 | DIR |
| REQ-AEM-022 | Milan §5.4.2.29 / IEEE §7.4.76 | GET_DYNAMIC_INFO: fixed-size-GET whitelist (else BAD_ARGUMENTS, nothing processed); per-element status; skip-on-overflow; incompatible with IN_PROGRESS | shall | P | [GAP-15](#gap-15) | GDI iterator | 06 §6.7 | DIR |
| REQ-AEM-023 | IEEE §9.3.5.3.3 | Correctly-sized NOT_IMPLEMENTED response for every unimplemented opcode | shall | A | [GAP-01](#gap-01) | response-size ROM | 06 §6 | TOL |
| REQ-AEM-024 | IEEE §9.3.2.6 | AEM: respond ≤240 ms (250 ms controller timeout); policy: never IN_PROGRESS | shall | P | [GAP-07](#gap-07) | deadline engine | 08 §4 | TIM |
| REQ-AEM-025 | Milan §5.4.2.22 + Table 5.22 | DEREGISTER on auto-removal sent unsolicited to that controller only | shall | A | [GAP-06](#gap-06) | KL_aecp_notify targeted holder (landed) | 06 §7 | RND |
| REQ-AEM-026 | IEEE §7.4.39, Milan §5.4.5.4 | IDENTIFY_NOTIFICATION: unsolicited-only (command ⇒ BAD_ARGUMENTS); multicast DA 91-E0-F0-01-00-01; 3× @150 ms; 1 s re-arm | should | A | [GAP-06](#gap-06) | identify handler | 06 §7 | DIR |

### 6.4 Milan Vendor Unique (MVU)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-MVU-001 | Milan §5.4.3.2 | MVU framing: protocol_id 00-1B-C5-0A-C1-00; r=0; 15-bit command_type; padding excluded from cdl | shall | A | [GAP-03](#gap-03) | MVU sub-decoder | 06 §6.9 | DIR |
| REQ-MVU-002 | Milan §5.4.4.1, §4.2.4 | GET_MILAN_INFO: protocol_version = 1; features (REDUNDANCY=0; TALKER_DYNAMIC_MAPPINGS optional); certification_version | shall | A | [GAP-03](#gap-03) | F06.11 | 06 §6.9 | DIR |
| REQ-MVU-003 | Milan §5.4.4.2/.3 | SET/GET_SYSTEM_UNIQUE_ID (default 0; set ≠ 0) | rec | A | [GAP-03](#gap-03) | P-EN-MVU-SUID | 06 §6.9 | DIR |
| REQ-MVU-004 | Milan §5.4.4.4/.5, §7.6 | SET/GET_MEDIA_CLOCK_REFERENCE_INFO: flags = supported set in responses; default prio read-only; 64-B UTF-8 domain name, default "DEFAULT" | rec | A | [GAP-03](#gap-03) | P-EN-MVU-MCR | 06 §6.9 | DIR |
| REQ-MVU-005 | Milan §5.4.3.3/.4 | MVU status {SUCCESS, NOT_IMPLEMENTED}; 250 ms timeout / respond ≤240 ms | shall | A | [GAP-03](#gap-03) | deadline engine | 08 §2 | TIM |

### 6.5 Notifications and registry

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-NOT-001 | Milan §5.4.5.1 | Fan-out: one message per registered controller excluding requester; per-entry DA/EID/seq on recorded port; seq +1 after handing to stack | shall | A | [GAP-06](#gap-06) | KL_aecp_notify row walk (landed) | 06 §7 | STORM |
| REQ-NOT-002 | Milan §5.4.5.2 | Triggers: every successful state-changing command; equivalent non-ATDECC changes while unlocked | shall | A | [GAP-06](#gap-06) | command effect queue and observed fabric triggers (landed) | 06 §7 | RND |
| REQ-NOT-003 | Milan Table 5.22 | Async triggers: GET_STREAM_INFO/GET_AVB_INFO/GET_AS_PATH field changes; GET_COUNTERS ≤1/descriptor/s; LOCK auto-unlock; auto-DEREGISTER | shall | P | [GAP-06](#gap-06) | KL_aecp_notify observed trigger set and per-descriptor limiter (landed) | 06 §7 | STORM |
| REQ-NOT-004 | Milan §5.4.5.3 | Departing-controller detection: per-controller random 30–60 s; CONTROLLER_AVAILABLE + retry; any-status reply re-arms; silence ⇒ remove + targeted DEREGISTER | shall | A | [GAP-06](#gap-06) | registry monitor plus originator (landed) | 06 §7 | TIM |
| REQ-NOT-005 | Milan §5.3.4.2 | Registry cleared by power cycle | shall | A | [GAP-09](#gap-09) | volatile policy | 07 §5 | NVM |

### 6.6 Entity model

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-MDL-001 | Milan §5.3.2 | Descriptor subset + cardinalities (AVB_INTERFACE ≥1, CLOCK_DOMAIN ≥1, CLOCK_SOURCE ≥1/domain); exactly one parent per descriptor | shall | A | [GAP-08](#gap-08) | F07.2 | 07 §3 | DIR |
| REQ-MDL-002 | Milan §5.3.3.4 | STREAM: buffer_length ≥ 2 126 000 ns; CLASS_A flag; no CRF+AAF mix in one format list; current_format ∈ list | shall | A | [GAP-08](#gap-08) | model lint | 07 §3 | DIR |
| REQ-MDL-003 | Milan §5.3.3.4 → IEEE 1722.1-2021 §7.2.6 | STREAM descriptors in Table 7-8 layout: formats_offset 138, N ≤ 47, `timing` at 136, redundancy tail `redundant_offset` = 138+8N with R = 0. Milan Annex C Table C.1 (formats at 136, no `timing`) is a **may** for any Stream and a shall only for a redundant pair; this PAAD declares none, so it is not emitted | shall (layout) | A | [GAP-08](#gap-08) | descriptor assembly | 07 §3 | DIR |
| REQ-MDL-004 | Milan §5.3.3.5 | Same AVB_INTERFACE index for the same physical port in all configurations | shall | A | [GAP-12](#gap-12) | index maps | 07 §3 | DIR |
| REQ-MDL-005 | Milan §5.3.3.6 | CLOCK_SOURCE construction: one INPUT_STREAM per CRF-capable input (or the single AAF input); ≥1 INTERNAL if any output; gPTP-as-MC only non-redundant single-interface | shall | A | [GAP-08](#gap-08) | model lint | 07 §3 | DIR |
| REQ-MDL-006 | Milan §5.3.3.7 | STREAM_PORT_INPUT has **no** static AUDIO_MAP (dynamic input mappings mandatory) | shall | A | [GAP-08](#gap-08) | model lint | 07 §3 | DIR |
| REQ-MDL-007 | Milan §5.3.3.8 | AUDIO_CLUSTER channel_count = 1 | shall | A | [GAP-08](#gap-08) | model lint | 07 §3 | DIR |
| REQ-MDL-008 | Milan §5.3.3.9 | ≤1 static mapping per output stream channel across all AUDIO_MAPs | shall | A | [GAP-08](#gap-08) | model lint | 07 §3 | DIR |
| REQ-MDL-009 | Milan §5.3.3.10 | Primary IDENTIFY CONTROL exists in all configurations at the same index | shall | A | [GAP-06](#gap-06) | model lint | 07 §3 | DIR |
| REQ-MDL-010 | Milan §6.3/§6.4 | Talker ≥1 Stream Output and Listener ≥1 Stream Input advertising Base formats (AAF PCM32, 48/96/192 k, {1,2,4,6,8} ch); rate-completeness and configuration-uniformity rules | shall | A | [GAP-01](#gap-01) | format tables | 07 §3 | DIR |
| REQ-MDL-011 | Milan §7.3 | CRF media-clock stream format 0x041060010000BB80; Class A | shall (if CRF) | A | [GAP-01](#gap-01) | format tables | 07 §3 | DIR |

### 6.7 Persistence

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-PER-001 | Milan §5.3.5.1, §5.3.7.1/.6, §5.3.8.1/.2/.3/.7, §5.3.9.1, §5.3.10.1, §5.3.11.1, §5.3.13 | Persist: sampling rate; stream formats in/out; presentation offset; bound state + binding params; started/stopped; output + input mappings; clock source; all user names | shall | A | [GAP-09](#gap-09) | NVM manager | 07 §5 | NVM |
| REQ-PER-002 | Milan §5.3.4.1/.2, §5.3.12 | Volatile: lock state; controller registry; identify = 0 after reset | shall | A | [GAP-09](#gap-09) | volatile policy | 07 §5 | NVM |
| REQ-PER-003 | (unstated) | Current configuration index persistence — Milan silent; design decision: persist | — | A | [GAP-09](#gap-09) | open decision §8 | 07 §5 | NVM |

### 6.8 Base-protocol crossings (control-plane visible)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-NET-001 | Milan §5.3.6.1 | Track per interface: gPTP GM ID, path sequence, domain, propagation delay (GET_AVB_INFO/GET_AS_PATH + notifications) | shall | P | [GAP-04](#gap-04) | E_GAVB/E_GASP + gsi face (supports live propagation delay, depth-8 path data, and independent AVB/path change strobes; the consumer owns their sources) | 02 §4, 06 §6.10 | DIR |
| REQ-NET-002 | Milan §5.3.6.2, §4.2.7.2.1 | Track MSRP domain params (Class A priority 3, default VID 2); adopt + re-declare on differing Domain declaration; notify on change | shall | A | [GAP-04](#gap-04) | `srp` contract; SRP engine | 02 §4, 10 §6.1 | DIR |
| REQ-NET-003 | Milan §5.3.7.2–.4, §5.3.8.8/.9 | Track SRP talker declaration + listener registration states, failure code + bridge ID, accumulated latency | shall | A | [GAP-04](#gap-04) | `srp` contract; SRP engine | 02 §4, 10 §6.3/.4 | DIR |
| REQ-NET-004 | Milan Tables 5.1/5.13 | LINK_UP/LINK_DOWN counter invariant; GPTP_GM_CHANGED counter | shall | A | [GAP-05](#gap-05) | counters | 06 §6.6 | DIR |
| REQ-NET-005 | Milan §4.4.2.2 | Listener discards AVTPDUs not matching configured input format (enforced in AVTP engine; control plane configures) | shall | A | [GAP-04](#gap-04) | AVTP adapter | 02 §4 | DIR |

### 6.9 SRP endpoint engine (in scope by owner decision — §8 item 9)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-SRP-001 | Milan Table 4.3 | MRP timers: joinTime 200 ms (180–240), LeaveTime 5000 ms (4500–7500), leavealltimer 10–15 s, periodictimer 1000 ms (900–1500) | shall | A | [GAP-04](#gap-04) | T-MRP-* | 10 §9, 08 §2 | TIM |
| REQ-SRP-002 | Milan §4.2.7.1.2 | Malformed MRPDU: may process up to the bad field, then discard the rest of that vector-attribute list and all subsequent messages in the PDU | shall | A | [GAP-04](#gap-04) | decoder tolerance | 10 §3 | TOL |
| REQ-SRP-003 | Milan §4.2.7.1.3 | EndMark transmitted as explicit 0x0000 when padding follows | shall | A | [GAP-04](#gap-04) | vector encoder | 10 §3 | DIR |
| REQ-SRP-004 | Milan §4.2.7.2.1 | Class A Domain: priority 3 / default VID 2 at startup and link-up; adopt received params + re-declare on differing declaration; Domain TX independent of gPTP port state | shall | A | [GAP-04](#gap-04) | Domain FSM F10.2 | 10 §6.1 | DIR |
| REQ-SRP-005 | Milan §4.2.7.2.2 | Registrar `IN → MT` immediately on rLv (no leavetimer) outside the LeaveAll cycle (Δ13) | shall | A | [GAP-04](#gap-04) | registrar rule F10.9 | 10 §6.5 | MTXW |
| REQ-SRP-006 | Milan §4.2.7.3, §4.3.2, §4.4.1 | MVRP: talker joins the VLAN before sending any stream frames; listener declares the VID of its settled sinks | shall | A | [GAP-04](#gap-04) | VLAN FSM F10.3 | 10 §6.2 | DIR |

### 6.9b MAAP engine (in scope as the opt-in internal allocator — §8 item 11)

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-MAAP-001 | 1722-2016 B.1 + Table B.9 | Dynamic-pool addresses only via MAAP; the block drawn uniformly from 91:E0:F0:00:00:00..91:E0:F0:00:FD:FF with the whole block inside the pool | shall | A | [GAP-04](#gap-04) | generate_address + fit clamp | [11](architecture/11_maap_engine.md) §6 | RND |
| REQ-MAAP-002 | 1722-2016 B.2 (Figure B.1, Tables B.1/B.10) | PDU byte layout with cdl 16 and stream_id 0; PROBE/ANNOUNCE to 91:E0:F0:00:FF:00, DEFEND unicast to the probe's SA; higher maap_version with a known type interpreted, reserved types ignored | shall | A | [GAP-04](#gap-04) | frame builder + DA-qualified validator demux | [11](architecture/11_maap_engine.md) §3 | DIR |
| REQ-MAAP-003 | 1722-2016 Table B.7 + Table B.8 | The initial PROBE plus MAAP_PROBE_RETRANSMITS = 3 retransmits, the first ANNOUNCE immediately at probeCount!, the claim valid only in DEFEND | shall | A | [GAP-04](#gap-04) | walker | [11](architecture/11_maap_engine.md) §6 | MTXW |
| REQ-MAAP-004 | 1722-2016 B.3.4 | probe_timer strictly inside (500, 600) ms and announce_timer strictly inside (30, 32) s, drawn fresh at every start | shall | A | [GAP-04](#gap-04) | T-MAAP-* via PRNG kinds 5/6 | 08 §2, [11](architecture/11_maap_engine.md) §8 | TIM |
| REQ-MAAP-005 | 1722-2016 B.3.5.5–.7 + Table B.7 + B.3.6.4 | The conflict matrix: rProbe! defended in DEFEND without tie-break; compare_MAC (octet-wise reversed, TRUE = no action) in PROBE/rProbe! and DEFEND/rDefend!+rAnnounce!; every yield re-randomizes | shall | A | [GAP-04](#gap-04) | row decode | [11](architecture/11_maap_engine.md) §6 | MTXW |
| REQ-MAAP-006 | 1722-2016 B.3.6.6 + B.2.7/B.2.8 | DEFEND echoes the probe's requested_*; conflict_start = first allocated conflicting address, conflict_count from it; both fields 0 in PROBE/ANNOUNCE | shall | A | [GAP-04](#gap-04) | defend fields | [11](architecture/11_maap_engine.md) §3 | DIR |
| REQ-MAAP-007 | 1722-2016 B.3.5.2 + Table B.7 footnote c | Release! is a local event: stop timers, INITIAL, no PDU on the wire | shall | A | [GAP-04](#gap-04) | engage-fall arc | [11](architecture/11_maap_engine.md) §6 | DIR |

### 6.10 Non-redundant scoping

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-SCP-001 | Milan §4.2.5, §8.1 | Redundancy optional; non-redundant PAAD excludes all of ch. 8 | may | A | [GAP-12](#gap-12) | scoping stmt | 01 §1 | DIR |
| REQ-SCP-002 | Milan Table 5.20 | GET_MILAN_INFO REDUNDANCY flag = 0 | shall | A | [GAP-12](#gap-12) | F06.11 | 06 §6.9 | DIR |
| REQ-SCP-003 | Milan §5.3.4.2, §8 | Keep per-interface keying (registry, ADP, counters) parameterized as the redundancy seam | design | A | [GAP-12](#gap-12) | P-N-AVB-INTERFACES | 01 §7 | DIR |

### 6.11 Reusability, verification and process requirements

| REQ | Clause | Requirement | Mand | Cov | Finding | Arch | Doc | Ver |
|---|---|---|---|---|---|---|---|---|
| REQ-REU-001 | project charter | Bus-agnostic interface contracts: every external contract is a signal table with a handshake class (A–F) | design | A | [GAP-10](#gap-10) | interface classes | 02 §1–§8 | — |
| REQ-REU-002 | project charter | One parameter master table with defaults and consumers; derived values referenced by ID, never copied | design | A | [GAP-10](#gap-10) | F01.5 + single-source rules | 01 §7, docs/README §2 | lint |
| REQ-REU-003 | project charter | One core clock domain; MAC boundaries cross via dual-clock FIFOs with frame-atomic handoff | design | A | [GAP-10](#gap-10) | clocking contract | 02 §2 | — |
| REQ-VER-001 | project charter | Requirement↔verification traceability: every REQ row names its Ver category or an explicit non-dynamic marker; release gate = the categories of 09 §3 + the CI gates of 09 §7 | design | A | [GAP-11](#gap-11) | verification plan | 09 §3, 09 §7 | — |
| REQ-VER-002 | project charter | Single-source generation: ROMs, golden model, stimulus vectors and doc tables all derive from one command model | design | A | [GAP-11](#gap-11) | F09.1 | 09 §1 | lint |
| REQ-FWX-001 | IEEE §9.3.5.3.3 (outside Milan's mandatory command set; IEEE Annex D is informative) | No firmware update, REBOOT, MEMORY_OBJECT operations or AEM checksum; those opcodes take the unknown-opcode path → `NOT_IMPLEMENTED` echo | shall | A | [GAP-13](#gap-13) | dispatch default | 06 §6 | DIR |
| REQ-DOC-001 | project charter | Every figure an editable artifact (Mermaid/WaveDrom/draw.io) with committed exports, regeneration and staleness gates | design | A | [GAP-14](#gap-14) | Makefile gates | docs/README §3 | lint |

## 7. Disposition of findings (F00.2)

<a id="fig-00-disposition"></a>

| GAP | Severity | Resolution | Addressed in | Verified by | Open residue |
|---|---|---|---|---|---|
| [GAP-01](#gap-01) | Blocker | Full command/descriptor inventory + per-command rules | [F06.14](architecture/06_aecp_engine.md#fig-06-cmdtable), §6 matrix | DIR/TOL | [#76](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/76) |
| [GAP-02](#gap-02) | Blocker | Milan-native ACMP: stateless talker + listener SM package | [05](architecture/05_acmp_engine.md) | MTXW | none found |
| [GAP-03](#gap-03) | Major | MVU sub-decoder + 3 command groups + feature flags | [06 §6.9](architecture/06_aecp_engine.md) | DIR | [#77](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/77) |
| [GAP-04](#gap-04) | Blocker | Interface classes A–F; SRP/MAAP, gPTP, AVTP, media-clock adapters; status dictionary; in-scope SRP engine | [02](architecture/02_interfaces.md), [10](architecture/10_srp_engine.md) | DIR/MTXW/TOL/TIM | [#78](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/78) |
| [GAP-05](#gap-05) | Major | Counters subsystem with Milan-precedence masks | [06 §6.6](architecture/06_aecp_engine.md), [07 §4](architecture/07_memory_maps.md) | DIR | [#79](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/79) |
| [GAP-06](#gap-06) | Major | Registry + monitor + fan-out + lock manager + identify | [06 §7](architecture/06_aecp_engine.md) | RND/STORM/TIM | [#80](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/80) |
| [GAP-07](#gap-07) | Major | Master T-ID table, timer service, PRNG, budgets | [08](architecture/08_timing.md) | TIM | [#81](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/81) |
| [GAP-08](#gap-08) | Major | Entity-model store (image+overlay), Table 7-8 stream assembly, oversize TX slot | [07 §3](architecture/07_memory_maps.md), [03 §7](architecture/03_packet_engine.md) | DIR | [#82](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/82) |
| [GAP-09](#gap-09) | Major | NVM manager, records, commit/restore flows | [07 §5](architecture/07_memory_maps.md) | NVM | [#83](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/83) |
| [GAP-10](#gap-10) | Major | CDC/reset, interface contracts, parameter table, profiles, grounded hazards | [01](architecture/01_overview.md)/[02](architecture/02_interfaces.md)/[03](architecture/03_packet_engine.md) | DIR | [#84](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/84) |
| [GAP-11](#gap-11) | Minor | Verification strategy + traceability | [09](architecture/09_verification.md) | — | [#72](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/72) |
| [GAP-12](#gap-12) | Minor | Explicit non-redundant scope + parameterized seams | [01 §1/§7](architecture/01_overview.md) | DIR | [#69](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69) |
| [GAP-13](#gap-13) | Minor | Firmware assist optional behind side-port flag | [02 §7](architecture/02_interfaces.md) | DIR | none found |
| [GAP-14](#gap-14) | Info | All figures Mermaid/WaveDrom/draw.io + lint | [docs/README.md](README.md), `Makefile` | lint | [#75](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/75) |
| [GAP-15](#gap-15) | Info | Conventions + parser rules + status policies | [docs/README.md](README.md) §4, [03 §3](architecture/03_packet_engine.md) | TOL | [#45](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/45) |
| [GAP-16](#gap-16) | Blocker | ADP advertise SM + talker-discovery SM (entity table dropped) | [04](architecture/04_adp_engine.md) | MTXW | [#85](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/85) |
| [GAP-17](#gap-17) | Blocker | Originator + inflight table; four transaction origins | [03 §5](architecture/03_packet_engine.md) | RND | [#86](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/86) |

The **Open residue** column records the audit of 2026-09-18 at main `6a878f6`: each finding was
checked against what `hdl/` and `tb/` carry, not against this table. A linked issue tracks what is
still unimplemented or ungraded for that finding and lists the requirement tickets under it;
"none found" means the resolution is implemented and a suite of the named category grades it.

## 8. Residual risks and open decisions

| # | Item | Decision taken | Recorded in |
|---|---|---|---|
| 1 | Current configuration index persistence unstated by Milan | **Persist** (least surprise across power cycles) | 07 §5 |
| 2 | AEM status for lock violation unspecified by Milan | Use IEEE `ENTITY_LOCKED` (3) | 06 §6.8 |
| 3 | Milan §5.4.2.13 references "UNSUPPORTED" status | Read as `NOT_SUPPORTED` (11) — no such code exists | 06 §6.4 |
| 4 | `user_mcr_prio` / media-clock-domain-name persistence unstated | Persist alongside REQ-PER-001 set (cheap, user-visible) | 07 §5 |
| 5 | Dual ADP startup delay (0–2 s) vs link-up (0–4 s) — easy single-constant bug | Two distinct T-IDs | 08 §2 |
| 6 | talker/listener_capabilities bits unconstrained by Milan | Set per IEEE Table 6-3/6-4 (IMPLEMENTED + AUDIO/MEDIA_CLOCK as per product) | 04 §3 |
| 7 | IN_PROGRESS vs GET_DYNAMIC_INFO | Never emit IN_PROGRESS; hard ≤240 ms response budget | 06 §5, 08 §4 |
| 8 | Milan-vs-IEEE STREAM_OUTPUT counter masks | Milan masks in Milan profile (Δ-tagged); IEEE masks in plain-IEEE profile ROM | 06 §6.6 |
| 9 | SRP location (originally out of scope per the reviewed doc's §21) | Owner decision 2026-08-11: SRP endpoint (MSRP/MVRP participant) moved **in scope** as doc 10 — 1 Domain FSM, 1 VLAN FSM (Class A, single VID), N + M stream FSMs; MAAP stays external; external-stack alternative retained (`P-EN-SRP-ENGINE`) | [10](architecture/10_srp_engine.md), §6.9 |
| 11 | MAAP location (item 9 recorded "MAAP stays external") | The seam grew an internal server: `KL_pp_maap` ([11](architecture/11_maap_engine.md)) answers the 02 §4.2 contract when the quasi-static `cfg_maap_internal_i` = 1 and publishes the claim for the fabric; the DEFAULT stays 0 = external, byte-identical to the landed integrations, so item 9's shipping wiring is unchanged until the integrator flips the input | [11](architecture/11_maap_engine.md), §6.9b |
| 10 | Implementation strategy for the reference platform | Owner decision 2026-08-11: full implementation (scenario B of [docs/10](10_RESOURCE_AND_EFFORT.md)) proceeds in this repository; the reference platform cuts over by **direct substitution at parity** — the superseded planes are deleted, never parameterized (git history preserves them); the area verdict is accepted with eyes open, the architecture/conformance value is the goal | [docs/10](10_RESOURCE_AND_EFFORT.md) §5/§10 |
