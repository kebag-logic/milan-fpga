[A249] DEV SILICON CHECK: **PASS** on dev `3d2f3e31`, with the #540 gPTP pin `e5dcea6e`

Nothing was bound, flashed, power-cycled or rewired. Times are UTC.

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | DUT identity | **PASS** | Console `ID=4d494c4e`, `VERSION=00020060`. The QSPI bitstream payload reads CRC32 `b07f8550`, the eppo seed of `3d2f3e31`. It is not any `c593cbef` seed. ROM `f6afa4ec`, AEM `93742dd2` |
| 2 | gPTP lock, grader, asCapable | **PASS** | Bare-metal grader **10/10** four times, 09:48 to 10:11. The grandmaster is the bench AVB switch. The DUT's path is [GM]. The reference peer is in the same domain, with path [GM, peer]. `SYNC=1 ASCAPABLE=1 TU=0` and `CLKV_STAT=00010002` in **900/900** console samples. The controller's GET_AVB_INFO read as_capable 1 in **900/900** polls on the DUT and 900/900 on the reference peer. Peer delay 375 to 391 ns |
| 2 | Offset and rate (tap, 907 s) | recorded | 904 samples of DUT PHC minus grandmaster time, from the DUT's Pdelay timestamps against the switch's Sync/Follow_Up on the tap clock. **Median +1.7 ns, stdev 10.0 ns, range -24 to +32 ns. Frequency difference -0.006 ppb.** The previous pin on the previous image read median -1.4 ns and stdev 10.1 ns in this morning's A237 capture |
| 3 | Soak >= 10 min, grandmaster stable, no spurious step or `tu` | **PASS, 0 events** | **900 s** sampled every 1 s, 09:51:59 to 10:06:58. The grandmaster was stable: 907 Announces, one GM, stepsRemoved 0, and 7264 Syncs with 0 sequence gaps. `tu` and the step holdover bit were never set (0/900). **`CLKV_TUCNT` (TIMESTAMP_UNCERTAIN) read 10 throughout, and also from 09:48 to 10:11.** It latches every 1 s interval in which a step raised `tu`, so it cannot miss a step between samples. Stream Output `TIMESTAMP_UNCERTAIN` 0 and `GPTP_GM_CHANGED` 0 in 900/900 reads. gPTP drop counters 0. On the wire, the largest 1 s change of the offset was **47 ns, with none above 1 us**. The step policy only steps above 20 us |
| 4 | la_avdecc enumeration, 3 runs | **PASS 3/3** | The DUT was `IEEE17221\|Milan` in all three runs, before and after the soak and at the end. No compatibility events, 0 complaints, 0 query errors, and 0 AECP retries or timeouts. Same binary, libraries and arguments as #529. Each log is identical to #529's step-2 log apart from the order of the online/offline events. The counters probe was CLEAN, with the same transcript as #529 |
| 5 | Restore | **PASS** | The end census equals the start: ACMP 18/18 unbound, AEM settings 15/15. The start census also equals A237's end census from this morning |

**Step counters.** This image has no CSR that counts the plane's steps. The step pulse drives the PHC, the clock-validity holdover (which raises `tu`) and the render re-centre, whose tally is visible in simulation only. So a step was looked for in three places: `CLKV_TUCNT`, `CLKV_STAT` at 1 s, and the wire offset. All three were quiet.

**Not covered.**
- No grandmaster change or link-up was provoked, so the step branch of the policy did not run on silicon here.
- There was no CRF binding, because the #530 talker fix is not on dev.

**The exact-image check that includes #530 follows after #530 merges.**

The handoff, raw captures, logs, commands and tool hashes are in the A249 bench packet.
