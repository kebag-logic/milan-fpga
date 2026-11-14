[R838] NEGATIVE - exact head 9606b3a915de284c71d3063c2e8d94b097f18241

R838-6 applied Conformance, RTL, Robustness, Tests and Docs to the ten-commit delta from `7398ec0aeea468d92ff642a03a06e291a0cd58d1`. Two MINOR findings concern quantitative documentation and evidence. No functional regression was demonstrated. Focused implementation tests, all twelve new mutation controls, class controls and the 1x1/1if row gate pass. Three wording RESIDUE items are separate from the negative verdict.

Tree: `29bfeabee4a8a4e2b61dfa06c137b1588d3d7d8c`. This is an independent external source-head review, not merge-candidate validation or hardware acceptance.

## Authority and evidence

Reconstruction followed AGENTS/CONTRIBUTING, docs/README, the issue's frozen acceptance and public decisions, REQUIREMENTS product ownership, FR_NFR 3.4.1, AECP/interface and split-memory contracts, then diff/history and public execution evidence. The requested `66f713267f201d1a00d7f711e04b3a996d804dee..9606b3a9` inventory contains imported work; the assigned later-delta rule limits fresh review to the 17 changed files and affected dependencies. Untouched behavior retains prior assessment. Prior public finding excerpts were examined after the independent diff pass; complete earlier reports were opened only after my own preliminary verdict and five-lens ledger were written. No concurrent review report or private author material was used.

Principal authorities:

- [Round-11 assignment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878230332), [class-split amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878532871), [AECP check](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6876349104), [measurement](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878200592), and [every-table instruction](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6881287231).
- [1x1 merge scope and explicit #910 debt](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [contingent bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025), [last-notice amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874), [egress and whole-ms pace ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), and [direct-index ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6870437042).
- [Author packet at f3320c19](https://github.com/kebag-logic/milan-fpga/tree/f3320c19d0d394ee7dd4a835e81c7a390df3fedb/review-evidence/894-r1/author-r11), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6883768027), and the live PR body. Below, `author-r11/` paths refer to that archive.

All **425 published author-r11 files** match the outer manifest's published SHA-256 values. The archive commit is **unsigned**: content integrity was verified, but signer authentication was unavailable. The inner index has 424 rows; four refer to pre-redaction bytes, while the outer manifest provides verifiable published hashes. No manager source bank is claimed or inferred.

## Findings

### R838-6-F1 — MINOR — Tests, Docs — universal ROM-growth claim contradicts image totals

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:2479`: “The cut adds 220 B of rom to every image.” Related total at `:2379`; author-r11 `HANDOFF-r11.md:60`; author-r10 `receipts/images/every-image-head.txt` at the same archive.
- **Authority/evidence:** quantitative evidence must reconcile with its receipts. Previous fixture ROM 110,576 B to current published 110,800 B is **+224 B**. Previous 8x8/2if platform ROM 130,496 B to current published 130,704 B is **+208 B**. Neither is +220 B. `receipts/previous-image-sizes.txt` and `receipts/evidence-audit.json` retain the comparison. R838-3-F3 previously required this distinction between code growth and aligned ROM growth.
- **Impact:** the universal measured-growth assertion is false. No image-cap failure is demonstrated: the fixture allocation is 41.0 tiles and the platform retains 368 ROM bytes. Correct absolute totals do not make the universal delta true.
- **Required outcome:** reconcile per-image ROM growth against the previous head, or remove the unsupported universal delta and retain verified absolute totals. If 220 B names a section's growth, identify and verify that section separately from ROM.
- **Verification:** compare every claimed before/after size; the two examples above must reconcile. No functional change is required. This corrects a numeric evidence claim, so it is MINOR rather than wording-only RESIDUE.

### R838-6-F2 — MINOR — Tests, Docs — current R4 and validation-load summaries retain previous-head figures

- **Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:2495`, current tier summary “R4 12.85 ms”; PR #902 validation example, fetched body line 294, `load_grade.py --check # 0.513 and 0.509, PASS`. See `receipts/public-pr-excerpts.json`.
- **Authority/evidence:** the round-11 restatement and every-table instruction require this head's figures. My exact-head runs give **R4 12.93 ms** and loads **0.515 / 0.511**. The updated table at `:2346` already gives 12.93, and the first part of `:2495` gives the new loads. Receipts: `flip-1x1.log`, `load-check.log`.
- **Impact:** a current summary and advertised expected validation output contradict the executable result and adjacent current figures. Bounds still hold; this is not a demonstrated timing failure. R838-4-F1's current-summary defect has recurred after the model changed.
- **Required outcome:** change the current summary to R4 **12.93 ms** and the validation example to **0.515 and 0.511**, or explicitly identify retained numbers as historical rather than expected head results.
- **Verification:** compare those sites with exact-head flip/load commands. These corrections change figures, so they are not wording-only RESIDUE.

### R838-6-R1 — RESIDUE — Docs — new source comments contain prohibited round and lane identifiers

- **Artifacts:** `edit_rows.py:3,29`; `record_classes.py:4,5,72`; `load_grade.py:126,130`; `poll_grade.py:86,89`, under `tb/verilator/ctrl_service_budget/`.
- **Authority/evidence:** the owner's source-comment rule excludes review rounds and lane names. These added comments/docstrings name “round-11”, “round 11”, “round 4”, “round 9”, or “lane 894b”.
- **Impact:** wording only; executable statements and measurements need not change.
- **Exact outcome:** use “#894's class-split amendment” in `edit_rows.py:3`; “the one-row edit cut (#894)” at `:29`, `load_grade.py:126` and `poll_grade.py:86`; replace “round 9's head” with measured commit `5b264bf2` at `load_grade.py:130` and `poll_grade.py:89`; describe the missed `aecp-fanout` measurement directly at `record_classes.py:4-5`, without review chronology; replace “lane 894b's” at `:72` with “the single-interface follow-up's, #894”. Preserve numbers and behavior.
- **Verification:** scan added comments/docstrings and confirm no executable-token change. Unrelated existing #746 material is not reopened.

### R838-6-R2 — RESIDUE — Docs — retain R837-5-R1's historical-margin heading repair

- **Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:2493`, and equivalent “arm A's least margin at this head” at `:2484`.
- **Evidence/impact:** both passages identify numbers as round-30 measurements on `0fb66211`; “at this head” misdescribes provenance. Figures can remain unchanged.
- **Exact outcome:** replace “The margins at this head” at `:2493` with “The margins in round 30's measurements”; remove “at this head” at `:2484`. Preserve attribution and numbers.
- **Verification:** wording consistently describes the named historical measurement. R837-5-R1 remains open as residue.

### R838-6-R3 — RESIDUE — Docs — identity wording confuses source files with compiled output

- **Artifacts:** PR body line 240, “none changes a compiled firmware file”; REVIEW READY's paragraph on final-pass fixes.
- **Evidence:** `3e0ca737` changes declarations in `aecp_maps.c`; `6ec12ad7` changes `ctrl_loop.h`. Object/image hashes nevertheless remain identical. Carry rests on output identity, not absence of edits to compiled source files.
- **Impact:** wording only; the 332-file identity figures are correct.
- **Exact outcome:** use “none changes the compiled firmware output, as the image/object identity receipts show.”
- **Verification:** compare the source diff with unchanged output inventories; preserve the identity evidence.

## Implementation and robustness

`aecp_maps.c:178-313,353-505` preserves direct indexing and its shared-stride domain. The assertion covers actual slot-array storage. Geometry/range refusal precedes insertion; byte-sized links remain bounded by `AECP_MAP_PAGE < 256`. The new little-endian guard matches held-word construction.

Partial initialization clears every reachable slot and each inserted mapping's link, flags and count before use. A duplicate references an earlier initialized representative. The sentinel never accesses uncleared floor-only slots. Illegal geometry and earlier conflicts still terminate table formation; ordered validation preserves status and port-read precedence before mutation.

FOUND records the first and last matching rows. REMOVE leaves the prefix in place, consumes occurrences within that reach, and compacts the suffix without another lookup. Empty edits/reaches retain count and contents. Duplicate-removal multiplicity and order remain governed by the unchanged definition oracle. The coverage exclusion for `kept++ != k` is justified: a kept row within a successful nonempty REMOVE reach follows the first removed row, so it cannot remain in its original position.

The complete definition test is byte-identical to the previous head, SHA-256 `d8bdcce2a2010aaf8b603edc02e6f8f99955846fa9ad3fb3003c8d74fca37180`. My work-arm filter passes **16 tests**. All **twelve new plants** are independently caught by required test and diagnostic: reach start/end, suffix preservation, kept-row movement, row-word/copy coordinates, slot/flag/count/link initialization, and descriptor/page echo. Raw results are `map-plants.json`, `maps-baseline.log` and `plant-*.log`. Only disposable copies were mutated.

No HDL, reset, clock, CDC or pin changes occur in this delta. The architecture assessment covers changed map work and the loop's stated transmit figure. `CTRL_LOOP_TX_MS` is consumed by a compile-time assertion, not runtime scheduling.

## Timing, classes and table survey

Published span summaries reproduce **REMOVE 22,728** and **ADD 20,595** CPU cycles. REMOVE attribution sums 2,863 commits, 8,200 short-stall cycles, 10,245 fetch-stall cycles and 1,420 data-stall cycles to 22,728. REMOVE still exceeds 235 us, so the amendment's class split applies. Output-map REMOVE is **24,360 cycles**, giving **260 us**; the 8x8/2if edit is **30,563**, giving **325 us**. I inspected summaries and independently checked arithmetic; I did not regenerate CPU traces.

The surcharge counts at most `min(k, ceil((w+1)/P))` edits among a row's k AECP records. Unpaced windows charge all k. Independent boundaries cover both points and paces 0, 1, 8 and 13 on the solver's documented hundredth-ms grid. Making ordinary edit costs extreme leaves both LONG_ROWS results unchanged, confirming the surcharge does not leak into R4L/txL's separate accounting.

`record_classes.py` holds formal arms and answering-ports edits to their class, retains the explicitly reported SET_CONFIGURATION exception, and refuses a missing `aecp-fanout` arm-A group. All six controls pass. The tier self-test also catches its separate unpaced-undercharge plant.

The published survey covers `load_grade`'s two columns, `poll_grade.STATED_US`, `whole_grade`/loop pass costs, `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, LONG_NOTICE_US and LONG_RECORD_US at both points. `evidence-audit.json` recomputes every parsed row's rounding/verdict and records exceptions. Important comparisons:

| Cost | Measured cycles | Rule, us | Stated, us |
|---|---:|---:|---:|
| 1x1 TICK | 4,612 | 50 | 50 |
| 1x1 ACMP owed frame | 4,890 | 55 | 55 |
| 1x1 polls' base | 18,843 | 200 | 205 |
| 8x8 events' fixed part | 2,859 | 35 | 35 |
| 8x8 ACMP owed frame | 6,193 | 70 | 70 |
| 1x1 long record | 86,978 | 915 | 975 |
| 8x8 long record | 145,770 | 1,535 | 1,650 |
| 1x1 long notice | 34,280 | 360 | 365 |
| 8x8 long notice | 61,637 | 650 | 655 |

Held ordinary AECP maxima are 21,908 cycles at 1x1, 235 us by the rule, and 23,715 at 8x8, 250 us against 265. Broad-survey long-notice/edit comparisons against ordinary costs are reconciled by their class tables. The 8x8 build of one remains **146,376 cycles, 1,540 us by the rule against 1,215**, expressly refuted under [#910](https://github.com/kebag-logic/milan-fpga/issues/910) and ruling 6867393730(c). It is neither a passing measurement nor a new finding in this scope. Zero-observation survey entries are not fresh measurement proof.

Own exact-head 1x1/1if results:

| Row | ms | Bound, ms |
|---|---:|---:|
| R4 | 12.93 | 20 |
| R4L | 188.41 | 238 |
| ACMP / ADP / MAAP | 28.64 / 27.01 / 27.13 | 30 each |
| First / last queued notice | 14.56 / 127.22 | 20 / 130 |
| R5 / R6 | 73.39 / 69.24 | 90 each |
| tx / txL | 33.01 / 48.23 | 49 each |

`CTRL_LOOP_TX_MS=34` covers tx rounded up to whole milliseconds. Pace remains **8 ms**. Design search chooses the built **900 us** slice. Loads are **0.515 / 0.511**, below 0.70. Published join-summary extrema are **186.492–190.044 ms**, within 181–239; this aggregation includes the separately identified planted leg and is not an independent-unplanted interval count. Full arm A alone reports 188.002–190.022 ms, 96 groups, zero refusals, seven known held-egress budget misses and zero of 139,557 passes over the share. These are simulation receipts, not wire measurements.

The independently run 8x8/2if gate fails as expected for the reported point: R4 42.62, last notice 665.47, txL 459.40 ms. No passing 8x8 claim is inferred.

## Execution evidence and identity carry

Own focused results: flip self-test **585/585**, tier self-test **1,032/1,032**, class self-test **6/6**, map baseline **16 tests**, and new plants **12/12**; all exit zero. The 1x1 and load gates pass; 8x8 returns expected one. Scripts and raw logs are in MANIFEST.sha256.

Published inventories have identical paths/hashes for **332 files: 8 ELFs, 8 binaries and 316 objects** across `9fda93a1`, `3e0ca737` and `6ec12ad7`. The MAP_FLOOR=264 control differs in **24**. I compared the inventories independently. Between `bc971054` and `9fda93a1`, only model/documentation files change, leaving measured firmware inputs unchanged. The later declaration split and assertion-only constant change are covered by object/image identity. From `6ec12ad7` to this head, only documentation and graders/model tables change. This supports carrying compiled execution while rerunning changed readers; it does not imply unchanged model or documentation.

Published local workflow receipts show 139 executed steps and 226 NOT RUN entries with reasons at each broad pass. At `9fda93a1`, idiom and coverage failed; at `6ec12ad7`, coverage remained failed. The later `2d579e89` firmware/docs receipt has 67 zero exits, including repaired coverage; exact-head docs has 61 zero exits. Four sweep command receipts at `9fda93a1` end rc 0. The author's complete AECP campaign reports **286/286** at `6ec12ad7`; source/tests remain unchanged afterward. I checked available execution-status/digest receipts and reran the twelve new controls, not all 286. Early `plants/rows.txt` contains exploratory escapes followed by reruns and is not treated as the final full-campaign verdict.

Whole workflow logs, target traces and binaries are not all published; several are represented by hashes/summaries. I verified available integrity and spot-checked claims, without claiming inspection of unavailable raw bytes. No prohibited full bank was rerun.

## Prior findings: resolved or retained

The following uses [R838-5](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6874731724) and [R837-5](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6874821615) to enumerate earlier findings, then current artifacts/delta to assess their causes.

| Earlier IDs | Disposition at this head and cause-level artifact |
|---|---|
| R837-4-1 | Actual-array assertion against MAP_DOMAIN and separate floor retained in `aecp_maps.c:158-196`; compile plant unchanged. New partial clearing covers the reachable domain and passes independent controls. |
| R838-4-F1 | Current table updated, but summary regressed at `SPLIT_CONTROL_MEMORY.md:2495`; retained as F2. |
| R838-4-F2 | Correct broad map filter retained; current work-arm selection executes 16 tests including added echo/clearing cases. |
| R838-3-F1 / R837-3-1 / R838-2-F2 | Collision/quadratic causes remain resolved by direct indexing, early range/geometry refusal and bounded linkage. Definition/work tests pass through this cut. |
| R838-3-F2 / R837-3-2 / R838-2-F3 / R837-2-3 | Corrected 49/238 bounds, 181–239 join gate, 130 last-notice bound, 0.9 ms slice and decision references retained at prior sites. New summary mismatch is F2. |
| R838-3-F3 | Historical +184/+176 aligned-ROM reconciliation remains. New universal-growth claim repeats the evidence problem as F1. |
| R837-2-1 / R837-2-2 | Egress and whole-ms pace fixes retained in `ctrl_loop.h`, `paced_rows.py`, `join_grade.py`; boundary/model checks pass. |
| R838-2-F1 | Horizon-free released/empty/late/absent/unresolved resolver and join controls unchanged; new intervals fit corrected bounds. |
| R838-1 F1 / R837-1-1 | All tier-1 rows and 552-byte storage retained. R4L/txL retain largest-command charges; surcharge isolation checked. |
| R838-1 F2 / R837-1-2 | Ruled MRP budget, compile assertion and every-source tx/txL proof retained and recomputed. |
| R838-1 F3/F4 | Longer-notice-after-drain and ordinary-round-clear tests/plants unchanged in `test_aecp.cpp`, `test_port_loop.cpp`, `aecp_owed_mutants.py`, `loop_step_mutants.py`; no related runtime change. |
| R838-1 F5 / R837-1-3 | Corrected MAILBOX_SPLIT 0.9 ms slice retained. |
| R838-1 F6/F7 / R837-1-5 | Rotating order and conditional Domain/VLAN claim retained; licensing, resume/reset and gap-test code unchanged. |
| R837-1-4 / R838-1 S5 | Scope resolution retained: 8x8 reported, #910 explicitly refuted, no passing flip claimed. |
| R838-1 RS1 / R837-1-6; R838-2-R1 / R837-2-4; R837-4-R1 | Original source-comment fixes retained; new prohibited identifiers are R1. |
| R838-2-R2 / R837-2-5; R838-3-R1 / R837-3-R1; R837-4-R2; R838-4-R1 | Historical receipt/head/count attribution and original wording repairs retained. No planted interval count is promoted to a new unplanted count. |
| R837-5-R1 | Still open as wording residue R2. |
| R838-4-S10 | Earlier share-maximum attribution correction retained; current pass evidence separately reported above. |

## Optional suggestions consolidated

Every item below is SUGGESTION; none creates a requirement or dirties coverage. Artifacts identify the evidence; the last column states outcome and verification.

| ID / all lenses / artifact | Evidence and impact | Optional outcome and verification |
|---|---|---|
| R838-5-S1; Docs; AECP README owed ordering | Accepted later-response/earlier-notice order can expose an older cached value. | Explain with two controllers editing one field; compare response/notice order. |
| R838-5-S2; RTL; `aecp.c` counter reset | Prior redundant defensive reset unchanged. | Explain invariant, or remove only with queue/retry proof. |
| R838-5-S3 / R837-1-8; Tests; `aecp_owed_notice_steps.py` | Offline scenario model remains; native tests supply execution evidence. | Drive compiled behavior and require a behavioral plant to fail without anchor edits. |
| R838-5-S4; Tests; measurement inventories | Full-arm survey improves coverage; sustained pressure and complete sample counts remain useful. | Publish counts/maxima and longer expiry pressure; reconcile spans and padding. |
| R838-5-S5 / R837-1-7; Tests; `rows_tiers.least_margin` | Unsolved -1 can rank above solved scores below -1; passing choice unaffected. | Rank unsolved last before failed searches matter; add mixed-order control. |
| R838-5-S6; Tests; ACMP decline bound | Conservative bound unchanged. | Tighten only with source-derived proof and mutation control. |
| R838-5-S7 / R837-5-S1; Docs; author INDEX | Four of 424 inner rows differ after redaction; outer manifest verifies all 425 files. | Generate index after redaction or name outer published hashes as authoritative; rehash bytes. |
| R838-5-S8; Tests; `mrpdu_grade.py:84` | Callback late-classification and owed-centisecond origins remain distinct. | Explain/align origins and test delayed callback. |
| R838-5-S9; Tests, Docs; H-81N | Resolved for this packet: `final/legs/H-81N.txt` identifies the 40-notice/model-size RuntimeError, not a measured miss. | No further action for the requested diagnostic distinction. |
| R838-5-S11 / R837-4-S1; Tests; `place()` first-coordinate guard | Prior guard-removal plant survived under product admission; guard unchanged. | Add matching descriptor/first-coordinate edge case and show plant failure. |
| R838-5-S12; Docs; floor discussion | Placement sensitivity remains; new attribution improves current explanation. | Explain remaining margin assumptions against measured counterfactual. |
| R838-5-S13; Robustness, Docs; format/domain contract | Safety depends on admitted output formats and fixed cluster widths. | State precondition; widen domain when adaptation changes it; check generated keys. |
| R838-5-S14; Robustness, Docs; `struct edit` | Wide-geometry table size is not whole-call-chain stack proof. | Measure target peak call-chain use before extending supported images. |
| R838-5-S15; Tests, Docs; historical item-2 provenance | Current carry has explicit heads/inventories; older subset attribution remains optional context. | Retain run heads/source-identity spans beside reused historical probes. |
| R837-5-S2; Tests; undersized-table plant | Wide 544-slot-domain refusal is shown by prior probes, not a permanent wide plant. | Add floor-only plant at 16x32 and require assertion words. |

## Reviewer-owned completion ledger

This covers the delta and affected dependencies at the exact head. Open MINOR findings are not banked clean; residue/suggestions do not dirty a lens.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Public amendments; FR_NFR 3.4.1; `aecp_maps.c:353-505`; class split, table survey, own flip/load/pace results | R838-6 | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| RTL | CLEAN | `aecp_maps.c:158-313,424-505`; `ctrl_loop.h:360-366`; no HDL/pin delta; identity inventories and later input diff | R838-6 | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| Robustness | CLEAN | Refusal precedence, empty/duplicate/reach cases, stale-table test, 12 caught plants; pace boundaries and LONG_ROWS isolation | R838-6 | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| Tests | UNCLEAN: F1, F2 | Own map/model/class receipts pass; mutation/class graders and workflow receipts; image-growth and expected-output evidence disagree as specified | R838-6 | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| Docs | UNCLEAN: F1, F2 | `SPLIT_CONTROL_MEMORY.md:2346,2379,2468-2495`; FR_NFR:383; AECP/SRP/service READMEs; PR output; prior dispositions | R838-6 | 9606b3a915de284c71d3063c2e8d94b097f18241 |

## Limits, integrity and pending duties

- SET_CONFIGURATION is explicitly reported: 33,724 cycles / 355 us at 1x1, and 78,332 / 825 us at 8x8. The PR identifies the pending owner decision. Per assignment it is not a new finding and is not silently covered by ordinary costs.
- Source validation is author-published evidence plus focused probes. No manager source bank exists at this head. Local executed steps are distinguished from NOT RUN entries; hosted CI does not execute on these split PRs. Hosted/act acceptance belongs to the manager.
- Physical calibration was NOT RUN. Field skips and simulated joins are not hardware proof. S12b still owes wire capture and physical acceptance. #908 original-bound restoration, #909 placement sensitivity, 8x8/1if follow-up, and #910/#872 remain pending under public decisions.
- No source fixes, commits, pushes, merges, GitHub writes, author contact, sub-agents, privilege, shared installs, hardware, Docker/act or prohibited full banks were performed. Pinned simulator identity was checked, but no new simulation build used it. Focused map compilation used at most 16 jobs; independent model checks ran concurrently in a foreground-supervised driver.
- `checkout-integrity.json` verifies all **1,621 parent tracked blobs**, filesystem modes, exact stage-zero index and absence of hidden index flags. All five populated submodules match gitlinks, bytes, modes and indexes; no untracked files remain. Unpopulated `external` retains its exact tree/index pin. Disposable probes are only under packet `scratch/`.
- Manager duties: fixes/re-review for F1/F2; carry R1–R3 to residue; obtain both independent current-head verdicts; ensure no round is in flight; validate the refreshed **current-dev merge candidate**, including builder/native banks, before an explicitly authorized merge. Source base is `66f713267f201d1a00d7f711e04b3a996d804dee`; supplied live dev is `b7d692952305e4e0e132abb8f99c339eeb17a873`, subject to refresh. No candidate was built or validated here. Post-merge containment and issue/project completion remain required.
- Publish REPORT.md and only MANIFEST.sha256 paths. Scratch is excluded. Portable scripts and focused raw receipts are included; published author evidence is linked rather than represented as newly executed work.

R838-6 FINISHED
