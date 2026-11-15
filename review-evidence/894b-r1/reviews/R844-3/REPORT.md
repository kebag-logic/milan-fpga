[R844] POSITIVE - exact head af2c4d7a4a1930aba712792a7facd8e9cb88e7c7

External independent delta review R844-3, issue #894 / PR #914. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR is open in the reviewed delta. Four wording residues are recorded below. This verdict is about the source head, not authorization to merge or validation of the current-dev candidate.

Tree: `63cae1575a884c869dd92698c8d4a9bb685f6aba`. I examined the PR source-base range `7398ec0aeea468d92ff642a03a06e291a0cd58d1..af2c4d7a4a1930aba712792a7facd8e9cb88e7c7`, concentrating on the 29 changed files since previously reviewed `98c0b62be911f5cff7a03ebfee7f837c23847d14`. Unaffected implementation retains its earlier coverage; changes to dependencies were examined here. An independent verdict and five-lens ledger were written before reading earlier reviewer reports. No current-round peer report, private author material or management checkout was read.

## Authority and scope

The reconstruction followed AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and public decisions, requirements/interfaces, then diff/history and executable evidence. REQUIREMENTS.md section 1, FR_NFR.md 3.4.1, MAILBOX_SPLIT.md and SPLIT_CONTROL_MEMORY.md section 13 supply the contracts.

The issue body's original every-source acceptance is refined for this follow-up by the [shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), [retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227), and binding [round-6 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049). The public author-r5 assignment records the sync to `234bc149` and remeasurement; round 6 requires the later sync, image identity, two restatements with controls, and final pass. The [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6895387328) supplies source execution evidence.

At 8x8/1if the trigger is a measured CPU-decided row over its bound or load over 0.75. Every-source rows remain reported debt to #872. Held-egress rows remain service-budget misses even when within the ruled ledger. Images beyond their entries must be reported, not silently restated or treated as an automatic STOP. No protocol bound was reinterpreted by this review.

## Results at this head

**Conformance: PASS.** `ctrl_loop.h:324`, `load_grade.py:288`, `edit_rows.py:48`, `record_classes.py:102`, `egress_ledger.py:56` and the public measurement receipts implement the scoped decisions.

- Both upstream merges are present: `647d5c4a` has parent `234bc149`; `5aadbc8c` has parent `4ae887a1`. The shape table remains keyed by interfaces, sources and sinks. The 1x1/1if block alone takes 950 us slice, 735 us build of one and 280 us SRP limit. The 8x8/1if block retains 1,475 / 1,795 / 1,475 us for slice / both builds / one build, with SRP limit 365 us and retry costs 165/25 us. No HDL, mailbox schema, SoC glue or donor gitlink changes occur in the PR source-base range.
- The ledger reads the scenario's 60 ms hold. Its rule is `60 + ceil_0.01((measured_ms - 60) * 1.05)`. Independent decimal arithmetic reproduces all seven figures: 63.40, 63.64, 63.93, 64.16, 64.41, 62.30 and 61.94 ms. The 5% applies to service behind the hold, not the hold itself.
- Section 13:2573-2583 records both the round-3 and merged-image measurements. All seven bare-merge BUDGET lines at `647d5c4a` equal the measured-image lines at `a15345f7` to the published microsecond resolution. This supports attribution to #902's merged code rather than the subsequent 8x8/1if changes. The ledger's ten-nanosecond measurements agree with the regrade table; the bare-merge proof does not claim that finer resolution.
- The ADP measurement of 12,210 cycles becomes 130 us under the 5%/5-us rule. `load_grade.OWN` supplies that floor for 8x8/1if; the pin's conservative 240 us remains and the donor column's inherited 125 becomes 130. The 8x8/2if tables are unchanged by this own-point restatement. The independent load check gives 0.711 at the pin and 0.673 in the second column, below the 0.75 flip ceiling.
- The same rule gives 635 us for the accepted SET_CONFIGURATION record at 60,027 cycles, 1,510 us for the largest command at 143,648, 145 us for the notice item at 13,572, and 55 us for the walk at 4,905. The record-class point selection distinguishes 8x8/1if from 1x1/1if. The published survey reports zero exceeded statements.

The published source measurement covers 114 groups and 1,717 measured instances. Worst CPU-decided rows are AECP 4.860 ms; ACMP/ADP/MAAP 7.231/6.014/6.255; SRP 10.474; MRPDU 4.114; first/last queued notice 2.812/26.636; largest-command row 2.547. These fit 20/30/90/49/20/130/238 ms respectively. Joins are 187.397-190.147 ms against 181-239. The 2,453,084 retry rounds have no stated-cost overrun; maximum SRP/build/retry slices are 142,809/138,906/92,744 cycles against 147,500. The transmit-aged control is caught in 8/8. One largest-command pass over THE SHARE remains explicitly reported under the existing scope, not counted as newly passing.

The current every-source receipt reports R4 19.82, R5 126.36, R6 118.28, first 17.83, last 325.90, R4L 192.81, ACMP 48.37, ADP 48.33, MAAP 49.03, tx 67.24 and txL 134.96 ms. The over-bound rows are not hidden by the measured acceptance result; they remain #872 debt under the ruling.

**RTL and architecture: PASS.** `sw/firmware/ctrl/loop/ctrl_loop.h:324`, `aecp_commands.c:100,183`, `aecp_face.c:115,166`, `aecp_maps.c:274,426`, and their callers/tests were examined. This lens covers firmware architecture here; there is no HDL delta.

The imported configuration optimization retains the bound/running owners, reads one GSI word to prove observation availability, and still refuses an unanswered observation. Ordinary stream reads initialize the brief flag false and retain the full read. The changed callback distinguishes a configuration-index move from its first override; stream publication follows the move, while settings still commit. Accepted configuration records stamp the pace and rejected ones do not. Map edits clear the reachable domain slots and initialize each inserted node before traversal; REMOVE bounds its second scan to the matched range, moves remaining rows in order and preserves occurrence accounting. The existing legality checks precede indexing. I inspected the added stale-state, echo, configuration, publication and pacing tests and their defect tables, including ordering and refusal paths. No new runtime ownership or crossing is introduced.

**Robustness: PASS.** `egress_ledger.py:143,180,316`, `record_classes.py:147,262`, and `aecp_configuration_mutants.py` / `aecp_map_mutants.py` provide the relevant boundary/failure evidence.

Independent ledger probes accept all seven rows at their limits and reject each row one bus cycle over, the original 100 ms fault, a new CPU miss, a run-level refusal and a missing results.json. The public measurement logs regrade successfully with conservative half-microsecond log rounding; the smallest remaining margin is 0.09350 ms. This is a regrade of held-egress evidence, not a fresh measurement of the other rows. The reader still rejects unmeasured/never-completed instances and wrong-group names. A new or larger miss is never waived just because its name was previously ledgered.

**Tests: PASS.** Independent executions are recorded in the packet:

| Check | Result |
|---|---|
| Ledger self-test | 35 controls in process and as processes; 13 mutants caught |
| Load check and self-test | PASS; 28/28 controls |
| Record classes | 13/13 controls |
| Shape check and self-test | PASS; 24/24 controls |
| Flip checks at 1x1/1if and 8x8/1if | Both exit 0; 8x8/1if explicitly reports its every-source debt |
| Independent ledger fixtures and real-log regrade | 13 expected outcomes; seven independent decimal derivations agree |
| Published acceptance-gate controls rerun at this head | All 21 pass, including original fault shapes and run refusal |
| Added-source comment scan over the full source-base range | Zero prohibited issue-comment/review-wording lines |
| Diff whitespace and final tracked-content integrity | PASS |

The broad source execution remains the author's [published archive](https://github.com/kebag-logic/milan-fpga/tree/d0318d2add19efec6d659b6c42201d143dea9658/review-evidence/894b-r1), not a manager source bank:

- All 98 extracted author-r5/r6 files match MANIFEST.json's published SHA-256. Round-5 and round-6 INDEX entries reconcile to their original digests or declared publication redactions: 44+6 and 39+7 respectively. The Git archive commit contains no embedded signature; this proves object/digest consistency, not a verified cryptographic signer.
- Full ELF and loadable-byte hash pairs match for all eight images from measured `a15345f7` through `5aadbc8c` to `af2c4d7a`. The six fixed images also match `4ae887a1`. These are audited published image receipts, not reviewer rebuilds.
- All 65 lane-gate return codes match their declared expectations, including the deliberately nonzero model reports.
- The workflow inventory contains 139 locally executed steps at rc 0 and 226 NOT RUN entries with reasons. These are local executions of workflow commands, not 139 hosted jobs or a hosted acceptance verdict.
- Campaign receipts record 716 control, 302 AECP and 345 SRP mutants caught, zero escaped; boundary, firmware/wire and both counter shapes pass.
- The four final sweep receipts total 65 suites and 2,713,040 checks, zero failures, timeouts or SKIPPED lines. The earlier failed sweep attempt remains recorded and is not counted as passing.
- plat_ledger records 7/7 controls and PASS at four points. Its mapped 8x8/1if platform is 56/56 RAMB36. The mapped-platform and stand-in image receipts have different ROM byte counts; they are separate builds, not contradictory image hashes.

**Docs: PASS with residue.** FR_NFR.md:393-397, SPLIT_CONTROL_MEMORY.md:2510-2596, the AECP/SRP/harness READMEs, public rulings, PR body and evidence indices were checked against code and receipts. The current ledger, own ADP record, shape table and debt treatment are documented. Historical paragraphs need clearer labels as listed below; current measurement and model results are publicly available and are not missing evidence.

## Prior public findings at this head

Prior reports were read only after the independent pass and ledger were written: [R844-1](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6885381555), [R843-1](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6885564795), [R843-2](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6888161058), and [R844-2](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6888161829).

| Prior ID | Severity / lenses | Disposition and cause-level evidence |
|---|---|---|
| R844-1-F1 | MAJOR; Conformance, Robustness, Tests | RESOLVED, retained clean. Numeric comparisons in egress_ledger.findings remain active under the newly ruled figures. The packet gate delegates to them. Independent one-cycle/100-ms probes and the 21 wrapper controls fail as required. |
| R844-1-R1 / R843-1-R1 | RESIDUE; Docs / Docs, RTL, Tests | RESOLVED, retained clean. Current added-source scan is empty; final comment replacements name the ledger ruling by subject/items. |
| R843-1-S1 | SUGGESTION; RTL, Robustness | Addressed within the disclosed guard scope. aecp.c still loads the table before declaring the charging unit; aecp.h:67 preserves the named refusal. aecp_arms.py and test_aecp.cpp preserve the generated-contract/assertion path. The narrower debug/wire remainder is S2 below. |
| R844-2-R1 | RESIDUE; Docs, RTL | RESOLVED. aecp.h:63 says “Most units”; the PR's disposition quotes the corrected wording. |
| R843-2-RES1 | RESIDUE; Docs | RESOLVED. Ledger documentation names its measurement and derivation; the mutant is “a ledger row waived by its name whatever its size.” |
| R843-2-RES2 | RESIDUE; Docs | RESOLVED by current PR correction: the assertion covers host arms compiling test_aecp.cpp, with debug/wire exclusions explicitly stated. |
| R843-2-RES3 / R844-2-R2 | RESIDUE; Docs | Addressed by the current PR's explicit corrigendum: counters-f5-98c0b62b.txt and 716a8ae7..98c0b62b. The immutable old packet is not silently rewritten; its stale sentence is superseded by that correction. |
| R843-2-S1 | SUGGESTION; Robustness, Tests | RESOLVED at its cause. run_refusals reads results.json; missing summary or a nonempty refusal list fails both the tracked ledger and packet gate. Independently reproduced. |
| R843-2-S2 | SUGGESTION; RTL, Robustness | RETAINED, optional. Debug and wire arms still intentionally use the tracked contract and do not measure retry costs. No new claim that they do is accepted. |
| R843-2-S3 | SUGGESTION; Docs | Addressed for the current packets. Every r5/r6 index digest is verified or reconciled through the publication-redaction manifest. No unexplained mismatch. |

No earlier blocking finding is deferred to another issue.

## Wording residues

**R844-3-R1 — RESIDUE — Docs — `tb/verilator/ctrl_service_budget/record_classes.py:96`.**

Authority/evidence: the point_name docstring calls 8x8/1if “reported,” while COMPLETE, held and the module's main contract correctly hold its formal legs at their own statements. Impact: stale explanatory wording only. Exact required fix: replace the parenthetical “#894's 8x8 follow-up, reported” with “#894's 8x8/1if shape.” Verification: docstring-only diff; preserve classification, completeness checks, statements and all results.

**R844-3-R2 — RESIDUE — Docs — `docs/design/MAILBOX_SPLIT.md:390`.**

Authority/evidence: the slice description uses “at one interface” as shorthand for the 1x1/1if row, although THE SHAPES explicitly distinguishes 8x8/1if. Impact: an overbroad prose qualifier; the authoritative shape table and implemented figures are correct. Exact required fix: replace “the slice rule's choice at one interface, 0.95 ms” with “the slice rule's choice at 1x1/1if, 0.95 ms.” Link THE SHAPES for the other one-interface shape. Verification: preserve all numerical figures and contracts; inspect only the qualifier/link change.

**R844-3-R3 — RESIDUE — Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:2547,2593`.**

Authority/evidence: the retained load paragraph and every-source list carry round-3 figures beside newly added current statements. The new own-ADP paragraph and current public model receipt already give the updated result. Impact: ambiguous historical attribution, not missing or changed measurement evidence. Exact required fix: start line 2547's bullet “The round-3 load record” and label the line-2593 block “Round-3 reported rows, owed to #872”; add a link to author-r6/receipts/model/rows-8x8-1if-af2c4d7a.txt for the current report. Keep the historical numbers unchanged. Verification: wording/link-only diff, no recomputation or changed figure, bound, verdict or normative claim.

**R844-3-R4 — RESIDUE — Docs — PR #914, “8x8/1if's own ADP record,” final survey bullet.**

Authority/evidence: the body says every statement is “within its measurement,” reversing the relation that the survey and adjoining text correctly establish. Impact: reversed wording only. Exact required fix: “The survey over every leg finds every measurement within its statement by the rule.” Verification: compare to author-r6/receipts/model/survey-compare-ordinary-af2c4d7a.txt, which reports zero exceeded statements. No numerical value, test or verdict changes.

These residues do not leave a lens unclean. The retained optional S2 remains optional.

## Reviewer-owned completion ledger

Every row covers the changed artifacts and named prior causes at this head, with unaffected earlier coverage carried only where dependencies remain unchanged.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #894 round-6 ruling; FR_NFR 3.4.1; ctrl_loop.h:324; load_grade.py:288; egress_ledger.py:56; record_classes.py:102; measurement and image receipts | R844-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| RTL | CLEAN | Full/delta path inventories; ctrl_loop.h:324; aecp_commands.c:100,183; aecp_face.c:115,166; aecp_maps.c:274,426; test_aecp.cpp; gitlink and image identity receipts | R844-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| Robustness | CLEAN | egress_ledger.py:143,180,316; record_classes.py:147,262; configuration/map mutation tables; ledger-probes.log; packet-gate-controls.log | R844-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| Tests | CLEAN | Six focused-check logs; independent decimal/boundary probes; acceptance-wrapper controls; published final gate/campaign/sweep receipts; evidence-verification.log | R844-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| Docs | CLEAN | SPLIT_CONTROL_MEMORY section 13; FR_NFR.md:393; MAILBOX_SPLIT.md:390; firmware/harness READMEs; public scope, PR disposition and r5/r6 indices; R1-R4 wording residue | R844-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |

## Limits and pending manager duties

This review did not rerun CPU measurement, image builders, full parent/processor banks, synthesis banks, hosted jobs or container workflows. Broad execution claims rest on the author's published receipts; independent execution was limited to the focused checks, falsification probes, log regrade, archive comparisons and integrity checks listed above. The archive does not supply every raw trace behind every measurement. No manager source bank at this head exists or is inferred. Physical calibration is NOT RUN; field skips and CPU simulation are not hardware proof.

Known pre-existing or ruled exclusions remain: the 8x8/1if Mailbox.ARoundFillsWhatItsPassHasLeft test, inherited 1x1 cost/history concerns, optional two-interface debt, valid-destinations belonging to #895, and every-source debt to #872. They are not silently certified by this delta.

The manager must publish the report/manifested receipts, carry R1-R4 to the residue checklist, and finish the other independent review. Synchronization onto #902's later comments/docs head `41ca9f87` remains known work, not a new finding. When composing #901, preserve 8x8/1if's own queued-notice bound of 130 ms by shape; an interface-only 140 ms must not overwrite it.

At the merge turn, build and validate the actual current-dev candidate with the builder/native banks and required hosted/local acceptance, and publish those receipts separately. Source base `7398ec0aeea468d92ff642a03a06e291a0cd58d1`, supplied live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`, and this source head are distinct. Renew affected lens coverage after changes, wait for every review in flight, and complete containment and issue/project closure after an authorized merge.

No source fix, commit, push, GitHub write, author contact or sub-agent was used. integrity.log proves all 1,630 superproject tree/index entries, 1,624 raw blobs and their modes, plus the five required initialized submodules and gitlinks. No hidden/sparse flags or tracked changes remain; external stays uninitialized at its original gitlink. REPRO.md explains receipt provenance and portable commands. Only REPORT.md and files listed in MANIFEST.sha256 are publishable; scratch is excluded.

R844-3 FINISHED
