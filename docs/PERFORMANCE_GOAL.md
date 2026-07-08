# Throughput goal — >500 Mbit/s RX *and* TX, reach for 1 Gbit/s

**North star for the performance campaign on the fully-FPGA Milan NIC** (Alinx AX7101,
dual VexiiRiscv RV64IMA @100 MHz, 64-bit datapath, MTU 1500 everywhere).

## The goal

1. **Sustain > 500 Mbit/s best-effort TCP in *both* directions** (RX and TX) at MTU 1500.
   **Raised 2026-07-07** from the prior **≥200 milestone, now MET** (measured: TX 238–247, RX
   209/223). 500 needs roughly **2×** the current best in each direction.
2. **Reach toward 1 Gbit/s (PHY line rate)** on both directions wherever the hardware allows.

The NIC's PHY is 1 GbE and the 64-bit datapath has ample raw bandwidth (3.2 Gbit/s @ 50 MHz,
6.4 Gbit/s @ 100 MHz), so 1 Gbit/s is a *system* problem (CPU per-frame cost, DMA latency,
memory latency), not a wire limit. Every step is measured on silicon with HW counters +
CPU profile side by side — no blind changes.

## Where we are (measured on silicon, 2026-07-08)

| path | best measured | ≥500? | bound by | next lever toward 500+ |
|------|:-------------:|:-----:|----------|------------------------|
| TX TCP, 100 MHz dp, **CBS unshaped**³ | **339** (−P4) / **354** (2 proc) / 265 single | ✗ (✓200) | **CPU-saturated** (84–96% both harts) | cut per-ACK/reap/wakeup CPU cost; 2nd TX queue; fix the wedge⁴ for stable −P4+ |
| TX TCP, 100 MHz dp, CBS default (historical²) | 238–247 | ✗ | **CBS shaper pacing BE at 300 Mb/s** (config bug — fixed³) | — (fixed) |
| RX TCP single (RSC on) | **209** (50 MHz gw) / 193 (100 MHz gw) | ✗ (✓200) | per-frame CPU, amortized by RSC | bigger RSC coalescing + completion IRQ |
| RX TCP parallel (−P2) | **223** (50 MHz gw, historical) | ✗ | **RX overload wedge**⁴ kills delivery | **fix the wedge first**, then 2-queue fan-out |
| TX TCP single, 50 MHz (historical) | 145–186¹ | ✗ | superseded by the 100 MHz datapath | — |
| UDP TX / RX | 19.5 / 40 | ✗ | no TSO / no coalescing | USO / UDP-GRO offloads (not built) |

¹ 145 unpinned / 186 pinned-SSH with HW-TSO zerocopy; the datapath-input probe proved the
50 MHz shaper stage was the wall.
² **MEASURED 2026-07-07** on `build_dp100_p0` (reader latency/starve probes, `phase0_measure.sh`,
two runs, rsc250 hwtso+rsc_clk_mhz=100, hash_sel=1): TX **238/247 Mbit/s, 0 retr**. Reader is only
**3.8% busy**; `L_pay = 45 cyc` (450 ns, NOT the ~140 assumed); prefetchable read-latency stall is
only **~13%** and interconnect depth (`rxw_out_hi`) is **2**. So **reader prefetch was refuted** —
the walls were datapath back-pressure (`stall` 39%) and CPU/ring-empty (`idle` 39%). Full evidence:
`docs/TX_READER_PREFETCH_PLAN.md` (MEASURED VERDICT + Appendix A). "Never assume, always measure."
³ **CBS root cause, MEASURED + FIXED 2026-07-08.** The 39–42% datapath-input `stall` was the
**802.1Qav CBS shaper actively pacing best-effort traffic**: `milan_csr` reset `CBS_EN_RST=0011`
shaped **q0 at idleSlope 300 Mb/s** while the default class map (`cls_dpcp=0`, `cls_tcq=0xE4`)
routes untagged/BE traffic exactly to q0 — two defaults contradicting each other (the comment even
says BE stays unshaped per REQ-CBS-02). Verified live on silicon (q0 read back idle=0x11E1A300,
en=1), then clearing en via `devmem 0x9000_040C` dropped `tx_dma` stalls **418‰ → 4‰** on the spot.
Permanent fix: **`CBS_EN_RST = 4'b0000`** (all queues strict-priority at reset; SRP/AVDECC opts SR
classes into shaping) — `tb/verilator/csr` updated (76 checks green), built as `build_dp100_cbs0`
(WNS **+0.031**), **verified at reset on silicon** (q0–q3 en=0). Un-paced TX then measured
265 single / **339 −P4 @ rx-usecs 1000** / **354 dual-process** — now genuinely **CPU-bound**
(`/proc/stat` 84–96% busy; the +23% from rx-usecs 500→1000 = fewer ACK-batch wakeups; iperf3 −P is
single-threaded, hence the dual-process-per-hart test; noZ costs ~20% → zerocopy is load-bearing).
⁴ **RX overload wedge — the RX blocker, characterized 2026-07-08.** Parallel RX (−P2) reliably
kills RX **delivery** while **every HW stage keeps flowing** (stage probes wire=core=dp=dma tick in
lockstep; the writer keeps committing BDs; `rx_dropped` counts buffer-exhaustion drops during the
burst; BD ring hit full: `occ_hi=768`). Flavor 1: HW commits, but the driver's **FIFO-paired page
lookup** (`page[comp_i++]`) rejects everything after a popped-buffer drop shifts the pairing — a
**v1-BD address-verify + realign guard** is now in `kl-eth` (with `KL_BD_ENTRIES` 64→256); flavor 2
(guard never fires): post-overload delivery stays inconsistent until reset. **Root-cause forensics
with a sim repro (RSC aggregate + no-buffer drop interleave in `test_ring_bd.py`) is the top next
task** — it gates all parallel-RX numbers and TX −P8 stability. Also seen: idle RTT is 3–11 ms
(irq 13 fires but delivery rides the 5 ms fallback poll; `rx-usecs-low` 200 µs storms the CPU) —
a completion-IRQ-driven NAPI is the latency fix, secondary to the wedge.

**Status vs goal (>500):** ≥200 holds with margin on TX (**354** best stable — was 172 at the
start of the campaign: **2×**, via the measured CBS root cause + coalesce tuning + dual-process).
**Neither direction is at 500 yet.** TX is now honestly CPU-bound: the remaining ~40% needs
per-unit CPU cost cuts (ACK path, xmit/reap, poll wakeups) and the wedge fix for stable −P4+.
RX cannot even run its parallel campaign until the **overload wedge**⁴ is fixed — that fix gates
the 2-queue fan-out numbers. Reader prefetch stays **refuted**². 1 Gbit/s remains the stretch.
UDP is a separate (offload) problem. Every step measured on silicon — HW counters + `/proc/stat`
side by side; the books must balance.

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

## Roadmap toward >500 Mbit/s, then 1 Gbit/s (ordered, each independently measurable)

**Immediate bar: >500 both directions** (≥200 met; TX at 354). The levers below are the same
ones that carry on to 1 Gbit.

0. **Fix the RX overload wedge (NEW top item — gates everything parallel).** Parallel RX kills
   delivery while all HW stages keep flowing (footnote ⁴ above). Sim-reproduce the buffer/BD
   lockstep break under RSC + no-buffer drops in `test_ring_bd.py`, fix the RTL drop-path
   contract (a popped buffer must never be consumed without a completion BD — or the BD must
   carry the address for *every* type, incl. v2), keep the driver's address-verify realign guard
   as defense-in-depth. Without this there are no stable −P2 RX numbers and no stable TX −P8.
1. ~~**TX reader prefetch**~~ — **REFUTED by measurement (2026-07-07)**; and the `stall` half of
   the old bottleneck map is **also resolved**: it was the CBS default shaping BE (footnote ³,
   fixed in `milan_csr`). The measured TX levers now: cut per-ACK/per-reap/per-wakeup CPU cost
   (rx-usecs 1000 already buys +23%), a second TX queue for dual-hart xmit, completion-IRQ
   latency. See `TX_READER_PREFETCH_PLAN.md` MEASURED VERDICT.
2. **Recover 100 MHz timing margin:** +0.031 ns on `build_dp100_cbs0`; **2-queue RxSteer at
   100 MHz** still needs re-validation once the wedge (item 0) is fixed — it may have been the
   wedge all along. Then run both directions at 100 MHz with the fan-out intact.
3. **Cut RX per-frame cost further:** wire a completion IRQ (drop the hrtimer poll — idle RTT is
   3–11 ms today and `rx-usecs-low=200` storms the CPU), scale the RX fan-out to more
   queues/harts, and lean on RSC + GRO. Line-rate RX needs fewer frames or more parallel harts.
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
