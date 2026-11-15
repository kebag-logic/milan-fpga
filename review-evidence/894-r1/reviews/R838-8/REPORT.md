[R838] POSITIVE - exact head 234bc149ff888eb96659ecaaa5ce6e4fb27319d4

R838-8 resolves R838-7-F1 (MINOR, Tests and Docs). Both corrected PR-body sites agree with exact-head execution. The complete body scan found no other current-figure contradiction. No new BLOCKER, MAJOR or MINOR finding remains in this narrow re-review.

Tree: `9b54edcc9bd235b734ad559291cdf1ec6da4716c`. The source head is unchanged from R838-7. This verdict covers the two PR-text corrections and their quantitative consistency; R838-7's unchanged implementation assessment, limits, residue and optional suggestions stand.

## Scope, authority and independence

Reconstruction followed AGENTS.md and CONTRIBUTING.md, docs/README, issue #894 and public scope decisions, REQUIREMENTS.md and FR_NFR 3.4.1, the full-base diff inventory/history, then public executable evidence. The later-round instruction restricts new review to the metadata delta; code was not re-reviewed. The requested base inventory is retained in `base-diff-paths.txt` and the recent source history in `history.txt`.

The [round-13 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796) fixes the slice at the rule's choice, preserves the 130 ms bound and 0.70 load ceiling, and keeps 8x8/2if reported. The [1x1 scope ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [last-notice amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874) and [egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126) explain the frozen scope and 49/238 ms bounds.

The current PR body was independently scanned and the two checks executed before reading [R838-7's public findings](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6890766701). No other reviewer's report or private author material was read. Comparison with R838-7's public body snapshot shows exactly two changed content lines and a final blank line (`pr-body-delta.diff`). A final read confirmed the published source head and body remained unchanged; PR metadata last updated `2026-11-15T07:01:04Z`.

## Resolved finding

**R838-7-F1: MINOR, Tests and Docs - RESOLVED.**

- **Artifact:** PR #902 section 8, `pr-body.md:203`, and Findings row R838-6-F2, `pr-body.md:282`.
- **Authority/evidence:** AGENTS.md requires artifact-supported current claims. Exact-head `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` both exit 0. Raw outputs and exit receipts are `flip-check.txt/.rc` and `load-check.txt/.rc`.
- **Correction verified:** the section-8 load is **0.516 / 0.512**. The Findings row now gives **R4 13.10 ms**, **last queued notice 127.21 ms within 130**, at **950 us**. Its **13.05 / 132.71** figures are explicitly historical at **900 us**.
- **Impact/outcome:** the PR no longer describes a failed historical last-notice row as the current result. The quantitative defect is resolved without a source change. This also closes the retained PR cause of R838-6-F2 / R838-4-F1.
- **Verification:** local outputs are byte-identical to the published final author receipts. `reproduce.sh` repeats the focused checks from the exact source checkout.

| Current 1x1/1if row | Result, ms | Bound, ms |
|---|---:|---:|
| R4 | 13.10 | 20 |
| R4L | 188.48 | 238 |
| ACMP / ADP / MAAP | 28.95 / 27.30 / 27.42 | 30 each |
| First / last queued notice | 14.66 / 127.21 | 20 / 130 |
| R5 / R6 | 74.07 / 69.86 | 90 each |
| tx / txL | 33.38 / 48.43 | 49 each |

The entire numeric scan is recorded in `figure-scan.md`: status, attribution, class tables, restatement history, image claims, test counts, both Findings tables, validation examples, final gate table and limitations. The published pace/grid, class and join receipts agree with the current claims. Historical intermediate values remain identified as history. The reported 8x8/2if rows match their failing receipt; no passing 8x8 flip is inferred. Untouched campaign/image/source evidence keeps R838-7's prior assessment rather than becoming a claim of fresh execution.

## Five-lens results and reviewer-owned ledger

[R838] PASS Conformance - `pr-body.md:27,35,39,282`; FR_NFR 3.4.1; `flip-check.txt`, `load-check.txt` - current rows, bounds and load agree with the frozen 1x1 scope and exact-head checks; no bound or clause claim changed.

[R838] PASS RTL - `pr-body-delta.diff`; `source-integrity.txt`; unchanged `ctrl_loop.h`, `ctrl_loop.c`, mailbox/product wiring at the recorded tree - the metadata delta changes no architecture or source dependency. R838-7's source coverage carries at the identical head.

[R838] PASS Robustness - `pr-body-delta.diff`; `pr-body.md:232-253,360-365`; unchanged configuration/refusal/recovery tests recorded by R838-7 - no boundary, failure path or reported-limit claim changed. The 8x8 failures remain reported. Prior source coverage carries.

[R838] PASS Tests - `flip-check.txt/.rc`, `load-check.txt/.rc`, `published/model__flip-1x1-ed0df35b.txt`, `published/model__load-check-ed0df35b.txt` - both executed checks pass and match published receipts byte for byte; the corrected expected/current figures agree.

[R838] PASS Docs - `pr-body.md:203,282`, `pr-body-delta.diff`, `figure-scan.md` - both stale-current sites are repaired and all numeric claims were scanned in context. No remaining current-figure contradiction found.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PR current rows/bounds/load; FR_NFR 3.4.1; exact-head flip/load receipts | R838-8 metadata; R838-7 unchanged source | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| RTL | CLEAN | Two-line PR delta; byte/mode/index/pin integrity; unchanged architecture artifacts named above | R838-7 carried, R838-8 dependency check | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| Robustness | CLEAN | PR limitations and reported failures; metadata delta; unchanged prior recovery/configuration coverage | R838-7 carried, R838-8 dependency check | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| Tests | CLEAN | Local flip/load checks and exit codes; published final receipts; corrected PR expectations | R838-8; R838-7 unchanged tests | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |
| Docs | CLEAN | Whole PR numeric scan; corrected lines 203/282; old/current snapshot comparison | R838-8 | 234bc149ff888eb96659ecaaa5ce6e4fb27319d4 |

## Receipt and checkout integrity

At the fixed [published evidence commit](https://github.com/kebag-logic/milan-fpga/tree/9222da670fb7437ee6a0d5c939c44b2af40e2fbe/review-evidence/894-r1), all **222 author-r13 files** match the outer manifest. Of **221** inner-index entries, **216** match exact sizes/hashes; **five** script entries map original hashes through documented publication redactions. The final measurement receipts have no mismatch. The evidence commit is **unsigned**; checksums and object identity were verified, not cryptographic signer authentication. This is the same recorded evidence limit as R838-7.

`verify_source.py` checks actual tracked bytes, modes and stage-zero index entries against the commit tree, independently of status flags. It verifies **1,622** superproject blobs and all tracked blobs in the five required initialized submodules: protocol-processor, gptp-processor, third_party/lwSRP, third_party/tsn-c-stack and third_party/verilog-axis. All pins equal the head's gitlinks. `external` is uninitialized and not required. Checkout tracked status is clean. No source bytes were changed, so no restoration was needed.

## Residue and optional clarity

**R838-7-R1 - RESIDUE - Docs - retained for the manager's checklist, not a finding reopened here.** Artifact: `tb/verilator/ctrl_service_budget/edit_rows.py:3`. The owner comment rule excludes issue-comment IDs from source docstrings. Exact fix: replace `its ruling 6883864236 item 3` with `its SET_CONFIGURATION ruling, item 3`, retaining `#894`. Impact is wording only. Verify the docstring change leaves executable tokens unchanged. It does not dirty coverage.

**R838-8-S1 - SUGGESTION - Docs - final receipt label in the corrected Findings row.** Artifact: `pr-body.md:282`, verification column. The printed exact-head commands are correct, but the parenthetical still names `receipts/model/*-3909588f.txt`. For clearer provenance, replace that parenthetical with `author-r13/receipts/model/flip-1x1-ed0df35b.txt` and `author-r13/receipts/model/load-check-ed0df35b.txt`. These are the final receipts whose outputs match this head byte for byte. This changes neither a figure nor its pass/fail claim; the exact-head commands already validate the corrected row. Verification: open those receipts and compare to `flip-check.txt` and `load-check.txt`. Optional only.

All other prior finding dispositions and optional suggestions stand at unchanged causes. The following tables retain them for one-pass absorption; they are carried public conclusions, not fresh code-review claims. References inside these carried tables to probes or receipts belong to the published R838-7 packet unless present in this packet.

| Prior IDs | Disposition and cause-level artifact |
|---|---|
| R837-6-F1 | Resolved: final compare receipts include E1; timer/LINK/build/TICK corrected and rows/rules rerun. |
| R838-6-F1 / R837-6-R2 | Resolved: per-image receipt and section 13 replace universal ROM growth. |
| R838-6-F2 / R838-4-F1 | Resolved in R838-8: current PR load and row figures now agree with exact-head checks. |
| R838-6-R1 / R837-6-R1 | Listed round/lane instances removed; new comment-ID residue is R838-7-R1. |
| R838-6-R2 / R837-5-R1 | Resolved: historical-margin heading names round-30 measurements; misleading current-head wording removed. |
| R838-6-R3 | Resolved: PR says compiled firmware output, supported by identity evidence. |
| R837-6-S1 / R837-5-S1 / R838-5-S7 | Indexer checks readback after sanitizing; publisher redactions map through outer manifest. Optional S2 retained. |
| R837-6-S2 | Later-record case fixed and planted; gap/deferred-response limit remains optional S1. |
| R837-4-1 | Actual-array/domain assertion and floor retained in `aecp_maps.c`; map storage/indexing unchanged. |
| R838-4-F2 | Correct work-arm selection retained in `aecp_arms.py`. |
| R838-3-F1 / R837-3-1 / R838-2-F2 | Direct-index collision/work fixes retained; map algorithm unchanged. |
| R838-3-F2 / R837-3-2 / R838-2-F3 / R837-2-3 | Corrected bounds/references retained; current slice sites updated to 950. PR summary exception is resolved by R838-8. |
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

## Limits and pending manager duties

This is source-head review, not merge-candidate validation or merge authorization. No manager source bank exists at this head and none is claimed. Author source execution receipts remain distinct from the final candidate. The manager must validate and publish builder/native receipts for the candidate against current live dev (stated live tip `6b66f66d89cf25d2717687bcc2c3bf617685a99a`; source base `66f713267f201d1a00d7f711e04b3a996d804dee`), settle hosted/local workflow acceptance, obtain both independent positive reviews with no round in flight, and perform post-merge containment and the remaining issue workflow duties.

No full banks, source fixes, commits, pushes, GitHub writes, merge, author contact, sub-agents, container workflow runs or hardware operations were performed. Only the two focused graders ran anew. Historical executed steps and skipped contexts remain distinct; no new hosted-job acceptance claim is made. Physical calibration is NOT RUN; field skips and simulated join intervals are not hardware proof. Existing product-port, 8x8 and #910 limitations stand as R838-7 recorded.

Publish only REPORT.md and files listed in MANIFEST.sha256. Scratch data is excluded. All commands have finished.

R838-8 FINISHED
