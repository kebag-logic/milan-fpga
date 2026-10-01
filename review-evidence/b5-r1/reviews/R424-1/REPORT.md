[R424] NEGATIVE - exact head bf9e5d82a401d167a8ffc786677a19dc7aac0cf2

Round R424-1, internal independent review of PR #628 (Refs #117, acceptance box 4, the audio continuity row; bench lane B5, evidence only).
Head `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`, tree `ffe4fa9192c2926c749dcf22abf413dedb9bd412`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b` (one commit; `docs/findings/117_AUDIO_CONTINUITY.md` new, one row in `docs/findings/README.md`).
Evidence examined: the published packet at `ef3a709151f9bdbd4718c0783d0b8991ede7fd36:review-evidence/b5-r1` (142 files, every published SHA-256 verified, none unlisted).

Two MINOR findings are open, so Conformance, Tests and Docs are UNCLEAN. RTL and Robustness are CLEAN. The page's core measurements hold up when re-derived from the packet:

- the identity gate;
- the binding rule, applied before every bind;
- integrity;
- the DUT's INTERNAL beat;
- the one-frame-slip period;
- the restart distribution;
- the restore.

What is open: the page's attribution of the 2- to 59-frame skips to the capture path is stated more strongly than the published evidence supports. Also, the controller tool revision that ran the binds is not established.

## Re-derivation against the seven review questions

1. **Identity gate: confirmed.** The packet's readbacks give:
   - VERSION `0x00020060`;
   - AEM CRC32 `93742dd2` over 7,352 bytes;
   - ROM `acad92b9` over 53,344 bytes;
   - QSPI payload `d178f19a` over 3,825,788 bytes;
   - ENTITY (312 bytes) and CONFIGURATION (106 bytes) byte-equal to the QSPI AEM bytes, entity `020000fffe000001`;
   - the UART grader 10 of 10 at the start and the end.

   The VERSION, AEM, ROM and QSPI values equal the merged #617 page's readback on the same `ec0cc0c1` image (`docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:44-52`). The NVM line is slot B seq 238 authoritative, `backed=1`, `pend=1`, commits 2, and it is identical at the start and the end. (Packet: `author/identity/*`, `author/restore/dut-start.txt`, `author/restore/dut-end.txt`.)
2. **Format check before every bind: confirmed.** `receipts/binding_rule_audit.txt` walks every run's controller log, 34 binds in all.
   - Each bind follows a fresh talker read and listener read.
   - On each run's first bind the listener read `0205022001006000` and was set to the talker's `0205022002006000`, SUCCESS, then read back equal. The 30 cycle rebinds found the formats equal.
   - The talker was set 0 times. Every SET_STREAM_FORMAT targets the listener.
   - After every run's last unbind the listener was set back to `0205022001006000` and read back equal.
   - Every bind returned status 0 with connection count 1. Two of the 31 `a-long` binds answered with a zero stream ID in the listener's response; both had status 0 and connection count 1. This is immaterial.
3. **Integrity: confirmed for the window.**
   - The window holds 31,569,600 frames: 31,569,594 valid, 0 torn, 0 invalid non-zero and 6 zero frames, with 0 backward steps.
   - The graded transitions add up: 31,567,967 in order, 334 repeats and 1,286 skips, which leaves 12 ungraded. Those 12 are exactly the transitions next to the six zero frames.
   - The pattern rule is checked bit by bit at the captured 24 bits. A planted-defect probe of the published classifier (`receipts/probe_grader_steps.txt`) detects repeat, one-frame and six-frame skip, backward, wrap, torn and wrong-tag cases.
   - The page's whole-run statement, 39,356,186 frames of which 3,407,496 are zero, is not computed by any published tool. It is not needed for the window verdict.
4. **Continuity FAIL and its three attributions.**
   - **Repeats, the DUT's INTERNAL beat: supported, strongly.** Counted in content frames, the repeats are 93,989 to 93,993 frames apart. The page says 93,989 to 93,992; the extra frame of 93,993 is the two spacings that straddle a zero frame, whose neighbouring ordinals the packet does not carry. Four spacings are doubled, so 338 beats fall in 660.15 s.
     - Divider plan A gives -10.6393 ppm, which is a 93,991.4-frame (1.9582 s) beat (`docs/litex/CLOCK_DOMAINS.md:119`).
     - This matches the earlier pages: first light gives 93,989 to 93,992 (`docs/findings/451_TDM8_FIRST_LIGHT.md:310`) and #617 gives 93,990 to 93,993 (`docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:145`).
     - `SLIP_TDM` duplicates rose 327 in 640.474 s, which is 0.5106 per second, with skips at 0 throughout. The lane as a whole went from 38,142 to 39,040 at the same rate.
     - The counter is `tdm_dup_cnt_o` (`hdl/ieee1722/aaf/KL_chan_map_capture.sv:1037-1038`). Both the TDM frame clock and the media grid are derived inside the DUT, so the beat is internal to it.
   - **One-frame drops at the peer's output: supported, and stated with the right limit.**
     - The 526 one-frame skips form 520 events: 514 single events and 6 events of the form skip, zero frame, skip, with the zero at +6 and the second skip at +12.
     - The spacing is 60,546 to 60,923 content frames, median 60,768, which is 1.266 s and 16.4 ppm. One spacing is doubled.
     - The peer listener's counters show no sequence mismatch, late timestamp or early timestamp across `a-long`, and AAF_FRAMES runs at 7,999.997 per second. So the stream reached the listener intact.
     - The page's Limits section says the mechanism, the peer's INTERNAL media clock, is untested. That is the honest strength.
   - **Capture-path losses: overstated for the 2- to 59-frame class.** See F1.

   **Verdict "FAIL as measured": the honest reading.** No clean 10-minute window exists. The FAIL does not depend on any of the attributions.
5. **Restarts: confirmed** (`receipts/rederive_restarts.txt`).
   - 30 of 30 cycles stopped in their hold, with 0 valid frames in any hold. All 30 restarted under 1 s.
   - The distribution is min 0.0262 s, median 0.0279 s, p95 0.0389 s, max 0.1358 s. The initial bind took 0.2676 s.
   - Before the first valid run there were zero frames only.
   - The least-squares slope is -0.000664 s per cycle, 95% interval [-0.001495, +0.000166]. Without cycle 1, which follows the 660 s window, it is +0.000033 s per cycle, interval [-0.000067, +0.000134]. So there is no growth.
   - All 30 cycle rows on the page equal the packet values.
6. **Direction B NOT RUN: the reason is consistent with the packet.**
   - The peer's STREAM_PORT_OUTPUT 0 maps its stream channels 0 to 3 from that port's own clusters, base 16.
   - The DUT's STREAM_INPUT 0 lists `0205022002006000` and `0215022002006000`.
   - Whether clusters 16 to 19 are physical inputs cannot be re-derived, because their descriptor names are redacted in the packet. It is accepted as an operator statement.
7. **Restore: confirmed.**
   - The census is equal in 45 of 46 entries. The one difference is the DUT's GET_AVB_INFO propagation delay, `0x17f` against `0x17d`.
   - All 18 stream states are unbound.
   - Both DUT maps read back empty after every run.
   - The NVM line is unchanged, so there was no commit.
   - The bridge legs run with the same command lines under new process IDs.
   - The controller staging is removed.

**Public text.** The page names no host, peer, switch or instrument. It gives no capture channel numbers. It states no clock distribution or physical wiring beyond the SoC board's McASP0 feeding the DUT's TDM input, which the assignment and the merged first-light and #617 pages already state. It does state the DUT's and the peer's AEM clock-source selections, both INTERNAL. That is device state the attribution needs, and the merged `docs/findings/451_USB_AUDIO_CAPTURE.md:43` states the DUT's the same way. I judge this acceptable. The docs gates pass at the head (`receipts/docs_gates.txt`).

## Findings

**F1 - MINOR - Conformance, Tests, Docs - `docs/findings/117_AUDIO_CONTINUITY.md:196-212`, and the same claim at `:19`, `:186-187`, `:226-228` and `:329` - the capture-path attribution of the 2- to 59-frame skips is stated as fact, but the published evidence does not establish it**

- *Authority/evidence:*
  - The page says: "Skips of two frames or more: the capture path. These are frames the bench host's USB path never delivered." It also counts all 117,104 frames as capture-path loss (`:19`, `:329`).
  - For the 521 skips of 2 to 59 frames (7,176 frames, 354 of them six-frame skips), the only support offered is the frame-count drift: "fell behind the bench host's clock by 115,614 frames ... covers most of the 7,176".
  - **That figure is not computed by any published tool.** It also disagrees with the page's own window: 660.151102 s at 48 kHz less 31,569,600 captured frames is a deficit of 117,652.9 frames, not 115,614.
  - With 115,614, and the page's own 17.3 ppm peer offset (548 frames), 2,038 skipped frames are left unexplained. That is about the 2,124 frames in the 354 six-frame skips.
  - With 117,652.9, every skip of 2 or more is explained. But that holds only because the page's "17.3 ppm" for the peer's output is itself obtained by assuming every skip of 2 or more is a capture loss: the remainder is 548.9 frames, which is 17.32 ppm. The page presents it as a measurement.
  - The operator's own record in the packet (`author/HANDOFF.md`, "Deviations and incidents") states: "Small skips (1 and 6 frames) leave no read-timing trace and are not attributed."
  - The page itself notes that a six-frame loss and an AAF packet cannot be separated by frame counts (`:210-211`).
  - Only 232 of the 521 small skips fall within 10 ms of a 60-or-more-frame skip (`receipts/small_skip_context.txt`).
  - "236 of the 239 ... line up with a capture stall" uses a stall criterion different from the packet grader's. The grader counts 220 stalls of more than 15 ms in the window. The criterion's input, the read-time file, is not published.
- *Impact:* The page directs the follow-up to "a capture path that loses no frames". It does so on an attribution the evidence does not separate from a whole-packet (six-frame) loss downstream of the peer listener's counters. A re-run with a lossless capture could fail again for a cause this page dismissed. Or a real packet-level drop could be filed as a bench artifact.
- *Required outcome:* The page states the 2- to 59-frame class at the strength the evidence supports. For example: the part that coincides with stalls is attributed, the rest is not separable from packet-sized loss, and the operator record's non-attribution is reflected. It also reconciles or removes 115,614 against the 660.15 s and 657.7 s figures. And it labels the 0.8 ppm and 17.3 ppm rates as derived under the capture-loss assumption. Alternatively, it publishes the derivation (tool and per-read inputs) that supports the categorical claim.
- *Verification:* A reviewer recomputes every figure the page uses for this class from published inputs, and finds no class stated as caused by the capture path beyond what those figures show.

**F2 - MINOR - Docs, Conformance - `docs/findings/117_AUDIO_CONTINUITY.md:360-371` (tool table) - the revision of the controller tool that executed the binds and format sets is not established**

- *Authority/evidence:*
  - #117 acceptance box 5 requires tool revisions in the findings.
  - The page pins `b5_ctl.py` at `47b7387a...` and discloses a revision difference for `run_a.py` only (`:370-371`).
  - The packet's only controller-side hash recorded before the runs is `author/restore/controller-start.txt`, taken at the baseline staging. It shows `b5_ctl.py` `24208ef2...` (8,642 bytes).
  - `47b7387a...` (9,842 bytes) first appears at the end staging, in `author/restore/controller-end.txt`.
  - The run tool executes whatever is staged and records no hash (`author/tools/run_a.py:189`). No staging between the two snapshots is recorded.
  - The executed AECP and ACMP exchanges are logged, so the binding-rule audit itself stands. The identity of the tool that produced them does not.
- *Impact:* Box 5's tool-revision claim for the binding-rule and bind tool is unsupported, and a reader would take the listed revision as the executed one.
- *Required outcome:* The page states which `b5_ctl.py` revision ran each run, with the evidence. If the revision is unrecorded, it says so, as it already does for `run_a.py`. Any executed revision that differs from the listed one is identified by hash.
- *Verification:* The tool table and its notes match a controller-side hash, or an explicit unrecorded statement, for every run.

**S1 - SUGGESTION - Docs - `docs/findings/117_GPTP_SILICON_EVIDENCE.md:59`, `docs/findings/README.md:14` - forward pointers**

The #117 ledger's audio continuity row still reads "NOT RUN: deferred to 2026-12-31". The #75 index row still reads "AAF unmeasured". This page measures both. The repository's practice, as with the 451 row pointing to the #617 re-run, is a forward pointer. The assignment fixed the output as one page and its index row, so whether to add the pointers is the manager's call.

**S2 - SUGGESTION - Conformance, Docs - `docs/findings/117_AUDIO_CONTINUITY.md:26-30` - the reading that exempts the INTERNAL beat**

The page cites TIME_SYNC.md, which documents the beat but does not accept it. The acceptance authority is the standing free-run rule:

- `docs/reference/REGISTER_MAP.md:1849-1850`, "slips accepted";
- `docs/CHANNEL_MAP_64.md:229`, "the accepted free-run, not a defect".

Cite these, or record the owner's confirmation that the row tolerates the beat. As written, a future run with only beat repeats would PASS on a reading this page chose.

**S3 - SUGGESTION - Tests, Robustness - `author/tools/grade_a.py:142-145`, `author/tools/b5_tables.py:23-26`; page `:18`, `:163-164`, `:215-216` - how the evidence is graded and presented**

- State the order criterion as 0 backward steps.
- Note that the grader leaves the 12 transitions next to the six zero frames ungraded. The planted probe shows that a zero frame replacing a content frame is not graded as a skip. So "each of which removes one frame", for the six skip, zero, skip events, rests on ordinals not in the packet.
- `b5_tables.py` promises a content-time column that the CSV lacks (its `pos` variable is unused). No published tool computes the page's content-frame spacings; they were re-derived here within one frame.

**Prior public findings on this PR.** None. The PR carries only two review-start notices and no reviews or review comments.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2 open) | Issue #117 body, box 4 and box 5; owner decisions (comments 5789767491, 5795898094) and assignment 5925737609; page `:15-30`, `:144-232`, `:299-309`, `:342-371`; packet `author/summary/a-long/*`, `author/runs/*/ctl.jsonl`, `author/HANDOFF.md`; `receipts/rederive_continuity.txt`, `binding_rule_audit.txt`, `stream_counters.txt`, `small_skip_context.txt` | R424-1 | `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` |
| RTL | CLEAN | No RTL in the diff (`git diff --stat e4b771f9..bf9e5d82`: two Markdown files). The page's RTL-behaviour claims were checked against `hdl/ieee1722/aaf/KL_chan_map_capture.sv:452-453,1032-1038` (dup and skip counters), `docs/reference/REGISTER_MAP.md:1862` (`SLIP_TDM` layout), `docs/design/TIME_SYNC.md:463-479` (frame-atomic handoff, beat), `docs/litex/CLOCK_DOMAINS.md:119` (-10.6393 ppm, recomputed), and DUT console reads `author/runs/a-long/dut-cont-*.txt` (`receipts/provenance_checks.txt`) | R424-1 | `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` |
| Robustness | CLEAN | The packet's failure and edge paths: `a-try1` (timed out and restored), `abort-agent-start` (stopped before any map or bind), cycle 20's stall (disclosed), cycle 1 after the window, zero-frame events, and the doubled beat and slip spacings; teardown and restore in every run (`author/runs/*/ctl.jsonl` map and format readbacks); `author/restore/census-*.jsonl` and `census-compare.txt`; `author/restore/dut-*.txt`; `author/soc/*-health.log` | R424-1 | `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` |
| Tests | UNCLEAN (F1 open) | `author/tools/grade_a.py` (planted-defect probe, `receipts/probe_grader_steps.txt`); `author/tools/b5_tables.py`; restart and growth re-fit (`receipts/rederive_restarts.txt`, 30 of 30 page rows equal); continuity class counts and spacings re-derived (`receipts/rederive_continuity.txt`) | R424-1 | `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` |
| Docs | UNCLEAN (F1, F2 open) | `docs/findings/117_AUDIO_CONTINUITY.md` (all 371 lines), `docs/findings/README.md:20`; docs gates at the head, all rc 0 (`receipts/docs_gates.txt`); anchors; bench-identity token scan; tool hashes on the page against the packet (`receipts/provenance_checks.txt`); packet manifest (`receipts/packet_manifest_check.txt`) | R424-1 | `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` |

## Real limits

- The raw capture, the read-time file and the full grades are not public, so they were not re-graded. Integrity and continuity are re-derived from the packet's summary and event list, not from the bytes. The page's whole-run zero-frame census and stall alignment could not be reproduced.
- The capture channel identity and the peer's cluster names are redacted in the packet. Direction B's physical-input statement is accepted as an operator statement.
- There was no hardware access. Physical calibration was NOT RUN, and every rate is relative to an uncalibrated host clock.
- The pinned Markdown lock was installed in a disposable environment outside the clone for the docs gates. No other bank was run.
- A top-level name listing of the manager's private working area was taken inadvertently. No file there was opened, and nothing from it was used.
- The clone is restored and verified (`receipts/clone_integrity.txt`). HEAD, the index tree and the worktree are equal to the head, nothing is untracked or ignored, and all four gitlinks match HEAD. The bytecode caches the gate runs created were removed.

## Pending manager duties

- The hosted `docs-check` was pending when read; RTL contexts are skipped for this docs-only scope and `rtl-fast` passed (`receipts/hosted_checks.txt`). Hosted and act acceptance stays with the manager.
- The full source static, builder and native banks, and the final candidate built on current dev at the merge turn.
- Disposition of F1 and F2, a re-review at the corrected head, and the external review's verdict.
- The decision on S1's forward pointers, which sit outside the frozen output.

R424-1 FINISHED
