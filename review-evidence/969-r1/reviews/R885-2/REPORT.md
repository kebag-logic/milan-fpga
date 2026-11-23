[R885] NEGATIVE - exact head e816c74da53a5822f2ddc1661e5ffae297f1b3aa

Round R885-2, internal independent delta review of issue #969 / PR #971. All five lenses applied. The prior functional findings are resolved under the public #977 ruling. Four new MINOR findings remain: incomplete share-grading data can produce a standalone false PASS; two documentation claims contradict the published measurements; and the advertised grader self-test leaves three guards untested. One RESIDUE item contains two exact wording corrections. No new firmware functional failure was found.

This is a source review verdict, not merge authorization or validation of a current-dev merge candidate.

## Scope and provenance

Reviewed head: e816c74da53a5822f2ddc1661e5ffae297f1b3aa; tree: e2b9b5f88b2c9ffb5aff42996c34150c2afda190.

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/969), public scope decisions, linked requirements and interfaces, then the dd163e41..e816c74d change and f863258d..e816c74d delta. Prior public findings were consulted after the independent diff pass. No other current-round reviewer report was consulted.

Authorities: Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4 and Tables 5.9/5.10; IEEE 802.1Q-2018 10.7.7/10.7.8, Tables 10-3/10-4 and 35.2.6; REQUIREMENTS.md section 1; FR_NFR.md 3.4.1; the SRP adapter and pinned library integration/filter contracts. The filter remains non-reentrant; counting occurs before receive outside callbacks.

The [STOP](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7083505751), [option-1 ruling](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7083542634), and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7086009278) govern the cost disposition. The registration cost and the reference bound group's own share overrun belong to #977. This review does not reopen them as #969 defects or treat them as passing their original budgets.

Verified 173 author receipt blobs against published_sha256 in the [packet at 1cd9d3fd](https://github.com/kebag-logic/milan-fpga/tree/1cd9d3fd3e46aaeeff6650f1bc60cce139645f0e/review-evidence/969-r1), with zero mismatches. The Git commit has no signature header: this verifies manifest/content integrity at the supplied public commit, not a cryptographic signer. See receipts/evidence-verification.txt.

Production firmware C/H inputs are unchanged since f02d44cd. The final commit after 5dba2089 changes only the standalone grader's missing-JSON check. Earlier receipts were assessed against their actual input changes, not represented as newly executed source-head banks. See receipts/public-receipt-audit.txt.

## Prior findings: explicit disposition

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R885-1-F3 = R886-1-F1, stale count; all five lenses | RESOLVED | srp_mbx.c:290, :489, :951, :968, :1340 account for registration end, a new kept entry, a counted MT entry, binding change/returned block, and reset zeroing. Both reviewers' original reset/reclaim probes pass at both shapes and both interface counts. At f863258d they fail while fresh/flood/unbind-rebind controls pass. All five added trigger plants are caught at all three campaign points. |
| R885-1-F4 = R886-1-F2, absent 8x8 early campaign; Tests, Docs | RESOLVED | test_ctrl_firmware.py:232 includes srp_early_mutants.PREFIX and results identify their shape. Independently reran all 16 early plants at 1x1/1if, 1x1/2if and 8x8/1if: 48 caught, zero escaped. Published shard 3 also contains exactly 16 at each point. The PR corrects its earlier claim. |
| R885-1-F2 = R886-1-F3, memory figures; Docs | RESOLVED | All eight locations named in the prior reports match the ledger: 63.5/58.5 entries; 64.0/63.5/59.0 planted values; 7.5/2.5 tile debts and 30,720/10,240 B. Platform README and ledger docstring agree. Current ROM figures include the extra 152 B. F2 below is a separate new count discrepancy. |
| R885-1-F1, unexecuted changed CPU paths; RTL, Robustness, Tests, Docs | RESOLVED under the ruling | kept_window.py:89 exercises kept Advertises, reclamation/recount and refusals, LeaveAll response builds, reset and Failed registrations; :71 supplies the bound reference on the same image. Both product points have measured receipts, explicit OWED #977 lines, unchanged units/rows, and the comparison/build/share outcomes below. New F1/F4 concern grader robustness and coverage, not an observed source-run violation of the ruling. |

## Findings

### R885-2-F1 - MINOR - Robustness, Tests, Docs - incomplete share results are accepted as a clean grade

**Artifacts:** tb/verilator/ctrl_service_budget/kept_grade.py:123, :227, :230, :232; the condition claimed in its README.md:780; receipts/grader-probes/.

**Authority/evidence:** the ruling requires no srp-kept work pass over THE SHARE; a missing graded result must be a finding. The final-head fix rejects an absent JSON file, but accepts either an empty JSON object or an object containing group=srp-kept and an empty passes object. over_share substitutes empty containers for missing grading fields; main checks only whether the parsed result is None.

The independent synthetic CLI probe holds the logs constant, including a 250,000-cycle work pass at 100 MHz, above the 200,000-cycle share. A complete grade.pass_share result fails correctly, and deleting the JSON file fails correctly. Either incomplete object produces exit 0 and “kept_grade: PASS (0 finding(s)...)”. These are incomplete-result probes, not measured firmware overruns. Inputs and raw stdout/stderr/RCs are retained under complete-over-share, missing-json, empty-json and missing-share.

The reader also mishandles a valid result shape: grade.pass_share includes idle-overrun entries with idle_run instead of start_sys. Passing such a result to over_share raises KeyError('start_sys'), instead of extracting work passes. See the idle-only case in receipts/grader-probes/SUMMARY.txt.

**Impact:** the standalone gate can claim the share condition without a share grade, or crash on a result its existing grader legitimately emits. The integrated run with complete results is not shown to falsely pass by these probes.

**Required outcome:** require usable grading evidence for both groups before clearing the condition, or derive it from the parsed logs. Distinguish idle entries from work-pass entries. Missing/incomplete evidence must produce a named finding, not an empty overrun set.

**Verification:** scripts/probe_kept_grade.py must retain the clean, overrun and absent-file control outcomes; both incomplete-result cases must fail by name, and the valid idle-only case must not crash. Add regression controls for these cases.

### R885-2-F2 - MINOR - Docs - the hot-function count contradicts its receipt

**Artifacts:** docs/design/SPLIT_CONTROL_MEMORY.md:693; PR #971, Known limitations / Block RAM; published author-r2/receipts/budget/hot-section-f02d44cd.txt, reproduced in receipts/public-receipt-audit.txt.

**Authority/evidence:** the document and PR say 152 hot functions *after* reset_interface each move by 16 B. At both points the receipt says 152 functions differ in **offset or size**, including reset_interface as the first: its offset is unchanged, and its size grows 16 B. Under that census, only 151 other functions shift. The receipt's closing prose repeats the incompatible 152-after count.

**Impact:** the documented numerical account of the measured hot-section change is inconsistent. The 16 B growth itself is supported; no firmware-size or timing regression is alleged.

**Required outcome:** reconcile the inclusive changed-function count with the strictly shifted-function count. If the receipt's census is correct, state 152 changed in offset or size, comprising the resized reset function and 151 shifted functions. Otherwise correct the receipt from the symbol comparison. Preserve the supported 16 B measurement.

**Verification:** document, PR and receipt must agree on the counted population at both points. This is MINOR rather than RESIDUE because it changes a numerical measurement claim.

### R885-2-F3 - MINOR - Docs - the described LeaveAll frame is not the frame measured carrying the kept values

**Artifacts:** tb/verilator/ctrl_service_budget/kept_window.py:18; its README.md:771; published author-r2/receipts/budget/leaveall-build-with-the-kept.txt.

**Authority/evidence:** the new text says the build sending LeaveAll carries the kept attributes. The decoded receipt distinguishes two MRPDUs. At 1x1/1if, the 14.213 s LeaveAll frame is 127 B; the 14.404 s next frame carries the two kept Advertises. At 8x8/1if, the 14.253 s LeaveAll frame is 127 B; the 14.443 s next frame carries the nine kept Advertises. The receipt correctly identifies that subsequent response as the observed attributes answering with In.

**Impact:** the documentation attributes the changed encoding work to the wrong build/frame. The scenario waits long enough to exercise both and its build-cost receipt covers the later one; no missing execution is alleged.

**Required outcome:** describe the subsequent MRPDU answering LeaveAll with In for the kept Talkers, and identify that build as the changed encoding path. Keep the separate LeaveAll-owner/deadline check explicit.

**Verification:** compare corrected descriptions with both decoded sequences and the cost receipt. This changes a behavior/evidence claim, so it is not wording-only RESIDUE.

### R885-2-F4 - MINOR - Tests, Docs - the advertised self-test does not plant every held-condition breach

**Artifacts:** tb/verilator/ctrl_service_budget/README.md:783; kept_grade.py:168; receipts/selftest-coverage-probes.txt.

**Authority/evidence:** “--selftest plants each breach” follows the listed paired-group, record, share and build conditions. Its five checks exercise record limits/comparison, a missing record and supplied share overruns. They do not exercise Disposition's group-pair requirement, the standalone missing-result guard, or a build pass. Three independent in-memory plants respectively remove the build-over-cost finding, missing-JSON finding, and paired-group requirement. Every plant escapes with all five self-tests passing.

**Impact:** the claimed regression coverage cannot detect removal of three conditions authorizing the #977 disposition. The unmutated build-over-cost and single-group controls pass in this review's independent probes; those guards currently work.

**Required outcome:** add negative controls that fail for each of the three removed guards, including the standalone path, and cover F1's incomplete-result cases. Make the coverage description match the executed coverage.

**Verification:** scripts/probe_selftest_coverage.py must show each corresponding defect caught; the repository self-test must remain green without the plants.

### R885-2-R1 - RESIDUE - Docs - two source-comment corrections

**Artifacts and exact fixes:**

- kept_grade.py:48: replace “#969's STOP of round 2, ruled 2026-11-22, option 1” with “#969, ruling of 2026-11-22, option 1”. This new source comment contains a review-round label forbidden by the owner's comment rule.
- kept_window.py:30: replace “kept_grade.disposed” with “kept_grade.Disposition”. The helper is the class at kept_grade.py:129; no disposed symbol exists.

**Authority/evidence:** owner source-comment rule and the class declaration. **Impact:** wording/navigation only; no measurement, behavior, verdict, test or privacy change. **Required outcome:** the exact substitutions above. **Verification:** inspect the comments and confirm executable behavior is unchanged. This item does not make a lens unclean.

## Execution and evidence

Focused campaigns and arms ran concurrently under one foreground supervisor, with at most 16 compiler jobs. No full parent, processor, builder or synthesis bank was run. No hardware, container, host CI orchestrator, shared installation, source fix, commit, push or GitHub write was performed.

| Check | Result and receipt |
|---|---|
| Original internal/external probes plus refreshed-at-bound reset, LeaveAll expiry and other-interface reset | At head: 10/10 on each one-interface shape; 11/11 on each two-interface shape. At f863258d: both original reset/reclaim pairs and the added expiry probe fail at all four arms; remaining applicable controls pass. receipts/arms/PROBES-SUMMARY.txt and individual logs/RCs. The other-interface-only test is excluded at one interface. |
| Full SRP adapter suite | 102, 103, 102, 103 tests pass, at 1x1 and 8x8 with one and two interfaces. receipts/arms/head-full-*.log. |
| Platform sink composition at both product shapes | 14/14 each, including saved-binding restore and bind-while-bound with REGISTERING / REGISTERING_FAILED. receipts/checks/platsinks-*.log. |
| Early campaigns | 16/16 at each of 1x1/1if, 1x1/2if and 8x8/1if; all five new count-trigger plants caught, including reset zeroing. receipts/early-*.log and raw per-plant receipts/campaigns/. |
| Independent grader controls | Existing five self-tests pass; build-one one cycle over and a single group are findings; OWED lines name/link #977. Incomplete JSON and idle-shape probes expose F1; three guard-removal plants expose F4. |
| Stated-figure checks | Both flip points, load and shape checks pass; docs check passes. receipts/checks/. These check stated rows, not fresh CPU simulations. |
| Published firmware gates | Shard 0 at 5dba2089, shard 3 at ecd5bf41, shards 1/2 at f02d44cd: PASS. Shard 3 includes the corrected reset test and 48 shape-attributed early results. The earlier failed reset-plant run remains visible, superseded by the corrected run. |
| Published coverage | 40-file gate PASS; SRP 861/861 lines, 779/779 counted branches after exclusions. Raw table: 779/782 before exclusions. The head's ratchet agrees. |
| Published twin/routes | Twin, twin-plants, twin-maps and twin-maps-plants pass on unchanged production inputs. ExtraPostPlacementOpt routes meet #818 at every corner: worst WNS/WHS +0.128/+0.032 ns and +0.096/+0.036 ns. Image-identity checks pass. Other directives were not executed. |
| Published docs workflow | 99/103 commands pass at exact head; four CI-environment-dependent commands refuse locally (installation directory and event-path requirements). Those four are not passes. |

The resumed probe wrapper initially had a namespace compile error, corrected only in this packet. Its first one-interface run also included an inapplicable two-interface test, which the harness rejects as skipped; the final filter excludes it. Final receipts are listed above. Neither setup issue was a PR failure; obsolete attempts remain only in unpublished scratch/.

The paired cost measurements below are the author's published source-input-equivalent image runs. This review verified receipt hashes and grading logic; it did not rebuild or rerun those CPU simulations.

| Point | Kept Advertise / recount / Failed, CPU cycles | Bound Advertise | Kept maximum work pass | Kept / bound maximum single-build pass; limit |
|---|---:|---:|---:|---:|
| 1x1/1if | 34,497 / 32,224 / 36,859 | 38,956 | about 0.53 ms | 39,123 / 53,970; 73,500 |
| 8x8/1if | 137,352 / 68,692 / 142,909 | 153,208 | about 1.63 ms | 82,768 / 101,786; 147,500 |

Kept <= bound holds on each image. The 285/375 us SRP units are unchanged; every over-unit record is explicitly OWED #977. The 8x8 bound path's 224,540-cycle share overrun, walk and polls excesses are named OWED, not hidden passes. The kept group has no measured work pass over 2 ms. The unchanged row checks retain the 76.81/77 ms transmit row and 0.744/0.75 load figure. The five earlier groups retain their seven pre-existing backlog-owed misses. The 16 B hot-section growth was measured through those groups and the two new groups, not across every group.

Memory receipts/current docs agree on platform ROM/SRAM needs: 127,376/56,736 B at 1x1/1if; 128,984/59,104 at 1x1/2if; 140,136/98,288 at 8x8/1if; 141,720/115,760 at 8x8/2if. Planned tiles: 45.5, 46, 58.5, 63.5. The latter two use their named ledger debt, not the ordinary 56-tile limit. The fixture's 8x8/1if stand-in is 56 tiles with 112 B of ROM left. Ledger rejection thresholds remain in force.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance; cited clauses; srp_mbx.c:465, :968, :1340; original probes; test_plat_sinks.cpp Early.S13/S14 at both shapes. Registration survives until binding and produces the next transmit's Listener and flags in the host model. | R885-2 | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| RTL | CLEAN | No HDL, mailbox-contract or gitlink delta; srp_mbx.h:129/:200 storage/bounds; srp_mbx.c lifecycle and callback separation; library contracts; memory, hot-section, paired-cost and route receipts under the #977 ruling. Untouched hardware retains its prior verdict. | R885-2 | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| Robustness | UNCLEAN | Firmware reset/reclaim/expiry/refresh/flood/interface-isolation probes pass; kept_grade.py:123/:227 leave F1 open for missing grading fields and idle-result handling. | R885-2, applied; F1 open | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| Tests | UNCLEAN | srp_mbx.cpp, srp_early_mutants.py, campaign selection/platform tests; 48 independent kills; gate/coverage/twin receipts; kept_grade.py controls/plants. F1/F4 remain open. | R885-2, applied; F1/F4 open | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| Docs | UNCLEAN | SRP/plat READMEs, SPLIT_CONTROL_MEMORY.md, memory ledger prose, budget README/docstrings, PR/public receipts. Prior figures corrected; F1/F2/F3/F4 open; R1 is RESIDUE only. | R885-2, applied; F1/F2/F3/F4 open | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |

## Limits and pending manager duties

- Physical calibration NOT RUN. Field skips, host models, software routes and desk gates are not hardware proof. The physical acceptance rerun remains pending.
- No manager source bank exists at this exact head; none is inferred. Source evidence here is the author receipts plus this review's focused executions.
- The inspected exact-head hosted snapshot had all four workflows queued, with no completed execution to count. No skipped context is presented as executed evidence. Hosted/act acceptance remains the manager's.
- The source base is dd163e41, not GitHub's frozen PR base oid. The supplied live-dev point is e275d7950ef3385753e6a15d2e191ba855b171ed. The final current-dev candidate must be constructed and validated at the merge turn, including builder/native banks and published receipts; this review does not validate that future tree.
- Resolve MINOR findings and re-review the corrected head. Await all reviews and required independent positives, complete repository gates and candidate validation, then obtain explicitly authorized merge. Containment, current documentation, issue closure and Done remain pending. #977 remains owed before qualification closes.
- The clone was never source-edited. Byte/mode/index verification passes for all 1,938 candidate blobs and 1,362 blobs in the five required initialized submodules at their exact gitlinks. The unused external submodule is deliberately uninitialized. See receipts/tree-verification.txt.

## Reproduction and publication

Scripts take CHECKOUT PACKET as positional arguments. prepare_base.py extracts the prior adapter into scratch/f863; run_focused.py runs adapter/platform arms and three campaigns with a 16-job ceiling. probe_kept_grade.py and probe_selftest_coverage.py reproduce the new grader findings and intentionally exit nonzero while they exist. verify_evidence.py, audit_receipts.py, run_checks.py and verify_tree.py reproduce the other checks. Original probe bodies are retained; the wrapper supplies the fixture include and the internal class's anonymous namespace.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch trees, builds, extracted packets and obsolete attempts are excluded. No GitHub comment or review was posted.

R885-2 FINISHED
