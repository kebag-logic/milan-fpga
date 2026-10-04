<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Disconnect order seen by a controller, on the bbf704ec image

Refs #653. Operator [A535], 2026-10-04, under the
[bench lane B11 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983239639).

The owner reported that, on a controller's disconnect, the DUT sent the
counters notification carrying MEDIA_UNLOCKED before its UNBIND_RX response.
The simulation lane did not reproduce it
([STOP](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980272602)),
and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980290102)
left the hardware order to a capture at the DUT's port. This page is that
capture, with what a real controller library reports for the same disconnects.

These are operator observations, not review verdicts.

## Contents

- **[#653 bench: disconnect order, 2026-10-04](#653-bench-disconnect-order-2026-10-04)** -- The verdict per #653 acceptance item, and the answer to the owner's report.
- **[Identity and state as found](#identity-and-state-as-found)** -- The image's identity readback and the DUT's live state before the lane.
- **[Method](#method)** -- The controller probe, the binding rule, the cycles, the tap captures and how each one is decoded.
- **[Per-cycle results](#per-cycle-results)** -- The wire order, the intervals, the pushed counter pair and the library's view, for every disconnect.
- **[What the controller library reported](#what-the-controller-library-reported)** -- Compatibility flags, diagnostics and counter state held by the library across the session.
- **[The control capture](#the-control-capture)** -- A disconnect whose order is known, which the order check must read as counters first.
- **[The CRF input before PR #655](#the-crf-input-before-pr-655)** -- The 100 ms window in which an unbound CRF input still reads locked.
- **[Bench as left](#bench-as-left)** -- The state at the end against the start, and the residuals.
- **[Limits](#limits)** -- What these runs do not show.
- **[Artifact hashes](#artifact-hashes)** -- The captures, the probe and the lane tools.

## #653 bench: disconnect order, 2026-10-04

The owner's report is **not reproduced** on this bench. In all 23
disconnects, 20 of the AAF input, 2 of the CRF input and 1 control, the
UNBIND_RX response left the DUT's port first. The la_avdecc controller library
flagged nothing in any of them.

| #653 acceptance | On this image | Evidence |
|---|---|---|
| 1. The UNBIND_RX response leaves before the counters notification that reports the unlock, for AAF and CRF and each input | Held, 23 of 23 | Response 7.5 µs after the command every time. The unlock's GET_COUNTERS follows 114.2 to 116.8 µs later on the AAF input 0, and 99.3 and 99.7 ms later on the CRF input 1. See [Per-cycle results](#per-cycle-results). |
| 2. A bench capture of a disconnect, with a control that fails the check | Done | One tap capture per disconnect, each read response first by the lane grader and by the provided decoder. In the control, the check reads counters first against the probe's own GET_COUNTERS. See [The control capture](#the-control-capture). |
| 3. MEDIA_LOCKED = MEDIA_UNLOCKED after the unbind; STREAM_INTERRUPTED does not count it | AAF held; CRF not at every instant | AAF: the first push after the unbind reads 1/1, STREAM_INTERRUPTED 0. CRF: 1/0 until the silence timeout, then 1/1, as expected before PR #655. See [The CRF input before PR #655](#the-crf-input-before-pr-655). |
| 4. A controller session connects and disconnects 20 times with no counter error | Held for the library | One la_avdecc session ran 20 AAF and 2 CRF cycles. No compatibility change, diagnostic, query error or lost notification. The Hive application itself was not run. |

The AAF talker was still streaming at every UNBIND_RX command: 303 to 1,562
AAF frames reached the DUT after it. So each unlock came from the bind fall,
not from a talker that stopped first, one of the simulation lane's open
questions.

## Identity and state as found

The image is the one lanes B7 to B10 used: dev `bbf704ec`, flashed and booted
by the manager. The lane base is dev `6c22d3ca`. The identity gate ran first,
under the bench lock.

| Identity check | Result |
|---|---|
| Entity ID, entity name, firmware version and serial over ATDECC | `020000fffe000001`, "Milan FPGA 1x1 TDM8", "2.96.0", "AX7101-0001": PASS |
| VERSION | `0x00020060` |
| CRC32 of the AEM image, the BIOS ROM and the bitstream payload | `5ba355eb`, `2144df1c`, `e6b8febc`, each equal to the build's |
| Static descriptor bytes over AECP | Equal to the build's AEM image |
| UART grader | 10 of 10 |

Three live-state values differ from the AEM image, as on lane B10:
STREAM_INPUT 0's current format, the CLOCK_DOMAIN's current source and its
GET_CLOCK_SOURCE.

As found, the DUT matched lane B10's end state:

- CLOCK_DOMAIN 0 on CLOCK_SOURCE 1, the CRF input, with the media-clock servo
  IDLE (`MCSRV_STAT` `0x00000020`), at 48 kHz.
- STREAM_INPUT 0 at `0205022001006000` and STREAM_INPUT 1 at
  `041060010000bb80`, the formats of the peer's AAF and CRF talkers.
- One mapping on STREAM_PORT_INPUT 0 (stream 0 channel 0 to cluster 0); the
  output map empty.
- Every stream of both entities unbound.
- NVM image seq 51, 20 commits.

## Method

Every bench action held the shared lock and ran in the foreground with a
deadline. No flash, power, wiring, instrument or USB-function action occurred.
No DUT register was written.

**The probe.** A C++ program on the controller host, linked against the
bench's la_avdecc 4.3.1.1 build; the library reports its version as
`4.3.1-beta1`. It runs two local controller entities on the AVB interface:

- **The session**: the library's high-level controller
  (`la::avdecc::controller::Controller`), the layer a controller application
  uses. It enumerates the DUT and the reference peer and registers for their
  unsolicited notifications. It issues every bind and unbind, and reports
  through its observer.
- **An auxiliary entity**: a low-level controller entity with its own ProgID.
  It reads both stream formats live before each bind, and sends the control's
  GET_COUNTERS. It never binds and never sets.

The installed include tree lacks one header the high-level API includes,
`avdeccVirtualControlledEntityInterface.hpp`. It was taken from the same tag's
source tree, whose other headers equal the installed ones. The JSON feature
was left out; it gates only free functions.

At the end of each session the controller was destroyed. An entity with the
session's ProgID, and so its entity ID, then sent
DEREGISTER_UNSOLICITED_NOTIFICATION to both entities; each answered SUCCESS.

**One cycle:**

1. **Binding rule.** GET_STREAM_FORMAT on the talker's STREAM_OUTPUT and the
   listener's STREAM_INPUT. A difference would set the listener's format to
   the talker's. The formats were equal in all 23 cycles, so none was set.
2. **Bind** through the library (BIND_RX): SUCCESS in all 23.
3. **Wait for MEDIA_LOCKED**, as the library reports it: a counters update
   after the bind with MEDIA_LOCKED above MEDIA_UNLOCKED.
4. **Hold** 2.0 to 3.0 s, stepped by 137 ms per cycle.
5. **Control only:** the auxiliary entity's GET_COUNTERS, answered before the
   next step.
6. **Unbind** through the library (UNBIND_RX).
7. **Wait** 2.5 s (AAF) or 3 s (CRF), then snapshot the library's state.

The DUT resets an input's counters at a bind and pushes them at once. Its next
push for that input comes one second later, so the library reports
MEDIA_LOCKED 1,003 ms after every bind. That figure is the push cadence, not a
lock time. Every unbind came at least 2 s after the input's last push.

| Cycles | Talker | Listener | Session |
|---|---|---|---|
| A01 to A20 | The peer's AAF STREAM_OUTPUT 0 | The DUT's STREAM_INPUT 0 | s1 |
| R01, R02 | The peer's CRF STREAM_OUTPUT 2 | The DUT's STREAM_INPUT 1 | s1, after A20 |
| C0, the control | The peer's AAF STREAM_OUTPUT 0 | The DUT's STREAM_INPUT 0 | s0b, a separate session |

**The captures.** The inline tap sits at the DUT's port. A capture started
before each cycle's first command and stopped after its wait. It kept every
frame of the AVTP ethertype, control and stream alike. Each record carries the
port (switch to DUT, or DUT to switch) and a 64-bit nanosecond timestamp. In
every capture the timestamp never decreases in file order across both ports.

**Decoding.** Each capture was read twice:

- by the provided `tap_order_decode.py`, unchanged, for its line order;
- by the lane grader. It finds the UNBIND_RX command and response for the
  cycle's input. The unlock's GET_COUNTERS is the first unsolicited
  GET_COUNTERS from the DUT for that input whose MEDIA_UNLOCKED exceeds every
  value pushed before the command. The order is whichever comes first in the
  capture.

The two agree on all 23 captures. The provided decoder's time column is not in
milliseconds: it reads the timestamp's two 32-bit words swapped. Its ACMP
listener, unique ID and connection count columns also read the wrong offsets.
Neither affects its line order.

## Per-cycle results

Intervals are tap timestamps at the DUT's port. "Library: input state at that
update" is the library's view of the DUT's input when it delivered the
counters update carrying the unlock. The library pair is MEDIA_LOCKED,
MEDIA_UNLOCKED and STREAM_INTERRUPTED as the library held them after the
cycle's wait.

| Cycle | Stream, DUT input | MEDIA_LOCKED reported after bind (ms) | Hold (ms) | UNBIND_RX command to response (µs) | Response to the unlock's GET_COUNTERS (µs) | Order at the DUT's port | Pushed LOCKED/UNLOCKED/INTERRUPTED | Stream frames after the command | Library: input state at that update | Library flags | Library pair after | Capture |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 (control) | AAF, 0 | 1003 | 2000 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 1,168 | NotConnected | none | 1/1/0 | `4fa8c57c4b58` |
| A01 | AAF, 0 | 1003 | 2000 | 7.5 | 115.5 | RESPONSE_FIRST | 1/1/0 | 303 | NotConnected | none | 1/1/0 | `6e2879e6ad58` |
| A02 | AAF, 0 | 1003 | 2137 | 7.5 | 114.2 | RESPONSE_FIRST | 1/1/0 | 448 | NotConnected | none | 1/1/0 | `2da6e350212c` |
| A03 | AAF, 0 | 1003 | 2274 | 7.5 | 114.5 | RESPONSE_FIRST | 1/1/0 | 1,111 | NotConnected | none | 1/1/0 | `95ece933ecb6` |
| A04 | AAF, 0 | 1003 | 2411 | 7.5 | 116.8 | RESPONSE_FIRST | 1/1/0 | 776 | NotConnected | none | 1/1/0 | `a2cb6bd81919` |
| A05 | AAF, 0 | 1003 | 2548 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 799 | NotConnected | none | 1/1/0 | `03ba3c61e102` |
| A06 | AAF, 0 | 1003 | 2685 | 7.5 | 116.8 | RESPONSE_FIRST | 1/1/0 | 1,304 | NotConnected | none | 1/1/0 | `c3861dbadd69` |
| A07 | AAF, 0 | 1003 | 2822 | 7.5 | 116.1 | RESPONSE_FIRST | 1/1/0 | 848 | NotConnected | none | 1/1/0 | `303d24587e20` |
| A08 | AAF, 0 | 1003 | 2959 | 7.5 | 114.8 | RESPONSE_FIRST | 1/1/0 | 867 | NotConnected | none | 1/1/0 | `9e34b4baa256` |
| A09 | AAF, 0 | 1003 | 2096 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 1,297 | NotConnected | none | 1/1/0 | `bd9f74e69513` |
| A10 | AAF, 0 | 1003 | 2233 | 7.5 | 115.1 | RESPONSE_FIRST | 1/1/0 | 640 | NotConnected | none | 1/1/0 | `d9469de78767` |
| A11 | AAF, 0 | 1003 | 2370 | 7.5 | 116.0 | RESPONSE_FIRST | 1/1/0 | 425 | NotConnected | none | 1/1/0 | `9a8f2c276fef` |
| A12 | AAF, 0 | 1003 | 2507 | 7.5 | 116.8 | RESPONSE_FIRST | 1/1/0 | 729 | NotConnected | none | 1/1/0 | `80983fa9bd3e` |
| A13 | AAF, 0 | 1003 | 2644 | 7.5 | 114.9 | RESPONSE_FIRST | 1/1/0 | 1,513 | NotConnected | none | 1/1/0 | `6f0de98ab446` |
| A14 | AAF, 0 | 1003 | 2781 | 7.5 | 116.0 | RESPONSE_FIRST | 1/1/0 | 1,256 | NotConnected | none | 1/1/0 | `dd5774b30f8c` |
| A15 | AAF, 0 | 1003 | 2918 | 7.5 | 115.7 | RESPONSE_FIRST | 1/1/0 | 1,562 | NotConnected | none | 1/1/0 | `6f7c12331830` |
| A16 | AAF, 0 | 1003 | 2055 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 746 | NotConnected | none | 1/1/0 | `b8293ce029b5` |
| A17 | AAF, 0 | 1003 | 2192 | 7.5 | 116.2 | RESPONSE_FIRST | 1/1/0 | 410 | NotConnected | none | 1/1/0 | `7321a54e63dd` |
| A18 | AAF, 0 | 1003 | 2329 | 7.5 | 114.8 | RESPONSE_FIRST | 1/1/0 | 485 | NotConnected | none | 1/1/0 | `d23198019e43` |
| A19 | AAF, 0 | 1003 | 2466 | 7.5 | 115.3 | RESPONSE_FIRST | 1/1/0 | 1,057 | NotConnected | none | 1/1/0 | `008deccfe05f` |
| A20 | AAF, 0 | 1003 | 2603 | 7.5 | 116.2 | RESPONSE_FIRST | 1/1/0 | 442 | NotConnected | none | 1/1/0 | `8e07888e2ba3` |
| R01 | CRF, 1 | 1003 | 2740 | 7.5 | 99,346.2 | RESPONSE_FIRST | 1/1/0 | 32 | NotConnected | none | 1/1/0 | `970a213ab53c` |
| R02 | CRF, 1 | 1003 | 2877 | 7.5 | 99,731.4 | RESPONSE_FIRST | 1/1/0 | 18 | NotConnected | none | 1/1/0 | `c743c09453ab` |

On the wire, every disconnect has the same shape:

1. UNBIND_RX command, switch to DUT.
2. UNBIND_RX response, 7.5 µs later, SUCCESS.
3. An unsolicited GET_STREAM_INFO for the input. In R01 an unsolicited
   GET_AVB_INFO also went out here.
4. The unsolicited GET_COUNTERS reporting the unlock.

This is the order the simulation lane traced at `fea346e7`.

The last AAF frame reached the DUT 37.8 to 195.2 ms after the command; the
last CRF frame 35.7 and 63.3 ms after it.

## What the controller library reported

At the session's start both entities were online, compatible with IEEE 1722.1
and Milan 1.2, and subscribed to unsolicited notifications. Neither had a
compatibility event or a diagnostic.

Across the session's 22 cycles, and the control's session, the library raised
none of these:

- a compatibility change: the Milan flag was never removed, and no warning
  flag was added;
- a diagnostics change;
- an entity query error, an AECP timeout or an unexpected response;
- a lost unsolicited notification.

Both entities' compatibility-event lists were still empty at each session's
end.

In every cycle the library marked the DUT's input NotConnected, on the
UNBIND_RX response, before it delivered the counters update carrying the
unlock. On the AAF input that update arrived 51 to 113 µs after the input went
NotConnected, and 0.9 to 5.2 ms after the probe issued the unbind. After every
cycle the library held 1/1/0 for the input.

The shared library carries a compatibility check worded "Invalid
MEDIA_LOCKED / MEDIA_UNLOCKED counters value on STREAM_INPUT", cited to Milan
1.3 clause 5.3.8.10. It raised no event in any cycle.

## The control capture

C0 ran in its own short session with the same probe. After the hold, the
auxiliary entity sent GET_COUNTERS for STREAM_INPUT 0 and waited for the
answer, LOCKED 1, UNLOCKED 0, before the session sent UNBIND_RX. The order on
the wire is therefore known.

Both decoders show it: the probe's GET_COUNTERS command and response, then
the UNBIND_RX command and response, then the unsolicited GET_STREAM_INFO and
GET_COUNTERS. The response came 1,629.8 µs after the probe's own
GET_COUNTERS answer.

Run against the probe's own GET_COUNTERS answer instead of the unlock's push,
the order check reads COUNTERS_FIRST. A counters frame ahead of the response
is therefore detected, and the check can fail. Against the unlock's push, C0
reads RESPONSE_FIRST, like every other cycle.

## The CRF input before PR #655

The image predates [PR #655](https://github.com/kebag-logic/milan-fpga/pull/655),
which counts a locked CRF input's unlock at the bind fall. As expected, the
DUT counted the CRF unlock only at its 100 ms silence timeout. It pushed it
99.3 and 99.7 ms after the UNBIND_RX response.

In that window the library held the CRF input at MEDIA_LOCKED 1,
MEDIA_UNLOCKED 0 while showing it NotConnected: for 95.0 ms in R01 and
100.0 ms in R02. It flagged nothing then, and nothing when 1/1/0 arrived.

## Bench as left

| Item | Start | End |
|---|---|---|
| CLOCK_DOMAIN 0 | CLOCK_SOURCE 1 | CLOCK_SOURCE 1, read back |
| Media-clock servo | IDLE, `0x00000020` | IDLE, `0x00000020` |
| Stream formats, map, bindings | As found | 45 of 46 census entries equal; the 46th is the live propagation delay, 381 to 387 ns |
| STREAM_INPUT 0 and 1 counters | 1/1 each | 1/1 each |
| CLOCK_DOMAIN 0 LOCKED/UNLOCKED counters | 3/3 | 6/6 |
| NVM | Image seq 51, 20 commits | Image seq 98, 67 commits |
| UART grader | 10 of 10 | 10 of 10 |

The CRF cycles left the servo in HOLDOVER with a held trim (`0xffa40035`),
because CLOCK_SOURCE 1 selects the CRF input. A set to INTERNAL releases that
trim, as lane B10 found. So the lane set CLOCK_SOURCE 0, then 1, on the DUT's
CLOCK_DOMAIN, the listener's, each read back; the servo read IDLE again.

Residuals:

- 47 NVM commits: the 23 binds, the 23 unbinds and the clock-source restore.
- Three servo lock and unlock pairs on CLOCK_DOMAIN 0's counters.

The probe and its staging were removed from the controller host. The captures
were removed from the tap host once their hashes matched on both hosts.
Nothing was left running. The SoC board was read only, for health, and its
audio bridge kept the same processes.

## Limits

- **One controller layer.** The probe records what la_avdecc's high-level
  controller reports. The owner's session used the Hive application on top of
  it, which may apply counter checks of its own; Hive was not run here.
- **One registered controller.** Each push went to the session's controller
  only. A session with several registered controllers adds one push per
  controller.
- **The DUT's port only.** The order is captured where it is produced. The
  frames' order on arrival at the controller host was not captured; the
  library's processing order was recorded through its callbacks instead.
- **Push cadence.** Every unbind came at least 2 s after the input's last
  counters push. An unbind less than a second after a push was not run; the
  push would then wait for the cadence, later still.
- **The 1/0 window** on the CRF input is the pre-#655 behaviour. It is not
  re-measured on an image with PR #655.

## Artifact hashes

The captures stay outside the repository and the lane packet; their SHA-256
values were taken on the tap host and again after the copy, and match.

| Capture | Bytes | SHA-256 |
|---|---|---|
| `b11-a535-s0b-C0.pcap` | 4,385,862 | `4fa8c57c4b58ff3d1ce4fb9c7a25c9a71b0ca6bad107579fc537507a01bbef10` |
| `b11-a535-s1-A01.pcap` | 4,387,470 | `6e2879e6ad58674714d984ed5feff65c527ba90ec2496e99ba64661f375cbe78` |
| `b11-a535-s1-A02.pcap` | 4,463,782 | `2da6e350212c19bcaf11820ef981b11e9d7dab4b2e7a2c9e6c4c1347e3ca2187` |
| `b11-a535-s1-A03.pcap` | 5,058,874 | `95ece933ecb628125e48f7ab7bf0659257e87fbf30874387ebdcda0710ee3279` |
| `b11-a535-s1-A04.pcap` | 5,058,984 | `a2cb6bd81919b1bb9ccc3b1a5ed4387c57795e3b77bcff60e88b0f0dd940e4ef` |
| `b11-a535-s1-A05.pcap` | 5,356,290 | `03ba3c61e102d586e36ccba9f0eb1c3ecb43438f6acf64c054c989c2fd2252dd` |
| `b11-a535-s1-A06.pcap` | 5,653,836 | `c3861dbadd690456b50c251b4b43309a858224df11cae94eeaed1cf04e98d65a` |
| `b11-a535-s1-A07.pcap` | 5,654,184 | `303d24587e209f1f8650f17e51ef85b121f45fa6d9d0250b4408a0f8964da408` |
| `b11-a535-s1-A08.pcap` | 5,951,654 | `9e34b4baa2562a51e16dc7bb5ea982dd3cccd8ff6fc535f8026f38f798052c4b` |
| `b11-a535-s1-A09.pcap` | 4,761,490 | `bd9f74e6951333a4d60314ce14e5542e387cf47e140f60cd41dc807f24888b41` |
| `b11-a535-s1-A10.pcap` | 4,761,330 | `d9469de78767d7a6530f4d7f19a4cac9b7d7eb5955a45befa4043e4bbbf4b787` |
| `b11-a535-s1-A11.pcap` | 5,058,580 | `9a8f2c276feff3c4cbae858b1cbe1d5a44b20ea24fec382733cf80f1cb75d0e7` |
| `b11-a535-s1-A12.pcap` | 5,058,854 | `80983fa9bd3e92815b81612be22d86281f690cc5fa974bf59d7755c6830f5335` |
| `b11-a535-s1-A13.pcap` | 5,653,944 | `6f0de98ab4468ccd9026b0e623b4cdacc8f8a0dc366b1a27b5bc13d94265f692` |
| `b11-a535-s1-A14.pcap` | 5,654,074 | `dd5774b30f8c07dffc5ed2ed2cd3e3abac2746f97e749313b1d358b19ca74b25` |
| `b11-a535-s1-A15.pcap` | 5,951,784 | `6f7c123318303584ad43da24b0829480e377f8da1f4b72abd6d889d29c14f32e` |
| `b11-a535-s1-A16.pcap` | 4,463,674 | `b8293ce029b5a28a9763ed9e5ece5a4940922aed2b603a6133ecef146e22c4ef` |
| `b11-a535-s1-A17.pcap` | 4,761,274 | `7321a54e63ddb8db360e5aff96fa855c3dccd6a8a9d4a7c9b80c0d170990fa0a` |
| `b11-a535-s1-A18.pcap` | 4,763,350 | `d23198019e434c60fae86c6832a229585f932aec55d6ccc6e0566d0c07012caa` |
| `b11-a535-s1-A19.pcap` | 5,058,798 | `008deccfe05f3c9055871989bfc5ac531a166dc6a873dfa4756c0ca8ee1223b3` |
| `b11-a535-s1-A20.pcap` | 5,356,160 | `8e07888e2ba37232fb64e48c5236ea39046199db0fa0c1e7b8e7877a610b0463` |
| `b11-a535-s1-R01.pcap` | 209,072 | `970a213ab53c7797e463ae3ffb23dcaba88e0db65a08d7339bba73ee7b8eaba9` |
| `b11-a535-s1-R02.pcap` | 208,964 | `c743c09453ab8669b74523b5fe5708a27c53bc2850405a346d35d3ecb628ab84` |

| Lane file | SHA-256 |
|---|---|
| Probe source, `o653_probe.cpp`, as built for s1 | `2d8079e3d4cdcfcdc2613331419cd450add0f4aa7b6b0572a40d476e982be8c5` |
| Probe binary, s1 | `eafd3eb518ff4f0dd66816d9c6e567fecf62bc09dcb009d5949688d872fc133d` |
| Probe source, as built for s0b | `3821d3d54a653d8cee2d6c0642dc9ace9ee1c2d05332adccff2ee2468b95bb80` |
| Probe binary, s0b | `305884f608be621292d3c721862ca397c4ee0fa26ed29c26141bf7fd7a17b36f` |
| The header taken from the source tree | `3d09fa6968b6f3564b56b3aeaee6f37b23cf8db6adcade3317b0d7d64a8d35ce` |
| Session driver, `run_o653.py` | `4ee7b9c49edbc2f4d0b1a79ce468dcc4742064d4bb2055a59a8fcce3c6e055b6` |
| Lane grader, `o653_grade.py` | `435ddc80daed242582f05ef095f34758b0a9152516bdd5fc0a0c7a9c627d22e9` |
| Provided decoder, `tap_order_decode.py`, unchanged | `144fce57549660363320c626d94ee3a2dc3131122fa9a2048b93dca7ebeea5cf` |

The lane packet holds the probe's and the driver's logs, both decoders'
outputs per capture, the identity gate, the baselines and the restore
transactions.

The probe was built three times:

- **s0**, the first control session, bound nothing. The probe misread the
  library's status text, "Success." with a full stop, and ended the cycle
  before the bind.
- **s0b** ran C0 on the second build, with that fixed. Its lock wait compared
  MEDIA_LOCKED with the value before the bind, which holds only for a
  session's first cycle, as C0 was.
- **s1** ran on the third build. Its lock wait accepts any update after the
  bind with MEDIA_LOCKED above MEDIA_UNLOCKED, because the DUT resets the
  counters at a bind. Nothing else changed.
