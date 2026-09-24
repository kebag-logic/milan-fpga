# HANDOFF: issue 387 dev silicon check of the #540 gPTP pin, A249 bench author, 2026-09-24

Assignment: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5811705085
Reference checkout: $VALIDATION_STORAGE/worktrees/build-dev-3d2f3e3131c9 (dev `3d2f3e31`, detached HEAD,
read-only, clean, untouched). `origin/dev` has since moved to `9d328810` (#543, offline AECP
model and tests); the board runs `3d2f3e31`. Nothing was flashed, power-cycled, rewired or
reconfigured. Nothing was bound. No repository was edited or pushed. No sub-agent was used. Every
bench step ran under `flock /tmp/milan-bench.lock`.

## Outcome

**PASS on all five items.** The dev `3d2f3e31` image (gPTP processor pin `e5dcea6e`) holds lock to
the grandmaster (the bench AVB switch) with asCapable in every sample. Over a 900 s soak with the
grandmaster stable there was no step and no `tu`. The wire offset matches the previous pin's.
la_avdecc classifies the DUT Milan in 3 of 3 enumerations. The end census equals the start.

## Per-item table

Build-box times are UTC but not NTP-disciplined. The build box ran 1.2695 s (start) to 1.2731 s
(end) behind the controller host and the capture server, which are NTP-synchronized
(`bench/clock-start.jsonl`, `bench/clock-end.jsonl`). Controller-host and tap times are NTP UTC.

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Start state: binding census | recorded | `bench/census-start.jsonl` (09:48:36 build box): ACMP 18 states, all unbound, count 0 (peer SI 0 to 9, peer SO 0 to 3, DUT SI 0/1, DUT SO 0/1). AEM 15 settings reads. It equals A237's end census of 06:06 UTC this morning: **ACMP 18/18, AEM 15/15** (`bench/census-start-vs-a237-final.txt`) |
| 1 | DUT identity | **PASS** | `identity/console-identity.txt` (09:48:12 build box): `ID=4d494c4e`, `VERSION=00020060`, also by `mem_read 0x90000000/4`. The QSPI CRC readback reads ROM `f6afa4ec`, bitstream payload **`b07f8550`**, AEM `93742dd2`. `b07f8550` is the **eppo seed of `3d2f3e31`**, the build `build_ax7101_eppo_tdm8dev3d2f3e31` named by the assignment. The asl seed is `ad9185ae` and the eto seed `b8452657`. The previous image's seeds (`c593cbef`) are `11a89d32`, `e5ff3498` and `1963bdfc` (`identity/expected-crc.txt`). The eppo build's `flashboot_layout.json` records the same payload sha256 `3756dc0d…` that `expected_crc.py` computes. `RST_EPOCH=1`, `CRFT_COUNT=0` |
| 2 | gPTP lock, grader, asCapable | **PASS** | Grader `scripts/baremetal_uart_smoke.py` **10/10** four times: 09:48:36, 09:51:57, 10:06:58, 10:11:05 build box. Console `GPTP_GM=GPTP_PARENT=3cc0c6fffefe0210` (the bench AVB switch), `AS_PATH_COUNT=1`, `SYNC=1 ASCAPABLE=1 TU=0`, `CLKV_STAT=00010002` in **900/900** soak samples. Controller GET_AVB_INFO: as_capable 1, gptp_enabled 1, GM the switch, **900/900 SUCCESS on the DUT and 900/900 on the reference peer**. GET_AS_PATH: [GM] for the DUT, [GM, peer] for the reference peer, 900/900 each. Peer delay (console) median 385, 375 to 391 ns, stdev 3.2 ns |
| 2 | Offset and rate statistics (wire) | recorded | `bench/soak/wire-analysis.txt`. Tap capture of the DUT link, 907.9 s, 0 drops. 904 samples at 1 s. DUT PHC minus grandmaster time, `o2 - d`: **median +1.7 ns, stdev 10.0 ns**, p1 -22.8, p99 +22.7, min -24.2, max +32.0 ns. The independent `o3` series: median +0.3, stdev 7.7, range -24.7 to +24.8 ns. **Frequency: DUT minus GM -0.006 ppb** (slope of the offset over 907 s: -0.001 ppb). Per-60 s window medians range 380.8 to 390.9 ns (`o2`). Baseline on the previous pin `c1b61743`, from A237's 877 s capture this morning (`c593cbef`): median -1.4, stdev 10.1 ns, range -33.4 to +38.2 ns, -0.005 ppb (`bench/baseline-a237/wire-a237-run.txt`). #117 Run A (`ede8d48e`, same pin): median +1.1, stdev 9.6 ns. Method under "Wire offset method" |
| 3 | Soak >= 10 min, grandmaster stable | **900 s** | Console poll every 1.000 s: 900 rounds, 09:51:58.008 to 10:06:57.008 build box (09:51:59.28 to 10:06:58.28 UTC), spacing 1.000 s, no gap. Tap span 09:51:56.4 to 10:07:04.3 UTC. **The grandmaster was stable**: 907 Announces on the DUT link, all GM `3cc0c6fffefe0210`, priority1 246, stepsRemoved 0. 7264 Syncs, every one with its Follow_Up, 0 sequence gaps, intervals 100.7 to 149.3 ms (mean 125.000). Follow_Up correctionField 0, cumulativeScaledRateOffset 0 and gmTimeBaseIndicator 0 on all. `ASP_CMD` (path generation and count) `0x11` throughout. `GPTP_GM_CHANGED` 0 in 900/900 reads. The DUT sent only Pdelay messages (no Sync, no Announce). It answered 905/905 of the switch's Pdelay_Req, and the switch answered 908/908 of the DUT's |
| 3 | No spurious step, no `tu` | **PASS: 0 events** | **`CLKV_TUCNT` (0x780) read 10 in every one of 900 samples**, and read 10 at identity (09:48:12) and at the final read (10:11:04 build box). It counts every 1 s interval in which `tu` was set, and a step always sets `tu` for its 0.25 to 0.5 s holdover. So no step happened in those **22.9 min**, including between samples. `CLKV_STAT` bit 0 (`tu`) 0/900, bit 3 (holdover) 0/900. Stream Output 0 and 1 `TIMESTAMP_UNCERTAIN` (GET_COUNTERS) 0 in 900/900 each. CLOCK_DOMAIN 0 LOCKED 1, UNLOCKED 0, unchanged. `GPTP_DROPW`/`GPTP_DROPE` 0, `RST_EPOCH` 1, `LINKG_STAT` `0x83`, unchanged. On the wire: the largest 1 s change of the offset was 46.8 ns (`o2`) and 34.3 ns (`o3`). **No change above 1 us**. The step policy steps at 20 us or more (link-up) and above 100 us (locked), and a 100 us slew would show as an excursion of the same size |
| 4 | la_avdecc enumeration x3: DUT classified Milan | **PASS 3/3** | Runs at 09:48:57 (before the soak), 10:07:31 (after it) and 10:10:24 (final), build box. Each: DUT `flags=IEEE17221\|Milan`, milanInfo protocol 1, certification 0.0.0.0, specification 1.2.0.0, `query-errors 0`, `SUMMARY online=2 complaints=0`, `ENUM_RC=0`. Entity dumps: `compatibility_events` empty, `compatibility_flags` IEEE17221 and MILAN, AECP retries/timeouts/unexpected 0, unsolicited loss 0, enumeration 224, 224 and 199 ms. Each log is **identical to the #529 step-2 log** apart from the order of the online/offline events and the output path. Runs 1 and 2 ran the counters probe first: DUT and reference peer CLEAN rc 0, transcripts **identical to #529's**. The reference peer was `IEEE17221\|Milan` in all three |
| 5 | Restore: census equal to start | **PASS** | `bench/final/census-final.jsonl` (10:10:23 build box) against the start: **ACMP 18/18 identical, AEM settings 15/15 identical** (`bench/final/census-compare.txt`). Nothing was bound at any point. Final console: `CLKV_STAT=00010002`, `CLKV_TUCNT=10`, `CRFT_CTRL=0x3`, `RST_EPOCH=1`. Remote temporary files were hashed, copied, verified and removed (`bench/pw1-tmp-before-cleanup.txt`, `bench/capture-server-tmp-before-cleanup.txt`, `bench/cleanup.txt`). No leftover process. The lock is free. A237's `/tmp/a237` on both hosts was left as found |

## What "step counters" can mean on this image

The dev `3d2f3e31` register map has no CSR that counts the plane's steps. One step is one
`phc_step_we_o` pulse (docs/design/TIME_SYNC.md "Step policy"). In `hdl/milan/milan_datapath.sv`
that pulse (`gptp_step_we_w`) drives three things:

- the PHC adjtime (`eff_ptp_adjust_w`, line 2747);
- `KL_ptp_clock_validity`'s `phc_adj_p_i` (line 1941), which arms the 0.25 to 0.5 s holdover
  (`CLKV_STAT[3]`) that raises `tu` (`CLKV_STAT[0]`) and so moves `CLKV_TUCNT`;
- the render re-centre (`render_recentre_p_w`, line 6004), whose tally `rsp_recentres_w`
  (line 6133) is `verilator public_flat_rd` and has no CSR.

So on silicon, a step was looked for in three places, from strongest to weakest:

1. `CLKV_TUCNT`, which latches;
2. `CLKV_STAT` bits 0 and 3 at 1 s, which can miss a 0.25 s holdover between samples;
3. the wire offset, which is independent of the DUT's own publication.

All three are quiet. `PTP_ADJ` (0x508) is the software CSR face, not the plane's trim, so the
servo's rate is not readable either. The rate figures above come from the wire.

## Wire offset method (`tools/a249_gptp_wire.py`)

The tap stamps every frame in hardware. It is decoded by `wire_summary.py`, unchanged from #117.
Port 2 carries the switch's frames to the DUT and port 3 the DUT's frames.

- **Grandmaster time.** `G(T)` is the grandmaster time at tap time `T`, linearly interpolated
  between the switch's Syncs. Each Sync's value is preciseOriginTimestamp plus both
  correctionFields, from its Follow_Up. The switch is the grandmaster.
- **`o2`** = the DUT's `t2` (requestReceiptTimestamp in its Pdelay_Resp) minus `G` at the moment
  the switch's matching Pdelay_Req passed the tap.
- **`o3`** = the DUT's `t3` (responseOriginTimestamp plus correctionField in its
  Pdelay_Resp_Follow_Up) minus `G` at the moment its Pdelay_Resp passed the tap.

Let `a` be the switch-to-tap delay and `b` the tap-to-DUT delay, taken as the same both ways. Then:

- the DUT-minus-GM offset is `o2 - (a + b)`, which also equals `o3 - a + b`;
- so `o2 - o3 = 2b`;
- with `a + b` = the published mean link delay `d` (385 ns), the offset is `o2 - d`.

The measured `o2 - o3` median is 382.9 ns, consistent with `2b`.

Only the variation of `o2` and `o3` is free of path assumptions. The absolute value assumes a
symmetric link and equal tap port latencies, as gPTP itself does. Frequency is the least-squares
slope of the offset over the span, and separately `t3` against tap time minus `G` against tap time.
Both use the tap oscillator as the common reference. `--jump-ns 1000` lists any 1 s change of
`o2` or `o3` above 1 us. There were none.

## Observations outside the items (not graded)

1. **Two TIMESTAMP_UNCERTAIN readings.** `CLKV_TUCNT` read 10: the 1 s intervals with `tu` since
   the cold boot, before lock. The Stream Output GET_COUNTERS `TIMESTAMP_UNCERTAIN` read 0 on both
   outputs. REGISTER_MAP describes `CLKV_TUCNT` as engine-wide and serving every STREAM_OUTPUT. The
   AEM counter restarts at STREAM_START and neither output has started since the boot. That
   restart is #117 A202 follow-up 2 and was already reported, so it is not new here. Both readings
   were flat for the whole run.
2. **The DUT's `GPTP_GM_CHANGED` reads 0** although it adopted the switch as GM after the cold
   boot. #529 read the same. The reference peer's reads 15, also flat.
3. **The step branch of the policy was not exercised.** No GM change, link-up or other
   disturbance was provoked, as the assignment required. Any link-up step belongs to the cold
   boot, before this session. This run shows the steady state: no spurious step and slew-only
   tracking at the old pin's quality. It does not measure a step's physical re-base. That remains
   GM_LOSS_RECOVERY.md's "#117 bench measures it".

## Exact commands (packet root `$MANAGEMENT/2026-09-23/387-a249`)

```sh
PK=$MANAGEMENT/2026-09-23/387-a249
W=$WORKSPACE_HOME/litex-milan/work
# expected CRCs and origin
python3 $PK/tools/expected_crc.py $W/build_ax7101_{asl,eppo,eto}_tdm8dev3d2f3e31 $W/build_ax7101_{asl,eppo,eto}_tdm8devc593cbef > $PK/identity/expected-crc.txt
git ls-remote origin refs/heads/dev > $PK/identity/origin-dev.txt
# deploy (controller host), verified in bench/deploy-pw1-verify.txt
scp avdecc_ro.py a231_counters_poll.py a249_census.sh <bench-host-prefix>pw1:/tmp/a249/; scp a200_enum.bin <bench-host-prefix>pw1:/tmp/a249/a200_enum
# clock offsets
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do python3 tools/clock_offset.py $h 25; done > bench/clock-start.jsonl
# identity, grader, start census (lock 09:48:12.286 to 09:48:37.935 build box)
timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_identity.sh > identity/lock-window.txt 2>&1
python3 tools/census_compare.py $REVIEWS/530-a237-packet/bench/final/census-final.jsonl bench/census-start.jsonl > bench/census-start-vs-a237-final.txt
# enumeration 1 (lock 09:48:53.212 to 09:51:43.532)
timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_enum.sh enum1
# soak (lock 09:51:54.679 to 10:07:04.099); longer than one tool call, so detached and waited on in the foreground
setsid nohup bash -c "timeout 1400 flock -w 60 /tmp/milan-bench.lock bash $PK/tools/run_soak.sh > $PK/bench/soak/lock.txt 2>&1; echo flock_rc=\$? >> $PK/bench/soak/launch.txt; ..." &
scp <bench-host-prefix>ubuntu-server:/tmp/a249/tap-soak.pcap <bench-host-prefix>pw1:/tmp/a249/{pw1-soak.pcap,watch.jsonl,counters.jsonl} bench/soak/
# enumeration 2 (lock 10:07:25.083 to 10:10:15.245)
timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_enum.sh enum2
# final: census, enumeration 3, console, grader (lock 10:10:20.316 to 10:12:30.485)
timeout 480 flock -w 60 /tmp/milan-bench.lock bash tools/run_final.sh
python3 tools/census_compare.py bench/census-start.jsonl bench/final/census-final.jsonl > bench/final/census-compare.txt
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do python3 tools/clock_offset.py $h 25; done > bench/clock-end.jsonl
# analysis (offline)
cd bench/soak
python3 ../../tools/a249_console_summary.py console.txt --json console-summary.json > console-summary.txt
python3 ../../tools/a249_ctrl_summary.py --watch watch.jsonl --counters counters.jsonl > ctrl-summary.txt
python3 ../../tools/a249_gptp_wire.py tap-soak.pcap --pdelay-ns 385 --json wire-analysis.json > wire-analysis.txt
python3 ../../tools/wire_summary.py tap-soak.pcap > wire-summary.txt
python3 tools/a249_gptp_wire.py $REVIEWS/530-a237-packet/bench/run/tap-run.pcap > bench/baseline-a237/wire-a237-run.txt
```

What `run_soak.sh` does, in order (all recorders bounded by `timeout`, nothing bound or written):

1. It starts the tap capture of the DUT link on the capture server, and a capture of the
   controller host's own port (`ether proto 0x22f0`).
2. Grader.
3. It starts the pollers:
   - console poll every 1 s for 900 s: `milan_status`, `CLKV_TUCNT` 0x780, `ASP_CMD` 0x7E4,
     `GPTP_DROPW` 0x7E8, `GPTP_DROPE` 0x7EC, `RST_EPOCH` 0x720, `LINKG_STAT` 0x774;
   - controller `avdecc_ro.py watch` (GET_AVB_INFO and GET_AS_PATH) every 1 s on the DUT and the
     reference peer;
   - `a231_counters_poll.py` every 1 s on DUT SO 0 and 1, DUT AVB_INTERFACE 0, DUT CLOCK_DOMAIN 0
     and peer AVB_INTERFACE 0.
4. Preflight check: both captures listening and the console transcript growing.
5. It waits for the pollers. Then it runs the grader and a final console read, and stops the
   captures.

`run_enum.sh` is #529's `run_step2.sh` with the path `/tmp/a231` changed to `/tmp/a249` and the
output directory parametrized. `run_final.sh` is #529's `run_final.sh` with the same path change
and a different set of console `mem_read`s. `a249_census.sh` is A237's `a237_census.sh` with
`/tmp/a237` changed to `/tmp/a249`, line 2 only.

## Tool hashes (sha256)

| Tool | sha256 | Origin |
|---|---|---|
| a200_enum.bin (run as `/tmp/a249/a200_enum`) | `8c9f288573e5846d10779b8f96e09fbbcd4d2d7dc3d5ed8fbe398fc28a8b6b35` | #117 binary, as #529, unchanged |
| a200_enum.cpp | `2d8950f5cdc37617a211a1bb3f2198c005db795f3114bfd86b8db3a94267bd22` | #117 source |
| libla_avdecc_cxx.so.4.3.1.1 | `95d64fd50715a5170b5a71d8018510d580d12cfce3c0a7b1b389b87a1ce55982` | controller host, unchanged since #117 |
| libla_avdecc_controller_cxx.so.4.3.1.1 | `8ef4b00829b9f1baf602e67fdd750302b0bf452db569e660dfde4f72041bbc32` | same |
| target-counters-probe | `ad579e18e46b566cbeea34c188e4b324228bb3daac6296742f689fecff159dc7` | controller host, unchanged since 2026-09-08 |
| avdecc_ro.py | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` | #117, unchanged |
| a231_counters_poll.py | `c32a20bc33c64ce96fc95212df13f1fc92e7808c67570792e8b2fafbd46920f7` | #529, unchanged |
| a249_census.sh | `11c66313a2865f6b0f77ac782b917532dee91c89518360145b727e09400ddce1` | A237 `a237_census.sh` (`d29f1176…`), path only |
| console_read.py | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` | #117, unchanged |
| console_poll.py | `3a0de7d8e1f9f4e0f87d03364c3cf35e9965210dd7095b21ef9d1b7bdb1bd326` | #117, unchanged |
| census_compare.py | `40424c61b958a42e2f4da4415fe0c1f7c37b75aec9085c516d1874f1e0e9b4f2` | #117 A202, unchanged |
| clock_offset.py | `950533caa8d3a2bb1c42ae4d2a60f56769cb8877a9b82149bd74e52fe6e6590d` | #117 A202, unchanged |
| expected_crc.py | `04d128bb0a9ffe8ad5898f4ece380899a096a1595aadda3ece1048c313bf19d7` | #117, unchanged |
| wire_summary.py | `c5039d950eaf42e274cfaddfc38f3845bd66dd8cba011899fbd3172ef66a3d5e` | #117, unchanged |
| baremetal_uart_smoke.py | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` | `scripts/baremetal_uart_smoke.py` at `3d2f3e31`, unchanged since `ede8d48e` |
| run_identity.sh | `d636643dff1fd900fc3bf3c6544ee418fcec5664e9c3f56cd32fe087944e476b` | new (A249) |
| run_enum.sh | `f058f1c2fb5e6a78940230a46670da442658e4105e871dc61ee3ad0db92b3223` | new (A249), #529 `run_step2.sh` shape |
| run_soak.sh | `5ab4d6d96155b9ea343fb31eaad4420ef75bc8a2ed5b4446d28b1a61e682e300` | new (A249) |
| run_final.sh | `5a74566b2da78a79c4aa9ece5b9b9e9e8d5cdbb056d5ba87346de5d88a30dac4` | new (A249), #529 `run_final.sh` shape |
| a249_console_summary.py | `d6d52a8538adf6f8d62840bcf0f36bcd3890c49f5237d590e3ca8e10a9cf8d9f` | new (A249), offline |
| a249_ctrl_summary.py | `5f9618dc544799a471ee491ea701c0cadcab2d0a9ffaff11294f54ded58446cf` | new (A249), offline |
| a249_gptp_wire.py | `e374175ba419bc54dade80c35bf0ffb1ec6b607c8311b9742a89a98c35ecfcea` | new (A249), offline |

Host tools: Python 3.14.6, tcpdump 4.99.6 and libpcap 1.10.6 on the controller host. The
controller host and the capture server are both `NTPSynchronized=yes`.

## Raw data (hashes in `MANIFEST.sha256`)

| Artifact | Path |
|---|---|
| identity transcript, grader, expected CRCs, origin | `identity/` |
| start census, cross-check with A237's end | `bench/census-start.jsonl`, `bench/census-start-vs-a237-final.txt` |
| soak: tap capture (0 drops) | `bench/soak/tap-soak.pcap` `27bcce60…` |
| soak: controller-port capture (0 drops) | `bench/soak/pw1-soak.pcap` `d2dca393…` |
| soak: console transcript (900 rounds), end read | `bench/soak/console.txt`, `console-end.txt` |
| soak: controller GET_AVB_INFO/GET_AS_PATH, GET_COUNTERS | `bench/soak/watch.jsonl` `997ef3ff…`, `counters.jsonl` `b12d5392…` |
| soak: graders, receipts | `bench/soak/uart-smoke-{pre,post}.log`, `timeline.txt`, `lock.txt`, `launch.txt`, `*.rc`, `tcpdump-*.log`, `remote-sha256.txt` |
| soak: analysis | `bench/soak/console-summary.{txt,json}`, `ctrl-summary.txt`, `wire-analysis.{txt,json}`, `wire-summary.txt` |
| baseline (previous pin) | `bench/baseline-a237/wire-a237-run.txt` (input: `$REVIEWS/530-a237-packet/bench/run/tap-run.pcap`) |
| enumerations | `bench/enum1/`, `bench/enum2/`, `bench/final/`: `a200-enum.log`, entity JSONs, controller-port pcap, probe logs (1 and 2), `remote-sha256.txt` |
| end census, comparison, final console, grader | `bench/final/` |
| clock offsets | `bench/clock-start.jsonl`, `bench/clock-end.jsonl` |
| remote cleanup | `bench/pw1-tmp-before-cleanup.txt`, `bench/capture-server-tmp-before-cleanup.txt`, `bench/cleanup.txt` |

Each enumeration capture's `capture_rc=124` is its `timeout 170`/`timeout 130` expiring, which is
by design, as at #529. Every remote file was hashed on its host before copying, and every copy
matches.

Private provenance note (not public): the eppo build's synthesis log reads `gptp_ucode.hex` from
the `3d2f3e31` build worktree (`sw/builder/out/endstation_ax7101_1x1_tdm8/gptp_ucode.hex`, sha256
`547dd211…`, mtime 10:05 CEST, before the bitstream at 10:31). The `c593cbef` build worktree's file
is `7d850971…`, so the flashed microcode differs from the previous image's.

## Public comment

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5812223671, posted
2026-09-24T10:17:01Z. `public-comment-387.md` is the posted text, and
`posted-comment-387.readback.md` is the API readback, identical except for one trailing newline.
