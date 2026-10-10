# [A588] Bench lane B15 handoff

Refs #629: locate where Direction B's known tone is lost (the reference peer's talker, the DUT's link, the DUT's TDM output, the external capture), then repair it if the DUT loses it; dev `5603c353` bench image as flashed and booted.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6097827871
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6097896607 (posted 15:16 CEST; TAKEN.readback.md equal but for one trailing newline)
- STOP: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6098146914 (posted with the head and the per-run tables; STOP.md, STOP.readback.md equal but for one trailing newline, stop-url.txt)
- Posted on #629: TAKEN and STOP only; no existing comment was edited or deleted.
- Branch: `629-b15-tone` from dev `e8454e275`, lane worktree on the physical /data path.
- Packet: this directory. Raw files (pcaps, recordings) stay outside it on the bench host (RAW-ARTIFACTS.json); private endpoints, the redaction map, the unmasked originals, the tone's loop and playback log, the tone source's state reads and the external capture's all-channel rows stay in a private directory (not in the packet).

## State

**STOP** (2026-10-10; bench work 15:13 to 15:36 CEST, STOP posted after the packet), under the assignment's branch "Tone absent at (a)". The known tone is already absent in the reference peer's own talker stream on the peer's link, (a); identical on the DUT's link, (b); and at the DUT's TDM output, (c), whose four mapped channels equal the received stream sample for sample (480,000 of 480,000 frames in both runs). A positive control on the same taps and the external capture, (d), finds a tone sample-exact. So the loss is upstream of the peer's talker: instrument-side, for the owner. The playback and routing state was read read-only; no instrument setting was changed. No DUT stage was localised, no RTL or firmware changed, and B0, B-CRF and B-AAF were not run.

- **Commit:** `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` on `629-b15-tone`, one commit on dev `e8454e275`, one-line subject, no body, no trailers. Local, not pushed, no PR. It adds the dated section "Dev 5603c353, 2026-10-10: lane B15" (with its Contents line, the introduction's pointer and the page title's image list) to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, and updates its row in `docs/findings/README.md`; no other file.
- **Gates:** every gate rc 0 at `70cd90a4` (gates/gates.txt, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 331 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check e8454e27 HEAD`. The bare `check_baremetal_only.py` is a usage error, rc 2 (gate-13), as lanes B6 to B10 recorded.
- **PR body:** PR-BODY.md, "Refs #629".

## Step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only): #629 and every [A10] comment; the findings page (lanes B6 to B8 on dev; B9 and B10's STOPs and packets); first light; #617 and its bench page; lane B9 and B10's packets | Read | this file |
| 1 | Local preconditions | 15:13: the board-link host address present; the UAC2 card and the external capture card present; three serial adapters; the lock free. SoC board over key-based SSH: uid 0; to-host leg running (pid 234), from-host DEAD as found; UDC configured | soc/precheck-status.log |
| 1b | The tone source's state, read only (its documented state read; nothing written) | 15:15: recorded privately; the playback route is checked from its meters with the tone playing (step 7) | private |
| 2 | TAKEN on #629 | POSTED 15:16 | TAKEN.md, taken-url.txt, TAKEN.readback.md |
| 3 | Identity gate (identity_b15.sh, identity_b15.py) | 15:17:48 to 15:17:54: **PASS**: entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001"; console ID 4d494c4e, VERSION 00020060; AEM CRC 5ba355eb over 7,512 B; live ENTITY and CONFIGURATION byte-equal to the QSPI AEM; CLOCK_SOURCE 0 to 2 of #629, 3 absent; CLOCK_DOMAIN 0 lists 0, 1, 2 and reads 0; grader 10/10; ADP model 001bc5c1935893e1 | identity/ |
| 4 | Start baseline (baseline_b15.sh start) | 15:18:57 to 15:19:04, all rc 0. As found: DUT unbound, STREAM_INPUT 0 at `0205022001006000`, STREAM_PORT_INPUT 0 with 4 identity mappings, STREAM_PORT_OUTPUT 0 with 8, CLOCK_SOURCE 0; the peer's STREAM_INPUT 0 bound to the DUT's AAF talker and its CRF input to the DUT's CRF, its CLOCK_DOMAIN on the source on that CRF input; NVM seq 272, 38 commits, pend=0 | restore/*-start* |
| 5 | Tap probe: 200 frames on each tap | 15:20:38 to 15:20:39: both taps carry the 28-byte record header; port 2 = switch to device, 3 = device to switch | runs/tapprobe-lock.txt |
| 6 | Tool controls (offline) | 15:21 to 15:25: lane B6's and lane B9's byte-equal to lane B10's (`7bbefc71...`, `728a4f0e...`); the new tap decode (tone_points_b15.py control) 5 of 5 PASS | controls/ |
| 7 | Tone started (tone_play_b15.sh start 1800) | 15:26:58 to 15:27:06: STARTED, one process; loop `d9684a8f...` (lanes B9 and B10's); playback RUNNING (+48,257 frames in 1.007 s); the tone source's meters, read passively: the tone leaves it at -38.5 dBFS on the outputs that carry it and no other (playback -20.0 dB, an output level setting of -18.5 dB read in step 1b) | runs/tone-start.txt; meter rows private |
| 8 | pts1: four points, (d) by binding the peer's listener to its own talker (points_locked_b15.sh ... pts1 10 control) | 15:27:19 to 15:27:59, ACTION_RC 0. (a) TONE ABSENT: channels 0 to 3 at -141.09 to -141.49 dBFS, -2 to +1 LSB, 191,843 PDUs, 0 gaps; (b) the same; (c) TONE ABSENT, the same levels, channels 4 to 7 zero; (d) unusable: the peer's listener received nothing (a switch does not send a frame back out of its ingress port; its counters 0), its digital output exact zero. Restore: every bind undone, the peer's STREAM_INPUT 0 format restored and its as-found bind remade (rx flags 0x0082 as found, 0x0002 right after, 0x0082 again at pts2) | runs/pts1/, summary/pts1/ |
| 8b | Incident: pts1's leg restart printed LEG_PRESENT_NOT_STARTED (the `ps` presence check matched its own SSH command line); the to-host leg was down from 15:27:23 to 15:28:23; check fixed to read `status`; restarted under the lock: pid 1723 | soc/pts1-legs.log |
| 9 | pts2: four points with the positive control (points_locked_b15.sh ... pts2 10 dira) | 15:31:03 to 15:31:44, ACTION_RC 0. Lane B6's loop (`566d3dfa...`) copied to the board, checked, played into McASP0 (the DUT's TDM input) and removed. (a), (b), (c) TONE ABSENT as in pts1; the DUT's talker on both taps and (d) carry both tones at -1.00 dBFS, 997.0000 and 9,973.0000 Hz, THD+N at the loop's floor in every block wholly inside the playback (15 of 23 per tap, 13 of 16 at (d)). Final state equal to the run's start in every read | runs/pts2/, summary/pts2/ |
| 10 | Alignment (c) against (b) (align_b15.py) and its planted controls | pts1 and pts2 SAMPLE-EXACT: 480,000 of 480,000 frames, the first window matched once, 0 slips; controls 5 of 5 (first run: the drop case failed by one frame on an expected index; the expectation now follows the content) | summary/pts*/align-b-c.json, controls/b15-align-controls.json |
| 11 | The peer's routing over ATDECC, read only (READ_DESCRIPTOR, GET_CONTROL) | 15:35:10: AUDIO_CLUSTER 0 to 19 (16 to 19, the talker port's, take their signal from AUDIO_UNIT 0); no JACK, EXTERNAL_PORT or INTERNAL_PORT descriptors; one CONTROL, IDENTIFY; with the start survey's GET_AUDIO_MAP (talker channel c from cluster c, identity) | private (descriptor payloads); summarised on the page |
| 12 | Tone stopped (tone_play_b15.sh stop) | 15:35:30 to 15:35:34: KILLED by its PID; no playback process left; the playback device closed; 0 underruns | runs/tone-stop.txt |
| 13 | End baseline (baseline_b15.sh end), controller staging removed | 15:35:37 to 15:35:44, all rc 0; census 45 of 46 equal (the DUT's live propagation delay, 381 to 387 ns); DUT words equal but the live ones and `SLIP_LB` 146 to 152 dups; NVM seq 276, 42 commits, pend=0; board: to-host leg pid 1948, from-host DEAD as found, UDC configured | restore/*-end*, restore/census-compare.txt, restore/controller-cleanup.txt |
| 14 | Findings section, index row, gates, commit | `70cd90a4`, every gate rc 0 | gates/ |
| 15 | Redaction pass (redact_b15.py, private map), value scan | 31 files masked; a scan for every private name, address, identifier and the capture's format finds none | redaction.json |
| 16 | STOP on #629 | POSTED (comment 6098146914); readback equal but for one trailing newline. After it: nothing running on this host, the controller host, the tap host or the SoC board; the bench lock free | STOP.md, STOP.readback.md, stop-url.txt |
| 17 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 15:16:59-15:17:03 | Controller staging and ADP discovery | rc 0 |
| 15:17:48-15:17:54 | Identity gate: DUT console reads, UART grader, AECP descriptor walk, ADP | all rc 0 |
| 15:18:57-15:19:04 | Start baseline: SoC health (SSH), DUT reads, census, counters, descriptor surveys, controller, host view | all rc 0 |
| 15:20:38-15:20:39 | Tap probe, 200 frames per tap, removed from the tap host | rc 0 |
| 15:26:58-15:27:06 | Tone start (`flock -o`; playback detached with its own log, self-ending after 1,800 s) and a passive meter read | STARTED, RUNNING; the lock free after |
| 15:27:19-15:27:59 | pts1: to-host leg stopped by PID; peer AAF to DUT STREAM_INPUT 0; the peer's listener unbound from the DUT and bound to its own talker (format set and restored); 24.5 s of both taps, 16 s external capture, 10 s McASP0; teardown with read-backs; tap files fetched and removed | ACTION_RC 0; leg restart NOT done (incident) |
| 15:28:2x | The to-host leg restarted with its recorded line | STARTED, pid 1723 |
| 15:31:03-15:31:44 | pts2: to-host leg stopped by PID; lane B6's loop staged on the board; peer AAF to DUT STREAM_INPUT 0; the same captures with McASP0 playing the loop; teardown with read-backs; loop removed from the board; tap files fetched and removed; leg restarted | ACTION_RC 0; leg pid 1948 |
| 15:35:10 | The peer's routing descriptors and its one control, read only | rc 0 |
| 15:35:30-15:35:34 | Tone stop by PID (command line checked) | KILLED; device closed |
| 15:35:37-15:35:44 | End baseline and controller staging removal | all rc 0 |

No outlet, JTAG, flash, reload, SoC board reboot, USB gadget action, UDC write, wiring or instrument setting was touched. The SoC board was reached only over key-based SSH; its serial console was not used. The only instrument actions were starting and stopping the tone's playback, a read of the tone source's state and passive reads of its meters, and the external capture's recordings. No DUT register was written; the DUT changes were the method's binds of its STREAM_INPUT 0, each undone and read back. The bench lock was taken for every console, controller, tap and board action and was free at the end.

## Run ledger (one row per case or cycle)

| Case | Window start | Window | Result |
|---|---|---|---|
| pts1 (a), (b), (c), (d) | captures from 15:27:28.7 | taps 24.5 s, external 16 s, McASP0 10 s | (a), (b), (c) TONE ABSENT at the -141 dBFS floor; (c) equal to (b) sample for sample; (d) unusable |
| pts2 (a), (b), (c), (d) and the control | captures from 15:31:13.1 | as pts1 | (a), (b), (c) TONE ABSENT; (c) equal to (b); the control present at both taps and (d), sample-exact |
| B0 (control) | - | - | NOT RUN: the tone does not reach the DUT |
| B-CRF | - | - | NOT RUN: as above |
| B-AAF | - | - | NOT RUN: as above |

## Tool changes

Lane B10's tools directory was copied as taken (tools/ORIGIN-B10.sha256 pins every file, tap_order_decode.py included; lane B9's tools are byte-equal to lane B10's where both exist). Unchanged and used: b6_thdn.py, b9_thdn.py (controls), b6_tone.py, b9_tone.py, avdecc_ro.py, b8_ctl.py, console_read.py, census_cmp.py. Copied, not used: every other inherited tool (run_*, grade_*, probe_*, identity_b7 to b10, baseline_b7 to b10, soc_legs_*, tone_play_b8 to b10, soccon*, lane_state_b10.sh, extcap_b10.py, redact_b9.py, the B5 to B8 helpers).

| Tool | Taken from | Change |
|---|---|---|
| identity_b15.sh | lane B10's identity_b10.sh | Environment B15_ENV, staging /tmp/a588; the console reads drop the BIOS ROM and bitstream payload CRCs (no dev 5603c353 build values here) |
| identity_b15.py | new (lane B10's identity_entity_b10.py inside it) | The four ATDECC facts, the console ID, VERSION and AEM CRC, live ENTITY and CONFIGURATION against the QSPI AEM, the clock sources, the grader and ADP. Its first run used CLOCK_SOURCE and CLOCK_DOMAIN offsets 2 bytes off and raised; corrected to IEEE 1722.1-2021 7.2.9 and 7.2.32 and run on the same read: PASS |
| baseline_b15.sh | lane B10's baseline_b10.sh | Environment and staging; the SoC board read over SSH instead of its console, same commands |
| soc_legs_b15.sh | lane B10's soc_legs_b10.sh | Over SSH; the to-host leg only (from-host DEAD as found); after pts1, the start's presence check reads `status` instead of a `ps` pattern |
| tone_play_b15.sh | lane B10's tone_play_b10.sh | Environment B15_ENV and its private directory; `start` and `status` end with a passive meter read |
| mixer_read_b15.py | new; kept privately, not in the packet, because it describes the tone source (SHA-256 `d5da1599e9547190e5c03277cff5eb6ecf771217bc5a8c90adee2feba3c0ec0a`) | The tone source's state read (one documented read request, no setting written) and a passive mode that sends nothing; tone_play_b15.sh calls it |
| redact_b15.py | lane B10's redact_b10.py | Its own name, tools/ORIGIN-B10.sha256 and the two inherited redact tools in the skip list; run once with a private map: 31 files masked (interface, host, account and adapter names, link addresses, USB positions, the peer's, the controller's and another entity's identifiers, the grandmaster's identity, the peer's ENTITY descriptor payload, the external capture's device name, format and channel count and its raw sizes). tone_points_b15.py is masked at its synthetic stream ID and is a record of the tool as run; redaction.json holds both hashes |
| points_b15.py, points_locked_b15.sh | new (the Agent class and controller agent are lane B10's probe_b10.py's) | The four-point capture under one lock; modes `control` (pts1) and `dira` (added after pts1, the positive control) |
| tone_points_b15.py | new | The AAF tap decode and the per-channel tone figures for every point, with 5 synthetic controls |
| align_b15.py | new | (c) against (b), frame by frame, with 5 planted controls |
| points_tables_b15.py | new | Renders summary/points.md from the grades and run records |

## Deviations and decisions

- **The STOP.** The assignment's branch "Tone absent at (a)" applied: the playback and routing state was read read-only, no instrument setting was changed, and the lane stopped. The DUT branch (stage localisation, fix, suite check, planted defect, RTL gates) and the THD+N cases did not run.
- **The tone source's routing check.** Its state read does not report the playback-to-output route, so the route was shown by its level meters with the tone playing: the tone left it on the outputs that carry it at -38.5 dBFS, its playback at -20.0 dB and the output level setting reading -18.5 dB. The owner's condition (the playback routed to those outputs at 0 dB) was taken as met by the route, with the output level recorded as read; the tone would be about 18.5 dB lower than -20 dBFS at the peer's inputs. That level does not explain a tone absent at (a), where only one or two LSB remain.
- **Point (d).** pts1 bound the peer's listener to the peer's own talker so that (d) would witness the talker without the DUT; it cannot work through a switch, and the run is recorded as run. pts2 made (d) a positive control instead, with McASP0 playing lane B6's loop into the DUT's TDM input (the McASP0 playback method lanes B3 and B6 used), keeping every binding as found.
- **Tap statistics.** The tap host's `tail` rejected `-2`, so tcpdump's packet and drop counts were not logged in runs/pts*/tap.txt. The decoded streams have 0 sequence gaps at (a) and (b) in both runs.
- **Grading criteria.** Lane B8's presence rule (over 90 % of the channel's power within 5 Hz, at -40 dBFS or more), fixed before any capture; the alignment verdict SAMPLE-EXACT needs every frame equal with no slip.

## Residuals

- **DUT NVM:** image seq 272 to 276, commits 38 to 42 (the two binds of STREAM_INPUT 0 and their unbinds), pend=0 at both ends.
- **DUT `SLIP_LB`:** 146 to 152 dups (3 slipped frames on the loopback ring, with the DUT on INTERNAL while the peer's talker was bound), not timed.
- **SoC board:** the to-host leg under a new pid (1948); it was down 15:27:23 to 15:28:23 in the incident; the from-host leg dead as found and not started.
- **The peer:** every state as found; its listener's rx flags read 0x0002 right after pts1's rebind and 0x0082 again afterwards.

## Open items for the owner and the manager

- **The tone's path into the peer's talker.** The tone leaves the tone source, but the peer's talker carries only one or two LSB on its channels 0 to 3. The path from the peer's inputs to its talker is not observable over ATDECC. The owner decides any instrument change; Direction B's THD+N (B0, B-CRF, B-AAF) then needs a tone present at (a), and pts2's method grades the whole chain.
- #629 stays open: "Refs #629".

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.*, STOP.*, *-url.txt | The posts and their readbacks |
| PR-BODY.md | Proposed PR body |
| identity/ | The identity gate: console reads, grader, AECP descriptor walk, ADP, verdict |
| soc/ | SoC board status before the lane, health at start and end, the leg stop and restart transcripts |
| runs/ | Each locked action's record: the tap probe, the tone start and stop, pts1 and pts2 (events, controller transactions, board recording log, capture logs) |
| summary/ | Per-point grades (tone_points_b15.py), the alignments, the reduced external-capture rows and points.md |
| controls/ | Lane B6's and lane B9's controls, the tap decode's and the alignment's |
| restore/ | Census, counters, DUT reads, descriptor surveys, controller and host views at start and end, the census comparison, the cleanup |
| tools/ | Every tool used or copied; ORIGIN-B10.sha256 pins lane B10's |
| gates/ | Gate commands and outputs at `70cd90a4` |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| RAW-ARTIFACTS.json | Every raw file by path and SHA-256 (the external capture's sizes and the tone loop's size withheld) |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
