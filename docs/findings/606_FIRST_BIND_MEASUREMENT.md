<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# First talker bind on the 13eda870 image

Refs #606. Operator [A440], measured 2026-09-29, under the
[bench lane B2 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413).

The image carries processor pin `c951a9ff`, adopted by [PR #613](https://github.com/kebag-logic/milan-fpga/pull/613).

That pin retries a refused destination-address allocation every 100 ms.

| #606 item | Verdict | Evidence |
|---|---|---|
| 1. When a talker must declare Talker Advertise | Not a bench item | Answered by the [A10 analysis](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5860869610) on #606. The declaration gate is observed here; see [Declaration gate on the wire](#declaration-gate-on-the-wire). |
| 2. Reproduce and attribute in simulation | Not a bench item | The [A10] analysis and PR #613's first-probe regression. |
| 3. First bind on the bench, against 1 s | PASS, 5 of 5 | 0.059-0.229 s from the `CONNECT_RX` response to the first valid CRF PDU. See [Per-bind results](#per-bind-results). |
| 3. Long-hold connect on the bench, against 1 s | PASS, 4 of 4 | Binds 2-5 follow 36.9-39.3 s unbound, each after the DUT withdrew its Talker Advertise. |
| 3. Periodic refresh and LeaveAll kept | Observed, not graded | DUT MSRP kept 1.000 s periodic spacing, 0.2 s after a LeaveAll. A DUT LeaveAll crossed every pre-bind window. |

These are operator measurements, not review verdicts.

The post-reset allocation path is not exercised; see [Limits](#limits).

The [#608 and #75 page](608_75_WITHDRAWAL_AND_RESTART.md) records the same session's 100 cycles.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, its identity readback, the bound pair and the bench as found.
- **[Method](#method)** -- What makes a bind fresh, how it is reached without a reset, and the timing anchors.
- **[Per-bind results](#per-bind-results)** -- Five first binds and the four unbinds between them.
- **[Declaration gate on the wire](#declaration-gate-on-the-wire)** -- When the DUT declares and withdraws its Talker Advertise.
- **[Comparison with the 9e9954e9 first bind](#comparison-with-the-9e9954e9-first-bind)** -- The PR #604 first bind beside these five.
- **[Limits](#limits)** -- What this bench run does not show.
- **[Restore](#restore)** -- The bench as left, and the DUT's saved-state layer at start and end with its cause.
- **[Artifact hashes](#artifact-hashes)** -- Image, tool and raw-capture identities.

## Identity and setup

The image is dev `13eda870d1a6cf3f946fc228a98862366b08d102`, seed `eto`.

Lane B1 identified the same image in [PR #620](https://github.com/kebag-logic/milan-fpga/pull/620).

The lane base is the same commit, so no source differs.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d84bce7b`, the `eto` seed; `eppo` reads `bf44ccc9`, `asl` reads `809fcffa` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Live ENTITY and CONFIGURATION | Byte-exact to the AEM image at `0x110` (312 bytes) and `0x248` (106 bytes); entity `020000fffe000001` |
| UART grader | 10 of 10, exit 0 |
| Reset epoch | 1, before and after every action |

Readback proves CRC consistency, not a configuration SHA-256.

The [identity method](117_GPTP_SILICON_EVIDENCE.md#candidate-image-and-identity-proof) was repeated.

Topology: the DUT, the inline tap, the bench AVB switch, the reference peer.

The switch is the adjacent bridge and the grandmaster.

The controller host shares the AVB network behind it.

| Binding | Talker output | Listener input | Format |
|---|---|---|---|
| DUT talker | DUT Stream Output 1, stream `0200000000010001` | Reference peer Stream Input 8 | CRF `041060010000bb80` |

As found, all 18 queried stream states were unbound.

The DUT selected clock source 0, INTERNAL.

The reference peer was in configuration 1 at 48 kHz, as PR #620 found.

Neither setting changed in this lane.

Both DUT Stream Outputs already held MAAP-range destinations.

Output 0 (`91:e0:f0:00:e5:11`) was never bound in this lane.

On image `9e9954e9` both outputs read all-zero at the #75 start census.

That matches processor PR 129's automatic acquisition.

The acquisition itself happened before this lane and was not observed.

## Method

**Fresh state.** A bind is fresh when the DUT declares no Talker Advertise for the stream.

The runner checks at least 16 s of tap before sending `CONNECT_RX`.

That window must contain a DUT MSRP LeaveAll.

A declaring applicant re-declares its attributes after its own LeaveAll.

Only `New`, `JoinIn` and `JoinMt` count as declarations.

The window must also carry no bridge Listener declaration and no stream PDU.

The runner refuses to bind otherwise; it refused none of the five.

**Reaching it without a reset.** The processor's talker declares under a gate.

It declares while a probe is under 15 s old, or while a listener is registered.

The gate is `T-SRP-DAFRESH` in the processor's
[ACMP engine design](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/c951a9ff0cb5851fb159d33e966e5a2a9a188fe3/docs/architecture/05_acmp_engine.md), section 6bis.

So after an unbind the DUT sends `Lv` once the last probe is 15 s old.

The unbind action waits for that `Lv`, then 10 s more.

The next bind's 16 s window follows, so its `CONNECT_RX` comes at least 26 s after the `Lv`.

That exceeds the 802.1Q LeaveTime of 0.6-1.0 s and the processor's 4.5-7.5 s in its
[timer table](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/c951a9ff0cb5851fb159d33e966e5a2a9a188fe3/docs/architecture/08_timing.md).

Bind 1 followed more than 30 minutes unbound, since lane B1's restore.

The DUT was never reset, rebooted, flashed or power-cycled.

**Timing.** Each bind is one `CONNECT_RX` from the controller host.

The successful response crossing the tap starts the interval.

The first valid CRF PDU of the stream ends it.

The validity predicate is [PR #604's](75_RECONNECT_RESTART_MEASUREMENT.md#method):

- EtherType `0x22f0`, subtype `0x04`, at least 28 bytes;
- `sv=1`, version 0, type 1, 48 kHz with pull 0;
- eight bytes of data per 96 samples;
- VLAN 2 with PCP 3, the bound stream ID;
- the DUT's tap port and source address;
- the settled binding's destination address;
- the next PDU advancing sequence and timestamp.

The tap stamps both directions on one hardware clock.

Its nanosecond word is unwrapped against the capture host's timestamps.

Host clock offsets do not enter any interval.

CRF PDUs come every 2 ms, which bounds when streaming could start.

**Other records.** Each action read the DUT console before and after.

The reads were `milan_status` and six read-only CSR words.

The controller read AVB_INTERFACE and stream counters before and after.

Every action held the bench lock for its own duration only.

An offline replay of every capture reproduces each live interval exactly.

## Per-bind results

All times are seconds after the tapped `CONNECT_RX` response.

| Bind | Unbound before, s | Pre-bind tap, s | DUT LeaveAll PDUs / target TA declarations in it | First probe status | First DUT TA, s | First bridge MRPDU, s | Bridge Listener Ready, s | First valid PDU, s | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | more than 1,800 (lane B1's restore) | 17.315 | 2 / 0 | SUCCESS | 0.171413 (JoinMt) | 0.227724, Listener New | 0.227724 | 0.228304 | PASS |
| 2 | 39.3 | 17.323 | 1 / 0 | SUCCESS | 0.068868 (JoinMt) | 0.125289, Listener New | 0.125289 | 0.126451 | PASS |
| 3 | 36.9 | 17.341 | 1 / 0 | SUCCESS | 0.074340 (JoinMt) | 0.129176, Listener New | 0.129176 | 0.130400 | PASS |
| 4 | 37.0 | 17.373 | 1 / 0 | SUCCESS | 0.172822 (JoinMt) | 0.227576, Listener New | 0.227576 | 0.229360 | PASS |
| 5 | 36.9 | 17.334 | 2 / 0 | SUCCESS | 0.000337 (JoinMt) | 0.057989, Listener New | 0.057989 | 0.059352 | PASS |

- The reference peer's `PROBE_TX` crossed the tap 27-83 us after the response.
- The DUT answered each with SUCCESS 7 us later.
- The DUT's first Talker Advertise was a `JoinMt`, inside one 0.2 s join period.
- The bridge's first MRPDU was its Listener Ready (`New`) each time.
- No bridge LeaveAll came between the response and that Ready.
- The first valid PDU followed Ready by 0.6-1.8 ms.
- DUT Stream Output 1 counted STREAM_START +1 per bind.

Unbinds between binds, seconds after the tapped `DISCONNECT_RX` response:

| Unbind | After bind response, s | Bridge Listener Lv, s | Last PDU, s | PDUs after Lv + 2 ms | DUT TA Lv, s | Quiet after TA Lv, s | START / STOP |
|---|---|---|---|---|---|---|---|
| 1 | 25.7 | 0.009225 | 0.008539 | 0 | 0.021 | 10.2 | +0 / +1 |
| 2 | 7.9 | 0.008669 | 0.007266 | 0 | 7.168 | 10.8 | +0 / +1 |
| 3 | 7.9 | 0.009364 | 0.007875 | 0 | 7.144 | 10.8 | +0 / +1 |
| 4 | 8.1 | 0.009182 | 0.008618 | 0 | 7.122 | 10.8 | +0 / +1 |

"After bind response" is on the controller host's clock; the rest are tap times.

Every unbind stopped the stream within one PDU of the bridge's Listener `Lv`.

## Declaration gate on the wire

- Unbind 1 came 25.7 s after its bind; the DUT withdrew 21 ms after the response.
- Unbinds 2-4 came 7.9-8.1 s after their binds.
- Their withdrawals came 7.1-7.2 s later, 15.07-15.17 s after the bind.
- That is the 15 s probe freshness of the gate.
- Before each bind the DUT sent only `Mt` for the stream, never a declaration.
- DUT MSRP PDUs kept 1.000 s periodic spacing, 0.2 s after a LeaveAll, in the baseline and final captures.
- Each off-grid DUT PDU there was a reply to the bridge's LeaveAll, its own LeaveAll, or the PDU 0.2 s after it.

## Comparison with the 9e9954e9 first bind

The earlier record is PR #604's `talker-setup` capture, with [A10]'s analysis on #606.

| Event after the `CONNECT_RX` response | `9e9954e9`, one bind | `13eda870`, binds 1-5 |
|---|---|---|
| First `PROBE_TX` response | status 3, `TALKER_DEST_MAC_FAILED` | SUCCESS, 5 of 5 |
| First DUT Talker Advertise | 0.079 s | 0.000337-0.172822 s |
| Bridge's first MRPDU | LeaveAll at 6.080 s | Listener Ready at 0.057989-0.227724 s |
| Bridge Listener Ready | 6.888605 s | 0.057989-0.227724 s |
| First valid CRF PDU | 6.889398 s | 0.059352-0.229360 s |

The old first bind waited for the peer's second probe after a refused one.

Here the first probe succeeds and no LeaveAll is involved.

## Limits

- **The post-reset path is not exercised.** The #606 cause was a refused startup allocation.
- Reaching it needs a DUT reset, which this lane forbids.
- The DUT's destinations were already held, so no allocation ran here.
- PR #613's first-probe regression remains that branch's evidence.
- The reference peer's own link is behind the bridge and not tapped.
- Only CRF was measured; AAF remains unmeasured.
- Printed precision is not a calibrated timestamp accuracy.

## Restore

- The pair was unbound on the first attempt; all 18 stream states read connection count 0.
- The start and end censuses agree on all 53 non-counter reads.
- The DUT still selects INTERNAL; the peer is unchanged.
- A final 16.9 s tap capture carried no CRF PDU.
- The UART grader passed 10 of 10; the reset epoch read 1.
- The temporary controller and capture scripts were removed.
- The temporary capture module was unloaded and its build removed.
- The capture host's interface set is as found.
- Outlets read as B1 left them; this lane switched none.
- The bench lock was verified free.
- The DUT's saved-state layer read the same at start and end; see [Saved-state layer](#saved-state-layer).

The [#608 and #75 page](608_75_WITHDRAWAL_AND_RESTART.md#counters-and-restore) gives the counter reconciliation.

### Saved-state layer

The census compares AEM state only; the DUT's saved-state status read the same at start and end.

| Saved-state field | Identity gate, 06:49:58Z | Final restore, 07:20:45Z |
|---|---|---|
| NVM slots A / B, image sequence | 229 / 230, image 230 | 229 / 230, image 230 |
| Records, writer | 53 records, 3,264 B, writer live | 53 records, 3,264 B, writer live |
| Commits ok / failed | 2 / 0 | 2 / 0 |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000c44`, 1 | `0x5b000c44`, 1 |
| `PP_NVM_STAT` | `0xc34000e4`, pend 1 | `0xc34000e4`, pend 1 |

The round-2 packet's `saved_state_b2.py` derives this from every console sample and controller transcript.

- The two `milan_nvm` reads bracket every action: the action console samples run from 06:53:46Z to 07:20:32Z.
- Only those two reads carry `PP_NVM_STAT`, the slot sequences and the commit counts.
- The 224 action console samples between them carry `PP_STAT` alone.
- `PP_STAT` read `0x5b000c44` in all 226 console samples.
- So `nvm_pend` and `nvm_backed` read 1, and `nvm_dirty`, `nvm_stale` and `nvm_alarm` 0, at every sample.
- The lane's only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`.
- All went to the reference peer's Stream Input 8; every `CONNECT_RX` named DUT Stream Output 1.
- Every AECP command, to either entity, was a GET_ or READ_ command.
- The DUT's two stream inputs read connection count 0 in all 340 polls.

Only the binding records, ids `0x20` to `0x2F`, have a record writer ([snapshot ownership, section 11](../design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#11-persistent-field-materialization)).

They are indexed by sink, the DUT's stream inputs ([record allocation](../design/SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged)).

No record holds a stream output's connections.

So none of the lane's binds, unbinds or cycles wrote a record, and no commit ran.

The commit count stayed 2 / 0 and the slots stayed 229 / 230.

`nvm_pend` = 1 was inherited from lane B1.

Its final restore on [PR #620](https://github.com/kebag-logic/milan-fpga/pull/620) reads the same slots, commits, `PP_STAT` and `PP_NVM_STAT`.

That page attributes the pending bit to SET_CLOCK_SOURCE writes, whose sticky level only a DUT reset clears.

The persisted records were not read back or compared with the found state.

## Artifact hashes

The author's bench packet holds scripts, transcripts, analyses and `MANIFEST.sha256`.

`RAW-ARTIFACTS.json` there indexes every raw capture by size and SHA-256.

Raw captures stay outside the packet and the repository.

Retention follows [TESTING section 6b](../testing/TESTING.md#6b-bench-evidence-retention).

| Image artifact | Bytes | SHA-256 |
|---|---|---|
| `gateware/alinx_ax7101.bit` | 3825992 | `690d87e407bbb7f7bba52bbe7a7e0dc85cd264df2db5eec87bfaf85f99bda24b` |
| bitstream payload | 3825788 | `6597f7a601ddb3dbba1bf058c38716277e8feb1147fb89edcf1d39e755dc369f` |
| `aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `csr.csv` | 9033 | `7723d0b8129df7b77b3b49980366f18c91adb15f8c38526f48a5ebd32d1207a2` |

| Tool | Role | SHA-256 |
|---|---|---|
| `b2_action.py` | acquisition: one locked capture and controller action | `b38b34cd816ea3b54bdcbe517e95137aec4b942323f2aacaee1bf7e740278a0b` |
| `run_action.sh` | bench-lock wrapper for one action | `77ca9d6448bf9a400594c775e1788b7642933765dc803cdc3daf5cfac27488bb` |
| `series.sh` | cycle series, one lock window per cycle | `d314a982b566e132545c30551342d919128d3b1971f5c050a6a0d49f6d718cbd` |
| `identity_locked.sh` | identity readback and UART grader under the lock | `0facac30157c813ad21f5a869dc9f31d9a0313f53346ef9d2cacf67539d03090` |
| `b2_analyze.py` | offline replay of one capture | `22a010930831c5bdb0a27240dd09e3decb3cef96dc1991390caa2ad3cadbee14` |
| `b2_summary.py` | distributions, growth and stop classes | `c7c753aaa156b7a2ef1552dbbcdec32f5ea24e1efb99377fb1d98e322cde725c` |
| `b2_pages.py` | page tables from the summary | `1e3412ff9ab6a4ba5d6f25c4c1865e1a92811d7bffafec9cf70bdfbe84bb8382` |
| `b2_assemble.py` | page assembly from the tables | `876016dfe28f7017d1a074092f6bb1136ee18265d66f8a86d0c0c63a60737067` |
| `aecp_identity.py` | ENTITY and CONFIGURATION byte comparison | `5e9ddcc669c1ab846413fff18d622f1fd2c87b51f99b4a5c0a0249438a0ef2f2` |
| `b2_reconnect.py` | controller transactions for the one pair | `3c86cf246fea8fd1736f42904dfff342d367eea98bcf302f328b75ca6b8d4b4c` |
| `b2_controller.py` | controller reads; PR #604 copy, import renamed | `29a3d493ba3c82b6618aef9dfd1a940057857230a7315d63a6cbf1c11a2beb51` |
| `avdecc_ro.py` | raw AVDECC reader, unchanged from PR #604 | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` |
| `capture.py` | bounded tap capture, unchanged from PR #604 | `2601b03e16c0caa7c13f170a7316d7262a9f9bc4cc265dcba881165364a1fb61` |
| `console_read.py` | read-only console reader, unchanged from PR #604 | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` |
| `wire_summary.py` | tap decoder, unchanged from PR #604 | `7a8af475fa5f8bfbb90636b92bf9d07a86140c54a9be10c12f9b76235bccd922` |
| `expected_crc.py` | reference CRC table, unchanged from PR #604 | `04d128bb0a9ffe8ad5898f4ece380899a096a1595aadda3ece1048c313bf19d7` |
| `census_compare.py` | census comparison, unchanged from PR #620 | `f014c6f2bd80e4622960c76dba3c908299357f8c9fcc03097441750d40d8db79` |
| [UART grader](../../scripts/baremetal_uart_smoke.py) at `13eda870` | identity and restore | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` |

The baseline observation ran an earlier `b2_action.py`, whose pre-window wait counted host time.

Every bind, unbind, cycle and restore ran the revision above.

| Capture identifier | Bytes | SHA-256 |
|---|---|---|
| `baseline/tap.pcap` | 53300 | `4779ea0960f065d34ac7b544d06d7a0dc638b39c60de1c60684f9608b70c5d48` |
| `bind-1/tap.pcap` | 253549 | `94a00dca9adebb4fac57d6353789d3ccb0f4f5831ad848083025914f1ef7aa53` |
| `unbind-1/tap.pcap` | 194880 | `a74a6d60b2f8dcb4d5590a220b84582394d61aaed2c42d3df5302286845003e4` |
| `bind-2/tap.pcap` | 259895 | `83ef6d655a570ff9e833c64e00196c4fd9e33ceffff6eab8b8ec9015793dc979` |
| `unbind-2/tap.pcap` | 237865 | `15f343af974934d7f6961966c51a357383f94a926f669bfb964e542aaf715e8b` |
| `bind-3/tap.pcap` | 260379 | `9c7375c5cbd30c3082b86d47bad583750beef8e19bcd48233c0ca6c2e4c096db` |
| `unbind-3/tap.pcap` | 238485 | `cf5f152c684124ca8a40d04605c00e1125b61aa6bcddc5b550409d16883b19e3` |
| `bind-4/tap.pcap` | 255843 | `eaace30cf643fc320d5afbc91a34dc5f5cfa70dea742e5ef644daab928eade00` |
| `unbind-4/tap.pcap` | 239794 | `729260503680f614fc0d54cff32c4d735237bf6e5433e8d46ee02f0f35621932` |
| `bind-5/tap.pcap` | 267770 | `11af012b4f312d0b8dce151d21042c127afc156abe2813967efa8e414f990c95` |
| `unbind-restore/tap.pcap` | 193755 | `5c13c51cee24742f25a5502d4bdc6b50f879dd8d2b85e9becb6d7c64db088afb` |
| `final/tap.pcap` | 55800 | `056ceae89a0c0418418e4d787a6c47e485fd95ba479442bc292857194da5324c` |
