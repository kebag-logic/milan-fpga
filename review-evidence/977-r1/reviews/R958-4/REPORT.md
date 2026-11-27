[R958] NEGATIVE - exact head 3256d1d21e525e564eb92d1cf721750ddf44fde2

R958-4 applied all five lenses to the four-commit delta `3181a3ec372b6473175cc1c842ada8133a96b127..3256d1d21e525e564eb92d1cf721750ddf44fde2`, tree `6810c12ebf0f060a9557e3fbe356a99cffef8c2a`. The adapter defect is corrected. The deferred-delivery decision is public, its after-window baseline is implemented, and the stated arithmetic and floor controls agree. Two findings remain: the owner ceiling decision, and incomplete per-record coverage in the published delivery measurement extractor. Two wording/publication residues follow.

**At 0.77 the PR does not pass.** Independently reproduced loads are **0.7821365 at 8x8/1if** and **0.5325402076023392 at 1x1/1if**. Everything apart from authorization was judged against the requested proposed ceiling of **0.79**. That passing calculation does not authorize a new owner bound.

Reconstruction followed the repository contract, documentation index, frozen issue acceptance/public decisions, linked requirements/interfaces, source-base diff inventory/history, narrow delta, then public executable evidence. The source base inspected was `dev-soft-core` at `0b5940237e8de8bd5912db87e5e036a78f59b5a6`. Authorities included REQUIREMENTS ownership/NFR-SCOUT-03, FR_NFR section 3.4.1, SPLIT_CONTROL_MEMORY section 13, `ctrl_app_srp.c:134-209`, and the issue's population, delivery, alone-record and deferred-cost rulings. Prior public findings were read after the independent diff pass. No current-round reviewer report or private author material was consulted. Unchanged implementation retains its previous assessment, subject to the measurement dependency below.

**R958-4-F1 - MAJOR - Conformance - `tb/verilator/ctrl_service_budget/flip_grade.py:67-70`, `docs/reference/FR_NFR.md:427`, commit `3256d1d2`: the 0.79 ceiling still requires the owner's decision.**

- Authority/evidence: the [manager decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7229657853), items 3-4, leaves 0.77 in force and requires the owner answer before merge. The [owner's 0.77 decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7213594113) remains the latest ceiling approval. The final issue read contained 19 comments, ending with the manager decision; the PR and last commit expressly say the answer is pending. `model-probe.json` records the passing 0.79 calculation and failing 0.77 calculation. The last commit's reverse applies cleanly, exit 0.
- Impact: the proposed bound is reviewable, but its passing result does not satisfy the currently published acceptance criterion. This retains R958-3-F2 at the new proposed figure.
- Required outcome: publish the owner answer. If approved, cite it in the ceiling authority and requirement text. If refused, revert the separate ceiling commit and retain the failing 8x8/1if status pending authorized margin work. Preserve the sourced delivery term.
- Verification: reconcile the public answer, FLIP/RULED_FLIP, requirement text and resulting load. A citation correction alone requires no product rebuild.

**R958-4-F2 - MINOR - Conformance, RTL, Tests, Docs - public `author-r12/receipts/deliv12.py.txt:24-43` and both `meas/deliv-*-e59cf6ea.txt`: burst labels repeatedly select the first receive commit, leaving the claimed per-record maximum incompletely established.**

- Authority/evidence: this is the measurement dependency of R957-3-F1, within the requested DELIVERY_US re-review. The issue requires the fastest registering burst; `load_grade.py:379-382` claims the dearest record over every registering group of both arms. The extractor collects unqualified RXC timestamps and independently chooses the first timestamp at or after each mark. It neither associates the tagged record nor consumes a matched receive. `register_window.py:147-182` queues three separately tagged records at each burst opportunity and adds a transmit probe.
- The published 8x8 receipt's lines 4-7 assign `t0.r0`, `t0.r1`, `t0.r2` and `register_tx.t0` the identical receive timestamp **198715609** and identical window. This repeats for every triple at both shapes. Each table has 40 labelled rows but only 22 distinct group/record timestamps. Six rows per shape are transmit-probe aliases; twelve later burst records are not independently located. The single-record swap maximum reproduces, but this does not prove the omitted windows are cheaper.
- `probe_extraction.py` executes the exact published extractor with a synthetic queued-record fixture and controlled parsed poll sections. Three marks precede receive commits at 10000, 20000 and 30000. The extractor selects 10000 three times and reports zero excess. Applying its same five-pass window and after-window baseline to the distinct later records gives **495 cycles per sink**. This proves the association error can hide a larger later window; it does not claim that the product's actual cost is 495 or exceeds 160/200 us. See `extraction-probe.json` and `evidence-audit.json`.
- Impact: the new baseline and reported single-record arithmetic are correct, but complete coverage supporting the maximum/floor is unproved. A later burst record can be omitted from CPU-cost evidence. This affects the load-model resource claim, acceptance evidence and documentation; no firmware behavior defect is asserted.
- Required outcome: associate each registering record with its own tagged receive commit on the correct channel, exclude transmit-only probe aliases, and refuse missing/ambiguous records. Re-extract from existing logs, keeping the accepted after-window baseline and both comparison medians. Update the maximum/floor if the complete measurement requires it.
- Verification: a queued triple must yield three distinct matching commits; the synthetic later-window excess must be observed. Publish corrected per-record receipts for both arms/shapes and rerun floor/load/flip checks. If the resulting load breaches the proposed ceiling, return that result to the owner. No broad firmware bank or new product build is requested.

**R958-4-R1 - RESIDUE - Docs - new source comment identifiers.**

- Artifacts: `load_grade.py:13,374`, `load_deliveries.py:3`, `flip_grade.py:66` newly spell `comment 7229657853`.
- Authority/evidence: the owner comment rule excludes issue-comment IDs from source comments while permitting issue and requirement IDs. These are prose/docstring references only; the identifier changes no executable control, value, verdict or clause claim.
- Impact: wording only; this residue leaves no lens unclean.
- Exact fix: replace these references with `#977, the manager's decision of 2026-11-27 on deferred deliveries`, adjusting sentence order as needed. Keep actual decision hyperlinks in authoritative Markdown.
- Verification: scan added source comments for the removed identifier and preserve the decision links in FR_NFR and SPLIT_CONTROL_MEMORY.

**R958-4-R2 - RESIDUE - Docs - historical packet notes remain unpublished.**

- Artifacts: public `author-r10/receipts/INDEX.md`, `author-r11/receipts/INDEX.md`, `author-r12/REVIEW-READY.md:16`, PR Contents/Status summary.
- Evidence: the older indexes still lack the dated supersession and compressed-to-published-path notes. New REVIEW-READY accurately says they remain to be published. The r12 index includes its own publication note. The PR Contents nevertheless says both reviews' findings and residues are fixed.
- Impact: historical prose/navigation only; receipt bytes and manifest hashes remain available and verified. This retains the publication part of R958-3-R2 / R957-3-R4.
- Exact fix: append the dated r10 note naming supersession of pending-80-ms wording, reviewer placeholders, all-zero run counts and default-option explanation. Append notes to both older indexes mapping `.txt.gz` rows to published `.txt` paths and identifying MANIFEST.json as hash authority. Preserve receipt bytes. Until publication, change the PR summary to `code corrections applied; historical index notes remain to be published`.
- Verification: fetch the updated public indexes and follow their mapped paths. This residue leaves no lens unclean.

**Prior findings at their causes**

| Prior finding | Disposition | Examined evidence |
|---|---|---|
| R957-3-F1, Conformance/RTL/Tests/Docs | Baseline/floor correction accepted; measurement completeness retained as F2; owner acceptance retained as F1 | `load_grade.py:374-389,690-704`; `load_deliveries.py:35-39`; published extractor/tables; arithmetic and probes |
| R957-3-F2, Conformance/Docs | CLOSED | Public comment 7229657853 explicitly selects option (a), baseline, rule and floor. FR_NFR:427 and SPLIT_CONTROL_MEMORY:2561 link it. Source references identify it, with wording residue R1. |
| R958-3-F1, Tests/Robustness | CLOSED | `flip_grade.py:70-74,202-206,458-465`, `load_grade.py:955-966`: 0.70-to-0.71 fails controls(), flip_checks() and ceiling_checks(); unknown failures remain visible through both adapters. |
| R958-3-F2, Conformance | RETAINED as F1 at proposed 0.79 | Load fails 0.77; separate ceiling commit reverses cleanly; owner answer pending. |
| R958-3-R1 / R957-3-R3, Docs | CLOSED | PR labels read `the internal review` and `the external review`, with direct prior-finding links. |
| R958-3-R2 / R957-3-R4, Docs | Partly corrected; publication retained as R2 | Current handoff no longer claims notes are public; published older indexes lack them. |
| R957-3-R1 and R957-3-R2, Docs | CLOSED | Cost comments describe the method without the old script label; harness README:244 states the deliveries exception. |
| R957-3-S1, Tests | ADDRESSED | `srp_deliver_mutants.py:15-17` states where unprefixed plants run; this delta changes only its docstring. |

Earlier closures stand where this delta changes no dependency. No broad repeat review of firmware, CDC/reset behavior, S14, loss-turn logic or existing routes is claimed.

**Evidence and limits**

| Check | Result |
|---|---|
| Manifest | All **285 author/author-text/author-r10/r11/r12 files** match published SHA-256 values. Review-report files were excluded from the hash audit. |
| ELF identity | Three parsed receipts each contain two matching maps of **80 ELF paths**; all maps agree across measured images, `25ff0632`, previous review head and exact head. There are 30 distinct hashes. This verifies published identity receipts, not an independent rebuild or direct rehash of binaries. |
| Product identity | Six production source/hot-list files changed since `25ff0632` have equal comment-free tokens/entries. The narrow delta changes no production code or gitlink. |
| Delivery arithmetic | 8x8: 135935 / 9 = 15103.8889 cycles, **160 us** by the rule, after-median 12089. 1x1: 37555 / 2 = 18777.5 cycles, **200 us**, after-median 6016. Comparison baselines reproduce 125/145 us at 8x8 and 190/200 us at 1x1. F2 limits the completeness claim. |
| Floor refusals | 155 us at 8x8 is refused against 160, including `load_grade --check` exit 1. 195 us at 1x1 is refused against 200. |
| Independent focused gates | Load check, both held-point flip checks, load self-test **32/32**, flip self-test **628/628** all exit 0. Baseline adapter checks pass; malformed-ceiling and unknown-name probes fail. 0.790 passes; 0.791 fails. Commands/logs/rc files are retained. |
| Author source-head gates | Hash-verified r12 receipts report harness self-test, shape/kept checks and documentation checks at this head. These are author receipts, not a manager source bank. |
| Whitespace / final ceiling | Source-base `git diff --check` exits 0. Final ceiling reverse-application check exits 0; no actual revert was made. |
| Packet signature | Evidence commit `6208d96398000bce22a2fedc14788fee68b9f4ae` has no signature header. Hash integrity is verified; a cryptographic packet signature is **not established**. |

Full CPU trace logs and ELF binaries are not published in this packet. The audit checks published arithmetic and extraction logic; the synthetic probe cannot supply corrected product measurements. No scoped simulator, hardware or broad bank was used. Physical calibration is **NOT RUN**; field skips are not hardware proof. Hosted jobs were not audited in this narrow pass; neither an executed hosted gate nor a manager source bank is inferred.

**Independent lens results and reviewer-owned ledger**

[R958] MAJOR Conformance - issue decision 7229657853, FR_NFR:427, `load_grade.py:374-389`, delivery receipts - baseline/rate arithmetic and proposed-ceiling checks agree; F1 retains authorization and F2 complete measurement evidence.

[R958] MINOR RTL - `ctrl_app_srp.c:134-209`, production-token/ELF identity, `load_grade.py:379-387` - scheduling, interfaces, placement and pins retain prior implementation results; complete deferred-work cost supporting the resource model remains limited by F2.

[R958] PASS Robustness - `flip_grade.py:458-465`, `load_grade.py:955-966`, `load_deliveries.py:16-39`, `model-probe.json` - prohibited ceilings, unknown failed-control names, missing/halved/zero delivery terms and below-floor costs are refused. Prior adapter failure closed; product robustness behavior unchanged.

[R958] MINOR Tests - `selftest_mutants.py:539-543`, control adapters, published `deliv12.py.txt:24-43`, delivery tables and extraction probe - controls detect their claimed faults; F2 leaves later burst windows unmeasured by this extractor.

[R958] MINOR Docs - SPLIT_CONTROL_MEMORY:2548,2561,2578; FR_NFR:427; harness README:244; PR and packet - decision, baseline and comparison medians are documented correctly; F2 limits the complete-maximum claim. R1/R2 are wording residue.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F1, F2 | Public decisions; FR_NFR; rate/floor arithmetic; burst extraction | R958-4 applied; no clean covering round | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| RTL | UNCLEAN - F2 | Delivery contract; production tokens/gitlinks; 80-path identity; deferred-work cost | R958-4 applied; runtime assessment inherited | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| Robustness | CLEAN | Invalid-ceiling, unknown-control and below-floor probes; unchanged product behavior | R958-4, retaining unaffected prior coverage | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| Tests | UNCLEAN - F2 | Adapter controls/CLI checks; extractor/tables; queued-record probe | R958-4 applied; no clean covering round | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| Docs | UNCLEAN - F2 | Maximum-cost claims; decision links; PR; packet indexes | R958-4 applied; no clean covering round | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |

**Manager duties and reproduction**

Publish the owner answer, obtain corrected extraction receipts and re-review F2, and carry both residues. Complete the independent-review bar and hosted/local-replica acceptance. Validate the actual then-current `dev` merge candidate with builder/native banks at the merge turn and link receipts. Supplied live `dev` is `e275d7950ef3385753e6a15d2e191ba855b171ed`; source-head evidence against `dev-soft-core` does not validate that candidate. Explicit merge authorization, containment and issue/project completion remain separate duties.

Run supplied scripts with `python3 -B <script> <source-root>`: `audit_evidence.py`, `probe_model.py`, `probe_extraction.py`, `run_checks.py`, `verify_checkout.py`. The extraction probe uses the exact copied script under `published/`; temporary fixtures stay under `scratch/`. Probes were disposable/in-memory. Final verification proves **1997 parent tracked blobs and 1377 blobs across five required submodules**, modes, exact indexes and gitlinks; the parent tree is unchanged. The optional `external` gitlink is preserved and uninitialized. No source fix, commit, push, GitHub write or merge occurred.

Only files listed in `MANIFEST.sha256` and this report are publication artifacts; `scratch/` is excluded.

R958-4 FINISHED
