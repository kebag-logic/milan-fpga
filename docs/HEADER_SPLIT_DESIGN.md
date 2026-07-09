# Header-split zero-copy RX — design (2026-07-10)

**Goal** (GIGABIT_HEADROOM_ANALYSIS R-3): payload lands at **offset 0 of order-0 4 KB
pages** so `tcp_zerocopy_receive`'s `can_map_frag()` accepts every full frag —
measured enabler: batched PTE moves 1.22 µs/page vs 26.3 µs copy (21.5×). Target
~700–870 Mbit socket TCP at 100 MHz.

## Layout

- **Payload**: driver posts order-0 4 KB pages (same RING_POST FIFO). An aggregate
  concatenates TCP payload tightly across pages: page k holds payload bytes
  [4096k, 4096(k+1)). Pages pop **just-in-time at each 4 KB crossing** — the AW/W
  burst splitter already never crosses 4 KB (`to_4k`), so a burst never spans pages;
  crossing = swap `s_buf[slot]` to the next popped page. Per-slot state stays
  {current page, payload offset} — no page lists in HW.
- **Headers**: opener's captured beats (`hdr_reg`, ≤ 72 B) burst-written at aggregate
  open to `hs_hdr_base + hdr_idx*128` (32-slot ring, `hdr_idx` free-running 5-bit;
  safe: outstanding v2 BDs < BD-ring bound 64/(1v2+Nv3) < 32).
- **v1 singles** (non-TCP/ineligible/ACK-flush): UNCHANGED — whole frame at offset 0
  of one page (4 KB ≥ max frame), w1 = addr, realign guard intact.

## BD encodings (hs mode only; hs_en=0 ⇒ bit-exact legacy)

| word | v2 meta (aggregate) | v3 page |
|---|---|---|
| w0[7:0] | 0xBD | 0xBD |
| w0[15:8] | seq | seq |
| w0[31:16] | total len (hdr+payload, as legacy) | bytes in THIS page |
| w0[47:32] | mss | 0 |
| w0[53:48] | drops (6-bit saturating) | drops6 |
| w0[55:54] | **slot tag** | slot tag |
| w0[56] | 1 | 1 |
| w0[57] | psh | 0 |
| w0[58] | 0 = meta | **1 = page** |
| w0[63:59] | **hdr_idx** (5 b) | 0 |
| w1 | {ack, win, segs, doff} (legacy) | **page phys addr** |

## Ordering (CQ, extends R2's pop-order invariant)

- v2 meta CQ entry allocs at **open** (no buffer pop — new alloc site), done at close.
- Page entries alloc at their pops; **fill+done at page-complete** (next crossing or
  close) — pages of an open aggregate drain AFTER its v2 (pop order) but need no wait
  on close.
- Driver sees: v2(tag) first → alloc skb, copy header (~54 B) from
  `hdr_ring[hdr_idx]`, set gso from {mss, segs}; then N = ceil((len−hdrlen)/4096)
  v3(tag) BDs (interleaved with other tags) → attach full-4K frags (tail partial);
  countdown → `napi_gro_receive`. hdrlen = 34 + 4*doff (ihl=5 enforced by parser).
- Famine mid-aggregate (no page at crossing): close with what's written (psh=0).

## Driver (kl-eth `hsplit` mode, module param; legacy default intact)

order-0 `page_pool`; header ring 32×128 B coherent alloc + `hs_hdr_base` write +
`hs_en=1`; per-tag assembly slots (4); v1 path untouched. Validation:
`tools_recv_zc.c` (TCP_ZEROCOPY_RECEIVE) — expect zero-copied% > 0 for the first
time, then steady −P8 time-series.

## CSRs (appended after rsc_agemax — all existing offsets preserved)

`hs_en` (1 b, reset 0), `hs_hdr_base` (64 b). Verify via csr.csv diff.
