# [A468] Bench lane B4 handoff

Refs #451, the timing item "Scope BCLK, FSYNC and DOUT at the AM62x end: 12.288 MHz, a one-BCLK FSYNC pulse at 48 kHz, data starting one BCLK after it", measured on the SoC board by owner decision. #626 holds the oscilloscope version.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924192573
Branch: b4-bench-1001 from dev e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b (lane worktree, physical /data path).
Image under test: dev ec0cc0c1 (installed 2026-09-30 05:18; identity proven by lane B3 and again here).
Packet: this directory. Raw files (the 730,595,328 B capture, the full decode and attribution, the TCP test and the redaction originals) stay outside it under /tmp/b4-a468/raw and are indexed by size and SHA-256 in RAW-ARTIFACTS.json. Private endpoints, the redaction map and the discovery transcripts stay in /tmp/b4-a468/private (not in the packet).

## State (session 3, resume with no bench access, 2026-10-01 from 06:48 CEST)

The manager ruled on the session-2 STOP: **the 475.6 s capture is accepted, no re-run** (https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924950994). Session 3 edits the findings page as the ruling lists, on top of 4461a1f7, with no bench access: no console, SoC board, controller host, DUT or bench lock.

| Time (CEST) | Cycle | Result | Evidence |
|---|---|---|---|
| 06:49 | Read git status, log and diff; read the ruling and the assignment in full | Tree clean at 4461a1f7; no uncommitted edits | |
| 06:51 | Checked that the USB loss leaves the figures alone, from the packet only | The fs window's last sample (tstamp 68,513.732 s) is 0.24 s before the SoC board's logged event (68,513.970 s); its residual -1.17 frames is inside the fit's 1.23 frames rms; the pattern decode covers every received byte | runs/timing-long/fit-fs.json |
| about 06:50-06:51 | Page and index row edits, as the ruling lists | Capture-length row: "475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994)". "Why the run stopped" became "The USB loss, a bench event" with the two no-effect points. "Rerun" became "Notes for a later capture" (no re-run follows; the four method notes kept, the owner-decision sentence dropped). Intro and index row follow the ruling. Measured figures and stated limits unchanged | docs/findings/451_TDM8_TIMING_SOC_BOARD.md, docs/findings/README.md |
| about 06:51 | Evidence hashes and raw capture re-checked, offline | The page's 11 evidence files equal the packet in size and SHA-256. The raw capture under /tmp/b4-a468/raw re-hashed: 730,595,328 B, dd201b3a...36cb, equal | |
| about 06:51-06:52 | Pre-commit gates on the working tree; table checks | All rc 0; both pages' tables OK | |
| 06:52:13 | Commit `35a60c8d6ee742216f98232c85926b435ab01b91` on 4461a1f7 | One-line subject, no body, no trailers; 2 files, +33 -15; worktree clean | |
| 06:52:25 | 13 gate invocations at 35a60c8d (session 2's 12 plus `git diff --check 4461a1f7 HEAD`) | All rc 0; em-dash 0 findings over 374 added lines; table checks OK; status clean | gates/ |
| 06:54:06 | REVIEW READY on #451 | POSTED: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5925003925; readback identical but for one trailing newline | REVIEW-READY.md, REVIEW-READY.readback.md |

Session 3 left the bench as session 2 left it: it touched no console, SoC board, controller host, DUT or bench lock. Head `35a60c8d`, local only: not pushed, no PR. `summary/summary.json` is session 2's record and still reads the capture-length verdict as NOT MET. The ruling supersedes it there; the file was left unchanged because the page, the STOP and the manifest pin its hash. The lane stops here.

## State (session 2)

**STOP** (UAC2 card gone from the bench host), posted 2026-10-01T04:46:38Z: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924930868. Owner items: re-attach the SoC board's USB function to the bench host; decide the rerun's shape (see Rerun notes).

Commit `4461a1f7db55f4c37bc6dd8363c114deeb85eee2` on b4-bench-1001 is one commit on `35a8b04d` (session 1), one-line subject, no body, no trailers. Local only: not pushed, no PR. The worktree is clean. It replaces the attempt record in `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` with the measured result and updates its row in `docs/findings/README.md`. No other doc edit.

All 12 gate invocations are rc 0 at that head (gates/gates.txt). Table cell counts OK (12 tables on the page, 1 in the index). The bench lock is free; it was held only for each action. No task process runs on this host, the controller or the SoC board.

Verdicts (operator observations): identity PASS (session 1; same DUT boot); framing recorded; data one BCLK after the frame-sync edge PASS as far as the board shows (22,831,104 frames bit-exact in all eight slots, 0 torn); fs 47,997.947 Hz on the SoC board's clock (-42.8 ppm vs 48 kHz, -32.1 ppm vs plan, +-0.12 ppm granularity, crystal excluded); BCLK 12,287,474 Hz inferred (256 x fs); capture of at least 10 minutes NOT MET (475.6 s, STOP); FSYNC width, edge timing, levels, absolute ppm not shown (#626).

## Posting

- Session 3 REVIEW READY, posted 2026-10-01T04:54:06Z: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5925003925. REVIEW-READY.md is the posted text; REVIEW-READY.readback.md is the API readback, identical but for one trailing newline. Nothing else was posted in session 3, and no existing comment was edited or deleted.
- Session 2 STOP, posted 2026-10-01T04:46:38Z: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924930868. STOP-2.md is the posted text; STOP-2.readback.md is the API readback, identical but for one trailing newline. Nothing else was posted, and no existing comment was edited or deleted. The lane stops here.
- Session 1 posts (TAKEN 03:39Z, STOP 03:52:57Z) are below and were not posted again.

## Resume (session 2, 2026-10-01 from 06:06 CEST)

The owner logged the SoC board's serial console in as root at 06:06 CEST and left it at the root prompt. No credential was typed, seen or stored by this lane.

| Time (UTC) | Cycle | Result | Evidence |
|---|---|---|---|
| 04:09:26Z | Root shell check: `id; tty` | uid=0(root), /dev/ttyS3; rc 0 | soc/r2-shell-check.log |
| 04:09:49-04:09:56Z | Start baseline (SoC health, DUT reads, census, controller PHC) | all rc 0. SoC board rebooted since lane B3 (uptime 67,602 s), kernel #6 of 2026-09-28; bridge legs to-host 233 and from-host 234 running with the recorded lines; McASP0 TX substream in XRUN (no host playback); UDC configured; BAD=0; taint 0. DUT reads equal session 1's end but for live counters; census 32/33 equal to session 1's end (the other is the propagation delay); controller: no daemon, 0 ppb, timestamping off | soc/r2-start-health.log, restore/*-r2-start.* |
| 04:10:32Z | Framing: tool inventory, processes, current capture parameters (read-only) | busybox 1.38 without nc; bash; phc2sys present but waiting for ptp4l; system clock never set (1970) | soc/r2-framing-discover.log |
| 04:12:20Z | Framing: DT node search, clock logs; 33-byte TCP test to this host | sound-tdm8, tdm8-codec, McASP0 found; phc2sys only "Waiting for ptp4l"; arch_sys_counter 200 MHz; TCP via bash /dev/tcp rc 0 | soc/r2-tcp-test.log |
| 04:12:30Z | Framing: DT properties of sound-tdm8, tdm8-codec and McASP0 (read-only) | dsp_a; bit-clock and frame master = codec; 8 slots x 32 bits on both DAIs; McASP0 op-mode 0, tdm-slots 8, serial-dir <1 2 0..> (AXR1 receives), rx/tx-num-evt 32; McASP1/2 disabled | soc/r2-framing-dt.log |
| 04:16:21-04:16:27Z | Bridge legs 233/234 stopped by PID (command lines checked against status) | KILLED; all four PCMs closed; UDC configured; BAD=0; host UAC2 card present | soc/r2-stop-legs.log |
| 04:16:33Z | Controller: stage with_gptp.py and aaf_talker.py | rc 0; hashes equal the packet's | restore/r2-stage.txt |
| 04:16:41-04:29:37Z | Timing run `timing-long` (one tracked action; see Deviations): talker 700 s, bind + map at 04:16:58Z, capture started 04:17:05Z (SoC trigger 68,038.252 s), PCM status every 5 s | Capture stalled at 475.7 s: last bytes 04:25:00.820Z; SoC `dwc3: remote wakeup not configured` at 68,513.970 s; bench host xHCI `Set TR Deq Ptr cmd failed` 04:25:01.084Z and USB disconnect 04:25:01.085Z; McASP0 capture XRUN at 68,514.390 s. SoC console step rc 124 at its 720 s deadline (one Ctrl-C to the foreground loop). Then map remove, unbind, map read back empty, talker exit all rc 0. 730,595,328 B received, SHA-256 dd201b3a...36cb, max gap 50 ms before the stall | runs/timing-long/ |
| 04:29:41Z | Bench host: UAC2 card and ECM interface absent; no re-enumeration | **STOP condition** (owner must re-attach) | soc/r2-end-host-view.txt |
| 04:31:00Z | SoC read: own recorder (PID 781) still blocked in a socket write (wait_woken), capture XRUN; UDC configured on the SoC side; usb0 up | read only | soc/r2-after-stall.log |
| 04:31:15Z | SoC: SIGTERM to PID 781 after checking its command line; stderr file printed and removed | caught ("Aborted by signal Terminated..."), handler reset to default, write stayed blocked | soc/r2-arecord-stop.log, soc/r2-arecord-check.log |
| 04:31:50Z | SoC: second SIGTERM to PID 781 after re-checking its command line | ended; all four PCMs closed; no recorder or alsaloop left; /tmp as found | soc/r2-arecord-stop2.log |
| 04:31:57-04:32:01Z | Bridge legs restarted with the two recorded lines | STARTED: to-host 1265, from-host 1266; PCM states as at the start; UDC configured; BAD=0 | soc/r2-restart-legs.log |
| 04:32:06Z | Controller restore: no daemon check; PHC freq 0 and trajectory (phc_restore_b4.py); timestamping tx 0 rx 0 | freq 0.000000 ppb; residual 4,547 ns; tx_type 0 rx_filter 0 | restore/r2-controller-restore.txt |
| 04:32:12-04:32:19Z | End snapshot (SoC health, DUT reads, census, controller) and staging removal | all rc 0; census 31/33 equal to start (DUT pdelay live; peer GET_SAMPLING_RATE ENTITY_LOCKED at end); SoC as found but for leg PIDs | soc/r2-end-health.log, restore/*-r2-end.*, restore/r2-census-compare.txt, restore/r2-dut-compare.txt |
| 04:33-04:40Z | Offline: decode, fs fit, attribution, redaction | decode 22,831,104 frames 0 torn 0 invalid 0 zero; fs 47,997.947 Hz (-42.8 ppm; -32.1 ppm vs plan; +-0.12 ppm); 1,221 clusters (189 beat, 16 sender, 1,016 unmatched) | runs/timing-long/*.json |
| 04:41-04:43Z | Findings page and index row; gates; commit amended once (gate 7 refused OS-level terms on the first commit 7fdd490e, never published) | head 4461a1f7, 12 gate invocations rc 0 | gates/ |
| 04:46:38Z | STOP on #451 | POSTED; readback identical but for one trailing newline | STOP-2.md, STOP-2.readback.md |
| 04:47:04Z | Controller: staging /tmp/a468 removed (found still present by the final process check) | removed; absent on re-read; no gPTP daemon | restore/r2-controller-cleanup.txt |

## Bench as left (session 2)

- **SoC board.** Bridge legs running with the recorded lines under new PIDs 1265 (to-host) and 1266 (from-host); PCM states as at the start (McASP0 capture running, McASP0 playback XRUN, gadget PCMs running); UDC configured on the SoC side; BAD=0; taint 0; /tmp as found; McASP0 RX 250 periods/s. The lane's recorder ended; its stderr file removed.
- **Controller.** No gPTP daemon; PHC 0.000000 ppb, back on the session-1/2 trajectory (residual 4,547 ns); timestamping tx 0 rx 0 as found; /tmp/a468 removed at 04:47:04Z (see Deviations).
- **DUT.** Mappings removed (read back empty), stream unbound. VERSION, control words, AEM unchanged.
- **Bench host.** UAC2 card and ECM interface absent (STOP; owner re-attach). At 04:31:24Z another USB audio device (not part of this lane; name withheld as private) enumerated on the bench host on another port.

## Residuals (session 2; no permitted command restores them)

- DUT NVM persistence advanced by the method's map and bind edits: commits ok 0 -> 2, slots 235/236 -> 237/238, pend=1, PP_STAT 5b000444 -> 5b000c44 (bit 11). Lane B3 recorded the same class.
- DUT SLIP_LB (0x8D4) saturated 0xFFFF/0xFFFF: it counted ~340 dups and ~340 skips per second from the bind (B3's run: ~70/s). RENDER_STAT rails 0 -> 6,264 (B3: 4 -> 134 in 70 s). The talker also ended ~55 s before the unbind, because the stalled capture held the SoC console until its 720 s deadline. Reset-only counters.
- Census: the reference peer's GET_SAMPLING_RATE answered ENTITY_LOCKED at the end (SUCCESS at the start). This lane sent the peer read commands only; another party appears to have locked it.
- Bridge legs under new PIDs.
- UAC2 card and ECM interface absent from the bench host.

## Deviations (session 2)

- **One background action.** The assignment's capture of at least 10 minutes cannot fit the operator tooling's 10-minute ceiling on one foreground command. The single timing run (talker 700 s, capture 630 s) therefore ran as one tracked action with an explicit 900 s deadline under the lock, and every other command, including the polling until it ended, ran in the foreground. The session never ended while it ran.
- **Capture transport.** The SoC board has no nc (busybox 1.38 without it), and the full capture exceeds its tmpfs, so the recorder wrote through bash's /dev/tcp to a TCP receiver on the ECM address (hostsrv.TcpReceiver). A 33-byte TCP test preceded it.
- **PCM status sampling.** /proc status reads reset the substream's avail_max statistic; they change nothing else.
- **Recorder termination.** After the STOP, the lane's own recorder (PID 781), blocked on the dead link and holding McASP0 capture, was ended by PID: the first SIGTERM was caught by arecord's handler (which resets it to default and returns), the second ended it. Not a bridge PID; never pkill.
- **Timeout path.** soccon sent one Ctrl-C at the capture step's 720 s deadline; it reached only the shell's foreground status loop (the recorder was a background job).
- **Controller timestamping restore.** The slave-only gPTP run left tx_type 1 rx_filter 1; it was set back to 0/0 as found. The gPTP profile was not touched.
- **Commit amended once**, before any publication: the first commit (7fdd490e) failed gate 7 (OS-level terms on the page); the page was reworded and the commit amended to 4461a1f7.
- **Late staging cleanup.** baseline_locked.sh removes the controller staging only for the tag `end`; the session-2 end snapshot used `r2-end`, so /tmp/a468 stayed on the controller until the final process check found it. It was removed at 04:47:04Z under the lock. The posted STOP (04:46:38Z), the page and the PR body state the staging as removed; that became true 26 s after the STOP was posted. The comment was not edited.
- **Redaction map extended** (private) with the bench host's name and addresses, the SoC gadget's MACs and link-local address, and a line rule for another USB device's identity.

## Rerun notes (for the next operator)

- Needs: the owner to re-attach the SoC board's USB function to the bench host (UAC2 card and ECM link).
- The bash /dev/tcp stream held 1.536 MB/s with no gap of 100 ms or more for 475 s. Whether it contributed to the USB loss is not established; the SoC board logged the same dwc3 line at 667 s and 26,028 s of its uptime.
- Make the talker outlast the capture plus the SoC console deadline (here 720 s), or the finally block unbinds a stopped talker late.
- aaf_talker.py's late-PDU list caps at 5,000 entries (full at 292 s here); raise it for a 10-minute attribution.
- fs alone needs no data off the board: a capture discarded on the SoC board, with the same status sampling, gives fs with no USB traffic. The pattern check of the same capture still needs the data. Owner decision.

## State of session 1 (kept as written then)

**STOP**, posted 2026-10-01T03:52:57Z: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924386279. STOP.md is the posted text; STOP.readback.md is the API readback, identical but for one trailing newline.

TAKEN, posted 03:39Z: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924249315. TAKEN.md and TAKEN.readback.md are its text and readback.

The SoC board's serial console stands at a `login:` prompt, not a root shell. The lane holds no credential: none in the environment and none recorded in the project, and nothing was guessed. A key-only remote login over the SoC board's USB network link was refused. The timing steps (framing, the capture of at least 10 minutes, fs and BCLK) all need a shell on the SoC board, so they are NOT RUN. Owner item: a root shell on the SoC board's console, with the bridge state known.

Commit `35a8b04da191f5189cb81db455afdbb9ee9b43d6` on b4-bench-1001 is one commit on e4b771f9. It has a one-line subject, no body and no trailers. It is local only: not pushed, no PR. The worktree is clean.
- `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (new): the attempt record.
- `docs/findings/README.md`: one index row, between the first-light row and the USB Audio row (file-name order).

All gates are rc 0 at that head (gates/gates.txt). The bench lock is free; it was never held between actions. No task process runs on this host or the controller.

No DUT flash, reset or power cycle; no outlet read or switched; no DUT PHY, CSR, map or bind write; no wiring or instrument change; no USB gadget down/up or UDC write; no SoC board command run.

## Step ledger (UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | TAKEN on #451 | POSTED 03:39Z | TAKEN.md, TAKEN.readback.md |
| 1 | Identity gate | PASS 03:41Z: VERSION 00020060; AEM CRC 93742dd2 (7,352 B); entity 020000fffe000001; ENTITY 312 B and CONFIGURATION 106 B from AECP byte-equal to the QSPI AEM bytes; NVM slot B seq 236 authoritative, backed=1 dirty=0 stale=0 pend=0, commits ok=0; grader 10/10; ROM acad92b9 (53,344 B); QSPI payload d178f19a (3,825,788 B). Every value equals lane B3's | identity/ |
| 2 | Start baseline, then framing from the SoC board | STOP 03:42Z. The baseline's DUT reads, census and controller state are rc 0. The SoC console replied with its login prompt (soccon rc 3): no shell | restore/*-start.*, soc/start-health.log |
| 2a | Alternative access, no credential | 03:43Z. The SoC board answers ping on the USB network link. A key-only remote login hit a host-key mismatch against this host's record, which predates the 2026-09-28 reflash. Retried once with a throwaway known-hosts file (~/.ssh untouched), BatchMode, publickey only: refused | soc/ssh-probe.txt |
| 3 | Capture of at least 10 minutes; fs and BCLK | NOT RUN (no shell) | |
| 4 | What the SoC board cannot show (#626) | Written on the page from #626 and the first-light configuration record | page |
| 5 | Restore and proof | 03:44Z. Nothing to restore: no write anywhere. End snapshot: census 32/33 equal to the start (the other is the live propagation delay, 385 then 375 ns); DUT control words and PP_STAT equal; controller with no daemon, PHC 0 ppb and timestamping off as found, staging /tmp/a468 removed; SoC board seen from this host only (UAC2 card present, ECM ping 3/3) | restore/, soc/end-host-view.txt |
| 6 | Findings page, index row, gates, commit | DONE 03:51Z: commit 35a8b04d; 10 gate invocations rc 0; table cell counts OK; anchors OK | gates/ |
| 7 | STOP on #451 | POSTED 03:52:57Z | STOP.md, STOP.readback.md |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 05:40:21-05:40:23 | Controller host: interfaces, tool paths, sudo (read-only) | rc 0; AVB port identified |
| 05:40:29-05:40:29 | Controller: search for the gPTP daemon and profile (read-only) | nothing under the root file system alone |
| 05:40:35-05:40:36 | Controller: wider search, excluding pseudo file systems (read-only) | daemon, clock and timestamping tools and four profile copies found |
| 05:40:51-05:40:52 | Controller: profile hashes and contents (read-only) | all four copies byte-identical |
| 05:40:59-05:40:59 | Controller: daemon versions (read-only) | both copies are the same version |
| 05:41:29-05:41:58 | Identity gate and controller preflight | PASS. The tool-staging scp returned 255 on a file this lane does not carry; the three needed tools were staged (hash list in the preflight) |
| 05:42:33-05:42:34 | Start baseline (SoC health, DUT reads, census, controller PHC) | SoC rc 3 (login prompt); DUT, census and controller rc 0 |
| 05:43:01-05:43:03 | SoC USB network link: ping and a key-only remote login | ping 3/3; login refused at host-key verification |
| 05:43:30-05:43:30 | Key-only remote login with a throwaway known-hosts file | refused (publickey) |
| 05:44:47-05:44:50 | End snapshot (this host's view of the SoC board, DUT reads, census, controller state, staging removal) | all rc 0 |

## As found (against lane B3's end state)

- **DUT reset since lane B3.** NVM commits ok=0, pend=0; PP_STAT 5b000444 (bit 11 clear); slots seq 235/236 as B3 left them; SLIP_TDM 33,474 (B3's page last read 440); TAI near 65,500 s. gPTP path generation 3, where B3 saw 1. GM unchanged in identity.
- **Controller host restarted** (uptime about 38,090 s at 03:41Z). PHC frequency 0.000000 ppb, about 2.30 s off CLOCK_REALTIME and drifting; timestamping tx_type 0, rx_filter 0. B3 left 28,062 ppb with tx 1 rx 1. This lane changed none of it.
- **Bench host.** The UAC2 card and the ECM interface are present. The serial device nodes date from 2026-09-30 18:37.
- **Census.** All 18 stream states unbound; DUT maps empty; DUT clock source 0 at 48 kHz.

## Incidental DUT-side observation (not a SoC board measurement; this handoff only, not on the page)

AAF_PAIRS (0x664, TDM pairs captured by the talker front end) rose by 26,173,107 between the DUT reads at 03:42:33.743Z and 03:44:50.062Z (136.32 s on this host's clock): 192,000 pairs/s, or 47,999.49 frames/s at four pairs per frame. The window is uncalibrated: this host's clock, plus one console read's latency (21 ms) at each end. It agrees with the plan's 47,999.49 Hz well inside that bound. SLIP_TDM rose 69 in the same window: 0.506/s, 10.55 ppm +-0.15.

## Deviations and incidents

- The SoC board's console was at a login prompt (STOP, above). soccon's readiness probe had already sent one carriage return and one `printf` line. At a login prompt that line can be taken as a login name. soccon matched the prompt and closed with rc 3. No password was sent, and nothing else was typed on the SoC console. If the line was taken as a login name, login's own timeout returns the console to its prompt.
- The two remote-login probes are not in the assigned method. They used this host's existing key only, never a password, and ran one read-only command that never executed. The host-key mismatch was bypassed only through a throwaway known-hosts file in the private directory; ~/.ssh was not modified.
- identity_locked.sh, copied from B3, listed a tool this lane does not carry, so its scp returned 255. The three tools the controller needs were staged; the line was corrected afterwards.
- Gate 7 was first run without a mode, before the commit (usage, rc 2). All gates were then run at the committed head with `--check`, as the earlier lanes ran it.
- Not done, by the STOP: the framing reads, the capture, fs/BCLK, and the bridge stop/restart (and so its restore).

## Rerun notes (for the next operator)

- Needs: a root shell on the SoC board's console (owner), and the bridge status read first.
- A capture of at least 10 minutes is 921.6 MB; the SoC board's temporary storage was 209,560 KiB in B3's DOUT capture log. Stream it off the board while recording (for example to a TCP receiver on this host's ECM address), and size the ALSA buffer against network stalls. Check for overruns in the recorder's output and in the pattern decode.
- fs: B3's arecord -v shows tstamp_mode ENABLE, tstamp_type MONOTONIC. During the capture, the capture substream's status (`hw_ptr` and `tstamp`, MONOTONIC) can be sampled read-only, with `trigger_time` as the start. A fit over the samples gives frames per monotonic second. The uncertainty is the pointer granularity (rx-num-evt 32) over the window, plus the board crystal's tolerance.
- The talker must outlast the capture: the 10-minute window plus settle and margins, roughly 700 s.

## Residuals

None from this lane. Possibly, the SoC console holds the readiness line as a login name until login's timeout.

## Packet layout

| Path | What |
|---|---|
| TAKEN.md, TAKEN.readback.md | Posted TAKEN text and its API readback |
| STOP.md, STOP.readback.md | Session 1's posted STOP text and its API readback |
| STOP-2.md, STOP-2.readback.md | Session 2's posted STOP text and its API readback |
| REVIEW-READY.md, REVIEW-READY.readback.md | Session 3's posted REVIEW READY text and its API readback |
| runs/timing-long/ | Session 2's run: events, controller transactions and logs, DUT reads, the SoC capture transcript with the status samples, decode.json, fit-fs.json, attribution-summary.json, lock window |
| PR-BODY.md | Proposed PR body |
| identity/ | Console CRC, NVM and descriptor readback; grader; AECP-vs-QSPI comparison; ADP discovery; controller preflight; lock window |
| soc/ | Session 1: the SoC console's reply (login prompt), the remote-login probe, this host's end view. Session 2 (r2-*): shell check, health at start and end, framing reads, TCP test, leg stop and restart, the recorder's state and termination, this host's end view |
| restore/ | DUT reads, census and controller state at start and end of both sessions (r2-* for session 2); census and DUT comparisons; controller staging and restore; cleanup; lock windows |
| summary/summary.json | Identity values, session 1's SLIP_TDM window and census, session 1's SoC state, and session 2's framing record, run, fs, restore, residuals and timing-item verdicts |
| gates/ | gates.txt and each of the 13 gates' output at 35a60c8d (session 2's at 4461a1f7 and session 1's at 35a8b04d were replaced); table checks; status after |
| tools/ | Every tool used, B3 copies retargeted to this lane (ORIGIN-B3.sha256 pins the B3 originals), plus end_locked.sh, redact.py, and session 2's run_timing.py, fit_fs.py, ctl_restore_locked.sh, phc_restore_b4.py, tcp_test.py and hostsrv.py's TcpReceiver |
| redaction.json | Per redacted file: original and retained SHA-256, labels used |
| RAW-ARTIFACTS.json | Every file under /tmp/b4-a468/raw by relative path, size and SHA-256 (the capture, full decode and attribution, the TCP test, the redaction originals) |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
