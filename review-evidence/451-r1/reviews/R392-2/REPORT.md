[R392] POSITIVE - exact head 335e55c4135979a554dc0281d6980ac1e2158aee

Round R392-2 is the internal independent re-review of PR #616 (Relates to
#451). Tree `5b797a0d1efdc19e59a8df4fce73de5f28f679b8`, source base
`6d5ebd7357c1e468e446f18a61527c5be6118a04`. This is a delta review of
`6339479d..335e55c4`: one documentation commit by the round-2 executor, which
changes `docs/findings/451_TDM8_FIRST_LIGHT.md` (+50 / -16) and adds one row to
`docs/findings/README.md`. Against the base, the net change is the one added
page and that one index row.

I applied all five lenses at this head. Both of my round-1 MINOR findings
(F1, F2) are resolved, and so are the three MINOR findings of the external
round R393-1 (F1, F2, F3). No BLOCKER, MAJOR or MINOR finding is open. Three
SUGGESTIONs remain (S1, S2 and the retained round-1 F7). They are optional and
do not affect coverage.

I re-derived every number the delta changes from the hash-verified raw
captures, using decoders written for this round. That covers the 777-frame stop
tail, the census of words outside the region, the transition frame, 36 beat
crossings with 34 in the beat row, the two crossings inside underrun clusters
at 129,825 and 411,321, and the roughly 25 s of non-playback in the unrouted
recordings. All of them agree exactly. The measurement tables are unchanged
apart from the beat-row label. All 17 documentation and scope gates return
rc 0 at the exact head.

## Method

- **Reading order.** I read the sources in this order:
  - AGENTS.md and CONTRIBUTING.md (as in round 1), then `docs/README.md`;
  - the #451 body, including the recipe checklist;
  - the PocketBeagle 2 amendment (5729936674), which defines the wiring;
  - the owner report (5872564358);
  - the round-2 assignment (5872564881);
  - the round-2 executor's TAKEN (5872586533) and REVIEW READY (5872792112);
  - the PR #616 body and issue #617;
  - the delta diff and the history;
  - the public evidence archive at `851f835c`.

  I read the R393-1 review only after my own pass over the delta, to settle
  its findings at this head (see "Prior public findings").
- **Raw inputs.** I hashed every raw file I read before using it
  (`raw-hashes.txt`). All eight match the author's `RAW-ARTIFACTS.json`. The
  four captures also match the page's artifact table and my round-1 hashes.
  The raw originals are not published: they can carry bench identifiers.
- **Decoders.** I wrote the decoders for this round and used no author tool:
  - `r392_2_din_outside.py` rebuilds the talker frame sequence from each AAF
    pcap and makes a census of every word outside the playback region;
  - `r392_2_dout_crossings.py` fits the beat line to the short, net-one-drop
    clusters, enumerates every crossing inside the capture, and assigns each
    crossing to its cluster;
  - `r392_2_tables.py` compares every table row of the page between
    `6339479d` and `335e55c4`.
- **Gates.** `r392_2_gates.sh` runs the same 17 gates as round 1, with the
  pinned Markdown environment named in the assignment. Each gate writes one
  receipt, is unpiped and records its rc.
- **Exact head restored.** The clone is at the exact head, with no untracked or
  ignored files. All 931 regular tracked files rehash to their index blobs, and
  the file modes match. The index equals the HEAD tree, and all four gitlinks
  equal the pins (`receipts/head-verification.txt`).

## Round-1 items at this head

| Item | Required | At `335e55c4` | Evidence |
|---|---|---|---|
| R392-1 F1 (MINOR), idle-high claim | State what the capture shows outside playback, including the 777 zero frames; drop "a zero word could not have come from the pin" | **Resolved.** The claim is gone from both places (`:124-125` and `:229-230` at the old head) and from the owner-items row. `:130-136` now says the pin can deliver zero words, and rests the root cause on the unrouted recordings, which are zero across about 25 s of non-playback. `:242-256` lists everything outside the region. Every number agrees with my decode (below). | `receipts/din3-long-outside.json`, `receipts/din-playback-timeline.json` |
| R392-1 F2 (MINOR) = R393-1 F1, no issue for the frame-coherence defect | Link #617 where the page names the defect and in the owner-items row | **Resolved.** #617 is linked in the summary (`:15-18`), in the section (`:294-295`), in the owner-items row (`:409`) and in the index row. #617 is open and cites this page's evidence. | `receipts/hosted-and-links.txt` |
| R393-1 F2 (MINOR), missing index row | Row in `docs/findings/README.md` | **Resolved.** `docs/findings/README.md:11` is at the top of "Current entries". The index has no written ordering rule. On live dev `ce550952` the most recently added rows (#75, #397) are also at the top, so putting this row first follows the practice. A textual conflict with those rows is expected at the merge turn (see "Pending manager duties"). | `docs/findings/README.md:8-18`; dev `ce550952:docs/findings/README.md` |
| R393-1 F3 (MINOR), wiring check and conductor count | Cite the owner report; make the count agree with the cited spec | **Resolved.** `:109-113` and `:401` cite 5872564358. That comment says "checked end to end (BCLK, FSYNC, DOUT, DIN and ground) and found correct, with no change made", and the page repeats exactly that. The amendment's wiring table says "Seven conductors: four signals, three grounds", and `:112-113` says the same. The "all five connections" text is gone. | #451 comments 5872564358 and 5729936674 |
| S2 (R393-1; my F3), transient status line | Drop the status token | **Taken.** `:3` reads `[A403] Refs #451.` | page `:3` |
| S3 (R393-1; my F4), USB Audio device checklist item | State it is not delivered | **Taken.** `:408` is a NOT RUN row that quotes the #451 checklist item ("through the USB Audio device") and says both legs used McASP0 directly. | page `:408`; #451 body, "Before trusting audio" |
| S4 (R393-1; my F6), PR body commit count | Correct it | **Taken.** The PR body now says "Five commits", lists all five and describes the net change correctly. The PR API reports 5 commits and 2 changed files. | `receipts/scope.txt`; PR #616 body |
| S5 (R393-1), DOUT beat-crossing count | Correct it | **Taken.** `:310` labels the row as the 34 crossings clear of any underrun, and `:314-316` gives 36 in total, with the other two inside the underrun clusters at 129,825 and 411,321, both in the "no host-visible lateness" row. `:287` now cites lines 959 to 960, which is correct: those lines are the TDM arm, and 958 is the I2S arm. | `receipts/dout-long-crossings.json`; `receipts/scope.txt` |
| S6 (R393-1), archive link | Link the public evidence archive | **Taken.** `:417-421` links `tree/851f835c.../review-evidence/451-r1/author`. That path exists, and `851f835c` is an ancestor of the `451-review-evidence` tip (ahead by 2, behind by 0). | `receipts/hosted-and-links.txt`, `receipts/archive-check.json` |
| My F5 (SUGGESTION), index row | Optional | Answered by the R393-1 F2 fix above. | - |
| My F7 (SUGGESTION), fitted alignment behind the 9 / 8 underrun split | Optional; not in the taken list | **Retained as a SUGGESTION** and unchanged at `:311-312`. The totals it rests on reproduce exactly (below). | `receipts/dout-long-crossings.json` |

## Re-derived evidence for the changed text

| Page claim at `335e55c4` | Reviewer decode | Receipt |
|---|---|---|
| `:242` 1,193,185 frames outside the region | 4,553,220 frames; region 150,490 to 3,510,524 (3,360,035 frames, every frame all-own-tag); outside 1,193,185 | `receipts/din3-long-outside.json` |
| `:244-245` frames 0 to 150,488 and 3,511,302 to 4,553,219 read `0xffffff00` in every word | All-idle frame runs outside the region: exactly [0, 150,488] and [3,511,302, 4,553,219] | same |
| `:246-247` frame 150,489 reads `ffffff00`, `fff80000`, then six zeros | `ffffff00 fff80000 00000000 x6` | same |
| `:248-252` stop tail: frames 3,510,525 to 3,511,301 (777 frames, 16.2 ms); first frame torn, pair 0 zero, pairs 1 to 3 at `0x44ff`; next 775 frames all zero; last frame holds five zeros, two `ffffff00` and one `00ffff00` | Tail [3,510,525, 3,511,301] = 777 frames = 16.19 ms. Frame 3,510,525 = `00000000 00000000 0344ff00 ... 0844ff00`, and the last region frame has pair 0 at `44ff` with pairs 1 to 3 at `44fe`. All-zero run [3,510,526, 3,511,300] = 775 frames. Frame 3,511,301 = `ffffff00 ffffff00 00000000 x5 00ffff00` | same |
| `:254-256` 9,545,480 words outside: 9,539,259 `ffffff00`, 6,213 zero and 8 others (`fff80000`, six pattern words of frame 3,510,525, `00ffff00`) | 9,545,480 = 9,539,259 + 6,213 + 8, and the eight others are exactly those values. The 6,213 zeros are 6,207 in the stop tail plus 6 in frame 150,489 | same |
| `:130-131` the stop-tail zeros came in through the TDM input | The first tail frame has the per-pair torn shape (pair 0 newest), which only the TDM hold path produces (`KL_chan_map_capture.sv:486-487`, `:959-960`) | same; `receipts/scope.txt` |
| `:132-135` unrouted recordings 94.8 s and 94.9 s, each holding 70 s of playback, so about 25 s without playback, zero as well | 4,550,280 frames = 94.80 s and 4,554,432 frames = 94.88 s. Every word is `00000000`: 36,402,240 and 36,435,456 words. On the recording host's clock, the 70.3 s play step lies inside each recording: 22.3 s and 24.4 s of recording follow it, and 24.5 s and 24.6 s of each recording lie outside it | `receipts/din-long-outside.json`, `receipts/din2-long-outside.json`, `receipts/din-playback-timeline.json` |
| `:135-136` routed recording reads `0xffffff00` before playback and after the stop tail | As above, about 3.1 s before and 21.7 s after | `receipts/din3-long-outside.json` |
| `:128` the map edit was the only change between the second session's two runs | The routed run's step sequence is the unrouted one plus `map-initial`, `map-add`, `map-remove` and `map-final`; the unrouted run has no step the routed run lacks. The DUT state dumps differ only in timestamps and running counters | `receipts/din-playback-timeline.json` |
| `:310` beat row: 34 clusters, 657 / 691 | 51 clusters, 2,173 / 2,191. The fitted beat line has a period of 93,990.39 frames and 36 crossings inside the capture. 34 of them fall in short net-one-drop clusters totalling 657 / 691, which are exactly the author's `beat` clusters | `receipts/dout-long-crossings.json` |
| `:314-316` the other two crossings fall inside the underrun clusters starting at 129,825 and 411,321, both in the "no host-visible lateness" row | The crossing predicted at 129,825 falls in cluster 129,825 to 131,181 (483 / 484), and the one predicted at 411,796 falls in cluster 411,321 to 411,852 (25 / 25). The author's attribution classes both as `unexplained`, the "no host-visible lateness" row. My cluster boundaries match the author's for all 51 | same |
| `:311-312` rows 9 / 975 / 963 and 8 / 541 / 537 (unchanged) | Summing my clusters under the author's classes gives sender 9 / 975 / 963 and unexplained 8 / 541 / 537 | same |
| `:112-113` seven conductors, four signals and three grounds | The amendment's table has BCLK, FSYNC, DOUT and DIN, plus GND J11.1, J11.37 and J11.38: "Seven conductors: four signals, three grounds" | #451 comment 5729936674 |
| Measurement tables unchanged | 11 tables at both heads. The only changed measurement row is the beat row, whose label changed and whose figures did not. The other row changes are the required owner-items edits: the DIN path, continuity and coherence rows, and the new USB Audio device row | `receipts/page-table-delta.json` |

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

**S1 - SUGGESTION - lenses: Docs, Tests**

- **Where:** `docs/findings/451_TDM8_FIRST_LIGHT.md:417-421` and the linked
  archive artifact `851f835c:review-evidence/451-r1/author/MANIFEST.sha256`.
- **Evidence:** The delta newly links the archive, and says the packet's
  manifest "covers every retained file except itself". Coverage holds: 211
  entries, no retained file unlisted, and the manifest does not list itself.
  A cold reader who runs `sha256sum -c` on it at `851f835c` still sees three
  FAILED lines:
  - `gates/gates.json` and `gates-s2/gates.json` are explained. The archive's
    own `MANIFEST.json` records each as `path_redacted`, with its original hash
    equal to the author-manifest hash.
  - `PR-BODY.md` is not explained. The author manifest lists `699c8daa...`, but
    both the original and the published hash in `MANIFEST.json` are
    `248a2499...`, and no redaction record covers it.

  The archive-level `MANIFEST.json` matches every published file (212 of 212).
- **Impact:** None on the page's measurements. All raw-artifact and capture
  hashes are unaffected, and the file concerned is a draft PR body. A cold
  reader nevertheless meets an unexplained integrity failure in the packet the
  page points to.
- **Suggested outcome:** One of the following:
  - say where the page links the archive that the archive-level
    `MANIFEST.json` is the published-bytes authority;
  - have the archive annotate the stale `PR-BODY.md` entry.
- **Verification:** `receipts/archive-check.json` re-run against whatever
  commit the link names.

**S2 - SUGGESTION - lens: Docs**

- **Where:** `docs/findings/README.md:11`, the State column.
- **Evidence:** The State column lists the continuity check, scope and
  calibrated items as NOT RUN. It does not list the capture through the USB
  Audio device, which the page's owner-items table now records as NOT RUN
  (`:408`). The row does not overclaim.
- **Suggested outcome:** Optionally name that item in the State column, so the
  index shows the #451 checklist item that is still outstanding.

**Retained R392-1 F7 - SUGGESTION - lenses: Docs, Tests**

- **Where:** `:311-312`, unchanged.
- **Evidence:** The 9 / 8 split between "after logged talker lateness" and "no
  host-visible lateness" depends on a fitted alignment. The totals and the beat
  class reproduce exactly.
- **Status:** Optional, and not taken in round 2.

Outside the PR: the body of #617 cites `KL_chan_map_capture.sv` "lines
958-960". The TDM arm is 959 to 960, which is what the page now says. This is
the issue's text, not the PR's, and nothing is required here.

## Prior public findings on this PR

I read R393-1 (PR #616 comment 5872558700) after my own pass. Its findings at
this head:

| Finding | Severity and lenses as assigned | Disposition at `335e55c4` |
|---|---|---|
| R393-1 F1, coherence defect has no issue | MINOR; Docs | Resolved: #617 is linked in three places on the page and in the index row |
| R393-1 F2, findings index row | MINOR; Docs | Resolved: `docs/findings/README.md:11` |
| R393-1 F3, "all five connections" without a public source | MINOR; Docs, Conformance | Resolved: cited to 5872564358; the count agrees with the amendment's seven conductors |
| R393-1 S1, outside-region words | SUGGESTION, superseded by R392-1 F1 | Resolved with R392-1 F1 |
| R393-1 S2 to S6 | SUGGESTION | Taken (table above) |
| R393-1's retention of R392-1 F1 and F2 | MINOR | Resolved (table above) |
| R393-1's retention of R392-1 F3 to F7 | SUGGESTION | F3, F4, F5 and F6 taken; F7 retained as an optional SUGGESTION |

No MINOR or higher finding from any round remains open.

## Clean-lens results

```text
[R392] PASS Conformance - docs/findings/451_TDM8_FIRST_LIGHT.md:1-24,105-137,396-413; docs/findings/README.md:11; #451 body checklist, amendment 5729936674, owner report 5872564358, assignment 5872564881 items 1-4 and S2-S6; #617 - every required item and taken suggestion is met; the wiring text matches the owner report verbatim and the amendment's seven conductors; the new USB Audio device row states the #451 checklist item as NOT RUN; the root-cause argument (empty dynamic output map; the map edit is the only procedural change) is stated in a supportable form; the page still closes nothing, and #386 acceptance 4, #117 and the scope items stay NOT RUN
[R392] PASS RTL - hdl/ieee1722/aaf/KL_chan_map_capture.sv:486-487,959-960; hdl/milan/milan_datapath.sv:1344; receipts/scope.txt - no RTL, config, software or gitlink path changes in 6d5ebd73..335e55c4 or from image source 9e9954e9 to the head (0 paths); the page's RTL citations, including the corrected 959 to 960, point at the per-pair TDM hold write and the TDM read arm; the frame-coherence mechanism text is unchanged apart from that line reference
[R392] PASS Robustness - receipts/din3-long-outside.json, din-long-outside.json, din2-long-outside.json, din-playback-timeline.json, dout-long-crossings.json - playback start and stop boundaries word by word (transition frame, 777-frame stop tail, idle runs); unrouted versus routed across the non-playback intervals; play-step containment in all three recordings; beat crossings that coincide with underrun clusters; the stop-boundary text now matches the capture
[R392] PASS Tests - raw-hashes.txt (8 of 8 match RAW-ARTIFACTS.json); r392_2_din_outside.py, r392_2_dout_crossings.py, r392_2_tables.py and their receipts; receipts/gates/gate-1..17 (all rc 0) - every changed number re-derived exactly from raw captures by independent decoders; unchanged measurement rows confirmed row by row; no executable test is in scope for a documentation-only delta
[R392] PASS Docs - docs/findings/451_TDM8_FIRST_LIGHT.md (all 438 lines) and docs/findings/README.md at 335e55c4; receipts/gates/gate-1..17; receipts/page-table-delta.json; receipts/hosted-and-links.txt; receipts/archive-check.json; PR #616 body - all links resolve (#617 open, comment 5872564358, archive tree at 851f835c); the index row is present; the status token is removed; the commit count is correct; no private host, path, address or tool name appears in the 51 added lines; S1 and S2 are optional
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page `:1-24,105-137,396-413`; index `:11`; #451 body and checklist; amendment 5729936674; owner report 5872564358; assignment 5872564881; #617; R393-1 F3 disposition | R392-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| RTL | CLEAN | `KL_chan_map_capture.sv:486-487,959-960`; `milan_datapath.sv:1344`; range and image-source scope (0 RTL, config, software or gitlink paths), `receipts/scope.txt` | R392-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| Robustness | CLEAN | routed and both unrouted pcaps, word census outside the region, stop tail and transition frame, play-step timeline, beat crossings inside underrun clusters (`receipts/din*-outside.json`, `din-playback-timeline.json`, `dout-long-crossings.json`) | R392-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| Tests | CLEAN | 8 hash-verified raw inputs; three reviewer probes and their receipts; author cluster attribution cross-checked (51 of 51 boundaries match); 17 gates rc 0 | R392-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |
| Docs | CLEAN (S1, S2 and retained F7 are SUGGESTIONs) | full page and index at the head; table delta; link targets; public-record scan of the added lines; archive manifest cross-check; PR body; gates | R392-2 | `335e55c4135979a554dc0281d6980ac1e2158aee` |

The head `335e55c4` changes every artifact in these lenses' scope that the PR
touches, so round 1's CLEAN results for Conformance and RTL at `6339479d` do
not carry forward. This round re-covers all five lenses at the exact head.

## Limits

- **Raw captures not published.** The raw captures were read from the run's
  raw root on the bench host after hash matching. They are not published, and
  anyone holding bytes with the listed hashes can reproduce the decode.
- **Timeline precision.** The play-step timeline uses the controller host's
  event log and the pcap timestamps on the same host. It bounds the play step,
  not the first and last sample on the pin. The page's "about 25 s" figure is
  consistent at that precision.
- **Unchanged text taken from round 1.** Page text this delta did not change
  was not re-derived in this round; round 1 covered it at `6339479d`. The DOUT
  listener counters, the uncalibrated gPTP-slope figure, the talker pacing and
  the peer-side restoration states remain as limited in round 1.
- **No simulation or hardware.** No simulation, builder or synthesis probe was
  run, and none was needed for a documentation-only delta. The scoped
  simulator was not used, so its identity was not checked. There was no
  physical measurement. Calibration, continuity and scope items stay NOT RUN,
  and field skips are not hardware proof.
- **Hosted checks at the exact head, observed at 2026-09-28T15:24Z:**
  - 0 check runs, 0 commit statuses and 0 workflow runs for `335e55c4`;
  - PR #616 reports `mergeable_state` `dirty`, consistent with the
    index-row conflict against live dev that the executor disclosed.

  No hosted evidence exists at this head. That is not a pass.

## Pending manager duties

- **Hosted and local acceptance.** The manager owns hosted and act acceptance
  at the exact head. Hosted workflows had not run when observed, and the PR
  merge state is `dirty`.
- **Candidate merge.** The manager validates the current-dev candidate at the
  merge turn: base `6d5ebd73`, live dev `ce550952`. That includes resolving the
  `docs/findings/README.md` conflict with the #75 and #397 rows, keeping all
  rows, and re-running the Markdown gates on the candidate. A change to the
  page or index at the candidate re-opens Docs.
- **Second review.** The second independent review, R393-2, is still required.
- **Merge authorization.** The merge needs explicit maintainer authorization.

R392-2 FINISHED
