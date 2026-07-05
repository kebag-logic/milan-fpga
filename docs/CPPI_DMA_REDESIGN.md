# CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)

**Goal:** attack the two biggest per-frame costs found in [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md)
— the DRAM/CSR **descriptor-access latency** (§4/§5) and the **per-frame memcpy** (§6) — by
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
- **P0 — RX-completion interrupt + reset multicycle** *(in progress).* Drive the existing
  `ev.rx` `EventSourceLevel` (currently tied to 0) from `wr≠rd`; driver `kl_irq`
  `napi_schedule`s + masks/unmasks. Add a `set_multicycle_path`/false-path on the held sync
  reset (replication is DONT_TOUCH-blocked — see LATENCY_INVESTIGATION §8) to recover its
  slack. First CPPI reflex: "descriptor committed → interrupt", and low-latency delivery
  without the empty-poll CSR cost.
- **P1 — pointer-writeback** *(built, sim-verified: engine 400 kpps, +2.4 %).* Shadow the
  ring head to coherent memory — descriptor-in-memory groundwork; ride P0's bitstream.
- **P2 — on-chip BD RAM.** Replace the DRAM header + `wr_ptr` CSR with a BRAM descriptor
  ring the driver reads directly. **Biggest latency win.** New RTL: `RingDMAWriter` gains a
  BD-RAM write port + a CSR/AXI-lite window for the driver to read BDs; driver walks BDs.
- **P3 — cut-through + shrink the ingress FIFO.** Post DRAM buffers via BDs; DMA cut-through
  into them; drop `fifo_beats` to elastic-only. **Reduces MAC RAM** (~16 KB → ~1 KB).
- **P4 — zero-copy.** BDs point at pre-posted `skb` page buffers; driver page-flips instead
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
port — exactly TI's split (CPPI on the host port, ALE for the fabric).
