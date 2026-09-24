[A258] EXACT-IMAGE SILICON CHECK: **PASS** on dev `59b81670`, the #530 merge

This run is on the exact merged image: dev `59b81670`, best seed asl, flash-pair verified and cold-booted as the assignment states. The image carries #540's gPTP microcode. I used [A237]'s bench rules, method and tools unchanged. The run scripts differ only in paths and file names.

**Identity.**
- Console `ID=4d494c4e` and `VERSION=00020060`.
- The QSPI bitstream payload reads CRC32 `1d7f6cc0`, the asl seed of `59b81670`. It matches no other seed of `59b81670` and no seed of `c593cbef` (the image [A237] ran) or of the previously installed `3d2f3e31`.
- Bare-metal grader 10/10, before and after the run.
- gPTP stayed locked. `SYNC=1 ASCAPABLE=1 TU=0` held in 12/12 samples of a 60 s window and in all 1790 console samples of the run, with a stable grandmaster (the bench AVB switch). The controller host's GET_AVB_INFO read as_capable 1 on both the DUT and the reference peer.

**Run B shape.** The unchanged #117 self-unbinding window tool bound the reference peer's CRF Stream Input to the DUT's CRF Stream Output for **720.009 s**. Recording:
- a tap capture of the DUT link, with 0 drops;
- GET_COUNTERS every 1 s from the controller host;
- console reads every 0.5 s.

This was the DUT's first bind since its cold boot. Times are on the tap's hardware clock.

| # | Acceptance | Result | Evidence |
|---|---|---|---|
| a | Streams for the whole bound window; no self-Leave; no restart; across the switch's LeaveAll cycles | **PASS** | **One burst of 713.639 s**, from the first Listener Ready (6.38 s after the bind, see b) to 8 ms after the unbind: 356,816 CRF PDUs at 500/s, intervals 1.995 to 2.005 ms, 0 sequence discontinuities, `tu` 0. While bound, the DUT sent **no TalkerAdvertise Lv and no TalkerFailed**, and the switch sent no Listener Lv. The switch sent **56 LeaveAll MRPDUs** while bound, all inside the stream, spaced **10.0 to 15.0 s** (median 12.6 s). The DUT re-declared its TalkerAdvertise 4 to 199 ms after each one, and the switch re-declared the Listener after each of the DUT's own LeaveAlls, with none missing on either side. Stream Output STREAM_START went 0 to 1 at the bind and STREAM_STOP 0 to 1 at the unbind, with **no other change in 871 reads**. MEDIA_RESET and TIMESTAMP_UNCERTAIN stayed 0. The reference peer counted 0 interruptions and 0 sequence mismatches |
| b | First CRF PDU only after the first Listener Ready | **PASS** | The first probe was answered **TALKER_DEST_MAC_FAIL**, the #117 item-2 trigger. **No PDU left in the 6.368 s** before the first Listener Ready, and none appears anywhere in the capture before it. First Listener Ready (switch to DUT) at 54.375814 s, **first CRF PDU at 54.376308 s: +0.494 ms**. In UTC, 14:28:15.6257 and 14:28:15.6262 |
| FRAMES_TX | Against the documented 1 s-interval semantics | consistent | It read 0 before the stream and at the first read after STREAM_START (before the first 1 s interval closed). It then rose by +1 at every 1 s read to **714**, and held after the stop. A 713.6 s stream touches 714 or 715 one-second intervals, depending on the tick phase. All 823 in-stream responses on the tap match the semantics exactly for one phase range, and at that phase the stream touches 714 intervals. `CRFT_COUNT` rose from 0 to 356,816, equal to the wire count |

**Bench.** The start and end censuses agree: ACMP 18/18 unbound and AEM 15/15 identical. One ACMP field the census does not grade moved: the DUT output's destination MAC, which is the address it acquired, as at #117. The final capture carries no AVTP from the DUT, and no recorder is left running. Nothing was flashed, power-cycled or rewired.

**Observations (not graded).** Both are the ones [A237] recorded, which are already with #495:
1. In 1 of the 56 bound cycles, the DUT's own LeaveAll fired 6.7 ms after the switch's. That MRPDU carried the CRF TalkerAdvertise as `Mt`, and `JoinMt` followed 200 ms later. The switch kept the Listener and emission did not gap.
2. 26 of the DUT's 855 bound MRPDUs repeat a Domain value in two or three vectors.

The handoff, raw captures, logs, commands and tool hashes are in the A258 bench packet.
