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
- **[What the controller library reported](#what-the-controller-library-reported)** -- Compatibility flags, diagnostics and counter state held by the library across the session, and what its one counter check can detect.
- **[The control capture](#the-control-capture)** -- A disconnect whose order is known, which the order check must read as counters first.
- **[The CRF input before PR #655](#the-crf-input-before-pr-655)** -- The 100 ms window in which an unbound CRF input still reads locked.
- **[Bench as left](#bench-as-left)** -- The state at the end against the start, and the residuals.
- **[Limits](#limits)** -- What these runs do not show.
- **[Artifact hashes](#artifact-hashes)** -- The captures, the probe and the lane tools.
- **[#653 bench: disconnect order with the controller library, VLAN build, 2026-10-05](#653-bench-disconnect-order-with-the-controller-library-vlan-build-2026-10-05)** -- The VLAN library cycles, sequence windows and restoration readbacks.

## #653 bench: disconnect order, 2026-10-04

The owner's report is **not reproduced** on this bench. In all 23
disconnects, 20 of the AAF input, 2 of the CRF input and 1 control, the
UNBIND_RX response left the DUT's port first. The la_avdecc controller library
flagged nothing in any of them. Its one counter check accepts either order, so
that silence is not evidence about the order; see
[What the controller library reported](#what-the-controller-library-reported).

| #653 acceptance | On this image | Evidence |
|---|---|---|
| 1. The UNBIND_RX response leaves before the counters notification that reports the unlock, for AAF and CRF and each input | Held, 23 of 23 | Response 7.5 µs after the command every time. The unlock's GET_COUNTERS follows 114.2 to 116.8 µs later on the AAF input 0, and 99.3 and 99.7 ms later on the CRF input 1. See [Per-cycle results](#per-cycle-results). |
| 2. A bench capture of a disconnect, with a control that fails the check | Done | One tap capture per disconnect, each read response first by the lane grader and by the provided decoder. In the control, the check reads counters first against the probe's own GET_COUNTERS. See [The control capture](#the-control-capture). |
| 3. MEDIA_LOCKED = MEDIA_UNLOCKED after the unbind; STREAM_INTERRUPTED does not count it | AAF held; CRF not at every instant | AAF: the first push after the unbind reads 1/1, STREAM_INTERRUPTED 0. CRF: 1/0 until the silence timeout, then 1/1, as expected before PR #655. See [The CRF input before PR #655](#the-crf-input-before-pr-655). |
| 4. A controller session connects and disconnects 20 times with no counter error | No miscount flagged by the library; not a test of the order | One la_avdecc session ran 20 AAF and 2 CRF cycles. No compatibility change, diagnostic, query error or lost notification. The library's one counter check accepts MEDIA_LOCKED = MEDIA_UNLOCKED or MEDIA_UNLOCKED + 1 in any connection state, so it could flag neither order nor the CRF 1/0 window. The Hive application, the only remaining source of the owner's flag, was not run. See [What the controller library reported](#what-the-controller-library-reported). |

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
| Static descriptor bytes over AECP | Equal to the build's AEM image, except the three live-state fields below; the scripted gate reports FAIL on exactly those three |
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

**The library's counter check, and what it can detect.** The library has one
check on a STREAM_INPUT's counter values. At tag `v4.3.1.1`, commit
`6d61a92e`, the tag the probe was built against, it is
[`src/controller/avdeccControllerImpl.cpp:1611-1613`](https://github.com/L-Acoustics/avdecc/blob/6d61a92e7f264c69f23cdc38f50d31114e567aa0/src/controller/avdeccControllerImpl.cpp#L1611-L1613),
in the function that stores every counters update for an input. For a Milan
entity it removes the Milan flag, with the message "Invalid MEDIA_LOCKED /
MEDIA_UNLOCKED counters value on STREAM_INPUT" and the citation Milan 1.3
clause 5.3.8.10, only when MEDIA_LOCKED is neither equal to MEDIA_UNLOCKED nor
one more than it. The input's connection state is not an input to the check.
The library's one other use of MEDIA_UNLOCKED,
`src/controller/avdeccControllerImplHandlers.cpp:35`, lists the counters a
Milan input must carry. The bench's source tree describes itself as that tag,
and the header taken from it equals the tag's copy.

So the check accepts 1/1 and 1/0 whether the input is bound or not. It can
flag neither order of the UNBIND_RX response and the unlock's push, nor the
CRF input's 1/0 window below. Every counters update the library delivered in
these sessions carried 0/0 or 1/0 while the input was Connected, or 1/1 while
it was NotConnected, and the check accepts all three. It raised no event in
any cycle, but that means no miscount was flagged; it is not evidence about
the order.

The flag the owner saw therefore cannot come from this library check. It must
come from the Hive application's own rules, which this lane did not run.

## The control capture

C0 ran in its own short session with the same probe. After the hold, the
auxiliary entity sent GET_COUNTERS for STREAM_INPUT 0 and waited for the
answer, LOCKED 1, UNLOCKED 0, before the session sent UNBIND_RX. The order on
the wire is therefore known.

Both decoders show it: the probe's GET_COUNTERS command and response, then
the UNBIND_RX command and response, then the unsolicited GET_STREAM_INFO and
GET_COUNTERS. The UNBIND_RX command left 1,629.8 µs after the probe's own
GET_COUNTERS answer, and its response 1,637.3 µs after it.

Run against the probe's own GET_COUNTERS answer instead of the unlock's push,
the order check reads COUNTERS_FIRST. A counters frame ahead of the response
is therefore detected, and the check can fail. Against the unlock's push, C0
reads RESPONSE_FIRST, like every other cycle. The control exercises that
comparison only, not the grader's selection of the unlock's push among the
DUT's unsolicited frames.

## The CRF input before PR #655

The image predates [PR #655](https://github.com/kebag-logic/milan-fpga/pull/655),
which counts a locked CRF input's unlock at the bind fall. As expected, the
DUT counted the CRF unlock only at its 100 ms silence timeout. It pushed it
99.3 and 99.7 ms after the UNBIND_RX response.

In that window the library held the CRF input at MEDIA_LOCKED 1,
MEDIA_UNLOCKED 0 while showing it NotConnected: for 95.0 ms in R01 and
100.0 ms in R02. That 1/0 was the update delivered one second after the bind,
while the input was Connected. No counters update for the input reached the
library inside either window; the next one carried 1/1.

The library's counter check runs only on an update, and it accepts 1/0 in any
connection state. So it had nothing to judge inside the window, and could not
have flagged the window even with an update there. No miscount was flagged,
inside the window or when 1/1/0 arrived; that is not evidence that a
controller tolerates the window.

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
  controller reports, and its one counter check cannot flag the order. The
  owner's session used the Hive application on top of it, so Hive's own rules
  are the only remaining source of the owner's flag. Hive was not run here, and
  the owner's Hive and library versions are not known to this lane.
- **The library check read from source.** Its condition was read in the
  public source at the build's tag, not in the bench's installed binary.
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

## #653 bench: disconnect order with the controller library, VLAN build, 2026-10-05

Operator [A543]; Refs #653. These are operator observations.

The [B12 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993102892) extends [PR #659](https://github.com/kebag-logic/milan-fpga/pull/659).
The flashed image remains dev `bbf704ec`.

The four assigned ATDECC identity checks passed.
The findings branch starts at `fa450d301805881ad713b67521477bf042ddadfd`.

### B12 method and interpretation

The controller host built library commit `a71ffa997c21fea9f2c73ee40e99770a33475c7a`.
Both linked libraries report version `5.0.0-beta1`.

The high-level session subscribed to both entities.
An auxiliary entity read formats and counters.

Every bind checked both current stream formats.
Every pair already matched; no format change was needed.

The error rule follows Hive commit `a13db9d97009dca49a00fb299805e379131dafb3`.
Its source is `libs/modelsLibrary/controllerManager.cpp:730-796`.

MEDIA_UNLOCKED counts only with the input Connected.
STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, LATE_TIMESTAMP, EARLY_TIMESTAMP and UNSUPPORTED_FORMAT count increases unconditionally.

The probe preserves cache initialization and reset handling.
Connection state is sampled within the library callback.

Eight rule controls passed; an inverted predicate failed.
The full graphical application was outside this method.

Seven fixed holds received five repetitions per direction.
AAF and CRF each received that complete matrix.

Fixed holds run from bind completion to unbind submission.
Actual wire durations include callback and submission latency.

Forty additional cycles bracket observed input-counter push boundaries.
Their actual durations appear separately below.

A fixed duration cannot independently choose its push phase.
Boundary cycles therefore supplement the requested fixed-duration matrix.

Boundary targets bracket the observed cadence by 25 ms.
The tables report measured timing, including controller latency.

The peer's push phase varied relative to bind completion.
Its boundary holds consequently differed from the DUT's.

Every cycle captured the DUT link through unbind completion.
A companion capture retained VLAN-tagged stream frames.

The specified plain filter alone excludes those tagged frames.
Both captures retain the tap's 28-byte record header.

Peer-directed unicast notifications require the controller-side control capture.
Each interval uses one capture's clock exclusively.

ACMP matching checks controller, listener, input and sequence identifiers.
Counter matching checks target, input, controller and unsolicited status.

The last pre-unbind observation supplies the MEDIA_UNLOCKED baseline.
This includes auxiliary readbacks before delayed first peer pushes.

Raw bytes corrected inherited decoder column assumptions.
Eight ordering controls passed, including a reversed-order failure control.

### B12 specification references

| Reference | Applied rule |
|---|---|
| IEEE 1722.1-2021, Sections 8.2.1, 8.2.4 and 8.2.5 | Match the ACMP response and interpret status zero as SUCCESS. |
| IEEE 1722.1-2021, Sections 7.4.42, 7.4.42.2.4 and 7.5 | Decode STREAM_INPUT counters and distinguish unsolicited notifications. |
| Milan v1.2, Section 5.3.8.10, Table 5.6 | Reset counters at bind; interpret unlock, interruption and sequence counters. |
| Milan v1.2, Sections 5.4.5.1 and 5.4.5.2, Table 5.22 | Account for the one-second notification rate limit. |
| Milan v1.2, Sections 5.5.2.5 and 5.5.3.5.45, Table 5.36 | Apply controller unbind behavior and the listener's SUCCESS response. |
| IEEE 1722-2016, Sections 4.4.4.6 and 10.4.6 | Accept arbitrary initial sequence numbers; check modulo-256 progression. |
| IEEE 1722-2016, Sections 4.4.4.3, 4.4.4.5, 4.4.4.7 and 4.4.4.9; Clause 7 | Decode AAF timestamps, validity, uncertainty and media-reset fields. |

### B12 outcome and classification

The reported disconnect order was not reproduced.
All 182 unbinds returned SUCCESS with response-first ordering.

Every unlock update found the library input NotConnected.
Hive therefore counted zero MEDIA_UNLOCKED errors.

Both sequence windows completed without mismatches or interruptions.
The first-PDU checks also remained clear.

| Classification | Observation |
|---|---|
| DUT sends wrong order | None observed across 91 DUT-listener unbinds. |
| DUT sends wrong status | None observed; all 91 DUT-listener responses report SUCCESS. |
| Legitimate event | Controlled unbinds produced unlock notifications after responses. No observed unlock increase preceded its unbind command. |
| Peer behaviour | The peer returned SUCCESS in all 90 peer-listener short cycles and its long window. It reported timestamp-counter increases, detailed below. |

Counts include 140 fixed holds and 40 boundary controls.
Two ten-minute windows supply the remaining unbinds.

CRF retains the previously documented delayed-unlock behavior.
These observations concern the image preceding PR #655.

The notification limit can add another second of delay.
That delay preserves the observed response-first ordering.

### B12 per-cycle tables

A means reference peer to DUT.
B means DUT to reference peer.

R means the response precedes the unlock notification.
NC means the library reported NotConnected at that update.

Intervals are microseconds; actual holds are milliseconds.
Zero denotes no increment under the implemented Hive rule.

A intervals use the DUT-link tap.
B intervals use the controller-side control capture.

#### B12 A AAF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| A0300-1 | 300 / 302.212 | SUCCESS | R / 697287.022 | NC | 0 |
| AAAF0300-2 | 300 / 302.801 | SUCCESS | R / 696519.351 | NC | 0 |
| AAAF0300-3 | 300 / 302.869 | SUCCESS | R / 696534.254 | NC | 0 |
| AAAF0300-4 | 300 / 302.945 | SUCCESS | R / 696428.971 | NC | 0 |
| AAAF0300-5 | 300 / 302.922 | SUCCESS | R / 696474.388 | NC | 0 |
| AAAF0600-1 | 600 / 603.064 | SUCCESS | R / 396366.064 | NC | 0 |
| AAAF0600-2 | 600 / 603.046 | SUCCESS | R / 396330.640 | NC | 0 |
| AAAF0600-3 | 600 / 602.996 | SUCCESS | R / 396434.112 | NC | 0 |
| AAAF0600-4 | 600 / 603.086 | SUCCESS | R / 396347.160 | NC | 0 |
| AAAF0600-5 | 600 / 602.861 | SUCCESS | R / 396564.641 | NC | 0 |
| AAAF0900-1 | 900 / 903.011 | SUCCESS | R / 96463.960 | NC | 0 |
| AAAF0900-2 | 900 / 903.056 | SUCCESS | R / 96406.344 | NC | 0 |
| AAAF0900-3 | 900 / 903.026 | SUCCESS | R / 96473.272 | NC | 0 |
| AAAF0900-4 | 900 / 903.020 | SUCCESS | R / 96495.201 | NC | 0 |
| AAAF0900-5 | 900 / 903.081 | SUCCESS | R / 96438.136 | NC | 0 |
| AAAF1000-1 | 1000 / 1002.737 | SUCCESS | R / 996684.408 | NC | 0 |
| AAAF1000-2 | 1000 / 1003.035 | SUCCESS | R / 996505.429 | NC | 0 |
| AAAF1000-3 | 1000 / 1002.956 | SUCCESS | R / 996627.510 | NC | 0 |
| AAAF1000-4 | 1000 / 1002.919 | SUCCESS | R / 996634.052 | NC | 0 |
| AAAF1000-5 | 1000 / 1002.886 | SUCCESS | R / 996679.192 | NC | 0 |
| AAAF1100-1 | 1100 / 1102.999 | SUCCESS | R / 896578.879 | NC | 0 |
| AAAF1100-2 | 1100 / 1103.057 | SUCCESS | R / 896539.469 | NC | 0 |
| AAAF1100-3 | 1100 / 1103.028 | SUCCESS | R / 896576.626 | NC | 0 |
| AAAF1100-4 | 1100 / 1102.982 | SUCCESS | R / 896603.715 | NC | 0 |
| AAAF1100-5 | 1100 / 1102.945 | SUCCESS | R / 896666.651 | NC | 0 |
| AAAF1500-1 | 1500 / 1502.891 | SUCCESS | R / 496761.823 | NC | 0 |
| AAAF1500-2 | 1500 / 1503.077 | SUCCESS | R / 496585.142 | NC | 0 |
| AAAF1500-3 | 1500 / 1502.977 | SUCCESS | R / 496621.463 | NC | 0 |
| AAAF1500-4 | 1500 / 1502.855 | SUCCESS | R / 496785.670 | NC | 0 |
| AAAF1500-5 | 1500 / 1503.052 | SUCCESS | R / 496664.865 | NC | 0 |
| AAAF3000-1 | 3000 / 3003.065 | SUCCESS | R / 115.448 | NC | 0 |
| AAAF3000-2 | 3000 / 3003.066 | SUCCESS | R / 116.552 | NC | 0 |
| AAAF3000-3 | 3000 / 3003.099 | SUCCESS | R / 116.056 | NC | 0 |
| AAAF3000-4 | 3000 / 3002.869 | SUCCESS | R / 116.280 | NC | 0 |
| AAAF3000-5 | 3000 / 3002.872 | SUCCESS | R / 114.984 | NC | 0 |

#### B12 A CRF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| ACRF0300-1 | 300 / 300.831 | SUCCESS | R / 698909.558 | NC | 0 |
| ACRF0300-2 | 300 / 300.850 | SUCCESS | R / 698909.137 | NC | 0 |
| ACRF0300-3 | 300 / 300.882 | SUCCESS | R / 698883.415 | NC | 0 |
| ACRF0300-4 | 300 / 301.009 | SUCCESS | R / 698696.478 | NC | 0 |
| ACRF0300-5 | 300 / 300.959 | SUCCESS | R / 698750.321 | NC | 0 |
| ACRF0600-1 | 600 / 601.006 | SUCCESS | R / 398740.353 | NC | 0 |
| ACRF0600-2 | 600 / 601.028 | SUCCESS | R / 398705.481 | NC | 0 |
| ACRF0600-3 | 600 / 600.997 | SUCCESS | R / 398710.319 | NC | 0 |
| ACRF0600-4 | 600 / 600.920 | SUCCESS | R / 398777.537 | NC | 0 |
| ACRF0600-5 | 600 / 600.953 | SUCCESS | R / 398781.695 | NC | 0 |
| ACRF0900-1 | 900 / 900.911 | SUCCESS | R / 98860.025 | NC | 0 |
| ACRF0900-2 | 900 / 901.051 | SUCCESS | R / 98754.776 | NC | 0 |
| ACRF0900-3 | 900 / 900.864 | SUCCESS | R / 98920.424 | NC | 0 |
| ACRF0900-4 | 900 / 900.916 | SUCCESS | R / 1098870.791 | NC | 0 |
| ACRF0900-5 | 900 / 900.874 | SUCCESS | R / 98938.432 | NC | 0 |
| ACRF1000-1 | 1000 / 1001.182 | SUCCESS | R / 998546.534 | NC | 0 |
| ACRF1000-2 | 1000 / 1000.847 | SUCCESS | R / 998953.939 | NC | 0 |
| ACRF1000-3 | 1000 / 1000.932 | SUCCESS | R / 998903.541 | NC | 0 |
| ACRF1000-4 | 1000 / 1000.795 | SUCCESS | R / 999004.483 | NC | 0 |
| ACRF1000-5 | 1000 / 1000.898 | SUCCESS | R / 998919.234 | NC | 0 |
| ACRF1100-1 | 1100 / 1100.886 | SUCCESS | R / 898906.906 | NC | 0 |
| ACRF1100-2 | 1100 / 1100.751 | SUCCESS | R / 898953.714 | NC | 0 |
| ACRF1100-3 | 1100 / 1100.911 | SUCCESS | R / 898907.633 | NC | 0 |
| ACRF1100-4 | 1100 / 1100.832 | SUCCESS | R / 899004.891 | NC | 0 |
| ACRF1100-5 | 1100 / 1100.942 | SUCCESS | R / 898877.122 | NC | 0 |
| ACRF1500-1 | 1500 / 1500.872 | SUCCESS | R / 498942.563 | NC | 0 |
| ACRF1500-2 | 1500 / 1500.940 | SUCCESS | R / 498838.325 | NC | 0 |
| ACRF1500-3 | 1500 / 1500.911 | SUCCESS | R / 498968.947 | NC | 0 |
| ACRF1500-4 | 1500 / 1500.914 | SUCCESS | R / 498863.524 | NC | 0 |
| ACRF1500-5 | 1500 / 1500.937 | SUCCESS | R / 498889.645 | NC | 0 |
| ACRF3000-1 | 3000 / 3000.867 | SUCCESS | R / 99033.528 | NC | 0 |
| ACRF3000-2 | 3000 / 3000.873 | SUCCESS | R / 99481.786 | NC | 0 |
| ACRF3000-3 | 3000 / 3000.987 | SUCCESS | R / 98942.841 | NC | 0 |
| ACRF3000-4 | 3000 / 3000.917 | SUCCESS | R / 99596.234 | NC | 0 |
| ACRF3000-5 | 3000 / 3001.033 | SUCCESS | R / 98231.943 | NC | 0 |

#### B12 B AAF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| BAAF0300-1 | 300 / 304.955 | SUCCESS | R / 694946.000 | NC | 0 |
| BAAF0300-2 | 300 / 300.464 | SUCCESS | R / 35576.000 | NC | EARLY +1 |
| BAAF0300-3 | 300 / 300.925 | SUCCESS | R / 381282.000 | NC | 0 |
| BAAF0300-4 | 300 / 300.539 | SUCCESS | R / 756916.000 | NC | 0 |
| BAAF0300-5 | 300 / 301.067 | SUCCESS | R / 122530.000 | NC | 0 |
| BAAF0600-1 | 600 / 600.758 | SUCCESS | R / 98177.000 | NC | 0 |
| BAAF0600-2 | 600 / 601.282 | SUCCESS | R / 83899.000 | NC | 0 |
| BAAF0600-3 | 600 / 601.163 | SUCCESS | R / 54534.000 | NC | 0 |
| BAAF0600-4 | 600 / 600.803 | SUCCESS | R / 90300.000 | NC | 0 |
| BAAF0600-5 | 600 / 600.529 | SUCCESS | R / 116050.000 | NC | 0 |
| BAAF0900-1 | 900 / 901.180 | SUCCESS | R / 876929.000 | NC | 0 |
| BAAF0900-2 | 900 / 901.072 | SUCCESS | R / 552663.000 | NC | 0 |
| BAAF0900-3 | 900 / 900.873 | SUCCESS | R / 328399.000 | NC | 0 |
| BAAF0900-4 | 900 / 901.208 | SUCCESS | R / 249261.000 | NC | 0 |
| BAAF0900-5 | 900 / 901.206 | SUCCESS | R / 535195.000 | NC | LATE +1 |
| BAAF1000-1 | 1000 / 1000.357 | SUCCESS | R / 581040.000 | NC | 0 |
| BAAF1000-2 | 1000 / 1000.501 | SUCCESS | R / 167042.000 | NC | 0 |
| BAAF1000-3 | 1000 / 1000.726 | SUCCESS | R / 242916.000 | NC | 0 |
| BAAF1000-4 | 1000 / 1000.898 | SUCCESS | R / 213792.000 | NC | 0 |
| BAAF1000-5 | 1000 / 1000.873 | SUCCESS | R / 199687.000 | NC | 0 |
| BAAF1100-1 | 1100 / 1101.291 | SUCCESS | R / 675799.000 | NC | 0 |
| BAAF1100-2 | 1100 / 1100.490 | SUCCESS | R / 616686.000 | NC | 0 |
| BAAF1100-3 | 1100 / 1100.901 | SUCCESS | R / 502440.000 | NC | 0 |
| BAAF1100-4 | 1100 / 1100.976 | SUCCESS | R / 843312.000 | NC | 0 |
| BAAF1100-5 | 1100 / 1100.966 | SUCCESS | R / 394069.000 | NC | 0 |
| BAAF1500-1 | 1500 / 1500.796 | SUCCESS | R / 510157.000 | NC | 0 |
| BAAF1500-2 | 1500 / 1500.964 | SUCCESS | R / 786030.000 | NC | 0 |
| BAAF1500-3 | 1500 / 1501.127 | SUCCESS | R / 41791.000 | NC | 0 |
| BAAF1500-4 | 1500 / 1501.283 | SUCCESS | R / 247615.000 | NC | 0 |
| BAAF1500-5 | 1500 / 1501.410 | SUCCESS | R / 438512.000 | NC | 0 |
| BAAF3000-1 | 3000 / 3000.595 | SUCCESS | R / 179402.000 | NC | 0 |
| BAAF3000-2 | 3000 / 3000.545 | SUCCESS | R / 830662.000 | NC | 0 |
| BAAF3000-3 | 3000 / 3000.506 | SUCCESS | R / 416655.000 | NC | 0 |
| BAAF3000-4 | 3000 / 3000.460 | SUCCESS | R / 142626.000 | NC | 0 |
| BAAF3000-5 | 3000 / 3000.392 | SUCCESS | R / 908773.000 | NC | 0 |

#### B12 B CRF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| BCRF0300-1 | 300 / 303.545 | SUCCESS | R / 649162.000 | NC | 0 |
| BCRF0300-2 | 300 / 304.061 | SUCCESS | R / 989885.000 | NC | 0 |
| BCRF0300-3 | 300 / 303.725 | SUCCESS | R / 310364.000 | NC | 0 |
| BCRF0300-4 | 300 / 304.217 | SUCCESS | R / 646108.000 | NC | 0 |
| BCRF0300-5 | 300 / 303.956 | SUCCESS | R / 901775.000 | NC | 0 |
| BCRF0600-1 | 600 / 604.571 | SUCCESS | R / 877408.000 | NC | 0 |
| BCRF0600-2 | 600 / 604.305 | SUCCESS | R / 953049.000 | NC | 0 |
| BCRF0600-3 | 600 / 603.897 | SUCCESS | R / 933910.000 | NC | 0 |
| BCRF0600-4 | 600 / 604.746 | SUCCESS | R / 889526.000 | NC | 0 |
| BCRF0600-5 | 600 / 604.320 | SUCCESS | R / 870298.000 | NC | 0 |
| BCRF0900-1 | 900 / 905.489 | SUCCESS | R / 490542.000 | NC | 0 |
| BCRF0900-2 | 900 / 904.081 | SUCCESS | R / 196542.000 | NC | 0 |
| BCRF0900-3 | 900 / 903.760 | SUCCESS | R / 62415.000 | NC | 0 |
| BCRF0900-4 | 900 / 904.701 | SUCCESS | R / 843195.000 | NC | 0 |
| BCRF0900-5 | 900 / 904.382 | SUCCESS | R / 609048.000 | NC | 0 |
| BCRF1000-1 | 1000 / 1004.430 | SUCCESS | R / 239548.000 | NC | 0 |
| BCRF1000-2 | 1000 / 1004.328 | SUCCESS | R / 960441.000 | NC | 0 |
| BCRF1000-3 | 1000 / 1004.191 | SUCCESS | R / 546185.000 | NC | 0 |
| BCRF1000-4 | 1000 / 1004.077 | SUCCESS | R / 127249.000 | NC | 0 |
| BCRF1000-5 | 1000 / 1004.021 | SUCCESS | R / 703114.000 | NC | 0 |
| BCRF1100-1 | 1100 / 1104.261 | SUCCESS | R / 193508.000 | NC | 0 |
| BCRF1100-2 | 1100 / 1104.061 | SUCCESS | R / 719521.000 | NC | 0 |
| BCRF1100-3 | 1100 / 1103.968 | SUCCESS | R / 275269.000 | NC | 0 |
| BCRF1100-4 | 1100 / 1103.827 | SUCCESS | R / 821260.000 | NC | 0 |
| BCRF1100-5 | 1100 / 1103.989 | SUCCESS | R / 391770.000 | NC | 0 |
| BCRF1500-1 | 1500 / 1503.900 | SUCCESS | R / 487777.000 | NC | 0 |
| BCRF1500-2 | 1500 / 1504.053 | SUCCESS | R / 608523.000 | NC | 0 |
| BCRF1500-3 | 1500 / 1504.324 | SUCCESS | R / 664399.000 | NC | 0 |
| BCRF1500-4 | 1500 / 1504.530 | SUCCESS | R / 710281.000 | NC | 0 |
| BCRF1500-5 | 1500 / 1503.780 | SUCCESS | R / 771145.000 | NC | 0 |
| BCRF3000-1 | 3000 / 3003.943 | SUCCESS | R / 427275.000 | NC | 0 |
| BCRF3000-2 | 3000 / 3004.510 | SUCCESS | R / 38355.000 | NC | 0 |
| BCRF3000-3 | 3000 / 3004.469 | SUCCESS | R / 689551.000 | NC | 0 |
| BCRF3000-4 | 3000 / 3004.665 | SUCCESS | R / 265408.000 | NC | 0 |
| BCRF3000-5 | 3000 / 3003.459 | SUCCESS | R / 946664.000 | NC | 0 |

#### B12 push-boundary controls

The prior-push column measures push-to-unbind command time.
Before and after refer to the observed one-second cadence.

The prior-push column uses milliseconds.

| Cycle | Phase | Actual hold | Since prior push | Status | Order / interval | State | Hive increments |
|---|---|---:|---:|---|---:|---|---|
| AAAF-edge1025-1 | after | 1028.804 | 29.389 | SUCCESS | R / 970605.895 | NC | 0 |
| AAAF-edge1025-2 | after | 1028.792 | 29.387 | SUCCESS | R / 970607.590 | NC | 0 |
| AAAF-edge1025-3 | after | 1028.738 | 29.325 | SUCCESS | R / 970670.309 | NC | 0 |
| AAAF-edge1025-4 | after | 1028.795 | 29.359 | SUCCESS | R / 970636.940 | NC | 0 |
| AAAF-edge1025-5 | after | 1028.750 | 29.284 | SUCCESS | R / 970710.920 | NC | 0 |
| AAAF-edge975-1 | before | 978.811 | 978.740 | SUCCESS | R / 20531.850 | NC | 0 |
| AAAF-edge975-2 | before | 978.873 | 978.802 | SUCCESS | R / 20469.602 | NC | 0 |
| AAAF-edge975-3 | before | 978.777 | 978.705 | SUCCESS | R / 20608.795 | NC | 0 |
| AAAF-edge975-4 | before | 978.846 | 978.775 | SUCCESS | R / 20518.634 | NC | 0 |
| AAAF-edge975-5 | before | 978.754 | 978.683 | SUCCESS | R / 20652.250 | NC | 0 |
| ACRF-edge1025-1 | after | 1028.800 | 29.237 | SUCCESS | R / 970757.683 | NC | 0 |
| ACRF-edge1025-2 | after | 1028.806 | 29.214 | SUCCESS | R / 970780.873 | NC | 0 |
| ACRF-edge1025-3 | after | 1028.750 | 29.153 | SUCCESS | R / 970841.201 | NC | 0 |
| ACRF-edge1025-4 | after | 1028.743 | 29.150 | SUCCESS | R / 970846.090 | NC | 0 |
| ACRF-edge1025-5 | after | 1029.193 | 29.656 | SUCCESS | R / 970338.914 | NC | 0 |
| ACRF-edge975-1 | before | 978.754 | 978.684 | SUCCESS | R / 1020770.347 | NC | 0 |
| ACRF-edge975-2 | before | 978.784 | 978.714 | SUCCESS | R / 1020747.309 | NC | 0 |
| ACRF-edge975-3 | before | 978.866 | 978.796 | SUCCESS | R / 1020682.637 | NC | 0 |
| ACRF-edge975-4 | before | 978.880 | 978.811 | SUCCESS | R / 1020669.967 | NC | 0 |
| ACRF-edge975-5 | before | 978.766 | 978.696 | SUCCESS | R / 1020783.264 | NC | 0 |
| BAAF-edge1025-1 | after | 910.695 | 29.445 | SUCCESS | R / 970241.000 | NC | 0 |
| BAAF-edge1025-2 | after | 986.069 | 28.306 | SUCCESS | R / 971394.000 | NC | 0 |
| BAAF-edge1025-3 | after | 660.978 | 27.595 | SUCCESS | R / 972165.000 | NC | 0 |
| BAAF-edge1025-4 | after | 825.697 | 26.963 | SUCCESS | R / 972780.000 | NC | 0 |
| BAAF-edge1025-5 | after | 696.411 | 26.167 | SUCCESS | R / 973489.000 | NC | 0 |
| BAAF-edge975-1 | before | 1555.647 | 978.764 | SUCCESS | R / 21000.000 | NC | 0 |
| BAAF-edge975-2 | before | 1740.794 | 977.904 | SUCCESS | R / 21877.000 | NC | 0 |
| BAAF-edge975-3 | before | 1761.063 | 977.038 | SUCCESS | R / 22593.000 | NC | 0 |
| BAAF-edge975-4 | before | 1801.375 | 976.252 | SUCCESS | R / 23463.000 | NC | 0 |
| BAAF-edge975-5 | before | 1805.597 | 975.355 | SUCCESS | R / 24377.000 | NC | 0 |
| BCRF-edge1025-1 | after | 916.006 | 28.850 | SUCCESS | R / 970873.000 | NC | 0 |
| BCRF-edge1025-2 | after | 812.656 | 29.984 | SUCCESS | R / 969781.000 | NC | 0 |
| BCRF-edge1025-3 | after | 890.673 | 27.632 | SUCCESS | R / 972030.000 | NC | 0 |
| BCRF-edge1025-4 | after | 971.132 | 26.696 | SUCCESS | R / 973032.000 | NC | 0 |
| BCRF-edge1025-5 | after | 821.043 | 26.047 | SUCCESS | R / 973652.000 | NC | 0 |
| BCRF-edge975-1 | before | 1331.006 | 978.130 | SUCCESS | R / 21568.000 | NC | 0 |
| BCRF-edge975-2 | before | 1871.031 | 977.361 | SUCCESS | R / 22352.000 | NC | 0 |
| BCRF-edge975-3 | before | 1841.376 | 976.515 | SUCCESS | R / 23243.000 | NC | 0 |
| BCRF-edge975-4 | before | 1890.763 | 975.877 | SUCCESS | R / 23885.000 | NC | 0 |
| BCRF-edge975-5 | before | 1781.683 | 980.562 | SUCCESS | R / 19113.000 | NC | 0 |

### B12 sequence windows

Each window held its AAF binding for ten minutes.
Each listener received 300 scheduled counter polls.

| Cycle | Actual bound ms | SEQ / SI increments | Captured stream frames | Sequence gaps | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---:|---|---:|---|---|
| A-600s | 600005.422 | 0 / 0 | 4,799,477 | 0 | SUCCESS | R / 116.128 | NC | 0 |
| B-600s | 600006.707 | 0 / 0 | 4,798,340 | 0 | SUCCESS | R / 318749.000 | NC | 0 |

Capture reports recorded zero drops on the capture hosts.
Sequence checks cover captured headers, including truncated payload frames.

Each bind also received 20/100/250 ms counter reads.
All 546 early reads showed zero SEQ and SI.

The following examples show arbitrary starting sequence values.
Receipts preserve twelve initial PDUs for every cycle.

| Cycle | First twelve sequence numbers after bind command |
|---|---|
| A0300-1 | 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130 |
| BAAF0300-1 | 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199 |
| ACRF0300-1 | 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38 |
| BCRF0300-1 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 |
| A-600s | 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83 |
| B-600s | 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59 |

### B12 peer observations

The peer reported two timestamp-counter increments during short cycles.
They were EARLY +1 and LATE +1.

| Cycle | Controller callback time, UTC | Library state | Hive increment | Classification |
|---|---|---|---|---|
| BAAF0300-2 | 2026-10-05T11:19:04.049264+00:00 | NotConnected | EARLY +1 | Peer behaviour |
| BAAF0900-5 | 2026-10-05T11:20:10.059350+00:00 | Connected | LATE +1 | Peer behaviour |

These observations identify the reporting listener, not fault ownership.
Timestamp fault attribution remains unresolved.

The library also flagged peer STREAM_INFO reserved bit 24.
See Milan v1.2, Section 5.4.2.10.1.

That compatibility warning is separate from Hive counter increments.
No corresponding DUT compatibility change was observed.

#### B12 startup characterization, 2026-10-05

The [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5994490678) requested retained startup evidence.
This analysis accessed no bench device or lock.

Both increments were already observable before unbind submission.
The table below uses only the controller's clock.

| Cycle | First nonzero read, UTC | Counter / FRAMES_RX | Bind submission to read (ms) | Read before unbind submission (ms) | Read to callback (ms) |
|---|---|---|---:|---:|---:|
| BAAF0300-2 | 2026-10-05T11:19:03.730732Z | EARLY 1 / 68 | 29.880 | 278.656 | 318.532 |
| BAAF0900-5 | 2026-10-05T11:20:09.640696Z | LATE 1 / 67 | 29.947 | 878.672 | 418.654 |

The corresponding pre-bind timestamp counters were zero.
Subsequent early reads retained one through the post-unbind read.

These are observation bounds, not individual offending-packet times.
The NotConnected callback does not date the EARLY event.

Retained captures supply twelve initial AAF headers per selected cycle.
Both flagged cycles and two clean controls were decoded.

All 48 headers have `tv=1`, `tu=0` and `mr=0`.
All use normal timestamp mode, `sp=0`.

Bind-to-PDU intervals and packet spacing use the tap clock.
Presentation steps use signed modulo-2^32 AVTP timestamp differences.

| Cycle | Result | Initial sequence range | Bind command to first PDU (ms) | First two presentation timestamps (hex) | Presentation step, PDU 1 to 2 (ns) | Tap spacing, PDU 1 to 2 (ns) |
|---|---|---|---:|---|---:|---:|
| BAAF0300-2 | EARLY | 184-195 | 20.227033 | d9353fed / d7ccf250 | -23612829 | 125025 |
| BAAF0900-5 | LATE | 30-41 | 20.407250 | 113d7f85 / 3050f58d | 521369096 | 125016 |
| BAAF0300-1 | Clean control | 188-199 | 222.566994 | cdcb2d53 / cdcd159a | 124999 | 123944 |
| BAAF0900-4 | Clean control | 5-16 | 20.091409 | dba7c762 / dba9afa9 | 124999 | 125000 |

The flagged cycles show first-to-second presentation timestamp discontinuities.
Their subsequent ten steps range from 124999 to 125020 ns.

Every clean-control step ranges from 124999 to 125019 ns.
Each twelve-PDU sequence remains consecutive modulo 256.

The tap observes these headers leaving the DUT.
Valid sequence progression does not establish valid presentation timing.

**gPTP correlation: NOT RUN.**
The retained cycle filters select EtherType `0x22f0`.

They retain no gPTP Sync/Follow_Up time reference.
No measured tap-to-gPTP clock mapping is available.

Absolute presentation lead or lag therefore remains unmeasured.
The tap and controller intervals must not be subtracted.

The headers alone cannot assign timestamp fault ownership.
These startup observations feed [#667](https://github.com/kebag-logic/milan-fpga/issues/667).

`startup-headers.json` retains independently decodable, identity-sanitized AVTP headers.
`startup_decode.py` reproduces `startup-analysis.json` from those receipts.

`check_startup.py` matches the earlier sequence receipts and poll rows.
Its controls exercise flag bits, rollover, truncation and timestamp changes.

### B12 restoration and evidence

Both entities match their as-found effective configuration.
The comparison uses successful start and final protocol readbacks.

`restore-start.json` and `restore-end.json` publish all 43 observations.
Each carries its role, descriptor identity, status and effective value.

Source filenames, line numbers, sizes and hashes preserve provenance.
Private entity and transport identities are omitted.

`restore_compare.py` first requires successful responses and the complete inventory.
It then requires effective equality and zero bindings.

Missing, malformed, truncated and duplicate observations are rejected.
The two independent DUT source reads must also agree.

The equal-success control passes with exit zero.
All fourteen adverse controls fail with exit one.

These include changed source selection, binding, format and missing observations.
Matching failures, empty populations and conflicting duplicates also fail.

`restore-controls.json` records every planted control and exit status.

| Role | Bindings | Formats | Maps | Clock sources |
|---|---|---|---|---|
| DUT | Equal (4 observations) | Equal (4 observations) | Equal (2 observations) | Equal (2 observations) |
| Reference peer | Equal (14 observations) | Equal (14 observations) | Equal (2 observations) | Equal (1 observation) |

All streams are unbound.
The DUT servo reads its as-found IDLE state.

AEM clock-source release cleared the CRF-induced holdover.
The original source selection was read back afterward.

NVM image sequence advanced from 98 to 230.
Successful commits advanced from 67 to 199.

Failed commits remained zero; dirty and stale remained clear.
These monotonic counters were retained as observed.

Host prerequisites remained present; the read-only shell check passed.
Remote staging was removed and session deregistration succeeded.

The bench lock is released.
No power, flash, wiring or audio-playback action occurred.

The packet is identified as `653-b12-a543`.
`MANIFEST.sha256` covers its bounded-size receipts and source files.

The round-2 packet audit includes decoded peer identity fields.
Wire receipts replace those identifiers with consistent neutral tokens.

Timing, status, descriptor indices and counter bytes are unchanged.
`redaction-r2.json` records the affected receipts and hashes.

The DUT identity remains permitted by the public ruling.

Raw captures remain outside the packet.
The artifact indexes record their locations, sizes and SHA-256 values.

| Stable artifact | SHA-256 |
|---|---|
| `cycles.csv` | `778b0e16495007ed6190c46666081e50a2d1a9e1e7e5c930dc3d0c08600f6f00` |
| `probe.cpp` | `749836d785ddf462e484a7972c8410a3067c68080be2d914b727515fb3eaf74c` |
| `probe_phase.cpp` | `8d00c3da36a98d4bd0f965594d5e5234e2229d433f187c8467a742bbd4e35365` |
| `wire.py` | `9ab03659da2c77a70aa8f444c96dced18dd03165f94069a5bfe68ce7bbb938c4` |
| `restore-comparison.json` | `c9e4bf1c02d4f3e0ee0d5f59e5a2499c8510471a577a6bc811ce2cfbf561d7ad` |

The sampled cycles bound these conclusions.
They do not establish behavior on other firmware images.
