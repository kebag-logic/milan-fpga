[R625] NEGATIVE - exact head 3619019350936d5af851933df0b5444ef8387e69

Round R625-5, external independent review of issue #629 / PR #725. Tree: `11777358b03b38ceda5ade1e1ed59e31b08473e5`. Comparison: `c20c85bd..3619019350936d5af851933df0b5444ef8387e69`.

All five lenses were applied. One MINOR remains: the figures checker accepts an unsupported measurement across a multiline HTML comment. No incorrect current bench figure or DUT implementation defect was found. The unchanged page, all standing controls, and the three unchanged prior review probes pass. The new finding affects Conformance, Robustness, Tests and Docs; RTL is CLEAN.

**Scope and independent reconstruction**

Read the operating contract and CONTRIBUTING.md, docs/README.md, the [issue contract](https://github.com/kebag-logic/milan-fpga/issues/629), the [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), [B16c clock exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), and subsequent public scope decisions through [round 5](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6125608002). Then examined the linked repository authorities, complete diff/history and public executable evidence. The independent verdict and ledger were written before reading prior public review findings. No current-round peer report or private author material was consulted.

Authorities include REQUIREMENTS.md; FR-CLK-03/04 at `docs/reference/FR_NFR.md:252`; the clause discussion and Bench contract in `docs/design/MEDIA_CLOCK_FOLLOWING.md`; `docs/design/TIME_SYNC.md:135`; `docs/overview/ARCHITECTURE.md:72`; and `docs/reference/REGISTER_MAP.md:1870`, `:2080`, `:2139`.

Eight commits change only the findings page and its index: 1,572 inserted lines and one deleted line. The measured image is dev `5603c353`, distinct from this documentation head. There is no implementation, generated-image or gitlink change.

Evidence paths below refer to `author-r5/` in the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/a73ce5c42ee97fb53b272a51b5f41a55afba5fa5/review-evidence/629-b16-r1). Review receipts and scripts are relative to this report. All 593 author-r5 publication hashes verify, including the 33 declared path-redacted files. All 76 current packet-file hash/size rows on the findings page match their files. Both figure-check outputs reproduce byte for byte.

**R625-5-F1 - MINOR - Conformance, Robustness, Tests, Docs**

Artifacts: published `author-r5/tools/check_b16_figures.py:2333` (`SEP`), `:2334` (`MEASURE`), `:2342` (`measured`), and `:2422` (descriptor category); `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3745`; PR #725 body, Round 5 item 2. Reproduction changes only a disposable copy of findings lines 3108 and 3109.

Authority/evidence: round 5 requires a number followed by a unit to be claimed by a receipt row, never an identifier. The page and PR body expressly include HTML comments among the permitted separators and say the check reads across line breaks. `SEP` uses `<!--.*?-->`, but `MEASURE` is compiled without DOTALL. The comment arm therefore stops at a newline. The descriptor category can still cover the preceding digit.

The controlled probe inserts the following sentence into the B16c channel paragraph, keeping exactly the original number of source lines. It moves the existing `Channels 2 and` onto the next line so every original receipt row retains its line number:

```text
The residual was CLOCK_DOMAIN 7<!--
-->ppm.
```

The published checker and all receipt files remain unchanged. The inserted 7 has no receipt row.

| Probe | Check exit | Result |
|---|---|---|
| Unchanged page | 0 | 1,749 rows OK; 13,209 numeric characters; zero uncovered |
| Same measurement with `7<!-- -->ppm` on one line | 1 | Names 7 at line 3108 as an uncovered measurement |
| Measurement with `7<!--` followed by newline and `-->ppm` | 0 | 1,749 rows OK; 13,210 numeric characters; zero uncovered; added 7 covered as `descriptor index` |

The false pass has 11,037 numeric characters claimed by rows and 2,173 claimed by categories, across 1,099 identifier spans. The baseline has 2,172 category characters across 1,098 spans. This isolates an identifier exemption swallowing a measurement; no row mismatch or shifted line contributes to the result. `receipts/comment-probe.json` preserves the exact old/new text, outputs and category evidence. The three raw logs and return-code files are also published.

Impact: the counter can account for every digit while classifying a new, unsupported measurement as an identifier. The current receipt-backed figures remain valid, but the promised protection against unreceipted measurements is incomplete. This changes executable validation and its evidence claim, so it is not wording-only RESIDUE.

Required outcome: a multiline HTML comment between a number and its unit must not grant an identifier exemption. Reject the unsupported measurement and identify its digit and line. Add a standing control for this reproduced boundary while preserving the unchanged page, existing controls and prior probes. Narrowing the prose alone does not satisfy the assigned rule.

Verification: run `probe_comment_separator.py REPO AUTHOR_R5 REVIEW_PACKET`. At this head the campaign exits 1 with individual statuses `[0, 1, 0]`; a corrected checker must produce `[0, 1, 1]` and campaign exit 0. Then rerun the 22 standing controls, earlier runners and unchanged prior probes, and re-review the corrected checker and documentation. No source fix was made here.

**Evidence by lens**

Conformance is UNCLEAN for F1. The bench sequence otherwise agrees with the scope decisions. `summary/loop2/acmp-peer-tap.json` shows two unanswered self-directed CONNECT_TX probes 200 ms apart, supporting the unreflected PROBE_TX diagnosis and STOP. B16b grades the four points and stops before circular following. B16c uses the peer-INTERNAL exception only for B-CRF and B-AAF. `runs/{bcrf,baaf}/ctl.jsonl` independently confirms all eight successful source SETs and matching GET fields: peer INTERNAL, DUT CRF/AAF, DUT INTERNAL, peer CRF. The run records put the peer restore after the DUT unbinds. Listener formats are read equal or adapted before binding. All nine final run states equal their as-found fields. The INTERNAL mismatch control and timed ratio remain NOT RUN; #629 remains open.

[R625] PASS RTL - the complete two-file diff; `docs/overview/ARCHITECTURE.md:72`; `docs/reference/REGISTER_MAP.md:1870`, `:2080`, `:2139`; both `r2/*-poll-trace.tsv` files - the documented interface and clock interpretations agree with their authorities. Source indices 0/1/2, servo state 4, signed trim in 1/16 ppm, stream rate in 512 units/ppm, slip-counter fields and meter word `0x001e0007` were checked. Both windows decode to 596 LOCKED polls and zero TDM slips. The selected AAF meter has zero history restarts and 30 ns maximum deviation. This is coverage of the documentation's architecture/interface claims, with no new implementation execution or hardware validation.

Robustness is UNCLEAN for F1. Examined `runs/{loop1,loop2,b0}/events.jsonl`, the disclosed busy-capture incident, `tools/run_b16c.py:590` and `:718`, the eight published dry-run outcomes and wrapper-deadline receipt, positive-control boundary blocks and both poll traces. The failed B0 capture remains ungraded. The dry-run receipts cover refused selection, absent lock, busy playback, incorrect initial state, controller termination and deadline teardown; these were inspected, not re-executed. Restore code orders DUT INTERNAL, unbinds, then peer CRF and re-establishes a terminated controller when needed. Actual restores were checked independently. Each following trace has five IDLE slip steps before selection, then one/two ACQUIRE steps, with none after observed LOCKED. F1 is a separate unsupported-input acceptance case in the evidence checker.

Tests are UNCLEAN for F1. Independent per-block arithmetic reproduces B0's 169/300 floor blocks, medians -123.98/-123.95 dB, split degraded runs 43-44 and 46-54, and 23 degraded blocks inside the common tap overlap versus 108 beyond. The B0 reduction reproduces byte for byte, including recording launch plus the two-second lead, about 26 seconds after binding. Both following cases have 300/300 floor blocks, no reported discontinuities and -123.98/-123.97 dB floor medians at (c). The checker verifies every existing summary/attribution figure; the exact four-value replacement at (a) is present. Positive controls exclude silent blocks 0/1 and playback-start block 2: 303/303 wholly playing blocks in B0/B-CRF/B-AAF, and 11/13 in pts2. Direct sample equality remains limited to the documented 34.1-34.3-second overlaps.

Docs are UNCLEAN for F1. Examined findings lines 2287-3833, index line 15, live PR title/body, extraction procedures, publication mapping, hash tables, author gate receipts and privacy. The findings, index and PR body distinguish measured overlap from later inference. Source routing and clock changes are attributed outside the lane. Source-state claims are bounded to common entries. The reference peer and external capture are named by role, with no identifying host paths in the added prose. Documentation hygiene, style and diff-whitespace checks pass. The advertised measurement guard remains unsupported in the F1 boundary case.

**Prior public findings at this exact head**

Reconciled all eight prior public findings comments after the independent pass and written verdict/ledger: [R624-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428), [R625-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570), [R624-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119878041), [R625-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119899949), [R624-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121093801), [R625-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121186527), [R624-4](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125594896), and [R625-4](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125596576). The public inventory has zero formal reviews and zero inline review comments.

| Prior items and attributable lenses | Disposition and evidence |
|---|---|
| R625-1-F1: Conformance, Tests, Docs | RESOLVED. Findings:2826,2835,3254; index:15; PR body retain 131 at (c), 23 observed inside the overlap and 108 inferred beyond. Independent block/overlap arithmetic agrees. |
| R625-1-F2: Tests, Docs; R624-1-S2: Tests | RESOLVED. Public `r2/` receipts contain extrema, timestamped slip transitions/states and neutral source comparisons, bound to raw hashes with extraction instructions at findings:3426. Both traces were decoded and all twelve source-read hash bindings checked. Private reductions were not regenerated. |
| R624-1-F1: Conformance, Docs; R625-1-F3: Conformance, Tests, Docs | RESOLVED. B0 floor medians, split block runs and recording start match the receipts. `receipts/b0-recomputed.json` is byte-equal to the published reduction. |
| R624-1-F2: Conformance, Docs; R625-1-F4: Conformance, Tests, Docs | RESOLVED. Findings:3198 states all four B6 terms for both cases: three met, timed ratio NOT RUN, no replacement decision. Acceptance, limits, index and PR body preserve this. |
| R624-1-R1 / R625-1-R1: Docs | RESOLVED. Live PR title exactly uses the requested distinction between B0 grading and following cases at the floor; `receipts/public-state.json`. |
| R624-1-R2 / R625-1-R2: Docs | RESOLVED. Findings:3040,3095,3172 place the first mark 20 seconds after the DUT set, about six seconds before recording; header says before the window and near its end. |
| R625-2-F1: Conformance, Tests, Docs | RESOLVED. Findings:3244 uses the exact required replacement: -123.98/-123.97 dB at (a) for B-CRF, -123.98/-123.98 dB for B-AAF, each worst block -123.93 dB. The figure rows match both tap receipts. |
| R624-2-F1: Robustness, Tests, Docs | RESOLVED. Positive-control counts exclude the two silent blocks and transition block; independent arithmetic confirms 303/303 and 11/13. Both pts2 taps' 15 wholly playing floor blocks are covered by the figure checker. |
| R624-2-F2: Tests, Docs | RESOLVED. Findings:3172-3181, summaries, index and body use 2.585-3.161 and 6.602-7.180 seconds, beginning at the last ACQUIRE poll's start. The reduced traces reproduce the lower endpoints; upper endpoints match the raw-hash-bound receipts within the rounded trace's sub-millisecond resolution. |
| R624-2-R1: Docs | RESOLVED. Findings:2784,3261,3275 bound source-state claims to 1,255 common entries and the 618/668 entries around B16c. |
| R624-2-R2: Docs | RESOLVED. Findings:3214 states clock difference and the first bind slip as possible causes, with receipts unable to separate them. |
| R624-2-R3: Docs | RESOLVED. PR body explicitly names Direction B's INTERNAL mismatch control and explains why it did not run. |
| R624-2-S1: Docs | RESOLVED. Findings:3341 records servo status bit 4, DRP config mismatch, without claiming analysis. |
| R624-1-S1 / R625-1-S1 / R624-2-S2 / R625-2-S1 / R625-3-S1: Docs | RESOLVED. Census wording is 44 of 45 reads. Each lane and B16 start against B16c end independently agree after excluding the header; only live propagation delay differs. |
| R624-3-F1: Docs | RESOLVED. Findings:2608 names branch, pinned commit, author-r1/r2/r3 and the later author-r4 directory. Historical MANIFEST.json has the stated hash and 1,680 entries. All 66 historical table rows match author-r3 publication bytes; location receipt regenerates byte-equal. |
| R625-3-F1: Conformance, Robustness, Tests, Docs | Original quote/link escapes RESOLVED: no whole-label/whole-quote exemption, and its unchanged probe detects 7/7. The broad measurement guarantee remains open under new F1 above. |
| R624-4-F1 / R625-4-F1: Conformance, Robustness, Tests, Docs | Original spellings, spacing and unbound-continuation escapes RESOLVED: unchanged probes detect 8/8 and 12/12, with published script hashes verified. Coverage now counts numeric characters; rows and keyword-bound categories cover the unchanged text. The measurement/category boundary remains unclean under new F1. |
| R624-4-S1: Docs | RESOLVED. Findings:2308 points to rounds 2 through 5. |

No prior wording residue remains. F1 is the only classified open finding from this round.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue and scope decisions; findings:3040,3082,3198,3745; controller readbacks; nine run restores; measurement probe | R625-5 applied; no clean coverage | 3619019350936d5af851933df0b5444ef8387e69 |
| RTL | CLEAN | Complete two-file diff; architecture:72; register map:1870,2080,2139; both raw-word traces; required gitlinks | R625-5 | 3619019350936d5af851933df0b5444ef8387e69 |
| Robustness | UNCLEAN: F1 | Checker separators and identifier boundary; incident records; control silence; poll transitions; teardown and dry-run receipts | R625-5 applied; no clean coverage | 3619019350936d5af851933df0b5444ef8387e69 |
| Tests | UNCLEAN: F1 | 1,749 figure rows; standing controls; unchanged prior probes; independent arithmetic; comment-separator probe | R625-5 applied; no clean coverage | 3619019350936d5af851933df0b5444ef8387e69 |
| Docs | UNCLEAN: F1 | Findings and index; PR title/body; manifests; extraction procedure; coverage claim; hygiene/style checks | R625-5 applied; no clean coverage | 3619019350936d5af851933df0b5444ef8387e69 |

**Executed verification and reproduction**

| Check | Result and receipt |
|---|---|
| Unchanged figures checker | rc 0; 1,749 matching rows; 13,209 numeric characters; zero uncovered; `receipts/figures.log` and both TSV files |
| Round-5 standing controls | 22/22 PASS, each defect named; `receipts/r5-controls.json` |
| Earlier controls, unchanged | 5/5 and 8/8 PASS; `receipts/r3-controls.json`, `receipts/r4-controls.json` |
| Prior review probes, unchanged | R624-4 8/8, R625-4 12/12, R625-3 7/7 detected; `receipts/prior-probe-reruns.json` and per-probe receipts |
| Published additional forms | 36/36 detected; `receipts/self-probes.json` |
| Independent separator control | Baseline 0, single-line comment 1, multiline comment 0; reproduces F1; `receipts/comment-probe.json` |
| Independent exploratory campaign | 64 forms: 57 rejected, seven accepted; all exact inputs and outputs in `receipts/own-probes.json`. Includes small/fullwidth hyphen-minus and punctuation variants. These exploratory acceptances are not seven separate findings; the controlled multiline-comment comparison establishes F1 without relying on ambiguous punctuation. |
| Independent receipt audit | PASS; publication hashes, floor arithmetic, overlap, positive controls, register traces, eight controller readbacks, nine restores, four census comparisons and source comparisons; `receipts/receipt-audit.json` |
| Regeneration | Checker, B0 reduction and evidence-location receipt byte-equal; `receipts/regeneration.json` |
| Focused documentation checks | Hygiene, style and diff whitespace rc 0; `receipts/focused-checks.json` and logs |
| Exact checkout verification | 1,291 parent blobs and 880 required-submodule blobs verified, including bytes, modes, indexes and pins; `receipts/integrity-final.json` |

Portable scripts accept the repository, public author packet and review packet as positional arguments. Obtain author-r5 and its parent MANIFEST.json from the pinned evidence commit, retaining source history and fetching the pinned evidence commit into the repository object store. Run in the foreground:

```sh
python3 run_checks.py REPO AUTHOR_R5 REVIEW_PACKET
python3 replay_probes.py REPO AUTHOR_R5 REVIEW_PACKET
python3 audit_receipts.py REPO AUTHOR_R5 REVIEW_PACKET
python3 probe_additional.py REPO AUTHOR_R5 REVIEW_PACKET
python3 probe_comment_separator.py REPO AUTHOR_R5 REVIEW_PACKET
python3 verify_checkout.py REPO REVIEW_PACKET/receipts/integrity-final.json
```

The isolated comment probe intentionally returns nonzero at this head. Independent campaigns were joined in foreground processes, with at most eight concurrent children. Disposable copies and generated builds remain under scratch. No candidate bytes were edited.

One initial review-driver call supplied the wrong arguments to the optional additional-forms runner. The corrected invocation passed all 36 forms; `receipts/checks.json` preserves both the setup error and retry result. Independent-audit development also corrected handling of older restore records and displayed rounding; the final script passes on the unchanged published data. These are review-harness corrections, not candidate findings.

**Real limits and pending manager duties**

Raw audio and tap captures, full raw polls, private source reads/class map and playback logs were not accessed. Hash agreement with inventories binds the public citations; it does not rehash unavailable captures. Reduced traces support register decoding, while source-role classification depends on the published reduction. B16b's overwritten playback log remains supported only by its expressly cited operator record. Physical calibration was NOT RUN.

Each following case is one 300-second run on this DUT/reference-peer pair. Direct sample equality covers only the taps' overlap. The timed ratio and Direction B INTERNAL mismatch control were NOT RUN. Printed precision, field skips and desk controls are not calibrated hardware or release proof. #645 and the remaining #629 acceptance stay open.

The author's exact-head source evidence records 14 successful entries, including two environment-version checks, at `gates/r5/results.json`; these are captured in the independent audit. No manager source bank ran at this head, and none is claimed or inferred. Hosted checks were not polled in this round. Hosted and local workflow acceptance remain the manager's responsibility; a skipped context is not an executed job.

No source fixes, commits, pushes, GitHub writes, author contact, hardware access, shared installs, privilege, full banks or local workflow replica occurred. Final verification confirms the exact head/tree, tracked blob bytes and modes, index entries and the three required registered submodule pins.

The manager must publish this packet, obtain correction and independent re-review of F1's affected lenses, secure both required positive reviews and ensure no review remains in flight. This report does not authorize merge. At the merge turn, validate the candidate combining the corrected lane from source base `c20c85bd` with then-current dev (provided tip `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`), run the required builder/native banks and link exact-candidate receipts. Source validation here does not validate that future merge candidate. Hosted/local workflow acceptance, maintainer authorization and post-merge containment remain pending.

R625-5 FINISHED
