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
