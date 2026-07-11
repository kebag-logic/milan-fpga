# HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)

> **STATUS: PARTIALLY SUPERSEDED (single-slot RSC era).** Concepts hold; the implementation is now 4-slot mslot + pop-ordered CQ + header-split (v2/v3 BDs) + the hsq6 BD-ring gate + (hsq12) close-allocated metas. Living map: **RX_PERF_TUNING_MAP.drawio**; silicon history: HEADER_SPLIT_DESIGN.md.


**Goal**: ≥200 Mbit/s TCP at MTU 1500. Profile-proven wall at 46 Mbit/s: per-WIRE-frame
stack traversal + locks (~20-25% CPU) + per-frame driver work; TCP logic itself ~1%/fn.
RSC merges K in-order same-flow TCP data segments in gateware → the stack pays per
SUPER-segment: traversal/locks/wakeups ÷K, driver BDs ÷K. K≈8-12 → 200 clears with margin.

## Merge rules (v1)
Eligible frame: IPv4 (ethertype 0x0800), ihl=5, proto=TCP, frag_off∈{0,DF}, TCP flags ⊆
{ACK,PSH}, tcp payload > 0. Continues the OPEN aggregate iff: same 4-tuple, same doff,
seq == expected (first_seq + accumulated payload). Pure ACKs (payload 0) and everything
else pass through as singles (today's path).

CLOSE the aggregate and emit its BD when: PSH set on the arriving segment (merge it, then
close — preserves interactive latency); ineligible/4-tuple-change/seq-gap frame arrives
(close, then handle the newcomer fresh); seg_count = 16; next payload would overflow the
posted buffer; **timeout 100 µs** since last merge (µs counter in engine); ring disable.
Checksum: v1 does NOT verify in HW — merged BDs are delivered CHECKSUM_UNNECESSARY only
if the driver opts in (param `rsc_csum_trust=1`, default for bring-up); v2 adds the
two-region sum (pseudo-header verify per segment, abort-merge on bad).

## Buffer/write path
Posted buffers become **16 KB** (page_pool order-2; driver contract: post ≥ 16 KB).
Frame 1 of an aggregate: written WHOLE (headers+payload) at buffer offset 0 (today's path).
Frames 2..K: payload ONLY, appended contiguously at agg_off (= end of previous payload).
Payload source offset = 14+20+doff*4 (54 or 66) — byte-granular, and agg_off is byte-
granular ⇒ **write-side realign**: carry+shift on the FIFO stream (same structure as the
TX v2 read realign) + AXI WSTRB head/tail partial beats. Geometry cone must keep the
registered-burst pattern (timing lesson: keep muxes off frame_bytes cones — see a82fc2e).

## BD format v2 (16 B, LE) — merged aggregates
w0: [7:0]=0xBD | [15:8]=seq | [31:16]=total_len (hdr_len + Σpayloads; ≤16 K)
    | [47:32]=mss (first segment payload size) | [55:48]=drops | [63:56]=flags
    flags: bit0 MERGED, bit1 PSH-seen, bit2 csum-verified(v2)
w1: [31:0]=last ACK number | [47:32]=last window | [55:48]=seg_count | [63:56]=doff<<2
Single frames keep BD format v1 (w0 csum field = raw sum, CHECKSUM_COMPLETE; w1[63]=0
distinguishable via flags bit0=0... v1 w1 carried buf_addr — driver already tracks order,
so w1 is repurposed; bump a BD-format bit: w0[55:48] were drops[15:8] — drops narrowed to
8 bits (wraps fine, telemetry only)).

## Driver contract
- Pool: order-2 pages, 16 KB posts (KL_BD_MAX_LEN grows; copybreak path unchanged).
- Merged BD: fix up the first header IN the buffer (cache-warm): ip.tot_len = total_len-14,
  tcp.ack = w1.ack, tcp.win = w1.win, set PSH if flags.bit1; ip/tcp checksums left stale →
  skb: CHECKSUM_UNNECESSARY (trust) ; gso_size = mss, gso_segs = seg_count,
  gso_type = SKB_GSO_TCPV4 (forwarding-correct).
- Deliver via napi_gro_receive as today (SW GRO passes super-segments through).

## RTL integration points (RingDMAWriter, BD mode only)
1. Header register file: first 9 beats (72 B) of each frame consumed into regs before
   AW issues (covers eth14+ip20+tcp(doff≤10)); parse fields combinationally off the regs.
2. Aggregate state regs: open flag, 4-tuple (98 b), expected_seq, agg_off, seg_count,
   first_buf handle, mss, last_ack/win, psh_or, µs timer.
3. Streaming mux: header beats from regs then FIFO (single path today = frame-1 case);
   merged case skips hdr bytes via the realign shifter into agg_off.
4. Close path reuses today's WB_AW/WB_W/WB_B with the v2 BD mux; timeout close runs from
   IDLE (no frame in flight).
5. `rsc_en` CSR bit (default 0 = bit-identical legacy) — every stage A/B-able on silicon.

## Sim plan (extend test_ring_bd.py)
tcp_frame() generator (4-tuple/seq/flags/doff params). Tests: (1) 4-segment merge byte-
exact (payload concat, BD v2 fields incl mss/ack/win/segs); (2) PSH closes; (3) seq gap
closes + newcomer opens fresh; (4) flow interleave A,B,A → three aggregates (v1 has ONE
aggregate slot); (5) non-TCP passthrough mid-aggregate; (6) 16-seg cap; (7) timeout close;
(8) buffer-overflow guard; (9) doff=8 (timestamps) merge; (10) single-frame BDs unchanged
when rsc_en=0 (regression) and eligible-but-alone frames (timeout single→still v1 format?
→ aggregates of 1 emit v1-format BD = zero driver churn for singles).

## Phasing
A: parser+hdr regfile (sim: field extraction). B: aggregate open/append (write realign)
(sim: 2-seg merge). C: close matrix + BD v2 + timeout. D: driver (16 K pool + fixup).
E: silicon A/B (rsc_en, iperf + profile: expect tcp_v4_rcv/locks ÷K). F(v2): HW csum
verify, multi-flow slots, ACK-run merging.

---

## Implementation status (2026-07-07) — phases A+B DONE, sim-verified

**Phase A — parser + header regfile (commit `a158711`).** New `HDR_CAP` FSM state in the
RX BD engine: with `rsc_en=1` (CSR, default 0) the first ≤9 beats of each frame are
consumed into a 9×64 b register file before dispatch; the eth/IPv4/TCP fields
(totlen/flags/doff/seq/ack/win/4-tuple/eligibility) parse combinationally off the regs,
and `rsc_dbg` (CSR) exposes `{eligible,doff,flags,totlen}` of the last capture. The
captured beats are replayed **byte-exact** through the same W path. With `rsc_en=0` the
FSM never enters `HDR_CAP`/`DISPATCH` — bit-identical legacy behaviour (regression-held).

**Phase B — aggregate open/append/close (commit `8f0dfc5`).** `DISPATCH` decides 4-way:
**append** (matches the open aggregate → payload-only into its buffer at `agg_off`),
**close-first** (aggregate open but no match → emit its v2 BD, park the newcomer,
re-dispatch it), **fresh-open** (eligible, no aggregate → whole frame into a posted
buffer, aggregate opens after the last B), **plain single** (v1 BD, today's path).
Single-slot aggregate state (4-tuple, expected seq, byte-granular `agg_off`, buffer
handle, seg count, mss, last ack/win, psh-or). **Write-side realign** as designed:
carry+rotate on the source stream (an `APRIME` state preloads one beat when source
lane > destination lane) + **AXI WSTRB partial head/tail beats**; `rsc_bufsz` (CSR) guards
buffer overflow via the match term. Close fires on **PSH / seq-gap / flow-change or
ineligible newcomer / 16 segments / buffer-full**; **timeout close is phase C**. BD v2 on
close, as specified: `w0={magic 0xBD, seq[7:0], total_len[15:0], mss[15:0], drops[7:0],
flags[7:0] (bit0 MERGED, bit1 PSH)}`, `w1={ack[31:0], win[15:0], seg_count[7:0], doff<<2}`.

### As-built rules — where the implementation pins down (or diverges from) the spec text
- **Aggregates of 1 emit a v2 BD with the MERGED flag set** — NOT the v1 format the sim-plan
  item (10) parenthetical hoped for. Opening an aggregate defers the BD, and the v1 csum
  (CHECKSUM_COMPLETE raw sum) is not carried in aggregate state, so a close-at-1 can only
  emit v2. Driver consequence: v2 handling must not assume `seg_count ≥ 2` (asserted in
  `test_rsc_gap_closes`).
- **An eligible frame arriving with PSH already set does NOT open an aggregate** — the arm
  term is `ap_arm & ~PSH`, so it takes the plain-single leg and emits a **v1 BD** (the
  spec's merge-then-close would have built a 1-segment v2 for nothing). Interactive /
  short-flow segments stay on the v1 fast path.
- **Close-on-PSH merges the PSH segment first, then closes** (as specified) — implemented
  from the append completion in `WAIT_B` (`psh_or |= PSH`; close when PSH or seg 16), not
  as a separate pre-close pass.
- **True singles (ineligible frames, pure ACKs) emit v1 BDs unchanged** (as specified).
  Merged BDs carry **no checksum** in v1 of the feature (driver trust via
  `rsc_csum_trust`; HW verify is phase F).

### Sim inventory — 14/14 green (`sw/litex/test_ring_bd.py`)
At `8f0dfc5` (12/12): the 6 BD-engine regressions (zero-copy, no-buffer drop, ring wrap,
1520 B content, reload flush, throughput) + RSC: parse fields + **byte-exact regfile
replay**; eligibility (SYN rejected / data-ACK accepted); **3-segment byte-exact merge** →
ONE v2 BD (len 414 = 166+200+48, mss 100, flags MERGED|PSH, segs 3, doff 0x20), closed by
PSH; **seq-gap close + fresh-open** (parked-frame re-dispatch: 1-seg aggregate v2 then a
2-seg aggregate, the newcomer landing whole in the second buffer). Coverage follow-up
(`024dde2`, → 14/14): **alignment sweep** (doff 5 and 8 × chained lengths walking
`agg_off` through ALL dest lanes = the pass-through / rotate / rotate+prime shifter
regimes, byte-exact each close); **16-segment cap auto-close**; **pure ACK mid-flow**
(closes the aggregate, delivered as a plain v1 single). Harness note: the sim AXI memory
model (`test_ring_dma.py`) is now **WSTRB-aware** — the realign path writes partial beats,
and a strobe-ignoring model would hide corruption.

### Phase C — DONE (commit `18fcec3`, 16/16 sims)
Idle-timeout close: `rsc_tout` CSR (24-bit milan_clk cycles, reset 5000 = 100 µs
@50 MHz); the timer resets on every arm/merge (`agg_touch`) and the close fires from
IDLE (frame processing has priority — a pending frame merges or closes first). Ring
disable clears any open aggregate (reload hygiene, no stray BD). Tests: timeout flush,
timer-reset-on-merge (no premature close), disable-with-open-aggregate.

### Remaining
**D** — driver: order-2 16 KB pool,
merged-BD header fixup (`ip.tot_len`/ack/win/PSH), `gso_size=mss`/`gso_segs`,
CHECKSUM_UNNECESSARY. **E** — silicon A/B (`rsc_en`, iperf + tick-profile: expect
per-frame stack cost ÷K). **F** (v2) — HW csum verify, multi-flow slots, ACK-run merging.

## Phase E — SILICON RESULT (2026-07-07): **GOAL MET — 203 Mbit/s TCP RX @ MTU 1500**

`build_rsc1` (dual-hart + RSC A–C): WNS +0.667 (healthiest recent build — the realign
shifter closes with margin), 61.3 % LUTs (~1.3 k for RSC). Driver `rsc=1` (af65df6).
Measured, sustained 15 s iperf3, wire MTU 1500:

| | before campaign | copybreak | **RSC** |
|---|---|---|---|
| TCP RX | 25 | 46.5 | **203 Mbit/s** |
| merge factor | — | — | **9.0 segs/BD** (rx_packets/BDs) |
| CPU during RX | 99 % sys, 0 idle | 90 % | **66 % sys, 32 % idle** |
| TCP TX | 35.6 | 57.5 | 58 |

The ÷K arithmetic landed exactly (46.5 × ~4.4 ≈ 203 at K=9). CPU now has 32 % idle at
200 Mbit/s — headroom remains. Ring drops during the run: 2 (negligible); ~1.5 k IRQ/s.
Day total: RX **8.1×**, achieved via profile-guided steps: 3-copies fix (copybreak+frag),
dual-hart SMP, and HW receive coalescing. TX (58) is the next frontier if needed —
levers: HW-TSO (spec'd), O2 kernel via BIOS-LZ4.

## TX ≥200 campaign — design (2026-07-07 profile-guided)

TX@61 profile: skb_segment payload memcpy 11.7% (SW-GSO with SG off copies per wire
segment) + usercopy 10.6% (irreducible) + allocator ~9% + locks 6.4%; tcp_ack only 1.2%
(ACK-RX is NOT the wall); idle 13%.

**Step 1 — cross-BD realign continuity (TX RingDMAReader)**: byte-granular output
position (`frame_olane` 0-7 + partial `hold` beat) carried ACROSS the BD chain of one
frame; per-segment shift p = (s_lane − frame_olane) mod 8; DRAIN emits the residual
only at EOF. Removes the `len%8==0` mid-segment contract. Implementation shape: rework
PAY realign as an occupancy shifter (hold 0-7 bytes; emit when ≥8; valid_in = 8 except
seg-head (8−s_lane) and seg-tail). Sims: multi-frag frames, arbitrary lengths ×
alignments, byte-exact wire image (extend test_tx_bd).
**Step 2 — driver SG**: NETIF_F_SG on in TX-BD mode; kl_xmit_bd posts BD chains
(linear head BD + one BD per frag, EOF last; per-chain slot bookkeeping; reap unmaps
the walked frags). SW-GSO then splits super-skbs by frag reference → the 11.7% copy
and most per-seg allocs disappear. Expected TX ≈ 90-120.
**Step 3 — HW TSO** (the 200 lever): first-BD w1 {tso_en, mss, hdr16}; engine caches
the ≤96 B header in a regfile once, replays it per MSS-cut with patches (ip.tot_len,
ip.id+=k with end-around-carry check fix from driver-precomputed check_full/check_last,
tcp.seq += k·mss, FIN/PSH only on last, tcp.check per segment = fold(driver-const
pseudo+hdr sum + seq_k halves + engine per-segment payload pre-pass sum — the v2b
double-read machinery)); payload phase consumes the continuity stream with cuts at
mss. Stack cost then runs once per 64 KB: TCP output ÷44, skb_segment gone entirely.

## TX ladder — EXECUTED on silicon (2026-07-06): soft-TSO + cs-across-BDs, TX 58 → 103

Step 3 landed as **soft-TSO**: no per-MSS header-replay gateware — the DRIVER does the
MSS cutting by writing BDs, and the Step-1 continuity engine does the stitching.

**Soft-TSO via BD choreography (driver `kl-eth`, the-private-test-repo `e7b9c77`).**
`NETIF_F_TSO` advertised; each gso super-skb is segmented by the driver writing
per-segment BD chains: a per-segment header built in a coherent **header arena**
(256 slots × 128 B, one slot per BD index, headers at **slot+2** so the IP/TCP fields
are 4-byte aligned) + payload BDs pointing straight into the super-skb frags (**no data
copy**). The continuity engine (assembly shifter) stitches the arbitrary offsets/lengths
into one wire frame. BD ring 64 → 256 entries (driver constant; the ring mask CSR is
programmable).

**The +2 alignment lesson.** Headers first went into the arena at +0 → iph at +14, tcph
at +34 (2 mod 4): every u32 field store trapped to SBI misaligned-emulation on
VexiiRiscv — ≈ **56 µs per 94-byte header = 69 % of the whole TSO cost** (measured with
the driver stage timers). Moving headers to slot+2 (NET_IP_ALIGN) took TX
**42 → 88 Mbit/s**.

**Measured TX ladder @ MTU 1500** (iperf3, peer i210):

| | baseline | soft-TSO @ +0 (misaligned) | **+2 fix** | `-P2` | `-l 1M` single-flow |
|---|---|---|---|---|---|
| TCP TX | 58 | 42 | **88** | 98 | **103** |

RX regression holds at **203 Mbit/s**.

**cs-across-BDs (gateware `e633032`, bitstream `rsc6`).** The TX v2b checksum pre-pass
now walks the WHOLE BD chain (the accumulator survives BD hops), **rewinds the BD ring
to the chain's first BD** (new `rd_c` anchor), and re-walks it streaming with the folded
ones-complement sum patched at the frame-relative `csum_off`. cs fields latch ONLY from
the chain's **first** BD w1; a new **published rd** (`rd_pub`) hides the pre-pass rd
excursion from the driver — otherwise the reaper frees skbs the real pass still reads.
Driver side: the per-segment TCP checksum seed = pseudo − sum(pre-TCP header bytes),
field patched by HW — the SW payload `csum_partial` pass (**845 µs/64 KB super-skb,
16 %**) is deleted. Non-TSO chained PARTIAL skbs also switch from `skb_checksum_help`
to the same first-BD w1 mechanism. Sim: `test_tx_bd.py::test_bd_csum_chain` (chain
pre-pass + rewind + patch + rd publish); whole suite **8/8**.

### Multi-flow hardening — the `-P4` root causes (2026-07-06)

Three `-P4` stability root causes found & fixed on silicon, plus an RSC crash exposed
alongside:

1. **Lost doorbell at ring-full (driver).** The xmit_more-deferred doorbell was lost
   when the ring filled. Fix: flush the doorbell BEFORE `netif_stop_queue`.
2. **Zombie-full ring (driver).** xmit wrote `kl->txbd_rd` (the REAPER's cursor) on the
   full-path refresh → the cursor jumped past unfreed slots → permanently-full ring.
   Rule: **only the reaper owns the cursor**; xmit re-checks against a LOCAL hw rd read.
3. **RSC DISCARD black hole (gateware `9584927`, bitstream `rsc5`).** A frame with
   beats ≤ hdr_take (any pure ACK ≤ 9 beats) dropped with an EMPTY post FIFO entered
   DISCARD with `disc=0`, which wraps 11 bits and eats **2047 beats of FOLLOWING
   frames** → permanent len/data FIFO desync (drops tick forever, frames frozen).
   Fix: count the drop and return to IDLE without touching `data_fifo`. Regression:
   `test_ring_bd.py::test_rsc_tiny_drop_recovers`.
4. **RSC single-segment aggregate panic (driver, 2026-07-06).** Single-segment
   aggregates (timeout / newcomer-closed, len ≤ copybreak 192) crashed the kernel:
   `skb_add_rx_frag(len - copybreak)` wrapped as u32 → `skb->len < data_len` →
   `eth_type_trans` BUG → panic in interrupt. Fix: clamp the linear part
   (`lin = min(len, copybreak)`), recycle the page when fully linear, gso fields only
   when `segs > 1`, and reject `len < 54` v2 BDs.

**Profiling methodology.** Driver `get_cycles()` stage timers (per-stage buckets printed
every 2048 frames) + `/proc/profile` tick profiling (`profile=4`) + capacity reasoning —
**books must balance**: the 56 µs header cost was found because b1 dominated the stage
print, and the misalignment hypothesis was confirmed by the **9.4× drop after +2**.

### ACK-run merging — LIVE on silicon (2026-07-07): TX 109 → 121

The phase-F item landed (gateware `ee52742`, bitstream `rsc7`, WNS +0.146): the RSC
writer grew a **pending-ACK slot** that absorbs runs of pure ACKs (flags == ACK-only,
plen == 0, doff = 5 or timestamp-only options `01 01 08 0A`), delivering only the
LATEST as a normal **v1 BD** — **zero driver changes needed**. SACK-shaped ACKs pass
through untouched.

**The `rsc_tout` sweep (silicon, 2026-07-07).** `rsc_tout` is the SHARED idle-flush
timeout — data aggregates AND the pending ACK. At the 100 µs default the merge never
engages: peer ACK spacing is ~200 µs at 115 Mbit/s, so each pending ACK flushes before
its successor arrives (merge rate ~8/s). At **512 µs** (25600 cycles @50 MHz) the merge
fully engages (~2,000 ACKs/s absorbed) and single-flow TX goes **109 → 121 Mbit/s**. At
**≥1 ms TX COLLAPSES** to ~300 Kbit/s — the sender's ACK clock starves. RX is
insensitive across 100 µs–2 ms (201-206 Mbit/s). The driver (the-private-test-repo `85122fa`)
programs 25600 at init.

**Final measured ladder @ MTU 1500** (`rsc7` + driver `85122fa`; session baseline TX 58):

| | single-flow | `-P2` | `-l 1M` | zerocopy | RX |
|---|---|---|---|---|---|
| TCP | **118-121** | 136 | 132 | **142** | **201-206** |

zerocopy = iperf3 `-Z` (sendfile), board-as-client, measured on `rsc6`.

### Post-mortem corrections (2026-07-07)

- **The "-P4 wedge" is NOT a hang or a HW/driver bug** — it is an extreme TCP crawl
  (~1-2 frames/s) under 4-flow competition. Driver+engine were proven alive during it
  via a poll heartbeat (rd/seq advancing, BD ring config intact). Page-pool exhaustion
  (4× pool test) and CSR/BD-config corruption theories: disproven. Open item: TCP
  dynamics under 4-flow competition on the 2×100 MHz SoC.
- **"bd_base cleared to 0" was an instrumentation error** — a debugging gotcha: LiteX
  64-bit CSRs expose the HIGH word at the LISTED address (`milan_dma_rx_bd_base`
  0xf0003058 reads bits[63:32], always 0 for 32-bit DMA addresses; the live value is
  at +4).

### Driver robustness (the-private-test-repo `85122fa`)

RX and TX **BD-ring self-heal** paths: full CSR reprogram (base/mask/rd/tout/enable) +
page/skb reclaim, behind a **race-free detector** — re-read the BD after sampling the
HW `wr` (the engine commits BDs before advancing `wr`, so a BD that appears on re-read
was a lost race, not a wedge). Plus rate-limited poll/bd dmesg heartbeats.
