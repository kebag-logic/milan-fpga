<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# TDM8 link timing at the SoC board: attempt on the ec0cc0c1 image

Refs #451. Operator [A468], 2026-10-01, under the
[bench lane B4 assignment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924192573).

The last open #451 recipe item reads "Scope BCLK, FSYNC and DOUT at the AM62x
end: 12.288 MHz, a one-BCLK FSYNC pulse at 48 kHz, data starting one BCLK
after it". By owner decision it is measured on the SoC board itself, from the
McASP0 receiver. [#626](https://github.com/kebag-logic/milan-fpga/issues/626)
holds the oscilloscope version.

The run stopped before its first SoC board command. The SoC board's serial
console stands at a login prompt, and this lane holds no credential for it.
Without a shell on the SoC board, none of the timing measurements can run.
Nothing was changed on either board.

| #451 timing item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `ec0cc0c1` | PASS | See [Identity and setup](#identity-and-setup) |
| Framing from the SoC board's McASP0 configuration and capture parameters | NOT RUN | No shell on the SoC board. See [Why the run stopped](#why-the-run-stopped) |
| Bit-exact decode of the DUT's frames in all eight slots, in order | NOT RUN | Same |
| fs and BCLK = 256 x fs from a capture of at least 10 minutes | NOT RUN | Same |
| FSYNC pulse width, edge timing, levels and absolute ppm | Not shown by the SoC board | [#626](https://github.com/kebag-logic/milan-fpga/issues/626). See [What the SoC board can and cannot show](#what-the-soc-board-can-and-cannot-show) |

These are operator observations, not review verdicts.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image's identity readback and the bench as found.
- **[Why the run stopped](#why-the-run-stopped)** -- The SoC board's console state, and what was and was not sent to it.
- **[What the SoC board can and cannot show](#what-the-soc-board-can-and-cannot-show)** -- What a McASP0 measurement can establish for each part of the item, and what stays with #626.
- **[Bench as left](#bench-as-left)** -- DUT, controller and SoC board state at the end, against the start.
- **[Rerun](#rerun)** -- What the rerun needs before its first step.
- **[Artifact hashes](#artifact-hashes)** -- The lane packet's evidence files.

## Identity and setup

The DUT runs the image of dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`,
installed on 2026-09-30. The gate repeats the
[#617 bench page](617_DIN_FRAME_COHERENCE_BENCH.md#identity-and-setup)'s
readback, and every value equals that page's.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Live ENTITY and CONFIGURATION | Byte-equal to the AEM bytes the console dumps from QSPI (312 and 106 bytes); entity `020000fffe000001` |
| UART grader | 10 of 10 |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d178f19a` |
| Identity gate | PASS |

This is CRC consistency and descriptor identity, not a configuration SHA-256
readback.

As found, the DUT counters show a reset since lane B3:

- The NVM reads `backed=1`, `dirty=0`, `stale=0` and `pend=0`, with 0
  commits. Slot B, seq 236, is authoritative, as lane B3 left it.
- `PP_STAT` reads `5b000444`, with bit 11 clear.
- `SLIP_TDM` read 33,474 duplicates and 0 skips. Lane B3's page last read
  440.

All 18 queried stream states, the DUT's and the reference peer's, were
unbound, and both DUT audio maps were empty. The DUT selected clock source 0
at 48 kHz and was synchronized, with SYNC=1, ASCAPABLE=1 and TU=0.

`SLIP_TDM` rose by 69 duplicates in 136.3 s across this lane, 0.506 per
second. At one duplicate per frame that is 10.55 ppm, +-0.15 ppm for one
count. It agrees with the
[first-light figure](451_TDM8_FIRST_LIGHT.md#continuity-and-rate) and the
-10.64 ppm divider plan. The counter is the DUT comparing its own two clocks.
It is not a SoC board or pin measurement.

## Why the run stopped

The SoC board's console, which the assigned method uses as a root shell, stood
at a login prompt. The console tool sends one carriage return and one shell
`printf` line. It then waits for that line's output, or for a login or
password prompt. It saw the login prompt and stopped with no command run.
At a login prompt that line can be taken as a login name. No password was
sent, and nothing else reached the console.

The lane holds no credential for the SoC board, and none is recorded in the
project. A key-based remote login over the SoC board's USB network link was
refused. No password was offered. The SoC board answers on that link, and its
USB Audio card is present on the bench host.

Every timing step reads the SoC board's own state or records McASP0, so none
of them can run. The STOP keeps the SoC board as found.

## What the SoC board can and cannot show

This is what a McASP0 measurement can establish, once a shell is available.

- **Data one BCLK after the frame-sync edge.**
  [First light](451_TDM8_FIRST_LIGHT.md#scope-and-identity) read McASP0's
  live configuration. McASP0 runs `dsp_a`, with the codec side as bit-clock and
  frame master, in eight 32-bit slots. In that format the receiver takes the
  first data bit one bit clock after the frame-sync edge. Shifted by one bit
  either way, every pattern word's tag field changes, so no word would decode
  to its own channel. On this image the
  [#617 bench page's DOUT run](617_DIN_FRAME_COHERENCE_BENCH.md#dout-run)
  decoded 3,360,000 frames with 0 torn and 0 invalid words. This lane re-read
  neither the configuration nor the capture parameters. It gives no verdict of
  its own.
- **fs.** The receiver counts frames. Frames received against the SoC board's
  monotonic clock give fs. The uncertainty is the SoC board's crystal
  tolerance plus the timing granularity. #626 puts the crystal at tens of ppm,
  too coarse to resolve the plan's -10.64 ppm.
- **BCLK.** The receiver does not measure the bit-clock frequency, so BCLK =
  256 x fs rests on the master's frame of eight 32-bit slots.
- **Not shown by the SoC board,** and left to
  [#626](https://github.com/kebag-logic/milan-fpga/issues/626):
  - the FSYNC pulse width, since the receiver uses only the frame-sync edge;
  - edge timing: setup and hold of DOUT and FSYNC at the AM62x pins, BCLK
    duty cycle, and rise and fall times;
  - signal levels, overshoot and ringing;
  - the absolute frequency, against a calibrated reference.

## Bench as left

| State | As left |
|---|---|
| DUT | Unchanged. Every control word and `PP_STAT` read the same, and only live counters moved. The census after the STOP equals the start in 32 of 33 entries; the other is the live propagation delay, 385 then 375 ns |
| DUT stream state | All 18 queried stream states unbound; both audio maps empty; no map, bind or control write |
| Controller host | Read commands only; no gPTP daemon started. NIC clock frequency 0 ppb and timestamping off, as found. Staging removed |
| SoC board | No command ran. The console tool's readiness line reached the login prompt. The USB Audio card is present on the bench host. The USB network link answers |
| SoC audio bridge | Not read: no shell |

No flash, reset, power, wiring, instrument or USB function action occurred.

## Rerun

The rerun needs a root shell on the SoC board's console, with the bridge state
known. The assignment can then run unchanged.

A 10-minute capture of eight 32-bit channels at 48 kHz is 921.6 MB. The
earlier lanes stored each capture on the SoC board before copying it off.
Lane B3's DOUT capture log reads 209,560 KiB of temporary storage there, so
this capture has to stream off the SoC board as it records.

## Artifact hashes

This lane made no capture, so there is no raw capture file. The lane packet,
`b4-a468`, holds the redacted per-action evidence and tools. Its manifest
covers every retained file except itself.

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `identity/console-identity.txt` (console CRC, NVM and AEM readback) | 3594 | `64e4bcc457e57809a118ea144f2dcf48287cbfd1dda1c2cc5a8a17dc601c7689` |
| `identity/grader-identity.txt` (UART grader, 10 of 10) | 683 | `5696476b02bf4116ed169d932b499542d9159f7cbe9f49547092cfaca8dea4f4` |
| `identity/identity-aecp-comparison.txt` (ENTITY and CONFIGURATION against QSPI) | 208 | `d4404b599a53ea3264e7b6cd84a0c24051277d54bb93770e572f084ba17b4a78` |
| `restore/census-compare.txt` (census, start against end) | 415 | `74a8280aaf8c418d7bf4d1f1e9a13647131d454c730807f1b0fa4113eee51acd` |
| `soc/start-health.log` (the SoC board console's reply) | 86 | `ed5c18d22b5b970042782486e72c73225aa8bf837d02661071e48d48b4ef2eb4` |
| `summary/summary.json` | 2040 | `9ac066c23e02129d0df9d6afa7376a6f09f5f88edb079a75a124f1be97088726` |
