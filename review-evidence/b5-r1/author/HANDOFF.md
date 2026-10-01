# [A472] Bench lane B5 handoff

Refs #117, acceptance box 4, the audio continuity row, end to end against the reference peer.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609
Branch: b5-bench-1001 from dev e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b (lane worktree, physical /data path).
Image under test: dev ec0cc0c1 (installed; identity proven by lanes B3 and B4, and again here).
Packet: this directory. Large raw files stay outside it under /tmp/b5-a472/raw and are indexed by size and SHA-256. Private endpoints stay in /tmp/b5-a472/private (not in the packet).

## State

Session 2026-10-01 08:06-08:56 CEST. The lane stops here. Bench work finished 08:44 CEST; everything restored and proven; bench lock free; no task process on this host, the controller or the SoC board.

Commit `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` on b5-bench-1001: one commit on e4b771f9, one-line subject, no body, no trailers; local only, not pushed, no PR; worktree clean. It adds `docs/findings/117_AUDIO_CONTINUITY.md` and its row in `docs/findings/README.md`; no other doc edit. All 11 gate invocations rc 0 at that head (gates/gates.txt).

Verdicts (operator measurements): identity PASS; Direction A integrity PASS (bit-exact, in order); continuity FAIL as measured (one-frame drops every 1.266 s at the peer's output, plus capture-path losses); restarts PASS (30 of 30 under 1 s, median 0.0279 s, max 0.1358 s); Direction B NOT RUN; #117 audio continuity row FAIL as measured.

## Step ledger (UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | TAKEN on #117 | POSTED 06:11:09Z: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925793636 | TAKEN.md, taken-url.txt |
| 1 | Identity gate | PASS 06:11:38-06:12:07Z: VERSION 00020060; AEM CRC 93742dd2 (7,352 B); ROM acad92b9 (53,344 B); QSPI payload d178f19a (3,825,788 B), all equal to lanes B3 and B4; ENTITY 312 B and CONFIGURATION 106 B from AECP byte-equal to the QSPI AEM bytes, entity 020000fffe000001; NVM slot B seq 238 authoritative, backed=1, pend=1, commits ok=2 (lane B4's residual, no DUT reset since); grader 10/10. ADP: DUT, the reference peer, and one other entity advertising controller capability only | identity/ |
| 2 | Baseline: SoC root-shell check and health, DUT reads, census, formats | DONE 06:14-06:21Z: SoC console at a root shell (`id; tty`: uid 0, ttyS3); SoC same boot as lane B4 left it (uptime 75,102 s), legs to-host 1265 / from-host 1266 running with the recorded lines, UDC configured, BAD=0, McASP0 RX 1,252 DMA events in 5.02 s. Census: all 4 DUT and <peer-stream-count> peer stream states unbound; DUT maps empty; DUT clock source 0 at 48 kHz; DUT STREAM_OUTPUT 0 format 0205022002006000 (AAF 48 kHz INT32, 8 ch); peer AAF inputs <peer-stream-indices> at 0205022001006000 (4 ch), each advertising 0215022002006000 (up to 8 ch); peer configuration 1, clock source 0 (INTERNAL), 48 kHz. Peer stream-port dynamic maps: <peer-channel-map>. External capture as found: <capture-channel-layout> at 48 kHz. Controller: no gPTP daemon | restore/, soc/, runs/cap-asfound-lock.txt |
| 3 | Direction A: integrity, continuity (>= 10 min), restarts (>= 20 cycles) | DONE 06:26:15-06:40:04Z (`a-long`): initial bind (format set 4 ch to 8 ch, SUCCESS) restart 0.2676 s; 660 s window 31,569,600 frames: 31,569,594 bit-exact, 0 torn, 0 invalid, 6 single zero frames; 334 repeats (DUT beat), 526 one-frame skips (520 slip events, peer output 16.4 ppm slow), 760 multi-frame skips (117,104 frames, capture path); 30/30 restarts < 1 s. Earlier attempts `abort-agent-start`, `a-try1`, `diag1` and the later `cap-test1` all restored | runs/, summary/ |
| 4 | Direction B | NOT RUN: the peer's talker channels carry its own physical inputs (its STREAM_PORT_OUTPUT 0 map sources them from its input clusters); no known signal drives them without an instrument output or a wiring change | restore/peer-descs-2.jsonl |
| 5 | Restore and proof | DONE 06:43:56-06:44:15Z: legs restarted (to-host 2339, from-host 2340) with the recorded lines; end census 45/46 equal (the other: DUT live propagation delay); peer format as found; DUT maps empty; DUT console words equal but for live counters; NVM line unchanged (no commit); grader 10/10; controller staging removed, no task process; bench host shows both USB audio devices | restore/, soc/ |
| 6 | Findings page, index row, gates, commit | DONE 06:50:24Z: commit bf9e5d82; 11 gate invocations rc 0 at that head | gates/ |
| 7 | REVIEW READY on #117 | POSTED 06:54:19Z: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926301675 | REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 08:11:23-08:11:24 | Controller host: interfaces, tools, processes (read-only) | AVB port identified; no gPTP daemon; no staging |
| 08:11:38-08:12:07 | Identity gate (console CRC, NVM, descriptor dump, grader; AECP ENTITY/CONFIGURATION; ADP) | PASS |
| 08:14:28-08:14:29 | SoC root-shell check `id; tty` | uid 0, ttyS3 |
| 08:14:48-08:14:56 | Start baseline (SoC health, DUT reads, census, peer descriptor survey, controller, host view) | all rc 0 |
| 08:16:05-08:16:06 | Peer descriptor survey with the audio unit's children (read-only) | rc 0; stream port maps read |
| 08:16:40-08:16:44 | External capture, 3 s of all <capture-channel-count> channels as found | <capture-channel-layout> |
| 08:16:53-08:16:53 | DUT stream descriptors (READ_DESCRIPTOR, read-only) | STREAM_INPUT 0 lists 0205022002006000 and 0215022002006000; STREAM_OUTPUT 0 lists 0205022002006000 |
| 08:20:48-08:20:49 | Controller agent dry run (sync, format reads, RX state, counters; read-only) | rc 0 |
| 08:21:17-08:21:23 | SoC bridge legs 1265/1266 stopped by PID (command lines checked against status) | KILLED; all four PCMs closed; UDC configured; BAD=0 |
| 08:21:34 | run_a.py `a-long` launch | argument error in the wrapper before any step; nothing on the bench (runs/a-long-argfail not kept: no step ran) |
| 08:21:46-08:21:53 | run_a.py `abort-agent-start` | period built and verified on the SoC board, then the tool stopped at the agent's first line (a start record, not the ready line); period removed. No map, bind or playback |
| 08:22:08-08:22:54 | run_a.py `a-try1` (capture channels <capture-channel-index>) | format set 4 ch to 8 ch SUCCESS, bind SUCCESS, DUT AAF_FRAMES +239,384 (talker streamed); <capture-channel-index> stayed zero so the online check timed out at 30 s; teardown: unbind, peer format restored and read back equal, map removed and read back empty, playback stopped, period removed |
| 08:23:41-08:24:12 | run_a.py `diag1` (all <capture-channel-count> channels kept, 15 s bound) | pattern on capture channels <capture-channel-index> (tag 1) and <capture-channel-index> (tag 2), 716,886 frames bit-exact; peer STREAM_INPUT 0 counters: media locked 1, timestamp-valid = frames received, no late/early/sequence counts; teardown as above, all restored |
| 08:26:15-08:40:04 | run_a.py `a-long` (one tracked action, 1,850 s deadline; 660 s continuity, 30 cycles) | ACTION_RC 0; 31 binds and 31 unbinds SUCCESS; teardown: unbind, peer format restored and read back equal, map removed and read back empty, playback stopped by PID, period removed |
| 08:41:42-08:42:38 | run_a.py `cap-test1` (40 s, capture period 6,000 / buffer 48,000) | ACTION_RC 0; capture path lost frames at the same rate; restored as above |
| 08:43:56-08:43:59 | SoC bridge legs restarted with the two recorded lines | STARTED: to-host 2339, from-host 2340; PCM states as at the start; UDC configured; BAD=0 |
| 08:44:07-08:44:15 | End snapshot (SoC health, DUT reads, census, controller, host view) and controller staging removal | all rc 0 |
| 08:44:15-08:44:15 | UART grader | 10/10 |

## Restart cycles (one row per cycle)

Run `a-long`. Initial bind: talker 0205022002006000 / listener 0205022001006000, set listener to 0205022002006000 (SUCCESS, read back equal), bind SUCCESS cc 1, restart 0.2676 s.

| Cycle | Formats read (talker / listener) | Set | Rebind response | Stop | Restart, s | Result |
|---|---|---|---|---|---|---|
| 1 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.0 ms after unbind | 0.1358 | PASS |
| 2 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.0 ms after unbind | 0.0282 | PASS |
| 3 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.5 ms after unbind | 0.0269 | PASS |
| 4 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.2 ms after unbind | 0.0273 | PASS |
| 5 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 24.6 ms after unbind | 0.0276 | PASS |
| 6 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.1 ms after unbind | 0.0287 | PASS |
| 7 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.7 ms after unbind | 0.0262 | PASS |
| 8 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.5 ms after unbind | 0.0271 | PASS |
| 9 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.5 ms after unbind | 0.0268 | PASS |
| 10 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.4 ms after unbind | 0.0279 | PASS |
| 11 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.4 ms after unbind | 0.0288 | PASS |
| 12 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.7 ms after unbind | 0.0270 | PASS |
| 13 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.8 ms after unbind | 0.0281 | PASS |
| 14 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.5 ms after unbind | 0.0285 | PASS |
| 15 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.9 ms after unbind | 0.0274 | PASS |
| 16 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.8 ms after unbind | 0.0283 | PASS |
| 17 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.5 ms after unbind | 0.0282 | PASS |
| 18 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.5 ms after unbind | 0.0270 | PASS |
| 19 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.2 ms after unbind | 0.0273 | PASS |
| 20 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.6 ms after unbind | 0.0389 | PASS, stall 19.8 ms |
| 21 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.4 ms after unbind | 0.0279 | PASS |
| 22 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.4 ms after unbind | 0.0275 | PASS |
| 23 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.0 ms after unbind | 0.0280 | PASS |
| 24 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.6 ms after unbind | 0.0284 | PASS |
| 25 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.1 ms after unbind | 0.0285 | PASS |
| 26 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.5 ms after unbind | 0.0283 | PASS |
| 27 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.3 ms after unbind | 0.0271 | PASS |
| 28 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.8 ms after unbind | 0.0282 | PASS |
| 29 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 15.2 ms after unbind | 0.0269 | PASS |
| 30 | 0205022002006000 / 0205022002006000 | none | SUCCESS, cc 1 | stopped in hold; last valid 14.5 ms after unbind | 0.0275 | PASS |

## Deviations and incidents

- The external capture ran as this user (member of the audio group) rather than under `sudo -n`, so the run tool can stop it with SIGINT. Same device, format, rate and channel count.
- The peer's output pair is capture channels <capture-channel-index>, identified by content in `diag1`; the first attempt `a-try1` assumed <capture-channel-index> and timed out (restored).
- Capture path loss: on this host the external capture's USB path loses frames. Each skip of 66 frames or more coincides with a capture read stall whose excess over the 10 ms read cadence equals the lost duration (for example 10.62 ms lost, 10.51 ms excess); they recur about every 2.99 s. No kernel message during the run. Small skips (1 and 6 frames) leave no read-timing trace and are not attributed.

- PR #627 (lane B4's findings) is open, not merged at the lane base; it was read from the PR.

- run_a.py gained the capture-period option (environment, default 480 / 24,000) while `a-long` ran; `a-long` ran the revision without it, at the same values. `diag1` ran with the diagnostic mode and channels <capture-channel-index> in the online check only (it kept all <capture-channel-count> channels); `a-try1` ran before the diagnostic mode.
- census_cmp.py (lane B3's copy) gained `t_tx` and `t_rx` in its volatile set, because b5_ctl.py stamps every exchange; the first end comparison without them is not kept.
- The redaction pass ran three times from the saved originals (the second added the peer's interface identities, the third fixed the ENTITY descriptor mask, whose reserved field is non-zero on the peer); the retained files and hashes are from the last pass.
- The diagnostic and test runs (`a-try1`, `diag1`, `cap-test1`) each set the listener's format and bound, under the binding rule, and each restored it.
- Session time: the long run was one tracked action with an explicit deadline; every other command ran in the foreground with its own deadline, and the session polled until the action ended.

## Posting

- TAKEN, posted 06:11:09Z: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925793636 (TAKEN.md).
- REVIEW READY, posted 06:54:19Z: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926301675 (REVIEW-READY.md is the posted text; REVIEW-READY.readback.md is the API readback, identical but for the trailing newline).

No existing comment was edited or deleted.

## Residuals

- SoC board bridge legs run under new PIDs (2339 to-host, 2340 from-host).
- None else: the DUT's NVM line is unchanged (slots 237/238, commits 2, pend=1 as found, lane B4's residual); the controller's gPTP state was never touched (no daemon ran).

## Packet layout

| Path | What |
|---|---|
| TAKEN.md, taken-url.txt, REVIEW-READY.md, REVIEW-READY.readback.md | Posted texts and the API readback |
| PR-BODY.md | Proposed PR body |
| identity/ | Console CRC, NVM and descriptor readback; grader; AECP-vs-QSPI comparison; ADP discovery; lock window |
| soc/ | SoC board root-shell check, health at start and end, bridge stop and restart transcripts |
| runs/<run>/ | `abort-agent-start`, `a-try1`, `diag1`, `a-long`, `cap-test1`: events, controller transactions (ctl.jsonl), DUT reads, SoC transcripts, console; runs/agent-dryrun.txt, runs/cap-asfound-lock.txt |
| restore/ | Census start/end and comparison, peer descriptor surveys, DUT stream descriptors, DUT reads start/end, controller state and cleanup, host view, grader end, lock windows |
| summary/a-long/, summary/cap-test1/ | summary.json (the grade without the per-event list), continuity-events.csv, tables.md (a-long) |
| tools/ | Every tool used; ORIGIN-B3.sha256 pins the lane B3 originals as copied |
| gates/ | gates.txt and each gate's output at bf9e5d82; status after |
| redaction.json | Per redacted file: original and retained SHA-256, labels used |
| RAW-ARTIFACTS.json | Every raw file under /tmp/b5-a472/raw by relative path, size and SHA-256 |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |

Private endpoints, the redaction map and the redaction originals stay in /tmp/b5-a472/private (not in the packet). The full grades are raw files (a-long/grade-full.json, cap-test1/grade-full.json).
