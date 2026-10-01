[R427] POSITIVE - exact head e3f28f2f69343b54844ddfea368ef4cdd03facb6

# R427-2: external review of PR #630 (issue #629, bench lane B6), round 2

- **Head under review:** `e3f28f2f69343b54844ddfea368ef4cdd03facb6`, tree `bef3d2fece33754b73940e195a2cdae996862f29`. It is one docs-only commit on my round-1 head `b5e9242e2e1911bb2bac11221527f8965a4ccaef`, which sits on dev `ea3fb38877842f223afea97e3bd72a10500455c9` (the live dev tip when this round ran).
- **Round-2 diff:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only, +143 / -17. The PR as a whole changes that page (new) and one row in `docs/findings/README.md`.
- **Assignment:** #629 comment 5932539168, answered by the executor's REVIEW READY (#629 comment 5932914235).
- **Evidence examined:**
  - Branch `b6-review-evidence` at the page's pin `ff542b62ae79f283b80b7945dd76110f986b0737`.
  - The same branch's live tip `8871d419a9c8e1cfa1ceee94db077512201512ca`, for the round-2 author packet `review-evidence/b6-r1/author-r2/`.
  - The assigned round-1 archive `c9ada33881b714f2faf2414123c2b16fac240b6a`.
  - The ancestry is `c9ada338` -> `ff542b62` -> `8871d419`. The tip changes only `author-r2/` and `MANIFEST.json`, so `author/` is unchanged since the pin (`receipts/archive-ancestry.json`).
- **Reconstruction order:**
  1. AGENTS.md and CONTRIBUTING.md.
  2. The #629 body.
  3. The lane assignment (5929778646) and the round-2 assignment (5932539168).
  4. The executor's TAKEN and REVIEW READY comments.
  5. The manager's PR comments (review starts, self-test evidence 5932531424).
  6. The PR body, the round-2 diff, the full page at head, and the cited RTL, design and register documents.
  7. The evidence archive.

  My own round-1 findings were read only after this independent pass. The other reviewer's round-1 report was read only after this verdict and ledger were written (see "Prior findings").

## Verdict summary

The round-2 commit answers every round-1 finding.

- Every new factual statement I could check against the published grades, run logs, tool outputs and code is true.
- Every statement that rests on the unpublished raw read times agrees with the author's archived receipt, and is consistent with what the published grades can decide.
- All 15 tables are byte-identical to round 1. No rule, figure or verdict changed, and none should.
- The two reproduction commands run and match.
- The docs and repository gates pass at this head.
- The public text names no host, peer, switch or instrument. It states no wiring, channel map, stream count, capture layout or clock topology.

No BLOCKER, MAJOR or MINOR is open, so the verdict is POSITIVE. Four SUGGESTIONs follow; none affects coverage.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R427-2-S1 - SUGGESTION - Docs - one of path 4's "seven rises" was not measured

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:255-259`.
- **Evidence:** the page says of A1's and B CRF's seven clusters under 98 frames: "Their rises, 0.99 to 1.00 ms, sit at the floor's step".
  - Six of the seven have a measured rise of 0.9906 to 1.0026 ms.
  - A1's cluster 9 (60 frames, after a 33.452 ms read gap) has no measured rise. Its basis is `read gap`, the gap-only branch that path 5 counts (`summary/a1/grade.json` `skip_clusters[9]`; `receipts/attribution-recheck.txt`; the author's `author-r2/receipts/attribution-checks.txt` agrees).
- **Impact:** none on the conclusion. Read gap plus size carry that cluster too, and it is 48 n + 12 after a gap of 14.9 ms or more. A reader may think seven rises were measured, not six.
- **Suggested outcome:** "six of them have rises of 0.99 to 1.00 ms; the seventh, A1's 60-frame gap-only cluster, has none".

### R427-2-S2 - SUGGESTION - Robustness, Docs - the 12.4 s edge residual is wider than one frame

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:232-235` and `:556-558`.
- **Evidence:** A1's 12.4 s loss (cluster 13, 12 loops + 18,626 frames) has no size pattern, so only the rise test applies to it. The measured rise is 12,387.94 ms against a lost duration of 12,388.04 ms, 0.10 ms apart. But the read-time floor itself steps by up to 1.0 ms (path 4). So a listener skip of up to about 50 frames merged at that edge is as unresolvable as the one-frame drop the page names.
  - The page's general limit, that events inside lost audio cannot be seen, covers this in kind.
  - A1's only observed listener behaviour elsewhere is one-frame slips.
- **Related completeness note (no change needed):**
  - A multi-frame listener step grouped into a capture-path cluster within 300 ms is not one of the five named paths.
  - It is excluded in A1 and B CRF by the same per-step size data the page cites for path 1. Every positive step there is 48 n + 12 except the two named ones. The only negative steps are the stale-replay returns of exactly 23,880 and 24,000 frames (`receipts/attribution-recheck.txt`).
- **Suggested outcome:** name the residual as "a drop or a skip of up to about 1 ms" at that edge, and say that the per-step size check also covers steps grouped into a cluster.

### R427-2-S3 - SUGGESTION - Docs - a fourth lock window before the shakedowns

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:93-108`.
- **Evidence:** the archive records `runs/smoke-a0-importfail-lock.txt`. It is a 150 ms lock window in which the run tool failed at import before any step. HANDOFF.md:62 also lists it: "nothing on the bench".
  - The page lists three shakedown runs.
  - "Every bench action held the shared lock" stays true, because this window took no bench action.
- **Suggested outcome:** optionally add it as a fourth, actionless lock window, for completeness.

### R427-2-S4 - SUGGESTION - Docs, Tests - the round-2 derivations have no pointer from the PR

- **Where:** the PR #630 body, "Round 2" (the packet is named only as `b6-a480`); page `:220-264`.
- **Evidence:** the tools and receipts behind the round-2 statements (path 5's 16 to 28 %, the per-path checks, the window and floor checks) are public at `review-evidence/b6-r1/author-r2/` on the evidence branch tip `8871d419`. Neither the PR body nor the page points there. A cold reader of the PR cannot find `attribution_checks.py` or its receipt.
- **Suggested outcome:** the PR body (manager-owned) maps `b6-a480` to `review-evidence/b6-r1/author-r2/` at `8871d419`, as the page does for `b6-a477`.

## Round-1 findings (my own, R427-1), resolved at this head

| R427-1 item | Status at `e3f28f2f` | Evidence |
|---|---|---|
| F1(a) MINOR, B CRF window start | **Resolved.** :155-159 now reads 20.5 s after the clock-source set, 14.0 s after the servo first read LOCKED, under the same 20 s rule. | `runs/bcrf/events.jsonl`: set-clock ...054.756, servo-lock ...061.249 (6.49 s), window-start ...075.253, so 20.50 s after the set and 14.00 s after LOCKED. All five windows opened 20.01 to 20.50 s after the last bind or set, within the page's "20.0 to 20.5 s". |
| F1(b) MINOR, read-time exceptions | **Resolved.** :507-516 attribute the 2.7 ms and 177 ms exceptions to A2 DUT beat repeats, and state 135 of A2's 674 measurable listener events, 497 of 520 for A0 and 485 of 507 for B INTERNAL. Listener events reach at most 1.0 ms. | `summary/a2/events.csv`: the two exceptions are at capture frames 28,121,160 (2.6798 ms) and 28,147,698 (176.8061 ms), both `DUT beat`, at -0.193 s and +0.360 s from the 13.3 s stall's cluster 55 ("within 0.4 s" holds). The measurable counts and the 1.0067 ms maximum re-derive exactly. So do the beat counts: 300/321, 312/315, 313/316, 303/322 (`receipts/attribution-recheck.txt`, `receipts/a2-detail.txt`). |
| F2 MINOR, attribution blind spots | **Resolved** (wording nits S1, S2). Method :220-264 states five absorption paths, each with its A1 and B CRF data check. The capture-path section :492-499 and Limits :555-559 state the residual and A0's and A2's 48 n + 13 skips. | See "The attribution statements" below. |
| F3 MINOR, PR body template | **Resolved by the manager.** The body carries Contents, Status, Linked Issue / roles, Description, Authoritative references, How to get into the same state, How to validate (runnable commands with expected results), Known limitations and Definition of Done. Its Round 2 section is additional. "Relates to #629" only; no closing keyword. | PR body against `.github/PULL_REQUEST_TEMPLATE.md` headings. |
| S1, a control for a 3 dB band error | **Answered, and adequate.** :316-322 records an independent check instead of a new control. | Independent check below. |
| S2, docs nits | **Done.** `KL_crf_tx.sv` named with its header (:410); lane B5's 16.46 ppm linked to PR #628 (:388-390); LOCKED at three reads, 5, 315 and 615 s in (:460-462); bridge legs stopped by process ID and restarted (:93-96); comb residual "within 1.82 frames" (:379). | `KL_crf_tx.sv:20-27` describes the /512 divider of `clk_audio_i`. PR #628 head `e5ad1187`, `117_AUDIO_CONTINUITY.md:302` reads 16.46 ppm. Reads at 5.17, 315.42 and 615.21 s, all LOCKED, `SLIP_TDM` static at `0xc066` (`receipts/slip-tdm.txt`). Largest residual 1.817 frames. |
| S3, link A2's tracking and the DRP bit | **Done.** :421-423 and Limits :562-568 link #74 comments 5932380322 and 5932538721. | Both comments exist on #74, "Media clock: select CRF and align the audio grid" (OPEN), and carry the A2 measurement and the DRP-bit observation (`receipts/issue74-comments.txt`). |

## What this round was asked to judge

### The attribution statements (R426-1 F1, R427-1 F2): true, complete in effect, no verdict change

These were re-derived from the published `summary/<case>/grade.json` and `events.csv` at the pin (`scripts/attribution_recheck.py` -> `receipts/attribution-recheck.txt`; `scripts/a2_detail.py` -> `receipts/a2-detail.txt`).

**Path 1, a one-frame drop at a capture loss.**
- B CRF: all 38 positive capture-path steps are 48 n + 12. The only negative steps are -24,000 twice, in cluster 5. Its net -46,644 frames plus one whole loop gives a 1,356-frame loss (48 n + 12), so a merged drop would also show there.
- A1: all positive steps are 48 n + 12 but two:
  - the 23,880 edge, cancelled by a step back of exactly 23,880 frames;
  - the 18,626-frame skip of the 12-loop loss (18,626 = 48 n + 2).
- A0's only off-pattern skip is 1,165 frames (48 n + 13), in cluster 0. The cluster's net is 4,801 frames, with a rise of 99.98 ms against 100.02 ms lost.
- A2's only 48 n + 13 skip is 109 frames, in stale-replay cluster 15.
- No case has a 48 n + 11 skip.
- The capture-path section's "255 of 265" re-derives exactly. So does its split of the other ten: two longer than a loop (18,626 and 7,395), four stale-replay edges (23,880, 23,689, 22,392 and 23,999), two parts of cluster 46, which totals 2,268 = 48 n + 12, and the two 48 n + 13 skips.
- "May each be one low, about 0.03 ppm" is right: one frame is 0.033 ppm of the window.

**Path 2, a repeat near a beat tooth.**
- A1's 315 members are at least 93,989 source frames apart, so there is one per tooth.
- The nearest capture-path event is 75 capture frames away.
- The one gap that spans missing teeth, members 221 and 222, is 156,807 captured frames. Two capture-path losses lie in it: the 12.4 s loss (12 loops + 18,626 frames, cluster 13) and a 492-frame loss (cluster 14). With them the gap is 751,924 source frames, 8.000 periods, so 7 teeth are missing. The loss spans source offsets 85,869 to 680,495 after member 221, and the teeth fall at 93,990 to 657,933. So all 7 missing teeth lie inside the 12.4 s loss.
- B CRF has no one-frame event of any kind.

**Path 3, the gap and size branch.** A1 and B CRF have no cluster with basis `read gap and 48 n + 12 size`. A2 has two (clusters 17 and 56).

**Path 4, a skip of 2 to 48 frames with no stall.**
- The arithmetic holds. A zero rise matches a skip s when s/48 <= 1 + 0.02 s/48, so s <= 48.98 frames. A 1.0 ms rise extends that to s <= 97.96 frames, "about 98".
- The smallest capture-path loss in A1 and B CRF is 60 frames.
- The clusters under 98 frames are exactly seven, each one 60-frame skip after a read gap of 14.907 ms or more: A1 0, 3, 5 and 9, and B CRF 8, 12 and 13. See S1 for cluster 9.

**Path 5, the gap-only branch.**
- A1's two gap-only clusters, [348, 204, 492, 204] and [60], are all 48 n + 12. B CRF has none.
- The share of read positions meeting the gap test (16.0 to 27.5 % across the five windows) needs the raw read times, which are not published. I take it from the author's receipt.
- The published stall data are consistent with it. A1 has 232 read stalls over 15 ms in 617 s. With Poisson arrivals, that alone puts about 20 % of positions within 600 ms of one.

**Completeness.**
- A one-frame event never joins a cluster, so the five paths plus the per-step size data cover every route by which a listener event could leave the listener class (S2's note).
- The residual is stated: an event at the edge of A1's 12.4 s loss.
- The page names A0's 1,165-frame and A2's 109-frame skips as possibly merged listener drops.

**Verdicts.**
- None should change.
- A0 and A2 move by at most one listener drop each.
- A1 PASS and B CRF PASS rest on 0 listener events. The checks above exclude every named route in their data, apart from the edge residual, which is equivalent to lost audio.
- B CRF is further corroborated by 0 net non-capture steps in 30,237,600 frames and a static `SLIP_TDM`.

### The B CRF window and the read-time exceptions

These are verified; see F1(a) and F1(b) above.

### The archive pointer (:603-624)

- The pin `ff542b62` is an ancestor of the live branch tip.
- `b6-a477` -> `review-evidence/b6-r1/author/` holds. The page's example path exists.
- All 240 `author/` files re-hash to their `MANIFEST.json` `published_sha256`. I did not open the reviewer subtrees; I only re-hashed `author/`.
- All 54 page hash rows resolve: 33 to `original_sha256` in `MANIFEST.json`, and 21 to `RAW-ARTIFACTS.json` by path, size and hash. The tone loop resolves to `a0/serve/tone.raw` and its siblings.
- Exactly 12 of the page's evidence rows are label-masked, and they are the twelve the page names (5 `grade.json`, 5 run `events.jsonl`, `grade_b6.py`, `run_b6.py`) (`scripts/hash_resolve.py` -> `receipts/hash-resolve.txt`).
- **The two reproduction commands, run from `ff542b62`'s `review-evidence/b6-r1/author/tools`:**
  - `b6_tone.py` exits 0 and the loop hashes to `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588`, the page's value: 48,000 unique pairs, 0 silent frames.
  - `b6_thdn.py controls` exits 0 with `ALL_PASS True`, and `cmp` against `controls/controls.json` is silent. Both files hash `7bbefc71...` (`receipts/repro.txt`).
  - The control rows on the page match the regenerated output: 8 and 1 decodable frames in the resampled controls; 23 and 4 slips.

### R427-1 S1 answered by an independent floor check: adequate

I ran my own 48,000-point DFT of the regenerated loop, independent of the tool and of the author's check (`scripts/floor_dft.py` -> `receipts/floor-dft.txt`).

| Tone | DFT THD+N | DFT SNR | Tool, full precision |
|---|---|---|---|
| 997 Hz | -146.0647 dB | 146.0671 dB | -146.06470 dB |
| 9,973 Hz | -145.9933 dB | 145.9933 dB | -145.99328 dB |

- The DFT matches the tool's full-precision figures in `controls.json` within 0.0001 dB.
- The analytic 24-bit rounding floor over the band is -146.0515 dB.
- Doubling the band power gives -143.05 and -142.98 dB, so a 3 dB band error would show against both references.

Not adding a control to the hashed tool is reasonable: `controls.json` is evidence of the graded runs and must stay byte-reproducible. The page also states plainly that the controls alone would pass such an error.

### The 17.1 ppm cell

The explanation is true: `summary/a0/grade.json` `effective_offset_ppm.listener_only` = 17.1416 ppm = 518 / 30,218,880. That is the 519 drops net of the one silent insert; 519 alone is 17.17 ppm.

### #74 and the DRP bit

- #74 is named for A2 at :421-423 and :562-564.
- The DRP bit is in Limits at :565-568, "observed and not analysed", with the #74 comment.
- `REGISTER_MAP.md:2082` decodes `MCSRV_STAT` `0xffaa0033` (ACQUIRE) and `0xffa00034` / `0xffa10034` (LOCKED). Each has `[4]` DRP config mismatch set, and the LOCKED trim is -96/16 = -6.0 ppm. So "from ACQUIRE on" holds.

### Tables

- All 15 tables are byte-identical to round 1: 161 table lines, 16,010 bytes, sha256 `540ab528...` on both sides, and `cmp` silent.
- Each table also keeps its order. Only two tables' preceding prose lines differ, both from round-2 prose edits (`scripts/table_identity.sh` -> `receipts/table-identity.txt`).

### Public text

- The pattern scan covered:
  - the round-2 added lines;
  - the full page;
  - the PR body;
  - both commit messages.

  Its only hits are benign (`scripts/public_scan.py` -> `receipts/public-scan.txt`):
  - generic `/tmp` paths in the reproduction commands;
  - four-part clause numbers;
  - the AEM stream formats' channel counts and the DUT-side tone-loop channels, both already in round 1.
- Read by eye, the page names no host, peer, switch or instrument. It states no wiring, channel map, stream count, capture layout or clock topology.
- Both commit messages are one line with no trailers.
- The PR says "Relates to #629" only.

### Gates at this head

All rc 0, none piped, Markdown gates in the pinned environment, whose lock hash `40cdefe08ebd...` matches the environment and installed versions (`receipts/gates/summary.txt` and per-gate files):
- `docs_check.py`: 0 findings over 183 md files.
- `check_doc_style.py`, `gen_toc.py --check` and `gen_toc.py --verify-anchors` (285 links).
- `check_em_dash.py --base ea3fb388`: 0 findings over 661 added lines.
- `check_doc_paths.py`: 862 cited paths.
- `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test` (46/46).
- `git diff --check`, against `ea3fb388` and against `b5e9242e`.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #629 body bench acceptance. Assignments 5929778646 and 5932539168. Page :20-33, :93-108, :155-167, :220-264, :384-390, :421-423, :459-469, :492-516, :555-568. `runs/{a0,a1,a2,bint,bcrf}/events.jsonl` (bind, set-clock, servo-lock, window-start, restore). `summary/*/grade.json` `dut_reads` (`MCSRV_STAT`, `SLIP_TDM`) against `REGISTER_MAP.md:2082`. #74 comments 5932380322 and 5932538721 | R427-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| RTL | CLEAN | Diff name-status: no `hdl/` path. Gitlinks (4) equal to base `ea3fb388`. RTL claims on the page: `hdl/ieee1722/crf/KL_crf_tx.sv:20-27` (the /512 divider of `clk_audio_i`), `hdl/milan/milan_datapath.sv:445`, `MCSRV_STAT` bit and trim decode (`REGISTER_MAP.md:2082`), `SLIP_TDM` 0x8D8 (`REGISTER_MAP.md:134`) | R427-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| Robustness | CLEAN (S2 is a suggestion) | Five absorption paths re-derived from `summary/{a0,a1,a2,bint,bcrf}/{grade.json,events.csv}` (`receipts/attribution-recheck.txt`, `receipts/a2-detail.txt`). Every capture-path step by size modulo 48. Stale-replay and loop-folded clusters (A1 13/18, A2 13/15/36/46/55/56, B CRF 5). Beat-comb tooth occupancy and the 12.4 s loss. Read-time rise measurability. Author receipt `author-r2/receipts/attribution-checks.txt` compared | R427-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| Tests | CLEAN | Tone and controls reproduced from `ff542b62` (`receipts/repro.txt`). Independent DFT and analytic floor (`receipts/floor-dft.txt`). 54 page hashes resolved and 240 files re-hashed (`receipts/hash-resolve.txt`). 15-table identity (`receipts/table-identity.txt`). Window timings from `runs/*/events.jsonl`. 13 gates rc 0 (`receipts/gates/`) | R427-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| Docs | CLEAN (S1, S3, S4 are suggestions) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (all 660 lines at head; round-2 diff `b5e9242e..e3f28f2f`). `docs/findings/README.md` index row (unchanged in round 2). PR #630 body against `.github/PULL_REQUEST_TEMPLATE.md`. Commit messages. Public-text scan (`receipts/public-scan.txt`). Docs gates in the pinned environment | R427-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |

## Real limits of this round

- **Raw data.** The raw captures, read-time records (`cap-ts.bin`) and full grades (`grade-full.json`) stay on the bench host.
  - Everything decidable from the published summaries was re-derived from them.
  - Path 5's 16 to 28 % share and the 1.0 ms floor step "with no loss" rest on the author's receipt over the raw files. They were checked only for consistency with published stall data and one-frame rise maxima.
- **Bench and calibration.** No hardware or bench access. Physical calibration NOT RUN. Rates are on uncalibrated clocks, as the page states.
- **RTL.** No RTL changed, so no simulation ran and the pinned Verilator was not used (its identity was therefore not checked). No full banks, act, Docker or host runner actions were run.
- **Hosted checks at the exact head.** Snapshot at 14:07:15Z (`receipts/hosted-checks-e3f28f2f.tsv`):
  - Executed and succeeded: `rtl-fast`, `full-ci-gate`, `elaborate`, `bdd-conformance`, `wire-accountability`, `changes` and `docs-check-no-git`.
  - Still in progress: `docs-check`. The combined status was pending.
  - Skipped contexts, which are not evidence: the Verilator and Yosys shards, `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration` and the physical gPTP job.
- **Manager banks.** The manager's static/builder and native banks at this head were not re-run here. No archived receipt for them at `e3f28f2f` was found on the evidence branch: the tip holds author round-2 gates only.
- **Clone integrity.** After every probe the clone was verified (`receipts/clone-integrity.txt`):
  - `HEAD` and the index tree equal `bef3d2fe`;
  - 978 tracked blobs have equal bytes and modes;
  - there are no assume-unchanged or skip-worktree flags and no status entries;
  - the 4 gitlinks equal the head tree and base.

  All probes ran in scratch copies, never in the clone. The page's reproduction commands write under `/tmp`. This round ran them with `/tmp/r427-2-*` output names, and removed both files afterwards. The evidence archive was extracted into the unpublished scratch area only.

## Pending manager duties

- **Evidence archive mask (outside the PR diff).**
  - At `ff542b62`, and so at the live tip, the archived grade tool masks the capture channel count. But one result-field identifier in its channel-identification step still spells the two tone channel indices of the external capture. The archived run tool masks those same indices as `<capture-channel-index>`.
  - The run logs (`runs/*/events.jsonl`, `ctl.jsonl`) also carry the reference peer's stream descriptor indices.
  - The earlier commit `c9ada338` stays in the branch history.
  - Decide whether this matters under the masking rule. If it is re-masked, the page's pin at :604 changes with it. This report does not repeat the values.
- **Round-2 packet pointer:** see S4.
- **Self-test evidence at `e3f28f2f`:** the DoD item is unchecked, and the PR comment 5932531424 covers `b5e9242e`.
- **Merge-turn duties:**
  - hosted `docs-check` completion;
  - act acceptance;
  - the current-dev candidate merge build (source base `ea3fb388`, live dev `ea3fb388` when this round ran);
  - the internal review R426-2;
  - post-merge containment.

## Prior findings

The verdict and ledger above were written before I read the internal round-1 report, R426-1 (PR #630 comment 5932376922). My own round-1 findings are resolved in the table above. R426-1's findings, judged at this head:

| R426-1 item | Status at `e3f28f2f` | Where and why |
|---|---|---|
| F1 MINOR (Robustness, Tests, Docs), three absorption paths | **Resolved** | The page's paths 1 to 3 are R426-1's (a), (b) and (c). (a) is the merged one-frame drop, 48 n + 13 or 48 n + 11. (b) is the 50-frame comb window with no one-member-per-tooth check. (c) is the spoiled-rise arm on gap plus size. Each has its A1 and B CRF data check, re-derived above: no off-pattern skip outside replay edges and the 12-loop loss; beat members at least 93,989 frames apart; no gap-and-size cluster. A0's and A2's listener counts are qualified for the two 48 n + 13 steps at :496-499 and :558-559. |
| F2 MINOR (Docs, Tests), B CRF window | **Resolved** | :157-159, verified against `runs/bcrf/events.jsonl`: 20.50 s after the set, 14.00 s after LOCKED. |
| F3 MINOR (Docs), read-rise exceptions | **Resolved** | :507-516: the exceptions are A2 beat repeats; per-case measurable counts are given for the three cases with listener events, and A1 and B CRF have none. Verified against `summary/*/events.csv`. |
| S1, 17.1 or 17.2 ppm | **Done** | :384-386, verified (518 net = 17.1416 ppm). |
| S2, smoke runs | **Done** | :93-108. A fourth, actionless lock window is noted in R427-2-S3. |
| S3, LOCKED reads | **Done** | :460-462. |
| S4, A2 tracking | **Done** | :421-423, #74. |
| S5, PR body Contents | **Done** (manager) | The PR body carries Contents. |

No prior finding is retained at this head. This round neither adopts nor answers the concurrent internal round R426-2, which I have not read.

R427-2 FINISHED
