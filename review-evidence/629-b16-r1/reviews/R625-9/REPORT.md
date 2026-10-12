[R625] NEGATIVE - exact head cb5ff79f1f69117efba353484851eceb620e5c92

External independent review R625-9 of issue #629 / PR #725, B16, B16b and B16c, documents only. Tree: `6467d108ba0ddd10bf252fe0a241f90e090cefc3`; diff base: `c20c85bd`. All five lenses were applied. One open MINOR in the PR body leaves Docs UNCLEAN. No new defect was found in the bench findings or the figure checker. The earlier public findings are resolved at this head, subject to the expressly retained measurement limits below.

The independent diff review, verdict and ledger were written before reading earlier review findings. Reconciliation then used their public PR comments. This report does not approve a merge or claim completion of issue #629.

**R625-9-F1 — MINOR — Docs — PR #725 body, “B16: result”, line 29 in the saved snapshot: wrong origin for the first probe delay.**

Authority/evidence: the body says “99.6 ms after the bind command”. `author-r9/summary/loop2/acmp-peer-tap.json` records DISCONNECT_RX_COMMAND at 2.600600 s, CONNECT_RX_COMMAND at 2.600686 s, and the first CONNECT_TX_COMMAND at 2.700216 s. Therefore the delays are 99.616 ms after unbind and 99.530 ms after bind. Rounded to the body's precision, these are 99.6 ms and 99.5 ms respectively. The findings correctly define their origin as the controller's UNBIND_RX at `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2423`.

Impact: the public summary attaches a measured delay to the wrong event. It does not change the no-stream conclusion, but it is a measurement claim, so it is not wording-only RESIDUE.

Required outcome: replace “99.6 ms after the bind command” with “99.6 ms after the unbind command”, or retain the bind origin and use 99.5 ms. No source change is needed.

Verification: subtract the timestamps above and re-read the updated public body. This review independently performed the subtraction; see `receipts/pr-claim-snapshot.json` and `receipts/independent-evidence-audit.json`, `probe_timing`. The snapshot identifies the public URL, exact head and body's update time. This finding is confined to Docs: it concerns the PR summary's event reference, not a protocol threshold, a DUT behavior change, or a claim that the checker validates PR bodies.

**R625-9-R1 — RESIDUE — Docs — PR #725 body, Round 9 item 2, snapshot line 422: stale source-line locator.**

Authority/evidence: this item names the appended footnote definition at line 4424. Both the published `author-r9/r9/r624-7-escapes-probe-rerun.json` and this review's unchanged rerun name it at line 4426, with the reference still refused at line 3011. See `receipts/r624-7-escapes-probe-rerun.json` and `receipts/pr-claim-snapshot.json`.

Impact: a reader is directed two lines early in a disposable probe copy. This is solely a locator in prose; it changes no measurement, figure value, test outcome, code, generated artifact, conformance claim or privacy rule.

Exact fix: in that PR-body bullet, replace “line 4424 instead of 4274” with “line 4426 instead of 4274”. Verification: compare the pointer with the existing `footnote_ref_and` result. This residue does not affect the verdict or coverage; the manager can carry it to the residue checklist.

**Authorities and artifacts examined.**

Reconstruction followed AGENTS.md / CONTRIBUTING.md, `docs/README.md`, the issue's frozen acceptance and public manager decisions, requirements and interface authorities, the complete two-file diff and its history, then executable evidence. The scope authorities include [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), [B16c ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), [round 9 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132350672), and [the diagnostic-expectation decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481). The last decision is recorded both where earlier runner outcomes appear and in the round-9 findings.

Technical authorities examined include REQUIREMENTS.md section 8, `docs/design/MEDIA_CLOCK_FOLLOWING.md`'s baseline, bench acceptance and limits, and `docs/reference/REGISTER_MAP.md:1870`, `:1871`, `:2076` and `:2139` for slip counters, AAF status and signed servo/state interpretation. This is a review of documented observations against those authorities, not fresh protocol certification.

The evidence used is the [public snapshot at 4ab00ba575cf1ea2ab17c232886637524c9876cb](https://github.com/kebag-logic/milan-fpga/tree/4ab00ba575cf1ea2ab17c232886637524c9876cb/review-evidence/629-b16-r1). Paths prefixed `author-r9/` below are relative to that snapshot's packet. The historical location paragraph was independently checked against its pinned evidence commit `b0134c639a35a731787dd62586fca6c4500842c8`: branch, round directories, source/evidence pins, manifest and all 98 listed hash rows matched. Independently hashing 5,468 published author evidence files against the supplied publication manifest found no mismatch. No prior reviewer report was used to form the independent verdict.

[R625] PASS Conformance — `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2287`, `:2411`, `:2797`, `:3080`, `:3165`, `:3331`; public scope rulings; `receipts/independent-evidence-audit.json` — the findings distinguish observed behavior, inference and unrun acceptance terms against the frozen bench scope.

B16's loopback did not form: two outgoing probes, no response, no peer talker PDUs and zero output. The finding places the failure before audio transport and does not claim a DUT defect. B16b's four points and their finite overlap are kept separate. B0's two floor medians recompute to -123.98/-123.95 dB; 169 of 300 blocks are at the floor and 131 are degraded, including 23 wholly within the taps' overlap and 108 beyond it. The interrupted run boundary and recording start match their receipt rows. Block 45 is not in the degraded run. Sample equality inside the overlap supports direct upstream attribution there; extension beyond it is expressly inference in the findings, index and PR summary.

B-CRF and B-AAF each have 300 of 300 tone blocks at the floor, no detected discontinuity, and 596 of 596 complete window polls reading LOCKED. Their output floor medians recompute to -123.98/-123.97 dB. The corrected upstream-attribution values at point (a), including R625-2-F1's exact replacement, match each case's own summary. Positive-control counts exclude the two pre-playback blocks and the partial start block: 11/13 for `pts2`, 303/303 for each longer capture. All four B6 terms are stated, with the timed ratio NOT RUN. The INTERNAL mismatch control is NOT RUN. Neither is silently substituted by the observed counted ratio.

[R625] PASS RTL — complete `c20c85bd..cb5ff79f1f69117efba353484851eceb620e5c92` diff; `docs/reference/REGISTER_MAP.md:1870`, `:1871`, `:2139`; `author-r9/r2/*-poll-trace.tsv`; `receipts/checkout-integrity.json` — the two changed Markdown files introduce no RTL, reset, CDC, width, source-selection or interface change, and their hardware-state interpretations agree with the register authority.

The LOCKED brackets use the start of the last ACQUIRE poll and end of the first LOCKED poll: 2.585–3.161 s for B-CRF and 6.602–7.180 s for B-AAF. Signed trim decodes to -6.125 through -6.000 ppm. The six B-CRF slip transitions are five in IDLE and one in ACQUIRE; the seven B-AAF transitions are five in IDLE and two in ACQUIRE. None occurs while LOCKED; `SLIP_TDM` stays zero. Status bit 4's recorded mismatch and configuration limitations are disclosed, not converted into a new hardware proof. The first counter mark is correctly stated as 20 s after the set and about 6 s before the window.

[R625] PASS Robustness — `author-r9/tools/run_b16c.py:706`, run events, `restore/census-start.jsonl`, `restore/census-endc.jsonl`, current parser/allowlist implementation and `receipts/independent-probes.json` — restoration evidence and adverse-input behavior were independently examined.

All eight B16c clock-source sets have SUCCESS and equal readback, including both restores. All nine recorded runs finish equal to their initial scoped state. An independent comparison across the full lane, without dropping repeated census records, finds 44 of 45 returned records equal after removing only exchange timing/sequence fields. The sole difference is the GET_AVB_INFO timing payload; all binding, mapping, format and clock-source records match and all reads succeed. The teardown attempts restore stages independently and handles a terminated controller. Published dry-run failure evidence was inspected; no hardware routine was executed in this review.

The closed Markdown allowlist is applied to actual source extents, including HTML block literals, multi-line image/link extents and struck text. Misplaced paragraph positions are refused rather than used to skip covered text. The original raw-tag and comment normalizers are superseded by the pinned parser. Own probes covered multi-line code and markup crossing the introduction boundary, entities, invisible separators, unit spellings, image constructs and a permitted hard break. All 38 met their stated outcome: 36 negatives refused/detected at the relevant line with receipts, two positives passed.

[R625] PASS Tests — `author-r9/tools/check_b16_figures.py`, its row specification, round-3 through round-9 controls, unchanged review probes, `tools/markdown/requirements.txt`, and this packet's raw receipts — baseline checks, independent arithmetic and fault probes substantiate the claimed check behavior.

The checker ran in a disposable environment installed from the repository's hash-locked Markdown requirements. Baseline: 1,909/1,909 rows OK; 14,956 digit characters accounted for, 12,531 by rows and 2,425 by keyword-bound categories; zero uncovered digits and zero forbidden constructs. These counts cover the specified findings and README suffix, not the PR body. Claims inside quotations and link labels are read as visible text. Images and other constructs off the allowlist are refused at their covered source line. The unit-spelling and identifier controls detect the mandated joined, spaced, non-breaking-space, signed, leading-point, exponent, hyphen and unlisted-unit forms.

The round-9 runner passes 97/97 controls, including all 73 controls from round 8. The parser extent audit passes 37/37. R624-8's unchanged `intro_pre_from_line_above_with_figure` is refused at `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18`, named `html_block`. R625-7's four index cases are refused at README line 15 with both receipts and no traceback. All 14 supplied unchanged review-probe scripts were rerun: the round-8 set of 13 plus R624-8's boundary probe. The earlier comment, digit-coverage, escape-form and per-case receipt mutations were included. The line-3200 LOCKED mutation names B-CRF 595 and B-AAF 596; the unmodified poll count correctly stays 596. The complementary poll-count mutation independently fails that other row.

Historical runners were not falsely reported green. Their results were R3 5/5, R4 7/8, R5 21/22, R6 38/39, R7 48/50 and R8 73/73. The only unmet historical control expectations are the link-label measurement and code-literal comment diagnostics expressly superseded by decision 6132293481. Both altered pages still fail at the correct line and write their receipts. Some older probe programs also retain old exit assertions or deliberately permitted follower forms; their detailed outcomes are preserved in this packet instead of being equated with new escapes. The current controls and this review's expectations pass.

[R625] Docs applied — the findings, README row, PR body and public evidence location were checked against the receipts and scope decisions. Earlier numerical, attribution, counter-mark, source-comparison and packet-location corrections are present. Neutral role labels are used for the reference peer and external capture; no host paths or their identities are introduced by the reviewed additions. Docs is UNCLEAN only because R625-9-F1 remains open. R625-9-R1 is a non-blocking residue.

**Disposition of earlier public findings.** All dispositions below are at the exact head in this report. Earlier reviews were read only after the independent verdict and ledger were saved. “Resolved” means checked here, not merely asserted by the author.

| Public round / findings | Disposition and present evidence |
|---|---|
| R624-1 F1; R625-1 F3 | Resolved: B0 floor medians, degraded runs and recording start match receipt rows and independent reductions. |
| R624-1 F2; R625-1 F4 | Resolved: all four B6 terms, with timed ratio explicitly NOT RUN (`:3198`). |
| R625-1 F1 | Resolved: 23 degraded whole blocks in overlap, 108 beyond; direct attribution and inference separated in findings, index and PR. |
| R625-1 F2 | Resolved: neutral poll extrema/trace, slip/state transitions, source meter/state comparisons and extraction procedure published; 14 raw hashes match findings hash tables. Raw identity-bearing reads remain outside the public packet as required. |
| R624-2 F1 | Resolved: positive-control floor counts exclude blocks 0 and 1 before playback and partial block 2. |
| R624-2 F2 | Resolved: lock brackets use the previous poll's start (`:3178`), reproduced from traces. |
| R625-2 F1 | Resolved: point-(a) median/worst-block replacement matches per-case upstream summaries (`:3564`). |
| R624-3 F1 | Resolved: evidence branch, pins, round directories and manifest are located and hash-checked. |
| R625-3 F1 | Resolved: no whole-quote or whole-link exemption; unchanged seven-case probe and current controls reject the planted claims. |
| R624-4 F1; R625-4 F1 | Resolved: per-digit coverage, keyword binding and varied numeric/unit spellings; unchanged probes detected their eight and twelve cases respectively. |
| R624-5 F1 | Resolved: each line-3200 case reads its own receipt; unchanged mutation fails the LOCKED row with both case values. |
| R624-5 F2 | Resolved: closed follower rule detects unlisted units; explicit approximation/code limits remain documented. |
| R624-5 F3 | Resolved: author-r5 location is in the current packet map and independently verified. |
| R625-5 F1; R625-6 F1 | Resolved: comment and raw-HTML forms are parsed/refused at their source line; unchanged comment and six rendered probes rerun. The clean control remains clean. |
| R624-7 F1 | Resolved: images, including reference forms, are refused and named; unchanged image probe rerun. |
| R625-7 F1 | Resolved: all four README markup forms refuse at line 15 with receipts, no traceback. |
| R624-8 F1 | Resolved: actual source extent reaches line 18 and is refused there; unchanged boundary probe, 97 controls, 37 extent cases and own boundary probes pass. |
| R625-8 F1 | Resolved by the public decision 6132293481, recorded beside older runner outcomes and in round 9; frozen diagnostic mismatches remain visible. |
| Earlier R1/R2 wording items from round 1 | Resolved: title/PR scope and first counter-mark timing corrected. |
| R624-2 R1/R2/R3 and S1 | Resolved: common-entry comparisons narrowed, pre-set slips not assigned a unique cause, Direction B antecedent corrected, status bit 4 disclosed. |
| R624-5 R1; R624-6 S1/S2; R624-8 S1 | Applied or answered: identifier categories/follower limits documented, the line-3200 poll-count question expressly closed in PR Round 7 item 3, and emoji/tooltip limits stated. |
| Repeated census suggestion; R624-1 S2; R624-4 S1 | Census suggestion now independently checked across the whole lane; poll-extrema publication and round-location pointers are present. No unresolved finding is hidden by these suggestions. |

**Reviewer-owned coverage ledger.**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen scope/rulings; findings B16/B16b/B16c; bench authority; summary and independent reductions | R625-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| RTL | CLEAN | Complete two-file diff/history; register authority; poll traces and state decoding; no implementation changes | R625-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| Robustness | CLEAN | Restore events/full census; teardown; parser allowlist/extents; adverse-input controls and 38 own probes | R625-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| Tests | CLEAN | Figure checker/spec; pinned parser; R3–R9 runners; 14 unchanged review probes; independent reductions and controls | R625-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| Docs | UNCLEAN | Findings/index/PR body, publication manifest and packet map; F1 open, R1 residue | R625-9 applied; no clean coverage | cb5ff79f1f69117efba353484851eceb620e5c92 |

**Reproduction and retained receipts.**

`MANIFEST.sha256` lists all publishable scripts and receipts, relative to this packet. `REPORT.md` is the review. `scratch/` is disposable and excluded. The scripts accept explicit repository, public evidence and output directories; no fixed host location is required. `run_checks.py` runs independent subprocesses concurrently, waits for every result and records each command, log and exit status; maximum concurrency is eight. Each probe tree stays below the output's `scratch/` directory.

With a Python interpreter installed from `tools/markdown/requirements.txt` using hash verification, the portable commands are:

```text
python run_checks.py REPO EVIDENCE_ROOT OUTPUT
python probe_independent.py REPO EVIDENCE_ROOT/author-r9 OUTPUT
python audit_evidence.py EVIDENCE_ROOT OUTPUT REPO
python verify_checkout.py REPO OUTPUT/receipts/checkout-integrity.json
python -I EVIDENCE_ROOT/author-r9/tools/r9_parser_extents.py EVIDENCE_ROOT/author-r9/tools/check_b16_figures.py REPO OUTPUT/scratch/parser-extents OUTPUT/receipts/parser-extents.json
python -I EVIDENCE_ROOT/author-r9/tools/r9_evidence_receipt.py REPO b0134c63 b522bb92 OUTPUT/receipts/evidence-location.json
```

The repository must also contain the fetched public evidence commit and the historical evidence pin named above. The exact control/probe commands and statuses are in `receipts/check-commands.json`, accompanying logs and per-probe JSON. `docs_check.py` and the em-dash check against `c20c85bd` independently passed. The author's published exact-head gate receipt is copied as `receipts/author-gates.json`; its 14 entries have exit zero, including two environment/version checks. These are author source-head receipts, not manager source-bank execution.

After the probes, raw tracked blob bytes, executable modes and the index were checked against the exact Git trees without filters. All 1,291 parent blobs and all 880 blobs in the three required submodules matched, with their required gitlinks intact and a clean worktree. All five parent gitlinks are recorded in `receipts/checkout-integrity.json`. Only the two expected findings Markdown files differ from the source base. No probe modified source bytes.

**Limits and pending manager duties.**

This review checks the public reduced receipts, extracted traces, arithmetic, source extent rules and stated conclusions. It does not recreate physical captures or independently authenticate raw identity-bearing source-control reads. The neutral source comparisons and their extraction procedure were examined; their twelve raw hashes and the two poll hashes are bound to the findings, while the private raw inputs are not republished. Source routing/clock changes outside the lane remain attributed as external observations, not DUT behavior.

No hardware action, calibration, implementation bank, synthesis bank, hosted job acceptance or local hosted-workflow replica was performed. Physical calibration NOT RUN and field skips are not hardware proof. B6's timed ratio, Direction B's INTERNAL mismatch control and the separately tracked remaining behavior stay open as documented. Sampling LOCKED at every poll is not continuous-time observation. Tap attribution outside the captured overlap remains inference. The checker follows the pinned parser's visible text; documented emoji post-processing, link tooltip, code/follower and approximation limits are not silently claimed covered.

The manager must obtain the F1 correction and a Docs re-review, carry R1 to the residue checklist, publish this packet, and satisfy the independent review and hosted/local acceptance requirements. No manager source bank is claimed at this head. Source validation is distinct from final current-dev candidate validation: the source base is `c20c85bd`; the supplied live-dev tip is `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. The manager owns the merge-turn candidate builder/native banks, linking their receipts on the PR, exact candidate checks, maintainer merge authorization and post-merge containment. A changed artifact invalidates coverage within its lens as required by AGENTS.md.

R625-9 FINISHED
