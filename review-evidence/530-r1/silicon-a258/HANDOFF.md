# HANDOFF: issue 530 exact-image silicon check, A258 bench author, 2026-09-24

Assignment: https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5815962401
Reference checkout: `$VALIDATION_STORAGE/worktrees/build-dev-59b816708852`, dev `59b816708852472da6ed4576386c30ebd5f8f839`
(the #530 merge; clean before and after, read-only, untouched). Image on the board: build
`build_ax7101_asl_tdm8dev59b81670`. It was flash-pair written and verified by the manager at 14:12:45 to 14:15:51Z,
and the DUT cold-booted to `VERSION=00020060` with the entity enabled
(`../build-59b81670/flash.log`, `console-after-flash.log`). Nothing was flashed, power-cycled, rewired or
reconfigured by A258. No repository was edited or pushed. No sub-agent was used. Every step that touched
the console, the tap capture or the bench network ran under `flock /tmp/milan-bench.lock`.

## Outcome

**PASS on both acceptance items, on the exact merged image. FRAMES_TX matches the documented 1 s-interval
semantics on every read.**

The reference peer's CRF Stream Input 8 was bound to the DUT's CRF Stream Output 1 for 720.009 s
(14:28:09.249 to 14:40:09.260 UTC). This was the DUT's first bind since its cold boot, so it held no
destination address. The first probe was answered TALKER_DEST_MAC_FAIL, the exact #117 item-2 trigger.
The DUT sent no PDU until the first Listener Ready 6.368 s later, and its first PDU followed that Ready by
0.494 ms. From then on it emitted one uninterrupted CRF burst of 713.639 s up to the unbind: 356,816 PDUs,
sequence-continuous, with intervals of 1.995 to 2.005 ms. The bench AVB switch sent 56 LeaveAll
MRPDUs in that span. The DUT sent no self-Leave, and there was no restart. Stream Output 1 STREAM_START
and STREAM_STOP each moved once.

This run has the shape of A237's attempt 1 on `c593cbef`: a first probe answered status 3, then a single
burst, bound for the same 720 s.

## Per-acceptance table

Times are seconds on the tap's hardware clock from the first captured record, unless marked UTC. UTC is
the capture server's clock through a straight-line fit (see "Timebases").

| # | Acceptance (#530 / assignment) | Result | Evidence |
|---|---|---|---|
| 1a | DUT identity: console CSR ID, VERSION `0x00020060`, bitstream from build `build_ax7101_asl_tdm8dev59b81670` of dev `59b81670` | **PASS** | `identity/console-identity.txt` (14:25:34Z): `ID=4d494c4e`, `VERSION=00020060`, also by `mem_read 0x90000000/4` (`4e 4c 49 4d`, `60 00 02 00`). The QSPI CRC readback gives bitstream payload **`1d7f6cc0`**, ROM `f6afa4ec`, AEM `93742dd2`. That payload CRC is the **asl seed of `59b81670`** (`identity/expected-crc.txt`, computed from the build directory). The other `59b81670` seeds are eppo `4712e52c` and eto `15b44c0e`. The previously installed image, eppo `3d2f3e31`, is `b07f8550` (asl `ad9185ae`, eto `b8452657`), and the `c593cbef` asl image that A237 ran is `11a89d32`. Grader `baremetal_uart_smoke.py` passed 10/10 at 14:25:58Z and 14:42:38Z |
| 1b | gPTP locked (grader, asCapable) | **PASS** | Grader `gptp-locked`, `clkv-fabric-owner` and `gptp-pdelay` PASS, both times. Console `SYNC=1 ASCAPABLE=1 TU=0` with `CLKV_STAT=00010002` and GM `3cc0c6fffefe0210` (the bench AVB switch) as parent: **12/12** samples in the 60 s window and **1790/1790** in the bind run. Peer delay was 378 to 392 ns in the window and 376 to 391 ns over the run. `CLKV_TUCNT` held at `0xb`, and `GPTP_DROPW`/`GPTP_DROPE` stayed 0 over all 1790 samples. `AS_PATH_COUNT=1 AS_PATH_GEN=2` never changed. Controller GET_AVB_INFO read as_capable 1 in 12/12 polls on both the DUT and the reference peer. GET_AS_PATH read [GM] for the DUT and [GM, peer] for the peer (`bench/gptp/controller-host-watch.jsonl`) |
| 2 | Run B shape: peer CRF Stream Input bound to the DUT CRF Stream Output, bounded self-unbinding window >= 600 s, wire captured, counters and console polled | done | `crf_bind_window.py` unchanged from #117 (`29b4ac46…`), args `ens10 30 720 90`. CONNECT_RX was on the wire at 47.998910 s (14:28:09.2488Z) and DISCONNECT_RX at 768.007468 s (14:40:09.2601Z): **bound 720.009 s**. All 144 bound-state polls read the peer input connected to the DUT's uid 1, status 0 and connection count 1. The first two (bind+0 and +5 s) were before the successful probe and show stream id and DA 0; the other 142 show `0200000000010001` / `91:e0:f0:00:43:10`. Unbind succeeded on the first attempt, and the tool exited `BIND_RC=0`. Tap capture: 385,585 packets, 0 dropped. Controller-port capture: 6,531, 0 dropped. GET_COUNTERS: 871 reads each of DUT SO1, DUT SO0 and peer SI8, all SUCCESS. Console: 1790 rounds at 0.5 s |
| 3a | Keeps streaming for the whole bound window | **PASS** | **One burst**, 54.376308 to 768.015610 s: 713.639 s, **356,816 PDUs**, 499.99 PDU/s. Intervals: min 1.995, median 2.000, max 2.005 ms. **0 sequence discontinuities**. Every PDU has `tu` 0, PCP 3, VID 2, DA `91:e0:f0:00:43:10` and stream `0200000000010001`. The burst starts at the first Listener Ready, 6.377 s after the bind (item 3b explains the wait). It ends 8.1 ms after the unbind command and 1.86 ms before the switch's Listener Lv reached the DUT link (768.017466 s), and the next 2 ms slot was not used. The peer's SI8 counted MEDIA_LOCKED 1, FRAMES_RX 356,811 (= TIMESTAMP_VALID), STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, LATE 0, EARLY 0 and UNSUPPORTED_FORMAT 0, and MEDIA_UNLOCKED 1 at the unbind |
| 3a | No self-Leave while bound | **PASS** | While bound, the DUT sent **no MSRP TalkerAdvertise Lv and no TalkerFailed**, and the switch sent no Listener Lv. The DUT's only TalkerAdvertise Lv came at 768.101158 s: 93.7 ms after the unbind command and 83.7 ms after the switch withdrew the Listener (`bench/run/crosscheck.txt`, `msrp-around-768.txt`) |
| 3a | No stream restart: STREAM_START/STOP +1 at bind, +1 at unbind | **PASS** | Stream Output 1 went STREAM_START 0 to 1 at the first read after the first PDU (response on the tap at 55.005 s), and STREAM_STOP 0 to 1 at the first read after the last PDU (769.005 s). There was **no other change in 871 reads** (870 responses are on the tap; the last read came after the tap stopped). MEDIA_RESET and TIMESTAMP_UNCERTAIN stayed 0. These are the first start and stop since the cold boot. Console `CRFT_CTRL` went `0x3` to `0x300223` (bound, DA held, no Ready; 48.36 s) to `0x3002e3` (54.86 s) to `0x3` (768.36 s). `LWSRP_STATUS` went `0x0` to `0x210` to `0x250` to `0x0`. Each had exactly those three edges in 1790 samples |
| 3a | Across the switch's repeated LeaveAll cycles: count and spacing | **56 cycles, 10.0 to 15.0 s** | Switch LeaveAll MRPDUs in the bound window: **56**, all 56 inside the stream (the first 4.52 s after the first PDU, the last 12.52 s before the last). Spacing: min 10.000, median 12.611, mean 12.665, max 15.000 s (55 intervals). The whole capture holds 69, spaced 10.000 to 15.000 s. Every one flags Domain, Listener, TalkerAdvertise and TalkerFailed. While bound they carry TalkerAdvertise and TalkerFailed as NumberOfValues-0 vectors. The DUT re-declared its TalkerAdvertise 4 to 199 ms after each (median 8 ms), **none missing**. The DUT's own LeaveAlls while bound numbered 57, spaced 10.000 to 15.000 s. Each flags all four types, with NumberOfValues-0 vectors for Listener and TalkerFailed. The first (48.899 s) came before any Listener existed. After each of the other 56, the switch re-declared the Listener 0 to 93 ms later, **none missing** (`bench/run/supplement.txt`) |
| 3b | First CRF PDU only after the first Listener Ready, on one timebase | **PASS** | Tap clock: first probe answered **TALKER_DEST_MAC_FAIL** (status 3) at 48.007733 s, 8.8 ms after the bind. The DUT declared TalkerAdvertise `New` at 48.099434 after its MAAP grant, and the reference peer's second probe got SUCCESS at 54.364282. First Listener Ready for `0200000000010001` (switch to DUT, `New/Ready`): **54.375814 s**. First CRF PDU (DUT to switch): **54.376308 s**, **+0.494 ms**. UTC: 14:28:15.625708 and 14:28:15.626202. There was **no CRF PDU anywhere in the capture before that Ready**, so none in the 6.368 s between the status-3 answer and the Ready (at #117 the DUT began 0.18 ms after that answer). Before the first PDU the switch sent exactly one Listener message for the stream, that `New/Ready`. Across the gap the DUT sent 10 TalkerAdvertise declarations and no PDU. Console `CRFT_CTRL` read `0x300223` in the gap and `0x3002e3` after it |
| 3c | FRAMES_TX against the documented 1 s-interval semantics | **consistent** | This is Milan v1.2 5.3.7.7 Table 5.4 as documented in `docs/reference/REGISTER_MAP.md` `0x764`, `tb/verilator/milan_dp/README.md` ("FRAMES_TX is an interval count") and the `KL_talker_diag_ctx.sv` banner: +1 at the end of each 1 s interval that carried at least one PDU, reset at STREAM_START (`DIAG_TICK_CYC_P = MILAN_CLK_FREQ_HZ`). It read 0 before the stream, and 0 at the first response after STREAM_START, 0.629 s into the stream, before the first interval closed. It then rose by exactly +1 per 1 s read (714 steps), final **714**, held for the 108 s after the stop. A 713.639 s stream touches 714 or 715 one-second intervals, depending on where the tick falls. **All 823 in-stream responses on the tap match the semantics exactly** for tick phases 0.016 to 0.376 s (tap s mod 1), and at every such phase the stream touches **714** intervals (`a258_supplement.py`, section 4). `CRFT_COUNT` (`0x764`, the PDU total) went 0 to **356,816, equal to the wire count**. SO0 (AAF) stayed all 0, and no AAF PDU was on the wire |
| 4 | Restore the bench: unbind, census equal to the start | **PASS** | Final census (14:42:36Z) against the start census (14:25:26Z): **ACMP 18/18 identical** (peer SI 0 to 9, peer SO 0 to 3, DUT SI 0 and 1, DUT SO 0 and 1, all unbound, count 0). **AEM settings reads 15/15 identical** (`bench/final/census-compare.txt`). One ACMP field the compare does not grade moved, as it did at #117: the DUT SO1 GET_TX_STATE `stream_dest_mac` read `00:00:00:00:00:00` at the start and `91:e0:f0:00:43:10` at the end, the MAAP address the DUT acquired during the run. The 40 s final tap capture holds no AVTP from the DUT (`bench/final/wire-summary-final.txt`). Console: `CRFT_CTRL=0x3`, `LWSRP_STATUS=0`, `LWSRP_SLOPE=0`. No process is left running on the controller host or the capture server (`bench/final/procs-after.txt`) |

## Observations outside the acceptance (not graded)

These are the same two A237 recorded on `c593cbef`, which A10 routed to #495.

1. **Mt in the DUT's LeaveAll MRPDU when the two LeaveAll timers nearly coincide.** This happened once in
   the 56 bound cycles, at 625.300810 s. The DUT's own LeaveAll MRPDU went out 6.7 ms after the switch's
   (625.294097 s) and carried the CRF TalkerAdvertise as `Mt`, not `JoinMt`. `JoinMt` followed 200 ms
   later, at 625.500816 (`bench/run/msrp-around-625.txt`). The switch kept the Listener (JoinMt/Ready at
   625.394), sent no Listener Lv, and emission did not gap: the stream's maximum interval is 2.005 ms. The
   same effect showed on `c593cbef` at 7.5 ms and 1.5 ms offsets.
2. **Repeated Domain vectors.** 26 of the DUT's 855 bound MRPDUs carry the same Domain value in two or three
   vectors (`bench/run/la-detail.txt`). A237 counted 27 of 850. The switch never does this.
3. **Stop at unbind.** The DUT's last PDU preceded the switch's Listener Lv on the DUT link by 1.86 ms, and
   the next 2 ms slot was not used (A237: 1.19 ms). The TalkerAdvertise Lv followed 83.7 ms after the Listener
   Lv (A237: 140 ms). Afterwards the DUT sent TalkerAdvertise `Mt` as many times as there were LeaveAll
   MRPDUs on the link after the unbind: 18 (9 + 9), as A237 saw.
4. **Timebases.** The capture-server fit has slope 3.85 ppm and residuals of -3.2 to +5.8 ms, the same kind
   of NTP slew A237 saw on its attempt 2. Everything graded above is on the tap clock and unaffected. The
   UTC strings and the counter/console alignment carry that error. The FRAMES_TX check reads the GET_COUNTERS
   responses on the tap, so it is on the tap clock too.

## Differences from A237's method

- The scripts are A237's. The run scripts change only the packet path, the remote directory (`/tmp/a258`)
  and the file names that carried host names: the controller-port capture is `controller-host-run.pcap`,
  and the gPTP watch is `controller-host-watch.jsonl`. `diff` against A237's `run_bind.sh` after
  normalising those names shows only comment and label lines. `a258_census.sh` is `a237_census.sh` with
  the remote path changed. `run_start_census.sh` is A237's `run_resume.sh` shape: a process list, the
  census and a console readback.
- `a258_supplement.py` is new and offline. It splits A237's bound-window LeaveAll statistics at the first
  PDU, since this run's stream starts 6.4 s into the window. It counts PDUs before the first Listener
  Ready over the whole capture. It checks FRAMES_TX response by response on the tap clock, over a 1 ms
  grid of tick phases.
- There was a single attempt, from the cold boot. That is why STREAM_START/STOP went 0 to 1 here, where
  A237's attempt 2 went 1 to 2.

## Timebases

The tap stamps each frame in hardware. `wire_summary.records` gives the tap time and the port. Port 3
carries frames the DUT sent, and port 2 frames the switch sent toward the DUT. Host-generated records are
excluded (135). `a237_analyze.py` maps tap time to the capture server's clock with a least-squares line
through the per-5 s minima of (pcap host time minus tap time). Controller-host times (GET_COUNTERS, bind
log) are NTP and go on the same axis by subtraction. Console times are build-box times plus the measured
capture-server offset, +1.31335 s: the mean of 1.312166 at the start and 1.314534 at the end
(`bench/clock-*.jsonl`). The controller host read +1.316694 and +1.319594 against the build box. The
build box is not NTP-synchronised, so the build-box times in `timeline.txt`, `lock.txt` and this file's
wall-clock times sit about 1.3 s behind UTC.

## Exact commands (packet root `$MANAGEMENT/2026-09-23/530-a258`)

```sh
# expected CRCs (offline)
W=$WORKSPACE_HOME/litex-milan/work
python3 tools/expected_crc.py $W/build_ax7101_{asl,eppo,eto}_tdm8dev59b81670 $W/build_ax7101_asl_tdm8devc593cbef > identity/expected-crc.txt
python3 tools/expected_crc.py $W/build_ax7101_{asl,eppo,eto}_tdm8dev3d2f3e31 >> identity/expected-crc.txt
# deploy the controller-host tools (hashes in bench/deploy-controller-host-verify.txt)
ssh <bench-host-prefix>pw1 'mkdir -p /tmp/a258'; scp tools/{avdecc_ro.py,crf_bind_window.py,a231_counters_poll.py,a258_census.sh} <bench-host-prefix>pw1:/tmp/a258/
ssh <bench-host-prefix>ubuntu-server 'mkdir -p /tmp/a258'
# 1. start census, identity, gPTP
timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_start_census.sh > bench/start/lock.txt 2>&1
timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_identity_gptp.sh > identity/lock-window.txt 2>&1
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do timeout 60 python3 tools/clock_offset.py $h 25; done > bench/clock-start.jsonl
# 2. the bind run (~15 min, longer than one tool call, so it was detached and waited on in the foreground;
#    crf_bind_window.py runs on the controller host and unbinds by itself even if the build box goes away)
setsid nohup bash -c "timeout 1300 flock -w 60 /tmp/milan-bench.lock bash $PWD/tools/run_bind.sh > $PWD/bench/run/lock.txt 2>&1; echo flock_rc=\$? >> $PWD/bench/run/launch.txt" &
scp <bench-host-prefix>pw1:/tmp/a258/{bind.jsonl,counters.jsonl,controller-host-run.pcap} bench/run/; scp <bench-host-prefix>ubuntu-server:/tmp/a258/tap-run.pcap bench/run/
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do timeout 60 python3 tools/clock_offset.py $h 25; done > bench/clock-end.jsonl
# 4. final state
timeout 500 flock -w 60 /tmp/milan-bench.lock bash tools/run_final.sh > bench/final-lock.txt 2>&1
scp <bench-host-prefix>ubuntu-server:/tmp/a258/tap-final.pcap bench/final/
python3 tools/census_compare.py bench/census-start.jsonl bench/final/census-final.jsonl > bench/final/census-compare.txt
python3 tools/wire_summary.py bench/final/tap-final.pcap > bench/final/wire-summary-final.txt
# analysis (offline), in bench/run
python3 ../../tools/a237_analyze.py tap-run.pcap --counters counters.jsonl --bind bind.jsonl \
  --console console.txt --console-offset-s 1.31335 --json analysis.json > analysis.txt
python3 ../../tools/a237_crosscheck.py tap-run.pcap analysis.json > crosscheck.txt
python3 ../../tools/a237_la_detail.py  tap-run.pcap analysis.json > la-detail.txt
python3 ../../tools/a258_supplement.py tap-run.pcap analysis.json > supplement.txt
python3 ../../tools/a237_msrp_around.py tap-run.pcap 625.30081 1.5 > msrp-around-625.txt
python3 ../../tools/a237_msrp_around.py tap-run.pcap 768.01 0.3 > msrp-around-768.txt
```

What `run_bind.sh` does, in order (unchanged from A237):

1. Starts the recorders, all bounded by `timeout`:
   - tap capture (`tcpdump -i <tap if>` on the capture server);
   - controller-port capture (`ether proto 0x22f0`);
   - console poll every 0.5 s: `milan_status`, `CRFT_CTRL`, `CRFT_COUNT`, `LWSRP_STATUS`, `ACMP_TALKER`,
     `CLKV_TUCNT`, `GPTP_DROPW`, `GPTP_DROPE`.
2. Refuses to bind unless both captures are listening and the console transcript is growing
   (`preflight_ok console=22104->29472`).
3. Starts GET_COUNTERS every 1 s on DUT SO1, DUT SO0 and peer SI8.
4. Runs `crf_bind_window.py ens10 30 720 90` on the controller host. The tool refuses unless the input
   reads unbound, and it unbinds at the window end, on a signal and on any exception.
5. Stops the recorders.

Run timeline (build-box clock): lock 14:27:19.746Z; pre-flight OK 14:27:27.762Z; bind window start
14:27:37.765Z; bind window end `BIND_RC=0` 14:41:37.966Z; recorders stopped 14:41:58Z; unlock 14:42:14.773Z;
`flock_rc=0`. `counters-poll.rc` reads `CTR_RC=143`. That is the script's own SIGTERM, which ends the poll
after the post window by design (`ctr_stop_rc=0`). The final capture's `capture_rc=124` is its `timeout 40`,
also by design.

## Tool hashes (sha256)

| Tool | sha256 | Origin |
|---|---|---|
| crf_bind_window.py | `29b4ac468f5fb58f53053db353be675c0d8aad84e6a296fc02722140aa8ee152` | #117 A200 packet, unchanged (= A237) |
| avdecc_ro.py | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` | #117 A200/A202, unchanged (= A237) |
| a231_counters_poll.py | `c32a20bc33c64ce96fc95212df13f1fc92e7808c67570792e8b2fafbd46920f7` | #529 A231, unchanged (= A237) |
| wire_summary.py | `c5039d950eaf42e274cfaddfc38f3845bd66dd8cba011899fbd3172ef66a3d5e` | #117 A200/A202, unchanged (= A237) |
| console_read.py | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` | #117 A200/A202, unchanged (= A237) |
| console_poll.py | `3a0de7d8e1f9f4e0f87d03364c3cf35e9965210dd7095b21ef9d1b7bdb1bd326` | #117 A200/A202, unchanged (= A237) |
| census_compare.py | `40424c61b958a42e2f4da4415fe0c1f7c37b75aec9085c516d1874f1e0e9b4f2` | #117 A202, unchanged (= A237) |
| clock_offset.py | `950533caa8d3a2bb1c42ae4d2a60f56769cb8877a9b82149bd74e52fe6e6590d` | #117 A202, unchanged (= A237) |
| expected_crc.py | `04d128bb0a9ffe8ad5898f4ece380899a096a1595aadda3ece1048c313bf19d7` | #117 A200/A202, unchanged (= A237) |
| baremetal_uart_smoke.py | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` | `scripts/baremetal_uart_smoke.py` at `59b81670` (identical to A237's copy) |
| a237_analyze.py | `7ea34430f95c94c5e71b36228e9b7787864ed020a0c72ff03a988b086a2563c9` | A237, unchanged |
| a237_crosscheck.py | `fe725f823c9f8bdfc28805551fee9d863aeada2b801cbacb77761c6c766389a2` | A237, unchanged |
| a237_la_detail.py | `bac70bb20813903f81730be59aa45a576c4323d46f89af9aec0ee1dbc105050b` | A237, unchanged |
| a237_msrp_around.py | `14226aa75d3147140a521ea5fe1467ea7e9aecb2eeabbea6ad502fbcaeea0d96` | A237, unchanged |
| a258_census.sh | `6f73c48e22e9a8ea5e0d94b75143553f869d4d76e7c056e6a6b2918736a55c1c` | `a237_census.sh` with the remote path `/tmp/a237` changed to `/tmp/a258` |
| run_start_census.sh | `02a482b4bdd78dd2f05b98f70fc3377a73e638bb000f6a121288dba1465fd792` | new (A258), A237 `run_resume.sh` shape |
| run_identity_gptp.sh | `6010737705a53ee8a1a5ad0b17de9e81a3afd30ea807728d141d3fc7b83f95a3` | A237's, path and file name changes |
| run_bind.sh | `670c161d2a5bf1c2718fc667df8fd080b373733f1e4b7acb67fab2fc6328b1b1` | A237's, path and file name changes |
| run_final.sh | `2f741639233cec2d365721060f466e9f9ec36a134b9929e1122c3b8a3d20fbcd` | A237's, path changes |
| a258_supplement.py | `790be4eeb60c998011bde7fd2831b8d5b6560fd7eed616e715ccc08651957096` | new (A258) |

Host tools: Python 3.14.6 on the controller host, tcpdump 4.99.6 / libpcap 1.10.6 on both remote hosts
(`bench/deploy-controller-host-verify.txt`). The deployed copies on the controller host hash equal to the
packet's.

## Raw data (hashes in `MANIFEST.sha256`)

| Artifact | File (`bench/run/` unless noted) |
|---|---|
| tap capture of the DUT link | `tap-run.pcap` `7b8032c7e97fe74dc45b968914c165e0d5d60cef86bf7aa121c77d4c26a184bb` (42.2 MB) |
| controller-port capture (AVDECC) | `controller-host-run.pcap` `cb400e16ec754fa9c0dd1b47d712bbb78322dc0bc7b1cb214320ef8c09d5c56e` |
| bind-window log | `bind.jsonl` `0294b13ad15bb993d5d7df08ccaea98f49323e5894435c4a825592a7715e8aee` |
| GET_COUNTERS log | `counters.jsonl` `760a643498ef95ef489f9155ae6d494aba11f8f60a01167c43ff0dd21811a3f1` |
| console transcript | `console.txt` |
| analysis | `analysis.txt`, `analysis.json`, `crosscheck.txt`, `la-detail.txt`, `supplement.txt`, `msrp-around-625.txt`, `msrp-around-768.txt` |
| run receipts | `timeline.txt`, `launch.txt`, `lock.txt`, `bind.rc`, `counters-poll.rc`, `console-poll.stdout`, `tcpdump-*.log` |
| identity | `identity/` (console readback, grader log, expected CRCs, lock window) |
| gPTP window | `bench/gptp/` |
| censuses | `bench/census-start.jsonl`, `bench/final/census-final.jsonl`, `bench/final/census-compare.txt`; start-state receipts in `bench/start/` |
| final state | `bench/final/` (40 s tap capture, its summary, console, grader, processes after) |
| clock offsets | `bench/clock-start.jsonl`, `bench/clock-end.jsonl` |

The remote copies stay in `/tmp/a258` on the controller host (logs, tools, controller-port capture) and
on the capture server (both tap captures). No process was left running.

## Public comment

https://github.com/kebag-logic/milan-fpga/issues/530#issuecomment-5816442814, posted
2026-09-24T14:49:36Z. `public-comment-530.md` is the posted text, and `posted-comment-530.readback.md` is
the API readback, identical except for one trailing newline. It names equipment by role only.
