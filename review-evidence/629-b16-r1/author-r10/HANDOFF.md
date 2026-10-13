# [A603] Bench lane B16 handoff

Refs #629: Direction B's known tone after the maintainer's loopback result. Reproduce the reference peer's own loopback (its listener bound to its own talker) as the positive reference, locate the step where lane B15's setup differs, then grade Direction B end to end; dev `5603c353` bench image as flashed and booted.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117358154 (posted 05:44 CEST; TAKEN.md, taken-url.txt)
- STOP: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117604151 (posted 06:11 CEST with the head and the per-run tables; STOP.md, stop-url.txt; STOP.readback.md equal but for one trailing newline). TAKEN.readback.md likewise
- Initial cycle posted TAKEN and STOP; subsequent round posts are recorded below. No existing comment was edited or deleted.
- Branch: `629-b16-tone` from dev `c20c85bd`, lane worktree on the physical /data path.
- Packet: this directory. Raw files (pcaps, recordings) stay outside it on the bench host (RAW-ARTIFACTS.json); private endpoints, the redaction map, the unmasked originals, the tone's loop and playback log, the tone source's state reads and meter rows, the external capture's all-channel rows and the private mixer read tool stay in the private directory (not in the packet).

## State

**Current: Round 10, documents only, local head `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, not pushed. All required gates pass; 117/117 standing controls, 172/172 self-probes and all review-probe outcomes verified. REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6135221777. No bench action or lock acquisition. See Round 10 below.**

**Round 8 (B16 findings round 8, documents only): REVIEW READY, posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132021882; see "Round 8" at the end of this file; head `b522bb923fa59581478460b61633bce2cb90ac1d`. No bench action. The earlier records stand as written; the section's fenced code block is now a list of code spans on the same lines, and two earlier control expectations change under the parser (listed there, for the manager's decision).**

**Round 7 (B16 findings round 7, documents only): REVIEW READY, posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6129482994; see "Round 7" at the end of this file; head `295ba9d7f7dfed65e95002478ed6d55ccc14e580`. No bench action. The earlier records stand as written; the section's table markers are now blank lines and one code block's placeholders are in braces (listed there).**

**Round 6 (B16 findings round 6, documents only): REVIEW READY, posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6127756184; see "Round 6" at the end of this file; head `e91a62ee266e182a804ca1f45a0f18f715096563`. No bench action. The earlier records stand as written; the covered text was reworded within its lines where the closed list refused an identifier's follower (listed there), and the three acceptance headings now read "acceptance of #629".**

**Round 5 (B16 findings round 5, documents only): REVIEW READY, posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126360842; head `3619019350936d5af851933df0b5444ef8387e69`. No bench action. See "Round 5" at the end of this file. The earlier records stand as written; the page's round 3 and round 4 paragraphs now describe those checks as they were.**

**Round 4 (B16 findings round 4, documents only): REVIEW READY, posted as https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6121671136; head `61ae86419c50f2707d6ee1dc5433bc6dee66ce84`. No bench action. See "Round 4" at the end of this file. The earlier records stand as written; the page's census counts are now stated as reads (R625-3-S1, taken), and seventeen phrases were reworded (listed there).**

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

## Round 4 (B16 findings round 4, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6121193402 (the manager, after R624-3 and R625-3 on PR #725, each NEGATIVE on one MINOR, neither alleging a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121093801 (R624-3, Docs: the packet's location), https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121186527 (R625-3, Conformance, Robustness, Tests, Docs: figures inside quoted phrases and link labels escaped the check). R625-3's probe, `scripts/probe_figure_coverage.py`, came from the `629-b16-review-evidence` branch at `bfb17c2e` (fetched; extracted with `git show` into its own scratch directory, read in full, run with `-I`, no checkout).
- Head at resume: `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` (git rev-parse, 11:10 CEST), as pushed for PR #725. New commit only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** the bench lock was never taken; no controller, board, tap or instrument was touched. Nothing private was read: the round read only the repository (including the evidence branch's objects) and this packet.

### Round 4 state

**REVIEW READY.** Commit `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` (tree `ed284e802555e2e1cb92f15d95dafa2702d3fc1d`) on `0782c55f`, one-line subject, no body, no trailers; not pushed. Diff against `0782c55f`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md` (172 insertions, 51 deletions): a "Where the packet is" paragraph in "B16: artifact hashes", the pointer at the section's start, the round 3 coverage paragraph made true of round 3's check, a new subsection "B16, round 4: packet and coverage", the census stated as reads, seventeen rewordings, and the introduction, Contents and index pointers.

- **The figures check at `61ae8641`:** `python3 -I tools/check_b16_figures.py <page> . r4/figures-rows.tsv r4/figures-coverage.tsv` rc 0: 1,727 rows, all equal to their receipts; 1,874 tokens in 1,433 covered lines, 147 in identifier categories, 0 uncovered, 0 uncovered measurements (`r4/figures-check.stdout`). Re-run byte-equal at the head, and again after this file was written (the check reads it for two rows).
- **Its rows reproduce:** `python3 -I tools/r4_figures_build.py <page> tools/r4_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py`.
- **Its controls:** `python3 -I tools/r4_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r4-controls.json` rc 0, 8 of 8 PASS: round 3's five (code unchanged) and three new (quoted, linked, planted category). Round 3's runner, unchanged, against the new check: `controls/r4-rerun-r3-controls.json`, 5 of 5 PASS. Both re-run byte-equal at the head.
- **The new controls fail on round 3's check:** the same runner against `author-r3/tools/check_b16_figures.py` (`13d7a0de...`) and the page and index at `0782c55f`, exported into a plain scratch tree: round 3's five PASS, the three new FAIL, each with the figure not named (`controls/r4-controls-on-r3-check.json`). So each new control can fail for the defect it targets.
- **R625-3's probe, unchanged, against the new check:** 7 of 7 detected, rc 0, including its quoted and linked forms (`r4/r625-3-probe-rerun.json`, its own results file kept verbatim under `results`).
- **The packet's location:** `python3 -I tools/r4_evidence_receipt.py <repo> b84584e4 0782c55f r4/evidence-receipt.json` rc 0, re-run byte-equal at the head. The manifest at `b84584e4`, SHA-256 `8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034`, 1,680 entries (author-r1 471, author-r2 499, author-r3 526, reviews 184); path-redacted 1, 9, 17 and 4; the hashes differ exactly where the flag is set. All 66 packet-file hash rows of lane B16's section at `0782c55f` equal the original hash, the published hash and the published blob in `author-r3/`, by size and SHA-256; none is path-redacted.
- **Gates at `61ae8641`:** all 14 rc 0 (gates/r4/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,427 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree first.
- **Before the commit:** the added lines and every new packet file were scanned for the private names, hosts, interfaces, addresses, capture-side values, home and temporary paths, and tool or model names: 0 hits. The post and this file were scanned the same way.

### Round 4 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R624-3-F1, MINOR | Docs | Fixed: "Where the packet is" gives the branch, the pinned commit `b84584e4ccb069248909f0fdeb7f8b72a1c41ae4`, each round's directory with the page commit its archive subject names, the manifest's SHA-256 and entry count, its two hashes and flag per file, the path-redacted counts per round and what they are, and that all 66 packet-file rows equal both hashes and the published file. Every new token is claimed by a row reading `r4/evidence-receipt.json`. The published round-1 directory is `author-r1/`, not `author/` as the assignment and R624-3 wrote; the page states the real name | B16: artifact hashes; `r4/evidence-receipt.json`; `tools/r4_evidence_receipt.py` |
| R625-3-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed: the whole-link and whole-quote categories removed, and with them every category that was not an identifier (tone name, unit, heading, pronoun, idiom, phrase, bench rule, linked ruling's date, method name and the like). What remains: commit names (listed), clause numbers, descriptor, channel, step, round and list-item indices after their keywords, the packet's label and branch name, and a link's target. The tokens those categories covered now have rows (tone frequencies, block length, bit width, frame step, the one-LSB floor, the lane's limit on a locked action, the four capture points, dates in link labels, the quoted reworded phrases) or were reworded (seventeen phrases that state no figure). A measurement guard: a token followed by a unit can only be claimed by a row. Tokens now include 40-character commit names and the number words for tens. Controls for both of R625-3's forms, plus the planted-category guard control | round 4 subsection; `tools/check_b16_figures.py`; `controls/r4-controls.json` |
| R625-3-S1, SUGGESTION (= R624-1-S1, R625-1-S1, R624-2-S2, R625-2-S1) | Docs | Taken: "44 of 45 reads equal, the census's start record aside" in the five census statements of lane B16's section; each row recomputes both counts from the two census files with `census_cmp.py`'s rule and checks them against the comparison file's counts less the start record | B16, B16b and B16c bench-as-left tables; both identity-gate-again rows |

### Round 4 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| t0 | Context: the round 4 assignment; R624-3 and R625-3 in full; R625-3's probe; the evidence branch fetched (`bfb17c2e`), its manifests at `b84584e4` and `bfb17c2e` read | Read | this file |
| t1 | The evidence receipt: manifest, archive subjects, published blobs of every packet-file row at `0782c55f` | rc 0; 66 of 66 rows equal | `r4/evidence-receipt.json` |
| t2 | The page: "Where the packet is", the pointer, the round 3 paragraph, the round 4 subsection, the census as reads, the rewordings, the introduction, Contents and index | Done | the page |
| t3 | The check: tokens (40-character commits, tens), identifier-only categories, the measurement guard, new helpers; the spec and builder as round 4 copies with GEN3 for the tone frequencies | 1,727 rows, 0 uncovered | `tools/check_b16_figures.py`, `tools/r4_figures_spec.py`, `tools/r4_figures_build.py` |
| t4 | The controls, round 4 runner and round 3 runner | 8 of 8, 5 of 5 | `controls/r4-controls.json`, `controls/r4-rerun-r3-controls.json` |
| t5 | R625-3's probe against the new check (working tree) | 7 of 7 detected | - |
| t6 | Gates on the working tree, privacy scan, commit, gates at the head | `61ae8641`, every gate rc 0 | gates/r4/ |
| t7 | The check, builder, receipt and both controls runners re-run at the head | Byte-equal | `r4/`, `controls/` |
| t8 | The round 4 controls against round 3's check and page | Round 3's five PASS, the new three FAIL | `controls/r4-controls-on-r3-check.json` |
| t9 | R625-3's probe at the head | 7 of 7 detected, rc 0 | `r4/r625-3-probe-rerun.json` |
| t10 | HANDOFF.md, PR-BODY.md (Round 4), REVIEW-READY-r4.md | Written | this directory |
| t11 | REVIEW READY on #629 | POSTED 11:39:42 CEST (comment 6121671136); readback equal but for one trailing newline | REVIEW-READY-r4.md, REVIEW-READY-r4.readback.md, review-ready-r4-url.txt |
| t12 | The check re-run after this file's last edit (it reads this file for two rows); manifest | Byte-equal; MANIFEST.sha256 over every packet file but itself | `r4/`, MANIFEST.sha256 |

### Round 4 tool changes

| Tool | Bytes | SHA-256 | Change |
|---|---|---|---|
| tools/check_b16_figures.py | 192,835 | `d2b51f85b10f33427396044703f20820df64b7b57601fe25f498a44e28f17edd` | Edited from round 3's (`13d7a0de...`, published at `b84584e4`): docstring; TENS and a 40-character commit alternative in TOKEN; MEASURE and the guard in the coverage loop; standard output names a guarded token as a measurement; helpers `tone_hz`, `points`, `cmp_bits`, `blk_grade`, `blk_points`, `step_frames`, `lock_limit`, `census_reads`; ROWS_TSV and EXCLUDE regenerated from the round 4 spec |
| tools/r4_figures_spec.py | 152,849 | `ee2fef18f24849f255f90743bfa8375dda42855a8ca00297a5f3f45a6729c18d` | New, a copy of `r3_figures_spec.py`: X identifier-only; anchors moved with the text; census rows on `census_reads`; round 3's row for the R624-2-R2 cell's number word replaced by the exact phrase at `0782c55f`; round 4 rows; GEN3 |
| tools/r4_figures_build.py | 4,673 | `ba3085a75a99d17009fda6580adf90887db21c8c64f50144ce8d6fd173688de0` | New, a copy of `r3_figures_build.py`: a row may give its occurrence index; GEN3 hook; TENS for the token regex |
| tools/r4_check_controls.py | 10,379 | `54d2e1df507cb1b8c8b77214942f49cfcbe3a524f4e52b882ae124384e6d4e0f` | New, a copy of `r3_check_controls.py`: the five controls' code unchanged, each recorded with `from`; `run_out`; three round 4 controls |
| tools/r4_evidence_receipt.py | 5,191 | `7dca8a53f24c1e7330ed2e154e41f4e30a47012171d68c2a80c138c2834c6164` | New: the published packet's location from the repository's object store |

`r3_figures_spec.py`, `r3_figures_build.py` and `r3_check_controls.py` are unchanged; the first two reproduce round 3's check, published as `author-r3/tools/check_b16_figures.py` at `b84584e4`, not the one now in `tools/`.

The check's SHA-256 and its outputs' are not on the findings page, for round 3's reason. They are here, in PR-BODY.md, in the post and in MANIFEST.sha256.

### Round 4 deviations and decisions

- **"Exemptions cover only demonstrable identifiers."** Read strictly: every category that was not an identifier was removed, not only the two R625-3 named. Descriptor, channel, step, round and list-item indices are kept as identifiers, each bound to its keyword; register-address and bit-index categories, which covered nothing, were removed.
- **Rows or rewording.** A token that states a figure got a row reading a packet file. A number word that states none (a pronoun, an idiom, a count of the cases a sentence names, the bench's single DUT and peer in the limits) was reworded rather than given a contrived receipt; the seventeen phrases are quoted on the page, each quoted word with a row finding it on the page before its rewording.
- **The lane's limit on a locked action** has no tool constant: the wrappers take the deadline as an argument and the runs do not record it. Its row reads this file's own statement of the rule (the B16b and B16c deviation entries), as the underruns cite step b17. The 10-minute rule is the operator's working limit, not a figure of the public assignment.
- **The ruling dates** were dropped from the text: no packet file records a ruling's date, and the section's heading carries it.
- **"Where the packet is" pins `b84584e4`,** the round 3 archive, whose manifest covers `author-r1/` to `author-r3/`. Round 4's directory does not exist yet; the page says it follows on the same branch.
- **The probe re-run and the negative run** are in the packet, not on the page: each records the check's counts on altered copies of the page, so a hash of either on the page would chase itself.

### Round 4 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6121671136 (posted 11:39:42 CEST with the head, the dispositions, the check's results, the file hashes and the per-run tables; REVIEW-READY-r4.md, review-ready-r4-url.txt; REVIEW-READY-r4.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 4 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r4.md, REVIEW-READY-r4.readback.md, review-ready-r4-url.txt | The round 4 post and its readback |
| tools/r4_figures_spec.py, tools/r4_figures_build.py, tools/r4_check_controls.py, tools/r4_evidence_receipt.py | The round's new tools; tools/check_b16_figures.py edited |
| r4/figures-rows.tsv, r4/figures-coverage.tsv, r4/figures-check.stdout | The check's output at the head: its receipt |
| r4/evidence-receipt.json | Where the packet is published, reduced from the evidence branch |
| r4/r625-3-probe-rerun.json | R625-3's probe against the new check |
| controls/r4-controls.json, controls/r4-rerun-r3-controls.json, controls/r4-controls-on-r3-check.json | The check's controls: round 4's runner, round 3's runner, and round 4's runner on round 3's check |
| gates/r4/ | Gate logs and results at `61ae8641` |

## Round 5 (B16 findings round 5, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6125608002 (the manager, after R624-4 and R625-4 on PR #725, each NEGATIVE on one MINOR about the figures check passing a number its token pattern does not read; neither alleges a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125594896 (R624-4), https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125596576 (R625-4). Their probes came from the `629-b16-review-evidence` branch at `9cae35ed` (fetched; extracted with `git show` into a scratch directory, read in full, run with `-I`, no checkout): R624-4's `tools/probe_escape_forms.py` (`5c2dbc69...`) and `tools/untokenized_digits.py` (read, with its receipts), R625-4's `probe_coverage.py` (`e8749cbe...`) and its copy of R625-3's `probe_figure_coverage.py` (`f4c4d91b...`, equal to the one round 4 ran).
- Head at resume: `61ae86419c50f2707d6ee1dc5433bc6dee66ce84` (git rev-parse, 15:50 CEST), as pushed for PR #725. New commits only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** no controller, board, tap or instrument was touched. The bench lock was taken once, after the post, by a non-blocking `flock -n` running only `true`, to confirm it was free; it was released at once. Nothing private was read but this lane's own private redaction map and environment file, for the privacy scan.

### Round 5 state

**REVIEW READY.** Two commits on `61ae8641`, each a one-line subject, no body, no trailers; not pushed:

- `f60132ca63ee74d34b6994ee189b2e87e85091ef`: the subsection "B16, round 5: every digit"; the round 3 and round 4 paragraphs made true of those checks; the section's opening paragraph pointing to rounds 2 to 5 (R624-4-S1); the introduction, Contents and index pointers.
- `3619019350936d5af851933df0b5444ef8387e69` (tree `11777358b03b38ceda5ade1e1ed59e31b08473e5`): the page's statement of what may stand between a number and its unit, made complete (a soft or non-breaking hyphen, a backslash) and given the quoted-mention rule the check applies. Found while writing PR-BODY.md, after the first commit.

Diff against `61ae8641`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md`. No figure on the page changed.

- **The figures check at `36190193`:** `python3 -I tools/check_b16_figures.py <page> . r5/figures-rows.tsv r5/figures-coverage.tsv` rc 0: 1,749 rows, all equal to their receipts; 1,919 tokens in 1,571 covered lines; 13,209 digits, 11,037 in claimed figures, 2,172 in 1,098 bound identifiers, 0 uncovered (`r5/figures-check.stdout`). Re-run byte-equal at the head, and again after this file was written (the check reads it for two rows).
- **Its rows reproduce:** `python3 -I tools/r5_figures_build.py <page> tools/r5_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py`.
- **Its controls:** `python3 -I tools/r5_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r5-controls.json` rc 0, 22 of 22 PASS: rounds 3 and 4's eight (code unchanged) and fourteen new. Round 3's runner and round 4's, unchanged, against the new check: 5 of 5 and 8 of 8 (`controls/r5-rerun-r3-controls.json`, `controls/r5-rerun-r4-controls.json`). All three re-run byte-equal at the head.
- **The new controls on round 4's check:** the same runner against the published `author-r4/tools/check_b16_figures.py` (`d2b51f85...`, equal to this packet's round 4 check) and the page at `61ae8641`, exported with `git archive` into a scratch tree, with `GIT_DIR` set to the lane's repository so its `git:` rows read (round 4's check passes that page there, rc 0): the eight earlier PASS; eleven new FAIL, three new PASS (a non-breaking space, a hyphen, the planted category: forms round 4's guard already read) (`controls/r5-controls-on-r4-check.json`).
- **The reviews' probes, unchanged:** `python3 -I tools/r5_probe_reruns.py <repo> . tools/review-probes <scratch> <head>` rc 0: R624-4's 8 of 8, R625-4's 12 of 12 (its own exit 0) and R625-3's 7 of 7 detected; each probe refused unless its SHA-256 equals the published one; each probe's own results file kept verbatim (`r5/*-probe-rerun.json`).
- **Further forms:** `python3 -I tools/r5_self_probes.py tools/check_b16_figures.py <page> . <scratch> r5/self-probes.json` rc 0, 36 of 36 detected. Two of its first runs missed: a line-break form (the probe looked for its figure on the wrong line; fixed in the probe) and a line inside a paragraph starting `7. ` (a real escape: the list-item category now requires a real ordered list).
- **Gates at `36190193`:** all 14 rc 0 (gates/r5/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,565 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before each commit, and at `f60132ca` (3,562 added lines).
- **Before each commit:** the added lines and every new packet file were scanned for the private map's values, the private environment's values, the private names, hosts, interfaces, addresses, capture-side values, home and temporary paths, and tool or model names: 0 hits (one false match: the common word "regex", a field name of the private map, which round 4's published check already contains). The post, PR-BODY.md and this file were scanned the same way.

### Round 5 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R624-4-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed by construction: coverage is decided per digit, not per token. Every digit (any Unicode digit or numeral) must lie in a figure a row claims or in an identifier a category binds to its keyword in the same sentence; anything else is UNCOVERED in its spelling. A spelling the token pattern does not read (`26s`, `10dB`, `300ms`, `.5 ppm`) can never be claimed, so it always fails. Controls for each form; R624-4's probe 8 of 8 | round 5 subsection; `tools/check_b16_figures.py`; `controls/r5-controls.json`; `r5/r624-4-probe-rerun.json` |
| R625-4-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed: `-.25 ppm` and `7e2 ppm` as above; a number before a unit is a measurement whatever stands between (any whitespace run, line breaks, hyphens, marks, quotes, brackets, HTML entities, tags and comments), so `CLOCK_DOMAIN 7  ppm` fails; the line-start continuation category is gone, and channel indices bind to their keyword across a line break, so R625-4's unbound continuation fails. Controls for each; R625-4's probe 12 of 12 | the same; `r5/r625-4-probe-rerun.json` |
| R624-4-S1, SUGGESTION | Docs | Taken: the section's opening paragraph points to rounds 2 to 5. Not kept on one source line, as the check's rows are regenerated by anchor | B16: opening paragraph |

R624-4's verification asks for `untokenized_digits.py` adapted to the corrected pattern: the token pattern is unchanged, and the check itself now accounts for every digit outside a token (2,172 in bound identifiers, 0 uncovered); `r5/figures-coverage.tsv` lists each identifier with its category and line.

### Round 5 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| u0 | Context: the round 5 assignment; R624-4 and R625-4 in full; their probes and R624-4's untokenized-digit receipts from the evidence branch at `9cae35ed`; the round 4 check | Read | this file |
| u1 | The per-digit engine in a scratch copy of the check: blocks, a number lexer (sign, leading point, exponent, Unicode digits), the separator set, the categories read over blocks with their tests | Unchanged page: 0 uncovered after three fixes (unit `read` made `reads`; fenced code read as code; anchors as addresses) | - |
| u2 | R624-4's and R625-4's probes against the scratch check | 8 of 8, 12 of 12 | - |
| u3 | The check's size: 201 KB with round 5's code; the rows table now writes a receipt equal to the row above's as `^` | 180 KB | `tools/r5_figures_build.py` |
| u4 | The page: round 5 subsection, round 3 and 4 paragraphs, opening paragraph, introduction, Contents, index; four number words reworded before the first commit | Done | the page |
| u5 | The spec and the controls runner; one control of round 4 (the quoted `"37" blocks`) failed under the new separator set; the quoted-mention rule restored it with its code unchanged | 22 of 22 | `tools/r5_figures_spec.py`, `tools/r5_check_controls.py` |
| u6 | The hash table filled and the controls re-run until byte-stable | Stable | `controls/` |
| u7 | Further forms; the list-item escape found and closed | 36 of 36 | `tools/r5_self_probes.py`, `r5/self-probes.json` |
| u8 | Gates on the working tree, privacy scan, commit `f60132ca`, gates at the head | Every gate rc 0 | gates/r5/ (overwritten at u10) |
| u9 | The page's separator statement completed and the quoted-mention rule stated; the check's docstring the same; commit `36190193` | Done | the page |
| u10 | At `36190193`: gates, the check, the build, the three runners, the round 4 run, the probes, the further forms | All as stated above; every controls file byte-equal | gates/r5/, `r5/`, `controls/` |
| u11 | HANDOFF.md, PR-BODY.md (Round 5, and the round 3 and 4 claims about the check), REVIEW-READY-r5.md | Written | this directory |
| u12 | REVIEW READY on #629 | POSTED 16:32:10 CEST (comment 6126360842); readback equal but for one trailing newline | REVIEW-READY-r5.md, REVIEW-READY-r5.readback.md, review-ready-r5-url.txt |
| u13 | The check re-run after this file's last edit; manifest | Byte-equal; MANIFEST.sha256 over every packet file but itself | `r5/`, MANIFEST.sha256 |

### Round 5 tool changes

| Tool | Bytes | SHA-256 | Change |
|---|---|---|---|
| tools/check_b16_figures.py | 180,489 | `2641412c62d2c55c800b96dde53eecbd3983ec7d251dbab58eeda90312d73814` | Edited from round 4's (`d2b51f85...`, published as `author-r4/`): docstring; `parse_rows` reads `^`; a row's figure must be the whole number written there; the coverage section rewritten per digit: `NUM`, `SEP`, `MEASURE` (separators widened, units in either case), `ZERO`, `measured` (the quoted-mention rule), `X` with a test and an address flag, `packet_path`, `in_code`, `list_item`, `on_page`, `blocks`; the summary line adds the digit counts; ROWS_TSV and EXCLUDE regenerated from the round 5 spec. TOKEN unchanged |
| tools/r5_figures_spec.py | 155,187 | `725dbe2c0d40bce8de478b3a64300d7387bb643dad78d77b1ec09d7883dd8565` | New, a copy of `r4_figures_spec.py`: X with round 5's categories; rows for round 5's counts |
| tools/r5_figures_build.py | 4,767 | `b7d95befe349e1f15ea4cc3ef027afd3e78ece53a80a347d7a86e4d0509af0e6` | New, a copy of `r4_figures_build.py`: the `^` encoding |
| tools/r5_check_controls.py | 16,186 | `bf84a387ebdaae6fee5dc93f9da5b9b06bcb827281ff1c51eac3b7da17a8aa2e` | New, a copy of `r4_check_controls.py`: the eight controls' code unchanged; fourteen round 5 controls |
| tools/r5_probe_reruns.py | 3,526 | `893b97d6a71c6a78df33af38ecbad2c7ce3d1f21400b9a930869cd8aeb3a84c2` | New: the reviews' probes, unchanged, against this packet |
| tools/r5_self_probes.py | 6,083 | `c936663d25276c463a946d50b5dbeb59dd80cce27c83e22bf53b38d61c9d981b` | New: further escape forms |
| tools/review-probes/probe_escape_forms.py, probe_coverage.py, probe_figure_coverage.py | 2,334; 2,996; 2,602 | `5c2dbc69...`, `e8749cbe...`, `f4c4d91b...` | The reviews' scripts, copied unchanged from the evidence branch |

`r4_figures_spec.py`, `r4_figures_build.py`, `r4_check_controls.py` and the round 3 tools are unchanged; the first two reproduce round 4's check, published as `author-r4/tools/check_b16_figures.py`, not the one now in `tools/`.

The check's SHA-256 and its outputs' are not on the findings page, for round 3's reason. They are here, in PR-BODY.md, in the post and in MANIFEST.sha256.

### Round 5 deviations and decisions

- **One rule, not a list of forms.** The assignment's item 1 is applied as stated: every digit, any Unicode digit or numeral (`str.isnumeric`), is accounted for; the token pattern only finds row candidates. A spelling the pattern cannot read is refused rather than given a new token form: no figure on the page uses one, and a row can claim only a plain spelling.
- **Separators beyond the assignment's list.** Item 2 lists none, one or more spaces, a non-breaking space or a hyphen. The check also takes line breaks, thin and zero-width spaces, soft and non-breaking hyphens, emphasis and code marks, a backslash, a double quote, an opening bracket, HTML entities, tags and comments, and units in either case. A table cell's bar is not a separator: a match that crosses a cell counts for nothing, and with the bar the page's `pts3` cell before "SAMPLE-EXACT" read as a measurement.
- **The quoted-mention rule.** With the double quote a separator, round 4's quoted control (`in "37" blocks`, expected not a measurement) failed. The assignment requires the eight existing controls green with their code unchanged, so a number quoted on its own is a mention: its closing quote does not join it to a unit. Coverage is the same either way (no category takes a quoted number); only its label differs. Stated on the page and in the check.
- **Link targets as addresses.** A resolving anchor's digits are covered even where a hyphen and a unit-like word follow (`#b16-round-4-packet-and-coverage`): the anchor stands for its heading, which the check reads where it stands. URLs are limited to the repository's issues, pull requests and comments; an anchor must be a heading slug of the findings page.
- **Paths by existence.** A digit-bearing word in code is covered only if it names a packet file or directory, a raw file `RAW-ARTIFACTS.json` lists, or one of them under the published packet's directory; a bare name must be a base name of one.
- **R625-4's continuation where it stands.** The assignment places the controls on the attribution row; a table row cannot hold a line break, so that control alters the B16c channels paragraph, as R625-4's probe does.
- **The `^` receipt.** Round 5's code took the check past the packet's 200 KB limit; repeated receipts are written as `^` (23 KB less), restored by `parse_rows`, so the rows output is unchanged in form.
- **A second commit.** The first commit's page listed the separators without the soft and non-breaking hyphens and the backslash, and did not state the quoted-mention rule; the second states both. No figure changed.

### Round 5 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126360842 (posted 16:32:10 CEST with the head, the dispositions, the check's results, the file hashes and the per-run tables; REVIEW-READY-r5.md, review-ready-r5-url.txt; REVIEW-READY-r5.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock free (the one non-blocking check above, no action under it).
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 5 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r5.md, REVIEW-READY-r5.readback.md, review-ready-r5-url.txt | The round 5 post and its readback |
| tools/r5_figures_spec.py, tools/r5_figures_build.py, tools/r5_check_controls.py, tools/r5_probe_reruns.py, tools/r5_self_probes.py | The round's new tools; tools/check_b16_figures.py edited |
| tools/review-probes/ | The reviews' three probes, unchanged |
| r5/figures-rows.tsv, r5/figures-coverage.tsv, r5/figures-check.stdout | The check's output at the head: its receipt |
| r5/r624-4-probe-rerun.json, r5/r625-4-probe-rerun.json, r5/r625-3-probe-rerun.json | The reviews' probes against the new check |
| r5/self-probes.json | Further escape forms against the new check |
| controls/r5-controls.json, controls/r5-rerun-r3-controls.json, controls/r5-rerun-r4-controls.json, controls/r5-controls-on-r4-check.json | The check's controls: round 5's runner, round 3's and round 4's runners, and round 5's runner on round 4's check |
| gates/r5/ | Gate logs and results at `36190193` |

## Round 6 (B16 findings round 6, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126774639 (the manager, after R624-5 and R625-5 on PR #725, both NEGATIVE; neither alleges a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6126709633 (R624-5: F1, F2, F3 MINOR; R1 residue; S1) and https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6126763696 (R625-5: F1 MINOR). Their probes came from the `629-b16-review-evidence` branch at `13738cb1` (fetched; extracted with `git show` into a scratch directory, read in full, checked against each review's MANIFEST.sha256, run with `-I`, no checkout): R624-5's `scripts/probe_row3200.py` (`11188752...`) and `scripts/probe_r624_5_escapes.py` (`c7ea04fb...`), R625-5's `probe_comment_separator.py` (`d799fce3...`); R625-5's `receipts/own-probes.json` (its 64-form campaign) was read for the forms it accepted.
- Head at resume: `3619019350936d5af851933df0b5444ef8387e69` (git rev-parse, 16:56 CEST), as pushed for PR #725. New commits only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** no controller, board, tap or instrument was touched, and the bench lock was not taken. Nothing private was read.

### Round 6 state

**REVIEW READY.** One commit on `36190193`, a one-line subject, no body, no trailers; not pushed:

- `e91a62ee266e182a804ca1f45a0f18f715096563`: the subsection "B16, round 6: the closed list"; the covered text reworded within its lines where the closed list refused an identifier's follower; the "Where the packet is" paragraph mapping rounds 4 and 5 (R624-5-F3); R624-5-R1's exact wording in round 5's list of identifiers; a note in round 5's measurement paragraph that its list missed units written as words; the introduction, Contents, opening paragraph and index row pointing to round 6.

Diff against `36190193`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md`; every edit before the round 6 subsection keeps its line, so no line before it moved (R624-5's probe reads lines 3008, 3174 and 3200 by number). No figure on the page changed.

- **The figures check at `e91a62ee`:** `python3 -I tools/check_b16_figures.py <page> . r6/figures-rows.tsv r6/figures-coverage.tsv` rc 0: 1,790 rows, all equal to their receipts; 1,980 tokens in 1,728 covered lines; 13,849 digits, 11,445 in claimed figures, 2,404 in 1,186 identifiers that count, 0 uncovered; 2 identifiers refused by the closed list, both "channels 2 and 3" before "carry" (B16b's and B16c's point-table preambles), whose digits the context-bound rows claim (`r6/figures-check.stdout`).
- **Its rows reproduce:** `python3 -I tools/r6_figures_build.py <page> tools/r6_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py` (`r6/build.stdout`). The check is 194,617 bytes, under the packet's 200 KB limit.
- **No key ignores its loop variable:** `python3 -I tools/r6_key_scan.py tools/check_b16_figures.py r6/key-scan.json` rc 0 (1,790 rows, 553 loops, 0 unused). On round 5's published check it finds exactly the row R624-5-F1 named, row 667 at line 3200 (`r6/key-scan-r5-check.json`), so it can fail for that defect.
- **Its controls:** `python3 -I tools/r6_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r6-controls.json` rc 0, 39 of 39 PASS: round 5's 22 (code unchanged) and 17 new. Round 3's, round 4's and round 5's runners, unchanged, against the new check: 5 of 5, 8 of 8 and 22 of 22 (`controls/r6-rerun-r3-controls.json`, `controls/r6-rerun-r4-controls.json`, `controls/r6-rerun-r5-controls.json`). All four re-run byte-equal at the head.
- **The new controls on round 5's check:** the same runner against the published `author-r5/tools/check_b16_figures.py` (`2641412c...`, equal to this packet's round 5 check) and the page at `36190193`, exported with `git archive` into a scratch tree with `GIT_DIR` set to the lane's repository (round 5's check passes that page there, rc 0): the 22 earlier PASS, the 17 new FAIL (`controls/r6-controls-on-r5-check.json`). So each new control can fail for the defect it targets.
- **The reviews' probes, unchanged:** `python3 -I tools/r6_probe_reruns.py <repo> . tools/review-probes <scratch> e91a62ee...` rc 0; each probe refused unless its SHA-256 equals the published one; each probe's own results kept verbatim (`r6/*-probe-rerun.json`):
  - R624-4's 8 of 8, R625-4's 12 of 12 (its own exit 0), R625-3's 7 of 7 detected;
  - R624-5's `probe_row3200.py`: its exit 0, `row3200_insensitive` false; at line 3200 the LOCKED row (671) is MISMATCH, recomputed "bcrf 595, baaf 596", receipt "r2/bcrf-poll-receipt.json; r2/baaf-poll-receipt.json"; the poll-count row (672) stays OK at 596;
  - R624-5's `probe_r624_5_escapes.py`: 21 of 25 forms detected; 18 of its 19 `id+` forms, every one whose unit is a ruling unit written as a word among them; not detected: the `id+ colon` form (a colon ends the identifier's phrase, a stated limit) and the three `word:` forms (a number in words, which the probe gives no digit to detect);
  - R625-5's `probe_comment_separator.py`: statuses [0, 1, 1], its own exit 0.
- **Further forms:** `python3 -I tools/r6_self_probes.py tools/check_b16_figures.py <page> . <scratch> r6/self-probes.json` rc 0: 78 forms, each meeting its expectation; 70 detected (round 5's 35 that still apply and 35 new), 8 pass as stated (round 5's page marker, now in a comment the check drops; and a full stop twice, a comma, a colon, a spaced dash, a possessive and a code literal before a word or unit).
- **Where the packet is:** `python3 -I tools/r6_evidence_receipt.py <repo> a73ce5c4 36190193 r6/evidence-receipt.json` rc 0: `MANIFEST.json` at `a73ce5c4` (3,044 entries) binds each author directory's files, hashes differing exactly where `path_redacted` is set; `author-r4/` last changed by `b83e5d76` ("at 61ae8641"), `author-r5/` by `a73ce5c4` ("at 36190193"); all 76 hash rows of the section at `36190193` equal their files in `author-r5/`, none path-redacted; 592 of `author-r5/`'s 593 files equal round 5's own MANIFEST.sha256 there (the 593rd is that manifest).
- **Gates at `e91a62ee`:** all 14 rc 0 (gates/r6/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,722 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before the commit.
- **Before the commit:** the added lines and every new packet file were scanned for private names, hosts, interfaces, addresses, capture-side values, home and temporary paths, and tool or model names: 0 hits (the gate results record the lane's /data path, as every earlier round's). The post, PR-BODY.md and this file were scanned the same way.

### Round 6 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R624-5-F1, MINOR | Tests, Conformance | Fixed: the row reads each case's count from that case's own receipt through `each()`, which returns the shared value or raises `Cases`, a MISMATCH naming each case's value; the rows output names both files read (an empty receipt column lists what the key read). The poll-count row beside it does the same. A control changes B-CRF's count only and sees the MISMATCH; R624-5's probe, unchanged, turns the LOCKED row MISMATCH. A key scan shows no other key ignores its loop variable | `tools/check_b16_figures.py` (`each`, `Cases`); `controls/r6-controls.json`; `r6/r624-5-row3200-probe-rerun.json`; `r6/key-scan.json` |
| R624-5-F2, MINOR | Conformance, Robustness, Tests, Docs | Fixed by the closed list (item 3) and by the units' names in `MEASURE`: per cent, percentage, decibels, hertz with kilo-, mega- and giga-, parts per million, billion or trillion, milli-, micro-, nano- and picoseconds, msec, usec, nsec. Controls for each spelling R624-5 named and for furlongs; R624-5's probe detects every ruling unit in words | the round 6 subsection; `controls/r6-controls.json`; `r6/r624-5-escapes-probe-rerun.json` |
| R624-5-F3, MINOR | Docs | Fixed: the paragraph maps round 4 to `author-r4/` (archived at `61ae8641`, published by `b83e5d76`) and round 5 to `author-r5/` (archived at `36190193`, published by `a73ce5c4`), and names round 6's `author-r6/`; rows recompute those commits from the receipt | "Where the packet is"; `r6/evidence-receipt.json` |
| R624-5-R1, RESIDUE | Docs | Applied verbatim on the page (round 5's list) and in PR-BODY.md (round 5, item 1) | the page; PR-BODY.md |
| R624-5-S1, SUGGESTION | Tests | Taken: "What the rule does not cover" states the limits; its forms run as self-probes, most now detected | the round 6 subsection; `r6/self-probes.json` |
| R625-5-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed: every HTML comment is dropped before any matching (one over several lines too), and `SEP`'s comment arm spans line breaks. A control applies R625-5's form where R625-5 did; R625-5's probe gives [0, 1, 1] | `normalise`, `blocks`; `controls/r6-controls.json`; `r6/r625-5-comment-probe-rerun.json` |

### Round 6 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| v0 | Context: the round 6 assignment; R624-5 and R625-5 in full; their probes and R625-5's campaign from the evidence branch at `13738cb1` | Read | this file |
| v1 | Normalisation, the closed list and the units' names in a scratch copy of the check; the unchanged page run through it | 143 refused identifiers, at 120 places, all but a few followed by a verb or a noun | - |
| v2 | The page reworded within its lines (127 edits); spec anchors moved with them | 6 left, then 0 | the page; `tools/r6_figures_spec.py` |
| v3 | "Channels 2 and 3 carry": R625-5's probe needs that text unchanged and passing, and R625-4's continuation must still fail, so rows claim the indices bound to the text around them | Both hold | `IDLE_CH` rows |
| v4 | Round 5's planted control failed: a refused match had made a digit a measurement though another category's identifier, followed by an item of the list, held it | A digit only refused identifiers hold is a measurement | `tools/check_b16_figures.py` |
| v5 | A colon in `SEP` tried and dropped: "round 4: packet" read as a measurement | Colon stays a phrase end, a stated limit | - |
| v6 | The round 6 subsection, the packet mapping, R624-5-R1, the pointers; the evidence receipt | Done | the page; `r6/evidence-receipt.json` |
| v7 | Controls, the three earlier runners, round 5's check, further forms; hash table filled; all re-run until byte-stable | Stable | `controls/`, `r6/` |
| v8 | Gates on the working tree, privacy scan, commit `e91a62ee`, gates at the head | Every gate rc 0 | gates/r6/ |
| v9 | At `e91a62ee`: the check, the build, the four runners, round 5's check, the six probes, the further forms, the key scan | All as stated above; every controls file byte-equal | `r6/`, `controls/` |
| v10 | HANDOFF.md, PR-BODY.md (Round 6; R624-5-R1 in round 5's item 1), REVIEW-READY-r6.md | Written | this directory |
| v11 | REVIEW READY on #629 | POSTED 17:52:34 CEST (comment 6127756184); readback equal but for one trailing newline | REVIEW-READY-r6.md, REVIEW-READY-r6.readback.md, review-ready-r6-url.txt |
| v12 | The check re-run after this file's last edit; manifest | Byte-equal; MANIFEST.sha256 over every packet file but itself | `r6/`, MANIFEST.sha256 |

### Round 6 tool changes

| Tool | Bytes | SHA-256 | Change |
|---|---|---|---|
| tools/check_b16_figures.py | 194,617 | `62bce479615dc54b107261b3f987434271bbab25e8acedd8bb39579b9be19274` | Edited from round 5's (`2641412c...`, published as `author-r5/`): docstring; `DASHES`, and `SEP` with every dash and a comment over line breaks; `MEASURE` with the units' names; `AFTER`, `ENDS`, `PAST`, `POSSESSIVE`, `SPACED_DASH` and `follows` (the closed list); `X` with a code flag; `packet_path` and the directory category to `author-r6`; `list_item` by source line starts; `normalise` and `blocks` rewritten; `each` and `Cases`; in `main`, tokens read on the normalised text, a row's figure bound to the text around it when its row names it, and the closed list applied to every category but addresses; the summary line adds `refused_identifiers`; the scope finds the reworded introduction; ROWS_TSV and EXCLUDE regenerated from the round 6 spec. TOKEN unchanged |
| tools/r6_figures_spec.py | 158,415 | `64c5314e274cbbcc454f76f56f22d1238ba4459c54372b8aeabb05c55bbca7e4` | New, a copy of `r5_figures_spec.py`: X marks code literals and drops the page marker; anchors moved; the LOCKED and poll-count rows through `each`; `IDLE_CH` context rows; rows for the packet mapping and round 6's counts |
| tools/r6_figures_build.py | 5,229 | `cb8aab2fe2530178bfe5e004dbd396e59006d6fcf3d824b2eb19318c9473433f` | New, a copy of `r5_figures_build.py`: the new introduction anchor; `@` rows keep their context |
| tools/r6_check_controls.py | 21,545 | `789a4f7ca25b8ef0d5b38bae9432d9f6be23434fe69ad20f0db9d7a80eb875de` | New, a copy of `r5_check_controls.py`: the 22 controls' code unchanged; 17 round 6 controls |
| tools/r6_evidence_receipt.py | 6,586 | `71d32ba09f2ec1f4ab02bc9adf8085b66e96e5ca35c7243026b25ba10fe1f0bb` | New, a copy of `r4_evidence_receipt.py`: every author directory, rows against the newest, its own manifest compared |
| tools/r6_self_probes.py | 9,132 | `f614715a9b4e4ffe504e9e2dafb043bdea7bf1656592a790e4016628d8da4bb5` | New: round 5's forms read from `r5_self_probes.py`, then round 6's, with stated passes |
| tools/r6_probe_reruns.py | 5,847 | `a08f1f4d718acd15c62203a3fd9ea932a0d74e19e39a4954d8d82d5f06ad7cae` | New, a copy of `r5_probe_reruns.py` with round 6's three probes |
| tools/r6_key_scan.py | 1,767 | `084a9d17ff7e74f070f32a18c9b05495e7c51f1d9e9fd6e6c027d563c68f14ed` | New: row keys whose loop variable is never read |
| tools/review-probes/probe_row3200.py, probe_r624_5_escapes.py, probe_comment_separator.py | 1,921; 4,283; 1,984 | `11188752...`, `c7ea04fb...`, `d799fce3...` | The reviews' scripts, copied unchanged from the evidence branch |

The round 5 tools are unchanged; `r5_figures_spec.py` and `r5_figures_build.py` reproduce round 5's check, published as `author-r5/tools/check_b16_figures.py`, not the one now in `tools/`.

### Round 6 deviations and decisions

- **The closed list reads after the identifier, not after each digit run.** A digit run inside a name (B16, McASP0, CRC32, `pts1`) is followed by the rest of the name; the list is read after the identifier's last group, so after "Milan v1.2 Table 5.4" or "channels 2 and 3". What is looked past is stated (spaces, dashes and hyphens, a slash or backslash, emphasis and code marks, brackets, quotes but a possessive, an HTML tag, a link's target).
- **Punctuation, read narrowly.** The assignment allows punctuation. The check takes only marks that end a phrase (. , ; : ! ? and a table's bar, a dash set off by spaces) as the end; it looks past brackets, quotes, slashes and dashes that touch, so `7) ppm`, `7' ppm`, `7/ppm`, `7—ppm` and the small and fullwidth hyphen-minus fail. A point or comma before a digit is a decimal sign.
- **A range.** A word of the list followed by a measurement makes the identifier one too ("CLOCK_DOMAIN 7 to N ppm"), so a row claiming the second number does not shelter the first.
- **Code literals end with their code word.** A packet path, a listed commit, the label, the branch, a field name, a packet directory or the command ends at the code mark or the space after it inside code: command lines in the page's fenced blocks put paths side by side. A prose identifier inside code is held to the list. Only the guard reads a code literal's digits, so `` `pts1` milliseconds `` fails and `` `pts1` furlongs `` passes; stated on the page.
- **Comments.** A comment shown in code is kept; a comment holding a blank line is dropped only at a line start, as an HTML block, since CommonMark shows it as text elsewhere. The round 5 page-marker category is gone: markers are comments.
- **A refused identifier and another that counts.** A digit becomes a measurement only when every identifier holding it is refused. Otherwise round 5's planted control failed: its catch-all category is refused inside `r2/...` while the path category, ending at the code mark, holds the same digit.
- **The words of the list stay four.** Most refused followers were verbs or nouns ("bound", "found", "acceptance", "item", "start"); no short list could hold them, and nouns can be units. The text was reworded instead, within its lines.
- **Context-bound rows for "Channels 2 and 3 carry".** R625-5's probe asserts that text unchanged and needs it to pass; the list refuses "carry". Rows claim the indices from every run's point summaries, each bound to "Channels «2» and" or "and «3» carry", so R625-4's unbound continuation (which changes the keyword) still fails, and so does round 5's continuation control.
- **R624-5's row probe and "both rows".** The assignment asks the unchanged probe to turn both line-3200 rows MISMATCH. The probe changes only the window's LOCKED count, 596 to 595, and leaves its poll count at 596, so the second row, the poll count of "596 of 596", is still correct and stays OK; the first is MISMATCH and the probe reports `row3200_insensitive` false. Making the poll-count row fail would make it check the LOCKED count, which is the first row's job. Line 3174's pair behaves the same, and R624-5 counted that line as turning MISMATCH. R624-5's own verification allows "or the check must otherwise fail at line 3200". Stated as an open question in the post.
- **The colon.** `SEP` with a colon read "round 4: packet" and "R624-5: per cent" on the page as measurements, so the colon stays a phrase end; `CLOCK_DOMAIN 7: ppm` passes, a stated limit (R624-5's `id+ colon`, an S1 form).
- **No figure changed; headings did.** The three acceptance headings changed slug; nothing on the page, in the repository's docs or in the PR body linked to them.

### Round 6 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6127756184 (posted 17:52:34 CEST with the head, the dispositions, the open question on R624-5's row probe, the check's results, the file hashes and the per-run tables; REVIEW-READY-r6.md, review-ready-r6-url.txt; REVIEW-READY-r6.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 6 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r6.md, REVIEW-READY-r6.readback.md, review-ready-r6-url.txt | The round 6 post and its readback |
| tools/r6_figures_spec.py, tools/r6_figures_build.py, tools/r6_check_controls.py, tools/r6_evidence_receipt.py, tools/r6_self_probes.py, tools/r6_probe_reruns.py, tools/r6_key_scan.py | The round's new tools; tools/check_b16_figures.py edited |
| tools/review-probes/probe_row3200.py, probe_r624_5_escapes.py, probe_comment_separator.py | Round 6's review probes, unchanged |
| r6/figures-rows.tsv, r6/figures-coverage.tsv, r6/figures-check.stdout, r6/build.stdout | The check's output at the head, and the build's |
| r6/evidence-receipt.json | Where the packet is published, rounds 1 to 5 |
| r6/*-probe-rerun.json, r6/probe-reruns.stdout | The six review probes against the new check |
| r6/self-probes.json, r6/self-probes.stdout | Further forms against the new check |
| r6/key-scan.json, r6/key-scan-r5-check.json | Row keys' loop variables, this check and round 5's |
| r6/controls.stdout, r6/rerun-r3.stdout, r6/rerun-r4.stdout, r6/rerun-r5.stdout, r6/controls-on-r5.stdout | The runners' standard output |
| controls/r6-controls.json, controls/r6-rerun-r3-controls.json, controls/r6-rerun-r4-controls.json, controls/r6-rerun-r5-controls.json, controls/r6-controls-on-r5-check.json | The check's controls |
| gates/r6/ | Gate logs and results at `e91a62ee` |

## Round 7 (B16 findings round 7, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6128175910 (the manager, after R624-6 POSITIVE and R625-6 NEGATIVE on PR #725; neither alleges a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6128169977 (R624-6: no finding; S1, S2) and https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6128099316 (R625-6: F1 MINOR). Their probes came from the `629-b16-review-evidence` branch at `a9535408` (fetched; extracted with `git show` into a scratch directory, read in full, checked against each review's MANIFEST.sha256, run with `-I`, no checkout): R625-6's `scripts/probe_rendered_comment.py` (`22c38feb...`) and `scripts/probe_followers.py` (`6703a346...`), R624-6's `probe_r624_6_escapes.py` (`f4c9d523...`) and `probe_row3200_polls.py` (`13a323fd...`).
- Head at resume: `e91a62ee266e182a804ca1f45a0f18f715096563` (git rev-parse, 18:18 CEST), as pushed for PR #725. New commits only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** no controller, board, tap or instrument was touched, and the bench lock was not taken. Nothing private was read but the private scan's term list.

### Round 7 state

**REVIEW READY.** One commit on `e91a62ee`, a one-line subject, no body, no trailers; not pushed:

- `295ba9d7f7dfed65e95002478ed6d55ccc14e580`: the subsection "B16, round 7: no markup"; the section's eleven table markers replaced by blank lines and one code block's four angle-bracket placeholders put in braces; "Where the packet is" mapping round 6; the introduction, Contents, opening paragraph and index row pointing to round 7.

Diff against `e91a62ee`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md`, 144 insertions and 19 deletions; every edit before the new subsection keeps its line, so no line before it moved (R624-5's probe reads lines 3008, 3174 and 3200, R624-6's line 3244). No figure on the page changed.

- **The figures check at `295ba9d7`:** `python3 -I tools/check_b16_figures.py <page> . r7/figures-rows.tsv r7/figures-coverage.tsv` rc 0: 1,834 rows, all equal to their receipts; 1,853 covered lines, 2,049 tokens; 14,531 digits, 11,910 in claimed figures, 2,621 in 1,271 identifiers that count, 0 uncovered; 2 identifiers refused by the closed list (as in round 6, both claimed by context rows); 0 lines with markup (`r7/figures-check.stdout`).
- **Its rows reproduce:** `python3 -I tools/r7_figures_build.py <page> tools/r7_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py` (`r7/build.stdout`). The check is 198,839 bytes, under the packet's 200 KB limit. With the round 7 rows left out, the rebuilt ROWS block equals round 6's byte for byte (checked before the round 7 text was added).
- **No key ignores its loop variable:** round 6's `tools/r6_key_scan.py`, unchanged, rc 0 (1,834 rows, 565 loops, 0 unused; `r7/key-scan.json`).
- **Its controls:** `python3 -I tools/r7_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r7-controls.json` rc 0, 50 of 50 PASS: round 6's 39 (code unchanged) and 11 new. Round 3's to round 6's runners, unchanged, against the new check: 5 of 5, 8 of 8, 22 of 22 and 39 of 39 (`controls/r7-rerun-r3-controls.json` to `controls/r7-rerun-r6-controls.json`).
- **The new controls on round 6's check:** the same runner against this packet's round 6 check (`62bce479...`, equal to `author-r6/tools/check_b16_figures.py`) and the page at `e91a62ee`, exported with `git archive` into a scratch tree with `GIT_DIR` set to the lane's repository (round 6's check passes that page there, rc 0): the 39 earlier PASS, the exception control PASS (round 6 dropped every comment), and the 10 refusal controls FAIL; round 6's check exits 0 on the three short-comment forms, the former marker and the changed marker (`controls/r7-controls-on-r6-check.json`).
- **The reviews' probes, unchanged:** `python3 -I tools/r7_probe_reruns.py <repo> . tools/review-probes <scratch> 295ba9d7... <renderer python>` rc 0; each probe refused unless its SHA-256 equals the published one; each probe's own results kept verbatim (`r7/*-probe-rerun.json`):
  - R625-6's `probe_rendered_comment.py`, under the renderer environment (cmarkgfm 2025.10.22, html5lib 1.1): statuses [0, 1, 1, 1, 1, 1]; every comment form names MARKUP and `UNCOVERED 7` at line 3011; the probe's own exit 1, from its last assertion, which states [0, 1, 1, 0, 0, 0];
  - R625-6's `probe_followers.py`: `code_directory_comment` and `malformed_comment` now exit 1 (0 in R625-6's record); the other 20 forms keep their status;
  - R624-6's `probe_r624_6_escapes.py`: every form's exit status equals R624-6's record at `e91a62ee`; the forms it expects to fail and that pass are `of-unit`, `and-unit`, `possessive-unit` and `list-item-7`, as R624-6 recorded (its S1);
  - R624-6's `probe_row3200_polls.py`: the poll-count row of line 3200 MISMATCH, `bcrf 595, baaf 596`;
  - R624-4's 8 of 8, R625-4's 12 of 12, R625-3's 7 of 7; R624-5's row probe `row3200_insensitive` false; R624-5's escape probe 21 of 25 (not detected: the `id+ colon` form and the three `word:` forms); R625-5's comment probe [0, 1, 1], its own exit 0.
- **Further forms:** `python3 -I tools/r7_self_probes.py tools/check_b16_figures.py <page> . <scratch> r7/self-probes.json` rc 0: 111 forms, each meeting its expectation; 92 detected, 19 passing as stated (`r7/self-probes.json`). The 33 round 7 forms: 20 markup forms, digit-free, each refused at its line as MARKUP; angle brackets around a link target, Markdown rather than markup, failing on its anchor's digits; a generator's marker as its own line passing; an entity-escaped tag, a less-than sign before a space and a fullwidth one passing; R624-6-S1's seven forms and a list marker before a unit passing. Round 5's page marker is now detected.
- **Where the packet is:** `python3 -I tools/r7_evidence_receipt.py <repo> b616e7ea e91a62ee r7/evidence-receipt.json` rc 0: `MANIFEST.json` at `b616e7ea` (3,800 entries, SHA-256 `4bced092...`) binds each author directory's files, hashes differing exactly where `path_redacted` is set; `author-r6/` (647 entries, 41 path-redacted) last changed by `b616e7ea` ("at e91a62ee"); all 84 hash rows of the section at `e91a62ee` equal their files in `author-r6/`, none path-redacted; 646 of `author-r6/`'s 647 files equal round 6's own MANIFEST.sha256 there (the 647th is that manifest).
- **Byte-stable:** every round 7 output (33 files: the check, its outputs, the controls, the probe records, the self-probes, the key scan, the evidence receipt) re-runs byte-equal at `295ba9d7`.
- **Gates at `295ba9d7`:** all 14 rc 0 (gates/r7/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 3,847 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before the commit, after one docs_check finding ("this round", process language) was reworded.
- **Before the commit:** the added lines and every new packet file were scanned for every private-map entry, private environment value, private name, host, interface, address, capture-side value, home and temporary path, and tool or model name: 0 hits in the added lines. The packet files' only hits are the redaction map's own field words "regex" and "literal" in ordinary prose and code, as in round 6's files. PR-BODY.md's only hits predate this round: "literal" in round 6's text and a four-hex substring of a round 6 SHA-256. The post and this file were scanned the same way.

### Round 7 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R625-6-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed by refusal, not imitation: any covered line holding `<` before a letter, `/`, `!` or `?` is refused and named MARKUP, in code too; the comment-stripping branch of `normalise` is removed; a generator's exact marker line is the only exception. R625-6's probe gives [0, 1, 1, 1, 1, 1]; standing controls for R625-6's four forms, R625-5's two, a raw tag between a number and its unit, a comment in a code span, a former table marker, and a generator's marker one byte off and exact | `markup`, `GENERATED`, `normalise`; `controls/r7-controls.json`; `r7/r625-6-rendered-probe-rerun.json` |
| R624-6-S1, SUGGESTION | Tests, Robustness | Taken as documentation: "What the rule does not cover" states the approximate-quantity forms and a list marker; they run as stated passes | the round 7 subsection; `r7/self-probes.json` |
| R624-6-S2, SUGGESTION | Docs | Closed as answered in PR-BODY.md, Round 7 item 3, and the round 6 open question there marked answered; the manager records it | PR-BODY.md |

### Round 7 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| w0 | Context: the round 7 assignment; R624-6 and R625-6 in full; their probes from the evidence branch at `a9535408` | Read | this file |
| w1 | The comment branch removed from `normalise`; markup refused by line in a scratch copy of the check; the unchanged page run through it | 15 places refused: the section's eleven table markers and four placeholders in one code block; the markers' digits now read | - |
| w2 | Markers to blank lines, placeholders to braces; GEN2 by header rows; build | Page passes, 1,790 rows as in round 6, markup 0; ROWS byte-identical to round 6's | - |
| w3 | R625-6's probe, unchanged; the pinned environment lacks `six`, so a disposable renderer environment from the hash-locked requirements | [0, 1, 1, 1, 1, 1] | `r7/r625-6-rendered-probe-rerun.json` |
| w4 | Controls runner (11 new), the four earlier runners, round 6's check and page exported at `e91a62ee` | 50 of 50; 5, 8, 22, 39; 10 refusal controls FAIL on round 6's check | `controls/` |
| w5 | Probe re-run tool with the four new probes; self-probes (33 new forms); evidence receipt | As stated above | `r7/` |
| w6 | Round 7 subsection, pointers, packet mapping, index row; rows; reworded where the closed list refused new text (and one file name that reads as a number before "polls") | Page passes | the page; `tools/r7_figures_spec.py` |
| w7 | The exception control and the stated-pass self-probes required exit 0, which the page's own counts decide: a cycle that does not settle. Both now compare with the unchanged page | Converged; outputs byte-stable over two passes | `tools/r7_check_controls.py`, `tools/r7_self_probes.py` |
| w8 | Gates on the working tree (one docs_check finding, "this round", reworded), privacy scan, commit `295ba9d7`, gates at the head | Every gate rc 0 | gates/r7/ |
| w9 | At `295ba9d7`: the round's outputs installed and regenerated in the packet; a second run | All 33 files byte-equal | `r7/`, `controls/` |
| w10 | HANDOFF.md, PR-BODY.md (Round 7; header, commit list, round 6 question marked answered), REVIEW-READY-r7.md | Written | this directory |
| w11 | The self-probes tool's docstring corrected (angle brackets around a link target are Markdown, not markup); the self-probes re-run | Output byte-equal | `tools/r7_self_probes.py`, `r7/self-probes.json` |
| w12 | REVIEW READY on #629 | POSTED 19:42:46 CEST (comment 6129482994); readback equal but for one trailing newline | REVIEW-READY-r7.md, REVIEW-READY-r7.readback.md, review-ready-r7-url.txt |
| w13 | The check re-run after the post; manifest | Byte-equal; MANIFEST.sha256 over every packet file but itself | `r7/`, MANIFEST.sha256 |

### Round 7 tool changes

| Tool | Bytes | SHA-256 | Change |
|---|---|---|---|
| tools/check_b16_figures.py | 198,839 | `6b2570b8361356f71f36dc8ec72197c5a8882fa3507f7a01a533f23e575897a0` | Edited from round 6's (`62bce479...`, published as `author-r6/`): docstring (round 7: no markup; normalisation without comments); `normalise` without its comment branch; `MARKUP`, `GENERATED` and `markup()`; in `main`, MARKUP lines in the coverage receipt and on standard output, `markup` in the summary, exit 1 on any; `packet_path` to `author-r7`; ROWS_TSV and EXCLUDE regenerated from the round 7 spec (the commit list gains `e91a62ee` and `b616e7ea`, the packet directory `author-r7/`). `SEP`, `PAST`, TOKEN and the closed list unchanged |
| tools/r7_figures_spec.py | 161,071 | `635427db447ec4dd575af3d55da60836ec4e17a6471bc20e23cbffa0709f211b` | New, a copy of `r6_figures_spec.py`: GEN2 knows a table by its header row; the code block's anchor in braces; X as above; rows for round 6's packet location and round 7's figures |
| tools/r7_figures_build.py | 5,318 | `2be351307059e55b1e5065111f5f238867258f8b858ce6f6f093856fbd6ed52d` | New, `r6_figures_build.py` unchanged but for its name and docstring |
| tools/r7_check_controls.py | 28,060 | `6a53a284ef5e70910282c3551285d82161d77412804c27830b7c684adc80c8fb` | New, a copy of `r6_check_controls.py`: the 39 controls' code unchanged; 11 round 7 controls |
| tools/r7_probe_reruns.py | 9,983 | `66a23643d0b01973b8f7f32ae08ac235a9b3ffff048392125bded8bab630a379` | New, a copy of `r6_probe_reruns.py` with round 7's four probes and a renderer interpreter for R625-6's |
| tools/r7_self_probes.py | 9,571 | `28e553c86740d55fae92fcc661c051a771af692f82bd03afcdc26db8477ae843` | New: round 5's and round 6's forms read from their files, then round 7's; MARKUP counts as detection; stated passes compared with the unchanged page |
| tools/r7_evidence_receipt.py | 6,919 | `a46c4ad554c6a1448319f7d1e26fdf6e01407aedb0d4868d1fb96bf66d8b099e` | New, `r6_evidence_receipt.py` unchanged but for its name, docstring and note |
| tools/review-probes/probe_rendered_comment.py, probe_followers.py, probe_r624_6_escapes.py, probe_row3200_polls.py | 3,299; 2,817; 5,181; 1,674 | `22c38feb...`, `6703a346...`, `f4c9d523...`, `13a323fd...` | The reviews' scripts, copied unchanged from the evidence branch |

The round 6 tools are unchanged; `r6_figures_spec.py` and `r6_figures_build.py` reproduce round 6's check, published as `author-r6/tools/check_b16_figures.py`, not the one now in `tools/`. The disposable renderer environment and the private scan stay outside the packet.

### Round 7 deviations and decisions

- **Refused in code too.** The assignment refuses markup in the text the check reads. The check does not decide what is code for this rule: a `<` followed by a letter, `/`, `!` or `?` is refused wherever it stands on a covered line. Its code reading (fences, indented lines, code spans) is an imitation of the renderer, and any difference, such as an info string with a backtick or an unclosed span in an earlier table cell, could otherwise shelter a tag. The cost was the four placeholders of one fenced block, now in braces (`{raw}`, `{class map}`, `{list of the twelve reads}`); the row that claims "twelve" there moved with its anchor.
- **A superset of raw HTML.** The pattern also refuses an autolink, an unclosed tag and a backslash before a tag, which render as text or as a link. The section uses none of them. A less-than sign before a space or a digit, an entity that gives one, and a fullwidth one are not refused; they are not markup, and self-probes record them passing.
- **The generators' markers.** `scripts/gen_toc.py` writes no comment marker: it finds its list by the `## Contents` heading. `scripts/check_solution_docs.py` generates its product and interface tables with four exact markers, and these are `GENERATED`. The markers that `check_submodule_docs.py` and `check_feature_status.py` read delimit hand-written text and are not generated, so they are not excepted. A marker is excepted only as a whole line, byte for byte; a control and a self-probe show one with a byte changed, or a space after it, refused.
- **Markers to blank lines.** The section's eleven table markers became blank lines, not deleted lines. R624-5's row probe reads lines 3008, 3174 and 3200 by number, and R624-6's escape probe reads line 3244, so no line before them could move. Two blank lines render as one, and no gate refuses them. The spec's GEN2 now knows a point or grade table by its header row, and the rebuilt rows are byte-identical to round 6's.
- **`SEP` and `PAST` unchanged.** They still look past a tag or a comment, as in round 6, to decide only whether a number is a measurement; they make nothing disappear. Any line holding markup fails before either matters. Keeping them keeps round 6's R625-5 control, which expects the 7 named a measurement, green with its code unchanged.
- **S1 as documentation.** R624-6 offered two options. Refusing a follower word whenever a unit follows before the phrase's end would read "peer's" as a number before the seconds symbol, among others, and force another rewording of the page; the ruling's list stands. The forms are stated limits on the page and run as stated passes.
- **S2.** Closed as answered in PR-BODY.md, Round 7 item 3; the manager records it.
- **The renderer for R625-6's probe.** The pinned Markdown environment lacks `six`, which html5lib 1.1 imports. As R625-6 did, the renderer was installed from `tools/markdown/requirements.txt` with `--require-hashes` into a disposable environment in the lane's scratch area, outside the packet: cmarkgfm 2025.10.22, html5lib 1.1. Only that probe runs under it.
- **R625-6's probe exits 1.** Its last assertion states the statuses before the fix, `[0, 1, 1, 0, 0, 0]`, and R625-6 wrote that it must be updated for the correction. The probe is run unchanged; its statuses are `[0, 1, 1, 1, 1, 1]`, and its exit status is recorded beside them.
- **A file name the page cannot write.** `probe_row3200_polls.py` in code reads as 3200 before the unit "polls" (the guard reads a code literal's digits, a stated round 6 limit), so the page calls it R624-6's poll-count probe.
- **Self-probes.** A form is detected when the check names an UNCOVERED number or a MARKUP line at its line; the round 7 forms hold no digit, so only the refusal can catch them.

### Round 7 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6129482994 (posted 19:42:46 CEST with the head, the item table, the choices, the check's results, the file hashes and the per-run tables; REVIEW-READY-r7.md, review-ready-r7-url.txt; REVIEW-READY-r7.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 7 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r7.md, REVIEW-READY-r7.readback.md, review-ready-r7-url.txt | The round 7 post and its readback |
| tools/r7_figures_spec.py, tools/r7_figures_build.py, tools/r7_check_controls.py, tools/r7_probe_reruns.py, tools/r7_self_probes.py, tools/r7_evidence_receipt.py | The round's new tools; tools/check_b16_figures.py edited |
| tools/review-probes/probe_rendered_comment.py, probe_followers.py, probe_r624_6_escapes.py, probe_row3200_polls.py | Round 7's review probes, unchanged |
| r7/figures-rows.tsv, r7/figures-coverage.tsv, r7/figures-check.stdout, r7/build.stdout | The check's output at the head, and the build's |
| r7/evidence-receipt.json, r7/evidence-receipt.stdout | Where the packet is published, rounds 1 to 6 |
| r7/*-probe-rerun.json, r7/probe-reruns.stdout | The ten review probes against the new check |
| r7/self-probes.json, r7/self-probes.stdout | Further forms against the new check |
| r7/key-scan.json | Row keys' loop variables |
| r7/controls.stdout, r7/rerun-r3.stdout to r7/rerun-r6.stdout, r7/controls-on-r6.stdout | The runners' standard output |
| controls/r7-controls.json, controls/r7-rerun-r3-controls.json to controls/r7-rerun-r6-controls.json, controls/r7-controls-on-r6-check.json | The check's controls |
| gates/r7/ | Gate logs and results at `295ba9d7` |

## Round 8 (B16 findings round 8, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6130721355 (the manager, after R624-7 and R625-7, both NEGATIVE on PR #725 with one MINOR each; neither alleges a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6130711392 (R624-7: F1, image syntax hides a phrase mark) and https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6130634625 (R625-7: F1, markup in the index suffix crashes the check). Their probes came from the `629-b16-review-evidence` branch at `82662b7c` (R624-7's archive; R625-7's is `c1b06ee4`), extracted with `git show` into a scratch directory, read in full, each checked against its review's MANIFEST.sha256 and run with `-I`, no checkout: R624-7's `scripts/probe_r624_7_markdown_escapes.py` (`4366f8ca...`) and `scripts/probe_r624_7_invisible.py` (`ef5ebaae...`), R625-7's `probe_markup.py` (`d23a4cb5...`).
- Head at resume: `295ba9d7f7dfed65e95002478ed6d55ccc14e580` (git rev-parse, 21:02 CEST), as pushed for PR #725. New commits only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** no controller, board, tap or instrument was touched, and the bench lock was not taken. Nothing private was read but the private scan's term list.

### Round 8 state

**REVIEW READY.** One commit on `295ba9d7`, a one-line subject, no body, no trailers; not pushed:

- `b522bb923fa59581478460b61633bce2cb90ac1d`: the subsection "B16, round 8: the parser"; the section's fenced code block (round 2's four extraction commands) rewritten as a list of code spans on the same lines, its fence lines blank; "Where the packet is" mapping round 7; a pointer from round 7's rule to round 8's; the introduction, Contents, opening paragraph and index row pointing to round 8; the index row's round 7 sentence no longer claims that no markup can hide a unit.

Diff against `295ba9d7`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md`, 169 insertions and 12 deletions; every edit before the new subsection keeps its line, so no line before it moved (R624-5's probe reads lines 3008, 3174 and 3200, R624-6's line 3244, R625-6's and R624-7's line 3011, R625-5's 3108). No figure on the page changed.

- **The figures check at `b522bb92`:** `<parser python> -I tools/check_b16_figures.py <page> . r8/figures-rows.tsv r8/figures-coverage.tsv` rc 0: 1,867 rows, all equal to their receipts; 2,010 covered lines, 2,099 tokens; 14,442 digits, 12,164 in claimed figures, 2,278 in 1,243 identifiers that count, 0 uncovered; 2 identifiers refused by the closed list (as before, both claimed by context rows); 0 constructs refused (`r8/figures-check.stdout`). `<parser python>` is an interpreter with `tools/markdown/requirements.txt` installed by hash, in a disposable environment outside the packet (cmarkgfm 2025.10.22, cffi 2.1.1, pycparser 3.0, html5lib 1.1, six 1.17.0, webencodings 0.6.1). The gates' Markdown environment gives byte-equal rows, coverage and standard output.
- **Its rows reproduce:** `python3 -I tools/r8_figures_build.py <page> tools/r8_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py` (`r8/build.stdout`). The check is 199,434 bytes, under the packet's 200 KB limit.
- **No key ignores its loop variable:** round 6's `tools/r6_key_scan.py`, unchanged, rc 0 (1,867 rows, 569 loops, 0 unused; `r8/key-scan.json`).
- **Its controls:** `<parser python> -I tools/r8_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r8-controls.json` rc 0, 73 of 73 PASS: round 7's 50 (code unchanged but for two expectations, below) and 23 new. Round 3's to round 7's runners, unchanged, against the new check: 5 of 5, 7 of 8, 21 of 22, 38 of 39 and 48 of 50 (`controls/r8-rerun-r3-controls.json` to `controls/r8-rerun-r7-controls.json`); the only FAILs are round 4's link-label control (in the r4, r5, r6 and r7 runners) and round 7's code-span comment control, each on one expectation the parser changes.
- **The new controls on round 7's check:** the same runner against round 7's check (`6b2570b8...`, equal to `author-r7/tools/check_b16_figures.py`) and the page at `295ba9d7`, exported with `git archive` (docs, scripts, tools/markdown) into a scratch tree with `GIT_DIR` set to the lane's repository (round 7's check passes that page there, rc 0): the 48 unchanged controls PASS, and the 2 changed and 23 new controls FAIL (`controls/r8-controls-on-r7-check.json`).
- **The reviews' probes, unchanged:** `<parser python> -I tools/r8_probe_reruns.py <repo> . tools/review-probes <scratch> b522bb92...` rc 0; each probe refused unless its SHA-256 equals the published one; each probe's own results kept verbatim (`r8/*-probe-rerun.json`):
  - R624-7's `probe_r624_7_markdown_escapes.py`: 17 forms, none escapes; exit 0 for the unchanged page and the stated full-stop form, 1 for every other; each image form names `MARKUP ... image` at line 3011;
  - R624-7's `probe_r624_7_invisible.py`: all 10 forms exit 1;
  - R625-7's `probe_markup.py`: 25 cases; every case but the unchanged page exits 1; the four index markup cases name `MARKUP README.md:15 html_inline ...`, the index digit case names its numbers UNCOVERED at `README.md:15`; both receipts written in every case; no exception;
  - the ten earlier probes keep round 7's readings (exit statuses and detections), but for the construct name each MARKUP now carries (`html_inline <!-- -->` for `<!-- -->`) and R624-6's `link-ref-title`, a form R624-6 marked "any": a reference definition with a title, which renders nothing, now exits 0 (1 at round 7). R625-6's rendered-comment probe still gives [0, 1, 1, 1, 1, 1] and exits 1 from its own last assertion, as at round 7.
- **Further forms:** `<parser python> -I tools/r8_self_probes.py tools/check_b16_figures.py <page> . <scratch> r8/self-probes.json` rc 0: 138 forms, each meeting its expectation; 108 detected, 30 passing as stated. Five round 7 forms are now expected to pass, each with its reason (RULED): an autolink, a tag in a code span, a comment after a backslash, an unclosed tag, and angle brackets around a link target that resolves.
- **Where the packet is:** `python3 -I tools/r8_evidence_receipt.py <repo> fa974c3f 295ba9d7 r8/evidence-receipt.json` rc 0: `MANIFEST.json` at `fa974c3f` (4,711 entries, SHA-256 `461642b2...`) binds each author directory's files, hashes differing exactly where `path_redacted` is set; `author-r7/` (707 entries, 49 path-redacted) last changed by `fa974c3f` ("at 295ba9d7"); all 93 hash rows of the section at `295ba9d7` equal their files in `author-r7/`, none path-redacted; 706 of `author-r7/`'s 707 files equal round 7's own MANIFEST.sha256 there (the 707th is that manifest).
- **Byte-stable:** the round's outputs were generated in a scratch copy of the packet, installed, and regenerated in the packet at `b522bb92`: 34 files byte-equal; the 13 probe records then ran twice in the packet, byte-equal (the scratch probe records predated the final reflow of three paragraphs and differed only in digit counts and line numbers).
- **Gates at `b522bb92`:** all 14 rc 0 (gates/r8/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 4,004 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before the commit.
- **Before the commit:** the added lines and every new packet file were scanned for every private-map entry, private environment value, private name, host, interface, address, capture-side value, home and temporary path, and tool or model name: the only hits are the redaction map's own field words "literal" and "regex" in ordinary prose and code, as in rounds 6 and 7. The post and this file were scanned the same way.

### Round 8 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R624-7-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed by reading through the pinned parser: only visible inline text is judged (text, code spans, link text), so an image's `!` is never in the text; an image is off the closed allowlist and refused at its line as MARKUP, and the text around it is read without it, so the 7 before `ppm` is UNCOVERED. R624-7's probe, unchanged: no form escapes. Standing controls for its eight image forms | `blocks`, `ALLOWED`; `controls/r8-controls.json`; `r8/r624-7-escapes-probe-rerun.json` |
| R625-7-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed: the index row is parsed with its document and read from the lane B16 part's first byte by the parser's source columns; markup there is refused as MARKUP at `README.md:15` with both receipts written. R625-7's probe, unchanged: the four index markup cases refused at the index line, receipts written, no traceback. Standing controls for those four cases | `blocks`; `controls/r8-controls.json`; `r8/r625-7-markup-probe-rerun.json` |

### Round 8 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| w0 | Context: the round 8 assignment; R624-7 and R625-7 in full; their probes from the evidence branch at `82662b7c` | Read | this file |
| w1 | The pinned parser's node tree on the page and the index row: source positions of text and code nodes equal their source bytes, in table cells too | Usable for line numbers and the index row's columns | - |
| w2 | Prototype reader in a scratch copy of the check: the repository's renderer module for the pin check, extensions and options; a closed allowlist; markup patterns, the code and escape normaliser, the list-item and link-target categories removed | Unchanged page: 1,833 of 1,834 rows, 0 uncovered, one refusal: the section's fenced code block | - |
| w3 | The fenced block rewritten as a list of code spans on the same lines | 1,834 of 1,834 rows, 0 uncovered, 0 refused | the page |
| w4 | R624-7's and R625-7's probes, unchanged, against the prototype | No escape; the four index cases refused at the index line with both receipts | - |
| w5 | Round 3 to round 7 runners against the prototype | Two expectations changed (below); a raw HTML block's end line (cmark-gfm reports the line before its start) fixed | - |
| w6 | Parser quirks: footnotes typed `<unknown>` (named by type number), autolinked text without a start column (placed at its end) | Handled | `tree`, `place` |
| w7 | A fresh environment from the hash-locked requirements; round 8 runner, self-probes, probe re-run tool, evidence receipt | 73 of 73; 138 met; all probes as stated | `tools/r8_*` |
| w8 | Round 8 text, pointers, location paragraph, index row; rows; rewording where the closed list refused new text; the check's own documentation trimmed to stay under 200 KB | Page passes | the page; `tools/r8_figures_spec.py` |
| w9 | Fixed point over the hash table, controls and reruns; three paragraphs reflowed within their line counts | Stable over two passes | - |
| w10 | Gates on the working tree, privacy scan, commit `b522bb92`, gates at the head | Every gate rc 0 | gates/r8/ |
| w11 | At `b522bb92`: outputs installed in the packet and regenerated there; probes run twice | 34 files byte-equal; 13 probe records byte-equal on the second run | `r8/`, `controls/` |
| w12 | HANDOFF.md, PR-BODY.md (Round 8; header, commit list), REVIEW-READY-r8.md; the three scanned for private terms | Written; no hit in the round 8 text | this directory |
| w13 | REVIEW READY on #629 | POSTED 22:25:34 CEST (comment 6132021882); readback equal but for one trailing newline | REVIEW-READY-r8.md, REVIEW-READY-r8.readback.md, review-ready-r8-url.txt |
| w14 | MANIFEST.sha256 over every packet file but itself; no packet file over 200 KB | Written | MANIFEST.sha256 |

### Round 8 tool changes

| Tool | Bytes | SHA-256 | Change |
|---|---|---|---|
| tools/check_b16_figures.py | 199,434 | `2eb5a24e427015d39154d28f778693f1170cf513e3e3d34f2cac308f2adc0284` | Edited from round 7's (`6b2570b8...`, published as `author-r7/`): docstring (round 8); the reader (`bind`, `tree`, `place`, `blocks`) parses both documents whole with the pinned parser, verified by the repository's `scripts/gen_toc_renderer.py` (`verify`, `PINNED`, `EXTENSIONS`; `render`'s options), walking the node tree through the binding's exported C API as that module does; `ALLOWED`, `LEAVES`, `GENERATED`; `normalise` keeps its name and signature but only collapses whitespace and drops invisible characters (R625-6's probe extracts it by AST); `MARKUP`, `markup()`, `ESCAPABLE`, `ENTITY`, `BLANK`, `STARTS` and `list_item` removed; `SEP` and `PAST` without their entity, comment, tag and link-target alternatives; `in_code` by the parser's code spans (`CODE`); `on_page` reads a target and the parser's headings; code categories must lie in one code span; `X` without `address`; `passed()` for round 8's rows; `packet_path` to `author-r8`; ROWS_TSV and EXCLUDE regenerated from the round 8 spec; documentation trimmed |
| tools/r8_figures_spec.py | 163,934 | `d7873c54bc42e64410dd9bc6ecb4f21d020037007672c293adf4d57039056d80` | New, a copy of `r7_figures_spec.py`: X without the list-item and link-target categories, review names to round 7, the packet directory to `author-r8/`; rows for round 7's packet location and round 8's figures |
| tools/r8_figures_build.py | 5,383 | `95b1abb5aef4063253f236649a982aaa464cee5b4092e807b017e75633325ee7` | New, `r7_figures_build.py` unchanged but for its name and docstring |
| tools/r8_check_controls.py | 36,524 | `68f85edf41723ad7e87aa7dd4353182666022bb7286cdfa81cccbbe86fb864d6` | New, a copy of `r7_check_controls.py`: the 50 controls' code unchanged but for the two expectations the parser changes (each recorded with `"expectation": "round 8"`); 23 round 8 controls |
| tools/r8_probe_reruns.py | 13,525 | `1213ddb41e1c3d4653a50173e43ae8f0b9f2667dc72fd6fcce5a017b2f6b49da` | New, a copy of `r7_probe_reruns.py` with round 8's three probes; every probe runs under the parser's interpreter |
| tools/r8_self_probes.py | 9,116 | `ae8637b6dea365f9870867e1d0f0245e496c84b6eb143ffa467c817af7d41f39` | New: round 5's to round 7's forms read from their files, five of round 7's ruled to pass, then round 8's 27; detection at any line the inserted text occupies |
| tools/r8_evidence_receipt.py | 7,353 | `95c3ca5ea4f5ebda66ea3d5bbeb2584cb7dda9773182ac40b3b9aea4c6a1ebee` | New, `r7_evidence_receipt.py` unchanged but for its name, docstring and note |
| tools/review-probes/probe_r624_7_markdown_escapes.py, probe_r624_7_invisible.py, probe_markup.py | 4,503; 1,462; 3,426 | `4366f8ca...`, `ef5ebaae...`, `d23a4cb5...` | The reviews' scripts, copied unchanged from the evidence branch |

The round 7 tools are unchanged; `r7_figures_spec.py` and `r7_figures_build.py` reproduce round 7's check, published as `author-r7/tools/check_b16_figures.py`, not the one now in `tools/`. The disposable parser environment, the scratch packet copy, the regeneration driver and the private scan stay outside the packet.

### Round 8 deviations and decisions

- **Two earlier expectations change (published for the manager's decision).** Item 4 asks that earlier controls keep their outcomes; reading only what the parser yields changes two expectations, and the check still fails both altered pages and names the added number. Round 4's link-label control expects the `37` of `[37](#b16c-attribution) blocks` not to be named a measurement: the link's target stood between the number and its unit in the raw text, but a reader sees "37 blocks", and the check now names it a measurement. Round 7's control for a comment inside a code span expects MARKUP: a reader sees the comment written out in the code, so the check reads it as text, names the 7 UNCOVERED and refuses nothing (item 2: code spans are on the allowlist; the markup patterns are removed). Keeping either expectation would need a character the reader does not see, or a markup pattern inside code, the two things the round removes. The unchanged earlier runners report these as FAILs (4 runners for the first, 1 for the second); `tools/r8_check_controls.py` carries both forms with the round 8 expectation.
- **Code spans between code marks.** The check reads a code span's literal with a backtick at each end. The marks stand for the span's boundary, which the parser gives; every rule looks past them (`SEP`, `PAST`), none counts them as a phrase mark, and a code literal still ends at its closing mark. So the code categories keep their patterns, and they now also need the match inside one parser code span.
- **Link targets.** A link's target and title are not text and are not read. A target must still resolve (round 5's rule: an issue or pull request of the repository on GitHub, or a heading's anchor on the page, the headings now read from the parser); one that does not is read as a block of its own at its line, so round 5's anchor control stays green with its code unchanged. The link-target category is removed: no target is in the text.
- **List numbers.** A list's numbers are drawn by the renderer from the list's structure and are not text the parser yields, so the list-item category is removed; a numbered item that is only a unit passes, as R624-6-S1's stated form already did.
- **Refusal naming.** Each construct off the allowlist is named once, at its first covered line, as `MARKUP <document>:<line> <parser's name> <source, at most 40 characters>`; what it holds is not read. The parser names footnote definitions and references `<unknown>`; the check names them by their type number (cmark-gfm's header). A refused construct that starts above the section and runs into it is named at the first covered line.
- **Parser quirks met.** cmark-gfm reports a raw HTML block's end on the line before its start; the check reads it as ending on its own line. Text the autolink extension makes has no start column; its characters take the node's end column, so in the index row they count when the link ends inside the lane B16 part.
- **The environment.** The repository's renderer module imports html5lib only when its own `binding()` runs; the check loads the module for `verify`, `PINNED` and `EXTENSIONS` only and needs cmarkgfm and cffi. A disposable environment from `tools/markdown/requirements.txt` with `--require-hashes` ran everything; the gates' Markdown environment gives byte-equal check outputs. Without the parser the check exits 1 naming it (a round 8 control).
- **The section's code block.** A fenced block is off the allowlist, so the four extraction commands are now a list of code spans; its two fence lines are blank, so no line moved.
- **Size.** The check was over the packet's 200 KB limit with the reader and round 8's rows, so its own documentation was condensed (the page states every rule) and a `passed()` helper shortens round 8's rows; 199,434 bytes.
- **`normalise` kept.** R625-6's probe extracts `normalise` and its old globals by AST and calls it; it keeps its name, signature and return shape and needs no global.
- **The index row's round 7 sentence.** It said no markup could hide a unit; R624-7 showed an image could. The sentence now ends at the removed markers, and round 8's sentence states the rule as it is.

### Round 8 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132021882 (posted 22:25:34 CEST with the head, the item table, the two changed expectations for the manager's decision, the choices, the check's results, the file hashes and the per-run tables; REVIEW-READY-r8.md, review-ready-r8-url.txt; REVIEW-READY-r8.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 8 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r8.md, REVIEW-READY-r8.readback.md, review-ready-r8-url.txt | The round 8 post and its readback |
| tools/r8_figures_spec.py, tools/r8_figures_build.py, tools/r8_check_controls.py, tools/r8_probe_reruns.py, tools/r8_self_probes.py, tools/r8_evidence_receipt.py | The round's new tools; tools/check_b16_figures.py edited |
| tools/review-probes/probe_r624_7_markdown_escapes.py, probe_r624_7_invisible.py, probe_markup.py | Round 8's review probes, unchanged |
| r8/figures-rows.tsv, r8/figures-coverage.tsv, r8/figures-check.stdout, r8/build.stdout | The check's output at the head, and the build's |
| r8/evidence-receipt.json, r8/evidence-receipt.stdout | Where the packet is published, rounds 1 to 7 |
| r8/*-probe-rerun.json, r8/probe-reruns.stdout | The thirteen review probes against the new check |
| r8/self-probes.json, r8/self-probes.stdout | Further forms against the new check |
| r8/key-scan.json | Row keys' loop variables |
| r8/controls.stdout, r8/controls-on-r7.stdout, r8/rerun-r3.stdout to r8/rerun-r7.stdout | The runners' standard output |
| controls/r8-controls.json, controls/r8-controls-on-r7-check.json, controls/r8-rerun-r3-controls.json to controls/r8-rerun-r7-controls.json | The check's controls |
| gates/r8/ | Gate logs and results at `b522bb92` |

## Round 9 (B16 findings round 9, documents only)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132350672 (the manager, after R624-8, NEGATIVE with one MINOR, and R625-8, NEGATIVE with one MINOR settled by the decision https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481; neither alleges a DUT defect). Reviews: https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6132342798 (R624-8: F1, a raw HTML block from the line above a covered region to its first covered line is neither refused nor read; S1, emoji shortcodes and link titles) and https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6132288182 (R625-8: F1, two changed control expectations awaiting a decision). R624-8's `tools/probe_r624_8_html_block_edge.py`, `tools/dump_tree.py` and `receipts/parser-positions.txt` came from `629-b16-review-evidence` at `f4936667` (`review-evidence/629-b16-r1/reviews/R624-8/`), extracted with `git show` into a scratch directory, each equal to R624-8's MANIFEST.sha256, read in full and run with `-I`, no checkout.
- Head at resume: `b522bb923fa59581478460b61633bce2cb90ac1d` (git rev-parse, 22:48 CEST), as pushed for PR #725. New commits only; no rebase, no amend; TAKEN not posted again; nothing pushed; no PR edited.
- **No bench action:** no controller, board, tap or instrument was touched, and the bench lock was not taken. Nothing private was read but the private scan's term list.

### Round 9 state

**REVIEW READY.** One commit on `b522bb92`, a one-line subject, no body, no trailers; not pushed:

- `cb5ff79f1f69117efba353484851eceb620e5c92`: the subsection "B16, round 9: source extents"; "Where the packet is" mapping round 8; round 8's rule paragraph, its "Earlier expectations" paragraph and its runner list recording the decision and pointing to round 9; the introduction, Contents, opening paragraph and index row pointing to round 9.

Diff against `b522bb92`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and the lane's row in `docs/findings/README.md`, 161 insertions and 9 deletions; every edit before the new subsection keeps its line, so no line before it moved. No figure on the page changed.

- **The figures check at `cb5ff79f`:** `<parser python> -I tools/check_b16_figures.py <page> . r9/figures-rows.tsv r9/figures-coverage.tsv` rc 0: 1,909 rows, all equal to their receipts; 2,162 covered lines; 14,956 digits, 12,531 in claimed figures, 2,425 in identifiers that count, 0 uncovered; 2 identifiers refused by the closed list (both claimed by context rows, as before); 0 constructs refused (`r9/figures-check.stdout`). `<parser python>` is round 8's disposable environment from `tools/markdown/requirements.txt` by hash.
- **Its rows reproduce:** `python3 -I tools/r9_figures_build.py <page> tools/r9_figures_spec.py tools/check_b16_figures.py <out>` writes a check byte-equal to `tools/check_b16_figures.py` (199,529 bytes, under 200 KB).
- **The reader alone moves nothing:** `GIT_DIR=<repo>/.git <parser python> -I tools/r9_reader_on_r8.py <round 8 check> tools/check_b16_figures.py <tree of b522bb92> . <scratch> r9/reader-on-r8.json` rc 0: round 9's reader with round 8's ROWS and EXCLUDE blocks, on the page at `b522bb92`, gives rows, coverage and output byte-equal to `r8/`.
- **What the parser reports:** `<parser python> -I -B tools/r9_parser_extents.py tools/check_b16_figures.py <repo> <scratch> r9/parser-extents.json` rc 0, 37 of 37 cases met; kinds reported short of their source: html_block, image, link, strikethrough; six paragraph forms misplaced. `-B` keeps the imported check's bytecode out of the packet.
- **No key ignores its loop variable:** `tools/r6_key_scan.py`, unchanged, rc 0 (1,909 rows, 541 loops, 0 unused; `r9/key-scan.json`).
- **Its controls:** `<parser python> -I tools/r9_check_controls.py tools/check_b16_figures.py <page> . <scratch> controls/r9-controls.json` rc 0, 97 of 97 PASS: round 8's 73 (unchanged) and 24 new. Round 3's to round 8's runners, unchanged, against the new check: 5 of 5, 7 of 8, 21 of 22, 38 of 39, 48 of 50 and 73 of 73 (`controls/r9-rerun-r3-controls.json` to `controls/r9-rerun-r8-controls.json`); the only FAILs are the expectations the decision supersedes (round 4's link-label control in the r4 to r7 runners, round 7's code-span comment control).
- **The new controls on round 8's check:** the same runner against round 8's check (`2eb5a24e...`, equal to `author-r8/tools/check_b16_figures.py`) and the page at `b522bb92`, exported with `git archive` (docs, scripts, tools/markdown) with `GIT_DIR` set: the 73 earlier PASS and the 24 new FAIL (`controls/r9-controls-on-r8-check.json`).
- **The reviews' probes, unchanged:** `<parser python> -I tools/r9_probe_reruns.py <repo> . tools/review-probes <scratch> cb5ff79f...` rc 0; each refused unless its SHA-256 equals the published one; results kept verbatim (`r9/*-probe-rerun.json`):
  - R624-8's `probe_r624_8_html_block_edge.py`: `intro_pre_from_line_above_with_figure` DETECTED, `MARKUP 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18 html_block <pre>`; no case escapes; every case keeps its exit status and verdict; `heading_pre_*`, `heading_comment_*` and `contents_pre_*` now also name the block at 2287 or 84;
  - the 13 earlier probes: readings equal to round 8's, but for R624-7's `footnote_ref_and` form, whose footnote definition, appended after the page's last line, is named at 4424 rather than 4274 as the page grew.
- **Further forms:** `<parser python> -I tools/r9_self_probes.py tools/check_b16_figures.py <page> . <scratch> r9/self-probes.json` rc 0: 156 forms, each meeting its expectation; 122 detected, 34 passing as stated; no form of rounds 5 to 8 changed its exit status, detection or verdict.
- **Where the packet is:** `python3 -I tools/r9_evidence_receipt.py <repo> b0134c63 b522bb92 r9/evidence-receipt.json` rc 0: `MANIFEST.json` at `b0134c63` (5,646 entries); `author-r8/` (771 entries, 57 path-redacted) last changed by `b0134c63` ("at b522bb92"); all 98 hash rows of the section at `b522bb92` equal their files in `author-r8/`; 770 of 771 files equal round 8's own MANIFEST.sha256 (the 771st is that manifest).
- **Byte-stable:** outputs generated in a scratch copy of the packet at `cb5ff79f`, installed, and regenerated in the packet: 54 files byte-equal; the probe records then ran a second time, 15 files byte-equal.
- **Gates at `cb5ff79f`:** all 14 rc 0 (gates/r9/, results.json, one log per gate, unpiped, physical /data path, Markdown gates in the pinned environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` (0 findings over 4,156 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check c20c85bd HEAD`. The same set ran rc 0 on the working tree before the commit.
- **Before the commit:** the added lines and every new packet file were scanned for every private-map entry, private environment value, private name, host, interface, address, capture-side value, home and temporary path, and tool or model name: the only hits are the redaction map's field words "literal" and "regex" in ordinary prose and code, as in rounds 6 to 8; the PR body's two hits are both in round 8's text (a hex run inside an earlier SHA-256, and a field word).

### Round 9 finding dispositions

| Finding | Lens (reviewer's) | Disposition | Where |
|---|---|---|---|
| R624-8-F1, MINOR | Conformance, Robustness, Tests, Docs | Fixed: each node judged by its source extent (`extents`): an html_block ends on its literal's last line; a node spans its descendants; a link or image starts a line higher per break in its text. Also fixed, same class, found while auditing every kind: a block whose lines the parser misplaces (backslash break, link or image target/title/label over a break, reference definition opening it) is refused whole; lines counted as the parser counts them (`lines_of`). R624-8's probe, unchanged: its case DETECTED at :18, html_block; 24 standing controls | `extents`, `blocks`, `lines_of`, `scope`; `controls/r9-controls.json`; `r9/r624-8-html-block-edge-probe-rerun.json`; `r9/parser-extents.json` |
| R624-8-S1, SUGGESTION | Docs, Tests | Taken as text: "What the rule does not cover" states the emoji shortcode and the link title. Not refused: that would change two of R624-8's own cases, which item 2 keeps | the page's round 9 subsection |
| R625-8-F1, MINOR | Conformance, Tests, Docs | Settled by the decision 6132293481; recorded in round 8's "Earlier expectations" paragraph and runner list and in round 9's "The decision"; the historical runners keep their code and recorded outcomes and are not reported as wholly green | the page; `controls/r9-rerun-r3-controls.json` to `controls/r9-rerun-r8-controls.json` |

### Round 9 step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| w0 | Context: the round 9 assignment, the decision, R624-8 and R625-8 in full; R624-8's probe and receipts from the evidence branch at `f4936667` | Read | this file |
| w1 | Node positions of every construct at and across line breaks, in scratch documents | Under-reported: html_block (ends at a closing marker), strikethrough (end), link and image (start when their text spans lines). Misplaced: everything after a backslash break, a link or image target/title/label over a break, a reference definition opening a paragraph | `r9/parser-extents.json` |
| w2 | Round 8's check on the page with such breaks above the introduction, and with a form feed on line 5 | The figure on line 18 unread in each; the page failed only through a shifted row | - |
| w3 | `extents`, the misplacement test, `lines_of` in a scratch copy of the check | Unchanged page: rows, coverage and output byte-equal to round 8's; R624-8's case DETECTED at :18 | `r9/reader-on-r8.json` |
| w4 | Round 9 controls (24), self-probes (18), probe reruns (with R624-8's), the parser-extents receipt, the evidence receipt | 97 of 97; 156 met; no escape | `tools/r9_*` |
| w5 | Round 9 text, pointers, location paragraph, decision record, index row; rows; rewording where the closed list refused new text | Page passes | the page; `tools/r9_figures_spec.py` |
| w6 | Size: the check over 200 KB with round 9's code and rows | `BC`, `PT`, `tones(d)` and `passed(d)` in row keys (rows otherwise unchanged), the check's own documentation condensed; 199,529 bytes | `tools/check_b16_figures.py` |
| w7 | Fixed point over the hash table and controls | Stable on the second pass | - |
| w8 | Gates on the working tree, privacy scan, commit `cb5ff79f`, gates at the head | Every gate rc 0 | gates/r9/ |
| w9 | At `cb5ff79f`: outputs in scratch, installed, regenerated in the packet; probes run twice | 54 files byte-equal; 15 probe files byte-equal on the second run | `r9/`, `controls/` |
| w10 | HANDOFF.md, PR-BODY.md (Round 9; header, commit list), REVIEW-READY-r9.md; the three scanned for private terms | Written; no hit in the round 9 text | this directory |
| w11 | REVIEW READY on #629 | POSTED 00:17:00 CEST, 2026-10-13 (comment 6133625420); readback equal but for one trailing newline | REVIEW-READY-r9.md, REVIEW-READY-r9.readback.md, review-ready-r9-url.txt |
| w12 | MANIFEST.sha256 over every packet file but itself; no packet file over 200 KB | Written | MANIFEST.sha256 |

### Round 9 tool changes

| Tool | Bytes | SHA-256 | Change |
|---|---|---|---|
| tools/check_b16_figures.py | 199,529 | `bafea39b3af1d6ba654cfbfc8c2feaf30e147a0abb5e8226650108d1e3238f11` | Edited from round 8's (`2eb5a24e...`, published as `author-r8/`): `lines_of` (lines as the parser counts them) used by `scope` and `blocks`; `extents` (each node's source extent and the parser's last line under it); `blocks` judges every node by its extent, refuses a leaf whose parser lines fall short of its source (`LOST`), names refusals with their reason (`OFF`, `LOST`) and places an unresolved target at its first covered line; `packet_path` accepts `author-r9`; `BC`, `PT`, `tones` for row keys; docstrings and comments condensed; ROWS_TSV and EXCLUDE regenerated from the round 9 spec |
| tools/r9_figures_spec.py | 164,406 | `857a99905d04e00dfdababd641cd94f8c96aefb2ad152d15b401439f517cd45a` | New, a copy of `r8_figures_spec.py`: review names to round 8, packet directory to `author-r9/`, commit `b522bb92` in the commit list; `passed(d)`, `BC`, `PT`, `tones(d)` in keys (string literals only; every row's line, figure, receipt and value unchanged); rows for round 8's packet location and round 9's figures |
| tools/r9_figures_build.py | 5,464 | `6a96840c61ebdf57acb1b7b131a508ef89e246c14fb3be620d8c000bd2b14d62` | New, `r8_figures_build.py` unchanged but for its name and docstring |
| tools/r9_check_controls.py | 43,115 | `11fc340920756e9e86dbe415f132b1eac204c8c5bcca4ce70114e5be09072c1e` | New, a copy of `r8_check_controls.py`: the 73 controls unchanged; 24 round 9 controls, each replacing whole lines |
| tools/r9_probe_reruns.py | 15,043 | `05deed808a213deb448a8d08ab0891f539a6283147f551aef39462ef7367cb8a` | New, a copy of `r8_probe_reruns.py` with R624-8's probe; results to `r9/` |
| tools/r9_self_probes.py | 12,100 | `5a42d8018b72e4c0d2d6ee6aeef398ea7245e0c76f56e01812406971c89097fe` | New: round 5's to round 8's forms read from their files, then round 9's 18, with a line-replacing mode |
| tools/r9_evidence_receipt.py | 7,868 | `681dc44a5272671ccbce6d1f87cecbf2d812f4c3f47b3175d674f602881487fb` | New, `r8_evidence_receipt.py` unchanged but for its name, docstring and note |
| tools/r9_parser_extents.py | 6,592 | `d26cdd914e6da3916adcc64782e357bed4e22a18192adc5fffa5b2593a078885` | New: 37 documents with their true lines, through the check's own `tree` and `extents` |
| tools/r9_reader_on_r8.py | 3,002 | `5641dd595603005e472e94f7ddb290bacbdfcb0b376ed44c9058e161bb34e6e0` | New: round 9's reader with round 8's rows on the page at `b522bb92`, against `r8/` |
| tools/review-probes/probe_r624_8_html_block_edge.py | 5,117 | `106710c3213e985d6a59eb212444b7ac8056664c59b9e3ae24c610c48c03424f` | R624-8's script, copied unchanged from the evidence branch |

The round 8 tools are unchanged; `r8_figures_spec.py` and `r8_figures_build.py` reproduce round 8's check, published as `author-r8/tools/check_b16_figures.py`, not the one now in `tools/`. The parser environment, the scratch packet copy, the regeneration driver and the private scan stay outside the packet.

### Round 9 deviations and decisions

- **Beyond the literal finding (same class, published).** Item 1 asks for every node kind whose end the parser may under-report. The audit (`r9/parser-extents.json`) found the html_block, struck text, and links and images whose text spans lines. It also found that a backslash line break, a link's or image's target, title or reference label over a line break, and a reference definition opening a paragraph make the parser place every later node in that paragraph on an earlier line. Round 8's check then dropped the introduction's first covered line when such a break stood above it. The page failed only through a shifted row, which a careful edit could also shift. Correcting those positions would mean imitating the parser, so the check refuses such a block whole, named by its kind with its own reason. It also found that `str.splitlines` splits at characters the parser reads as text; the check now splits lines as the parser does.
- **R624-8-S1 as text, not refusal.** Refusing `:word:` or link titles would turn R624-8's `emoji_shortcode_*` and `link_title_*` cases from PASS to FAIL, against item 2's "every other case keeps its outcome".
- **Outcomes kept, MARKUP added.** R624-8's heading and Contents cases keep exit 1 and their verdicts; each now also names the block at its covered line, where round 8 failed them only through a lost row.
- **Size.** Round 9's code and rows took the check over 200 KB. The row keys name the two most-looped case pairs once (`BC`, `PT`) and a grade's tone pair (`tones(d)`), and use `passed(d)` for round 8's control sums. The replacements were made in string literals only. Each row's line, figure, receipt, precision and value are unchanged (`r9/figures-rows.tsv` holds no key). The check's documentation was condensed; the page states every rule.
- **Bytecode.** `tools/r9_parser_extents.py` imports the check; run with `-B` so no `__pycache__` lands in the packet.

### Round 9 posted

- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6133625420 (posted 00:17:00 CEST, 2026-10-13, with the head, the item table, the choices, the check's results and the file hashes; REVIEW-READY-r9.md, review-ready-r9-url.txt; REVIEW-READY-r9.readback.md equal but for one trailing newline).
- After it: nothing running; the bench lock never taken in this round.
- TAKEN was not posted again; no existing comment was edited or deleted; nothing pushed; no PR edited.

### Round 9 packet layout (additions)

| Path | What |
|---|---|
| REVIEW-READY-r9.md, REVIEW-READY-r9.readback.md, review-ready-r9-url.txt | The round 9 post and its readback |
| tools/r9_figures_spec.py, tools/r9_figures_build.py, tools/r9_check_controls.py, tools/r9_probe_reruns.py, tools/r9_self_probes.py, tools/r9_evidence_receipt.py, tools/r9_parser_extents.py, tools/r9_reader_on_r8.py | The round's new tools; tools/check_b16_figures.py edited |
| tools/review-probes/probe_r624_8_html_block_edge.py | Round 9's review probe, unchanged |
| r9/figures-rows.tsv, r9/figures-coverage.tsv, r9/figures-check.stdout, r9/build.stdout | The check's output at the head, and the build's |
| r9/parser-extents.json, r9/parser-extents.stdout | What the parser reports, per kind |
| r9/reader-on-r8.json, r9/reader-on-r8.stdout | Round 9's reader with round 8's rows on round 8's page |
| r9/evidence-receipt.json, r9/evidence-receipt.stdout | Where the packet is published, rounds 1 to 8 |
| r9/*-probe-rerun.json, r9/probe-reruns.stdout | The 14 review probes against the new check |
| r9/self-probes.json, r9/self-probes.stdout | Further forms against the new check |
| r9/key-scan.json | Row keys' loop variables |
| r9/controls.stdout, r9/controls-on-r8.stdout, r9/rerun-r3.stdout to r9/rerun-r8.stdout | The runners' standard output |
| controls/r9-controls.json, controls/r9-controls-on-r8-check.json, controls/r9-rerun-r3-controls.json to controls/r9-rerun-r8-controls.json | The check's controls |
| gates/r9/ | Gate logs and results at `cb5ff79f` |

## Round 10 (2026-10-13)

[A603]. Documents only under assignment 6134101205. Resumed after an external interruption; source head cb5ff79f1f69117efba353484851eceb620e5c92. No bench action or lock acquisition in this round. New commit only, no push. Round 10 REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6135221777. Local commit: f1b2489f5b1c929e81eeae79a469b2b27c47e340.

| Cycle | Work | Result | Evidence |
|---|---|---|---|
| r10-resume-0 | Inspect status, diff, history, packet and public assignment/reviews | Two Markdown files changed; partial checker and receipts retained in scratch; final packet still at round 9 | Assignment 6134101205; reviews 6134093761 and 6133964452 |
| r10-resume-1 | Audit position refusal, digit conservation and controls | Stable-packet rerun passes all 97 unchanged round 9 controls. The eight scratch failures were stale receipt state; no expectation changed. Final controls complete: 117 of 117; earlier runners keep 5/5, 7/8, 21/22, 38/39, 48/50, 73/73 and 97/97. All 172 self-probes meet their expectations | Round 10 scratch receipts |
| r10-resume-2 | Gates, public wording, manifest and new commit | Local commit f1b2489f5b1c929e81eeae79a469b2b27c47e340. Head gates: all 14 entries rc 0. All 15 review probes finished; older outcomes retained. Final control repeat: 117/117, byte-equal | Round 10 gate receipts |
| r10-resume-3 | REVIEW READY with head, readback and final manifest | Posted once; readback equal; final manifest verified | Issue #629 comment 6135221777 |

Round 10 resumption: the earlier draft said 89 of 97 and incorrectly grouped those eight failures with the superseded expectations. The unchanged runner on the stable draft returned 97 of 97; its actual receipt replaced the stale scratch receipt, and the text/spec now say 97 of 97. Missing-start handling was extended to a block itself and enclosing structural nodes. Parser-output controls pass for those cases and digit loss, duplication and substitution. R624-9-R1 is corrected in PR-BODY.md; both R625-9 manager corrections remain.

### Round 10 tool changes

All changes are in the packet; the repository delta remains two Markdown files. Earlier tools and reviewer probes remain unchanged except the current checker.

| File | Change |
|---|---|
| `tools/check_b16_figures.py` | From round 9: whole-block refusal for missing source starts; independently rendered digit conservation; the pinned HTML parser is loaded; round 10 rows and identifiers. Missing starts on blocks and enclosing structure are refused too. |
| `tools/r10_figures_spec.py` | Copy of round 9: packet mapping through round 9, round 10 figures and receipts; no bench value changed. |
| `tools/r10_figures_build.py` | Copy of round 9: removes unnecessary spacing in row keys, asserting identical Python syntax trees to keep the checker below 200 KB. |
| `tools/r10_check_controls.py` | Round 9's 97 controls unchanged, plus 20 autolink, boundary, conservation and later-line controls. |
| `tools/r10_probe_reruns.py` | Copy of round 9: adds R624-9's unchanged probe and records refusal lines. |
| `tools/review-probes/probe_r624_9_autolink.py` | Unchanged published R624-9 original, SHA-256 checked against the evidence branch. |
| `tools/r10_parser_extents.py` | Round 9's 37 cases unchanged; adds 22 position cases, including zero-position autolinks and fully positioned controls. |
| `tools/r10_self_probes.py` | Earlier forms retained; adds round 10 autolinks, boundary and rendering cases. |
| `tools/r10_layers.py` | New: removes each of the two rules separately to show its contribution. Missing-position mutation disables the shared predicate, including structural checks. |
| `tools/r10_reader_controls.py` | New during resumption: in-memory parser-output mutations for missing starts and digit loss, duplication and substitution. |
| `tools/r10_reader_on_r9.py` | Copy of the previous round's comparison, one round forward; compares unchanged-page outputs byte for byte. |
| `tools/r10_evidence_receipt.py` | Copy of round 9, extended to verify the round 9 publication pin and file mapping. |

The new checker is 199,268 bytes. All final file sizes and hashes are in MANIFEST.sha256. Scratch trees, parser environments and regeneration drivers remain outside this packet. The Markdown gates use the assigned pinned environment; isolated checker runs use the retained environment installed from the same hash-locked requirements. No packages were installed in this resumption.

### Round 10 completion evidence

| Cycle | Work | Result | Evidence |
|---|---|---|---|
| r10-resume-4 | Final receipt installation and hash-table update | Stable page: 1,960 rows equal, 15,597 digits covered, no refused block | r10/figures-check.stdout; rows and coverage TSVs |
| r10-resume-5 | New commit, exact-head gates and final control repeat | One new local commit, all 14 gate entries rc 0; 117/117 controls and byte-equal receipt | gates/r10/results.json; controls/r10-controls.json |
| r10-resume-6 | Unchanged review probes and comparison | R624-9: original passes, 14 changes reject; all 14 older outcomes retained, only appended footnote line 4426 to 4604 | r10/*-probe-rerun.json; r10/probe-comparison.json |
| r10-resume-7 | Install complete packet; regenerate checker; reconcile reader hashes | Final packet passes; checker rebuild and prior-page reader comparison byte-equal; no unused key variable | r10/reader-on-r9.json; r10/key-scan.json |
| r10-resume-8 | Public comment, readback and final manifest | Posted 2026-10-13T00:24:27Z; readback equal; manifest regenerated | REVIEW-READY-r10.md; REVIEW-READY-r10.readback.md |

`tools/r10_compare_probes.py` is a new offline comparison: it checks earlier probe hashes, exits and outcome fields and retains every reading difference. No reviewer probe was edited. The first packet check during installation refused the not-yet-copied autolink receipt path; after completing the copy, the final packet check passed. No source edit was needed.

`r10/source-files-before-hash-update.json` identifies the full-run draft; `r10/source-files.json` identifies the committed files after updating the control receipt hash. The exact-head standing-control repeat is byte-equal to the receipt that the page hashes. All earlier runner outcomes, the 172 self-probes and 59 parser audit cases were retained and verified. The renderer versions match between environments; the assigned gate environment inherits pycparser 3.1 while the isolated checker uses the lock's 3.0, recorded in r10/parser-environment.json. No environment was changed.

No bench action or lock acquisition, push, PR edit, merge, rebase, amend, new checkout or delegation occurred. The existing restore evidence is unchanged. Remaining issue items: Direction B INTERNAL mismatch control, B6 timed ratio for B-CRF/B-AAF, and #645. Publication and independent re-review remain with the manager.

Round 10 post: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6135221777 (2026-10-13T00:24:27Z). Readback matches the submitted body up to its trailing newline. All foreground validation commands finished. No bench lock was acquired in this round.
