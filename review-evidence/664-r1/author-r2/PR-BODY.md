[A548]

## Contents

- [Status](#status): candidate and validation state.
- [Linked Issue / roles](#linked-issue--roles): task and review ownership.
- [Description](#description): resulting document contract.
- [Authoritative references](#authoritative-references): owner decisions and clauses.
- [Requirement text for owner approval](#requirement-text-for-owner-approval): exact old/new text and new bounds.
- [How to get into the same state](#how-to-get-into-the-same-state): candidate and dependencies.
- [How to validate](#how-to-validate): command bank and outcomes.
- [Known limitations / out of scope](#known-limitations--out-of-scope): remaining implementation and approval.
- [Definition of Done](#definition-of-done): completion conditions.

## Status

Round-2 documentation correction; owner approval and independent re-review remain pending.
`664-mark2-reqs` -> `dev`.
Candidate: `8fb296e3e02985aee27ef04cb08278836b734a14`.
Base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
All 93 command exit codes are zero. B33 skipped vendor analysis; B48 gate 11 calibration did not run because its historical placement report is absent.

## Linked Issue / roles

Relates to #664

Executor: `[A548]`
Internal cleared-context reviewer: `[R508]`
External reviewer: `[R509]`

## Description

Round 2 corrects the MAAP state-machine authority and adds H-DISC for received
ADP and discovery aging, through connection state and any resulting TX commit.
The owner-approval text matches the corrected requirements; PR #674 publication
wording identifies the existing PR and the exact corrected candidate.

The requirement and architecture documents now select ADP, ACMP, AECP
(including notifications and counter serving), MAAP and SRP per function.
Mark II defaults to bare-metal firmware. All-fabric remains supported and stays
the shipping default until F2 to F5 pass suites and bench acceptance for every
stream, all counters and the audio soak. Media and gPTP remain fabric-owned.

One proposed 10 ms project service budget covers each moved control path.
The clause table distinguishes response deadlines, cadence, spacing and ordering.
Eight named hooks measure mailbox/event-to-commit service and wire timing.
The split document ties ownership to F0 rings/HAL/YAML and F1 boot read/apply,
plus the bare-metal-first and FT unit-test directives.

The generated module matrix and leaf indexes were regenerated without drift.
Their inventory remains actual RTL/test evidence. The hand-maintained summary
and MRP timing trace now include the split obligations. Current implementation
pages are explicitly scoped; historical and measured evidence remains historical.
VERSION remains `0x0002_0060`; the architecture describes the later major-3 flip.

## Authoritative references

- #664 assignment 6009584763; owner decisions 6009576644; service-budget ruling 6009675758; round-2 assignment 6010431422 and reviews R508-1/R509-1.
- #665 bare-metal/lwSRP directive 5992455815; unit-test directive 6008744385; #640 D3 and milestone decisions.
- Merged F0 #668 and F1 #669; `docs/design/MAILBOX_SPLIT.md`, `docs/reference/MAILBOX_CONTRACT.md`, both control firmware READMEs.
- `REQUIREMENTS.md`, `docs/reference/FR_NFR.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/reference/REGISTER_MAP.md` VERSION policy.
- Milan v1.2 4.2.7.1.1/Table 4.3; 5.4.2.2; 5.4.3.4; 5.4.5.2/Table 5.22; 5.4.5.3; 5.5.2.3/Table 5.26; 5.6.2; 5.6.3.5/Table 5.50/Table 5.51; 5.6.4.1/Table 5.54/5.6.4.5.1-.4.
- IEEE 1722.1-2021 6.2.2.5, 7.5.1, 7.5.2, 9.3.2.6; IEEE 1722-2016 B.3.2/Table B.7, B.3.3/Table B.8, B.3.4.1/.2, B.3.5.5 and B.3.6.6; IEEE 802.1Q-2018 10.7.4/10.7.11/Table 10-7.
- `docs/spec-refs.md` is absent at the assigned base, as acknowledged by ruling 6009675758. Clause checks used the pinned processor timing transcription and direct standards where the extracts lacked the rule.

## Requirement text for owner approval

Approval is requested for the exact text below, including `T_svc = 10 ms`.
The number is project policy under ruling 6009675758, not a standard timeout.
The owner has not yet approved this candidate. Keep `Relates to #664` until approval.

| Requirement section | Old text at base | New text at candidate |
|---|---|---|
| REQUIREMENTS.md Section 1 | - Bare-metal firmware owns boot policy, CSR initialization, identity,<br>  persistence orchestration, UART diagnostics, and remaining software-visible<br>  control.<br>- The fabric gPTP plane is the sole product PHC, protocol, servo, and public<br>  state owner.<br>- `GPTP_PLANE_EN_P=0` is verification-only hardware. It has no product image<br>  and zero runtime gPTP owners: GM, parent, PathTrace and peer delay are zero;<br>  sync/asCapable are zero; `tu` is one; retained writes are inert.<br>- The fabric owns per-frame classification, reservation, shaping,<br>  timestamping, AVTP/AAF/CRF, MAAP, and IEEE 1722.1 processing.<br>- Required Milan state must survive power loss. The current blank-flash NVM<br>  face does not satisfy this requirement and is the release blocker in #70. | - Bare-metal firmware owns boot policy, CSR initialization, identity,<br>  saved-state boot read/apply and write-back, and UART diagnostics.<br>- ADP, ACMP, AECP (commands, unsolicited notifications and counter serving),<br>  MAAP and SRP MUST each have build-selectable placement.<br>  The Mark II default places them on the bare-metal core.<br>  The all-fabric build remains a supported option.<br>  It remains the shipping default until F2 to F5 pass<br>  their suites and bench acceptance: all streams, counters and audio soak.<br>  Requirement approval precedes that default flip (#664, #665).<br>- The fabric gPTP plane is the sole product PHC, protocol, servo, and public<br>  state owner.<br>- `GPTP_PLANE_EN_P=0` is verification-only hardware. It has no product image<br>  and zero runtime gPTP owners: GM, parent, PathTrace and peer delay are zero;<br>  sync/asCapable are zero; `tu` is one; retained writes are inert.<br>- The fabric MUST retain framing, timestamps, the ingress filter,<br>  the gPTP plane, and the AVTP/AAF/CRF and physical-media paths.<br>  Audio and gPTP deadlines MUST remain independent of firmware service.<br>  Reservation protocol control follows its selected placement.<br>  Media admission enforcement and any shaping remain in fabric.<br>- Each selected function MUST have exactly one authoritative state owner.<br>  Both placements MUST preserve wire behavior, ordering and normative timeouts.<br>  Firmware service MUST satisfy NFR-SCOUT-03 and its path-specific hooks<br>  in the requirements register.<br>- Required Milan state must survive power loss.<br>  The shipping backend is partial; #70 remains a release blocker.<br>  F1 supplies the split store without integrating a shipping image.<br>  Its boot contract governs validation and apply.<br><br>The split architecture defines both placements.<br>Major `0x0003` identifies only images running the split.<br>The major changes with the default-flip implementation, not this document change.<br>MINOR remains flat and continuous across majors.<br>The landing plan pins the simulations and firmware string.<br>The current VERSION remains `0x0002_0060`. |

| Row | Old text at base | New text at candidate |
|---|---|---|
| FR-CTRL-04 | FR-CTRL-04 &#124; `GET_COUNTERS` MUST return the 1722.1-2021/Milan counter sets for STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE (see model `counters`), throttled ≤ 1/s. &#124; M &#124; T | FR-CTRL-04 &#124; Solicited `GET_COUNTERS` MUST return the 1722.1-2021/Milan counter sets for STREAM_INPUT, STREAM_OUTPUT and AVB_INTERFACE (see model `counters`) within NFR-LAT-02. Only unsolicited counter notifications are limited to at most one per descriptor per second (Milan v1.2 5.4.5.2, Table 5.22). &#124; M &#124; T |
| NFR-LAT-02 | NFR-LAT-02 &#124; AVDECC control command→response round-trip SHOULD be < 250 ms (well within 1722.1 inflight timeouts). &#124; S &#124; T | NFR-LAT-02 &#124; AVDECC command responses MUST meet their applicable normative limit in Section 3.4.1 in either placement. Firmware paths MUST also meet NFR-SCOUT-03; a 250 ms transaction timeout MUST NOT replace the 240 ms AECP response bound or the 200 ms Milan ACMP timeout. &#124; M &#124; T |
| NFR-SCUP-02 | NFR-SCUP-02 &#124; Increasing `P_CH`/`P_SR` MUST only linearly increase bandwidth, buffer, and DSP; the control plane (ADP/AECP/ACMP) MUST be unaffected. &#124; M &#124; A | NFR-SCUP-02 &#124; Increasing `P_CH`/`P_SR` MUST only linearly increase media bandwidth, buffer and DSP costs. ADP/AECP/ACMP wire semantics MUST remain unchanged; the selected control placement MUST meet NFR-SCOUT-03 at every supported shape. &#124; M &#124; A |
| NFR-SCUP-04 | NFR-SCUP-04 &#124; The builder MUST generate and size the flat AEM image from the selected end-station model, and bare-metal boot MUST validate and install it at the processor's compile-time descriptor base without an RTL edit as descriptor counts grow. &#124; S &#124; I | NFR-SCUP-04 &#124; The builder MUST generate and size the flat AEM image from the selected entity model. Bare-metal boot MUST validate and install it before entity enable: at the descriptor base for fabric AECP, or in the validated image store for firmware AECP. Descriptor growth MUST NOT require an RTL edit. &#124; S &#124; I |
| NFR-SCOUT-01 | NFR-SCOUT-01 &#124; The release architecture MUST use one cacheless RV32I control hart; increasing stream capacity MUST elaborate additional fabric contexts rather than create a software packet or media plane. &#124; M &#124; A,D | NFR-SCOUT-01 &#124; The release architecture MUST use one cacheless RV32I control hart. Stream capacity MUST grow through fabric media contexts and static, entity-sized control contexts in the selected placement. Every supported shape MUST meet NFR-SCOUT-03 without adding harts or a software media path. &#124; M &#124; A,D |
| NFR-SCOUT-02 | NFR-SCOUT-02 &#124; Protocol control, media movement, and time discipline MUST retain their explicit fabric owners as stream counts grow. &#124; M &#124; A | NFR-SCOUT-02 &#124; ADP, ACMP, AECP (including unsolicited notifications and counter serving), MAAP and SRP MUST each be build-selectable between bare-metal firmware and fabric. Mark II defaults to firmware; all-fabric remains supported and the shipping default until F2 to F5 pass suites and bench acceptance for all streams, counters and audio soak. Each function MUST have one state owner. Framing, timestamps, ingress filtering, gPTP and media MUST remain fabric-owned. &#124; M &#124; A |
| NFR-SCOUT-03 | NFR-SCOUT-03 &#124; Packet and audio deadlines MUST depend only on bounded fabric handshakes, never on firmware service latency. &#124; M &#124; A,T | NFR-SCOUT-03 &#124; Each moved control path MUST meet the single project service budget T_svc = 10 ms, proposed for owner approval, under Section 3.4.1 and measured by Section 3.4.2. Numeric normative response timeouts MUST also hold with margin; ordering, spacing and timer obligations remain independently normative. Audio and gPTP deadlines MUST depend only on bounded fabric handshakes, independent of firmware service latency. &#124; M &#124; A,T |
| NFR-REL-02 | NFR-REL-02 &#124; Fabric liveness monitors SHOULD detect a stalled protocol, time, or media engine and recover or report it without requiring a full-board reboot. &#124; S &#124; T | NFR-REL-02 &#124; Fabric liveness monitors SHOULD detect a stalled time or media engine. Control liveness SHOULD detect a stalled selected protocol owner, including firmware, and recover or report it without a full-board reboot. Expired control-service bounds MUST NOT be hidden by continued advertising. &#124; S &#124; T |

The NFR-LAT-02 priority changes from S to M to enforce existing protocol limits.
FR-CTRL-04 separates solicited response deadlines from unsolicited push spacing.
No normative wire timeout, ordering rule or timer tolerance is relaxed.

The following new sections have no previous text. They define the exact timing,
measurement and integration-test obligations added by NFR-SCOUT-03.

### 3.4.1 Control service budget and normative timing

This section implements the #664 service-budget ruling.
**Proposed project budget: `T_svc = 10 ms`.**
Owner approval of this value is required before merge.
It is not a numeric timeout supplied by a standard.

Each immediate path measures mailbox RX commitment to TX commitment.
Events start at their occurrence, including time awaiting event-ring space.
A timer event starts at its armed deadline, not dequeue.
TX commitment means the complete record's accepted `TX_HEAD` write.
The last required recipient's commit ends a notification fan-out.
Backlog, preemption, state access and saved-state service consume this budget.
TX-ring backpressure also consumes it; freeing space never restarts timing.

Some paths intentionally wait under a normative timer or spacing rule.
Their full RX/event-to-TX interval MUST also be recorded.
Let `W` denote only that required or selected normative wait.
The bound is `elapsed <= W + T_svc` for that action.
All software overhead around the wait shares one `T_svc`.
No extra budget is granted at timer arm, expiry or retry.
A zero random draw gives `W=0`.
For a periodic expiry alone, the deadline starts the service interval.
State-machine inputs requiring no transmission finish at state/timer commitment.
Their transition service has the same project bound.

| Moved path | Normative timing and source | Derivation: related interval and 10% ceiling | Additional normative obligation |
|---|---|---|---|
| ADP startup AVAILABLE | Milan v1.2 5.6.3.5.2: random delay 0 to 2 s | 2 s random-window extent gives 200 ms; `T_svc=10 ms` fits. Zero draws are serviced immediately, never treated as a positive interval | Preserve the selected draw and startup state |
| ADP DISCOVER, GM_CHANGE, LINK_UP and periodic AVAILABLE | Milan v1.2 5.6.3.5.3/.4/.5/.7/.9 and Table 5.50: 0 to 4 s random delay; fixed 5 s advertise timer. Milan 5.6.2: `valid_time=10`; IEEE 1722.1-2021 6.2.2.5: two-second units, hence 20 s validity | min(4 s, 5 s, 20 s) x 10% = 400 ms. For the whole ADP function, startup tightens this to 200 ms | Apply Table 5.51; a DISCOVER or GM change in DELAY does not restart it. Advertisement and discovery aging are separate timers |
| ADP SHUTDOWN to DEPARTING | Milan v1.2 5.6.3.5.8/.11 requires transmission, without a numeric shutdown-response maximum | Related ADP minimum positive window extent is 2 s, giving 200 ms. The 10 ms service bound is project policy | Stop the applicable timer and send DEPARTING. Preserve its order before a restart's AVAILABLE |
| Listener ADP AVAILABLE, DEPARTING and discovery aging | Milan v1.2 5.6.4.1, Table 5.54 and 5.6.4.5.1-.4: process each matching bound sink; arm/reset TMR_NO_ADP from received `valid_time`. IEEE 1722.1-2021 6.2.2.5: two-second units; Milan 5.6.2 sends 10, hence 20 s | Milan validity 20 s gives 2 s; the minimum legal received validity is 2 s, giving 200 ms (also the related ADP startup ceiling). A resulting ACMP action uses the tighter 200 ms transaction interval (Milan 5.5.2.3, Table 5.26), giving 20 ms. The same project service <= 10 ms covers reception or original expiry through discovery and connection commitments, including any resulting TX commit | Preserve received validity, interface/GM/domain guards and restart event ordering. Record normative connection waits separately; do not restart the service allowance at discovery-to-connection handoff |
| ACMP PROBE_TX, GET_TX_STATE, BIND_RX, UNBIND_RX, GET_RX_STATE | Milan v1.2 5.5.2.3, Table 5.26: each transaction times out at 200 ms, replacing the applicable IEEE 1722.1-2021 Table 8-1 value | 200 ms x 10% = 20 ms; service <= 10 ms. The complete command transaction must finish inside 200 ms with measured margin | A retry cannot enlarge one attempt's timeout; delayed probe/backoff events retain Milan 5.5.3 timers |
| AECP solicited AEM, descriptor and counter responses | IEEE 1722.1-2021 9.3.2.6: respond within 240 ms; transaction timeout 250 ms | min(240, 250) ms x 10% = 24 ms; service <= 10 ms. The complete response must meet 240 ms with margin | The existing no-IN_PROGRESS policy remains. If adopted later, its 120 ms cadence yields a tighter 12 ms ceiling, still above T_svc |
| AECP MVU response | Milan v1.2 5.4.3.4: response within 240 ms; transaction timeout 250 ms | 240 ms x 10% = 24 ms; service <= 10 ms, with the same wire-response margin | Apply the MVU-specific response and refusal rules |
| AECP successful-command and asynchronous notifications | Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2: immediate notification after the successful state-changing response; Table 5.22 defines asynchronous triggers, without a numeric delivery maximum | Related AECP response interval 240 ms gives 24 ms. `T_svc=10 ms` is a project event-to-commit budget, not a new normative timeout | Response precedes its notification, including cross-protocol causality (#653). Do not wait out T_svc deliberately; notify immediately |
| AECP GET_COUNTERS push | Milan v1.2 5.4.5.2, Table 5.22: at most one notification per descriptor per second. Counter updates: Milan 5.3.7.7/5.3.8.10, at most 1 s | Spacing gives 100 ms; shared AECP response interval tightens the ceiling to 24 ms. Service <= 10 ms once eligible; record the preceding rate-limit wait separately | One second is minimum spacing, not a maximum delivery latency. Coalesce pending changes; preserve counter observation and reset semantics |
| AECP liveness, unlock and optional identification | Milan v1.2 5.4.5.3: 30 to 60 s monitor then CONTROLLER_AVAILABLE; 5.4.2.2: 60 s unlock. IEEE 1722.1-2021 7.5.1/7.5.1.2.1: three Identify notifications, spaced 150 ms when enabled | 150 ms x 10% = 15 ms is the tightest enabled notification interval; service <= 10 ms. Probe responses still obey 9.3.2.6 | Preserve registration, retry, removal and identification ordering; the optional feature is not enabled by this requirement |
| MAAP PROBE and conflict DEFEND | IEEE 1722-2016 B.3.4.2 with constants B.3.3/Table B.8: strictly 500 ms < probe interval < 600 ms; `MAAP_PROBE_RETRANSMITS=3`. B.3.2/Table B.7 defines conflict handling; B.3.5.5 defines the conflicting-PROBE event and B.3.6.6 the DEFEND action | 500 ms x 10% = 50 ms; service <= 10 ms. Three retransmissions do not multiply the per-action budget | DEFEND on the applicable conflicting PROBE transition. The probe interval is not a normative received-PROBE response timeout |
| MAAP ANNOUNCE and reallocation | IEEE 1722-2016 B.3.4.1 with constants B.3.3/Table B.8: strictly 30 s < announcement interval < 32 s; B.3.2/Table B.7 governs loss and retry | Announcement gives 3 s; the shared 500 ms probe interval tightens this to 50 ms | Preserve randomization, strict bounds and address-loss handling; service time cannot push a timer beyond its upper bound |
| SRP/MRP MSRP and MVRP join, leave, periodic and LeaveAll | IEEE 802.1Q-2018 10.7.4/10.7.11, Table 10-7; Milan v1.2 4.2.7.1.1, Table 4.3 overrides: JoinTime 200 ms (180 to 240), LeaveTime 5000 ms (4500 to 7500), periodic 1000 ms (900 to 1500), LeaveAll 10 to 15 s (+/-0.5 s) | Conservative shortest allowed interval: 180 ms x 10% = 18 ms. LeaveTime gives 450 ms; periodic 90 ms; LeaveAll 950 ms. Service <= 10 ms fits each | A point-to-point requested transmit opportunity occurs within JoinTime, at most three per 1.5 x JoinTime. Timer resolution stays <= 1 centisecond; delayed service must not lose ticks |

The tightest mandatory ceiling above is 18 ms for MRP.
Optional identification tightens it to 15 ms.
Even a future IN_PROGRESS cadence would allow 12 ms.
Choosing 10 ms remains below each listed ceiling.
MRP timer resolution is a separate precision requirement, not service allowance.

Normative timer bounds include service and egress effects where applicable.
At the 200 ms MRP default, 40 ms remains before 240 ms.
The proposed 10 ms service uses only part of that slack.
MAAP draws near 600 ms cannot absorb another 10 ms blindly.
Schedule with measured error margins while preserving randomization and strict bounds.
No budget converts a minimum interval into a response deadline.

For numeric response deadlines, measure the complete interval separately.
Ingress, service, TX queuing, arbitration, serialization and network allowance count.
Require `T_ingress + T_svc + T_egress + T_network < timeout`.
For AECP, also enforce its separate 240 ms response endpoint.
Publish each measured allowance and the remaining positive margin.
A mailbox commit alone cannot prove the wire deadline.
Dropped or unserved accepted records fail, rather than disappearing from measurements.

### 3.4.2 Control service test hooks

These hooks are acceptance requirements for the integration lanes.
They are not claims of implemented instrumentation or passing target timing.
Use a monotonic elapsed-time clock, independent of PHC steps.
Record placement, shape, core clock, input identity and timestamp resolution.
A measured upper bound includes that resolution and instrumentation error.

| Hook | Trace to requirements | Start and completion observations | Required checks |
|---|---|---|---|
| H-ADP | FR-DISC-01..05; NFR-SCOUT-01..03 | ADP `RX_HEAD` commit or startup/GM/link/shutdown occurrence; timer arm and original deadline; AVAILABLE/DEPARTING `TX_HEAD` commit and wire departure | Startup, DISCOVER, periodic, GM, both link edges, shutdown/restart; full rings; zero/max draws; ignored events and stale tags; DEPARTING before AVAILABLE |
| H-DISC | FR-DISC-01..05; FR-CONN-01..04; NFR-SCOUT-01..03 | Received ENTITY_AVAILABLE/ENTITY_DEPARTING `RX_HEAD` commit or original TMR_NO_ADP deadline to every matching sink's discovery/timer and resulting connection-state commitment; include the last resulting `TX_HEAD` commit and wire observation where transmission follows | Every Table 5.54 cell; received-valid_time arm/reset and expiry; available_index restart; interface and GM/domain mismatch; departing; all matching bound sinks; late receive handling or aging must fail independently of H-ADP |
| H-ACMP | FR-CONN-01..04; NFR-LAT-02; NFR-SCOUT-01..03 | ACMP `RX_HEAD` commit to the matched response `TX_HEAD`; originated command commit to response receipt; discovery/probe timer deadline to its action | Each Table 5.26 command, success/refusal, retry, distinct sequence/unique IDs, restore and fast connect; wire round-trip < 200 ms with margin |
| H-AECP | FR-ENUM-01/02; FR-CTRL-01..06; FR-MVU-01..03; NFR-SCUP-04; NFR-LAT-02 | AECP `RX_HEAD` commit to matched response `TX_HEAD`, plus received-command and emitted-response wire observations | AEM/MVU, descriptors, getters/setters, counters and refusals; longest image/state access; locks; malformed/truncated requests; response <= 240 ms with margin |
| H-NOTIFY | FR-CTRL-03; FR-MGT-01/02; NFR-SCOUT-02/03 | Causal command RX or asynchronous state-change occurrence to the last required notification `TX_HEAD`; record response commit and every recipient's wire departure | Successful-command ordering, cross-channel ACMP response then AECP notice, all registered recipients, departure probes, unlock, enabled Identify spacing, full transmit rings |
| H-COUNTERS | FR-CTRL-04; FR-STR-04; NFR-OBS-01; NFR-SCOUT-02/03 | Fabric counter snapshot/update event to the last push `TX_HEAD`; previous notification wire time supplies eligibility; solicited GET_COUNTERS uses H-AECP | Every descriptor bank and stream, coherent snapshots, resets/wrap, multiple changes while rate-limited; >= 1 s per-descriptor wire spacing; <= 1 s counter update |
| H-MAAP | FR-MAAP-01; NFR-SCOUT-02/03 | MAAP `RX_HEAD` commit or original timer deadline to PROBE/DEFEND/ANNOUNCE `TX_HEAD`; state completion when no frame is required | Conflict in each state, three probe retransmissions, allocation loss/retry, strict probe/announce intervals, ring stalls and boundary draws |
| H-SRP | FR-SRP-01..03; FR-CONN-02; NFR-SCOUT-01..03 | SRP `RX_HEAD` commit or fabric timer deadline to MRPDU `TX_HEAD`; registrar/state-apply commitment for non-transmitting transitions | MSRP/MVRP joins, withdrawal, malformed vectors, LeaveAll/periodic expiry, coalesced tick backlog, reservation/licence updates; JoinTime and LeaveTime bounds |

H-DISC follows discovery events through their connection actions.
All matching sinks share one service allowance for the received record.
State commitment does not restart timing before a resulting TX.
Only normative waits contribute `W`; total service remains <= 10 ms.
Record the original aging deadline and the received validity separately.
Test received validity 1, 10 and 31, without substituting 10.
An unchanged discovery state still requires observing completed input handling.
These checks follow Milan v1.2 Table 5.54:

| Discovery input and state | Required H-DISC check | Milan v1.2 clause |
|---|---|---|
| AVAILABLE in TK_NOT_DISCOVERED | Reject GM/domain mismatch; otherwise save interface/index, arm received validity, commit discovery and EVT_TK_DISCOVERED's connection action | 5.6.4.5.1 |
| AVAILABLE in TK_DISCOVERED | Ignore interface mismatch; a rising available_index refreshes index/validity. On index <= last, apply EVT_TK_DEPARTED first; GM/domain mismatch stops aging and leaves TK_NOT_DISCOVERED, otherwise apply EVT_TK_DISCOVERED then refresh index/validity | 5.6.4.5.2 |
| DEPARTING in TK_DISCOVERED | Ignore interface mismatch; otherwise stop aging, commit TK_NOT_DISCOVERED and EVT_TK_DEPARTED's connection action | 5.6.4.5.3 |
| Original TMR_NO_ADP expiry in TK_DISCOVERED | Commit TK_NOT_DISCOVERED and EVT_TK_DEPARTED's connection action within the same service allowance, including delayed event publication | 5.6.4.5.4 |
| DEPARTING or stray expiry in TK_NOT_DISCOVERED | DEPARTING is ignored; no aging timer may remain armed. Inject a stale expiry and require no invented departure or connection action | Table 5.54, ignored and impossible cells |

Each hook MUST run at every supported stream/channel/rate shape.
Exercise simultaneous protocol traffic, maximum legal backlog and NVM write-back.
Test saturation, reset, timer wrap, CPU stalls and both bus adapters.
Test every supported placement combination across cross-protocol state changes.
Plant late-service and reordered-output defects that the named checks reject.
Late service remains a failed bound even if recovery succeeds.
A stopped core must not leave a fabric ADP advertiser running.
Audio and gPTP must retain their deadlines under these loads.

F0 proves mailbox-access counts under stated assumptions, not target milliseconds.
F1 proves model-time flash bounds, not the complete loop's CPU time.
See F0 service latency
and F1 service bounds.
Their integration must establish the proposed budget before changing defaults.

The corresponding changed architecture and traceability rows follow.
These describe placement and evidence; they do not upgrade implementation status.

| Trace row | Old | New |
|---|---|---|
| FR_NFR: **Control** | **Control** &#124; ADP, AECP/AEM+MVU, ACMP, MAAP, MSRP/MVRP &#124; bounded protocol deadlines &#124; protocol processor plus fabric MAAP &#124; generated stream contexts | **Control** &#124; ADP, AECP/AEM+MVU, ACMP, MAAP, MSRP/MVRP &#124; normative limits plus T_svc in firmware &#124; one selected owner per function; Mark II firmware default, current shipping fabric default &#124; static generated control contexts |
| FR_NFR: Discovery | Discovery &#124; FR-DISC-\* &#124; Section 5.2 &#124; `adp`, ENTITY &#124; M-B2 -- processor (Section 2.0) | Discovery &#124; FR-DISC-\*, NFR-SCOUT-01..03 &#124; Sections 5.6.2/5.6.3/5.6.4 &#124; `adp`, ENTITY &#124; Current fabric ledger: Section 2.0; split F0/F3, hooks H-ADP/H-DISC/H-ACMP |
| FR_NFR: Enum/Control | Enum/Control &#124; FR-ENUM/CTRL &#124; Section 5.3–5.4 &#124; full descriptor tree &#124; M-B3, processor AECP uCPU plus the builder-generated image copied by bare-metal firmware; the served inventory and mandatory gaps are listed in Section 2.0 | Enum/Control &#124; FR-ENUM/CTRL, NFR-LAT-02, NFR-SCOUT-01..03 &#124; Sections 5.3/5.4 &#124; full descriptor tree &#124; Current fabric ledger: Section 2.0; split F5, hooks H-AECP/H-NOTIFY/H-COUNTERS |
| FR_NFR: Connection | Connection &#124; FR-CONN-\* &#124; Section 5.5 &#124; STREAM_\*, CBS CSR &#124; M-B4 -- processor; fast-connect/persistence **NOT MET** | Connection &#124; FR-CONN-\*, NFR-LAT-02, NFR-SCOUT-01..03 &#124; Section 5.5; Table 5.26 &#124; STREAM_\*, selected state owner &#124; Current fabric ledger: Section 2.0; split F1/F3, H-ACMP; cold restore remains unproven |
| FR_NFR: MAAP/SRP | MAAP/SRP &#124; FR-MAAP/SRP &#124; Section 5.6 &#124; STREAM_\*, classifier/CBS &#124; M-B5 -- MAAP in fabric, SRP on the processor | MAAP/SRP &#124; FR-MAAP/SRP, NFR-SCOUT-01..03 &#124; Sections 4.3.1/4.2.7; Table 4.3 &#124; STREAM_\*, admission &#124; Current fabric ledger: Section 2.0; split F2/F4, H-MAAP/H-SRP |
| FR_NFR: Scale-out | Scale-out &#124; NFR-SCOUT-\* &#124;  -  &#124; fabric contexts / replicated endpoint &#124; Section 4 | Scale-out &#124; NFR-SCOUT-\*, NFR-SCUP-02/04, NFR-REL-02 &#124; Sections 3.4.1/3.4.2 list timing clauses &#124; fabric media / static selected-owner control contexts &#124; Section 4; every shape, placement and hook |
| IEEE 802.1Q: MRP-6 | MRP-6 &#124; 10.7.11 &#124; Timer values: JoinTime ~200 ms, LeaveTime 600–1000 ms, LeaveAllTime ~10 s (+Milan tolerances 4.2.7.1.1) &#124; processor timer service &#124; 🔵 PROCESSOR -- Milan Table 4.3 tightens these values and the submodule owns them now; since processor pin `b2db3a97` its srp_top suite grades joinTime, the periodictimer and the leavealltimer against Table 4.3 (Q1-Q4, processor issue 64). `tb/verilator/pp_shadow` compresses the prescaler for liveness only, never for cadence &#124; 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. | MRP-6 &#124; 10.7.11 &#124; Timer values: JoinTime 200 ms (180 to 240), LeaveTime 5000 ms (4500 to 7500), periodic 1000 ms (900 to 1500), LeaveAllTime 10 to 15 s (+/-0.5 s), Milan 4.2.7.1.1 Table 4.3; firmware service uses NFR-SCOUT-03 and H-SRP &#124; processor timer service &#124; 🔵 PROCESSOR -- Milan Table 4.3 overrides the IEEE defaults and the submodule owns them now; since processor pin `b2db3a97` its srp_top suite grades joinTime, the periodictimer and the leavealltimer against Table 4.3 (Q1-Q4, processor issue 64). `tb/verilator/pp_shadow` compresses the prescaler for liveness only, never for cadence &#124; 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. |

### Round-2 changes from the reviewed candidate

R508-1-F1 and R509-1-F1 concern MAAP authority; R509-1-F2 concerns listener timing.
The exact changed or added rows follow; unchanged rows retain their approved-scope proposal.

| Row | Old text at reviewed head | New text at candidate |
|---|---|---|
| MAAP PROBE and conflict DEFEND | MAAP PROBE and conflict DEFEND &#124; IEEE 1722-2016 B.3.4.2, Table B.8: strictly 500 ms < probe interval < 600 ms; `MAAP_PROBE_RETRANSMITS=3`. B.3.3, B.3.5.5 and B.3.6.6 define conflict handling &#124; 500 ms x 10% = 50 ms; service <= 10 ms. Three retransmissions do not multiply the per-action budget &#124; DEFEND on the applicable conflicting PROBE transition. The probe interval is not a normative received-PROBE response timeout | MAAP PROBE and conflict DEFEND &#124; IEEE 1722-2016 B.3.4.2 with constants B.3.3/Table B.8: strictly 500 ms < probe interval < 600 ms; `MAAP_PROBE_RETRANSMITS=3`. B.3.2/Table B.7 defines conflict handling; B.3.5.5 defines the conflicting-PROBE event and B.3.6.6 the DEFEND action &#124; 500 ms x 10% = 50 ms; service <= 10 ms. Three retransmissions do not multiply the per-action budget &#124; DEFEND on the applicable conflicting PROBE transition. The probe interval is not a normative received-PROBE response timeout |
| MAAP ANNOUNCE and reallocation | MAAP ANNOUNCE and reallocation &#124; IEEE 1722-2016 B.3.4.1, Table B.8: strictly 30 s < announcement interval < 32 s; B.3.3 governs loss and retry &#124; Announcement gives 3 s; the shared 500 ms probe interval tightens this to 50 ms &#124; Preserve randomization, strict bounds and address-loss handling; service time cannot push a timer beyond its upper bound | MAAP ANNOUNCE and reallocation &#124; IEEE 1722-2016 B.3.4.1 with constants B.3.3/Table B.8: strictly 30 s < announcement interval < 32 s; B.3.2/Table B.7 governs loss and retry &#124; Announcement gives 3 s; the shared 500 ms probe interval tightens this to 50 ms &#124; Preserve randomization, strict bounds and address-loss handling; service time cannot push a timer beyond its upper bound |
| Listener ADP AVAILABLE, DEPARTING and discovery aging | Absent: no explicit row at the reviewed head | Listener ADP AVAILABLE, DEPARTING and discovery aging &#124; Milan v1.2 5.6.4.1, Table 5.54 and 5.6.4.5.1-.4: process each matching bound sink; arm/reset TMR_NO_ADP from received `valid_time`. IEEE 1722.1-2021 6.2.2.5: two-second units; Milan 5.6.2 sends 10, hence 20 s &#124; Milan validity 20 s gives 2 s; the minimum legal received validity is 2 s, giving 200 ms (also the related ADP startup ceiling). A resulting ACMP action uses the tighter 200 ms transaction interval (Milan 5.5.2.3, Table 5.26), giving 20 ms. The same project service <= 10 ms covers reception or original expiry through discovery and connection commitments, including any resulting TX commit &#124; Preserve received validity, interface/GM/domain guards and restart event ordering. Record normative connection waits separately; do not restart the service allowance at discovery-to-connection handoff |
| H-DISC | Absent: no explicit row at the reviewed head | H-DISC &#124; FR-DISC-01..05; FR-CONN-01..04; NFR-SCOUT-01..03 &#124; Received ENTITY_AVAILABLE/ENTITY_DEPARTING `RX_HEAD` commit or original TMR_NO_ADP deadline to every matching sink's discovery/timer and resulting connection-state commitment; include the last resulting `TX_HEAD` commit and wire observation where transmission follows &#124; Every Table 5.54 cell; received-valid_time arm/reset and expiry; available_index restart; interface and GM/domain mismatch; departing; all matching bound sinks; late receive handling or aging must fail independently of H-ADP |
| AVAILABLE in TK_NOT_DISCOVERED | Absent: no explicit row at the reviewed head | AVAILABLE in TK_NOT_DISCOVERED &#124; Reject GM/domain mismatch; otherwise save interface/index, arm received validity, commit discovery and EVT_TK_DISCOVERED's connection action &#124; 5.6.4.5.1 |
| AVAILABLE in TK_DISCOVERED | Absent: no explicit row at the reviewed head | AVAILABLE in TK_DISCOVERED &#124; Ignore interface mismatch; a rising available_index refreshes index/validity. On index <= last, apply EVT_TK_DEPARTED first; GM/domain mismatch stops aging and leaves TK_NOT_DISCOVERED, otherwise apply EVT_TK_DISCOVERED then refresh index/validity &#124; 5.6.4.5.2 |
| DEPARTING in TK_DISCOVERED | Absent: no explicit row at the reviewed head | DEPARTING in TK_DISCOVERED &#124; Ignore interface mismatch; otherwise stop aging, commit TK_NOT_DISCOVERED and EVT_TK_DEPARTED's connection action &#124; 5.6.4.5.3 |
| Original TMR_NO_ADP expiry in TK_DISCOVERED | Absent: no explicit row at the reviewed head | Original TMR_NO_ADP expiry in TK_DISCOVERED &#124; Commit TK_NOT_DISCOVERED and EVT_TK_DEPARTED's connection action within the same service allowance, including delayed event publication &#124; 5.6.4.5.4 |
| DEPARTING or stray expiry in TK_NOT_DISCOVERED | Absent: no explicit row at the reviewed head | DEPARTING or stray expiry in TK_NOT_DISCOVERED &#124; DEPARTING is ignored; no aging timer may remain armed. Inject a stale expiry and require no invented departure or connection action &#124; Table 5.54, ignored and impossible cells |
| Discovery | Discovery &#124; FR-DISC-\*, NFR-SCOUT-01..03 &#124; Sections 5.6.2/5.6.3/5.6.4 &#124; `adp`, ENTITY &#124; Current fabric ledger: Section 2.0; split F0/F3, hooks H-ADP/H-ACMP | Discovery &#124; FR-DISC-\*, NFR-SCOUT-01..03 &#124; Sections 5.6.2/5.6.3/5.6.4 &#124; `adp`, ENTITY &#124; Current fabric ledger: Section 2.0; split F0/F3, hooks H-ADP/H-DISC/H-ACMP |
| MAILBOX_SPLIT listener discovery | The listener's discovery machine (5.6.4) feeds ACMP and belongs to F3. Its<br>ENTITY_AVAILABLE and ENTITY_DEPARTING from bound talkers need an accept term<br>the ADP channel does not carry yet; adding one is a minor contract change. | The listener's discovery machine (5.6.4) feeds ACMP and belongs to F3. Its<br>ENTITY_AVAILABLE and ENTITY_DEPARTING from bound talkers need an accept term<br>the ADP channel does not carry yet; adding one is a minor contract change.<br><br>F3 must also meet the listener-discovery timing requirement.<br>H-DISC starts at received AVAILABLE/DEPARTING publication or original TMR_NO_ADP expiry.<br>It ends after discovery and resulting connection-state commitments.<br>Any resulting TX commit shares that same service allowance.<br>Normative waits are recorded separately; service remains <= 10 ms.<br>Milan v1.2 5.6.4.1 requires processing every matching bound sink.<br>Sections 5.6.4.5.1/.2 arm/reset aging from the received `valid_time`.<br>IEEE 1722.1-2021 6.2.2.5 defines its two-second units.<br>Table 5.54 and 5.6.4.5.1-.4 supply the transition checks.<br>They cover available_index restart, interface/GM/domain mismatch, departing and expiry.<br>Delayed receive handling or aging must fail H-DISC independently.<br>F0's advertiser checks do not establish this listener timing. |

H-DISC shares one T_svc across all matching sinks and connection/TX work.
The complete timing/hook text above also requires received-validity checks at 1, 10 and 31.
MAILBOX_SPLIT now states the same start, completion, 10 ms allowance and separate waits.
R1 publication wording is corrected: PR #674 already exists. The executor made no remote PR update.


## How to get into the same state

PR #674 is the review object. The first round examined
`a27808375427859dc357f6bfd0a88842062b20ed`. Reproduce this correction at the
exact candidate commit named in Status.

```sh
git checkout --detach 8fb296e3e02985aee27ef04cb08278836b734a14
git rev-parse HEAD
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt -r tools/hdl_reference/requirements.txt
python3 -m pip install pyyaml wavedrom==2.0.3.post3
```

Expected HEAD is the full candidate above. Use an external writable `CHECK_ROOT`
for logs, temporary files, the SDK, HDL reference and a metadata-free export.
Set `TMPDIR` to a directory there. `DEPS_ROOT` denotes the reusable scratch
dependency directory containing the SDK; it may equal `CHECK_ROOT`. Required tools: Verilator 5.050, sv2v 0.0.12,
librsvg, a host C/C++ compiler, Tcl, and the documented LiteX dependencies.
The full builder used the existing RV32 GCC 14.3.0 selector. The repository installer re-verified the reusable pinned Bootlin SDK cache.
No new SDK installation was needed in this round.

## How to validate

Run every command below directly, without piping its result. Independent gates
may run concurrently; keep a log and exit-code file for each. B01 to B48 are the
48-command bank. D01 to D40 add the remaining docs-check workflow commands.
G01 runs the imported gPTP documentation target. N01/N02 run in a `git archive`
export with no git metadata. E01/E02 check generated mailbox consistency. The SDK installer verifies the pinned archive separately.

The offline runner self-test must execute inside a disposable CI job boundary
without host credentials, a Docker socket or network access. B33 was also run
in that container, where no vendor analyzer is installed. Its rc 0 is a SKIP,
not proof of vendor analysis. The full builder also reports one NOT RUN arm:
gate 11 calibration needs the historical mf48 placement-utilization report, which
is absent here. All other builder arms passed. No Vivado or simulation build was run.

| ID | Exact command | rc | Result |
|---|---|---:|---|
| B01 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | PASS |
| B02 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | PASS |
| B03 | `python3 scripts/lint_rtl.py --check --self-test` | 0 | PASS |
| B04 | `python3 scripts/suite_shards.py --selftest` | 0 | PASS |
| B05 | `python3 scripts/ci_events.py --check` | 0 | PASS |
| B06 | `python3 scripts/ci_scope.py --selftest` | 0 | PASS |
| B07 | `python3 scripts/ci_events.py --selftest` | 0 | PASS |
| B08 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | PASS |
| B09 | `python3 scripts/check_feature_status.py` | 0 | PASS |
| B10 | `python3 scripts/check_submodule_docs.py` | 0 | PASS |
| B11 | `python3 scripts/check_cpp_idiom.py` | 0 | PASS |
| B12 | `python3 scripts/check_py_idiom.py` | 0 | PASS |
| B13 | `python3 scripts/docs_check.py` | 0 | PASS |
| B14 | `python3 scripts/check_doc_style.py` | 0 | PASS |
| B15 | `python3 scripts/check_doc_style.py --selftest` | 0 | PASS |
| B16 | `python3 scripts/check_solution_docs.py` | 0 | PASS |
| B17 | `python3 scripts/check_doc_paths.py` | 0 | PASS |
| B18 | `python3 scripts/check_archive.py` | 0 | PASS |
| B19 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | PASS |
| B20 | `python3 scripts/gen_toc.py --check` | 0 | PASS |
| B21 | `python3 scripts/check_hygiene.py --check` | 0 | PASS |
| B22 | `python3 scripts/check_todo_ownership.py` | 0 | PASS |
| B23 | `python3 scripts/check_sv_idiom.py` | 0 | PASS |
| B24 | `python3 scripts/check_sh_idiom.py` | 0 | PASS |
| B25 | `python3 scripts/check_rtl_source_lists.py` | 0 | PASS |
| B26 | `python3 scripts/check_soc_sources.py` | 0 | PASS |
| B27 | `python3 scripts/check_port_contracts.py` | 0 | PASS |
| B28 | `python3 scripts/check_nvm_record_space.py` | 0 | PASS |
| B29 | `python3 scripts/check_baremetal_only.py --check` | 0 | PASS |
| B30 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | PASS |
| B31 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | PASS |
| B32 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | PASS |
| B33 | `python3 scripts/xvlog_gate.py --check` | 0 | SKIPPED: no vendor analyzer in disposable container; not an analysis pass |
| B34 | `python3 scripts/measure_control_flow.py --selftest` | 0 | PASS |
| B35 | `python3 scripts/measure_cohesion.py --selftest` | 0 | PASS |
| B36 | `python3 scripts/check_em_dash.py --base 423ac5d910d09ab189b3acc39ae3ae1d10d50b19` | 0 | PASS |
| B37 | `python3 scripts/measure_fail_fast.py --check` | 0 | PASS |
| B38 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS |
| B39 | `python3 scripts/measure_naming.py --check` | 0 | PASS |
| B40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | PASS |
| B41 | `python3 scripts/gen_toc.py --selftest` | 0 | PASS |
| B42 | `python3 scripts/check_em_dash.py --selftest` | 0 | PASS |
| B43 | `python3 scripts/docs_check.py --selftest` | 0 | PASS |
| B44 | `git diff --check 423ac5d910d09ab189b3acc39ae3ae1d10d50b19 8fb296e3e02985aee27ef04cb08278836b734a14` | 0 | PASS |
| B45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | PASS |
| B46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | PASS |
| B47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | PASS |
| B48 | `python3 sw/builder/test_builder.py --require-rv32` | 0 | PASS; elapsed 1165.2 s; gate 11 calibration NOT RUN because the mf48 placement-utilization report is absent |
| D01 | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | PASS |
| D02 | `python3 scripts/gen_hdl_reference.py --output $CHECK_ROOT/hdl-reference` | 0 | PASS |
| D03 | `python3 scripts/check_gptp_docs.py` | 0 | PASS |
| D04 | `python3 scripts/check_gptp_docs.py --selftest` | 0 | PASS |
| D05 | `python3 docs/DOC_MAP.gen.py --check` | 0 | PASS |
| D06 | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | PASS |
| D07 | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | PASS |
| D08 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | PASS |
| D09 | `python3 scripts/check_solution_docs.py --selftest` | 0 | PASS |
| D10 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | PASS |
| D11 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | PASS |
| D12 | `python3 scripts/check_submodule_docs.py --selftest` | 0 | PASS |
| D13 | `python3 scripts/gen_wavedrom.py --selftest` | 0 | PASS |
| D14 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | PASS |
| D15 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | PASS |
| D16 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | PASS |
| D17 | `python3 scripts/check_diagram_pngs.py` | 0 | PASS |
| D18 | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | PASS |
| D19 | `python3 scripts/check_feature_status.py --self-test` | 0 | PASS |
| D20 | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | PASS |
| D21 | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | PASS |
| D22 | `python3 scripts/ci_rv32_sdk.py --destination $DEPS_ROOT/rv32-sdk` | 0 | PASS |
| D23 | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | PASS |
| D24 | `python3 sw/builder/test_firmware_compiler.py --absent --audit $CHECK_ROOT/rv32-absent.jsonl` | 0 | PASS; compiler-absence controls, zero actual firmware compiler invocations; compiler-dependent proof intentionally NOT RUN here and covered by B48 |
| D25 | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | PASS |
| D26 | `python3 scripts/check_nvm_capture.py` | 0 | PASS |
| D27 | `python3 scripts/check_soc_sources.py --selftest` | 0 | PASS |
| D28 | `python3 sw/litex/iob_pack_selftest.py` | 0 | PASS |
| D29 | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | PASS |
| D30 | `python3 scripts/measure_naming.py --selftest` | 0 | PASS |
| D31 | `python3 scripts/check_port_contracts.py --selftest` | 0 | PASS |
| D32 | `python3 scripts/measure_fail_fast.py --selftest` | 0 | PASS |
| D33 | `python3 scripts/check_todo_ownership.py --selftest` | 0 | PASS |
| D34 | `python3 scripts/check_hygiene.py --selftest` | 0 | PASS |
| D35 | `python3 scripts/check_sv_idiom.py --selftest` | 0 | PASS |
| D36 | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | PASS |
| D37 | `python3 scripts/check_py_idiom.py --selftest` | 0 | PASS |
| D38 | `python3 scripts/check_sh_idiom.py --selftest` | 0 | PASS |
| D39 | `python3 scripts/act_ci.py --selftest` | 0 | PASS; offline self-test in unprivileged, networkless disposable container |
| D40 | `python3 scripts/check_archive.py --selftest` | 0 | PASS |
| G01 | `make -C gptp-processor docs` | 0 | PASS; six imported documentation checks |
| N01 | `python3 scripts/docs_check.py` | 0 | PASS; committed export without git metadata; inventory parity intentionally unavailable without Git; B13 checks it in the checkout |
| N02 | `python3 scripts/check_feature_status.py` | 0 | PASS; committed export without git metadata |
| E01 | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | PASS |
| E02 | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | PASS |

Expected result: all exit codes 0, no drift or findings, and the documented B33
skip and the missing-report calibration limitation. The requirements table and timing hooks still need independent review;
these gates do not establish target service time or hardware acceptance.

## Known limitations / out of scope

- Owner approval of the exact requirements and 10 ms budget remains pending.
- F2 to F5 owe target-time measurements, worst-case load, all-stream/counter acceptance and audio soak before the default flip.
- The assignment's `tb/verilator/hostplane` suite is absent after #259. The landing plan names all five extant VERSION simulations and carries the retired `VERSION >> 16` major assertion into a live suite. It does not restore a retired runtime.
- F0 mailbox access counts and F1 model-time flash bounds are not proof of the composed target loop. No implementation verdict is upgraded.
- No RTL, firmware source, test, VERSION or build-script change.
- During the executor's local validation phase, no push, PR creation/edit, hosted run, merge, hardware access or bench operation was performed. PR #674 was already published before this round.

## Definition of Done

- [ ] Linked Issue acceptance criteria approved by the owner
- [x] Changed documentation defines self-checking integration-test obligations
- [ ] Required local verification bar accepted, including the explicit vendor skip and calibration limitation
- [ ] Self-test evidence posted in a PR comment by the manager
- [x] No undocumented requirement or interface change remains in this candidate
- [ ] Internal cleared-context re-review is positive
- [ ] External re-review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result validated per CONTRIBUTING.md
- [x] Documentation updated where needed
- [ ] Post-merge containment checked before the Issue moves to Done
