# [A403] Bench handoff: #451 TDM8 first light retry

Refs #451. Session 1: 2026-09-28, 14:02 to 14:55 CEST (STOP). Session 2:
2026-09-28 from 15:58 CEST; bench actions 16:00 to 16:22 (DIN re-run after
the owner's wiring check; REVIEW READY).

Status: REVIEW READY. Both directions decode in all eight slots, in order,
over 70 s each. The first session's all-zero DIN came from the DUT talker's
empty dynamic output map, not the wiring. One DUT property (DIN frame
coherence across pairs) is an open risk for a separate issue. Bench fully
restored; lock released.

Branch `451-tdm8-first-light`, base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
Local commits, not pushed, no PR:

- `361d1f47fe29ada509f99813001369188217eaaa` (session 1): adds
  `docs/findings/451_TDM8_FIRST_LIGHT.md`, removes the attempt page.
- `4f06bfc762724a71999371840a36fadfc1cf08d9` (session 2): updates the page.
  Gate 7 failed here on the word for the SoC's playback command.
- `6339479d69830614d4267bd3170113737afbf8f4` (session 2, head): rewords that
  line. All nine gates rc 0 here (`gates-s2/`). Nothing was amended.

Comments: TAKEN https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5869431595 ;
STOP https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5870277592 ;
REVIEW READY https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5872125759
(read back equal to REVIEW-READY.md).

## Results

| Direction | Window | Decode | Continuity |
|---|---|---|---|
| DOUT (s1) | 70 s SoC capture, 3,357,952 frames | All 8 channels in order: SoC channel k = stream channel k = TDM slot k; 0 torn; 0 invalid | 34 beat clusters; 17 underruns (9 after logged talker lateness) |
| DOUT (s2) | 3 s SoC capture, 144,000 frames | Same; 0 torn; 0 invalid; 0 zero | 2 beat clusters, 93,989 frames apart, net one drop each |
| DIN (s1) | 70 s playback in 94.8 s | All zero (empty output map) | 0 AVTP sequence gaps |
| DIN (s2 run 1, unchanged method) | 70 s playback in 94.9 s | All 4,554,432 frames zero | 0 AVTP sequence gaps |
| DIN (s2 run 2, output map routed) | 70.001 s playback region, 3,360,035 frames | All 8 channels: stream channel k = tag k+1 = TDM slot k, every word valid | Per channel only 35 or 36 beat clusters (93,990 to 93,993 apart), net one repeat each; 0 AVTP gaps in 758,870 PDUs |

DIN frame coherence (open risk): L/R of each pair always agree; pairs 1 to 3
lag pair 0 by one TDM frame in 67.5% of frames ([0,0,-1] 22.7%, [0,-1,-1]
22.7%, [-1,-1,-1] 22.2%), cycling once per 1.958 s beat. Mechanism:
`KL_chan_map_capture.sv` per-pair holds (lines 486 to 487) read at the media
tick with no frame buffer (lines 958 to 960). Not filed as an issue (not
authorized here); coordinator to triage.

Frame-rate offset: SLIP_TDM 10,682 -> 14,893 over 8,244.7 s = 0.5108/s =
10.64 ppm (plan -10.64 ppm). Idle DIN line reads `0xffffff00` (high) once
routed.

## Session 2 timeline (CEST)

- 15:59 Context reloaded; no new #451 comment since the STOP.
- 16:00 Host: no UAC2 card, no ECM link (as the owner said); lock free.
- 16:00 SoC health (read-only): same boot as session 1 (uptime 9,962 s), image
  build #6, legs 911 (to-host, holds hw:0,0 capture) and 912 (from-host,
  holds hw:0,0 playback, XRUN) running; UDC reports configured; BAD=0,
  taint 0. McASP0 RX DMA 1,254 events in 5.02 s (249.8/s): clocks arrive.
- 16:01 DUT read-only: VERSION 00020060, PP_STAT 5b000c44, control words
  equal to session 1's final state; SLIP_TDM 11,859 -> 14,261 over 4,703 s
  (0.511/s): no DUT reset. Controller clean (no /tmp/a403, no ptp4l).
- 16:04 On-board period build test (awk | xxd -r -p): 4.3 s, SHA-256 equals
  the host period b6a92e97...; file removed. Board has no `stat`.
- 16:05 Controller tools staged (hashes equal the executed session-1 copies).
  Census: 32/33 equal to session 1's after-census (pdelay 386 -> 383 ns).
- 16:05:33 Legs 911/912 stopped by PID (cmdlines verified); all PCMs closed.
- 16:05:41 to 16:07:38 DIN run 1 (`din2-long`, unchanged method): all zero;
  aplay rc 0; TX DMA 1,648 periods in 70.06 s.
- 16:08 to 16:11 Cause found in the image: GET_AUDIO_MAP on STREAM_PORT_OUTPUT 0
  answers number_of_maps 1, given only for a dynamic output port
  (`ADP_DMAP_OUT_MASK_C` = 1 in the 1x1_tdm8 shape); `cap_xbar_live_w` is
  then true (milan_datapath.sv:1344) and the empty crossbar map sends silence.
  Session 1's "default front end" statement and its wiring inference were
  wrong (operator error; the owner's wire check followed from it).
- 16:11:16 to 16:13:12 DIN run 2 (`din3-long`): same plus 8 identity
  mappings on STREAM_PORT_OUTPUT 0 (map-add SUCCESS, map-remove SUCCESS, read
  back empty). Decoded in all 8 slots.
- 16:15:29 to 16:15:56 DOUT sanity (`dout2-sanity`, 3 s): bind, map, capture,
  unmap, unbind all SUCCESS. The console transfer then failed (the board's xz
  only decompresses) and the exception skipped the rest of `finally`; the
  talker ended on its own deadline. 16:16:51 to 16:21 re-fetched with gzip
  (`fetch_capture.py`, SHA-256 equal to the board's); 16:21:00 board file
  removed, controller logs taken and DUT read by hand.
- 16:21:27 Legs restarted: to-host PID 1224, from-host PID 1225.
- 16:21:46 Census after (32/33 vs session start; pdelay 383 -> 381 ns);
  controller /tmp/a403 copied and removed; DUT final read. Last bench action.
- 16:22 onward: offline analysis, page, commits, gates, packet (no bench).

## Session 1 timeline (CEST, corrected from the evidence timestamps)

The first version of this handoff gave wrong clock times. These are from the
logs.

- 14:02 TAKEN posted. 14:03 to 14:12 SoC read-only health and McASP0 tree.
- 14:04 DUT UART identity PASS; AECP ENTITY/CONFIGURATION byte-identical.
- 14:11 SRP baseline. About 14:13 INCIDENT (own tool): GET_AUDIO_MAP coded
  0x002A (REBOOT); two REBOOTs refused NOT_IMPLEMENTED; no reset (14:14 check).
- 14:16 gPTP trial on the controller port (slave-only ptp4l synced in about
  1 s). 14:19 DUT PHC rate.
- 14:20 Legs 403/404 stopped by PID; direct 3 s capture all zero.
- 14:21 DOUT preflight 1 failed (talker dropped its own probes). 14:23 probe
  debug. 14:25 DOUT preflight 2: first light. 14:27 to 14:30 DOUT 70 s run.
- 14:34 DIN preflight 1 (first probe TALKER_DEST_MAC_FAIL). 14:36 MRP debug.
  14:37 DIN preflight 2. 14:39 to 14:41 DIN 70 s run: all zero.
- 14:42 DUT final state. 14:43 legs restarted (911, 912).
- 14:50 gates at 361d1f47. 14:55 STOP posted.

## Restoration (after session 2)

- SoC: legs restarted with exactly
  `nohup alsaloop -C hw:0,0 -P hw:1,0 -c 8 -r 48000 -f S32_LE -t 8000 -S samplerate -z >/dev/null 2>&1 </dev/null &`
  (PID to `/run/tdm8/to-host.pid`) and the same with `-C hw:1,0 -P hw:0,0`
  (`/run/tdm8/from-host.pid`), then `disown -a`. Status: both running (1224,
  1225); PCM states as at baseline (hw:0,0 playback XRUN, as before); UDC
  configured; BAD=0; taint 0; board /tmp holds only system files. No gadget
  down/up, no UDC write, no pkill.
- DUT: all streams unbound; input and output maps empty (read back); every
  control word and PP_STAT equal to the session start; only counters moved.
  No CSR was ever written.
- Peer: untouched.
- Controller: `/tmp/a403` copied to the raw root and removed; no ptp4l,
  tcpdump or task process.
- Host: no task process; lock free. The UAC2 card and ECM link are still not
  visible here (they were not at the start; the owner must re-attach).

Residuals (unchanged from session 1): DUT STREAM_OUTPUT 0 reports its MAAP
destination; PP_STAT bit 11 (nvm_pend) set; controller NIC clock at ptp4l's
last frequency with hardware timestamping on; counters advanced (render rails
142 -> 144, slip counters, AAF frames).

## Paths (private)

Raw root `/tmp/a382` on this host; session 2 under `/tmp/a382/s2`. Large
captures: `s2/din2-long/din2-long.pcap`, `s2/din3-long/din3-long.pcap`,
`s2/dout2-sanity/dout2-sanity.raw`, the 2.7 MB console transfer transcript
`s2/dout2-sanity/soc-fetch2.log`, plus session 1's files. `s2/bench.env`
holds the bench identifiers for the tool environment; `s2/tools/package_s2.py`
holds the redaction map (both private, indexed, never copied). `venv-md/`
holds the pinned Markdown renderer for two gates and the table check; it is
excluded from the index and may be deleted.

## Next owner

- Coordinator: publish the three local commits and arrange two independent
  reviews (PR-BODY.md is prepared). Triage the DIN frame-coherence property as
  a new issue.
- Owner: re-attach the SoC board's USB function to the bench host if the
  USB audio path is needed; NOT RUN items remain (recorded continuity check,
  scope, #386 acceptance 4, #117).
