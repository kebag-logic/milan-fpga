# CPPI-style DMA redesign  -  on-chip descriptors, cut-through, zero-copy (plan)

> **STATUS: DESIGN-ERA (pre-gate).** The BD/CPPI mode shipped, then gained: the drain full-gate at wr+16==rd (hsq6  -  the missing piece that caused the lap/desync storms this doc could not foresee), 256-entry rings (hsplit10), per-queue instances, hs v2/v3 encodings, cut-through ordering (hsq12). Living map: **RX_PERF_TUNING_MAP.drawio**.


**Goal:** attack the two biggest per-frame costs found in [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md)
 -  the DRAM/CSR **descriptor-access latency** (§4/§5) and the **per-frame memcpy** (§6)  -  by
moving the RX/TX DMA from the current contiguous **byte-ring in DRAM** to a **descriptor
(buffer-descriptor) ring in on-chip BRAM**, exactly the model TI's CPSW/CPPI uses
(`ti_eth.pdf`: 8 KB on-chip BD RAM + RX/TX pulse interrupts + ALE wire-rate forwarding).
It also **reduces the MAC's on-chip RAM**.

## Why (measured, from LATENCY_INVESTIGATION.md)
- A random DRAM miss = **1424 ns** (50 % sv39 TLB walk + 50 % DRAM/CPU floor). The driver
  reads `wr_ptr` via a slow MMIO CSR every poll and reads the frame header from DRAM.
- Per-frame `memcpy` (ring→skb) = ~35 µs for a 1500 B frame at the platform's ~42 MB/s copy.
- The single flow is compute/latency-bound (CPU 94 % idle); the flood ceiling (14k pps) is
  memory-latency-bound. Both improve if descriptor access and the copy leave the DRAM path.

## Current RX path (silicon-proven `RingDMAWriter`)
```
MAC ─▶ 16 KB store-forward ingress FIFO ─▶ AXI burst ─▶ 256 KB byte-ring in DRAM (+ 8B hdr/frame)
                                                          │
driver: poll wr_ptr (MMIO CSR)  +  read hdr from DRAM  +  memcpy payload → skb
```
On-chip cost: `fifo_beats=2048` × 64b = **16 KB BRAM (~4 RAMB36)** whole-frame buffer.

## Target CPPI-style RX path
```
MAC ─▶ ~1 KB elastic FIFO ─▶ cut-through AXI write into a driver-POSTED DRAM buffer
                              └▶ write BD {buf_addr,len,flags,csum} to on-chip BD RAM ─▶ ev.rx IRQ
driver: poll/ISR reads BD from BRAM (~10 ns)  +  page-flip the DRAM buffer into the skb (zero-copy)
```
- **BD RAM**: ring of buffer descriptors in FPGA BRAM (256 BDs × 16 B = **4 KB**). Driver
  reads the head BD from BRAM (~10 ns) → no `wr_ptr` CSR, no DRAM header read.
- **Cut-through**: frame beats stream straight into a pre-posted DRAM buffer as they arrive,
  so the ingress FIFO holds only burst-alignment slack (**~1 KB**), not a whole max-frame.
- **Zero-copy**: BDs point at pre-posted **skb page** buffers → DMA lands data in the skb →
  no per-frame memcpy.

## Net effect on MAC RAM
| | store-forward ring (now) | CPPI BD-RAM |
|---|---|---|
| ingress FIFO | 16 KB (~4 RAMB36) | ~1 KB elastic |
| descriptors | DRAM + MMIO CSR | 4 KB on-chip BD RAM |
| **on-chip MAC RAM** | **~16 KB** | **~5 KB → frees ~2–3 BRAM tiles** |
| descriptor-access latency | 1424 ns + CSR stall | ~10 ns BRAM |
| per-frame copy | ~35 µs / 1500 B | 0 (page-flip) |

Net: **less** on-chip BRAM **and** the two biggest per-frame costs removed.

## Phased plan (each phase builds + is sim-verified against `sw/litex/test_ring_*.py`)
- **P0  -  RX-completion interrupt + reset multicycle** *(in progress).* Drive the existing
  `ev.rx` `EventSourceLevel` (currently tied to 0) from `wr≠rd`; driver `kl_irq`
  `napi_schedule`s + masks/unmasks. Add a `set_multicycle_path`/false-path on the held sync
  reset (replication is DONT_TOUCH-blocked  -  see LATENCY_INVESTIGATION §8) to recover its
  slack. First CPPI reflex: "descriptor committed → interrupt", and low-latency delivery
  without the empty-poll CSR cost.
- **P1  -  pointer-writeback** *(built, sim-verified: engine 400 kpps, +2.4 %).* Shadow the
  ring head to coherent memory  -  descriptor-in-memory groundwork; ride P0's bitstream.
- **P2  -  on-chip BD RAM.** Replace the DRAM header + `wr_ptr` CSR with a BRAM descriptor
  ring the driver reads directly. **Biggest latency win.** New RTL: `RingDMAWriter` gains a
  BD-RAM write port + a CSR/AXI-lite window for the driver to read BDs; driver walks BDs.
- **P3  -  cut-through + shrink the ingress FIFO.** Post DRAM buffers via BDs; DMA cut-through
  into them; drop `fifo_beats` to elastic-only. **Reduces MAC RAM** (~16 KB → ~1 KB).
- **P4  -  zero-copy.** BDs point at pre-posted `skb` page buffers; driver page-flips instead
  of memcpy. Removes the ~35 µs/1500 B copy; raises the 14k-pps drain ceiling.

## Risk & verification
P2–P4 rework the silicon-proven `RingDMAWriter` (the RX path that took the most bring-up
effort), so each phase is **incremental + migen-sim-verified** (`test_ring_dma.py`,
`test_ring_tx.py`, `test_ring_writeback.py`) before a bitstream, and silicon-verified
(membench latency + iperf + the UDP-flood pps ceiling) after. The driver ABI stays
descriptor-compatible; the `kl,dma-ether` binding gains a BD-RAM `reg` window.

## Relation to the switch
For **switched** traffic the CPU is never in this path (fabric/ALE forwards at line rate),
so CPPI matters for **CPU-terminated** traffic (management, gPTP, AVDECC) and for the host
port  -  exactly TI's split (CPPI on the host port, ALE for the fabric).

---

## Bring-up log & current state (2026-07-05, end of session)

**HW path: WORKING and sim-regressed.** Three silicon bugs found (each via the layer
telemetry), fixed, and locked with sim regressions in `sw/litex/test_ring_bd.py` (6 tests):
1. **off_r masked with the BD-ring mask** → frames >1 KB overwrote their own head
   (ping fine, TCP dead; HW-frames == delivered told us payload, not delivery).
   Fix: linear `off_r` in BD mode. Regression: 1520 B/12-burst byte-exact content test.
2. **Post FIFO survived driver reloads** → stale freed-buffer addresses desynced the
   FIFO↔driver pairing (100 % garbage RX after rmmod; `posted`=64 vs 32 was the tell).
   Fix: FIFO drains while `enable=0`. Regression: reload-flush test.
   **Driver contract: post buffers only AFTER `RING_EN=1`** (posts while disabled drain).
3. Driver `posted=0` after fix #2 → driver posted before enable; reordered.

**Perf status: NOT yet at parity  -  the bottleneck is the Linux stack's handling of the
delivered skbs, not the HW.** Layer view on silicon (`lview.sh` methodology below):
wire 1257 fps → datapath 1181 → drops ~0 → BDs 1125 → delivered ~800, **CPU 97 % sys**.
In-driver stage counters (get_cycles instrumentation, printed per 2048 frames):
build_skb 12.8 µs + meta 4.3 µs + **stack (napi_gro_receive) 490 µs/frame** + post 8.9 µs.
Ruled out on silicon: GRO off (no change), TCP window 2 M (no change), RX-interrupt off
via `devmem` on ev_enable  -  IRQD=0 (no change), sender retransmits (14, clean).
A hybrid (BD HW path + right-sized `napi_alloc_skb` copy, pool page recycled immediately)
still measured ~150 µs in-stack  -  ~6× the ring driver's whole per-frame budget.

**OPEN  -  the control experiment**: the ring rootfs driver re-measured on the *same* bd3
bitstream/boot (all attempts were eaten by serial-console corruption). If it also gives
~15 Mbit/s → the regression is bd3/boot-wide, not the BD driver path; if ~30 → the delta
is in the BD driver software path alone. **Run this first next session.**

## Layer-per-layer debug method (use `lview.sh`)

One 5 s sample under load prints per-layer rates; the first layer whose rate collapses
vs the one above is the problem layer:
```
L1 wire (tlm rx_wire) → L2 datapath (tlm rx_dp) → L3 eng-drops (CSR dropped)
→ L4 BDs-out (CSR frames) → L6 delivered (rx_packets) → L7 tcp → L8 CPU (vmstat)
```
Plus: `posted` CSR (0xf0003058) = HW buffer-FIFO level (48 = healthy, 0 = repost broken,
64 = stale reload entries); in-driver stage counters print as `bd-stage ns/frame` in dmesg.
Serial-console rule: the console DROPS characters  -  set variables and `echo`-verify them
before use; verify every rmmod/insmod via `lsmod`/dmesg timestamps, never assume.

### 2026-07-06 addendum  -  batching + a false-parity retraction

**Batching implemented** (driver): consume all pending BDs per NAPI poll, then ONE
`RING_RD` write + batch replenish (was 2 CSR writes + a pool op PER FRAME). Also: `bd=0`
module param forces the ring path (one module, both paths, identical stage timers) and an
xmit-stage timer (ACK transmits run *inside* `napi_gro_receive`, so they land in the gro
stage  -  decompose before blaming the stack).

**RETRACTION / lesson**: the first "batched-BD = 31.5 = parity" measurement was FALSE  - 
the A/B module was built against a NEWER kernel tree than the board was running;
`page_pool_create` failed silently and `kl_bd_init` fell back to the ring path, so the
31.5 was the ring baseline re-measured. Tells that caught it: **no `BD zero-copy` probe
line in dmesg** and **`posted`=0 under load** (the user's "are you still feeding the DMA?"
question). RULES: (1) after every driver load, verify the probe line SAYS which path is
active; (2) module and kernel must come from the same build tree; (3) `posted` ≈ 48 under
load is the feed-health check. Batched-BD performance is **still unverified**  -  first test
on the flash-booted matching kernel.

### P5 v1 TX-BD  -  silicon results (2026-07-06)

**Works end-to-end** ('TX-BD zero-copy: 64 descriptors', both BD directions active), after
two lessons: (1) adding `bd_base` grew the TX CSR window → every later window shifted →
DT update needed (LiteX packs windows back-to-back); (2) **OpenSBI embeds the DTB
(`FW_FDT_PATH` in build_opensbi.sh) and copies it over the flash-loaded one  -  DT changes
require an OpenSBI rebuild**, not just a dtb reflash.

**Honest perf: TX 16.2 / RX 20.7 = copy-path parity, not a win.** Root cause: Ethernet's
14-byte header ⇒ `skb->data ≡ 2 (mod 8)` essentially always ⇒ the 8-aligned zero-copy path
never fires; v1 falls back to a bounce copy (into cached tx_buf slots  -  the first fallback
via `netdev_alloc_skb` cost 199 µs/frame of slab work; the bounce is 99 µs). The per-frame
memory tax cannot be dodged in software on this no-MLP core.

**v2 (the real win, RTL):** BD gains a byte-offset field + the engine barrel-shifts the
first beat (true zero-copy from any skb address), plus HW checksum-insert in the MilanMAC
PacketFIFO (frame is store-and-forward there: sum on ingress, patch on egress)  -  removes
BOTH remaining CPU payload touches. Sim harnesses (`test_tx_bd.py`) are ready to extend.

### P5 v2 (byte-offset realign)  -  silicon results (2026-07-06)

The engine now reads segments from **any byte address** (aligned-beat reads + carry/shift
realign + a DRAIN residual beat; offsets 0–7 × lengths sim-verified before the bitstream).
WNS +0.528. Measured ladder, xmit cost per frame → TX throughput:
`199 µs (slab fallback) → 99 µs (bounce) → 38.6 µs (true zero-copy)` → TX
`12.5 → 16.2 → 18.2 Mbit/s` (copy-path baseline 16.7). The freed cycles converted to
throughput exactly as the per-frame arithmetic predicts. The wall is now the **RX side**
(build ~150 µs + stack ~120 µs on the slim kernel)  -  next targets, plus part B
(HW csum-insert) and the residual ~30 µs of the BD post (uncached BD-ring writes suspected).

### P5 v2b HW checksum-insert  -  VERIFIED + full perf/counter analysis (2026-07-07)

**Checksum correctness proven 4 ways** (after two bugs: +0.039 timing flake → registered
one-hot patch selects, WNS +0.221; and driver seed algebra  -  `csum_fold` complements, seed
must be `~csum_fold(...)`):
1. Numeric chain: driver+RTL formula predicts the exact correct field (0x4d55)  -  the buggy
   `eae1` predicted 0x6d80, which is what the pre-fix wire showed.
2. TCP sustains 34 Mbit/s (a single wrong checksum drops that segment → 0 throughput).
3. `/proc/net/snmp` `InCsumErrors = 0`.
4. `tcpdump -vv` on the peer: `cksum … (correct)` (was `(incorrect -> …)` with `eae1`).

**Perf matrix** (txbd4 gateware + `c72e` driver: TX-BD v2 zero-copy realign + HW csum,
1 ms/5 ms coalescing, MTU 1500):
| direction | throughput | note |
|---|---|---|
| TCP TX | ~34 Mbit/s | zero CPU checksum work (HW insert) |
| TCP RX | ~25 Mbit/s | ack-clocked |
| UDP TX | 19.5 Mbit/s, 0% loss | iperf3 userspace sender bound (~1.6 kpps) on the 100 MHz core |
| UDP RX flood | see counters ↓ | |

**Counter analysis  -  where UDP RX loss lives (definitive):** peer offered ~9.8 kpps.
- Driver `rx_packets` delta = **22,561 delivered** to the stack during the sample.
- HW ring `rx_missed_errors = 0`  -  the always-ready ring **never dropped** a frame.
- `InCsumErrors = 0`  -  RX checksum offload clean.
- **`Udp RcvbufErrors = 180,748` = every datagram overflowed the socket buffer**; iperf3
  (single-threaded, 100 MHz) drained only ~764.
- **CPU = 99 % sys, 0 % idle** during bulk RX.

Conclusion: the HW + driver RX path delivers everything; the ceiling is the **single-thread
userspace consumer on the 100 MHz core**, not the NIC. The AVTP media path (fabric-consumed,
no userspace recv) never hits this; for CPU-terminated bulk the remaining lever is HW-GRO/RSC
(fewer, larger deliveries per CPU event).

### 2026-07-07 campaign  -  SMP, the three-copies profile, copybreak RX, stall verdict

**Goal set: ≥200 Mbit/s TCP @ MTU 1500.** Start of day **RX 25 / TX 35.6** → end of day
**RX 46.5 / TX 57.5–59 Mbit/s** (all measured on silicon: AX7101, VexiiRiscv @100 MHz).

**SMP  -  dual-hart VexiiRiscv is live** (`smp: Brought up 2 CPUs`): `milan_soc.py
--cpu-count 2` (`build_smp2b`), WNS **+0.574**, LUTs **59 %**  -  the RV64IMA 2-hart config
*fits* the 100T (the 122 %-doesn't-fit result was the NaxRiscv 2-issue+FPU config).
**TX 35.6 → 59 (+66 %)**; **RX unchanged**  -  the RX path is one serialized NAPI chain, so
a second hart cannot parallelize it (RPS measured neutral). Timing prerequisite: the v2b
**csum-accumulate cone (21 logic levels) was the design critical path**; pipelined
(lane-sum register + deferred add, commit `a82fc2e`) → the dual-core build closes +0.574.
Three OpenSBI gotchas, solved (details in `milan-tests-avb/fpga/README.md`):
1. the custom `litex_nax` platform **hard-codes `hart_count`**  -  it does NOT read the DTB;
2. `build_opensbi.sh` **copies `milan-tests-avb/fpga/opensbi/litex_nax/platform.c` over the
   OpenSBI tree on every run**  -  edit the repo copy, never `~/opensbi-nax`;
3. fix = the **`NAX_HARTS=2`** env param to `build_opensbi.sh`.
SMP DTS: `milan-tests-avb/fpga/dts/milan_ax7101_smp.dts` (`cpu@1` + both harts' CLINT
`interrupts-extended = <&L0 3 &L0 7 &L1 3 &L1 7>` and PLIC `<&L0 11 &L0 9 &L1 11 &L1 9>`).

**Kernel tick-profile  -  RX CPU time is THREE COPIES of every byte** (`CONFIG_PROFILING` +
`profile=4` bootargs, readprofile-style analysis):
| where | % ticks | what |
|---|---:|---|
| driver ring→skb `memcpy` | 6.3 % | copy #1 |
| TCP receive-queue coalesce `__pi_memmove` | 9.2 % | copy #2 (`skb_try_coalesce` on linear skbs) |
| scalar usercopy (kernel→user) | 9.7 % | copy #3 |
| TCP protocol logic | ~1 % per function | cheap |
| locks + task-switch | ~12 % | |
| idle | 18.8 % | |

**The stack logic is cheap  -  bytes are expensive.** Fix shipped (`kl-eth`, milan-tests-avb
commit `2786912`): **header-copybreak (192 B) + page-frag payload RX**  -  payload delivered
via `skb_add_rx_frag` + `skb_mark_for_recycle`, so TCP coalesces by frag pointers instead
of memmove (frames ≤192 B keep full-copy+recycle). **RX 25 → 45.6.** Re-profile: memmove
9.2 → 2.3 %, memcpy 6.3 → 2.0 %. Copy #3 (kernel→user, scalar word-wise) is the
irreducible app-delivery cost  -  ~44 MB/s effective on cold data on this core.

**TX stalls  -  hardware exonerated.** User-reported 0-bit/s intervals (Retr=0, cwnd flat):
6/6 scripted monitored rounds ran clean and `TX_EN` never dropped; every hardware theory
was disproven by experiment (no link flap; concurrent CSR hammer 0/400k errors on both
harts; per-hart pinned IO monitors clean). Best-fit explanation: **garbled serial-console
input executing mutated `devmem` commands**. Mitigated permanently by the SSH workflow  - 
the board now boots dropbear on :2222 from flash (see `milan-tests-avb/fpga/README.md`);
the 1.5 Mbaud serial console drops input characters and is for boot logs only.

**Active workstream toward ≥200: [HW-GRO/RSC](HW_GRO_RSC.md)**  -  the ÷K lever (merge K
in-order TCP segments in gateware; the stack pays per super-segment). Spec commit
`710a670`; **phases A+B implemented and sim-verified** (parser+regfile capture, aggregate
open/append/close with write-side realign, BD v2)  -  status section in that doc.
