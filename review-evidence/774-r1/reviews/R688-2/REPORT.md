[R688] NEGATIVE - exact head 01fc54756f1ffb0a3aa836681215e8321ee7e86c

# R688-2: external independent review of issue #774 / PR #778

The implementation and all three prior blocking/minor findings pass this review. One new MINOR remains: the public handoff claims six planted BDD faults, while the script and receipts show five faults plus one clean control. Under the assigned numerical-evidence rule, this is not wording-only RESIDUE. No RTL correction is requested.

Reviewed the whole PR, without inheriting a R688-1 verdict. Source base: `a032c6d6e3775f145349d5a495c1e1ad12294936`; reviewed tree: `7d8822f99d37284635fc34101123477e0c89846c`. History contains the original three commits followed by five round-2 commits, without a rebase. Reconstructed AGENTS/CONTRIBUTING, docs/README, public scope, requirements/interfaces, full diff/history, then executable evidence. An independent first-pass verdict and ledger were written before explicit prior-finding reconciliation. No other round-2 report was used.

Authorities: [issue #774](https://github.com/kebag-logic/milan-fpga/issues/774), [frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6379902807), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/778#issuecomment-6382693550), REQUIREMENTS.md, CONTRIBUTING.md sections 1/3/6, `protocol-processor/docs/guides/integrator.md:326-340`, `protocol-processor/docs/architecture/02_interfaces.md:277`, and their cited Milan Table 4.4 / IEEE 802.1Q 35.2.2.8.4 contract.

## Findings

### R688-2-F1: MINOR; Tests, Docs; overstated negative-control count

- **Artifact:** [issue comment 6385545886](https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6385545886), Validation, second bullet: "six planted faults against the unchanged step are all caught."
- **Authority/evidence:** AGENTS section 6 requires reproducible test evidence and accurate public documentation. Published `author-r2/scripts/round2/bdd_frame_mutants.py` defines six cases: one clean positive control and five mutations. Published `receipts/round2/bdd/frame_mutants.log` records five `[PASS mutant caught]` lines and one `[PASS clean]`. Independent reproduction agrees: [bdd-frame-mutants.log](bdd-frame-mutants.log), six checks passed. The PR body enumerates the five faults correctly. The handoff snapshot is retained in [public-snapshot.json](public-snapshot.json).
- **Impact:** REVIEW READY claims a sixth negative control that was not executed. This overstates measured coverage; it does not invalidate the five catches or establish an RTL defect.
- **Required outcome:** replace the sentence with: "Five planted faults against the unchanged step are caught, and the clean control passes: six checks total." No new mutation or source change is required.
- **Verification:** compare the corrected public handoff with the six case definitions and six result lines. A focused documentary re-review suffices if the source head remains unchanged. The assigned owner rule excludes numerical test-count claims from RESIDUE, so Tests and Docs remain unclean pending correction.

### R688-2-R1: RESIDUE; Docs; PR role placeholders

- **Artifact:** PR #778 body, "Linked Issue / roles"; [public-snapshot.json](public-snapshot.json).
- **Authority/evidence:** both reviewer lines still say `[R<n>] (to be assigned)`, although public review-start comments assign the roles. This is administrative wording, changing no measurement, figure, verdict, clause or privacy claim.
- **Impact:** readers must consult the comments to identify reviewers.
- **Exact fix:** `Internal cleared-context reviewer: [R687]` and `External cleared-context reviewer: [R688]`.
- **Verification:** compare those lines with the round-2 review-start comments. This residue does not dirty a lens.

### R687-1-S1 retained: SUGGESTION; Tests; distinguish AAF source widths

- **Artifact:** `hdl/milan/milan_datapath.sv:9057`; `tb/verilator/milan_dp/sim_crf_licence.cpp:1269-1277`.
- **Authority/evidence:** required shapes give all AAF talkers eight channels. They distinguish AAF from CRF but cannot distinguish an AAF slot's own value from talker 0's equal value. The implementation uses the correct `gmf` index. Frozen acceptance requires the all-source talker-0 mutation, which is caught on both shapes.
- **Impact:** optional coverage improvement for unequal per-talker configuration; no unmet frozen acceptance criterion.
- **Optional outcome:** configure one 8x8 AAF talker's TCTX channel count differently before declaration; grade its independently calculated TSpec.
- **Verification:** an AAF-only slot-0 substitution should then fail. No additional campaign was run for this optional suggestion.

## Prior public findings at this head

Read [R687-1](https://github.com/kebag-logic/milan-fpga/pull/778#issuecomment-6382684028) after the independent diff pass. Every named item is accounted for:

| Prior item | Disposition | Evidence |
|---|---|---|
| F1 BLOCKER, RTL/Tests | RESOLVED | `KL_crf_tx.sv:235` uses `CRF_HDR_C + 32'(CRF_DLEN_C)`: same value 28 and explicit 32-bit width. Feature and step files are byte-identical to base. Independent behave passes 406/406 scenarios and 1977/1977 steps, no skips. Original resolver probe gives FRAME_BYTES 60. Native replica includes successful bdd-conformance. Both wire-model receipts still report CRF 29. |
| F2 MINOR, Docs | RESOLVED | SRP-10 cites `Milan 4.3.3.2 Table 4.4` without a version token. Original matrix probe keeps `35.2.2.8.4`, `802.3`, `4.3.3.2`. Three module rows and regenerated README-test rows omit `1.2`; generator `--check` passes. |
| F3 MINOR, Tests | RESOLVED | Script digest matches `baec486a...`; reviewed non-installing class remains valid. New executable has the matching runtime pattern. Both build forms are registered. Whole-tree walks encounter the same base drift. Extended in-memory suite walks find no missing changed-script/new-executable entry; both affected forms retain exactly base's three source-list differences. See inventory-patterns.log. |
| R1 RESIDUE, Docs | RESOLVED | `ieee8021q.md:103` uses the requested exact wording: real frame geometry, one slot per source, each AAF channel count and CRF PDU shape. |
| S1 SUGGESTION, Tests | RETAINED, optional | Recorded above; does not dirty a lens. |

The [R688-1 void note](https://github.com/kebag-logic/milan-fpga/pull/778#issuecomment-6382962829) supplies no prior coverage or verdict.

## Applied lenses

- **[R688] PASS Conformance** - `KL_pp_shadow.sv:301,1284`, `KL_crf_tx.sv:223-248`, `milan_datapath.sv:6730,9046-9060,9407`, and published `legs/crflic-run.log` / `tspec8-run.log`: wrapper width and slot order match the pinned processor's `[16*s +: 16]` interface. AAF uses its own geometry; CRF derives 20 + 8 + 1 = 29 from the framer. No copied 29 literal or scratch-only replication remains. Wire-model declarations are 217/29 for 1x1 and eight 217s/29 for 8x8. Emitted-AVTPDU comparison passes in 1x1. The required talker-0 control fails on both shapes.
- **[R688] PASS RTL** - `milan_datapath.sv:1675-1694,6714-6743,7427,9053-9058,9246`; `KL_crf_tx.sv:227-248,458-490`; processor `protocol_processor_top.sv:303,2701`: the addition is combinational configuration wiring. No clock, reset, latch, state transition, handshake or backpressure path is introduced. Header/data indices match the derived 28-byte array and unchanged 60-byte padded frame. Vector widths agree. Published lint and synthesis support the inspection.
- **[R688] PASS Robustness** - `milan_datapath.sv:1675-1694,9053-9058`; `sim_crf_licence.cpp:733-756,1274-1281,1304-1328,1359-1364`; published crf_tx/crflic receipts: the no-CRF shape generates valid AAF indices; the existing guard excludes other source counts. Tests require each source to appear, accumulate incorrect TSpecs across declarations, and apply FirstValue's TSpec to packed values. Malformed MRP is counted. Staged oversized grant tests are explicitly excluded from the normal-format oracle. Existing refusal, disable, reset and backpressure behavior is unchanged. Five independently rerun BDD faults fail for their intended causes beside a passing clean control.
- **Tests applied; UNCLEAN only by R688-2-F1** - examined the entire harness diff, Makefile/default-run integration, mutation driver, test_sim_pool, BDD, inventory and gate receipts. Mutation catches require a built executable, failing verdict and named failure; a failed compilation alone cannot count. Default execution includes tspec8; its source-count boot check prevents silently testing the wrong shape. Executable checks pass; public count correction remains.
- **Docs applied; UNCLEAN only by R688-2-F1** - examined all changed Markdown, generated rows, source comments, PR and issue evidence. Firmware README's 167 matches native `firmware-verilator.14.log:329-330`, including its count mutation control. No new prohibited bench-lane/reviewer/comment identifier was found in added source comments. Harness phase labels are test phases. Role placeholders are separate residue.

## Validation and provenance

All 538 author receipt files match `published_sha256` in the [public archive](https://github.com/kebag-logic/milan-fpga/tree/4484c29cd1224098b5b0d4576cc5d8e4897b4836/review-evidence/774-r1). See [public-hashes.log](public-hashes.log) and [evidence-checks.log](evidence-checks.log). Selected raw receipts are copied unchanged under `published-receipts/`.

| Validation | Evidence head | Result and limit |
|---|---|---|
| Independent behave, original frame/matrix probes, matrix check | reviewed head | 406/406; FRAME_BYTES 60; proper clause tokens; generated files current |
| Independent BDD fault controls | reviewed head | Five faults caught plus clean control: six checks, zero failures |
| Independent inventory walks and in-memory suite audit | head and base | Same pre-existing drift; changed digest/runtime entries correct. Entire inventory is not claimed green |
| Native rtl-fast replica | reviewed head | All 11 recorded jobs successful, bdd-conformance included; action/setup substitutions explicit in receipts |
| crflic / tspec8 / crf_tx / pool self-test | `0d4b4620` | Published executions: 427/0; 61/0; 129/0; 17/17 |
| crflic-mutants | `0d4b4620` | 10/10: two clean controls plus eight mutations |
| Four-shard sweep | `0d4b4620` | 64/64 suites; independently summed 2,189,325 checks, zero failures; four tsn_fuzz field/freshness skips explicit |
| Lint | `0d4b4620`, native replica at head | PASS, 89 <= 89 |
| Yosys | `2a0085dd` | 60/60; tied-input and observer-purity checks pass |
| Docs bank | reviewed head | 44 recorded steps: 42 executed, zero failures, two explicit skips; separate no-git pair rc 0 |
| route-1x1 | `2a0085dd` | PASS against eleventh record: 15,831 slices (-4), WNS 0.281 ns, WHS 0.009 ns, route complete; +5-slice STOP not reached |
| ooc-1x1 / ooc-8x8 | `e70a99ba` | Prior author receipts PASS: LUT +19 / +45, FF +0 / +1. Round-2 arithmetic preserves value/width; other changes are documentation/inventory |

Verified carry: `0d4b4620..HEAD` changes only command-table.json and the firmware README; `2a0085dd..HEAD` changes only that README. Source executions above belong to the author. No manager source bank is claimed. Initial inventory-suite attempts stopped at setup/base drift; completed in-memory walks subsequently reached all targets. Their logs retain the distinction between an audit refusal and a successful test.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue scope; processor :303/:2701; wrapper :301/:1284; CRF :235/:248; g_pp_maxf :9053; wire receipts | R688-2 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| RTL | CLEAN | CRF array/framing :458-490; widths and no-CRF guard; source mapping :9053-9058; lint/synthesis receipts | R688-2 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| Robustness | CLEAN | Source guard :1675-1694; MRP decode/cumulative grading; refusal/disable cases; BDD faults | R688-2 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| Tests | UNCLEAN: R688-2-F1 | Harness, Makefile, mutation driver, BDD, inventory, sweep; handoff count versus script/log | R688-2, applied; not clean | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| Docs | UNCLEAN: R688-2-F1 | All changed Markdown; generated rows; firmware count; PR/issue handoff | R688-2, applied; not clean | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |

## Real limits and pending manager duties

- Full standards editions were not independently obtained. Clause/formula checks use the frozen task, repository authorities, pinned processor interface/admission implementation and builder budget. This is not independent certification against full standards texts.
- Hash consistency is verified. No detached signature was provided; the archive commit has no embedded Git signature. Signer authentication is not claimed.
- Full synthesis, builder, processor, timing and simulation banks were not rerun here. Their evidence is the author's published receipts. Physical calibration was NOT RUN; field skips and simulation are not hardware proof.
- Exact-head hosted snapshot: docs, elaborate and rtl-fast queued; rtl-full in progress. No hosted success or executed/skipped job coverage is inferred. The manager owns hosted/act acceptance and required contexts.
- Correct F1 publicly and obtain focused re-review. Carry R1 to the residue checklist. S1 remains optional.
- The manager must validate the current-dev candidate with builder/native banks at the merge turn and link receipts. Source validation does not replace that duty. Complete independent review, ensure no review is in flight, obtain merge authorization, then perform containment and Issue/Project completion.
- Inventory regeneration remains separate manager work for pre-existing drift.

[checkout-integrity.log](checkout-integrity.log) proves all 1,447 superproject entries and every populated required submodule's tracked bytes, modes and index match their recorded objects. All six gitlinks match; optional `external` remains uninitialized. No source fixes, commits, pushes, GitHub writes, hardware operations or forbidden banks were performed. Disposable copies are confined to `scratch/`, excluded from publication.

R688-2 FINISHED
