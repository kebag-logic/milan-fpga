# Single-port throughput on VexiiRiscv — what a second core would (not) buy

> **This doc is the first slice of a larger investigation.** The "second core won't help /
> latency-bound not CPU-bound" conclusion below is correct, but the root cause was chased
> much deeper afterward — to **memory latency (1424 ns/miss)** with a UDP-flood test that
> shows the CPU *does* saturate at 14k pps, a TLB-vs-DRAM decomposition, the `rx-usecs-low`
> +32 % win, the pointer-writeback, and the 112.5 MHz floorplan. **Read
> [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) for the complete, corrected story.**

**Date:** 2026-07-05 · **Silicon:** AX7101 (XC7A100T-2), VexiiRiscv RV64IMA @ 100 MHz,
sv39 · **Link:** 1000BASE-T copper to an Intel i210 peer (`enp6s0`, 192.168.127.2) ·
**Frame:** MTU 1500 · **Load:** `iperf3` TCP.

## The question

> Improve single-port perf *without changing the processor* — **and only add a second
> core if a second core would actually help.**

To answer honestly you have to find the bottleneck *first*, then check whether more
cores (or a coalescing change) touch it. The answer, measured three independent ways,
is **no — a second core cannot help this workload**, because the single port is not
CPU-bound at all.

## Matrix 1 — baseline single flow

| Direction | Throughput | Latency | Loss | **CPU idle during transfer** |
|-----------|-----------:|--------:|-----:|-----------------------------:|
| RX (peer→board) | 30.1 Mbit/s | — | 0% | **94 %** |
| TX (board→peer) | 26–27 Mbit/s | — | 0% | **94 %** |
| ping (ICMP) | — | 0.87 ms avg | 0% | — |

`vmstat` during a sustained RX transfer: `us 1–3 / sy 2–4 / **id 94** `, ~3130 int/s.
**The core is 94 % idle while the flow runs.** There are no spare-cycle problems to
offload — so there is nothing for a second core to do.

## Matrix 2 — RX-coalesce (poll-cadence) sweep

The rings are IRQ-less and drained by an hrtimer-driven NAPI poll. `ethtool -C eth0
rx-usecs N` (added to `kl-eth`, see below) sets that active poll period directly, so
this sweep spans "spend idle cycles on tight latency" (5 µs) → "batch hard" (1 ms):

| `rx-usecs` | RX Mbit/s | TX Mbit/s | RX retr |
|-----------:|----------:|----------:|--------:|
| 5    | 30.7 | 26.3 | 23 |
| 20 *(default)* | 28.4 | 24.0 | 10 |
| 50   | 29.8 | 26.5 | 16 |
| 100  | 28.8 | 23.8 | 7  |
| 200  | 30.0 | 26.8 | 13 |
| **1000 (1 ms)** | 29.8 | 29.3 | 12 |

**Flat across 200× of coalescing.** 1 ms neither helps nor hurts (all variation is
run-to-run noise). The poll cadence is **not** the bottleneck — so interrupt/poll
coalescing is not a throughput lever here (it *would* be, once many flows saturate the
core; see "When coalescing does matter").

## Matrix 3 — parallel streams (does the ceiling aggregate?)

| Streams | RX aggregate | TX aggregate | CPU idle |
|--------:|-------------:|-------------:|---------:|
| `-P 1` | 30 Mbit/s | 26 Mbit/s | 94 % |
| `-P 4` | 20 Mbit/s | 20 Mbit/s | **95 %** |

Four parallel flows do **not** aggregate — they come in slightly *lower* (per-poll
contention overhead) while the CPU stays 95 % idle. So the ceiling is **not** a
per-flow TCP-window limit either; it is a single serialized limit that more flows
(and therefore more cores) cannot widen.

## Root cause — a per-frame *latency* ceiling, not a *throughput* one

All three matrices point the same way: **~30 Mbit/s single-flow with the core 94–95 %
idle, insensitive to poll cadence and to flow count.** That signature is a fixed
per-frame *latency* on the serialized RX/TX critical path (DMA-ring → NAPI → GRO → TCP
→ ACK), not a shortage of CPU *throughput*:

* It caps a single flow (window ÷ per-frame-latency), which is why parallelism and
  coalescing — both throughput/batching levers — don't move it.
* It leaves the core idle, because the latency is dominated by serialized dependency
  and memory-stall cycles, not by keeping an execution unit busy.

The one variable that changes it is **per-instruction latency of the CPU on that path**:
the identical datapath on **NaxRiscv (dual-issue)** reached **TX 62 / RX 67 Mbit/s at
the same MTU 1500** — ~2.3× higher — precisely because higher IPC shortens the
per-frame critical path. That is *changing the processor*, which this task explicitly
excludes.

### Why a second core is the wrong tool

A second core adds *throughput* (more independent work in parallel). This ceiling is
*latency* on a serialized single-flow path. Adding a core to a 94 %-idle core does not
shorten that path, so **it cannot raise single-flow throughput** — confirmed by Matrix 3,
where even four in-flight flows on the existing core don't aggregate. (Two VexiiRiscv
cores were also measured *not to fit* alongside the 4-GMII switch on the 100T — but the
point stands regardless of budget: for this workload a second core has no work to do.)

### Levers that *would* move single-flow throughput — and why they're out

| Lever | Effect | Status here |
|-------|--------|-------------|
| Higher-IPC / higher-clock core | Shortens per-frame critical path | **Excluded** ("without changing the processor"). A 112.5 MHz / DDR3-900 build *was* later closed and run on silicon (VexiiRiscv's +0.143 ns slack cashed into fmax) and did lift this single flow +25 % — confirming it is **compute/latency-bound, not clock-fixed** — but it worsened memory latency + the flood pps ceiling, so the board runs 100 MHz (see `LATENCY_INVESTIGATION.md` §8). |
| Larger MTU (4074) | Fewer per-frame trips → more bytes per unit latency | Excluded (MTU must stay 1500); measured to reach RX 92 Mbit/s on the same datapath. |
| Second core | More parallel throughput | **No effect** — path is latency-bound & core is idle (this doc). |
| RX coalescing (incl. 1 ms) | Batches per-packet cost | **No effect** on a single idle-core flow (Matrix 2). |

## When coalescing *does* matter (the switch case)

The `rx-usecs` knob is not useless — it's aimed at a workload this single-port test
doesn't create. Once the CPU is the bottleneck (many flows / high pps, e.g. the CPU
terminating management + gPTP + AVDECC while 4 GMII ports pour aggregate traffic at
it), a coarse poll period amortises per-packet overhead and recovers cycles. That is
why the knob exists and is now runtime-tunable — but on a single idle-core flow it is
flat, so the default stays **20 µs** to keep RX-delivery latency low for gPTP/PTP
timestamping. Bump it with `ethtool -C eth0 rx-usecs <µs>` when the control-plane core
actually saturates.

## Bottom line for the switch

Single-port CPU throughput is **the wrong thing to optimise for the AVB switch**: in
the switch role the CPU is the *control plane* (gPTP / AVDECC / management), and
**forwarding runs in the fabric at line rate**, never through this software path. The
~30 Mbit/s software ceiling never gates switched traffic. So: keep VexiiRiscv (it fits
the 4-GMII fabric — the reason we moved off NaxRiscv), keep MTU 1500, and do **not**
spend a core on this. If a pure single-port NIC ever needs the higher number, that is
the NaxRiscv+FPU bitstream (`~/litex-milan/work/fpu32.bit`), not more cores.

## Reproduce

```sh
# on the board (kl-eth ≥ the rx-usecs build):
ethtool -c eth0                      # show coalesce
ethtool -C eth0 rx-usecs 1000        # 1 ms coalescing (runtime)
iperf3 -c 192.168.127.2 -t 8 -R      # RX; drop -R for TX; -P 4 for parallel
vmstat 2 4                           # watch 'id' (idle) during the transfer
```

Driver change: `fpga/kl-eth/kl-eth.c` — `kl->coalesce_us` + `get/set_coalesce`
(`ETHTOOL_COALESCE_RX_USECS`); the active NAPI poll period is `coalesce_us` (default 20).
