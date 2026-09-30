# [A453] Bench lane B3 handoff

Refs #617 (acceptance 4). Refs #451 (capture through the USB Audio device; continuity check).

Assignment: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5903384996
Branch: b3-bench-0930 from dev ec0cc0c1df7d7ab3e25d973958f53f0074393d2c (lane worktree, physical /data path).
Packet: this directory. Large raw captures stay outside it under /tmp/b3-a453/raw and are indexed by size and SHA-256.

## State

REVIEW READY posted 2026-09-30T04:04Z: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5903778274 (REVIEW-READY.md is the posted text; REVIEW-READY.readback.md and TAKEN.readback.md are the API readbacks, identical but for one trailing newline).

Commit `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` on b3-bench-0930: one commit on ec0cc0c1, one-line subject, no body, no trailers; local only, not pushed, no PR; worktree clean.
Bench work finished 05:50 CEST; everything restored and proven; bench lock free (non-blocking flock rc 0); no task process on this host or the controller.
No DUT flash, reset or power cycle; no outlet read or switched; no DUT PHY or CSR write (only the first-light method's AECP map and ACMP bind edits, all removed); no wiring or instrument change; no USB gadget down/up or UDC write; no SoC board change beyond stopping and restarting its two bridge legs by the recorded method.

Verdicts (operator measurements): identity PASS; #617 acceptance 4 PASS (0 torn); DIN and DOUT order PASS (identity); render path unchanged PASS; #451 capture through the USB Audio device FAIL (both runs); #451 continuity check NOT RUN (needs a meter on unpowered boards).

Times in the action table are CEST; the step ledger uses UTC (Z).

## Step ledger

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | TAKEN on #617 | POSTED 03:20Z: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5903420728 | TAKEN.md |
| 1 | Identity gate | PASS 03:26Z: VERSION 00020060; AEM CRC 93742dd2 (7,352 B); entity 020000fffe000001; ENTITY 312 B and CONFIGURATION 106 B from AECP byte-equal to the QSPI AEM bytes; NVM slot B seq 230 authoritative, backed=1; grader 10/10; ROM acad92b9 (53,344 B), QSPI payload d178f19a (3,825,788 B) | identity/ |
| 2 | SoC board read-only health, baseline census | DONE 03:28Z: SoC same boot (uptime 144,847 s), kernel #6, bridge legs to-host 1224 / from-host 1225 running, UDC configured, BAD=0, taint 0, McASP0 RX 1,252 TR events in 5.02 s; census: 18/18 stream states unbound, both DUT maps empty, DUT clock source 0 at 48 kHz; SLIP_TDM dups 333 skips 0; controller: no gPTP daemon, PHC freq and trajectory recorded, timestamping tx 1 rx 1 | soc/start-health.log, restore/*-start.* |
| 3 | #617 acc. 4: DIN routed 70 s | DONE 03:29:48-03:31:46Z: 758,604 PDUs, 0 sequence gaps; playback region 3,360,036 frames (70.001 s); 0 torn frames in the whole recording; every word valid in the region; channel c = tag c+1 = TDM slot c; 36 whole-frame repeats, identical frames in all 8 channels, 93,990-93,993 apart; SLIP_TDM dups +36 over the playback, skips 0 | runs/din-long/ |
| 4 | #617 acc. 4: DOUT 70 s (render unchanged) | DONE 03:33:49-03:36:08Z: 3,360,000 frames, 0 torn, 0 invalid, 0 zero; SoC channel c = tag c+1 = slot c; 59 clusters: 36 beat (696 repeats, 732 skips, net one drop each, 93,989-93,992 apart), 23 underrun (12 after logged talker lateness at multiple 7, 11 without); AVTPRX_ERR 0, depacketizer drops 0, ts_delta 1.98 ms, render rails 4 -> 134; TFTP 107,520,000 B verified by SHA-256 | runs/dout-long/ |
| 5 | #451: capture on the host USB Audio card through the bridge, >= 70 s | DONE, FAIL (no STOP condition) 03:37:46-03:46:57Z: two 75 s runs (usb-long, usb-long2), each 3,600,000 frames, full length, rc 0, card present throughout. 0 frames pass the strict pattern rule in either run: ~97.5% of words carry a non-zero low byte (a small tag-proportional offset, the bridge's sample-rate-converting copy), the eight tags arrive as a cyclic rotation of the slot order that changes 2,833 / 238 times (identity order in 9.6% / 11.9% of frames), silent frames 327,339 in 2,420 stretches / 3,244 in 4. Bridge side: McASP0 RX 250.0 periods/s (18,942 and 18,957 periods in about 75.8 s, 75.78 s and 75.83 s between the same uptime read of the before and after status logs), 5 capture restarts per run | runs/usb-long*/, receipts/mcasp-rx-rate.txt |
| 6 | #451 continuity check | NOT RUN: it needs a meter on the unpowered boards (J11 pins 1, 37, 38 to ground; the amendment's per-wire ohm readings); no instrument, power or wiring action is allowed in this lane | |
| 7 | Restore and proof | DONE 03:49:17-03:50:01Z: controller PHC frequency reads back as found (28062.332153 ppb) and back on its recorded trajectory (residual 4.4 us), timestamping tx 1 rx 1 as found, no gPTP daemon, staging removed; census end 33/33 equal to start; DUT control words equal; SoC same boot, legs running with the recorded command lines (PIDs 1498/1499 replace 1224/1225), UDC configured, BAD=0, /tmp as found; host: card present, nothing running; lock free. Residual: DUT NVM persistence advanced (commits ok 0 -> 6, slots 229/230 -> 235/236, pend=1, PP_STAT bit 11 set) by the method's map and bind edits | restore/ |
| 8 | Findings pages, gates, commit | DONE: commit 6dfa64a7506a8660a70d77eaa7c96c5de2886f5d (one line, no body, no trailers, local, not pushed; worktree clean); docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md and docs/findings/451_USB_AUDIO_CAPTURE.md; all 10 gate invocations rc 0 at that head (gates/gates.txt); table cell-count check OK on both pages | gates/ |
| 9 | REVIEW READY on #617 | POSTED 04:04Z: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5903778274 | REVIEW-READY.md, REVIEW-READY.readback.md |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 05:26:21-05:26:50 | identity gate + controller preflight (tools staged in /tmp/a453 on the controller) | PASS |
| 05:28:10-05:28:17 | start baseline (SoC health, DUT reads, census, controller PHC) | all rc 0 |
| 05:29:38-05:29:44 | SoC bridge legs 1224/1225 stopped by PID (command lines checked against status) | KILLED; all PCMs closed; UDC configured; BAD=0 |
| 05:29:48-05:31:46 | DIN routed run `din-long` (listen 95 s, play 70 s) | all steps rc 0; maps read back empty |
| 05:33:49-05:36:08 | DOUT run `dout-long` (talker 125 s, capture 70 s, TFTP over the USB network link) | all steps rc 0; unbound; map read back empty |
| 05:37:36-05:37:39 | SoC bridge legs restarted with the two recorded lines | STARTED; to-host 1498, from-host 1499; UDC configured; BAD=0 |
| 05:37:46-05:40:19 | USB run `usb-long` (talker 140 s, 75 s capture on this host's USB Audio card) | all steps rc 0; 115,200,000 B |
| 05:44:24-05:46:57 | USB run `usb-long2` (identical repeat) | all steps rc 0; 115,200,000 B |
| 05:49:17-05:49:17 | controller state read (no daemon; timestamping tx 1 rx 1) | rc 0 |
| 05:49:25-05:49:26 | controller logs copied; PHC restored; staging removed | rc 0 |
| 05:49:37-05:49:37 | PHC frequency re-set so it reads back as found | 28062.332153 ppb |
| 05:49:54-05:50:01 | end snapshot (SoC, DUT, census, controller) + staging cleanup | all rc 0 |

## Deviations and incidents

- The packet's avdecc_rw.py reads the peer identity from the environment, which sudo drops; the run tools pass PEER_EID/PEER_MAC (and GM_ID for the talker's advertisement) through `sudo env`. First light's executed copies had literals.
- The first USB grade model rounded each word to the nearest pattern word; the low byte is a tag-proportional offset, so the grader was changed to read the recipe's 24-bit sample (bits 31:8) and then to fractional ordinals. The page numbers come from the final grade_usb.py (hash in the #451 page); the strict first-light decoder result (0 valid frames) is unchanged by any model.
- USB capture repeated once (usb-long2), identical method, to show the failure reproduces.
- The controller PHC was first restored to the as-found frequency value, which reads back quantized (28062.316895 ppb); it was re-set with lane B1's value so it reads back as found (28062.332153 ppb).
- The redaction pass ran twice (the first missed an upper-case grandmaster identifier); the tool re-reads the saved originals, so the retained files and hashes are from one clean pass.
- PR #619 (builder and tooling) is also in the image history, beside the PRs the assignment lists; it changes no RTL, and the ROM CRC equals 13eda870's.
- Not done: the findings index row (no other doc edit allowed).
- Round 2 ([A456], documentation only, no bench access): step 5's McASP0 receive rate is corrected from 250.7 to 250.0 periods/s (R414-1 F2). 250.7 paired the before log's closing uptime read with the after log's opening one, the shortest interval the two reads allow; receipts/mcasp-rx-rate.txt re-derives the consistent bracket. The findings index rows were added under the round-2 ruling. summary/summary.json gains each USB run's McASP0 bracket and the eight words of `usb-long` frame 1,632 (summary/usb-long-frame-1632.json, from tools/usb_frame_words.py over the raw capture, SHA-256 checked).

## Residuals (no permitted command restores them)

- DUT NVM persistence advanced through the method's map and bind edits: commits ok 0 -> 6, slots seq 229/230 -> 235/236, pend=1, PP_STAT 5b000444 -> 5b000c44 (bit 11). Live maps and bindings equal the start.
- SoC bridge legs run under new PIDs (1498 to-host, 1499 from-host).
- Controller PHC: back on the recorded trajectory within about 4-6 us.

## Packet layout

| Path | What |
|---|---|
| TAKEN.md, REVIEW-READY.md, REVIEW-READY.readback.md | posted texts and the API readback |
| PR-BODY.md | proposed PR body |
| identity/ | console CRC and descriptor readback, grader, AECP-vs-QSPI comparison, ADP discovery, controller preflight, lock window |
| soc/ | SoC board health at start and end, bridge stop and restart transcripts |
| runs/<action>/ | din-long, dout-long, usb-long, usb-long2: events, DUT reads, controller transactions and logs, SoC logs, decodes and grades (large grade files as grade-summary.json); runs/controller/ the controller's per-action gPTP and talker/listener logs |
| restore/ | census start/end and comparison, DUT reads start/end, controller state, PHC restore, cleanup, lock windows |
| summary/ | summary.json and the generated page tables; usb-long-frame-1632.json, the first non-silent USB frame's eight words (round 2) |
| tools/ | every tool used; ORIGIN-A403.sha256 pins the first-light tools as copied; usb_frame_words.py (round 2) |
| receipts/ | mcasp-rx-rate.txt, the McASP0 receive-rate bracket (round 2) |
| gates/ | gate outputs, gates.txt, table checks |
| redaction.json | per redacted file: original and retained SHA-256, labels used |
| RAW-ARTIFACTS.json | every raw file under /tmp/b3-a453/raw by relative path, size and SHA-256 (captures, full grades, redaction originals) |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |

Private endpoints and the redaction map stay in /tmp/b3-a453/private (not in the packet).
