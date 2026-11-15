[R838] NEGATIVE - exact head 234bc149ff888eb96659ecaaa5ce6e4fb27319d4

R838-7 applied all five lenses to the fifteen-commit, 24-file delta from `9606b3a915de284c71d3063c2e8d94b097f18241`. One MINOR remains: the PR presents earlier quantitative results as current, retaining R838-6-F2's cause. No functional regression was demonstrated. One source-comment RESIDUE and optional suggestions are separate from the negative verdict.

Tree: `9b54edcc9bd235b734ad559291cdf1ec6da4716c`. This is an external source-head review, not current-dev candidate validation or hardware acceptance.

## Authority and method

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README, issue #894 and its public decisions, linked requirements/interface authorities, the requested full-base diff inventory/history, then the delta and public evidence. The full `66f713267f201d1a00d7f711e04b3a996d804dee..234bc149` comparison includes imported earlier work; the later-round instruction governs fresh examination. Untouched behavior retains prior assessment unless a changed dependency affects it.

I recorded an independent preliminary verdict and five-lens ledger before reading prior public review findings. Reconciliation then exposed the PR contradictions below. No concurrent reviewer report, private author material or management checkout was read. No source fix, commit, push, GitHub write, merge, hardware operation or prohibited bank was performed.

Principal authorities:

- [Round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6883864236), [SRP drain relay](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6886633874), [round-13 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796).
- [Contingent bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025), [last-notice amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874), [egress/pace ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), [table-survey instruction](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6881287231), [1x1 scope/#910 disposition](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730).
- REQUIREMENTS.md product ownership; FR_NFR 3.4.1; ARCHITECTURE_HW_SW_SPLIT ownership/clocks; MAILBOX_CONTRACT.md:346,1133; AECP README; Milan v1.2 5.4.2.5/5.4.5.2 and IEEE 1722.1-2021 7.4.7/7.5.2/9.3.2.6 as traced by those authorities.
- [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6890460677), [review start](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6890507252), [published archive](https://github.com/kebag-logic/milan-fpga/tree/9222da670fb7437ee6a0d5c939c44b2af40e2fbe/review-evidence/894-r1). Below, author-r12/r13 paths refer to that archive.

## Finding

### R838-7-F1 - MINOR - Tests, Docs - stale current figures remain in the PR's claimed resolution

- **Artifact:** PR #902 body, section 8's **No stale current figure** bullet and the Findings table's **R838-6-F2** row. Fetched snapshot: `public-pr-body.md:203,282` in this packet.
- **Authority/evidence:** R838-6-F2 requires current quantitative summaries to agree with executable results. The bullet explicitly calls **0.515 / 0.511** this head's load. The resolution row calls **R4 13.05 ms** and **last queued notice 132.71 ms, over 130** the current summary and says the figures are the head's. Exact-head commands instead give **0.516 / 0.512**, **R4 13.10 ms**, and **last 127.21 ms, within 130** (`checks/load-check.log`, `checks/flip-check.log`). SPLIT_CONTROL_MEMORY section 13 and the PR's later validation example already carry the corrected figures.
- **Impact:** the public resolution contradicts executable results and, for the last notice, describes a failing earlier row as current. This is a quantitative evidence defect, not a demonstrated firmware timing failure. Changing a figure or its pass/fail claim is not wording-only RESIDUE under the specified rule.
- **Required outcome:** change the section-8 loads to **0.516 / 0.512**. Change the resolution row's current results to **R4 13.10 ms, last 127.21 ms within 130 at the 950 us slice**, referencing the final receipt. Alternatively label old values explicitly as historical intermediate results and point to their final replacement.
- **Verification:** compare both sites with exact-head flip/load commands. A public-text correction suffices; no source change or new full bank is needed. R838-6-F2 remains open at this cause until the correction is reviewed.

## Residue

### R838-7-R1 - RESIDUE - Docs - new source docstring names an issue-comment ID

- **Artifact:** `tb/verilator/ctrl_service_budget/edit_rows.py:3`.
- **Authority/evidence:** the owner comment rule prohibits issue-comment IDs in new source comments/docstrings. The new text says `its ruling 6883864236 item 3`.
- **Impact:** wording only; no measurement, clause claim, behavior or privacy rule changes.
- **Exact outcome:** replace that phrase with `its SET_CONFIGURATION ruling, item 3`, retaining the existing `#894` reference.
- **Verification:** inspect the added docstring line; executable tokens stay identical. This does not dirty coverage.

## Implementation, architecture and robustness

`aecp_commands.c:100-137,178-220` keeps the configuration status order: length, observation/running refusal, foreign lock, index validity, acceptance. Naming the current index still performs the running check. `observe` receives a zero-initialized structure with `brief=true` only for running checks; ordinary `aecp_stream_read` retains full observations.

`aecp_face.c:119,169-187` reads selector 0 for a brief observation, retains output-running ownership through the SRP licence, and propagates failed window observations. `ctrl_app_aecp.c:49-66` still supplies input binding from the ACMP owner. Reducing six reads to one therefore does not substitute unowned running state.

The configuration change reports `moved` independently of override establishment. Only a moved index publishes stream entries; the same-index first SET still persists and commits settings. The application forwards the marker, while `aecp_nvm_changed` marks configuration independently of that index, so persistence is not misaddressed. Notification and repeated-SET behavior remain intact. The late-commit recovery path still republishes whole state.

Acceptance stamps `edited_ms` before publication, including an accepted no-op; refused commands do not stamp it. The adapter's readiness gate holds the next record without dropping it. `edit_rows.PACED` derives the shared class from the dearer member: **300 us** at 1x1/1if, **595 us** at 8x8/2if. The whole-ms `ceil((w+1)/P)` count remains, and largest-command rows retain separate charging.

`CTRL_LOOP_SRP_UNIT_US` is **280/365 us**. `ctrl_loop.c:322` reserves it before starting a record. `load_grade.srp_unit` checks both points against the dearer table column in the actual check, with named plants at both points. `Loop.L23TheDrainIsTierTwoInASlice` reads the constant; the existing drain-limit mutation targets the runtime expression.

The one-interface slice is **950 us**, with its rule in `ctrl_loop.h:263-285`. Self-tests read the header and computed rule instead of requiring a 900 literal. `CTRL_LOOP_BUILD_MOST` remains **1**, since 950 is below the **1,010 us** build-of-both statement. No HDL or submodule pin changes occur in this delta.

### Item 5: product completion argument

The claim in `author-r13/receipts/item5-no-late-completion.md` has a code basis, not just a desired timeout. `milan_soc.py:3248-3273` connects the product face through the CDC block. `KL_mbx_cdc.sv:266-280` transfers the commit edge, captures held settings on the destination pulse and uses that same pulse to initiate the acknowledgement crossing. There is no ready/backpressure condition. `KL_mbx.sv:606` clears BUSY on acknowledgement. `mbx.c:337-352` waits through up to 65 status reads after GO, covering the contract's 64 mailbox cycles; sequential firmware finishes one commit before another begins.

Thus the normal live-clock product path does not create an owed interface or enter delayed completion. `split_soc.py:226-239` deliberately holds the fixture acknowledgement to the contract limit. The published product-composition receipt reports two polls. This discharges the ruling's alternative for supported operating clocks and reset state. It is not a proof against stopped clocks, reset/CDC failure or a noncompliant datapath. The independent native baseline passes `Face.ALateCommitIsOwedAndPublishedAgainWhole`; recovery behavior remains tested. No late-completion CPU cost was newly measured or claimed.

## Measurements and executable checks

`audit_timing.py` independently checks **263**, **91** and **66** comparison rows in the published full-1x1, separate answering-port and 8x8 surveys. Integer arithmetic verifies measurement plus 5%, rounded up to 5 us. All parsed rounding/verdict calculations agree. The 1x1 exceptions are separated long-notice and paced-record classes; the 8x8 build-of-one exception is the known #910 limitation, not a pass.

The repaired survey includes all **16** 1x1 answering-every-port groups, all **96** arm-A groups, and the answering-ports leg. The 8x8 survey includes its published arm-A/answering-port legs; it does not establish a fresh complete 96-group run there. This resolves the specific omitted held leg in R837-6-F1. Zero-observation rows remain carried statements, not fresh measurements.

| Restated cost | Triggering cycles | Rule, us | Stated, us |
|---|---:|---:|---:|
| Build of one | 69,635 | 735 | 735 |
| AECP timer slot | 6,206 | 70 | 70 |
| LINK | 14,715 | 155 | 155 |
| TICK after drain change | 4,784 | 55 | 55 |

The rebuilt image's TICK maximum is **4,692**, or **50 us** by the rule; retaining **55** is conservative. Its polls' base is **19,074 cycles**, **205 us** by the rule, within its 205 statement. No new restatement is needed for published final 1x1 measurements.

Pre-cut attribution sums reconcile: **6,322 + 16,131 + 8,823 + 2,448 = 33,724**, and **17,729 + 37,812 + 7,322 + 15,469 = 78,332**. The author reports intermediate cut results **28,509 / 55,377**, rounding to **300 / 585 us**; cut-run receipts identify `f275b619` and exit zero. Final class receipts contain **28,376 / 56,474**, rounding to **300 / 595 us**, held as paced. The extracted cut receipts do not contain intermediate per-record raw traces, so I do not claim independent raw-event reproduction of 28,509/55,377.

`record_classes.py` now requires accepted SET_CONFIGURATION and SET_STREAM_INFO in the answering-ports fanout leg and holds them by class. All eleven controls pass. Its next-record boundary prevents the reported attribution to a later record's response; a remaining optional limit is S1 below.

Own exact-head results:

| Row | ms | Bound, ms |
|---|---:|---:|
| R4 | 13.10 | 20 |
| R4L | 188.48 | 238 |
| ACMP / ADP / MAAP | 28.95 / 27.30 / 27.42 | 30 each |
| First / last queued notice | 14.66 / 127.21 | 20 / 130 |
| R5 / R6 | 74.07 / 69.86 | 90 each |
| tx / txL | 33.38 / 48.43 | 49 each |

Flip and load checks pass; loads **0.516 / 0.512**. `tier_grid` chooses the built **950 us**, aecp-first/srp-first, queue, cap 2 design; ten of 420 candidates hold. Pace stays **8 ms**. Published join extrema **185.486-190.147 ms** fit **181-239 ms**; full arm A separately reports **187.994-190.021 ms**. These are simulation commitments, not physical/wire calibration.

Own tests: flip controls **585/585**, tier controls **1,033/1,033**, load controls **26/26**, class controls **11/11**, all exit zero. The focused native baseline passes **eight tests**, covering statuses, observations, moved-index publication, pacing and late recovery. Three disposable mutations fail with their required diagnostic: no GSI read, stream publication on every SET, and accepted configuration left unpaced. Build failures/crashes do not count. See `configuration/results.json` and raw logs. Jobs ran concurrently within sixteen compile jobs; all have finished.

## Integrity, carries and source evidence

All **394** published author-r12/r13 files match the outer manifest (**172 + 222**). Inner indexes have **392** rows. Twelve script rows reference bytes before additional publisher path redaction; each maps through `original_sha256` and `path_redacted=true`, and every published file matches `published_sha256`. No measurement receipt mismatch remains. The archive commit is unsigned: content integrity was verified, but cryptographic signer authentication was unavailable.

All eight ROM rows reconcile. Earlier edit-cut growth is **+224 B** per 1x1 image and **+208 B** per 8x8 image. Configuration cut/stamp growth is **+224 B** for the 1x1/1if fixture and **+216 B** for each other image. The 8x8/2if platform remains **130,920 / 131,072 B**, **152 B** spare. R838-6-F1 is resolved.

Independent inventory comparisons verify **166/166** two-interface image hashes and **6/6** two-interface harness ELF hashes. The four one-interface images differ only in loop object, ELF and binary inventories. From `c274b9f5` to `ed0df35b`, only five Markdown files change; from there to `234bc149`, only `ctrl_service_hooks/hooks.py`. Inspected sweep/workflow inputs do not read that module; its lane reader was rerun. The final hooks receipt reports **28/28 checks, 96/96 mutants**, with the corrected publication anchor and retained `every` reference.

Published author receipts cover firmware/RTL/elaboration jobs, lane b/c and four successful sweep shards at `ed0df35b`, with refreshed part a and applicable jobs at `234bc149`. The combined workflow receipt distinguishes **139 executed zero-exit steps** from **226 NOT RUN entries**. Full campaigns report **299/299 AECP**, **716/716 control**, and passing coverage. I inspected available receipts and ran focused checks, not those full banks. Digest/summary evidence does not imply inspection of unpublished full logs or binaries.

Raw tracked bytes, modes and index were independently verified: **1,622** superproject blobs and all tracked blobs in the five required initialized submodules. Pins equal the head's gitlinks. `external` remains uninitialized and is not required. `identity.txt` records exact identities; checkout status is clean. All disposable trees/builds are inside unpublished `scratch/`.

## Prior findings: resolved or retained

Reconciliation used [R838-6](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6884009601) and [R837-6](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6884063444) after the independent pass. Earlier resolutions are carried at unchanged causes, not represented as newly rerun full reviews.

| Prior IDs | Disposition and cause-level artifact |
|---|---|
| R837-6-F1 | Resolved: final compare receipts include E1; timer/LINK/build/TICK corrected and rows/rules rerun. |
| R838-6-F1 / R837-6-R2 | Resolved: per-image receipt and section 13 replace universal ROM growth. |
| R838-6-F2 / R838-4-F1 | Source-document summary corrected; PR cause retained as R838-7-F1. |
| R838-6-R1 / R837-6-R1 | Listed round/lane instances removed; new comment-ID residue is R838-7-R1. |
| R838-6-R2 / R837-5-R1 | Resolved: historical-margin heading names round-30 measurements; misleading current-head wording removed. |
| R838-6-R3 | Resolved: PR says compiled firmware output, supported by identity evidence. |
| R837-6-S1 / R837-5-S1 / R838-5-S7 | Indexer checks readback after sanitizing; publisher redactions map through outer manifest. Optional S2 retained. |
| R837-6-S2 | Later-record case fixed and planted; gap/deferred-response limit remains optional S1. |
| R837-4-1 | Actual-array/domain assertion and floor retained in `aecp_maps.c`; map storage/indexing unchanged. |
| R838-4-F2 | Correct work-arm selection retained in `aecp_arms.py`. |
| R838-3-F1 / R837-3-1 / R838-2-F2 | Direct-index collision/work fixes retained; map algorithm unchanged. |
| R838-3-F2 / R837-3-2 / R838-2-F3 / R837-2-3 | Corrected bounds/references retained; current slice sites updated to 950. PR summary exception is F1. |
| R838-3-F3 | Historical aligned-ROM reconciliation retained; new arithmetic checked. |
| R837-2-1 / R837-2-2 | 49/238 egress bounds and whole-ms count retained in loop/pace/join artifacts; model checks pass. |
| R838-2-F1 | Horizon-free join classification/controls unchanged; new joins fit corrected bounds. |
| R838-1 F1 / R837-1-1 | Tier-1 rows, long-record storage/charges retained; recomputed rows pass. |
| R838-1 F2 / R837-1-2 | MRP budget, static assertion, tx/txL proof retained; 33.38/48.43 ms now. |
| R838-1 F3/F4 | Longer-notice-after-drain and ordinary-round-clear tests/plants unchanged in AECP/loop files. |
| R838-1 F5 / R837-1-3 | MAILBOX_SPLIT current slice correctly updated to 0.95 ms. |
| R838-1 F6/F7 / R837-1-5 | Rotating order and conditional Domain/VLAN claims retained; licence/resume/reset/gap causes unchanged. |
| R837-1-4 / R838-1 S5 | Reported 8x8/#910 scope retained; no passing flip inferred. |
| R838-1 RS1 / R837-1-6; R838-2-R1 / R837-2-4; R837-4-R1 | Original source-comment repairs retained; new residue separately listed. |
| R838-2-R2 / R837-2-5; R838-3-R1 / R837-3-R1; R837-4-R2; R838-4-R1 / R838-4-S10 | Historical receipt/head/count/share repairs retained; no historical count promoted to fresh measurement. |

## Optional suggestions consolidated

All rows below are SUGGESTION. None creates a merge requirement or dirties coverage. Each row gives all lenses, artifact, evidence/impact, suggested outcome and verification.

| ID; lenses; artifact | Evidence / impact | Suggested outcome / verification |
|---|---|---|
| R838-7-S1, retaining R837-6-S2; Tests, Robustness; `record_classes.py:102-112` | Naming ends at next record start, not measured span end. `audit_timing.py` demonstrates a span ending at 23,000 named by a response at 40,000 before next start 1,000,000, charged paced. No published run is shown misclassified. | Correlate deferred replies with request/sequence identity or use true spans where valid; preserve legitimate polled replies and add a gap control. |
| R838-7-S2, retaining R837-6-S1 / R838-5-S7; Docs; archive INDEX/MANIFEST | Twelve script hashes differ after publisher redaction but are explicitly mapped; published bytes verify. | Re-index published bytes or state beside INDEX that original hashes map through MANIFEST; rehash to verify. |
| R838-5-S1; Docs; AECP README owed ordering | Later-response/earlier-notice order can expose an older cached value. | Add a two-controller example; compare response/notice order. |
| R838-5-S2; RTL; `aecp.c` counter reset | Earlier redundant defensive reset unchanged. | Explain invariant, or remove only with queue/retry verification. |
| R838-5-S3 / R837-1-8; Tests; `aecp_owed_notice_steps.py` | Offline scenario remains; native tests supply execution evidence. | Drive compiled behavior and require a behavioral plant failure. |
| R838-5-S4; Tests; measurement inventories | Widened survey improves coverage; sustained pressure/counts remain useful. | Publish counts/maxima and reconcile spans under longer expiry pressure. |
| R838-5-S5 / R837-1-7; Tests; `rows_tiers.least_margin` | Unsolved -1 can outrank solved scores below -1; passing choice unaffected. | Rank unsolved last; add mixed failed-search ordering control. |
| R838-5-S6; Tests; ACMP decline bound | Conservative prior bound unchanged. | Tighten only with source proof and mutation control. |
| R838-5-S8; Tests; `mrpdu_grade.py:84` | Callback-late and owed-centisecond origins differ. | Explain/align origins; test delayed callback. |
| R838-5-S9; Tests, Docs; H-81N receipt | Resolved: model-size exception distinguished from timing miss. | Retain distinction; no new action. |
| R838-5-S11 / R837-4-S1; Tests; `aecp_maps.c` first-coordinate guard | Earlier guard-removal plant survived admission; guard unchanged. | Add an admitted descriptor/edge case killing it. |
| R838-5-S12; Docs; floor discussion | Placement sensitivity remains; attribution improves explanation. | Explain remaining margin assumptions against measured counterfactuals. |
| R838-5-S13; Robustness, Docs; format/domain contract | Safety depends on admitted formats/fixed cluster widths. | State precondition; check generated keys when widths change. |
| R838-5-S14; Robustness, Docs; `struct edit` | Wide-table size is not full-call-chain stack proof. | Measure target peak stack before extending supported images. |
| R838-5-S15; Tests, Docs; historical item-2 provenance | Current carry has inventories; older subset attribution optional. | Retain run heads/input-identity spans beside historical probes. |
| R837-5-S2; Tests; undersized-table plant | Wider-domain refusal was probed, but lacks permanent wide plant. | Add floor-only 16x32 plant requiring assertion diagnostics. |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR 3.4.1; `aecp_commands.c:178-220`; `aecp_face.c:119,169`; `edit_rows.py`; `checks/flip-check.log`; `timing-audit.txt` | R838-7 | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| RTL | CLEAN | `ctrl_loop.h:263-331`, `ctrl_loop.c:322`, `mbx.c:337-352`, `KL_mbx_cdc.sv:266-280`, product wiring, image carry | R838-7 | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| Robustness | CLEAN | `test_aecp.cpp` configuration/refusal/recovery cases; new mutation table; three independent plants; class/SRP controls | R838-7 | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| Tests | UNCLEAN: F1 | Exact-head checks, native logs, timing/packet audits; contradictory PR expected/current figures at snapshot lines 203,282 | No clean covering round; examined R838-7 | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| Docs | UNCLEAN: F1 | Section 13, FR_NFR, changed READMEs/comments; PR snapshot lines 203,282; archive provenance | No clean covering round; examined R838-7 | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |

## Limits and pending manager duties

No manager source bank exists at this head and none is claimed. Author source receipts are distinct from the future candidate against live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`; source base is `66f713267f201d1a00d7f711e04b3a996d804dee`. The manager must publish candidate builder/native results at merge, settle hosted/act acceptance, obtain independent positive reviews with none in flight, and perform merge containment before closing the issue. This verdict is not merge authorization.

No full parent, processor, synthesis or builder bank was rerun. No hardware or physical calibration ran. Field skips and simulated joins are not hardware proof. The product's one-word GSI observation cost is not measured by the answering-ports fixture, which supplies observations directly; the packet states that limit. Reported 8x8/2if rows, #910 and known 8x8/1if exits remain outside this lane's flip acceptance, not newly passing results.

Publish only REPORT.md and files listed in MANIFEST.sha256. Disposable builds, extracted evidence and intermediates remain under unpublished scratch/.

R838-7 FINISHED
