<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# The ALSA playback path, measured instead of inferred (2026-08-03)

Everything previously written about why `aplay` stutters or dies on the
AX7101 — the period count, the driver's double copy, `ktimers/0` priority,
"mmap would be zero copies" — was **inferred** from one bit (did aplay
survive?) plus `dmesg`. This page replaces that with an instrumented,
re-runnable measurement of the software path, and the verdict changes in
three places.

Tooling lives in `milan-tests-avb/fpga/audio-audit/` (see its
[README](https://github.com/kebag-logic/milan-tests-avb) for the trap log);
the runner is `run-audit.sh`, the matrix is `matrix.txt`, and every number
below is reproducible with `./run-audit.sh all`.

Board: AX7101, single-hart 100 MHz RV32 VexiiRiscv, Linux 7.0.11
PREEMPT_RT, `snd-kl-milan` version `i4`, 8ch/48k S32_BE out of the
`KL_pcm_tx` playback ring.

## Contents

- **[1. What this board can and cannot be measured with](#1-what-this-board-can-and-cannot-be-measured-with)** — The tooling census, done first because it bounds every claim: no ftrace at all, but `CONFIG_PERF_EVENTS` was already on, so a cross-built `perf` gave a full on-CPU timeline with **no reflash**. Software events only.
- **[2. The instrument](#2-the-instrument)** — `pcm_probe`, an aplay-equivalent that timestamps the path, and what it deliberately does not measure.
- **[3. Survival: what actually kills aplay](#3-survival-what-actually-kills-aplay)** — The A/B table. Two configurations die and they die of *different things*.
- **[4. The mechanism: drain margin, not CPU](#4-the-mechanism-drain-margin-not-cpu)** — The one arithmetic identity that explains every survival result.
- **[5. mmap: the "zero copies" claim is wrong](#5-mmap-the-zero-copies-claim-is-wrong)** — Measured, `aplay -M` saves ~1.5 points of CPU, not 13.
- **[6. Where the hart actually goes](#6-where-the-hart-actually-goes)** — CPU decomposition, and the thief named from the context-switch timeline.
- **[7. Verdict and shipping recommendation](#7-verdict-and-shipping-recommendation)**
- **[8. What this did NOT cover](#8-what-this-did-not-cover)**

## 1. What this board can and cannot be measured with

This is stated first because it is the reason several previous questions
went unanswered rather than answered wrongly.

| capability | state | consequence |
|---|---|---|
| `CONFIG_FTRACE` | **not set** | No `/sys/kernel/tracing`, `mount -t tracefs` fails `No such device`. **No `sched:*` or `hrtimer:*` tracepoints at all.** `perf sched`, `trace-cmd`, latency histograms: unavailable. |
| `CONFIG_PERF_EVENTS` | **=y** | `/proc/sys/kernel/perf_event_paranoid` exists. Only the *binary* was missing. |
| `perf` binary | absent → **cross-built** | Built from `br-milan-rv32/build/linux-7.0.11/tools/perf`, static rv32, 4.0 MB stripped. **No reflash needed** — it is a file copy. |
| hardware PMU | **none exposed** | `CONFIG_RISCV_PMU_SBI=y`, but `perf list` has no `hardware:` section and `perf stat -e cycles` answers *"the cycles event is not supported"*. Software events only. |
| `CONFIG_KALLSYMS` | not set | Kernel samples are raw addresses; symbolize offline against `System.map` ([PERF_ON_MILAN.md](PERF_ON_MILAN.md)). |
| `CONFIG_SCHEDSTATS`, `TASKSTATS` | not set | No `/proc/schedstat`, no delay accounting. **True wakeup→run scheduling latency is not measurable on this kernel.** |
| `cyclictest`, `trace-cmd` | absent | — |

Two rv32-specific fixes were needed to build `perf`: `SYS_futex` does not
exist on rv32 (only the `time64` variant), and `arch/riscv/util/header.c`
trips `-Werror` on a const discard. Both are in `run-audit.sh build-perf`.

**Nothing was reflashed for this work.** The kernel was not rebuilt and no
kernel fragment was changed. That was checked first precisely because a
reflash costs a bench round — and it turned out the only thing missing was
userspace.

### What replaced the missing tracing

Since wakeup→run latency cannot be measured, two things stand in for it, and
the report is careful never to call them that:

* **`pcm_probe`'s wake interval** — the *end-to-end, application-visible*
  period cadence (hrtimer → `ktimers/0` → `snd_pcm_period_elapsed` → wake →
  writer runs). This is the quantity that actually decides whether the ring
  drains, so it is the more useful one anyway.
* **`perf record -a -e context-switches -c 1`** — the core perf software
  event, no tracepoints required. Each record is a task *leaving* the CPU,
  so consecutive records reconstruct a complete single-hart on-CPU timeline:
  who held the CPU, and for how long.

### Observer effect, measured not assumed

* An **interactive `ssh` session costs ~9.6% of the hart** — `dropbear`
  burned 2.6 s of CPU over a 27.2 s window doing softcore crypto for one
  session. (That figure is restated from the raw ticks: the run it came from
  had the tick rate mis-derived as 112/s before the USER_HZ fix below, which
  had under-reported it as 8.6%.) Every measurement window below therefore
  runs **detached** (`setsid nohup`), with no ssh attached.
* **`perf record -a -e context-switches -c 1` costs +1.7 points of CPU** and
  inflates the wake tail. Config `c1` is config `b1` with the recorder
  attached and nothing else changed:

  | | `b1` (no perf) | `c1` (perf ctxsw) | delta |
  |---|---|---|---|
  | periods | 11 258 | 11 258 | — |
  | xruns | 0 | 0 | **none** |
  | wake p50 | 10.632 ms | 10.633 ms | +0.001 ms |
  | wake p99 | 15.09 ms | 16.25 ms | +1.16 ms |
  | late >2× period | 1 | 5 | +4 |
  | process CPU | 28.09% | 29.75% | +1.66 pts |

  **Verdict on trustworthiness:** the median cadence and the xrun count are
  unaffected, so the timeline is sound for *attributing* stalls. The tail
  statistics measured *under* perf are inflated by roughly one millisecond
  at p99 and should not be quoted as the system's own tail — §4 quotes the
  perf-free runs for that.
* `perf record` also lengthens the enclosing script: `c1`'s `/proc/stat`
  window is 279.6 s for a 127.1 s run (perf spends the difference writing
  and folding its 5.8 MB capture), so **`c1`'s per-thread percentages are
  diluted and are not used** — §6 quotes `a4` and `b1`.

## 2. The instrument

`pcm_probe` walks the identical ALSA path as `aplay` — same `hw_params`,
same `sw_params` (`start_threshold = buffer`, `stop_threshold = buffer`,
`avail_min = period`), one period per write — and timestamps it:

* **wake interval** — `CLOCK_MONOTONIC` between successive `snd_pcm_wait()`
  returns.
* **writei time** — time inside `snd_pcm_writei()` when space is already
  available, i.e. the pure cost of the driver's `.copy`.
* **read() time** — the `tmpfs → user buffer` copy, kept separate so file
  I/O is not billed to ALSA.
* **avail / delay** — ring occupancy at each wake.
* **xruns** — every `-EPIPE` with its timestamp and the preceding wake
  interval, plus a `# t0_mono_s` anchor so records join a `perf` timeline.
* **its own CPU** — `getrusage(RUSAGE_SELF)`, because the player exits
  before any external sampler can read `/proc`. That is exactly why aplay's
  own cost had never been measured.

`aplay` is still run for every configuration: `pcm_probe` explains the
mechanism, `aplay` is the shipping question.

## 3. Survival: what actually kills aplay

120 s windows, board otherwise in its normal boot state, detached, player at
`chrt -f 60` unless noted. `/tmp/music.raw` is exactly 120.0 s, so a clean
run ends at EOF; **survival is decided by aplay's own exit status and
whether it printed `write error`, never by the watchdog.**

Every core configuration was run **twice** (pass `a`, repeated as pass `d`),
because an earlier "zero xruns over 85 s" did not reproduce at 115 s.

| period | periods | ktimers/0 | player prio | PipeWire | rep 1 | rep 2 |
|---|---|---|---|---|---|---|
| 2048 | 2 | 1 (RT default) | FIFO 60 | off | `a1` **DIED at 37.9 s**, 1 xrun | `d1` survived, **0 xruns** |
| 512 | 8 | 1 (RT default) | FIFO 60 | off | `a2` survived, 1 xrun (2.1 ms) | `d2` survived, **0 xruns** |
| 512 | 8 | 70 | FIFO 60 | off | `a3` survived, **0 xruns** | `d3` survived, **0 xruns** |
| 512 | 8 | 70 | FIFO 60 | off, `-M` | `a5` survived, **0 xruns** | `d5` survived, **0 xruns** |
| 512 | 8 | 70 | FIFO 60 | **on** | `a4` survived, **0 xruns** | — |
| 512 | 8 | 70 | **SCHED_OTHER** | off | `a6` **DIED**, **480 xruns** | — |

Instrumented, the same picture holds across reps: `b1`/`d6` (rw) and
`b2`/`d7` (mmap) each ran **11 258 periods with zero xruns, twice**.

### The stock death is probabilistic, not deterministic

`d1` is `a1` repeated, same session, nothing changed. **It survived the full
120 s file with zero xruns** (rc 0, no `write error`, 292 fabric ticks ≈
1.5 ms) — where `a1` died at 37.9 s.

| run | config | outcome |
|---|---|---|
| `a1` | p2048, ktimers 1 | **died at 37.9 s**, 1 xrun then `-EIO` |
| `d1` | p2048, ktimers 1 | survived 120 s, **0 xruns** |
| `b3` | p2048, ktimers 1, instrumented | 1 xrun at t=160 ms (recovered; `pcm_probe` recovers where aplay dies) |

So "the stock geometry dies at ~20 s" is not a property of the
configuration — it is a **coin flip per window**. The stock geometry is
*marginal*: it survives unless a stall larger than its 42.7 ms margin
happens to land, and such stalls occur roughly once per 120 s (§4). This is
exactly what the repeat-every-window rule exists to catch, and it means any
"fix" validated on a single surviving run of the stock geometry would have
been a false positive.

Three further results contradict what was previously written down:

1. **`ktimers/0` priority is not what converts fatal into survivable.**
   `a2` runs at the stock PREEMPT_RT `ktimers/0` priority of FIFO 1 — below
   `napi` (50) — and **survives the full file** with a single 2.1 ms xrun.
   The period count alone is what separates `a1` from `a2`. Raising
   `ktimers/0` is still worth doing (it takes xruns from 1 to 0, and §6
   shows it cuts late wakeups from 56 to 1), but it is a *refinement*, not
   the fix.
2. **Stopping PipeWire is not required for survival.** `a4` keeps the whole
   consumer stack running — measured at **21.4% of the hart**
   (`wireplumber` 7.07, `data-loop.0` 6.53 + 1.75, `pw-loopback` 3.13,
   `pw-milan-ring-source` 2.96) — and still takes **zero** xruns. It is
   pure waste and should still be stopped, but it is not load-bearing.
3. **The player's own scheduling class is load-bearing, and nobody had
   tested it.** `a6` at `SCHED_OTHER` took **480 xruns** and died. This is
   the single largest effect in the table, larger than period count.

### The fabric's own view

`snd-kl-milan` reads the `KL_pcm_tx` `PB_UNDER` counter at `TRIGGER_STOP`.
The RTL increments it **once per channel-pair slot per media tick** while the
ring is empty (`hdl/ieee1722/aaf/KL_pcm_tx.sv`, `PT_STEP_S`; the read
pointer is deliberately *not* advanced). At 8 channels that is 4 ticks per
starved 48 kHz frame, so `ms = ticks / 4 / 48000 × 1000` — **derived from
the RTL, not calibrated against a known-length starvation.**

| config | fabric ticks | ⇒ substituted audio |
|---|---|---|
| `a1` (died) | 7 020 + 51 480 | ≈ 305 ms |
| `a2` | 38 616 + 612 | ≈ 204 ms |
| `a3` | 96 | ≈ 0.5 ms |
| `a4` (PipeWire on) | 136 | ≈ 0.7 ms |
| `a5` (mmap) | 68 | ≈ 0.35 ms |

The ~100-tick floor on the clean runs is the stream teardown draining the
ring, not a defect. **Caveat: `under_r` is 16 bits and wraps at 65 536**, so
the large counts are lower bounds mod 65 536, not exact.

### The two deaths are not the same failure

`a1` and `a6` both print `write error: Input/output error`, and that message
has been read as "a bad xrun". It is not. In this kernel `-EIO` has exactly
one source on the playback write path:

```
sound/core/pcm_lib.c:2027, wait_for_avail()
        if (!tout) {
                pcm_dbg(substream->pcm,
                        "%s timeout (DMA or IRQ trouble?)\n", ...);
                err = -EIO;
```

The timeout is **not** the 10 s that older kernels used, and getting this
right matters — read from this tree, not remembered:

```
sound/core/pcm_lib.c:1970, wait_for_avail()
        wait_time = 100;                                  /* ms */
        if (runtime->rate) {
                long t = runtime->buffer_size * 1100 / runtime->rate;
                wait_time = max(t, wait_time);
        }
```

`snd-kl-milan` does not set `substream->wait_time`, so the default path
applies: `buffer_size × 1100 / rate` = `4096 × 1100 / 48000` = **93 ms**,
and `max(93, 100)` = **100 ms**.

So **`-EIO` means: one `writei()` sat for 100 ms without `avail` ever
reaching one period.** An xrun is `-EPIPE`, which `aplay` recovers from; and
the accompanying message is `pcm_dbg`, so with `CONFIG_SND_DEBUG` off it
never reaches `dmesg` — which is why this failure has always looked like it
had no kernel-side evidence at all.

That reading makes both deaths the **same** phenomenon as §4, not a separate
one. The writer blocks only when the ring is nearly full, and it needs
`avail_min` = one period of consumption to make progress:

| period | `twake` | consumption needed within the 100 ms window |
|---|---|---|
| 2048 | 2048 frames | **42.7 ms** |
| 512 | 512 frames | **10.7 ms** |

For the timeout to expire, the writer must go 100 ms without a wakeup that
leaves it enough room — i.e. `snd_pcm_period_elapsed()` (which is what wakes
`runtime->tsleep`) must be starved for longer than 100 ms. The measured
stall distribution has a 60–67 ms maximum per 120 s window (§4), so a >100 ms
excursion is simply the tail of the same distribution, and the large `twake`
at 2 periods is what turns such an excursion into a fatal one instead of a
recoverable one.

**This supersedes the "ten-second freeze ⇒ stalled consumer" reading** that
an earlier draft of this page carried; that draft quoted a remembered
constant instead of reading it, and the conclusion it supported — that `a1`
must be a second, independent defect — does not follow from the real
constant. A dedicated stall hunt (`matrix-followup.txt` pass `f`) still
samples the ALSA runtime status at 5 Hz through repeated `a1`-style deaths,
because the one thing that *would* still indicate a stalled consumer is
`hw_ptr` flatlining while the state stays `RUNNING`. **Result pending at
time of writing.**

## 4. The mechanism: drain margin, not CPU

The instrumented runs make the mechanism arithmetic rather than narrative.

The writer is woken when `avail >= avail_min = period`; at that instant the
ring holds `buffer − period` frames, and the one period it then writes tops
the ring back up to full. So the ring runs dry exactly `buffer` frames after
a write, and the *next* wake was due one period after that write. The
quantity that decides survival is therefore

> **tolerable lateness = buffer − period frames**

— how late a single wake may be before the ring empties. That is measured,
not assumed: `delay at wake` lands on `buffer − period` exactly.

| config | period | buffer | tolerance (frames) | tolerance (ms) | measured `delay` p50 | measured `delay` max |
|---|---|---|---|---|---|---|
| `b3` | 2048 | 4096 | 2048 | **42.7** | 1932 | **2048** |
| `b1` | 512 | 4096 | 3584 | **74.7** | 3518 | **3584** |

The `delay` maxima are `buffer − period` to the frame — 2048 and 3584 — which
is the identity above, measured rather than argued.

The wake-interval distributions, 120 s each:

| config | period | ktimers | periods | xruns | wake p50 | wake p99 | wake max | late >2× |
|---|---|---|---|---|---|---|---|---|
| `b1` | 512 | 70 | 11 258 | 0 | 10.63 ms | 15.09 ms | **66.9 ms** | 1 |
| `b2` (mmap) | 512 | 70 | 11 258 | 0 | 10.65 ms | 15.79 ms | 20.1 ms | 0 |
| `b3` | 2048 | 1 | 2 814 | **1** | 42.70 ms | 51.29 ms | **64.1 ms** | 0 |
| `b4` | 512 | 1 | 11 256 | **1** | 10.72 ms | 19.34 ms | **60.1 ms** | **56** |

Nominal period is 10.667 ms at 512 frames and 42.667 ms at 2048; the p50s
land on nominal to within 0.1%, so **the hrtimer cadence itself is correct**.

The wake *interval* is not directly comparable across geometries — subtract
the nominal period to get the **lateness**, which is the thing the tolerance
budget is spent on:

| config | period | nominal | max interval | **max lateness** | tolerance | headroom left |
|---|---|---|---|---|---|---|
| `b1` | 512 | 10.67 ms | 66.9 ms | **56.2 ms** | 74.7 ms | 18.4 ms |
| `b4` | 512 | 10.67 ms | 60.1 ms | **49.4 ms** | 74.7 ms | 25.2 ms |
| `c1` | 512 | 10.67 ms | 59.7 ms | **49.0 ms** | 74.7 ms | 25.6 ms |
| `b2` | 512 (mmap) | 10.67 ms | 20.1 ms | **9.4 ms** | 74.7 ms | 65.2 ms |
| `b3` | 2048 | 42.67 ms | 64.1 ms | **21.4 ms** | 42.7 ms | 21.2 ms |

Now the survival table falls out of one comparison:

> **Lateness excursions of ~50–56 ms were observed repeatedly** (`b1` 56.2,
> `b4` 49.4, `c1` 49.0). At 8 periods the tolerance is 74.7 ms and they are
> absorbed. **At 2 periods the tolerance is 42.7 ms and any of them is
> fatal.**

The excursions are a property of the *system* — soft-hrtimer service on a
saturated 1-hart RT kernel — not of the geometry, so the same distribution
applies to both. What the geometry changes is only how much of it the ring
can swallow. That is why `a1`/`d1` is a coin flip: a 2-period ring survives
until one of these lands.

Two honest caveats on this table:

* `b3` never actually spent its budget in steady state (21.4 ms of 42.7 ms).
  Its one xrun is recorded with its cause attached —
  `t=160 ms, preceding wake 64 096 µs, avail=2918` — and `avail=2918` means
  the ring held only 1 178 frames (24.5 ms) at the time, i.e. this xrun is a
  **start-up transient**, before the ring first reached full. It is not
  evidence about steady state.
* The 120 s windows here caught max latenesses of 56 ms; the fatal `a1`/`a6`
  events imply excursions beyond 100 ms (§3) that no probe window happened
  to contain. The distribution's tail is therefore **bounded below, not
  characterised** — a longer soak would be needed to state it.

This is why **the binding constraint is neither CPU nor the copy path**.
Both point the other way: the *stock, fatal* geometry is the **cheaper** one.

| config | period | writei p50 | copy duty | read duty | process CPU |
|---|---|---|---|---|---|
| `b3` | 2048 | 3684 µs | 8.54% | 5.09% | **18.12%** |
| `b1` | 512 | 1152 µs | 13.85% | 7.46% | **28.09%** |
| `b4` | 512 (kt 1) | 1145 µs | 12.11% | 6.86% | 34.16% |

Larger periods amortize the per-period syscall/wake overhead (≈230 µs per
period) and cost **10 points less CPU** — and die anyway. Conversely the
surviving configuration is the expensive one. Any story in which playback
fails because the CPU is too slow or the copy too expensive has to explain
that inversion, and cannot.

## 5. mmap: the "zero copies" claim is wrong

The driver's own analysis comment predicts that an mmap-access player
"writes straight into the ring and `.ack` rings the doorbell: **ZERO
copies**", and proposes it as the way to remove `kl_milan_pb_copy()` — which
copies every byte twice — from the profile. Measured, matched 120 s windows:

| config | access | user ms | sys ms | process CPU | writei p50 | copy duty |
|---|---|---|---|---|---|---|
| `b1` | `RW_INTERLEAVED` | 2 898 | 30 810 | **28.09%** | 1152 µs | 13.85% |
| `b2` | `MMAP_INTERLEAVED` (`aplay -M`) | 9 243 | 22 653 | **26.58%** | 995 µs | 12.15% |

**`aplay -M` saves 1.5 points of CPU, not 13.** The kernel's double copy
does disappear — `sys` drops by 8.2 s over the window — but **6.3 s of it
reappears in user space**, because `snd_pcm_mmap_writei()` is still a
`memcpy` from the application's buffer into the ring, and that ring is a
**write-combining** mapping which is slow to write from userspace too. "mmap
access" and "zero copies" are not the same thing for a *file* player: the
bytes have to reach the ring somehow.

The genuine zero-extra-copy configuration — `snd_pcm_mmap_begin()` then
`read()` **straight into the ring**, then `snd_pcm_mmap_commit()` — is
implemented as `pcm_probe -Z` and run in `matrix-followup.txt` pass `e`
against matched controls in the same session. **Result pending at time of
writing.** Its purpose is to establish the floor: if `-Z` is not decisively
cheaper than `b1`, then no amount of copy surgery in the driver changes
playback survival, and lever 2 of the driver's comment should be closed as
*not worth doing*.

Separately, and importantly: **an mmap run being fast is not an mmap run
being correct.** Userspace writes through the WC mapping, and the driver's
own comment records an "mf52 WC-read anomaly" that made byte-granular access
through this mapping untrustworthy — which is precisely why the kernel copy
path bounces through a stack buffer and uses aligned 64-bit stores. This
audit measured **timing only**; audio correctness under `-M`/`-Z` is
untested (§8).

## 6. Where the hart actually goes

Whole-CPU, from `/proc/stat` deltas over the matched windows. `/proc` times
are **USER_HZ = 100**, not `CONFIG_HZ = 250`; the script derives ticks/second
from the measured window rather than assuming either (an early version
assumed 250 and scaled every figure by 2.5×).

| config | user | sys | softirq | **idle** |
|---|---|---|---|---|
| `a2` (p512, kt1) | 8.2% | 74.0% | 17.8% | **0.0%** |
| `a4` (p512, kt70, PipeWire on) | 16.4% | 75.9% | 7.6% | **0.0%** |
| `a5` (p512, kt70, mmap) | 18.5% | 74.8% | 6.7% | **0.0%** |
| `a6` (SCHED_OTHER) | 21.3% | 76.0% | 2.6% | **0.0%** |

The board is at **0% idle in every playback configuration**, including the
ones that never xrun. That is the honest headline: this path works with no
margin to spare.

Per-thread, from `/proc/<tid>/stat` deltas (config `a4`, the loaded case):

| thread | CPU | share |
|---|---|---|
| `ktimers/0` | 29 140 ms | 21.6% |
| `aplay` | 25 320 ms | 18.8% |
| `wireplumber` | 9 540 ms | 7.1% |
| `data-loop.0` | 8 820 ms | 6.5% |
| `napi/eth%d-0` (×2) | 14 630 ms | 10.8% |
| `kcompactd0` | 6 420 ms | 4.8% |
| `pw-loopback` | 4 220 ms | 3.1% |
| `pw-milan-ring-source` | 3 990 ms | 3.0% |
| `ptp4l` + `rcu*` + `irq/13-eth0` + shell loops | — | ≈ 6% |

`ktimers/0` at 21.6% is the largest single consumer — that is the driver's
own period hrtimer plus every other soft timer on the box, and it is the
thread the recipe raises to FIFO 70.

### Naming the thief

The `perf` context-switch timeline (config `c1`) reconstructs every interval
`pcm_probe` was off the CPU and attributes it to whoever held it. On a
single hart that attribution is exact — only one thing runs at a time.

Clean window: 90.5 s, 87 035 switch records, 13 014 off-CPU intervals for
the writer, **mean 6.95 ms, max 25.1 ms**. (The capture is 108 s long but
the last ~17 s are excluded — see the caveat below.)

| comm | held while writer off-CPU | slices | share |
|---|---|---|---|
| `ktimers/0` | 14 641 ms | 21 371 | **23.1%** |
| `napi/eth%d-0` | 13 072 ms | 24 535 | **20.6%** |
| `ptp4l` | 6 032 ms | 4 948 | 9.5% |
| `stream_phc_sync` | 3 474 ms | 1 889 | 5.5% |
| `sleep` | 3 307 ms | 1 695 | 5.2% |
| `pmc` | 3 217 ms | 1 671 | 5.1% |
| `awk` | 2 998 ms | 1 493 | 4.7% |
| `dropbear` | 2 824 ms | 1 431 | 4.5% |
| `rcu_preempt` | 2 291 ms | 5 032 | 3.6% |
| `gptp2csr.sh` | 2 041 ms | 1 079 | 3.2% |
| `irq/13-eth0` | 1 445 ms | 2 689 | 2.3% |
| `devmem` | 1 133 ms | 562 | 1.8% |
| `rcuc/0` | 970 ms | 1 910 | 1.5% |
| `perf` | 754 ms | 346 | 1.2% |

Read this correctly: **most of the writer's off-CPU time is it legitimately
sleeping between periods**, so this table is "how the hart is shared", not
"who stole 100% of it". Three things stand out anyway:

1. **The network RX path is the biggest non-timer consumer** —
   `napi/eth%d-0` 20.6% plus `irq/13-eth0` 2.3% = **22.9%**, on a board
   doing nothing but gPTP and one AVB stream.
2. **The board's own gPTP-publisher shell loop is the next biggest thing on
   the machine.** `gptp2csr.sh` 3.2% *plus the processes it forks every
   iteration* — `pmc` 5.1%, `awk` 4.7%, `sleep` 5.2%, `devmem` 1.8% —
   totals **~20%** of the writer's off-CPU time. A shell script polling with
   `pmc`/`awk`/`devmem` is costing about as much as the entire network stack
   on a board that sits at 0% idle.
3. **The single worst excursion is network-shaped.** The one interval over
   20 ms in the clean window is 25.1 ms at `t=10844.30`, and its occupants
   in order are `napi/eth%d-0 | ktimers/0 | napi/eth%d-0 | ktimers/0 |
   napi/eth%d-0 | napi/eth%d-0` — RX threads at FIFO 50 alternating with the
   timer thread.

**Two caveats, both material.**

* **The tail of the capture is excluded because it is a transfer artifact,
  not a measurement.** The raw analysis initially reported off-CPU intervals
  of 96–156 ms clustered in one ~1 s burst at `t≈10901`, which would have
  been the fatal-class excursion this whole page is looking for. It is not
  real: `t≈10901` is exactly where `pcm_probe` stops appearing in the
  capture, the `perf.data` had been **truncated at 89% by a stalled `scp`**,
  and the probe's own instrumentation for the same run reports a maximum
  wake interval of **59.7 ms** — which a 104 ms off-CPU interval would
  contradict. The instrument disagreeing with itself is the tell; the
  truncated region is discarded and the numbers above are from the intact
  90.5 s.
* **`dropbear` at 4.5% is contamination I introduced.** The matrix runs
  detached precisely so no ssh is attached, but I polled progress during
  this run. It should read ~0 in a clean re-run.

Consistent with all of this, `c1`'s worst clean off-CPU interval (25.1 ms)
is far inside the 74.7 ms tolerance, and `c1` took **zero** xruns. **The
fatal >100 ms class of excursion was not captured in any probe window** —
see §4's second caveat.

## 7. Verdict and shipping recommendation

**Is the software path behaving as designed?** For the shipped `play-milan`
geometry: **yes.** The hrtimer cadence is correct to 0.1%, the writer keeps
the ring at exactly `buffer − period`, and 11 258 consecutive periods ran
with **zero xruns** at 8ch/48k on a 1-hart 100 MHz core at 0% idle.

**The binding constraint is drain margin — `buffer − period` — versus a
60–67 ms worst-case scheduling stall.** It is *not* CPU-bound (the fatal
geometry uses 10 points less CPU than the surviving one), *not* copy-bound
(§5), and not ring-depth-bound in the sense usually meant: the ring is
already 85.3 ms and the *whole* of it is never the margin — the period size
is subtracted from it.

Recommendations, in the order they are worth doing:

1. **Make the survivable geometry the only geometry, in the driver.**
   `periods_min` is 2 in `kl_milan_pb_hw`; the measured-safe configuration
   is 8. A `snd_pcm_hw_constraint_minmax()` on `SNDRV_PCM_HW_PARAM_PERIODS`
   at open (or raising `periods_min`) makes any player that does not know
   the recipe get a survivable buffer by construction. The buffer is pinned
   to the sub-ring either way, so more periods means smaller periods, never
   a larger allocation. **Driver-only, no fabric, no DT.** The follow-up
   pass `e4`–`e7` walks 2/4/8/16 periods at fixed priority to locate the
   knee exactly, so the constant is measured rather than picked.
2. **Set the player's scheduling class, and say so.** `SCHED_OTHER` is the
   biggest single failure lever measured (480 xruns → death) and it is the
   default for anything that is not `play-milan`. This cannot be a driver
   `hw_constraint`; it belongs in the boot overlay and in documentation.
3. **`ktimers/0` at FIFO 70 belongs in the boot overlay** (it already is, in
   `S99milan-audio`). Measured value: late wakeups 56 → 1, xruns 1 → 0.
   Keep it — but its description should stop claiming it converts fatal into
   survivable, because `a2` shows it does not.
4. **Stop PipeWire for host playback** — worth 21.4% of the hart — but
   demote it from "required" to "reclaims a fifth of the CPU". `a4` proves
   playback survives with it running.
5. **Do not deepen the ring for this.** 85.3 ms already exceeds every
   observed stall; what fails is `buffer − period`, and that is fixed for
   free by (1). Ring depth costs a bitstream round (fabric `PB_LEN` + DT +
   driver must move together) and multiplies by stream count. Revisit only
   if the `f`-pass stall hunt shows genuine multi-hundred-ms starvation.
6. **`aplay -M` is not the answer** (§5). Keep the `.copy` path.

**Hedge on the open item:** recommendation (1) attacks the fatal mechanism
from both sides at once, which is why it holds regardless of how the `f`-pass
comes out. More periods raises the drain margin (§4) *and* shrinks `twake`,
so the 100 ms `wait_for_avail` window needs only 10.7 ms of consumption
instead of 42.7 ms (§3). If the `f`-pass nevertheless shows `hw_ptr`
flatlining while the state stays `RUNNING`, that would be a *second,
independent* defect — a stalled consumer rather than a late writer — needing
its own fabric or driver fix, and the ring-depth question in (5) would
reopen. Nothing in (1)–(4) would become wrong; (1) would stop being
*sufficient*.

## 8. What this did NOT cover

Stated explicitly so the gaps are not mistaken for clean results.

* **Audio correctness was never checked.** This is a timing and ring-health
  instrument. Nothing here verifies that the samples reaching the PEER are
  right, and that matters most for `-M`/`-Z`, which write through the WC
  mapping from userspace (§5). No listener-side capture, no THD+N, no
  channel-identity check was run.
* **True wakeup→run scheduling latency is not measurable on this kernel**
  (no `SCHEDSTATS`, no tracepoints). Only end-to-end wake intervals and
  off-CPU intervals were measured, and the report never calls either one
  "scheduling latency".
* **No hardware PMU**, so no cache-miss, IPC, or precise-IP attribution —
  the copy-cost figures are wall-clock, not cycle-accounted.
* **The fabric tick→ms conversion is derived from RTL**, not calibrated
  against a deliberate known-length starvation, and the counter is 16-bit
  and wraps.
* **The `+160 ppm media-clock defect` was deliberately not touched.** It is
  fixed in RTL and awaiting a bitstream, and it is a separate phenomenon
  from ALSA xruns; no attempt was made to attribute anything here to it.
* **Only 8ch/48k/S32_BE** was exercised, only stream 0, only the playback
  direction, only `hw:` (never `plughw:`), and only with `/tmp/music.raw` as
  the source. Capture, multi-stream playback, and format variation are
  untested.
* **Single board, single session.** The core configurations are repeated
  twice (`matrix.txt` pass `d`) because an earlier "zero xruns over 85 s"
  did not reproduce at 115 s; anything reported from a single window is
  labelled as such.
