# [A603] Bench lane B16 handoff

Refs #629: Direction B's known tone after the maintainer's loopback result. Reproduce the reference peer's own loopback (its listener bound to its own talker) as the positive reference, locate the step where lane B15's setup differs, then grade Direction B end to end; dev `5603c353` bench image as flashed and booted.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117358154 (posted 05:44 CEST; TAKEN.md, taken-url.txt)
- STOP: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117604151 (posted 06:11 CEST with the head and the per-run tables; STOP.md, stop-url.txt; STOP.readback.md equal but for one trailing newline). TAKEN.readback.md likewise
- Posted on #629: TAKEN and STOP only; no existing comment was edited or deleted.
- Branch: `629-b16-tone` from dev `c20c85bd`, lane worktree on the physical /data path.
- Packet: this directory. Raw files (pcaps, recordings) stay outside it on the bench host (RAW-ARTIFACTS.json); private endpoints, the redaction map, the unmasked originals, the tone's loop and playback log, the tone source's state reads and meter rows, the external capture's all-channel rows and the private mixer read tool stay in the private directory (not in the packet).

## State

**Round 3 (B16 findings round 3, documents only): REVIEW READY; head `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5`. No bench action. See "Round 3" at the end of this file. The earlier records stand as written; the page's figures they quote were corrected where round 3's check found them off (listed there).**

**Round 2 (B16 findings round 2, documents only): REVIEW READY; head `35e332b6be3de2b36c4aec0f1d0bc9f390447b74`. No bench action. See "Round 2" at the end of this file. The B16, B16b and B16c records stand as written, but for one count in B16c's step c6, corrected there.**

**B16c (the resume after the manager's ruling on the B16b STOP): REVIEW READY; B-CRF and B-AAF graded; head `e20fd2820a9c6b9effabc529a742e732263fafa8`; posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118971388. See "B16c" at the end of this file. The B16 and B16b records stand as written.**

**B16b (the resume after the manager's ruling): STOP at step 4, B-CRF and B-AAF needing a decision; head `0d4ff91952bf46f786e08c7da24ffe777ba166da`; posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118143691. See "B16b (resume after the manager's ruling)" at the end of this file. The B16 record below stands as written.**

**STOP** (2026-10-12; bench work 05:44 to 06:03 CEST), under step 2 of the assignment: "If the tone is absent here, record the per-channel levels for each source output channel that the documented wiring allows, read the source's routing read-only, and STOP". The reference peer's listener, bound to its own talker under the binding rule, never formed a stream in two runs. The tap over the bind (`loop2`) shows why: the peer sends PROBE_TX (CONNECT_TX) for its own talker to the network twice, 200 ms apart, and nothing answers, so its listener never learns the stream and its talker never starts. The peer's digital output read exact zero. The tone source, read only: the playback reaches the documented outputs at 0 dB as lane B15 read, and now also a second pair of outputs that lane B15 read silent. Steps 3 and 4 and B0, B-CRF and B-AAF did not run; no DUT stage was reached and no DUT change was made.

- **Commit:** `694d7da601a29c099d1d01fd29b61fc23f2160c0` on `629-b16-tone`, one commit on dev `c20c85bd`, one-line subject, no body, no trailers. Local, not pushed, no PR. It adds the dated section "Dev 5603c353, 2026-10-12: lane B16" (with its Contents line and the introduction's pointer) to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, and updates its row in `docs/findings/README.md`; no other file.
- **Gates:** every gate rc 0 at `694d7da6` (gates/results.json and one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The bare `check_baremetal_only.py` is a usage error (rc 2), as lanes B6 to B15 recorded, so its two modes were run.
- **PR body:** PR-BODY.md, "Refs #629".

## Step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only): #629 and every [A10] comment; the findings page (lanes B6 to B8 and B15; B9 and B10's STOPs; B9 and B10 have no section on dev); first light (#451) and #617's bench page; lane B15's packet and its private tool for the tone source's state | Read | this file |
| 1 | Local preconditions | 05:44: the board-link host address present; the board's USB audio card and the external capture card present; the lock free. SoC board over key-based SSH: uid 0; to-host leg running (pid 1948), from-host DEAD, McASP playback closed (no music), UDC configured | soc/precheck-status.log |
| 2 | TAKEN on #629 | POSTED 05:44 | TAKEN.md, taken-url.txt |
| 3 | Identity gate (identity_b16.sh, identity_b15.py) | 05:45:07 to 05:45:13: **PASS**, every fact equal to the assignment's | identity/ |
| 4 | Start baseline (baseline_b16.sh start) | 05:45:29 to 05:45:36, all rc 0. As found: lane B15's end state (DUT unbound on CLOCK_SOURCE 0, STREAM_INPUT 0 at `0205022001006000`, 4 and 8 identity mappings; the peer's STREAM_INPUT 0 on the DUT's AAF talker, STREAM_INPUT 8 on its CRF talker, its CLOCK_DOMAIN on CLOCK_SOURCE 1; NVM seq 276, 42 commits; `SLIP_LB` 152) | restore/*-start* |
| 5 | Tone source state, read only | 05:47:48 passive (nothing sent), 05:47:56 state read (one documented read request). Outputs of the documented pair: level setting -18.5 dB, unmuted; a second pair +6.0 dB | private (mixer-state-1.json) |
| 6 | Tool controls (offline) | lanes B6 and B9's byte-equal to lane B15's (`7bbefc71...`, `728a4f0e...`); tone_points_b16.py 8 of 8; align_b16.py synthetic 6 of 6 | controls/ |
| 7 | Tone started (tone_play_b16.sh start 7200) | 05:55:37 to 05:55:44: STARTED, one process; loop `d9684a8f...`; RUNNING (+48,335 frames in 1.007 s); meters: the documented pair -38.5 dBFS (-20.0 before the setting), a second pair -14.0 dBFS (-20.0 before the setting), playback -20.0 | runs/tone-start.txt; meter rows private |
| 8 | loop1: the peer's loopback (run_locked_b16.sh ... loop1 loop 16) | 05:56:31 to 05:57:31, ACTION_RC 0. Bind SUCCESS; the listener's stream ID and destination 0, flags `0x0002`, counters 0 at all 14 polls; the talker's connection count 0; no peer talker PDU on either tap; the peer's output exact zero. Restored and read back equal | runs/loop1/, summary/loop1/ |
| 9 | loop2: the same, taps over the bind (mode looptap, added after loop1) | 05:59:18 to 06:00:29, ACTION_RC 0. As loop1; the tap records BIND_RX response at +99.6 ms and PROBE_TX for its own talker at +99.6 ms and +299.6 ms, no response in 49 s | runs/loop2/, summary/loop2/ |
| 10 | STOP branch: per-channel levels and the routing, read only | 06:01:44 meters (unchanged), 06:01:48 state read: identical to 05:48 (2,266 state entries, 0 differ) | runs/tone-status.txt; private |
| 11 | Tone stopped (tone_play_b16.sh stop) | 06:02:00 to 06:02:03: KILLED by its PID; device closed; no underrun logged | runs/tone-stop.txt |
| 12 | End baseline (baseline_b16.sh end), staging removed | 06:02:07 to 06:02:14, all rc 0; census 45 of 46 (the DUT's live propagation delay, 387 to 377 ns); DUT NVM and `SLIP_LB` unchanged; tap host clean at 06:02:37 | restore/*-end*, restore/census-compare.txt, restore/tap-host-end.txt |
| 13 | Findings section, index row, gates, commit | `694d7da6`, every gate rc 0 | gates/ |
| 14 | Redaction pass (redact_b16.py, private map), value scan | redaction.json; the scan for every private name, address, identifier and the capture's format finds none | redaction.json |
| 15 | STOP on #629 | POSTED (comment 6117604151); readback equal but for one trailing newline. After it: nothing running on this host, the controller host, the tap host or the SoC board; the bench lock free | STOP.md, STOP.readback.md, stop-url.txt |
| 16 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 05:44:40 | SoC board status over key-based SSH (read only) | rc 0 |
| 05:45:07-05:45:13 | Identity gate: DUT console reads, UART grader, controller staging, AECP descriptor walk, ADP | all rc 0 |
| 05:45:29-05:45:36 | Start baseline: SoC health, DUT reads, census, counters, descriptor surveys, controller, host view | all rc 0 |
| 05:47:48-05:47:51 | Tone source, passive meter read (nothing sent) | rc 0 |
| 05:47:56-05:48:02 | Tone source, state read (its documented read request) | rc 0 |
| 05:55:37-05:55:44 | Tone start (`flock -o`; playback detached with its own log, self-ending after 7,200 s) and a passive meter read | STARTED, RUNNING; the lock free after |
| 05:56:31-05:57:31 | loop1: the peer's STREAM_INPUT 0 unbound from the DUT's AAF talker and bound to the peer's own talker (format set and restored); polls; 30.6 s of both taps and 22 s of the external capture; teardown with read-backs; tap files fetched and removed | ACTION_RC 0 |
| 05:59:18-06:00:29 | loop2: the same with both taps started before the unbind (52.5 s) and 16 s of the external capture | ACTION_RC 0 |
| 06:01:44-06:01:48 | Tone status and passive meter read | RUNNING |
| 06:01:48-06:01:54 | Tone source, state read | rc 0 |
| 06:02:00-06:02:03 | Tone stop by PID (command line checked) | KILLED; device closed |
| 06:02:07-06:02:14 | End baseline and controller staging removal | all rc 0 |
| 06:02:37 | Tap host check: no lane file, no capture process | clean |

No outlet, JTAG, flash, reload, SoC board reboot, USB gadget action, UDC write, wiring or instrument setting was touched. The SoC board was reached only over key-based SSH; its serial console was not used, and its bridge legs were never stopped (no McASP0 recording was needed). The only instrument actions were starting and stopping the tone's playback, two state reads of the tone source and passive reads of its meters, the external capture's recordings, and the method's binds of the peer's STREAM_INPUT 0, each undone and read back. No DUT register was written and no DUT stream was bound. The bench lock was taken for every console, controller, tap, board and tone-source action and was free at the end.

## Run ledger (one row per case or cycle)

| Case | Window start | Window | Result |
|---|---|---|---|
| loop1 (step 2) | bind 05:56:31.3; captures from 05:56:45 | taps 30.6 s, external 22 s; polls 12 s after the bind and after the captures | No stream; the peer's output exact zero; TONE ABSENT: STOP |
| loop2 (step 2, taps over the bind) | taps from 05:59:19; bind 05:59:22.1; external from 05:59:36 | taps 52.5 s, external 16 s | As loop1; the unanswered PROBE_TX recorded |
| Step 3, the talker stream | - | - | NOT RUN: no loopback carried the tone; the talker sent no PDU |
| Step 4, Direction B end to end | - | - | NOT RUN: STOP at step 2 |
| B0, B-CRF, B-AAF | - | - | NOT RUN: STOP at step 2 |

## Tool changes

Lane B15's tools directory was copied as taken (tools/ORIGIN-B15.sha256 pins every file; lane B15's copies of lanes B6 and B9's tools are byte-equal to lane B10's). Unchanged and used: b6_thdn.py and b9_thdn.py (controls), b9_tone.py, b6_tone.py, avdecc_ro.py, b8_ctl.py, console_read.py, census_cmp.py, identity_b15.py. Copied, not used: every other inherited tool.

| Tool | Taken from | Change |
|---|---|---|
| identity_b16.sh | lane B15's identity_b15.sh | Environment B16_ENV and staging /tmp/a603 in the commands; nothing else |
| baseline_b16.sh | lane B15's baseline_b15.sh | The same |
| soc_legs_b16.sh | lane B15's soc_legs_b15.sh | Environment B16_ENV; copied for step 4, not used |
| tone_play_b16.sh | lane B15's tone_play_b15.sh | Environment B16_ENV and its private directory; the passive meter read calls the private mixer_read_b16.py under sudo |
| mixer_read_b16.py | new, from lane B15's private mixer_read_b15.py decode; kept privately, not in the packet, because it describes the tone source (SHA-256 `b1c8ebfef21cc455c005852b70eac1d1610bb6e14c838cb0479d1d56a77d28a5`) | Another client held the tone source service's reply port, which lane B15's tool binds. This tool sniffs the loopback interface for the service's replies instead (it binds nothing); `state` sends the same one documented read request as lane B15's, `passive` sends nothing |
| tone_points_b16.py | lane B15's tone_points_b15.py | Presence floor -100 dBFS (lane B15: -40), with a flag below -40; the controls use a synthetic stream ID and address (lane B15's carried the peer's, masked); three new controls (-60 dBFS present and flagged, -130 dBFS absent, 8 channels with the tone on 5/6). Fixed before any capture |
| align_b16.py | lane B15's align_b15.py | Compares full 24-bit values (lane B15 keyed on each sample's low byte, exact only for the idle floor); a sixth control (+256 LSB, low byte unchanged) that lane B15's misses; a synthetic-stream control mode; an optional stream channel list. Built for step 4, which did not run |
| run_b16.py | new; lane B15's points_b15.py restructured (its Agent, binding rule, captures, tap fetch, teardown) | Modes loop, looptap (added after loop1), dirb, dirbloop; listener and talker polls every 2 s; a McASP playback precheck; the final read-back also covers the DUT's STREAM_INPUT 1 and the peer's STREAM_INPUT 8 and ignores the rx flags word (recorded) |
| run_locked_b16.sh | lane B15's points_locked_b15.sh | One run_b16.py action under `flock -o` with a deadline; the to-host leg is stopped only for the McASP0 modes (not used: only loop modes ran) |
| acmp_tap_b16.py | new | ACMP messages and stream PDU counts from a tap capture |
| extcap_pair_b16.py | new | The external capture's grade reduced to the peer output pair, indices passed from the private record |
| gates_b16.py | lane B15's gates_r2.py pattern | The lane's gate list, one log per gate, unpiped |
| redact_b16.py | lane B15's redact_b15.py | Its own name, ORIGIN-B15.sha256 and the inherited redact tools skipped; the rule text |

## Deviations and decisions

- **The STOP.** Step 2's branch applied: the tone was absent at the loopback's output, the per-channel levels were recorded and the source's routing read read-only. The lane did not continue to steps 3 and 4. The cause found is not wiring but the bind: no stream formed. The STOP and its "Needed to resume" say so and ask the owner for the working loopback's method, or a ruling to run lane B15's four-point capture with the DUT bound.
- **loop2.** Added after loop1, whose taps started after the bind; it is the same run with the taps started first, to put the bind's ACMP exchange on record.
- **The tone source read.** The playback-to-output routes are not reported by the service, so they are shown by the meters before and after each output's level setting. The state read is the service's documented read request, sent once per read; the transport changed because another client held the reply port.
- **The second output pair.** Found carrying the tone; it was silent in lane B15's read. Recorded, not changed, not part of the documented wiring.
- **Presence floor.** Lowered to -100 dBFS before any capture (the tone leaves the source at -38.5 dBFS); no capture held any tone, so no verdict depends on it.

## Residuals

- **DUT:** the AAF talker's STREAM_START and STREAM_STOP each +2 (the peer's listener unbound and rebound twice); NVM seq 276 and 42 commits, unchanged; `SLIP_LB` 152, unchanged.
- **The peer:** its STREAM_INPUT 0 counters restarted at the rebinds (TIMESTAMP_VALID and FRAMES_RX lower at the end; SEQ_NUM_MISMATCH 1 to 0); every state as found.
- **SoC board:** untouched beyond reads; the to-host leg still pid 1948.

## Open items for the owner and the manager

- **The working loopback.** It is not an ATDECC bind of the peer's listener to its own talker on this network path: the peer's probe of its own talker is never answered. The owner holds the method.
- **The tone source's second output pair** now carries the playback; whether the peer's talker now carries the tone is not shown, because no listener received the talker in this lane. Lane B15's four-point capture (the DUT bound to the peer's talker) would show it; step 4 and B0, B-CRF and B-AAF can then run with run_b16.py (dirb), align_b16.py and b9_thdn.py.
- #629 stays open: "Refs #629".

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.*, STOP.*, *-url.txt | The posts and their readbacks |
| PR-BODY.md | Proposed PR body |
| identity/ | The identity gate: console reads, grader, AECP descriptor walk, ADP, verdict |
| soc/ | SoC board status before the lane and health at start and end |
| runs/ | Each locked action's record: the tone start, status and stop, loop1 and loop2 (events, controller transactions, capture logs) |
| summary/ | Per-point grades (tone_points_b16.py), the ACMP decodes, the reduced external-capture rows |
| controls/ | Lanes B6 and B9's controls, the tap decode's and the alignment's |
| restore/ | Census, counters, DUT reads, descriptor surveys, controller and host views at start and end, the census comparison, the cleanup, the tap host check |
| tools/ | Every tool used or copied; ORIGIN-B15.sha256 pins lane B15's |
| gates/ | Gate logs and results at `694d7da6` |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| RAW-ARTIFACTS.json | Every raw file by path and SHA-256 (the external capture's sizes and the tone loop's size withheld) |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |

## B16b (resume after the manager's ruling)

- Ruling: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835 (2026-10-12 04:19 UTC): run lane B15's four-point capture with the DUT's listener bound to the peer's talker, under the binding rule: (a) the peer's talker stream on the peer's link, (b) the same stream on the DUT's link, (c) the DUT's TDM output on the audio board's McASP, (d) the external capture's positive control. Play lane B15's tone through the same source; record the source's route read-only and change nothing. If the tone is present at (a), run step 4 (B0, B-CRF and B-AAF by THD+N and SNR) and attribute every loss to a stage; if absent at (a), record the per-channel levels at each point and STOP. Restore exactly as in B16; check before each bind that the audio board's McASP playback is free.
- Head at resume: `694d7da601a29c099d1d01fd29b61fc23f2160c0` (git rev-parse, 06:20 CEST). New commits only; TAKEN not posted again.

### B16b state

**STOP** (2026-10-12; bench work 06:22 to 06:53 CEST), at step 4 of the ruling: B-CRF and B-AAF need a decision. Lane B15's four-point capture finds the tone present in the peer's own talker stream at (a), equal at (b), and at the DUT's TDM output (c) sample for sample in every compared frame; the positive control (d) is present. B0 (the DUT on INTERNAL) was graded by THD+N and SNR over 300 s with every loss attributed to a stage: all impairments are already in the peer's talker stream, none is added by the network or the DUT. B-CRF and B-AAF were not run: as found the peer's CLOCK_DOMAIN follows the DUT's CRF talker, so either case would have the DUT follow its own clock through the peer, and the clock-source rule forbids setting the peer (the talker). The tone source's clock setting changed during the lane, outside it (read only). No DUT change was needed or made.

- **Commit:** `0d4ff91952bf46f786e08c7da24ffe777ba166da` (tree `ba8dbac504520148ff4c375f9612bd1ff19d22fb`) on `694d7da6`, a new commit (no rebase, no amend), one-line subject, no body, no trailers. Local, not pushed, no PR. Diff against `694d7da6`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+344/-4: ten `### B16b:` subsections at the end of lane B16's section, the Contents line, the introduction's pointer, a pointer in the B16 introduction, and the B16 hash row of `run_b16.py` moved to its as-run copy `tools/b16-asrun/run_b16.py`, same hash) and its row in `docs/findings/README.md`.
- **Gates at `0d4ff919`:** all 14 rc 0 (gates/b16b/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 2,651 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before the commit (private record).
- **Before the commit:** a scan of the added lines for private names, addresses, identifiers, capture formats, home paths and tool or model names: no match.
- **PR body:** PR-BODY.md, "Refs #629".

### B16b step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| b0 | Context: the ruling, lane B15's `pts2` method (points_b15.py `dira`), lanes B7 and B9's B0 definition (run_b9.py) | Read | this file |
| b1 | run_b16.py mode `dira` restored from lane B15's points_b15.py, before any B16b bench action | Done | tools/run_b16.py |
| b2 | Local preconditions and SoC board status | 06:22:23: board-link address present; both USB audio cards present; lock free. Board: uid 0; to-host leg pid 1948, from-host DEAD; McASP playback closed (no music); UDC configured | soc/b16b-precheck-status.log |
| b3 | Identity gate (identity_b16.sh, identity_b15.py) | 06:22:29 to 06:22:34: **PASS**, every fact as in B16 | identity-b16b/ |
| b4 | Start baseline (baseline_b16.sh startb) | 06:22:38 to 06:22:45, all rc 0; census equal to B16's end in 45 of 46 (the DUT's live propagation delay) | restore/*-startb*, restore/census-compare-b16-to-b16b.txt |
| b5 | Tone source, passive meters and state read (read only) | 06:23:03 to 06:23:13; the state read equal to B16's 06:01 read (2,262 entries, 0 differ) | private |
| b6 | Tone started (tone_play_b16.sh start 7200) | 06:23:26 to 06:23:33: STARTED, loop `d9684a8f...`, RUNNING; meters as in B16 | runs/b16b-tone-start.txt |
| b7 | `pts1` (dirb, 10 s) | 06:23:39 to 06:24:28, ACTION_RC 0; tone PRESENT at (a), (b), (c); (c) SAMPLE-EXACT to (a) and (b) | runs/pts1/, summary/pts1/ |
| b8 | `pts2` (dira, 10 s, the positive control) | 06:28:06 to 06:28:56, ACTION_RC 0; as `pts1`; (d) lane B6's loop present; two 2-frame repeats at (d) on neither tap | runs/pts2/, summary/pts2/ |
| b9 | Decision: B0 runs; B-CRF and B-AAF stop for a decision (the peer follows the DUT's CRF as found; the clock-source rule) | Recorded before B0 | this file |
| b10 | run_b16.py mode `b0` added (lane B9's second bind, DUT console words, 40 s taps, 20 s settle) | Done before `b0` | tools/run_b16.py |
| b11 | `b0` (300 s) | 06:31:28 to 06:37:05, ACTION_RC 0, but McASP0's recording "Device or resource busy": the wrapper did not stop the leg for mode `b0`. Binds undone and read back; leg untouched (pid 2808) | runs/b0/, soc/b0-after-status.log |
| b12 | run_locked_b16.sh: mode `b0` stops and restarts the leg | Done | tools/run_locked_b16.sh |
| b13 | `b0-2` (300 s), B0 | 06:37:31 to 06:43:17, ACTION_RC 0; McASP0 460,800,000 bytes, no overrun; graded | runs/b0-2/, summary/b0-2/ |
| b14 | Grading of `b0-2` (b9_thdn.py, tone_points_b16.py, align_b16.py); the tone's change found (0.000 ppm, -14.1035 dBFS) | Offline | summary/b0-2/ |
| b15 | `pts3` (dirb, 10 s): does the change follow the CRF bind? | 06:48:55 to 06:49:45, ACTION_RC 0; no: as `b0-2` | runs/pts3/, summary/pts3/ |
| b16 | Tone source, passive meters and state read (read only) | 06:50:05 to 06:50:15; of 1,255 entries both reads hold, four differ: the clock setting, two monitoring-mix values, one unused output's level | private |
| b17 | Tone stopped (tone_play_b16.sh stop) | 06:52:19 to 06:52:22: KILLED by PID; device closed; the log holds five underruns (06:45:27 to 06:46:38, during offline grading) | runs/b16b-tone-stop.txt |
| b18 | End baseline (baseline_b16.sh endb), staging removed | 06:52:28 to 06:52:35, all rc 0; census 45 of 46 equal to the B16b start | restore/*-endb*, restore/census-compare-b16b.txt |
| b19 | Tap host check | 06:53:18: no lane file, no capture process | restore/tap-host-endb.txt |
| b20 | dloop_b16.py (new) and its planted control; (d) decoded in `pts2`, `b0`, `b0-2` | Control PASS; `pts2` two 2-frame repeats at 6.131 s and 12.113 s; `b0` and `b0-2` none | controls/b16b-dloop-control.json, summary/*/d-loop-decode.json |
| b21 | B16 as-run copies of run_b16.py and run_locked_b16.sh rebuilt by reversing the B16b edits; equal to the B16 manifest's hashes | `d1a60cc2...`, `9d701ec3...` | tools/b16-asrun/ |
| b22 | Redaction pass (redact_b16.py, private map), run before the commit and again after the gates | 61 B16b files masked (104 in redaction.json in all); the tools need none. A value scan of the packet for private names, addresses, identifiers, the capture's format and home paths finds only the local tool path in lane B15's inherited tools/gates_r2.py, pinned unchanged by ORIGIN-B15.sha256 | redaction.json |
| b23 | Findings, index row, gates, commit | `0d4ff919`, every gate rc 0 | gates/b16b/ |
| b24 | STOP on #629 | POSTED (comment 6118143691); readback equal but for one trailing newline | STOP-b16b.md, STOP-b16b.readback.md, stop-b16b-url.txt |
| b25 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

### B16b bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 06:22:23-06:22:24 | SoC board status over key-based SSH (read only) | rc 0; McASP playback closed |
| 06:22:29-06:22:34 | Identity gate: DUT console reads, UART grader, controller staging, AECP descriptor walk, ADP | all rc 0 |
| 06:22:38-06:22:45 | Start baseline: SoC health, DUT reads, census, counters, controller, host view | all rc 0 |
| 06:23:03-06:23:13 | Tone source: passive meter read (nothing sent), then its documented state read | rc 0 |
| 06:23:26-06:23:33 | Tone start (`flock -o`; playback detached, self-ending after 7,200 s) and a passive meter read | STARTED, RUNNING; the lock free after |
| 06:23:39-06:24:28 | `pts1`: to-host leg stopped by PID; the peer's AAF to the DUT's STREAM_INPUT 0; polls; both taps, the external capture, McASP0; teardown with read-backs; taps fetched and removed; leg restarted (pid 2576) | ACTION_RC 0 |
| 06:28:06-06:28:56 | `pts2`: as `pts1`, with lane B6's loop staged on the board and played into McASP0; loop removed; leg restarted (pid 2808) | ACTION_RC 0 |
| 06:31:28-06:37:05 | `b0`: DUT console reads; the peer's CRF to the DUT's STREAM_INPUT 1 and AAF to STREAM_INPUT 0; 300 s; McASP0 recording busy (leg not stopped); teardown with read-backs | ACTION_RC 0; incident |
| 06:37:14 | SoC board status (read only) | the leg pid 2808 running; McASP playback closed |
| 06:37:31-06:43:17 | `b0-2`: as `b0` with the leg stopped by PID and restarted (pid 3706) | ACTION_RC 0 |
| 06:48:55-06:49:45 | `pts3`: as `pts1`; leg restarted (pid 3899) | ACTION_RC 0 |
| 06:50:05-06:50:15 | Tone source: passive meter read and its documented state read | rc 0 |
| 06:52:19-06:52:22 | Tone stop by PID (command line checked) | KILLED; device closed |
| 06:52:28-06:52:35 | End baseline and controller staging removal | all rc 0 |
| 06:53:18-06:53:19 | Tap host check | clean |

No outlet, JTAG, flash, reload, SoC board reboot, USB gadget action, UDC write, wiring or instrument setting was touched. The SoC board was reached only over key-based SSH; its serial console was not used. Its to-host bridge leg was stopped only by the PID its `status` named, after the command-line check, and restarted with its recorded line; the from-host leg stayed dead as found. The only instrument actions were starting and stopping the tone's playback, two state reads and passive meter reads of the tone source, and the external capture's recordings. No DUT register was written; the DUT changes were the method's binds of its STREAM_INPUT 0 and 1, each undone and read back. No clock source was set on either entity. The bench lock was taken for every console, controller, tap, board and tone-source action and was free at the end.

### B16b run ledger

| Case | Window start (CEST) | Window | Result |
|---|---|---|---|
| `pts1` | McASP0 06:24:02; taps 06:23:58 | McASP0 10 s, taps 24.5 s, external 16 s | (a), (b), (c) TONE PRESENT (-14.1353 dBFS, +6.94 ppm); (c) SAMPLE-EXACT to (a) and (b); (d) no control in this mode |
| `pts2` | McASP0 06:28:29; taps 06:28:25 | as `pts1` | as `pts1` (+6.96 ppm); (d) the positive control PRESENT, 13 of 16 blocks at the loop's floor, two 2-frame repeats on neither tap |
| `b0` | taps 06:31:50 | taps 40 s, external 306 s | Incident: no McASP0 recording; not graded as B0; (a) 0.000 ppm, -14.1035 dBFS; (d) 0 discontinuities |
| B0, `b0-2` | McASP0 06:38:03; taps 06:37:59 | McASP0 300 s, taps 40 s, external 306 s | THD+N -123.95 / -122.80 dB median (floor -123.98 / -123.95, 169 of 300 blocks), 0 discontinuities, 0.0000 ppm; (c) SAMPLE-EXACT to (a) and (b) over 34.1 s; (d) 0 discontinuities in 14,583,286 frames |
| `pts3` | McASP0 06:49:18; taps 06:49:14 | as `pts1` | (a), (b), (c) TONE PRESENT (-14.1035 dBFS, 0.000 ppm); (c) SAMPLE-EXACT |
| B-CRF | - | - | NOT RUN: decision needed (STOP) |
| B-AAF | - | - | NOT RUN: decision needed (STOP) |

### B16b tool changes

Every tool is lane B16's as copied from lane B15 (tools/ORIGIN-B15.sha256), with these B16b changes. The B16 as-run versions of the two changed tools are kept in tools/b16-asrun/, rebuilt by reversing the B16b edits and checked equal to the B16 manifest's hashes.

| Tool | Change |
|---|---|
| run_b16.py | Mode `dira` (lane B15's points_b15.py `dira`: McASP0 plays lane B6's loop into the DUT's TDM input while it records the DUT's TDM output; the DUT's STREAM_PORT_OUTPUT 0 eight identity mappings and the peer's STREAM_INPUT 0 bound to the DUT's AAF talker checked as found, nothing edited; the loop staged at /tmp/a603-loop.raw on the board, SHA-256 checked there, removed at the end). The final read-back adds the DUT's STREAM_PORT_OUTPUT 0 map in that mode. Mode `b0` (added after `pts2`): `dira` plus lane B9's CRF bind (the peer's STREAM_OUTPUT 2 to the DUT's STREAM_INPUT 1) before the AAF bind, lane B9's DUT console words before the binds and after the captures, the DUT's clock source read after the binds and after the captures (refusing if not INTERNAL), a 20 s settle from the last bind, taps limited to 40 s, GET_COUNTERS of the DUT's STREAM_INPUT 1, and its format in the final read-back. The docstring records McASP0's 1 s recording buffer (`-B 1000000`), present since B16 but first used here |
| run_locked_b16.sh | Modes `dira` and `b0` also stop and restart the to-host leg around the action, as `dirb`; `b0` added after run `b0` |
| dloop_b16.py | New: lane B6's loop decoded at the external capture with lane B6's b6_tone.decode and b6_thdn.steps, unchanged; the pair's indices come from the private record; a planted control (one drop and one repeat after 2 s of silence) PASS |
| tools/b16-asrun/ | New: the B16 as-run run_b16.py (`d1a60cc2...`) and run_locked_b16.sh (`9d701ec3...`) |

Unchanged and used in B16b: identity_b16.sh, identity_b15.py, baseline_b16.sh, soc_legs_b16.sh, tone_play_b16.sh, tone_points_b16.py, align_b16.py, extcap_pair_b16.py, b9_thdn.py, b6_tone.py, b6_thdn.py, console_read.py, census_cmp.py, gates_b16.py, redact_b16.py; the private mixer_read_b16.py.

### B16b deviations and decisions

- **The STOP at B-CRF and B-AAF.** As found the peer follows the DUT's CRF talker (its CLOCK_SOURCE 1 on STREAM_INPUT 8, kept by the restore). Following the peer's CRF or AAF talker would close a loop through the DUT's own clock; the clock-source rule forbids setting the peer (the talker in both cases). Running the loop would grade something other than B-CRF and B-AAF, so the lane published the conflict instead of choosing.
- **B0's window** is 300 s, not lane B7's 630 s: one locked action must end within 10 minutes.
- **`pts3`** was added after `b0-2` to separate the tone's change from the CRF bind.
- **The tone source changed during the lane, outside it.** Recorded read only; nothing changed back.
- **The external capture's (d) discontinuities** were classified with lane B6's decoder (dloop_b16.py, new, with a planted control) after the grading showed blocks 6 and 12 of `pts2` off the floor; B16's draft wording ("partly outside the playback") was corrected before the commit.

### B16b residuals

- **The peer:** its AAF talker counted five more stream starts and stops (one per DUT bind), its CRF talker two; its listeners as found.
- **DUT:** `SLIP_LB` 152 to 162 dups (five slipped frames over five binds of STREAM_INPUT 0; one in each B0 run between its console reads); `SLIP_TDM` 0; servo IDLE; NVM seq 276 to 286, commits 42 to 52; its talkers' and CLOCK_DOMAIN counters unchanged.
- **SoC board:** the to-host leg under a new pid (3899) with its recorded line; the from-host leg dead as found.
- **Tone source:** its clock setting and three other settings differ from the lane's start, changed outside the lane.

### B16b posted

- STOP: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118143691 (posted 07:09:44 CEST with the head and the per-run tables; STOP-b16b.md, stop-b16b-url.txt; STOP-b16b.readback.md equal but for one trailing newline).
- After it: nothing running on this host, the controller host, the tap host or the SoC board beyond its bridge leg; the bench lock free.
- TAKEN was not posted again; no existing comment was edited or deleted.

### B16b packet layout (additions)

| Path | What |
|---|---|
| STOP-b16b.md, STOP-b16b.readback.md, stop-b16b-url.txt | The B16b post and its readback |
| identity-b16b/ | The identity gate at 06:22 |
| soc/b16b-precheck-status.log, soc/startb-health.log, soc/endb-health.log, soc/pts*-legs.log, soc/b0-2-legs.log, soc/b0-after-status.log | SoC board status, health and the leg stop and restart transcripts |
| runs/pts1/, runs/pts2/, runs/b0/, runs/b0-2/, runs/pts3/, runs/*-lock.txt, runs/b16b-tone-*.txt | Each locked action's record |
| summary/pts1/, summary/pts2/, summary/b0/, summary/b0-2/, summary/pts3/ | Per-point grades, alignments, the B0 grade, the (d) decodes |
| controls/b16b-dloop-control.json | The loop decode's planted control |
| restore/*-startb*, restore/*-endb*, restore/census-compare-b16b.txt, restore/census-compare-b16-to-b16b.txt, restore/tap-host-endb.txt | Census, counters, DUT reads, controller and host views at the B16b start and end |
| tools/b16-asrun/ | Lane B16's as-run copies of the two tools B16b changed |
| gates/b16b/ | Gate logs and results at `0d4ff919` |

## B16c (resume after the manager's ruling on the B16b STOP)

- Ruling: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090 (2026-10-12 05:31 UTC). The maintainer allows, for B-CRF and B-AAF only, setting the reference peer's clock source to its INTERNAL source over ATDECC (SET_CLOCK_SOURCE on the peer's CLOCK_DOMAIN, read back with GET_CLOCK_SOURCE), and after grading restoring it to following its CRF input, as found, read back. Every other part of the clock rule stands: the DUT's clock source is set only on the DUT as the listener, and read back. With the peer on INTERNAL: grade B-CRF (the DUT follows the peer's CRF talker) and B-AAF (the DUT follows the peer's AAF talker) with lanes B9 and B10's run tools, THD+N and SNR at the DUT's TDM output on McASP0, and B16b's four-point attribution. Then restore exactly as in B16, including the peer's clock source, and verify by census and counters. Check before each change that the audio board's McASP playback is free.
- Head at resume: `0d4ff91952bf46f786e08c7da24ffe777ba166da` (git rev-parse, 07:32 CEST). New commits only; TAKEN not posted again.

### B16c state

**REVIEW READY** (2026-10-12; bench work 07:47 to 08:04 CEST). Under the ruling, the reference peer's CLOCK_DOMAIN was set to INTERNAL and read back before each case and returned to its CRF input, as found, and read back after it. B-CRF and B-AAF were graded by THD+N and SNR at the DUT's TDM output over 300 s each, with B16b's four-point attribution. Both cases: servo LOCKED (2.66 to 3.16 s and 6.68 to 7.18 s after the set) and at all 596 window polls; THD+N -123.98 dB at 997 Hz and -123.97 dB at 9,973 Hz median, all 300 blocks at the path's floor, 0 discontinuities, 0.0000 ppm; (c) sample-exact to (a) and (b) over the taps' 34 s; (d) 0 discontinuities and 0 net steps. No stage loses the tone; no DUT change was needed or made. Restored exactly and verified by census and counters. #629 stays open (Direction B's INTERNAL mismatch control not run; #645): "Refs #629".

- **Commit:** `e20fd2820a9c6b9effabc529a742e732263fafa8` (tree `6299ec05fc1085b62defe945c9dc5c426e54d055`) on `0d4ff919`, a new commit (no rebase, no amend), one-line subject, no body, no trailers. Local, not pushed, no PR. Diff against `0d4ff919`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+367/-3: eleven `### B16c:` subsections at the end of lane B16's section, pointers in the introduction, the Contents line and the B16 introduction) and its row in `docs/findings/README.md` (+1/-1).
- **Gates at `e20fd282`:** all 14 rc 0 (gates/b16c/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,015 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before the commit (private record); `check_em_dash.py` reads the committed range only, so the run at the head is the one that covers the B16c lines.
- **Before the commit:** a scan of the added lines for every private-map entry, name, address, identifier, capture format, home path and tool or model name: no match. The post was scanned the same way.
- **PR body:** PR-BODY.md, "Refs #629".

### B16c step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| c0 | Context: the ruling; lanes B9 and B10's run tools (run_b9.py, run_b10.py: the B-CRF and B-AAF set, the servo poll, the window marks); the design's bench row; the peer's and the DUT's CLOCK_SOURCE descriptors from B16's surveys (the peer: 0 INTERNAL, 1 its STREAM_INPUT 8, as found; the DUT: 0 INTERNAL, 1 CRF on STREAM_INPUT 1, 2 AAF on STREAM_INPUT 0) | Read | this file |
| c1 | tools/run_b16c.py and tools/run_locked_b16c.sh (copies of B16b's run_b16.py and run_locked_b16.sh with modes `bcrf` and `baaf`), before any B16c bench action | Done (changes in "B16c tool changes") | tools/ |
| c2 | Offline dry run of run_b16c.py against stand-ins (tools/dryrun_b16c/): nominal B-CRF and B-AAF; the DUT's set refused; a deadline SIGTERM mid-window; the owner's music found before the binds; no servo lock; the peer not as found; the controller agent ending at a bind | 8 of 8 PASS, after one fix each to the stand-in and to the tool (the teardown now restarts a controller agent that ended, found by the first run); the wrapper's deadline path PASS | controls/b16c-dryrun-*.json, controls/b16c-wrapper-deadline.txt |
| c3 | Local preconditions and SoC board status | 07:47:56: board-link address present; both USB audio cards present; lock free. 07:48:07 board: uid 0; to-host leg pid 3899, from-host DEAD; McASP playback closed (no music); UDC configured | soc/b16c-precheck-status.log |
| c4 | Identity gate (identity_b16.sh, identity_b15.py) | 07:48:16 to 07:48:22: **PASS**, every fact as in B16 | identity-b16c/ |
| c5 | Start baseline (baseline_b16.sh startc) | 07:48:27 to 07:48:34, all rc 0; census equal to B16b's end in 45 of 46 (the DUT's live propagation delay); the peer on CLOCK_SOURCE 1, the DUT on 0 | restore/*-startc*, restore/census-compare-b16b-to-b16c.txt |
| c6 | Tone source, passive meters and state read (read only) | 07:48:53 to 07:49:03; the state read equal to B16b's 06:50 read in every entry both hold (618, 0 differ; round 2 corrected this from 622, which counted four meter addresses as entries) | private |
| c7 | Tone started (tone_play_b16.sh start 7200) | 07:49:29 to 07:49:37: STARTED, loop `d9684a8f...`, RUNNING; meters as in B16b (playback -20.0 dBFS, the documented pair -38.5, the second pair -14.0) | runs/b16c-tone-start.txt |
| c8 | `bcrf` (B-CRF, 300 s) | 07:50:00 to 07:56:15, ACTION_RC 0. The peer set to CLOCK_SOURCE 0, read back 0; both binds SUCCESS; the DUT set to 1, read back 1; servo LOCKED 2.66 to 3.16 s after the set, and at all 596 polls of the window; restore: the DUT to 0 (read back 0), unbinds, the peer to 1 (read back 1); final read-back equal to the start; tone RUNNING at all 1,805 reads | runs/bcrf/ |
| c9 | `baaf` (B-AAF, 300 s) | 07:56:52 to 08:03:07, ACTION_RC 0. As `bcrf` with the DUT's source 2, read back 2; servo LOCKED 6.68 to 7.18 s after the set, and at all 596 window polls; restored and read back equal; tone RUNNING at all 1,803 reads | runs/baaf/ |
| c10 | Tone source, passive meters and state read (read only) | 08:03:29 to 08:03:39; meters as at the start; of 668 entries both B16c reads hold, two differ only in which of two messages per address the read caught (two inputs of a monitoring mix, at minus infinity in both) | private |
| c11 | Tone stopped (tone_play_b16.sh stop) | 08:03:52 to 08:03:56: KILLED by PID; device closed; no underrun in the log | runs/b16c-tone-stop.txt |
| c12 | End baseline (baseline_b16.sh endc), staging removed | 08:04:02 to 08:04:09, all rc 0; census 45 of 46 equal to the B16c start (the DUT's live propagation delay); counters moved only as the method implies (below) | restore/*-endc*, restore/census-compare-b16c.txt |
| c13 | Tap host and SoC board check | 08:04:43: no lane file, no capture process on the tap host; the board's to-host leg running with its recorded line (pid 5145), from-host dead as found, McASP playback closed, no lane file | restore/tap-host-endc.txt |
| c14 | Grading of `bcrf` and `baaf` (tone_points_b16.py at (a), (b), (c), (d); b9_thdn.py grade; align_b16.py (c) against (a) and (b); extcap_pair_b16.py; dloop_b16.py), niced, with the tone stopped | 08:05 to 08:14, every rc 0; results in the run ledger | summary/bcrf/, summary/baaf/ |
| c15 | `SLIP_LB` timed against the servo state from the raw console polls; the window's trim, CRF and AAF meter rates; (d) blocks at the floor | Five steps before the DUT's set in each case, one (B-CRF) and two (B-AAF) in ACQUIRE, none after LOCKED; trim -6.000 to -6.125 ppm; the followed stream +10.6 ppm against gPTP; (d) 305 of 306 at the floor, block 2 the playback's start | runs/*/events.jsonl (poll-summary); raw polls listed in RAW-ARTIFACTS.json |
| c16 | tables_b16c.py (new) renders the findings rows from the packet's files | summary/b16c-tables.md; byte-equal when rendered again from the redacted files | summary/b16c-tables.md |
| c17 | Dry-run stand-ins: a capture-side value replaced by a neutral one; the dry run repeated | 8 of 8 PASS again | controls/b16c-dryrun-*.json |
| c18 | Redaction pass (redact_b16.py, private map) | 35 B16c files masked (139 in redaction.json in all); the B16c tools need none | redaction.json |
| c19 | Findings section, pointers, index row; scan; gates on the working tree; commit; gates at the head | `e20fd282`, every gate rc 0 | gates/b16c/ |
| c20 | RAW-ARTIFACTS.json: the 14 B16c raw files, each rehashed on disk equal to its run's record | 44 files listed | RAW-ARTIFACTS.json |
| c21 | REVIEW READY on #629 | POSTED 08:26:52 CEST (comment 6118971388); readback equal but for one trailing newline | REVIEW-READY-b16c.md, REVIEW-READY-b16c.readback.md, review-ready-b16c-url.txt |
| c22 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

### B16c bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 07:48:07 | SoC board status over key-based SSH (read only) | rc 0; McASP playback closed |
| 07:48:16-07:48:22 | Identity gate: DUT console reads, UART grader, controller staging, AECP descriptor walk, ADP | all rc 0 |
| 07:48:27-07:48:34 | Start baseline: SoC health, DUT reads, census, counters, controller, host view | all rc 0 |
| 07:48:53-07:49:03 | Tone source: passive meter read (nothing sent), then its documented state read | rc 0 |
| 07:49:29-07:49:37 | Tone start (`flock -o`; playback detached, self-ending after 7,200 s) and a passive meter read | STARTED, RUNNING; the lock free after |
| 07:50:00-07:56:15 | `bcrf`: to-host leg stopped by PID (3899); the peer's CLOCK_DOMAIN to INTERNAL (read back); the peer's CRF to the DUT's STREAM_INPUT 1 and AAF to STREAM_INPUT 0; the DUT's CLOCK_DOMAIN to 1 (read back); 300 s: both taps 40 s, the external capture, McASP0 playing lane B6's loop and recording; the DUT to 0 (read back), unbinds, the peer to 1 (read back); taps fetched and removed; loop removed; leg restarted (pid 4602) | ACTION_RC 0 |
| 07:56:52-08:03:07 | `baaf`: as `bcrf` with the DUT's source 2; leg restarted (pid 5145) | ACTION_RC 0 |
| 08:03:29-08:03:39 | Tone source: passive meter read and its documented state read | rc 0 |
| 08:03:52-08:03:56 | Tone stop by PID (command line checked) | KILLED; device closed |
| 08:04:02-08:04:09 | End baseline and controller staging removal | all rc 0 |
| 08:04:43-08:04:44 | Tap host check and SoC board status (read only) | clean |

### B16c run ledger

| Case | Window start (CEST) | Window | Result |
|---|---|---|---|
| B-CRF, `bcrf` | McASP0 07:50:56; taps 07:50:50; the DUT's set 07:50:29.8 | McASP0 300 s, taps 40 s, external 306 s | Servo LOCKED 2.66 to 3.16 s after the set, at 596 of 596 window polls. (a), (b), (c) TONE PRESENT at -14.1035 dBFS, 0.000 ppm. (c): THD+N -123.98 / -123.97 dB median (worst -123.93 / -123.90), 300 of 300 blocks at the floor, 0 discontinuities, 0.0000 ppm. (c) SAMPLE-EXACT to (a) over 1,647,859 frames and to (b) over 1,646,473. (d) 0 discontinuities, 0 net steps in 14,583,391 frames |
| B-AAF, `baaf` | McASP0 07:57:47; taps 07:57:42; the DUT's set 07:57:21.5 | as `bcrf` | Servo LOCKED 6.68 to 7.18 s after the set, at 596 of 596; AAF meter `0x001e0007` throughout the window (0 history restarts, largest deviation 30 ns). (c): THD+N -123.98 / -123.97 dB median (worst -123.92 / -123.91), 300 of 300 at the floor, 0 discontinuities, 0.0000 ppm. (c) SAMPLE-EXACT to (a) over 1,641,156 frames and to (b) over 1,644,390. (d) 0 discontinuities, 0 net steps in 14,585,924 frames |

### B16c tool changes

Every tool is lane B16b's (tools/ORIGIN-B15.sha256 pins lane B15's), unchanged and used where listed, with these B16c additions. No existing tool was edited; `run_b16.py` and `run_locked_b16.sh` keep their B16b hashes.

| Tool | Taken from | Change |
|---|---|---|
| run_b16c.py | lane B16b's run_b16.py (`424234725a20...`) | Modes `bcrf` and `baaf`: mode `b0`'s binds, captures and teardown with lanes B9 and B10's following set (run_b9.py's BCRF and BAAF): the DUT's CLOCK_DOMAIN set to 1 or 2 after the binds and read back; the ruling's exception, the peer's CLOCK_DOMAIN set to 0 before the binds and read back, refused unless the peer reads 1 with its STREAM_INPUT 8 bound to the DUT's STREAM_OUTPUT 1; teardown in the order DUT clock, unbinds, peer clock, each step on its own and restarting a controller agent that ended (added after the first dry run). Lane B9's console poll (console_poll_b8.py, unchanged) and its LOCKED wait (60 s); the window from 20 s after the set; lane B9's tone monitor and tone check; window marks (GET_COUNTERS of both CLOCK_DOMAINs and the three listeners, both GET_CLOCK_SOURCEs); the McASP playback check also before the peer's set, the binds and the DUT's set; SIGTERM runs the teardown (run_b9.py's handler) and is then ignored; the agent's stderr appended. Every other mode unchanged |
| run_locked_b16c.sh | lane B16b's run_locked_b16.sh (`8694f9b0e3c3...`) | Runs run_b16c.py; modes `bcrf` and `baaf` stop and restart the to-host leg; the deadline inside the lock (flock, then timeout) with a 100 s kill delay and the inner shell trapping SIGTERM, so the teardown and the leg's restart finish under the lock |
| tables_b16c.py | new | The findings rows rendered from the packet's summary and run files |
| dryrun_b16c/ | new | Offline stand-ins (controller agent, DUT console pty, ssh, scp, sudo, external capture) and eight scenarios with an order-and-end-state checker; never touches the bench |

Unchanged and used in B16c: identity_b16.sh, identity_b15.py, baseline_b16.sh, soc_legs_b16.sh, tone_play_b16.sh, tone_points_b16.py, align_b16.py, extcap_pair_b16.py, dloop_b16.py, b9_thdn.py, b6_tone.py, b6_thdn.py, console_read.py, console_poll_b8.py, census_cmp.py, gates_b16.py, redact_b16.py; the private mixer_read_b16.py.

### B16c deviations and decisions

- **The peer's set and restore per case.** The ruling allows the peer on INTERNAL for B-CRF and B-AAF only and asks for the restore "after grading". Each case set the peer and restored it inside its own locked action, so the peer was on INTERNAL only while a case ran (about 6 minutes each) and never between actions; the grading, offline, came after both restores.
- **The teardown order** (the DUT to INTERNAL, the DUT's unbinds, then the peer to its CRF input) is fixed so that no step has each entity following the other.
- **The window** is 300 s, as B0's, not lane B7's 630 s: one locked action must end within 10 minutes.
- **No B0 with the peer on INTERNAL.** The exception does not cover it, so Direction B's INTERNAL mismatch control stays open; published as the open question.
- **Grading after the tone stopped.** B16b's playback underran during offline grading; B16c graded only after the tone was stopped, and the tone monitor found no restart in either window.
- **The stand-ins' capture-side value** was replaced by a neutral one before the packet was finalised, and the dry run repeated.

### B16c residuals

- **The peer:** its AAF and CRF talkers counted two more stream starts and stops each; its listeners of the DUT's talkers four MEDIA_RESETs each; its CLOCK_DOMAIN LOCKED / UNLOCKED 6 / 5 to 8 / 7 (one each per restore to its CRF input).
- **DUT:** both talkers MEDIA_RESET 0 to 4; CLOCK_DOMAIN LOCKED / UNLOCKED 22 / 21 to 24 / 23; `SLIP_LB` 162 to 188 dups, every step before LOCKED; `SLIP_TDM` 0; servo IDLE; NVM seq 286 to 292, commits 52 to 58.
- **SoC board:** the to-host leg under a new pid (5145) with its recorded line; the from-host leg dead as found.
- **Tone source:** as the owner left it; nothing written.

### B16c posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118971388 (posted 08:26:52 CEST with the head and the per-run tables; REVIEW-READY-b16c.md, review-ready-b16c-url.txt; REVIEW-READY-b16c.readback.md equal but for one trailing newline).
- After it: nothing running on this host, the controller host, the tap host or the SoC board beyond its bridge leg; the bench lock free.
- TAKEN was not posted again; no existing comment was edited or deleted.

### B16c packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-b16c.md, REVIEW-READY-b16c.readback.md, review-ready-b16c-url.txt | The B16c post and its readback |
| identity-b16c/ | The identity gate at 07:48 |
| soc/b16c-precheck-status.log, soc/startc-health.log, soc/endc-health.log, soc/bcrf-legs.log, soc/baaf-legs.log | SoC board status, health and the leg stop and restart transcripts |
| runs/bcrf/, runs/baaf/, runs/bcrf-lock.txt, runs/baaf-lock.txt, runs/b16c-tone-*.txt | Each locked action's record |
| summary/bcrf/, summary/baaf/, summary/b16c-tables.md | Per-point grades, alignments, lane B9's grade at (c), the (d) decodes, the rendered tables |
| controls/b16c-dryrun-*.json, controls/b16c-wrapper-deadline.txt | The dry run's eight scenarios and the wrapper's deadline path |
| restore/*-startc*, restore/*-endc*, restore/census-compare-b16c.txt, restore/census-compare-b16b-to-b16c.txt, restore/tap-host-endc.txt | Census, counters, DUT reads, controller and host views at the B16c start and end; the tap host and board check |
| tools/run_b16c.py, tools/run_locked_b16c.sh, tools/tables_b16c.py, tools/dryrun_b16c/ | The B16c tools |
| gates/b16c/ | Gate logs and results at `e20fd282` |

## Round 2 (B16 findings round 2, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763 (the manager, after R624-1 and R625-1 on PR #725, both NEGATIVE on evidence claims, neither alleging a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428 (R624-1), https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570 (R625-1); their scripts and receipts read from the `629-b16-review-evidence` branch (fetched, read with `git show`, no checkout).
- Head at resume: `e20fd2820a9c6b9effabc529a742e732263fafa8` (git rev-parse, 08:56 CEST), as pushed for PR #725. New commit only; no rebase, no amend; TAKEN not posted again; nothing pushed.
- **No bench action:** the bench lock was never taken; no controller, board, tap or instrument was touched. Every receipt came from files already retained: the packet, the raw root and the private store.

### Round 2 state

**REVIEW READY.** Commit `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` (tree `870785667820e5cae10f060bbd48d0b524db4aeb`) on `e20fd282`, one-line subject, no body, no trailers; not pushed. Diff against `e20fd282`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+250/-86 with the index: corrections in the B16, B16b and B16c subsections, a new subsection "B16, round 2: reduced receipts", the Contents line and pointers) and the lane's row in `docs/findings/README.md`.

- **Gates at `35e332b6`:** all 14 rc 0 (gates/r2/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,179 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. On the working tree first, `docs_check.py` flagged one process phrase in a new table cell; it was reworded, and the full set then ran rc 0 on the working tree and again at the head.
- **Before the commit:** the added lines and every new packet file were scanned for every private-map entry and for the private names, addresses, capture-side values, home and temporary paths, and tool or model names: 0 hits. The post was scanned the same way.

### Round 2 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R624-1 F1 = R625-1 F3, MINOR | Conformance, Docs (R624); Conformance, Tests, Docs (R625) | Fixed. `b0-2`'s floor -123.98 / -123.95 dB (`pts3` -123.98 on both); runs 43 to 44 and 46 to 54; the recording from about 06:38:05.2, the command plus the 2 s lead, 26 s after the binds. The same 2 s lead was then found in `pts2` (McASP0 from about 06:28:31.5) and corrected too | B16b method table and window paragraph; B16b tone-source table; B16b B0; round 2 table; `r2/b0-2-receipt.json` |
| R624-1 F2 = R625-1 F4, MINOR | Conformance, Docs; Conformance, Tests, Docs | Fixed. All four of lane B6's terms stated for B-CRF and B-AAF; the timed ratio NOT RUN; the other three met; the counted ratio stands in as evidence only; no scope decision replaces the term | B16c summary rows, following record (a new four-term table), acceptance row and closing line, limits, Contents, index, PR body |
| R625-1 F1, MINOR | Conformance, Tests, Docs | Fixed. 131 is the count at (c); 23 inside the taps' 34.1 s (whole blocks 0 to 33) shown in (a) sample for sample; 108 beyond, labelled inference, including the worst block of each tone (block 224, -100.47 / -80.48 dB; inside, the worst is block 7, -100.61 / -80.63 dB) | B16b summary row, B0 paragraph, the attribution table (now with "shown directly" and "by inference only" columns), limits; B16c "Against B0" and limits; index; PR body |
| R625-1 F2, MINOR (with R624-1 S2) | Tests, Docs | Fixed by reduced receipts, bound to the raw hashes, with the extraction commands and controls. Every carried figure reproduced. Narrowed: B16b's four differing state entries (two are settings, two differ only in which messages were caught); B16's "every other output: Silent" (no reading above -135.2 dBFS); the `SLIP_LB` step times (now brackets of two polls); the private playback log named as private where it is the source | Round 2 subsection; `r2/`; `controls/r2-controls.json` |
| R624-1 R2 = R625-1 R2, RESIDUE | Docs | Fixed with the reviewers' wording; the GET_CLOCK_SOURCE sentence, the MEDIA_RESET and CLOCK_DOMAIN paragraphs also name the marks | B16c method step 7, clock-source record, following record |
| R624-1 R1 = R625-1 R1, RESIDUE | Docs | The PR title is the manager's; PR-BODY.md carries the reviewers' title | PR-BODY.md |
| R624-1 S1 = R625-1 S1, SUGGESTION | Docs | Not taken: optional, and "45 of 46 entries" is true under the census tool's definition, as both reviews say | - |

### Round 2 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| r0 | Context: the assignment; both reviews, read in full; their receipts (`audit.json` `b0_attribution_boundary`, `prior-findings-reconciled.json`, `figures.txt`); the findings page at `e20fd282`; the B6 rule (`## Method`), the design's bench rows, the register map's `0x8F8`, `0x8E0`, `0x8D4`, `0x738`, `0x748` | Read | this file |
| r1 | B0 receipt (new `tools/r2_b0_receipt.py`, packet files only) | Floor -123.98 / -123.95 dB; 131 degraded in 15 runs; overlap 1,637,452 frames (a), 1,637,980 (b), whole blocks 0 to 33; 23 inside, 108 beyond; recording 26.0 s after the binds, the lead found in `run_b16.py` | `r2/b0-2-receipt.json` |
| r2 | Self-check of every McASP0 start against its run's events and board log | `pts2` (mode `dira`) had the same 2 s lead: hw_ptr 96,020 at the recording's start; `pts1` and `pts3` (mode `dirb`) none | `runs/pts2/events.jsonl`, `runs/pts2/soc-record.log` |
| r3 | Poll receipts (new `tools/r2_poll_b16c.py`) on the two raw polls, each rehashed equal to its run's record first | Both: the published poll summary recomputed equal; LOCKED brackets 2.657 to 3.161 s and 6.68 to 7.18 s, equal to the runs'; window trim -6.125 to -6.000 ppm; CRF +10.600 to +10.652 ppm (B-CRF), AAF +10.600 to +10.631 ppm and CRF +10.586 to +10.646 ppm (B-AAF); `0x...0034`/`0x...0074` 580/16 and 584/12; `SLIP_LB` six and seven steps, five each between the binds and the set (IDLE), one and two in ACQUIRE, none after LOCKED | `r2/*-poll-receipt.json`, `r2/*-poll-trace.tsv` |
| r4 | The twelve tone-source reads copied unchanged into the raw root under `source/` (hashes equal); the private class map written | 12 files; class map `7c0f1843...` | RAW-ARTIFACTS.json (56 files) |
| r5 | Source receipt (new `tools/r2_source_b16.py`) | Comparisons 2,262/2,262/2,262/0; 2,262/1,255/1,255/4; 1,255/1,351/618/0; 1,351/1,248/668/2; meters as the page states; other outputs at most -135.2 dBFS (before setting) and -147.6 dBFS (leaving). Found: B16c step c6's "622" counted four meter addresses as entries; 618 under the page's own definition (corrected in c6) | `r2/source-receipt.json` |
| r6 | Controls of the three tools on altered copies | 6 of 6 PASS: a changed raw byte refused (rc 2); a changed published-summary field reported (rc 1); nominal byte-equal; a planted `SLIP_LB` step listed at poll 300, LOCKED, in the window; a planted setting and meter level reported; a shortened overlap moves the counts to 19 and 112 | `controls/r2-controls.json` |
| r7 | Findings page and index edited; private scan; gates on the working tree (one docs_check finding fixed); commit; gates at the head | `35e332b6`, every gate rc 0 | gates/r2/ |
| r8 | HANDOFF.md, PR-BODY.md (Round 2), REVIEW-READY-r2.md | Written | this directory |
| r9 | REVIEW READY on #629 | POSTED 09:18:59 CEST (comment 6119604288); readback equal but for one trailing newline | REVIEW-READY-r2.md, REVIEW-READY-r2.readback.md, review-ready-r2-url.txt |
| r10 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

### Round 2 tool changes

No existing tool was edited. New:

| Tool | Reads | Writes |
|---|---|---|
| tools/r2_poll_b16c.py | a raw `poll-run.jsonl` and its run's `events.jsonl` | a poll receipt (spans, extrema, `SLIP_LB` steps, the published summary recomputed) and a per-poll trace; refuses a raw file whose size or hash differs from the run's record |
| tools/r2_source_b16.py | the private class map and a private list of the twelve reads | a neutral source receipt: meters per role, settings, comparisons with classes; no control named |
| tools/r2_b0_receipt.py | packet files only | B0's receipt |

### Round 2 deviations and decisions

- **`pts2`'s start** was not in either review; found by the self-check in r2 and corrected, as the assignment asks that every figure equal its receipt.
- **The private playback log** is the only source of B16b's five underruns and of B16c's "the playback log holds none"; both statements now say the log is kept privately. The public tone monitor summary (`tone-summary` in each B16c `events.jsonl`) carries the B16c result on its own.
- **The source reads' sizes** are withheld in RAW-ARTIFACTS.json and the page, like the external capture's: they would state the source's control layout. Per-role reading counts for "every other output" are withheld for the same reason (they would state the output count).
- **S1** not taken (optional).
- **Title (R1):** the reviewers' title is put in PR-BODY.md for the manager; the PR itself is not edited.

### Round 2 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119604288 (posted 09:18:59 CEST with the head, the dispositions and the per-run tables; REVIEW-READY-r2.md, review-ready-r2-url.txt; REVIEW-READY-r2.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 2 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r2.md, REVIEW-READY-r2.readback.md, review-ready-r2-url.txt | The round 2 post and its readback |
| r2/b0-2-receipt.json | B0's figures from packet files: floor, runs, overlap, inside and beyond, timing |
| r2/bcrf-poll-receipt.json, r2/baaf-poll-receipt.json, r2/bcrf-poll-trace.tsv, r2/baaf-poll-trace.tsv | The console-poll receipts and traces |
| r2/source-receipt.json | The tone source's neutral receipt |
| tools/r2_poll_b16c.py, tools/r2_source_b16.py, tools/r2_b0_receipt.py | The extraction tools |
| controls/r2-controls.json | Their controls, 6 of 6 PASS |
| gates/r2/ | Gate logs and results at `35e332b6` |
| RAW-ARTIFACTS.json | Now 56 files: the twelve tone-source reads added under `source/` |

## Round 3 (B16 findings round 3, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508 (the manager, after R624-2 and R625-2 on PR #725, both NEGATIVE on figure-versus-receipt slips, neither alleging a DUT defect or reversing a bench verdict). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119878041 (R624-2), https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119899949 (R625-2). Their scripts and receipts came from the `629-b16-review-evidence` branch at `dc31ee09` (fetched, extracted with `git archive` into a scratch directory, no checkout); two of R624-2's scripts, read in full first, were run with `-I` as a cross-check.
- Head at resume: `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` (git rev-parse, 09:41 CEST), as pushed for PR #725. New commit only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** the bench lock was never taken; no controller, board, tap or instrument was touched. Beyond the packet, the only retained files read were the two playback logs in the private store, copied unchanged into the raw root under `playback/`.

### Round 3 state

**REVIEW READY.** Commit `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` (tree `dd6c3f3cb7bc5059aa9e976a9131a4e19212d103`) on `35e332b6`, one-line subject, no body, no trailers; not pushed. Diff against `35e332b6`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md` (192 insertions, 65 deletions): the corrections in the B16, B16b, B16c and round 2 subsections, a new subsection "B16, round 3: figures check", and the introduction, Contents and index pointers.

- **The figures check at `0782c55f`:** `python3 -I tools/check_b16_figures.py <page> . r3/figures-rows.tsv r3/figures-coverage.tsv` rc 0: 1,610 rows, all equal to their receipts; 1,815 tokens in 1,312 covered lines, 205 in identifier categories, 0 uncovered. Re-run byte-equal at the head.
- **Its controls:** `python3 -I tools/r3_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r3-controls.json` rc 0, 5 of 5 PASS; re-run byte-equal at the head.
- **Its rows reproduce:** `python3 -I tools/r3_figures_build.py <page> tools/r3_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py`.
- **Gates at `0782c55f`:** all 14 rc 0 (gates/r3/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,306 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. On the working tree first, `docs_check.py` flagged one bare reference to the findings index; it became a link, and the full set then ran rc 0 on the working tree and again at the head.
- **Before the commit:** the added lines and every new packet file were scanned for every private-map entry, every private environment value, the private names, addresses, capture-side values, home and temporary paths, and tool or model names: 0 hits. The post and this file were scanned the same way.

### Round 3 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| Assignment item 1: a figures check | - | Done: `tools/check_b16_figures.py`, its output as the receipt, its controls 5 of 5. It covers lane B16's section, the page's introduction and Contents entry on lane B16, and lane B16's part of the index row; the PR body's figures were checked against its rows by hand (every number there is one of its figures, an identifier, or the check's or gates' own totals) | round 3 subsection; `r3/`; `controls/r3-controls.json` |
| R625-2-F1, MINOR | Conformance, Tests, Docs | Fixed with the exact replacement | B16c attribution |
| R624-2-F1, MINOR | Robustness, Tests, Docs | Fixed: every count is over blocks wholly inside the playback (303 of 303; `pts2` 11 of 13, blocks 6 and 12 the repeats), the silent and start blocks named; the `pts2` taps' "every block but the first and last" narrowed the same way (15 of 15) | B16b point (d) table and taps paragraph, B0 attribution, B16c point (d) table and attribution |
| R624-2-F2, MINOR | Tests, Docs | Fixed: each bracket from the start of the last poll that read ACQUIRE to the end of the first that read LOCKED, at the trace's ms precision (2.585 to 3.161 s, 6.602 to 7.180 s), and the rule stated; the `SLIP_LB` brackets already used it | B16c summary rows, following record, lane B6's term table, round 2 paragraph, index row, PR body |
| R624-2-R1, RESIDUE | Docs | Fixed with the exact text | B16b tone source; B16c "Against B0" |
| R624-2-R2, RESIDUE | Docs | Fixed with the exact text | B16c `SLIP_LB` paragraph |
| R624-2-R3, RESIDUE | Docs | Fixed with the exact text | PR-BODY.md, "#629" |
| R624-2-S1, SUGGESTION | Docs | Taken: the bit 4 limit, checked against both traces (set at every ACQUIRE and LOCKED poll, clear at IDLE) | B16c limits |
| R624-2-S2 = R625-2-S1, SUGGESTION | Docs | Not taken: optional, and "45 of 46 entries" is true under the census tool's definition | - |

The check's own findings, each corrected and listed in the round 3 subsection's second table: clock times under one rule (cut to the last digit shown), lane B16's tone start (05:55:38 to 05:55:37, from the first status read less the frames played), `loop2`'s "remaining 49 s" (49.6 s), the drift (+3.00 and +3.01 frames) and offset (+6.94 to +6.96 ppm) before the tone source's change, B16c's decoded span at (d) (303.8 s and 303.9 s) and the peer's rate (+10.59 to +10.65 ppm). Narrowed or cited where no retained receipt exists: the resume times (now the first bench action, 06:22:23 and 07:48:07), lane B15's `pts1` flags (now what lane B15's section records), lane B16b's underruns (now cited to step b17 of this file: that log was overwritten when lane B16c started the playback; "0.43 to 1.63 s each" removed, as nothing records it), and six number words.

### Round 3 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| s0 | Context: the assignment; both reviews in full; their scripts and receipts (`d_floor_blocks.py`, `locked-bracket.txt`, `receipt-audit.json`, `audit_receipts.py`, `check_point_tables.py`); the findings page at `35e332b6`; `console_poll_b8.py` (the read order) and `r2_poll_b16c.py`; the register map's `0x8F8` and `0x8E0` | Read | this file |
| s1 | Items 2 to 5 and R3 on the page and in PR-BODY.md, with the reviewers' exact texts | Done | the page |
| s2 | The check written: rows by anchor and generator (the authoring aids `tools/r3_figures_spec.py`, `tools/r3_figures_build.py`), keys over the packet's receipts, decimals rounded half up, coverage by tokenising every number and number word | 1,610 rows | `tools/check_b16_figures.py` |
| s3 | Every mismatch and uncovered figure the check found, corrected on the page or narrowed; one rule for clock times chosen (truncation: no more changes than rounding, about 15 each, and the clock convention) | 0 mismatches, 0 uncovered | round 3 subsection |
| s4 | The playback logs: lane B16's and lane B16c's retained logs copied unchanged into the raw root under `playback/` and listed in RAW-ARTIFACTS.json (58 files); a neutral receipt written | 0 underrun lines in each; lane B16b's log not retained | `r3/playback-logs.json`, `tools/r3_playback_logs.py` |
| s5 | The check's controls on altered copies | 5 of 5 PASS | `controls/r3-controls.json`, `tools/r3_check_controls.py` |
| s6 | Two of R624-2's scripts on the corrected page and packet | `check_point_tables.py` 19 of 20, the one flag `pts3`'s stored 122.475 dB SNR, which binary-float formatting shows as 122.47 and the page, by the stated half-up rule, as 122.48; `d_floor_blocks.py` the counts the page now gives | - |
| s7 | Gates on the working tree (one docs_check finding fixed), privacy scan, commit, gates at the head | `0782c55f`, every gate rc 0 | gates/r3/ |
| s8 | The check, its controls and the row builder re-run at the head | Byte-equal | `r3/`, `controls/r3-controls.json` |
| s9 | HANDOFF.md, PR-BODY.md (Round 3), REVIEW-READY-r3.md | Written | this directory |
| s10 | REVIEW READY on #629 | POSTED 10:43:55 CEST (comment 6120810912); readback equal but for one trailing newline | REVIEW-READY-r3.md, REVIEW-READY-r3.readback.md, review-ready-r3-url.txt |
| s11 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

### Round 3 tool changes

No existing tool was edited. New:

| Tool | Bytes | SHA-256 | What |
|---|---|---|---|
| tools/check_b16_figures.py | 179,675 | `13d7a0deb20ca5b16c478491c1499de37864693545a70d0c876ef7e9288d1ea3` | The figures check: one row per quoted figure, recomputed from its receipt; coverage of every token |
| tools/r3_check_controls.py | 6,541 | `85fc57876334b823cd349a9752bf12581bbb22f9f5c5b2a4d6f68ab948a54157` | Its five controls on altered copies |
| tools/r3_playback_logs.py | 1,990 | `27334c6d3106f9305187deef6196a7dcb7e14b10d6fbea08f721029766dcf595` | The neutral receipt of the retained playback logs |
| tools/r3_figures_build.py | 3,736 | `ec0e1ce6baa09891204687d097f7bca54f9a58f7d781a12a4cc488023b1e5519` | Authoring aid: writes the check's rows from the spec |
| tools/r3_figures_spec.py | 141,228 | `6338e6fd1a63ccd0d9022942863e491c942dc66d08a6194d9539a9ced54b57fa` | Authoring aid: the rows by anchor, and the table generators |

The check's SHA-256 and its outputs' are not on the findings page: the check holds the page's figures, so the page cannot hold the check's hash. They are here, in PR-BODY.md, in the post and in MANIFEST.sha256.

### Round 3 deviations and decisions

- **Scope beyond the section.** The assignment names lane B16's findings section. R624-2-F2 also named the index row and the PR body, so the check covers the page's introduction and Contents entry on lane B16 and lane B16's part of the index row too. The PR body is outside the tree; its numbers were compared with the check's rows by hand.
- **One rule for clock times.** The page mixed rounding and truncation. Truncation was chosen: it is how a clock shows time, and it needed no more changes than rounding. Numbers stay rounded half up on exact decimals, the rule that makes `pts3`'s stored 122.475 show as 122.48.
- **The check's hash off the page**, for the reason above.
- **No nominal control in the controls file.** A control comparing the check's output with the packet's would depend on the controls file the page cites, and would never settle. The committed page's pass is the check's own output, re-run byte-equal.
- **Lane B16b's underruns** have no retained log: lane B16c's start overwrote it. Their count and times now cite this file's step b17, and "0.43 to 1.63 s each", which nothing retained records, is removed.
- **The authoring aids** are in the packet so a reviewer can see how each row's key was chosen and regenerate the rows; the check does not import them.

### Round 3 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6120810912 (posted 10:43:55 CEST with the head, the dispositions, the check's results and the per-run tables; REVIEW-READY-r3.md, review-ready-r3-url.txt; REVIEW-READY-r3.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 3 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r3.md, REVIEW-READY-r3.readback.md, review-ready-r3-url.txt | The round 3 post and its readback |
| tools/check_b16_figures.py, tools/r3_check_controls.py, tools/r3_playback_logs.py, tools/r3_figures_build.py, tools/r3_figures_spec.py | The round's tools |
| r3/figures-rows.tsv, r3/figures-coverage.tsv | The check's output: its receipt |
| r3/playback-logs.json | The playback logs' neutral receipt |
| controls/r3-controls.json | The check's controls, 5 of 5 PASS |
| gates/r3/ | Gate logs and results at `0782c55f` |
| RAW-ARTIFACTS.json | Now 58 files: the two playback logs added under `playback/` |

