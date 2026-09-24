# HANDOFF: issue 529 silicon confirmation, A231 bench author, 2026-09-24

Assignment: https://github.com/kebag-logic/milan-fpga/issues/529#issuecomment-5806759522
Reference checkout: $LANES/trusted-dev-20260924-50e78097 (dev `50e78097`, read-only, untouched).
Nothing was flashed, pushed or edited in any repository. No sub-agent was used.

## Outcome

**PASS.** On the dev `50e78097` image the la_avdecc controller classifies the DUT
`IEEE17221|Milan` in all three full enumerations of this run (the #117 step 5
re-run, a 300 s registered session spanning a 180 s CRF bind, and a final
re-run). It logged no compatibility event and no complaint about the DUT. The
#117 downgrade ("[Milan 1.3 - 5.3.8.10] Milan mandatory counters missing for
STREAM_INPUT descriptor") is gone: the CRF Stream Input (STREAM_INPUT 1) now
answers GET_COUNTERS SUCCESS, cdl 148, `counters_valid` `0x00000F3F` with its
ten Table 5.16 counters. At #117 it answered `counters_valid` 0.

Public comment: https://github.com/kebag-logic/milan-fpga/issues/529#issuecomment-5807074042,
posted 2026-09-24T03:36:04Z. `public-comment-529.md` is the posted text, and
`posted-comment-529.readback.md` is the API readback, identical except for one
trailing newline.

## Per-acceptance table

| # | Acceptance (assignment) | Result | Evidence |
|---|---|---|---|
| 1a | DUT identity on the console: CSR ID, VERSION `0x00020060` | PASS | `identity/console-identity.txt`: `ID=4d494c4e` (MILN), `VERSION=00020060`, also by `mem_read 0x90000000/0x90000004`. The CRC readback identifies the image: the QSPI bitstream payload reads `e5fb8b18`, the **eppo seed of dev 50e78097**. The asl seed is `b46a9492`, the eto seed `a1be376b`, and the #117 image (ede8d48e asl) `02036e95`. ROM reads `f6afa4ec` and AEM `93742dd2`, the same as all three 50e78097 seeds (and ede8d48e). Grader 10/10 at 03:14 and 03:28 UTC. `origin/dev` = `50e78097` |
| 1b | gPTP locked (as #117 step 2 checks) | PASS | Console `SYNC=1 ASCAPABLE=1 TU=0` in 12/12 (60 s window), 64/64 (bind window) and 3/3 single reads. GM and parent are the bench AVB switch throughout. Peer delay 381 to 394 ns. `CLKV_STAT=00010002`. gPTP drop counters 0. `RST_EPOCH=1`. The controller's GET_AVB_INFO shows as_capable=1, gptp_enabled=1 and the same GM in 12/12 polls, on the DUT and on the reference peer. GET_AS_PATH is [GM] for the DUT and [GM, peer] for the peer |
| 2 | Full controller enumeration as #117 step 5; no Milan downgrade over the Stream Input counters (CRF input included) | **PASS** | Same enumerator binary (`8c9f2885…`), same la_avdecc libraries (`95d64fd5…`, `8ef4b008…`), same counters probe (`ad579e18…`), same arguments and order as #117 Run C. Counters probe: DUT CLEAN rc 0, complaints 0, transcript identical to the reference peer's. Enumeration: DUT `IEEE17221\|Milan`, milanInfo protocol 1 / certification 0.0.0.0 / specification 1.2.0.0, `compatibility_events` empty, 0 query errors, 0 AECP retries/timeouts/unexpected, enumeration 239 ms, SUMMARY complaints=0. The same result in the 300 s session (224 ms, 0 DUT complaints) and the final run (complaints=0) |
| 3 | GET_COUNTERS on every Stream Input and Output; the reference peer bound to the DUT's CRF output for a few minutes; counters before, during, after; unsolicited notifications | PASS (recorded) | 57 rounds at 5 s over 285 s. Every read of DUT STREAM_INPUT 0/1, STREAM_OUTPUT 0/1, AVB_INTERFACE 0, CLOCK_DOMAIN 0 and peer STREAM_INPUT 8 was SUCCESS (399/399). Bind 180 s, unbound on the first attempt. 187 unsolicited GET_COUNTERS for STREAM_OUTPUT 1, 0 lost. Tables below |
| 4 | HANDOFF, exact commands, tool hashes, raw logs; [A231] comment on #529 | done | this file, `MANIFEST.sha256`, the comment |

## Step 2: enumeration against #117

| | #117 (dev ede8d48e, Run C) | This run (dev 50e78097) |
|---|---|---|
| DUT flags | `IEEE17221` | `IEEE17221\|Milan` (3 of 3 enumerations) |
| compat events | `IEEE17221\|Milan -> IEEE17221`, clause "Milan 1.3 - 5.3.8.10", "Milan mandatory counters missing for STREAM_INPUT descriptor" | none |
| COMPLAINT lines about the DUT | 2 | 0 |
| GET_COUNTERS STREAM_INPUT 1 (la_avdecc, from the capture) | `counters_valid` 0 | SUCCESS, cdl 148, `0x00000F3F`, all ten 0, no unclaimed quadlet non-zero |
| la_avdecc model, STREAM_INPUT 1 counters | `{}` | MEDIA_LOCKED, MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP, FRAMES_RX |
| other GET_COUNTERS (DUT) | SI0 `0xFFF`, SO0/SO1 `0x1F`, AVB `0x23`, CD `0x3`, ENTITY NOT_SUPPORTED, SI 999 NO_SUCH_DESCRIPTOR | identical |
| la_avdecc statistics | enum 164 ms, 0 retry/timeout/unexpected, 33 unsolicited | enum 239 ms, 0 retry/timeout/unexpected, 35 unsolicited, 0 lost |
| reference peer | `IEEE17221\|Milan` | `IEEE17221\|Milan` |
| LOCK_ENTITY | one, flags `0x00000001` (UNLOCK, la_avdecc's lock-state query) | the same |

## Step 3: counters before, during and after the CRF bind

Bind: reference peer STREAM_INPUT 8 (its primary CRF input, clock source not selected)
from DUT STREAM_OUTPUT 1 (CRF output), 03:21:42.077 to 03:24:42.078 UTC (controller-host
NTP clock), by `crf_bind_window.py` unchanged (`29b4ac46…`), args `20 180 40`.

| Descriptor | valid | Before (7 reads, 03:21:07 to 03:21:37) | During (36 reads) | After (14 reads, to 03:25:52) |
|---|---|---|---|---|
| DUT STREAM_INPUT 0 (AAF) | `0xFFF` | all 12 = 0 | all 0 | all 0 |
| **DUT STREAM_INPUT 1 (CRF input)** | **`0xF3F`** | **all 10 = 0** | **all 0** | **all 0** |
| DUT STREAM_OUTPUT 0 (AAF) | `0x1F` | all 0 | all 0 | all 0 |
| DUT STREAM_OUTPUT 1 (CRF output) | `0x1F` | all 0 | STREAM_START 1 to 12, STREAM_STOP 0 to 11. FRAMES_TX restarts at each STREAM_START and rises about one per second, max 20. MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0 | STREAM_START 12, STREAM_STOP 12 (the last stop about 14 s after the unbind), FRAMES_TX 16, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0 |
| DUT AVB_INTERFACE 0 | `0x23` | LINK_UP 1, LINK_DOWN 0, GPTP_GM_CHANGED 0 | unchanged | unchanged |
| DUT CLOCK_DOMAIN 0 | `0x3` | LOCKED 1, UNLOCKED 0 | unchanged | unchanged |
| Peer STREAM_INPUT 8 | `0xFFF` | left from an earlier bind: FRAMES_RX 45,739, MEDIA_LOCKED 1, MEDIA_UNLOCKED 1 | reset to 0 at the bind. MEDIA_LOCKED 1. FRAMES_RX 2,019 (+10 s) to 79,099 (at the unbind). One interruption near 03:22:32 (MEDIA_UNLOCKED 1, STREAM_INTERRUPTED 1, cleared at the restart, as #117 item 12). No SEQ, late, early or unsupported-format counts | FRAMES_RX 79,103, MEDIA_LOCKED 1, MEDIA_UNLOCKED 1 |

The DUT's CRF input counters stay 0 because no CRF stream was directed at the DUT's
CRF input. The assigned bind makes the DUT the talker. `CRF_CTRL` and `CRF_STATUS` read 0
on the console throughout. So on silicon this run proves the CRF input's **solicited
read** (mask, layout, controller decoding, Milan classification). It does not prove non-zero
counting or the CRF input's unsolicited push: its counters never changed, so no push was
due. Those remain evidenced by the root-wire tests (`[CTRS-CRF]`, `[NOTIFY-CRF]`) only.
Exercising them on silicon needs a bind of the DUT's STREAM_INPUT 1 to a CRF talker,
which this assignment did not authorize.

Console during the bind (64 samples, 5 s): `CRFT_CTRL` toggled between `0x3` and
`0x3002e3` (tagged, reservation active, licensed, VID 2, PCP 3). `CRFT_COUNT` went 0 to
89,377 (`0x15d21`) and was frozen from 03:24:55 to the final read at 03:28:55.
`CLKV_TUCNT` stayed 11, and the gPTP drop counters 0.

### Unsolicited notifications (DUT to the registered la_avdecc controller)

The la_avdecc controller was registered 03:20:55.506 to 03:25:55.055 UTC. Every frame was
captured on the controller host's own port, not on the tap.

| Notification | Count | Timing | Content |
|---|---:|---|---|
| GET_COUNTERS STREAM_OUTPUT 1 | 187 | The first came 0.10 ms after the DUT's first probe response and the last 14.4 s after the unbind. Gaps: 185 of mean 0.999996 s, σ 0.075 ms, min 0.999110 s, max 1.000047 s, and one of 9.42 s (the stream was stopped). 57 gaps are under 1.000 s by at most 0.89 ms at the receiver; the controller host's kernel timestamps cannot separate that from path jitter or a few ppm between the DUT's and the host's clocks | All SUCCESS, cdl 148, `0x1F`, addressed to la_avdecc's controller id. Every push differs from the one before, and there were none after the counters stopped. FRAMES_TX drops at each STREAM_START (#530) |
| GET_COUNTERS STREAM_INPUT 0, **STREAM_INPUT 1**, STREAM_OUTPUT 0, AVB_INTERFACE 0, CLOCK_DOMAIN 0 | 0 | none | their counters never changed |
| GET_STREAM_INFO STREAM_OUTPUT 1 | 50 | 3 pairs within 10 ms | outside #529 |
| GET_AVB_INFO AVB_INTERFACE 0 | 259 | about 1 per second | the documented design (#117 item 4) |
| CONTROLLER_AVAILABLE (DUT to controller) | 6 | every 36 to 50 s | all answered SUCCESS within 4 ms |

la_avdecc statistics for the DUT over that session: 496 unsolicited AEM received
(259 + 187 + 50), 0 lost, 0 retries, timeouts or unexpected responses. The final
enumeration (no bind) received 32 unsolicited GET_AVB_INFO and no GET_COUNTERS push.

## Method, and where it differs from #117

- **Identity:** `console_read.py` (the #117 reader, unchanged) under the bench lock: `milan_status`, `mem_list`, three BIOS `crc` reads, `milan_status`, and two `mem_read`s. Then `scripts/baremetal_uart_smoke.py` from the reference checkout (unchanged since ede8d48e, `bc41ab03…`). The expected CRCs come from `expected_crc.py` (unchanged) over the three 50e78097 seed builds and the #117 image.
- **gPTP:** a 60 s console poll at 5 s, with a controller GET_AVB_INFO/GET_AS_PATH watch at 5 s on both entities (`avdecc_ro.py watch`, unchanged).
- **Step 2:** #117 Run C's sequence, with the same controller-host commands and arguments. The only change is the paths: `/tmp/a231/a200_enum` and `/tmp/a231/enum-step2` instead of `/tmp/a200/…`. **Difference:** #117 captured on the inline tap. The tap is an instrument, and instruments are excluded here, so this run captured the controller host's own port (`tcpdump … ether proto 0x22f0`). It sees every AECP exchange with the controller, but not the DUT link's gPTP or the CRF PDUs.
- **Step 3:** `tools/run_bind.sh`, run under the lock. Its parts:
  - the controller-host capture;
  - a console poll every 5 s;
  - the #117 enumerator binary kept alive 300 s as the registered controller (the same binary with a longer `seconds` argument);
  - `a231_counters_poll.py` (new, read-only: GET_COUNTERS through the unchanged `avdecc_ro.Aecp`, sequence ids from `0x1000`);
  - `crf_bind_window.py` (unchanged). It imports `avdecc_ro` from its own directory, `/tmp/a231`, because `/tmp/a200` did not exist.
- **Analysis:** `a231_aecp_pcap.py` (new, offline) decodes every AECP PDU to or from the DUT in the controller-host captures.
- **Census:** `a231_census.sh` = the #117 `census-final.sh` with the tool path changed from `/tmp/a200` to `/tmp/a231`. The diff is line 2 only.
- **Lock:** I also held the bench lock for the console-less controller phases (steps 2 and final), to keep the bench exclusive; #117 did not.
- **Controller-host alias:** `ssh pw1` failed host-key verification, because the name `pw1` is not in known_hosts. `pw1` resolves to the same address as the configured alias `<bench-host-prefix>pw1`, whose pinned key is known, so every remote command used `<bench-host-prefix>pw1`. No host key was accepted or changed.

## Exact commands

Build box, with `PK=$MANAGEMENT/2026-09-23/529-a231` and
`P=/dev/serial/by-id/<adapter>`.

```sh
# identity (lock 03:14:10.636 to 03:14:34.629)
timeout 200 flock -w 60 /tmp/milan-bench.lock bash -c "python3 $PK/tools/console_read.py $P $PK/identity/console-identity.txt milan_status mem_list 'crc 0x00000000 52200' 'crc 0x01000000 3825788' 'crc 0x01400000 7352' milan_status 'mem_read 0x90000000 4' 'mem_read 0x90000004 4'; python3 $LANES/trusted-dev-20260924-50e78097/scripts/baremetal_uart_smoke.py --port $P"
python3 $PK/tools/expected_crc.py $WORKSPACE_HOME/litex-milan/work/build_ax7101_{asl,eppo,eto}_tdm8dev50e78097 $WORKSPACE_HOME/litex-milan/work/build_ax7101_asl_tdm8devede8d48e
# gPTP window (lock 03:15:07.326 to 03:16:07.348)
flock ... python3 $PK/tools/console_poll.py $P $PK/bench/gptp/console.txt 60 5 milan_status 'mem_read 0x90000780 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' 'mem_read 0x900006f4 4' 'mem_read 0x90000750 4' 'mem_read 0x90000764 4'
ssh <bench-host-prefix>pw1 "sudo -n timeout 80 python3 /tmp/a231/avdecc_ro.py watch ens10 60 5 020000fffe000001=02:00:00:00:00:01 3cc0c60102030000=3c:c0:c6:01:02:03"
ssh <bench-host-prefix>pw1 'sudo -n timeout 15 python3 /tmp/a231/avdecc_ro.py discover ens10 6'
ssh <bench-host-prefix>pw1 'bash /tmp/a231/a231_census.sh'            # start 03:16:15, final 03:28:14
# step 2 (lock 03:16:39.036 to 03:19:29.361)
ssh <bench-host-prefix>pw1 'sudo -n timeout 170 tcpdump -i ens10 -w /tmp/a231/step2.pcap ether proto 0x22f0' &
for e in 020000fffe000001 3cc0c60102030000; do ssh <bench-host-prefix>pw1 "sudo -n timeout --signal=TERM 35 $WORKSPACE_HOME/milan-bench/2026-09-08/controller-probe/target-counters-probe ens10 $e 20; echo PROBE_RC=\$?"; done
ssh <bench-host-prefix>pw1 'sudo -n timeout --signal=TERM 70 /tmp/a231/a200_enum ens10 40 /tmp/a231/enum-step2; echo ENUM_RC=$?'
# step 3 (lock 03:20:50.678 to 03:26:36.027)
timeout 480 flock -w 60 /tmp/milan-bench.lock bash $PK/tools/run_bind.sh
# final (lock 03:28:11.372 to 03:30:21.710): tcpdump 130 s, census, a200_enum ens10 40, console_read, grader
python3 $PK/tools/a231_aecp_pcap.py <pcap> 020000fffe000001 --lines     # offline analysis
```

The identity/gPTP, step 2 and final wrappers are recorded verbatim in `tools/run_identity_gptp.sh`,
`tools/run_step2.sh` and `tools/run_final.sh` (each ran as a foreground command under the flock
shown there; step 3 ran `tools/run_bind.sh` itself). Their outputs
(`timeline.txt`, `lock.txt`) record each phase's start and end. Build-box times are UTC but not
NTP-synchronized: the controller host is +1.203 s ahead (`bench/clock-offset-start.txt`, best
RTT 0.8 ms). Controller-host and capture times are NTP.

## Tool hashes (SHA-256)

| Tool | SHA-256 | Provenance |
|---|---|---|
| `a200_enum.bin` (run as `/tmp/a231/a200_enum`) | `8c9f288573e5846d10779b8f96e09fbbcd4d2d7dc3d5ed8fbe398fc28a8b6b35` | #117 binary, unchanged |
| `a200_enum.cpp` | `2d8950f5cdc37617a211a1bb3f2198c005db795f3114bfd86b8db3a94267bd22` | #117 source |
| `libla_avdecc_cxx.so.4.3.1.1` | `95d64fd50715a5170b5a71d8018510d580d12cfce3c0a7b1b389b87a1ce55982` | controller host, unchanged since #117 |
| `libla_avdecc_controller_cxx.so.4.3.1.1` | `8ef4b00829b9f1baf602e67fdd750302b0bf452db569e660dfde4f72041bbc32` | same |
| `target-counters-probe` / `.cpp` | `ad579e18e46b566cbeea34c188e4b324228bb3daac6296742f689fecff159dc7` / `0e9faf3096c87294e966d6f5ffb93298e40473dbf3fc490e6e83f262f91016dc` | unchanged since 2026-09-08 |
| `avdecc_ro.py` | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` | #117, unchanged |
| `crf_bind_window.py` | `29b4ac468f5fb58f53053db353be675c0d8aad84e6a296fc02722140aa8ee152` | #117, unchanged |
| `console_read.py` | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` | #117, unchanged |
| `console_poll.py` | `3a0de7d8e1f9f4e0f87d03364c3cf35e9965210dd7095b21ef9d1b7bdb1bd326` | #117, unchanged |
| `expected_crc.py` | `04d128bb0a9ffe8ad5898f4ece380899a096a1595aadda3ece1048c313bf19d7` | #117, unchanged |
| `scripts/baremetal_uart_smoke.py` | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` | dev 50e78097 (identical to ede8d48e) |
| `a231_census.sh` | `d4e94e204d5a4a0d6be1910b91b8480c5327d679eb115854fd7f5e97a56efbdb` | #117 `census-final.sh` (`06e9383b…`) with the path changed |
| `a231_counters_poll.py` | `c32a20bc33c64ce96fc95212df13f1fc92e7808c67570792e8b2fafbd46920f7` | new |
| `a231_aecp_pcap.py` | `f169ce9d9ab85e6266d7da74a87e3630c1d922d98fa44d7c4c32b6593d1f2be8` | new, offline |
| `a231_clock_offset.py` | `81fc009763c93afd43b8bcda4b0c355868df2b5fb87c39f103ee963613ffcbe1` | new |
| `run_bind.sh` | `4cc7396afeaa57362fe543e0d32a45ac8293b8c735280c2d1bb5b6cc732b1038` | new |
| controller host | Python 3.14.6, tcpdump 4.99.6, libpcap 1.10.6, NTPSynchronized=yes | |

## Raw logs (primary)

| Artifact | SHA-256 |
|---|---|
| `identity/console-identity.txt` | see MANIFEST |
| `bench/step2/a200-enum.log` | see MANIFEST |
| `bench/step2/entity_0x020000fffe000001.json` | `38bdc1fceda8a80e090ae07e793115892ee2ab0dcd392437cb07d0a8da155ab8` |
| `bench/step2/pw1-step2.pcap` | `f6617ab7908b24e62eacb04642d89221aec2c38ef006608026f242b4951cfb99` |
| `bench/step3/pw1-bind.pcap` | `0dc0dd8f72303964c893810fabde43fc3d6d6a34e0f582c14a9f2b04fcdda8db` |
| `bench/step3/entity_0x020000fffe000001.json` | `9510638e490c98c891f01b801722857bded92d1e76a84d75040f02e6ba744ae4` |
| `bench/final/pw1-final.pcap` | `04165d678d3ef59acb417d9d877ece37e92def8572bbf9c82518b7070664c6bd` |
| `bench/final/entity_0x020000fffe000001.json` | `1ae3ccec9b5ca8dba2ff206639bb948838a7e1333dabf1f03284663cf8572f63` |

Each pcap and JSON was hashed on the controller host before copying, and the copy verified
against it (`bench/*/remote-sha256.txt`, and `bench/pw1-tmp-before-cleanup.txt` for every
remote file). `MANIFEST.sha256` covers every file in this packet except itself.

## Observations outside #529 (for the coordinator; no issue filed)

1. **`CTLR_DIAG` (0x6F4) is a structural zero, but the register map describes it as live.** `hdl/milan/milan_datapath.sv:3201` has `assign aecp_ctlr_diag = 32'd0;`. The REGISTER_MAP row (line 1223) and its note (1227 to 1234) describe live probe, reply and eviction tallies, with no STRUCTURAL ZERO marker. It read 0 throughout, while the capture shows the DUT sent 6 CONTROLLER_AVAILABLE probes, all answered. So the departing-controller behaviour works on the wire, but the CSR cannot show it. The #117 evidence page's inference "CTLR_DIAG still read 0 … so no controller was left for it to evict" therefore rests on a tied-off word. Candidate: a Docs issue (and a check of the #117 page's sentence).
2. **#530 items reproduced on 50e78097** (already tracked; no new issue):
   - The CRF talker restarted 12 times in 194 s (STREAM_START 12, bursts of about 15 s).
   - FRAMES_TX rises about 1 per second and restarts at each STREAM_START.
   - The stream kept running after the unbind: its last STREAM_STOP was pushed 14.4 s after the DISCONNECT_RX response, and 16.1 s after the DUT's last probe response (03:24:40.419).
   - The first counters push (STREAM_START 1) came 0.10 ms after the DUT's first probe response, which carried status 3 (TALKER_DEST_MAC_FAIL); later probe responses were SUCCESS, with `dmac` `91:e0:f0:00:6b:4e`. This is #530 item 2.
   - The DUT emitted 89,377 PDUs (`CRFT_COUNT`) against the peer's FRAMES_RX of 79,103. Without the tap this run cannot place the difference in time.
3. **Unsolicited GET_STREAM_INFO for STREAM_OUTPUT 1 came 3 times as two pushes within 10 ms.** This is not assessed against the per-descriptor limit here.
4. **The reference peer, not the DUT,** drew 22 la_avdecc complaints while bound: "[Milan 1.2 - 5.4.2.10.1] StreamInfoFlag bit 24 is reserved and must be set to 0". la_avdecc flagged it `IEEE17221|Milan|MilanWarning` during the 300 s session, and `IEEE17221|Milan` again in the final run.
5. **The #117 enumerator records `seconds` of discovery, then dumps.** Keeping it alive as the registered controller for step 3 is a longer argument to the same binary, not a new build.

## Not run

- Hive: needs an interactive desktop, as at #117.
- behave on hardware: the suite has no hardware tier.
- Non-zero counting and the unsolicited push of the DUT's CRF **input**: not exercised, because the assigned bind has the DUT as talker. See step 3.
- Tap captures: the tap is an instrument.

## Bench access and state

| Window (build-box UTC; controller host +1.2 s) | What | Lock |
|---|---|---|
| 03:14:10.636 to 03:14:34.629 | identity, grader | held |
| 03:14:47 to 03:14:50 | clock offset, ADP discovery | none (controller only, read-only) |
| 03:15:07.326 to 03:16:07.348 | gPTP window | held |
| 03:16:15 to 03:16:17 | census start | none (read-only) |
| 03:16:39.036 to 03:19:29.361 | step 2 | held |
| 03:20:50.678 to 03:26:36.027 | step 3 (bind 03:21:42.077 to 03:24:42.078 NTP) | held |
| 03:28:11.372 to 03:30:21.710 | final census, enumeration, console, grader | held |

State changes made and their end state:

- **Bind.** Peer STREAM_INPUT 8 from DUT STREAM_OUTPUT 1, for 180 s. It unbound on the first attempt, and the input read unbound in all 8 post reads and in the final census.
- **la_avdecc registrations.** Three: 03:16:47.023 to 03:17:24.425, 03:20:55.506 to 03:25:55.055, and 03:28:18.927 to 03:28:56.851 NTP. Each REGISTER and DEREGISTER was answered SUCCESS.
- **Census.** Final against start: 18 of 18 ACMP states unbound, with connection count 0. Peer configuration 0, 96 kHz, clock source 0, CRF input format `041060010000bb80`, and GET_CLOCK_SOURCE, GET_STREAM_FORMAT and GET_SAMPLING_RATE identical. READ_DESCRIPTOR payloads differ only in the reserved half-word after `configuration_index`, which the peer varies (as #117). The DUT's GET_AVB_INFO differs only in the propagation-delay low byte.
- **Residuals, as at #117.** The DUT's STREAM_OUTPUT 1 GET_TX_STATE `stream_dest_mac` reads `91:e0:f0:00:6b:4e` (was `00:00:00:00:00:00`). STREAM_OUTPUT 1 counters read STREAM_START and STREAM_STOP 12, FRAMES_TX 16. `CRFT_COUNT` is 89,377. These are counters and the last destination; the talker is idle (`CRFT_CTRL=0x3`, `CRFT_COUNT` frozen for 4 minutes).
- **DUT at the end.** Grader 10/10 at 03:28:56. `SYNC=1 ASCAPABLE=1 TU=0`, same GM, `CLKV_STAT 00010002`, `LINKG_STAT 0x83`, `RST_EPOCH 1`, drops 0.
- **Controller host.** `/tmp/a231` was created at 03:14 and removed at 03:31, after every file had been hashed (`bench/pw1-tmp-before-cleanup.txt`) and the copies verified. No process of this run remains.
  - **Disclosure:** at 03:11 a probe command ran `flock -n /tmp/milan-bench.lock true` on the controller host by mistake. That created an empty `/tmp/milan-bench.lock` there, which I removed in the next command (03:11). It was never a bench lock, since the bench lock is the build box's.
- **Not touched.** Flash, JTAG, power strip, wiring, instruments, the tap and its capture server. The local bench lock is free.
