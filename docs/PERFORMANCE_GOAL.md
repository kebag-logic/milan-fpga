# Throughput goal — ≥200 Mbit/s RX *and* TX, reach for 1 Gbit/s

**North star for the performance campaign on the fully-FPGA Milan NIC** (Alinx AX7101,
dual VexiiRiscv RV64IMA @100 MHz, 64-bit datapath, MTU 1500 everywhere).

## The goal

1. **Sustain ≥ 200 Mbit/s best-effort TCP in *both* directions** (RX and TX) at MTU 1500.
2. **Reach toward 1 Gbit/s (PHY line rate)** on both directions wherever the hardware allows.

The NIC's PHY is 1 GbE and the 64-bit datapath has ample raw bandwidth (3.2 Gbit/s @ 50 MHz,
6.4 Gbit/s @ 100 MHz), so 1 Gbit/s is a *system* problem (CPU per-frame cost, DMA latency,
memory latency), not a wire limit. Every step is measured on silicon with HW counters +
CPU profile side by side — no blind changes.

## Where we are (measured on silicon, 2026-07-07)

| path | best measured | goal ≥200 | bound by | fix in flight |
|------|:-------------:|:---------:|----------|---------------|
| TX TCP single, 50 MHz datapath | 145–186¹ | ✗/≈ | **TX datapath** (CBS shaper grant latency, 60% stall) | ran datapath at 100 MHz → below |
| TX TCP single, 100 MHz datapath | **238–247** | ✔ | datapath **stall 39%** + ring-empty **idle 39%** (CPU) — **NOT** the reader² | — (met) |
| RX TCP single (RSC on) | **209** | ✔ | per-frame CPU (amortized by RSC) | — (met) |
| RX TCP −P2 (2-queue fan-out) | **223** | ✔ | scales across harts | — (met) |
| UDP TX | 19.5 | ✗ | no TSO (per-frame) | USO offload (not built) |
| UDP RX | 40 (84% loss @300M) | ✗ | no coalescing for UDP | UDP-GRO offload (not built) |

¹ 145 unpinned / 186 pinned-SSH with HW-TSO zerocopy; the datapath-input probe proved the
50 MHz shaper stage was the wall.
² **MEASURED 2026-07-07** on `build_dp100_p0` (reader latency/starve probes, `phase0_measure.sh`,
two runs, rsc250 hwtso+rsc_clk_mhz=100, hash_sel=1): TX **238/247 Mbit/s, 0 retr**. Reader is only
**3.8% busy**; `L_pay = 45 cyc` (450 ns, NOT the ~140 assumed); prefetchable read-latency stall is
only **~13%** and interconnect depth (`rxw_out_hi`) is **2**. So **reader prefetch was refuted** —
the walls are datapath back-pressure (`stall` 39%) and CPU/ring-empty (`idle` 39%). Full evidence:
`docs/TX_READER_PREFETCH_PLAN.md` (MEASURED VERDICT + Appendix A). "Never assume, always measure."

**Status vs goal:** RX **meets ≥200** (209/223 on the 50 MHz gateware; single reverse flow on the
100 MHz build measured ~187–193 here — re-confirm 2-queue once RxSteer is fixed at 100 MHz). TX
now **meets ≥200** (238–247 measured, was mis-attributed to the reader at 172). **1 Gbit/s is not
yet reached on any TCP path** — the remaining TX levers are `stall` (datapath per-frame grant) and
`idle` (CPU TX-queue rate), NOT the reader. UDP is far below and is a separate (offload) problem.

## Why we are not at 1 Gbit/s yet — the bottleneck map

The datapath is never the raw-bandwidth limit (64-bit × 50–100 MHz ≫ 1 Gbit). The real walls,
in the order they surface as load rises:

- **TX ≤ ~186:** the 50 MHz CBS-shaper stage adds per-frame grant latency (datapath-input
  probe: 60% stall). Raising the datapath to 100 MHz halved that (→27% stall) and moved the
  wall to the **RingDMAReader**, which is serial/latency-exposed — one outstanding coherent
  DMA read at a time (70% starve). See `RX_FANOUT_AND_TX_CEILING.md`, `tx-datapath-limit`.
- **RX per-frame CPU cost:** each RX frame pays DMA cache ops + skb alloc + stack traversal;
  a single flow saturates one hart in `sys` at ~40 Mbit/s. **RSC** (HW receive coalescing)
  amortizes this and lifts single-flow RX to 209; the 2-queue fan-out reaches 223. Beyond
  that, the ceiling is CPU per-frame cost again.
- **Memory latency is the deep limit** (`LATENCY_INVESTIGATION.md`): **1424 ns/miss**
  (≈50% TLB walk + 50% DRAM), DDR3-800, 32 KB L2. Both directions are ultimately gated by
  how fast a 100 MHz RV64 core can touch uncached DMA memory per frame.

## Roadmap toward 1 Gbit/s (ordered, each independently measurable)

1. ~~**TX reader prefetch (primary TX lever)**~~ — **REFUTED by measurement (2026-07-07)**, do
   not build. Phase-0 measured `L_pay=45 cyc` (not ~140), prefetchable stall ~13%, interconnect
   depth 2, and TX already 238–247 (≥200). The reader is 3.8% busy — not the wall. The actual TX
   levers toward 1 Gbit are: **(a) datapath per-frame grant latency** (`stall` 39% — a best-effort
   passthrough fast-path in `traffic_controller_802_1q` to bypass classify/queue/CBS-grant when
   unshaped) and **(b) CPU TX-queue rate** (`idle` 39% — the ring runs empty; cut per-descriptor
   xmit cost / batch doorbells). See `TX_READER_PREFETCH_PLAN.md` MEASURED VERDICT.
2. **Recover 100 MHz timing margin:** the isolated 100 MHz datapath closed at only **+0.010 ns**
   and **2-queue RxSteer hangs** at that clock. Pipeline the worst path / floorplan the milan
   region to buy slack, then run *both* directions at 100 MHz with the fan-out intact.
3. **Cut RX per-frame cost further:** wire a completion IRQ (drop the hrtimer poll), scale the
   RX fan-out to more queues/harts, and lean on RSC + GRO. Toward line-rate RX needs either
   fewer frames (bigger coalescing) or more parallel harts.
4. **Attack memory latency:** faster DRAM (DDR3-800 → higher), bigger/smarter L2, huge-page or
   pinned DMA arenas to cut the 50% TLB-walk component. This is what ultimately unlocks 1 Gbit.
5. **UDP offloads (separate track):** USO (TX segmentation) + UDP-GRO (RX) to bring UDP off the
   per-frame path. Until then UDP is inherently ~20 (TX) / ~40 (RX) Mbit/s.
6. **More/faster cores:** a higher-clock or higher-IPC RV64 (or >2 harts) shortens the per-frame
   critical path directly — the single biggest lever, at the cost of timing closure.

## Detailed investigations (read these for the evidence)

| topic | doc |
|-------|-----|
| HW-TSO, single-flow ceiling, RX fan-out, datapath-input probe, 100 MHz datapath | `docs/RX_FANOUT_AND_TX_CEILING.md` |
| Memory-latency root cause (1424 ns/miss), floorplan/clock experiments | `docs/LATENCY_INVESTIGATION.md`, `docs/SINGLE_PORT_PERF.md` |
| RX RSC coalescing + `ethtool -C rx-usecs` (default 250 µs) | `../the-private-test-repo/fpga/kl-eth/README.md` |

## Ground rules for this campaign

- **MTU stays 1500** everywhere. Best-effort TCP is the primary metric.
- **Measure both HW and SW at every step** — `milan_tlm` counters (incl. the datapath-input
  and RX-pipeline probes) read alongside `/proc/stat` + `/proc/profile`; "the books must balance."
- **Verify the driver identity** (`MODULE_VERSION`) and measure over a clean path — console
  garble and stale drivers have produced phantom regressions before.
