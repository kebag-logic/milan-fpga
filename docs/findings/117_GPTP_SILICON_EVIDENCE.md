<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# gPTP silicon evidence for issue 117: one AX7101 against the reference peer

*Measured on 2026-09-23 on the AX7101 flashed with the dev `ede8d48e` image
at 12:35 UTC. Owning issue:
[#117](https://github.com/kebag-logic/milan-fpga/issues/117), under
[#110](https://github.com/kebag-logic/milan-fpga/issues/110); it gates the
physical acceptance of [#116](https://github.com/kebag-logic/milan-fpga/issues/116).
Bench steps 2, 4 and the controller part of step 5 ran between 12:41 and
13:14 UTC. Step 3 (grandmaster loss and return) and the grandmaster-change
half of step 4 ran between 13:44 and 14:13 UTC, after the owner authorized
power-cycling the bench switch and fixed the recovery bound
([decisions](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795898094)).
Audio continuity is deferred to 2026-12-31 and is not measured here.*

## Contents

- **[Result per acceptance box](#result-per-acceptance-box)** -- PASS, FAIL or NOT RUN for every part of the five acceptance boxes, and why the asCapable partner is the bench switch.
- **[Candidate image and identity proof](#candidate-image-and-identity-proof)** -- The exact build, its artifact hashes, and the console CRC readback that proves the board runs it.
- **[Topology and capture points](#topology-and-capture-points)** -- Who is grandmaster, where the reference peer and the controller host sit, the peer's firmware identity, the power-strip outlets, and what the tap records.
- **[Methodology](#methodology)** -- Each run's window, what it exercised, how long it held the bench lock, how CSRs were read, and how step 3 puts four clocks on one timeline.
- **[Tool revisions](#tool-revisions)** -- Revisions and hashes of every script, library and capture tool used.
- **[Step 2: asCapable, cadence and turnaround](#step-2-ascapable-cadence-and-turnaround)** -- Sync, Announce and Pdelay cadence, the Pdelay turnaround in both directions, and the asCapable retention record.
- **[Step 3: GM loss and return](#step-3-gm-loss-and-return)** -- Six switch power cycles: the proof that OUT4 is the switch, loss declaration, the DUT as its own grandmaster, recovery against the 5 s bound, the reference peer, and the stream.
- **[Step 4: publication CSRs and tu against the wire](#step-4-publication-csrs-and-tu-against-the-wire)** -- Every publication word set beside the wire and the controller view, the `tu` bit on 34,061 CRF PDUs, and the same words through six grandmaster losses and returns.
- **[Step 5: controller discovery and enumeration](#step-5-controller-discovery-and-enumeration)** -- Counters-probe parity with the reference peer, and the la_avdecc enumeration that downgrades the DUT from Milan.
- **[Observations outside the acceptance boxes](#observations-outside-the-acceptance-boxes)** -- Measured behavior no box covers: CRF talker bursts, stream counters, notification rate, the switch's Pdelay and timescale, link counters, ADP, and the reference peer.
- **[Bench state restored](#bench-state-restored)** -- The before-and-after censuses and outlet reads proving no binding, peer setting or outlet was left changed.
- **[Owner blockers](#owner-blockers)** -- The two decisions step 3 needed, both made on 2026-09-23, and the two blockers that remain.
- **[Raw artifacts](#raw-artifacts)** -- SHA-256 of the primary raw captures, transcripts and logs in the two private packets.

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
| 2. GM loss and return recover automatically within the documented bound | DUT recovery after the switch returns, six switch power cycles | PASS: asCapable, sync and `tu` clear 0.43 to 1.60 s after the switch's first post-boot Announce, against the [5 s bound](../design/GM_LOSS_RECOVERY.md#recovery-bound); see [Step 3](#step-3-gm-loss-and-return) |
| | automatic | PASS: no operator action reached the DUT beyond read-only AECP queries; no CSR write, no reset, and `RST_EPOCH` read 1 throughout |
| | resulting stream state | PASS: with a CRF binding held through cycles 4 to 6, the stream restarted once after each return with `tu` clear, and the listener locked again |
| | reference peer's recovery against the bound | NOT RUN: the peer's own link is not tapped, so the switch's return on it has no time; the controller view is recorded |
| 3. Publication words and `tu` are fabric-owned on the booted image | steady state against the wire | PASS: every word agrees with the wire and with the controller view |
| | transition (GM change, sync loss) | PASS: over six losses and returns every publication word moved with the wire, inside one 0.1 s console sample; see [Step 4](#grandmaster-change-across-the-loss-and-return) |
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

The identity gate ran again before step 3, 13:44:58 to 13:45:22 UTC, with the
same read-only commands. The board read ROM `f6afa4ec`, QSPI payload
`02036e95` and AEM `93742dd2`, with `VERSION=00020060`, and the grader passed
10 of 10. The reference CRC table was recomputed from the four build
directories and is byte-identical to the one above. `origin/dev` was still
`ede8d48e`. The grader passed 10 of 10 again at 14:13 UTC, after the last
cycle.

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
- **Power.** The bench power strip feeds the switch from outlet OUT4, the DUT from OUT0 and the reference peer from OUT2, per the 2026-08-15 outlet map. Step 3 switched OUT4 only, and its first cycle proved that OUT4 is the switch; see [Step 3](#step-3-gm-loss-and-return). The strip read OUT0, OUT1, OUT2, OUT4, OUT5 and OUT6 on and OUT3 off before and after step 3.
- **Second observation point (step 3).** The controller host's own AVB port on switch port 8. Its carrier is the switch's link edge, and a capture of that port is in the packet. It is inside the partition while the switch is off.
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
| Identity 2 | 13:44:58 to 13:45:22 | console CRC readback, UART grader | lock held 24 s |
| Outlets, start | 13:45:31 | power-strip status read | lock held 0.5 s |
| Census, start | 13:50:59 | binding and settings census, both AVB_INTERFACE counter blocks | no lock (no console) |
| Attempt 1 (aborted) | 13:51:23 to 13:52:04 | a cycle whose console poller failed to start; the guard turned OUT4 back on after 6 s; not counted, see [Step 3](#step-3-gm-loss-and-return) | lock held 41 s |
| Poll check | 13:52:59 to 13:53:04 | 5 s console poll at 0.1 s, liveness check; no power action | lock held 5 s |
| Cycles 1 to 6 | 13:53:17 to 14:12:05 | each: tap capture, controller-host capture and watcher, 0.1 s console poll, OUT4 off for 20 s then on; cycles 4 to 6 hold a CRF binding | lock held 160 s (cycle 1), 120 s (2, 3), 125 s (4 to 6), released between cycles |
| Outlets, end | 14:12:29 | power-strip status read | lock held 0.5 s |
| Census, end | 14:12:30 | binding and settings census | no lock (no console) |
| Final 2 | 14:13:19 | 22 s tap capture; console read; UART grader | lock held 0.5 s |

**Step 3 cycle.** One script runs each cycle in the foreground; every remote
process is bounded by a timeout and is stopped explicitly at the end.

- The tap records the DUT link, and the controller host records its own port.
- A watcher on the controller host logs the carrier every 0.1 s and every ADP advertisement heard. While the carrier is up it polls, once a second, GET_AVB_INFO, GET_AS_PATH and the AVB_INTERFACE counters of the DUT and of the peer.
- In cycles 4 to 6 the watcher also binds the peer's primary CRF input (Stream Input 8) to the DUT's CRF output (Stream Output 1) 28 s before the outage, polls both stream counter blocks and the ACMP state, and unbinds about 110 s after it. It refuses to bind unless the input reads unbound, and it retries the unbind until the input reads unbound.
- Under the bench lock the console is polled every 0.1 s: `milan_status` plus `CLKV_TUCNT`, `LINKG_STAT` and `RST_EPOCH`, and in cycles 4 to 6 `CRFT_CTRL` and `CRFT_COUNT`.
- After 20 s (25 s with the binding) a guard confirms that the console transcript is still growing. Only then does the power-strip host run one sequence: status, OUT4 off, 20 s, OUT4 on, status. That sequence is started under `nohup`, so the "on" half runs even if the build box loses the session.
- In cycle 1 the guard checked the DUT console again 6 s after the off, ready to turn OUT4 back on at once.

**Timebase.** The build box is not NTP-synchronized. Before and after every
cycle, 25 bracketed time exchanges over one session to each of the capture
server, the controller host and the power-strip host measured it 1.080 to
1.085 s behind them. The best round trips were 0.2 to 0.4 ms, and the three
NTP-synchronized hosts agreed within 1.5 ms. Tap records are placed on the
capture server's clock by a straight line through the per-5 s minima of pcap
host time minus tap time; the residual of the kept minima is at most 2.0 ms.
All step 3 times are seconds after that cycle's outlet-off command on the
build-box clock. A console sample carries its command's send time; a
transition lies between two samples about 0.10 s apart, and the tables give
the later one.

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
| Step 3 reused unchanged | `console_read.py` `652d6f83...`, `console_poll.py` `3a0de7d8...`, `avdecc_ro.py` `17283696...`, `wire_summary.py` `c5039d95...`, `expected_crc.py` `04d128bb...` |
| Step 3 cycle | `run_cycle.sh` `45889a7d...`, `cycle_locked.sh` `c4ef8c9a...`, `powerstrip_cycle.sh` `b2f1593e...` (the power-strip host side), `console_alive.py` `644bcfb8...` (the guard) |
| Step 3 controller host | `a202_watch.py` `48c248b2...` (carrier, ADP, AECP polls, the bounded CRF binding), `census.sh` `d7912881...` |
| Step 3 timebase and analysis | `clock_offset.py` `950533ca...`, `analyze_cycle.py` `bdd228a1...`, `summarize.py` `d6f53575...`, `census_compare.py` `40424c61...` |

Full hashes are in the packet manifests listed under
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

**PASS against the 5 s bound in six of six cycles, worst case 1.60 s.** The
bench switch is the grandmaster, so switching off its outlet removes the
grandmaster from every end station at once, and switching it on is the
return. The owner authorized that on 2026-09-23 and fixed the
[recovery bound](../design/GM_LOSS_RECOVERY.md#recovery-bound): 5 s from the
grandmaster's return to asCapable and sync, with media recovering within one
further stream restart. Each cycle held the outlet off for 20 s, far past the
3 s announce receipt timeout. Nothing was written to the DUT, and no
priority1 was touched.

The baseline is the Step 2 record: Sync at 125 ms, Announce and Pdelay at
1 s, GM `3cc0c6fffefe0210`, peer delay 380 to 391 ns. Before every cycle the
console read that GM with `SYNC=1 ASCAPABLE=1 TU=0` in every sample.

### OUT4 is the switch

Cycle 1 was the proof, and no other cycle ran before it passed.

| Check | Cycle 1 result |
|---|---|
| The grandmaster disappears when OUT4 goes off | The switch's last frame on the DUT link came 0.73 s after the off command, and nothing came from it again until 38.24 s. The controller host's port lost carrier at 1.12 s. The DUT lost sync at 1.16 s and replaced the switch's identity with its own at 3.56 s. |
| The DUT keeps power | The console answered 6 s after the off (the guard's check), and 1,600 samples show a largest gap of 0.106 s. `RST_EPOCH` read 1 throughout. |
| The reference peer keeps power | Its ADP available_index went on counting (5866 to 5895), and its GPTP_GM_CHANGED counter from 3 to 5. A restart resets both. |
| Nothing else changes | With OUT4 off, the strip read OUT0, OUT1, OUT2, OUT5 and OUT6 on and OUT3 off. The capture server and the controller host stayed reachable over the management network. |

### Attempt 1, aborted and not counted

At 13:51:43 UTC a first attempt switched OUT4 off with no console record. The
operator had not copied the console poller into the packet, so it exited at
once. The guard found no transcript 6 s later and switched OUT4 back on after
5.95 s off. The controller host's port lost carrier 1.14 s after the off and
regained it 13.7 s after the early "on". The controller's first successful
poll, about 4 s later, found the DUT naming itself as grandmaster with
asCapable clear; the poll 2 s after that found the switch, with asCapable
set. The poller was then added, a pre-flight check now refuses
any power action until the console transcript is growing, and a 5 s poll
check passed before cycle 1. The partial artifacts are in the packet.

### Per-cycle record

Seconds after the outlet-off command. "Recovery" is DUT all-good minus the
switch's first post-boot Announce or Sync on the DUT link, whichever came
first; in every cycle that was the Announce (in cycle 5 both came together).
"All-good" is the first console sample from which GM = the switch, `SYNC=1`,
`ASCAPABLE=1` and `TU=0` hold in every later sample; the sample 0.10 s before
it did not.

| Cycle | CRF binding | Off for | DUT sync 0, `tu` 1 | DUT GM = itself | DUT asCapable 0 | Switch first frame | Switch first Announce | DUT asCapable 1 | DUT GM = switch | DUT all-good | Recovery | 5 s bound |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | no | 20.29 | 1.16 | 3.56 | 5.66 | 38.24 | 39.95 | 39.66 | 39.96 | 40.46 | **0.51** | PASS |
| 2 | no | 20.40 | 1.08 | 3.48 | 4.78 | 37.75 | 39.06 | 38.78 | 39.08 | 39.58 | **0.52** | PASS |
| 3 | no | 20.39 | 1.08 | 2.88 | 5.48 | 38.07 | 39.07 | 39.48 | 40.08 | 40.58 | **1.51** | PASS |
| 4 | yes | 20.29 | 1.17 | 3.66 | 4.91 | 38.57 | 40.00 | 39.91 | 40.01 | 40.42 | **0.43** | PASS |
| 5 | yes | 20.40 | 1.09 | 2.96 | 5.75 | 38.07 | 39.07 | 39.71 | 40.12 | 40.54 | **1.46** | PASS |
| 6 | yes | 20.40 | 1.06 | 3.24 | 5.62 | 38.12 | 39.12 | 39.68 | 40.20 | 40.72 | **1.60** | PASS |

- Measured from the switch's first Sync instead, recovery is the same or up to 0.02 s shorter.
- The switch's boot dominates the outage. From the "on" command to DUT all-good took 19.18 to 20.32 s, and from the switch's first frame on the DUT link 1.83 to 2.60 s.

### Loss declaration

- **DUT**, every cycle, from the console:
  - Sync lost and `tu` set 0.40 to 0.46 s after the switch's last Sync on the wire, with `CLKV_STAT` bit 3 (holdover) for 0.3 s. The sample before read sync, so the edge lies 0.30 to 0.46 s after that Sync, around the 375 ms sync receipt timeout.
  - GM identity replaced by its own, `020000fffe000001`, 3.01 to 3.08 s after the switch's last Announce, the 3 s announce receipt timeout. The parent followed, the path generation advanced by one, and the path count stayed 1.
  - asCapable cleared 5.0 to 5.1 s after the last Pdelay response the DUT received.
- **Reference peer**: not observable while the switch is off. Its link is not tapped, and the controller host is inside the partition. Its GPTP_GM_CHANGED counter advanced by 2 in every cycle. In cycles 2 and 3 it still named its own clock, `3cc0c6fffe010203`, as grandmaster after the return: in GET_AVB_INFO at 38.16 and 38.15 s, and in ADP at 39.84 and 41.65 s.

### While the grandmaster is absent

The DUT becomes its own grandmaster. With priority1 248 and no other
time-aware system reachable, best-master selection picks its own clock, and
the fabric plane publishes that choice while keeping sync false and `tu` set.
In all six cycles, from the identity change until the switch returned:

- GM and parent read `020000fffe000001`, path count 1. The first reachable GET_AS_PATH read `[020000fffe000001]`.
- `SYNC=0`, `ASCAPABLE=0` from about 5 s, `TU=1`, holdover clear, and `CLKV_TUCNT` rising by one a second.
- `LINKG_STAT` went from `0x83` to `0x03` 2.73 s after the last received frame (RX activity clear, both clocks alive), and back to `0x83` within one sample of the first frame after the return. `RST_EPOCH` stayed 1.
- The switch's last frame reached the DUT link 0.63 to 0.73 s after the off. The tap then recorded nothing in either direction from 1.03 to 1.71 s until 37.55 to 38.57 s.
- When the link returned the DUT acted as master from becoming asCapable until it adopted the switch, 0.1 to 0.6 s later. In that window it sent 1 to 4 Sync and Follow_Up pairs as master in every cycle. In cycles 3 and 5 it also sent one Announce naming itself as grandmaster, priority1 248. The switch's Announce, priority1 246, then made its port a slave.

### Return and recovery

- **The switch.** Its port 8 regained carrier 13.6 to 13.8 s after the "on" command. It forwarded its first frame onto the DUT link 3.7 to 4.5 s after that, answered Pdelay at once, and sent its first Announce 1.0 to 1.7 s later, with its first Sync 0 to 18 ms behind.
- **Which Announce the DUT takes.**
  - In cycles 1, 2 and 4 the DUT was asCapable before the switch's first Announce, and adopted the switch 9 to 20 ms after that Announce on the wire.
  - In cycles 3, 5 and 6 the first Announce came 0.41 to 0.64 s before asCapable. The DUT adopted the switch on the next Announce, 1.007 s later, within one console sample.
  - That one announce interval separates the 0.43 to 0.52 s group from the 1.46 to 1.60 s group.
- **After adoption.** The holdover bit set and the PHC stepped (Observation 7). Sync followed 0 to 0.2 s later, and `tu` cleared 0.41 to 0.52 s after adoption, which is the holdover of at least 0.25 s.
- **Counters.** GPTP_GM_CHANGED advanced by exactly 2 per cycle on the DUT, to itself and back, matching the two identity edges in the CSR. LINK_UP and LINK_DOWN did not move (Observation 8).

### Reference peer

Controller view only; the peer's link is not tapped.

| Cycle | First reachable poll after the return | Peer names the switch as grandmaster | GPTP_GM_CHANGED |
|---|---|---|---|
| 1 | 38.23 s: the switch, asCapable | 38.23 s | +2 |
| 2 | 38.16 s: itself, asCapable | 46.66 s (ADP 46.62 s) | +2 |
| 3 | 38.15 s: itself, asCapable | 46.65 s (ADP 46.82 s) | +2 |
| 4 | 38.80 s: the switch, asCapable | 38.80 s | +2 |
| 5 | 38.15 s: the switch, asCapable | 38.15 s | +2 |
| 6 | 38.64 s: the switch, asCapable | 38.64 s | +2 |

In four cycles the peer already named the switch before the switch's first
Announce reached the DUT link. In cycles 2 and 3 it did so 7.6 s after that
Announce (Observation 11). When the switch's Announce reached the peer's own
link is not recorded, so its recovery time against the bound is NOT RUN. Its
AS path returned to `[3cc0c6fffefe0210, 3cc0c6fffe010203]` every time. Its
available_index counted on through every cycle (5843 at the start census,
6067 at the end), so it never restarted.

### Stream and media state (cycles 4 to 6)

The binding, peer Stream Input 8 from DUT Stream Output 1, was made 28 s
before each outage and held through it. Every ACMP read of the listener named
the DUT as talker with connection count 1, and nothing re-bound it. The peer's
clock source stayed INTERNAL, as in Run B.

| Phase | DUT: console and wire | Reference peer: controller |
|---|---|---|
| Before | Licensed, `CRFT_CTRL` `0x3002E3`. CRF at 500 PDU/s with `tu=0`, in the 15 s bursts of #530. | MEDIA_LOCKED, FRAMES_RX counting |
| Loss | First `tu=1` PDU at 1.08, 1.07 and 1.00 s, each inside the console interval where `CLKV_STAT[0]` rose (1.06 to 1.17, 0.99 to 1.09 and 0.96 to 1.06 s). Then 316, 293 and 243 PDUs with `tu=1` until emission ended with the link at 1.71, 1.65 and 1.49 s. The licence dropped (`CRFT_CTRL` `0x3`) at 2.21, 5.23 and 1.89 s. | unreachable |
| Absent | Idle, no emission. | unreachable; the binding was retained |
| Return | Relicensed at 41.25, 42.92 and 41.45 s, 0.83, 2.38 and 0.72 s after the DUT was all-good. The first PDU, at 41.28, 42.96 and 41.46 s, and every later one carried `tu=0`. STREAM_START +1. | First poll, 38.2 to 38.8 s: MEDIA_UNLOCKED and STREAM_INTERRUPTED counted once, FRAMES_RX frozen. The ACMP talker-registration failure flag (`0x0040`) was set once, at 41.6 to 41.8 s in cycles 4 and 6, and clear 3 s later. MEDIA_LOCKED again at the polls at 44.80, 43.16 and 44.64 s. |
| After | The same 15 s bursts. | Locked in each burst |

Media verdict: PASS. Each return cost exactly one stream restart. The first
PDU after it already carried `tu=0`, and the listener locked by the next poll.

### Verdict

- DUT recovery: PASS in six of six cycles, 0.43 to 1.60 s against the 5 s bound.
- Automatic: PASS. The DUT received read-only AECP queries only: no CSR write, no reset, no gPTP setting.
- Media: PASS, one stream restart per return.
- Reference peer's recovery time: NOT RUN; the switch's return on the peer's link is not observable on this bench.

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
- **Transition.** The steady state above is one half. The grandmaster-change half, `tu` asserting on sync loss and the publication following each new grandmaster, is below.

### Grandmaster change across the loss and return

The same words, read every 0.1 s through the six step 3 cycles, set beside
the tap on the DUT link and the controller host's AECP and ADP view. Times
are seconds after the outlet-off command, as in
[Step 3](#step-3-gm-loss-and-return).

| Transition | Console CSR | Wire | Controller |
|---|---|---|---|
| Sync loss | `CLKV_STAT` sync 0, `tu` 1 and holdover (bit 3) set, 0.40 to 0.46 s after the switch's last Sync | the switch's last Sync; in cycles 4 to 6 the first CRF PDU with `tu=1` falls inside the console interval where `CLKV_STAT[0]` rose | inside the partition |
| Grandmaster loss | `0x624`/`0x628` and `0x730`/`0x734` read `020000fffe000001` 3.01 to 3.08 s after the switch's last Announce; `ASP_CMD` generation +1, count 1 | the switch's last Announce; the DUT sent no ADPDU while its link was dark | the first reachable GET_AVB_INFO, every cycle, names `020000fffe000001` with AS_CAPABLE clear; GET_AS_PATH `[020000fffe000001]` |
| asCapable loss | `CLKV_STAT[16]` 0 at 5.0 to 5.1 s after the last Pdelay response the DUT received | that response | AS_CAPABLE clear at the first reachable poll |
| asCapable return | `CLKV_STAT[16]` 1 at 38.78 to 39.91 s | after the DUT's first Pdelay exchanges with the switch | AS_CAPABLE set while GM is still `020000fffe000001`, seen in cycles 1, 3 and 6 |
| Grandmaster return | GM and parent read `3cc0c6fffefe0210` within one sample of the Announce the DUT accepted (0 to 74 ms after it); generation +1, count 1; holdover set | Announce from `3cc0c6fffefe0210`, priority1 246, PathTrace `[3cc0c6fffefe0210]` | GET_AVB_INFO names the switch at the next poll; GET_AS_PATH `[3cc0c6fffefe0210]`; GPTP_GM_CHANGED +2 per cycle, one per identity edge in the CSR; the DUT's next ADPDU names the switch, 0.54 to 2.56 s after adoption |
| `tu` clear | `CLKV_STAT[0]` 0 at 0.41 to 0.52 s after adoption | in cycles 4 to 6 emission resumes only after that, every PDU with `tu=0` | Stream Output 1 TIMESTAMP_UNCERTAIN had counted the loss (2, 5 and 2) |
| `tu` intervals | `CLKV_TUCNT` +40, +39, +41, +40, +40 and +41: the 1 s intervals of a 38.5 to 39.7 s span with `tu=1` | none | not served |

- **Fabric-owned in transition.**
  - Each identity edge in the CSRs matched the wire's timeout or the accepted Announce within one console sample.
  - The controller view agreed at its next poll.
  - The `tu` bit on the wire agreed with `CLKV_STAT[0]` at the loss edge and after the return.
  - Nothing wrote to the DUT.
- **Limit.** The wire shows `tu=1` only at the loss edge. The stream stops with the link and restarts after `tu` has cleared, so no return-edge `tu` transition reaches the wire. The loss edge is bounded by the 0.1 s console interval, not better.

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

These are measured facts that no acceptance box of #117 covers. Items 1 to 6
each need their own issue; none is assigned a cause here.

1. **The DUT's CRF talker ends its own bursts while the listener stays bound.** Run B has four bursts: 19.67 s, 18.45 s, 15.00 s and 15.00 s. At each end the DUT stops emitting, sends an MSRP TalkerAdvertise Leave 10 to 166 ms later, and the switch withdraws the Listener about 2 ms after that. The reference listener then re-probes (ACMP CONNECT_TX) and emission resumes 0.3 to 0.7 ms after the DUT's probe response. The pauses last 1,106 ms, 578 ms and 148 ms, with no sequence gap. Three of the four ends fall 15.00 s (plus or minus 2 ms) after the latest successful probe response. That includes the last, which came 9.95 s after the unbind had already withdrawn the Listener.
2. **The first CRF burst started before any reservation existed.** The DUT answered the first probe with TALKER_DEST_MAC_FAIL (status 3) and began emitting 0.18 ms later. The first Listener Ready reached it 4.7 s after that.
3. **Stream Output 1 FRAMES_TX reads 16.** The wire and `CRFT_COUNT` both show 34,061 PDUs. STREAM_START and STREAM_STOP (4 each) and TIMESTAMP_UNCERTAIN (0) do agree with the wire.
4. **The DUT sends one unsolicited GET_AVB_INFO per second to a registered controller.** Each carries a propagation delay a few nanoseconds away from the last: 33 in 40 s, with no two consecutive values equal. This is the documented design (register map, `VERSION` `0x0055` notes), recorded here for controller-load review.
5. **The bench AVB switch requests an IPv4 address by DHCP every 15 s on the AVB segment, and nothing answers.**
6. **The bench AVB switch answered two of the DUT's Pdelay requests after 18.33 and 18.36 ms (Run A).** That is over the 15 ms limit on its side. Its other 568 answers took at most 0.88 ms. The DUT completed both exchanges, and its published peer delay did not move outside 380 to 391 ns.

Items 7 to 12 come from the step 3 cycles. Items 8 to 10 concern the DUT and
each need their own issue, with no cause assigned. Items 7, 11 and 12 are
facts about the switch or the reference peer: they bound what the evidence
can show rather than asking for DUT work.

7. **The switch's gPTP time restarts from the same origin at every power-on.** Each return stepped the DUT's PHC by minus the time since the switch's previous power-on: -128.5, -355.9, -163.3, -154.5, -180.3 and -154.1 s. Each equals the interval between the two "on" commands within 0.04 s. The holdover and `tu` covered every step.
8. **Neither end station's AVB_INTERFACE LINK_UP or LINK_DOWN counter moved over seven switch outages.** The DUT read 1 and 0, and the peer 1 and 0, at both censuses, while GPTP_GM_CHANGED advanced by 14 on both. The tap showed the DUT link silent for 36 to 37 s each time; whether the DUT's PHY link dropped is not recorded.
9. **The DUT's Stream Output 1 TIMESTAMP_UNCERTAIN and FRAMES_TX restart at each STREAM_START.** TIMESTAMP_UNCERTAIN read 2, 5 and 2 after the three bound losses and 0 after the next STREAM_START. FRAMES_TX rose by one per 1 s poll during emission and returned to 0 at each STREAM_START. STREAM_START and STREAM_STOP kept counting, from 4 at the start census to 25 at the end. This extends item 3.
10. **The DUT never put its own identity on the wire in an ADPDU.** While it was its own grandmaster its link was dark, except for the 1.3 to 2.1 s between the link's return and its adoption of the switch, in which it sent no ADPDU. Its first ADPDU after each return already named the switch, 0.54 to 2.56 s after the adoption. This is recorded for the re-advertise-on-change path.
11. **In cycles 2 and 3 the reference peer named itself as grandmaster until 46.6 s, 7.6 s after the switch's first Announce reached the DUT link.** In the other four cycles it named the switch at its first reachable poll, before that Announce. The switch's Announce onto the peer's own link is not tapped, so this is not a recovery time.
12. **The reference peer resets its Stream Input counters when bound, and MEDIA_LOCKED, MEDIA_UNLOCKED and STREAM_INTERRUPTED again at each stream restart.** Each bind started the block at 0. In every bound cycle those three counters returned to 0 at the restart after the return, while FRAMES_RX kept counting. Its stream counters therefore cannot show a peer restart; its available_index and GPTP_GM_CHANGED do.

The Run B timeline with tap-clock times is in the packet (`stream-timeline.txt`).

## Bench state restored

- **Bindings.** The binding census after the runs matches the one before them for all 18 states read: peer Stream Inputs 0 to 9, peer Stream Outputs 0 to 3, DUT Stream Inputs 0 and 1, and DUT Stream Outputs 0 and 1. All are unbound, with connection count 0.
- **Peer settings.** Configuration 0, sampling rate 96 kHz, clock source 0 (INTERNAL), CRF input format `041060010000bb80`, the same firmware hash and the same descriptor bytes. The only difference is the reserved half-word ahead of each descriptor, which the peer fills with varying values.
- **Run B cleanup.** The Run B unbind succeeded on its first attempt. The DUT's `CRFT_CTRL` returned to `0x3`, and the final capture carries no AVTP stream.
- **DUT.** 10 of 10 on the grader at 13:13 UTC, same GM, `CLKV_STAT` `0x00010002`, drop counters 0, `LINKG_STAT` `0x83`, `RST_EPOCH` 1.
- **Hosts.** The multicast memberships ended with their processes. Every temporary file on the controller host and the capture server was copied, verified by SHA-256, and removed. No capture or probe process remains, and the bench lock is free.
- **Not touched.** Flash, JTAG, power, wiring and instruments were not touched.

### After step 3

- **Outlets.** The power strip read OUT0, OUT1, OUT2, OUT4, OUT5 and OUT6 on and OUT3 off at 13:45 and again at 14:12 UTC, as found. Only OUT4 was switched: seven times off, seven times on (attempt 1 and cycles 1 to 6).
- **Bindings.** The end census matches the start census for all 18 ACMP states: every input unbound, connection count 0. Each of the three CRF bindings unbound on its first attempt, about 110 s after its outage.
- **Peer settings.** The 15 settings reads of both entities match: configuration 0, 96 kHz, clock source 0 (INTERNAL), both stream formats, and the ENTITY and six stream descriptors. The only difference is the reserved half-word after `configuration_index`, which the peer varies (as above).
- **Counters that moved, as expected.** GPTP_GM_CHANGED rose by 14 on the DUT and on the peer's interface 0. The DUT's Stream Output 1 STREAM_START and STREAM_STOP went from 4 to 25. The peer's available_index went from 5843 to 6067.
- **DUT.** The grader passed 10 of 10 at 14:13 UTC. The console read the switch as grandmaster, `CLKV_STAT` `0x00010002`, `CRFT_CTRL` `0x3`, drop counters 0, `CTLR_DIAG` 0, `LINKG_STAT` `0x83` and `RST_EPOCH` 1. A 22 s tap capture around that read carried no AVTP stream.
- **Hosts.** The watcher, census and power-strip scripts were removed from the controller host and the power-strip host; the captures were copied, their SHA-256 checked against the remote copy, and removed. No process of the runs remains, and the bench lock is free.
- **Not touched.** Flash, JTAG, wiring, instruments and every outlet but OUT4.

## Owner blockers

- **B1. No permitted way to induce GM loss and return.** RESOLVED on 2026-09-23: the owner [authorized](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795898094) power-cycling the switch's outlet under the bench lock, which is the repository's own procedure, the physical checklist entry `phys.switch-cycle.gm-partition` of [`tb/tools/torture_campaign.py`](../../tb/tools/torture_campaign.py). Step 3 ran that way. The facts that made it a blocker still hold:
  - The grandmaster is the bench AVB switch, not the reference peer. The peer is a slave in the same domain.
  - The peer's AEM exposes a single CONTROL, IDENTIFY (control type `90E0F00000000001`). AVDECC defines no command that changes gPTP priority.
  - The switch has no AVDECC entity and no address on the AVB segment, and no management path or credentials are provisioned on any bench host.
- **B2. No numeric recovery bound is documented.** RESOLVED on 2026-09-23: the owner fixed 5 s from the grandmaster's return to asCapable and sync, with media recovering within one further stream restart. It is recorded with its derivation in [GM loss and recovery](../design/GM_LOSS_RECOVERY.md#recovery-bound).
- **B3. The switch's firmware identity is not readable.** It has no AVDECC entity and no management path. Its Announce fields above are its only recorded identity.
- **B4. Hive needs an interactive desktop session on the controller host.**

## Raw artifacts

Raw artifacts are kept in two private bench packets, each with a per-file
SHA-256 manifest. The primary ones for steps 2, 4 (steady state) and 5, in
`117-a200-packet`:

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

The primary ones for step 3 and the grandmaster-change half of step 4, in
`117-a202-packet`:

| Artifact | SHA-256 |
|---|---|
| identity 2 console transcript | `caa36a384cdf2e6ea7b0cad380cabd5ec1387cd2c520765d532d7cc2142bc00e` |
| identity 2 grader transcript | `7538e887a1373ca9d44e8d2b1fac86f24485d8cb154ecd44dc92ea2e87d9b5ac` |
| reference CRC table, recomputed (byte-identical to the one above) | `c8916b01af28e1682bd03b153ddf546079dd0123a412fe48f0adc6d97c778f92` |
| power-strip status, start | `4c1d74f395c8c1e4000156c24d0c3a9f20dbe80bc0fe9c0429aa07d2594e140d` |
| power-strip status, end | `070bf31964d5c263e0792806a867dd38febf0f7c261feed36d104c52a7caf9e9` |
| binding and settings census, start | `cb185107bd2eb26d71dea220cb694f621cef6d6965fd20e98e42a80572cb495a` |
| binding and settings census, end | `c45572d9502dcc8b69a70b764a1d9db9fe7b38fb81aed0f863d2f3f95ee6544a` |
| census comparison | `2dfecb1baea1d9f5fd906df20819da21ac8c7bfede2073a8f447263fde5dcd6b` |
| attempt 1: power-strip log | `dec14c0b01b9b26cb142c1c56dac9e9195838a7874630597ef0efab8bb0e49e8` |
| attempt 1: lock log | `909699f5d1aeb001b046e91a4903b818f9ca3238e1dbf629eaebc734be649654` |
| attempt 1: controller-host watcher | `f6f0ecf0f799e4e28992f1b5f4e1bbb25bf1cae29c7c99960be27d970454618f` |
| attempt 1: tap capture | `7f4b2bd3cbad5d7bdf7bc5297c7eb761da855209bd7d416758e7a173ab82b83e` |
| cycle 1: tap capture | `b154802f6dbede16219ff8eab109aea54ec4610888660776ea2adadad2e79f8e` |
| cycle 1: console transcript | `59d7dd4f0ed449c8d0178779975704549aede9c7722318faced754ede821a001` |
| cycle 1: controller-host watcher | `42e0fb537a546528ae3683fd816da967ade6de42b378799e59f4bf23e405b132` |
| cycle 1: controller-host port capture | `3212ffc4543efb0f2853fd9660ceb1659f6606c932a743dc40b7c775d76f207e` |
| cycle 1: power-strip log | `2e97281d5c93946f43d00caf583161402aa4228cac3f472b1ec4a031a6d498fe` |
| cycle 1: analysis | `cdbdc542aa481f63d6c75b9b71a83254835e977d7709efd37f9625df8d91963c` |
| cycle 2: tap capture | `1e892cf350e6e88996e65b9a6d7a000d655bc6fc652cac907cb076a153e4409b` |
| cycle 2: console transcript | `b913fc92e0d3cdb215a189f7c88a200cdb3f883846fcf7c5c11470bef63a9bb3` |
| cycle 2: controller-host watcher | `209781f6cfd339ab2e86debcd8698d256ff03f4505cdb65caf3a5381e37ba3cd` |
| cycle 2: controller-host port capture | `ff9e16f2090c724819ae5289eb6959ae84370a43e46bf9eb46cecc21ca429f9f` |
| cycle 2: power-strip log | `be0725f7463646a42ea7bc7cb384a5880a03fd72ad53586158dd74a2f1f6b7fc` |
| cycle 2: analysis | `b36027bcc88ba30e7d83a934c3bb27439ae689367dc6f4906304765ee2bde641` |
| cycle 3: tap capture | `12b8c263871d4ffbf203b30d8963d79f472576c0484617802340f06b8a2398b1` |
| cycle 3: console transcript | `a4dc7683b374b00c39053a433ca78c9cd3f9de19517a8149003c27b127e8df2e` |
| cycle 3: controller-host watcher | `cea282b0bee69f6a2e1b27aaa6607d46a669b471ea18d960436e334d5a52326b` |
| cycle 3: controller-host port capture | `816249e43cbb2684118dac3bef127c7f51d66ddc070bd4016904e9b8c0512d13` |
| cycle 3: power-strip log | `06b09ca4686898c7687baf1af57f108bd403b120fba13291b8d0f64d651b27e1` |
| cycle 3: analysis | `12448e4a7fc69d53e787a29b2131b55059ab36ae67577273d5234c1add1c4e8d` |
| cycle 4: tap capture | `b4b110d0ff7969c39d8b5010563e71d352d59d128e3185e414baba9e6fde7fc2` |
| cycle 4: console transcript | `e66a11f685326289f41a84ce3ca8b15f4493f93ed7808abf41f6a2f958eb6adb` |
| cycle 4: controller-host watcher | `499588c787cfda885d75b67fbb74b0fc265614cae0762fda1fcc208389bc5f57` |
| cycle 4: controller-host port capture | `71c40df9af5aba12690697098724969e848169ae875841832036336f78ebe26a` |
| cycle 4: power-strip log | `fa162ec8a3b6a49f6829e1e6bbb049e15816d68b14ef4026916b34ae2bb7c20b` |
| cycle 4: analysis | `0bfdc6e8bfbaa04c246518e8d1581bb9412a91e1e3d77ca6d985772775f75087` |
| cycle 5: tap capture | `acebedfdf38fe8043b9f101fcca7baa1af6111e7579055a8a7aeb669307de79b` |
| cycle 5: console transcript | `c8167b24aff280339a33c2c5405a04cbf8401f319d120e61e0af2f4f4f7b46a4` |
| cycle 5: controller-host watcher | `86b81a207ae68fb009fa06d815a506adff944602cd913d72d8245315683dfc28` |
| cycle 5: controller-host port capture | `8dadb45ccb339660d3730f6e73857c2cd19d6c8cfb7ea071596c138c0b876cd1` |
| cycle 5: power-strip log | `2ab825b61ac6ed55b4907f51c4ac43f93d6cec0ae228a692fae95c927eaeb61a` |
| cycle 5: analysis | `353d222b6764c0d8ca256b46733af53674e5e8a796e9317792f8692fc08dc59c` |
| cycle 6: tap capture | `6b4f090a04feb89c22e5e5061453e80a06d372215412894d9fa262c356a7753e` |
| cycle 6: console transcript | `5a16a9bf2d5170311df4a804654de6d02a1bd6937e09760a215e89bdad809db7` |
| cycle 6: controller-host watcher | `9ca7e270732274d8abe246efd2351a6703b0a07cb57a948092ac87e5c83284e2` |
| cycle 6: controller-host port capture | `1576b4550b6656ba004fc5abd9dc9454a802c6784c23423468afb1fb44b7a312` |
| cycle 6: power-strip log | `66a6b6a50bdbea4c1ccc204260a3bc7ecb35e76f9f25ecf6de13a858c13cf49f` |
| cycle 6: analysis | `a3256a0b130fdf9ddd18c9d5fbb052a03cac0925c3984d3810c95deda9f022d5` |
| per-cycle summary | `4e750d619e90bef47c0a170d0cdf26b28f088ef6d0321d80993bf45bd7d39198` |
| final tap capture | `f508377309320ffcb1848d4f2fb880081711783757c3fa5d08d5d7a08aa49e98` |
| final console transcript | `bbb2e801a71d35d65afa4b6847bf1f7c1ddcbdf6cee5834b80f93806bd6a1851` |
| final grader transcript | `df57bad1e4c121b0d524ee72950c166f9074df83a4c5a80fbd19964d478720a8` |
| host cleanup record | `c09c026880d41ecb3083f1325edd7855a621c00b37f1d9aece888028a90fc19d` |
