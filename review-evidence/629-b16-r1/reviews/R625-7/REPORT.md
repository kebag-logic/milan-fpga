[R625] NEGATIVE - exact head 295ba9d7f7dfed65e95002478ed6d55ccc14e580

One new MINOR, R625-7-F1, remains open under Conformance, Robustness, Tests and Docs. RTL is CLEAN. All five lenses were applied independently. Earlier public findings are resolved as detailed below. No present bench figure, grade or DUT behavior is challenged by the new finding: a covered index line containing markup crashes the evidence checker before it emits the promised line-specific refusal and receipts. It fails closed.

The reviewed tree is `160ba4535ed6caf63d23994b364b1f054bd95589`. The full `c20c85bd..295ba9d7` diff and its ten commits change only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`. In this report, **findings** means the former file at this head, **index** means the latter, and evidence paths prefixed `author-r7/` belong to the [pinned public packet](https://github.com/kebag-logic/milan-fpga/tree/fa974c3f1f9a1ef3a461ebb3b090b1915faaf251/review-evidence/629-b16-r1). Reviewer receipts are relative to this report.

The independent verdict and ledger were written before consulting previous public review findings. Reconstruction followed the requested order: repository contract and documentation map; frozen issue acceptance and public scope decisions; linked requirements and interfaces; full diff/history; public executable evidence. Prior findings were then reconciled. No other reviewer's report supplied the independent verdict.

## R625-7-F1 — MINOR — Conformance, Robustness, Tests, Docs

**Artifact:** `author-r7/tools/check_b16_figures.py:2767`, with partial-line scope at `:2628`; index `:15`; findings `:4023`. Reproduction: `probe_markup.py` and `receipts/own-markup.json`, cases `index-comment`, `index-short-comment`, `index-tag`, and `index-tag-no-digit`.

**Authority/evidence:** The [round-7 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6128175910) requires rejection of any HTML comment or raw tag in the text the check reads, with the refused line identified. Findings:4023 says the check names each refused line with its markup as MARKUP before failing. The index's B16 suffix is explicitly within scope.

Append ` <b>evidence</b>` to the B16 suffix of index:15 in a disposable copy and run the unmodified published check. It exits 1 with `AttributeError: 'NoneType' object has no attribute 'group'`. Standard output is empty, and neither the rows nor coverage receipt is written. An ordinary comment, short comment and tag between a number and unit reproduce the same failure. The same four forms in findings:3011 produce the intended named MARKUP refusals and both receipts. An ordinary unclaimed number in index:15 also produces the intended receipt-backed refusal.

`MARKUP.finditer(t, at)` yields offsets relative to the full line `t`. The diagnostic extraction then slices at `at + m.start()`, adding the B16 suffix offset twice. The corresponding findings lines start at offset zero, which is why the existing page controls do not expose this branch.

**Impact:** The forbidden text cannot obtain a passing verdict, but a supported input location aborts the check and suppresses all computed receipts and the required source-line diagnostic. This contradicts the round's executable contract and its documentation. It is MINOR rather than wording-only RESIDUE because executable failure behavior changes.

**Required outcome:** Markup anywhere in the covered index suffix must produce a named `README.md:15` MARKUP refusal and write the two receipts without an exception. Add coverage of the partial-line index case, including markup without a digit, while preserving ordinary page refusals, exact generator-marker exceptions and baseline figures.

**Verification:** Re-run `probe_markup.py`; all four index markup cases must reject with MARKUP at the index line, write both receipts, and have no traceback. The unchanged page must pass; prior controls and defect probes must retain their expected outcomes.

## Evidence applied to each lens

**Conformance:** Checked the issue's acceptance against [B16's assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), the [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), the [B16c exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), `docs/reference/FR_NFR.md:252`, and `docs/design/MEDIA_CLOCK_FOLLOWING.md:1661`. Findings:2314, 2640, 3005, 3198 and 3317 preserve the scope and limits.

B16's loopback does not form: `summary/loop2/acmp-peer-tap.json` contains two unreflected CONNECT_TX probes, approximately 200.015 ms apart; the connection reads never resolve the stream. This is reported as a bench stop. B16b's four points and B0 grading are supported by the tap, alignment and per-block receipts. Independent arithmetic reproduces 169 floor blocks and 131 degraded blocks, floor medians -123.98/-123.95 dB, the split at floor block 45, and 23 degraded blocks inside the 34.1136-second common overlap versus 108 beyond it. The latter attribution is explicitly inference in findings, index and PR body. The recording starts about 06:38:05.2 after the two-second playback lead, about 26 seconds after the binds.

Both B16c following cases have 300/300 blocks at the path's floor, medians -123.98/-123.97 dB, and no recorded discontinuity. The four-point comparisons are sample-exact within their measured overlap. At point (a), the exact replacement at findings:3244 gives -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF; each worst block rounds to -123.93 dB. The positive control counts only wholly playing blocks: 11/13 for `pts2` and 303/303 for B0 and both following cases, excluding the two pre-playback blocks and the start block.

Findings:3198 states all four B6 terms. Three are met; the timed ratio is NOT RUN and no decision replaces it. Direction B's INTERNAL mismatch control is also NOT RUN: B0 has the reference peer following the DUT; the permission to select the peer's INTERNAL source covers B-CRF and B-AAF only. Thus the lane's documentation does not claim completion of every broader #629 bench criterion. F1 alone leaves this review's Conformance lens unclean.

[R625] PASS RTL — complete two-file diff; `docs/reference/REGISTER_MAP.md:1870`, `:2076`, `:2139`; `author-r7/r2/bcrf-poll-trace.tsv` and `author-r7/r2/baaf-poll-trace.tsv` — checked the documentation's interface interpretation against the authoritative register fields. No RTL, firmware, build, image or gitlink change occurs in the candidate.

All 1,420 poll rows were independently decoded. Servo state 4, signed trim in 1/16 ppm, stream rate in 512 units/ppm, slip fields and AAF meter word `0x001e0007` agree with the register map. Both windows contain 596 LOCKED polls, trim -6.125 to -6.000 ppm, and zero TDM slips. The selected AAF meter records enabled/locked/rate-valid, zero history restarts and 30 ns maximum deviation. LOCKED brackets are 2.585–3.161 seconds and 6.602–7.180 seconds from the preceding ACQUIRE poll's start through the first LOCKED poll's end. This is interface/documentation coverage, with no new implementation or hardware execution.

**Robustness:** Examined all nine `runs/*/events.jsonl` restoration sequences, `restore/census-*.jsonl`, the B16c dry-run/deadline controls, both poll traces, positive-control exclusions and the checker's scope, normalisation, identifier followers and markup code. The failed first B0 run is disclosed; cleanup and readback evidence covers the later usable runs. Every changed format, binding, map and source returns to its recorded as-found value under the documented comparison. All eight clock-source sets have SUCCESS and matching readbacks. In each following case the peer goes INTERNAL, the DUT selects the followed source, the DUT returns INTERNAL, its binds are undone, and the peer returns to its original source. The full B16-start/B16c-end census has 44 of 45 reads equal; the difference is the DUT's live propagation delay.

The traces contain five pre-selection IDLE loopback-slip transitions per case, then one/two ACQUIRE transitions, with none after LOCKED. The page distinguishes observation from proposed causes. Partial source snapshots are compared only over common entries: 2,262 identical entries, then 1,255 shared with four differences, then 618 identical and 668 shared with two monitoring-mix differences. Actual source clock/routing changes outside the lane are attributed to the source rather than to DUT behavior. F1 leaves Robustness unclean.

**Tests:** Ran the published checker independently, reproduced its generation byte for byte, ran all standing round-3 through round-7 controls, all ten published historical probe scripts unchanged, and 25 reviewer cases. Independent arithmetic used the reduced receipts without importing the checker's calculations; see `audit_receipts.py` and `receipts/independent-receipt-audit.json`. Source read hashes, all source/restore comparisons, grade medians, overlap counts and register decodes agree. Existing controls exercise many substantive failures, but all four new index markup cases abort before diagnostics. F1 leaves Tests unclean.

**Docs:** Read the full added section, introduction, index, current PR title/body, round assignments, publication mappings and source gate receipts. Findings:2608 names the evidence branch, pinned commit, author-r1 through author-r6 mappings, and the manifest; it says author-r7 follows in a later publication. The assigned publication supplies that directory. Checked all 707 author-r7 publication hashes, including 49 declared path redactions; all 93 packet hash/size table rows match their published bytes. Historical mapping, manifest counts and hashes verify. Reduced extrema, timestamped slips/states, neutral source meter/state comparisons, raw hash bindings and extraction procedures are public at findings:3426 onward. Names remain neutral and no host paths are exposed in the reviewed changed text. The counter mark is stated exactly: 20 seconds after the set, about six seconds before the recording window. Local documentation gates pass. F1 leaves Docs unclean because the line-specific refusal claim is false for the covered index suffix.

## Executed checks and interpretation

Exact commands, return codes and raw output are in `receipts/campaign-results.json` and the adjacent `.log`, `.rc`, `.json` and `.tsv` files.

| Execution | Result |
|---|---|
| Unchanged figure check | rc 0; 1,834/1,834 rows OK; 14,531 digits, 11,910 claimed by rows and 2,621 by categories; zero uncovered digits or markup |
| Figure/coverage receipts | Byte-identical to the publication; `receipts/reproduction-comparison.json` |
| Checker regeneration | Byte-identical; SHA-256 `6b2570b8361356f71f36dc8ec72197c5a8882fa3507f7a01a533f23e575897a0`; `receipts/checker-regeneration.json` |
| Standing controls, rounds 3/4/5/6/7 | 5/5, 8/8, 22/22, 39/39, 50/50; each runner rc 0; outputs byte-identical to published reruns |
| Round-7 self-probes | 111 expected outcomes, comprising 92 rejections and 19 stated passes; byte-identical |
| R625-3 quote/link probe | 7/7 detected; no whole-quote or whole-link exemption remains |
| R624-4 spelling probe / R625-4 coverage probe | 8/8 and 12/12 detected unchanged, including joined units, spacing, sign, leading point and exponent forms |
| R624-5 row-3200 numerator / R624-6 denominator probes | Each independent mutation makes its corresponding row MISMATCH, reading both cases' own receipts |
| R625-5 comment probe | `[0, 1, 1]`: unchanged passes; single-line and multiline comments are refused at source lines |
| R625-6 six-case rendered-comment probe | `[0, 1, 1, 1, 1, 1]`: all five altered cases refused; the plain digit is UNCOVERED and comments are MARKUP |
| Reviewer cases | Unchanged passes; all 24 altered cases reject, including four index markup exceptions; no new false pass observed |
| Independent receipt audit and evidence mapping | PASS |
| Documentation style, paths, contents, anchors, punctuation and whitespace checks | All seven commands rc 0 |
| Checkout verification | Exact tracked bytes/modes/index, required submodule checkouts and all gitlinks; clean status |

The unchanged R625-6 rendered-comment script itself exits 1 because its assertion expects the old broken vector `[0, 1, 1, 0, 0, 0]`. Its measured current vector demonstrates the fix; reporting every historical script as rc 0 would be wrong.

Likewise, the broader exploratory probes include acknowledged limits. R624-5's escape probe detects 21/25 forms, with colon separation and digit-free quantities outside the stated rule. R624-6's 37 forms include four old expected-fail cases that still pass: bare units after “of” or “and”, a possessive separator, and a unit-only numbered item. Round 7 discloses these and approximate word phrases explicitly. The 22-case follower probe preserves stated literal-path/identifier exceptions while rejecting its comments and tags. These are optional prior scope limits, not newly represented as exhaustive natural-language parsing.

The check accounts for each numeric character in its covered text, keeps source locations through whitespace/entity/escape normalisation, and has no comment-dropping normaliser. Generator-marker exceptions compare the full line byte for byte. The index-offset defect is the remaining failure of the new markup policy. Reviewer multiline additions can also shift fixed row positions; the dedicated unchanged historical probes and standing controls supply the isolated multiline evidence.

## Prior public findings at this head

These resolutions follow this round's own examination and execution; earlier verdicts do not substitute for it. Finding lenses retain their original attribution.

| Prior finding(s) | Disposition and current evidence |
|---|---|
| R625-1-F1 | RESOLVED: 23 directly observed degraded blocks versus 108 inferred beyond the taps; findings:2836, index:15 and PR body; independent overlap arithmetic |
| R625-1-F2; R624-1-S2 | RESOLVED/TAKEN: neutral raw-hash-bound reductions and extraction procedure at findings:3426; both traces and twelve source-read bindings verified |
| R624-1-F1; R625-1-F3 | RESOLVED: B0 floor medians, block-45 split and recording start at findings:2673, 3415; receipts agree |
| R624-1-F2; R625-1-F4 | RESOLVED: all four B6 terms at findings:3198, including timed ratio NOT RUN; acceptance, index and PR retain the limit |
| R624-1-R1/R2; R625-1-R1/R2 | RESOLVED: exact corrected PR title and exact counter-mark timing at findings:3040, 3095, 3421 |
| R624-1-S1; R625-1-S1; R624-2-S2; R625-2-S1; R625-3-S1 | TAKEN: 44/45 reads, excluding the census header; full restore recount agrees |
| R625-2-F1 | RESOLVED: exact replacement at findings:3244 agrees with all four point-(a) medians and worst blocks |
| R624-2-F1 | RESOLVED: only wholly playing positive-control blocks counted; independent 11/13 and 303/303 results |
| R624-2-F2 | RESOLVED: LOCKED brackets use the preceding state-read poll's start; independently decoded traces |
| R624-2-R1/R2/R3 | RESOLVED: source-state claims bounded to common entries; pre-selection slip causes qualified; PR explicitly names Direction B's missing INTERNAL mismatch control |
| R624-2-S1 | TAKEN: findings:3341 records status bit 4, DRP configuration mismatch, without claiming analysis |
| R624-3-F1 | RESOLVED: findings:2608 maps branch, commits, directories and manifest; historical and current publication mappings verify |
| R625-3-F1 | Original quote/link escapes RESOLVED: unchanged 7/7 probe and narrowed categories. F1 above is a distinct diagnostic defect |
| R624-4-F1; R625-4-F1 | Original digit/spacing/spelling escapes RESOLVED: unchanged 8/8 and 12/12 probes; per-character coverage |
| R624-4-S1 | TAKEN: opening paragraph points to subsequent rounds |
| R624-5-F1 | RESOLVED: each case read separately. Numerator and denominator mutations each fail their own line-3200 row; unchanged values need not mismatch |
| R624-5-F2 | Original spelled-unit escapes RESOLVED: required unit words and unfamiliar direct followers are detected; broader stated limits remain optional |
| R624-5-F3 | RESOLVED: author-r5 mapping at findings:2616, publication and manifest verified |
| R625-5-F1 | Original multiline-comment escape RESOLVED: source-line refusal replaces comment stripping; historical `[0,1,1]` result |
| R624-5-R1 | RESOLVED: exact channel/step/round and issue-number wording at findings:3764 and in the PR body |
| R624-5-S1; R624-6-S1 | TAKEN: closed-list and approximate-quantity limits expressly stated; self-probes retain the documented behavior |
| R625-6-F1 | RESOLVED: short comments no longer hide visible units; six-case result above and raw-tag control reject at the line |
| R624-6-S2 | Technical question answered: independent numerator/denominator mutations prove the original verification condition. Optional managerial acknowledgement remains administrative |

No previous BLOCKER, MAJOR or MINOR is retained. No new RESIDUE or SUGGESTION is filed.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — R625-7-F1 | Issue #629 acceptance/rulings; findings:2314, 3005, 3198, 3317, 4023; public events, grade and restore receipts | R625-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| RTL | CLEAN | Complete two-file diff; REGISTER_MAP:1870, 2076, 2139; both 710-row poll traces; checkout gitlinks | R625-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| Robustness | UNCLEAN — R625-7-F1 | Checker:2628, 2638, 2767; negative/deadline controls; runs/restore receipts; independent index/page probes | R625-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| Tests | UNCLEAN — R625-7-F1 | Checker and generator; 1,834 figure rows; controls r3–r7; ten historical probes; own markup and receipt audits | R625-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |
| Docs | UNCLEAN — R625-7-F1 | Full findings diff; index:15; PR title/body; publication/manifest maps; source gate receipts and local document checks | R625-7 | 295ba9d7f7dfed65e95002478ed6d55ccc14e580 |

## Reproduction, limits and pending duties

The four published scripts take symbolic local inputs, not embedded host paths. `REPO` is a detached exact-head checkout; `AUTHOR_PACKET` is the published `author-r7` directory with its publication `MANIFEST.json` in the parent; `OUT` is an empty reviewer packet directory. Supply the repository's hash-locked Markdown dependencies in an isolated environment and make the cited evidence commit available in the repository object store. Run in the foreground:

```text
python run_review.py REPO AUTHOR_PACKET OUT --jobs 8
python probe_markup.py REPO AUTHOR_PACKET OUT
python audit_receipts.py REPO AUTHOR_PACKET OUT
python verify_checkout.py REPO OUT/receipts/checkout-integrity.json
```

All disposable trees belong under `OUT/scratch/`. The campaign joins every subprocess; this run used at most nine concurrent focused jobs. No source file was edited. Final verification compares 1,291 parent tracked files' actual blob bytes and modes, the entire index, required initialized submodule bytes/indexes, and all five gitlinks. The source head/tree remain exact; status is clean. See `receipts/checkout-integrity.json`. `MANIFEST.sha256` lists every publishable script and receipt; scratch is excluded.

The review validates the public reductions, executable checks and document claims. Original waveform, capture and source-state bytes were not available for independent remeasurement; their hashes bind the reductions but do not replace raw acquisition evidence. The historical five-overrun statement depends on a public operator receipt whose underlying original console log is unavailable, as the findings disclose. No fresh hardware operation, full parent/protocol/timing/synthesis bank or builder bank was run. Physical calibration is NOT RUN. Skipped field or physical jobs are not hardware proof.

`author-r7/gates/r7/results.json` reports fourteen rc-0 source-head checks, including identity/version and whitespace checks; these are the author's published results, distinct from this review's listed executions. No manager source bank exists at this head and none is inferred. The hosted snapshot in `receipts/hosted-snapshot.tsv` contains some successful executed jobs, queued/in-progress jobs, and a skipped physical context. It does not establish completed mandatory aggregate acceptance. The manager owns hosted/local-replica acceptance.

The manager must publish this report and listed receipts, arrange correction and independent re-review of F1, and obtain the required review approvals. At the merge turn the manager must build and validate the final candidate against then-current dev, starting from the stated live-dev reference `dc4d06cbfec209cc2ff76806f4b49c51f46639ae` rather than treating source base `c20c85bd` as current, publish those receipts, complete hosted/local acceptance, and perform authorized merge and post-merge containment. This review grants no merge authorization and does not close #629's unperformed physical or bench work. No review campaign remains running.

R625-7 FINISHED
