<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# gPTP silicon evidence for issue 117: one AX7101 against the reference peer

*Measured on 2026-09-23 between 12:41 and 13:14 UTC on the AX7101 flashed with
the dev `ede8d48e` image at 12:35 UTC. Owning issue:
[#117](https://github.com/kebag-logic/milan-fpga/issues/117), under
[#110](https://github.com/kebag-logic/milan-fpga/issues/110); it gates the
physical acceptance of [#116](https://github.com/kebag-logic/milan-fpga/issues/116).
Bench steps 2, 4 and the controller part of step 5 ran. Step 3 (grandmaster
loss and return) did not run: no permitted software control exists on this
bench, recorded under [Owner blockers](#owner-blockers). Audio continuity is
deferred to 2026-12-31 and is not measured here.*

## Contents

- **[Result per acceptance box](#result-per-acceptance-box)** -- PASS, FAIL or NOT RUN for every part of the five acceptance boxes, and why the asCapable partner is the bench switch.
- **[Candidate image and identity proof](#candidate-image-and-identity-proof)** -- The exact build, its artifact hashes, and the console CRC readback that proves the board runs it.
- **[Topology and capture points](#topology-and-capture-points)** -- Who is grandmaster, where the reference peer and the controller host sit, the peer's firmware identity, and what the tap records.
- **[Methodology](#methodology)** -- Each run's window, what it exercised, how long it held the bench lock, and how CSRs were read.
- **[Tool revisions](#tool-revisions)** -- Revisions and hashes of every script, library and capture tool used.
- **[Step 2: asCapable, cadence and turnaround](#step-2-ascapable-cadence-and-turnaround)** -- Sync, Announce and Pdelay cadence, the Pdelay turnaround in both directions, and the asCapable retention record.
- **[Step 3: GM loss and return](#step-3-gm-loss-and-return)** -- Why the step did not run and the baseline a later run measures against.
- **[Step 4: publication CSRs and tu against the wire](#step-4-publication-csrs-and-tu-against-the-wire)** -- Every publication word set beside the wire and the controller view, and the `tu` bit on 34,061 CRF PDUs.
- **[Step 5: controller discovery and enumeration](#step-5-controller-discovery-and-enumeration)** -- Counters-probe parity with the reference peer, and the la_avdecc enumeration that downgrades the DUT from Milan.
- **[Observations outside the acceptance boxes](#observations-outside-the-acceptance-boxes)** -- Measured behavior that needs its own issue: CRF talker bursts ending on their own, FRAMES_TX, notification rate, the switch.
- **[Bench state restored](#bench-state-restored)** -- The before-and-after census proving no binding or peer setting was left changed.
- **[Owner blockers](#owner-blockers)** -- The decisions the owner must make before step 3 and the remaining rows can run.
- **[Raw artifacts](#raw-artifacts)** -- SHA-256 of the primary raw captures, transcripts and logs in the private packet.

## Result per acceptance box

Every row states what was measured. A row that was not measured says NOT RUN.

| Acceptance box of #117 | Part | Result |
|---|---|---|
| 1. Reaches and retains asCapable against the Milan-validated reference peer, inside Milan limits, compliant intervals and turnaround, no software gPTP daemon | retains asCapable | PASS: asCapable on every console, controller and wire observation from 12:41 to 13:14 UTC |
| | reaches asCapable | NOT RUN: the transition happened after the 12:35 UTC power cycle, before these windows opened |
| | peer delay inside the 800 ns bound | PASS: 380 to 391 ns |
| | message intervals | PASS: see [Step 2](#step-2-ascapable-cadence-and-turnaround) |
| | Pdelay turnaround inside 15 ms | PASS: at most 11.009 us |
| | no software gPTP daemon | PASS: bare-metal image; no daemon on any bench host |
| 2. GM loss and return recover automatically within the documented bound | all | NOT RUN: [Owner blockers](#owner-blockers) B1 and B2 |
| 3. Publication words and `tu` are fabric-owned on the booted image | steady state against the wire | PASS: every word agrees with the wire and with the controller view |
| | transition (GM change, sync loss) | NOT RUN: needs box 2 |
| 4. External conformance, latency and audio continuity pass without a stale or skipped mandatory row | la_avdecc counters probe, parity with the reference peer | PASS |
| | la_avdecc full enumeration, Milan compatibility | FAIL: Milan downgraded to IEEE 1722.1 over the CRF Stream Input counters |
| | Hive | NOT RUN: needs an interactive desktop |
| | behave against hardware | NOT RUN: the suite has no hardware tier |
| | latency (#64, #213) | NOT RUN: outside this assignment |
| | audio continuity | NOT RUN: deferred to 2026-12-31 |
| 5. Findings include topology, capture points, raw artifacts, exact hashes, tool revisions and methodology | this page | PASS for the runs recorded here |

The asCapable link partner is port 1 of the bench AVB switch, which is the
grandmaster. The reference peer is a time-aware end station on another port
of the same switch, synchronized to the same grandmaster. That is the one-DUT
topology the owner fixed on 2026-09-06; see
[Topology and capture points](#topology-and-capture-points).

## Candidate image and identity proof

The DUT runs build `build_ax7101_asl_tdm8devede8d48e`: dev
`ede8d48ecd7c7f589a14b957951f040d92c99c70` (tree
`ff9950bcc396341f0156829ea1a2bf371abeaad0`),
`configs/endstation_ax7101_1x1_tdm8.yaml`, seed `asl` (routed WNS +0.194 ns),
`VERSION` `0x0002_0060`. The manager flashed it with `flash-pair` and a cold
power cycle at 12:35 UTC.

| Artifact | SHA-256 |
|---|---|
| `gateware/alinx_ax7101.bit` | `f0725eef7a361bd7dc6d692c369868f25e5d4f49f6b7267562a0b5f949ada33d` |
| bitstream payload (3,825,788 B after the 204 B header) | `aaece32fc6c84f790273878350f674c142407a6b9ff2097862870784921da5fb` |
| `aem_desc.bin` (7,352 B) | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `software/bios/bios.bin` | `69322600bc9dc40a698ed30d125d29d2723f51cc1b26c0f1c3abc96acb39deab` |
| `flashboot_layout.json` | `71e798fc401ed3fbaac4cd43a299f23498beafa466aaa17d6773590a62fa93e2` |
| `csr.csv` | `4db0e6da9c9c910a5ee00e56c25908c190c380799e44c846bcfb4ffc7dc045a7` |

The identity was read back over the console under the bench lock, 12:41:19
to 12:41:43 UTC, with read-only commands only (`milan_status`, `mem_list`,
three BIOS `crc` reads). The method is the one the earlier identity gate on
#117 used.

| Region | Bytes | Expected CRC32 | On board |
|---|---:|---|---|
| ROM (BIOS with linked firmware) | 52,200 | `f6afa4ec` (all three seeds) | `f6afa4ec` |
| QSPI offset 0, bitstream payload | 3,825,788 | `02036e95`; seeds `eppo` `7b415f48`, `eto` `2567bab7`; the replaced `f6b31625` image `a6fb19bb` | `02036e95` |
| QSPI +4 MiB, AEM slot | 7,352 | `93742dd2` | `93742dd2` |

- `VERSION=00020060` on both status reads.
- [`scripts/baremetal_uart_smoke.py`](../../scripts/baremetal_uart_smoke.py) passed 10 of 10 with exit 0, both at 12:41 UTC and at 13:13 UTC.
- `origin/dev` was still `ede8d48e` when the run started, so no later dev change could need a byte comparison.
- `VERSION` is shared with the replaced `f6b31625` image, so it does not identify the image; the CRCs and hashes above do.
- Limits: CRC32 is a consistency check, not a SHA-256 readback, and the running configuration was not read back over JTAG.

## Topology and capture points

```text
  AX7101 DUT --- inline tap --- port 1 [ bench AVB switch ] port 8 --- controller host
                                        [ grandmaster     ]
                                        [ clock 3cc0c6fffefe0210 ]
                                        [ another port    ] ------- reference peer, primary interface
```

- **Grandmaster.** The bench AVB switch, clock identity `3cc0c6fffefe0210`. It announces priority1 246, clockClass 248, clockAccuracy `0x20`, offsetScaledLogVariance `0x436A`, priority2 248 and timeSource `0xA0`, with stepsRemoved 0. The PathTrace carries itself only.
- **Reference peer.** A Milan-validated end station with two AVB interfaces, both priority1 248. Its GET_AS_PATH on interface 0 is `[3cc0c6fffefe0210, its own clock]`, and its GET_AVB_INFO names the same grandmaster. Its GET_MILAN_INFO reports protocol version 1, `certification_version` 1.1.0.0 and specification 1.2.0.0.
- **Peer firmware identity.** The ENTITY `firmware_version` field holds seven octets. The SHA-256 of the 64-octet field is `33f0e7f9e86fe4829a2de6f6d04d1edf1463b7d6653c2865ad985f183b0ddfbc`, the same value recorded on 2026-09-14. The string itself stays in the private packet, as it did then.
- **Peer state.** Configuration 0 of 2, sampling rate 96 kHz, clock source 0 (INTERNAL). Every Stream Input was unbound and every Stream Output idle, both before and after the runs.
- **Controller host.** It sits on switch port 8. It runs no gPTP daemon, so the switch sends it Pdelay_Req only.
- **Capture point.** One inline tap on the DUT link, the only tap attached. It stamps both directions on one clock: tap port 3 carries frames the DUT sent, tap port 2 carries frames the switch sent. Each record carries a 28-octet envelope whose nanosecond word wraps every 2^32 ns. The decoder unwraps it against the capture host time. Records without a valid envelope are the capture host's own traffic and are excluded (76 in Run A, none elsewhere). Every capture reports 0 kernel drops.

## Methodology

Times below are the build box's UTC. That clock was not NTP-synchronized and
ran about 1.2 s behind the two NTP-synchronized bench hosts (plus or minus
0.2 s). No correlation below depends on it at better than 1 s. Intervals come
from the tap clock, and the controller-host times are NTP times.

| Run | Window (UTC) | What ran | Bench access |
|---|---|---|---|
| Identity | 12:41:19 to 12:41:43 | console CRC readback, UART grader | lock held 24 s |
| Probe | 12:42 to 12:53 | 12 s tap capture (12:42), ADP discovery (12:46), reference peer descriptors (12:47), binding census (12:52), peer clock sources (12:53) | no lock (no console) |
| CSR read check | 12:51:58 | console `mem_read` of words whose values are known (ID, VERSION, PDELAY, CLKV_STAT, GPTP_LAT) | lock held 0.2 s |
| A | 12:56:14 to 13:01:29 | 315 s tap capture; console `milan_status` plus nine CSR reads every 5 s; controller GET_AVB_INFO and GET_AS_PATH on the DUT and the peer every 5 s | lock held 300 s |
| B | 13:04:35 to 13:06:30 | 115 s tap capture; console poll every 2 s; a 60 s bind of the peer's primary CRF input to the DUT's CRF output, 13:04:49 to 13:05:49 | lock held 105 s |
| C | 13:10:39 to 13:12:20 | 100 s tap capture; la_avdecc counters probe on the DUT, then on the peer; la_avdecc full enumeration | no lock (no console) |
| Final | 13:13:43 to 13:14:25 | 40 s tap capture; console read; UART grader; binding and settings census | lock held 1 s |
| Peer control | 13:19 | the reference peer's one CONTROL descriptor, read-only | no lock (no console) |

Console CSR reads use the LiteX BIOS `mem_read` on the Milan CSR window at
`0x90000000`. They read single words that are not cleared by a read. The
firmware's `milan_status` supplies the snapshot pairs (GM and parent), so no
raw read ever splits a snapshot. The console reader refuses any command
outside a read-only allowlist.

The Pdelay turnaround follows the method the owner's 2026-09-20 record used,
with its script reused byte for byte. The turnaround seen at the tap is
compared with the turnaround the responder claims (`t3 - t2`, correction
fields included), per exchange, in both directions. The same pairing gives
the tap-observed turnaround bound checked against the Milan 15 ms limit
([Milan compliance matrix](../reference/MILAN_COMPLIANCE_MATRIX.md), row
4.2.6.2.6).

## Tool revisions

| Tool | Revision |
|---|---|
| UART grader | `scripts/baremetal_uart_smoke.py` at `ede8d48e`, SHA-256 `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` |
| Console readers | `console_read.py` `652d6f83...` (adds `mem_read` to the earlier read-only allowlist), `console_poll.py` `3a0de7d8...` |
| Tap decoder and correlation | `wire_summary.py` `c5039d95...`, `analyze_run.py` `6ac03a87...`, `stream_timeline.py` `9d2e8629...` |
| Pdelay turnaround script | `pdelay_turnaround.py` `790e6b7c...`, unchanged from the 2026-09-20 record |
| Raw AVDECC reader | `avdecc_ro.py` `17283696...`; joins `91:E0:F0:01:00:00`; AECP control_data_length 12 plus payload; ACMP control_data_length 44 |
| CRF bind window | `crf_bind_window.py` `29b4ac46...`; one fixed pair; refuses unless the input reads unbound; unbinds on exit or signal |
| la_avdecc | 4.3.1-beta1 built from tag `v4.3.1.1` (`6d61a92e7f264c69f23cdc38f50d31114e567aa0`); `libla_avdecc_cxx.so.4.3.1.1` `95d64fd5...`, `libla_avdecc_controller_cxx.so.4.3.1.1` `8ef4b008...` |
| la_avdecc counters probe | `target-counters-probe` `ad579e18...` from source `0e9faf30...`, both unchanged since 2026-09-08 |
| la_avdecc enumerator | `a200_enum.cpp` `2d8950f5...`, binary `8c9f2885...`, g++ 16.1.1, the defines the installed library exports |
| Capture | tcpdump 4.99.6, libpcap 1.10.6, tap driver 1.11.3, tap firmware 0.2.3.41 |

Full hashes are in the packet manifest listed under
[Raw artifacts](#raw-artifacts).

## Step 2: asCapable, cadence and turnaround

Counts and statistics below are summed over the Run A, B, C and final
captures (570 s of tapped link).

| Stream | Direction | Count | Interval | Check |
|---|---|---:|---|---|
| Sync (with one Follow_Up each) | switch to DUT | 4,556 intervals | mean 124.99 to 125.02 ms per run, min 100.6 ms, max 149.4 ms; `logMessageInterval` -3 | all 4,556 within 30 % of 125 ms |
| Announce | switch to DUT | 565 intervals | mean 1000.2 to 1006.0 ms, max 1010.6 ms; `logMessageInterval` 0 | all within 30 % of 1 s |
| Pdelay_Req | switch to DUT | 564 intervals | mean 1002.0 to 1007.6 ms, max 1029.6 ms | all within 30 % of 1 s |
| Pdelay_Req | DUT to switch | 566 intervals | every interval 1000.002 ms; `logMessageInterval` 0; source port `020000fffe000001:0001` | all within 30 % of 1 s |

The DUT sends no Sync or Announce on this link. Its port is a slave port, and
the only gPTP frames it sends are its Pdelay requests and its responses.

| Pdelay exchange | Exchanges | Tap-observed request to response | Response to Follow_Up | Claimed `t3 - t2` | Tap minus claimed |
|---|---:|---|---|---|---|
| switch requests, DUT responds | 568 of 568 complete | 10,984 to 11,009 ns (median 10,992 to 11,000 per run) | 7,552 to 7,569 ns | 10,608 to 10,629 ns | median 383 to 391 ns per run (371 to 400) |
| DUT requests, switch responds | 570 of 570 complete | 0.68 to 0.88 ms, and two at 18.33 and 18.36 ms (Run A) | 0.53 to 1.11 ms | the same as the tap, less 385 to 524 ns | median 393 to 394 ns per run (385 to 524) |

- **Turnaround.** The DUT answers within 11.009 us, against the 15 ms Milan limit.
- **Tap check.** The tap-minus-claimed difference in both directions matches the 2026-09-20 record (391 and 392 ns). The tap's own transit dominates it, so the DUT's corrected stamps still read like the switch's.
- **asCapable retained.**
  - The console read `SYNC=1 ASCAPABLE=1 TU=0` in all 116 samples (60 in Run A, 53 in Run B, two at the identity read, one at the end), and the grader read the same at 12:41 and 13:13 UTC.
  - The controller's GET_AVB_INFO reported AS_CAPABLE in all 60 Run A polls.
  - On the wire, the switch never stopped sending Sync to the DUT: the largest gap is 149.4 ms.
  - All 1,138 Pdelay exchanges completed.
- **No software gPTP daemon.** The DUT runs bare-metal firmware with no operating system. Every DUT-side gPTP frame carries the fabric port identity. A process check at 12:55 UTC found no gPTP daemon on the controller host or on the capture server.

## Step 3: GM loss and return

NOT RUN. This assignment allows GM loss and return only through the
reference peer's own software controls or a managed-switch port command, and
neither exists on this bench without physical action. The facts are under
[Owner blockers](#owner-blockers) B1 and B2. Nothing on the bench was powered,
unplugged or reconfigured to substitute for it.

The baseline a later step 3 run would measure against is the Step 2 table:
Sync at 125 ms, Announce and Pdelay at 1 s, GM `3cc0c6fffefe0210`, peer delay
380 to 391 ns and `CLKV_TUCNT` steady at 11.

## Step 4: publication CSRs and `tu` against the wire

Steady state, Runs A and B plus the final read. Addresses and fields are as
in the [register map](../reference/REGISTER_MAP.md).

| Publication | Console CSR | Wire | Controller (AECP) |
|---|---|---|---|
| GM identity | `0x624`/`0x628` `3cc0c6fffefe0210`, every sample | Announce grandmasterIdentity, all 569; DUT ADPDU `gptp_grandmaster_id`, all | GET_AVB_INFO `gptp_grandmaster_id`, 60 of 60 |
| Parent | `0x730`/`0x734` `3cc0c6fffefe0210` | Announce and Sync source port `3cc0c6fffefe0210:0001` | not served |
| Path | `ASP_CMD` `0x11` (generation 1, count 1) | PathTrace TLV `[3cc0c6fffefe0210]` in every Announce | GET_AS_PATH count 1, `[3cc0c6fffefe0210]`, 60 of 60 |
| Peer delay | `GPTP_PDELAY` 380 to 391 ns (median 385) | tap minus claimed, median 383 to 394 ns | GET_AVB_INFO propagation_delay 381 to 391 ns (median 385) |
| Domain | `0x62C` 0 | domainNumber 0 in every gPTP frame; ADPDU domain 0 | domain 0 |
| sync, asCapable, `tu` | `CLKV_STAT` `0x00010002` (sync 1, asCapable 1, holdover 0, `tu` 0), every sample | `tu=0` on all 34,061 CRF PDUs the DUT sent in Run B | flags `0x17` (AS_CAPABLE, GPTP_ENABLED, SRP_ENABLED, AVTP_DOWN_VALID with AVTP_DOWN clear); Stream Output 1 TIMESTAMP_UNCERTAIN 0 |
| `tu` intervals | `CLKV_TUCNT` 11, unchanged from 12:56 to 13:14 UTC | none with `tu=1` | not served |
| Latency corrections | `GPTP_LAT` `0x029000DB` (656 ns ingress, 219 ns egress) | not on the wire | not served |
| Plane drops | `GPTP_DROPW` and `GPTP_DROPE` 0 | no incomplete exchange | not served |
| CRF emission | `CRFT_COUNT` 0 before the bind, 34,061 (`0x850D`) after | 34,061 CRF PDUs, sequence numbers continuous | Stream Output 1 STREAM_START 4 and STREAM_STOP 4, matching the four bursts on the wire; FRAMES_TX 16 (see [Observations](#observations-outside-the-acceptance-boxes)) |
| CRF licence | `CRFT_CTRL` `0x3` idle, `0x3002E3` while licensed (tagged, reservation active, licensed, PCP 3, VID 2), `0x3` after | frames tagged PCP 3, VID 2 | not served |

- **The `tu` bit on the wire.** The DUT emits AVTP only for a licensed stream, so Run B bound the reference peer's primary CRF input (its clock source stayed INTERNAL) to the DUT's CRF output for 60 s. The DUT sent 34,061 CRF PDUs between 13:04:49.297 and 13:05:59.198 UTC, every one with `tu=0`, while `CLKV_STAT[0]` read 0 in all 53 samples. The peer, as listener, counted MEDIA_LOCKED 1, FRAMES_RX 26,646, TIMESTAMP_VALID 26,646 and TIMESTAMP_UNCERTAIN 0.
- **Why "fabric-owned".**
  - The firmware only reads these words. The register map declares them read-only live with inert writes.
  - No software gPTP owner exists on the image.
  - Each word tracks the wire it summarizes.
- **Timescale.** A coarse check put the DUT PHC minus grandmaster time at -0.072 s at each Run A console read. It was constant within 2 ms over 5 minutes, which is inside the 0.3 s host-clock uncertainty: the PHC runs on the grandmaster's timescale and rate.
- **Limit.** This is steady-state correlation only. The transition half (`tu` asserting on a GM change or on sync loss, and the publication following a new GM) needs step 3.

## Step 5: controller discovery and enumeration

| Check | Result |
|---|---|
| ADP discovery from the controller host | two entities: the DUT (`020000fffe000001`, model `0x001BC5C40236BA0E`, firmware `2.96.0`) and the reference peer; both advertise grandmaster `3cc0c6fffefe0210` |
| la_avdecc counters probe, DUT | CLEAN, rc 0, complaints 0: GET_COUNTERS ENTITY NOT_SUPPORTED, STREAM_INPUT 0 SUCCESS (`0x00000FFF`), STREAM_INPUT 999 NO_SUCH_DESCRIPTOR, AVB_INTERFACE 0 SUCCESS (`0x00000023`), CLOCK_DOMAIN 0 SUCCESS (`0x00000003`) |
| la_avdecc counters probe, reference peer | the same transcript line for line: PASS by parity, the bar [TESTING.md](../testing/TESTING.md) sets |
| la_avdecc full enumeration, DUT | enumeration time 164 ms (library statistic), 0 query errors, 0 AECP retries, timeouts or unexpected responses, average response 3 ms |
| la_avdecc Milan compatibility, DUT | FAIL: flags `IEEE17221` only; the library logged "[Milan 1.3 - 5.3.8.10] Milan mandatory counters missing for STREAM_INPUT descriptor" and "Entity not fully Milan compliant" |
| la_avdecc full enumeration, reference peer | online, 0 query errors, flags `IEEE17221` and `MILAN` |
| Hive | NOT RUN: needs an interactive desktop |
| behave against hardware | NOT RUN: [tests/README.md](../../tests/README.md) defines the suite as offline only, with no hardware tier |

- **Why Milan was downgraded.** The failing descriptor is Stream Input 1, the CRF media-clock input: its GET_COUNTERS returns `counters_valid` 0. The register map already records this CRF Stream Input counter gap with closure criteria. The DUT's GET_MILAN_INFO reports protocol version 1, `certification_version` 0.0.0.0 and specification 1.2.0.0.
- **Controller registration.** la_avdecc registered for unsolicited notifications at 13:10:47.0 and deregistered at 13:11:26.5 UTC. The DUT answered both with SUCCESS, and its `CTLR_DIAG` still read 0 at 13:13 UTC, so no controller was left for it to evict.

## Observations outside the acceptance boxes

These are measured facts that no acceptance box of #117 covers. Each needs its
own issue; none is assigned a cause here.

1. **The DUT's CRF talker ends its own bursts while the listener stays bound.** Run B has four bursts: 19.67 s, 18.45 s, 15.00 s and 15.00 s. At each end the DUT stops emitting, sends an MSRP TalkerAdvertise Leave 10 to 166 ms later, and the switch withdraws the Listener about 2 ms after that. The reference listener then re-probes (ACMP CONNECT_TX) and emission resumes 0.3 to 0.7 ms after the DUT's probe response. The pauses last 1,106 ms, 578 ms and 148 ms, with no sequence gap. Three of the four ends fall 15.00 s (plus or minus 2 ms) after the latest successful probe response. That includes the last, which came 9.95 s after the unbind had already withdrawn the Listener.
2. **The first CRF burst started before any reservation existed.** The DUT answered the first probe with TALKER_DEST_MAC_FAIL (status 3) and began emitting 0.18 ms later. The first Listener Ready reached it 4.7 s after that.
3. **Stream Output 1 FRAMES_TX reads 16.** The wire and `CRFT_COUNT` both show 34,061 PDUs. STREAM_START and STREAM_STOP (4 each) and TIMESTAMP_UNCERTAIN (0) do agree with the wire.
4. **The DUT sends one unsolicited GET_AVB_INFO per second to a registered controller.** Each carries a propagation delay a few nanoseconds away from the last: 33 in 40 s, with no two consecutive values equal. This is the documented design (register map, `VERSION` `0x0055` notes), recorded here for controller-load review.
5. **The bench AVB switch requests an IPv4 address by DHCP every 15 s on the AVB segment, and nothing answers.**
6. **The bench AVB switch answered two of the DUT's Pdelay requests after 18.33 and 18.36 ms (Run A).** That is over the 15 ms limit on its side. Its other 568 answers took at most 0.88 ms. The DUT completed both exchanges, and its published peer delay did not move outside 380 to 391 ns.

The Run B timeline with tap-clock times is in the packet (`stream-timeline.txt`).

## Bench state restored

- **Bindings.** The binding census after the runs matches the one before them for all 18 states read: peer Stream Inputs 0 to 9, peer Stream Outputs 0 to 3, DUT Stream Inputs 0 and 1, and DUT Stream Outputs 0 and 1. All are unbound, with connection count 0.
- **Peer settings.** Configuration 0, sampling rate 96 kHz, clock source 0 (INTERNAL), CRF input format `041060010000bb80`, the same firmware hash and the same descriptor bytes. The only difference is the reserved half-word ahead of each descriptor, which the peer fills with varying values.
- **Run B cleanup.** The Run B unbind succeeded on its first attempt. The DUT's `CRFT_CTRL` returned to `0x3`, and the final capture carries no AVTP stream.
- **DUT.** 10 of 10 on the grader at 13:13 UTC, same GM, `CLKV_STAT` `0x00010002`, drop counters 0, `LINKG_STAT` `0x83`, `RST_EPOCH` 1.
- **Hosts.** The multicast memberships ended with their processes. Every temporary file on the controller host and the capture server was copied, verified by SHA-256, and removed. No capture or probe process remains, and the bench lock is free.
- **Not touched.** Flash, JTAG, power, wiring and instruments were not touched.

## Owner blockers

- **B1. No permitted way to induce GM loss and return.**
  - The grandmaster is the bench AVB switch, not the reference peer. The peer is a slave in the same domain.
  - The peer's AEM exposes a single CONTROL, IDENTIFY (control type `90E0F00000000001`). AVDECC defines no command that changes gPTP priority.
  - The switch has no AVDECC entity and no address on the AVB segment, and no management path or credentials are provisioned on any bench host.
  - The repository's own procedure is the physical checklist entry `phys.switch-cycle.gm-partition` of [`tb/tools/torture_campaign.py`](../../tb/tools/torture_campaign.py), a power-strip cycle of the switch. This assignment excludes power actions as a GM-loss method.
  - Decision needed: authorize that switch power cycle under the bench lock, or provision a management path to the switch (address and credentials) for a port or priority command.
- **B2. No numeric recovery bound is documented.** The box asks for recovery "within the documented bound", and [GM loss and recovery](../design/GM_LOSS_RECOVERY.md) states none. The protocol figures are:
  - a 3 s announce receipt timeout (3 times 1 s);
  - a 375 ms sync receipt timeout (3 times 125 ms);
  - a `tu` holdover of at least 0.25 s.

  The bound has to be stated before step 3 can pass or fail.
- **B3. The switch's firmware identity is not readable.** It has no AVDECC entity and no management path. Its Announce fields above are its only recorded identity.
- **B4. Hive needs an interactive desktop session on the controller host.**

## Raw artifacts

Raw artifacts are kept in the private bench packet `117-a200-packet`, with a
per-file SHA-256 manifest. The primary ones:

| Artifact | SHA-256 |
|---|---|
| identity console transcript | `60bdd7d3f54db8bc7aa3c58a0670cb5a0ae21bef0324ff0ff0045e7f47f22dd1` |
| identity grader transcript | `0aad30446e7e71427f59860152c0cac5e73f32b80c56bb372e324582d858ee51` |
| reference CRC table (three seeds and the replaced image) | `c8916b01af28e1682bd03b153ddf546079dd0123a412fe48f0adc6d97c778f92` |
| Run A tap capture | `26c4529a7d0dd4e335af3073aa8080072dfbb4642042c5de66f487fafb56fc43` |
| Run A console transcript | `4118f0fb3082b96d3454d2fff01ae2724d442ebf0bdbae001c40f2fcb7136232` |
| Run A controller poll | `33478b3a9cfbaec9964153be0d83524c12cba896131b01027164177a59f7ec0b` |
| Run A Pdelay turnaround output | `5082dcfadc74dfb4c4ee2db5bef386f2599f47113b851571256145fcfa9f469f` |
| Run B tap capture | `febe8a1643e88c5b0b12eb3f0fa837b17e9330fcb5cd33998c7a9b30701d029b` |
| Run B console transcript | `d956745df61c4423f3f13e8e73fce66bcf2d4fa0db8dab73df3667f00ae64ed9` |
| Run B bind window log | `392307147da1a8a7edc1727578d43abdec2523fa6c204e93c11adca89d05bdf1` |
| Run C tap capture | `f07b7230a8535d470168d5c0547561d69b3cf353982035e8d93baa57493aa80c` |
| Run C counters probe, DUT | `f1ffd611d3562a6d923a964328af054b7d55472a2c581cfa5d67e80ea9d9c6cc` |
| Run C counters probe, reference peer | `3ab650224f321d2347523babd8cbd9f67fbd8b81fd121ee3da27963cf1b5c2a2` |
| Run C enumeration log | `bdb4e3b253e5bfa1e54744a590187e043d7078a4abbd3464d777bef3018f6cd5` |
| Run C DUT entity model dump | `be48dca9d507922adc72fab0bebebd1c69c65af035aa3eb66fabd7eb4b601d1e` |
| DUT stream counters, raw | `9847b8e1d55ec85dccb0b08aa53c88f70c2e6b872bd946579448a4cb5d0e0d25` |
| final tap capture | `66ad849afd8be73ecf15a97e97bdbcdc16264e357e23eff5a890081b5685d54c` |
| final console transcript | `a9ba578178a7224f007b2ed96a2a6c522bba0e63013eada386077b51dae72861` |
| final grader transcript | `25bc03e190d4781b95794d540cf15d443f264f22a22645b77058d6f8754a0af5` |
| binding census, start | `fdc55f2fee850484661703a24a0137d814140755ab5e542ad22e2c8c79ea5911` |
| binding census, end | `1a0e025cc565e48e2bc2bc47df272f406e52cf85d622fb4dfcfdf6ec07d3acbf` |
