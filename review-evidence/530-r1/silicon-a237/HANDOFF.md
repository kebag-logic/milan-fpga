# HANDOFF: issue 530 silicon rerun, A237 bench author, 2026-09-24

Assignment: https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5808071755
Reference checkout: $LANES/530-crf-talker-licence (branch head `446e79b9`, which contains
PR #549 head `c593cbef`; read-only, untouched). Nothing was flashed, power-cycled, rewired or
reconfigured. No repository was edited or pushed. No sub-agent was used. Every bench step ran under
`flock /tmp/milan-bench.lock`.

**Reference checkout note.** The checkout was clean at 07:47 CEST when this session started, and
A237 only read it. Between 08:09:19 and 08:11:06 CEST it gained uncommitted edits to six files that
A237 did not make: `CHANGELOG.md`, `docs/reference/{EGRESS_QUEUE_MAP,FR_NFR,REGISTER_MAP}.md`,
`docs/traceability/ieee8021q.md` and `hdl/milan/milan_datapath.sv` (+122/-39). They are presumably
another session working in the same worktree. A237 left them untouched: no restore, no commit.
No evidence here depends on them. The board runs the flashed `c593cbef` image, and every document
cited was read at `c593cbef`/`446e79b9` before 08:09.

## Outcome

**PASS on both acceptance items. FRAMES_TX matches the documented 1 s-interval semantics.**

The acceptance run is attempt 2 (05:51:36 to 06:06:31 UTC). The reference peer's CRF Stream
Input 8 was bound to the DUT's CRF Stream Output 1 for 720.009 s. The DUT emitted one
uninterrupted CRF burst for 719.801 s: 359,897 PDUs, sequence-continuous, intervals 1.995 to
2.005 ms. The bench AVB switch sent 56 LeaveAll MRPDUs in that window, with no self-Leave and no
restart. Stream Output 1 STREAM_START and STREAM_STOP each moved once. The first CRF PDU left
1.413 ms after the first Listener Ready.

Attempt 1 (05:15:15 to 05:30:10 UTC) ran the same script on the same image. It completed and
unbound itself before the network outage cut the session (see "Bench resume"). It is kept as
corroboration, not as the acceptance run. It is the stronger evidence for item (b): its first
probe was answered TALKER_DEST_MAC_FAIL, the exact #117 item-2 trigger, and no PDU left during the
5.21 s until the first Listener Ready.

## Per-acceptance table (attempt 2 unless marked)

Times are seconds on the tap's hardware clock from the first captured record, unless marked UTC.
UTC is the capture server's clock through a straight-line fit (see "Timebases").

| # | Acceptance (#530 / assignment) | Result | Evidence |
|---|---|---|---|
| 1a | DUT identity: console CSR ID, VERSION `0x00020060`, bitstream from build `c593cbef` | PASS | `identity/console-identity.txt` (05:49:51Z): `ID=4d494c4e`, `VERSION=00020060`, also by `mem_read 0x90000000/4`. The QSPI CRC readback reads bitstream payload `11a89d32`, ROM `f6afa4ec`, AEM `93742dd2`. That payload CRC is the **asl seed of `c593cbef`** (`identity/expected-crc.txt`). The eppo seed is `e5ff3498` and the eto seed `1963bdfc`. The `50e78097` seeds (the previous image) are `b46a9492`, `e5fb8b18` and `a1be376b`. Grader `scripts/baremetal_uart_smoke.py` 10/10 at 05:50:15Z and 06:06:52Z |
| 1b | gPTP locked | PASS | Console `SYNC=1 ASCAPABLE=1 TU=0`, GM `3cc0c6fffefe0210` (the bench AVB switch), `CLKV_STAT=00010002`: 12/12 samples in the 60 s window, **1790/1790 in the bind run**, and every single read. Peer delay 381 to 389 ns in the 60 s window and 377 to 390 ns over the 1790 bind-run samples. `CLKV_TUCNT` stayed 10. gPTP drop counters stayed 0. Controller GET_AVB_INFO shows as_capable 1 in 12/12 polls on both the DUT and the reference peer. GET_AS_PATH is [GM] for the DUT and [GM, peer] for the peer (`bench/gptp/pw1-watch.jsonl`) |
| 2 | Run B shape: peer CRF Stream Input bound to the DUT CRF Stream Output, bounded self-unbinding window >= 600 s, wire captured, counters and console polled | done | `crf_bind_window.py` unchanged from #117 (`29b4ac46…`), args `ens10 30 720 90`. CONNECT_RX on the wire at 47.813198 s (05:52:26.2007Z), DISCONNECT_RX at 767.821821 s (06:04:26.2116Z): **bound 720.009 s**. The tool's 144 bound-state polls all read the peer input connected to the DUT's uid 1. Unbind SUCCESS on the first attempt. Tap capture 388,728 packets, 0 dropped. Controller-port capture 6,537, 0 dropped. GET_COUNTERS 871 reads each of DUT SO1, DUT SO0 and peer SI8, all SUCCESS. Console 1790 rounds at 0.5 s |
| 3a | Keeps streaming for the whole bound window | **PASS** | **One burst**, 48.029738 to 767.830936 s: 719.801 s, **359,897 PDUs**, 499.99 PDU/s. Intervals: min 1.995, median 2.000, max 2.005 ms. **0 sequence discontinuities**. `tu` 0 on every PDU, PCP 3 VID 2, DA `91:e0:f0:00:5a:8e`, stream `0200000000010001`. The first PDU came 0.217 s after the bind and the last 9.1 ms after the unbind. The peer's SI8 counted MEDIA_LOCKED 1, FRAMES_RX 359,892 (= TIMESTAMP_VALID), STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, LATE 0, EARLY 0. It recorded MEDIA_UNLOCKED 1 at the unbind |
| 3a | No self-Leave while bound | **PASS** | While bound, the DUT sent **no MSRP TalkerAdvertise Lv and no TalkerFailed**, and the switch sent no Listener Lv. The DUT's only TalkerAdvertise Lv came at 767.972054 s, 150 ms after the unbind command and 140 ms after the switch withdrew the Listener (767.832125 s) (`bench/run/crosscheck.txt`) |
| 3a | No stream restart: STREAM_START/STOP +1 at bind, +1 at unbind | **PASS** | Stream Output 1 went STREAM_START 1 to 2 at the first 1 s read after the first PDU (tap approx. 48.82 s), and STREAM_STOP 1 to 2 at the first read after the last PDU (768.82 s). There was **no other change in 871 reads**. MEDIA_RESET and TIMESTAMP_UNCERTAIN stayed 0. (Attempt 1 went 0 to 1 and 0 to 1 the same way, so since the cold boot there has been exactly one start and one stop per bind.) Console `CRFT_CTRL` went `0x3` to `0x3002e3` to `0x3`, and `LWSRP_STATUS` `0x0` to `0x250` to `0x0`. Each had exactly two edges in 1790 samples |
| 3a | Across the switch's repeated LeaveAll cycles: count and spacing | **56 cycles, 10.0 to 14.8 s** | Switch LeaveAll MRPDUs in the bound window: **56**, spacing min 10.000, median 13.200, mean 12.778, max 14.800 s (55 intervals). In the whole capture there were 69, spaced 10.000 to 14.800 s. Every one flags Domain, Listener, TalkerAdvertise and TalkerFailed, carrying TalkerAdvertise and TalkerFailed as NumberOfValues-0 vectors. The DUT re-declared its TalkerAdvertise 0 to 200 ms after each (median 8 ms), **none missing**. The DUT's own LeaveAlls while bound: 56, spacing 10.000 to 14.800 s. Each flags all four types, with NumberOfValues-0 vectors for Listener and TalkerFailed (the processor #106/#107 change, seen on the wire). The switch re-declared the Listener 0 to 92 ms after each, none missing |
| 3b | First CRF PDU only after the first Listener Ready, on one timebase | **PASS** | Tap clock: first Listener Ready for `0200000000010001` (switch to DUT, `New/Ready`) at **48.028325 s**, first CRF PDU (DUT to switch) at **48.029738 s**, **+1.413 ms**. UTC: 05:52:26.415804 and 05:52:26.417217. Before the first PDU the switch sent exactly one Listener message for the stream, that `New/Ready`. The probe was answered SUCCESS at 47.821808 s because the DUT still held its DA from attempt 1. **Attempt 1:** first probe answered **TALKER_DEST_MAC_FAIL** (status 3) at 47.640853 s. The DUT declared TalkerAdvertise `New` at 47.731685 after its MAAP grant, and the second probe got SUCCESS at 52.837255. First Listener Ready at **52.848561 s**, first PDU at **52.849771 s**, **+1.210 ms**; UTC 05:16:10.467018 and 05:16:10.468228. **No PDU in the 5.21 s** between the status-3 answer and the Listener Ready. At #117 the DUT began 0.18 ms after that answer. Console `CRFT_CTRL` read `0x300223` in that gap and `0x3002e3` after it |
| 3c | FRAMES_TX against the documented 1 s-interval semantics | consistent | Milan v1.2 Table 5.4 as documented in `docs/reference/REGISTER_MAP.md` `0x764` and `tb/verilator/milan_dp/README.md` ("FRAMES_TX is an interval count"). At the first read after STREAM_START, FRAMES_TX read 1 (reset from attempt 1's 716). It then rose by exactly +1 at every 1 s read (720 steps), final **721**, held through the 109 s after the stop. A 719.801 s stream spans 721 one-second observation intervals. Attempt 1: 716 for 714.801 s. `CRFT_COUNT` (`0x764`, the PDU total) went 357,397 to 717,294, **+359,897, equal to the wire count**. SO0 (AAF) stayed all 0, and no AAF PDU was on the wire |
| 4 | Restore the bench: unbind, census equal to the start | **PASS** | Final census (06:06:50Z) against the attempt-2 start (05:51:24Z) and against attempt 1's start (05:14:01Z): **ACMP 18/18 identical** (peer SI 0 to 9, peer SO 0 to 3, DUT SI 0 and 1, DUT SO 0 and 1, all unbound, count 0). **AEM settings reads 15/15 identical**. The 40 s final tap capture holds no AVTP from the DUT. Console `CRFT_CTRL=0x3`, `LWSRP_STATUS=0`, `LWSRP_SLOPE=0` |

## Bench resume (after the 07:30 to 07:46 CEST network outage)

The details are in `bench/resume/RESUME.md`. The check was read-only under the lock at 05:48:17Z.
Attempt 1 had completed before the cut. Its bind window exited `BIND_RC=0` at 05:29:34Z after
unbinding at the window end. The script stopped every recorder by 05:29:54Z and released the lock
at 05:30:10Z. The outage fell after that, before the remote files were fetched.

- No capture, bind-window or poll process was running on the controller host or the capture server.
- Nothing was bound. The resume census matched attempt 1's start census: ACMP 18/18, AEM 15/15.
- The console was responsive and gPTP was locked.
- The leftover remote files were fetched into `bench/attempt1/`.

No unbind was needed, and the acceptance was rerun from the beginning.

## Observations outside the acceptance (not graded)

1. **Mt in the DUT's LeaveAll MRPDU when the two LeaveAll timers nearly coincide.** This happened
   in 2 of the 113 bound LeaveAll cycles, once per attempt (attempt 2 at 666.77 s, attempt 1 at
   140.93 s). The DUT's own LeaveAll MRPDU went out 7.5 ms and 1.5 ms after the switch's LeaveAll,
   and it carried the CRF TalkerAdvertise as `Mt`, not `JoinMt`. `JoinMt` followed 200 ms later
   (`bench/run/msrp-around-666.txt`, `bench/attempt1/msrp-around-140.txt`). When the DUT's LeaveAll
   preceded the switch's (by 0.2 ms, at 197.77 s) or trailed it by about 207 ms, the value went out
   as `JoinMt`. Neither `Mt` changed the outcome: the switch kept the Listener, sent no Listener Lv,
   and emission did not gap. The margin is the 200 ms Join delay against the switch's leave timer,
   which was not measured. Whether `Mt` at that transmit opportunity matches the 802.1Q applicant
   table (rLA! then txLA!) is not assessed here.
2. **Repeated Domain vectors.** 27 of the DUT's 850 bound MRPDUs carry the same Domain value two
   or three times, e.g. LA=1 `JoinIn` followed by LA=0 `JoinIn` with the same value
   (`bench/run/la-detail.txt`). Attempt 1: 21 of 860. The switch never does this.
3. **Stop at unbind.** The DUT's last PDU (767.830936 s) preceded the switch's Listener Lv on the
   DUT link (767.832125 s) by 1.19 ms. The next 2 ms slot was not used. The TalkerAdvertise Lv
   followed 140 ms after the Listener Lv (attempt 1: 82 ms). Afterwards the DUT sent TalkerAdvertise
   `Mt`, as many times as there were LeaveAll MRPDUs on the link in that phase: 18 after the unbind (9 + 9)
   and 8 before the attempt-2 bind (4 + 4). It sent no Join for the stream before either bind.
4. **Timebases.** The attempt-2 capture-server fit has slope 3.22 ppm and residuals of -3.0 to +7.4 ms
   (attempt 1: 0.32 ppm, -0.4 to +0.6 ms). The capture server's NTP clock slewed during the run.
   Everything graded above is on the tap clock and unaffected. The UTC strings and the
   counter/console alignment carry that error.

## Timebases

The tap stamps each frame in hardware. `wire_summary.records` gives the tap time and the port:
port 3 carries frames the DUT sent and port 2 frames the switch sent toward the DUT. Host-generated
records are excluded (167 in attempt 2). `a237_analyze.py` maps tap time to the capture server's
clock with a least-squares line through the per-5 s minima of (pcap host time minus tap time).
Controller-host times (GET_COUNTERS, bind log) are NTP and are placed on the same axis by
subtraction. Console times are build-box times plus the measured capture-server offset,
+1.2297 s: the mean of 1.228382 at the start and 1.231101 at the end (`bench/clock-*.jsonl`).
Attempt 1 used +1.220162.

## Exact commands (packet root `$REVIEWS/530-a237-packet`, also linked as `$MANAGEMENT/2026-09-23/530-a237`)

```sh
# resume check (read-only), under the lock
timeout 500 flock -w 60 /tmp/milan-bench.lock bash tools/run_resume.sh > bench/resume/lock.txt 2>&1
python3 tools/census_compare.py bench/attempt1/census-start.jsonl bench/resume/census-resume.jsonl > bench/resume/census-compare.txt
scp <bench-host-prefix>pw1:/tmp/a237/{bind.jsonl,counters.jsonl,pw1-run.pcap} <bench-host-prefix>ubuntu-server:/tmp/a237/tap-run.pcap bench/attempt1/
# deployed controller-host tools equal the packet's (bench/deploy-pw1-verify.txt)
ssh <bench-host-prefix>pw1 'cd /tmp/a237 && sha256sum a231_counters_poll.py a237_census.sh avdecc_ro.py crf_bind_window.py'
# attempt 2
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do python3 tools/clock_offset.py $h 25; done > bench/clock-start.jsonl
timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_identity_gptp.sh > identity/lock-window.txt 2>&1
timeout 300 flock -w 60 /tmp/milan-bench.lock timeout 200 ssh -o BatchMode=yes <bench-host-prefix>pw1 'bash /tmp/a237/a237_census.sh' > bench/census-start.jsonl
# the bind run is ~15 min, longer than one tool call, so it was detached and waited on in the foreground;
# crf_bind_window.py runs on the controller host and unbinds by itself even if the build box goes away
setsid nohup bash -c 'timeout 1300 flock -w 60 /tmp/milan-bench.lock bash tools/run_bind.sh > bench/run/lock.txt 2>&1; echo flock_rc=$? >> bench/run/launch.txt' &
scp <bench-host-prefix>pw1:/tmp/a237/{bind.jsonl,counters.jsonl,pw1-run.pcap} <bench-host-prefix>ubuntu-server:/tmp/a237/tap-run.pcap bench/run/
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do python3 tools/clock_offset.py $h 25; done > bench/clock-end.jsonl
timeout 500 flock -w 60 /tmp/milan-bench.lock bash tools/run_final.sh > bench/final-lock.txt 2>&1
scp <bench-host-prefix>ubuntu-server:/tmp/a237/tap-final.pcap bench/final/
python3 tools/census_compare.py bench/census-start.jsonl bench/final/census-final.jsonl > bench/final/census-compare.txt
python3 tools/census_compare.py bench/attempt1/census-start.jsonl bench/final/census-final.jsonl > bench/final/census-compare-vs-attempt1-start.txt
# analysis (offline)
cd bench/run && python3 ../../tools/a237_analyze.py tap-run.pcap --counters counters.jsonl --bind bind.jsonl \
  --console console.txt --console-offset-s 1.2297 --json analysis.json > analysis.txt
cd bench/attempt1 && python3 ../../tools/a237_analyze.py tap-run.pcap --counters counters.jsonl --bind bind.jsonl \
  --console console.txt --console-offset-s 1.220162 --json analysis.json > analysis.txt
python3 tools/a237_crosscheck.py  <run>/tap-run.pcap <run>/analysis.json > <run>/crosscheck.txt
python3 tools/a237_la_detail.py   <run>/tap-run.pcap <run>/analysis.json > <run>/la-detail.txt
python3 tools/a237_msrp_around.py bench/run/tap-run.pcap 666.771838 1.5 > bench/run/msrp-around-666.txt
python3 tools/a237_msrp_around.py bench/attempt1/tap-run.pcap 140.931882 0.5 > bench/attempt1/msrp-around-140.txt
```

What `run_bind.sh` does, in order:

1. Starts the recorders, all bounded by `timeout`:
   - tap capture (`tcpdump -i <tap if>` on the capture server);
   - controller-port capture (`ether proto 0x22f0`);
   - console poll every 0.5 s: `milan_status`, `CRFT_CTRL`, `CRFT_COUNT`, `LWSRP_STATUS`, `ACMP_TALKER`, `CLKV_TUCNT`, `GPTP_DROPW`, `GPTP_DROPE`.
2. Refuses to bind unless both captures are listening and the console transcript is growing.
3. Starts GET_COUNTERS every 1 s on DUT SO1, DUT SO0 and peer SI8.
4. Runs `crf_bind_window.py ens10 30 720 90` on the controller host. The tool refuses unless the input reads unbound, and it unbinds at the window end, on a signal and on any exception.
5. Stops the recorders.

## Tool hashes (sha256)

| Tool | sha256 | Origin |
|---|---|---|
| crf_bind_window.py | `29b4ac468f5fb58f53053db353be675c0d8aad84e6a296fc02722140aa8ee152` | #117 A200 packet, unchanged |
| avdecc_ro.py | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` | #117 A200/A202, #529 A231, unchanged |
| a231_counters_poll.py | `c32a20bc33c64ce96fc95212df13f1fc92e7808c67570792e8b2fafbd46920f7` | #529 A231, unchanged |
| wire_summary.py | `c5039d950eaf42e274cfaddfc38f3845bd66dd8cba011899fbd3172ef66a3d5e` | #117 A200/A202, unchanged |
| console_read.py | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` | #117 A200/A202, #529 A231, unchanged |
| console_poll.py | `3a0de7d8e1f9f4e0f87d03364c3cf35e9965210dd7095b21ef9d1b7bdb1bd326` | #117 A200/A202, #529 A231, unchanged |
| census_compare.py | `40424c61b958a42e2f4da4415fe0c1f7c37b75aec9085c516d1874f1e0e9b4f2` | #117 A202, unchanged |
| clock_offset.py | `950533caa8d3a2bb1c42ae4d2a60f56769cb8877a9b82149bd74e52fe6e6590d` | #117 A202, unchanged |
| expected_crc.py | `04d128bb0a9ffe8ad5898f4ece380899a096a1595aadda3ece1048c313bf19d7` | #117 A200/A202, #529 A231, unchanged |
| baremetal_uart_smoke.py | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` | `scripts/baremetal_uart_smoke.py` at `c593cbef`, unchanged |
| a237_census.sh | `d29f1176062d2a268e4f8585068fa6483eadf9a8934466f256edfae88c126227` | #529 `a231_census.sh` with the remote path `/tmp/a231` changed to `/tmp/a237` |
| a237_analyze.py | `7ea34430f95c94c5e71b36228e9b7787864ed020a0c72ff03a988b086a2563c9` | new (A237) |
| a237_crosscheck.py | `fe725f823c9f8bdfc28805551fee9d863aeada2b801cbacb77761c6c766389a2` | new (A237) |
| a237_la_detail.py | `bac70bb20813903f81730be59aa45a576c4323d46f89af9aec0ee1dbc105050b` | new (A237) |
| a237_msrp_around.py | `14226aa75d3147140a521ea5fe1467ea7e9aecb2eeabbea6ad502fbcaeea0d96` | new (A237) |
| run_resume.sh | `6a78680196c9422765917908fa6ee53ee98bd9a39d749695969a9a762b75ec15` | new (A237) |
| run_identity_gptp.sh | `92644d4e01f2a847a6c45fc83821a23efd58e4f3e39d4459691d8b169fcd3c41` | new (A237) |
| run_bind.sh | `e0c1cd18c114710dcb6997059847e29eb252ea8e6d6d703073e59679c23da156` | new (A237) |
| run_final.sh | `eed44d57472dccd01959c0bc846df4b1d29c8504b419d6d97e273d5755356a3c` | new (A237) |

Host tools: Python 3.14.6 on the controller host, tcpdump 4.99.6 / libpcap 1.10.6 (`tools/deploy-pw1.sha256`).

## Raw data (hashes in `MANIFEST.sha256`)

| Artifact | Attempt 2 (`bench/run/`) | Attempt 1 (`bench/attempt1/`) |
|---|---|---|
| tap capture of the DUT link | `tap-run.pcap` `9733dc49…` | `tap-run.pcap` `638d0035…` |
| controller-port capture (AVDECC) | `pw1-run.pcap` `fe6aba5f…` | `pw1-run.pcap` `99992427…` |
| bind-window log | `bind.jsonl` `801feecc…` | `bind.jsonl` `10fc02b0…` |
| GET_COUNTERS log | `counters.jsonl` `9fd10a2c…` | `counters.jsonl` `11b61484…` |
| console transcript | `console.txt` | `console.txt` |
| analysis | `analysis.txt`, `analysis.json`, `crosscheck.txt`, `la-detail.txt`, `msrp-around-666.txt` | the same set, `msrp-around-140.txt` |
| run receipts | `timeline.txt`, `launch.txt`, `lock.txt`, `*.rc`, `tcpdump-*.log` | the same |

- Identity: `identity/`.
- gPTP window: `bench/gptp/`.
- Censuses:
  - attempt-2 start: `bench/census-start.jsonl`;
  - attempt-1 start: `bench/attempt1/census-start.jsonl`;
  - resume: `bench/resume/census-resume.jsonl`;
  - final: `bench/final/census-final.jsonl`.
- Final state: `bench/final/`.
- Clock offsets: `bench/clock-start.jsonl` and `bench/clock-end.jsonl`, with attempt 1's in `bench/attempt1/`.

`counters-poll.rc` reads `CTR_RC=143` in both attempts. That is the script's own SIGTERM, which
ends the poll after the post window by design (`ctr_stop_rc=0` in `timeline.txt`). The final
capture's `capture_rc=124` is its `timeout 40` expiring, also by design.

## Public comment

https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5808765013, posted
2026-09-24T06:13:35Z. `public-comment-530.md` is the posted text, and
`posted-comment-530.readback.md` is the API readback, identical except for one trailing newline.
