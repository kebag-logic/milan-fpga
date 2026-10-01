# [A477] Bench lane B6 handoff

Refs #629, bench acceptance: media-clock following graded by THD+N.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5929778646
- Branch: `b6-bench-1001` from dev `ea3fb38877842f223afea97e3bd72a10500455c9`, lane worktree on the physical /data path.
- Image under test: dev `ec0cc0c1`, as installed; identity re-proven here (step 5).
- Packet: this directory. Raw files stay outside it under /tmp/b6-a477/raw and are indexed by size and SHA-256 in RAW-ARTIFACTS.json. Private endpoints, the redaction map and the redaction originals stay in /tmp/b6-a477/private (not in the packet).

## State

**DONE.** Session 2 ran 2026-10-01 13:02-15:01 CEST after the owner's fix (#629 comment 5929969516). Bench work finished at 14:41 CEST. Everything was restored and read back, the bench lock is free, and no task process remains on this host, the controller host or the SoC board.

- Commit `b5e9242e2e1911bb2bac11221527f8965a4ccaef` on `b6-bench-1001`: one commit on `ea3fb388` with a one-line subject, no body and no trailers. It is local, not pushed, with no PR, and the worktree is clean. It adds `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and its row in `docs/findings/README.md`; there is no other doc edit.
- The commit was amended once before any push: `f8b842f0` became `b5e9242e`, adding the attribution history to the page.
- All gate invocations are rc 0 at `b5e9242e` (gates/gates.txt). The bare `check_baremetal_only.py` without a mode is a usage error, rc 2; it ran with `--check` and `--selftest`.
- Verdicts (operator measurements):
  - identity PASS; tool controls PASS;
  - A0 PASS as a control; A1 PASS; A2 FAIL;
  - B INTERNAL PASS as a control; B CRF PASS;
  - Direction B THD+N NOT RUN (no known signal); the DUT's AAF following is not in this image.
- Posted on #629:
  - TAKEN (session 1);
  - STOP (session 1);
  - REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5931956275 (head `f8b842f0`);
  - REVIEW READY (head updated): https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5932007806 (head `b5e9242e`).
- No existing comment was edited or deleted, and nothing else was posted.

## Step ledger (UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only) | #629 and #74, the [A10] comments on #117, the B3/B4 findings pages, PR #628 at its head (`e5ad1187` in session 2), the first-light page, TIME_SYNC, the register map, and the B5, B3, B4, B2, 75 and 117-a373 packets | this file |
| 1 | Session 1 precondition check | **FAIL, STOP** at 10:57Z: the bench host's address on the SoC board link was missing | precheck/host-view.txt |
| 2 | TAKEN on #629 | POSTED 11:01Z (session 1) | TAKEN.md, TAKEN.readback.md, taken-url.txt |
| 3 | STOP on #629 | POSTED 11:01Z (session 1) | STOP.md, STOP.readback.md, stop-url.txt |
| 4 | Session 2 precondition re-check (local) | PASS 11:02:48Z: address present on the static profile, board answers ping, both USB audio cards and the serial adapters present | - |
| 5 | Identity gate | PASS 11:07:21-11:07:50Z: VERSION 00020060; AEM CRC 93742dd2; ROM acad92b9; QSPI payload d178f19a; ENTITY 312 B and CONFIGURATION 106 B byte-equal to the QSPI AEM bytes; NVM slot B seq 238, commits 2, pend=1; grader 10/10; ADP sees the DUT and the reference peer | identity/ |
| 6 | SoC root shell | 11:10:00Z: uid 0 on the console's login bash, read back over the board link (see Deviations) | soc/shell-check-net.log |
| 7 | Start baseline and surveys | 11:11:09-11:11:16Z all rc 0 | restore/*-start*, restore/peer-descs.jsonl, restore/dut-descs.jsonl, soc/start-health.log |
| 8 | Tool and synthetic controls | PASS (offline) | controls/controls.json, tools/b6_tone.py, tools/b6_thdn.py |
| 9 | Cases A0, A1, A2, B INTERNAL, B CRF | 11:32:23-12:28:33Z, each one locked action, each restored and read back | runs/<case>/, summary/<case>/ |
| 10 | Direction B known-signal probe | 12:39:52-12:40:14Z: no known signal; restored | runs/probe/ |
| 11 | Restore and proof | 12:40:24-12:40:41Z: legs restarted, end snapshot, census compare, grader 10/10 | restore/*-end*, restore/census-compare.txt, soc/s02-start-legs.log, restore/grader-end.txt |
| 12 | Findings page, index row, gates, commit | 12:53-13:00Z: `f8b842f0`, gates rc 0; amended to `b5e9242e` (attribution history added), gates rc 0 | gates-f8b842f0/, gates/ |
| 13 | REVIEW READY on #629 | POSTED 12:58:02Z (`f8b842f0`) and 13:01Z (head updated, `b5e9242e`); each readback equals the posted text but for one trailing newline | REVIEW-READY*.md, review-ready*-url.txt |

## Bench actions (one row per locked action, CEST)

Session 1: none. Session 2:

| Time | Action | Result |
|---|---|---|
| 13:06:51 | Controller host: interfaces, processes, staging, sudo (read-only) | AVB port identified; no gPTP daemon; no staging |
| 13:06:57-13:07:01 | Controller: stage the read-only probe; ADP discovery | DUT and the reference peer seen; endpoints recorded privately |
| 13:07:21-13:07:50 | Identity gate | PASS |
| 13:08:08-13:08:23 | SoC root-shell check through the serial reader (`soccon.py`) | no reply (rc 3): the manager's interactive serial terminal on this host (started 12:06:57 CEST) holds the console and consumes the board's output; it was left alone |
| 13:10:00-13:10:01 | SoC root-shell check with the reply over the board link (`soccon_net.py`): `id`, the console shell's tty and command line | uid 0, /dev/ttyS3, login bash; board uptime 92,813 s (no reboot since lane B5) |
| 13:11:09-13:11:16 | Start baseline (SoC health, DUT reads, census, peer and DUT descriptor surveys, controller, host view) | all rc 0; bridge legs 2339/2340 with the recorded lines; all binds unbound; both clock domains on source 0 |
| 13:13:58 | SoC capability probe (read-only): shell, clock variable, ALSA tools, PCM parameters | bash 5.2 with a microsecond clock; aplay 1.2.16 without a timestamp option; fractional sleep; no `timeout` applet |
| 13:21:36-13:21:42 | SoC bridge legs 2339/2340 stopped by PID (command lines checked against status) | KILLED; all four PCMs closed; UDC configured; BAD=0; both USB audio cards still on this host |
| 13:21:55 | run_b6.py `smoke-a0` (first launch) | import error in the tool before any step (runs/smoke-a0-importfail-lock.txt); nothing on the bench |
| 13:22:04-13:22:09 | run_b6.py `smoke-a0-clkparse` | tone and sampler fetched to the SoC board and checked; the tool's clock-source parse returned none, so it refused at the as-found check before any map, bind or playback; the teardown's format read-back then crashed the controller agent (a field-order slip); nothing was set; board files removed |
| 13:22:22-13:23:26 | run_b6.py `smoke-a0` (A0, 30 s window) | ACTION_RC 0. Format set 4 ch to 8 ch SUCCESS and read back, bind SUCCESS; tone valid 0.15 s after the bind; teardown: unbind, peer format restored and read back equal, map removed and read back empty, every clock source and format read back as found. The board sampler lost the hw_ptr line in 107 of 249 samples (line-by-line reads of the status file); fixed |
| 13:28:22-13:30:30 | run_b6.py `smoke2-a0` (A0, 90 s window) | ACTION_RC 0, restored as above; 535 of 535 samples parsed. Tool check only, not a graded case |
| 13:32:23-13:43:33 | run_b6.py `a0` (A0, 630 s window) | ACTION_RC 0. Peer clock source 0 (as found), DUT 0; format set 4 ch to 8 ch SUCCESS and read back; bind SUCCESS; teardown: unbind, peer format restored and read back, map read back empty, clock sources read back 0 and 0 |
| 13:43:52-13:54:50 | run_b6.py `a1` (A1, 630 s window) | ACTION_RC 0. Peer SET_CLOCK_SOURCE to the source located on its AAF input SUCCESS, read back equal; teardown: peer clock source set back to 0 and read back 0, unbind, peer format restored and read back, map read back empty |
| 13:54:59 | SoC: `od` and `awk` statistics test on 9,600 random bytes in /tmp (removed) | the board's awk has no `sqrt`; the probe reports the mean square instead |
| 13:55:08-14:06:09 | run_b6.py `a2` (A2, 630 s window) | ACTION_RC 0. CRF bind DUT STREAM_OUTPUT 1 to the peer's CRF input SUCCESS (formats equal, no set); peer SET_CLOCK_SOURCE to the source located on that input SUCCESS, read back equal; teardown: peer clock source set back to 0 and read back 0, both unbinds SUCCESS, peer format restored and read back, map read back empty |
| 14:06:13-14:17:19 | run_b6.py `bint` (B INTERNAL, 630 s window) | ACTION_RC 0. AAF bind DUT to peer, CRF bind peer to DUT STREAM_INPUT 1 SUCCESS (formats equal); DUT clock source left at 0; teardown: both unbinds SUCCESS, peer format restored and read back, map read back empty, clock sources read back 0 and 0 |
| 14:17:24-14:28:33 | run_b6.py `bcrf` (B CRF, 630 s window) | ACTION_RC 0. Binds as `bint`; DUT SET_CLOCK_SOURCE 1 SUCCESS, read back 1; servo LOCKED 6.5 s later and through the window (MCSRV_STAT 0xffa00034 to 0xffa10034: state 4, MMCM locked, trim -6.0 ppm, DRP config mismatch bit 4 set); teardown: DUT clock source set back to 0 and read back 0, both unbinds SUCCESS, peer format restored and read back, map read back empty |
| 14:39:52-14:40:14 | probe_b6.py `probe` (Direction B known-signal probe) | ACTION_RC 0. Binding rule: talker (peer AAF output) 0205022001006000, listener (DUT STREAM_INPUT 0) 0205022002006000, set the DUT's to 0205022001006000 SUCCESS, read back; four identity mappings on DUT STREAM_PORT_INPUT 0; bind SUCCESS; 2 s McASP0 capture reduced on the board: channels 0-3 only values -2 to 0 (24-bit LSB), mean square 0.49-0.54, channels 4-7 all zero; teardown: unbind, mappings removed and read back empty (as found), DUT format restored to 0205022002006000 and read back, recording removed |
| 14:40:24-14:40:28 | SoC bridge legs restarted with the two recorded lines | STARTED: to-host 22949, from-host 22950; PCM states as at the start; UDC configured; BAD=0 |
| 14:40:34-14:40:41 | End snapshot (SoC health, DUT reads, census, controller, host view) and controller staging removal | all rc 0; staging removed, no task process |
| 14:40:41 | UART grader | 10/10 |

## Run ledger (one row per case; final grading)

| Case | Window start | Window | Result |
|---|---|---|---|
| Tool controls (synthetic) | 13:17 CEST | offline | PASS: clean at the floor (-146.06 / -145.99 dB), drop and repeat found at the planted frame, 16.000000 and 1.000000 ppm fitted, slips at the planted spacing |
| A0 as found | 13:32:50 CEST | 629.56 s | PASS as a control: 519 one-frame listener drops (17.14 ppm) and 1 silent insert, 321 DUT beat repeats on the comb, capture path 25 events in 10 clusters (26,173 frames); 54 blocks at the floor; counted McASP0/peer ratio +6.519 ppm, timed +6.44 +-0.72 ppm |
| A1 AAF following | 13:44:12 CEST | 617.32 s captured in 630 s | PASS: 0 listener discontinuities; 315 DUT beat repeats; capture path 51 events in 23 clusters, 615,026 frames lost (one 12.7 s read stall); 291 of 617 blocks at the floor; counted ratio -10.631 ppm (the peer follows the stream, so this is the DUT's own beat); timed -12.19 +-2.44 ppm |
| A2 CRF following | 13:55:31 CEST | 616.14 s captured in 630 s | FAIL: 494 one-frame listener drops and 180 silent inserts on one phase, 316 DUT beat repeats on another, about half a beat apart (net within two frames); capture path 143 events in 61 clusters, 686,656 frames lost (one 13.3 s stall); 1 of 616 blocks at the floor; counted ratio -0.068 ppm, timed -0.59 +-1.24 ppm. The peer follows the DUT's CRF, which runs on the DUT's physical audio clock (`KL_crf_tx` divides `clk_audio_i` by 512); at INTERNAL the DUT's AAF stream runs on the free-running 48 kHz packet grid, 10.64 ppm off it |
| B INTERNAL control | 14:06:41 CEST | 629.98 s | PASS as a control: counted ratio +6.052 ppm, timed +6.85 +-1.46 ppm; 506 listener drops, 1 silent insert, 322 beats; CRF sink locked (CRF_CTRL[31]), servo IDLE (MCSRV_STAT 0x20) |
| B CRF following | 14:17:55 CEST | 629.95 s | PASS: servo LOCKED 6.5 s after the set and through the window; counted ratio 0 (0 net steps in 30,237,600 frames; 1 frame = 0.033 ppm); timed -0.01 +-0.65 ppm; 0 listener discontinuities and 0 DUT beat repeats (SLIP_TDM static); 611 of 629 blocks at the floor, the other 18 hold capture-path losses only |
| B known-signal probe | 14:40 CEST | 2 s | No known signal: the peer's talker channels carry -2 to 0 LSB; Direction B THD+N NOT RUN, graded by the frame-rate ratio |
| Restore | 14:40 CEST | - | DONE: every clock source, format and map read back as found after each run; legs restarted; end census 43 of 46 equal to the start; DUT NVM commits 2 to 8 (slots 243/244, pend=1); grader 10/10 |

## Grading criteria (fixed 13:38 CEST, before any following case ran)

- Window: at least 10 minutes (630 s), from 20 s after the last bind or clock-source set (BCRF: after the DUT servo reads LOCKED), untouched.
- Tool controls: PASS when every planted defect is found with its exact size and position and the clean capture sits at the floor.
- A0 (control): PASS when the metric shows the mismatch: listener discontinuities at a rate of the order B5 measured (about 16 ppm), with clean blocks at the floor.
- A1, A2: PASS when the window holds 0 listener discontinuities, every block free of discontinuities sits at the 24-bit floor (within 0.01 dB), the fitted offset on those blocks is below 0.001 ppm in magnitude, and the clock source read back as set.
- B INTERNAL (control): PASS when the McASP0 to peer frame-rate ratio shows the DUT off the peer's clock (counted ratio beyond 2 ppm in magnitude).
- B CRF: PASS when the DUT servo reads LOCKED, the counted ratio is within 0.5 ppm of zero, the timed ratio's interval holds zero, and the tone path holds 0 listener discontinuities.
- Attribution as first written: capture path = a skip of two frames or more at a capture read gap of at least 11 ms within three reads; DUT beat = a one-frame repeat within 600 frames of a whole number of 93,990-frame beats from another; listener = everything else.

### Refinements made while grading (each applied to every case; stated on the page)

| Time (CEST) | Refinement | Trigger | Effect |
|---|---|---|---|
| 13:52 | Timed-ratio interval: bootstrap half-width in quadrature with half the halves' difference | A0: the capture's deficit floor is a 1 ms sawtooth | interval widened; no verdict depends on it |
| 13:52 | Capture path: clusters within 300 ms, tested by the read-time rise (1 ms + 2 %), read-gap fallback in the 600 ms before | A0: a 9,996-frame skip whose stall came 370 ms earlier | A0 listener 521 to 519 |
| 13:58 | Counted ratio over captured frames (events inside lost audio cannot be seen) | A1: a 12.4 s loss hides 6 beats | A1 counted -10.41 to -10.63 ppm |
| 14:00 | Whole loops added to match the rise; a cluster's net step (stale replays) | A1: the 12.4 s loss showed as 18,626 frames; a 6-frame replay one capture buffer back | A1 listener 4 to 0 |
| 14:10 | Read gap plus 48 n + 12 size where a rise is spoiled | A2: rises spoiled next to the 13.3 s stall | A2 two multi-frame events to capture path |
| 14:30 | DUT beat as one comb in source frames (densest phase, line fit, 50 frames) with the SLIP_TDM cross-check | A2: the listener slips at the beat's rate on its own phase | A2 180 events from beat to listener; A0 and B INTERNAL one each |
| 14:35 | Source frames placed per event inside clusters | A1, B INTERNAL: beats between a cluster's skips misplaced by its loss | two beats back on the comb |
| 14:45 | Silent inserts labelled | A2: the 180 extra frames are silent, not repeated | labels only |

Under the rule as first written, A1 has 4 and B CRF 3 multi-frame events outside the capture path, and both would fail. Every one lies in a capture-path cluster whose read-time rise matches its loss, or follows a 33 ms read stall. A0, A2 and B INTERNAL keep their verdicts under either rule.

## Deviations and incidents

- **SoC console reader.** The manager's interactive serial terminal on this host (microcom, started 12:06:57 CEST on pts/2) held the SoC board's console open and consumed what the board printed, so lane B5's `soccon.py` saw nothing (rc 3; it had typed only `printf` lines). It was not touched. `soccon_net.py` types one `wget ... | bash` line on the console. The script, served from this host for that one request, returns its output over the board's USB network link (bash `/dev/tcp`). The root shell was confirmed with `id` before any other board action. Every board action in this session used it. The board's echo of each typed line appeared in that terminal.
- **Long actions.** Each case ran as one tracked action with an explicit deadline (1,100 s; B CRF 1,300 s) under the lock. Every other command ran in the foreground with its own deadline, and the session polled until each action ended.
- **Capture path.** The external capture lost audio at read stalls up to 13.3 s on this host, which carried other workloads (its kernel log shows soft lockups at 12:59 CEST from compile jobs). The read-time record separates every loss from clock effects.
- **External capture as this user**, not under `sudo -n`, as in lane B5, so the run tool can stop it with SIGINT.
- **Descriptor survey.** The audio-unit walk of the inherited `descs` mode uses wrong type codes for clusters and maps (PR #628 records it). This lane used the survey only for stream, clock-source, clock-domain, AVB-interface and control descriptors, whose codes are right; `b6_descs.py` labels the codes per IEEE 1722.1 Table 7.1.
- **Commit amended once** before any push (`f8b842f0` to `b5e9242e`) to add the attribution history to the page; a second REVIEW READY states the new head.
- **Redaction.** One pass from a private map over every packet file but the tools, MANIFEST and redaction.json; originals in /tmp/b6-a477/private/orig; precheck/host-view.txt (already masked in session 1) went through it again. A token scan over the whole packet, tools included, finds no private identifier.

## Residuals

- SoC board bridge legs under new PIDs (22949 to-host, 22950 from-host).
- DUT NVM commits 2 to 8 (slots 243/244, pend=1) from the method's format, map and clock-source edits; lane B3 recorded the same class.
- Two of the reference peer's talker states keep a stream ID, destination MAC and VLAN with connection count 0.
- DUT counters that clear only on reset moved: SLIP_TDM, RENDER_STAT, CRF_RATE and CRF_STATUS (hold their last values).

## Open items for the owner

- **A2 FAIL.** At INTERNAL the DUT's AAF stream and its CRF talker run on different clocks (packet grid against the physical audio clock, 10.64 ppm), so a listener following the DUT's CRF drops one AAF frame per beat. Owner decision or a new Issue; not filed here (this lane posts only TAKEN, REVIEW READY and STOP).
- The B CRF servo status carries bit 4, DRP config mismatch, from ACQUIRE on; recorded, not analysed.
- The DUT's AAF following (#629 work) is not in this image; that part of the bench acceptance stays open.
- The manager's serial terminal still holds the SoC board console.

## Session 1 (kept as written then, condensed)

Session 1 (12:47-13:01 CEST) stopped at the precondition: the bench host's hand-set address on the SoC board link was missing because an auto-created DHCP profile re-activated every 45 s. The owner bound the static profile to the gadget by MAC and stopped the DHCP profile's autoconnect. The session-1 resume plan was followed. It differed in two places: the console reply came over the board link, and the probe reduced levels on the board instead of pulling a capture.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.md, TAKEN.readback.md, taken-url.txt; STOP.md, STOP.readback.md, stop-url.txt | Session 1 posts and readbacks |
| REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt; REVIEW-READY-2.md, REVIEW-READY-2.readback.md, review-ready-2-url.txt | Session 2 posts and readbacks |
| PR-BODY.md | Proposed PR body |
| precheck/ | Session 1 host view (masked) |
| identity/ | Console CRC, NVM and descriptor readback; grader; AECP-vs-QSPI comparison; ADP discovery; lock window |
| soc/ | SoC root-shell checks, capability probe, od test, health at start and end, bridge stop and restart transcripts |
| runs/<run>/ | `smoke-a0-clkparse`, `smoke-a0`, `smoke2-a0`, `a0`, `a1`, `a2`, `bint`, `bcrf`, `probe`: events, controller transactions (ctl.jsonl), DUT reads, SoC transcripts; runs/*-lock.txt the lock windows |
| summary/<case>/ | grade.json (the full grade without the per-event and per-block lists), events.csv, blocks.csv; summary/tables.md as rendered |
| controls/controls.json | The tool's synthetic controls |
| restore/ | Census start/end and comparison, peer and DUT descriptor surveys, DUT reads start/end, controller state and cleanup, host view, grader end, lock windows |
| tools/ | Every tool used; ORIGIN-B5.sha256 pins the lane B5 copies as taken |
| gates/, gates-f8b842f0/ | Gate commands and outputs at `b5e9242e` and at the superseded `f8b842f0` |
| redaction.json | Per redacted file: original and retained SHA-256, labels used |
| RAW-ARTIFACTS.json | Every raw file under /tmp/b6-a477/raw by relative path, size and SHA-256 |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
