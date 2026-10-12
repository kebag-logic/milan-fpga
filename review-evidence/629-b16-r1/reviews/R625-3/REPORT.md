[R625] NEGATIVE - exact head 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5

Round R625-3, external independent review of issue #629 / PR #725.
Tree: `dd6c3f3cb7bc5059aa9e976a9131a4e19212d103`.
Comparison: `c20c85bd..0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5`.

All five lenses were applied. The prior MINOR findings and wording residues are resolved. One new MINOR remains: the figures check accepts an unsupported measurement in the attribution summary when quoted or placed in link text. This affects Conformance, Robustness, Tests and Docs. RTL is CLEAN. No new DUT defect is alleged.

The current figures reproduce. The published checker exits 0 with 1,610 matching rows, 1,815 numeric tokens, 205 category tokens and zero uncovered tokens. Its two output files reproduce byte-for-byte. That proves the current rows agree with their receipts; the new finding concerns its claimed protection against additional unreceipted figures.

Scope and evidence were reconstructed in the requested order: operating rules, documentation map, [issue contract](https://github.com/kebag-logic/milan-fpga/issues/629), [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), [B16c exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), [round 2](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763) and [round 3](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508); linked repository authorities; complete diff/history; public receipts. Authorities include REQUIREMENTS.md section 8, FR-CLK-03/04, MEDIA_CLOCK_FOLLOWING.md's clause discussion and Bench contract, ARCHITECTURE.md's media ownership, and REGISTER_MAP.md's servo, meter and slip fields.

Evidence paths below refer to `author-r3/` in the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/b84584e4ccb069248909f0fdeb7f8b72a1c41ae4/review-evidence/629-b16-r1). All 525 author-manifest entries verify against the publication manifest. Seventeen files have declared publication redactions; their original and published hashes both reconcile. The independent verdict and ledger were written before opening earlier reviewers' reports. Only the four prior public findings comments were then reconciled; no current-round peer report or private author material was used.

**R625-3-F1 - MINOR - Conformance, Robustness, Tests, Docs**

Artifact: published `author-r3/tools/check_b16_figures.py:2128` and `:2158`; `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3501`; reproduced in its attribution-summary row at line 2975.

Authority/evidence: the round-3 assignment requires receipt-backed coverage of every summary and attribution figure. The findings state, “A figure added without a row fails the check.” The checker exempts whole Markdown links, including their visible labels, and every double-quoted phrase. Those are formatting categories, not proof that their contents are identifiers.

A disposable copy of line 2975 was tested three ways, without altering the checker or any receipt:

| Added sentence | Checker exit | Result |
|---|---|---|
| `The measured residual was 7.25 ppm.` | 1 | Correctly reports an uncovered figure |
| `The measured residual was "7.25 ppm".` | 0 | Unsupported measurement accepted as a quoted phrase |
| `The measured residual was [7.25 ppm](#b16c-attribution).` | 0 | Unsupported measurement accepted as a link |

Both accepted cases report 1,610 rows OK, 1,816 tokens, 206 category tokens and zero uncovered. The unchanged page passes. Four independent changes to existing summary/attribution figures are rejected. The comparison isolates the coverage exception as the cause. Reproduction: `scripts/probe_figure_coverage.py`; raw outputs: `receipts/probe-new_plain_figure.log`, `receipts/probe-new_quoted_figure.log`, `receipts/probe-new_linked_figure.log`; full results: `receipts/figure-coverage-probes.json`.

Impact: a measurement can enter an attribution summary without a receipt while the checker reports complete coverage. The existing five controls miss this accepted-input case. The current bench numbers remain supported, but the promised protection against this defect class is incomplete. This changes test behavior and an evidence claim, so it is not wording-only RESIDUE.

Required outcome: require receipt rows for measurement-bearing quoted text and link labels. Limit exemptions to demonstrable identifier content, preserving legitimate citations. Add controls for both reproduced forms. Merely weakening the stated coverage claim would not satisfy the round-3 requirement.

Verification: both unsupported-figure forms must exit nonzero and identify the missing figure; the unchanged page must still pass with receipt-backed coverage, and the five existing controls must remain green. Re-review the corrected published checker and corresponding documentation.

**R625-3-S1 - SUGGESTION - Docs; retained optional**

Artifacts: published `tools/census_cmp.py`, `restore/census-*.jsonl`, and the findings' census descriptions. Retains R624-1-S1 / R625-1-S1 / R624-2-S2 / R625-2-S1.

Authority/evidence: 46 entries include a header and 45 device reads. “45 of 46 entries equal” is correct under the comparator's definition. Impact: readers can mistake entries for reads. Optional outcome: use “44 of 45 reads equal” when excluding the header. Verification: remove only the `type=start` row and compare. This suggestion does not make any lens unclean.

**Prior findings, resolved or retained at this head**

Primary public comments: [R624-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428), [R625-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570), [R624-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119878041), [R625-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119899949). The public inventory has no formal reviews or inline review comments.

| Prior item and assigned lenses | Disposition and evidence at this head |
|---|---|
| R625-1-F1: Conformance, Tests, Docs | RESOLVED. Findings:2790,2804,3217; index:15; live PR body distinguish 131 degraded blocks at (c), 23 demonstrated inside the 34.1136-second overlap, and 108 attributed upstream by inference. Independently recomputed from blocks and both alignments. |
| R625-1-F2: Tests, Docs; R624-1-S2: Tests | RESOLVED. Findings:3362 onward publish neutral poll extrema, slip transitions with states, source meters/comparisons, raw hash bindings and extraction commands. Both 710-row traces were decoded independently; twelve source-read hash bindings checked. Raw source extraction remains unavailable and is not claimed. |
| R624-1-F1: Conformance, Docs; R625-1-F3: Conformance, Tests, Docs | RESOLVED. B0 floor medians are -123.98/-123.95 dB, block runs split at 45, and recording starts about 06:38:05.2, 26 seconds after binding, including the two-second playback lead. The B0 reduction reproduces byte-for-byte. |
| R624-1-F2: Conformance, Docs; R625-1-F4: Conformance, Tests, Docs | RESOLVED. Findings:3157-3169 state all four B6 terms for both following cases: three met, timed ratio NOT RUN, no replacement decision. Acceptance, limits, index and PR body retain this qualification. |
| R624-1-R1 / R625-1-R1: Docs | RESOLVED. The live PR title exactly matches the requested replacement, distinguishing B0 grading from following cases at the floor. |
| R624-1-R2 / R625-1-R2: Docs | RESOLVED. Findings:3004,3060,3134 identify the first counter mark 20 seconds after setting, about six seconds before recording; the header says before the window and near its end. |
| R625-2-F1: Conformance, Tests, Docs | RESOLVED. Findings:3206 uses the exact required replacement: “At (a), medians are -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block is -123.93 dB.” Checked against both tap summaries. |
| R624-2-F1: Robustness, Tests, Docs | RESOLVED. Findings:2708-2714,3121,3122 and attribution rows exclude silent blocks 0/1 and transition block 2. Counts reproduce as 303/303 wholly playing blocks for B0/B-CRF/B-AAF and 11/13 for pts2; both pts2 taps have 15 wholly playing floor blocks per tone. |
| R624-2-F2: Tests, Docs | RESOLVED. Findings:2972,2973,3136,3137,3140; index:15; PR body use 2.585-3.161 and 6.602-7.180 seconds. The lower endpoint is the start of the last ACQUIRE poll; the upper is the first LOCKED poll's end. The actual state read lies within each poll. |
| R624-2-R1: Docs | RESOLVED. Findings:2749 and 3217-3227 narrow the state claims to 1,255 common entries and the 618/668 common entries around B16c. |
| R624-2-R2: Docs | RESOLVED. Findings:3171-3178 describe pre-set slips as consistent with clock difference and, for the first step, a bind slip; receipts do not distinguish the causes. |
| R624-2-R3: Docs | RESOLVED. The live PR body says “Direction B's INTERNAL mismatch control did not run,” with the requested explanation. |
| R624-2-S1: Docs | RESOLVED. Findings:3303 records status bit 4, DRP config mismatch, as observed but not analysed. |
| Census suggestions listed under S1 above: Docs | RETAINED OPTIONAL. No false numerical claim under the existing entry-count definition. |

**Evidence by lens**

Conformance: the assignment's STOP/resume sequence is preserved. The public loopback decode shows two unanswered CONNECT_TX probes 200.0 ms apart, and both external outputs are zero. B16b stops before circular following. B16c uses the authorised exception only for the two following cases. Controller responses independently confirm all eight successful source sets and GET readbacks: peer INTERNAL, DUT CRF/AAF, DUT INTERNAL, peer CRF after unbinding. Listener formats are adapted or verified equal before binding. All nine run-final payloads match their as-found values. INTERNAL mismatch control and timed ratio remain NOT RUN; #629 stays open. Only F1 prevents clean coverage.

[R625] PASS RTL - complete `c20c85bd..0782c55f` diff; `docs/overview/ARCHITECTURE.md:72`; `docs/reference/REGISTER_MAP.md:1870`, `:2078`, `:2139`; both published raw-word traces. Five commits change only two findings documents. No RTL, firmware, executable source, generated image or gitlink changes. Source indices, state 4, signed trim at 1/16 ppm, stream rates at 512 units/ppm, and meter word `0x001e0007` agree with the interface authorities. Both windows decode to 596 LOCKED polls, static zero TDM slips, zero AAF history restarts and 30 ns maximum deviation where AAF is selected. This covers documentation's interface claims; it is no new implementation or hardware validation.

Robustness: unsuccessful loopback and the empty busy-capture B0 incident are explicitly ungraded. Positive-control silence and boundary blocks are excluded. The published eight dry-run outcomes and deadline receipt cover refusal, music busy, no lock, incorrect peer state, controller loss and teardown; they were inspected, not re-executed. Actual restore order, controller responses and all final states were checked. Both traces contain five pre-set IDLE slip steps, then one/two ACQUIRE steps and none after observed lock. F1 exposes a separate fail-open input case in the new figure checker.

Tests: independent arithmetic reproduces all six output grades, all alignment spans, positive-control block counts and B0's 23/108 attribution boundary. B-CRF/B-AAF each have 300/300 floor blocks, zero reported discontinuities, and -123.98/-123.97 dB median at (c). Direct sample comparisons cover only 34.2-34.3 seconds of each 300-second recording. Poll extrema, states, slip transitions and lock brackets reproduce from the public traces. Grading and alignment controls reproduce byte-for-byte. Four changed existing figures and one new plain figure are rejected; two formatted new figures escape, as F1 records.

Docs: examined both changed pages, the current PR title/body, published source gate receipts, hash citations, extraction procedures, privacy and attribution. Outside-lane routing/clock changes are attributed to the source path. B0's measured overlap and later inference remain separate in all three public summaries. Source-state claims now retain the partial-comparison limits. The reference peer and external capture are named by role; no new identifying host paths appear. F1 leaves the advertised figure-coverage guarantee unsupported. All focused documentation checks pass.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue/rulings; FR-CLK-03/04; findings:2975,3485-3515; B6 terms; clock responses and restore records | R625-3 applied; no clean coverage | 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5 |
| RTL | CLEAN | Complete two-file diff; architecture:72; register map:1870,2078,2139; both raw-word traces; required gitlinks | R625-3 | 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5 |
| Robustness | UNCLEAN: F1 | Checker input exceptions; silence/boundary blocks; failed-run receipts; dry-run results; nine restores and post-lock traces | R625-3 applied; no clean coverage | 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5 |
| Tests | UNCLEAN: F1 | Figure rows, point/grade/alignment receipts; independent arithmetic; five checker controls; seven independent probes | R625-3 applied; no clean coverage | 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5 |
| Docs | UNCLEAN: F1 | Findings:2281-3574; index:15; current PR title/body; extraction instructions; coverage claim and documentation checks | R625-3 applied; no clean coverage | 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5 |

**Executed checks and reproduction**

| Check | Result and receipt |
|---|---|
| Published figure checker | rc 0; 1,610/1,610 rows; outputs byte-equal; `receipts/figures-check.log`, `figures-rows.tsv`, `figures-coverage.tsv` |
| Published checker fault controls | 5/5 PASS, byte-equal; `receipts/figures-controls.json` |
| Alignment controls | 6/6 PASS, byte-equal; `receipts/alignment-controls.json` |
| Presence controls | 8/8 PASS, byte-equal; `receipts/presence-controls.json` |
| Synthetic grade controls | 20/20 PASS, byte-equal; `receipts/grade-controls.json` |
| Loop decoder control | PASS, byte-equal; `receipts/loop-controls.json` |
| B0 reduction | Byte-equal; `receipts/b0-recomputed.json` |
| Independent receipt audit | PASS; grades, overlap, floors, 1,420 poll rows, twelve source hashes, nine restores, eight controller set/readbacks, censuses and counters; `receipts/independent-audit.json` |
| Independent figure probes | Five rejected correctly; two escaped, proving F1; `receipts/figure-coverage-probes.json` |
| Documentation/whitespace checks | Seven final rc 0; `receipts/focused-results.json`, `focused-retry.json` and per-check logs/rc files |
| Exact tracked-byte verification | PASS before and after probes; `receipts/integrity-initial.json`, `integrity-final.json` |

The initial three renderer-dependent invocations exited 2 because the review driver resolved the environment interpreter's symlink. Keeping the environment launcher path fixed that review setup error; only those three checks were repeated. Original statuses remain in focused-results.json; final attempts are in focused-retry.json and the per-check logs. There was no source change.

Scripts accept repository, public-evidence and output locations. Obtain `author-r3/` and its parent `MANIFEST.json` from the pinned evidence commit. Run the published checker with the exact-head findings page, evidence root and two output TSV paths. Then run `scripts/run_focused.py REPO EVIDENCE REVIEW_PACKET MARKDOWN_PYTHON`, `scripts/audit_evidence.py EVIDENCE REVIEW_PACKET`, and `scripts/probe_figure_coverage.py REPO EVIDENCE REVIEW_PACKET`. The last command returns 1 at this head because the two probes escape. `scripts/verify_checkout.py REPO OUTPUT_JSON` proves tracked bytes, modes, indexes and required submodule pins. All disposable files remain under scratch; independent checks ran in a waited foreground process, at most eight children with numeric-library threads limited to one.

The full B16-start to B16c-end census has 45/46 equal entries, with only live propagation delay changed. DUT LOCKED/UNLOCKED moves 22/21 to 24/23, peer 6/5 to 8/7, and each DUT talker's MEDIA_RESET 0 to 4. These are reconciled public receipts, not fresh hardware measurements.

**Limits and pending manager duties**

The measured image is dev `5603c353`, distinct from this documentation head. No private raw audio/taps, full poll files, source reads or class map were accessed. Raw-inventory hashes bind citations; unavailable bytes were not rehashed. Public traces permit independent register decoding; source-role classification remains dependent on the published reduction. B16b's overwritten playback log is supported only by the expressly cited public operator record, not a retained raw log.

There is one 300-second run per following case. Sample equality is limited to the tap overlaps. The timed ratio, Direction B INTERNAL mismatch control and physical calibration were NOT RUN. Printed precision, field skips and desk controls are not calibrated hardware or release proof. #645 and the remaining #629 acceptance stay open. The declined census wording suggestion remains optional; no wording residue remains from the prior rounds.

The author's exact-head gate receipt has 14 successful entries, including two environment-version checks (`receipts/author-source-gates.json`). It is the published source-validation evidence. No manager source bank ran at this head, and none is claimed or inferred. Hosted checks were not polled in this round; hosted and local workflow acceptance remain with the manager. A skipped context is not an executed suite or physical proof.

No source fixes, commits, pushes, GitHub writes, hardware access, shared installs, privilege, full banks, simulator invocation or local workflow replica were performed. Final integrity verification covers 1,291 parent blobs and 880 required-submodule blobs, file modes and indexes, at the exact head/tree and pins.

The manager must publish this packet, have F1 corrected, obtain independent re-review of the affected lenses and both required positives, and ensure no review remains in flight. This verdict does not authorize merge. At the merge turn, the manager must validate the candidate combining the corrected lane from source base `c20c85bd` with then-current dev (provided tip `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`), run the required builder/native banks and link exact-candidate receipts. Source evidence here does not cover that future candidate. Hosted/local workflow acceptance, maintainer merge authorization and post-merge containment remain pending.

R625-3 FINISHED
