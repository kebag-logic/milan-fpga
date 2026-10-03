# [A519] Bench lane B7 handoff

Refs #629, bench acceptance on dev `bbf704ec` (PR #634 merged): media-clock following graded by THD+N and the frame-rate ratio.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5969106115
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5969120739
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5969917459
- Posted on #629: TAKEN and REVIEW READY only; no existing comment was edited or deleted.
- Branch: `629-b7-bench` from dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`, lane worktree on the physical /data path.
- Image under test: the manager's build of dev `bbf704ec`, as installed (flashed 13:16 CEST, cold power cycle 14:20 CEST).
- Packet: this directory. Raw files stay outside it under /tmp/b7-a519/raw; private endpoints under /tmp/b7-a519/private (not in the packet).

## State

**DONE** (2026-10-03, 14:22-16:05 CEST). Bench work ran 14:28-15:50 CEST; every case was restored and read back; the bench lock is free; no task process remains on this host, the controller host or the SoC board.

- Commit `4eee41a558a56024e57b27a956fdaf7910ca69dc` on `629-b7-bench`: one commit on `bbf704ec`, one-line subject, no body, no trailers. Local, not pushed, no PR; the worktree is clean. It adds the dated section "Dev bbf704ec, 2026-10-03: lane B7" (and its Contents line, a pointer line in the intro and the two-image title) to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, and updates its row in `docs/findings/README.md`; no other doc edit.
- Every gate rc 0 at `4eee41a5` (gates/gates.txt); the bare `check_baremetal_only.py` without a mode is a usage error, rc 2, so it ran with `--check` and `--selftest`, as in lane B6. The same gates on the uncommitted worktree are in gates-worktree/.
- Verdicts (operator measurements): identity PASS; tool controls PASS; A0 PASS as a control; A1 PASS; A2 PASS; B0 PASS as a control; B-CRF PASS; B-AAF PASS; the lock loss observed as declared; Direction B THD+N NOT RUN (no known signal, probe repeated).
- #629: not every acceptance item is met (Direction B's THD+N; no bench evidence for the stream-to-stream switch, a followed CRF stream's lock loss or the saved selection across a power cycle), so the PR body says "Refs #629".

## Step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only) | #629 and its [A10] rulings, PR #634's design page, B6's findings page and packet, B5/B4/B3/B2/75/117 packets (skimmed for rules), the register map's 0x8E0/0x8F8 sections, the meter RTL header | this file |
| 1 | TAKEN on #629 | POSTED 14:24; readback equal but for one trailing newline | TAKEN.md, TAKEN.readback.md, taken-url.txt |
| 2 | Local preconditions | PASS 14:27: board-link address present on this host; both USB audio cards present (UAC2, external capture); the three serial adapters present; no process holds any console | - |
| 3 | Controller survey (locked, read-only) | 14:28: AVB port identified; no gPTP daemon; no staging; sudo ok | (private) |
| 4 | ADP discovery (locked) | 14:28: DUT (entity model `001bc5c1935893e1`) and the reference peer | (private) |
| 5 | Identity gate | **PASS** 14:29:50-14:30:19: VERSION `00020060`; console CRCs equal the build's: AEM image 7,512 B `5ba355eb`, BIOS ROM 53,588 B `2144df1c`, QSPI bitstream payload 3,825,788 B `e6b8febc`; QSPI AEM bytes and all 12 live AECP descriptors byte-equal to the build's AEM image; CLOCK_SOURCE 0 INTERNAL, 1 INPUT_STREAM on STREAM_INPUT 1 (CRF), 2 INPUT_STREAM on STREAM_INPUT 0 (AAF); CLOCK_SOURCE 3 NO_SUCH_DESCRIPTOR; CLOCK_DOMAIN 0 lists 0, 1, 2 and reads 0; grader 10/10; ADP model ID equal | identity/ |
| 6 | SoC console | 14:32:28 one carriage return: root prompt; 14:32:37 `id` over the board link: uid 0; uptime 270,576 s (same boot as lane B6) | soc/peek.log, soc/shell-check-net.log |
| 7 | Start baseline and surveys | 14:32:57-14:33:04, all rc 0 | restore/*-start*, restore/peer-descs.jsonl, restore/dut-descs.jsonl, soc/start-health.log |
| 8 | Tool and synthetic controls | PASS (offline, 14:37), byte-equal to lane B6's | controls/ |
| 9 | Grading criteria fixed | 14:50, before any graded case | "Grading criteria" below |
| 10 | Shakedown `smoke-baaf`, cases A0, A1, A2, B0, B-CRF, B-AAF (with the lock-loss observation), the known-signal probe | 14:39-15:49, each one locked action, each restored and read back | runs/<case>/, summary/<case>/ |
| 11 | Restore and proof | 15:49-15:50: legs restarted, end snapshot, census compare 45/46, grader 10/10 | restore/*-end*, restore/census-compare.txt, soc/s02-start-legs.log, restore/grader-end.txt |
| 12 | Grading, absorption checks, tables | all six cases graded with the final grader; verdicts computed from the fixed criteria | summary/, summary/verdicts.json, summary/checks/absorb.jsonl |
| 13 | Redaction | one pass (repeated once, idempotent) over 227 packet files, tools included; token and decoded-payload scans clean | redaction.json |
| 14 | Findings section, index row, gates, commit | `4eee41a5`, every gate rc 0 | gates/ |
| 15 | REVIEW READY on #629 | POSTED: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5969917459 (head `4eee41a5`); the readback equals the posted text but for one trailing newline | REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 14:28:00 | Controller host: interfaces, processes, staging, sudo (read-only) | rc 0 |
| 14:28:09-14:28:14 | Controller: stage the read-only probe; ADP discovery | rc 0; DUT and peer seen |
| 14:29:50-14:30:19 | Identity gate (identity_b7.sh) | all rc 0; PASS |
| 14:32:28-14:32:32 | SoC console peek (one carriage return) | root prompt |
| 14:32:37-14:32:38 | SoC `id` over the board link | uid 0 |
| 14:32:57-14:33:04 | Start baseline (baseline_b7.sh start): SoC health, DUT reads, census, counters, peer and DUT descriptor surveys, controller, host view | all rc 0. Bridge legs to-host 23634 and from-host 23635 with the script's command lines (lane B6 left 22949/22950: restarted since by others); McASP0 playback XRUN since board uptime 164,054 s; UDC configured; BAD=1 (one dmesg line matching the fault scan, present as found). DUT: all unbound, maps empty, CLOCK_DOMAIN 0 on 0, STREAM_INPUT 0 `0205022002006000`; `MCSRV_STAT` 0x20, AAF meter 0, SLIP_TDM 0. Peer: all unbound, on source 0; its sources 3 (STREAM_INPUT 0, AAF) and 1 (STREAM_INPUT 8, CRF) as in lane B6 |
| 14:39:14-14:39:20 | SoC bridge legs 23634/23635 stopped by PID (command lines checked against status) | KILLED; all four PCMs closed; UDC configured; BAD=1 unchanged; both USB audio cards still on this host |
| 14:39:27-14:41:33 | run_b7.py `smoke-baaf` (B-AAF, 60 s window; tool shakedown, not graded) | ACTION_RC 0. DUT STREAM_INPUT 0 took the peer talker's `0205022001006000` (SUCCESS, read back); binds SUCCESS; DUT SET_CLOCK_SOURCE 2 SUCCESS, read back 2; servo LOCKED 6.6-7.1 s after the set (meter locked under 0.56 s, rate valid 4.1-4.6 s); lock loss: HOLDOVER within 0.56 s of the unbind, trim held, GET_CLOCK_SOURCE 2 throughout, LOCKED 6.1-6.6 s after the rebind, DUT AAF output MEDIA_RESET 1 -> 2 -> 2, CLOCK_DOMAIN LOCKED/UNLOCKED 2/1 -> 2/2 -> 3/2; teardown: DUT source 0 read back, unbinds, both listener formats restored and read back, map read back empty |
| 14:41:42-14:52:47 | run_b7.py `a0` (A0, 630 s window) | ACTION_RC 0. Peer and DUT on source 0 (as found); peer format set 4 ch to 8 ch SUCCESS and read back; bind SUCCESS; tone valid 0.2 s after the bind; teardown: unbind, peer format restored and read back, map read back empty, clock sources read back 0 and 0, every RX state unbound |
| 14:52:53-15:03:57 | run_b7.py `a1` (A1, 630 s window) | ACTION_RC 0. Peer format set 4 ch to 8 ch SUCCESS and read back; bind SUCCESS; peer SET_CLOCK_SOURCE 3 (its source on STREAM_INPUT 0) SUCCESS, read back 3; teardown: peer source set back to 0 and read back 0, unbind, peer format restored and read back, map read back empty |
| 15:04:02-15:15:07 | run_b7.py `a2` (A2, 630 s window) | ACTION_RC 0. Peer format set 4 ch to 8 ch SUCCESS and read back; AAF bind SUCCESS; CRF bind DUT STREAM_OUTPUT 1 to peer STREAM_INPUT 8 SUCCESS (formats equal, no set); peer SET_CLOCK_SOURCE 1 (its source on STREAM_INPUT 8) SUCCESS, read back 1; teardown: peer source back to 0 and read back 0, both unbinds SUCCESS, peer format restored and read back, map read back empty |
| 15:15:16-15:26:20 | run_b7.py `b0` (B0, 630 s window) | ACTION_RC 0. AAF bind DUT to peer (peer format set and read back); CRF bind peer STREAM_OUTPUT 2 to DUT STREAM_INPUT 1 (formats equal); AAF bind peer STREAM_OUTPUT 0 to DUT STREAM_INPUT 0 (DUT format set 8 ch to 4 ch SUCCESS, read back); DUT left on source 0; teardown: three unbinds SUCCESS, peer and DUT formats restored and read back, map read back empty, sources 0 and 0 |
| 15:26:28-15:37:33 | run_b7.py `bcrf` (B-CRF, 630 s window) | ACTION_RC 0. Binds as B6 (AAF DUT to peer with the peer's format set and read back; CRF peer to DUT STREAM_INPUT 1, formats equal); DUT SET_CLOCK_SOURCE 1 SUCCESS, read back 1; servo LOCKED 3.1-3.6 s after the set; teardown: DUT source back to 0 and read back 0, both unbinds SUCCESS, peer format restored and read back, map read back empty |
| 15:37:41-15:49:15 | run_b7.py `baaf` (B-AAF, 630 s window, then the lock-loss observation) | ACTION_RC 0. AAF bind DUT to peer (peer format set and read back); AAF bind peer STREAM_OUTPUT 0 to DUT STREAM_INPUT 0 (DUT format set 8 ch to 4 ch SUCCESS, read back); DUT SET_CLOCK_SOURCE 2 SUCCESS, read back 2; servo LOCKED 6.6-7.1 s after the set. Lock loss after the window: unbind SUCCESS, HOLDOVER within 0.06-0.56 s, 12 s of polling, rebind under the binding rule (formats equal), LOCKED 5.6-6.1 s after the rebind; GET_CLOCK_SOURCE 2 at each step. Teardown: DUT source back to 0 and read back 0, both unbinds SUCCESS, peer and DUT formats restored and read back, map read back empty |
| 15:49:27-15:49:49 | probe_b7.py `probe` (Direction B known-signal probe, B6's method) | ACTION_RC 0. Binding rule: DUT STREAM_INPUT 0 set to the peer talker's `0205022001006000` SUCCESS, read back; four identity mappings on DUT STREAM_PORT_INPUT 0; bind SUCCESS; 2 s McASP0 capture reduced on the board: channels 0-3 -2 to 0 LSB (mean square 0.49-0.54), 4-7 zero; teardown: unbind, mappings removed and read back empty (as found), DUT format restored and read back, recording removed |
| 15:49:54-15:49:58 | SoC bridge legs restarted with the two recorded lines | STARTED: to-host 15379, from-host 15380; PCM states as at the start (McASP0 playback XRUN, capture RUNNING); UDC configured; BAD=1 unchanged |
| 15:50:07-15:50:14 | End snapshot (baseline_b7.sh end) and controller staging removal | all rc 0; staging removed, no task process on the controller |
| 15:50:14 | UART grader | 10/10 |

## Grading criteria (fixed 14:50 CEST, before any case ran)

B6's rules unchanged (window at least 630 s, from 20 s after the last bind or clock-source set, and for a DUT-following case after the servo reads LOCKED, untouched; B6's attribution with its refinements), except where stated:

- Tool controls: PASS when every planted defect is found at its exact size and position and the clean capture sits at the floor (re-run; must be byte-equal to B6's `controls.json`). **Result: PASS, byte-equal (`7bbefc71`).**
- A0 (control): PASS when the metric shows the DUT and the peer apart: the listener's net discontinuity rate beyond 2 ppm in magnitude, with blocks free of discontinuities at the floor. *Change, stated:* B6 asked for "the order B5 measured (about 16 ppm)"; under D4 = A2-a the DUT's AAF stream runs on its physical audio clock, so the expected magnitude is the physical clock against the peer (about 6.5 ppm in B6), not 17 ppm.
- A1, A2: PASS when the window holds 0 listener discontinuities, every block free of discontinuities sits at the 24-bit floor within 0.01 dB, the fitted offset on those blocks is under 0.001 ppm in magnitude, and the set clock source read back. Reported beside it, as A2-a evidence: the DUT's SLIP_TDM and the DUT-beat count.
- B0 (control): PASS when the counted McASP0-to-peer ratio is beyond 2 ppm in magnitude.
- B-CRF: PASS when the DUT servo reads LOCKED, the counted ratio is within 0.5 ppm of zero, the timed ratio's interval holds zero, and the tone path holds 0 listener discontinuities (B6's).
- B-AAF: B-CRF's four conditions, and the design's bench row (`docs/design/MEDIA_CLOCK_FOLLOWING.md`, Test plan, Bench, "B AAF"): the servo LOCKED within 15 s of the set and at every DUT read in the window (every 30 s), with the CLOCK_DOMAIN's LOCKED and UNLOCKED counters unchanged across the window; SLIP_TDM static; the meter's history-restart count unchanged across the window. Recorded: the set-to-LOCKED time and the meter's largest timestamp deviation.
- *Attribution change, stated:* a one-frame repeat counts as the DUT's beat only when the DUT's SLIP_TDM moved in the window (B6: cross-check only). With SLIP_TDM static every repeat is the listener's. It can only make a verdict stricter.
- Observations, not graded: (a) the B-AAF lock loss against the design's "Lock loss, holdover and restart" and "`mr`" sections; (b) the DUT's INTERNAL media clock against the peer (A0 and B0 ratios) with the oscillator grade as a known risk.

## Run ledger (one row per case)

| Case | Window start | Window | Result |
|---|---|---|---|
| Tool controls (synthetic) | 14:37 CEST | offline | PASS, byte-equal to lane B6's `controls.json` |
| A0 as found | 14:42:08 CEST | 630.31 s | PASS as a control: 470 one-frame listener drops and 291 silent one-frame inserts, net +5.92 ppm; counted McASP0/peer ratio +5.916 ppm, timed +5.71 +-0.55 ppm; SLIP_TDM static over 600 s and 0 DUT beat repeats (A2-a: B6 had 321); 444 of 630 blocks at the floor (within 0.0004 dB); capture path 15 events in 7 clusters, 5,058 frames |
| A1 AAF following | 14:53:19 CEST | 629.88 s | PASS: 0 listener discontinuities, 0 DUT beat repeats, SLIP_TDM static; 597 of 629 blocks at the floor (within 0.0003 dB), fitted offset at most 2.3e-7 ppm; counted ratio 0.000 (0 net steps in 30,234,240 frames; B6: -10.631, the beat), timed -0.28 +-1.40 ppm; capture path 37 events in 32 clusters, 5,580 frames |
| A2 CRF following | 15:04:29 CEST | 628.04 s | PASS (B6 failed it: 494 drops, 180 inserts): 0 listener discontinuities, 0 DUT beat repeats, SLIP_TDM static; 578 of 628 blocks at the floor; counted ratio 0.000 (0 net steps in 30,145,920 frames), timed +2.15 +-4.42 ppm (a 2.15 s read stall widens it); capture path 62 events in 53 clusters, 112,533 frames. Disclosed: two capture-path clusters are 2 and 1 frames short of the 48 n + 12 signature (a 2.1 s loss, and a 59-frame skip); each could hold a merged listener repeat or a short packet of the asynchronous capture interface (it delivers 0.5-0.8 frames/s under 48 kHz on this host's clock) |
| B0 INTERNAL control | 15:15:42 CEST | 629.55 s | PASS as a control: counted ratio +5.924 ppm, timed +5.62 +-0.44 ppm; servo IDLE; CRF sink locked, peer CRF +11.03 to +11.06 ppm against gPTP; SLIP_TDM static; the DUT's listener loopback ring (`SLIP_LB`) +342 dups in 600 s, 2 per slipped frame on the 4-channel stream = +5.94 ppm; tone path 457 drops and 278 silent inserts by the peer, net +5.92 ppm |
| B-CRF following | 15:26:55 CEST | 628.53 s | PASS: servo LOCKED 3.1-3.6 s after the set and at all 21 reads in the window, trim -6.00 to -5.94 ppm (bit 4, DRP config mismatch, set from ACQUIRE on, as in B6); counted ratio 0.000 (0 net steps in 30,169,440 frames), timed +1.98 +-6.52 ppm (holds zero; an 883 ms read stall widens it); 0 listener discontinuities; 559 of 628 blocks at the floor; SLIP_TDM static; CLOCK_DOMAIN LOCKED/UNLOCKED 4/3 through the window; capture path 86 events in 69 clusters, 74,568 frames, every cluster on the 48 n + 12 signature |
| B-AAF following | 15:38:07 CEST | 627.74 s | PASS: servo LOCKED 6.6-7.1 s after the set (within the design's 15 s) and at all 21 reads, trim -6.00 to -5.94 ppm; AAF meter locked with a valid rate at every read, rate +11.018 to +11.043 ppm (the peer's AAF media clock against gPTP), history restarts 0 -> 0, largest deviation 29 ns; counted ratio 0.000 (0 net steps in 30,131,520 frames), timed -1.49 +-11.64 ppm (holds zero; a 1.2 s read stall widens it); 0 listener discontinuities; 564 of 627 blocks at the floor; SLIP_TDM static; CLOCK_DOMAIN 5/4 through the window. Disclosed: three capture-path clusters one frame short of 48 n + 12. Observation outside the criteria: the DUT listener's `SLIP_LB` 386 -> 388 between 1 s and 31 s into the window, then static for 570 s |
| B-AAF lock loss (observation) | 15:48:38 CEST | 30.0 s | As declared: HOLDOVER within 0.06-0.56 s of the unbind, trim held at -5.94 ppm, GET_CLOCK_SOURCE 2 throughout; DUT AAF output MEDIA_RESET 1 -> 2 at the loss, 2 after the return (no second toggle); the peer's received MEDIA_RESET the same; CLOCK_DOMAIN 5/4 -> 5/5 -> 6/5; the DUT's STREAM_INPUT 0 MEDIA_UNLOCKED 0 -> 1; meter locked 0.05-0.55 s after the rebind, rate valid 4.07-4.58 s, servo LOCKED 5.58-6.08 s; tone path through it: 0 discontinuities of any kind, counted ratio 0 |
| Direction B known-signal probe | 15:49 CEST | 2 s | No known signal, as in B6: the peer's talker channels carry -2 to 0 LSB; Direction B THD+N NOT RUN |

## Deviations and incidents

- **DUT saved state at the update.** The identity readback shows both NVM slots `VD_SHAPE`, seq 0, 0 commits: the new image refused the old saved state once, as the design's Limits state ("Every unit loses its saved state once when the regenerated image first boots").
- **Identity gate against the build.** The assignment names "the build's design identity". The gate compared the console CRCs (AEM image, BIOS ROM, QSPI bitstream payload, over the build's own sizes) and every live descriptor with the build directory's outputs (identity/expected.json records the values and their source).
- **Long actions.** Each case ran as one tracked action with an explicit deadline (1,100 s; B-CRF 1,300 s; B-AAF 1,500 s) under the lock, detached so that no foreground command exceeded 10 minutes; every other command ran in the foreground with its own deadline, and the session polled until each action ended.
- **SoC console.** No other process held it in this session (lane B6 met the manager's terminal). Lane B6's `soccon_net.py` (reply over the board link) was kept, with its tag prefix changed.
- **Grader changes during grading, before any verdict.** `grade_b7.py` gained the lock-loss segment option and a guard for a bootstrap too short to run (only that segment uses it) before A0 was graded. The `tone.repeats` double subtraction (a lane B6 summary slip) was fixed after A0's first grade; A0 was regraded. `b7_decode.py` gained the `SLIP_LB` decode while A1 ran; A0 was regraded with it. Every final grade is from the final tools.
- **`mr` observed through counters.** The DUT's talker MEDIA_RESET and the peer's received MEDIA_RESET (GET_COUNTERS) stand in for a wire capture of the `mr` bit; no tap capture was taken.
- **Off-signature capture clusters.** A2 (2) and B-AAF (3) have capture-path clusters one or two frames short of the 48 n + 12 signature; the findings page discloses them under lane B6's "What the attribution can absorb", item 1, with the conservative reading (both cases would fail).
- **Redaction of tools.** Two tools (`run_b7.py`, `grade_b7.py`, and lane B6's copies `run_b6.py`, `grade_b6.py`) name the external capture's channel layout; they are masked in the packet, so the packet copies record the tools as run and do not run. The originals stay private; redaction.json records both hashes, and the findings page cites the as-run hashes.

## Residuals

- SoC board bridge legs under new PIDs (15379 to-host, 15380 from-host).
- DUT NVM: `VD_SHAPE` seq 0 at the start, slots seq 17/16 `VD_OK` at the end, commits ok 17, failed 0, `pend=1`: the method's format, map and clock-source edits on the new image's first saved state.
- DUT counters that clear only on reset moved: `SLIP_LB` (0 to 390), `RENDER_STAT`, `CRF_RATE`, `CRF_STATUS`, `AAFM_RATE` (holds its last value).
- The DUT's CRF output's MEDIA_RESET read 1 from its A2 stream start on, with no source change (recorded on the page, not analysed).

## Open items for the owner

- **Direction B THD+N.** No known signal reaches the peer's talker channels without a wiring change (probe repeated: -2 to 0 LSB). #629's bench quality metric stays open for Direction B; the owner's question on feeding a known tone is pending.
- **Not run at the bench:** the design's "Switch" row (AAF to CRF and back while streaming), a followed CRF stream's lock loss, and the saved selection across a power cycle (no power cycle allowed in this lane).
- **One `SLIP_LB` slip after lock in B-AAF** (2 dups 14-45 s after the servo first read LOCKED, then none for 570 s), beside #632 (phase alignment). Not filed here (this lane posts only TAKEN, REVIEW READY and STOP).
- **DRP config mismatch bit** in `MCSRV_STAT` under CRF and AAF following, from ACQUIRE on, as lane B6 recorded.
- **The A2/B-AAF attribution.** Five capture-path clusters one or two frames off the size signature; a reviewer may weigh the conservative reading.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.md, TAKEN.readback.md, taken-url.txt | The TAKEN post and its readback |
| REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt | The REVIEW READY post and its readback |
| PR-BODY.md | Proposed PR body |
| identity/ | Console CRCs, NVM and QSPI AEM readback; AECP descriptor walk; ADP; grader; expected.json (the build's values); identity-verdict.txt; lock window |
| soc/ | SoC console peek and root-shell check; health at start and end; bridge stop and restart transcripts |
| runs/<run>/ | `smoke-baaf`, `a0`, `a1`, `a2`, `b0`, `bcrf`, `baaf`, `probe`: events, controller transactions (ctl.jsonl), DUT reads, console polls, SoC transcripts; runs/*-lock.txt the lock windows |
| summary/<case>/ | grade.json (without the per-event and per-block lists), events.csv, blocks.csv; summary/baaf-lockloss/ the lock-loss segment; summary/tables.md, summary/verdicts.json, summary/checks/absorb.jsonl |
| controls/ | The synthetic controls, byte-equal to lane B6's |
| restore/ | Census and counters start/end, census comparison, peer and DUT descriptor surveys, DUT reads start/end, controller state and cleanup, host view, grader end |
| tools/ | Every tool used; ORIGIN-B6.sha256 pins the lane B6 copies as taken |
| gates/, gates-worktree/ | Gate commands and outputs at `4eee41a5` and on the uncommitted worktree |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| RAW-ARTIFACTS.json | Every raw file under /tmp/b7-a519/raw by path, size and SHA-256 |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
