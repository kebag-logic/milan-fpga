[R557] NEGATIVE - exact head ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3

Two MINOR findings remain: a deleted ACMP port obligation is missing from the replacement documentation, and the comment gate accepts forbidden prose inside an SPDX-prefixed block. Both are new in this follow-up. The seven verdict-bearing findings from R556-1 and R557-1 are resolved under their original severities. One previously classified wording residue remains in the closed PR #1 body.

The reviewed tree is `d8c4f1244d691e84b40a34cb0028b06d068613f3`. The base is `ae982af85ec97286bd35b39403926d8f0eaec81d`. Its tree equals the formerly reviewed `b9b9c20` tree. The [two-commit history](receipts/review-history.txt) contains the gate/RV32 changes in `086e5d37c19fbb6f4a628c376ce8f9f20e51df14`, followed by comment reduction in the exact head.

The [review start](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075090087), [issue](https://github.com/kebag-logic/milan-fpga/issues/697), [standalone assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112), [follow-up decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248), and [dual-target decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336) define this scope. Consumer pins, platform builds and firmware-image identity remain a later change. The separate Linux development branch was neither reviewed nor touched.

I reconstructed the contribution rules, README and quality documents, public acceptance and decisions, requirement and interface authorities, diff/history, then published executable evidence. There is no repository AGENTS.md. The session instruction was applied. The [independent verdict and ledger](receipts/independent-verdict.md) were written before reading either prior review report. The final PR #16 snapshot contained two start notices, no submitted reviews and no inline findings. The carried findings below come from PR #1, as required by the follow-up decision.

**R557-2-F1 | MINOR | Conformance, Robustness, Docs | Open**

Artifacts: [PORTING.md:89](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/PORTING.md#L89), [include/acmp.h:317](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/include/acmp.h#L317), and the [deleted-contract receipt](receipts/deleted-contract.txt).

The former header documented both meanings of the environment SRP callback: a stream starts reservation and packet listening; a null stream stops and clears it. Comment reduction deletes that explanation. PORTING now lists “SRP requests” and describes incoming reservation feedback, but neither PORTING nor ARCHITECTURE states the null-stream stop contract.

This remains executable behavior. [srp_stop at acmp.c:651](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/src/acmp.c#L651) clears the stream and calls the port with NULL. The successful-response path passes a stream at [acmp.c:906](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/src/acmp.c#L906). The existing [A13 test](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/tests/test_acmp.cpp#L664) and its null-aware fake confirm the stop operation. They pass in this review.

Authority: item B of the [follow-up decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) requires integrator contract material to move into PORTING or ARCHITECTURE before deletion. Impact: an implementer cannot derive this sentinel meaning from the replacement guide. Treating every callback argument as a stream can cause a null dereference; ignoring null can leave listening active. No production regression is alleged.

Required outcome: restore the obligation in PORTING, linked to the callback. For example: “The ACMP `srp` callback receives a stream to start reservation and packet listening. A null stream means stop listening and clear the stream parameters.” Audit the remaining deleted callback obligations for the same loss. Keep source behavior unchanged.

Verification: compare the deleted header contract against the replacement guide. Keep the existing reservation-start, timeout-stop and unregister-stop tests passing. This is an integration obligation, so it is not wording-only RESIDUE.

**R557-2-F2 | MINOR | Conformance, Tests, Docs | Open**

Artifact: [scripts/check_comments.py:24](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/scripts/check_comments.py#L24). Authority: the [follow-up decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) permits only SPDX lines, requirement tags and short standard references. The [coding standard](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/CODING_STANDARD.md#L3) and [verification table](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/VERIFICATION.md#L25) claim enforcement.

The checker accepts the entire comment when its stripped body starts with `SPDX-`. This planted source comment passes:

```c
/* SPDX-License-Identifier: MIT
This is forbidden integrator narrative.
*/
```

The [portable probe](scripts/probe_comments.py) appends it to a disposable copy of `src/adp.c`. The [receipt](receipts/comment-controls.json) records gate rc 0 and compilation rc 0 with `-std=c11 -Wall -Wextra -Werror`. Its object hash equals the baseline. An ordinary prose-comment control is correctly refused with rc 1. A spliced SPDX line also bypasses the scanner; that supplementary compile disables the multiline-comment warning and is not needed to establish the finding.

Impact: the mandatory gate accepts prohibited narrative while reporting that all code files pass. The current shipped comments meet the intended reduction; the defect is in the claimed refusal gate.

Required outcome: validate every comment line, including the remainder of a block that begins with SPDX. Account for supported line splicing. Add a real-source negative control for an SPDX line followed by prose, alongside valid licence and tracing controls.

Verification: the demonstrated block must compile but make the comment gate return nonzero. The unplanted head and legitimate SPDX/tracing controls must pass. This requires a code/gate correction and is not RESIDUE.

**Carried findings at this exact head**

Sources: [R556-1](https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074692175), [R557-1](https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074712341), and the [manager's disposition](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074721212). Original severities are retained below. None is worsened.

| Prior ID | Original severity | Disposition | Evidence and verification |
|---|---|---|---|
| R556-1-F1 | MINOR | Resolved | All fourteen export-introduced weak needles and the inherited exceptions now have specific messages. [Needle controls](receipts/local/needle_audit.log) refuse six empty/generic entries. [Independent audit](receipts/mutation-audit.json) verifies all 329 required assertion matches across 311 plants. |
| R556-1-F2 | MINOR | Resolved | Compiler dependencies and built-object imports replace text matching. [Compiling controls](receipts/local/boundary.log) refuse outside includes, digraphs, trigraphs, splices, macro includes, direct/macro/pointer heap use and a header-free OS call with both compilers. Two allowed controls pass. |
| R556-1-F3 | MINOR | Resolved | Requirement records split the standards. The generated matrix renders each part's own link. Both requirement documents were inspected and the [regeneration check](receipts/local/traceability.log) passes. |
| R557-1-F1 | MAJOR | Resolved | XML is deleted before each execution; registration, counts, uniqueness and completed statuses are checked. [Controls](receipts/local/mutation-controls.log) refuse stale, partial, truncated, skipped, erroneous and mismatched reports. A genuine catch followed by early exit in the same directory escapes and removes both old reports. Fresh and reused full campaigns catch 311 each. |
| R557-1-F2 | MINOR | Resolved | Same preprocessor/symbol correction as R556-1-F2. The [boundary receipt](receipts/local/boundary.log) includes the required compiling digraph refusal and pass controls. |
| R557-1-F3 | MINOR | Resolved | [Controls](receipts/local/registration_selftest.log) compile and execute indented, multiline and wrapper declarations. Unknown IDs and missing plants fail; unsupported wrappers produce a registration mismatch. [Inventory](receipts/local/test_inventory.log) reconciles 108 declarations with 369 instances in seven binaries. |
| R557-1-F4 | MINOR | Resolved under owner decision | ADP-01, PORTING and DEV-08 explicitly preserve all three malformed-input behaviors and assign validation to the caller. Four hosted controls and the RV32 equivalents pass. The correction remains [issue 3](https://github.com/kebag-logic/tsn-c-stack/issues/3), not an unapproved change here. |
| R556-1-R1 | RESIDUE | Resolved | COVERAGE links the reader, ratchet and relocated no-callback contract. |
| R556-1-R2 | RESIDUE | Resolved | The edition names in REQUIREMENTS are links. |
| R556-1-R3 | RESIDUE | Retained | The closed PR #1 still says hosted execution awaits publication. [Current excerpt](receipts/pr1-body-residue.md). PR #16 correctly identifies the historical runs. Exact fix below. |
| R556-1-R4 | RESIDUE | Resolved | IMPORT names all seven added cases and separates the original validation changes from this follow-up. |
| R556-1-S1 | SUGGESTION | Resolved | Both workflow actions use commit pins. |
| R556-1-S2 | SUGGESTION | Resolved | The 26-pair retained commit map is in IMPORT and explains the squash. |
| R556-1-S3 | SUGGESTION | Resolved | The ratchet has the generated header and unchanged measurement rows. [Coverage](receipts/local/coverage.log) passes. |
| R556-1-S4 | SUGGESTION | Resolved as a published confirmation; independent text corroboration limited | REQUIREMENTS' Clause checks section explicitly records checking both Milan clauses and distinguishes standard timeout values from local timing rules. Full v1.2 text was not independently available in this review. |

The referenced repository documents are [requirements and clause checks](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/REQUIREMENTS.md), [requirement records](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/requirements.json), [traceability](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/TRACEABILITY.md), [deviations](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/DEVIATIONS.md), [import record](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/IMPORT.md), [coverage register](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/docs/COVERAGE.md), [ratchet](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/tests/coverage.ratchet), and [workflow](https://github.com/kebag-logic/tsn-c-stack/blob/ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3/.github/workflows/quality.yml).

**R556-1-R3 | RESIDUE | Docs | Retained**

Artifact: [PR #1 body excerpt](receipts/pr1-body-residue.md). Authority: the original residue and item 7 of the manager's disposition. Impact: a stale historical publication sentence. Required exact replacement: “Hosted runs [37885778682](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778682) (pull_request) and [37885778700](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778700) (push) pass all 16 gates at `b9b9c20`.” Verification: read the updated body and confirm the stale sentence is gone. This retains its original RESIDUE classification and affects neither verdict nor lens cleanliness.

**Executed evidence and acceptance judgments**

| Area | Independent result |
|---|---|
| Linux | Seven binaries pass with GCC coverage and Clang address/undefined-behavior instrumentation. Each executes 369 instances. Leak detection and halt-on-error are enabled. [Gates](receipts/local/gates.json), [GCC tests](receipts/local/gcc-test.log), [sanitizer tests](receipts/local/clang-sanitizers-test.log). |
| RV32 | Debug and Release compile every core with RV32I, ILP32, freestanding C11, intrinsic/local headers and no default include search. Both whole-archive final links have zero undefined symbols; both execute ADP, ACMP and MAAP smoke checks. Examined startup, stack/BSS layout, memory subset, arithmetic-helper allowlist and completion path. [Results](receipts/local/rv32-results.json), [audit log](receipts/local/baremetal.log). This is simulator evidence. |
| Dual-target refusal | Both jobs run on push and PR events. Neither validation command is optional or marked continue-on-error. Either nonzero command fails its job and the workflow. Server-side merge protection settings were not inferred from YAML. |
| Comment-only production change | Commit A changes none of the seven production files. Across B, all 23 code files preserve non-comment tokens. All 311 mutated programs preserve tokens and killer mappings. All 22 core objects match byte-for-byte using the four CI configuration compile databases, stable paths and appended `-g0 -frandom-seed=0`. [Commands/hashes](receipts/comment-comparison/results.json), [script](scripts/compare_comments.py). F1/F2 prevent acceptance of the documentation/enforcement parts. |
| Before/after tests | Rebuilt the pre-reduction commit with both hosted and both RV32 configurations. All 369 completed test names/statuses match before and after for each hosted configuration. Both earlier RV32 images pass. [Comparison](receipts/supplement/results.json), [earlier RV32 results](receipts/supplement/before-rv32-results.json). |
| Mutation | The first fresh run, a second fresh directory, and reuse of that second directory each catch 311 plants, with zero escapes/errors. [First](receipts/local/mutation-results.json), [second fresh](receipts/supplement/mutation-repeat-results.json), [reused](receipts/supplement/mutation-reused-results.json). [Independent XML audit](receipts/mutation-audit.json) verifies all 329 required matches in the first and reused runs. |
| Refusal controls | [Reports](receipts/local/mutation-controls.log), [boundary](receipts/local/boundary.log), [registration](receipts/local/registration_selftest.log), [needles](receipts/local/needle_audit.log), [coverage](receipts/local/coverage_selftest.log), and [licence](receipts/local/check_license.log) controls pass. F2 supplies an additional failed enforcement control. |
| Coverage | Adjusted totals remain 1164/1164 lines and 583/583 branches. Raw ADP: 203/205 and 93/100; ACMP: 742/742 and 348/348; MAAP: 209/209 and 140/140; wire: 10/10 and 2/2. The same five ADP rows exclude two statements and seven arcs. Tests, example glue and debug assertion instructions are outside this denominator. [Receipt](receipts/local/coverage.log). |
| Analysis/privacy | Static analysis passes with the listed suppressions, including the new RV32 callback-related suppression. The history/current-tree privacy gate passes with the documented exact-owner-squash metadata exception; content remains scanned. [Analysis](receipts/local/static-analysis.log), [privacy](receipts/local/check_privacy.log). The export itself was not rerun. |
| Docs | Checked README, contribution/security/change records and every quality document. Persona entry points and scope limits remain. Generated test/traceability documents are current. All 392 checked local path/line links resolve. Three diagrams render; module and README flowcharts were viewed in browser rendering, and the sequence diagram was inspected. [Links](receipts/document-links.json), [graphs](receipts/local/render_graphs.log). F1 loses a contract; F2 contradicts an enforcement claim. |

Local work used foreground supervisors with bounded concurrent workers. Independent builds and campaigns overlapped, with at most sixteen worker jobs and no heavy FPGA build. Disposable copies, binaries and original logs remain under scratch. The [replay guide](REPLAY.md) and [versions](receipts/versions.json) describe this packet.

**Hosted evidence**

Both [push run 37889963458](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37889963458) and [PR run 37889967433](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37889967433) concluded success. Both quality and bare-metal checks are green in [gh pr checks](receipts/hosted-checks.json). Validation and upload steps executed; no recorded step was skipped. Downloaded artifacts contain twenty Linux gates with rc 0, 311 caught plants, and two successful RV32 configurations with zero unresolved final symbols. [Job/step and artifact audit](receipts/hosted/executed-evidence.json).

The [checkout logs](receipts/hosted/checkout-commits.json) distinguish actual revisions. Both push jobs and PR quality checked out the exact source head. PR bare-metal used synthetic merge `96db9aaead068c2f4c279d2540e8586a2c4e4a26`; its [tree](receipts/hosted/pr-merge-tree.json) equals the reviewed tree, with the stated base/head as parents. The push therefore provides exact-head execution for both targets. The synthetic PR merge is not the manager's later current-dev candidate. Hosted acceptance remains the manager's responsibility.

The [pinned original author packet](https://github.com/kebag-logic/milan-fpga/tree/2ae0b85299a979413a5ba4b7fe3e3de175967a19/review-evidence/697-r1) was read and all eight published hashes verified. It describes `b9b9c20`, not this head. The [current author declaration](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6075070051) and [PR #16](https://github.com/kebag-logic/tsn-c-stack/pull/16) publish follow-up source results, corroborated by current hosted artifacts and this review's execution. Manager comments record scope, dispositions and review starts. No manager source bank ran at this head; none is claimed or inferred.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F2 | Frozen decisions; requirements/standard links; ADP deferral; production/mutant tokens; object identity; deleted port obligation; comment refusal control | R557-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| RTL | CLEAN | No HDL in changed inventory; three C state machines and four public headers; unchanged production behavior; RV32 startup/link/runtime; imports/final symbols; both smoke configurations | R557-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| Robustness | UNCLEAN — F1 | Port ownership/serialization; refused callbacks; malformed input; bounds, wrap and backpressure tests; dependency/heap/OS and report controls; lost null-stream obligation | R557-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| Tests | UNCLEAN — F2 | Seven binaries, 369 instances; 311 plants, 329 matches; freshness controls; registration; coverage; sanitizer/static results; local/hosted dual-target checks; comment bypass | R557-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| Docs | UNCLEAN — F1, F2 | All quality documents; removed header contracts; generated records and links; three diagrams; PR/public claims; prior-findings reconciliation | R557-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |

All five lenses were applied independently. RTL CLEAN is limited to this portable implementation and its hardware-facing interface boundary; it claims no FPGA bank execution. The carried residue leaves no lens unclean. The two open MINOR findings require the NEGATIVE verdict.

This review does not recertify every clause. The [IEEE edition page](https://standards.ieee.org/ieee/1722.1/6670/) supplies metadata, not full text. The [Milan page](https://avnu.org/resource/milan-specification/) offers v1.3 through a form; cited v1.2 text was not independently obtained. The [1722 working-group page](https://sagroups.ieee.org/1722/) returned an access error. Later amendments/corrigenda were not audited. The published S4 confirmation is distinguished from independent textual verification.

The manager must resolve the open findings, carry the exact residue fix, obtain both independent positive reviews, and own hosted/replica acceptance. At merge, the manager validates the final current-dev candidate with builder/native banks and publishes receipts. This source review uses base `ae982af85ec97286bd35b39403926d8f0eaec81d`; stated live dev is `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. This review supplies no consumer integration or byte-identical firmware-image result. Physical calibration is NOT RUN. Field skips are not hardware proof. Repository publication remains a separate owner action.

No source fixes, commits, pushes, GitHub writes, author contact, other-checkout edits, hardware operations or prohibited banks occurred. Probes used disposable copies. [Final checkout verification](receipts/checkout-final.json) checks all 64 tracked blobs, modes and index entries against the exact head. Base and head have zero gitlinks; no required submodule pin changed. Publish REPORT.md and only files in [MANIFEST.sha256](MANIFEST.sha256). Scratch is excluded.

R557-2 FINISHED
