# HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)

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
