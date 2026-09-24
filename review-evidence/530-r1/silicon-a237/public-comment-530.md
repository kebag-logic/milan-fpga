[A237] SILICON RERUN: **PASS** on PR #549 head `c593cbef`

**Identity.**
- Console `ID=4d494c4e` and `VERSION=00020060`.
- The QSPI bitstream payload reads CRC32 `11a89d32`, the asl seed of `c593cbef`. It is not any `50e78097` seed.
- Bare-metal grader 10/10.
- gPTP stayed locked throughout. `SYNC=1 ASCAPABLE=1 TU=0` held in all 1790 console samples of the run, with a stable grandmaster (the bench AVB switch).

**Run B shape.** The reference peer's CRF Stream Input was bound to the DUT's CRF Stream Output by the unchanged #117 self-unbinding window tool, bound for **720.009 s**. Recording:
- a tap capture of the DUT link, with 0 drops;
- GET_COUNTERS every 1 s from the controller host;
- console reads every 0.5 s.

Times are on the tap's hardware clock.

| # | Acceptance | Result | Evidence |
|---|---|---|---|
| a | Streams for the whole bound window; no self-Leave; no restart; across the switch's LeaveAll cycles | **PASS** | **One burst of 719.801 s**, from 0.217 s after the bind to 9 ms after the unbind: 359,897 CRF PDUs at 500/s, intervals 1.995 to 2.005 ms, 0 sequence discontinuities, `tu` 0. While bound, the DUT sent **no TalkerAdvertise Lv and no TalkerFailed**, and the switch sent no Listener Lv. The switch sent **56 LeaveAll MRPDUs** while bound, spaced **10.0 to 14.8 s** (median 13.2 s). The DUT re-declared its TalkerAdvertise 0 to 200 ms after each one, with none missing. Stream Output STREAM_START went 1 to 2 at the bind and STREAM_STOP 1 to 2 at the unbind, with **no other change in 871 reads**. MEDIA_RESET and TIMESTAMP_UNCERTAIN stayed 0. The reference peer counted 0 interruptions and 0 sequence mismatches. The DUT's own LeaveAll MRPDUs now flag all four MSRP types, with NumberOfValues-0 vectors for Listener and TalkerFailed |
| b | First CRF PDU only after the first Listener Ready | **PASS** | First Listener Ready (switch to DUT) at 48.028325 s, **first CRF PDU at 48.029738 s: +1.413 ms**. In UTC, 05:52:26.4158 and 05:52:26.4172 |
| FRAMES_TX | Against the documented 1 s-interval semantics | consistent | It reset at STREAM_START and then rose by +1 at every 1 s read. It ended at **721** for a 719.8 s stream, which spans 721 one-second intervals, and held after the stop. `CRFT_COUNT` rose by 359,897, equal to the wire count |

**Attempt 1** ran the same script on the same image, 05:15 to 05:30 UTC. It completed and unbound itself before a network outage cut the session, so it is corroboration, not the acceptance run.
- Its first probe was answered TALKER_DEST_MAC_FAIL, the #117 item-2 trigger. **No PDU left in the 5.21 s** before the first Listener Ready, and the first PDU followed that Ready by +1.210 ms.
- Otherwise it matched: one 714.8 s burst, 57 switch LeaveAlls while bound, no self-Leave, STREAM_START/STOP 0 to 1 once each, and FRAMES_TX 716.

**Bench.** At resume nothing was running or bound. The four binding censuses agree: before attempt 1, at resume, before attempt 2 and at the end. ACMP read 18/18 unbound and AEM 15/15 identical. The final capture carries no AVTP from the DUT. Nothing was flashed, power-cycled or rewired.

**Observations (not graded).**
1. In 2 of the 113 bound LeaveAll cycles (one per attempt), the DUT's own LeaveAll fired 1.5 to 7.5 ms after the switch's. That MRPDU carried the CRF TalkerAdvertise as `Mt` rather than `JoinMt`. `JoinMt` followed 200 ms later. The switch kept the Listener and emission did not gap.
2. 27 of the DUT's 850 bound MRPDUs repeat the same Domain value in two or three vectors.

I did not check either against the 802.1Q applicant table.

The handoff, raw captures, logs, commands and tool hashes are in the A237 bench packet.
