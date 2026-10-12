[R625] NEGATIVE - exact head 61ae86419c50f2707d6ee1dc5433bc6dee66ce84

Round R625-4, external independent review of issue #629 / PR #725.
Tree `ed284e802555e2e1cb92f15d95dafa2702d3fc1d`; comparison `c20c85bd..61ae86419c50f2707d6ee1dc5433bc6dee66ce84`.

All five lenses were applied. One MINOR remains in Conformance, Robustness, Tests and Docs: the figures checker silently accepts numerical spellings its tokenizer does not recognize, its unit guard can be bypassed with whitespace, and a continuation exemption lacks its claimed keyword binding. RTL is CLEAN. No DUT defect or incorrect current bench measurement is alleged.

The unchanged page passes all 1,727 receipt rows. Both generated outputs, all eight standing controls, the five older controls, checker regeneration and the packet-location receipt reproduce byte for byte. The original R625-3 probe now detects all seven mutations. Those corrections are real; the new finding concerns the remaining claim that every added measurement needs a receipt row.

**Scope and reconstruction**

Read operating rules and CONTRIBUTING.md, docs/README.md, the [issue contract](https://github.com/kebag-logic/milan-fpga/issues/629), [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), [B16c exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), and rounds [2](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763), [3](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508) and [4](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6121193402), then the linked repository authorities, complete diff/history, and public executable evidence.

Authorities examined include REQUIREMENTS.md section 8; FR-CLK-03/04 at `docs/reference/FR_NFR.md:252`; the clause discussion and Bench contract in `docs/design/MEDIA_CLOCK_FOLLOWING.md:1661`; `docs/overview/ARCHITECTURE.md:72`; and the slip, meter and servo fields at `docs/reference/REGISTER_MAP.md:1870`, `:2078`, `:2139`.

Six commits change only the findings page and index. The measured image is dev `5603c353`, distinct from this documentation head. No implementation, generated image or gitlink changes exist. The independent verdict and ledger were written before reading the six prior public findings comments. No current-round peer report or private author material was read.

Evidence paths refer to `author-r4/` in the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/b83e5d76ede6597eb9831c2a90b0a1058abc85aa/review-evidence/629-b16-r1), unless otherwise stated.

**R625-4-F1 - MINOR - Conformance, Robustness, Tests, Docs**

Artifacts: published `author-r4/tools/check_b16_figures.py:2287` (TOKEN), `:2299` (MEASURE), `:2321` (channel continuation), `:2392` (coverage); `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3642` and `:3649`. Reproduced at the attribution-summary row, line 3006.

Authority/evidence: round 4 requires measurement-bearing tokens to have receipt rows wherever they occur. The page says a token followed by a unit is a measurement and only a row can claim it. The checker first enumerates TOKEN matches and applies its measurement guard only to those matches. TOKEN requires a leading digit, does not recognize exponent notation, and suppresses number starts after a dot. MEASURE accepts at most one space, nonbreaking space or hyphen before the unit.

The numerical probes insert only a sentence into a disposable copy of the attribution row. The checker and all receipts stay unchanged:

| Added measured residual | Exit | Observed result |
|---|---|---|
| `7.25 ppm` | 1 | Correctly named UNCOVERED as a measurement |
| `"7.25 ppm"` | 1 | Correctly named UNCOVERED as a measurement |
| `[7.25 ppm](#b16c-attribution)` | 1 | Correctly named UNCOVERED as a measurement |
| `.25 ppm` | 0 | No token added; 1,874 tokens, 1,727 rows OK, zero uncovered |
| `-.25 ppm` | 0 | No token added; same false-complete result |
| `7e2 ppm` | 0 | No token added; same false-complete result |
| `CLOCK_DOMAIN 7 ppm` | 1 | Unit guard overrides the identifier category |
| `CLOCK_DOMAIN 7  ppm` (two spaces) | 0 | Token 7 becomes the 148th category exemption; zero uncovered |

The first three escaped forms are ordinary numerical measurements, not identifiers. The whitespace pair separately isolates the guard defect. `coverage-probes.json` contains all twelve probes, full stdout, statuses and the exact insertion text; `probe_coverage.py` reproduces them and exits 1 because five escape. The eight standing controls all detect their own defects, but cover neither numerical spelling, separator boundaries nor the unbound continuation below.

The identifier-category requirement also fails at checker line 2321: `^(?P<t>3) carry -1 to 0 LSB` exempts a leading 3 without checking the preceding Channels keyword. In a disposable copy, change only `Channels 2 and` at findings line 3103 to `Channel 2 reports samples:`. The following `3 carry -1 to 0 LSB` now states a count of samples, but still passes as a channel-index exemption: exit 0, unchanged token/row/category counts. The `unbound_continuation` probe records the exact replacement.

Impact: a new unsupported measurement can enter a summary while the check reports complete coverage. The current matching receipt rows remain valid. This changes executable validation and the evidence guarantee, so it is not wording-only RESIDUE.

Required outcome: measurement spellings, including leading-dot decimals, signed variants and scientific notation, must require a receipt row or be explicitly refused. Whitespace before a unit must not permit an identifier exemption to hide a measurement. Identifier exemptions must verify their keyword context, including across line breaks. Add controls that fail on these reproduced defects; preserve the baseline, existing controls and original quoted/link probes. Merely narrowing the prose claim does not meet the round's every-figure requirement.

Verification: rerun `probe_coverage.py`, the original `probe_figure_coverage.py`, the eight standing controls and the unchanged-page checker. The escaped forms must exit nonzero and identify the measurement or unsupported numerical syntax. Re-review the corrected checker and its documentation. No source fix was made in this review.

**Independent evidence by lens**

Conformance - UNCLEAN for F1. The B16 STOP/resume sequence agrees with the public decisions. `summary/loop2/acmp-peer-tap.json` shows two unanswered CONNECT_TX probes 200 ms apart. Both loopback runs have 14 unresolved listener polls, zero talker connections and no received frames. B16b grades the permitted four-point capture and stops before circular following. B16c uses the peer INTERNAL exception only for B-CRF/B-AAF. Controller transcripts independently show all eight successful SETs and matching GET fields: peer INTERNAL, DUT CRF/AAF, DUT INTERNAL, peer CRF after unbinding. All nine run-final states equal their as-found states. The INTERNAL mismatch control and timed ratio remain NOT RUN; #629 remains open.

[R625] PASS RTL - complete two-file diff; `docs/overview/ARCHITECTURE.md:72`; `docs/reference/REGISTER_MAP.md:1870`, `:2078`, `:2139`; `r2/bcrf-poll-trace.tsv` and `r2/baaf-poll-trace.tsv` - reviewed architecture and interface claims. Selection 0/1/2, servo state 4, signed trim at 1/16 ppm, stream rate at 512 units/ppm, slip fields and `0x001e0007` agree with the authorities. Both windows independently decode to 596 LOCKED polls, zero TDM slips, and the documented trim/rate extrema. AAF has zero history restarts and 30 ns maximum deviation. No implementation execution or new hardware validation is claimed.

Robustness - UNCLEAN for F1. Examined `runs/{loop1,loop2,b0}/events.jsonl`, the empty incident capture, published `controls/b16c-dryrun-summary.json`, deadline receipt, run teardown, positive-control block boundaries and both poll traces. The eight bench-run dry-run scenarios and deadline receipt were inspected, not re-executed. They document refused selection, absent lock, busy playback, wrong initial state, controller loss and deadline teardown. The failed B0 capture remains ungraded. Positive-control silence is excluded. Each following trace has five IDLE slip steps before selection, then one/two ACQUIRE steps, none after observed LOCKED. F1 is the separate fail-open numerical-input and identifier-context cases in the figures checker.

Tests - UNCLEAN for F1. `audit_receipts.py` independently recalculates per-block medians, joint floor classification, degraded ranges, overlap, positive-control counts, poll decoding and restoration. B0 has 169/300 floor blocks with medians -123.98/-123.95 dB, all-block medians -123.95/-122.80 dB, degraded runs split at block 45, and recording about 26 seconds after binding. Of 131 degraded blocks, 23 fall inside the whole-block overlap and 108 beyond it. Both following cases have 300/300 floor blocks and zero reported discontinuities, with -123.98/-123.97 dB medians at (c). At (a), the four medians reproduce the exact R625-2 replacement. Direct sample equality is limited to the documented 34.1-34.3-second overlaps. The full 300-second output grade is distinct evidence.

Docs - UNCLEAN for F1. Examined findings lines 2284-3696, index line 15, live PR title/body, publication mapping, hashes, extraction procedures, author gate receipts and privacy. The findings, index and PR body consistently distinguish measured B0 overlap from later inference. Source routing and clock changes are attributed outside the lane. The source-state comparisons retain their common-entry limits. The reference peer and external capture are named by role; the added text has no identifying host paths. The documentation hygiene check reports zero findings. F1 prevents accepting the advertised complete measurement guard.

**Prior public findings, disposition at this exact head**

Read [R624-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428), [R625-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570), [R624-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119878041), [R625-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119899949), [R624-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121093801) and [R625-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121186527) only after the independent verdict/ledger. The inspected public inventory contains zero formal reviews and zero inline comments.

| Prior item and attributable lenses | Disposition and checked evidence |
|---|---|
| R625-1-F1: Conformance, Tests, Docs | RESOLVED. Findings:2823,2835,3254; index:15; PR body keep 131 at (c), 23 within the sample comparison and 108 as inference. `receipt-audit.json` recalculates the split and ranges. |
| R625-1-F2: Tests, Docs; R624-1-S2: Tests | RESOLVED. Public `r2/` receipts expose extrema, timestamped slip transitions/states and neutral source comparisons. Both 710-row traces were decoded; raw poll/event hash bindings and all twelve source-read hashes checked. Extraction procedure remains published at findings:3462. Private source reads/map were not regenerated. |
| R624-1-F1: Conformance, Docs; R625-1-F3: Conformance, Tests, Docs | RESOLVED. B0 floor medians -123.98/-123.95, ranges 43-44 and 46-54, recording launch plus two seconds, about 26 seconds after binds. Per-block records and events agree. |
| R624-1-F2: Conformance, Docs; R625-1-F4: Conformance, Tests, Docs | RESOLVED. Findings:3192-3202 state all four B6 terms: three met, timed ratio NOT RUN, no replacement decision. Acceptance, limits, index and PR body preserve this distinction. |
| R624-1-R1 / R625-1-R1: Docs | RESOLVED. Live title equals the requested replacement distinguishing B0 grading from the following cases at the floor (`public-state.json`). |
| R624-1-R2 / R625-1-R2: Docs | RESOLVED. Findings:3035,3090,3167 identify the first counter mark 20 seconds after selection, about six seconds before the recording; header says before the window and near its end. |
| R625-2-F1: Conformance, Tests, Docs | RESOLVED. Findings:3239 contains the exact replacement. Independent medians at (a) are -123.98/-123.97 for B-CRF and -123.98/-123.98 for B-AAF; each worst block rounds to -123.93. |
| R624-2-F1: Robustness, Tests, Docs | RESOLVED. Positive-control counts exclude pre-playback blocks 0/1 and transition block 2: 303/303 wholly playing blocks for B0/B-CRF/B-AAF and 11/13 for pts2. The figures check also covers the two pts2 taps' 15 wholly playing blocks per tone. |
| R624-2-F2: Tests, Docs | RESOLVED. Findings:3170-3181, summary, index and PR body use 2.585-3.161 and 6.602-7.180 seconds, from the last ACQUIRE poll's start to the first LOCKED poll's end. Trace records bound the state read. |
| R624-2-R1: Docs | RESOLVED. Findings:2779 and 3256 limit source comparisons to 1,255 common entries and the 618/668 common entries around B16c. |
| R624-2-R2: Docs | RESOLVED. Findings:3209-3213 say the pre-set slips are consistent with clock difference and, for the first, a bind slip; receipts do not separate the causes. |
| R624-2-R3: Docs | RESOLVED. PR body names Direction B's INTERNAL mismatch control explicitly and explains why it did not run. |
| R624-2-S1: Docs | RESOLVED. Findings:3336 records servo bit 4, DRP config mismatch, as observed but not analysed. |
| R624-1-S1 / R625-1-S1 / R624-2-S2 / R625-2-S1 / R625-3-S1: Docs | RESOLVED. Census wording is now 44 of 45 reads, excluding the header. Independent comparisons of each lane and B16 start to B16c end confirm it; only the live AVB propagation-delay read differs. |
| R624-3-F1: Docs | RESOLVED. Findings:2603 names branch, pinned commit, author-r1/r2/r3 directories and the later author-r4 publication. The actual first directory is author-r1, correctly differing from the assignment's shorthand author. Pinned MANIFEST.json has the stated hash and 1,680 entries; all 66 table rows agree with published author-r3 bytes. Receipt regeneration is byte-equal. |
| R625-3-F1: Conformance, Robustness, Tests, Docs | Original quoted/link escapes RESOLVED. No whole-quote or whole-link-label exemption remains. Original probe, unchanged, now detects all seven cases. Eight standing controls detect their respective defects. The broader every-measurement guarantee remains UNCLEAN under the distinct lexer/unit-boundary/identifier-context defect R625-4-F1. |

No prior wording residue remains. F1 above is the only open finding from this round.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue/rulings; findings:3006,3192,3649; B6 terms; controller exchanges and restores; coverage probes | R625-4 applied; no clean coverage | 61ae86419c50f2707d6ee1dc5433bc6dee66ce84 |
| RTL | CLEAN | Full two-file diff; architecture:72; register map:1870,2078,2139; both poll traces; required gitlinks | R625-4 | 61ae86419c50f2707d6ee1dc5433bc6dee66ce84 |
| Robustness | UNCLEAN: F1 | Checker numerical boundaries; failed-run records; control silence; poll bounds; nine restores; published dry-run/deadline receipts | R625-4 applied; no clean coverage | 61ae86419c50f2707d6ee1dc5433bc6dee66ce84 |
| Tests | UNCLEAN: F1 | Figure rows; eight standing controls; original seven probes; twelve new probes; independent receipt arithmetic | R625-4 applied; no clean coverage | 61ae86419c50f2707d6ee1dc5433bc6dee66ce84 |
| Docs | UNCLEAN: F1 | Findings and index; live PR title/body; packet-location receipt; manifests; coverage claim; hygiene check | R625-4 applied; no clean coverage | 61ae86419c50f2707d6ee1dc5433bc6dee66ce84 |

**Executed verification and portable reproduction**

| Check | Result and receipt |
|---|---|
| Published figure checker | rc 0; 1,727 rows OK, 1,874 tokens, 147 category tokens, zero uncovered; `figures-check.log`, `figures-rows.tsv`, `figures-coverage.tsv` |
| Round-4 controls | 8/8 PASS; each mutated check exits 1 for the named defect; `r4-controls.json` |
| Round-3 controls, unchanged | 5/5 PASS; `r3-controls.json` |
| Original R625-3 probe, unchanged | 7/7 detected; `receipts/figure-coverage-probes.json` and per-probe logs |
| New coverage probes | Seven rejected, five accepted incorrectly; campaign rc 1; `coverage-probes.json` and `.log` |
| Independent receipt audit | PASS; block arithmetic, overlap, playback counts, poll words/extrema, raw-hash bindings, source comparisons, loopback, eight controller readbacks and restore censuses; `receipt-audit.json` |
| Checker regeneration and location receipt | Byte-equal; `rebuild.log`, `packet-location.json`, `execution.json` |
| Publication hashes | PASS: 471/499/526/556 files across author-r1/r2/r3/r4, and all 555 inner author-r4 manifest rows; declared path-redaction differences reconcile; `publication.json` |
| Documentation hygiene and diff whitespace | rc 0; `docs-check.log`, `diff-check.log` and rc files |
| Tracked bytes, modes, indexes and required pins | PASS: 1,291 parent blobs and 880 required-submodule blobs; `integrity.json` |

To reproduce, obtain author-r4 from the pinned public evidence commit and retain the source history. Invoke `run_checks.py REPO AUTHOR_R4 REVIEW_PACKET` in the foreground. It runs at most four independent checks concurrently, waits for every child, and uses only REVIEW_PACKET/scratch for disposable files. At this head its expected overall result is nonzero because the independent coverage campaign exposes F1. The original R625-3 probe is preserved byte-for-byte. `verify_checkout.py` is the prior portable integrity checker with only the expected head/tree advanced. The hygiene check is `python3 scripts/docs_check.py` at the candidate root.

The audit initially counted polls by start alone; its final window rule requires the entire poll inside the window, consistent with the published extraction contract. The publication audit normalizes the inner manifest's leading ./ before lookup. These were review-harness setup corrections, not candidate defects. No candidate bytes were edited. All executed commands completed in foreground calls; the peak independent batch was four checks.

**Real limits and pending manager duties**

Raw audio/tap recordings, full raw polls, source reads/class map and playback logs were not accessed. Published summaries and reduced traces were checked; raw-inventory agreement binds citations but does not rehash unavailable captures. Source-role classification still depends on the published reduction. B16b's overwritten playback log remains supported only by its expressly cited public operator record. Physical calibration was NOT RUN.

Each following case is one 300-second run on this DUT/reference-peer pair. Sample equality covers only the taps' overlaps. The timed ratio and Direction B INTERNAL mismatch control were NOT RUN. Printed precision, field skips and desk controls provide no calibrated hardware or release proof. #645 and the remaining #629 acceptance stay open.

`author-source-gates.json` records the author's exact-head source evidence: 14 successful entries, including two environment-version checks. No manager source bank ran at this head, and none is claimed or inferred. Hosted checks were not polled in this round; hosted/local workflow acceptance remains the manager's responsibility. A skipped context is not an executed job or physical proof.

No source fixes, commits, pushes, GitHub writes, hardware access, shared installs, privilege, full banks, simulator execution or local workflow replica occurred. Final integrity confirms the exact head/tree, tracked bytes, file modes, indexes and the three required submodule pins.

The manager must publish this packet, obtain correction and independent re-review of F1's affected lenses, secure both required positive reviews, and ensure no review remains in flight. This report supplies no merge authorization. At the merge turn, validate the candidate combining the corrected lane from source base c20c85bd with then-current dev (provided tip c6bd08c6f52632c6d33d834ce842ac3cf63f29cc), run the required builder/native banks and link exact-candidate receipts. Source evidence here does not validate that future candidate. Hosted/local workflow acceptance, maintainer merge authorization and post-merge containment remain pending.

R625-4 FINISHED
