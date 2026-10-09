[R565] NEGATIVE - exact head 1e68d1b62ef2facdf0e8dbad28a202297d433c61

External independent review, round R565-1, issue #665 / PR #700, lane F5.
Tree: `ba72813fa634b7df0d9b937a144e427c6dd63ab6`.
Diff base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

Three MAJOR findings and one MINOR finding remain open. All five lenses were applied. The four independent probes complete with assertion failures at this head, while the standing composed suites pass at both interface counts. No production source was changed. This review does not clear any affected lens or authorize merge.

The independent verdict and ledger were written before examining prior public review findings. At the subsequent public-state check, PR #700 had two review-start comments, no submitted reviews and no inline comments. There were no prior published findings to resolve or retain. See `receipts/public-review-reconciliation.json`.

## Authority and reconstruction

Read the operating contract and CONTRIBUTING, the documentation index, then the frozen issue scope and public decisions before reviewing the normative references, code and evidence. The review covers the 19-commit, 36-file diff from the stated base, including the final maximum-body latency change. No private implementation material or other reviewer's report was used.

Principal public references:

- [F5 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081266905), [224 KB owner ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916), and [source review-ready evidence](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6084993566).
- `REQUIREMENTS.md`, `docs/reference/FR_NFR.md` NFR-SCOUT-02/03/08, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/MAILBOX_SPLIT.md`, and `sw/mailbox/README.md`.
- IEEE 1722.1-2021 7.4, 7.5 and 9.3; Milan v1.2 5.4 and Table 5.22, read from the standards themselves.
- [#637 saved maps](https://github.com/kebag-logic/milan-fpga/issues/637), [#653 response ordering](https://github.com/kebag-logic/milan-fpga/issues/653), [#678 callback boundary](https://github.com/kebag-logic/milan-fpga/issues/678), and [#697 portability boundary](https://github.com/kebag-logic/milan-fpga/issues/697).
- Processor [#69 interface contract](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69) and [#73 command model](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73). The latter remains open; future adoption is owed and is stated in the AECP README and PR.
- [Immutable public source evidence](https://github.com/kebag-logic/milan-fpga/tree/c7078141c09865a979913272774331198a209b2f/review-evidence/665f5-r1). Downloaded evidence files were checked against the publication manifest; `receipts/public-evidence-integrity.json` records their hashes. Historical preflight `evidence.json`, `integrity.json` and `link-receipts.json` concern the earlier base/128 KB STOP and are not final-head execution receipts.

## Findings

### R565-1-F1 — MAJOR — Conformance, Robustness, Tests

**Artifact:** `sw/firmware/ctrl/aecp/aecp_commands.c:83`; `sw/firmware/ctrl/test/test_aecp.cpp:530`.

**Title:** READ_DESCRIPTOR rejects an ignored configuration index for root descriptors.

**Authority/evidence:** IEEE 1722.1-2021 7.4.5.1 and 7.4.5.2 require the configuration index to be ignored on receipt for ENTITY and CONFIGURATION descriptors and transmitted as zero. The implementation validates this field before resolving the descriptor. The standing test explicitly expects BAD_ARGUMENTS for ENTITY with configuration index 1. `Core.R565ReadDescriptorIgnoresConfigurationForRootDescriptors` requests both descriptor types with configuration indices 1 and 65535. All four responses return status 7, echo the nonzero configuration and contain only the failure descriptor fields. Expected complete frame lengths in this fixture are 354 and 148 bytes; actual length is 46.

**Impact:** A valid root-descriptor read is refused because of a field the receiver must ignore. The native test enforces the same incorrect interpretation. Agreement with a fabric implementation would not establish conformance.

**Required outcome:** Resolve these two descriptor types independently of the received configuration field and emit zero in the response field, preserving descriptor-index validation and configuration checks for other descriptor types. Correct the standing test and the standards-based differential expectations.

**Verification:** The root-descriptor probe in `scripts/probe_cases.cpp` must pass. Include invalid root descriptor indices and ordinary configuration-scoped descriptors, with a planted regression reinstating the inappropriate configuration check. Raw reproduction: `receipts/independent-probes.log`.

### R565-1-F2 — MAJOR — Conformance, Tests

**Artifact:** `sw/firmware/ctrl/aecp/aecp_commands.c:276` and `:308`; `sw/firmware/ctrl/test/aecp_wire_oracle.py`.

**Title:** Successful SET_STREAM_INFO echoes request fields instead of current stream information.

**Authority/evidence:** IEEE 1722.1-2021 7.4.15.1 defines the response's current stream format, stream ID, destination MAC, VLAN and applicable validity flags. Milan v1.2 5.4.2.9 adopts that command and changes the latency behavior: successful latency echoes the requested value, but the other response-field rules remain applicable. The setter copies the request, updates latency and returns before the current-state serialization used by GET_STREAM_INFO. `Core.R565SetStreamInfoReturnsCurrentObservationFields` uses available, nonzero observations from the existing fixture. The successful response has zero format, ID, destination MAC and VLAN. Its latency assertion passes.

**Impact:** A successful mandatory command reports incorrect current stream state. Request fields and flags are echoed in place of response values. The differential's agreement checks do not independently establish these field semantics.

**Required outcome:** Form SET_STREAM_INFO responses from the applicable current descriptor and observation fields with the response validity rules, while preserving Milan's requested-latency behavior. Add clause-based assertions with nonzero current state to the native and differential checks, including refusal response semantics.

**Verification:** `Core.R565SetStreamInfoReturnsCurrentObservationFields` must pass; extend the standing checks to cover the applicable validity bits and plant request-echo regressions. Raw reproduction: `receipts/independent-probes.log`.

### R565-1-F3 — MAJOR — Conformance, RTL, Robustness, Tests

**Artifact:** `sw/firmware/ctrl/aecp/aecp.c:422` through `:448`; `sw/firmware/ctrl/test/test_aecp.cpp:873`.

**Title:** An unavailable observation indefinitely blocks unrelated required notifications.

**Authority/evidence:** Milan v1.2 5.4.5.2 Table 5.22 requires the asynchronous notification set. The port contract permits unavailable snapshots. The asynchronous scan restarts at descriptor zero each poll and returns after the first pending event even when its snapshot failed and remains pending. `Core.R565UnavailableStreamDoesNotStarveOtherNotices` queues a STREAM_INPUT GET_STREAM_INFO event whose provider returns false and an independent AVB_INTERFACE GET_AVB_INFO event whose provider succeeds. After 1000 polls over 999 ms, no AVB notification has been sent. The failed stream event remains pending. Standing snapshot tests check refusal/retry, but do not establish progress of a later independent event.

**Impact:** Persistent failure of one observation suppresses notifications for later descriptors indefinitely despite available providers and transmitter. A local service bound for the blocked notification cannot hold on this allowed failure path.

**Required outcome:** Preserve retry of unavailable snapshots while allowing independent eligible notifications bounded progress. Do not discard the failed event or emit an invented successful observation.

**Verification:** Run the two-event probe, then cover recovery, multiple unavailable events, transmit backpressure, counter spacing and interface fanout. Plant a regression restoring the early-return starvation. Raw reproduction: `receipts/independent-probes.log`.

### R565-1-F4 — MINOR — Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/aecp/aecp.c:5`; `sw/firmware/ctrl/test/test_aecp_debug.cpp:16`; `sw/firmware/ctrl/aecp/README.md:37`.

**Title:** The callback guard does not enforce the documented cross-instance rule.

**Authority/evidence:** Issue #678 requires F2-F5 adoption of the no-synchronous-callback rule with diagnostic assertion and release refusal/counting. The F5 contract explicitly includes another instance and claims this enforcement. `enter()` checks only the destination instance's `in_port`. `Core.R565CrossInstanceCallbackIsRefused` calls `aecp_open()` on a second initialized instance from the first instance's change callback. The second instance opens and records zero refusals. The diagnostic test sets the same instance's flag directly and covers no actual cross-instance callback.

**Impact:** An adapter violating this documented integration boundary is accepted silently, allowing nested core work excluded by the event-loop contract. In-tree adapters need not violate the rule for the required guard to remain incomplete. The documentation's enforcement claim is false at this head; this is not wording-only residue.

**Required outcome:** Enforce the agreed boundary across instances and public inputs, with diagnostic assertion and release refusal/counting. Keep the contract and actual guard scope consistent; exercise real callbacks rather than only setting an internal flag.

**Verification:** The cross-instance probe must refuse the nested entry without opening the second instance. Add a diagnostic equivalent and a guard-removal mutation. Check initialization and the other public entry points against the same boundary. Raw reproduction: `receipts/independent-probes.log`.

## Assignment coverage and other results

| Assignment item | Artifacts examined and result at this head |
|---|---|
| Portable core and adapter | `aecp.h`, `aecp_model.h`, core/commands/maps/state units, `aecp_image.c`, `aecp_mbx.c`, `aecp_nvm.c`, `ctrl_app_aecp.c`. Protocol state uses caller storage and typed ports; image parsing and mailbox/register knowledge stay in adapters. Directory relocation under #697 is separate work. Guard exception: F4. |
| Every image descriptor | `aecp_entity.py`, `aecp_shape.py`, image loader and descriptor lookup; all five image fixtures pass, including hostile directory/header cases. Root descriptor command semantics fail F1. |
| Mandatory command/status/field rules | Reviewed the dispatch and handlers against IEEE 7.4 and Milan 5.4: ACQUIRE refusal; LOCK/ENTITY_AVAILABLE; configuration; format; stream information; names; sampling rate; clock source; IDENTIFY control/refusal; START/STOP; register/deregister; AVB info/AS path/counters; audio maps; dynamic info; MVU Milan info/system ID; unknown-command NOT_IMPLEMENTED. Current-value refusal, lock/running precedence, descriptor geometry, lengths, whitelist and per-record status were examined. F1/F2 are the command findings. |
| Notifications and #653 | `aecp.c`, completion cookies in `aecp_mbx.c`, bridge polling and `App.MediaUnlockedNoticeCannotPassAnOwedUnbindResponse`. Response precedes command notification; UNBIND_RX acceptance precedes MEDIA_UNLOCKED; per-recipient sequence and final TX_TAIL counter spacing are tested. The ordering mutation was independently caught. F3 blocks complete notification compliance. |
| Saved maps and #637 | `aecp_maps.c`, `aecp_state.c`, `aecp_nvm.c`, application/NVM tests. Reviewed atomic restore, default identity clipping, rejected-map rollback, live format compatibility, global output-map ownership and deferred dirty marking. The map-framing mutation was caught. No additional finding. |
| Interface indexing | `aecp_config`, registration arrays, source MAC/egress and descriptor-derived observation interface, mailbox/application bridges. Composed one/two-interface suites pass. Locks/configuration/scalars remain entity-wide; registrations/liveness/egress remain interface-specific. |
| 100% ratchet and per-check plants | `coverage.ratchet` adds eight 100% line/branch entries and changes no exclusion. The source evidence reports 66 named checks and 59 caught plants; the campaign audits test ownership and requires completed named assertion failures. Five representative plants were independently reproduced. F1-F4 expose semantic gaps despite that coverage. |
| Wire differential | Read both drivers, source fingerprints, paired providers and oracle. Published results: 123 observations for one interface, 128 on each two-interface ingress, 42 descriptors, 31 AEM command codes including refusal paths, three MVU codes, 17 notification kinds and six oracle controls per ingress. Recorded differences are clause-labelled below. F1/F2 require standards-based expectation changes, beyond implementation equality. |
| Service latency | Read `aecp_latency_policy.hpp`, latency cases in `test_aecp.cpp`, and published per-path measurements. The desk cases pass under explicit assumptions; the failed-observer progress path F3 is uncovered. No target CPU or physical timing proof is inferred. |
| Linked sizes/resources | Read link fixture, builder changes, size matrix and runtime provenance; checked size/tile arithmetic and top BSS consumers below. Author-published spans fit the revised 224 KB stop threshold. No independent relink or routed-fit claim. |
| Scope containment | Exact diff has no RTL, submodule pin, product configuration, register-map or default shipping-entry change. The opt-in AECP link fixture does not replace the shipping image. |
| Required gates | Source execution evidence is the author's published receipts. Independent focused results are listed below. The manager's current-dev candidate builder/native banks and local-replica/hosted acceptance remain distinct and pending. No manager source bank exists or is inferred. |

The four permitted wire differences were examined against their cited clauses: core SET/GET_SYSTEM_UNIQUE_ID versus the reference's refusal (Milan 5.4.4.2/.3); first default-valued format/rate SET establishing persistent override intent and notifying (5.4.5.2); the core's additional changed-started-state GET_STREAM_INFO notification (Table 5.22); and unlock flag 1 versus 0 with owner zero (IEEE 7.4.2.1). These do not excuse F1/F2. The two-interface reference exposes ingress without a physical egress index; the evidence checks registration isolation and the core's egress index separately.

Published service maxima are 1.0770 ms for commands/refusals including maximum bodies, 1.1573 ms for full fanout, 2.0069 ms with a one-millisecond TX stall, and 9.0061 ms for deferred failure. These include 100 ns access/observation and 1 ms CPU allowances, measure acceptance at TX_HEAD, and are compared with T_svc = 10 ms and the 240 ms AEM response timeout. They are conditional desk bounds. Counter spacing separately uses final TX_TAIL retirement. Scheduling/calibration, complete call-chain stack bounds and physical egress remain integration work.

| Linked fixture | Interfaces | Span including 8192-byte stack | Nominal RAMB36, 4608 B/tile | 4096 B data packing |
|---|---:|---:|---:|---:|
| Shipping shape 1x1_tdm8 | 1 | 139072 B | 31 | 34 |
| Shipping shape 1x1_tdm8 | 2 | 151728 B | 33 | 38 |
| Largest shape 8x8 | 1 | 192240 B | 42 | 47 |
| Largest shape 8x8 | 2 | 219744 B | 48 | 54 |

The largest span fits both 224000 B and 224 KiB (229376 B). The author reports RV32I/ILP32, no-heap/unresolved-symbol and retained-symbol checks on all four links, with input/archive hashes. BSS already includes the listed pools. Runtime source provenance distinguishes the two compiler installations; it does not assert identical compiler binaries. The physical fixture observers explicitly report unavailable values, so the size fixture is not a deployed board image.

The largest/two-interface BSS leaders and published reduction options are: `image_arena` 48064 B (audit MRP capacities/peaks); `nvm_stage` 13264 B (consider streamed groups only with atomic restore/commit proof); `image_values` 11753 B (sparse mutable overlays with alias/bounds proof); `image_app` 9640 B (audit bounded queues); `image_srp` 5864 B (audit duplicated state/capacities). No unrelated storage reduction was made. The later default flip still owes actual routed RAMB36/LUT/FF fit and the owner's reserve.

## Execution and evidence accounting

The foreground drivers joined their independent jobs, each with its own receipt, within the 16-job limit. All disposable builds and mutations are under this packet's excluded `scratch/` directory. The pinned simulator was identified before use; its version receipt is included. No forbidden full bank, host orchestrator, container, hardware run, source fix, commit, push or GitHub write was performed.

| Independently executed check | Result | Raw receipt |
|---|---|---|
| Composed AECP, one interface | 62 tests passed; rc 0 | `receipts/app-if1.log`, `.rc` |
| Composed AECP, two interfaces | 62 tests passed; rc 0 | `receipts/app-if2.log`, `.rc` |
| Image fixtures and diagnostic guard | 3 tests on each of five shapes, plus 1 diagnostic test; rc 0 | `receipts/images-debug.log`, `.rc` |
| Five selected source plants | All named assertions caught; campaign rc 0 | `receipts/selected-mutations.log`, `.rc`, and individual logs under `receipts/selected-mutations/` |
| Focused mailbox `run-cosim` | 32 checks, 0 failures; rc 0 | `receipts/mailbox-cosim.log`, `.rc` |
| Mailbox generator `--check` | rc 0 | `receipts/mailbox-generator.log`, `.rc` |
| Documentation check | 0 findings; rc 0 | `receipts/docs-check.log`, `.rc` |
| Four independent defect probes | 4 completed tests, 4 assertion failures; rc 1 | `receipts/independent-probes.log`, `.rc` |
| Actual tracked identity, before/after | Exact blobs, file kinds/modes, index and required submodule pins pass; final status empty | `receipts/identity-before.log`, `identity-after.log`, `git-status-after.log` |

Selected plants were `descriptor-last-byte`, `scalar-refusal-reports-request`, `counter-spacing-short`, `app-notice-overtakes-unbind` and `nvm-hole-accepted`. The original assertion grader was retained. The full test-to-plant ownership control was run before selecting the subset; the subset's second full-table census was omitted because this was explicitly a focused campaign. It is not reported as the full 59-plant campaign.

The first independent-probe harness attempted a cross-file fixture include and failed a compiler warning promoted to an error. That receipt is retained as `receipts/probe-setup-failed.log`; it is not a production defect or a passing run. The portable driver instead concatenates the exact fixture and probe source in scratch. The subsequent completed run produces the four findings above.

The author's source evidence reports the complete firmware bank, sanitizer arm, 59 AECP plants, the unchanged inherited campaigns, raw coverage, full mailbox target, builder partitions and documentation workflows. `receipts/published-gate-audit.json` records attribution, return codes and partition cardinality checks. This review inspected those receipts and source graders but did not independently rerun the full firmware/builder/coverage or wire campaigns, or the RV32 links. Hashed but unpublished binaries/logs were not inspected; source-summary claims remain attributed to their publisher. No manager source-head builder/native execution is claimed.

The hosted-job snapshot in `receipts/hosted-jobs.json` is verified against this head. At capture, all four portability shards and one of five simulation shards succeeded; four simulation shards were still running. Lint, BDD, change detection and fast elaboration succeeded; firmware, docs and the separate elaboration job were still running. Wire-accountability and no-git docs succeeded. The physical nightly/manual job was explicitly **skipped**. A successful scheduling job is not proof that its dependent suites have completed. No all-green hosted acceptance is claimed, and no hosted completion was awaited.

## Reviewer-owned ledger

Paths in this table are repository-relative; file basenames under `sw/firmware/ctrl/aecp/` denote those exact files. RTL is the architecture lens as well as hardware review; the absence of RTL edits does not exclude the portable core's progress and integration contracts.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1-F4 | #665 scope/ruling; #637/#653/#678; IEEE 7.4/7.5/9.3 and Milan 5.4; `aecp_commands.c`, `aecp.c`, maps/state/NVM; differential oracle and four independent probes | R565-1 | 1e68d1b62ef2facdf0e8dbad28a202297d433c61 |
| RTL | UNCLEAN — F3/F4 | `receipts/source-inventory.log`; `aecp.h`, `aecp.c`, `aecp_mbx.c`, `sw/firmware/ctrl/app/ctrl_app_aecp.c`; mailbox completion/event-loop contracts and `receipts/mailbox-cosim.log` | R565-1 | 1e68d1b62ef2facdf0e8dbad28a202297d433c61 |
| Robustness | UNCLEAN — F1/F3/F4 | Parser and image bounds; unavailable snapshots, backpressure, timeout/reset/reentry; `aecp_maps.c`, `aecp_state.c`, `aecp_nvm.c`; native failure cases and `scripts/probe_cases.cpp` | R565-1 | 1e68d1b62ef2facdf0e8dbad28a202297d433c61 |
| Tests | UNCLEAN — F1-F4 | `sw/firmware/ctrl/test/test_aecp.cpp`, image/debug tests, `aecp_mutants.py`, wire driver/model/oracle; `coverage.ratchet`, public test ledger and executed receipts | R565-1 | 1e68d1b62ef2facdf0e8dbad28a202297d433c61 |
| Docs | UNCLEAN — F4 | `docs/README.md`, `REQUIREMENTS.md`, FR_NFR, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, MAILBOX_SPLIT; `sw/firmware/ctrl/aecp/README.md:37`; public scope, PR and source evidence | R565-1 | 1e68d1b62ef2facdf0e8dbad28a202297d433c61 |

There are no separate wording-only RESIDUE findings. Every finding above changes required behavior, a test expectation or the truth of an enforcement claim.

## Reproduction, integrity and pending duties

Use the exact source head and initialized required submodules. With `CHECKOUT` set to that clone and `PACKET` to this directory, the included portable scripts reproduce the focused work:

```sh
python3 -B "$PACKET/scripts/verify_tree.py" "$CHECKOUT"
python3 -B "$PACKET/scripts/run_focused.py" "$CHECKOUT" "$PACKET"
python3 -B "$PACKET/scripts/run_supplemental.py" "$CHECKOUT" "$PACKET" \
  --verilator $VALIDATION_TOOLS/pinned-verilator-5.050/verilator
python3 -B "$PACKET/scripts/verify_tree.py" "$CHECKOUT"
```

`run_focused.py` permits the expected negative-probe process to return 1 while recording that code separately; its driver exit is not a positive conformance verdict. Use a separate packet copy for reproduction to preserve the published receipt hashes. Prerequisites are the repository's existing native-test dependencies and the verified scoped simulator; no installation is performed by these scripts.

The final verification compared all 1263 root tracked blobs and index entries, plus actual tracked bytes/modes/index in the four required submodules: gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, lwSRP `9197193e47a6bb1c45a56d90a18c1784123aba44`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The separate external gitlink remains `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`; it was not needed or initialized. All production bytes remain at the exact head; no restoration was needed. `MANIFEST.sha256` enumerates every publishable receipt and script, with relative paths. Scratch is excluded.

The four findings require fixes and independent re-review at the corrected head. The manager retains publication, local-replica and hosted acceptance, current-dev merge-candidate builder (48) and native (5) banks with linked receipts, no-review-in-flight checks, explicit merge authorization and post-merge containment duties. The source base and live dev supplied for this round are both `5603c353137e90c1fa95429f6d00ef7a2298d9ee`; that does not substitute for validating the eventual current-dev merge candidate. Physical calibration is **NOT RUN**, and field skips are not hardware proof. Processor #73 adoption, target observation wiring/timing, full stack bounds and routed reserve remain the explicitly stated later obligations.

R565-1 FINISHED
