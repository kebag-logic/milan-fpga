[A548]

# Issue #664 round-3 handoff

## Status and identity

Candidate: `4dab80ae4564ef8d6e1030564dcea4ba19235ee6` on `664-mark2-reqs`.
Original assigned base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Approved round-2 head: `8fb296e3e02985aee27ef04cb08278836b734a14`.
Current-dev validation base: `30e3c018b9add0cb182d8f1229eeec062218130d`.
Required no-fast-forward merge: `f48d47cd93cc4b46fad3e537dee661fc2cd3ee6d`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
All 93 command exits are zero. Vendor analysis is skipped; historical placement calibration is not measured.
Executor [A548]; independent reviewers [R508] and [R509].
TAKEN: issue #664 comment 6014361171.

## Scope and decisions

The authored round-3 delta changes three Markdown files only.
It extends product ownership, NFR-SCOUT-02 and five filter hooks, adds
NFR-SCOUT-08 and its mailbox-contract trace, and distinguishes current F0
behavior from the required later filter. Every timing row is unchanged.
The complete lane remains 21 Markdown files relative to current dev.

The owner approved the prior text and 10 ms value at 8fb296e3.
R508-2 and R509-2 were positive at that earlier head; they do not approve
these additions. R509-2-R1 remains a manager wording-residue item:
the saved-state README's stale F0 publication bullet is outside this round.

The required dev merge incorporated 30e3c018 because it touched
docs/ENDSTATION_BUILDER.md and docs/fpga/DATAPLANE_WALKTHROUGH.md.
It completed without conflicts. Imported executable changes belong to dev;
all non-documentation entries remain identical to that dev tree.
No executable, test, firmware, mailbox YAML or VERSION change was authored.
The two round-3 commits have one-line subjects and no body or trailers.
No push, PR edit, rebase, amend, hardware access or release merge occurred.

## Clause confirmation and interpretation

The absent docs/spec-refs.md is already acknowledged by ruling 6009675758.
The pinned processor extracts were searched first: the ACMP architecture
page, section 3, says responses use 91-E0-F0-01-00-00. Its text does not
settle every command. The root 802.1Q trace lacks Table 10-1's address row.
The direct standards supplied those two missing statements.

| Check | Primary clause and text | Disposition |
|---|---|---|
| MVRP address | IEEE 802.1Q-2018 Table 10-1, printed page 256, PDF page 257: "Customer Bridge MVRP address" = "01-80-C2-00-00-21" | Matches decision 6014311316. |
| ACMP addressing | IEEE 1722.1-2021 8.2.1, printed/PDF page 338: "All ACMPDUs are transmitted to the ACMP multicast destination MAC address defined in Table B.1." | Transmission is multicast. The owner explicitly permits own-unicast reception as a tolerance; no normative unicast transmission is claimed. Retain the receive tolerance as specified. |
| AECP reply | Milan v1.2 5.4.5.3; processor AECP architecture section 7 describes a matching response rearming the monitor | Own-controller responses must reach the core even with a different target_entity_id. H-AECP exercises both positive and negative directions. |

The ACMP transmission rule does not contradict a labelled receive tolerance.
Neither confirmation requires changing the owner's table; no STOP condition arose.
MSRP/MVRP have no AVTP subtype. H-SRP rejects AVTP substitutions while
preserving valid MRP payload bytes as data, not invented subtype fields.

| Standard file | Bytes | SHA-256 |
|---|---:|---|
| 1722.1-2021.pdf | 5494661 | `ad7b822008c1b78bce8af1470f1ace177a22344aa48c0da939066d6db9a65b9c` |
| 802.1Q-2018.pdf | 18576069 | `55268b5f716aee085c3357a4cba398602d9f0cb340fe3d8a70de40fac58ed956` |

Licensed documents and full extracts are not included in these deliverables.

## Round-3 changed rows: old -> new

Everything outside the filter delta below is **approved at 8fb296e3**,
including `T_svc = 10 ms`, under owner approval 6014321497.
The prior wording that calls the budget proposed is preserved verbatim.
No timing bound, placement rule or VERSION text is reopened here.
The manager checks these additions against owner decision 6014311316.
The old/new cells reproduce the source text; link labels and table escaping
are presentation only. No unchanged requirement row is included.

| Row or filter passage | Old at 8fb296e3 | New at candidate |
|---|---|---|
| REQUIREMENTS section 1: fabric ownership bullet | - The fabric MUST retain framing, timestamps, the ingress filter,<br>  the gPTP plane, and the AVTP/AAF/CRF and physical-media paths.<br>  Audio and gPTP deadlines MUST remain independent of firmware service.<br>  Reservation protocol control follows its selected placement.<br>  Media admission enforcement and any shaping remain in fabric. | - The fabric MUST retain framing, timestamps, the ingress filter,<br>  the gPTP plane, and the AVTP/AAF/CRF and physical-media paths.<br>  Audio and gPTP deadlines MUST remain independent of firmware service.<br>  Reservation protocol control follows its selected placement.<br>  Media admission enforcement and any shaping remain in fabric.<br>  The mailbox ingress filter MUST enforce the acceptance rules below.<br>  Tagged frames MUST NOT reach any mailbox.<br>  Each channel MUST match its full tuple, then its identity term.<br>  Own unicast means the receiving AVB interface's MAC only.<br>  AECP MUST accept own-target commands or own-controller responses.<br>  Untagged control frames failing their tuple MUST increment `FILTER_MISMATCH`.<br>  Per-channel token buckets MUST remain in force. |
| REQUIREMENTS section 1: filter table scope | Absent | **Mailbox ingress acceptance (NFR-SCOUT-08).**<br>The owner filter decision<br>requires this exact channel table.<br>Each row matches VLAN tag, destination MAC, EtherType and subtype.<br>The identity term then restricts which matching frames are delivered.<br>All rows require untagged frames; tagged frames retain the fabric path.<br>AAF/CRF media use the SR class VLAN and have no mailbox channel.<br>Stray untagged AAF/CRF frames therefore cannot reach the core either. |
| Ingress tuple: `adp` | Absent | &#124; `adp` &#124; absent &#124; `91:E0:F0:01:00:00` &#124; `0x22F0` &#124; `0xFA` &#124; ENTITY_DISCOVER for entity_id 0 or own; F3 adds bound talkers' ENTITY_AVAILABLE/ENTITY_DEPARTING &#124; |
| Ingress tuple: `acmp` | Absent | &#124; `acmp` &#124; absent &#124; `91:E0:F0:01:00:00`; own unicast as a receive tolerance &#124; `0x22F0` &#124; `0xFC` &#124; talker_entity_id or listener_entity_id = own &#124; |
| Ingress tuple: `aecp` | Absent | &#124; `aecp` &#124; absent &#124; own unicast MAC on the receiving AVB interface &#124; `0x22F0` &#124; `0xFB` &#124; (command AND target_entity_id = own) OR (response AND controller_entity_id = own) &#124; |
| Ingress tuple: `maap` | Absent | &#124; `maap` &#124; absent &#124; `91:E0:F0:00:FF:00` &#124; `0x22F0` &#124; `0xFE` &#124; overlaps own range &#124; |
| Ingress tuple: `srp` MSRP | Absent | &#124; `srp` MSRP &#124; absent &#124; `01:80:C2:00:00:0E` &#124; `0x22EA` &#124; not applicable &#124; all &#124; |
| Ingress tuple: `srp` MVRP | Absent | &#124; `srp` MVRP &#124; absent &#124; `01:80:C2:00:00:21` &#124; `0x88F5` &#124; not applicable &#124; all &#124; |
| REQUIREMENTS section 1: filter rules and clause authority | Absent | A frame failing its tuple or identity term MUST be dropped.<br>A different unicast destination MUST NOT reach the core.<br>The record's interface index selects the own-MAC comparison.<br>This preserves the future redundancy seam without enabling that feature.<br>Control EtherTypes here are `0x22F0`, `0x22EA` and `0x88F5`.<br>An untagged frame with one failing its tuple increments `FILTER_MISMATCH`.<br>Tagged frames stay outside this counter's untagged-control definition.<br><br>IEEE 802.1Q-2018 Table 10-1 assigns the Customer Bridge MVRP address.<br>IEEE 1722.1-2021 8.2.1 requires multicast transmission of all ACMPDUs.<br>Table B.1 assigns that multicast address.<br>Own-unicast ACMP reception is the owner's tolerance, not normative transmission.<br>Milan v1.2 5.4.5.3 requires the CONTROLLER_AVAILABLE liveness exchange.<br>Its response must pass the own-controller AECP term.<br><br>The filter requirement<br>traces this table to the mailbox YAML and acceptance hooks.<br>The contract lane after FT implements these additions before F2 to F5.<br>F0's current filter is described in the mailbox design. |
| NFR-SCOUT-02 | &#124; NFR-SCOUT-02 &#124; ADP, ACMP, AECP (including unsolicited notifications and counter serving), MAAP and SRP MUST each be build-selectable between bare-metal firmware and fabric. Mark II defaults to firmware; all-fabric remains supported and the shipping default until F2 to F5 pass suites and bench acceptance for all streams, counters and audio soak. Each function MUST have one state owner. Framing, timestamps, ingress filtering, gPTP and media MUST remain fabric-owned. &#124; M &#124; A &#124; | &#124; NFR-SCOUT-02 &#124; ADP, ACMP, AECP (including unsolicited notifications and counter serving), MAAP and SRP MUST each be build-selectable between bare-metal firmware and fabric. Mark II defaults to firmware; all-fabric remains supported and the shipping default until F2 to F5 pass suites and bench acceptance for all streams, counters and audio soak. Each function MUST have one state owner. Framing, timestamps, ingress filtering, gPTP and media MUST remain fabric-owned. The mailbox filter MUST exclude tagged frames, match each channel's exact VLAN-tag/destination-MAC/EtherType/AVTP-subtype tuple, then apply its identity term. Own unicast MUST mean the receiving AVB interface's MAC, never any unicast. AECP MUST accept (command AND target_entity_id = own) OR (response AND controller_entity_id = own). Untagged control frames failing their tuple MUST increment FILTER_MISMATCH. Per-channel token buckets MUST remain; NFR-SCOUT-08 defines the table and checks. &#124; M &#124; A &#124; |
| NFR-SCOUT-08 | Absent | &#124; NFR-SCOUT-08 &#124; The fabric mailbox ingress filter MUST enforce the exact tuples and identity terms in product ownership, including tagged-frame exclusion, per-interface own unicast, both AECP directions and FILTER_MISMATCH for untagged control tuple failures, while retaining per-channel token buckets. The single-source mailbox contract MUST carry these rules. Verify with H-ADP, H-ACMP, H-AECP, H-MAAP and H-SRP in Section 3.4.2, including planted filter defects through both bus adapters and the host mailbox model. &#124; M &#124; A,I,T &#124; |
| H-ADP | &#124; H-ADP &#124; FR-DISC-01..05; NFR-SCOUT-01..03 &#124; ADP `RX_HEAD` commit or startup/GM/link/shutdown occurrence; timer arm and original deadline; AVAILABLE/DEPARTING `TX_HEAD` commit and wire departure &#124; Startup, DISCOVER, periodic, GM, both link edges, shutdown/restart; full rings; zero/max draws; ignored events and stale tags; DEPARTING before AVAILABLE &#124; | &#124; H-ADP &#124; FR-DISC-01..05; NFR-SCOUT-01..03; NFR-SCOUT-08 &#124; ADP `RX_HEAD` commit or startup/GM/link/shutdown occurrence; timer arm and original deadline; AVAILABLE/DEPARTING `TX_HEAD` commit and wire departure; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH &#124; Startup, DISCOVER, periodic, GM, both link edges, shutdown/restart; full rings; zero/max draws; ignored events and stale tags; DEPARTING before AVAILABLE; tagged-frame, wrong-destination and wrong-AVTP-subtype rejection; FILTER_MISMATCH count. &#124; |
| H-ACMP | &#124; H-ACMP &#124; FR-CONN-01..04; NFR-LAT-02; NFR-SCOUT-01..03 &#124; ACMP `RX_HEAD` commit to the matched response `TX_HEAD`; originated command commit to response receipt; discovery/probe timer deadline to its action &#124; Each Table 5.26 command, success/refusal, retry, distinct sequence/unique IDs, restore and fast connect; wire round-trip < 200 ms with margin &#124; | &#124; H-ACMP &#124; FR-CONN-01..04; NFR-LAT-02; NFR-SCOUT-01..03; NFR-SCOUT-08 &#124; ACMP `RX_HEAD` commit to the matched response `TX_HEAD`; originated command commit to response receipt; discovery/probe timer deadline to its action; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH &#124; Each Table 5.26 command, success/refusal, retry, distinct sequence/unique IDs, restore and fast connect; wire round-trip < 200 ms with margin; tagged-frame, wrong-destination and wrong-AVTP-subtype rejection; FILTER_MISMATCH count; own-unicast receive tolerance and foreign-unicast rejection. &#124; |
| H-AECP | &#124; H-AECP &#124; FR-ENUM-01/02; FR-CTRL-01..06; FR-MVU-01..03; NFR-SCUP-04; NFR-LAT-02 &#124; AECP `RX_HEAD` commit to matched response `TX_HEAD`, plus received-command and emitted-response wire observations &#124; AEM/MVU, descriptors, getters/setters, counters and refusals; longest image/state access; locks; malformed/truncated requests; response <= 240 ms with margin &#124; | &#124; H-AECP &#124; FR-ENUM-01/02; FR-CTRL-01..06; FR-MVU-01..03; NFR-SCUP-04; NFR-LAT-02; NFR-SCOUT-08 &#124; AECP `RX_HEAD` commit to matched response `TX_HEAD`, plus received-command and emitted-response wire observations; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH &#124; AEM/MVU, descriptors, getters/setters, counters and refusals; longest image/state access; locks; malformed/truncated requests; response <= 240 ms with margin; own-target commands and own-controller responses pass; CONTROLLER_AVAILABLE response reaches the core (Milan v1.2 5.4.5.3), while a response for another controller_entity_id is dropped even when target_entity_id = own; a foreign-target command is dropped even when controller_entity_id = own. Reject another interface's unicast MAC and a foreign destination. &#124; |
| H-MAAP | &#124; H-MAAP &#124; FR-MAAP-01; NFR-SCOUT-02/03 &#124; MAAP `RX_HEAD` commit or original timer deadline to PROBE/DEFEND/ANNOUNCE `TX_HEAD`; state completion when no frame is required &#124; Conflict in each state, three probe retransmissions, allocation loss/retry, strict probe/announce intervals, ring stalls and boundary draws &#124; | &#124; H-MAAP &#124; FR-MAAP-01; NFR-SCOUT-02/03; NFR-SCOUT-08 &#124; MAAP `RX_HEAD` commit or original timer deadline to PROBE/DEFEND/ANNOUNCE `TX_HEAD`; state completion when no frame is required; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH &#124; Conflict in each state, three probe retransmissions, allocation loss/retry, strict probe/announce intervals, ring stalls and boundary draws; tagged-frame, wrong-destination and wrong-AVTP-subtype rejection; FILTER_MISMATCH count. &#124; |
| H-SRP | &#124; H-SRP &#124; FR-SRP-01..03; FR-CONN-02; NFR-SCOUT-01..03 &#124; SRP `RX_HEAD` commit or fabric timer deadline to MRPDU `TX_HEAD`; registrar/state-apply commitment for non-transmitting transitions &#124; MSRP/MVRP joins, withdrawal, malformed vectors, LeaveAll/periodic expiry, coalesced tick backlog, reservation/licence updates; JoinTime and LeaveTime bounds &#124; | &#124; H-SRP &#124; FR-SRP-01..03; FR-CONN-02; NFR-SCOUT-01..03; NFR-SCOUT-08 &#124; SRP `RX_HEAD` commit or fabric timer deadline to MRPDU `TX_HEAD`; registrar/state-apply commitment for non-transmitting transitions; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH &#124; MSRP/MVRP joins, withdrawal, malformed vectors, LeaveAll/periodic expiry, coalesced tick backlog, reservation/licence updates; JoinTime and LeaveTime bounds; tagged-frame and wrong-destination rejection for MSRP and MVRP; wrong AVTP subtype cannot select srp; FILTER_MISMATCH count. MSRP/MVRP have no AVTP subtype field. &#124; |
| Section 3.4.2: common filter observations | Absent | The five filter hooks also start before mailbox publication.<br>Inject each table row's valid frame as a positive control.<br>Change tag, destination, EtherType, subtype and identity separately where applicable.<br>Rejected input MUST create neither an RX record nor core delivery.<br>Use an unassigned AVTP subtype for the wrong-subtype rejection.<br>Also inject untagged AAF and CRF; neither has a channel.<br>For MSRP/MVRP, test AVTP substitutions without inventing an MRP subtype.<br>Each untagged control tuple mismatch MUST increment FILTER_MISMATCH once.<br>Valid input and tagged input MUST NOT increment that counter.<br>Observe token-bucket enforcement separately from tuple and identity refusal.<br>AECP rejection cases must also test the opposite ID matching.<br>AECP acceptance cases use unrelated opposite IDs.<br>The response case includes the CONTROLLER_AVAILABLE liveness reply.<br>Repeat own-MAC checks for each configured AVB interface and record index.<br>Plant each acceptance-rule defect; require its named hook to fail.<br>These additions await the contract lane after FT, before F2 to F5. |
| Trace summary: Mailbox ingress filter | Absent | &#124; Mailbox ingress filter &#124; NFR-SCOUT-02/08 &#124; 5.4.5.3; IEEE 1722.1-2021 8.2.1/Table B.1; IEEE 802.1Q-2018 Table 10-1 &#124; mailbox YAML, per-interface MAC and entity identity &#124; Contract lane after FT, before F2 to F5; H-ADP/H-ACMP/H-AECP/H-MAAP/H-SRP &#124; |
| MAILBOX_SPLIT: current F0 filter scope | Absent | The following describes the implemented F0 filter.<br>NFR-SCOUT-08<br>and product ownership<br>add the owner's full-tuple acceptance rules and filter hooks.<br>They require per-interface own MACs and two-sided AECP identity matching.<br>Untagged control tuple failures must increment FILTER_MISMATCH.<br>The contract lane after FT implements these additions before F2 to F5.<br>Its YAML, generated outputs and filter tests must change together.<br>The command-only AECP term and uncounted refusals below describe F0 only.<br>They do not satisfy the added ingress requirement. |

## Cumulative requirement and traceability rows: old -> new

Original-base changes are recorded for completeness. Non-filter text is approved at 8fb296e3.

| Requirement row | Old at original base | New at candidate |
|---|---|---|
| REQUIREMENTS section 1 | - Bare-metal firmware owns boot policy, CSR initialization, identity,<br>  persistence orchestration, UART diagnostics, and remaining software-visible<br>  control.<br>- The fabric gPTP plane is the sole product PHC, protocol, servo, and public<br>  state owner.<br>- `GPTP_PLANE_EN_P=0` is verification-only hardware. It has no product image<br>  and zero runtime gPTP owners: GM, parent, PathTrace and peer delay are zero;<br>  sync/asCapable are zero; `tu` is one; retained writes are inert.<br>- The fabric owns per-frame classification, reservation, shaping,<br>  timestamping, AVTP/AAF/CRF, MAAP, and IEEE 1722.1 processing.<br>- Required Milan state must survive power loss. The current blank-flash NVM<br>  face does not satisfy this requirement and is the release blocker in #70. | - Bare-metal firmware owns boot policy, CSR initialization, identity,<br>  saved-state boot read/apply and write-back, and UART diagnostics.<br>- ADP, ACMP, AECP (commands, unsolicited notifications and counter serving),<br>  MAAP and SRP MUST each have build-selectable placement.<br>  The Mark II default places them on the bare-metal core.<br>  The all-fabric build remains a supported option.<br>  It remains the shipping default until F2 to F5 pass<br>  their suites and bench acceptance: all streams, counters and audio soak.<br>  Requirement approval precedes that default flip (#664, #665).<br>- The fabric gPTP plane is the sole product PHC, protocol, servo, and public<br>  state owner.<br>- `GPTP_PLANE_EN_P=0` is verification-only hardware. It has no product image<br>  and zero runtime gPTP owners: GM, parent, PathTrace and peer delay are zero;<br>  sync/asCapable are zero; `tu` is one; retained writes are inert.<br>- The fabric MUST retain framing, timestamps, the ingress filter,<br>  the gPTP plane, and the AVTP/AAF/CRF and physical-media paths.<br>  Audio and gPTP deadlines MUST remain independent of firmware service.<br>  Reservation protocol control follows its selected placement.<br>  Media admission enforcement and any shaping remain in fabric.<br>  The mailbox ingress filter MUST enforce the acceptance rules below.<br>  Tagged frames MUST NOT reach any mailbox.<br>  Each channel MUST match its full tuple, then its identity term.<br>  Own unicast means the receiving AVB interface's MAC only.<br>  AECP MUST accept own-target commands or own-controller responses.<br>  Untagged control frames failing their tuple MUST increment `FILTER_MISMATCH`.<br>  Per-channel token buckets MUST remain in force.<br>- Each selected function MUST have exactly one authoritative state owner.<br>  Both placements MUST preserve wire behavior, ordering and normative timeouts.<br>  Firmware service MUST satisfy NFR-SCOUT-03 and its path-specific hooks<br>  in the requirements register.<br>- Required Milan state must survive power loss.<br>  The shipping backend is partial; #70 remains a release blocker.<br>  F1 supplies the split store without integrating a shipping image.<br>  Its boot contract governs validation and apply.<br><br>**Mailbox ingress acceptance (NFR-SCOUT-08).**<br>The owner filter decision<br>requires this exact channel table.<br>Each row matches VLAN tag, destination MAC, EtherType and subtype.<br>The identity term then restricts which matching frames are delivered.<br>All rows require untagged frames; tagged frames retain the fabric path.<br>AAF/CRF media use the SR class VLAN and have no mailbox channel.<br>Stray untagged AAF/CRF frames therefore cannot reach the core either.<br><br>&#124; Channel &#124; VLAN tag &#124; Destination MAC &#124; EtherType &#124; AVTP subtype &#124; Identity term &#124;<br>&#124;---&#124;---&#124;---&#124;---&#124;---&#124;---&#124;<br>&#124; `adp` &#124; absent &#124; `91:E0:F0:01:00:00` &#124; `0x22F0` &#124; `0xFA` &#124; ENTITY_DISCOVER for entity_id 0 or own; F3 adds bound talkers' ENTITY_AVAILABLE/ENTITY_DEPARTING &#124;<br>&#124; `acmp` &#124; absent &#124; `91:E0:F0:01:00:00`; own unicast as a receive tolerance &#124; `0x22F0` &#124; `0xFC` &#124; talker_entity_id or listener_entity_id = own &#124;<br>&#124; `aecp` &#124; absent &#124; own unicast MAC on the receiving AVB interface &#124; `0x22F0` &#124; `0xFB` &#124; (command AND target_entity_id = own) OR (response AND controller_entity_id = own) &#124;<br>&#124; `maap` &#124; absent &#124; `91:E0:F0:00:FF:00` &#124; `0x22F0` &#124; `0xFE` &#124; overlaps own range &#124;<br>&#124; `srp` MSRP &#124; absent &#124; `01:80:C2:00:00:0E` &#124; `0x22EA` &#124; not applicable &#124; all &#124;<br>&#124; `srp` MVRP &#124; absent &#124; `01:80:C2:00:00:21` &#124; `0x88F5` &#124; not applicable &#124; all &#124;<br><br>A frame failing its tuple or identity term MUST be dropped.<br>A different unicast destination MUST NOT reach the core.<br>The record's interface index selects the own-MAC comparison.<br>This preserves the future redundancy seam without enabling that feature.<br>Control EtherTypes here are `0x22F0`, `0x22EA` and `0x88F5`.<br>An untagged frame with one failing its tuple increments `FILTER_MISMATCH`.<br>Tagged frames stay outside this counter's untagged-control definition.<br><br>IEEE 802.1Q-2018 Table 10-1 assigns the Customer Bridge MVRP address.<br>IEEE 1722.1-2021 8.2.1 requires multicast transmission of all ACMPDUs.<br>Table B.1 assigns that multicast address.<br>Own-unicast ACMP reception is the owner's tolerance, not normative transmission.<br>Milan v1.2 5.4.5.3 requires the CONTROLLER_AVAILABLE liveness exchange.<br>Its response must pass the own-controller AECP term.<br><br>The filter requirement<br>traces this table to the mailbox YAML and acceptance hooks.<br>The contract lane after FT implements these additions before F2 to F5.<br>F0's current filter is described in the mailbox design.<br><br>The split architecture defines both placements.<br>Major `0x0003` identifies only images running the split.<br>The major changes with the default-flip implementation, not this document change.<br>MINOR remains flat and continuous across majors.<br>The landing plan pins the simulations and firmware string.<br>The current VERSION remains `0x0002_0060`. |
| FR-CTRL-04 | &#124; FR-CTRL-04 &#124; `GET_COUNTERS` MUST return the 1722.1-2021/Milan counter sets for STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE (see model `counters`), throttled ≤ 1/s. &#124; M &#124; T &#124; | &#124; FR-CTRL-04 &#124; Solicited `GET_COUNTERS` MUST return the 1722.1-2021/Milan counter sets for STREAM_INPUT, STREAM_OUTPUT and AVB_INTERFACE (see model `counters`) within NFR-LAT-02. Only unsolicited counter notifications are limited to at most one per descriptor per second (Milan v1.2 5.4.5.2, Table 5.22). &#124; M &#124; T &#124; |
| NFR-LAT-02 | &#124; NFR-LAT-02 &#124; AVDECC control command→response round-trip SHOULD be < 250 ms (well within 1722.1 inflight timeouts). &#124; S &#124; T &#124; | &#124; NFR-LAT-02 &#124; AVDECC command responses MUST meet their applicable normative limit in Section 3.4.1 in either placement. Firmware paths MUST also meet NFR-SCOUT-03; a 250 ms transaction timeout MUST NOT replace the 240 ms AECP response bound or the 200 ms Milan ACMP timeout. &#124; M &#124; T &#124; |
| NFR-SCUP-02 | &#124; NFR-SCUP-02 &#124; Increasing `P_CH`/`P_SR` MUST only linearly increase bandwidth, buffer, and DSP; the control plane (ADP/AECP/ACMP) MUST be unaffected. &#124; M &#124; A &#124; | &#124; NFR-SCUP-02 &#124; Increasing `P_CH`/`P_SR` MUST only linearly increase media bandwidth, buffer and DSP costs. ADP/AECP/ACMP wire semantics MUST remain unchanged; the selected control placement MUST meet NFR-SCOUT-03 at every supported shape. &#124; M &#124; A &#124; |
| NFR-SCUP-04 | &#124; NFR-SCUP-04 &#124; The builder MUST generate and size the flat AEM image from the selected end-station model, and bare-metal boot MUST validate and install it at the processor's compile-time descriptor base without an RTL edit as descriptor counts grow. &#124; S &#124; I &#124; | &#124; NFR-SCUP-04 &#124; The builder MUST generate and size the flat AEM image from the selected entity model. Bare-metal boot MUST validate and install it before entity enable: at the descriptor base for fabric AECP, or in the validated image store for firmware AECP. Descriptor growth MUST NOT require an RTL edit. &#124; S &#124; I &#124; |
| NFR-SCOUT-01 | &#124; NFR-SCOUT-01 &#124; The release architecture MUST use one cacheless RV32I control hart; increasing stream capacity MUST elaborate additional fabric contexts rather than create a software packet or media plane. &#124; M &#124; A,D &#124; | &#124; NFR-SCOUT-01 &#124; The release architecture MUST use one cacheless RV32I control hart. Stream capacity MUST grow through fabric media contexts and static, entity-sized control contexts in the selected placement. Every supported shape MUST meet NFR-SCOUT-03 without adding harts or a software media path. &#124; M &#124; A,D &#124; |
| NFR-SCOUT-02 | &#124; NFR-SCOUT-02 &#124; Protocol control, media movement, and time discipline MUST retain their explicit fabric owners as stream counts grow. &#124; M &#124; A &#124; | &#124; NFR-SCOUT-02 &#124; ADP, ACMP, AECP (including unsolicited notifications and counter serving), MAAP and SRP MUST each be build-selectable between bare-metal firmware and fabric. Mark II defaults to firmware; all-fabric remains supported and the shipping default until F2 to F5 pass suites and bench acceptance for all streams, counters and audio soak. Each function MUST have one state owner. Framing, timestamps, ingress filtering, gPTP and media MUST remain fabric-owned. The mailbox filter MUST exclude tagged frames, match each channel's exact VLAN-tag/destination-MAC/EtherType/AVTP-subtype tuple, then apply its identity term. Own unicast MUST mean the receiving AVB interface's MAC, never any unicast. AECP MUST accept (command AND target_entity_id = own) OR (response AND controller_entity_id = own). Untagged control frames failing their tuple MUST increment FILTER_MISMATCH. Per-channel token buckets MUST remain; NFR-SCOUT-08 defines the table and checks. &#124; M &#124; A &#124; |
| NFR-SCOUT-03 | &#124; NFR-SCOUT-03 &#124; Packet and audio deadlines MUST depend only on bounded fabric handshakes, never on firmware service latency. &#124; M &#124; A,T &#124; | &#124; NFR-SCOUT-03 &#124; Each moved control path MUST meet the single project service budget T_svc = 10 ms, proposed for owner approval, under Section 3.4.1 and measured by Section 3.4.2. Numeric normative response timeouts MUST also hold with margin; ordering, spacing and timer obligations remain independently normative. Audio and gPTP deadlines MUST depend only on bounded fabric handshakes, independent of firmware service latency. &#124; M &#124; A,T &#124; |
| NFR-SCOUT-08 | Absent | &#124; NFR-SCOUT-08 &#124; The fabric mailbox ingress filter MUST enforce the exact tuples and identity terms in product ownership, including tagged-frame exclusion, per-interface own unicast, both AECP directions and FILTER_MISMATCH for untagged control tuple failures, while retaining per-channel token buckets. The single-source mailbox contract MUST carry these rules. Verify with H-ADP, H-ACMP, H-AECP, H-MAAP and H-SRP in Section 3.4.2, including planted filter defects through both bus adapters and the host mailbox model. &#124; M &#124; A,I,T &#124; |
| NFR-REL-02 | &#124; NFR-REL-02 &#124; Fabric liveness monitors SHOULD detect a stalled protocol, time, or media engine and recover or report it without requiring a full-board reboot. &#124; S &#124; T &#124; | &#124; NFR-REL-02 &#124; Fabric liveness monitors SHOULD detect a stalled time or media engine. Control liveness SHOULD detect a stalled selected protocol owner, including firmware, and recover or report it without a full-board reboot. Expired control-service bounds MUST NOT be hidden by continued advertising. &#124; S &#124; T &#124; |
| Trace: **Control** | &#124; **Control** &#124; ADP, AECP/AEM+MVU, ACMP, MAAP, MSRP/MVRP &#124; bounded protocol deadlines &#124; protocol processor plus fabric MAAP &#124; generated stream contexts &#124; | &#124; **Control** &#124; ADP, AECP/AEM+MVU, ACMP, MAAP, MSRP/MVRP &#124; normative limits plus T_svc in firmware &#124; one selected owner per function; Mark II firmware default, current shipping fabric default &#124; static generated control contexts &#124; |
| Trace: Discovery | &#124; Discovery &#124; FR-DISC-\* &#124; Section 5.2 &#124; `adp`, ENTITY &#124; M-B2 -- processor (Section 2.0) &#124; | &#124; Discovery &#124; FR-DISC-\*, NFR-SCOUT-01..03 &#124; Sections 5.6.2/5.6.3/5.6.4 &#124; `adp`, ENTITY &#124; Current fabric ledger: Section 2.0; split F0/F3, hooks H-ADP/H-DISC/H-ACMP &#124; |
| Trace: Enum/Control | &#124; Enum/Control &#124; FR-ENUM/CTRL &#124; Section 5.3–5.4 &#124; full descriptor tree &#124; M-B3, processor AECP uCPU plus the builder-generated image copied by bare-metal firmware; the served inventory and mandatory gaps are listed in Section 2.0 &#124; | &#124; Enum/Control &#124; FR-ENUM/CTRL, NFR-LAT-02, NFR-SCOUT-01..03 &#124; Sections 5.3/5.4 &#124; full descriptor tree &#124; Current fabric ledger: Section 2.0; split F5, hooks H-AECP/H-NOTIFY/H-COUNTERS &#124; |
| Trace: Connection | &#124; Connection &#124; FR-CONN-\* &#124; Section 5.5 &#124; STREAM_\*, CBS CSR &#124; M-B4 -- processor; fast-connect/persistence **NOT MET** &#124; | &#124; Connection &#124; FR-CONN-\*, NFR-LAT-02, NFR-SCOUT-01..03 &#124; Section 5.5; Table 5.26 &#124; STREAM_\*, selected state owner &#124; Current fabric ledger: Section 2.0; split F1/F3, H-ACMP; cold restore remains unproven &#124; |
| Trace: MAAP/SRP | &#124; MAAP/SRP &#124; FR-MAAP/SRP &#124; Section 5.6 &#124; STREAM_\*, classifier/CBS &#124; M-B5 -- MAAP in fabric, SRP on the processor &#124; | &#124; MAAP/SRP &#124; FR-MAAP/SRP, NFR-SCOUT-01..03 &#124; Sections 4.3.1/4.2.7; Table 4.3 &#124; STREAM_\*, admission &#124; Current fabric ledger: Section 2.0; split F2/F4, H-MAAP/H-SRP &#124; |
| Trace: Scale-out | &#124; Scale-out &#124; NFR-SCOUT-\* &#124;  -  &#124; fabric contexts / replicated endpoint &#124; Section 4 &#124; | &#124; Scale-out &#124; NFR-SCOUT-\*, NFR-SCUP-02/04, NFR-REL-02 &#124; Sections 3.4.1/3.4.2 list timing clauses &#124; fabric media / static selected-owner control contexts &#124; Section 4; every shape, placement and hook &#124; |
| Trace: Mailbox ingress filter | Absent | &#124; Mailbox ingress filter &#124; NFR-SCOUT-02/08 &#124; 5.4.5.3; IEEE 1722.1-2021 8.2.1/Table B.1; IEEE 802.1Q-2018 Table 10-1 &#124; mailbox YAML, per-interface MAC and entity identity &#124; Contract lane after FT, before F2 to F5; H-ADP/H-ACMP/H-AECP/H-MAAP/H-SRP &#124; |
| MRP-6 | &#124; MRP-6 &#124; 10.7.11 &#124; Timer values: JoinTime ~200 ms, LeaveTime 600–1000 ms, LeaveAllTime ~10 s (+Milan tolerances 4.2.7.1.1) &#124; processor timer service &#124; 🔵 PROCESSOR -- Milan Table 4.3 tightens these values and the submodule owns them now; since processor pin `b2db3a97` its srp_top suite grades joinTime, the periodictimer and the leavealltimer against Table 4.3 (Q1-Q4, processor issue 64). `tb/verilator/pp_shadow` compresses the prescaler for liveness only, never for cadence &#124; 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. &#124; | &#124; MRP-6 &#124; 10.7.11 &#124; Timer values: JoinTime 200 ms (180 to 240), LeaveTime 5000 ms (4500 to 7500), periodic 1000 ms (900 to 1500), LeaveAllTime 10 to 15 s (+/-0.5 s), Milan 4.2.7.1.1 Table 4.3; firmware service uses NFR-SCOUT-03 and H-SRP &#124; processor timer service &#124; 🔵 PROCESSOR -- Milan Table 4.3 overrides the IEEE defaults and the submodule owns them now; since processor pin `b2db3a97` its srp_top suite grades joinTime, the periodictimer and the leavealltimer against Table 4.3 (Q1-Q4, processor issue 64). `tb/verilator/pp_shadow` compresses the prescaler for liveness only, never for cadence &#124; 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. &#124; |

## Every timing bound, derivation and test hook

At the original base, sections 3.4.1 and 3.4.2 were absent. Old: absent; new: the
exact current text below, including every timing row, clause, derivation and hook.
No timing bound changed in round 3. The budget is approved at 8fb296e3.

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
| H-ADP | FR-DISC-01..05; NFR-SCOUT-01..03; NFR-SCOUT-08 | ADP `RX_HEAD` commit or startup/GM/link/shutdown occurrence; timer arm and original deadline; AVAILABLE/DEPARTING `TX_HEAD` commit and wire departure; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH | Startup, DISCOVER, periodic, GM, both link edges, shutdown/restart; full rings; zero/max draws; ignored events and stale tags; DEPARTING before AVAILABLE; tagged-frame, wrong-destination and wrong-AVTP-subtype rejection; FILTER_MISMATCH count. |
| H-DISC | FR-DISC-01..05; FR-CONN-01..04; NFR-SCOUT-01..03 | Received ENTITY_AVAILABLE/ENTITY_DEPARTING `RX_HEAD` commit or original TMR_NO_ADP deadline to every matching sink's discovery/timer and resulting connection-state commitment; include the last resulting `TX_HEAD` commit and wire observation where transmission follows | Every Table 5.54 cell; received-valid_time arm/reset and expiry; available_index restart; interface and GM/domain mismatch; departing; all matching bound sinks; late receive handling or aging must fail independently of H-ADP |
| H-ACMP | FR-CONN-01..04; NFR-LAT-02; NFR-SCOUT-01..03; NFR-SCOUT-08 | ACMP `RX_HEAD` commit to the matched response `TX_HEAD`; originated command commit to response receipt; discovery/probe timer deadline to its action; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH | Each Table 5.26 command, success/refusal, retry, distinct sequence/unique IDs, restore and fast connect; wire round-trip < 200 ms with margin; tagged-frame, wrong-destination and wrong-AVTP-subtype rejection; FILTER_MISMATCH count; own-unicast receive tolerance and foreign-unicast rejection. |
| H-AECP | FR-ENUM-01/02; FR-CTRL-01..06; FR-MVU-01..03; NFR-SCUP-04; NFR-LAT-02; NFR-SCOUT-08 | AECP `RX_HEAD` commit to matched response `TX_HEAD`, plus received-command and emitted-response wire observations; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH | AEM/MVU, descriptors, getters/setters, counters and refusals; longest image/state access; locks; malformed/truncated requests; response <= 240 ms with margin; own-target commands and own-controller responses pass; CONTROLLER_AVAILABLE response reaches the core (Milan v1.2 5.4.5.3), while a response for another controller_entity_id is dropped even when target_entity_id = own; a foreign-target command is dropped even when controller_entity_id = own. Reject another interface's unicast MAC and a foreign destination. |
| H-NOTIFY | FR-CTRL-03; FR-MGT-01/02; NFR-SCOUT-02/03 | Causal command RX or asynchronous state-change occurrence to the last required notification `TX_HEAD`; record response commit and every recipient's wire departure | Successful-command ordering, cross-channel ACMP response then AECP notice, all registered recipients, departure probes, unlock, enabled Identify spacing, full transmit rings |
| H-COUNTERS | FR-CTRL-04; FR-STR-04; NFR-OBS-01; NFR-SCOUT-02/03 | Fabric counter snapshot/update event to the last push `TX_HEAD`; previous notification wire time supplies eligibility; solicited GET_COUNTERS uses H-AECP | Every descriptor bank and stream, coherent snapshots, resets/wrap, multiple changes while rate-limited; >= 1 s per-descriptor wire spacing; <= 1 s counter update |
| H-MAAP | FR-MAAP-01; NFR-SCOUT-02/03; NFR-SCOUT-08 | MAAP `RX_HEAD` commit or original timer deadline to PROBE/DEFEND/ANNOUNCE `TX_HEAD`; state completion when no frame is required; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH | Conflict in each state, three probe retransmissions, allocation loss/retry, strict probe/announce intervals, ring stalls and boundary draws; tagged-frame, wrong-destination and wrong-AVTP-subtype rejection; FILTER_MISMATCH count. |
| H-SRP | FR-SRP-01..03; FR-CONN-02; NFR-SCOUT-01..03; NFR-SCOUT-08 | SRP `RX_HEAD` commit or fabric timer deadline to MRPDU `TX_HEAD`; registrar/state-apply commitment for non-transmitting transitions; filter checks observe ingress, RX publication, core delivery and FILTER_MISMATCH | MSRP/MVRP joins, withdrawal, malformed vectors, LeaveAll/periodic expiry, coalesced tick backlog, reservation/licence updates; JoinTime and LeaveTime bounds; tagged-frame and wrong-destination rejection for MSRP and MVRP; wrong AVTP subtype cannot select srp; FILTER_MISMATCH count. MSRP/MVRP have no AVTP subtype field. |

The five filter hooks also start before mailbox publication.
Inject each table row's valid frame as a positive control.
Change tag, destination, EtherType, subtype and identity separately where applicable.
Rejected input MUST create neither an RX record nor core delivery.
Use an unassigned AVTP subtype for the wrong-subtype rejection.
Also inject untagged AAF and CRF; neither has a channel.
For MSRP/MVRP, test AVTP substitutions without inventing an MRP subtype.
Each untagged control tuple mismatch MUST increment FILTER_MISMATCH once.
Valid input and tagged input MUST NOT increment that counter.
Observe token-bucket enforcement separately from tuple and identity refusal.
AECP rejection cases must also test the opposite ID matching.
AECP acceptance cases use unrelated opposite IDs.
The response case includes the CONTROLLER_AVAILABLE liveness reply.
Repeat own-MAC checks for each configured AVB interface and record index.
Plant each acceptance-rule defect; require its named hook to fail.
These additions await the contract lane after FT, before F2 to F5.

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

## Version, traceability and scope checks

VERSION stays 0x0002_0060. The five-simulation/default-flip plan is
approved at 8fb296e3 and unchanged. All 15 generated traceability outputs
regenerated byte-identically; the no-drift gate grades 77 modules and zero
untested modules. No generated output was hand-edited.

The authored commit changes REQUIREMENTS.md, FR_NFR.md and MAILBOX_SPLIT.md.
The merge preserves every non-documentation entry from its dev parent.
The approval audit reverses only the enumerated filter additions and proves
all three files then equal the approved head exactly. All 19 approval cells
match committed source fragments. The five-query contradiction census
reproduces all 680 original-base and 735 candidate hits, with dispositions.
The workflow inventory covers all 81 Python command occurrences in docs.yml,
including wire-accountability and both metadata-free checks.

Tracked-byte integrity passed: 1,109 root blobs and 876 required-submodule
blobs, including modes, index entries, index flags and pinned revisions.
The required submodule top-level was verified before each direct Git call.
The unused external gitlink is unchanged. No untracked source file remains.

## Contradiction search: every hit and disposition

All tracked root-repository Markdown blobs were searched at the original
base and candidate. Gitlinks are separate repositories, not root files.
Q1-Q4 reproduce the prior ownership and requirement census. Q5 adds the
filter vocabulary. Every query/line hit is listed below; duplicate matches
are retained per query. Each locator can be opened at its named revision.
The file disposition applies to every listed hit, with the exceptions below.

- Q1: `NFR-SCOUT-0[123]`
- Q2: `never on firmware|fabric-only|fabric.only|no firmware round trip|never becomes a packet|all per-frame protocol`
- Q3: `(?i)(ADP|ACMP|AECP|MAAP|SRP|protocol control).{0,70}(fabric|processor)|(fabric|processor).{0,70}(ADP|ACMP|AECP|MAAP|SRP|protocol control)`
- Q4: `NFR-LAT-02|NFR-SCUP-0[24]|NFR-REL-02|FR-CTRL-04`
- Q5: `(?i)NFR-SCOUT-08|FILTER_MISMATCH|CONTROLLER_AVAILABLE|command.only|untagged|full.tuple|own.unicast`

Base: 680 hits. Candidate: 735 hits.

Q1-Q4 alone reproduce 617 base and 645 candidate records.
E means corrected or scoped placement; H is historical evidence;
G is generated implementation inventory; I is an implemented interface;
P is a retained persistence/media contract; R is reset-domain language;
C is an architectural comparison. Base E hits describe the old text
corrected by this lane. Retained hits do not establish split implementation.

Filter-specific dispositions:

- REQUIREMENTS section 6 and REGISTER_MAP classify fabric queues; their
  broad control classification does not admit frames to a firmware mailbox.
- MAILBOX_SPLIT's old uncounted and command-only acceptance is F0 behavior,
  explicitly marked incomplete against NFR-SCOUT-08. The generated contract
  and mailbox YAML are unchanged implementation artifacts awaiting that lane.
- Saved-state materialization's untagged-port wording means transaction
  responses without operation tags, not Ethernet VLAN tags.
- Media parsers may parse untagged AAF/CRF without delivering them to any
  mailbox. Their test records and historical fallback measurements stand.
- CONTROLLER_AVAILABLE records in compliance, roadmap and processor pages
  describe implemented fabric monitoring or historical missing behavior;
  the new firmware response hook does not upgrade their measured verdicts.

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
| `docs/design/MAILBOX_SPLIT.md` | E: F0 implementation is explicitly scoped; the added filter note points to the later full-tuple/AECP/counter contract. |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` | P: existing fabric media or processor persistence contract; retained for that implementation. Split ownership and F1 integration are specified separately. |
| `docs/design/SAVED_STATE_FASTCONNECT.md` | P: existing fabric media or processor persistence contract; retained for that implementation. Split ownership and F1 integration are specified separately. |
| `docs/design/SAVED_STATE_MATERIALIZATION.md` | P: processor saved-state design and pinned implementation evidence; remains valid for all-fabric, with split boot/apply assigned to the F1 contract. |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` | P: current processor persistence/reset boundary and pinned evidence; no prohibition on firmware control placement. |
| `docs/development/CODE_QUALITY.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/397_SERVICE_BUDGET.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/findings/451_TDM8_FIRST_LIGHT.md` | H: dated media measurement, not mailbox acceptance. |
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
| `docs/reference/REGISTER_MAP.md` | I: current CSR/queue classification. Queue assignment is distinct from mailbox admission; upstream dev additions are preserved. |
| `docs/reference/REGISTER_MAP_CLASSES.md` | I: current implemented CSR or egress interface; preserved unchanged because this lane does not implement the split or change VERSION. |
| `docs/reference/SUBMODULES.md` | I: source dependency provenance and pinned processor responsibilities; not a restriction on future selectable placement. |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md` | H: dated implementation or measurement evidence; retain the recorded head and historical verdict, not a universal future-placement rule. |
| `docs/testing/SIMULATION.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/testing/TESTING.md` | I: current shipping build, integration, verification or troubleshooting evidence; retains the actual processor owner and does not claim completed split firmware. |
| `docs/traceability/MODULE_MATRIX.md` | G: generated inventory of actual RTL and tests; regenerated byte-identically, not evidence that firmware integration exists. |
| `docs/traceability/ieee8021q.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `hdl/ieee1722/aaf/doc/KL_aaf_rx_depacketizer/KL_aaf_rx_depacketizer.md` | I: media payload parsing, not mailbox acceptance. |
| `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `sw/builder/README-parameters.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `sw/firmware/ctrl/README.md` | E: current ownership corrected or explicitly scoped to the shipping all-fabric placement; split claims point to the selected-owner contract. |
| `sw/firmware/nvm_hosttest/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `syn/yosys/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/avtp_parser/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/avtp_stream/README.md` | I: media-parser test contract, not mailbox acceptance. |
| `tb/verilator/milan_dp/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tb/verilator/pp_shadow/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |
| `tests/README.md` | I: names an existing implementation, harness or synthesis target; retained for the supported all-fabric option, without a new target-architecture claim. |

### Base hit ledger

Revision: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.

| Query | Locator | Disposition |
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
| Q5 | `REQUIREMENTS.md:195` | E |
| Q5 | `REQUIREMENTS.md:210` | E |
| Q5 | `REQUIREMENTS.md:212` | E |
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
| Q5 | `docs/MILAN_V12_ROADMAP.md:461` | I |
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
| Q5 | `docs/design/MAILBOX_SPLIT.md:151` | E |
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
| Q2 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:843` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1485` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1558` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1797` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1882` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1930` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1944` | P |
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
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:883` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1389` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1397` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1847` | P |
| Q3 | `docs/development/CODE_QUALITY.md:218` | I |
| Q3 | `docs/development/CODE_QUALITY.md:372` | I |
| Q3 | `docs/development/CODE_QUALITY.md:380` | I |
| Q3 | `docs/development/CODE_QUALITY.md:601` | I |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:18` | H |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76` | H |
| Q3 | `docs/findings/397_SERVICE_BUDGET.md:190` | H |
| Q5 | `docs/findings/451_TDM8_FIRST_LIGHT.md:168` | H |
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
| Q5 | `docs/history/v1/MVP_TALKER.md:43` | H |
| Q3 | `docs/history/v1/MVP_TALKER.md:58` | H |
| Q5 | `docs/history/v1/MVP_TALKER.md:117` | H |
| Q5 | `docs/history/v1/MVP_TALKER.md:118` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:28` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:31` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:36` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:84` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:135` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:411` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:462` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:494` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:496` | H |
| Q5 | `docs/history/v1/NXN_ARCHITECTURE.md:542` | H |
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
| Q5 | `docs/history/v1/SPEC_TRACEABILITY.md:413` | H |
| Q5 | `docs/history/v1/SPEC_TRACEABILITY.md:419` | H |
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
| Q5 | `docs/history/v1/design/TIME_SYNC.md:147` | H |
| Q5 | `docs/history/v1/design/TIME_SYNC.md:329` | H |
| Q3 | `docs/history/v1/design/TIME_SYNC.md:553` | H |
| Q5 | `docs/history/v1/design/TIME_SYNC.md:660` | H |
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
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:280` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:284` | H |
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:313` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:357` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:363` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:370` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:371` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:373` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:375` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:378` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:380` | H |
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:381` | H |
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:385` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:390` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:391` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:395` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:416` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:417` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:19` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:42` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:195` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:206` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:216` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:219` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:221` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:226` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:227` | H |
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
| Q5 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:299` | H |
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
| Q5 | `docs/history/v1/traceability/ieee1722-2016.md:74` | H |
| Q5 | `docs/history/v1/traceability/ieee1722-2016.md:76` | H |
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
| Q5 | `docs/history/v1/traceability/ieee1722_1-2021.md:274` | H |
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
| Q5 | `docs/history/v1/traceability/milan-v12.md:226` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:227` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:265` | H |
| Q5 | `docs/history/v1/traceability/milan-v12.md:265` | H |
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
| Q5 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:59` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:62` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:89` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:93` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:117` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:144` | E |
| Q5 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:144` | E |
| Q5 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:204` | E |
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
| Q5 | `docs/reference/REGISTER_MAP.md:181` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:191` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:192` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:193` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:224` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:226` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:335` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:363` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:363` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:548` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:549` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:559` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:561` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:573` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:584` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:637` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:789` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:790` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:950` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:950` | I |
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
| Q5 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:236` | H |
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
| Q5 | `docs/traceability/ieee8021q.md:88` | E |
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
| Q5 | `docs/traceability/ieee8021q.md:133` | E |
| Q3 | `docs/traceability/ieee8021q.md:134` | E |
| Q3 | `docs/traceability/ieee8021q.md:135` | E |
| Q3 | `docs/traceability/ieee8021q.md:136` | E |
| Q3 | `docs/traceability/ieee8021q.md:137` | E |
| Q3 | `docs/traceability/ieee8021q.md:138` | E |
| Q3 | `docs/traceability/ieee8021q.md:139` | E |
| Q3 | `docs/traceability/ieee8021q.md:141` | E |
| Q5 | `docs/traceability/ieee8021q.md:141` | E |
| Q3 | `docs/traceability/ieee8021q.md:149` | E |
| Q5 | `hdl/ieee1722/aaf/doc/KL_aaf_rx_depacketizer/KL_aaf_rx_depacketizer.md:17` | I |
| Q3 | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3` | I |
| Q3 | `sw/builder/README-parameters.md:210` | I |
| Q3 | `sw/firmware/ctrl/README.md:18` | E |
| Q3 | `sw/firmware/ctrl/README.md:46` | E |
| Q3 | `sw/firmware/ctrl/README.md:47` | E |
| Q3 | `sw/firmware/ctrl/README.md:49` | E |
| Q3 | `sw/firmware/ctrl/README.md:54` | E |
| Q3 | `sw/firmware/nvm_hosttest/README.md:101` | I |
| Q3 | `syn/yosys/README.md:312` | I |
| Q5 | `tb/verilator/README.md:48` | I |
| Q5 | `tb/verilator/README.md:55` | I |
| Q5 | `tb/verilator/README.md:65` | I |
| Q5 | `tb/verilator/README.md:66` | I |
| Q3 | `tb/verilator/README.md:105` | I |
| Q3 | `tb/verilator/avtp_parser/README.md:17` | I |
| Q5 | `tb/verilator/avtp_parser/README.md:51` | I |
| Q5 | `tb/verilator/avtp_parser/README.md:52` | I |
| Q5 | `tb/verilator/avtp_parser/README.md:58` | I |
| Q5 | `tb/verilator/avtp_stream/README.md:14` | I |
| Q3 | `tb/verilator/milan_dp/README.md:75` | I |
| Q3 | `tb/verilator/milan_dp/README.md:76` | I |
| Q3 | `tb/verilator/milan_dp/README.md:428` | I |
| Q3 | `tb/verilator/milan_dp/README.md:630` | I |
| Q3 | `tb/verilator/milan_dp/README.md:632` | I |
| Q3 | `tb/verilator/milan_dp/README.md:634` | I |
| Q3 | `tb/verilator/milan_dp/README.md:647` | I |
| Q3 | `tb/verilator/milan_dp/README.md:653` | I |
| Q3 | `tb/verilator/milan_dp/README.md:907` | I |
| Q5 | `tb/verilator/milan_dp/README.md:914` | I |
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

Revision: `4dab80ae4564ef8d6e1030564dcea4ba19235ee6`.

| Query | Locator | Disposition |
|---|---|---|
| Q3 | `CHANGELOG.md:15` | H |
| Q3 | `CHANGELOG.md:495` | H |
| Q3 | `QUICKSTART.md:17` | I |
| Q3 | `QUICKSTART.md:266` | I |
| Q3 | `README.md:41` | E |
| Q3 | `README.md:42` | E |
| Q3 | `README.md:56` | E |
| Q3 | `README.md:372` | E |
| Q3 | `README.md:389` | E |
| Q3 | `README.md:431` | E |
| Q5 | `REQUIREMENTS.md:44` | E |
| Q5 | `REQUIREMENTS.md:45` | E |
| Q5 | `REQUIREMENTS.md:47` | E |
| Q1 | `REQUIREMENTS.md:51` | E |
| Q5 | `REQUIREMENTS.md:58` | E |
| Q5 | `REQUIREMENTS.md:63` | E |
| Q5 | `REQUIREMENTS.md:65` | E |
| Q5 | `REQUIREMENTS.md:70` | E |
| Q5 | `REQUIREMENTS.md:71` | E |
| Q5 | `REQUIREMENTS.md:81` | E |
| Q5 | `REQUIREMENTS.md:82` | E |
| Q5 | `REQUIREMENTS.md:87` | E |
| Q5 | `REQUIREMENTS.md:88` | E |
| Q3 | `REQUIREMENTS.md:229` | E |
| Q5 | `REQUIREMENTS.md:262` | E |
| Q5 | `REQUIREMENTS.md:277` | E |
| Q5 | `REQUIREMENTS.md:279` | E |
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
| Q3 | `docs/ENDSTATION_BUILDER.md:1019` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1035` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1059` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1061` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1069` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1074` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1076` | E |
| Q3 | `docs/ENDSTATION_BUILDER.md:1153` | E |
| Q3 | `docs/GLOSSARY.md:79` | E |
| Q3 | `docs/MILAN_V12_ROADMAP.md:201` | I |
| Q5 | `docs/MILAN_V12_ROADMAP.md:461` | I |
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
| Q5 | `docs/design/MAILBOX_SPLIT.md:150` | E |
| Q5 | `docs/design/MAILBOX_SPLIT.md:152` | E |
| Q5 | `docs/design/MAILBOX_SPLIT.md:154` | E |
| Q5 | `docs/design/MAILBOX_SPLIT.md:157` | E |
| Q5 | `docs/design/MAILBOX_SPLIT.md:166` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:343` | E |
| Q1 | `docs/design/MAILBOX_SPLIT.md:372` | E |
| Q3 | `docs/design/MAILBOX_SPLIT.md:453` | E |
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
| Q2 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:475` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:851` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1500` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1573` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1812` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1897` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1945` | P |
| Q5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1959` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2409` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2410` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2422` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2425` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2427` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2428` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2429` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2430` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2431` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2434` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2439` | P |
| Q3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2632` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:883` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1389` | P |
| Q3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1397` | P |
| Q2 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1847` | P |
| Q3 | `docs/development/CODE_QUALITY.md:218` | I |
| Q3 | `docs/development/CODE_QUALITY.md:372` | I |
| Q3 | `docs/development/CODE_QUALITY.md:380` | I |
| Q3 | `docs/development/CODE_QUALITY.md:601` | I |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:18` | H |
| Q3 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76` | H |
| Q3 | `docs/findings/397_SERVICE_BUDGET.md:190` | H |
| Q5 | `docs/findings/451_TDM8_FIRST_LIGHT.md:168` | H |
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
| Q5 | `docs/history/v1/MVP_TALKER.md:43` | H |
| Q3 | `docs/history/v1/MVP_TALKER.md:58` | H |
| Q5 | `docs/history/v1/MVP_TALKER.md:117` | H |
| Q5 | `docs/history/v1/MVP_TALKER.md:118` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:28` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:31` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:36` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:84` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:135` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:411` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:462` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:494` | H |
| Q3 | `docs/history/v1/NXN_ARCHITECTURE.md:496` | H |
| Q5 | `docs/history/v1/NXN_ARCHITECTURE.md:542` | H |
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
| Q5 | `docs/history/v1/SPEC_TRACEABILITY.md:413` | H |
| Q5 | `docs/history/v1/SPEC_TRACEABILITY.md:419` | H |
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
| Q5 | `docs/history/v1/design/TIME_SYNC.md:147` | H |
| Q5 | `docs/history/v1/design/TIME_SYNC.md:329` | H |
| Q3 | `docs/history/v1/design/TIME_SYNC.md:553` | H |
| Q5 | `docs/history/v1/design/TIME_SYNC.md:660` | H |
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
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:280` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:284` | H |
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:313` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:357` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:363` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:370` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:371` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:373` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:375` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:378` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:380` | H |
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:381` | H |
| Q5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:385` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:390` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:391` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:395` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:416` | H |
| Q3 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:417` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:19` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:42` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:195` | H |
| Q3 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:206` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:216` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:219` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:221` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:226` | H |
| Q5 | `docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:227` | H |
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
| Q5 | `docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:299` | H |
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
| Q5 | `docs/history/v1/traceability/ieee1722-2016.md:74` | H |
| Q5 | `docs/history/v1/traceability/ieee1722-2016.md:76` | H |
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
| Q5 | `docs/history/v1/traceability/ieee1722_1-2021.md:274` | H |
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
| Q5 | `docs/history/v1/traceability/milan-v12.md:226` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:227` | H |
| Q3 | `docs/history/v1/traceability/milan-v12.md:265` | H |
| Q5 | `docs/history/v1/traceability/milan-v12.md:265` | H |
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
| Q5 | `docs/reference/FR_NFR.md:322` | E |
| Q1 | `docs/reference/FR_NFR.md:323` | E |
| Q5 | `docs/reference/FR_NFR.md:328` | E |
| Q5 | `docs/reference/FR_NFR.md:367` | E |
| Q1 | `docs/reference/FR_NFR.md:403` | E |
| Q5 | `docs/reference/FR_NFR.md:403` | E |
| Q1 | `docs/reference/FR_NFR.md:404` | E |
| Q1 | `docs/reference/FR_NFR.md:405` | E |
| Q4 | `docs/reference/FR_NFR.md:405` | E |
| Q5 | `docs/reference/FR_NFR.md:405` | E |
| Q4 | `docs/reference/FR_NFR.md:406` | E |
| Q5 | `docs/reference/FR_NFR.md:406` | E |
| Q1 | `docs/reference/FR_NFR.md:407` | E |
| Q1 | `docs/reference/FR_NFR.md:408` | E |
| Q4 | `docs/reference/FR_NFR.md:408` | E |
| Q1 | `docs/reference/FR_NFR.md:409` | E |
| Q5 | `docs/reference/FR_NFR.md:409` | E |
| Q1 | `docs/reference/FR_NFR.md:410` | E |
| Q3 | `docs/reference/FR_NFR.md:410` | E |
| Q5 | `docs/reference/FR_NFR.md:410` | E |
| Q5 | `docs/reference/FR_NFR.md:417` | E |
| Q5 | `docs/reference/FR_NFR.md:419` | E |
| Q5 | `docs/reference/FR_NFR.md:424` | E |
| Q3 | `docs/reference/FR_NFR.md:452` | E |
| Q4 | `docs/reference/FR_NFR.md:466` | E |
| Q3 | `docs/reference/FR_NFR.md:557` | E |
| Q1 | `docs/reference/FR_NFR.md:594` | E |
| Q3 | `docs/reference/FR_NFR.md:594` | E |
| Q1 | `docs/reference/FR_NFR.md:595` | E |
| Q3 | `docs/reference/FR_NFR.md:595` | E |
| Q4 | `docs/reference/FR_NFR.md:595` | E |
| Q1 | `docs/reference/FR_NFR.md:597` | E |
| Q3 | `docs/reference/FR_NFR.md:597` | E |
| Q4 | `docs/reference/FR_NFR.md:597` | E |
| Q1 | `docs/reference/FR_NFR.md:598` | E |
| Q3 | `docs/reference/FR_NFR.md:598` | E |
| Q1 | `docs/reference/FR_NFR.md:599` | E |
| Q4 | `docs/reference/FR_NFR.md:604` | E |
| Q5 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:64` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:67` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:94` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:98` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:122` | E |
| Q3 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:149` | E |
| Q5 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:149` | E |
| Q5 | `docs/reference/MILAN_COMPLIANCE_MATRIX.md:209` | E |
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
| Q5 | `docs/reference/REGISTER_MAP.md:181` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:191` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:192` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:193` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:224` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:226` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:335` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:363` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:363` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:548` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:549` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:559` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:561` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:573` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:584` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:637` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:789` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:790` | I |
| Q3 | `docs/reference/REGISTER_MAP.md:950` | I |
| Q5 | `docs/reference/REGISTER_MAP.md:950` | I |
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
| Q3 | `docs/reference/REGISTER_MAP.md:2380` | I |
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
| Q5 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:236` | H |
| Q3 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:243` | H |
| Q3 | `docs/testing/SIMULATION.md:38` | I |
| Q3 | `docs/testing/TESTING.md:25` | I |
| Q3 | `docs/testing/TESTING.md:273` | I |
| Q3 | `docs/testing/TESTING.md:448` | I |
| Q3 | `docs/testing/TESTING.md:520` | I |
| Q3 | `docs/testing/TESTING.md:535` | I |
| Q3 | `docs/testing/TESTING.md:1176` | I |
| Q3 | `docs/testing/TESTING.md:1230` | I |
| Q3 | `docs/traceability/MODULE_MATRIX.md:52` | G |
| Q3 | `docs/traceability/MODULE_MATRIX.md:106` | G |
| Q3 | `docs/traceability/ieee8021q.md:35` | E |
| Q3 | `docs/traceability/ieee8021q.md:39` | E |
| Q3 | `docs/traceability/ieee8021q.md:54` | E |
| Q3 | `docs/traceability/ieee8021q.md:85` | E |
| Q3 | `docs/traceability/ieee8021q.md:87` | E |
| Q3 | `docs/traceability/ieee8021q.md:88` | E |
| Q5 | `docs/traceability/ieee8021q.md:94` | E |
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
| Q5 | `docs/traceability/ieee8021q.md:147` | E |
| Q3 | `docs/traceability/ieee8021q.md:148` | E |
| Q3 | `docs/traceability/ieee8021q.md:149` | E |
| Q3 | `docs/traceability/ieee8021q.md:150` | E |
| Q3 | `docs/traceability/ieee8021q.md:151` | E |
| Q3 | `docs/traceability/ieee8021q.md:152` | E |
| Q3 | `docs/traceability/ieee8021q.md:153` | E |
| Q3 | `docs/traceability/ieee8021q.md:155` | E |
| Q5 | `docs/traceability/ieee8021q.md:155` | E |
| Q3 | `docs/traceability/ieee8021q.md:163` | E |
| Q5 | `hdl/ieee1722/aaf/doc/KL_aaf_rx_depacketizer/KL_aaf_rx_depacketizer.md:17` | I |
| Q3 | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3` | I |
| Q3 | `sw/builder/README-parameters.md:210` | I |
| Q3 | `sw/firmware/ctrl/README.md:25` | E |
| Q3 | `sw/firmware/ctrl/README.md:53` | E |
| Q3 | `sw/firmware/ctrl/README.md:54` | E |
| Q3 | `sw/firmware/ctrl/README.md:56` | E |
| Q3 | `sw/firmware/ctrl/README.md:61` | E |
| Q3 | `sw/firmware/nvm_hosttest/README.md:101` | I |
| Q3 | `syn/yosys/README.md:312` | I |
| Q5 | `tb/verilator/README.md:48` | I |
| Q5 | `tb/verilator/README.md:55` | I |
| Q5 | `tb/verilator/README.md:65` | I |
| Q5 | `tb/verilator/README.md:66` | I |
| Q3 | `tb/verilator/README.md:105` | I |
| Q3 | `tb/verilator/avtp_parser/README.md:17` | I |
| Q5 | `tb/verilator/avtp_parser/README.md:51` | I |
| Q5 | `tb/verilator/avtp_parser/README.md:52` | I |
| Q5 | `tb/verilator/avtp_parser/README.md:58` | I |
| Q5 | `tb/verilator/avtp_stream/README.md:14` | I |
| Q3 | `tb/verilator/milan_dp/README.md:76` | I |
| Q3 | `tb/verilator/milan_dp/README.md:78` | I |
| Q3 | `tb/verilator/milan_dp/README.md:431` | I |
| Q3 | `tb/verilator/milan_dp/README.md:633` | I |
| Q3 | `tb/verilator/milan_dp/README.md:635` | I |
| Q3 | `tb/verilator/milan_dp/README.md:637` | I |
| Q3 | `tb/verilator/milan_dp/README.md:650` | I |
| Q3 | `tb/verilator/milan_dp/README.md:656` | I |
| Q3 | `tb/verilator/milan_dp/README.md:994` | I |
| Q5 | `tb/verilator/milan_dp/README.md:1001` | I |
| Q3 | `tb/verilator/milan_dp/README.md:1025` | I |
| Q3 | `tb/verilator/milan_dp/README.md:1031` | I |
| Q3 | `tb/verilator/milan_dp/README.md:1041` | I |
| Q3 | `tb/verilator/milan_dp/README.md:1051` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:14` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:82` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:121` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:139` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:145` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:146` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:147` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:168` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:172` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:333` | I |
| Q3 | `tb/verilator/pp_shadow/README.md:372` | I |
| Q3 | `tests/README.md:10` | I |
| Q3 | `tests/README.md:23` | I |
| Q3 | `tests/README.md:53` | I |
| Q3 | `tests/README.md:54` | I |
| Q3 | `tests/README.md:151` | I |

## Gate table and environment

### Reproduction setup

PR #674 is the existing review object. Its preceding published candidate is
8fb296e3; the local round-3 candidate named above has not been pushed by
the executor. Obtain that exact candidate before reproducing these results.

```sh
git checkout --detach 4dab80ae4564ef8d6e1030564dcea4ba19235ee6
git rev-parse HEAD
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt -r tools/hdl_reference/requirements.txt
python3 -m pip install pyyaml wavedrom==2.0.3.post3
```

Supply the pinned RV32 SDK, pinned HDL front end, HDL parser,
Markdown renderer, diagram renderer and the repository build environment.
CHECK_ROOT and DEPS_ROOT denote disposable disk-backed directories selected
by the reviewer. They must be outside the source tree.
Set TMPDIR there, disable Python bytecode writes, and use four workers at most.
The no-git checks run in a committed source archive under CHECK_ROOT/export.
Before any Git operation in a submodule, prove its repository top-level
equals that submodule directory. Do not substitute copied or linked trees.
After selecting CHECK_ROOT and DEPS_ROOT, prepare the portable gate paths:

```sh
export CANDIDATE_ROOT="$PWD"
export JOB_UID="$(id -u)"
export JOB_GID="$(id -g)"
mkdir -p "$CHECK_ROOT/export" "$CHECK_ROOT/container-B33" "$CHECK_ROOT/container-D39" "$CHECK_ROOT/gate-tmp"
export TMPDIR="$CHECK_ROOT/gate-tmp"
export PYTHONDONTWRITEBYTECODE=1
git archive HEAD --output "$CHECK_ROOT/head.tar"
tar -xf "$CHECK_ROOT/head.tar" -C "$CHECK_ROOT/export"
```

B48 uses the pinned RV32 build environment; the other Python checks use
the pinned documentation environment. The two container commands retain
the network, capability, credential and read-only source boundaries used here.

### Commands and results

Run every command below without a pipeline. Each has a separate log and
exit receipt. Independent gates run concurrently, while the foreground
monitor waits in bounded intervals. The final verdict requires all rc 0.
B01-B48 is the complete builder/static bank; the remaining commands supply
the full docs workflow, imported docs, metadata-free and mailbox checks.
B33 and D39 execute only inside a disposable, networkless container with
the candidate mounted read-only. D39 grants no host-side orchestration authority.
No candidate CI runner was used to control the host.

| ID | Command | rc | Seconds | Result |
|---|---|---:|---:|---|
| B01 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.12 | PASS |
| B02 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.32 | PASS |
| B03 | `python3 scripts/lint_rtl.py --check --self-test` | 0 | 7.03 | PASS |
| B04 | `python3 scripts/suite_shards.py --selftest` | 0 | 0.07 | PASS |
| B05 | `python3 scripts/ci_events.py --check` | 0 | 0.27 | PASS |
| B06 | `python3 scripts/ci_scope.py --selftest` | 0 | 8.07 | PASS |
| B07 | `python3 scripts/ci_events.py --selftest` | 0 | 18.01 | PASS |
| B08 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.32 | PASS |
| B09 | `python3 scripts/check_feature_status.py` | 0 | 0.98 | PASS |
| B10 | `python3 scripts/check_submodule_docs.py` | 0 | 0.57 | PASS |
| B11 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.97 | PASS |
| B12 | `python3 scripts/check_py_idiom.py` | 0 | 4.98 | PASS |
| B13 | `python3 scripts/docs_check.py` | 0 | 5.88 | PASS |
| B14 | `python3 scripts/check_doc_style.py` | 0 | 0.07 | PASS |
| B15 | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.07 | PASS |
| B16 | `python3 scripts/check_solution_docs.py` | 0 | 0.17 | PASS |
| B17 | `python3 scripts/check_doc_paths.py` | 0 | 0.12 | PASS |
| B18 | `python3 scripts/check_archive.py` | 0 | 0.47 | PASS |
| B19 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.07 | PASS |
| B20 | `python3 scripts/gen_toc.py --check` | 0 | 5.15 | PASS |
| B21 | `python3 scripts/check_hygiene.py --check` | 0 | 0.47 | PASS |
| B22 | `python3 scripts/check_todo_ownership.py` | 0 | 1.97 | PASS |
| B23 | `python3 scripts/check_sv_idiom.py` | 0 | 0.52 | PASS |
| B24 | `python3 scripts/check_sh_idiom.py` | 0 | 0.37 | PASS |
| B25 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.73 | PASS |
| B26 | `python3 scripts/check_soc_sources.py` | 0 | 0.22 | PASS |
| B27 | `python3 scripts/check_port_contracts.py` | 0 | 3.04 | PASS |
| B28 | `python3 scripts/check_nvm_record_space.py` | 0 | 3.03 | PASS |
| B29 | `python3 scripts/check_baremetal_only.py --check` | 0 | 19.28 | PASS |
| B30 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 8.75 | PASS |
| B31 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 87.52 | PASS |
| B32 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 18.23 | PASS |
| B33 | `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --memory 2g --cpus 2 --user "$JOB_UID:$JOB_GID" --mount "type=bind,src=$CANDIDATE_ROOT,dst=/candidate,readonly" --mount "type=bind,src=$CHECK_ROOT/container-B33,dst=/scratch" --workdir /candidate --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/xvlog_gate.py --check` | 0 | 0.87 | SKIPPED: no vendor analyzer in the disposable container |
| B34 | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.22 | PASS |
| B35 | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.12 | PASS |
| B36 | `python3 scripts/check_em_dash.py --base 30e3c018b9add0cb182d8f1229eeec062218130d` | 0 | 4.58 | PASS |
| B37 | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.67 | PASS |
| B38 | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.98 | PASS |
| B39 | `python3 scripts/measure_naming.py --check` | 0 | 0.62 | PASS |
| B40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.54 | PASS |
| B41 | `python3 scripts/gen_toc.py --selftest` | 0 | 1.02 | PASS |
| B42 | `python3 scripts/check_em_dash.py --selftest` | 0 | 3.83 | PASS |
| B43 | `python3 scripts/docs_check.py --selftest` | 0 | 0.22 | PASS |
| B44 | `git diff --check 30e3c018b9add0cb182d8f1229eeec062218130d 4dab80ae4564ef8d6e1030564dcea4ba19235ee6` | 0 | 0.02 | PASS |
| B45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.32 | PASS |
| B46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | 61.02 | PASS |
| B47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.52 | PASS |
| B48 | `python3 sw/builder/test_builder.py --require-rv32` | 0 | 1196.78 | PASS; gate 11 calibration NOT RUN: historical mf48 report absent |
| D01 | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.27 | PASS |
| D02 | `python3 scripts/gen_hdl_reference.py --output $CHECK_ROOT/hdl-reference` | 0 | 1.92 | PASS |
| D03 | `python3 scripts/check_gptp_docs.py` | 0 | 0.22 | PASS |
| D04 | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.23 | PASS |
| D05 | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.42 | PASS |
| D06 | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.52 | PASS |
| D07 | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.48 | PASS |
| D08 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.47 | PASS |
| D09 | `python3 scripts/check_solution_docs.py --selftest` | 0 | 3.02 | PASS |
| D10 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.42 | PASS |
| D11 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.57 | PASS |
| D12 | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.13 | PASS |
| D13 | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.17 | PASS |
| D14 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.32 | PASS |
| D15 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.37 | PASS |
| D16 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.42 | PASS |
| D17 | `python3 scripts/check_diagram_pngs.py` | 0 | 0.37 | PASS |
| D18 | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.43 | PASS |
| D19 | `python3 scripts/check_feature_status.py --self-test` | 0 | 1.07 | PASS |
| D20 | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.27 | PASS |
| D21 | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.42 | PASS |
| D22 | `python3 scripts/ci_rv32_sdk.py --destination $DEPS_ROOT/rv32-sdk` | 0 | 2.12 | PASS |
| D23 | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | 2.02 | PASS |
| D24 | `python3 sw/builder/test_firmware_compiler.py --absent --audit $CHECK_ROOT/rv32-absent.jsonl` | 0 | 526.88 | PASS; compiler-absence controls; no compiler-dependent proof |
| D25 | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 50.8 | PASS |
| D26 | `python3 scripts/check_nvm_capture.py` | 0 | 1.07 | PASS |
| D27 | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.32 | PASS |
| D28 | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.73 | PASS |
| D29 | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 3.43 | PASS |
| D30 | `python3 scripts/measure_naming.py --selftest` | 0 | 0.62 | PASS |
| D31 | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.33 | PASS |
| D32 | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.88 | PASS |
| D33 | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.87 | PASS |
| D34 | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.42 | PASS |
| D35 | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.52 | PASS |
| D36 | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.77 | PASS |
| D37 | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.53 | PASS |
| D38 | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.27 | PASS |
| D39 | `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --memory 2g --cpus 2 --user "$JOB_UID:$JOB_GID" --mount "type=bind,src=$CANDIDATE_ROOT,dst=/candidate,readonly" --mount "type=bind,src=$CHECK_ROOT/container-D39,dst=/scratch" --workdir /candidate --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest` | 0 | 4.08 | PASS; offline self-test inside disposable container only |
| D40 | `python3 scripts/check_archive.py --selftest` | 0 | 0.12 | PASS |
| G01 | `make -C gptp-processor docs` | 0 | 0.83 | PASS |
| N01 | `(from $CHECK_ROOT/export) python3 scripts/docs_check.py` | 0 | 5.69 | PASS; Git inventory parity unavailable; B13 supplies it |
| N02 | `(from $CHECK_ROOT/export) python3 scripts/check_feature_status.py` | 0 | 1.08 | PASS |
| E01 | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | 0.17 | PASS |
| E02 | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | 0.42 | PASS |

The same existing dependency installations were reused. Logs, compiler
packages, source exports and rendered references remain in the scratch
directory; they are not deliverables. Generated builder files and existing
bytecode caches are retained outside the source under retained-generated.
The generated-inventory receipt records each retained file's size and hash.
The four-worker gate supervisor is joined by bounded foreground monitoring
before this session ends.
No simulation build, vendor implementation or bench access was requested.
The two early link-label findings were corrected before the authored commit;
the committed-head docs gate passed. No test or gate was weakened.

## Evidence receipts

Paths in this table are relative to this round's scratch directory.
Each command's .rc and .json receipt accompany its .log file.
Running logs are omitted until their exit receipt exists.

| Log | Bytes | SHA-256 |
|---|---:|---|
| `gates/B01.log` | 3792 | `4d839b2ccf6371c67de11a04c03954a6d144c14441fd82c2a96544a508744be6` |
| `gates/B02.log` | 1156 | `96ebcbb42272c4d901258e5cc10b99d058dc9409479b9d371c0af4c37c5000ff` |
| `gates/B03.log` | 15091 | `61dae71e5994ed60f28b823085dd25622914f5b4e1bd59ae314905b767705b74` |
| `gates/B04.log` | 1464 | `be88bddfc556b339891759005fb3ffb9796e00c2707271dedf7a5bc42af05c00` |
| `gates/B05.log` | 356 | `09f3c45fc26ddce8435f7247f03ec3d236a05798ceca3c6f87b4f81b2d3ee355` |
| `gates/B06.log` | 6708 | `b8b158060e6c5be0f67d6009b288a73ea58d4e11ea26ed7f55242f33b24b14f2` |
| `gates/B07.log` | 142482 | `8292f0bbd47b1b90ebe3aca5262974537e9aa3448ef8fe3867452d65b476badb` |
| `gates/B08.log` | 325 | `06b79c56f82c959120ff81af2de76f483afc775cdb191b9a761ab4dc2c01998d` |
| `gates/B09.log` | 218 | `e44962e88de4e46a63838b6b6adcf76712f6ad7e2ae860444feec3679f5a3959` |
| `gates/B10.log` | 236 | `33b39d29fa28260bcb643758431e05c18785258a0b4a78ab7a56d96808b4eac8` |
| `gates/B11.log` | 499 | `90fc9e7b0a66e651a0ebc555de0aefe07b8d6304ea7cfe6a6a787f3759bf1dcb` |
| `gates/B12.log` | 644 | `1667b0260dfdb361f4d992f93aeb9a947c4dde4bbce177c954f9a15618fd5cf2` |
| `gates/B13.log` | 307 | `1565ce8e32e8fd6a9ce5c973b0d8678754ec6cd04f2ad5fcc595712dff2c96d5` |
| `gates/B14.log` | 231 | `9880ebdfc2e22dd1ad824473452bcc6212c19bf3ad4b908853e97f16e086b78e` |
| `gates/B15.log` | 231 | `c69914c7fa55381e7014532b38ebd5d403c0b037411b9866a2802262ad06b029` |
| `gates/B16.log` | 275 | `499b5af2e4d1b920afa1c8763c2dbd3bfad45179e7c557506fc3e0a69b49e426` |
| `gates/B17.log` | 269 | `db0ca9b68f0c1592099cba36f806367ca5e02a875e0452c5c3f9ee65ca7e0a5c` |
| `gates/B18.log` | 275 | `733ed2270b977e464cedbc3eac91b29a911a0f237393f6f318f763cad70239cd` |
| `gates/B19.log` | 260 | `f0425d0ff05fb15752a2fc3a2e81549164b91237f7d6f03fa4c087c0ae0bd043` |
| `gates/B20.log` | 281 | `42cedc3bce7004ac1328025133599dc1e9ba04598e1fe76db714e67c4520c77e` |
| `gates/B21.log` | 2191 | `44404605e6cf362ffe3280216efc8e98973d1463b43d7de1c56dbef8c69d4fa5` |
| `gates/B22.log` | 350 | `f3dcb210f81be3c1b06ed84d15b95bd573fb3abb8dcc5dcd564bae3687ef1723` |
| `gates/B23.log` | 401 | `f273d5c349847a4b9378498cb02c04f705536cd1e5354d8bccd645e9bdc06f2b` |
| `gates/B24.log` | 418 | `9200f3b9b1496f7b3b0cd1e4d57949dc21d038a4cb374c79f1c431ca38887aa8` |
| `gates/B25.log` | 344 | `4179a487b5d66ccb8d089d0ed78779abea73b3fc067a04ffad2a9d063f09bdcc` |
| `gates/B26.log` | 271 | `14a3fbee5f1ba6818f652cc5ec6c743db7e319e238712bbd08dcb2609e2ba2f4` |
| `gates/B27.log` | 610 | `de21f71432b2e3f21c7a86b311016bc85f2631de09f2f92e9e2063b74b2950ce` |
| `gates/B28.log` | 2769 | `fd54602586b30914464eaaa9763bb408570e0007a3a173fcbd697362d4fb2044` |
| `gates/B29.log` | 272 | `c5e9042bfdd649614744b453da9745af02b62aaa875d89037cf448433c8644da` |
| `gates/B30.log` | 246 | `e77693924755a2d79c4154ff5f533f6dfb0780ccbacee841294f8c7f2810c646` |
| `gates/B31.log` | 5407 | `04c8e3a573b9ca36f7507fff7636f1217621771750f0ec7734eb2e78f8966cda` |
| `gates/B32.log` | 19895 | `6b97e64c36f96a7460d203bc4ee905fca7f6a176e085a6b901db776de3cb2735` |
| `gates/B33.log` | 738 | `6f35675c753d01842d033e1b70031ef3dc2532f4efabb8a585359fe6b2f4cf3c` |
| `gates/B34.log` | 2768 | `b8b35d62a05422f3ba4c44cdae7815f8197c78bc8af9616185c094e27706a0d5` |
| `gates/B35.log` | 927 | `bd7b52cda12205eae796e1807db6834892975363a594147bcfbd72734d6bcc4f` |
| `gates/B36.log` | 377 | `b23965a6793121e98b551291d10a29610901adbfee4fbf6c602b2d50159e1bed` |
| `gates/B37.log` | 6282 | `7ac5931874af473e8b7651deff3b2bc0b11389a7767819ff51e5c57624c923bb` |
| `gates/B38.log` | 14836 | `a830f2161f99eade21a933f5b6f5109d6b11cfcbcc16294a8418eb322b4c226d` |
| `gates/B39.log` | 36802 | `a8c20e1b62679508e2100b178ea183a60ac6358f1c11090b1e71f69af7ccc2e8` |
| `gates/B40.log` | 5863 | `dd0dc6d517630afc56b9f16c07eadddb95bcfbaa0ba759bb4211c21da54fa14b` |
| `gates/B41.log` | 228 | `e2287b900963265f93aa8be9e6461aad01557ba6a8b1d129b588c21ad716b5ed` |
| `gates/B42.log` | 238 | `114fd1d3bebd0fb5ad21832a086bd7618f477e59aa44f217cab640ff5fb9ed7c` |
| `gates/B43.log` | 249 | `d508bed07265e801367b8f9c7163f9fa7041e8f941792f1f1d919dfcd01897d2` |
| `gates/B44.log` | 220 | `d5d35c467a8761bcace76ab2dbd4912678d40bfd5f0b3ba3a582c3838c0cc7c8` |
| `gates/B45.log` | 5174 | `a4557170e6c0509cd8e8595ea6b366724db99cb1b25470af19578cd8757bdea0` |
| `gates/B46.log` | 25899 | `fada4b735da436ca58dc42ad37fc175563a5104a441e9a0edf295aabe0be4c65` |
| `gates/B47.log` | 9478 | `d7078ccbdce51ef1ca61b02f7a818d2a40e3ce815345c58f8f4f93358c3f0301` |
| `gates/B48.log` | 102484 | `58f62c2414f2b56cd3d41e41379e4e8a35baa349fddb22761d02b50e771b5f38` |
| `gates/D01.log` | 621 | `ad18512c60a6045db5f5dee0d692ca2de60e11a9c47184d1f34a5fa147825816` |
| `gates/D02.log` | 652 | `dc33b4a9bec8afd60b4839db34212aa5cc696587bca518ca03e175ea5455cebb` |
| `gates/D03.log` | 225 | `2fd3a1fea37af5d747d1b961dc61937d3d84510527eb90fb7c2660e288b3c7b2` |
| `gates/D04.log` | 244 | `d1d24953b344dc9690df3e30d79a4636f4ed87f8e150afab00337beae029401c` |
| `gates/D05.log` | 249 | `9ad901a81c109bd52487b0d600e4fb38f80cd4299f7bee603cbb5d1b69c0296e` |
| `gates/D06.log` | 251 | `36d4166531b2fedef70a389328fb9f2d146ba1b42ca311ce2cda3994924bea80` |
| `gates/D07.log` | 264 | `ea35992a29a25f0577ca32ff31582a99098c04136e7064e80c4d95a7af1c469e` |
| `gates/D08.log` | 268 | `4b077a741342c4e036462cde193e176920eb158ac015e946a59897aa061d0a69` |
| `gates/D09.log` | 261 | `b479c62bb80ca3227b9932c9894c9caa6886930489c028deb4cf3c4a4f72f4f1` |
| `gates/D10.log` | 264 | `7237160aa3a46b4efa43753c68168c228ea265c6fb29bfffe353b0b20951620e` |
| `gates/D11.log` | 273 | `53c93ea4dd695db09801777411b96bba4bc010ea92d8532e284a129c20e24b08` |
| `gates/D12.log` | 269 | `da34d0ca1bb5dc7a91533e11c80e5c9da3675ba441d968dd5a3c17421b235b6f` |
| `gates/D13.log` | 272 | `8d58ec6d8eb4514bdb25e3b6c74862ddc0a5c683ef138baf275d91ee651ecbb2` |
| `gates/D14.log` | 315 | `0e4acd9ff2ff31bca0078ff9ab77af000653ad98cabaa33d6d9c1a77956acfd7` |
| `gates/D15.log` | 307 | `59834435f143393a567a5f851bdbfb6a6a20596d416cf5f7feea9e5fb11c1a28` |
| `gates/D16.log` | 303 | `c3d5df396251f9e407ad351e5333c0d8d67a699999b7690d80580c4064374995` |
| `gates/D17.log` | 253 | `9901003f14fcbcf70f124178db765c6f188d5c30c0adbe4ef60bf53bb0d0d959` |
| `gates/D18.log` | 260 | `58071bb97ddc8c53784c3c6f8699d2dbc873b088d1efc2e8a15c29a69312b2b3` |
| `gates/D19.log` | 1704 | `0185d45b816cf1cd00877cddd1485940766bf60a5b986926a69ab14a1e3b3666` |
| `gates/D20.log` | 270 | `b85ff924c212266c93f4a58f75b5f135a790ded7ea60d466e70058a1a90bd2c0` |
| `gates/D21.log` | 6704 | `5aa6447406e1a7fdaab1f1036b790560d2f043d57e2e42b202981156218bcdfc` |
| `gates/D22.log` | 1719 | `87cac55609ac1a3b10967f354a348b3345ad2324c7875af188f8b088fced319c` |
| `gates/D23.log` | 346 | `4a3b5484d292faad6653067ed06d8fb71156dc37c8ad4f5f6f9cc2e152bb8002` |
| `gates/D24.log` | 50804 | `bab994eedb1acd794cc3ba1d257f4a6fa3bbc5ba48e05aa3b8aaa159dc389160` |
| `gates/D25.log` | 7216 | `9e2c897de2e99d9f8bc6b7093a8f1b96b102f5cd5a82e148a26d31afd667ad13` |
| `gates/D26.log` | 510 | `a81aeae4f1b57f87bde9e6c88af79f314e6425ceaba5e3b5a427547bb8f32fe5` |
| `gates/D27.log` | 1701 | `5882f93daa8c8cbfb351cd3c2da24a4ac0bc8cf6dde7455eca8cd59d6c068659` |
| `gates/D28.log` | 3334 | `fc66f2ff99a116f3994d228e5e948419a1f446d5c157fd275335a5f11791984c` |
| `gates/D29.log` | 3505 | `36955ff751516f29018424971455e98bca554568262df6614d08f19b198cf694` |
| `gates/D30.log` | 4223 | `73824727f7997f88c564cd5923bc77e17ff0f3b13fd6704691896c5410b3c5f3` |
| `gates/D31.log` | 4822 | `2905d3d38b5304bb1bb8692d03f7da2ad5ea9ee218ae4fe8073f5d1983b0000b` |
| `gates/D32.log` | 6797 | `799f79cbbc80ede8f488b1b10782ec7c9ad7bb9d2db7d300d63fca3d739dd121` |
| `gates/D33.log` | 2787 | `f7e5c08d1e41bf5a1661a947de300a23ea7fa5acf2978e7cd29d22ab587acb39` |
| `gates/D34.log` | 2043 | `eca283a3e31fa111edfe10b067c980efd396953a1f527ee817697cce48eb877f` |
| `gates/D35.log` | 3152 | `906b4f895a84337a5b518eb84a21085d1f9193ed42a45be6dc8e9db46a461896` |
| `gates/D36.log` | 3791 | `3c5656ca20902ef58e63e0fcc500645af54f0c5901aab3142de5d6398d2d3147` |
| `gates/D37.log` | 2728 | `ca2157dac1a4b37b0080c2b81a6f7d8ddc907654544572ed87f57823d08d1c86` |
| `gates/D38.log` | 2658 | `fea8cde891d552fc1eef651267c82479be329c42e015e6cad9cf1075135b8a30` |
| `gates/D39.log` | 37111 | `f0918a7260382d009f207d9fd50fb841457525b3c39301ed1163e849c305b93b` |
| `gates/D40.log` | 231 | `f7863fc2da1007c35cc505915acba7f1023ca9d4a38fd316cf731a4e887bc741` |
| `gates/G01.log` | 2822 | `7d5382e95efdc39826b3f0c24abf33f56fca5e39a63b5515f290eb79449ffdbf` |
| `gates/N01.log` | 381 | `6628bb750cfe027708a907c0c49573c2787380916fb1919bbdbe754b9fe99b77` |
| `gates/N02.log` | 224 | `1ef05169c7c5eef2ac4314c84e32b7feea676037a703db0ad1376f5565e57c83` |
| `gates/E01.log` | 236 | `1c7598b0b46902ab22b0eff8bf3c51f696f152985aa1ee5de41082d1ea11df0d` |
| `gates/E02.log` | 1947 | `f3c48ff7532ac0c22668e2b10ea6019af09ba60e178553e2761d1f2e74eb8e61` |
| `head.tar` | 33003520 | `db626910511f279d26bfe0453e69a6a764dd89939411165c82a86ee1e30fe991` |
| `contradiction-base.json` | 353273 | `c5ac8ae28ccab00d2f7db1d1674d4c0ebc6d302d85a340af4dbbfae6ea9463b4` |
| `contradiction-head.json` | 377388 | `38dc96fa6ba2605304d8696abe9fdd735ce0b1a4a539270b80a750f078f4b6a9` |
| `manifest.json` | 11267 | `b4fd4b761af3a26f5cf8e63bcca93fd6921a4e813cdb455911aec3b6adb0292d` |
| `approval-delta.json` | 13993 | `e644f3d2f70ca801865fa07b076cacaef92b08e6e08d90342db65890ac278ffb` |
| `delivery-audit.log` | 543 | `97e6f90df8a808e9f144441b4ea1b46d3f556c012a5d5984f6cf8176fa593c3c` |
| `delivery-audit.json` | 1033 | `a8da64d334ecadbed61441a5fd345c0360fbec990be45f56025afb8574924bbe` |
| `integrity.log` | 759 | `bac67c59058f8815fee926e597572fd36c6cd3f46b5e9b77991f5926ba5f26a9` |
| `workflow-coverage.json` | 5692 | `1493f9ea37671e60110026925e7764bb9ea1eb2250eb98d712a5dbf241ceda48` |
| `bank-audit.json` | 16639 | `5784681d2a37dd9eb27154133df0234950692514ea8f007d20d80f469482b7ce` |
| `generated-inventory.json` | 68115 | `55cea56790400cce5614f88b80389956983b7061d5322396627545c5d402afab` |

## Acceptance and remaining work

- The full-tuple filter and FILTER_MISMATCH remain implementation obligations
  for the contract lane after FT, before F2 to F5. Existing F0 output stays unchanged.
- The 10 ms value and existing requirement text are approved at 8fb296e3.
  The new filter text still needs the manager's decision-parity check and fresh reviews.
- Source gates do not establish target runtime timing, bench acceptance,
  hosted CI or final candidate acceptance at merge time.
- Vendor analysis is skipped. The builder's historical placement calibration
  is NOT RUN without its report. Neither is a hardware proof claim.
- R509-2-R1 is a manager residue item outside the ingress-only assignment.
- During this round the executor made local commits and the required dev
  merge, and posted only TAKEN and the final handoff on issue #664.

## Definition of Done

- [x] Ingress requirements and hooks from the assignment are documented
- [x] Unrelated approved requirement text is preserved
- [x] Future filter behavior has explicit self-checking hook obligations
- [x] Required local documentation and builder command bank completed
- [ ] Self-test evidence is published to the PR by the manager
- [ ] Manager verifies filter text against owner decision 6014311316
- [ ] Internal cleared-context review is positive at the new head
- [ ] External review is positive at the new head
- [ ] Reviewer-owned lens coverage is accepted and no review remains in flight
- [ ] Current-dev candidate and hosted/local-replica evidence are accepted
- [ ] Explicit release-merge authorization is recorded
- [ ] Post-merge containment completes before the issue moves to Done
