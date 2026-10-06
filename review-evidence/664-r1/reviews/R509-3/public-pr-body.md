[A548]

## Contents

- [Status](#status): candidate and validation state.
- [Linked Issue / roles](#linked-issue--roles): task and review ownership.
- [Description](#description): ingress filter additions.
- [Authoritative references](#authoritative-references): decisions and clauses.
- [Requirement text for owner approval](#requirement-text-for-owner-approval): only this round's old/new delta.
- [How to get into the same state](#how-to-get-into-the-same-state): candidate and dependencies.
- [How to validate](#how-to-validate): exact command bank and results.
- [Known limitations / out of scope](#known-limitations--out-of-scope): remaining proof and reviews.
- [Definition of Done](#definition-of-done): completion conditions.

## Status

Round 3: ingress filter requirements and hooks only.
`664-mark2-reqs` -> `dev`.
Candidate: `4dab80ae4564ef8d6e1030564dcea4ba19235ee6`.
Validation base: `30e3c018b9add0cb182d8f1229eeec062218130d`.
All 93 command exits are zero. Vendor analysis is skipped; historical placement calibration is not measured.

## Linked Issue / roles

Relates to #664

Executor: `[A548]`
Internal cleared-context reviewer: `[R508]`
External reviewer: `[R509]`

## Description

Tagged and unrelated control traffic must stay out of the mailbox.
The requirements now match VLAN presence, destination MAC, EtherType and
AVTP subtype before the protocol identity term. AECP admits both commands
addressed to this entity and responses to this entity as controller,
including CONTROLLER_AVAILABLE. Untagged control tuple failures increment
FILTER_MISMATCH; existing token buckets remain required.

NFR-SCOUT-08 traces the filter to the single-source mailbox contract and
the five named hooks. The hooks observe rejected input before RX publication,
so a missing record cannot disappear from the check. The F0 design page
marks its earlier command-only filter as current implementation awaiting
the later contract lane. This PR changes requirements, not that implementation.

Everything else is approved at 8fb296e3, including T_svc = 10 ms.
The required current-dev merge was clean. The authored additions affect
three Markdown files; the complete lane remains documentation only.

## Authoritative references

- #664 round-3 assignment 6014341135; filter decision 6014311316;
  prior-text approval 6014321497; original assignment 6009584763;
  owner decisions 6009576644 and budget ruling 6009675758.
- Prior positive reviews R508-2 (6010971658) and R509-2 (6011008257)
  cover 8fb296e3 only. This round requires new review.
- REQUIREMENTS section 1; FR_NFR sections 3.4, 3.4.1, 3.4.2 and 6;
  mailbox YAML; MAILBOX_SPLIT ingress section; generated MAILBOX_CONTRACT.
- IEEE 802.1Q-2018 Table 10-1: Customer Bridge MVRP address
  01-80-C2-00-00-21. IEEE 1722.1-2021 8.2.1/Table B.1:
  ACMP transmits multicast; own-unicast reception is the owner's tolerance.
- Milan v1.2 5.4.5.3: controller liveness and CONTROLLER_AVAILABLE replies.
- #665 directives 5992455815 and 6008744385; #640; merged F0 #668 and F1 #669.

## Requirement text for owner approval

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

## How to get into the same state

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

## How to validate

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

## Known limitations / out of scope

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
