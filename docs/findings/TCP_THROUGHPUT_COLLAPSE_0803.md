<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# TCP throughput collapse 2026-08-03 - single-hart RV32 CPU saturation, not the RX shield

*Symptom → measurement chain → root cause → what the build should deliver.
Companion tooling: [`scripts/net_throughput_ab.sh`](../../scripts/net_throughput_ab.sh).
Platform history for the numbers this is measured against:
[PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md); knob map:
[RX_PERF_TUNING_MAP.md](RX_PERF_TUNING_MAP.md).*

## Contents

- **[Verdict in one line](#verdict-in-one-line)** — CPU saturation on the single RV32 hart, both directions; the historical 209/223 Mbit/s baseline was a dual-hart RV64 SoC this build no longer has.
- **[The four candidate causes, and how each died](#the-four-candidate-causes-and-how-each-died)** — sender and RX shield ruled out by measurement, `--no-rx-rsc` real but only ~a quarter of the shortfall, the ktimers priority inversion second-order.
- **[The premise that has to be corrected first](#the-premise-that-has-to-be-corrected-first)** — the brief's "85% idle" was `wget`'s own process accounting; `/proc/uptime` shows zero idle seconds across every transfer — 100% compute-bound.
- **[What actually consumes the hart](#what-actually-consumes-the-hart)** — the per-consumer breakdown: dropbear 24.6%, daemon fork/exec churn ~46%, ktimers 13–15%, napi under-prioritized at ~10%.
- **[Bench contamination - THE BENCH WAS NEVER QUIESCENT](#bench-contamination---the-bench-was-never-quiescent)** — a concurrent ALSA audit lane ran through both A/B arms (the A/B had no B), and every polling daemon was duplicated — all absolute numbers are contended-box lower bounds.
- **[The A/B table](#the-ab-table)** — nine lever configurations measured both directions; read the idle% column first (0 everywhere), treat the throughput columns as ordering evidence only.
- **[What this build should deliver, and what it does](#what-this-build-should-deliver-and-what-it-does)** — the sourced derate chain 223 → 209 → ~43 → ~15–20 estimated: the collapse is ~4x contention on top of a ~15x architectural regression that was chosen to make the design fit.
- **[Cost/benefit of the levers](#costbenefit-of-the-levers)** — RSC, the second hart (the largest lever), `rx-usecs`, and the hsplit trap: flipping it without `hs_pgsz=16384` would panic the board.
- **[Recommended fixes, cheapest first](#recommended-fixes-cheapest-first)** — the ordered list from "get a quiet bench" through reaping duplicate daemons, quiet console, the napi priority fix, and killing the fork churn.
- **[Method](#method)** — iperf3 is already on the board (no reflash needed), both directions always measured, and the A/B script's restore-on-exit discipline.

## Verdict in one line

The board is **CPU-saturated on a single RV32 hart**, in both directions. It is
not the RX shield, not the sender, and only ~a quarter of the shortfall is
`--no-rx-rsc`. **The dominant term is that the historical 209/223 Mbit/s numbers
were measured on a *dual-hart RV64* SoC that no longer exists in this build.**

## The four candidate causes, and how each died

| # | Hypothesis | Verdict | The measurement that killed it |
|---|------------|---------|-------------------------------|
| 4 | The sender (`python3 -m http.server` is single-threaded) | **RULED OUT** | Replaced HTTP with `iperf3` entirely (see below - it *is* on the board). Board→peer TX is equally collapsed at 1.40 Mbit/s with no Python anywhere in the path. |
| 2 | The RX shield (`rxsh1-32`) drops unicast | **RULED OUT** | `rx_errors=0`, `rx_missed_errors=0`, `rx_dropped=1595 / 345796 = 0.46 %`, per-queue drops q0 `0xf000303c`=1952 q1 `0xf00030b0`=90 over 9 ks ≈ 0.25/s. The [drop law](RX_PERF_TUNING_MAP.md) needs >5/flow/s. And the collapse is **symmetric** - a shield is RX-only. |
| 1 | `--no-rx-rsc` | **REAL, BUT ONLY PART** | Costs 209→~43 Mbit/s RX by the project's own silicon measurement. Explains a 5x cut, not the 100x observed. Zero effect on TX. |
| 3 | `ktimers/0` at SCHED_FIFO 70 above napi at 50 | **REAL, SECOND-ORDER** | Raising napi above it moved RX 3.07→8.91 Mbit/s and cut retransmits 121→35. But it does not compose with the other fixes, and *hurts* once the shell loops are stopped. |

## The premise that has to be corrected first

> "board-side CPU during the transfer: user 2.6 s, sys 20.1 s out of ~165 s wall,
> so the board is ~85 % IDLE - it is WAITING for data, not compute-bound."

That figure is **`wget`'s own process accounting**. It cannot see softirq, the
napi kernel threads, `ktimers/0`, `dropbear`, or the daemon fork churn - i.e.
nearly all of the CPU this workload actually costs. The machine-wide number is
in `/proc/uptime` field 2, and it says the opposite:

```
idle window across a 10 Mbit/s RX transfer:  8121.43 127.09  ->  8133.71 127.09
                                             ^ +12.28 s wall     ^ +0.00 s idle
```

**Zero idle seconds over the whole transfer, in every configuration tested.** The
board is 100 % compute-bound. At ~10 Mbit/s that is **~1 ms of hart time per
1500-byte frame**.

At rest, with no transfer at all, the hart is still ~88 % busy and **73.5 % of it
is `system` time** (`user 4.9 % / nice 7.1 % / system 73.5 % / idle 12 %`).

## What actually consumes the hart

Measured by per-PID `utime+stime` deltas over timed windows:

| Consumer | Share of the single hart | Note |
|---|---|---|
| `dropbear` (the SSH session doing the measuring) | **24.6 %** | Measuring over SSH on this box perturbs the result more than any knob below. |
| Daemon fork/exec churn (`gptp2csr.sh`, `stream_phc_sync.sh`, `acmp-persist`) | **~46 %** | Idle went **12 % → 58 %** when the three loops were `SIGSTOP`ped. ~5-8 `fork()`/s, ~1100-1500 ctxt/s. Invisible in per-PID sums because the children exit inside the window. |
| `ktimers/0` (SCHED_FIFO **70**) | 13-15 % | Raised by the ALSA lane. |
| `napi/eth*` x2 (SCHED_FIFO **50**) | ~10 % | **Below** both `ktimers/0` (70) and `ptp4l` (80) - a priority inversion against the network path. |
| Concurrent 8-channel `aplay` audit lane | ~4 % + kernel time | See the contamination note below. |

RTT is the corroborating tell - on a direct 1 GbE link, idle:
`min 1.15 / avg 4.85 / max 25.76 ms, mdev 5.18`.

## Bench contamination - THE BENCH WAS NEVER QUIESCENT

Every number in this document was taken on a board that was **already 100 %
CPU-saturated before any TCP traffic was added**. With no transfer running at
all:

```
idle over 6 s, no network load:   9719.77 147.19  ->  9729.83 147.19
                                  ^ +10.06 s wall     ^ +0.00 s idle
```

The cause is a **second lane's long-running audio campaign**, sweeping ALSA
configurations at 120 s each and still going:

```
1351 {batch.sh}     /bin/sh /root/batch.sh
4274 {pcm-audit.sh} /bin/sh /root/pcm-audit.sh -n a6_p512_kt70_schedother -P aplay -p 512 -k 70 ... -T 120
4572 aplay -D hw:Milan,0 -f S32_BE -r 48000 -c 8 --period-size=512 --buffer-size=4096 /tmp/music.raw
```

Consequences, all of which matter:

1. **The original "music playing 2m44.3 s vs music stopped 2m48.2 s - IDENTICAL"
   conclusion does not support "audio load is not the cause."** An
   `aplay`-driven audit was running across both arms, so the audio load never
   actually went away between them. **The A/B had no B.** This must be re-run in
   a genuinely quiet window before "audio is not the cause" can be asserted.
2. The `-k 70` in that campaign's run name is what set `ktimers/0` to FIFO 70 -
   hypothesis 3's precondition is *that lane's sweep variable*, and it changes
   from run to run (`a3_p512_kt70` → `a6_p512_kt70_schedother`).
3. All absolute throughput numbers here are **lower bounds on a contended box**,
   not this build's capability. The mechanism (CPU saturation) is proven; the
   ceiling is not measurable until the bench is quiet.

### Duplicate daemons - doubled fork churn (actionable)

`ps` shows **two copies of each polling daemon**, plus a third:

```
 406 {stream_phc_sync} /bin/sh /usr/bin/stream_phc_sync.sh     <-- boot copy
2531 {stream_phc_sync} /bin/sh /usr/bin/stream_phc_sync.sh     <-- DUPLICATE
 407 {gptp2csr.sh}     /bin/sh /usr/bin/gptp2csr.sh 2          <-- boot copy
2532 {gptp2csr.sh}     /bin/sh /usr/bin/gptp2csr.sh 2          <-- DUPLICATE
2581 {linkmon.sh}      /bin/sh /usr/bin/linkmon.sh
```

Something restarted the Milan init without stopping the boot instances, so the
fork/exec churn measured above - already the largest software consumer of the
hart - is running at **double rate**. Three concurrent `dropbear` sessions
(one per lane) add ~25 % of a hart each while connected.

## The A/B table

`iperf3`, 8-10 s per run, both directions, board as client. **Read the `idle%`
column first**: it is 0 everywhere, which is the whole finding. The throughput
columns move with whatever else the bench was doing at the time and should be
read as ordering evidence, not as calibrated numbers.

| Configuration | RX Mbit/s | TX Mbit/s | idle% | Note |
|---|---|---|---|---|
| as-found (first clean pair) | 3.07 | 1.40 | 0 | TX had **0 retransmits** - not a loss problem |
| napi raised to FIFO 90 | 8.91 | 2.03 | 0 | retrans 121 → 35 |
| shell loops `SIGSTOP`ped | 12.6 | 4.59 | 0 | at-rest idle 12 % → **58 %** |
| loops stopped + napi 90 | 7.33 | 2.26 | 0 | the two levers **do not compose** |
| console `dmesg -n 1` | 9.56 | 2.92 | 0 | 115200-baud UART unblocked |
| loops stopped + console quiet | 9.33 | 2.79 | 0 | |
| `rx-usecs` 5000 → 250 | 10.2 | 4.18 | 0 | driver default is 250, board had 5000 |
| `rx-usecs` 250 → 50 | 9.43 | 2.07 | 0 | 250 is the sweet spot |
| SSH-detached, during audit run `a6` | 2.61 / 1.98 | 0.72 / 0.56 | 0 | worst - the concurrent audio lane had ramped |

The spread across nominally identical conditions (RX 2.6-12.6) is the
contamination described above, not measurement error in the tool.

## What this build should deliver, and what it does

The chain, each step sourced:

| Configuration | RX Mbit/s | Source |
|---|---|---|
| dual-hart RV64 + RSC + 2-queue fan-out | **223** | `[PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md):131` (TX 238-247) |
| dual-hart RV64 + RSC, single flow | **209** | `[PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md):681` |
| dual-hart RV64, **no RSC** | **~43** | `kl-eth.c:221` *"measured TCP RX 43 -> 209 Mbit/s on silicon"*; `milan_soc.py --no-rx-rsc` help: *"expect the pre-RSC ~43 Mbit/s TCP RX regime"* |
| **single-hart RV32, no RSC (this build)** | **~15-20 (estimate)** | Derated, reasoning below - NOT measured, no dual-hart RV32 reference exists |
| **this build, as found on a contended bench** | **~2-10 (measured)** | This document |

The single-hart derate is the step the brief did not account for. `[PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md):112`
records how the historical regime actually ran:

> "Both harts are 100 % (cpu0 all-softirq, cpu1 all-sys/copy)"

The 209/223 regime **required two harts**: one saturated doing softirq/network,
the other saturated doing the `sys`/usercopy half. This build has **one**
(`rv32ima`, `processor: 0` only). Those two 100 %-busy workloads must now
timeshare a single hart, and the `~40 Mbit` pre-RSC figure was itself quoted as
*"a single flow saturates **one hart** in sys"* - i.e. it already consumed a
whole hart while the *other* hart carried everything else. Losing that second
hart is therefore at least a 2x cut on top of the RSC loss, before counting the
RV32 penalty (every 64-bit operation - checksums, byte counters, `div_u64` -
becomes multi-instruction) and before the daemon/SSH/audio load above.

**So: this build should be expected to do roughly 15-20 Mbit/s TCP RX on a quiet
bench, not 223.** It currently does ~2-10 depending on what else is running.
The collapse the user saw is real, but it is ~4x of bench contention on top of a
~15x architectural regression that was *chosen* (RV32 + single hart + no RSC,
all to make the design fit).

## Cost/benefit of the levers

- **`--no-rx-rsc`**: buys back RX 43 → 209 Mbit/s (4.9x) *if the second hart also
  returns*. Costs the LUTs freed for the fit. It is RX-TCP-only: AVTP, gPTP and
  UDP are unaffected (`milan_soc.py` help), which is why the audio path never
  noticed. The driver's `rsc=1` default is harmless on RSC-less gateware by
  design - the CSRs stay present but inert - so **there is no driver/gateware
  mismatch bug here**, contrary to first appearances. Corroborated on the board:
  `rx_bytes/rx_packets = 390468392/345796 = 1129 B/frame`, i.e. plain MTU-and-
  smaller frames. An active RSC engine would show multi-kB average super-segments.
- **Second hart**: the single largest lever, and the one the historical numbers
  actually depended on.
- **`rx-usecs`**: currently **5000**; the driver's own `KL_RX_USECS_DEFAULT` is
  **250**. Measured 250 > 5000 (RX 10.2 vs 9.42, TX 4.18 vs 2.75). Free, runtime.
- **`hsplit=0`**: header-split zero-copy is off. At ~2.5 MB/s md5 and ~40 MB/s
  memcpy on this core, payload copies are expensive, so this looks tempting.
  **Do not flip it as-is - it would panic the board.** The hsq14 capability CSR
  `0xf000311c` (`MILAN_HS_PGSZ_CAP_PHYS`, the elaborated `hs_page_bytes`
  readback) reads **`0x00004000` = 16384**, while the driver's `hs_pgsz`
  parameter is **4096**. That is exactly the STRICT pairing violation that
  DMA-overruns kernel memory and panicked a board on 2026-07-11
  ([RX_PERF_TUNING_MAP.md](RX_PERF_TUNING_MAP.md) step 2). Any `hsplit` experiment
  on this gateware must pass `hs_pgsz=16384` in the same `insmod`.

## Recommended fixes, cheapest first

0. **Get a quiet bench before believing any throughput number.** Stop the
   `batch.sh` audio campaign, reap the duplicate daemons, and hold the link.
   Nothing below is measurable while a 120 s-per-config `aplay` sweep runs.
1. **Reap the duplicate `gptp2csr.sh` / `stream_phc_sync.sh` instances** - free,
   and it halves the largest software CPU term immediately.
2. **Stop measuring over SSH.** `dropbear` costs 24.6 % of the hart. Run the
   client detached (`setsid nohup`) and read the result file afterwards.
3. **`dmesg -n 1` on the bench, or drop the per-frame instrumentation.**
   `kl-eth.c:1374` `netdev_info`s every 2048 frames at KERN_INFO, and
   `/proc/sys/kernel/printk` is **7** with `console=liteuart` - so each line is a
   *blocking* write to a 115200-baud UART. The four `get_cycles()` per RX frame
   (`kl-eth.c:1360-1372`) are unconditional fast-path instrumentation with no
   debug gate; they should be behind one.
4. **Fix the priority inversion**: `napi/eth*` at FIFO 50 sits under `ktimers/0`
   (70) and `ptp4l` (80). Worth ~3x on RX on its own.
5. **Kill the fork/exec churn** - the biggest software term at ~46 % of the hart.
   The three busybox loops re-`fork()` a pipeline of applets every 1-5 s
   (`gptp2csr.sh:325`, `stream_phc_sync.sh:41`, `acmp-persist:290`). Same root
   cause as the [single-hart FIFO starvation](GPTP_GM_LOSS_UNDER_RX_LOAD.md)
   class of defect.
6. **`ethtool -C eth0 rx-usecs 250`** - free, runtime, measured better.

## Method

`iperf3` **is present on the board** (`/usr/bin/iperf3`, v3.21) - the brief's
premise that it is absent and would need a buildroot rebuild + flash is wrong,
and no reflash is needed to measure this. Peer runs `iperf3 -s -p 5201`.

Both directions are always measured: an RX-only defect (shield, RSC) separates
from a symmetric one (CPU, stack) on the first pair of numbers.

[`scripts/net_throughput_ab.sh`](../../scripts/net_throughput_ab.sh) drives the A/B matrix. Every knob it touches is
runtime and reversible, a single EXIT trap restores the as-found posture on any
exit path, and `ptp4l`/`phc2sys` are never touched. **Its absolute numbers on a
contended bench are noise-dominated** (the run recorded here degraded
monotonically as the concurrent ALSA campaign ramped); the one robust signal
across every row is `idle% = 0`.
