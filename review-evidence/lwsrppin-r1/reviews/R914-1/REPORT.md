[R914] NEGATIVE - exact head dbba60e68a6e4a46f80e381c30ff823ee4ff7484

Round R914-1, external independent review of issue #991 / PR #992.
Base: `aa30d77f75cd97b3a29878ca0ed68010a7629266`.
Tree: `1e85cc2bb2ba13643ce6ae7cfb14a49a5a838c6c`.

The withdrawal fix reproduces correctly. One MINOR finding remains in the executable self-test census and its public evidence claim. Under the assigned completion rule, Tests and Docs are UNCLEAN. No functional defect was found in the pin change or the revised own-LeaveAll grading.

The task was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #991, the cited protocol and interface contracts, the four-commit diff, and then the public author evidence. No private author material or other reviewer's report was used. Acceptance remains the issue's red/green reproduction at both shapes, passing scoped gates, and unchanged tiles. The supplied owner-delegated disposition accepts the ROM mapping changes and reserves the routed build for merge. Issue #990 remains outside this change.

Public evidence examined: [author packet at c8dd5709](https://github.com/kebag-logic/milan-fpga/tree/c8dd5709168bfcce9d31f00ada7ed01141b77415/review-evidence/lwsrppin-r1/author). References below to `author/receipts/` mean that immutable packet. All 230 author entries match their published manifest hashes. The final commit changes only docstrings; receipts at `402834ac` remain applicable where the gate consumes none of the changed twin files. Twin and documentation receipts also ran at `dbba60e6`.

Finding R914-1-F1: MINOR; lenses Tests, Docs

Artifact: `tb/verilator/milan_dp/twin_mrp.py:449`, with the nine named calls at lines 419-440; PR #992, evidence-table row for `twin_mrp.py --selftest`.

Authority/evidence: AGENTS.md requires reproducible, accurate executable evidence; this review explicitly requires PR claims to match the packet. The command prints `OK (10 checks)`, and the PR repeats ten. Instrumenting execution of `selftest()` records exactly nine calls to `check`, with nine distinct names. `twin-probe.log` lists them. Counting the source calls gives the same result. The five planted faults remain caught; that does not create a tenth self-test case.

Impact: every successful run overstates its executed named-check census, and the public evidence repeats that overstatement. This is an executable measurement claim, not wording-only RESIDUE under the assigned rule. It does not establish a protocol or withdrawal regression.

Required outcome: report the actual executed census, nine named checks at this head, and correct the current PR/evidence summary. A dynamically counted total would prevent future drift. No additional test is required merely to retain the number ten; historical raw receipts should remain identifiable as historical.

Verification: rerun the command and the named-check census in `probe_twin.py`; the advertised number must equal the executed number. Retain the existing successful checks and five fault detections. Re-review Tests and Docs at the corrected head.

Independent lens evidence

[R914] PASS Conformance - `third_party/lwSRP/src/core/mrp_mad.c:771`, `:1509`, `tb/verilator/milan_dp/twin_mrp.py:180`, `:293`, and `sw/firmware/ctrl/test/srp_own_leaveall.cpp:205` - checked the issue's own-LeaveAll contract, Table 10-3 txLA!/txLAF!, Table 10-4 Registrar handling, and Milan's 240 ms withdrawal bound.

The dependency sends Registrar-only rLA! after successful transmission. Fitted Applicants take txLA! once; omitted Applicants take txLAF!. Incoming LeaveAll handling is unchanged. The twin permits omission through a bracketed txLA! cell or, only with insufficient room, txLAF!. It does not infer legality solely from the implementation's output. Independent probes check 72 combinations of application, Applicant and Registrar state. Minimum vector sizes are 28/37/12/7 bytes for the four MSRP types and five for MVRP. A decoded MVRP omission with 1,492 bytes used is not full; one with 1,497 is full. MAC padding contributes to neither length. The donor merge tree equals `25b5a740`'s tree, `ba42b8379d4a066580a8a5047083c355d102ae41`.

[R914] PASS RTL - complete 18-path diff; `sw/firmware/ctrl/srp/srp_mbx.c:515`, `:1262`; `author/receipts/ledger/image-deltas.txt`, `ledger/margins.md`, and `ooc/base.tsv`, `head.tsv`, `head2.tsv` - checked ownership, observer integration, retained-send semantics, image sizes and mapping against REQUIREMENTS.md section 1 and MAILBOX_SPLIT.md's firmware boundary.

No HDL, clock/reset, CSR or CDC implementation changes occur. The dependency preserves the observer callback's Applicant identity while reporting a real Registrar change; the adapter copies Registrar presence and schedules work without synchronous reentry. Send failure returns before state commit. Image `.text` grows 60 bytes; the only changed object is `mrp_mad.o`, whose object text total grows 64 bytes (13,155 to 13,219). Those are separate object and linked-section measurements in the receipts. Data, BSS, stack and tile counts remain unchanged. Platform 8x8/1if uses 104 bytes of its existing third ROM bank, with 1,944 bytes spare. Both head mapping runs agree: ROM +14 LUT/+13 FF at 8x8/1if, +23 LUT at 8x8/2if, and lower LUT counts at both 1x1 points. These accepted mapping changes are not findings.

[R914] PASS Robustness - `sw/firmware/ctrl/test/srp_own_leaveall.cpp:205`, `:249`; `third_party/lwSRP/src/core/mrp_mad.c:1494`; `third_party/lwSRP/tests/unit/own_leaveall_test.c:345`, `:572`, `:590`; `twin-probe.log` - checked withdrawal phases, concurrent bound inputs, held declarations, full/room boundaries, Registrar transitions and failed-send ordering.

The reproduction binds all streams simultaneously (nine inputs including CRF at 8x8, two at 1x1), then withdraws each while checking remaining bound inputs. It covers 43 offsets, including 129 ms and both sides of the 190 ms join timer. The 90-second held leg observes five board and two peer LeaveAlls with no Leave indication. It is not a simultaneous-unbind test. The Registrar-only loop allocates no MAP work and has no indicating rLA! cell. Existing retry, reset and malformed-input handling is unchanged; broader regression evidence is the published firmware gate, not a claim that the new focused test injects every such fault.

Tests applied, UNCLEAN only for F1 - `sw/firmware/ctrl/test/srp_arms.py:117`, `test_ctrl_firmware.py:211`, `tb/verilator/milan_dp/Makefile:1015`, `:1038`, `twin_mrp.py:398`; local `own-*.log`, `twin-probe.log`, and `author/receipts/firmware/gate-*.log`, `twin/dbba60e6-*.log`.

| Dependency | Shape | Withdrawals | Unsent Lv | Worst sent delay | Independent result |
|---|---|---:|---:|---:|---|
| 08ee86e8 | 8x8/1if | 387 | 351 | 190 ms | expected failure |
| 08ee86e8 | 1x1/1if | 86 | 78 | 190 ms | expected failure |
| d1bb4f4e | 8x8/1if | 387 | 0 | 190 ms | pass, 44 tests |
| d1bb4f4e | 1x1/1if | 86 | 0 | 190 ms | pass, 44 tests |

All four arms ran concurrently, four compiler jobs each, in disposable directories. The historical comparison changes only dependency selection inside a separate probe process; its source-tree pin verifier still runs. The reviewed checkout was not edited. Counts recounted from author logs match these local results. Both new-pin held legs pass.

Five independent in-memory mutations were caught: extra Applicant rLA!, removed txLAF!, missing Listener FourPackedEvents byte, capacity reduced by one, and missing MVRP EndMark bytes. The packet's five grade faults are also caught by name. Each of the two published head plant runs contains 32 explicit refusals: sixteen distinct plants, each checked twice. The unplanted twin reports zero findings. No captured LeaveAll is near full (least spare 1,359 bytes), so synthetic tests supply capacity-boundary evidence.

Firmware receipts contain 90 passing arms and 2,244 cases in passing verdicts. All four shards return zero with the required target build enabled; mutation shards report 832, 392 and 543 catches. No manager source bank is claimed. The published memory-ledger self-test reports 9/9 controls and zero findings; the memory test passes.

Independent load and flip checks pass and agree with the packet: loads 0.512/0.70 and 0.744/0.75; last notice 127.43 ms against 130 stated and 140 owner bound; ACMP 29.15/30 ms; txL 47.98/49 ms; 8x8/1if transmission row 76.81 ms under 77 ms. Recounting all six harness JSON files gives zero passes over THE SHARE: 99/98 main groups, sixteen answering-every-port groups per shape, and eight answering-later groups per shape. The seven main-arm misses are the disclosed backlog egress-hold rows; the 8x8/1if egress ledger accepts their figures. They are not silently counted as zero misses.

Docs applied, UNCLEAN only for F1 - `docs/reference/SUBMODULES.md:26`, `docs/design/MAILBOX_SPLIT.md:454`, `sw/firmware/ctrl/README.md:647`, `sw/firmware/ctrl/srp/README.md:76`, `:594`, `docs/diagrams/submodule_boundaries.*`, `PNG_MANIFEST.json`, `tb/verilator/milan_dp/README.md:1392`, and PR #992.

All active pin sites, both dependency permalinks and generated boundary artifacts move together. The old pin remains in historical measurements (`SPLIT_CONTROL_MEMORY.md:491` and `ci/image/exec-audit-receipt.json`). Callback/filter line ranges match the new dependency. Diagram check, diagram self-test, PNG and submodule-doc checks pass independently; the PNG was visually inspected. No new prohibited lane/reviewer labels or private identifiers were found in added source comments. Docs receipts explicitly record initial environment refusals, subsequent passing renderer and builder reruns, and four hosted-event steps not run locally. Those are not represented as executed hosted jobs. The current PR records acceptance of the mapping delta, superseding the packet handoff's earlier open-decision status.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | mrp_mad.c commit path; twin opportunity/length/observation paths; own-LeaveAll reproduction | R914-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| RTL | CLEAN | complete diff; adapter observers/build_mrpdu; image ledger and repeated mapping tables | R914-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| Robustness | CLEAN | all-input phase sweep; held leg; send refusal path; donor state tests; boundary probes | R914-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| Tests | UNCLEAN | focused reruns; self-test census/mutations; firmware/twin/harness receipts; F1 open | R914-1 applied, no clean coverage | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| Docs | UNCLEAN | pin sites, generated diagrams, interface links, PR claims and receipt index; F1 open | R914-1 applied, no clean coverage | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |

Limits and pending manager duties

- This review checks the issue's frozen protocol reading and repository tables/contracts. Complete licensed copies of IEEE 802.1Q-2022 and Milan v1.2 were not available in the checkout; no claim is made to have independently reopened those full publications. Public search did not provide authoritative current full text.
- Full parent, processor, timing, synthesis and builder banks were not rerun. Full source gate evidence is the author's packet. Only the focused commands and recounts named above were independently executed.
- Hosted/replica acceptance remains the manager's. This review does not treat a skipped context as an executed gate or assert exact-head hosted acceptance.
- Routed 8x8/1if base/head comparison must fit, meet #818's timing floor, and have LUT/FF and WNS/WHS totals added to the PR before merge. Accepted out-of-context deltas do not discharge that condition.
- The manager must validate the final current-dev candidate, with builder/native banks and receipts. Source base is `aa30d77f`; supplied live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`. Source-head evidence is not candidate evidence.
- Physical calibration is NOT RUN. Field skips and simulation are not hardware proof. Release qualification, merge authorization, completed independent reviews and post-merge containment remain separate obligations.
- F1 requires correction and re-review. No source fix, commit, push, GitHub write, hardware access or merge was performed.
- `checkout-integrity.log` verifies tracked blob bytes, executable modes and index entries against the exact head and five required dependency pins. The unused external gitlink is unchanged and uninitialized. No source restoration was needed.

Prior-public-finding reconciliation: after writing this independent verdict and ledger, the PR discussion and review submissions were read. The discussion contains only the two public review-start notices (7120222911 and 7120229842); there are no submitted reviews or prior public findings to resolve or retain. Issue #991 has no comments at the inspected snapshot. The earlier author handoff's open mapping decision is superseded by the assigned owner-delegated ruling and the current PR body, not treated as an unresolved prior review finding. No other reviewer's report was opened.

Reproduce with the reviewed checkout as argument: `python3 -B run_focused.py <checkout>`, `python3 -B probe_twin.py <checkout>`, `python3 -B run_checks.py <checkout>`, `python3 -B verify_checkout.py <checkout>`. `summarize_evidence.py` expects the immutable public author packet beneath `scratch/review-evidence/lwsrppin-r1`. Only MANIFEST.sha256-listed files and this report are publishable; `scratch/` is not.

R914-1 FINISHED
