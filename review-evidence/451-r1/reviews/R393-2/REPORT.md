[R393] POSITIVE - exact head 335e55c4135979a554dc0281d6980ac1e2158aee

# R393-2: external independent review of PR #616 (issue #451), round 2

- **Head under review.** `335e55c4135979a554dc0281d6980ac1e2158aee`, tree `5b797a0d1efdc19e59a8df4fce73de5f28f679b8`. Source base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- **Delta.** `6339479d..335e55c4` is one commit by the executor [A423]: "Correct the DIN stop-boundary record, link #617 and index the TDM8 first-light page". The message is one line with no trailers. It changes `docs/findings/451_TDM8_FIRST_LIGHT.md` (+51/-16) and `docs/findings/README.md` (+1). The net PR diff is now one added page (+438) and one index row, across five commits.
- **Round.** R393-2, external reviewer, cleared context. I rebuilt the task in this order:
  1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
  2. The #451 body, the PocketBeagle 2 amendment (#451 comment 5729936674), the owner report (5872564358) and the round-2 assignment (5872564881).
  3. Issue #617 and the PR body at this head.
  4. The delta diff and the history.
  5. The public evidence archive at `851f835c8ba778b82c78ca9cf0ec814613ddfeda:review-evidence/451-r1/author`, plus the hash-verified raw captures.

  My round-1 packet was read-only input.
- **Verdict: POSITIVE.** All three of my round-1 MINOR findings (F1 to F3) are resolved at this head. So is the stop-boundary finding I retained from the other round-1 review, which is also my S1. Suggestions S2 to S6 were all taken correctly. Every new or changed number was re-derived independently from the raw captures or the archived attribution, and each one matches. The measurement tables are unchanged apart from the requested beat-row label, and all eight documentation gates pass. I raise no new finding at MINOR or above. I have two optional suggestions.

## Findings

This round has no BLOCKER, MAJOR or MINOR finding.

### Suggestions (optional; they do not affect lens coverage)

- **S7 - SUGGESTION - Docs - `docs/findings/README.md:11` (the #451 row, State column).** The State column reads "continuity check, scope and calibrated items NOT RUN". The Scope column of the same row lists "continuity" among the things measured, meaning sample continuity, which is shown in the page's "Continuity and rate" section. Read cold, "continuity check ... NOT RUN" could be taken as saying that measurement did not run. The page's own row says "Electrical continuity check" (`451_TDM8_FIRST_LIGHT.md:401`). The State column also omits the USB Audio device capture item, which is NOT RUN (`:408`). Suggested outcome: write "electrical continuity check", and optionally name the USB Audio device capture among the NOT RUN items.
- **S8 - SUGGESTION - Docs - `docs/findings/451_TDM8_FIRST_LIGHT.md:3`.** The line "[A403] Refs #451." still carries a lane session identity on a durable page. The transient "REVIEW READY" status is gone, which is what S2 asked for. The other findings pages carry no session identity (`117_GPTP_SILICON_EVIDENCE.md:1-5`). "Refs #451." alone would be enough.
- **Not a PR artifact, for the issue owner.** The body of #617 cites the hold read at `KL_chan_map_capture.sv` "lines 958-960". The page now cites 959 to 960, which is correct: line 958 is the I2S arm. The issue text could be aligned. This does not affect this PR.

## Round-1 items verified at this head (focus items 1 to 6)

| Item | Round-1 source | Result at `335e55c4` | Evidence |
|---|---|---|---|
| (1) Idle-high claim gone; the page states exactly what the capture shows outside playback, including the 777 zero frames | R393-1 S1, the retained stop-boundary finding (other round-1 review F1) | **RESOLVED.** The page no longer says "idle line reads high", "reads all ones whenever the SoC is not playing" or "could not have come from the pin" (grep of the page: no match). `:242-256` now gives 1,193,185 frames outside the region: `ffffff00` spans 0 to 150,488 and 3,511,302 to 4,553,219; transition frame 150,489 = `ffffff00`, `fff80000`, then six zeros; 777 frames 3,510,525 to 3,511,301 (16.2 ms); the first torn frame, pair 0 zero and pairs 1 to 3 at `0x44ff`; 775 all-zero frames; the last frame with five zeros, two `ffffff00` and one `00ffff00`; and word totals 9,545,480 = 9,539,259 + 6,213 + 8. I re-derived every number exactly. The root-cause argument at `:125-136` now rests on the unrouted recordings being all zero over about 25 s without playback. I re-derived 94.7975 s and 94.884 s, only value `00000000`, and `aplay -d 70` with 1,648 periods of 2,048 frames (70.3 s) inside each listener window. "The map edit was the only change between the two runs" matches the archived run records: the SoC command line and the pattern period hash are identical, and the only procedural difference is `map-initial`/`map-add` and `map-remove`/`map-final` | `receipts/din3-outside-full.json`, `receipts/din-unrouted-length.json`; archive `evidence/s2/din2-long/` and `din3-long/` (`events.jsonl`, `soc-play.log`), `evidence/din-long/events.jsonl` |
| (2) #617 linked where the page names the defect and in the owner-items row | R393-1 F1 (also the other review's F2) | **RESOLVED.** The link is at `:15-16` (summary), `:294-295` (the section that names the defect) and `:409` (owner items), and also in the index row. #617 is open, titled "TDM capture crossbar mixes adjacent TDM frames across channel pairs (67.5% torn AAF frames)", and its acceptance requires a frame-atomic handoff, a failing-then-passing simulation and a bench re-run with 0 torn frames. The defect is tracked, not fixed, and the PR, which is documentation-only and did not introduce it, describes it as tracked | `receipts/gh/issue-617.json` |
| (3) Page in the findings index | R393-1 F2 | **RESOLVED.** A row is at the top of "Current entries" (`README.md:11`). Its facts match the page: image source `9e9954e9`, 70 s each way, NOT MET plus #617, NOT RUN items. Placing it first matches the de-facto newest-first order on live dev `ce550952` (#75, #397, #117). The row renders with 3 cells and no empty cell | `receipts/table-cells-index.json`, `receipts/gh/dev-ce550952-findings-README.md` |
| (4) Owner wiring check cites 5872564358; conductor count agrees with the cited spec | R393-1 F3 | **RESOLVED.** `:109-113` and `:401` cite the owner report, which is on #451 (URL verified). They restate it faithfully: "checked end to end (BCLK, FSYNC, DOUT, DIN and ground) and found correct, with no change made", before the second DIN session. The unsourced "five connections" is gone. The page states the amendment's link as "seven conductors: those four signals and three grounds", which equals the amendment's table (BCLK J11.6, FSYNC J11.8, DOUT J11.5, DIN J11.7, GND J11.1/37/38) and its sentence "Seven conductors: four signals, three grounds". The page claims no more than the report says about which grounds were checked | `receipts/gh/comment-5872564358.json`, `receipts/gh/comment-5729936674.json` |
| (5a) S2: transient status line | R393-1 S2 | **TAKEN.** "REVIEW READY" removed; see S8 for the residual session identity | page `:3` |
| (5b) S3: USB Audio device item stated as not delivered | R393-1 S3 | **TAKEN.** Row `:408`: "NOT RUN: both legs used McASP0 directly, without the SoC board's USB function". The label matches the #451 checklist line "Capture identifiable samples in both directions through the USB Audio device" | `receipts/gh/issue-451.json` |
| (5c) S4: PR body commit count | R393-1 S4 | **TAKEN.** The body says "Five commits" and lists `fba793c0`, `361d1f47`, `4f06bfc7`, `6339479d` and `335e55c4`. The API gives commits = 5 | `receipts/gh/pr-616.json` |
| (5d) S5: DOUT beat-crossing count, and line 959 | R393-1 S5 | **TAKEN.** The row label is now "clear of any underrun" (`:310`). `:314-316` says 36 crossings, 34 in the row, and the other two in the "no host-visible lateness" clusters starting at 129,825 and 411,321. I fitted the beat to the archived attribution's 34 beat clusters (period 93,990.39 frames) and enumerated 36 expected crossings in 3,360,000 frames. Exactly two fall outside the beat class, at 129,825 and about 411,796. They lie in clusters 129,825 to 131,181 and 411,321 to 411,852, both of class `unexplained`. Class sums re-add to 34/657/691, 9/975/963 and 8/541/537. The frame numbers follow the attribution's convention, one above my round-1 step-index convention (411,320 then, 411,321 now). The hold read is now cited at 959 to 960, and the head's `KL_chan_map_capture.sv:959-960` is the `SRC_TDM_C` arm reading `tdm_hold_r`; `:486-487` is the per-pair hold write | `receipts/dout-beat-crossings.json` |
| (5e) S6: public archive link | R393-1 S6 | **TAKEN.** `:418` links `tree/851f835c8ba778b82c78ca9cf0ec814613ddfeda/review-evidence/451-r1/author`. That commit exists, is an ancestor of `451-review-evidence`, and holds `author/` with the packet (MANIFEST, RAW-ARTIFACTS, evidence, gates) | scratch fetch of the public branch |
| (6) Measurement tables otherwise unchanged; Markdown gates pass | assignment | **HOLDS.** Comparing table rows between `6339479d` and `335e55c4` gives three changed hunks: the beat-row label, whose numbers are identical; two owner rows edited as required; and one owner row added. No measured number changed. All eight gates return rc 0 under the assignment's pinned Markdown environment. Cell counts are constant in all 11 page tables and the 1 index table, with no empty cell | `receipts/table-delta.json`, `receipts/gates/`, `receipts/table-cells-page.json` |

## Lens application at this head

- **Conformance.** Assignment items 1 to 4 and S2 to S6 are met (table above).
  - The page still claims no closure of #451, #448, #386 or #117 (`:413`).
  - The owner-items table now carries every #451 checklist item that this run did not deliver. The USB Audio device capture is a new explicit NOT RUN, and the J11 ground continuity check is covered by the "Electrical continuity check" row (NOT RUN).
  - The owner report is quoted without overclaiming.
  - The wiring spec restated on the page equals the amendment.
  - The root-cause inference no longer rests on a false premise, and its narrower argument holds on the raw data.
- **RTL.** The delta touches no HDL, config, software, test, script or tool path. The `hdl`, `configs`, `sw`, `tb`, `scripts` and `tools` tree hashes are identical at the base, at `6339479d` and at the head. The four gitlinks are unchanged. The page's RTL citations were re-checked at the head:
  - `KL_chan_map_capture.sv:486-487`: per-pair hold write on `tdm_pair_valid_i`.
  - `:959-960`: TDM hold read in the `resolve` case.
  - `milan_datapath.sv:1344`: unchanged since round 1.

  `KL_chan_map_capture.sv`, `milan_datapath.sv` and the generated `adp_shape_defaults.svh` have the same blobs at the image source `9e9954e9` and at the head. The round-1 RTL analysis (dynamic output map, crossbar selection, EN-gated silence, per-pair holds without a frame snapshot) therefore applies unchanged to this head (`receipts/rtl-scope.txt`).
- **Robustness.** Applied to the boundary and failure content the delta rewrote:
  - The playback start transition (frame 150,489) and the stop tail are now exact.
  - The torn-first-tail-frame argument that the zeros entered through the TDM holds holds on the raw words.
  - The unrouted recordings are zero across their non-playback intervals, while the routed recording reads `ffffff00` there. This is the discriminator the page now uses, and it holds.
  - The DOUT beat crossings that coincide with underruns are now stated rather than silently merged.

  No boundary claim on the page is contradicted by the raw data.
- **Tests.** No test or executable changed (see RTL). The evidence behind every new or changed claim was re-derived by my own decoders, which do not use the author's tools:
  - `din_outside_full.py`: single-stream assertion, region located by the own-tag rule, and a full word census outside it.
  - `din_length.py`.
  - `dout_beat_crossings.py`: a fit plus enumeration, independent of the author's class labels for the crossing count.
  - `table_delta.py`.
  - `table_cells.py`.

  The raw inputs were matched by SHA-256 to the page's artifact table (`receipts/raw-sha256.txt`: 4 of 4). The focused capture-crossbar harness result from round 1 (204 checks, 0 failures, killed by the EN-gate mutant) stands for this head, because the `hdl` and `tb` trees are byte-identical.
- **Docs.** Checked:
  - the page, all 438 lines, with the changed regions read in full;
  - the index;
  - every in-page anchor (10 targets, all resolving to headings);
  - every external link (the four #451 comment URLs, #617, the archive tree);
  - the PR body at the head;
  - the gates and the render check.

  A public-record scan of the delta found no private paths, addresses or host identifiers. The PR body discloses the textual index conflict with live dev and how it is to be resolved (see pending manager duties).

## Reviewer-owned completion ledger (R393-2)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #451 body checklist (lines 36-39), amendment 5729936674 wiring table, owner report 5872564358, assignment 5872564881 items 1-4 and S2-S6, #617; page `:1-18,105-136,237-262,283-295,297-316,396-421`; PR body | R393-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| RTL | CLEAN | `receipts/rtl-scope.txt` (delta = 2 Markdown files; `hdl`/`configs`/`sw`/`tb`/`scripts`/`tools` trees identical base/prior/head; gitlinks unchanged); `hdl/ieee1722/aaf/KL_chan_map_capture.sv:484-488,955-961` and `hdl/milan/milan_datapath.sv` blob-identical to image source `9e9954e9`; round-1 RTL analysis carried by byte identity | R393-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| Robustness | CLEAN | Routed DIN outside-region census (`receipts/din3-outside-full.json`), unrouted durations and values (`receipts/din-unrouted-length.json`), run timelines (archive `evidence/din-long/events.jsonl`, `evidence/s2/din2-long/`, `din3-long/`), DOUT underrun/beat coincidence (`receipts/dout-beat-crossings.json`); page `:125-136,242-256,314-316` | R393-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| Tests | CLEAN | No test changed (tree identity above); independent re-derivation scripts `scripts/din_outside_full.py`, `din_length.py`, `dout_beat_crossings.py`, `table_delta.py`, `table_cells.py` with receipts; raw inputs hash-matched (`receipts/raw-sha256.txt`); round-1 harness result applies by `hdl`/`tb` byte identity | R393-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| Docs | CLEAN (S7, S8 optional) | `docs/findings/451_TDM8_FIRST_LIGHT.md` (all 438 lines, changed regions in full), `docs/findings/README.md:1-23`, anchors and links, `receipts/gates/` (8 of 8 rc 0), `receipts/table-cells-page.json` (11 of 11), `receipts/table-cells-index.json`, `receipts/table-delta.json`, PR body at the head, public-record scan | R393-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |

## Prior public review findings on this PR

I read the prior public findings only after the verdict and ledger above were written. The PR's public comments list two review rounds with findings, both at `6339479d`: R392-1 (comment 5872415917, NEGATIVE) and my own R393-1 (comment 5872558700, NEGATIVE). R392-2 has been started (5872940592) but had published no findings when I read the PR. There are no PR review objects. Each prior finding is disposed of at `335e55c4` as follows.

| Prior finding | Severity; lenses | Disposition at `335e55c4` | Basis |
|---|---|---|---|
| R393-1 F1: no issue behind "recorded ... as a separate issue" | MINOR; Docs | **RESOLVED** | #617 is open, cites this page's evidence, and is linked at `:16`, `:295`, `:409` and in the index row (item 2 above) |
| R393-1 F2: page missing from the findings index | MINOR; Docs | **RESOLVED** | `README.md:11` row (item 3 above) |
| R393-1 F3: "all five connections" unsourced, conflicting with seven conductors | MINOR; Docs, Conformance | **RESOLVED** | Owner report cited, the count claim removed, and the amendment's seven conductors stated exactly (item 4 above) |
| R393-1 S1 to S6 | SUGGESTION; Docs (S3 also Conformance) | S1: resolved with R392-1 F1. S2 to S6: taken | Items 1 and 5a to 5e above; S8 records the remaining session identity on `:3` |
| R392-1 F1: idle-high and "could not have come from the pin" contradicted by the routed capture | MINOR; Docs, Tests, Robustness | **RESOLVED** | Each part of its required outcome is met: idle `ffffff00` before playback and after the tail; the 777-frame zero tail; the transition frame; and the root cause stated in its narrower, supportable form. Re-derived exactly from the raw capture (`receipts/din3-outside-full.json`, `receipts/din-unrouted-length.json`) |
| R392-1 F2: no issue for the frame-coherence defect | MINOR; Docs | **RESOLVED** | Same as R393-1 F1. #617's Evidence line names this page's "DIN frame coherence" section and its archived captures |
| R392-1 F3: transient status line | SUGGESTION; Docs | Taken | Same as S2; see S8 |
| R392-1 F4: USB Audio device checklist item omitted | SUGGESTION; Docs | Taken | Row `:408` |
| R392-1 F5: index lacks the page | SUGGESTION; Docs | Taken | `README.md:11` |
| R392-1 F6: PR body commit count and net change | SUGGESTION; Docs | Taken | The body says "Five commits" and "the net change is that one added page and one index row" |
| R392-1 F7: the 9 / 8 underrun split rests on a fitted alignment multiple | SUGGESTION; Docs, Tests | **Retained, optional, not taken** | Rows `:311-312` still present the split as a cause without naming the fitted alignment. The new sentence at `:314-316` puts the two coinciding crossings in the "no host-visible lateness" row, and that placement inherits the same dependence: both clusters have `late_pdus_before` 0 under the fitted alignment. The crossing count itself (36 = 34 + 2) is alignment-independent (`receipts/dout-beat-crossings.json`). As a SUGGESTION it does not affect coverage |

After this disposal, no MINOR, MAJOR or BLOCKER from any prior round remains open at this head. The ledger above stands unchanged.

## Limits (real)

- **Physical measurements.** Physical calibration was NOT RUN, and no hardware was touched. Bench facts come from the archived evidence and the public owner report. Field skips are not hardware proof. The owner's end-to-end wiring check is a public statement, not a measurement, and the page records the electrical continuity check as NOT RUN.
- **Raw captures.** The raw captures were read from the author's raw root on the review host, which is not public. I verified each by SHA-256 against the page's artifact table before use (`receipts/raw-sha256.txt`, 4 of 4). The re-derivations are reproducible only while that root is retained.
- **DOUT underrun split.** The 9 / 8 split, and therefore which row the two coinciding crossings fall into, depends on the author's fitted wall-clock alignment (R392-1 F7). I verified the crossing count and the class sums, not that alignment.
- **No simulation re-run.** I did not re-run the round-1 focused capture-crossbar harness. The `hdl` and `tb` trees are byte-identical to the head where it passed (`receipts/rtl-scope.txt`), so the round-1 result carries over. No Verilator was used in this round.
- **Hosted evidence.** At the exact head, GitHub reports 0 check runs, 0 workflow runs and an empty status rollup, and it marks the PR `mergeable: CONFLICTING` (`receipts/gh/check-runs-335e55c4.json`, `receipts/gh/actions-runs-335e55c4.json`, `receipts/gh/pr-616-rollup.json`). No hosted context, executed or skipped, exists at this head. I cite none as evidence.

## Pending manager duties

- **Merge conflict with live dev.** `git merge-tree` of the head against live dev `ce550952e47fbd92367f0d9b099345100f7f4215` conflicts only in `docs/findings/README.md` (`receipts/merge-tree-dev.txt`). The cause is the #75 and #397 rows that dev added at the same place. The PR body discloses this and plans to keep all rows, with #451 first. The conflict can be resolved in two ways:
  - **In the lane.** A new head changes an artifact within the Docs scope, so Docs coverage from this round would need to be re-applied at that head.
  - **Only in the manager's candidate.** The candidate result must be validated, including the index table render and the docs gates.
- **Hosted and act acceptance.** Hosted acceptance (`rtl-fast` and the documentation contexts) and the act replica at the exact PR head are still owed. None exists at `335e55c4` (see Limits), and the conflict may be preventing hosted pull-request runs.
- **Final candidate.** The final current-dev candidate build must be made against live dev at the merge turn.
- **Second review.** The second independent review verdict (R392-2) must be collected at this head. Merge authorization is required before merge.
- **Optional.** The executor may take S7, S8 or R392-1 F7. Any page or index edit makes a new head that re-opens Docs, and re-opens Conformance if it touches the scope, wiring or owner-items text.

## Clone state after probes

- **Worktree.** The review clone is at the exact head. `git status --porcelain --ignored --untracked-files=all` is empty.
- **Tracked files and index.** The index equals the HEAD tree. All 931 regular tracked files rehash to their index blobs, with 0 mode mismatches.
- **Gitlinks.** `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e` are equal in the HEAD tree and the index (`receipts/clone-integrity.txt`).
- **Probe hygiene.** The gates ran with byte-code writing disabled. The merge-tree probe and the archive fetch used separate clones under the packet's scratch directory, which is never published. No file in the review clone was modified.

R393-2 FINISHED
