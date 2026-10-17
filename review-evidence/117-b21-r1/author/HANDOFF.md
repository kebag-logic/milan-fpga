# [A625] Bench lane B21 handoff

Refs #117, acceptance box 4, the audio continuity row (owner: passes before release).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821
- Image: dev `9ef71772` as installed (flash 2026-10-15). Not flashed, not power-cycled, not reset.
- Branch: `117-b21-bench` from dev `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`, lane worktree on the physical /data path. Findings docs only. Not pushed; no PR (PR-BODY.md holds the body).
- Packet: this directory. Large raw files stay under /tmp/a625/raw (round 1: RAW-ARTIFACTS.json, 65 files, gone after the host restarts; round 3: RAW-ARTIFACTS-r3.json, 82 files, 10,194,884,483 bytes). Private endpoints and private transcripts under /tmp/a625/priv (not in the packet).

## Round 3 (after the round-2 STOP 6217670001, from `acba86cf`)

Round 3 terms: the controller host is back (owner start about 2026-10-16 17:20Z). The round restarts at the identity gate and keeps the round-2 plan: the McASP capture-path self-test, then Directions A and B. The SoC board's console (root prompt) is the board path, with key-based SSH over its USB network as the fallback (not needed: the console stayed at a root prompt). A dated round-3 section. REVIEW READY or STOP on #117, with no new TAKEN. Bench captures run on the tap host and the SoC board. Host-side stalls are cross-check noise and do not grade.

### Round 3 state

**DONE: REVIEW READY posted** (2026-10-17 ~07:58Z), comment https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6231525820 (REVIEW-READY-r3.md, review-ready-r3-url.txt, REVIEW-READY-r3.readback.md: equal but for one trailing newline). Head `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b`, one commit on `acba86cf` (three on dev `4a9b5a2a`), one-line subject, no body, no trailers; `docs/findings/117_AUDIO_CONTINUITY.md` only (+334 lines: the round-3 section and its Contents entry). Gates: working tree r3/gates-wt4/ (9 rc 0; the earlier r3/gates-wt/ and r3/gates-wt3/ runs each found wording the gates refuse, fixed before the commit; r3/gates-wt2/ was clean before two later wording edits), head r3/gates-head/ (11 rc 0). Not pushed; no PR (PR-BODY.md updated). Bench lock free. Posted on #117 in round 3: this REVIEW READY only; no existing comment edited or deleted.

| Item | Verdict |
|---|---|
| Identity gate | PASS 11/11 at 2026-10-16 17:22Z, 2026-10-17 06:51Z (after the controller reboot) and 07:51Z (end) |
| Step 1, McASP capture-path self-test | CLEAN (630 s) |
| Step 2, Direction A (both taps, DUT CSRs, peer counters; external capture cross-check) | PASS |
| Step 3, Direction B (both taps, DUT CSRs, McASP capture) | PASS |
| Restarts, 20 cycles | PASS, 20/20 under 1 s |
| #117 audio continuity row | PASS as measured (operator measurement, not a review verdict) |

**Cut.** A bench host reboot at 2026-10-16 about 17:32Z ended the round after the identity gate (T2), the start baseline and the SoC board checks (T3, T4). /tmp was wiped again (the private environment and any staging). The owner restarted the controller host at about 2026-10-17 06:49Z. The resume re-ran the identity gate (the controller rebooted) and went on from the McASP self-test. Receipts reused: r3/restore/*-start* (as found, 2026-10-16 17:22Z), r3/soc/ (root shell and tool check). Superseded: r3/identity (by r3/identity2).

### Round 3 step ledger (UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| T0 | Context: the round-3 terms, #117 (no new comment since the round-2 STOP), this packet | Read | this file |
| T1 | Local preconditions (2026-10-16 17:21Z) | bench lock free; bench host up 5:14 (load 16-26, candidate bank); controller host up 1 min | r3/controller-reach.txt |
| T2 | Identity gate (round 1's method), 2026-10-16 17:22:28-17:22:34Z | **PASS 11/11** (superseded by T7) | r3/identity/ |
| T3 | Start baseline (baseline_b21r3.sh), 2026-10-16 17:22Z | all rc 0 | r3/restore/*-start* |
| T4 | SoC board root-shell and tool checks, 2026-10-16 17:23-17:24Z | root shell (`uid=0`); capture and playback tools 1.2.16, gzip, xz, sha256sum; no python; 409 MiB RAM, /tmp tmpfs 204 MiB | r3/soc/ |
| T5 | CUT: bench host reboot about 2026-10-16 17:32Z; /tmp wiped | - | this file |
| T6 | Resume preconditions (2026-10-17 06:51Z); private environment re-created from the packet's records | bench lock free; all PCMs closed; three serial adapters; controller host up 2 min, AVB link up, no gPTP daemon | this file |
| T7 | Identity gate after the controller reboot, 06:51:33-06:51:38Z | **PASS 11/11** | r3/identity2/, r3/identity2-lock.txt |
| T8 | Start baseline `start2`, 06:52:02-06:52:05Z | all rc 0; census 45/46 equal to `start` (DUT live propagation delay); both bindings in place, formats equal on each side (DUT SO0/peer SI0 `0205022002006000`, peer SO0/DUT SI0 `0205022001006000`); peer SI8 <- DUT SO1 (CRF); DUT SPI0 map stream ch 0-3 -> clusters 0-3, SPO0 8 identity; peer clock source 1 (CRF) | r3/restore/*-start2* |
| T9 | SoC board read-only look, 06:52:40Z | root shell; bridge to-host leg running (on McASP0 capture), from-host DEAD; the board's player (its audio server holds McASP0 playback in SETUP). The full-argument process list printed a third-party API key: redacted at once, and the transcript then moved out of the packet to the private directory (hash: r3/soc2/look.log.moved-to-private.sha256); later process lists use pid,comm only | r3/soc2/look.log.moved-to-private.sha256 |
| T10 | Tap probe, 3 s per link, 06:57:02-06:57:10Z | DUT link: DUT SO0 8 ch 8000 pps (idle word `0xffffff00`), CRF 500 pps, peer SO0 4 ch 8000 pps; peer link: the same. Peer SO0 carries independent low-level noise on all 4 channels (0, -1, -2 LSB): the as-found signal at the peer's talker inputs | /tmp/a625/raw/probe |
| T11 | Board check (mounts, McASP DMA rows, leg command line), 06:59:41Z | /tmp tmpfs 204 MiB, / ext4 52 GB free; McASP DMA rows `485c0100.dma-controller chan0/chan1` | r3/soc2/check2.log |
| T12 | Board prep, 07:00:17-07:01:06Z: the player's `stop.sh`; to-host leg PID 5145 killed after `status` and its command line matched the recorded line; stamper fetched over the USB link | stopped linker, player, audio server; stop.sh also unmounted its /etc/ssl/certs bind mount; all McASP0/gadget PCMs closed; stamper SHA-256 `666ee35a...` matches | r3/soc2/prep.log, deploy.log |
| T13 | McASP self-test dry run `mst-dry`, 20 s, 07:01:47-07:03:56Z | 2,000 reads, every read one period, 0 overruns, 0 stalls; buffer 16,320 (24,000 asked). The 1 Hz board sampler causes a ~0.3 ms early-read wobble every ~1.03 s (no loss) | r3/selftest/mst-dry/ |
| T14 | McASP self-test `mst-long`, 630 s, 07:05:05-07:16:24Z | **CLEAN**: 63,000 reads, every read one period (30,240,000 frames), 0 overruns, 0 stamper drops, read interval 8.9-11.1 ms, 0 stalls; drift +43.06 ppm, linear; 10 s floors within -3.50..+1.94 frames of the line (no permanent step). The short floor test (W=110, to span the sampler wobble) flags 9 groups of +6..+8 frames, each one sampler cycle missing from a window; the permanent-step check shows none is a loss | r3/selftest/mst-long/ |
| T15 | Direction A `dA`, 07:17:26-07:29:00Z (taps 07:17:32 + 650 s; pattern from 07:17:39) | **PASS** (cycle ledger) | r3/runs/dA/, r3/summary/dA-* |
| T16 | Direction B `dB`, 07:31:29-07:43:53Z (taps 07:31:30 + 650 s; McASP from 07:31:34 for 635 s) | **PASS** (cycle ledger) | r3/runs/dB/, r3/summary/dB-* |
| T17 | Restarts `rA`, 07:44:12-07:47:52Z (cycles 07:44:28-07:46:28) | **PASS 20/20 < 1 s** (cycle ledger) | r3/runs/rA/, r3/summary/rA-restart.json |
| T18 | Board restore, 07:48:38-07:51:20Z | task files removed; to-host leg restarted with the recorded line (PID 4975, pid file updated), from-host DEAD as found; the player's `run.sh`: up but its login failed (CA store missing: stop.sh's unmount); the CA bind mount recreated from the player's own directory; `stop.sh` (unmounts again), the mount, `run.sh`: logged in, no CA error since. McASP0 playback closed until the player plays (as found: held open in SETUP) | r3/restore/soc-*.log, player-*-lock.txt; player log lines in the private directory |
| T19 | End baseline, census compare, end identity gate, controller and tap cleanup, 07:51:36-07:51:57Z | all rc 0; census 45/46 equal to `start2` (DUT live propagation delay); outlets equal; identity PASS 11/11; controller /tmp/a625 removed (identity re-staged it; removed again), no task process, no gPTP daemon; tap host: no a625 file, no tcpdump | r3/restore/*-end*, r3/identity2-end/, r3/restore/final-cleanup.txt |
| T20 | DUT words start2 vs end | equal but for live counters (PDELAY 381->385, TAI, AAF_FRAMES/PAIRS, RENDER_STAT fill, 0x6E0 live words); NVM line equal | r3/restore/dut-start2.txt, dut-end.txt |
| T21 | Findings section, commit `867fb945` | +334 lines (section + Contents entry) | the diff |
| T22 | Gates | working tree 9 rc 0 (r3/gates-wt4/), head 11 rc 0 (r3/gates-head/) | r3/gates-* |
| T23 | REVIEW READY on #117 | Posted, comment 6231525820; readback equal but for the trailing newline | REVIEW-READY-r3.* |
| T24 | PR-BODY.md, RAW-ARTIFACTS-r3.json, MANIFEST.sha256 | Done | |

### Round 3 cycle ledger (one row per run)

| Run | Window (UTC) | What | Result |
|---|---|---|---|
| mst-dry | 07:01:51-07:02:11 | McASP self-test dry run, 20 s | 0 overruns, 0 stalls |
| mst-long | 07:05:09-07:15:39 | McASP self-test, 630 s, deficit-only | CLEAN (0 overruns, 0 stalls, every read one period, no permanent floor step) |
| dA | 07:17:32-07:28:22 | Direction A, taps on both links, DUT CSRs every 5 s, counters pre/mid/post, external capture cross-check | Wire: DUT link 5,198,452 packets, peer link 5,198,499, 0 sequence breaks, avtp_timestamp steps 124,999-125,020 ns, tv set; 30,951,504 pattern frames (644.8 s) in order, 0 repeats, 0 skips, 0 torn, 0 invalid; 5,198,372 common packets equal in header and payload; CRF 500 pps, 0 gaps; transit jitter -27.7..+23.9 us after the tap clocks' 13.07 ppm. DUT: SLIP_TDM 0 in all 128 samples, RENDER_STAT converged, fill 8-14, rails 0; AVTPRX_STAT/ERR static; AAF_FRAMES 7,999.9/s. Counters: DUT SO0 FRAMES_TX = peer SI0 FRAMES_RX = 5,245,516; only frame counters moved. External: 30,624,574 valid frames (638.0 s), 0 repeats, 0 skips, 0 zero, 0 torn, 0 stalls in 64,005 reads |
| dB | 07:31:30-07:42:20 | Direction B, taps on both links, McASP slots 0-3 on the board, DUT CSRs every 5 s, counters pre/mid/post | Peer link 5,198,371 packets (sent), all present and equal on the DUT link (5,199,125), 0 sequence breaks; McASP 30,480,000 frames (635.0 s) equal to the received frames at one constant offset (148,874), all 32 bits of 4 slots: 0 skips, 0 repeats, 0 foreign; 0 overruns, 0 stamper drops; 25 board read stalls up to 87.1 ms absorbed (catch-up reads 960/1,920 frames). DUT: SLIP_TDM 0, RENDER_STAT converged, prefill 0, fill 8-14, rails 0; AVTPRX static. Counters: only frame counters moved |
| rA | 07:44:28-07:46:28 | 20 unbind/rebind cycles of DUT SO0 -> peer SI0 (2 s hold, binding rule, 4 s bound), pattern playing, taps with ACMP, external capture | 20/20 CONNECT_RX SUCCESS; format pairs read before every bind, all `0205022002006000` equal, no set; ended bound (conn 1, flags 0x0082). Wire restart (peer CONNECT_RX_RESPONSE -> first AAF at the peer) 13.4/13.8/86.8 ms; output less steady latency 23.5/24.8/97.8 ms; stop 9.7-10.8 ms after the DISCONNECT_RX_RESPONSE, 0 packets in any hold; first 480 frames valid each cycle; silences all zero frames; 0 capture stalls |

### Round 3 bench actions (one row per locked action)

| Window (UTC) | Action | Result |
|---|---|---|
| 2026-10-16 17:22:28-17:22:34 | identity gate | PASS 11/11 |
| 2026-10-16 17:22 | start baseline | all rc 0 |
| 2026-10-16 17:23-17:24 | SoC console: shell check, tool check | root shell |
| 06:51:33-06:51:38 | identity gate | PASS 11/11 |
| 06:52:02-06:52:05 | start baseline `start2` | all rc 0 |
| 06:52:40-06:52:41 | SoC console read-only look | root shell |
| 06:57:02-06:57:10 | tap probe 3 s per link, copy, delete | 0 drops; files removed on the tap host |
| 06:59:41-06:59:42 | SoC console read-only check | rc 0 |
| 07:00:17-07:01:06 | SoC: player stop, to-host leg kill (verified), stamper fetch | done |
| 07:01:47-07:03:56 | McASP self-test dry run | rc 0 |
| 07:05:05-07:16:24 | McASP self-test 630 s (tracked) | rc 0 |
| 07:17:26-07:29:00 | Direction A (tracked) | rc 0 |
| 07:31:29-07:43:53 | Direction B (tracked) | rc 0 |
| 07:44:12-07:47:52 | restarts (tracked) | rc 0 |
| 07:48:38-07:48:38 | SoC console read-only (CA mount source) | rc 0 |
| 07:48:53-07:49:04 | SoC: task files removed, to-host leg restart, player run.sh | done |
| 07:49:22-07:49:23 | SoC: player readback | login failed (CA store) |
| 07:49:30-07:49:30 | SoC: player error lines (to the private directory) | CA error 77 |
| 07:49:55-07:50:40 | SoC: CA bind mount recreated, 45 s readback | mounted; player still logged out |
| 07:50:54-07:51:20 | SoC: player stop, mount, run | logged in |
| 07:51:36-07:51:38 | end baseline, controller staging removed | all rc 0 |
| 07:51:38-07:51:43 | end identity gate | PASS 11/11 |
| 07:51:56-07:51:57 | controller staging removed again; tap host check | clean |

No outlet, JTAG, flash, reset, power, wiring or instrument-setting action; no DUT PHY or CSR write (console reads only); no clock-source, format or map command; ACMP binds only in the restart run, under the binding rule, ending bound as found; no USB gadget or UDC action; the from-host bridge leg left as found (DEAD).

### Round 3 deviations

- **The cut** (above). The private environment was re-created from the packet's census, ADP records and the bench rules; the identity gate and a start snapshot ran again before step 1.
- **API key in a transcript.** The board's full-argument process list printed a third-party API key into r3/soc2/look.log. Redacted within minutes, then the transcript moved to the private directory; no other file holds it (scanned). Later process lists use pid,comm only. Owner item: consider rotating that key.
- **Board-side stamper.** The board has no Python, so lane B5's reader runs as `b21stamp` (static aarch64, built on the bench host; binary kept under /tmp/a625/build, hash in the page). Same 24-byte record and 64 KiB reads.
- **Step 1 floor window.** 110-read windows (B5_W=110) for the short floor test, because the board sampler's wobble defeats 11-read windows; the 10 s permanent-step check is independent of it. The default W=10 output was not kept.
- **Direction B storage.** The McASP capture went to the board's root file system (/root/a625-b21, removed after the transfer), because /tmp there is 204 MiB.
- **Restart driver's format comparison.** restart_b21.py read a `format` field the agent does not emit, so its comparison saw nothing. The GET_STREAM_FORMAT reads ran before every bind and are logged (r3/runs/rA/agent.jsonl); all 20 pairs equal, so no set was due. The as-run tool is kept unchanged.
- **The player's CA mount.** stop.sh (owner instruction) removes the player's CA bind mount; run.sh does not recreate it, so the player could not log in after the restore. The lane recreated the mount from the player's own CA directory and restarted the player through its scripts; it logged in. Owner item: the start script does not make the mount.
- **mst-dry** ran with the transfer window at 100 s (edited to 40 s before mst-long).
- **Gates.** The first working-tree runs found wording the gates refuse (a capture tool's name, "This round", "certif"); reworded before the commit.

## Round 3 tools (SHA-256 as run; MANIFEST.sha256 holds all)

| Tool | From | Role |
|---|---|---|
| b21stamp.c (binary `666ee35a...`, not in the packet: 648 KB) | new; lane B5's Reader record | board-side per-read stamper with a RAM ring |
| mcasp_selftest_b21.sh | new | step 1 on the board |
| dir_b21.sh | new | one direction run |
| restart_run_b21.sh, restart_b21.py | new; lane B5's cycle | restart run and cycle driver |
| soc_locked_b21.sh, b21_xfer.py, hostsrv.py | new; hostsrv.py is lane B3's, unchanged | locked console action; HTTP/TFTP endpoints on the USB link |
| b21_aaf.py, b21_grade.py, b21_mcasp_ana.py, b21_restart.py | new; b21_mcasp_ana.py imports b5_attrib.py unchanged | decode and grades |
| baseline_b21r3.sh, identity_b21.sh, identity_b15.py, b8_ctl.py, console_poll.py, console_read.py, selftest_b21.py | rounds 1-2 and lane B19, unchanged | baseline, identity, controller, CSR poll, external capture |

## Round 3 packet layout

| Path | What |
|---|---|
| r3/identity, identity2, identity2-end | identity gates |
| r3/restore | baselines (start, start2, end), census, counters, controller views, SoC restore transcripts, final cleanup |
| r3/soc, r3/soc2 | SoC board checks, prep, deploy |
| r3/selftest | mst-dry, mst-long: board transcripts, analysis, derived read record |
| r3/runs | dA, dB, rA: events, DUT reads and poll, counters, tap logs, board transcripts, raw hashes; dB/ana: the McASP read analysis (record gzip-compressed) |
| r3/summary | the grades: wire, external, McASP alignment, CSR, counters, restarts |
| r3/gates-wt*, r3/gates-head | gate outputs |
| RAW-ARTIFACTS-r3.json | every round-3 raw file under /tmp/a625/raw by size and SHA-256 (82 files, 10,194,884,483 bytes) |
| REVIEW-READY-r3.*, review-ready-r3-url.txt | the post and its readback |

## Round 2 (resume after STOP 6208887896, from `d64336ba`)

Resume terms: the SoC board's console stands at a root prompt (owner login 2026-10-16 08:14 local); Direction B's capture is the McASP on the SoC board (owner decision 2026-09-30) and the host USB capture is a cross-check only; step 1 is redone as a self-test of the McASP capture path; the board's player is stopped with its stop script before taking the McASP and restarted with its run script at restore; a dated round-2 section; REVIEW READY or STOP on #117.

### Round 2 state

**DONE: STOP posted** (14:28Z), comment https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6217670001 (STOP-r2.md, stop-r2-url.txt, STOP-r2.readback.md: equal but for one trailing newline). Head `acba86cf02f04e8ee95f0bf5a5d8b9ec47f56d3d`, one commit on `d64336ba` (two on dev `4a9b5a2a`), one-line subject, no body, no trailers; `docs/findings/117_AUDIO_CONTINUITY.md` only (+64 lines: the round-2 section and its Contents entry). All gates rc 0 on the working tree (r2/gates-wt/) and at the head (r2/gates-head/). Not pushed; no PR (PR-BODY.md updated). Bench lock free. Posted on #117 in round 2: this STOP only. No round-2 TAKEN was posted, because the round stopped at its first bench action. No existing comment was edited or deleted.

STOP reason: the identity gate is incomplete. The controller host (the only ATDECC path) is unreachable from 14:04Z (no route to host) through 14:28Z. The 3 console checks PASS (ID/VERSION, AEM CRC `5ba355eb`, grader 10/10); the 8 ATDECC/ADP checks were not read (r2/identity/identity-verdict.txt: FAIL). The binding rule's format reads and the peer counters need the same host. The SoC board root-shell check, Soloist stop, step 1 and both directions were not started.

Owner item: bring the controller host back on the bench network. Then the round restarts at the identity gate.

- The bench host rebooted at about 12:07Z (uptime at 14:03Z: 1:56). /tmp is a tmpfs, so round 1's raw files under /tmp/a625/raw are gone; their sizes and SHA-256 stay in RAW-ARTIFACTS.json, and the packet keeps the derived read records. The private environment was re-created under /tmp/a625/priv from the packet's own records and the bench rules.

### Round 2 step ledger (UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| R0 | Context: the resume, the assignment, #117 since the STOP (no new comment), round 1's packet | Read | this file |
| R1 | Local preconditions (14:03Z) | bench lock free; UAC2 and capture cards present, all PCMs closed; three serial adapters; bench host up 1:56 (restart about 12:07Z); /tmp/a625 gone | this file |
| R2 | Private environment re-created (/tmp/a625/priv/b21.env) from the packet's ADP/census records and the bench rules | Done | not in the packet |
| R3 | Identity gate (round 1's identity_b21.sh + identity_b15.py), 14:04:33-14:04:43Z | **FAIL, incomplete**: console 3/3 PASS; controller host no route (STAGE/AECP/ADP rc 255), 8 checks not read | r2/identity/ |
| R4 | Controller host wait, 14:05-14:24Z (ICMP from the bench host, no lock: no bench device touched) | 54 polls, all down; neighbour entry FAILED; power-strip host and tap host answer SSH (no-op) | r2/controller-reachability.txt |
| R5 | Round-2 findings section, commit `acba86cf` | +64 lines (section + Contents entry) | the diff |
| R6 | Gates, working tree (9) and head (10), unpiped, physical path, pinned Markdown interpreter | all rc 0 | r2/gates-wt/, r2/gates-head/ |
| R7 | Controller rechecks before posting (14:26:43Z, 14:28:05Z) | down | this file |
| R8 | STOP on #117 | Posted, comment 6217670001; readback equal but for the trailing newline | STOP-r2.md, stop-r2-url.txt, STOP-r2.readback.md |
| R9 | PR-BODY.md, MANIFEST.sha256 updated | Done | |

### Round 2 cycle ledger (one row per run)

| Run | Window (UTC) | What | Result |
|---|---|---|---|
| step 1 McASP self-test | - | not run | STOP at identity gate |
| Direction A | - | not run | STOP at identity gate |
| Direction B | - | not run | STOP at identity gate |

### Round 2 bench actions (one row per locked action)

| Window (UTC) | Action | Result |
|---|---|---|
| 14:04:33-14:04:43 | identity gate: DUT console reads, UART grader; controller steps failed (no route) | console PASS; gate incomplete |

No other bench action: no SoC board console access, no Soloist or bridge action, no tap, outlet, JTAG, external capture, controller, flash, reset or power action; nothing written to the DUT. Restore: nothing to restore; bench lock free (checked before the STOP).

### Round 2 deviations

- **Gate rerun not possible.** The gate was run once; its controller steps cannot run while the host is down, so a rerun would only repeat the console half.
- **Round 1 raw files lost.** /tmp on the bench host is a tmpfs and the host restarted before this round; /tmp/a625/raw (65 files, 994,313,080 bytes) is gone. RAW-ARTIFACTS.json and the page keep their sizes and hashes; the packet keeps the derived read records (gzip). Nothing in round 2 depends on them.
- **No round-2 TAKEN.** Round 1's TAKEN stands for the lane; the resume asks for REVIEW READY or STOP, and the round stopped at its first action, so one STOP was posted.

## Round 1 state

**DONE: STOP posted** (2026-10-16 ~05:40Z), comment https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208887896 (STOP.md, stop-url.txt, STOP.readback.md: equal but for one trailing newline). Head `d64336badb959349846a226df213621eccb3a334`, one commit on dev `4a9b5a2a`, one-line subject, no body, no trailers; `docs/findings/117_AUDIO_CONTINUITY.md` only (+224 lines: the dated section and its Contents entry). All gates rc 0 at the head (gates/head/gates.txt). Bench lock free; restore read back. Posted on #117: TAKEN and STOP only; no existing comment edited or deleted.

STOP reasons: (1) the step-1 capture-path self-test was not clean in either 10-minute window; (2) the SoC board's console stands at `login:` (no root shell; no credential typed or stored), so neither direction can play or record McASP0.

| Item | Verdict |
|---|---|
| Identity gate | PASS 11/11, start and end |
| Step 1, capture-path self-test (deficit-only) | NOT CLEAN (st-long: 336 frames lost; st-long2: 10,945), losses whole 1 ms USB frames in stall episodes with USB controller interrupts missing; no 3.00 s recurrence |
| Step 2, Direction A | NOT RUN (STOP) |
| Step 3, Direction B | NOT RUN (STOP) |
| #117 audio continuity row | Not graded on this image; not passed |

## Step ledger (UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load: assignment, #117 in full (the [A10] comments, B5 rounds, B19), the B5 page, 451/617 pages, register map slip section, packets b3/b4/b2/75/117-a373/b5-a472/b5-a473/645-b18/117-b19 | Read | this file |
| 1 | Local preconditions (04:55Z) | dev tip = lane base `4a9b5a2a`; UAC2 and capture cards present, all PCMs closed; three serial adapters; bench lock free | this file |
| 2 | Tools copied, origin pins; b5_round3.py from the public archive `9006c78e` (`415ef1b0...`, equal to the page) | Done | tools/ORIGIN.sha256 |
| 3 | TAKEN on #117 | Posted, comment 6208396842; readback equal but for the trailing newline | TAKEN.md, taken-url.txt, TAKEN.readback.md |
| 4 | Identity gate (lane B19's method, identity_b21.sh + identity_b15.py) | **PASS 11/11**, 04:56:04-04:56:09Z | identity/ |
| 5 | Start baseline (baseline_b21.sh) | 04:56:25-04:56:27Z, all rc 0. As found: DUT SI0 bound to peer SO0 (flags 0x0002), peer SI0/SI8 bound to DUT SO0/SO1 (flags 0x0082); DUT clock 0, peer clock 1 (its CRF input); formats equal across each binding (DUT SO0/peer SI0 8 ch, peer SO0/DUT SI0 4 ch); DUT maps SPI0 4, SPO0 8 identity; SLIP_LB 0x0000FFFF, SLIP_TDM 0, RENDER_STAT 0x020C; outlets OUT0-OUT6 ON; controller: no gPTP daemon | restore/*-start* |
| 6 | SoC board root-shell check (`id; tty` via soccon_b21.py) | **No shell: `login:` prompt** (rc 3). The readiness line was taken as a login name; a 75 s passive (no-write) read saw `Login timed out after 60 seconds` and `login:` again (as found). No credential typed or stored | soc/ |
| 7 | External capture controls (read-only) | 0 mixer controls; no software loopback can be set and restored, so step 1 is the deficit-only self-test (manager rule) | this file |
| 8 | Self-test dry run, 20 s | rc 0, 0 stalls | selftest/st-dry*, selftest/st-dry-lock.txt |
| 9 | Self-test 1 `st-long`, 630 s | Not clean: 11 stalls (2 episodes), 2 losses (4 and 3 ms, 336 frames) with ~13.6 USB controller interrupts missing each; 11 floor steps of 1 ms (~60 s apart) with no interrupt shortfall; 0 stall spacings of 2.99-3.02 s | selftest/st-long/ |
| 10 | Self-test 2 `st-long2`, 630 s, sampler adds pressure and compaction counters | Not clean: 123 stalls (16 episodes, up to 88.4 ms), 18 losses (2-88 ms, 10,945 frames), USB shortfall median +21.3 vs control -1.2; pressure at losses equal to control; steal 0.008% | selftest/st-long2/ |
| 11 | End identity gate and end baseline (controller staging removed) | PASS 11/11 (05:29:44Z); census 45/46 equal (DUT live propagation delay); outlets equal; DUT words equal but live counters; NVM unchanged | identity-end/, restore/*-end*, restore/census-compare.txt |
| 12 | Findings section, commit `d64336ba` | +224 lines, the dated section and its Contents entry (gen_toc --write, description filled) | the diff |
| 13 | Gates: working tree, then at the head (unpiped, physical path, pinned Markdown interpreter) | working tree: 9 rc 0 (the bare-metal gate's first call lacked `--check`: usage error rc 2, re-run with `--check` rc 0, both kept); head: 10 rc 0 | gates/, gates/head/ |
| 14 | STOP on #117 | Posted, comment 6208887896; readback equal but for the trailing newline | STOP.md, stop-url.txt, STOP.readback.md |
| 15 | PR-BODY.md, MANIFEST.sha256 | Done | |

## Cycle ledger (one row per run)

| Run | Window (UTC) | What | Result |
|---|---|---|---|
| st-dry | 05:00:34-05:00:54 | 20 s self-test dry run | 0 stalls |
| st-long | 05:01:20-05:11:51 | 630 s deficit-only self-test | NOT CLEAN: 336 frames lost (burst at 367-383 s); 11 one-ms steps |
| st-long2 | 05:15:22-05:25:53 | 630 s deficit-only self-test, repeat | NOT CLEAN: 10,945 frames lost in 16 episodes; 13 one-ms steps |
| Direction A | - | not run | STOP |
| Direction B | - | not run | STOP |

## Bench actions (one row per locked action)

| Window (UTC) | Action | Result |
|---|---|---|
| 04:56:04-04:56:09 | identity gate | PASS |
| 04:56:25-04:56:27 | start baseline (DUT reads, census, counters, controller, host view, outlets) | all rc 0 |
| 04:57:38-04:57:38 | SoC console `id; tty` | login prompt, rc 3 |
| 04:58:24-04:59:39 | SoC console passive read, 75 s, nothing written | login timeout, back at `login:` |
| 05:00:34-05:00:54 | self-test dry run (external capture only) | rc 0 |
| 05:01:20-05:11:51 | self-test 1 (external capture only) | rc 0 |
| 05:15:22-05:25:53 | self-test 2 (external capture only) | rc 0 |
| 05:29:44-05:29:50 | end identity gate | PASS |
| 05:29:50-05:29:52 | end baseline, controller staging removed | all rc 0 |

No outlet, JTAG, flash, reset, power, wiring, tap or instrument-setting action; no DUT PHY or CSR write; no bind, format, map or clock-source change; no USB gadget action; nothing played on any device.

## Deviations and decisions

- **SoC board without a root shell.** The board's console stands at `login:`. Steps 2 and 3 need it (Direction A: the pattern into McASP0; Direction B: the McASP0 capture). The USB bridge path resamples (`alsaloop -S samplerate`), so it cannot carry a bit-exact grade. Owner item: a root shell on the SoC board's console.
- **Readiness line at the login prompt.** soccon's readiness line (as in lane B4) was taken as a login name; login timed out after 60 s and returned to its prompt (passive read). No password or credential was sent.
- **No partial step 2.** A wire-only tap and CSR observation without the pattern was considered and not run: the assignment's step 2 is Direction A with the pattern, and step 1 had not passed.
- **Long actions.** A 630 s capture exceeds one foreground call's 600 s limit, so each ran as one tracked action (tools/tracked_b21.sh: setsid, flock, a hard deadline that releases the lock) and was polled in the foreground until it ended.
- **Deficit with multi-period reads.** After a stall one read can deliver more than one period (1 read in st-long, 53 in st-long2); b21_selftest_ana.py counts the frames each read delivered (b5_attrib.py's window had none and counts 480 per read). The drift over one floor test is the median step (the whole-window linear fit is pulled by the losses). st-long2's record needs uint32 (one interval of 88.4 ms); the packet carries it gzip-compressed.
- **b5_attrib.py and b5_round3.py.** b5_attrib.py is imported unchanged for its definitions (it asserts B5's record hashes, so its own commands cannot run on this record). b5_round3.py is carried for its hash and not run: it grades content, and the self-test input was constant.
- **Sampler versions.** host_sampler_b21_st-long_asrun.py ran for st-dry and st-long; host_sampler_b21.py (adds /proc/pressure and /proc/vmstat counters) ran for st-long2.
- **Host snapshots kept out of the packet.** The process-table snapshots name other sessions on the shared bench host, so all host-*.txt files and st-*.stdout stay under /tmp/a625/raw (hashed in RAW-ARTIFACTS.json). Summary for the reader: two batch FPGA builds were replaced by two new ones about 5 minutes into st-long, a builder job ran, kernel compaction and reclaim threads were active; guest pressure at the losses equals the control times.
- **Stall source.** Not found on the bench host: the losses come with the capture's USB host controller interrupts missing while the host's own CPU, memory and I/O pressure stay at control values and steal time is near zero. No host configuration was changed (the manager's).

## Restore

| Item | Start (04:56Z) | End (05:29Z) |
|---|---|---|
| Bindings | DUT SI0 <- peer SO0 (0x0002); peer SI0 <- DUT SO0, peer CRF input <- DUT SO1 (0x0082) | same |
| Formats, maps, clock sources, configuration, sampling rate | as read | equal (census 45/46; the other: DUT live propagation delay 386 -> 381 ns) |
| DUT words | SLIP_LB 0x0000FFFF, SLIP_TDM 0, RENDER_STAT 0x020C | SLIP_LB 0x0000FFFF, SLIP_TDM 0, RENDER_STAT 0x020B (live fill) |
| DUT NVM | image seq 335, VD_OK, pend 0 | same |
| DUT sync | SYNC=1 ASCAPABLE=1 TU=0 | same; grader 10/10 |
| Outlets | OUT0-OUT6 ON | same (none switched) |
| SoC board console | `login:` | `login:` |
| Controller host | no gPTP daemon | same; staging /tmp/a625 removed |
| Bench host | all PCMs closed; UAC2 and capture cards present | same; no lane process; bench lock free |

Residuals: none from this lane.

## Tools (SHA-256 as run)

Inherited: tools/ORIGIN.sha256. New or adapted in this lane:

| Tool | From | Change |
|---|---|---|
| identity_b21.sh | lane B19's identity_b19.sh | environment B21_ENV, staging /tmp/a625 |
| baseline_b21.sh | lane B19's baseline_b19.sh | environment B21_ENV, staging /tmp/a625 |
| soccon_b21.py | lane B5's soccon.py | marker prefix only |
| console_listen.py | new | passive serial read, writes nothing |
| tracked_b21.sh | new | one long locked action, detached, hard deadline |
| selftest_b21.py | new; reader copied from lane B5's run_a.py | the self-test |
| host_sampler_b21.py (+ st-long as-run copy) | new | 20 Hz host sampler |
| b21_selftest_ana.py | new; imports b5_attrib.py | analysis |

All hashes: MANIFEST.sha256.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md, PR-BODY.md | this file; the proposed PR body |
| TAKEN.*, STOP.*, taken-url.txt, stop-url.txt | the two posts and their readbacks |
| STOP-r2.*, stop-r2-url.txt | round 2's STOP and its readback |
| r2/ | round 2: identity gate records, controller reachability, gates on the working tree and at the head |
| identity/, identity-end/ | identity gate at the start and the end |
| restore/ | start and end baselines, census comparison, controller views and cleanup, outlets |
| soc/ | SoC console check and passive read |
| selftest/ | per run: events, arecord log, lock window, analysis text, derived read record and its metadata |
| gates/, gates/head/ | gate outputs on the working tree and at the head |
| tools/ | every script used or carried, with ORIGIN.sha256 |
| RAW-ARTIFACTS.json | all raw files under /tmp/a625/raw by path, size and SHA-256 |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
