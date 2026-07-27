# Reference-device timestamp errors — root-caused 2026-07-27

The third-party reference listener on the bench was reported to be "showing a
lot of error-counter increase". This page verifies that on silicon, decodes
**every** counter by name, samples repeatedly to separate *large* from
*increasing*, and follows the chain to a root cause.

**Headline.** The errors are real, they are **increasing at ~8,000/s**, and
**we are the cause** — but *not* in the way that was suspected. The talker RTL
stamps correctly. The clock it is handed does not: the Arty board's PHC is
**216,446 s (60.1 h) away from the domain gPTP time**, and its `ptp4l` is
pinned at the hardware's ±1 % maximum frequency adjustment, slewing toward a
target it can never reach. Every AAF frame we send carries a presentation
timestamp from that clock, so the reference device flags **99.4 % of received
frames** LATE or EARLY.

Nothing on the bench was reflashed, rebooted or reconfigured to produce this
page. Every number below is a read.

## Contents

- **[Verdict](#verdict)** — The one-table answer: which counters move, at what rate, and the attribution chain from the reference device's stream input back to our Arty talker and its unsynchronised PHC.
- **[Method: the counters were read without la_avdecc](#method-the-counters-were-read-without-la_avdecc)** — Why the library was bypassed rather than fought, and the 24-byte AECP command that replaces it. Includes the two traps that cost time: ADPDU field offsets and the raw socket that silently sees nothing.
- **[The reference device's counters, every name, sampled seven times](#the-reference-devices-counters-every-name-sampled-seven-times)** — All 12 STREAM_INPUT counters plus AVB_INTERFACE, CLOCK_DOMAIN and STREAM_OUTPUT, with first/last/delta over 361 s. Three counters move; everything else is frozen. Note what is **zero**: no sequence gaps, no interruptions, no resets — delivery is perfect, only time is wrong.
- **[Attribution: the stream is ours](#attribution-the-stream-is-ours)** — Two independent matches that close the loop — the stream ID and destination MAC the listener is bound to, and our talker's own FRAMES_TX ticking at 7,999.9/s against the listener's 7,992/s.
- **[Root cause: the talker's clock, not the talker's logic](#root-cause-the-talkers-clock-not-the-talkers-logic)** — The measurement that separates the two hypotheses. Our AX board's transmitted timestamps hold constant against the domain clock; the Arty's PHC is 60 hours out and slewing at the ±1 % rail. Includes the `ptp4l` log line that names the mechanism.
- **[The sweep signature](#the-sweep-signature)** — Why the split is not "all late" but alternating blocks of 100 % LATE and 100 % EARLY, measured at 20 s cadence. Also the one number that does *not* close, recorded honestly rather than smoothed over.
- **[Why this is a regression against the 07-24 record](#why-this-is-a-regression-against-the-07-24-record)** — The grandmaster reboots; the PHC counts from boot, not from an epoch; a slew-only client can never re-acquire. The offset is measured *growing*, which is what makes this a trap rather than a transient.
- **[What to change](#what-to-change)** — Three candidate fixes with the measurement that would confirm each. Deliberately not applied — this was a read-only lane.
- **[Reproduce it](#reproduce-it)** — The exact command sequence, including our own CSR snapshot protocol and the `phc_ctl` trick that measures PHC frequency error with no network round-trip in the loop.

## Verdict

| Question | Answer | Evidence |
|---|---|---|
| Are the reference device's error counters large? | Yes — LATE 15,504,725 / EARLY 15,461,125 against FRAMES_RX 31,193,745 | `GET_COUNTERS`, STREAM_INPUT.0 |
| Are they *increasing*? | **Yes.** LATE +1,224,760 and EARLY +1,643,521 over 361 s | 7 sweeps, 60 s apart |
| Which ones? | `LATE_TIMESTAMP`, `EARLY_TIMESTAMP`, `FRAMES_RX`/`TIMESTAMP_VALID`. **All others frozen.** | table below |
| How bad? | LATE+EARLY = **99.4 %** of frames received | 2,868,281 / 2,885,168 |
| Is anything else wrong with the stream? | **No.** `SEQ_NUM_MISMATCH` 0, `STREAM_INTERRUPTED` 0, `MEDIA_RESET` 0, `MEDIA_UNLOCKED` 0, `UNSUPPORTED_FORMAT` 0, `TIMESTAMP_UNCERTAIN` 0 | same sweeps |
| Is the stream ours? | **Yes.** stream_id `0200000000020000`, dmac `91:e0:f0:00:10:31` — our Arty talker | `GET_STREAM_INFO` both ends |
| Are *we* the cause? | **Yes** | rate match + clock measurement |
| Is it our talker RTL? | **No.** Our AX board's transmitted timestamps track the domain clock to a constant offset | CRF vs PHC, 55 s |
| Then what? | The Arty's **PHC is 216,446 s off the domain** and slewing at the ±1 % rail | direct PHC reads + `ptp4l` log |

## Method: the counters were read without `la_avdecc`

The project has a standing trap on record: the `la_avdecc` probe SIGSEGVs
unless its build feature-defines match the library's. Rather than re-fight
that, the counters were read with a **~200-line raw-socket AECP controller**.
This turned out to be strictly better: no ABI surface, full control of the
decode, and it cross-checks byte-for-byte against our own CSR block (see
[Reproduce it](#reproduce-it)).

The AEM `GET_COUNTERS` command is 24 bytes on the wire and needs no library:

```
dst=<target MAC>  src=<our MAC>  ethertype 0x22F0
  byte 0      subtype              0xFB          (AECP)
  byte 1      sv/version/msg_type  0x00          (AEM_COMMAND)
  bytes 2-3   status<<11 | control_data_length   (= 24)
  bytes 4-11  target_entity_id
  bytes 12-19 controller_entity_id (any unique value)
  bytes 20-21 sequence_id
  bytes 22-23 u<<15 | command_type = 0x0029      (GET_COUNTERS)
  bytes 24-27 descriptor_type, descriptor_index
```

The response carries `counters_valid` (a 32-bit bitmap) followed by a fixed
**32-word counter block**; bit *N* of the bitmap says word *N* is meaningful.
The bit→name mapping is per descriptor type (1722.1-2021 Tables 7-155..7-158,
Milan 5.3.8.10). Decoding it is the whole job — an undecoded block is what
makes 5 M late frames look like a healthy datapath.

Two traps worth writing down:

* **ADPDU field offsets.** `entity_capabilities` is at byte 20, not 24;
  `talker_stream_sources` at 24, `listener_stream_sinks` at 28,
  `available_index` at 36, `gptp_grandmaster_id` at 40. A 4-byte shift still
  parses and still produces plausible-looking numbers — it reported the
  reference device as 10 talker sources when it has 4.
* **A raw `AF_PACKET` socket sees nothing** until it joins the group. AVDECC
  control needs `PACKET_ADD_MEMBERSHIP` on `91:E0:F0:01:00:00`; stream
  multicast needs its own group or `PACKET_MR_PROMISC`. `tcpdump` works only
  because it sets promiscuous mode for you — so "tcpdump sees it, my tool
  doesn't" is this bug, every time.

A third trap cost a full measurement: **the socket receive queue is a
backlog**. Sleeping 5 s between `recv()` calls returns 5-second-old frames,
one per iteration. The first pass through the clock comparison showed the
transmitted timestamp "falling behind real time by 5 s every 5 s" — which was
purely the queue draining. Drain to empty *before* sampling.

## The reference device's counters, every name, sampled seven times

Target entity `3CC0C60102030000`, 4 talker sources / 10 listener sinks,
firmware `1.00.06`. Seven `GET_COUNTERS` sweeps 60 s apart, span **361 s**.

**STREAM_INPUT.0** — `counters_valid = 0x00000FFF` (the Milan set plus
`TIMESTAMP_VALID`/`TIMESTAMP_NOT_VALID`):

| Counter | First | Last | Δ over 361 s | Rate | Verdict |
|---|---:|---:|---:|---:|---|
| `MEDIA_LOCKED` | 1 | 1 | 0 | — | static |
| `MEDIA_UNLOCKED` | 0 | 0 | 0 | — | static |
| `STREAM_INTERRUPTED` | 0 | 0 | 0 | — | static |
| `SEQ_NUM_MISMATCH` | 0 | 0 | 0 | — | static |
| `MEDIA_RESET` | 0 | 0 | 0 | — | static |
| `TIMESTAMP_UNCERTAIN` | 0 | 0 | 0 | — | static |
| `TIMESTAMP_VALID` | 28,308,577 | 31,193,745 | +2,885,168 | 7,992/s | **increasing** |
| `TIMESTAMP_NOT_VALID` | 0 | 0 | 0 | — | static |
| `UNSUPPORTED_FORMAT` | 0 | 0 | 0 | — | static |
| `LATE_TIMESTAMP` | 14,279,965 | 15,504,725 | +1,224,760 | 3,392/s | **increasing** |
| `EARLY_TIMESTAMP` | 13,817,604 | 15,461,125 | +1,643,521 | 4,552/s | **increasing** |
| `FRAMES_RX` | 28,308,577 | 31,193,745 | +2,885,168 | 7,992/s | **increasing** |

Everything else on the device is frozen or empty:

| Descriptor | Counters | Verdict |
|---|---|---|
| `ENTITY.0` | — | `NOT_SUPPORTED` (legal; Milan does not require it) |
| `AVB_INTERFACE.0` | `LINK_UP` 1, `LINK_DOWN` 0, `GPTP_GM_CHANGED` 2 | all static |
| `AVB_INTERFACE.1` | `LINK_UP` 1, `LINK_DOWN` 0, `GPTP_GM_CHANGED` 0 | all static |
| `CLOCK_DOMAIN.0` | `LOCKED` 0, `UNLOCKED` 0 | static |
| `STREAM_INPUT.1`..`.9` | all ten counters | **all zero, all samples** |
| `STREAM_OUTPUT.0`..`.3` | `STREAM_START`, `STREAM_STOP`, `MEDIA_RESET`, `TIMESTAMP_UNCERTAIN`, `FRAMES_TX` | **all zero** |

Read the zeros as carefully as the large numbers. `SEQ_NUM_MISMATCH` = 0 over
31 M frames means **not one frame was lost or reordered**. `MEDIA_LOCKED` = 1
with `MEDIA_UNLOCKED` = 0 means the sink locked once and never dropped out.
`LINK_DOWN` = 0, `GPTP_GM_CHANGED` = 2. The transport is flawless. The only
thing wrong with our stream is the number we write in the timestamp field.

That also disposes of the "it's a big historical count" reading: this is not
history. It is happening now, at 8,000 frames per second.

## Attribution: the stream is ours

`GET_STREAM_INFO` on the reference device's `STREAM_INPUT.0`:

```
stream_id                 0200000000020000
stream_dest_mac           91:e0:f0:00:10:31
stream_format             0205022000806000
msrp_accumulated_latency  137042
flags                     0xFE000086   (CONNECTED | FAST_CONNECT | SAVED_STATE | NO_SRP)
```

`GET_STREAM_INFO` on our Arty board's `STREAM_OUTPUT.0`:

```
stream_id                 0200000000020000
stream_dest_mac           91:e0:f0:00:10:31
msrp_accumulated_latency  750000
```

Same stream ID, same destination MAC. `0200000000020000` is
`{Arty MAC 02:00:00:00:00:02, uid 0}` — our talker, by construction.

The rates close independently. Our Arty's `FRAMES_TX` over a 60.2 s window:

```
2,842,929,767 -> 2,843,411,391   = +481,624 = 7,999.9 frames/s
```

against the reference device's `FRAMES_RX` at 7,992/s. That is the same
stream, and it is the **only** stream the reference device has ever received —
its other nine stream inputs have never counted a single frame.

One more confirmation, from the negative side: **the stream is invisible on
the bench host's port.** A 30 s AVTP subtype census there returned 2,987 CRF,
6 ADP, 4 MAAP, 3 AECP and **zero AAF**, and a filter on the destination MAC
`91:e0:f0:00:10:31` captured 0 packets in 12 s. The switch is forwarding the
stream only to the registered listener — correct behaviour, and the reason
this fault is invisible to a packet capture taken at the obvious place.

## Root cause: the talker's clock, not the talker's logic

The standing hypothesis was that our presentation timestamps are wrong —
specifically `transit_ns_i` in
[`hdl/ieee1722/aaf/aaf_talker_i2s.sv`](../../hdl/ieee1722/aaf/aaf_talker_i2s.sv),
the offset added to the PHC timestamp:

```systemverilog
ts_r <= ptp_ns_i[31:0] + transit_ns_i;
```

**That logic is correct, and it was measured to be correct.** Our AX board
emits a CRF stream continuously, whose timestamps come from the same PHC. The
bench host runs `ptp4l` synchronised to the AX grandmaster at **rms 33–80 ns**,
so its PHC *is* the domain clock. Comparing the two, twelve samples over 55 s:

```
crf_ts - phc =  +1.927, +1.569, +1.836, +1.886, +1.780, +1.893,
                +1.816, +1.818, +1.721, +1.883, +1.901, +1.846  ms
```

Mean **+1.82 ms**, no trend. That is the 2 ms presentation offset, behaving
exactly as designed; the ±0.18 ms spread is userspace scheduling jitter
between `recv()` and `clock_gettime()`, not the device. The RTL adds the right
offset to the clock it is given.

The clock it is given on the **Arty** is the problem. Three PHC reads taken
back-to-back:

| Clock | Reads |
|---|---:|
| AX board PHC (the grandmaster) | 11,096.456 s |
| Bench host PHC (`ptp4l`-disciplined) | 11,106.300 s |
| **Arty board PHC** | **227,547.526 s** |

The Arty is **216,446 s — 60.1 hours — ahead of the domain it claims to
follow.** And it does claim to follow it: the Arty's own ADPDU advertises
`gptp_grandmaster_id = 020000FFFE000001`, the AX. So this is *not* a
grandmaster-election disagreement. Both ends agree who the master is; the
Arty's clock is simply nowhere near the master's time.

Its `ptp4l` names the mechanism itself:

```
ptp4l: rms 82040485458461 max 82040489937806 freq +10000000 +/- 0 delay 404 +/- 0
ptp4l: rms 82040475350480 max 82040479778907 freq +10000000 +/- 0 delay 405 +/- 0
```

* `rms 82040485458461` — the offset from master is **82,040 seconds**.
* `freq +10000000` — parts-per-billion, i.e. **+1 %**: the hardware's maximum
  frequency adjustment, **saturated**, and constant (`+/- 0`).
* Successive lines close the gap by ~10.1 ms/s. At that rate, 82,040 s of
  offset needs **95 days**.

`ptp4l` is *slewing*, never *stepping*, because the board's `/etc/gptp.cfg` is
`clientOnly 1` with no `step_threshold`.

Confirmed independently, with no network in the loop: `phc_ctl` prints
`CLOCK_MONOTONIC` in its own log bracket, so one command yields both clocks.
Over 264.504 s of monotonic time the Arty's PHC advanced 261.858 s:

```
261.858382789 / 264.504 = 0.9899963   ->  -10,004 ppm  =  -1.0004 %
```

Exactly the ±1 % rail, sustained. The Arty's PHC is being dragged at maximum
rate, permanently, and the talker stamps every frame from it.

## The sweep signature

If the offset were merely constant, every frame would be late *or* every frame
early. Instead the cumulative counts sit near 50/50, which is the interesting
part. Sampling `STREAM_INPUT.0` every 20 s for 484 s resolves it:

| t (s) | FRAMES/s | LATE/s | EARLY/s | late % | early % |
|---:|---:|---:|---:|---:|---:|
| 20 | 8,039 | 7,924 | 115 | 98.6 | 1.4 |
| 41 | 7,657 | 0 | 7,657 | 0.0 | 100.0 |
| 61 | 8,041 | 0 | 8,041 | 0.0 | 100.0 |
| 81 | 8,039 | 0 | 8,039 | 0.0 | 100.0 |
| 101 | 8,045 | 0 | 8,045 | 0.0 | 100.0 |
| 121 | 8,037 | 3,050 | 4,565 | 37.9 | 56.8 |
| 141 | 8,037 | 8,037 | 0 | 100.0 | 0.0 |
| 161 | 8,042 | 244 | 7,797 | 3.0 | 97.0 |
| 181 | 8,049 | 4,516 | 3,111 | 56.1 | 38.6 |
| 201 | 8,056 | 8,056 | 0 | 100.0 | 0.0 |
| 222 | 7,660 | 7,660 | 0 | 100.0 | 0.0 |
| 242 | 8,040 | 8,040 | 0 | 100.0 | 0.0 |
| 262 | 8,041 | 8,041 | 0 | 100.0 | 0.0 |
| 282 | 8,038 | 571 | 7,467 | 7.1 | 92.9 |
| 302 | 8,049 | 0 | 8,049 | 0.0 | 100.0 |
| 322 | 8,044 | 0 | 8,044 | 0.0 | 100.0 |
| 342 | 8,039 | 0 | 8,039 | 0.0 | 100.0 |
| 362 | 8,045 | 2,376 | 5,248 | 29.5 | 65.2 |
| 382 | 8,042 | 8,042 | 0 | 100.0 | 0.0 |
| 403 | 7,660 | 7,660 | 0 | 100.0 | 0.0 |
| 423 | 8,047 | 8,047 | 0 | 100.0 | 0.0 |
| 443 | 8,041 | 8,041 | 0 | 100.0 | 0.0 |
| 463 | 8,044 | 2,723 | 5,321 | 33.8 | 66.2 |
| 483 | 8,041 | 0 | 8,041 | 0.0 | 100.0 |

A square wave: blocks of **100 % EARLY**, a short mixed transition, blocks of
**100 % LATE**, and back. This is the AVTP timestamp field — the low 32 bits of
the nanosecond count, wrapping every 4.294967296 s — sliding through the
listener's acceptance window because the two clocks run at different rates.
When the modular offset is in the "future" half the verdict is EARLY; in the
"past" half, LATE. The ~50/50 cumulative split is just the time-average of that
square wave, which is why an absolute counter read tells you nothing and the
cadence is the measurement.

**One number does not close, and is recorded rather than smoothed.** At the
measured −1.0004 % drift, a 2³² ns wrap predicts a half-period of
4.294967296 / 2 / 0.010004 ≈ **215 s**. The observed half-period is **~90 s**,
about 2.4× faster; the sample at t = 161 s also breaks the monotonic pattern.
So the sweep is real and the mechanism is established, but the exact period is
not fully accounted for by PHC drift alone. Candidates not yet excluded:
additional per-frame jitter in the stamped value, or a second rate error
between the Arty's PHC and its monotonic reference. This does not affect the
verdict — the clock is 60 hours out either way — but it should not be written
up as understood when it is not.

The mechanism behind this signature — why a huge offset alternates rather than
biasing, and why no listener-side heuristic can recover the truth from it — is
drawn out with timing diagrams in
[`../design/PRESENTATION_TIME_WRAP.md`](../design/PRESENTATION_TIME_WRAP.md).
That page also derives the observed half-period from the table above (90.62 s
against 214.66 s predicted) and leaves the 2.4x gap open rather than closing
it.

## Why this is a regression against the 07-24 record

The 2026-07-24 record has this path at **E2E = pto = 500 µs with 0 LATE**. The
difference is not in the RTL. It is uptime:

| Board | Uptime at test | PHC |
|---|---:|---:|
| AX (grandmaster) | 11,052 s (3.1 h) | 11,096 s |
| Arty (talker) | 355,551 s (4.1 d) | 227,548 s |

The PHC counts **from boot, not from an epoch**. When the grandmaster reboots,
the domain's time jumps backwards by the grandmaster's entire previous uptime.
A client configured to slew and never step cannot follow that jump — it can
only close the gap at 1 % of real time.

The offset is measured **growing**, which is what makes this a trap rather
than a transient. The Arty's `ptp4l` log recorded an offset of **82,040 s** at
board uptime 246,802 s; the direct PHC comparison now reads **216,446 s**. Over
the ~30 h between those two observations the offset increased by ~134,000 s.
It is diverging, not converging — each grandmaster restart adds to it faster
than the ±1 % rail can remove it.

`GPTP_GM_CHANGED` corroborates: **112** on the Arty, against **2** on the AX
and **2** on the reference device.

## What to change

Not applied — this was a read-only lane. Each is stated with the measurement
that would confirm it.

1. **Let the Arty's `ptp4l` step.** Its `/etc/gptp.cfg` is `clientOnly 1` with
   no `step_threshold`, so it slews only. Setting a step threshold (or
   `step_threshold 1` as the bench host already uses on its own `ptp4l`
   invocation) lets it re-acquire in one correction instead of 95 days.
   *Confirm by:* PHC difference to the grandmaster < 1 µs, then
   `LATE_TIMESTAMP`/`EARLY_TIMESTAMP` deltas going to zero over a 5-minute
   sweep.
2. **Gate the talker on clock validity.** Today we transmit at full rate with
   a PHC 60 h out and advertise `TIMESTAMP_UNCERTAIN` = 0 while doing it. A
   talker whose local clock is not synchronised to the domain should either
   not stream or should set the uncertainty bit. *Confirm by:* the reference
   device's `TIMESTAMP_UNCERTAIN` counter moving instead of its LATE/EARLY
   pair.
3. **Consider whether the PHC should survive a grandmaster restart at all.**
   The reboot-resets-time-to-zero behaviour is what creates the jump. This is
   a design question, not a bug fix, and is listed only so it is on the record.

## Reproduce it

Counters, both ends, purely over the network:

```sh
# reference device — the full 32-word block, decoded by name
avdecc_ctl --mode sweep --target-eid 0x3CC0C60102030000 \
           --target-mac 3c:c0:c6:01:02:03 --n-in 10 --n-out 4
# which stream the sink is bound to
avdecc_ctl --mode streaminfo --target-eid 0x3CC0C60102030000 \
           --target-mac 3c:c0:c6:01:02:03 --n-in 3 --n-out 1
```

Our own board exposes the same ten counters over CSR, but **only after arming
the snapshot** — a direct read returns zeros and looks like a dead counter
block:

```sh
devmem 0x90000800 32 0x0     # A_STRM_SEL  : stream 0, listener
devmem 0x90000804 32 0x1     # A_STRM_SNAP : latch
devmem 0x90000804 32         # poll until busy = 0
# then A_STRMW_CNT0..9 at 0x830 + 4k, in the documented order
```

The snapshot latches, so the ten reads are mutually consistent even though
each `devmem` call costs ~0.75 s. This path was cross-checked against AECP
`GET_COUNTERS` on the same board and agrees exactly —
`LATE_TIMESTAMP 0x012FAA66` = 19,901,030, `EARLY_TIMESTAMP 0x0126C7DE` =
19,318,750, `FRAMES_RX 0x0257D8B3` = 39,311,539.

PHC frequency error, with no network round-trip in the measurement loop —
`phc_ctl` prints `CLOCK_MONOTONIC` in its own bracket, so one command gives
both clocks and the ratio falls out of the first and last lines:

```sh
for i in $(seq 1 24); do phc_ctl /dev/ptp0 get; sleep 10; done
# phc_ctl[<monotonic>]: clock time is <phc>
```

Do **not** try to measure this by reading the board's PHC over `ssh` and the
domain PHC locally: the round-trip is ~9 s, which swamps a 1 % drift over any
practical baseline. That attempt returned −5,333 ppm ± 3,700 against the
−10,004 ppm the local method resolves cleanly.
