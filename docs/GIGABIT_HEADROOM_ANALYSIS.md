# Getting the maximum out of the gigabit link — headroom analysis at 100 MHz

*2026-07-09/10 night. Every number here is silicon-measured on `build_r2slots`
(+ kl-eth `mslot60c/d`) unless marked **hypothesis**. Clock fixed at 100 MHz by
direction (112.5 MHz shelved: three builds — best WNS −0.036 corrupted QSPI reads
on-die; a future 112.5 needs a dedicated retiming/floorplan campaign, not seeds).*

## 1. Where the link stands

Wire ceiling at MTU 1500: **~941 Mbit/s** TCP goodput.

| path | measured | % of wire | binder (measured) |
|---|:--:|:--:|---|
| RX, full stack, **no copy** (MSG_TRUNC −P2) | **925** | 98 % | none — HW+driver+GRO+TCP run line-rate-class |
| RX, TCP with real `recv()` copies, sustained | **368–407** (flat, peer-tx_bytes time-series) | ~41 % | 2-hart CPU equilibrium: cpu0 100 % softirq, cpu1 100 % sys/copy |
| RX transient drain (slow-start window) | ≥ 520 real reads | 55 % | proves the drain machinery exceeds steady state |
| TX −P4 (iperf3 `-Z`) | **503–513** (−P2 record 525–536) | ~54 % | CPU descriptor feed: TX reader **63.4 % idle**, busy 6.2 %, datapath stall 4.1 % |

**The one-sentence verdict: the gateware + driver data-plane is already a gigabit
data-plane (925/941); everything still on the table is the cost of the kernel
socket API on two 100 MHz in-order harts.**

## 2. The budget model (anchor for every lever)

Two harts × 100 MHz = **200 M cycles/s** total compute.

| regime | throughput | system cycles/byte | notes |
|---|:--:|:--:|---|
| no-copy stack (925 Mbit) | 115.6 MB/s | **1.73** | GRO+TCP+reap only |
| with-copy steady (400 Mbit) | 50 MB/s | **4.0** | + copy + recv envelope + full-queue tax |
| wire (941 Mbit) | 117.6 MB/s | 1.70 | the whole budget |

Decomposition of the with-copy 4.0 cycles/byte:
- **cpu0 (softirq/GRO/TCP): 2.0 cy/B** — already amortized by R2's 60 KB aggregates
  (22.8 segs/agg; interleave parks eliminated).
- **cpu1 (app hart): 2.0 cy/B**, of which the **raw copy is only 0.64 cy/B**
  (26.37 µs/4 KB cold, mapbench) — the other **~1.36 cy/B is the recv() envelope**:
  syscall + sock-lock (incl. backlog double-handling in the full-queue regime) +
  skb-chain walk + rcvbuf accounting + window updates.
- **Full-queue tax ≈ 25 %**: steady 390 vs ≥520 transient with identical machinery —
  when Recv-Q pegs, every byte drags window-update generation and sock-lock backlog
  processing with it.

Consequence: even a *free* copy inside the present socket path leaves ~3.4 cy/B ⇒
~470 Mbit. **No tuning of the existing recv() path reaches the wire. Reaching the
wire means removing bytes from the socket path, not polishing it.**

## 3. RX levers, ranked

| # | lever | expected (measured basis) | effort | confidence |
|---|---|---|---|---|
| R-1 | **Userspace data-plane on the existing BD ring** (UIO/mmap export of the completion-BD ring + posted buffers; DPDK-style poll-mode consumer; kernel keeps control-plane) | **toward 925** — the ring/buffer architecture already exists and measured 925 through a heavier path; no RTL | driver: UIO/mmap export + small user lib | high (arch exists; the 925 proves the HW side) |
| R-2 | **AF_PACKET v3 RX_RING for the AVTP/Milan product path** | same class as R-1, standard ABI; copy-free by design | none in RTL; app-side | high — this is the real media path anyway |
| R-3 | **HW header-split** (writer scatters payload across order-0 4 KB pages at offset 0, headers in a side ring; BD carries the page count) → unlocks `tcp_zerocopy_receive` / io_uring zero-copy RX for *socket TCP* | **MEASURED ENABLER (tonight): batched trap-free PTE moves = 1.22 µs/page vs copy 26.3 µs — 21.5× cheaper** (mremap ping-pong, mapbench mode C). The old refutation (48 µs "map-cycle") was a trap-per-page artifact; the real vm_insert_pages path pays no traps. Budget: copy 0.64 cy/B → ~0.03; socket TCP ~700–870 Mbit becomes arithmetically reachable at 100 MHz | RTL: writer 4 KB-scatter (AW/W already splits at 4 KB boundaries — geometry fits) + driver posts order-0 pages / multi-frag skbs + `tools_recv_zc.c` already exists for validation | **high** — enabler measured; remaining risk is the insert+zap syscall envelope (est. 3–5 µs/page batched, still 5–8× under copy) |
| R-4 | ~~rpt-block-ahead-max=8~~ **MEASURED FLAT**: copy 27.04 vs 26.37 µs/4 KB, steady −P8 371–394 ≈ keeper — ahead=4 already saturates the memory path's useful MLP at the downPending=8 knee (`build_r2rpt`, WNS −0.077, not a keeper) | 0 % | done | measured — refuted |
| R-5 | Pool 63 + rmem ~800 K ×8 flows (pool ≥ Σrwnd, tax-reduction attempt) | +5–10 % **hypothesis** — 196 K rmem was catastrophic (window < 2 aggregates), 1–2 MB untested against pool 7.5 MB max | config | low-medium |
| R-6 | recv envelope micro-opts (io_uring multishot, busy-poll) | ~5 % class | app/driver | low |

Refuted / structurally capped (do not revisit without new evidence):
- Aggregates > 64 KB: v2 BD `len`/`agg_off` are 16-bit and GRO's skb cap is 64 KB —
  60 KB is the practical max for skb-based delivery.
- DDIO / BRAM stash / page-flip zero-copy / bounded-rmem warm-copy: all measured dead
  (residency physics + 1 ms structural window-cycle + sv39 remap cost).
- 3rd hart: **slices 98.24 %**, LUTs 82.7 %, BRAM 83.3 % — does not fit beside this
  datapath on xc7a100t.
- 112.5 MHz: shelved by direction; empirically needs WNS ≥ +0.03 to survive QSPI on
  this die (−0.036 corrupted flash reads).

## 4. TX levers, ranked

At 503 Mbit the reader idles 63.4 % waiting for descriptors (books balance:
busy 6.2 + stall 4.1 + pre-pass 15.9 + rd-wait 9.8 + idle 63.4 + setup 0.6 = cyc).
The datapath could carry ~8× more. TX is purely a CPU-feed problem:

| # | lever | expected | effort |
|---|---|---|---|
| T-1 | Userspace TX ring (mirror of R-1; the TX BD engine already reads straight from arbitrary addresses) | toward line rate for the data-plane | driver export |
| T-2 | Feed batching: larger app writes, `sendmsg` batching, doorbell coalescing (`xmit_more` is already batched — verify), TCP autocork tuning | +10–20 % **hypothesis** | config/driver |
| T-3 | Board-side ACK-RX cost: the RSC ack-merge already coalesces; extend merge window at high TX rates | small | RTL knob exists (`rsc_tout`) |
| T-4 | csum pre-pass removal (16 % of *reader* cycles, structural double-read) | 0 % until T-1/T-2 land (reader isn't the binder) | RTL, later |

## 5. What actually reaches the wire (recommendation)

1. **Product path (AVTP/Milan): go around the socket.** R-1/R-2 (userspace BD ring
   or AF_PACKET ring). The 925 measurement is the proof the silicon side is done;
   this is driver+app work with no RTL and no timing risk. This is how this class
   of NIC reaches line rate everywhere (DPDK/AF_XDP precedent).
2. **Socket-TCP benchmark path: header-split (R-3) is the door to ~700–870 Mbit,
   and its enabler is now MEASURED** (PTE-move 21.5× cheaper than copy, mapbench
   mode C tonight). This is the highest-value RTL investment left in the design:
   4 KB-scatter in the RSC writer + order-0 page posting in kl-eth, validated by
   the existing `tools_recv_zc.c`.
3. **Keep harvesting the cheap %:** pool/rmem coupling (R-5), TX feed batching
   (T-2). rpt8 measured flat — struck off.
4. **Re-open 112.5 MHz only as a real timing campaign** (retime the writer-match and
   reader-assembly cones, floorplan CPU vs datapath) — worth +8–12 % on every
   CPU-bound number above, but not seed-lottery material.

## 6. Evidence index (tonight)

- 925 no-copy: two MSG_TRUNC flows 480.7+444.3, steer split live, drops Δ0, canary 0.
- Steady 368–407: 75 s / 60 s runs, peer `tx_bytes` 5 s windows, flat; both harts
  100 % via /proc/stat (cpu0 softirq-dominated, cpu1 sys-dominated).
- Transient ≥520: 8 s −P8 cells read 553 MB of real copies (rate-sum cross-checked).
- Copy 26.37 µs/4 KB, trap-fault remap-cycle 48.03 µs, **batched PTE move 1.22 µs
  (21.5× under copy)** — mapbench modes A/B/C on r2slots.
- TX buckets: POST deltas at 503 Mbit −P4, books balance to cyc.
- Famine: KL_BD_POST 48→60 zeroed 60 s drops (earlier +137/60 s at 48).
- Full histogram at −P2: psh 55 %, rollover-park 45 %, tout 0.2 %, cap/age/prs 0,
  ratio 22.8.
