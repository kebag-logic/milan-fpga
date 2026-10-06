# [A548] Issue #664 handoff

## Status and identity

Candidate: `8fb296e3e02985aee27ef04cb08278836b734a14` on `664-mark2-reqs`.
Verified assigned base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Verified origin: `https://github.com/kebag-logic/milan-fpga.git`.
All 93 command exit codes are zero. B33 skipped vendor analysis; B48 gate 11 calibration did not run because its historical placement report is absent.
Executor [A548]; independent reviewers [R508] and [R509].
No review verdict is claimed by the executor. Owner approval remains pending.
No push, PR creation/edit, merge, rebase, amend or hardware access occurred.
Only documentation files changed; VERSION and executable artifacts are unchanged.

The prior STOP 6009666033 was resolved by ruling 6009675758.
Round-2 starting head: `a27808375427859dc357f6bfd0a88842062b20ed`.
Round-2 TAKEN: issue #664 comment 6010446308.
Remote dev remained the assigned base; no merge was needed.
Four new one-line commits correct two documentation files.
The last three refine the extract citation for both checkout forms.
The complete lane still changes 21 Markdown files only.
The public handoff is the new REVIEW READY comment on issue #664 for this candidate.

## Scope and source decisions

All five control functions are individually selectable, with exactly one owner.
AECP includes unsolicited notifications and counter serving. The supported
all-fabric image remains the shipping default until F2 to F5 acceptance.
Framing, timestamps, ingress filtering, gPTP and media remain in fabric.
The single-hart/static-pool rule, F0 interface, F1 boot/apply sequence, FT and
unit-test requirements, and version landing plan are explicit in the split document.

Read the full #664 contract and assignment 6009584763, owner decisions 6009576644,
the service-budget ruling 6009675758, #665 directives 5992455815/6008744385, #640,
and merged #668/#669. Latest owner decisions supersede the earlier issue wording.
`docs/spec-refs.md` is absent at this base, explicitly acknowledged by the ruling.
The first timing source was `protocol-processor/docs/architecture/08_timing.md`.
Round-2 extracts: `protocol-processor/docs/architecture/04_adp_engine.md` section 6.2
and `11_maap_engine.md`, at processor pin `ead8036035affd53ef4b29979190f2f4f67084c0`.
Direct Milan 5.6.4.1/Table 5.54/5.6.4.5.1-.4 and IEEE 1722.1-2021
6.2.2.5 checks establish per-sink transitions and received-validity units.
Direct IEEE 1722-2016 B.3.2/Table B.7 supplies state-dependent conflict/loss/retry;
B.3.3/Table B.8 supplies constants; B.3.5.5 and B.3.6.6 supply event/action.
Direct standard clauses supplied missing ADP transitions, MAAP conflict ordering,
notification spacing and timer tolerance detail. Source digests follow below.

## Changed requirement text: old -> new

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


## Every timing bound and test hook

The following is the exact new FR_NFR timing and hook text. It is a proposal for
owner approval, not measured target performance. Required normative waits are
recorded explicitly as W; all service overhead around a wait shares one budget.
Intentional waits never become firmware latency allowance or relax wire limits.

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

## Version and generated traceability

VERSION remains `0x0002_0060`. Only a running split image may use major 3.
The flat minor sequence continues, and the CSR-derived firmware string follows it.
The default-flip PR updates the CSR, generated ENTITY identity, five extant
simulation assertions, documentation and changelog together after acceptance.

The five current files are `tb/verilator/csr/sim_main.cpp` and
`tb/verilator/milan_dp/sim_main.cpp`, `sim_nxn.cpp`, `sim_gptp.cpp`, `sim_prune.cpp`.
The assignment also names `tb/verilator/hostplane`, absent at the base after #259.
Its `VERSION >> 16` intent must be carried into a live suite, testing both major 2
all-fabric and major 3 split. No retired runtime is restored.

`python3 docs/traceability/gen_module_matrix.py` regenerated 15 outputs for 77
modules, with 5/5 controls, no archived or untested modules and no byte drift.
The generated module and leaf inventories still describe actual RTL/tests.
The requirement summary and MRP-6 row are hand-maintained authoritative inputs,
updated to trace the selectable implementation and Milan timing override.

## Contradiction search: method and every disposition

Searched all tracked root-repository Markdown files, including history and test
READMEs, using the four regular expressions below against exact committed blobs.
The census enumerates `git ls-tree -r --name-only` and reads `git show` at each
revision; matching line numbers are counted per query. Q1 to Q3 retain the
original ripgrep expressions, and Q4 audits the other changed requirement IDs. Gitlinks are not root
tracked files. Pinned donor implementation documentation remains evidence for
the supported all-fabric implementation, not a claim that split firmware exists.

- Q1: `NFR-SCOUT-0[123]`
- Q2: `never on firmware|fabric-only|fabric.only|no firmware round trip|never becomes a packet|all per-frame protocol`
- Q3: `(?i)(ADP|ACMP|AECP|MAAP|SRP|protocol control).{0,70}(fabric|processor)|(fabric|processor).{0,70}(ADP|ACMP|AECP|MAAP|SRP|protocol control)`
- Q4: `NFR-LAT-02|NFR-SCUP-0[24]|NFR-REL-02|FR-CTRL-04`

Base audit: 617 query/line records. Candidate audit: 644 records. A line can match more than one query.

E = corrected ownership or explicit current-shipping scope; H = dated evidence;
G = generated actual inventory; I = current implemented interface/test/provenance;
P = retained processor persistence or fabric-media contract; R = reset-domain term;
C = comparison of persistence designs. Retaining a hit does not erase its scope.

The two surviving "fabric-only" guide labels concern MAC-facing observations and
current shipping flow, both now explicitly scoped. The snapshot hits mean a reset
domain, and the materialization hit compares persistence architectures. None is
a blanket prohibition on the newly selected firmware control owner.

| File | Disposition and rationale |
|---|---|
| `CHANGELOG.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `QUICKSTART.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `README.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `REQUIREMENTS.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `THIRD_PARTY.md` | I: source dependency provenance and pinned processor responsibilities; not a restriction on future selectable placement. |
| `docs/AAF_LATENCY_TAPS.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/ENDSTATION_BUILDER.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/GLOSSARY.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/MILAN_V12_ROADMAP.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/design/MAAP_FABRIC.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/design/MAILBOX_SPLIT.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` | P: existing fabric media or processor persistence contract; retained for that implementation. Split ownership and F1 integration are specified separately. |
| `docs/design/SAVED_STATE_FASTCONNECT.md` | P: existing fabric media or processor persistence contract; retained for that implementation. Split ownership and F1 integration are specified separately. |
| `docs/design/SAVED_STATE_MATERIALIZATION.md` | P: processor saved-state design and pinned implementation evidence; remains valid for all-fabric, with split boot/apply assigned to the F1 contract. |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` | P: current processor persistence/reset boundary and pinned evidence; no prohibition on firmware control placement. |
| `docs/development/CODE_QUALITY.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/397_SERVICE_BUDGET.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/606_FIRST_BIND_MEASUREMENT.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/fpga/DATAPLANE_WALKTHROUGH.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/fpga/FPGA_DESIGN.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/history/v1/MVP_TALKER.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/NXN_ARCHITECTURE.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/SPEC_TRACEABILITY.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/design/GPTP_PLANE.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/design/MILAN_TALKER_SM.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/design/TIME_SYNC.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/findings/PP_SHADOW_AREA_0812.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/traceability/ieee1722-2016.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/traceability/ieee1722_1-2021.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/history/v1/traceability/milan-v12.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/integration/BAREMETAL_FIRMWARE.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/integration/BUILDING.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/integration/QSPI_FLASHBOOT.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/limitations/RECURRING_DEFECT_PATTERNS.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/limitations/TROUBLESHOOTING.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/overview/ARCHITECTURE.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/overview/FULL_FPGA_SOLUTION.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/reference/EGRESS_QUEUE_MAP.md` | I: current implemented CSR or egress interface; preserved unchanged because this lane does not implement the split or change VERSION. |
| `docs/reference/FR_NFR.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/reference/REGISTER_MAP.md` | I: current implemented CSR or egress interface; preserved unchanged because this lane does not implement the split or change VERSION. |
| `docs/reference/REGISTER_MAP_CLASSES.md` | I: current implemented CSR or egress interface; preserved unchanged because this lane does not implement the split or change VERSION. |
| `docs/reference/SUBMODULES.md` | I: source dependency provenance and pinned processor responsibilities; not a restriction on future selectable placement. |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/testing/SIMULATION.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/testing/TESTING.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/traceability/MODULE_MATRIX.md` | G: generated inventory of actual RTL and tests; regenerated byte-identically, not evidence that firmware integration exists. |
| `docs/traceability/ieee8021q.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `sw/builder/README-parameters.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `sw/firmware/ctrl/README.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `sw/firmware/nvm_hosttest/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `syn/yosys/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/avtp_parser/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/milan_dp/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/pp_shadow/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tests/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |

### Base hit ledger

| Query | Exact hit locator | Disposition |
|---|---|---|
| Q3 | `CHANGELOG.md:14` | H |
| Q3 | `CHANGELOG.md:474` | H |
| Q3 | `QUICKSTART.md:17` | I |
| Q3 | `QUICKSTART.md:266` | I |
| Q3 | `README.md:41` | E |
| Q3 | `README.md:42` | E |
| Q3 | `README.md:56` | E |
| Q3 | `README.md:364` | E |
| Q3 | `README.md:381` | E |
| Q3 | `README.md:423` | E |
| Q3 | `REQUIREMENTS.md:162` | E |
| Q3 | `THIRD_PARTY.md:19` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:64` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:182` | I |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:37` | E |
| Q2 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:38` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:5` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:17` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:42` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:135` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:138` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:221` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:222` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:568` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:989` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1005` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1029` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1031` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1039` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1044` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1046` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1123` | E |
| Q3 | `docs/GLOSSARY.md:29` | E |
| Q3 | `docs/GLOSSARY.md:30` | E |
| Q3 | `docs/GLOSSARY.md:79` | E |
| Q3 | `docs/MILAN_V12_ROADMAP.md:201` | I |
| Q3 | `docs/MILAN_V12_ROADMAP.md:467` | I |
| Q3 | `docs/design/MAAP_FABRIC.md:1` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:16` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:17` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:24` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:30` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:72` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:79` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:93` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:119` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:122` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:160` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:328` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:419` | E |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:102` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:150` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:213` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:275` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:278` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:279` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1265` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1266` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1269` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1275` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1295` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:119` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:121` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:416` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:1393` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:265` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:309` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:379` | P |
| Q2 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | C |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1558` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1797` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1882` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2394` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2395` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2407` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2410` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2412` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2413` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2414` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2415` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2416` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2419` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2424` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2617` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:883` | R |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1389` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1397` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1847` | R |
| Q3 | `docs/development/CODE_QUALITY.md:218` | I |
| Q3 | `docs/development/CODE_QUALITY.md:372` | I |
| Q3 | `docs/development/CODE_QUALITY.md:380` | I |
| Q3 | `docs/development/CODE_QUALITY.md:601` | I |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:18` | H |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76` | H |
| Q3 | `docs/findings/397_SERVICE_BUDGET.md:190` | H |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:108` | H |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:109` | H |
| Q3 | `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:218` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:554` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:737` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:738` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:740` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:741` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:746` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:747` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:750` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:751` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:752` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:753` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:757` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:758` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:812` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:813` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:814` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:815` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:816` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:817` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:818` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:819` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:820` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:821` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:822` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:823` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:824` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:825` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:826` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:828` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:829` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:832` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:833` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:834` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:835` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:836` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:837` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:839` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:840` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:971` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:980` | H |
| Q3 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:65` | H |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:41` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:47` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:79` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:89` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:91` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:195` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:17` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:20` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:21` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:27` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:29` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:110` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:151` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:305` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:342` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:353` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:354` | E |
| Q3 | `docs/history/v1/MVP_TALKER.md:28` | H |
| Q3 | `docs/history/v1/MVP_TALKER.md:58` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:28` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:31` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:36` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:84` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:135` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:411` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:462` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:494` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:496` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:630` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:711` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:772` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:23` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:26` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:56` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:108` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:112` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:246` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:286` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:287` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:289` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:325` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:354` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:358` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:438` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:444` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:524` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:531` | H |
| Q3 | `docs/history/v1/design/GPTP_PLANE.md:99` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:26` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:33` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:82` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:83` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:130` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:141` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:152` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:160` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:181` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:222` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:226` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:227` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:229` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:233` | H |
| Q3 | `docs/history/v1/design/TIME_SYNC.md:553` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:26` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:28` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:27` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:64` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:72` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:201` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:287` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:351` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:369` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:471` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:20` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:26` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:40` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:91` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:93` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:97` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:126` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:129` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:141` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:177` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:178` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:205` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:228` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:229` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:255` | H |
| Q1 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:274` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:276` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:279` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:304` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:33` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:40` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:41` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:47` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:49` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:134` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:156` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:189` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:191` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:192` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:199` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:213` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:214` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:217` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:221` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:223` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:224` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:225` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:226` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:227` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:230` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:239` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:244` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:268` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:269` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:270` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:279` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:284` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:357` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:363` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:370` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:371` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:373` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:375` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:378` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:380` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:390` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:391` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:395` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:416` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:417` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:19` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:195` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:206` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:19` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:77` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:78` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:87` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:88` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:89` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:90` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:91` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:110` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:220` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:252` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:268` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:269` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:270` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:271` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:273` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:332` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:342` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:343` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:344` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:345` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:346` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:351` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:355` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:359` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:360` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:361` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:374` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:387` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:24` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:35` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:112` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:113` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:118` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:262` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:28` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:57` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:59` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:68` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:107` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:133` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:47` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:53` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:58` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:87` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:97` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:98` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:104` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:115` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:116` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:117` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:118` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:119` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:120` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:121` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:122` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:123` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:124` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:125` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:126` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:127` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:128` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:129` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:130` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:141` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:156` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:157` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:158` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:159` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:160` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:161` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:162` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:163` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:164` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:167` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:168` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:169` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:174` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:179` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:184` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:241` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:242` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:243` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:244` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:245` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:246` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:249` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:255` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:275` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:279` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:283` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:289` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:290` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:79` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:156` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:157` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:158` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:159` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:172` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:173` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:174` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:175` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:176` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:177` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:179` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:183` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:193` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:194` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:195` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:201` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:202` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:203` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:204` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:205` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:206` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:207` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:208` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:210` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:216` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:217` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:218` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:225` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:226` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:227` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:265` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:271` | H |
| Q2 | `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:8` | E |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:221` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2030` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2163` | I |
| Q3 | `docs/integration/BUILDING.md:144` | I |
| Q3 | `docs/integration/QSPI_FLASHBOOT.md:52` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:334` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:338` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:94` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:151` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:816` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:914` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:978` | I |
| Q2 | `docs/overview/ARCHITECTURE.md:30` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:52` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:59` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:62` | E |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:48` | E |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:49` | E |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:9` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:28` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:127` | I |
| Q3 | `docs/reference/FR_NFR.md:13` | E |
| Q3 | `docs/reference/FR_NFR.md:14` | E |
| Q3 | `docs/reference/FR_NFR.md:28` | E |
| Q3 | `docs/reference/FR_NFR.md:47` | E |
| Q2 | `docs/reference/FR_NFR.md:71` | E |
| Q3 | `docs/reference/FR_NFR.md:98` | E |
| Q3 | `docs/reference/FR_NFR.md:102` | E |
| Q3 | `docs/reference/FR_NFR.md:145` | E |
| Q4 | `docs/reference/FR_NFR.md:148` | E |
| Q3 | `docs/reference/FR_NFR.md:151` | E |
| Q3 | `docs/reference/FR_NFR.md:153` | E |
| Q3 | `docs/reference/FR_NFR.md:154` | E |
| Q3 | `docs/reference/FR_NFR.md:160` | E |
| Q4 | `docs/reference/FR_NFR.md:162` | E |
| Q3 | `docs/reference/FR_NFR.md:165` | E |
| Q4 | `docs/reference/FR_NFR.md:187` | E |
| Q4 | `docs/reference/FR_NFR.md:286` | E |
| Q4 | `docs/reference/FR_NFR.md:300` | E |
| Q4 | `docs/reference/FR_NFR.md:302` | E |
| Q1 | `docs/reference/FR_NFR.md:307` | E |
| Q1 | `docs/reference/FR_NFR.md:308` | E |
| Q3 | `docs/reference/FR_NFR.md:308` | E |
| Q1 | `docs/reference/FR_NFR.md:309` | E |
| Q2 | `docs/reference/FR_NFR.md:309` | E |
| Q4 | `docs/reference/FR_NFR.md:320` | E |
| Q3 | `docs/reference/FR_NFR.md:342` | E |
| Q2 | `docs/reference/FR_NFR.md:349` | E |
| Q3 | `docs/reference/FR_NFR.md:359` | E |
| Q3 | `docs/reference/FR_NFR.md:410` | E |
| Q3 | `docs/reference/FR_NFR.md:447` | E |
| Q3 | `docs/reference/FR_NFR.md:448` | E |
| Q3 | `docs/reference/FR_NFR.md:451` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:62` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:89` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:93` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:117` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:144` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:260` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:261` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:265` | E |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:90` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:93` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:96` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:249` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:18` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:20` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:23` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:25` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:124` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:174` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:191` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:192` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:193` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:224` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:226` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:363` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:789` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:790` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:950` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:960` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:975` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:994` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:996` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1008` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1013` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1017` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1018` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1020` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1025` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1027` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1029` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1051` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1054` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1067` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1082` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1083` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1084` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1092` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1117` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1120` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1188` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1189` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1190` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1193` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1248` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1252` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1265` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1277` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1525` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1544` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1553` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1554` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1648` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1668` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1698` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:2373` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:12` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:55` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:84` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:85` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:89` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:90` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:91` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:93` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:98` | I |
| Q3 | `docs/reference/SUBMODULES.md:25` | I |
| Q3 | `docs/reference/SUBMODULES.md:35` | I |
| Q3 | `docs/reference/SUBMODULES.md:97` | I |
| Q3 | `docs/reference/SUBMODULES.md:98` | I |
| Q3 | `docs/reference/SUBMODULES.md:99` | I |
| Q3 | `docs/reference/SUBMODULES.md:132` | I |
| Q3 | `docs/reference/SUBMODULES.md:134` | I |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:67` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:171` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:175` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:243` | H |
| Q3 | `docs/testing/SIMULATION.md:38` | I |
| Q3 | `docs/testing/TESTING.md:25` | I |
| Q3 | `docs/testing/TESTING.md:273` | I |
| Q3 | `docs/testing/TESTING.md:445` | I |
| Q3 | `docs/testing/TESTING.md:517` | I |
| Q3 | `docs/testing/TESTING.md:532` | I |
| Q3 | `docs/testing/TESTING.md:1173` | I |
| Q3 | `docs/testing/TESTING.md:1227` | I |
| Q3 | `docs/traceability/MODULE_MATRIX.md:52` | G |
| Q3 | `docs/traceability/MODULE_MATRIX.md:106` | G |
| Q3 | `docs/traceability/ieee8021q.md:29` | E |
| Q3 | `docs/traceability/ieee8021q.md:33` | E |
| Q3 | `docs/traceability/ieee8021q.md:48` | E |
| Q3 | `docs/traceability/ieee8021q.md:79` | E |
| Q3 | `docs/traceability/ieee8021q.md:81` | E |
| Q3 | `docs/traceability/ieee8021q.md:82` | E |
| Q3 | `docs/traceability/ieee8021q.md:96` | E |
| Q3 | `docs/traceability/ieee8021q.md:97` | E |
| Q3 | `docs/traceability/ieee8021q.md:98` | E |
| Q3 | `docs/traceability/ieee8021q.md:99` | E |
| Q3 | `docs/traceability/ieee8021q.md:119` | E |
| Q3 | `docs/traceability/ieee8021q.md:120` | E |
| Q3 | `docs/traceability/ieee8021q.md:121` | E |
| Q3 | `docs/traceability/ieee8021q.md:122` | E |
| Q3 | `docs/traceability/ieee8021q.md:123` | E |
| Q3 | `docs/traceability/ieee8021q.md:124` | E |
| Q3 | `docs/traceability/ieee8021q.md:125` | E |
| Q3 | `docs/traceability/ieee8021q.md:132` | E |
| Q3 | `docs/traceability/ieee8021q.md:133` | E |
| Q3 | `docs/traceability/ieee8021q.md:134` | E |
| Q3 | `docs/traceability/ieee8021q.md:135` | E |
| Q3 | `docs/traceability/ieee8021q.md:136` | E |
| Q3 | `docs/traceability/ieee8021q.md:137` | E |
| Q3 | `docs/traceability/ieee8021q.md:138` | E |
| Q3 | `docs/traceability/ieee8021q.md:139` | E |
| Q3 | `docs/traceability/ieee8021q.md:141` | E |
| Q3 | `docs/traceability/ieee8021q.md:149` | E |
| Q3 | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3` | I |
| Q3 | `sw/builder/README-parameters.md:210` | I |
| Q3 | `sw/firmware/ctrl/README.md:18` | E |
| Q3 | `sw/firmware/ctrl/README.md:46` | E |
| Q3 | `sw/firmware/ctrl/README.md:47` | E |
| Q3 | `sw/firmware/ctrl/README.md:49` | E |
| Q3 | `sw/firmware/ctrl/README.md:54` | E |
| Q3 | `sw/firmware/nvm_hosttest/README.md:101` | I |
| Q3 | `syn/yosys/README.md:312` | I |
| Q3 | `tb/verilator/README.md:105` | I |
| Q3 | `tb/verilator/avtp_parser/README.md:17` | I |
| Q3 | `tb/verilator/milan_dp/README.md:75` | I |
| Q3 | `tb/verilator/milan_dp/README.md:76` | I |
| Q3 | `tb/verilator/milan_dp/README.md:428` | I |
| Q3 | `tb/verilator/milan_dp/README.md:630` | I |
| Q3 | `tb/verilator/milan_dp/README.md:632` | I |
| Q3 | `tb/verilator/milan_dp/README.md:634` | I |
| Q3 | `tb/verilator/milan_dp/README.md:647` | I |
| Q3 | `tb/verilator/milan_dp/README.md:653` | I |
| Q3 | `tb/verilator/milan_dp/README.md:907` | I |
| Q3 | `tb/verilator/milan_dp/README.md:938` | I |
| Q3 | `tb/verilator/milan_dp/README.md:944` | I |
| Q3 | `tb/verilator/milan_dp/README.md:954` | I |
| Q3 | `tb/verilator/milan_dp/README.md:964` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:14` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:81` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:120` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:138` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:144` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:145` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:146` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:167` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:171` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:332` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:371` | I |
| Q3 | `tests/README.md:10` | I |
| Q3 | `tests/README.md:23` | I |
| Q3 | `tests/README.md:53` | I |
| Q3 | `tests/README.md:54` | I |
| Q3 | `tests/README.md:151` | I |

### Candidate hit ledger

| Query | Exact hit locator | Disposition |
|---|---|---|
| Q3 | `CHANGELOG.md:14` | H |
| Q3 | `CHANGELOG.md:474` | H |
| Q3 | `QUICKSTART.md:17` | I |
| Q3 | `QUICKSTART.md:266` | I |
| Q3 | `README.md:41` | E |
| Q3 | `README.md:42` | E |
| Q3 | `README.md:56` | E |
| Q3 | `README.md:372` | E |
| Q3 | `README.md:389` | E |
| Q3 | `README.md:431` | E |
| Q1 | `REQUIREMENTS.md:44` | E |
| Q3 | `REQUIREMENTS.md:184` | E |
| Q3 | `THIRD_PARTY.md:19` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:64` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:182` | I |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:41` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:42` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:43` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:44` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:45` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:54` | E |
| Q1 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:60` | E |
| Q1 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:214` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:10` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:22` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:47` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:140` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:143` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:226` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:227` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:573` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:994` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1010` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1034` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1036` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1044` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1049` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1051` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1128` | E |
| Q3 | `docs/GLOSSARY.md:79` | E |
| Q3 | `docs/MILAN_V12_ROADMAP.md:201` | I |
| Q3 | `docs/MILAN_V12_ROADMAP.md:467` | I |
| Q3 | `docs/design/MAAP_FABRIC.md:1` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:23` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:24` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:31` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:37` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:79` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:86` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:100` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:126` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:129` | E |
| Q3 | `docs/design/MAAP_FABRIC.md:167` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:332` | E |
| Q1 | `docs/design/MAILBOX_SPLIT.md:361` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:442` | E |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:102` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:150` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:213` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:275` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:278` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:279` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1265` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1266` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1269` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1275` | P |
| Q3 | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1295` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:119` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:121` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:416` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:1393` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:265` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:309` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:379` | P |
| Q2 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | C |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1558` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1797` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1882` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2394` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2395` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2407` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2410` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2412` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2413` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2414` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2415` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2416` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2419` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2424` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2617` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:883` | R |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1389` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1397` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1847` | R |
| Q3 | `docs/development/CODE_QUALITY.md:218` | I |
| Q3 | `docs/development/CODE_QUALITY.md:372` | I |
| Q3 | `docs/development/CODE_QUALITY.md:380` | I |
| Q3 | `docs/development/CODE_QUALITY.md:601` | I |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:18` | H |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76` | H |
| Q3 | `docs/findings/397_SERVICE_BUDGET.md:190` | H |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:108` | H |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:109` | H |
| Q3 | `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:218` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:554` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:737` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:738` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:740` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:741` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:746` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:747` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:750` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:751` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:752` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:753` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:757` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:758` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:812` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:813` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:814` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:815` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:816` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:817` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:818` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:819` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:820` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:821` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:822` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:823` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:824` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:825` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:826` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:828` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:829` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:832` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:833` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:834` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:835` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:836` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:837` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:839` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:840` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:971` | H |
| Q3 | `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:980` | H |
| Q3 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:65` | H |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:48` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:54` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:86` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:96` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:98` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:202` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:24` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:27` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:28` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:34` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:36` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:117` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:158` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:312` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:349` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:360` | E |
| Q3 | `docs/fpga/FPGA_DESIGN.md:361` | E |
| Q3 | `docs/history/v1/MVP_TALKER.md:28` | H |
| Q3 | `docs/history/v1/MVP_TALKER.md:58` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:28` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:31` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:36` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:84` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:135` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:411` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:462` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:494` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:496` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:630` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:711` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:772` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:23` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:26` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:56` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:108` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:112` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:246` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:286` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:287` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:289` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:325` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:354` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:358` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:438` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:444` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:524` | H |
| Q3 | `docs/history/v1/SPEC_TRACEABILITY.md:531` | H |
| Q3 | `docs/history/v1/design/GPTP_PLANE.md:99` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:26` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:33` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:82` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:83` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:130` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:141` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:152` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:160` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:181` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:222` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:226` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:227` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:229` | H |
| Q3 | `docs/history/v1/design/MILAN_TALKER_SM.md:233` | H |
| Q3 | `docs/history/v1/design/TIME_SYNC.md:553` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:26` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:28` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:27` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:64` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:72` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:201` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:287` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:351` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:369` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:471` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:20` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:26` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:40` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:91` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:93` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:97` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:126` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:129` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:141` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:177` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:178` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:205` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:228` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:229` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:255` | H |
| Q1 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:274` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:276` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:279` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:304` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:33` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:40` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:41` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:47` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:49` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:134` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:156` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:189` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:191` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:192` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:199` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:213` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:214` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:217` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:221` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:223` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:224` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:225` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:226` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:227` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:230` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:239` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:244` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:268` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:269` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:270` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:279` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:284` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:357` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:363` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:370` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:371` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:373` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:375` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:378` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:380` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:390` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:391` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:395` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:416` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:417` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:19` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:195` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:206` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:19` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:77` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:78` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:87` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:88` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:89` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:90` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:91` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:110` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:220` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:252` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:268` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:269` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:270` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:271` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:273` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:332` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:342` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:343` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:344` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:345` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:346` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:351` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:355` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:359` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:360` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:361` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:374` | H |
| Q3 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:387` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:24` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:35` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:112` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:113` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:118` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:262` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:28` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:57` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:59` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:68` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:107` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:133` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:47` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:53` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:58` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:87` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:97` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:98` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:104` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:115` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:116` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:117` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:118` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:119` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:120` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:121` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:122` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:123` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:124` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:125` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:126` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:127` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:128` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:129` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:130` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:141` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:156` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:157` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:158` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:159` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:160` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:161` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:162` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:163` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:164` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:167` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:168` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:169` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:174` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:179` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:184` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:241` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:242` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:243` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:244` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:245` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:246` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:249` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:255` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:275` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:279` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:283` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:289` | H |
| Q3 | `docs/history/v1/traceability/ieee1722_1-2021.md:290` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:79` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:156` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:157` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:158` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:159` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:172` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:173` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:174` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:175` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:176` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:177` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:179` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:183` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:193` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:194` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:195` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:201` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:202` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:203` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:204` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:205` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:206` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:207` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:208` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:210` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:216` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:217` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:218` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:225` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:226` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:227` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:265` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:271` | H |
| Q2 | `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:8` | E |
| Q1 | `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:36` | E |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:221` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2030` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2163` | I |
| Q3 | `docs/integration/BUILDING.md:144` | I |
| Q3 | `docs/integration/QSPI_FLASHBOOT.md:52` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:334` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:338` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:94` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:151` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:816` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:914` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:978` | I |
| Q2 | `docs/overview/ARCHITECTURE.md:37` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:59` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:66` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:69` | E |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:54` | E |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:55` | E |
| Q1 | `docs/overview/FULL_FPGA_SOLUTION.md:97` | E |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:9` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:28` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:127` | I |
| Q3 | `docs/reference/FR_NFR.md:14` | E |
| Q3 | `docs/reference/FR_NFR.md:28` | E |
| Q3 | `docs/reference/FR_NFR.md:47` | E |
| Q3 | `docs/reference/FR_NFR.md:112` | E |
| Q3 | `docs/reference/FR_NFR.md:116` | E |
| Q3 | `docs/reference/FR_NFR.md:159` | E |
| Q4 | `docs/reference/FR_NFR.md:162` | E |
| Q3 | `docs/reference/FR_NFR.md:165` | E |
| Q3 | `docs/reference/FR_NFR.md:167` | E |
| Q3 | `docs/reference/FR_NFR.md:168` | E |
| Q3 | `docs/reference/FR_NFR.md:174` | E |
| Q4 | `docs/reference/FR_NFR.md:176` | E |
| Q3 | `docs/reference/FR_NFR.md:179` | E |
| Q4 | `docs/reference/FR_NFR.md:201` | E |
| Q1 | `docs/reference/FR_NFR.md:300` | E |
| Q4 | `docs/reference/FR_NFR.md:300` | E |
| Q1 | `docs/reference/FR_NFR.md:314` | E |
| Q4 | `docs/reference/FR_NFR.md:314` | E |
| Q3 | `docs/reference/FR_NFR.md:316` | E |
| Q4 | `docs/reference/FR_NFR.md:316` | E |
| Q1 | `docs/reference/FR_NFR.md:321` | E |
| Q1 | `docs/reference/FR_NFR.md:322` | E |
| Q3 | `docs/reference/FR_NFR.md:322` | E |
| Q1 | `docs/reference/FR_NFR.md:323` | E |
| Q1 | `docs/reference/FR_NFR.md:402` | E |
| Q1 | `docs/reference/FR_NFR.md:403` | E |
| Q1 | `docs/reference/FR_NFR.md:404` | E |
| Q4 | `docs/reference/FR_NFR.md:404` | E |
| Q4 | `docs/reference/FR_NFR.md:405` | E |
| Q1 | `docs/reference/FR_NFR.md:406` | E |
| Q1 | `docs/reference/FR_NFR.md:407` | E |
| Q4 | `docs/reference/FR_NFR.md:407` | E |
| Q1 | `docs/reference/FR_NFR.md:408` | E |
| Q1 | `docs/reference/FR_NFR.md:409` | E |
| Q3 | `docs/reference/FR_NFR.md:409` | E |
| Q3 | `docs/reference/FR_NFR.md:434` | E |
| Q4 | `docs/reference/FR_NFR.md:448` | E |
| Q3 | `docs/reference/FR_NFR.md:539` | E |
| Q1 | `docs/reference/FR_NFR.md:576` | E |
| Q3 | `docs/reference/FR_NFR.md:576` | E |
| Q1 | `docs/reference/FR_NFR.md:577` | E |
| Q3 | `docs/reference/FR_NFR.md:577` | E |
| Q4 | `docs/reference/FR_NFR.md:577` | E |
| Q1 | `docs/reference/FR_NFR.md:579` | E |
| Q3 | `docs/reference/FR_NFR.md:579` | E |
| Q4 | `docs/reference/FR_NFR.md:579` | E |
| Q1 | `docs/reference/FR_NFR.md:580` | E |
| Q3 | `docs/reference/FR_NFR.md:580` | E |
| Q4 | `docs/reference/FR_NFR.md:585` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:67` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:94` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:98` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:122` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:149` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:265` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:266` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:270` | E |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:90` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:93` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:96` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:249` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:18` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:20` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:23` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:25` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:124` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:174` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:191` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:192` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:193` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:224` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:226` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:363` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:789` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:790` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:950` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:960` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:975` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:994` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:996` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1008` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1013` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1017` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1018` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1020` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1025` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1027` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1029` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1051` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1054` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1067` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1082` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1083` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1084` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1092` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1117` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1120` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1188` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1189` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1190` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1193` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1248` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1252` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1265` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1277` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1525` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1544` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1553` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1554` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1648` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1668` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:1698` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:2373` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:12` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:55` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:84` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:85` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:89` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:90` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:91` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:93` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:98` | I |
| Q3 | `docs/reference/SUBMODULES.md:25` | I |
| Q3 | `docs/reference/SUBMODULES.md:35` | I |
| Q3 | `docs/reference/SUBMODULES.md:97` | I |
| Q3 | `docs/reference/SUBMODULES.md:98` | I |
| Q3 | `docs/reference/SUBMODULES.md:99` | I |
| Q3 | `docs/reference/SUBMODULES.md:132` | I |
| Q3 | `docs/reference/SUBMODULES.md:134` | I |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:67` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:171` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:175` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:243` | H |
| Q3 | `docs/testing/SIMULATION.md:38` | I |
| Q3 | `docs/testing/TESTING.md:25` | I |
| Q3 | `docs/testing/TESTING.md:273` | I |
| Q3 | `docs/testing/TESTING.md:445` | I |
| Q3 | `docs/testing/TESTING.md:517` | I |
| Q3 | `docs/testing/TESTING.md:532` | I |
| Q3 | `docs/testing/TESTING.md:1173` | I |
| Q3 | `docs/testing/TESTING.md:1227` | I |
| Q3 | `docs/traceability/MODULE_MATRIX.md:52` | G |
| Q3 | `docs/traceability/MODULE_MATRIX.md:106` | G |
| Q3 | `docs/traceability/ieee8021q.md:35` | E |
| Q3 | `docs/traceability/ieee8021q.md:39` | E |
| Q3 | `docs/traceability/ieee8021q.md:54` | E |
| Q3 | `docs/traceability/ieee8021q.md:85` | E |
| Q3 | `docs/traceability/ieee8021q.md:87` | E |
| Q3 | `docs/traceability/ieee8021q.md:88` | E |
| Q3 | `docs/traceability/ieee8021q.md:102` | E |
| Q3 | `docs/traceability/ieee8021q.md:103` | E |
| Q3 | `docs/traceability/ieee8021q.md:104` | E |
| Q3 | `docs/traceability/ieee8021q.md:105` | E |
| Q1 | `docs/traceability/ieee8021q.md:119` | E |
| Q3 | `docs/traceability/ieee8021q.md:133` | E |
| Q3 | `docs/traceability/ieee8021q.md:134` | E |
| Q3 | `docs/traceability/ieee8021q.md:135` | E |
| Q3 | `docs/traceability/ieee8021q.md:136` | E |
| Q3 | `docs/traceability/ieee8021q.md:137` | E |
| Q1 | `docs/traceability/ieee8021q.md:138` | E |
| Q3 | `docs/traceability/ieee8021q.md:138` | E |
| Q3 | `docs/traceability/ieee8021q.md:139` | E |
| Q3 | `docs/traceability/ieee8021q.md:146` | E |
| Q3 | `docs/traceability/ieee8021q.md:147` | E |
| Q3 | `docs/traceability/ieee8021q.md:148` | E |
| Q3 | `docs/traceability/ieee8021q.md:149` | E |
| Q3 | `docs/traceability/ieee8021q.md:150` | E |
| Q3 | `docs/traceability/ieee8021q.md:151` | E |
| Q3 | `docs/traceability/ieee8021q.md:152` | E |
| Q3 | `docs/traceability/ieee8021q.md:153` | E |
| Q3 | `docs/traceability/ieee8021q.md:155` | E |
| Q3 | `docs/traceability/ieee8021q.md:163` | E |
| Q3 | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3` | I |
| Q3 | `sw/builder/README-parameters.md:210` | I |
| Q3 | `sw/firmware/ctrl/README.md:25` | E |
| Q3 | `sw/firmware/ctrl/README.md:53` | E |
| Q3 | `sw/firmware/ctrl/README.md:54` | E |
| Q3 | `sw/firmware/ctrl/README.md:56` | E |
| Q3 | `sw/firmware/ctrl/README.md:61` | E |
| Q3 | `sw/firmware/nvm_hosttest/README.md:101` | I |
| Q3 | `syn/yosys/README.md:312` | I |
| Q3 | `tb/verilator/README.md:105` | I |
| Q3 | `tb/verilator/avtp_parser/README.md:17` | I |
| Q3 | `tb/verilator/milan_dp/README.md:75` | I |
| Q3 | `tb/verilator/milan_dp/README.md:76` | I |
| Q3 | `tb/verilator/milan_dp/README.md:428` | I |
| Q3 | `tb/verilator/milan_dp/README.md:630` | I |
| Q3 | `tb/verilator/milan_dp/README.md:632` | I |
| Q3 | `tb/verilator/milan_dp/README.md:634` | I |
| Q3 | `tb/verilator/milan_dp/README.md:647` | I |
| Q3 | `tb/verilator/milan_dp/README.md:653` | I |
| Q3 | `tb/verilator/milan_dp/README.md:907` | I |
| Q3 | `tb/verilator/milan_dp/README.md:938` | I |
| Q3 | `tb/verilator/milan_dp/README.md:944` | I |
| Q3 | `tb/verilator/milan_dp/README.md:954` | I |
| Q3 | `tb/verilator/milan_dp/README.md:964` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:14` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:81` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:120` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:138` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:144` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:145` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:146` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:167` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:171` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:332` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:371` | I |
| Q3 | `tests/README.md:10` | I |
| Q3 | `tests/README.md:23` | I |
| Q3 | `tests/README.md:53` | I |
| Q3 | `tests/README.md:54` | I |
| Q3 | `tests/README.md:151` | I |

## Gate table and environment

All final commands must name the candidate head in their log header.
The full docs workflow is the union of the bank and D entries, plus imported
and no-git checks. Independent processes run concurrently with individual logs
and rc files; no test output is piped. Vendor analysis is explicitly skipped. Builder gate 11 calibration has no
verdict because the historical mf48 placement-utilization report is absent.
The exact-head builder result and elapsed time are recorded with B48.
Its final receipt, rather than a prior-head run, supplies validation evidence.
The long process ran in the background while foreground waits stayed under a minute.
No runtime simulation build, synthesis, board or bench operation is performed.

Round 2 reused the scratch Python environment populated from both hash-locked
files, plus PyYAML and wavedrom 2.0.3.post3. Verilator is 5.050; sv2v is pinned 0.0.12.
The builder uses the existing canonical RV32 GCC 14.3.0 selector and LiteX
environment. The repository installer re-verified the separate pinned SDK cache; its
receipt reports a verified cache hit. No new SDK installation was needed.
No shared SDK was changed. The existing SDK lacks the installer's provenance
receipt, so it was not retroactively labelled as a verified pinned install.

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


Round 2 uses fresh log, reference-output and metadata-free export directories.
Earlier-head results are not substituted for this committed-head bank.
At `ff6d673ccf32136be0d0daeabe4188358b84041a`, B19 returned 1 for the new
raw-HTML fragment; N01 returned 1 because an archive lacks imported files.
B48 and D24 were interrupted (rc -2) before the candidate correction.
A heading-anchor correction passed B19, but retained the archive dependency.
A plain imported pathname then failed the tracked-file dead-reference gate.
The final text cites the normative table directly. The extract is recorded
in this handoff, without making a downloaded archive require submodule files.
The gates and their acceptance criteria are unchanged. The full bank was
restarted at the final committed head; superseded receipts remain in scratch.

Round-2 preliminary checks: style, contents and traceability regeneration passed.
Regeneration changed no generated output. The final bank repeats applicable
checks against the committed candidate. No gate or acceptance criterion changed.

## Final integrity checks

The final audit checks exact tracked bytes and modes, index entries and flags,
required submodule pins, the docs-only scope and unchanged VERSION sources.
It also checks exact owner-approval text, all round-2 changed rows, the complete
contradiction census, output privacy and size, and the live remote base.
All seven final audit commands returned zero.
The results and reproducible commands are recorded in `final-audits.json`;
`final-audits.log` records their output. Both have receipts below.

## Artifact receipts

Logs, SDKs, parser packages, text extractions and exported trees remain in
scratch. Large artifacts are recorded by size and SHA-256, not copied here.
`CHECK_ROOT` below denotes `round2` under the assigned scratch directory.
`DEPS_ROOT` denotes the reusable dependency directory one level above it.

| Artifact relative to CHECK_ROOT, unless marked standard | Bytes | SHA-256 |
|---|---:|---|
| `scope-version.json` | 2462 | `5f8041b38b320e1245261c847b14ceaa89f8cf5624c796d95375479170d6ef26` |
| `contradiction-base.json` | 297969 | `075c4730266f56802925357456519a52d17a40552f655162584cd58408c43272` |
| `contradiction-head.json` | 310068 | `abd6ee2b3309c2abd7de906e7188d06730b3337ca58a0d7960b3baa34cb9f11b` |
| `manifest.json` | 11267 | `32445135f2b965bc21fd11fb892cb0d3a75f96b879452be4dddf082e82aff867` |
| `gates-complete.json` | 14439 | `704e96bb0666f5d566cc3b17f8bbcc655fabb830bd8056d71e84b125b6d6d1cc` |
| `head.tar` | 32890880 | `c7fa77e374870b430cb05c672d60e38bb5a49db9d39316a2db594bc52fcc9b85` |
| `reused-dependencies/sv2v-v0.0.12.zip` | 2168551 | `ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00` |
| `reused-dependencies/rv32-present.jsonl` | 1718427 | `2cac09adbb83ab60bb0abd808d857fea237af40e0a9b42013c294e4a3a1eb9ad` |
| `rv32-absent.jsonl` | 2133 | `e4d608270e9168259121d1f55d3d6b4a7d47c161924ac0792afe7b01bf71c129` |
| `hdl-reference/index.html` | 1259098 | `2e052f82f308f51015c6b1c7a1bfc87fc6e5995a8d13c86a288688159ebc4297` |
| `check_approval.py` | 2197 | `aac31307d34b0c3864daaef4f7ac66b2e634054b2ef557ff006240e8e56c2573` |
| `check_round2_approval.py` | 1586 | `9f46eb8015a72c7ef2007f58a171e1a7c9ccc37bea50cbc7a4cd3b39534aa8ad` |
| `check_sweep.py` | 2042 | `ef98db11ef877c2dd7160e677edc0b17b497f35f989808a97b376833f3c5fa4e` |
| `verify_tree.py` | 3273 | `a0752aa491a623acd3b48e6873f356963ad43362d7b16bf2055a77c5af57766b` |
| `check_final_state.py` | 1970 | `0fe8790f352390a5fed5cd27ac3ddc9acfba0a15076c1e30b73853ccb5e1257c` |
| `check_delivery.py` | 765 | `1ad2200bfa456c7850a571b444d944eddc01b81bb49976468568991eee35952a` |
| `run_final_audits.py` | 1452 | `b1e69fb14bd07361bfd1455a49d9f70c322cac4b659f6e5b26e8ae2969331510` |
| `final-audits.log` | 4233 | `d55a6743ffd67a6a83345a815fdf1f89fee49aa398f0019959610305570c3139` |
| `final-audits.json` | 1761 | `7e27f584f701ff16368276e1eddb9dd484f99f50d81761ece809ec1cf2323719` |
| `gates/B01.log` | 3792 | `a54dd6c043ea27a8c8c8bdd389d84e6217c2b52c5cc8f88e007473d04d8a78d5` |
| `gates/B02.log` | 1156 | `eed31ae92bf063de4aa194b304cefcb446619f1cddee17942c47704fd1d0a670` |
| `gates/B03.log` | 15091 | `829f862c7ee3fe602020c25817584c23517a66da4962430533e97d3efebcfbd8` |
| `gates/B04.log` | 1464 | `27d41b4138d26075e80cfc3c9342341c596a1f0be5ffef686ad156186d8bed85` |
| `gates/B05.log` | 356 | `0e43ac42148249319283f6caf833391091a225c9d90f43d45762a6b4d762f4ac` |
| `gates/B06.log` | 6708 | `a99f1b78fdd15ebb4182954bd1984e1253bca888f99f32ae6b386f33231e7dcd` |
| `gates/B07.log` | 142482 | `5165a2e4d9f4b2368aa6eb01e5771c547d9451d3aebe8d33082ff23795919b16` |
| `gates/B08.log` | 325 | `c504c36f80b9100dc5b4c69ca126f02c8f8af15fc03d5cc84dd839780ae373fa` |
| `gates/B09.log` | 218 | `f53664494b610bc903071809b0c6e2a3f0c27f1c6d826884e7d8c43fa7fd36c4` |
| `gates/B10.log` | 236 | `be7dbb78678fb76ace02c346aa6eba6023d637136061f2e0b7cf338d9a55e787` |
| `gates/B11.log` | 499 | `e051f66d6b5f394672d880adfc5cc979676bb9c45e42df08f196778e6426d342` |
| `gates/B12.log` | 644 | `d85c10bd0fdb1db022fd63dd697c8e7f35c324abfd6f62bcae4d406f2a6141f5` |
| `gates/B13.log` | 307 | `ae2fad8549c848ea4a3525fb16e1435d101e0602051f2642355d6bd8faaf4c25` |
| `gates/B14.log` | 231 | `07abbdd651a834d0d283719346c661c11a4b4b39cb33bd87459f3f13d5e478f3` |
| `gates/B15.log` | 231 | `69e9816bf2ce876d6a97dca67ca17480bd329cf7a20ac262c98e49b3690a6d63` |
| `gates/B16.log` | 275 | `c345550b1203dc83156af04825dda2bb6072ec318f829e92701bc9d58713a2e7` |
| `gates/B17.log` | 269 | `7c6d51d47fe330c9f68e02d7848d2abf31abcf16942846afb1190c2894dcec37` |
| `gates/B18.log` | 275 | `3c7217c2611070ab480de1879c02fa0da2a387ec4eb7ec7930b8d14cdfda5edc` |
| `gates/B19.log` | 260 | `27da03278f493c67ae09395343fe5592b3778b1b1afe62519c195219e794fb56` |
| `gates/B20.log` | 281 | `c74e85f6c87dd1ca4a62dbc196626558e620e411624acee71147d30f2726cada` |
| `gates/B21.log` | 2191 | `dd97289e894acdef7e8058be381bdaeaee5eb7817fb78f2cf8bd70a13d715fe3` |
| `gates/B22.log` | 350 | `158fc5f067ca032c38945b67e7996fa9cb74e4c6541ce3c9d22e96ae3126c9c6` |
| `gates/B23.log` | 401 | `7230c375c409e5bd2be3fef818bf48d3bd9ace1b04493db3bd716e8cc6a2bba2` |
| `gates/B24.log` | 418 | `ee3ff7298c190fb128f88e0c9bbb4a28eca7e6aef89da153abe664ef285093da` |
| `gates/B25.log` | 344 | `711ce070ef2c12fbfafc8756e4426f9bd650d18c77a876bdce81b2965a8f469f` |
| `gates/B26.log` | 271 | `e19a9b70a2d0184b1322035bdf7216f4580fda5912c854cbe0636bffd74b2a22` |
| `gates/B27.log` | 610 | `2edb3757d9680fafdef2ad7ce574f1a978e264394c15d2eec5cc110f5ee9559e` |
| `gates/B28.log` | 2769 | `04120cfda54d073dac5b9863d431900a430ddd8fc89e1dffc4c2e2b8045284a0` |
| `gates/B29.log` | 272 | `ee4822995bbe333de0fb5e110e6eecec04cff02c0ce28534c66f754e65e47165` |
| `gates/B30.log` | 246 | `9c1a1a0a9cd6875e88ecc1de659d983de8b5764bcab09e9c06861d3975499821` |
| `gates/B31.log` | 5407 | `3ab6ac70f748331bf2248f4ea7962b0f71752767d95d0ccfa996232c3d684ff6` |
| `gates/B32.log` | 19895 | `ef9cf3d3ffc658df8c0fcab693e3ff744b40ae74896267e862a2588b9788a3dd` |
| `gates/B33.log` | 738 | `7a6a2f81c1992e571bee8b070542f2a2cf247c2da372eb6cfb4b6c5a77a95d1d` |
| `gates/B34.log` | 2768 | `8030e23437538f4d3ce8198df27f5275be3ad33a72a40c1754050dcaef08cf34` |
| `gates/B35.log` | 927 | `5154428a1dba715d2e560a6421e185859775c439c41f5c6af744c4b555056d2c` |
| `gates/B36.log` | 377 | `6d564ed4bf74071f6b82ee0644a3034fa1295c07d961c178f3ff66540f874c61` |
| `gates/B37.log` | 6282 | `40d1b59ebd167bc725fcf703c7242d56c4aea61dca737d2ac63907643d1955ea` |
| `gates/B38.log` | 14427 | `ed482a24ba509b7d06e910d7c51b9f67d34a7237f54bb4675d9335fa799adb20` |
| `gates/B39.log` | 36802 | `29280bd6b1f7d98b1c5e9524717e38802c686aed245ee5b7142371b3afe01f22` |
| `gates/B40.log` | 5863 | `d3bc9db61016fc3e4961389dfca89b8a1c6cd62ed05ba9aaf23cf984f4c685b5` |
| `gates/B41.log` | 228 | `712133586afc5cd4d7e4da7e808427e3901ca34480d5afc221880f535f53c9e1` |
| `gates/B42.log` | 238 | `2168345fc5ab76cef697612f51c5a68578caf5de69914ee84cd6f6f72a6d7c67` |
| `gates/B43.log` | 249 | `b75299d34b9e2fd6a4de91893b0174b0f470da875ce63d10cfc9312d4199b154` |
| `gates/B44.log` | 220 | `a75ae5ba308a77b7dd815d4cdd657853aa0811b63b89039031ed72d0418b1a57` |
| `gates/B45.log` | 5174 | `694c5c5a6b89c926e8cd5a511e23f6f66c00e9c350fe2033163a544c4df81574` |
| `gates/B46.log` | 25899 | `aa2bde117b261640f07d5623812445e76e04ba867131e5047abc2f394a8174f0` |
| `gates/B47.log` | 9478 | `b48f262111209363b5d08c6bbe42ba6ff2822c97927edeb416e54abe4f5a53e6` |
| `gates/B48.log` | 102484 | `698fa271ff4fddbc964a2294a3850b7781643f86eacf96100b3c4409b8980aca` |
| `gates/D01.log` | 621 | `dd7d7b11578b7b74c85ed18005953aab2ae5d452b2739b434fcd027335544e18` |
| `gates/D02.log` | 652 | `ecdd376d4b8018a7a2d680ef30126849677ee6cfff45dbb08184165753fbde27` |
| `gates/D03.log` | 225 | `802b608816c2c91009130402f67f9d6e37e963fc7b34d4274d2300ce85db094e` |
| `gates/D04.log` | 244 | `2af4f9b202566156e92e019105a48ef81bb6d8498382fa0163061d6198cb9d15` |
| `gates/D05.log` | 249 | `318b800b024324a05184dd48dbfe82f2147086eef938ac4c3580f978425912ee` |
| `gates/D06.log` | 251 | `323e216552d69c14f7d1a9c9dede7ad23797285beae4525ce4729286ad810ec1` |
| `gates/D07.log` | 264 | `196c7554db0441dd644e611e77905684d52121966832da8690b14fbafb6cff5e` |
| `gates/D08.log` | 268 | `596ab44943d39c9745c2949f19aecc5d8375acff5c9dfa2c69b25d28a594d8ba` |
| `gates/D09.log` | 261 | `56119b55978863570d22f48f3f2456fc73c3499a3e77af3fe5e77393f39514d1` |
| `gates/D10.log` | 264 | `c30993b4fd7abe5b704e51a1994307cf19e06201a7fdf6690249eb2b7eb08b24` |
| `gates/D11.log` | 273 | `bc54da19d7cbd241019fd2248df9e7edcf315d28114cfb59bea700a0f718706f` |
| `gates/D12.log` | 269 | `227ebf93f905405a4ecd2e22bfafd6c3b13d62c6f3f41ab9c0e09e17d22e6335` |
| `gates/D13.log` | 272 | `43d97a0ebcdda190d14f55c2b0e2e9e6015a764b3b987e2ef5a48d9fb565b2f3` |
| `gates/D14.log` | 315 | `00324431f4429902b9ea1862c3d437e930ad2aece38b2c2ae0ee1e2bf1ca4150` |
| `gates/D15.log` | 307 | `c6a4e238437ff60caa4a674f50245a1ef7bc9f4a9e1b14f6debb6926c65a31ff` |
| `gates/D16.log` | 303 | `e13b475c4be15770b532d57508e1da849f4db9cf8020a3853ce13159eff60447` |
| `gates/D17.log` | 253 | `6ede470824548bc7e4fb6b754c3826d6b0af898c5a030efba32501aa81d0d386` |
| `gates/D18.log` | 260 | `bbb5c23e950ce18e7183eca982e107c997f1af00495e3237731434096acc800d` |
| `gates/D19.log` | 1704 | `ad69506af8919b7e0f8747e5a122877f896d9d1a985454490f0e9398bd9963e9` |
| `gates/D20.log` | 270 | `5dc17be3d446a067c2b5669fc3a6cfbae5b6c6429fb386c9c57ee93ff4cd7f7a` |
| `gates/D21.log` | 6704 | `09391627ebdc88e402eb24c546a37c45699c83db5b0ad6108a41d4199446dc4b` |
| `gates/D22.log` | 1719 | `51d13a1e87baf62e04792feca5f93eed4a385aa0266be32ba6c3f586cad93e69` |
| `gates/D23.log` | 346 | `e74489dc3d60ad33d94105ead8271334de50a3616761c8aa6d86510bd75a6ddb` |
| `gates/D24.log` | 50804 | `dd6489735cfe912844d93a0d7083356020dbbcdbd34baa0bb47b27ffad8e6568` |
| `gates/D25.log` | 7216 | `6e60b49f83e542281becee49d72e3cd56a4523cd9c45f3cc922aa95d8e2a157e` |
| `gates/D26.log` | 510 | `f69d68682d5c69e914533f663f5fe40f878f759e8db7ad9ff7c58841c6c6e033` |
| `gates/D27.log` | 1701 | `a5924f29605fa4835b55324428fd3d7ce0506e766e673a38bb992b8c580bc0a2` |
| `gates/D28.log` | 3334 | `e5c555fdd5a9143f0dbc2d474f47e63f7c3e99b0ecfa635ec82021ed80c4abfe` |
| `gates/D29.log` | 3505 | `f635a97864b58954e4d88166bd559d8183801712d3592c21de010b16db260810` |
| `gates/D30.log` | 4223 | `9bdc5b64aab90d43a3ae189de498fbd485f72a179d64d7554411e8c3c0def85e` |
| `gates/D31.log` | 4822 | `87f19996ffeb62144f458b5f265dc5f949212f4ebbee4109dc5d2ed60506cd13` |
| `gates/D32.log` | 6797 | `a5517f3c9db4b0e7c54f6d962ff403f2b308a82527a1e3958b7aa6e014132b46` |
| `gates/D33.log` | 2787 | `9e8a9d89283226f7711d062c5299ad5edf5aa780055afc3acb67c63a4942d545` |
| `gates/D34.log` | 2043 | `a8d1fc47accf3ad13170a0555ff019188285901d180313906cc7f86622c1d405` |
| `gates/D35.log` | 3152 | `9a4c211528a368d0da6c5f61c9959bdc999d4c76b8a666004af1fb8e7e3b19db` |
| `gates/D36.log` | 3791 | `e4163804389dde4c5d76a1ed9ec6c0318f11319bd19deb4dd6d35661ef1c1ea4` |
| `gates/D37.log` | 2728 | `1e82853d0ea225c6f9c5db55544bdc6716f19b8e5e5697d5c153339665143022` |
| `gates/D38.log` | 2658 | `dd9267d23eb4daa5d607e907f1c2eee014c11873616803492fb88814cca96a65` |
| `gates/D39.log` | 37111 | `84713d05e9793ff53a8794c195a404200b96af142ca57519e466805bde3f9b5f` |
| `gates/D40.log` | 231 | `35e879cb70508b373d5a3a939de58010ba214655c0b65278d108b7f589cb8cb2` |
| `gates/E01.log` | 236 | `ce84631a40fe50d0bd164fa47ea69f970fff5452d2a69907568b24f68bde8c0d` |
| `gates/E02.log` | 1947 | `a2f2748cd653b88530199af5ede6ef4e0d70e82ad764bfefd5bdc3f006f0f59a` |
| `gates/G01.log` | 2822 | `7642c24598a1bda7f4d365be099389549a459e61fb3c1aae8ea93b69709199d4` |
| `gates/N01.log` | 381 | `7ce2c93279393328306b7249d2630353721fc099f3c67bed01a9b7e3b248ccb7` |
| `gates/N02.log` | 224 | `e54e063f8ba05f888fb1ba95a36eef06266cde12e821c89cff7a585babceda0e` |
| `superseded-gates/B01.log` | 3792 | `dc359af5d76668b844ff11da1332d8cbde768ec6da1407241dfa2f9fd7e2a141` |
| `superseded-gates/B02.log` | 1156 | `901b6afef6ced0af51124f99804b437dc1fe9af418c90cb88694508b7c6c3b6c` |
| `superseded-gates/B03.log` | 15091 | `9622c110dd7927f2c4a764cdb19a506c2f088b6a47b5f48ed4e216ef8cf64ca4` |
| `superseded-gates/B04.log` | 1464 | `7cc5f947fe0f1ccd91470e627c683ef506c02348939b223e30673e9b2e02172c` |
| `superseded-gates/B05.log` | 356 | `29a2ee8cbfd49ff55b4e9d11730dc376bb980a011ec6a2f540bdf8b6810ba8d9` |
| `superseded-gates/B06.log` | 6708 | `ae5aeef188a34494f6292b45da2688712db0ba260bafb0fd053f73d3cabc2e9c` |
| `superseded-gates/B07.log` | 142482 | `cebed0f026d5bc410c9730f5eea97bd0a3218553949d3976423b4b17a89dadba` |
| `superseded-gates/B08.log` | 325 | `13b2d16df5c57e9319019932f5b8775c983cff2f292053e7f137d1ae3ee9c665` |
| `superseded-gates/B09.log` | 218 | `f7126a06473da64282a1248a42dab3108abe1e954f2b70c1e1f0ced849e902fc` |
| `superseded-gates/B10.log` | 236 | `096af9099f72f464853135ebbdcdc19bba773f7dbe29305bcd6249391a689e57` |
| `superseded-gates/B11.log` | 499 | `73c6873c93955eaf4b644a3a1458bb111c3d462392b78ef706dfeedf1ed1a517` |
| `superseded-gates/B12.log` | 644 | `2acc9e9ce6940d277024b8325816be4c1aaabe1a7e3a2f923463098b4b6d8d73` |
| `superseded-gates/B13.log` | 307 | `7fc0139e6d33eb83af51f0f1387983c6c5e89b14bbc7e0c6bc5555b1bf4bc844` |
| `superseded-gates/B14.log` | 231 | `544c8dad6a50245aaf04be7951fe19cffec52cd2332a786123fccb2abcbbc8e8` |
| `superseded-gates/B15.log` | 231 | `afb18e93dc98bf7cbb292b55f91b868f4f3213b776df85522fd9f540679018d4` |
| `superseded-gates/B16.log` | 275 | `0dffb11e43e2349b204e490a8d55a29b2f8d2d97fb761e01c89c7b325d49ed31` |
| `superseded-gates/B17.log` | 269 | `e358ebb5cdd407ca4bed4487905a49754e6518fd2037ee3b209ea772f30594d6` |
| `superseded-gates/B18.log` | 275 | `f9c3357228a9c80771b8f923cf0555f9fb490a3b1e57d114aec5510da9c581dc` |
| `superseded-gates/B19.log` | 389 | `0fa19f732a9dcdb3da9fa821a9ecf6f62b23c160656a58018fe7e1906db1e234` |
| `superseded-gates/B20.log` | 281 | `012f882ccf3788704431571cd77a14b57906c4540f5733905188e2025be7ef8e` |
| `superseded-gates/B21.log` | 2191 | `942b0eca673d50697e4be6cd49e287aa568ebc817daba78edd78235a98433ab7` |
| `superseded-gates/B22.log` | 350 | `aff73a39932c18ab28abede807b2e699f4731e5ab5b2ecb2f1574feecf1bbae5` |
| `superseded-gates/B23.log` | 401 | `4d8096fb2d1e8fe0b0dbc07066dfeac90b6087d7030c6002defb90bd69351051` |
| `superseded-gates/B24.log` | 418 | `ea8dea206047ebfd26587247c2e27c88622f32a4c0d46d7cfe323cb8bcb717c5` |
| `superseded-gates/B25.log` | 344 | `33c07472b36b3c663888ad8f26927e54bb8be8eb060978e98626e3cc67014a09` |
| `superseded-gates/B26.log` | 271 | `008f365d21c75fbe31541bdef2993a14ae184db2c31e8c0cce88f00ac4af0202` |
| `superseded-gates/B27.log` | 610 | `af6473cdaf10662deb59c01d12729cb70249a0349b2ed14c9b509811172a8bd4` |
| `superseded-gates/B28.log` | 2769 | `50d31489f861250cb952453425fb2afbe17e4c6b637e9d52556de104b0aebbdb` |
| `superseded-gates/B29.log` | 272 | `d967a3b1bda393e43f50ab98db21f9a9d928d5fe66b5036c2aa5c530f0d704df` |
| `superseded-gates/B30.log` | 246 | `559038acbcedc301ff219d765506e999d7ce3975335957de6815b291df04fbad` |
| `superseded-gates/B31.log` | 5407 | `0a28ef3a828a5b2364e2f2139c4a80c17c4bf48c38230e71537d98eb57aa16fc` |
| `superseded-gates/B32.log` | 19895 | `c85abc7b53e2ef27e8650c505409ddc56e4c4758316554db04ee40ef39ea21f9` |
| `superseded-gates/B33.log` | 738 | `c871e248f3d341d944dc0345407736c9ea7f6809a92be39765966df33d0db89f` |
| `superseded-gates/B34.log` | 2768 | `69850c01967fd3bf72b7ee4352cacb0a1268cdf1ed84fcc1de24e85811116919` |
| `superseded-gates/B35.log` | 927 | `9a1e57a3d67064b784f43146fe423660f5c06661bb6836f44c930cd94d5a861f` |
| `superseded-gates/B36.log` | 377 | `bcfa4ad17c3ce12fafc27ed3f85930d8229e04976dd3a0fb4f09e1b5efb3b788` |
| `superseded-gates/B37.log` | 6282 | `e57f25ea9d5c80a33874530a84a658c1f113c9d136de9ba4b2ea98237178c029` |
| `superseded-gates/B38.log` | 14427 | `422c72194180827a5098536aa6df330f83b2b0603d33d801de9c438fc0d31ff0` |
| `superseded-gates/B39.log` | 36802 | `3fd4c50b524146a6e083426697b922a73e227bee26357ff7c56112904181a7a1` |
| `superseded-gates/B40.log` | 5863 | `5fee58c7607a27baa653be38e325357e20e2e3099f679dd50207f905d83c0d48` |
| `superseded-gates/B41.log` | 228 | `6610cc5beb7b62e92b342d593b366b5806a25053a5eb526426a80755f3ce3527` |
| `superseded-gates/B42.log` | 238 | `0710eb06af6f82d5de220c016a3ab60741a7d1d6b9f063e0f6ef39a111559b11` |
| `superseded-gates/B43.log` | 249 | `6c59bd93cc49ef513256e3fdb0afa418d9cb404e7aeed0be496da7858f2ee5c8` |
| `superseded-gates/B44.log` | 220 | `51fdbd812079096a82ab272b425d1a7b815c659b90930a8b4d5d2e974c625bee` |
| `superseded-gates/B45.log` | 5174 | `fc415fedfbe1a08f865c498f07a49fdb327a2d4fdaf5e943b8935d3f39953318` |
| `superseded-gates/B46.log` | 25899 | `c50afb48a4000c2d1add70a5a785710774d059753f6972c399a04c48f20086cc` |
| `superseded-gates/B47.log` | 9478 | `fc132ef70b459cbb941543496a1fb733ec0a49635750def319fd83b7b5a77f0d` |
| `superseded-gates/B48.log` | 12091 | `96f760bf45d1bf14d77d967c2d5c402b85358552d5ed794ad5b73dc1fdbacca2` |
| `superseded-gates/D01.log` | 621 | `2a89d7e9eab3ff497afabb1c6d063adca440933cf9192263d5855cb3fd889876` |
| `superseded-gates/D02.log` | 652 | `0a9d47f9cf0677e801ca485c7a78f8f989263efe009e589b12bb26f2555814ed` |
| `superseded-gates/D03.log` | 225 | `b7d9717fe348fd6872a8b2d0de90bab7201ff4eb523da2c47bfc9444e86dfe88` |
| `superseded-gates/D04.log` | 244 | `33cebfa0d51721c9aaa06e2364d8f0a1c39f62ff87af1c6e65f07c5147e3e881` |
| `superseded-gates/D05.log` | 249 | `5714faa35a1edb95e7c258e8673efcbf3ce8fb2f274fca9840e30ebe678f84d4` |
| `superseded-gates/D06.log` | 251 | `ea085a759c0257338587bce3e6e6d1503d4d9a8277424e1850f2711b1caa422f` |
| `superseded-gates/D07.log` | 264 | `31326aab8fb06c9538ff6e640af4f0036cad2f858182b7cfe7046293ee011ada` |
| `superseded-gates/D08.log` | 268 | `a116014d9b7b2fffd0a2816949def15188b139950e533fe54ea6ad6faacdb0f0` |
| `superseded-gates/D09.log` | 261 | `eba5b2ff33487e2d806d04734fc027fb6b7ddf763cad418a8080ba5fd5e4f8a0` |
| `superseded-gates/D10.log` | 264 | `34a633d86ea72efbf292e854fbe5854dc8f0f230f0d09410722543b55ff236fe` |
| `superseded-gates/D11.log` | 273 | `5fb6627b2087295da66603ae69055c5ed867d5af5467de488d00b324c7e698f6` |
| `superseded-gates/D12.log` | 269 | `700cee095832be1d2135d3e7d3319f76fa289b0fb121ab50e7ae69a993a4dbe9` |
| `superseded-gates/D13.log` | 272 | `a3e5595f4bcd2acf726c8b567e4193c8f46be6b03a386d913d66895866eb5102` |
| `superseded-gates/D14.log` | 315 | `ec31f6f44e334614cacd158d295cf268fa1f0366c0a3e0048fe11ec7d8142543` |
| `superseded-gates/D15.log` | 307 | `f5c03acf9df60cf4cc0f874fccaf263c1609611138a7b33f29a3aeaa424f0910` |
| `superseded-gates/D16.log` | 303 | `b328e6caf05ce475ffce977d9a18f71b0aa5b3f63319171be04e80a59da7d87c` |
| `superseded-gates/D17.log` | 253 | `4eb3905fc23d796fa49bdffa44a2afdf8b1d1513dc04eb136c069aeab61ba017` |
| `superseded-gates/D18.log` | 260 | `5dd3095c457820d25ff5929466d440383c6c9a930b7e4cdc7d67333293bc006b` |
| `superseded-gates/D19.log` | 1704 | `5000262efc491c0868081502991480444effe4a9344e75c923278103170b72f1` |
| `superseded-gates/D20.log` | 270 | `3b20f0e028002d9de5251f0eab4d58629e2145a733db8210db63299a23ad70bd` |
| `superseded-gates/D21.log` | 6704 | `6231ee5fb15c299d3ba9fa222cdfaf16e468e2b6477cce020094742839983a6d` |
| `superseded-gates/D22.log` | 1719 | `4d5b6cbf803153136a5b1535a307cb4f6c064bdf20a0cf6270bde023b0c48422` |
| `superseded-gates/D23.log` | 346 | `f7afd156bfe89633c5afa34a0828dbcb3ac2ad36039a0ada60e99d15ff029d22` |
| `superseded-gates/D24.log` | 6002 | `353182725d5a643ac89ee8d7ce298fd45a278b11ec1b188871cb86da7b1d597e` |
| `superseded-gates/D25.log` | 7216 | `a211db50a463311b4237dfa1fa5d75b00bf8a8e0d08a880ef622fd83867d0264` |
| `superseded-gates/D26.log` | 510 | `462f1ba0709d769395c66a3c043c8a02f09e5549c6e69924f23f00ae28e9d9f8` |
| `superseded-gates/D27.log` | 1701 | `9dc45bda6bb630322dd4a024c85a3967a5e032c242c77fcbcbea9de65912e68c` |
| `superseded-gates/D28.log` | 3334 | `43981c618be4c1e82e900454cffb3a04cbe0d4b44ac2a97ae081d420f88becbc` |
| `superseded-gates/D29.log` | 3505 | `5b2cd1f62d44295c597564009559554f7234717c5d9dd8d473cdb5596da66d62` |
| `superseded-gates/D30.log` | 4223 | `0c35da42551eae643a0078ccb583732db68e4d1adf5d8cfc8a10b4cb06ed7e05` |
| `superseded-gates/D31.log` | 4822 | `b89fde2e2fce34de9575c2a771b652068df5737d8d235442c7d7eb58583e099f` |
| `superseded-gates/D32.log` | 6797 | `4c8a8069661dde12170c30e28169b51200a899c698b7e3f738239221774add20` |
| `superseded-gates/D33.log` | 2787 | `c04ee34eb82b2228f5f34b47f1306eba0991d64e646a8d5afd6b3314b70b7764` |
| `superseded-gates/D34.log` | 2043 | `75020c1052635c918a1503bf8b24c40a8a45a3163072e689d2334d7a7096b50b` |
| `superseded-gates/D35.log` | 3152 | `ecc79eadac478e840b244191bad63d44158b708379be6b7651e1eb6b7c03aee6` |
| `superseded-gates/D36.log` | 3791 | `8329c2b6f68490620a0da28a2752a7395f2deefe2ca1470fc036a0430e7da885` |
| `superseded-gates/D37.log` | 2728 | `7d5e8a841cc9d213a3d02745d115cb14478317522f7027123947a7c2868441a7` |
| `superseded-gates/D38.log` | 2658 | `ab2fda40f3b6595ec82bb9979616dfd255f756fd2b31295ce1ddc98a3b0b4543` |
| `superseded-gates/D39.log` | 37111 | `64d61adca6b9fa429bd5deeeececc29c76b4ac683d50d55cd24d1593d0568a58` |
| `superseded-gates/D40.log` | 231 | `a1f6717aaf4bd8dba40a36d15ad599fc6c6b6e0a888a9854610f05238656ea90` |
| `superseded-gates/G01.log` | 2822 | `2f300420ad61c63366ee4a695df517cf2f657de89afff86cc26bd742d4bcf699` |
| `superseded-gates/N01.log` | 486 | `f2a9274bb1bbd6eb9d68116ab4fe5b44156b201770e13ee984a95b06bb4da92c` |
| `superseded-gates/N02.log` | 224 | `0e1102be9d32e7c6a8edcb7ea1d8249503f0b371561977c3f4b69944af52e60e` |
| `superseded-gates-complete.json` | 14119 | `931534904da9e2a3173dc2eb027f237d7c01542f608491c72a5676b925b652a2` |
| `superseded-progress.log` | 3393 | `f905fcf484e16b12bf5f766c5be4a4d92258d1fe9bc495a653e7d545f98fea91` |
| `reused-dependencies/.milan-rv32-sdk.json` | 789637 | `6c6ba8a0988aa284f0897fd3bcbb310d1bdcec5a1379f7208a1f753cbce76b8b` |
| `reused-dependencies/dependencies.log` | 1322 | `8b626d7f98c0f1a376534ec300e4d3a210989e3c5f089970a50831d4f054142b` |
| `reused-dependencies/dependencies-extra.log` | 788 | `ab28fa6af8e337e3ddbb416f010e556753aca3c3604796c56cff8a5710fef4af` |
| Pinned SDK archive | 102597892 | `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f` |
| Standard: `Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf` | 1684588 | `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8` |
| Standard: `1722.1-2021.pdf` | 5494661 | `ad7b822008c1b78bce8af1470f1ace177a22344aa48c0da939066d6db9a65b9c` |
| Standard: `1722-2016.pdf` | 7354196 | `ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c` |
| Standard: `802.1Q-2018.pdf` | 18576069 | `55268b5f716aee085c3357a4cba398602d9f0cb340fe3d8a70de40fac58ed956` |

## Acceptance and remaining work

Document scope, ownership, normative citations, the proposed service budget,
eight test hooks, traceability, contradiction dispositions and version landing
plan are present. The owner must approve the exact text before merge.
Independent internal and external reviews must reconstruct the task from public
state. Their lens ledger is not supplied by the executor. The manager handles
publication, hosted evidence, candidate-merge validation and post-merge work.

Final status message: `[A548] REVIEW READY` with the candidate head above.
See issue #664 for the public handoff comment. The manager must retain the
validation limitations and pending owner approval when updating PR #674.
Final worktree status is clean; all changed tracked files are Markdown.
