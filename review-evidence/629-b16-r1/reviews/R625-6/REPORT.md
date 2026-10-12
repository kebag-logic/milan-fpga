[R625] NEGATIVE - exact head e91a62ee266e182a804ca1f45a0f18f715096563

Round R625-6, external independent review of issue #629 / PR #725.
Tree: `f35f3e423e4b6a744b44f124a9281fb0f413d0e7`.
Comparison: `c20c85bd..e91a62ee266e182a804ca1f45a0f18f715096563`.

All five lenses were applied. One new MINOR remains: comment normalization can erase a visible unit, allowing an unsupported measurement to pass as an identifier. Conformance, Robustness, Tests and Docs are UNCLEAN; RTL is CLEAN. No incorrect current bench figure or new DUT defect is alleged.

The nine commits change only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`. The measured image is dev `5603c353`, distinct from this documentation head. The current figures reproduce: 1,790 receipt rows match, and the unchanged page reports 13,849 digits with zero uncovered. That result does not establish the check's protection against new unsupported measurements.

## Scope and evidence

Reconstructed operating rules, the documentation map, the [issue contract](https://github.com/kebag-logic/milan-fpga/issues/629), the [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), the [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), the [B16c exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), and the documents-only scope through [round 6](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126774639). Then examined repository authorities, complete diff/history and public executable evidence. Prior public findings were consulted after the independent diff pass. No current-round peer report or private author material was used.

Authorities examined include `REQUIREMENTS.md:309`, FR-CLK-03/04 at `docs/reference/FR_NFR.md:252`, the clause discussion and bench contract in `docs/design/MEDIA_CLOCK_FOLLOWING.md:1661`, media ownership at `docs/overview/ARCHITECTURE.md:72`, and slip/meter/servo interfaces at `docs/reference/REGISTER_MAP.md:1870`, `:2082` and `:2139`.

Evidence paths prefixed `author-r6/` refer to the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/b616e7ea76e375940886f0853b24470bb8efe6ec/review-evidence/629-b16-r1). All 647 author-r6 publication hashes verify; 41 files have declared path redactions. The six earlier probe scripts are byte-equal to their original published scripts, verified directly against the evidence commit. Local scripts and receipts below are relative to this report.

## R625-6-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifacts:** `author-r6/tools/check_b16_figures.py:2628` through its comment-removal branch; `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3858`, `:3870`; `docs/findings/README.md:15`; PR #725 body, Round 6 item 2. Reproduction changes only a disposable copy of the attribution-summary row at findings line 3011.

**Authority/evidence:** round 6 requires normalization before matching while preserving source lines, and permits an identifier only before the closed follower list. A unit, including an unlisted unit, must require a receipt row. The page says the check reads the text as a reader sees it.

The normalizer treats every `<!--` as extending to the next literal `-->`. The repository's pinned Markdown and HTML parsers instead terminate the short forms `<!-->` and `<!--->` immediately. Thus the following source leaves `CLOCK_DOMAIN 7ppm.` visible:

```text
CLOCK_DOMAIN 7<!-->ppm<!-- -->.
```

The checker reduces it to `CLOCK_DOMAIN 7.`. The full stop qualifies the descriptor index, and the added 7 receives no receipt row. The same happens with `<!--->`, and with `furlongs` instead of `ppm`.

| Disposable insertion at line 3011 | Visible text | Check exit | Result |
|---|---|---|---|
| None | Unchanged page | 0 | 1,790 matching rows, zero uncovered |
| `CLOCK_DOMAIN 7 ppm.` | `CLOCK_DOMAIN 7 ppm.` | 1 | 7 named UNCOVERED |
| `CLOCK_DOMAIN 7<!-- -->ppm.` | `CLOCK_DOMAIN 7ppm.` | 1 | 7 named UNCOVERED |
| `CLOCK_DOMAIN 7<!-->ppm<!-- -->.` | `CLOCK_DOMAIN 7ppm.` | 0 | 7 covered as descriptor index |
| `CLOCK_DOMAIN 7<!--->ppm<!-- -->.` | `CLOCK_DOMAIN 7ppm.` | 0 | 7 covered as descriptor index |
| `CLOCK_DOMAIN 7<!-->furlongs<!-- -->.` | `CLOCK_DOMAIN 7furlongs.` | 0 | 7 covered as descriptor index |

Each false pass retains all 1,790 matching rows, reports 13,850 digits, assigns 2,405 digits to 1,187 identifier spans, and reports zero uncovered. No receipt or checker byte was altered. Full-page rendering confirms that the unit remains visible in the actual table, not just in an isolated fragment. Renderer dependencies were installed from the repository's hash-locked requirements into a disposable environment.

Evidence: [rendered-comment.json](receipts/rendered-comment.json), the six `receipts/rendered-*.log` files and their return-code files. The receipt records source text, normalized text, rendered HTML, visible text, full-page context, coverage categories and checker output.

**Impact:** the normalization step itself hides a measurement from both the unit guard and the closed follower rule. Complete digit accounting can therefore produce a false pass. The current bench figures remain supported. This is executable validation behavior and an evidence claim, so it is not wording-only RESIDUE.

**Required outcome:** normalization must preserve this rendered unit or refuse the unsupported source form. Both short-comment forms, including the unlisted-unit variant, must fail and identify the added digit at its source line. Add standing controls for this boundary; retain the unchanged page, existing controls and earlier probes. Narrowing the prose alone does not meet the assigned normalization rule.

**Verification:** run `scripts/probe_rendered_comment.py REPO AUTHOR_PACKET OUTPUT` with the pinned documentation interpreter. At this head it reproduces checker statuses `[0, 1, 1, 0, 0, 0]`. The corrected behavior must be `[0, 1, 1, 1, 1, 1]`; the reproducer's final assertion deliberately records the present defect and must then be updated for the correction. Re-review the corrected check and documentation.

## Independent results

**Conformance:** the staged STOP/resume sequence matches the assignments. `author-r6/summary/loop2/acmp-peer-tap.json` contains two unanswered CONNECT_TX/PROBE_TX commands 200 ms apart. Both loopback runs contain zero peer-stream frames. B16b stopped before circular following; B16c used the authorized peer INTERNAL exception only for the two following cases. The page, index and PR body distinguish observed attribution inside the taps from inference beyond them. The INTERNAL mismatch control and lane B6 timed-ratio term remain NOT RUN, and #629 remains open. F1 leaves the documents-only validation requirement unmet.

**RTL:** the complete two-file diff introduces no RTL, firmware, configuration, generated image, interface or gitlink change. Compared receipt decoding with the register map: state 4 is LOCKED, signed trim uses 1/16 ppm, AAF/CRF rates use 512 units per ppm, and `0x001e0007` means enabled/valid/locked with zero history restarts and 30 ns largest deviation. No new RTL execution or silicon proof is claimed.

[R625] PASS RTL - `docs/overview/ARCHITECTURE.md:72`, `docs/reference/REGISTER_MAP.md:1870`, `:2082`, `:2139`, and the complete `c20c85bd..e91a62ee` two-file diff - checked measurement decoding and unchanged architectural/interface ownership.

**Robustness:** inspected `author-r6/tools/run_b16c.py:523`, `:706`, actual controller/event transcripts, `controls/b16c-dryrun-*.json` and the wrapper deadline receipt. They cover refused selection, missing lock, playback-busy refusal, controller loss, deadline teardown and restoration order. These historical bench-operation controls were inspected, not rerun. Independently checked all eight actual SETs against successful matching GET source fields, all three restore censuses, the failed loopback, and exclusion of the empty busy-capture incident. F1 concerns malformed-comment handling in the executable figure check.

**Tests:** [receipt-audit.json](receipts/receipt-audit.json) independently recomputes B0 block classification and medians, the 23/108 overlap split, positive-control playback-only counts, poll state/extrema/slip transitions, source-read hash bindings, clock SET/GET pairs and census comparisons. B0's reduction regenerates byte-equal. The full checker passes, and both outputs reproduce byte-equal. Its build aid regenerates the checker byte-equal; the row-key scan finds no unused loop variable. F1 supplies a controlled false pass beyond the existing tests.

**Docs:** the page's exact B16c attribution replacement, B0 floor/run/start corrections, all four B6 terms, counter-mark wording, neutral reduced receipts, packet mapping and R624-5-R1 wording agree with their primary evidence. The findings and PR body retain limits on upstream inference, source-state comparisons and physical calibration. Documentation/privacy, style, path, contents, anchor, em-dash and whitespace checks pass. F1 invalidates the remaining rendered-text coverage claim.

Numerical cross-checks include:

- B0: 300 blocks, 169 at the floor, medians -123.98/-123.95 dB on floor blocks; all-block medians -123.95/-122.80 dB. The degraded runs split at block 45. Recording begins at about 06:38:05.2, including the two-second playback lead, about 26 seconds after binding.
- B0: 23 degraded blocks lie within the shared 34.1136-second tap overlap; 108 lie beyond it. The latter remain inferred upstream. No raw hardware capture was re-graded.
- B-CRF/B-AAF: 300/300 floor blocks, zero reported discontinuities; 596 LOCKED polls each. The state-read brackets are 2.585-3.161 and 6.602-7.180 seconds, with trace rounding below one millisecond. Trim extrema are -6.125 to -6.000 ppm; decoded slip steps agree with the reduced receipts and occur before LOCKED.
- Positive controls: 303/303 wholly playing blocks at the floor for B0 and both following cases; `pts2` has 11/13. The two silent pre-playback blocks and the transition block are excluded.
- Eight successful clock SET/readback pairs, including both restorations; each lane census has 45 reads, 44 equal, with only live propagation delay differing. Binding, format, map and source state are restored.

## Executed checks and probes

`receipts/focused-status.json`, `document-checks.json`, `extra-checks.json` and their individual logs/return codes record the runs. Independent jobs were run concurrently under foreground controllers, with no more than 16 concurrent probe jobs.

| Check | Observed result |
|---|---|
| Unchanged page | 1,790/1,790 rows; 13,849 digits; zero uncovered; outputs byte-equal |
| Rounds 3, 4, 5 and 6 standing controls | 5/5, 8/8, 22/22 and 39/39 PASS; each intended defect named |
| Unchanged R625-3 probe | 7/7 detected |
| Unchanged R624-4 and R625-4 probes | 8/8 and 12/12 detected |
| Unchanged R625-5 comment probe | `[0, 1, 1]`, campaign exit 0; source line retained |
| Unchanged R624-5 escape probe | All ruling unit forms detected; 18/19 identifier forms. Colon and three digit-free number-word forms remain the documented limits |
| Unchanged R624-5 row-3200 probe | LOCKED row MISMATCH, `bcrf 595, baaf 596`; both actual receipt files named |
| Additional published self-probes | 78 forms meet their stated expectations, including documented accepted forms |
| Independent follower probes | 22 forms recorded; declared literal/punctuation limits distinguished from F1 |
| Independent rendered-comment probe | Three unsupported visible measurements falsely accepted: F1 |
| Historical packet-location checks | 66/66 author-r3 hash rows and 76/76 author-r5 hash rows match; 592 author-r5 manifest entries match |
| Focused document gates | All pass; em-dash check reports zero findings over 1,729 added lines |

The row-3200 probe changes only the LOCKED numerator. The separate total-poll denominator correctly remains 596 and OK. Thus the literal request that both rows mismatch is not observed. The original R624-5-F1 verification explicitly permits failure at line 3200, which now occurs; the defect is resolved. A stricter demand to fail the unchanged denominator needs a manager decision, not a knowingly incorrect denominator check.

## Prior public findings at this head

Reconciled the ten prior public findings comments from rounds 1-5, inventoried in [public-state.json](receipts/public-state.json). No prior open finding is silently deferred. The new F1 above reopens the broader protection claim on a distinct normalization route.

| Prior items and attributable lenses | Disposition and primary evidence |
|---|---|
| R625-1-F1: Conformance, Tests, Docs | RESOLVED. Findings:2826,2835,3254, index:15 and PR body distinguish 23 observed blocks from 108 inferred; independent arithmetic agrees |
| R625-1-F2: Tests, Docs; R624-1-S2: Tests | RESOLVED. Public `r2/` extrema, poll traces/transitions and neutral source comparisons are raw-hash-bound; extraction at findings:3426; twelve source hashes checked |
| R624-1-F1 / R625-1-F3: Conformance, Tests, Docs | RESOLVED. Correct floor medians, split degraded runs and recording start; B0 reduction byte-equal |
| R624-1-F2 / R625-1-F4: Conformance, Tests, Docs | RESOLVED. Findings:3198 states all four B6 terms, three met and timed ratio NOT RUN, with no replacement decision |
| R624-1-R1 / R625-1-R1: Docs | RESOLVED. Live PR title uses the exact requested distinction between graded B0 and the following cases at the floor |
| R624-1-R2 / R625-1-R2: Docs | RESOLVED. Findings:3040,3095,3172 state the counter mark 20 seconds after the set, about six seconds before recording |
| R625-2-F1: Conformance, Tests, Docs | RESOLVED. Exact replacement at findings:3244; four point-(a) medians and worst blocks agree with the tap receipts |
| R624-2-F1: Robustness, Tests, Docs | RESOLVED. Playback-only positive-control counts, including the silent and transition exclusions, independently reproduced |
| R624-2-F2: Tests, Docs | RESOLVED. LOCKED brackets begin at the preceding ACQUIRE poll's start; traces and receipt endpoints agree |
| R624-2-R1/R2/R3: Docs | RESOLVED. Source-state claims bounded to shared entries; pre-set slips have qualified causes; PR body explicitly names the missing INTERNAL mismatch control |
| R624-2-S1: Docs | TAKEN. Findings:3341 records DRP mismatch bit 4 without analysis; trace decoding confirms it |
| R624-1-S1 / R625-1-S1 / R624-2-S2 / R625-2-S1 / R625-3-S1: Docs | TAKEN. Census wording is 44 of 45 reads; independent comparisons agree |
| R624-3-F1: Docs | RESOLVED. Findings:2608 gives branch/pinned mapping; historical manifest and all 66 hash rows reproduce |
| R625-3-F1: Conformance, Robustness, Tests, Docs | Original quote/link escapes RESOLVED. Unchanged probe detects 7/7; no whole-quote/whole-label exemption remains. New normalization escape is F1 above |
| R624-4-F1 / R625-4-F1: Conformance, Robustness, Tests, Docs | Original glued-unit, decimal, exponent, spacing and unbound-continuation forms RESOLVED: 8/8 and 12/12 detected |
| R624-4-S1: Docs | TAKEN. Findings:2308 points to each findings round |
| R624-5-F1: Tests, Conformance | RESOLVED. Each case read from its own receipt; row 3200 now fails the unchanged numerator mutation, with both receipts named |
| R624-5-F2: Conformance, Robustness, Tests, Docs | Original spelled-unit escapes RESOLVED. Standing controls and unchanged probe detect them. Broader protection remains unclean under new F1 |
| R624-5-F3: Docs | RESOLVED. Findings:2617 maps author-r5 to `a73ce5c4` and names author-r6; historical hashes verify |
| R625-5-F1: Conformance, Robustness, Tests, Docs | Original multiline-comment escape RESOLVED: `[0,1,1]` and correct source lines. Short-comment normalization remains open as new F1 |
| R624-5-R1: Docs | RESOLVED. Exact channel/step/round wording and issue-number category applied on the page and in the live PR body |
| R624-5-S1: Docs | TAKEN. Findings:3915 states limits and the corresponding self-probes record them |

No wording residue is newly recorded.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | Issue assignments/rulings; findings:2286,2826,3198,3320,3858; FR-CLK-03/04; checker comment normalization | R625-6 applied; not banked | e91a62ee266e182a804ca1f45a0f18f715096563 |
| RTL | CLEAN | Complete two-file diff; architecture:72; register map:1870,2082,2139; decoded poll traces and unchanged gitlinks | R625-6 | e91a62ee266e182a804ca1f45a0f18f715096563 |
| Robustness | UNCLEAN, F1 | Loopback/busy-capture events; clock transcripts; restore censuses; run_b16c.py:706; dry-run/deadline receipts; malformed-comment probes | R625-6 applied; not banked | e91a62ee266e182a804ca1f45a0f18f715096563 |
| Tests | UNCLEAN, F1 | 1,790 figure rows; grade/poll/source receipts; all standing controls and named prior probes; rendered-comment reproduction | R625-6 applied; not banked | e91a62ee266e182a804ca1f45a0f18f715096563 |
| Docs | UNCLEAN, F1 | Both changed pages; live PR title/body; packet mapping/manifests; focused document gates; coverage claims at findings:3858 | R625-6 applied; not banked | e91a62ee266e182a804ca1f45a0f18f715096563 |

## Limits and pending manager duties

This reviews published receipts and documentation. Private raw recordings, source reads and source class map were not opened; hashes bind their reductions but do not independently prove those raw bytes or physical accuracy. Historical bench-operation dry runs were inspected only. Physical calibration was NOT RUN. Field skips and documentation checks supply no hardware proof. No full source banks, hardware operation, source fix, commit, push, external write or merge was performed.

Source-head validation is the author's published `author-r6/gates/r6/results.json`: 14 entries, including two version queries, all rc 0 at the exact head. There is no manager source bank at this head. Hosted/replica acceptance remains manager-owned; this review does not claim that skipped contexts executed work.

After F1 is corrected and re-reviewed, the manager still owns independent review completion, hosted/local-replication acceptance, the final candidate against current dev, and publication of the candidate's builder/native-bank receipts. Source base `c20c85bd` and the supplied live-dev tip `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc` are distinct; no merge candidate is validated here. Merge authorization, post-merge containment and issue/project disposition remain pending. The INTERNAL mismatch control, timed ratio and #645 remain open independently of this findings PR.

[Integrity verification](receipts/integrity.json) proves exact tracked blob bytes, modes and index entries for the 1,291 root blobs and the three required initialized submodules: 562 `protocol-processor`, 104 `gptp-processor` and 214 `third_party/verilog-axis` blobs. Their gitlinks match the exact head; the working tree is clean. All mutations were confined to disposable copies. `MANIFEST.sha256` lists publishable scripts and receipts; disposable trees are excluded.

R625-6 FINISHED
