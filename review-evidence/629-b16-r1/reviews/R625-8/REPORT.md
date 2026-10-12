[R625] NEGATIVE - exact head b522bb923fa59581478460b61633bce2cb90ac1d

Round R625-8, external independent review of issue #629 / PR #725. Tree: `66bd4852a98ca1065549515aa3c677d2fe482132`.

All five lenses were applied. One MINOR remains: the acceptance contract requires earlier controls to retain their outcomes, while two diagnostic expectations changed and the requested manager decision is absent. This is an unresolved acceptance conflict, not a reproduced false pass, incorrect bench measurement or DUT defect. The changes are technically consistent with reading visible parser output; I recommend explicitly accepting the two changed expectations. I cannot silently replace the frozen acceptance condition.

The complete `c20c85bd..b522bb92` diff and eleven commits change only the findings page and its index. The measured image is dev `5603c353`, distinct from this documentation head. Reconstruction used the repository contract and documentation map, issue and public scope decisions, linked requirements/interfaces, diff/history, then public executable evidence. Earlier public findings were reconciled after the independent diff pass. No current-round peer report or private lane material supplied this verdict.

Here, **findings** means `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`; **index** means `docs/findings/README.md`; **packet** means `author-r8/` in the [pinned public evidence](https://github.com/kebag-logic/milan-fpga/tree/b0134c639a35a731787dd62586fca6c4500842c8/review-evidence/629-b16-r1). Reviewer receipts and scripts are relative to this report.

**R625-8-F1 - MINOR - Conformance, Tests, Docs**

**Artifact:** findings:4192 and :4202; PR #725 body, Round 8 item 4; packet `tools/r4_check_controls.py` through `tools/r8_check_controls.py`; `receipts/control-summary.json` and `receipts/expectation-decision.json`.

**Authority/evidence:** The [round-8 assignment, item 4](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6130721355) requires earlier controls to retain their outcomes. AGENTS.md sections 2 and 4 require a public decision when scope and requirements conflict, and freeze active acceptance criteria. The [round-8 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132021882), page and PR body expressly request a manager decision on two changed expectations. None of the retrieved issue or PR scope comments records that decision.

Independent execution of the unchanged runners reproduces:

| Runner | PASS / total | Outstanding expectation |
|---|---|---|
| Round 3 | 5 / 5 | None |
| Round 4 | 7 / 8 | Link-label classification |
| Round 5 | 21 / 22 | Same inherited classification |
| Round 6 | 38 / 39 | Same inherited classification |
| Round 7 | 48 / 50 | Link-label classification and comment inside a code span |
| Round 8 | 73 / 73 | Both expectations changed in this runner |

The link-label control expects the `37` in `in [37](#b16c-attribution) blocks` to be uncovered but not classified as a measurement. The parser correctly presents `37 blocks`, so it is now classified as a measurement. The other control expects literal `CLOCK_DOMAIN 7<!-- -->ppm` inside a code span to produce MARKUP. The parser presents visible code; the checker instead reports 7 UNCOVERED. Both altered pages still exit 1 and identify the number at the correct line. This review does not recommend restoring the old interpretations of visible text.

**Impact:** The explicit earlier-control acceptance condition is unmet. The new runner's 73/73 cannot substitute for approval of the changed condition. This changes executable test expectations and the acceptance claim, so it is not wording-only RESIDUE. The author disclosed the conflict correctly; disclosure does not settle it.

**Required outcome:** Record a maintainer/manager decision explicitly accepting these two diagnostic changes under the parser contract, identifying the frozen expectations they supersede. Alternatively, resolve the conflict against a clarified contract. Preserve rejection, source-line diagnostics and receipts for both altered pages. Do not report the unchanged historical runners as wholly green.

**Verification:** Re-evaluate `receipts/controls-r4.json` through `controls-r8.json` against that decision and the published rule. Existing receipts already prove both mutations rejected. A decision accepting exactly these expectations can resolve this finding without a source or bench change; a changed head requires review of affected artifacts. No other new MINOR, MAJOR, BLOCKER or RESIDUE is filed.

**Independent lens results**

- **Conformance:** Issue #629's bench acceptance and B16/B16b/B16c rulings were compared with findings:2287, :2633, :2993, :3087, :3198 and :3320, `FR_NFR.md:252` and :253, and the media-clock design's bench row. All four B6 terms are stated, the timed ratio is NOT RUN, and B0 is not claimed as the missing INTERNAL mismatch control. Following cases use the authorized peer-INTERNAL exception and restore it. F1 is the only open finding under this lens.
- **RTL:** PASS - full two-file diff; `docs/design/TIME_SYNC.md:137`; `docs/reference/REGISTER_MAP.md:1870` and :2139; packet `r2/*-poll-trace.tsv`. The change touches no implementation, interface, configuration, generated hardware artifact or gitlink. Poll decoding agrees with documented servo states, signed trim and slip counters. No new RTL defect was found within this findings-only scope; this is not implementation-wide revalidation.
- **Robustness:** PASS - packet `tools/check_b16_figures.py:2618` through :2806; 73 current controls; 13 historical probe scripts; `probe_constructs.py` and `receipts/own-constructs.json`. The pinned parser supplies nodes and source positions, both documents use the same reader, and disallowed constructs fail with named locations. The handwritten comment/markup recognizers are gone from the reading path. The exact generator marker passes; padding and extra comments fail. Additional code/emphasis/link splits, character references, line breaks, tabs and unfamiliar-unit probes reject and write receipts without checker tracebacks.
- **Tests:** All 1,867 figure rows match, accounting for 14,442 digits with zero uncovered digits and no refused construct on the unchanged page. Output TSVs are byte-equal to the published ones. Regenerating the checker gives published SHA-256 `2eb5a24e427015d39154d28f778693f1170cf513e3e3d34f2cac308f2adc0284`. F1 retains the historical control conflict; these runners are not all green.
- **Docs:** Findings:2608 maps the evidence branch, commits, round directories and manifest; :3426 supplies raw-hash-bound reductions and extraction commands; :4192 discloses changed expectations. Index:15 and the PR body distinguish observed overlap from inferred attribution. The corrected PR title is present. Focused documentation gates pass; reviewed additions use neutral peer/capture labels and contain no host paths. F1 leaves the acceptance decision unresolved.

`audit_receipts.py` independently recounts measurements and restoration without importing the author's figure expressions. `receipts/independent-audit.json` establishes:

- B16's second loopback capture contains two CONNECT_TX/PROBE_TX commands approximately 200 ms apart, with no response. This supports an unformed loopback, not a DUT failure.
- B0: 300 blocks, 169 at the floor, floor medians -123.98/-123.95 dB. Block 45 is at the floor, splitting runs 43-44 and 46-54. Of 131 degraded blocks, 23 fall within the whole blocks covered by both taps and 108 beyond. The page correctly places recording approximately two seconds after capture launch, at 06:38:05.2, 26 seconds after binding.
- Positive-control counts exclude two pre-playback blocks and the playback-start block: 11/13 wholly playing blocks for `pts2`, and 303/303 for B0, B-CRF and B-AAF, on both tones.
- Poll traces yield LOCKED brackets 2.585-3.161 and 6.602-7.180 seconds at displayed precision, using the prior poll's start and first LOCKED poll's end. Both cases have 596 LOCKED window polls, trim extrema -6.125/-6.000 ppm and no slip-counter transition after first LOCKED. Six and seven transitions respectively precede lock. Raw-hash bindings and register interpretation agree.
- All eight clock-source sets succeed and read back correctly. Both cases restore DUT INTERNAL and peer CRF. All nine run-final records independently equal their corresponding as-found formats, clocks, bindings and maps. Each lane census has 45 reads, 44 equal; only the DUT's live AVB information changes. Counter marks are correctly described as 20 seconds after selection, about six seconds before the window.
- Twelve neutral source-read reductions bind to raw hashes. Comparisons are limited to the common 2,262, 1,255, 618 and 668 entries. Monitoring-mix message differences are distinguished from settings changed outside the lane. Source routing and clock changes are attributed outside the lane, not to DUT behavior.
- All 771 author-r8 files match the publication manifest; all 98 current packet-file hash rows match their files. The historical location check reproduces rounds 1-7, including 93 round-7 hash rows and its 706 manifest-listed files. See `receipts/published-location.json`.

**Executed checks**

`run_review.py` ran with four simultaneous jobs under a disposable environment installed from `tools/markdown/requirements.txt` with required hashes. It joins all work before exiting. `receipts/campaign.json` records commands/statuses; every command has its own log and status file.

| Check | Observed result |
|---|---|
| Unchanged figure check | Exit 0; 1,867/1,867 rows; output byte-equal |
| Current controls | 73/73 PASS |
| Published additional forms | 138/138 expectations met: 108 rejected, 30 stated passes |
| R625-3 quote/link probe | 7/7 detected |
| R624-4 / R625-4 probes | Unchanged: 8/8 and 12/12 detected |
| R624-5 row3200 and later denominator probe | Each mutation names its case and mismatches the affected numerator or denominator; the unaltered row correctly stays OK |
| R624-5 spelling probe | Mandated unit-word and direct-follower defects detected; optional documented limits retained |
| R625-5 comment probe | Statuses 0, 1, 1 |
| R625-6 rendered-comment probe | Statuses 0, 1, 1, 1, 1, 1; its old final assertion exits 1 after the fixes |
| R625-6 followers / R624-6 escapes | Rejection behavior and documented limits retained; invisible reference-definition form now passes under the parser rule |
| R624-7 Markdown probe | No escaping forms; every image form refused at its line |
| R624-7 invisible characters | 10/10 rejected |
| R625-7 markup probe | 24 altered cases rejected; unchanged case passes; four index markup cases name README.md:15, write both receipts, no traceback |
| Independent construct probes | 23 refusals, two specified passes; receipts written without checker exceptions |
| Documentation checks | docs-check, style, Contents, paths, em-dash and diff checks pass |

The optional R624-6 forms `of-unit`, `and-unit`, `possessive-unit` and `list-item-7` retain their documented passing behavior; they are not newly fixed defects. The R625-6 traceback belongs to its old expected-status assertion, not the checker. All 13 rerun scripts were hash-checked against their original public review-script blobs, not merely author-packet copies.

**Prior public findings at this head**

These dispositions use current receipts and executions, not earlier verdicts as proof.

| Prior finding or item | Disposition |
|---|---|
| R624-1-F1; R625-1-F3 | RESOLVED: B0 medians, block ranges and recording start |
| R624-1-F2; R625-1-F4 | RESOLVED: four B6 terms; timed ratio NOT RUN |
| R625-1-F1 | RESOLVED: 23 observed versus 108 inferred blocks in page, index and body |
| R625-1-F2; R624-1-S2 | RESOLVED/TAKEN: public neutral reductions, extraction and raw-hash bindings |
| R624-1-R1/R2; R625-1-R1/R2 | RESOLVED: corrected title and exact counter-mark timing |
| R624-1-S1; R625-1-S1; R624-2-S2; R625-2-S1; R625-3-S1 | TAKEN: 44/45 actual census reads, independently recounted |
| R625-2-F1 | RESOLVED: exact replacement at findings:3244, including four point-(a) medians |
| R624-2-F1/F2 | RESOLVED: playing-block counts and state-read LOCKED brackets |
| R624-2-R1/R2/R3; R624-2-S1 | RESOLVED/TAKEN: common-entry limits, bounded pre-set attribution, missing-control antecedent and unanalysed status bit 4 |
| R624-3-F1; R624-5-F3 | RESOLVED: archive mappings through author-r7; author-r8 stated as subsequent publication |
| R625-3-F1; R624-4-F1; R625-4-F1 | Original escapes RESOLVED; diagnostic expectation conflict separately recorded as R625-8-F1 |
| R624-4-S1 | TAKEN: pointers reach subsequent rounds |
| R624-5-F1 | RESOLVED: each case's receipt; numerator and denominator mutations detect at line 3200 |
| R624-5-F2; R625-5-F1 | Original unit-word and multiline-comment escapes RESOLVED |
| R624-5-R1 | RESOLVED: required channel/step/round and issue-number wording on page and body |
| R624-5-S1; R624-6-S1 | TAKEN: closed-list and approximate-quantity limits stated |
| R624-6-S2 | Technical condition satisfied: the affected row fails under its own mutation |
| R625-6-F1 | RESOLVED: short comments and tags refused; literal code-span expectation awaits F1's decision |
| R624-7-F1 | RESOLVED: eight image forms refused; no hidden exclamation-mark escape |
| R625-7-F1 | RESOLVED: four index markup cases give named refusals and both receipts without exceptions |

No prior BLOCKER, MAJOR or MINOR is retained as an unfixed original defect. F1 is the current acceptance conflict.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - R625-8-F1 | Issue assignments; findings:3198, :3320, :4192; FR_NFR.md:252; control-summary.json | R625-8 applied; no clean covering round asserted | b522bb923fa59581478460b61633bce2cb90ac1d |
| RTL | CLEAN | Full diff; TIME_SYNC.md:137; REGISTER_MAP.md:1870, :2139; poll traces; checkout.json | R625-8 | b522bb923fa59581478460b61633bce2cb90ac1d |
| Robustness | CLEAN | check_b16_figures.py:2618; current controls; 13 unchanged probes; own-constructs.json | R625-8 | b522bb923fa59581478460b61633bce2cb90ac1d |
| Tests | UNCLEAN - R625-8-F1 | Figure TSVs; controls-r3 through controls-r8; independent-audit.json; campaign.json | R625-8 applied; no clean covering round asserted | b522bb923fa59581478460b61633bce2cb90ac1d |
| Docs | UNCLEAN - R625-8-F1 | Findings:2608, :3426, :4192; index:15; PR body; scope decisions; documentation logs | R625-8 applied; no clean covering round asserted | b522bb923fa59581478460b61633bce2cb90ac1d |

**Limits and pending manager duties**

This is a public-receipt review. Raw audio, wire captures and private source-state records were not accessed or re-acquired. Their hashes bind the reductions; this does not independently establish calibration or regenerate raw measurements. Physical calibration was NOT RUN, and field skips are not hardware proof. INTERNAL mismatch, timed-ratio measurements and #645 remain open; this findings PR does not discharge the parent issue.

The author's exact-head `gates/r8/results.json` records source-head checks. No manager source-bank evidence is claimed or inferred. No full parent, processor, timing, synthesis or builder banks, hardware action, hosted acceptance polling, local workflow replica, source fix, commit, push or GitHub write was performed. The manager owns hosted/local-replica acceptance and the final candidate against live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`; source-base `c20c85bd` evidence is not candidate evidence. Resolve F1 publicly, complete independent review acceptance, publish current-dev candidate receipts, obtain merge authorization and perform containment before completion.

`receipts/checkout.json` proves exact tracked bytes, executable modes and index entries: 1,291 parent files and 104, 562 and 214 files in initialized submodules. Required processor gitlinks `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and `2ad2f845dd583f8310075fa2380cb60a04fd091a` match checkout bytes and indexes. All five parent gitlinks match the tree. External and lwSRP remain uninitialized as found. The worktree is clean; mutations stayed in scratch copies, so tracked restoration was unnecessary.

Portable scripts: `run_review.py`, `probe_constructs.py`, `audit_receipts.py`, `verify_checkout.py`; usage is in their docstrings. The audit's generated-check prerequisite uses published `r8_figures_build.py`. The location receipt uses published `r8_evidence_receipt.py` with evidence commit `fa974c3f` and page commit `295ba9d7`. Only manifest-listed artifacts and this report are intended for publication; scratch is excluded.

R625-8 FINISHED
