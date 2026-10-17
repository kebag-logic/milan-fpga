[R634] NEGATIVE - exact head 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b

# R634-1: internal cleared-context review of PR #758 (Refs #117), bench lane B21

Head `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b`, tree `a5f405e02461121570f89d27955e245269ed87d2`,
three one-line commits on source base `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`. The diff is one file,
`docs/findings/117_AUDIO_CONTINUITY.md`, +622 lines (+224, +64, +334): three dated sections
(round 1 STOP, round 2 STOP, round 3 PASS as measured).

**Bottom line.** Every graded round 3 figure I could re-derive from the published records holds. The
graders fail on every fault I planted. Round 3's measurement supports the row as measured on the
installed dev `9ef71772` image. The verdict is NEGATIVE for three MINOR evidence and accuracy defects
on the page, under `Tests` and `Docs`. None of them changes a round 3 grade. Each needs a page
correction, or published evidence, before the `Tests` and `Docs` lenses are clean. Five RESIDUE
wording items and five SUGGESTIONs follow.

## Reconstruction and inputs

- **Authorities.** Read in this order: AGENTS.md and CONTRIBUTING.md (sections 2, 4 and 6), and issue
  #117's body (acceptance box 4: audio continuity passes without a stale or skipped mandatory row;
  box 5: findings carry topology, capture points, raw artifacts, hashes, tools and method).
- **Issue #117 comments.** The B21 assignment (6208207821: step 1 capture-path self-test, steps 2
  and 3 with taps on both links, the DUT CSRs and the peer counters, step 4's pass rule, step 5 the
  trace), the TAKEN (6208396842), the two STOPs (6208887896, 6217670001) and the round 3 REVIEW READY
  (6231525820).
- **Owner decision of 2026-09-30.** Issue #625's body: bench audio capture uses the SoC board's
  McASP directly, and the USB path is out of scope.
- **Register map.** `docs/reference/REGISTER_MAP.md` for `SLIP_LB`/`SLIP_TDM` (0x8D4),
  `RENDER_STAT` (0x8DC), the AAF clock meter (0x8E0) and the stream counters' FRAMES_RX semantics.
  The per-interval FRAMES_RX note is at `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2087`.
- **Public executable evidence.** Commit `a43529800735820f1662690e4457bf9a6ece27e4`, tree
  `review-evidence/117-b21-r1` = `e0a908f7985f4e9987a3f6137f6043b5454dda25`. All 380 `MANIFEST.json`
  entries equal their `published_sha256`, and 78 are label-masked
  (`receipts/rederive_r3.txt`, `receipts/evidence_inputs.txt`).
- **Raw files.** Large raws are not available to this review. They are in the project's cold
  archive; `author/raw-retention-receipt-r3.txt` lists 82 files, `82 OK, 0 BAD`.
- **Prior public review findings on PR #758.** None at review time: two review-start notices, no
  review and no review comment. Nothing to resolve or retain.

## Re-derivation (receipts/rederive_r3.txt, scripts/rederive_r3.py)

The script reimplements the deficit, floor and block tests from their written definitions; it does
not import the packet's tools. Figures for which the packet publishes only tool outputs (tap and
McASP grades, restart cycles) were re-derived arithmetically from those outputs and cross-checked
for internal consistency.

| Figure on the page | Re-derived | Source |
|---|---|---|
| Identity gate 11 of 11, three times | 11 PASS lines and `IDENTITY GATE: PASS` in each | `author/r3/identity*/identity-verdict.txt` |
| Self-test `mst-long`: 630 s, 63,000 reads, 480 frames each, 0 overruns, 0 stalls, longest 11.1 ms, +43.06 ppm | 63,000 reads, 62,999 intervals, 630.017 s, max 11.1 ms, 0 over 15 ms, +43.06 ppm; stamper `dropped_bytes=0` | `mst-long-reads.u16` (hash equal), `mst-long-reads.json` |
| 10 s block floors within -3.50 to +1.94 | -3.50 .. +1.94, largest block-to-block change 2.81 | same |
| 11-read floor test reads as about ±16-frame steps | W=10: steps -16.8 .. +18.5 in 610 groups, about 1.03 s apart | same |
| W=110 floor test: "9 groups of +6 to +8 frames" | 9 groups. Absolute steps are +6.3 .. +8.4 for eight groups and **-2.5** for one (reads 57646 .. 57845). Relative to the +2.30 drift they are +4.0 .. +6.1 and **-4.8** | F1 |
| Direction A taps: 5,198,452 and 5,198,499 packets over 649.8 s, 0 sequence breaks, steps 124,999 .. 125,020 ns, `tv` set, 192 bytes | equal | `author/r3/summary/dA-wire.json` |
| Pattern frames 30,951,504 (644.8 s), all valid and in order; 0 repeats, skips, torn or invalid | `region_frames == valid`, `in_order == valid - 1`, all event counts 0, both taps | same |
| 5,198,372 common packets equal | 80 + 5,198,372 + 0 = DUT tap; 0 + 5,198,372 + 127 = peer tap; header (sequence and timestamp) and payload equal on all | same |
| Transit -27.7 .. +23.9 µs after the tap clocks' 13.07 ppm; CRF 500 pps with no sequence break on either tap | Not computed by any published tool. The published transit is ±4.2 ms with drift included. CRF rate and SEQ_NUM_MISMATCH 0 are supported by the counters (DUT SO1 FRAMES_TX = peer SI8 FRAMES_RX = 327,845) | F2 |
| Direction A CSRs: 128 samples; `SLIP_TDM` 0; `SLIP_LB` 0xFFFF; `RENDER_STAT` converged, prefill clear, fill 8 .. 14, rails 0; `AVTPRX_STAT`/`ERR` static; +5,079,938 / +121,918,506 in 635.0 s | equal, decoded against REGISTER_MAP 0x8DC's bit layout | `author/r3/runs/dA/dut-poll.txt` |
| DUT SO0 FRAMES_TX = peer SI0 FRAMES_RX = 5,245,516 over 655.7 s; no error counter moved | equal. TIMESTAMP_VALID also moved (R2) | `author/r3/runs/dA/counters-*.jsonl` |
| External cross-check: 30,624,574 valid (638.0 s), 0 repeats, skips, zero or torn, 0 stalls in 64,005 reads | equal | `author/r3/summary/dA-ext.json` |
| Direction B: peer tap 5,198,371 packets, 0 breaks, steps 124,953 .. 125,042 ns, 96 bytes; all present and equal on the DUT tap (5,199,125) | equal; partition 139 + 5,198,371 + 615 | `author/r3/summary/dB-wire.json` |
| McASP 30,480,000 frames (635.0 s), one constant offset, 0 skips, repeats or foreign | matched 30,480,000, offset changes 0, foreign 0, first aligned frame 0 | `author/r3/summary/dB-mcasp.json` |
| McASP capture: 0 overruns, 0 dropped bytes, 25 read stalls up to 87.1 ms, next reads 960 or 1,920 frames | 25 over 15 ms, longest 87.07 ms; six reads of 960/1,920 frames; ring peak 483,840 B of 64 MiB | `dB-reads.u32.gz` (hash equal after gunzip), `dB-reads.json` |
| Board-side and host-side hashes of the McASP files agree | `dB.pcm`, `dB.ts`, logs: equal | `soc-collect.log` vs `raw.sha256` |
| Direction B counters: peer SO0 5,207,829, DUT SI0 FRAMES_RX 5,207,944 over 651.0 s | equal. DUT TIMESTAMP_VALID moved 5,207,830 in the same reads (R2) | `author/r3/runs/dB/counters-*.jsonl` |
| Restarts: 20 SUCCESS binds; formats read and equal before each, no set; ended bound, flags 0x0082 | 20 binds, 20 equal pairs `0205022002006000`, 0 SET_STREAM_FORMAT, final state count 1, `0x0082` | `author/r3/runs/rA/agent.jsonl`, `cycles.jsonl` |
| Wire restart 13.4 / 13.8 / 86.8 ms; cycle 1 31.9 ms; others 13.4 .. 16.8; stop 9.7 .. 10.8 ms; no packet in any hold; first 480 frames valid | equal on the peer-link tap; DUT-link tap 13.4 / 13.8 / 86.8 | `author/r3/summary/rA-restart.json` |
| Output less steady latency 23.5 / 24.8 / 97.8 ms | recomputed restart + S/48000 - G: equal; silences all zero frames; 190.0 s capture, 0 stalls | same |
| Round 3 artifact table: 14 rows | 13 in the cold archive with equal size, 1 (`mst-long` derived record) in the packet with equal hash | `raw-retention-receipt-r3.txt` |
| Round 3 tool table | every hash equals the packet's `original_sha256`; three shell tools are published label-masked (R4) | `MANIFEST.json` |
| Round 1: losses 336 and 10,945 frames (4 and 3 ms; 2 to 88 ms, 228 ms in all); 1 ms steps about 60 s apart | equal | `author/selftest/st-long*/…-selftest.txt` |

**Time bases.** Each is stated on the page and matches the tools. The self-test uses the board's
monotonic clock, uncalibrated, against the DUT's TDM clock (the DUT is TDM master). Each restart is
timed on one tap clock, the peer link's. Transit spans two tap clocks, with drift stated. The CSR
polls carry host UTC.

**Limits stated against what each instrument sees.**
- **The taps** see every AVTPDU on each link. tcpdump's "received by filter" exceeds "captured" by
  758, 840 and 75 packets at stop. No gap falls inside any record, so these are tail packets.
- **The McASP** kept slots 0 to 3, which are the four mapped channels.
- **The external capture** sees channels 0 and 1 of the peer's output and is a cross-check.
- **Direction B's** signal is the noise already at the peer's talker inputs, as the assignment
  directed.

## Grader fault probes (receipts/probe_graders.txt, scripts/probe_graders.py)

The packet's own `b21_grade.py` (`a0f3b5ac…`) and `b21_aaf.py` (`b8fe677d…`), unmodified copies, ran
on synthetic captures. The wire probes used tap-envelope pcaps.

- **Wire grade.** It flags each fault:
  - a content repeat (repeats 1);
  - a content skip (skips 1);
  - a torn frame (torn 1);
  - a non-zero low byte (invalid 1);
  - a packet lost on either link (sequence break 1, and header/payload equality drops to 1,500 of
    2,999);
  - a peer payload bit flip (payload_equal 2,999);
  - a changed timestamp (header_equal 2,999).
- **McASP alignment** on low-level noise with 21.3% of frames equal to their predecessor:
  - a 6-frame skip reads as skips 1, 6 frames;
  - a 1-frame repeat reads as inserts 1;
  - 3 inserted zero frames read as inserts 3;
  - a bit flip reads as foreign 1;
  - a zero replacing a non-zero frame reads as foreign 1, zero 1.
  - A zero replacing a frame that was already zero is bit-exact, so it is not a fault.
- **External grade.** It flags a skip, a repeat, a zero frame and a torn frame.

So the round 3 grades are mechanical counts and able to fail. The step 1 verdict also uses the
self-test's mechanical counters (0 overruns, 0 dropped bytes, every read one period). The deficit
probe in `rederive_r3.txt` plants a loss into the published `mst-long` record. A loss of 6 frames
moves the block test to 4.6 .. 4.9 against a 2.81 baseline; 12 frames moves it to about 10.5; 48
frames to about 46. The W=110 floor test flags every plant (S2).

## Findings

**F1 - MINOR - Tests, Docs - `docs/findings/117_AUDIO_CONTINUITY.md:936-939`, artifact
`author/r3/selftest/mst-long/mst-long-analysis.txt` - the step 1 floor-test groups are misreported.**
- *Evidence.* The page says the 110-read floor test "flags 9 groups of +6 to +8 frames. Each is one
  sampler cycle missing from a window, where one early-read spacing exceeded 1.1 s." The published
  analysis lists eight groups of +6.3 to +8.4. The ninth, at reads 57646 .. 57845, has largest step
  **-2.5**, which is -4.8 against the +2.30 drift. A missing sampler cycle cannot produce a negative
  step. The "early-read spacing exceeded 1.1 s" evidence comes from the 1 Hz sample file, which is
  not published; no published output shows it.
- *Impact.* A figure in the evidence for step 1's CLEAN verdict is wrong, and its explanation is
  unverifiable from the packet. The CLEAN verdict itself still rests on 0 overruns, 0 dropped bytes,
  480 frames in every read and the 10 s block test, all re-derived.
- *Required outcome.* The page states the nine groups as the analysis prints them, including the
  negative one. The sampler-cycle explanation is either backed by a published output or marked as
  an inference, and the negative group is either explained the same way or recorded as unexplained.
- *Verification.* Re-run `B5_W=110 b21_mcasp_ana.py` on the archived `mst-long.ts`, or this review's
  `rederive_r3.py` on the published `.u16` record, and compare with the corrected sentence.

**F2 - MINOR - Tests, Docs - `docs/findings/117_AUDIO_CONTINUITY.md:967-970` and `:1023-1028` -
four stated measurements have no published computation.**
- *Evidence.* (a) "Transit … -27.7 to +23.9 µs" after "13.07 ppm": `b21_grade.py wire` publishes only
  transit minus median with drift included, -4237.5 .. +4209.1 µs in `dA-wire.json`. No published
  tool fits or removes the rate. (b) CRF "500 packets a second with no sequence break on either tap":
  no CRF tap grade is published, and the PR's reproduction list has no CRF command. The rate and the
  peer's SEQ_NUM_MISMATCH 0 are supported by counters only. (c) "About 21% of noise frames equal the
  one before." (d) "On a synthetic record built from the probe's noise, the grader recovered a
  planted 6-frame skip, a 1-frame repeat and 3 inserted zero frames exactly." Neither (c) nor (d) has
  a published script or output; the probe captures are archive-only. These figures appear only in
  the page and in HANDOFF prose.
- *Impact.* A cold reviewer cannot reproduce these claims, and (d) is the page's own argument that
  the Direction B grade can fail. This review's independent probe confirms the grader does detect
  those faults, so the row grade is not affected. The page's evidence does not show it.
- *Required outcome.* Publish the computation and output for each of (a) to (d), or remove each
  claim or mark it as not reproduced from the packet. For CRF, citing the counters is enough if the
  tap claim is dropped.
- *Verification.* The named outputs exist in a published packet and reproduce the figures, or the
  sentences are gone or qualified.

**F3 - MINOR - Tests, Docs - `docs/findings/117_AUDIO_CONTINUITY.md:659-660` (round 1), artifact
`author/selftest/st-long2/st-long2-selftest.txt` - "Each [loss] comes with frame interrupts
missing" is not true of every loss.**
- *Evidence.* In `st-long2` the loss at 530.522 s has USB shortfall **-5.2**: no interrupts missing.
  Two more, +6.8 at 510.385 s and +7.8 at 531.244 s, are within the clear-control maximum of +7.8.
  So 15 of 18 losses exceed the control range, not all.
- *Impact.* Round 1's placement of the cause "below the load the bench host can see" is overstated.
  The conclusion that the losses are on the recording side stands on the test's construction, with
  no DUT or peer in the path. Round 3 does not depend on this.
- *Required outcome.* The sentence states the counts the analysis shows, or otherwise stops
  claiming every loss.
- *Verification.* Compare the corrected sentence with the 18 `loss at t` lines of
  `st-long2-selftest.txt`.

## RESIDUE (wording only; carried to the residue checklist)

- **R1 - Docs - `:862`, `:936`, `:1122`.** "no step in the delivery deficit's floor" -> "no permanent
  step in the delivery deficit's floor" (the floor test flagged 9 groups). "110-read windows" ->
  "111-read windows (`B5_W=110`)" at both places, matching the page's "11 reads" for `W=10`.
- **R2 - Docs, RTL - `:980-984`, `:1041-1043`.**
  - "counted 5,245,516 frames sent" and "5,207,829 frames sent" -> "… AVTPDUs sent (FRAMES_TX)".
  - "Only frame counters moved" -> "Only FRAMES_TX, FRAMES_RX and TIMESTAMP_VALID moved" (both
    places).
  - "the same within the two reads' instants" -> "the same within one commit interval: the DUT's
    FRAMES_RX commits per observation interval of at most 1 s, and its TIMESTAMP_VALID moved
    5,207,830 in the same reads".
- **R3 - Docs - `:1020`.** "equal in header and payload" -> "equal in sequence number, timestamp and
  payload". The grader compares only those two header fields, as `:964-965` already says for
  Direction A.
- **R4 - Docs - `:1162-1167`.** After the round 3 tool table, add: "The `mcasp_selftest_b21.sh`,
  `dir_b21.sh` and `restart_run_b21.sh` hashes are the unmasked originals', `original_sha256` in the
  evidence archive's `MANIFEST.json`; their published copies are label-masked (`path_redacted`), so
  check them against `published_sha256`." Lane B5's section carries the same note for its tools.
- **R5 - Docs - `:753-754` (round 1).** "Raw files stay outside the tree and the packet, each
  identified by size and SHA-256." -> "Raw files were kept outside the tree and the packet, each
  identified by size and SHA-256. They did not survive the bench host's restart before round 2 (see
  round 2); the derived read records remain in the packet." Round 2 (`:835-838`) already records the
  loss; this removes the stale present tense.

## SUGGESTIONS

- **S1 - Robustness, Docs - `:1131-1133`.** State that Direction B's noise exercises only values
  within 0 to -2 LSB. Bit-exactness in that direction is shown for those values only; the full-scale
  listener path is not exercised in this window.
- **S2 - Tests - `b21_mcasp_ana.py`.** Print a mechanical step 1 verdict: overruns 0, dropped bytes 0,
  every read one period, and block-floor change at most a stated bound. A 6-frame loss moves the
  block test by only about 2 frames over its baseline.
- **S3 - Docs - `:785-788`, `:849-852`.** Link the public owner decision where the page states the
  resume terms: #625's body, owner, 2026-09-30, which cites #451 comment 5916029287.
- **S4 - Robustness, Docs - round 3 limits.** Restate the configuration dependence, as lane B5's
  limits do: the DUT on INTERNAL only, and the peer following the DUT's CRF.
- **S5 - Docs - round 3 limits.** Note tcpdump's tail difference between "received by filter" and
  "captured". It holds no in-record gap, so the claim "the taps kept every packet" refers to the
  written records.

## Lenses

- **Conformance - CLEAN.**
  - *Assignment.* Checked against 6208207821 and #625's owner decision: step 1 on the McASP path
    (deficit-only, clean by mechanical counters); Direction A with the peer on the DUT's CRF (peer
    clock source 1 in `census-start2.jsonl`); taps on both links; DUT CSRs; GET_COUNTERS on both
    entities; Direction B graded in the DUT's clock domain at the McASP.
  - *Pass rule.* Windows of 644.8 s at the wire, 638.0 s at the peer's output and 635.0 s at the
    McASP. No missing, repeated, torn or silent frame. The INTERNAL beat did not occur, which is
    consistent with REGISTER_MAP 0x8D4 (static since #629). 20 restarts under 1 s, the worst 86.8 ms
    at the wire.
  - *Scope.* Restore was proven by the census (45 of 46 equal; the other is GET_AVB_INFO's
    propagation delay). `Refs #117` rather than Closes is correct, since the other boxes stay open.
- **RTL - CLEAN.** No RTL, firmware or generated artifact is in the diff (`git diff --stat`: one
  Markdown file). Register interpretations were checked against `docs/reference/REGISTER_MAP.md`:
  - `RENDER_STAT` bits [7:0] fill, [8] prefill, [9] converged and [31:16] rails;
  - `SLIP_LB` saturating at 0xFFFF;
  - `SLIP_TDM` never cleared;
  - AAF meter words zero with no AAF clock source selected.
  R2's FRAMES_RX semantics are RESIDUE.
- **Robustness - CLEAN.**
  - *Stop and restart.* Every cycle stops within 10.8 ms and holds silent. The first 480 frames are
    valid after every rebind. The silences hold zero frames only.
  - *Buffering.* The McASP buffer absorbed 25 board read stalls up to 87.1 ms (16,320-frame buffer;
    ring peak 0.7% of 64 MiB). Equal formats meant no set was due, and the tool's non-comparison is
    disclosed.
  - *Residual state.* The restore's SoC player residual (McASP0 playback closed, against open and
    idle as found) is disclosed.
  - S1 and S4 are optional.
- **Tests - UNCLEAN.** F1, F2 and F3 are open. The graders themselves fail on every planted fault
  (`receipts/probe_graders.txt`).
- **Docs - UNCLEAN.** F1, F2 and F3 are open. The documentation gates pass at the head
  (`receipts/gates_r634.txt`): docs_check, doc style, the TOC check under the pinned renderer,
  em-dash from `4a9b5a2a`, doc paths, ci_scope self-test, baremetal-only, feature-status and
  `git diff --check`, all rc 0. The added lines carry no hostname, path, interface name or vendor
  name. Lane labels appear only in a findings page, which the owner rule permits. There are no
  source comments.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #117 box 4/5; assignment 6208207821; #625 owner decision; page `:843-1175`; `r3/summary/*.json`; `r3/runs/*/counters-*.jsonl`, `dut-poll.txt`, `agent.jsonl`; `r3/restore/census-*.jsonl` | R634-1 | `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b` |
| RTL | CLEAN | `git diff --stat 4a9b5a2a..867fb945` (one Markdown file); REGISTER_MAP 0x8D4, 0x8DC, 0x8E0, FRAMES_RX; `dut-poll.txt` decode | R634-1 | `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b` |
| Robustness | CLEAN | `rA-restart.json`, `cycles.jsonl`, `agent.jsonl`; `dB-analysis.txt`, `dB-reads.u32.gz`; `tools/b21stamp.c`; page restore tables `:1093-1114` | R634-1 | `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b` |
| Tests | UNCLEAN (F1, F2, F3) | `tools/b21_grade.py`, `b21_aaf.py`, `b21_mcasp_ana.py`, `b21_restart.py`; `mst-long-reads.u16`; `st-long2-selftest.txt`; probes in `receipts/probe_graders.txt` | R634-1 | `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b` |
| Docs | UNCLEAN (F1, F2, F3) | `docs/findings/117_AUDIO_CONTINUITY.md:557-1175`; PR #758 body; `MANIFEST.json`; `raw-retention-receipt-r3.txt`; `receipts/gates_r634.txt` | R634-1 | `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b` |

## Real limits of this review

- **No raw files.** No pcap, McASP `.pcm`, external capture or board sample file was available; they
  are in the cold archive. Packet counts, pattern grades, McASP alignment, restart timings and the
  external grades were re-derived from the packet's published tool outputs and records, not
  recomputed from raws. The tools' fault detection was tested on synthetic inputs.
- **No bench access.** Physical calibration was NOT RUN, and printed precision is not accuracy.
- **No source bank.** No manager source bank ran at this head, and none is claimed. The only
  execution at the head is the focused documentation gates above.
- **Hosted checks.** Hosted checks at the exact head were observed only. `rtl-fast` and `docs-check`
  ran and succeeded; Verilator, Yosys and firmware contexts were skipped by scope (docs-only). Their
  acceptance is the manager's.
- **Integrity after review.** The clone was not modified. HEAD and tree are unchanged, the status is
  empty, the index equals HEAD (`receipts/head_integrity.txt`), and the six gitlinks are unchanged.
  A fetch of the evidence commit added objects and FETCH_HEAD only.

## Pending manager duties

- Validate the current-dev merge candidate (source base `4a9b5a2a74fe…`, live dev `1f6f2f57…`)
  with the builder and native banks, and own hosted and act acceptance.
- Carry R1 to R5 to the residue checklist.
- Owner items recorded in the packet's HANDOFF are outside this PR: the SoC player's start script
  does not recreate its CA mount, and an exposed third-party key may need rotating.

R634-1 FINISHED
