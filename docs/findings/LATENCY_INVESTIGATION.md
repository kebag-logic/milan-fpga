# Latency & memory investigation  -  why single-port TCP caps at 30 Mbit/s (2026-07-05)

> ⚠️ **Point-in-time snapshot (2026-07-05).** Superseded  -  for current RX/TX numbers and the live bottleneck/lever see [`RX_TX_PERFORMANCE.md`](RX_TX_PERFORMANCE.md) + [`../CHANGELOG.md`](../../CHANGELOG.md). Numbers and "next steps" below are historical.

**Platform:** AX7101 (XC7A100T-2), VexiiRiscv RV64IMA @100 MHz, sv39, 32 KB L2, DDR3-800
(MT41J256M16, 1:4), Milan datapath @50 MHz · **Link:** 1000BASE-T to an Intel i210 peer
(`192.168.127.2`) · **Load:** iperf3, MTU 1500 · **Driver:** `kl-eth` (IRQ-less polled rings).

This is the full symptom → measurement → root-cause chain for the single-port throughput
ceiling, including **two conclusions I had to retract mid-investigation** (kept here on
purpose  -  the retractions are the lesson). Every number below was measured on silicon or
in cycle-accurate sim; nothing is estimated unless labelled "model".

> **Forward pointer (2026-07-07):** the per-frame cost decomposition below was completed
> (and, where it stopped at "per-frame CPU cost", superseded) by a kernel **tick-profile**
> (`CONFIG_PROFILING` + `profile=4`): at MTU 1500 the RX CPU time is **three copies of
> every byte**  -  driver ring→skb memcpy, TCP receive-queue coalesce memmove, and the
> kernel→user usercopy  -  while the TCP protocol logic itself costs ~1 % per function.
> See the **2026-07-07 campaign** addendum in
> [CPPI_DMA_REDESIGN.md](../fpga/CPPI_DMA_REDESIGN.md) for the profile and the copybreak/page-frag
> fix (RX 25 → 45.6 Mbit/s), and [HW_GRO_RSC.md](../fpga/HW_GRO_RSC.md) for the ÷K plan toward
> ≥200. This document's history below is unchanged.

---

## TL;DR

| Question | Answer (measured) |
|----------|-------------------|
| Is single-flow TCP CPU-bound? | **No**  -  94 % idle at 30 Mbit/s. It is **latency-bound** (TCP ack-clock × IRQ-less poll delivery latency). |
| Is there a silicon gate/bug? | **No**  -  under a flood the CPU pins at **100 % (98 % sys)** delivering 14k pps; frames arrive fine (172k/s at the MAC), the ring correctly drops overflow. |
| What is the real ceiling? | **Memory latency.** A random miss costs **1424 ns**; the stack touches many per frame → ~70 µs/frame → **14k pps** hard CPU ceiling. |
| What is 1424 ns made of? | **50 % TLB page-table walk (713 ns) + 50 % DRAM+CPU floor (716 ns)**  -  proven by a 2 MB-hugepage vs 4 KB-page A/B. |
| Cheapest win in hand? | `ethtool -C eth0 rx-usecs-low 2000` → **+32 % RX** (28→37), no rebuild. Live on the board now. |

---

## 1. The contradiction that drove everything

Single TCP flow: **RX 30.1 / TX 26–27 Mbit/s**, ping 0.87 ms, 0 % loss. But `vmstat`
during the transfer:

```
 in   cs  us sy id
3133  15   1  4 94   ← 94 % IDLE while pushing 30 Mbit/s
```

"CPU-bound" and "94 % idle" are mutually exclusive. A compute bottleneck pins the core at
100 %. So the core is **idle because it is *waiting***  -  something serialises each frame
and the CPU sleeps through the wait. The whole investigation is: *what is it waiting for,
and is that wait a protocol effect or a hardware gate?*

## 2. What it is NOT (each ruled out by measurement)

**Not coalescing / poll cadence.** `ethtool -C rx-usecs` (active poll period) swept 5 µs→1 ms:
flat at ~30 Mbit/s. *(Caveat found later: this knob only sets the `rx>0` re-arm; the idle
re-arm dominated  -  see §5.)*

**Not per-flow window.** `iperf3 -P 4` did **not** aggregate  -  RX/TX fell to ~20 Mbit/s
(poll contention) while the CPU stayed **95 % idle**. A shared serialisation, not a window.

**Not the clock (RETRACTED).** I first measured `sleep 12` → 20.5 s of real time and
claimed a "1.7× slow clock." **Wrong**  -  that was the flaky serial console corrupting the
`echo TMRDONE` marker into `echo TMRD`, so my detector timed out at its own 20 s poll
limit. The clean passive test overturned it: board uptime advanced **31.83 s over a real
31.83 s (ratio 1.000)**, and `sleep 10` self-timed at **10.26 s**  -  clocksource *and*
clockevent are correct. **Lesson: a marker that can be corrupted is not a measurement.**

**Not a silicon delivery gate.** See §3  -  the flood proves the CPU *does* saturate.

## 3. The two regimes  -  flood localises the ceiling

Flood the board with high-pps UDP (peer sends 400 Mbit/s of 250 B datagrams ≈ 200k pps)
and compare frames-at-MAC (fabric `rx_wire` telemetry) vs frames-delivered (`rx_packets`):

```
rx_wire  (MAC)     = 171,942 frames/s   ← arriving on the wire
rx_packets (Linux) =  14,355 frames/s   ← delivered to the stack   (~7-10 % through)
rx_missed (ringfull)= 260,076 frames/s  ← HW-dropped, ring full
```

CPU during the flood: **id 0 / sy 97-98**  -  pinned at 100 %. So:

| Regime | pps | CPU | Bound by |
|--------|----:|-----|----------|
| Single TCP flow | ~3k | 94 % **idle** | **latency** (ack-clock + poll delivery latency) |
| Flood (no ack-clock) | ~14k | 100 % **busy (sys)** | **per-frame CPU cost** |

The "10 % gets through" is **not** an aggressive drop policy  -  it is a **~14× overload**
(200k arrive / 14k drain). Under sustained overload ~93 % *must* drop regardless of buffer
size; a bigger ring only buffers a burst then drops the same steady-state excess. The drain
rate (14k pps) is the real number, and it is set by per-frame CPU cost.

## 4. Root cause  -  memory latency (the 14k-pps ceiling)

14k pps ≈ **70 µs/frame** on a 100 MHz core = ~7000 cycles/frame. Where does it go? A
static-linked microbenchmark (`membench`, pointer-chase over 16 MB = random DRAM misses):

| | baseline | under DMA flood |
|---|---|---|
| streaming `memcpy` | 42 MB/s | **14 MB/s (3× slower)** |
| random miss latency | **1424 ns** | 1430 ns (unchanged) |

- **1424 ns per random miss** is the villain: the network stack pointer-chases scattered
  cache lines (skb, sockets, TCP state) per frame; a few dozen misses ≈ the 70 µs.
- **Contention is real but secondary:** heavy DMA slows the CPU's *streaming* copy 3×
  (bandwidth contention), but the dominant *random-miss latency* is **inherent** (unchanged
  under load). So it is **latency, not bandwidth contention**.

### 4.1 Decomposing the 1424 ns  -  TLB vs DRAM (hugepage A/B)

Same 16 MB random chase under 4 KB pages vs 2 MB hugepages (a handful of TLB entries then
cover all 16 MB → ~zero TLB misses):

```
4KB-page chase = 1429 ns/access
2MB-huge chase =  716 ns/access
→ TLB-walk = 713 ns (50 %)  |  DRAM+CPU floor = 716 ns (50 %)
```

**Half the miss latency is sv39 page-table walks; half is the DRAM device + LiteDRAM
controller + CPU miss path.** Crucially, **hugepages alone halve it**, and that is mostly
a software change.

## 5. The poll-CSR cost (why backing off the poll helps +32 %)

The rings are **IRQ-less**  -  RX is delivered only by an hrtimer NAPI poll (NIC IRQ 13
fires **0** times). Each poll reads `wr_ptr` (+`dropped`) via MMIO CSR, which stalls the
in-order core. Sweeping the **idle** re-arm period (`rx-usecs-low`, added this session):

| `rx-usecs-low` | RX Mbit/s | | `rx-usecs-low` | RX Mbit/s |
|---:|---:|---|---:|---:|
| 5 | 5.1 | | 500 | 32.3 |
| 20 | 7.3 | | 1000 | 36.1 |
| 50 | 15.3 | | 2000 | 35.9 |
| 200 (default) | 27.9 | | **4000** | **37.0** |

Polling *faster* **collapses** throughput (empty-poll CSR stalls contend with the datapath);
polling *less* recovers +32 %. **Model** (`poll_cost_model.py`, fit to this sweep): the
CSR-free single-flow ceiling `Tmax ≈ 36 Mbit/s`, per-empty-poll cost ≈ 6 µs. So removing
the CSR cost recovers the plateau at low latency but does **not** exceed ~37 (that ceiling
is §4's per-frame cost). **Live mitigation applied:** `rx-usecs-low=2000` on the board.

## 6. Levers to reduce latency  -  ranked, tied to the measurement each attacks

| Lever | Attacks | Effort | Status |
|-------|---------|--------|--------|
| **Hardware L2 forwarding (ALE/TCAM)** | keeps CPU out of the switched path entirely | large (RTL) | `hdl/common/tcam.sv` exists; the switch answer |
| **RX completion interrupt + pacing** | RX delivery latency (unlocks 3k→14k headroom) | medium | IRQ 13 wired, unused  -  proposed |
| **Hugepage the ring/buffers** | TLB half (713 ns → ~0) | low (SW/DT) | proven 2× in `membench`; proposed |
| **Pointer-writeback** | per-poll MMIO CSR stall | done (RTL+sim) | §7 |
| **On-chip BRAM descriptors** (TI BD-RAM) | both halves, for metadata | medium | proposed |
| **Zero-copy RX** (CPPI-style) | the per-frame copy (35 µs/1500 B) | large | proposed |
| **Non-blocking D-cache + MSHRs** | overlaps the serial misses | medium (cfg) | proposed |
| **Floorplan + clock bump** | ns-per-cycle on the DRAM+CPU floor | medium | built+tested, **reverted** (§8): +25 % single-flow but −12 % flood / +40 % miss latency |

Note: a **faster DDR3 speed grade does NOT help** the 716 ns floor  -  first-word latency
(tRP+tRCD+CL ≈ 40 ns) is ~constant across grades; a faster grade only raises *bandwidth*
(which helps the §4 contention).

## 7. Pointer-writeback (implemented + sim-verified)

`RingDMAWriter` now DMA-writes `{dropped[63:32], wr_ptr[31:0]}` to a coherent shadow
(`status` CSR) after each frame commit, so the driver polls the ring head **from cache**
instead of an MMIO CSR. Verified in migen sim (`test_ring_writeback.py`):

- Engine drain: **WB off 405.8 kpps / 4.86 Gbit/s, WB on 396.4 kpps / 4.74 Gbit/s**  - 
  writeback costs **+5.8 cyc/frame (+2.4 %)**; the shadow value matches the CSRs exactly.
- The 6-test `test_ring_dma.py` regression still passes (writeback off when `status`=0).

**Honest scope:** the model (§5) says this recovers the ~36 Mbit/s plateau at low latency
but does not beat it for a single flow. Its real value is aggregate/many-flow pps and
removing the latency↔throughput tradeoff  -  so it should ride the *next* switch bitstream,
not a standalone spin.

## 8. The floorplanning finding  -  the 112.5 MHz build, and why it was REVERTED

Post-route timing at 100 MHz: **WNS +0.143 ns**, and the worst path is **not logic**:

```
Source: FDPE_1/C   Destination: milan_dma_ringdmawriter_s_data_reg[11]/R
Data Path Delay: 9.208 ns (logic 0.348 ns / route 8.860 ns)   Logic Levels: 0
net (fo=3896, routed) 8.860 ns   sys_rst
```

The 100 MHz ceiling is the **system reset net**  -  fanout **~3900**, **8.86 ns of pure route**
across the die, zero logic. The obvious fix is **replication**  -  fracture the one die-spanning
net into local copies. **It could not be done**, and that is the finding.

**Three replication methods  -  all three FAILED (kept as the lesson):**

- **`build_vexii_fp`**  -  post-synth XDC `set_property MAX_FANOUT`. Reset **never replicated**
  (still `fo=3969`, still the critical path). Vivado treats resets as **control sets** and
  will not fracture them from a post-synthesis property.
- **`build_vexii_fp2`**  -  an **RTL `(* max_fanout = 100 *)` attribute** on `cd_sys.rst`,
  applied at *synthesis* (before control-set grouping). Also a no-op on the reset: `synth_design`
  left `sys_rst` at `fo=3969`.
- **`build_vexii_fp3`**  -  `phys_opt_design -force_replication_on_nets [get_nets sys_rst]`
  on the placed design (the `-force` variant that is *supposed* to override control-set
  protection). Also failed to fracture the net.

**Root cause of all three failures:** the reset **synchronizer's clock carries a `DONT_TOUCH`**,
so Vivado will not touch the reset control set through *any* of the three levers  -  XDC property,
RTL synthesis attribute, or forced phys-opt replication. The reset stays one net of `fo≈3969`.
**The real reset fix is not replication at all**  -  it is to declare the reset a **multicycle /
false path** (the synchronized reset is not a single-cycle timing arc), which the `--floorplan`
flag does *not* do.

**Nevertheless all three builds *closed* at 112.5 MHz  -  WNS +0.043 ns, 0 failing.** That margin
came from the **placer working harder under the tighter clock** (a knife-edge that happens to
meet), **not** from replicating the reset. DDR3-900 + BIOS memtest were verified on silicon.

Clock target **112.5 MHz** (VCO 1800: sys 112.5 / sys4x 450 / idelay 200 / milan 50  -  all
integer; DDR3-900, within the part's 1600 rating). **PLL constraint (why 112.5, not 110):**
the same PLL must emit the fixed 200 MHz IDELAY ref and 50 MHz Milan clock, so the VCO must be
a multiple of 200; the only clean integer step above 100 MHz is VCO 1800 → 112.5 MHz.

### 8.1 The 112.5 MHz silicon result  -  a divergent-bottleneck trade-off, so REVERTED

Loaded and measured on the board. The +12.5 % clock helped one bottleneck and hurt the other
 -  **because the single flow and the flood/membench are bound by different things** (§3–§4):

| Workload | Bound by | @112.5 MHz vs 100 |
|----------|----------|-------------------|
| Single-flow TCP | **compute** (faster CPU wins) | **+25 %** throughput |
| `membench` random-miss latency | **memory** (DDR3-900 higher CAS + longer LiteDRAM pipeline) | **+40 % worse** |
| UDP-flood pps ceiling | **memory** (per-frame miss cost) | **−12 %** (14.4k → 12.7k pps) |

So a faster clock is the **right lever for a single compute-bound socket flow** and the
**wrong lever for the switch**, which needs low **DRAM latency** and high **aggregate pps**  - 
exactly the two things DDR3-900 made worse. **Decision: reverted to 100 MHz / DDR3-800.** The
+25 % single-flow number is real, but the switch role never runs that workload (forwarding is
in fabric, §9), and the −12 % flood ceiling + 40 % worse miss latency are the numbers that
matter. The `--floorplan` flag remains in `milan_soc.py` but, as above, does **not** actually
replicate the reset; the productive reset fix is a multicycle/false-path constraint.

## 9. The TI reference (`ti_eth.pdf`, AM5726 GMAC_SW)  -  validation & blueprint

The AM57x 3-port gigabit switch is exactly this project's target, and it dodges every
latency above by design:

- **CPPI descriptors in dedicated 8 KB on-chip BD RAM**  -  not DRAM. Descriptor access is
  ~10 ns SRAM with no TLB → sidesteps *both* halves of §4 for the hot metadata path. Our
  pointer-writeback is step 1; on-chip BRAM descriptors are the full pattern.
- **RX/TX interrupts with programmable pacing** (RX_PULSE / RX_THRESH_PULSE)  -  not polling.
  Validates §6's RX-interrupt lever.
- **ALE wire-rate L2 forwarding**  -  the CPU is never in the switched path. This is the
  architectural answer: forwarded AVB traffic never pays §4/§5 at all.
- AVB (802.1Qav CBS) + 1588 (CPTS) in the fabric  -  matches our CBS + PTP work.

## 10. What changed this session

| File | Change |
|------|--------|
| `sw/litex/milan_soc.py` | `RingDMAWriter` pointer-writeback (`status` CSR + WB_AW/W/B states); `--floorplan` (reset-fanout replication) |
| `sw/litex/test_ring_writeback.py` | NEW  -  writeback correctness + engine bandwidth sim |
| `sw/litex/poll_cost_model.py` | NEW  -  CSR-poll cost model fit to the silicon sweep |
| `fpga/kl-eth/kl-eth.c` (milan-tests-avb) | `ethtool -C` `rx-usecs` (active) + `rx-usecs-low` (idle) NAPI-poll-period knobs |
| board (live) | `rx-usecs-low=2000` (+32 % RX); new `.ko` hot-loaded (not yet in initrd) |
| build | `build_vexii_fp{,2,3}`  -  `--floorplan` + `--sys-clk-freq 112.5e6`: all 3 closed +0.043 ns, DDR3-900 on silicon, then **reverted to 100 MHz** (§8.1) |

## 11. Status & next steps

- **Done + reverted:** the 112.5 MHz build (`build_vexii_fp{,2,3}`) was built, loaded, and
  measured on silicon (§8.1)  -  +25 % single-flow but −12 % flood pps and +40 % worse miss
  latency, so the board runs **100 MHz / DDR3-800**. Reset replication proved impossible
  (DONT_TOUCH); the real reset fix is a multicycle/false-path constraint, not `--floorplan`.
- **Software win banked:** `rx-usecs-low=2000` (needs an initrd rebuild to persist).
- **Highest-value next levers:** hugepage the ring/buffers (proven 2× on the TLB half),
  then the RX interrupt (unlocks the 3k→14k headroom), then hardware forwarding for the
  switch (makes §4/§5 irrelevant to forwarded traffic).
