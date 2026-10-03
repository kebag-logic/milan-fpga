[A519] Bench lane B7: #629's bench acceptance on dev `bbf704ec`, after PR #634

Refs #629

Adds a dated section, "Dev bbf704ec, 2026-10-03: lane B7", to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and updates its row in `docs/findings/README.md`. Round 3 also drops the external capture's sample format from lane B6's raw-hash row in the same page. No other file changes.

Head: `40714c1bd166c2a05f9607a861e8550c705d183a`, three commits on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`: round 1 `4eee41a558a56024e57b27a956fdaf7910ca69dc`, round 2 `f4eb39d3fddbbd9e2de1947750cc1b482baff53d` and round 3 on top of it (see "Round 2" and "Round 3" below).

## What was measured

Lane B6's method, tools and grading rules on the image with #634, with every change stated on the page. The grading criteria were written down at 14:50 CEST, during A0's window (14:42:08 to 14:52:39), not before any graded case: the page gives the time each change was fixed and the basis of A0's threshold. Each window is 630 s, untouched. The listener's format was adapted before every bind and the talker's never set. Clock sources were set only on the listener's CLOCK_DOMAIN, read back, and restored.

| Case | Talker to listener, the listener follows | Result |
|---|---|---|
| Identity | VERSION `00020060`; AEM image, BIOS ROM and QSPI bitstream payload CRCs equal the build's; every live descriptor byte-equal to the build's AEM image; CLOCK_SOURCE 0 INTERNAL, 1 CRF, 2 the AAF input's INPUT_STREAM source | PASS |
| Tool controls | Synthetic slips and drift | PASS, byte-equal to lane B6's |
| A0 | DUT to peer, the peer on INTERNAL | PASS as a control: net +5.92 ppm of listener drops; the DUT's INTERNAL beat is gone |
| A1 | DUT to peer, the peer follows the DUT's AAF | PASS: 0 listener discontinuities, 0 net steps |
| A2 | DUT to peer, the peer follows the DUT's CRF | PASS: 0 listener discontinuities (lane B6: 494 drops, 180 inserts) |
| B0 | Peer to DUT, the DUT on INTERNAL | PASS as a control: +5.92 ppm counted. One DUT GET_COUNTERS timed out at the second mark; not analysed |
| B-CRF | Peer to DUT, the DUT follows the peer's CRF | PASS: LOCKED 3.1 to 3.6 s after the set and at every read; 0 net steps in 30,169,440 frames |
| B-AAF | Peer to DUT, the DUT follows the peer's AAF (CLOCK_SOURCE 2) | PASS: LOCKED 6.6 to 7.1 s after the set and at every read; 0 net steps in 30,131,520 frames; meter history never restarted, largest deviation 29 ns. Outside the criteria, the INTERNAL-to-AAF switch is not shown free of undeclared discontinuity: the DUT's listener ring slipped one frame after lock (#645) |
| Lock loss (observation) | Unbind of the followed AAF talker for 11.1 s | As declared: HOLDOVER within 0.56 s, the index kept, one `mr` toggle at the loss and none at the return, LOCKED 5.6 to 6.1 s after the return |
| INTERNAL clock (observation) | Frame-rate ratio against the peer | +5.92 ppm from the peer, about -5.1 ppm against gPTP time; the oscillator grade stays the owner's known risk |
| Direction B THD+N | Known-signal probe repeated | NOT RUN: no known signal on the peer's talker channels |

## #629 acceptance

Judged item by item on the page. Not every item is met, so this PR refers to #629. What stays open:

- the bench quality metric for Direction B: no known signal reaches the peer's talker without a wiring change;
- the fabric item's switch: the one switch run here, INTERNAL to AAF, leaves an undeclared one-frame slip on the DUT's listener ring after lock, which #645 takes;
- no bench evidence for a switch between the AAF and CRF streams, a followed CRF stream's lock loss, or the saved selection across a power cycle; simulation covers them.

A2 and B-AAF rest on lane B6's capture-path attribution. Five capture-path clusters are one or two frames off its size signature, and the page states the conservative reading: A2 would hold 3 listener frames in 2 clusters and B-AAF 3 in 3, and both would fail.

## Evidence

The evidence packet `629-b7-a519` is published on branch `629-b7-review-evidence` at `c6ad37e7d9163b5a85aef935a7d8e7f7f6686f7f`, path `review-evidence/629-b7-r1/author/`. The page gives the path mapping, every hash, and where each hash row is recorded: each run's `events.jsonl`, the packet's `RAW-ARTIFACTS.json`, or `redaction.json` for the two masked tools as run.

The packet was first published at `95448218`. In the tools, the lane packet's redaction pass had masked the external capture's channel count only in the channel-count assignment of `run_b7.py` and `run_b6.py`, and its sample format nowhere. Two later commits masked the rest:

- `d36de704` masked the channel count in the docstrings of `run_b7.py`, `grade_b7.py`, `run_b6.py` and `grade_b6.py`, and the sample format in the docstrings of `run_b7.py` and `run_b6.py` and in their code, as the capture command's format argument;
- `c6ad37e7` masked the channel count in the capture file's name, in 19 files: `RAW-ARTIFACTS.json`, each captured run's `events.jsonl` and lock record (seven runs, the B-AAF shakedown among them), and the code of the same four tools.

Both were added on top of the branch with no force-push, so `95448218` and `d36de704` stay in its history as published. Neither changed a file the page's evidence table cites, and the raw rows are recorded unchanged. The page and this body state neither value.

## Validation

At `40714c1b`, every command rc 0:

- `scripts/docs_check.py` (0 findings), `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/gen_toc.py --verify-anchors`, `scripts/check_em_dash.py --base bbf704ec`, `scripts/check_doc_paths.py` (the pinned Markdown environment)
- `scripts/ci_scope.py --selftest`
- `scripts/check_baremetal_only.py --check` and `--selftest` (the bare invocation is a usage error, rc 2)
- `scripts/check_feature_status.py --self-test`
- `git diff --check`, `git diff --check bbf704ec HEAD` and `git diff --check f4eb39d3 HEAD`
- the page's 45 hash rows, checked against the published packet at `d36de704` and at `c6ad37e7` and against the lane packet's records: 0 problems at both

## Round 2

Answers R450-1 and R451-1, both NEGATIVE at `4eee41a5` on MINOR documentation findings. Docs only: no bench access and no new measurement; every figure comes from the round-1 run artifacts. No verdict changes.

| Item | Finding | Change at `f4eb39d3` |
|---|---|---|
| 1 | R450-1 F2 = R451-1 F1: the grading order | "B7: method changes" says the criteria were written down at 14:50, during A0's window (A0 started 14:41:42, window 14:42:08 to 14:52:39, `runs/a0/events.jsonl`). A "Fixed" column places each change: the run-method changes in the run tool at 14:37, before A0; the A0 threshold, the beat attribution and the B-AAF bench row at 14:50, during A0's window; the `tone.repeats` summary fix at 14:55, after A0's first grade. It names the other criteria fixed at 14:50, the verdict tool's last write (15:40) and the `SLIP_LB` decode (14:58, used by no criterion). A0's threshold's basis is given apart from A0's data (lane B6's counted +6.52 ppm, and A2-a removing the 10.6 ppm beat), and A0 meets #629's "the metric must show the mismatch" whatever the threshold (186 of 630 blocks off the floor, 761 listener events). This body's sentence is corrected |
| 2 | R451-1 F2: where the evidence lives | "B7: artifact hashes" names the branch, the pinned commit `d36de704`, the path `review-evidence/629-b7-r1/author/` and the path mapping, as lane B6's section does. It says which rows each run's `events.jsonl` records (the 19 raw-file and tone-loop rows), that `RAW-ARTIFACTS.json` alone records the seven full-grade rows, and that the two masked tools' hashes are `redaction.json`'s `original_sha256`. It notes the four docstrings `d36de704` masked after publication (R450-1 F6); round 3 corrects that description |
| 3 | R450-1 F1: figures | The capture's drift reads 0.54 to 0.93 frames/s over the six windows. The conservative count is on one basis: A2 3 listener frames (2 clusters), B-AAF 3 (3 clusters) |
| 4 | R450-1 F3: the B0 timeout | Recorded in "B7: Direction B": the DUT's GET_COUNTERS on CLOCK_DOMAIN 0 at `window-mark-1`, 15:20:58, timed out after 1 s and was not retried. The mark's next DUT command answered at once, and the next mark (15:25:57) answered with 3/2. It is the only non-SUCCESS of the DUT's 336 AECP commands; its cause is not analysed. Also a limits bullet and a pointer from the method row |
| 5 | R450-1 F4 = R451-1 RESIDUE-1: the skipped context | The Simulation row says every executed context of PR #634 was SUCCESS (21) and names "Physical gPTP (nightly and manual)" as skipped |
| 6 | R450-1 F5: the fabric row | The Fabric row, the B-AAF summary row and the listener-ring paragraph say the INTERNAL-to-AAF switch run here is not shown free of undeclared discontinuity. They cite the post-lock `SLIP_LB` slip (386 to 388) and the 6 dups between the set and the window, and link #645. The closing acceptance sentence and the limits name it |
| 7 | R450-1 R1 and R2 | R1: "The tables below are arranged from `summary/tables.md`, which `b7_tables.py` renders from the grades; every value is unchanged." R2: "LOCKED 5.6 to 6.1 s after the return", on the page and in this body |
| 8 | R451-1 RESIDUE-2, a note | The round-1 REVIEW READY comment said "12 live descriptors". The identity verdict grades 11 live descriptors byte-equal, plus the CLOCK_SOURCE 3 absence check. The page says 11 and is unchanged; the comment is not edited |
| 9 | Suggestions | Not taken in this round (R450-1 S1 to S3, R451-1 S1 and S2). R451-1 S3 is covered by #645 |

## Round 3

Answers R450-2 and R451-2, both NEGATIVE at `f4eb39d3` on MINOR documentation and privacy findings. Docs only: no bench access and no new measurement; every figure comes from the round-1 run artifacts. No case verdict, result or acceptance judgement changes.

| Item | Finding | Change at `40714c1b` |
|---|---|---|
| 1 | R450-2 F1 = R451-2 F1: a private capture value on the page | Lane B7's and lane B6's `a0/cap-lr.raw` rows read "(the tone's two channels)" and no longer state the capture's sample format; lane B6's row is changed under the round-3 assignment. The page, the findings index and this body state neither the format nor the channel count. The manager masked the channel count in the published packet at `c6ad37e7`. A value-blind scan finds neither value on the page, in the findings index, in this body or in the packet at `c6ad37e7` |
| 2 | R450-2 F1 (b) = R451-2 F2: the masking described | "B7: artifact hashes" says what the lane packet's redaction pass masked in the tools and names both later commits with what each changed, in docstring or code: `d36de704` (the channel count in four docstrings; the format in two docstrings and in the capture command's argument) and `c6ad37e7` (the channel count in the capture file's name, 19 files). It states that both were added on top with no force-push, so `95448218` and `d36de704` stay in the history. The packet pin is now `c6ad37e7`; all 45 hash rows hold there. "Two tools name the external capture's channel layout" now reads four, as `redaction.json` lists |
| 3 | R451-2 F3 = R450-2 RES-1: B0's next command | "the DUT answered the mark's next command, GET_COUNTERS on STREAM_OUTPUT 0 (seq 22913), and its other three, at once." (`runs/b0/ctl.jsonl`, seq 22912 to 22917) |
| 4 | R450-2 RES-2 | "Each run's `events.jsonl` records the size and SHA-256 of every raw file of its run, among them the three per case below and the tone loop: the first 19 rows below." |
| 5 | R450-2 RES-3 | The "Round 2" table above is renumbered: the second 7 is 8, and 8 is 9 |
| 6 | R451-2 RESIDUE-1 | The 32,768-tick bound is cited to TIME_SYNC's clock-source settle row, after the Switching sources link |
| 7 | R451-2 RESIDUE-2 | The round-3 packet handoff's identity step reads "11 live AECP descriptors byte-equal, plus the CLOCK_SOURCE 3 absence check" |
| 8 | R451-2 S1 | "B7: method changes" says the order it gives supersedes the 14:50 record's heading in the published `author/HANDOFF.md` and the `grade_b7.py` docstring, and that the round-2 handoff carries the corrected heading |
| 9 | R451-2 S2 | The 6 dups lie between the DUT's read before the binds and the window's first read, 1 s into the window: an interval holding both binds, the set and the 20 s in which the servo locked. The B-AAF summary row and the Fabric row say "from before the binds to the window's first read" |
| 10 | R451-2 S3 | "No B0 criterion used that mark": B0 is graded on its counted ratio alone, and B-AAF's CLOCK_DOMAIN check reads the first and the last mark |
| 11 | Not taken | R450-2 S1 to S4 are outside the round-3 assignment; `docs/findings/README.md` is unchanged since round 1 |
