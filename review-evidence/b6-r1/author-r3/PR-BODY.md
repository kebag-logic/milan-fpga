[A477] Record #629's bench acceptance: media-clock following graded by THD+N

## Contents

- **[Status](#status)**: ready for review, three docs commits, `b6-bench-1001` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)**: relates to #629; executors and reviewers.
- **[Description](#description)**: the findings page, its index row and the per-case results.
- **[Round 2](#round-2)**: how each round-1 finding and suggestion is answered, and the evidence.
- **[Round 3](#round-3)**: the archive re-pin, the round-2 findings and suggestions, and the evidence.
- **[Authoritative references](#authoritative-references)**: the Milan and IEEE 1722.1 clauses and AES17.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and the evidence archive commit.
- **[How to validate](#how-to-validate)**: the gates, the table identity check and the commands that regenerate the tone and the tool controls.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what is not measured and why.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

Ready for review. Three commits on `ea3fb388`, `b6-bench-1001` -> `dev`, documentation only:

- `b5e9242e`, round 1: the page and its index row;
- `e3f28f2f`, round 2: the page revised for the round-1 findings. No table, rule, figure or verdict changes;
- `26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778`, round 3: the page revised for the round-2 findings and re-pinned to the evidence archive at `422dcf91`. No table, rule, figure or verdict changes.

Every gate below rc 0 at `26dfc82f`.

## Linked Issue / roles

Relates to #629 (its bench-acceptance item, for the sources this image offers; the DUT following an AAF stream is #629's own work and not in this image).

Executor: `[A477]` (bench lane B6, round 1); `[A480]` (round 2, docs only); `[A481]` (round 3, docs only)
Internal cleared-context reviewer: `[R426]`
External reviewer: `[R427]`

## Description

- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (new): the bench acceptance of #629. It holds the method, the tool controls, the binding rule and clock-source record, the per-case tables of THD+N, SNR, frequency offset and discontinuities, the frame-rate ratio, the capture-path losses, the bench as left, the limits and the artifact hashes.
- `docs/findings/README.md`: its index row.

No other file changes.

### Results

| Case | Blocks at the floor | Listener discontinuities | DUT beat repeats | McASP0 to peer ratio, counted, ppm | Timed, ppm | Result |
|---|---|---|---|---|---|---|
| Tool controls (synthetic) | - | every planted defect found at its frame and size | - | - | - | PASS |
| A0, the reference peer as found (control) | 54 of 629 | 519 drops, 1 silent insert | 321 | +6.519 | +6.44 +-0.72 | PASS as a control |
| A1, the peer follows the DUT's AAF stream | 291 of 617 | 0 | 315 | -10.631 | -12.19 +-2.44 | PASS |
| A2, the peer follows the DUT's CRF stream | 1 of 616 | 494 drops, 180 silent inserts | 316 | -0.068 | -0.59 +-1.24 | FAIL |
| B INTERNAL, the DUT on INTERNAL (control) | 57 of 629 | 506 drops, 1 silent insert | 322 | +6.052 | +6.85 +-1.46 | PASS as a control |
| B CRF, the DUT follows the peer's CRF stream | 611 of 629 | 0 | 0 | 0.000 | -0.01 +-0.65 | PASS |

- Blocks at the floor read THD+N -146.06 dB and SNR 146.07 dB at 997 Hz, and -145.99 dB and 145.99 dB at 9,973 Hz, in every case.
- A2 fails because at INTERNAL the DUT's AAF stream runs on the free-running 48 kHz packet grid, 10.64 ppm off the physical audio clock its CRF talker publishes. A listener that follows the DUT's CRF drops one frame per beat. Its root cause is tracked on #74.
- Direction B's THD+N is NOT RUN: the reference peer's talker channels carry 0 to 2 LSB, not a known signal.
- The DUT's AAF following is not in this image.

## Round 2

Executor `[A480]`, under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5932539168), answering [R426-1](https://github.com/kebag-logic/milan-fpga/pull/630#issuecomment-5932376922) and [R427-1](https://github.com/kebag-logic/milan-fpga/pull/630#issuecomment-5932505979). Docs only, no bench access. One commit, `e3f28f2f`, changing only the findings page. No rule, verdict or measured figure changes, and every table on the page is byte-identical to `b5e9242e` (15 of 15).

| Finding | Where answered on the page | What it states |
|---|---|---|
| R426-1 F1, R427-1 F2: attribution blind spots | Method, "What the attribution can absorb"; The capture path; Limits | The five ways the rules can hide a listener event: a one-frame drop merged with a capture loss; a repeat within 50 frames of a beat tooth; a capture-loss-sized skip after a read gap with no loss measured; a 2-to-48-frame skip with no stall; the gap-only branch. For each, the data check for A1 and B CRF. A0's 1,165-frame and A2's 109-frame skips are 48 n + 13, possibly merged listener drops, so those listener counts may each be one low |
| R426-1 F2, R427-1 F1(a): B CRF window start | Method, "Cases" | The window opened 20.5 s after the clock-source set, under the same 20 s rule as every case, which was 14.0 s after the servo first read LOCKED |
| R426-1 F3, R427-1 F1(b): read-time exceptions | The capture path | The 2.7 ms and 177 ms exceptions are A2 DUT beat repeats. Listener events reach at most 1.0 ms with no exception; 135 of A2's 674 listener events (497 of 520 in A0, 485 of 507 in B INTERNAL) have a measurable rise |
| Archive pointer (assignment item 4) | Artifact hashes, "Where the packet is" | Branch `b6-review-evidence` at `ff542b62ae79f283b80b7945dd76110f986b0737`; `b6-a477` is `review-evidence/b6-r1/author/`; masked files' hashes are the originals' `original_sha256`; the two reproduction commands |
| R426-1 S4, R427-1 S3: A2 tracking and the DRP bit (item 5) | A2 section; Limits | A2's root cause is tracked on #74 (comment 5932380322). The DRP config mismatch bit is observed and not analysed, recorded on #74 (comment 5932538721) |

Suggestions:

- R426-1 S1 (17.1 or 17.2 ppm): done in the A0 prose. The 519 drops are 17.2 ppm; the verdict table's 17.1 ppm is net of the one silent insert. The table cell is unchanged, to keep the tables byte-identical.
- R426-1 S2 (three smoke runs): done, Method, "Shakedown runs".
- R426-1 S3, R427-1 S2 (LOCKED rests on three reads): done, B CRF prose: 5 s, 315 s and 615 s into the window, with `SLIP_TDM` static.
- R426-1 S5, R427-1 F3 (PR body in the template): already handled by the manager; kept.
- R427-1 S1 (a control for a 3 dB band error): answered on the page, Tool controls. A 48,000-point DFT of the loop, independent of the tool, gives the published floor within 0.0001 dB, and the analytic 24-bit floor is -146.05 dB. A 3 dB band error would show against both. No control was added to `b6_thdn.py`: the tool and `controls.json` are hashed evidence of the graded runs.
- R427-1 S2: `KL_crf_tx.sv` named beside the datapath port comment; lane B5's 16.46 ppm with a link to PR #628 (its page is not on `dev`, so it is not linked as a path); the bridge legs stopped by process ID and restarted, in Method; the comb residual "within 1.82 frames".

Round-2 evidence (packet `b6-a480`: tools and receipts; all inputs are the round-1 packet, the archive at `ff542b62` and the raw files the page lists by SHA-256):

- `attribution_checks.py`: per case, every capture-path skip by size modulo 48, beat-member spacing and distance to capture losses, where each missing tooth falls, the spoiled-rise and gap-only clusters, the clusters under 98 frames, the share of read positions that meet the 11 ms gap test, and the read-time rise counts.
- `window_check.py`: each window's start against its last bind or set, and the in-window servo reads.
- `floor_check.py`: the floor by DFT and analytically, without the tool.
- `archive_check.py`: 291 of 291 archive files re-hash to `published_sha256`; 54 of 54 page hashes resolve (33 `original_sha256`, 12 of them label-masked; 21 `RAW-ARTIFACTS.json`).
- `table_identity.py`: 15 of 15 tables byte-identical, none added or removed.
- A scan of the diff, the page, the commit message and the packet for private names and capture-layout tokens: 0 hits.

## Round 3

Executor `[A481]`, under the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5933253532), answering [R426-2](https://github.com/kebag-logic/milan-fpga/pull/630#issuecomment-5933241034) (two MINOR). [R427-2](https://github.com/kebag-logic/milan-fpga/pull/630#issuecomment-5933242529) is POSITIVE. Docs only, no bench access. One commit, `26dfc82f`, changing only the findings page (+44 / -18). No rule, verdict or measured figure changes, and every table on the page is byte-identical to `e3f28f2f` and to `b5e9242e` (15 of 15).

| Item | Where answered on the page | What it states |
|---|---|---|
| 1. Re-pin the archive (R426-2 F1, resolved in the archive by the manager) | Artifact hashes, "Where the packet is" | Branch `b6-review-evidence` at `422dcf91008a09cb882dcc2b760779ce22e530cd`, and both reproduction commands at that commit. Rerun from that commit alone: the tone loop hashes to `566d3dfa...5588`, and `b6_thdn.py controls` is byte-identical to `controls.json` (`cmp` silent, ALL_PASS). All 54 page hashes resolve there |
| 2. R426-2 F2(a): item 4 | Method, "What the attribution can absorb", item 4 | Six of A1's and B CRF's seven clusters under 98 frames have a measured rise of 0.99 to 1.00 ms. The seventh, A1's 60-frame skip after a 33 ms read stall (cluster 9), has no measurable rise. It passed on the read gap alone, the gap-only branch of item 5 |
| 2. R426-2 F2(b): the capture-path bullet | The capture path | Gap-only clusters, whose rise is unmeasurable: 1 in A0, 2 in A1, 5 in A2, 3 in B INTERNAL and none in B CRF, every skip still 48 n + 12. A2's clusters 17 and 56 have a measured rise that does not match (154.5 ms for 60 frames, -155.8 ms for 1,020 frames). They passed on the read gap and size rule, item 3 |

R426-2 suggestions, all taken:

- S1 (a sixth way): Method, item 6. A multi-frame listener step within 300 ms of a capture loss joins its cluster, and the rise tolerance there is about 249 ms at A1's 12.4 s loss. In A1 and B CRF, item 1's per-step sizes exclude it: every member step is 48 n + 12 or an exact stale-replay edge, or it is the 12.4 s loss's own 18,626 frames, the only step in its cluster. A one-frame event never joins a cluster. Limits now says six ways.
- S2 (fresh clone): the page says to run the commands in a fresh clone or a disposable worktree, because the checkout writes the archive into the working tree and stages it. It records the versions they were reproduced with, Python 3.14.7 and NumPy 2.5.3, and says that the original run's versions were not recorded.
- S3 (the round-2 packet): the page maps `b6-a480` to `review-evidence/b6-r1/author-r2/` at `422dcf91`. Its `floor_check.py` repeats the floor check from the archive alone (rerun this round, output identical to its receipt). Its `attribution_checks.py` reads the raw files, so the gap share is checkable through its receipt.
- S4 ("each run's"): now "each graded case's `events.jsonl`", which matches the twelve.

R427-2's suggestions were not in this round's assignment. S1 is R426-2 F2(a), done above, and S4 is answered by R426-2 S3 here and on the page. S2 (the residual at the 12.4 s loss's edge as up to about 1 ms, not one frame) and S3 (a fourth, actionless lock window) are retained, because they are outside this round's assignment. Item 6 now names S2's related note about steps grouped into a cluster.

Round-3 evidence (packet `b6-a481`: tools and receipts; inputs are the archive at `422dcf91`, read with `git show` and `git archive` only):

- `round3_checks.py`: the facts behind items 4 and 6 and the capture-path bullet, from the published `summary/<case>/grade.json` and `events.csv`. RESULT PASS.
- `archive_check.py`: 400 of 400 manifest files re-hash to `published_sha256`, with no file unlisted or missing. 54 of 54 page hashes resolve: 33 to `original_sha256` (12 of them label-masked) and 21 to `RAW-ARTIFACTS.json`. The grade tool's `original_sha256` is still the page's `386ac2a6...`.
- The reproduction at `422dcf91`, as in item 1. R426-2's mask check at `422dcf91` reports RESULT CLEAN, and a capture-layout scan of `review-evidence/b6-r1` there finds no layout literal.
- `table_identity.py` and a `cmp` of every table line: all 15 tables are byte-identical at `b5e9242e`, `e3f28f2f` and `26dfc82f` (161 lines, sha256 `540ab528...d847`).
- A scan of the diff, the page, the commit message and the packet for private names and capture-layout tokens: no private name (see the packet's `receipts/token-scan.txt`).

## Authoritative references

- Milan v1.2 5.3.3.6 (the CLOCK_SOURCE set of a CLOCK_DOMAIN), 7.2.2 (the CRF Media Clock Input), 7.2.3 (the CRF Media Clock Output), 5.4.2.15 and 5.4.2.16 (SET/GET_CLOCK_SOURCE).
- IEEE 1722.1-2021 7.2.9 (CLOCK_SOURCE), 7.2.32 (CLOCK_DOMAIN), 7.4.23.1 (SET_CLOCK_SOURCE).
- AES17 (the THD+N measurement band, 20 Hz to 20 kHz).
- The owner decisions recorded on #629 (the listener follows a talker's AAF or CRF media clock, one source selected at a time; THD+N as the grade).

## How to get into the same state

```sh
git fetch origin b6-bench-1001 b6-review-evidence
git checkout 26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778
# Evidence: branch b6-review-evidence, review-evidence/b6-r1/author/ at 422dcf91008a09cb882dcc2b760779ce22e530cd
# (the lane packet labelled b6-a477; files the archive label-masked carry their unmasked original's hash as
#  original_sha256 in review-evidence/b6-r1/MANIFEST.json, and the page cites those originals).
# The round-2 packet b6-a480 is review-evidence/b6-r1/author-r2/ at the same commit.
```

## How to validate

```sh
# 1. Docs and repository gates at the head (Markdown gates in the pinned environment; all rc 0):
git checkout 26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_em_dash.py --base ea3fb388
python3 scripts/check_doc_paths.py
python3 scripts/ci_scope.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_feature_status.py --self-test
git diff --check ea3fb388 HEAD

# 2. Rounds 2 and 3 changed no table: every table line is identical to round 1.
git show b5e9242e:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md > /tmp/b6-r1.md
git show e3f28f2f:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md > /tmp/b6-r2.md
git show 26dfc82f:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md > /tmp/b6-r3.md
grep '^|' /tmp/b6-r1.md > /tmp/b6-r1-tables.txt
grep '^|' /tmp/b6-r2.md > /tmp/b6-r2-tables.txt
grep '^|' /tmp/b6-r3.md > /tmp/b6-r3-tables.txt
cmp /tmp/b6-r1-tables.txt /tmp/b6-r2-tables.txt
cmp /tmp/b6-r1-tables.txt /tmp/b6-r3-tables.txt

# 3. Evidence: regenerate the tone loop and the analysis tool's synthetic controls, and compare.
# Run this in a fresh clone or a disposable worktree: the checkout writes the archive into the
# working tree and stages it.
git checkout 422dcf91008a09cb882dcc2b760779ce22e530cd -- review-evidence/b6-r1   # from branch b6-review-evidence
cd review-evidence/b6-r1/author/tools
python3 b6_tone.py /tmp/b6-loop.bin && sha256sum /tmp/b6-loop.bin   # the page's tone-loop hash, 566d3dfa...
python3 b6_thdn.py controls /tmp/b6-controls.json && cmp /tmp/b6-controls.json ../controls/controls.json
```

Expected result / pass criteria:
- every command rc 0, every `cmp` silent, and the tone hash equal to the page's;
- every figure on the page traces to `summary/<case>/grade.json`, `events.csv` and `blocks.csv`;
- every hash on the page resolves to an `original_sha256` in `review-evidence/b6-r1/MANIFEST.json` or to a raw artifact in `RAW-ARTIFACTS.json`. The raw captures stay on the bench host.

## Known limitations / out of scope

- The figures come from the lane packet `b6-a477`: `summary/<case>/grade.json`, `events.csv` and `blocks.csv`, rendered by `tools/b6_tables.py`. The raw captures stay on the bench host, indexed by size and SHA-256.
- The attribution of each discontinuity to the capture path, the DUT's beat or the listener is defined on the page. Each case's `events.csv` holds every event with its evidence.
- The attribution was refined while grading, and each change was applied to every case. Under the rule as first written, A1 and B CRF would fail on 4 and 3 multi-frame events. Each of those lies in a capture-path cluster whose read-time rise matches its loss. The page's Method states the history ("How the attribution was refined").
- The attribution can absorb a listener event in six ways, stated on the page with the checks that exclude each in A1 and B CRF. The one exception is a one-frame drop at the very edge of A1's 12.4 s loss, which lost audio would hide anyway. A0's and A2's listener drop counts may each be one low.
- The A2 diagnosis rests on the measured rates, on `hdl/ieee1722/crf/KL_crf_tx.sv`, `hdl/milan/milan_datapath.sv:445` and `docs/design/TIME_SYNC.md`. No CRF timestamp was captured on the wire. Its root cause is tracked on #74.
- Residuals: DUT NVM commits went from 2 to 8. Two of the reference peer's talker states keep stream parameters with connection count 0.
- Direction B THD+N is NOT RUN: no known signal reaches the reference peer's talker channels without a wiring change. Direction B clock following is graded by the frame-rate ratio of the two hardware-clocked captures instead.
- The DUT following an AAF stream is not in this image (#629's work).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench item for the sources this image offers; #629 stays open)
- [x] New or changed behavior has self-checking tests (the analysis tool's synthetic controls)
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment (posted for `b5e9242e`; due again at `26dfc82f`)
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

