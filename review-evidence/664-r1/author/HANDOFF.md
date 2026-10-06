# [A548] Issue #664 handoff

## Status and identity

Candidate: `a27808375427859dc357f6bfd0a88842062b20ed` on `664-mark2-reqs`.
Verified assigned base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Verified origin: `https://github.com/kebag-logic/milan-fpga.git`.
All 91 command exit codes are zero. B33 skipped vendor analysis; B48 gate 11 calibration did not run because its historical placement report is absent.
Executor [A548]; independent reviewers [R508] and [R509].
No review verdict is claimed by the executor. Owner approval remains pending.
No push, PR creation/edit, merge, rebase, amend or hardware access occurred.
Only documentation files changed; VERSION and executable artifacts are unchanged.

The prior STOP 6009666033 was resolved by ruling 6009675758.
Resumed TAKEN: issue #664 comment 6009682962.
The final status comment is recorded below after publication.

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
| FR_NFR: Discovery | Discovery &#124; FR-DISC-\* &#124; Section 5.2 &#124; `adp`, ENTITY &#124; M-B2 -- processor (Section 2.0) | Discovery &#124; FR-DISC-\*, NFR-SCOUT-01..03 &#124; Sections 5.6.2/5.6.3/5.6.4 &#124; `adp`, ENTITY &#124; Current fabric ledger: Section 2.0; split F0/F3, hooks H-ADP/H-ACMP |
| FR_NFR: Enum/Control | Enum/Control &#124; FR-ENUM/CTRL &#124; Section 5.3–5.4 &#124; full descriptor tree &#124; M-B3, processor AECP uCPU plus the builder-generated image copied by bare-metal firmware; the served inventory and mandatory gaps are listed in Section 2.0 | Enum/Control &#124; FR-ENUM/CTRL, NFR-LAT-02, NFR-SCOUT-01..03 &#124; Sections 5.3/5.4 &#124; full descriptor tree &#124; Current fabric ledger: Section 2.0; split F5, hooks H-AECP/H-NOTIFY/H-COUNTERS |
| FR_NFR: Connection | Connection &#124; FR-CONN-\* &#124; Section 5.5 &#124; STREAM_\*, CBS CSR &#124; M-B4 -- processor; fast-connect/persistence **NOT MET** | Connection &#124; FR-CONN-\*, NFR-LAT-02, NFR-SCOUT-01..03 &#124; Section 5.5; Table 5.26 &#124; STREAM_\*, selected state owner &#124; Current fabric ledger: Section 2.0; split F1/F3, H-ACMP; cold restore remains unproven |
| FR_NFR: MAAP/SRP | MAAP/SRP &#124; FR-MAAP/SRP &#124; Section 5.6 &#124; STREAM_\*, classifier/CBS &#124; M-B5 -- MAAP in fabric, SRP on the processor | MAAP/SRP &#124; FR-MAAP/SRP, NFR-SCOUT-01..03 &#124; Sections 4.3.1/4.2.7; Table 4.3 &#124; STREAM_\*, admission &#124; Current fabric ledger: Section 2.0; split F2/F4, H-MAAP/H-SRP |
| FR_NFR: Scale-out | Scale-out &#124; NFR-SCOUT-\* &#124;  -  &#124; fabric contexts / replicated endpoint &#124; Section 4 | Scale-out &#124; NFR-SCOUT-\*, NFR-SCUP-02/04, NFR-REL-02 &#124; Sections 3.4.1/3.4.2 list timing clauses &#124; fabric media / static selected-owner control contexts &#124; Section 4; every shape, placement and hook |
| IEEE 802.1Q: MRP-6 | MRP-6 &#124; 10.7.11 &#124; Timer values: JoinTime ~200 ms, LeaveTime 600–1000 ms, LeaveAllTime ~10 s (+Milan tolerances 4.2.7.1.1) &#124; processor timer service &#124; 🔵 PROCESSOR -- Milan Table 4.3 tightens these values and the submodule owns them now; since processor pin `b2db3a97` its srp_top suite grades joinTime, the periodictimer and the leavealltimer against Table 4.3 (Q1-Q4, processor issue 64). `tb/verilator/pp_shadow` compresses the prescaler for liveness only, never for cadence &#124; 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. | MRP-6 &#124; 10.7.11 &#124; Timer values: JoinTime 200 ms (180 to 240), LeaveTime 5000 ms (4500 to 7500), periodic 1000 ms (900 to 1500), LeaveAllTime 10 to 15 s (+/-0.5 s), Milan 4.2.7.1.1 Table 4.3; firmware service uses NFR-SCOUT-03 and H-SRP &#124; processor timer service &#124; 🔵 PROCESSOR -- Milan Table 4.3 overrides the IEEE defaults and the submodule owns them now; since processor pin `b2db3a97` its srp_top suite grades joinTime, the periodictimer and the leavealltimer against Table 4.3 (Q1-Q4, processor issue 64). `tb/verilator/pp_shadow` compresses the prescaler for liveness only, never for cadence &#124; 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. |


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
| ACMP PROBE_TX, GET_TX_STATE, BIND_RX, UNBIND_RX, GET_RX_STATE | Milan v1.2 5.5.2.3, Table 5.26: each transaction times out at 200 ms, replacing the applicable IEEE 1722.1-2021 Table 8-1 value | 200 ms x 10% = 20 ms; service <= 10 ms. The complete command transaction must finish inside 200 ms with measured margin | A retry cannot enlarge one attempt's timeout; delayed probe/backoff events retain Milan 5.5.3 timers |
| AECP solicited AEM, descriptor and counter responses | IEEE 1722.1-2021 9.3.2.6: respond within 240 ms; transaction timeout 250 ms | min(240, 250) ms x 10% = 24 ms; service <= 10 ms. The complete response must meet 240 ms with margin | The existing no-IN_PROGRESS policy remains. If adopted later, its 120 ms cadence yields a tighter 12 ms ceiling, still above T_svc |
| AECP MVU response | Milan v1.2 5.4.3.4: response within 240 ms; transaction timeout 250 ms | 240 ms x 10% = 24 ms; service <= 10 ms, with the same wire-response margin | Apply the MVU-specific response and refusal rules |
| AECP successful-command and asynchronous notifications | Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2: immediate notification after the successful state-changing response; Table 5.22 defines asynchronous triggers, without a numeric delivery maximum | Related AECP response interval 240 ms gives 24 ms. `T_svc=10 ms` is a project event-to-commit budget, not a new normative timeout | Response precedes its notification, including cross-protocol causality (#653). Do not wait out T_svc deliberately; notify immediately |
| AECP GET_COUNTERS push | Milan v1.2 5.4.5.2, Table 5.22: at most one notification per descriptor per second. Counter updates: Milan 5.3.7.7/5.3.8.10, at most 1 s | Spacing gives 100 ms; shared AECP response interval tightens the ceiling to 24 ms. Service <= 10 ms once eligible; record the preceding rate-limit wait separately | One second is minimum spacing, not a maximum delivery latency. Coalesce pending changes; preserve counter observation and reset semantics |
| AECP liveness, unlock and optional identification | Milan v1.2 5.4.5.3: 30 to 60 s monitor then CONTROLLER_AVAILABLE; 5.4.2.2: 60 s unlock. IEEE 1722.1-2021 7.5.1/7.5.1.2.1: three Identify notifications, spaced 150 ms when enabled | 150 ms x 10% = 15 ms is the tightest enabled notification interval; service <= 10 ms. Probe responses still obey 9.3.2.6 | Preserve registration, retry, removal and identification ordering; the optional feature is not enabled by this requirement |
| MAAP PROBE and conflict DEFEND | IEEE 1722-2016 B.3.4.2, Table B.8: strictly 500 ms < probe interval < 600 ms; `MAAP_PROBE_RETRANSMITS=3`. B.3.3, B.3.5.5 and B.3.6.6 define conflict handling | 500 ms x 10% = 50 ms; service <= 10 ms. Three retransmissions do not multiply the per-action budget | DEFEND on the applicable conflicting PROBE transition. The probe interval is not a normative received-PROBE response timeout |
| MAAP ANNOUNCE and reallocation | IEEE 1722-2016 B.3.4.1, Table B.8: strictly 30 s < announcement interval < 32 s; B.3.3 governs loss and retry | Announcement gives 3 s; the shared 500 ms probe interval tightens this to 50 ms | Preserve randomization, strict bounds and address-loss handling; service time cannot push a timer beyond its upper bound |
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
| H-ACMP | FR-CONN-01..04; NFR-LAT-02; NFR-SCOUT-01..03 | ACMP `RX_HEAD` commit to the matched response `TX_HEAD`; originated command commit to response receipt; discovery/probe timer deadline to its action | Each Table 5.26 command, success/refusal, retry, distinct sequence/unique IDs, restore and fast connect; wire round-trip < 200 ms with margin |
| H-AECP | FR-ENUM-01/02; FR-CTRL-01..06; FR-MVU-01..03; NFR-SCUP-04; NFR-LAT-02 | AECP `RX_HEAD` commit to matched response `TX_HEAD`, plus received-command and emitted-response wire observations | AEM/MVU, descriptors, getters/setters, counters and refusals; longest image/state access; locks; malformed/truncated requests; response <= 240 ms with margin |
| H-NOTIFY | FR-CTRL-03; FR-MGT-01/02; NFR-SCOUT-02/03 | Causal command RX or asynchronous state-change occurrence to the last required notification `TX_HEAD`; record response commit and every recipient's wire departure | Successful-command ordering, cross-channel ACMP response then AECP notice, all registered recipients, departure probes, unlock, enabled Identify spacing, full transmit rings |
| H-COUNTERS | FR-CTRL-04; FR-STR-04; NFR-OBS-01; NFR-SCOUT-02/03 | Fabric counter snapshot/update event to the last push `TX_HEAD`; previous notification wire time supplies eligibility; solicited GET_COUNTERS uses H-AECP | Every descriptor bank and stream, coherent snapshots, resets/wrap, multiple changes while rate-limited; >= 1 s per-descriptor wire spacing; <= 1 s counter update |
| H-MAAP | FR-MAAP-01; NFR-SCOUT-02/03 | MAAP `RX_HEAD` commit or original timer deadline to PROBE/DEFEND/ANNOUNCE `TX_HEAD`; state completion when no frame is required | Conflict in each state, three probe retransmissions, allocation loss/retry, strict probe/announce intervals, ring stalls and boundary draws |
| H-SRP | FR-SRP-01..03; FR-CONN-02; NFR-SCOUT-01..03 | SRP `RX_HEAD` commit or fabric timer deadline to MRPDU `TX_HEAD`; registrar/state-apply commitment for non-transmitting transitions | MSRP/MVRP joins, withdrawal, malformed vectors, LeaveAll/periodic expiry, coalesced tick backlog, reservation/licence updates; JoinTime and LeaveTime bounds |

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
READMEs, with `rg --json -n` and Q1 to Q3 below. Q4 uses the same tracked-document
scope through `git grep -n -E` at both revisions to audit the other changed
requirement identifiers. Gitlinks are not root
tracked files. Pinned donor implementation documentation remains evidence for
the supported all-fabric implementation, not a claim that split firmware exists.

- Q1: `NFR-SCOUT-0[123]`
- Q2: `never on firmware|fabric-only|fabric.only|no firmware round trip|never becomes a packet|all per-frame protocol`
- Q3: `(?i)(ADP|ACMP|AECP|MAAP|SRP|protocol control).{0,70}(fabric|processor)|(fabric|processor).{0,70}(ADP|ACMP|AECP|MAAP|SRP|protocol control)`
- Q4: `NFR-LAT-02|NFR-SCUP-0[24]|NFR-REL-02|FR-CTRL-04`

Base audit: 617 query/line records. Candidate audit: 643 records. A line can match more than one query.

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
| Q1 | `docs/reference/FR_NFR.md:307` | E |
| Q1 | `docs/reference/FR_NFR.md:308` | E |
| Q1 | `docs/reference/FR_NFR.md:309` | E |
| Q1 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:274` | H |
| Q2 | `docs/overview/ARCHITECTURE.md:30` | E |
| Q2 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:38` | E |
| Q2 | `docs/reference/FR_NFR.md:71` | E |
| Q2 | `docs/reference/FR_NFR.md:309` | E |
| Q2 | `docs/reference/FR_NFR.md:349` | E |
| Q2 | `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:8` | E |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:883` | R |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1847` | R |
| Q2 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | C |
| Q3 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:65` | H |
| Q3 | `THIRD_PARTY.md:19` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:64` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:182` | I |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:37` | E |
| Q3 | `CHANGELOG.md:14` | H |
| Q3 | `CHANGELOG.md:474` | H |
| Q3 | `REQUIREMENTS.md:162` | E |
| Q3 | `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:218` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:26` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:28` | H |
| Q3 | `QUICKSTART.md:17` | I |
| Q3 | `QUICKSTART.md:266` | I |
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
| Q3 | `docs/GLOSSARY.md:29` | E |
| Q3 | `docs/GLOSSARY.md:30` | E |
| Q3 | `docs/GLOSSARY.md:79` | E |
| Q3 | `README.md:41` | E |
| Q3 | `README.md:42` | E |
| Q3 | `README.md:56` | E |
| Q3 | `README.md:364` | E |
| Q3 | `README.md:381` | E |
| Q3 | `README.md:423` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:328` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:419` | E |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1389` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1397` | P |
| Q3 | `docs/MILAN_V12_ROADMAP.md:201` | I |
| Q3 | `docs/MILAN_V12_ROADMAP.md:467` | I |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:41` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:47` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:79` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:89` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:91` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:195` | E |
| Q3 | `docs/history/v1/design/TIME_SYNC.md:553` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:24` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:35` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:112` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:113` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:118` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:262` | H |
| Q3 | `docs/integration/QSPI_FLASHBOOT.md:52` | I |
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
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:18` | H |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76` | H |
| Q3 | `docs/reference/SUBMODULES.md:25` | I |
| Q3 | `docs/reference/SUBMODULES.md:35` | I |
| Q3 | `docs/reference/SUBMODULES.md:97` | I |
| Q3 | `docs/reference/SUBMODULES.md:98` | I |
| Q3 | `docs/reference/SUBMODULES.md:99` | I |
| Q3 | `docs/reference/SUBMODULES.md:132` | I |
| Q3 | `docs/reference/SUBMODULES.md:134` | I |
| Q3 | `docs/history/v1/MVP_TALKER.md:28` | H |
| Q3 | `docs/history/v1/MVP_TALKER.md:58` | H |
| Q3 | `sw/firmware/nvm_hosttest/README.md:101` | I |
| Q3 | `docs/development/CODE_QUALITY.md:218` | I |
| Q3 | `docs/development/CODE_QUALITY.md:372` | I |
| Q3 | `docs/development/CODE_QUALITY.md:380` | I |
| Q3 | `docs/development/CODE_QUALITY.md:601` | I |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:108` | H |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:109` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:27` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:64` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:72` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:201` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:287` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:351` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:369` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:471` | H |
| Q3 | `syn/yosys/README.md:312` | I |
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
| Q3 | `docs/history/v1/design/GPTP_PLANE.md:99` | H |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:119` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:121` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:416` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:1393` | P |
| Q3 | `docs/findings/397_SERVICE_BUDGET.md:190` | H |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:62` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:89` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:93` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:117` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:144` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:260` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:261` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:265` | E |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:221` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2030` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2163` | I |
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
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:205` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:228` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:229` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:304` | H |
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
| Q3 | `sw/firmware/ctrl/README.md:18` | E |
| Q3 | `sw/firmware/ctrl/README.md:46` | E |
| Q3 | `sw/firmware/ctrl/README.md:47` | E |
| Q3 | `sw/firmware/ctrl/README.md:49` | E |
| Q3 | `sw/firmware/ctrl/README.md:54` | E |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:334` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:338` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:9` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:28` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:127` | I |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:19` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:195` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:206` | H |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:265` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:309` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:379` | P |
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
| Q3 | `tb/verilator/README.md:105` | I |
| Q3 | `sw/builder/README-parameters.md:210` | I |
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
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:67` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:171` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:175` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:243` | H |
| Q3 | `tb/verilator/avtp_parser/README.md:17` | I |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:48` | E |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:49` | E |
| Q3 | `docs/integration/BUILDING.md:144` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:90` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:93` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:96` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:249` | I |
| Q3 | `docs/traceability/MODULE_MATRIX.md:52` | G |
| Q3 | `docs/traceability/MODULE_MATRIX.md:106` | G |
| Q3 | `tests/README.md:10` | I |
| Q3 | `tests/README.md:23` | I |
| Q3 | `tests/README.md:53` | I |
| Q3 | `tests/README.md:54` | I |
| Q3 | `tests/README.md:151` | I |
| Q3 | `docs/overview/ARCHITECTURE.md:52` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:59` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:62` | E |
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
| Q3 | `docs/testing/SIMULATION.md:38` | I |
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
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:12` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:55` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:84` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:85` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:89` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:90` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:91` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:93` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:98` | I |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:28` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:57` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:59` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:68` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:107` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:133` | H |
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
| Q3 | `docs/limitations/TROUBLESHOOTING.md:94` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:151` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:816` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:914` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:978` | I |
| Q3 | `docs/testing/TESTING.md:25` | I |
| Q3 | `docs/testing/TESTING.md:273` | I |
| Q3 | `docs/testing/TESTING.md:445` | I |
| Q3 | `docs/testing/TESTING.md:517` | I |
| Q3 | `docs/testing/TESTING.md:532` | I |
| Q3 | `docs/testing/TESTING.md:1173` | I |
| Q3 | `docs/testing/TESTING.md:1227` | I |
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
| Q3 | `docs/reference/FR_NFR.md:13` | E |
| Q3 | `docs/reference/FR_NFR.md:14` | E |
| Q3 | `docs/reference/FR_NFR.md:28` | E |
| Q3 | `docs/reference/FR_NFR.md:47` | E |
| Q3 | `docs/reference/FR_NFR.md:98` | E |
| Q3 | `docs/reference/FR_NFR.md:102` | E |
| Q3 | `docs/reference/FR_NFR.md:145` | E |
| Q3 | `docs/reference/FR_NFR.md:151` | E |
| Q3 | `docs/reference/FR_NFR.md:153` | E |
| Q3 | `docs/reference/FR_NFR.md:154` | E |
| Q3 | `docs/reference/FR_NFR.md:160` | E |
| Q3 | `docs/reference/FR_NFR.md:165` | E |
| Q3 | `docs/reference/FR_NFR.md:308` | E |
| Q3 | `docs/reference/FR_NFR.md:342` | E |
| Q3 | `docs/reference/FR_NFR.md:359` | E |
| Q3 | `docs/reference/FR_NFR.md:410` | E |
| Q3 | `docs/reference/FR_NFR.md:447` | E |
| Q3 | `docs/reference/FR_NFR.md:448` | E |
| Q3 | `docs/reference/FR_NFR.md:451` | E |
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
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:178` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:255` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:276` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:279` | H |
| Q4 | `docs/reference/FR_NFR.md:148` | E |
| Q4 | `docs/reference/FR_NFR.md:162` | E |
| Q4 | `docs/reference/FR_NFR.md:187` | E |
| Q4 | `docs/reference/FR_NFR.md:286` | E |
| Q4 | `docs/reference/FR_NFR.md:300` | E |
| Q4 | `docs/reference/FR_NFR.md:302` | E |
| Q4 | `docs/reference/FR_NFR.md:320` | E |

### Candidate hit ledger

| Query | Exact hit locator | Disposition |
|---|---|---|
| Q1 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:60` | E |
| Q1 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:214` | E |
| Q1 | `docs/design/MAILBOX_SPLIT.md:348` | E |
| Q1 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:274` | H |
| Q1 | `REQUIREMENTS.md:44` | E |
| Q1 | `docs/reference/FR_NFR.md:300` | E |
| Q1 | `docs/reference/FR_NFR.md:314` | E |
| Q1 | `docs/reference/FR_NFR.md:321` | E |
| Q1 | `docs/reference/FR_NFR.md:322` | E |
| Q1 | `docs/reference/FR_NFR.md:323` | E |
| Q1 | `docs/reference/FR_NFR.md:401` | E |
| Q1 | `docs/reference/FR_NFR.md:402` | E |
| Q1 | `docs/reference/FR_NFR.md:404` | E |
| Q1 | `docs/reference/FR_NFR.md:405` | E |
| Q1 | `docs/reference/FR_NFR.md:406` | E |
| Q1 | `docs/reference/FR_NFR.md:407` | E |
| Q1 | `docs/reference/FR_NFR.md:557` | E |
| Q1 | `docs/reference/FR_NFR.md:558` | E |
| Q1 | `docs/reference/FR_NFR.md:560` | E |
| Q1 | `docs/reference/FR_NFR.md:561` | E |
| Q1 | `docs/overview/FULL_FPGA_SOLUTION.md:97` | E |
| Q1 | `docs/traceability/ieee8021q.md:119` | E |
| Q1 | `docs/traceability/ieee8021q.md:138` | E |
| Q1 | `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:36` | E |
| Q2 | `docs/overview/ARCHITECTURE.md:37` | E |
| Q2 | `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:8` | E |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:883` | R |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1847` | R |
| Q2 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | C |
| Q3 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:65` | H |
| Q3 | `docs/AAF_LATENCY_TAPS.md:64` | I |
| Q3 | `docs/AAF_LATENCY_TAPS.md:182` | I |
| Q3 | `THIRD_PARTY.md:19` | I |
| Q3 | `CHANGELOG.md:14` | H |
| Q3 | `CHANGELOG.md:474` | H |
| Q3 | `REQUIREMENTS.md:184` | E |
| Q3 | `QUICKSTART.md:17` | I |
| Q3 | `QUICKSTART.md:266` | I |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:26` | H |
| Q3 | `docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md:28` | H |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:41` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:42` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:43` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:44` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:45` | E |
| Q3 | `docs/ARCHITECTURE_HW_SW_SPLIT.md:54` | E |
| Q3 | `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:218` | H |
| Q3 | `README.md:41` | E |
| Q3 | `README.md:42` | E |
| Q3 | `README.md:56` | E |
| Q3 | `README.md:372` | E |
| Q3 | `README.md:389` | E |
| Q3 | `README.md:431` | E |
| Q3 | `docs/MILAN_V12_ROADMAP.md:201` | I |
| Q3 | `docs/MILAN_V12_ROADMAP.md:467` | I |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:24` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:35` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:112` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:113` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:118` | H |
| Q3 | `docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:262` | H |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:48` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:54` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:86` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:96` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:98` | E |
| Q3 | `docs/fpga/DATAPLANE_WALKTHROUGH.md:202` | E |
| Q3 | `docs/integration/QSPI_FLASHBOOT.md:52` | I |
| Q3 | `sw/firmware/nvm_hosttest/README.md:101` | I |
| Q3 | `docs/design/MAILBOX_SPLIT.md:332` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:429` | E |
| Q3 | `docs/development/CODE_QUALITY.md:218` | I |
| Q3 | `docs/development/CODE_QUALITY.md:372` | I |
| Q3 | `docs/development/CODE_QUALITY.md:380` | I |
| Q3 | `docs/development/CODE_QUALITY.md:601` | I |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:67` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:94` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:98` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:122` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:149` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:265` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:266` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:270` | E |
| Q3 | `docs/history/v1/MVP_TALKER.md:28` | H |
| Q3 | `docs/history/v1/MVP_TALKER.md:58` | H |
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
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:108` | H |
| Q3 | `docs/findings/606_FIRST_BIND_MEASUREMENT.md:109` | H |
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
| Q3 | `docs/reference/SUBMODULES.md:25` | I |
| Q3 | `docs/reference/SUBMODULES.md:35` | I |
| Q3 | `docs/reference/SUBMODULES.md:97` | I |
| Q3 | `docs/reference/SUBMODULES.md:98` | I |
| Q3 | `docs/reference/SUBMODULES.md:99` | I |
| Q3 | `docs/reference/SUBMODULES.md:132` | I |
| Q3 | `docs/reference/SUBMODULES.md:134` | I |
| Q3 | `docs/GLOSSARY.md:79` | E |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:119` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:121` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:416` | P |
| Q3 | `docs/design/SAVED_STATE_FASTCONNECT.md:1393` | P |
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
| Q3 | `docs/findings/397_SERVICE_BUDGET.md:190` | H |
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
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:18` | H |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76` | H |
| Q3 | `sw/firmware/ctrl/README.md:25` | E |
| Q3 | `sw/firmware/ctrl/README.md:53` | E |
| Q3 | `sw/firmware/ctrl/README.md:54` | E |
| Q3 | `sw/firmware/ctrl/README.md:56` | E |
| Q3 | `sw/firmware/ctrl/README.md:61` | E |
| Q3 | `docs/history/v1/design/TIME_SYNC.md:553` | H |
| Q3 | `syn/yosys/README.md:312` | I |
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
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:205` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:228` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:229` | H |
| Q3 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:304` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:67` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:171` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:175` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:243` | H |
| Q3 | `docs/history/v1/design/GPTP_PLANE.md:99` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:19` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:195` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:206` | H |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:9` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:28` | I |
| Q3 | `docs/reference/EGRESS_QUEUE_MAP.md:127` | I |
| Q3 | `sw/builder/README-parameters.md:210` | I |
| Q3 | `tb/verilator/avtp_parser/README.md:17` | I |
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
| Q3 | `tb/verilator/README.md:105` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:334` | I |
| Q3 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:338` | I |
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
| Q3 | `docs/integration/BUILDING.md:144` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:90` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:93` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:96` | I |
| Q3 | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:249` | I |
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
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:12` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:55` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:84` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:85` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:89` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:90` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:91` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:93` | I |
| Q3 | `docs/reference/REGISTER_MAP_CLASSES.md:98` | I |
| Q3 | `docs/testing/SIMULATION.md:38` | I |
| Q3 | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3` | I |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1389` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1397` | P |
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
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:265` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:309` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:379` | P |
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
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:221` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2030` | I |
| Q3 | `docs/integration/BAREMETAL_FIRMWARE.md:2163` | I |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:27` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:64` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:72` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:201` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:287` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:351` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:369` | H |
| Q3 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:471` | H |
| Q3 | `docs/overview/ARCHITECTURE.md:59` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:66` | E |
| Q3 | `docs/overview/ARCHITECTURE.md:69` | E |
| Q3 | `docs/traceability/MODULE_MATRIX.md:52` | G |
| Q3 | `docs/traceability/MODULE_MATRIX.md:106` | G |
| Q3 | `tests/README.md:10` | I |
| Q3 | `tests/README.md:23` | I |
| Q3 | `tests/README.md:53` | I |
| Q3 | `tests/README.md:54` | I |
| Q3 | `tests/README.md:151` | I |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:54` | E |
| Q3 | `docs/overview/FULL_FPGA_SOLUTION.md:55` | E |
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
| Q3 | `docs/traceability/ieee8021q.md:133` | E |
| Q3 | `docs/traceability/ieee8021q.md:134` | E |
| Q3 | `docs/traceability/ieee8021q.md:135` | E |
| Q3 | `docs/traceability/ieee8021q.md:136` | E |
| Q3 | `docs/traceability/ieee8021q.md:137` | E |
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
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:28` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:57` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:59` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:68` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:107` | H |
| Q3 | `docs/history/v1/traceability/ieee1722-2016.md:133` | H |
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
| Q3 | `docs/limitations/TROUBLESHOOTING.md:94` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:151` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:816` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:914` | I |
| Q3 | `docs/limitations/TROUBLESHOOTING.md:978` | I |
| Q3 | `docs/testing/TESTING.md:25` | I |
| Q3 | `docs/testing/TESTING.md:273` | I |
| Q3 | `docs/testing/TESTING.md:445` | I |
| Q3 | `docs/testing/TESTING.md:517` | I |
| Q3 | `docs/testing/TESTING.md:532` | I |
| Q3 | `docs/testing/TESTING.md:1173` | I |
| Q3 | `docs/testing/TESTING.md:1227` | I |
| Q3 | `docs/reference/FR_NFR.md:14` | E |
| Q3 | `docs/reference/FR_NFR.md:28` | E |
| Q3 | `docs/reference/FR_NFR.md:47` | E |
| Q3 | `docs/reference/FR_NFR.md:112` | E |
| Q3 | `docs/reference/FR_NFR.md:116` | E |
| Q3 | `docs/reference/FR_NFR.md:159` | E |
| Q3 | `docs/reference/FR_NFR.md:165` | E |
| Q3 | `docs/reference/FR_NFR.md:167` | E |
| Q3 | `docs/reference/FR_NFR.md:168` | E |
| Q3 | `docs/reference/FR_NFR.md:174` | E |
| Q3 | `docs/reference/FR_NFR.md:179` | E |
| Q3 | `docs/reference/FR_NFR.md:316` | E |
| Q3 | `docs/reference/FR_NFR.md:322` | E |
| Q3 | `docs/reference/FR_NFR.md:407` | E |
| Q3 | `docs/reference/FR_NFR.md:415` | E |
| Q3 | `docs/reference/FR_NFR.md:520` | E |
| Q3 | `docs/reference/FR_NFR.md:557` | E |
| Q3 | `docs/reference/FR_NFR.md:558` | E |
| Q3 | `docs/reference/FR_NFR.md:560` | E |
| Q3 | `docs/reference/FR_NFR.md:561` | E |
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
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:178` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:255` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:276` | H |
| Q4 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:279` | H |
| Q4 | `docs/reference/FR_NFR.md:162` | E |
| Q4 | `docs/reference/FR_NFR.md:176` | E |
| Q4 | `docs/reference/FR_NFR.md:201` | E |
| Q4 | `docs/reference/FR_NFR.md:300` | E |
| Q4 | `docs/reference/FR_NFR.md:314` | E |
| Q4 | `docs/reference/FR_NFR.md:316` | E |
| Q4 | `docs/reference/FR_NFR.md:402` | E |
| Q4 | `docs/reference/FR_NFR.md:403` | E |
| Q4 | `docs/reference/FR_NFR.md:405` | E |
| Q4 | `docs/reference/FR_NFR.md:429` | E |
| Q4 | `docs/reference/FR_NFR.md:558` | E |
| Q4 | `docs/reference/FR_NFR.md:560` | E |
| Q4 | `docs/reference/FR_NFR.md:566` | E |

## Gate table and environment

All final commands must name the candidate head in their log header.
The full docs workflow is the union of the bank and D entries, plus imported
and no-git checks. Independent processes run concurrently with individual logs
and rc files; no test output is piped. Vendor analysis is explicitly skipped. Builder gate 11 calibration has no
verdict because the historical mf48 placement-utilization report is absent.
The full builder completed in 1144.53 seconds, rc 0, with that one NOT RUN arm.
The long process ran in the background while foreground waits stayed under a minute.
No runtime simulation build, synthesis, board or bench operation is performed.

Python gate dependencies were installed in scratch from both hash-locked files,
plus PyYAML and wavedrom 2.0.3.post3. Verilator is 5.050; sv2v is pinned 0.0.12.
The builder uses the existing canonical RV32 GCC 14.3.0 selector and LiteX
environment. A separate fresh SDK install verifies the repository-pinned archive
through its repository installer.
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
| B44 | `git diff --check 423ac5d910d09ab189b3acc39ae3ae1d10d50b19 a27808375427859dc357f6bfd0a88842062b20ed` | 0 | PASS |
| B45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | PASS |
| B46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | PASS |
| B47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | PASS |
| B48 | `python3 sw/builder/test_builder.py --require-rv32` | 0 | PASS; gate 11 calibration NOT RUN because the mf48 placement-utilization report is absent |
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
| D22 | `python3 scripts/ci_rv32_sdk.py --destination $CHECK_ROOT/rv32-sdk` | 0 | PASS |
| D23 | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | PASS |
| D24 | `python3 sw/builder/test_firmware_compiler.py --absent --audit $CHECK_ROOT/rv32-absent.jsonl` | 0 | PASS |
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
| N01 | `python3 scripts/docs_check.py` | 0 | PASS; committed export without git metadata |
| N02 | `python3 scripts/check_feature_status.py` | 0 | PASS; committed export without git metadata |


The final HDL reference generator first refused a nonempty preliminary output
directory. That directory was retained separately and generation was rerun into
a fresh empty destination, without changing the gate.

Preflight corrections: regenerated the control README contents after moving new
scope paragraphs outside their contents blocks; split the integration guide's
paragraph to meet its 20-word rule. Final trace review separated solicited
GET_COUNTERS latency from unsolicited counter spacing in FR-CTRL-04. This is
included in the approval table and committed separately without amend.
The preliminary long checks were interrupted when the final requirement correction
required a fresh committed-head run. Preliminary validation is not substituted
for the final run; its logs remain separately in scratch.

## Artifact receipts

Logs, SDKs, parser packages, text extractions and exported trees remain in
scratch. Large artifacts are recorded by size and SHA-256, not copied here.
`CHECK_ROOT` below denotes the scratch directory supplied for this assignment.

| Artifact relative to CHECK_ROOT, unless marked standard | Bytes | SHA-256 |
|---|---:|---|
| `contradiction-hits.json` | 346438 | `7c4bd9df2d11f6e368ce4aa5303aee2faf69df147450f81d8be9e4e769f2f120` |
| `contradiction-head.json` | 309249 | `de6ece20b3ba0478994ade6d24b13315b0737c93eba0abd54ba2d629d398fd9a` |
| `manifest.json` | 10986 | `f683d495b5ffffdd7e29e82bf248bf7ac7c2e503d4e8fd1f05d2aa3f47370515` |
| `final-results.json` | 16173 | `5b73f949424a2964627c2608b44f32bedea29e0bea274c636c0f226f24b09b2f` |
| `head.tar` | 32880640 | `b660dab36c85b452d573102263dabc1fef9aa845e039f6a2824afb08a6c64e6e` |
| `sv2v-v0.0.12.zip` | 2168551 | `ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00` |
| `rv32-present.jsonl` | 1718427 | `2cac09adbb83ab60bb0abd808d857fea237af40e0a9b42013c294e4a3a1eb9ad` |
| `rv32-absent.jsonl` | 2021 | `457108d27fd4fa1f877ba0d43ec8324a9ce8d7490732eecdc9c318d3e504b657` |
| `hdl-reference/index.html` | 1259098 | `082c2fd78450897327abf51f7148d070bf16a950a2b95840579db98916fb0389` |
| `gates/B01.log` | 3792 | `c2227f08211977791e84550471d45663a3cf98f1a5ad66969ee25eaba7bdd99b` |
| `gates/B02.log` | 1156 | `51fadba0ed9426e8d72f3a382fe4fddfad70bd1744de09f4e9aaa7f687621857` |
| `gates/B03.log` | 15091 | `10273190da744f9f2e9894a7c1199b00ad80cacddb95ec24c4e22ccbd631ada1` |
| `gates/B04.log` | 1464 | `022c45ccc842af4485581d649e67d22fb02cf5ad5026462ccac13265def4ab41` |
| `gates/B05.log` | 356 | `8ed4e037d4cb29122ab192f901270ea3a3b9e2b27cef42193b5c3a243c601169` |
| `gates/B06.log` | 6708 | `0a6a633087cb0e630bb576dc4eb5df231ebf291ffad73f42f5aee6e13cef173e` |
| `gates/B07.log` | 142482 | `f4ec0721b9ec2530a2ca8f49c47272e088b86171b8faced0ebcb8052ed9a0840` |
| `gates/B08.log` | 325 | `ca6b5aad7aea16de15306315ea3e2a369b3b0c605e7e629b6664a594554554ad` |
| `gates/B09.log` | 218 | `bcc5d1e37c8b71edb161fa5a282578d1f776729efe13f1c424ea59561d034954` |
| `gates/B10.log` | 236 | `4fd563cdd0ddf4656e1252aad93b2fd2683defc4bf3f8e984f198432472b28e3` |
| `gates/B11.log` | 499 | `01118ed2e95c34e5c6e5e374938d5c18a925009a8b99aa4953f82b801d3564d8` |
| `gates/B12.log` | 644 | `cbefeadff9631835923b8a6af273a0e004db1862af88bd4f2766c7f12d83109c` |
| `gates/B13.log` | 307 | `56af7ce285d1a4cbbcfc057c3c163259a723f3b061587aa93411949c66d31139` |
| `gates/B14.log` | 231 | `8417a80370f3dabe70e5a39bac78830455440eb487c7bccfb4a174c25bcc22c0` |
| `gates/B15.log` | 231 | `88eff0fb556f6ebe9a54e8f858a233b61b5cb3d9a3123d057f9947c160465914` |
| `gates/B16.log` | 275 | `7a9a2efc95431af57b6f6933356a7bea69a940cad35b471e8e580f0b8397962a` |
| `gates/B17.log` | 269 | `5c9885c43e1050f1a83432293db756960d8fd28fd2870ab9fde8a062677ff097` |
| `gates/B18.log` | 275 | `f8b16a4816096a242e542ab77e03b892dfa1778495ac0834348feebb2367d511` |
| `gates/B19.log` | 260 | `5fc6859dd9602754ef2fe06f8d83943bc47b48c3be4ae97692fae5f96584768a` |
| `gates/B20.log` | 281 | `7d6027e58c079a871ca1fcc32c8ac0060664e4825d6a26463567b91ca0715e44` |
| `gates/B21.log` | 2191 | `e43bf518e8ff01917806740ef1eebe46dc99d39a944d7e8e4701be4fb086b551` |
| `gates/B22.log` | 350 | `b26acf40c70cc8582b5a7b10d9e5417187db9114b6686237cd447311d459cd49` |
| `gates/B23.log` | 401 | `13e955cc1d47c4d4f106f9ebf2e64f9982012b50ab59039bdf7a2f81f2ac223b` |
| `gates/B24.log` | 418 | `9809adb738dfb189b32685889ec1105fa2b44bdd7026f662414d8c8a931c923d` |
| `gates/B25.log` | 344 | `90f5fd356325bd63744aabaa85a3db1ae1c06abacafaaf231848850b8787d3a2` |
| `gates/B26.log` | 271 | `a75cfd18d1216220595c5dcae9340d7e8021764117c3548eaf3b2de1756c9a45` |
| `gates/B27.log` | 610 | `b51c55e89fb03041c29100db077373661f3bc286a47056a5986c35660e27616e` |
| `gates/B28.log` | 2769 | `51347d307b668541aa3b2cd3af6b8f040432645f04947ab67fe73cdf05b7bcf3` |
| `gates/B29.log` | 272 | `d684892f7d328993575dac40a606cbab070e3e25a6e58648584b4d1cee2b4ea8` |
| `gates/B30.log` | 246 | `8f1fb6f7dee1d92c8d377358e09232fb50ee2f0f5e20b47ab449fdbc4fbe0247` |
| `gates/B31.log` | 5407 | `f8589f7e2338a82c2d5bcb234cfdfc0f33d8a41daef2a89a2f65e014090146d1` |
| `gates/B32.log` | 19895 | `9292e8d6a032f02fe849413121a507b224862d47453e71274bb7819adee66f46` |
| `gates/B33.log` | 731 | `56a7931b2d6a064197bed884601b089ea48c68375c45a79814dd6e6903346a4d` |
| `gates/B34.log` | 2768 | `92aad8f81c1a9b5c1fca3619cee1524fd504abd8d837352771589b0163187e05` |
| `gates/B35.log` | 927 | `323a731b346b114dc729cf0b22e394dd2d658bde4a62f14821f0a1be536dee90` |
| `gates/B36.log` | 377 | `bc0f94ac8b63fa9e1366881c2925cee3e27f3c05c86302a483e93be7cef2e6bb` |
| `gates/B37.log` | 6282 | `42406fdbc2368fc9113f54affb9e3a428fe82ebcedc12bfdd439f08b99fe8baa` |
| `gates/B38.log` | 14427 | `c427d3c4de44a1c48ab36d486d976e813811af2f79c1c1eff2c58eed76885d17` |
| `gates/B39.log` | 36802 | `23be6fdeb8f784fb2cb5e2092622cc7a986797a93a8255af4b4d768f26842a7f` |
| `gates/B40.log` | 5863 | `d6639041e4c8a77d05e3b0f4f5e89236805a66f07ce219b69b4aed88d4d0afd3` |
| `gates/B41.log` | 228 | `8fea0e1735adad2a116df7243f744e14d7b47db34a472c3df888e1f2c3e54cba` |
| `gates/B42.log` | 238 | `1cc452119b36006e4f7b8ad5f9cb4b95bd3f0f5bb2e27391c38027154567e019` |
| `gates/B43.log` | 249 | `341c6a4ec4752d08062e67a714c9873f1f0e62c67612dd5e65b9c05c1f5747b8` |
| `gates/B44.log` | 220 | `2680ed039345a2742972474a70872cd0d6bdf179bcae7029ae29e0e1d83abfb6` |
| `gates/B45.log` | 5174 | `569088e877a24f9a2e403b7651775b840d652d07ee0ec6fdcf79776210bf5814` |
| `gates/B46.log` | 25899 | `cf787d6c66ffc05d3838a1c5911c7b3cdd8d7ad74bd83f5d48ddf5e7199b95ed` |
| `gates/B47.log` | 9478 | `c29e21dd015516541c62b34d74ae10cc6f0f99f1937f57da6f06a40e4b4fd3e5` |
| `gates/B48.log` | 102190 | `92d176d199f4395f04889669270314989286a04f993be7ba63e78317a9856127` |
| `gates/D01.log` | 614 | `f85d53d1f5d7d71dbb6ecaac32881371aab6181cd286404cb15d6af6336f245e` |
| `gates/D02.log` | 638 | `e7743c7f8927f6b50faec76c3dfc17ad26ee043ef9b2b3e5891bed617ffc6b50` |
| `gates/D03.log` | 225 | `fcad0bdc297e51eae6eb7be6361f9f7a299cc6acbfd6359589f97cf06614d37a` |
| `gates/D04.log` | 244 | `4b1bb08fc85ec5acd2d7d2edf1efd47ecbddb8522a3e5150671274424e515a71` |
| `gates/D05.log` | 249 | `351b97e75708a6fd81e44129faf6f037f59a1ac58fe562e7d334a0530ba90309` |
| `gates/D06.log` | 251 | `f5b0e31d2a107a0efbcabd09c718cf25b17a6512c65a7db2d00045fde248bb65` |
| `gates/D07.log` | 264 | `26c6fb8ee798c7d0edcd94df1601b2bc00315b4ff86ff80700ac7a1e8f2092f3` |
| `gates/D08.log` | 268 | `86ad1a98748436efbc119ae2497180cdfc8ef55204f6f869312e8989dfdc02c5` |
| `gates/D09.log` | 261 | `f80ec410b86a7d00aa90a6b4a1b48c171d608c3ce36fff035fb91a444ea57bc8` |
| `gates/D10.log` | 264 | `b87aeef5473380d03bc1889c29535ec467543c134a87214dbcd08b83520cc147` |
| `gates/D11.log` | 273 | `37a1dd441f9c4e4da966b79d8543b8eaa603cadb73dc77f5165e294e344868ca` |
| `gates/D12.log` | 269 | `e3dc1c970dbcb76781cff75e06f5fd1034da5c54aa600d40326e213c72f2e618` |
| `gates/D13.log` | 272 | `361ffa3fcb1ee73c84462fe5f192da1efbebe5048364e6bf56ec400bf6acef1d` |
| `gates/D14.log` | 315 | `18fe1b2c09ebdb6dc16bb2d69729546a2ad2d801ec127e0785288779bbeaeb0c` |
| `gates/D15.log` | 307 | `0705847498977d0d8a8cc4142c33522206f64e507e21fc4dcd6bff2ee6039ca1` |
| `gates/D16.log` | 303 | `9fec74277408a03aa999e0dc900f5094f9b475ae2fae22242bbd0e37cd86e6e7` |
| `gates/D17.log` | 253 | `71ec20faa17946836e79ed5132a9281cdbf16e079bf50a0c7f3d0c4121ebca30` |
| `gates/D18.log` | 260 | `81b8d8f5f5727edac2e1fd759f1e69c17afba4b9fd107f32f9f29f40259f653a` |
| `gates/D19.log` | 1704 | `565ae87c11d813cfd50bcd5f50cdb3aa83d5a818d09f52fea461a1ed401e607f` |
| `gates/D20.log` | 270 | `8dc9d4365aab90eb08fe599bb02691581097c66a9b77d73639ba1db928d6ef38` |
| `gates/D21.log` | 6557 | `0afebe212c17f8cb6270905ae39a0d3e68f8371257bef53b427be645178b79e9` |
| `gates/D22.log` | 1719 | `406df5e301f53d979923cb3f6d79e516539adce1bcfc7689952e2a09c4510176` |
| `gates/D23.log` | 346 | `992ec7bfc71935ebc64c896f087deb30d6bd3329046682949d2ecf8dc1aa868f` |
| `gates/D24.log` | 50790 | `01f700c4c6af27f329b0b6a2c50ed29f0785afc3f1d33667b88a50bc8bce5a2b` |
| `gates/D25.log` | 7216 | `5a52528a31e4795f9cd965431ffc167a9a58da07a6506bd020b9f79e1e62563c` |
| `gates/D26.log` | 510 | `7428f3b461bff48fd188ba6f43f1b27f84675f31268862e8e442ed4db1e25fe7` |
| `gates/D27.log` | 1701 | `3f1f7c18ee175afbc38a9a9b91afc50bb8c4a8b2958d77700a0264a8348f0083` |
| `gates/D28.log` | 3334 | `9237f12e0573b84b9509354ed064f8ebf01b5fadcb5673dd523fc926e718fcec` |
| `gates/D29.log` | 3505 | `45700462b2b353677fcef5132f7516b9cfe41a14375166f6175daf2c291bedad` |
| `gates/D30.log` | 4223 | `90da31b13e108930f5f9ae849a50641919a1251d56690ab901117ea618874264` |
| `gates/D31.log` | 4822 | `721b1dbfaf55a122344a2be5f0c3ea94a80134f9b47448f4b8a60a716ed0c680` |
| `gates/D32.log` | 6797 | `322c8bab6e301062f59ae78c38640229d841e64376c6f3230fde7f755d2f6826` |
| `gates/D33.log` | 2787 | `51f7f1a3f84e4e38428e0f2a9a103d9306a5f78bea1941a4a8e501223b34cc1a` |
| `gates/D34.log` | 2043 | `a6768ac8dd4902b0bff27a524ce5b4996436714edb67b01690540b24b57ff5d9` |
| `gates/D35.log` | 3152 | `991477da667fbc1b7f15d999ddc72bcd4534eaadd68af6d83699fcc7462c1616` |
| `gates/D36.log` | 3791 | `c003f255ce7f4ff750675eb8c258f913b2cead519f79c1b7e45ec52cfbda0ff0` |
| `gates/D37.log` | 2728 | `5c0014f3e2459fc154fe1d3b8a87b2c4ee427ea07947d337940cfe663d0359be` |
| `gates/D38.log` | 2658 | `c77e1ae57a07e740ad70346d2b68007f33a1872de8dc33afc8a8b9872c62e99e` |
| `gates/D39.log` | 37104 | `19e95332511ca5cddff136505097318b0a735057aca1ff96583110ee3cd68b9f` |
| `gates/D40.log` | 231 | `35a13a1dc5e189504bf9d6ed5f75f0fdae53e8dab39f97a53cd97780fbfde5fe` |
| `gates/G01.log` | 2822 | `e673e4bd8b62a2ee318ebee2d78ad07bc5d9cc1cd2cdb58b05865aeb9aaca2bc` |
| `gates/N01.log` | 374 | `56b5864bd2f68a11ab031b41d84b7bb465894f25cf85f5126d4d6d5428b560c6` |
| `gates/N02.log` | 217 | `e2447aae38ddcb97897527857b9419526593bb6a4294e36d262230bb876ecfbf` |
| `1722.txt` | 796018 | `f8725b4553a4afdecfc1adf888c7fc7ca44a14d67056b4836a151eb177caf40d` |
| `17221.txt` | 1677147 | `966138f9a20368c94ee24456ca485b69956777f3821adf0b1d019685dd1c8a9a` |
| `8021q.txt` | 7753051 | `1adf223299e6529dcb84de235addd0c5a67136bce9127f15718aecb41943313e` |
| `milan.txt` | 387172 | `8264854244415e364e1968b1da8e2bae7c067fa3cc98594ea54db08fc8a152c7` |
| `rv32-sdk/.milan-rv32-sdk.json` | 789637 | `6c6ba8a0988aa284f0897fd3bcbb310d1bdcec5a1379f7208a1f753cbce76b8b` |
| `dependencies.log` | 1322 | `8b626d7f98c0f1a376534ec300e4d3a210989e3c5f089970a50831d4f054142b` |
| `dependencies-extra.log` | 788 | `ab28fa6af8e337e3ddbb416f010e556753aca3c3604796c56cff8a5710fef4af` |
| Pinned SDK archive | 102597892 | `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f` |
| Standard: `Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf` | 1684588 | `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8` |
| Standard: `1722.1-2021.pdf` | 5494661 | `ad7b822008c1b78bce8af1470f1ace177a22344aa48c0da939066d6db9a65b9c` |
| Standard: `1722-2016.pdf` | 7354196 | `ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c` |
| Standard: `802.1Q-2018.pdf` | 18576069 | `55268b5f716aee085c3357a4cba398602d9f0cb340fe3d8a70de40fac58ed956` |

## Acceptance and remaining work

Document scope, ownership, normative citations, the proposed service budget,
seven test hooks, traceability, contradiction dispositions and version landing
plan are present. The owner must approve the exact text before merge.
Independent internal and external reviews must reconstruct the task from public
state. Their lens ledger is not supplied by the executor. The manager handles
publication, hosted evidence, candidate-merge validation and post-merge work.

Final status message: `[A548] REVIEW READY` with the candidate head above.
See issue #664 for the public handoff comment. The manager must retain the
validation limitations and pending owner approval when preparing the PR.
Final worktree status is clean; all changed tracked files are Markdown.
