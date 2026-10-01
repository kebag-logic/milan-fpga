[R426] NEGATIVE - exact head e3f28f2f69343b54844ddfea368ef4cdd03facb6

# R426-2: internal cleared-context re-review of PR #630 (Refs #629, bench lane B6, round 2)

- **Head under review:** `e3f28f2f69343b54844ddfea368ef4cdd03facb6`, tree `bef3d2fece33754b73940e195a2cdae996862f29`. It is one docs-only commit on the round-1 head `b5e9242e2e1911bb2bac11221527f8965a4ccaef`, which sits on dev `ea3fb38877842f223afea97e3bd72a10500455c9`.
- **Diff against dev:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (new, 660 lines) and one row in `docs/findings/README.md`.
- **Diff against round 1:** only the findings page, +143 / -17. No RTL, tool, test or configuration file changes.
- **Scope:** the round-2 assignment (#629 comment 5932539168) and the round-1 findings R426-1 and R427-1.
- **Evidence examined:**
  - `review-evidence/b6-r1/` at the page-pinned `ff542b62ae79f283b80b7945dd76110f986b0737`;
  - the round-2 author packet `review-evidence/b6-r1/author-r2/` at the branch tip `8871d419a9c8e1cfa1ceee94db077512201512ca`;
  - the manager's PR #630 evidence comment (5932531424) and the #74 comments the page cites (5932380322, 5932538721).
- **Reconstruction order:**
  1. AGENTS.md, CONTRIBUTING.md (section 6, documentation wording and privacy, and 6.1) and docs/README.md;
  2. the #629 body, the B6 assignment (5929778646), the round-2 assignment (5932539168), and the executors' TAKEN, STOP and REVIEW READY comments;
  3. the PR body against `.github/PULL_REQUEST_TEMPLATE.md`;
  4. the diffs `ea3fb388..e3f28f2f` and `b5e9242e..e3f28f2f`;
  5. the cited code and design references;
  6. the archive.
- **Prior findings:** read only after this round's own pass over the diff and the evidence was complete. See "Prior public findings" below.

**Verdict: NEGATIVE.** Two MINOR findings are open:

- F1, under Conformance and Docs, concerns the evidence archive the page now pins.
- F2, under Docs and Robustness, concerns two statements in the attribution accounting.

RTL and Tests are covered clean. The measured verdicts on the page hold up at this head: A0 and B INTERNAL as controls, A1 PASS, A2 FAIL with a measured diagnosis, and B CRF PASS. No verdict should change. Every round-1 finding on the page is resolved.

## What this round checked independently

| Check | Result | Receipt |
|---|---|---|
| The 15 tables against round 1 | 15 of 15 byte-identical, none added or removed. All table lines: 161 lines, 16,009 bytes joined without a trailing newline, the same SHA-256 at both heads. | `receipts/table-identity.txt`, `scripts/table_identity.py` |
| Docs and repository gates at the head, pinned Markdown environment (venv matching `tools/markdown/requirements.txt` sha256 `40cdefe0...`) | All 12 rc 0: `docs_check.py`; `check_doc_style.py`; `gen_toc.py --check` and `--verify-anchors`; `check_em_dash.py --base ea3fb388...` and `--selftest`; `check_doc_paths.py`; `ci_scope.py --selftest`; `check_baremetal_only.py --check`; `check_feature_status.py --self-test`; `git diff --check` against `ea3fb388` and against `b5e9242e`. | `receipts/gates/gate-01.txt` to `gate-12.txt` |
| The page's two reproduction commands, run as printed from `ff542b62` in a disposable clone, output paths moved into the scratch area | Both rc 0. The tone loop regenerates at `566d3dfa...5588` (48,000 unique pairs, no silent frame). `b6_thdn.py controls` is byte-identical to `controls.json` (`7bbefc71...530e`): `cmp` is silent and ALL_PASS. | `receipts/repro.txt` |
| Archive integrity and the page's 54 hashes | 291 of 291 files re-hash to `published_sha256`, with none unlisted and none missing. 29 entries differ from their original. 53 hash rows plus the tone loop resolve, 54 of 54: 21 in `RAW-ARTIFACTS.json` and 33 to `original_sha256`. Of those 33, 12 are the label-masked files the page names, which is exactly the twelve it states. | `receipts/archive-check.txt`, `scripts/archive_check.py` |
| The five absorption paths, re-derived from the published `summary/<case>/grade.json` and `events.csv` | All true except the two statements in F2. See the detail below. | `receipts/attribution-recheck.txt`, `scripts/attribution_recheck.py` |
| Beat-comb geometry, in source frames as `grade_b6.py` builds them | A1: 315 members, one per tooth; spacing at least 93,989 frames; at least 75 capture frames from any capture-path event. Its 7 missing interior teeth all fall inside the 594,626-frame (12.4 s) loss. A2's two read-time exceptions are DUT beat repeats, 0.19 s before and 0.36 s after the 13.3 s stall's first event. | `receipts/beat-geometry.txt`, `scripts/beat_geometry.py` |
| Window starts and B CRF servo record | A0, A1, A2 and B INTERNAL opened 20.008 to 20.212 s after their last bind or set. B CRF opened 20.497 s after the set, 14.004 s after `servo-lock`, which came 6.493 s after the set. `MCSRV_STAT` read ACQUIRE `0xffaa0033` at +3.33 s and LOCKED `0xffa10034` at +6.49 s. In the window it read LOCKED at +5.2, +315.4 and +615.2 s. Bit 4 is set from ACQUIRE on (`docs/reference/REGISTER_MAP.md:2082`). `SLIP_TDM` stays at 0xc066 throughout. | `receipts/window-check.txt`, `scripts/window_check.py` |
| Independent floor (R427-1 S1) | 48,000-point DFT of the regenerated loop, band 20 Hz to 20 kHz, summed over a mask: 997 Hz gives -146.0647 dB / 146.0671 dB; 9,973 Hz gives -145.9933 / 145.9933. These equal the grades' published floor (-146.065 / 146.067; -145.993 / 145.993) within 0.0001 dB. The analytic floor is -146.051 dB. | `receipts/floor-dft.txt`, `scripts/floor_dft.py` |
| 17.1 against 17.2 ppm | 519 / 30,218,880 = 17.17 ppm; (519 - 1) / 30,218,880 = 17.14 ppm. The page's explanation is correct. The counted +6.519 = (519 - 1 - 321) / 30,218,880. | arithmetic from `summary/a0/grade.json` |
| Cited references | `hdl/ieee1722/crf/KL_crf_tx.sv:20-28` describes the /512 divider of `clk_audio_i` as the CRF timestamp grid. `hdl/milan/milan_datapath.sv:443-447` states the same contract. Lane B5's page in PR #628 (head `e5ad1187`, `117_AUDIO_CONTINUITY.md:302`) states 16.46 ppm. Both #74 comments exist and say what the page says. | files at the head; PR #628; #74 |
| Shakedown runs | `runs/smoke-a0-clkparse/events.jsonl` has `clk-peer` and `clk-dut` null at as-found, then teardown, with no map, bind or playback. `smoke-a0` has a 30 s window and 249 samples (HANDOFF row: 107 of 249 lost `hw_ptr`). `smoke2-a0` has a 90 s window. Both bound under a format check and restored. | archive `runs/smoke*` |
| PR body | Every template heading is present, plus "Round 2". "Relates to #629" appears with no closing keyword and `closingIssuesReferences` is empty. The PR head equals the reviewed head. | `receipts/pr-body-headings.txt` |
| Public text of the round-2 additions | No host, peer, switch, instrument, wiring, channel map, stream count or capture layout. The only path tokens are `/tmp/...` in the reproduction commands. The McASP0 clock-consumer relation is already on dev (`docs/findings/451_TDM8_TIMING_SOC_BOARD.md:135`). | gate-01; scan of the diff |
| Capture-layout literals in the archive the page pins | Present. See F1. The receipt reports line numbers and counts only, never the values. | `receipts/mask-check.txt`, `scripts/mask_check.py` |
| Hosted contexts at the exact head (snapshot) | Executed and successful: `rtl-fast`, `bdd-conformance`, `changes`, `elaborate`, `docs-check-no-git`, `wire-accountability` and `full-ci-gate`. `docs-check` was in progress. The Verilator and Yosys aggregates, shards, lint and elaboration contexts, and the physical gPTP job, were skipped contexts, which are not evidence. | `receipts/hosted-checks.txt` |

### The absorption paths against the published data (page :220-264)

1. **Merge with a capture loss.**
   - B CRF: all 38 capture-path skips are 48 n + 12, and its two steps back are exactly 24,000 frames.
   - A1: all 50 skips are 48 n + 12 except the 18,626 (48 n + 2, the loss of more than a loop) and the 23,880 (48 n + 24). The 23,880 is cancelled by an exact -23,880.
   - No capture-path skip anywhere is 48 n + 11.
   - A0's 1,165 and A2's 109 are the only 48 n + 13 skips, and A2's 109 sits in stale-replay cluster 15.
   - The "255 of 265" bullet and its breakdown of the ten reconcile, including A2 cluster 46: 732 + 558 + 918 + 60 = 2,268 = 48 n + 12.
2. **Beat window.** True for A1, as in the geometry row above. B CRF has 40 events, all capture path ≥ 3 frames.
3. **Read gap and size with a non-matching measured rise.**
   - A1 and B CRF have no such cluster.
   - A2 has exactly two: cluster 17, a 60-frame skip with a 154.5 ms rise, and cluster 56, a 1,020-frame skip with a -155.8 ms rise.
4. **Small skip with no stall.**
   - The smallest capture-path loss in A1 and B CRF is 60.
   - Their clusters under 98 frames number seven, each a single 60-frame skip after a gap of at least 14.9 ms (14.907 to 59.758 ms).
   - Only six have a measured rise (0.9906 to 1.0026 ms). See F2.
   - The 98-frame bound follows from the rule: |r - s/48| ≤ 1 + 0.02 s/48 with r up to 1.0 ms of noise gives s ≤ 97.96.
5. **Gap-only.**
   - A1 has two gap-only clusters, both all 48 n + 12. B CRF has none.
   - The 16.0 to 27.5 % share needs the raw read times, which are not published.
   - From the published stall counts a lower bound is about 9 to 28 %, using gaps over 15 ms only.
   - The author's receipt from the raw files gives 16.0 / 23.0 / 27.5 / 24.5 / 16.0 %, which is consistent.
6. **Read-time rises.**
   - Listener events with a measurable rise: A0 497 of 520, A2 135 of 674, B INTERNAL 485 of 507. The median is 0.00 ms and the largest magnitude 0.998, 1.0067 and 0.9999 ms, with no exception.
   - Beat repeats: 300 of 321, 312 of 315, 313 of 316 and 303 of 322.
   - The only rises over 1.01 ms are A2 beat repeats at 2.6798 and 176.8061 ms.

### Judgement on what was asked

- **The attribution statements:** true in substance. They are complete for the mechanisms the rules contain, with one unnamed variant (S1) that the stated data checks already exclude. Two sentences mis-state which branch a cluster passed by (F2).
  - The residual, a drop at the very edge of A1's 12.4 s loss, is stated correctly.
  - The A0 and A2 48 n + 13 qualifications are correct, including "about 0.03 ppm low".
  - **No verdict should change.** A1 and B CRF have no event in any absorption path outside lost audio.
- **B CRF window start:** true as stated. The rule sentence now matches `run_b6.py`'s settle-from-set behaviour.
- **Read-time exceptions:** true as stated.
- **Archive pointer:**
  - The pin, the label mapping, the `original_sha256` rule and the two commands are correct, and the commands reproduce.
  - The commit it pins still carries capture-layout literals (F1).
- **#74 and the DRP bit:** named correctly in A2 (:421-423) and Limits (:562-568). The decode is verified.
- **R427-1 S1 answered by the independent floor check:** accepted.
  - The tool and `controls.json` are hashed evidence of the graded runs. Adding a control would change the artifact the verdicts rest on.
  - A DFT that reproduces the published floor exactly, together with the analytic floor, would expose a 3 dB band error.
  - The page states candidly that the controls alone would not catch one.
  - The check script itself is reachable only from the round-2 packet (S3).
- **The 17.1 ppm cell:** explained correctly.
- **Tables, references and gates:** all 15 tables byte-identical; `Relates to #629` only; docs gates rc 0.

## Findings

### F1 MINOR: Conformance, Docs. The evidence archive the page pins still spells the capture layout

- **Where:**
  - The pointer and commands: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:603-621`, "Where the packet is", pinned at `ff542b62ae79f283b80b7945dd76110f986b0737`.
  - The leak: archive `review-evidence/b6-r1/author/tools/grade_b6.py:86-87` at `ff542b62` and at the branch tip `8871d419`, plus the reachable history of that file.
- **Authority/evidence:**
  - The round-2 assignment (5932539168) and the B6 assignment (5929778646) forbid capture layout in public text: "channel count or indices, or byte sizes that divide to them". The repository is public.
  - R427-1 recorded the archive leak as a manager duty. The manager's comment 5932531424 states that "the capture layout is label-masked there, including the grade tool's channel-identification code".
  - At `ff542b62` and `8871d419` the channel-identification step still decodes two capture columns by numeric index at line 86, and stores a result key that spells both indices at line 87. `run_b6.py` in the same archive masks the same two values as `<capture-channel-index>`, so the leftover is an oversight, not a decision.
  - The masking commit `ff542b62` is the very commit the page pins. Its own diff removes, and so publishes, the numeric channel count, and its parent `c9ada338` carries the count at lines 77 and 80.
  - `receipts/mask-check.txt` reports these line numbers and counts without the values, and this report does not repeat them.
- **Impact:**
  - The page now tells every reader to fetch and check out a commit that discloses the capture layout the lane contract withholds.
  - The public record also states that the masking is complete when it is not.
  - No measured figure or verdict is affected.
- **Required outcome:**
  - The published tool carries no numeric capture index, index-spelling key or count, at a new archive commit whose `MANIFEST.json` `published_sha256` is updated. `original_sha256` and the page's tool hash stay the original's.
  - The page's pointer and its reproduction commands are re-pinned to that commit and still reproduce.
  - The literals left in reachable history (`c9ada338`, and `ff542b62` and its diff) are either removed by an owner-authorised rewrite, with every pin to the old commits updated, or kept by a recorded owner decision.
- **Verification:**
  - `scripts/mask_check.py <evidence repo> <new pin>` reports RESULT CLEAN.
  - The page's two commands rerun from the new pin with rc 0, the tone hash `566d3dfa...` and a silent `cmp`.
  - `archive_check.py` resolves 54 of 54 page hashes at the new pin.

### F2 MINOR: Docs, Robustness. Two statements misplace clusters between the absorption branches

- **Where:**
  - (a) `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:255-259`, path 4: "Each of their seven clusters under 98 frames ... Their rises, 0.99 to 1.00 ms, sit at the floor's step".
  - (b) `:488-491`, The capture path: "Every capture-path cluster's read-time rise matches its loss ... except clusters whose rise is unmeasurable. Those meet the read gap and size rule instead: 1 in A0, 2 in A1, 7 in A2, 3 in B INTERNAL and none in B CRF."
- **Authority/evidence:** `summary/a1/grade.json` and `summary/a2/grade.json` `skip_clusters`, in `receipts/attribution-recheck.txt` and in the author's own `author-r2/receipts/attribution-checks.txt`.
  - (a) Of the seven clusters, A1 cluster 9 (one 60-frame skip, gap 33.452 ms) has no measurable rise. Its basis is `read gap`, the gap-only branch that path 5 covers. Only six have rises, of 0.9906 to 1.0026 ms.
  - (b) Of A2's seven non-rise clusters, five are gap-only (rise unmeasurable). Two, clusters 17 and 56, have a measured rise that does not match: 154.54 ms against a 60-frame loss, and -155.81 ms against a 1,020-frame loss. They passed on read gap and size, which is path 3. Path 3 (:246-250) says "A2 has two", so the bullet contradicts it.
  - Separately, path 5 states that the gap-only branch has no size check. The bullet's "meet the read gap and size rule" is true of these 13 clusters as data, since every skip is 48 n + 12, but not as the rule they passed by.
- **Impact:**
  - No count, figure or verdict changes. The seven clusters' attribution still rests on read gap and size, as the page concludes.
  - The section exists to tell a cold reader exactly which branch carried each attribution. As written it assigns one A1 cluster to the wrong path, and it contradicts itself on A2's two spoiled-rise clusters.
- **Required outcome:**
  - (a) states that six of the seven have rises of 0.99 to 1.00 ms and that A1 cluster 9 is the gap-only cluster path 5 covers.
  - (b) distinguishes the unmeasurable-rise clusters (1, 2, 5, 3 and 0 per case) from A2's two measured but non-matching ones on the read gap and size rule.
  - No table changes.
- **Verification:** compare the revised sentences with `skip_clusters[].basis` and `read_rise_ms` in `summary/{a1,a2}/grade.json`, using `scripts/attribution_recheck.py`.

### Suggestions (optional; they do not affect coverage)

- **S1 (Robustness, Docs), :220-264.** Name a sixth way for completeness.
  - The mechanism: a multi-frame listener step within 300 ms of a capture loss joins that cluster. The cluster test is on the net step within 1 ms + 2 % of the loss, which is about 249 ms at A1's 12.4 s loss.
  - The page's own data check already excludes it in A1 and B CRF: every member step there is 48 n + 12, or an exact stale-replay edge, or the 18,626-frame loss. One-frame events never join a cluster.
- **S2 (Docs), :615-621.**
  - `git checkout <sha> -- review-evidence/b6-r1` writes and stages the archive into whatever checkout the reader is in. Say to run it in a fresh clone or a disposable worktree.
  - The byte-identical `cmp` was confirmed here on one interpreter and numeric-library version. Recording the versions the archive was produced with would help a later reader.
- **S3 (Docs/Tests), :316-322 and :260-263.**
  - The DFT floor check and the 16 to 28 % gap share are reproducible only from the round-2 packet (`review-evidence/b6-r1/author-r2/`, now at `8871d419`) and the raw read times. The page points only at `ff542b62`.
  - When F1 re-pins, point at a commit that also holds `author-r2/`.
- **S4 (Docs), :607-608.** "each run's `events.jsonl`": the probe run's `events.jsonl`, in the same table, is not masked. "Each graded case's" would match the count of twelve.

## Prior public findings, read after this round's own pass

| Prior finding | Status at `e3f28f2f` | Evidence |
|---|---|---|
| R426-1 F1, the attribution blind spots | RESOLVED. Five paths are stated, each with its A1 and B CRF data check, and the two 48 n + 13 skips are qualified in the capture-path section and Limits. The statements are verified against the grades. The two misplaced sentences are a new, narrower finding (F2), not a retention of F1. | `receipts/attribution-recheck.txt`, `receipts/beat-geometry.txt` |
| R426-1 F2, the B CRF window start | RESOLVED (:155-159) | `receipts/window-check.txt` |
| R426-1 F3, the read-time exceptions | RESOLVED (:507-516). The per-case measurable counts are stated and correct. | `receipts/attribution-recheck.txt` |
| R426-1 S1 to S5 | Done. S1, 17.2 against 17.1 (:384-386). S2, shakedown runs (:93-108). S3, three LOCKED reads (:460-462). S4, #74 (:421-423, :562-568). S5, the PR body has Contents. | above |
| R427-1 F1 (a) and (b) | RESOLVED, same evidence as R426-1 F2 and F3. "In the cases that have any" is honoured: "A1 and B CRF have no listener event". | as above |
| R427-1 F2, the blind spots | RESOLVED. The smallest capture-path loss is 60 frames, the gap-only clusters are 48 n + 12, and the 98-frame widening is stated. | as above |
| R427-1 F3, the PR template | RESOLVED by the manager. Every template heading is present and How to validate has runnable commands. | `receipts/pr-body-headings.txt` |
| R427-1 S1, the 3 dB band control | Answered by the independent floor check. Accepted, with the location caveat in S3. | `receipts/floor-dft.txt` |
| R427-1 S2 and S3 | Done: `KL_crf_tx.sv` cited, 16.46 ppm with the PR #628 link, bridge legs in Method, 1.82 frames, #74 links. | above |
| R427-1 manager duty: re-mask the archive's grade tool | NOT RESOLVED. Only the count literals were masked, and the index literals remain. Now in scope, because the page pins that commit. Retained as F1. | `receipts/mask-check.txt` |

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-2 assignment items 1 to 6 against page :93-108, :155-159, :220-264, :316-322, :384-391, :421-423, :488-516, :552-568 and :600-624. Tables byte-identical (`receipts/table-identity.txt`). `Relates to #629`, with no closing keyword or reference (`receipts/pr-body-headings.txt`). Public-text constraint against the pinned archive (`receipts/mask-check.txt`). | R426-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| RTL | CLEAN | No `hdl/` path in either diff, and gitlinks unchanged (`receipts/clone-state.txt`). The A2 references were checked at the head: `hdl/ieee1722/crf/KL_crf_tx.sv:20-28` (the /512 grid of `clk_audio_i`) and `hdl/milan/milan_datapath.sv:443-447` (the port contract). `MCSRV_STAT` was decoded per `docs/reference/REGISTER_MAP.md:2082` (state 4 LOCKED, bit 4 DRP config mismatch, trim -96/16 ppm) against `runs/bcrf/events.jsonl` (`receipts/window-check.txt`). Simulation was not needed, so the pinned Verilator was not invoked. | R426-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| Robustness | UNCLEAN (F2) | The absorption analysis, page :220-264 and :488-516, against archive `tools/grade_b6.py:114-203` (`floor_rise_ms`, `recent_gap` and the `cap`/`basis` decision) and `summary/*/grade.json` `skip_clusters` and `events.csv` (`receipts/attribution-recheck.txt`, `receipts/beat-geometry.txt`). The 98-frame bound was derived from the rule. | R426-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| Tests | CLEAN | The reproduction commands run from `ff542b62`: tone hash equal, `controls.json` byte-identical, ALL_PASS (`receipts/repro.txt`). Independent DFT and analytic floor (`receipts/floor-dft.txt`). Window and servo evidence (`receipts/window-check.txt`). Table identity (`receipts/table-identity.txt`). Every round-2 check re-derived by this round's own scripts, not the author's. | R426-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |
| Docs | UNCLEAN (F1, F2) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (all 660 lines) and `docs/findings/README.md:15`. 54 of 54 hashes against `MANIFEST.json` and `RAW-ARTIFACTS.json` at `ff542b62` (`receipts/archive-check.txt`). 12 docs and repository gates rc 0 (`receipts/gates/`). The PR body against the template. Public-text scan of the round-2 additions. | R426-2 | `e3f28f2f69343b54844ddfea368ef4cdd03facb6` |

## Real limits of this round

- The raw captures, read-time records and McASP0 samples stay on the bench host. These are not re-derivable here:
  - the 16 to 28 % gap share;
  - the "first rule" outcome;
  - the read-time floor's 1.0 ms step.

  They were checked for consistency with the published `capture_reads` statistics and with the author's round-2 receipt, which hashes its raw inputs.
- For the 12 label-masked files, only the hash is checkable. The page's byte counts for them are of unpublished originals.
- The reproduction commands ran with output paths in this round's scratch area instead of `/tmp`, on one interpreter and numeric-library version.
- No hardware or bench access, and physical calibration was NOT RUN. Field skips are not hardware proof.
- No full banks, act or Docker were run. Hosted acceptance is the manager's. At the snapshot, `docs-check` was still in progress, and the long RTL aggregates were skipped contexts, as for a docs-only PR.
- **Clone restored:**
  - HEAD and the index tree equal `bef3d2fe`.
  - 978 tracked non-gitlink entries are byte- and mode-equal to their blobs.
  - There are no assume-unchanged or skip-worktree flags.
  - The four gitlinks are unchanged.
  - `status --porcelain --ignored` is empty, after removing the `scripts/__pycache__/` this round's gate run created.
  - Receipt: `receipts/clone-state.txt`.

## Pending manager duties

- **F1:** re-mask the archived grade tool at a new commit. Have the page re-pinned and its commands re-verified. Obtain an owner decision on the literals in the reachable history of `b6-review-evidence`.
- **Hosted acceptance:** exact-head hosted and act acceptance, including the in-progress `docs-check`.
- **Self-test evidence:** at `e3f28f2f`, since the DoD item is still unchecked.
- **Candidate merge build:** on live dev (base `ea3fb388`).
- **Reviews:** the external round R427-2, and re-review of F1 and F2 at the corrected head.
- **Archiving:** archive the round-2 packet location and point to it (S3).

R426-2 FINISHED
