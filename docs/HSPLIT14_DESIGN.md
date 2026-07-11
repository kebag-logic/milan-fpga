# hsplit14 / hsq12 — per-page (cut-through) hs delivery

*2026-07-11. Kills the RSC hold latency (the per-flow ~95 Mbit plateau: rate =
PAYCAP/fill-cycle because ACKs wait for aggregate close — see SESSION_HANDOFF
"plateau closed-form"). Pages become visible as they complete; the meta arrives
LAST and only finalizes. Effective hold: PAYCAP-fill (~4.8 ms) → page-fill
(~1.3 ms @16K). Pairs STRICTLY: hsq12 gateware ↔ kl-eth hsplit14.*

## Why the current RTL holds everything to close

The hs opener allocates TWO CQ entries: meta FIRST (drains first), page second.
The meta's `done` only sets at close (stage_close fills it) — and the CQ drain
is pop-ordered, so the undone meta at the head **blocks every completed page
v3 behind it** until close. The driver (hsplit9..13) builds the header skb from
the meta then attaches v3 frags: meta-then-pages is the ABI today.

## hsq12 RTL changes (RingDMAWriter)

1. **Opener allocates ONE entry** (the first page). Delete `cur_cqm` staging and
   the second `cq_tail+2` bump (gate can relax to `cq_level < CQD-1`; keep -2
   for margin). Delete the `s_cqm` array, the `mcl_of_*` hops, and the hsq9
   META-at-head term in `head_open_hit` (dead — there is no undone meta at the
   head anymore; pages are done-at-completion, the close-meta is done-at-fill).
2. **stage_close(k, cqi, …) allocates the meta at CLOSE**: replace
   `NextValue(meta_cqi, mcqi)` with a tail alloc
   (`meta_cqi←cq_tail; cq_done[tail]←0; tail+1`) — CQ order becomes
   v3…v3, meta (meta LAST). The pv3 (last page) still fills `cqi` =
   `cq_of_sel`/the slot's registered page entry (LIVELOCK INVARIANT: the page
   v3 always targets the slot's own entry — unchanged).
3. **Every stage_close caller gains `& cq_room`** (alloc needs a free entry).
   Deferral semantics per site:
   - exp (tout/age) + pressure closes: simply retry next cycle (conditions
     persist).
   - same-flow-gap / victim park-closes: the existing `.Else` drop path
     already handles no-room (frame drops counted; BD-gate makes full-CQ safe).
   - psh-close-after-append: defer = aggregate stays open with s_psh[k] held;
     exp/pressure close it later. VERIFY s_psh persists (slot reg — it does).
   - ACK-flush-vs-open ordering (test_bd_ack_flush…): re-run, order semantics
     unchanged (v1 ACks unaffected).
4. **v3 w0 gains two fields** (both zero today):
   - `[63:59] hdr_idx` — same position as the meta's (uniform decode). Sites:
     HS_PGSWAP writes `s_hidx[slot_sel]`; the pv3 path stages `pv3_hidx` in
     stage_close (`s_hidx[k]`).
   - `[31:16] fill_len` — bytes in THIS page. HS_PGSWAP writes
     `hs_page_bytes`; the pv3 writes the partial fill
     `(s_off[k] & (hs_page_bytes-1))`, with the ==0 case fixed up to
     `hs_page_bytes` (one Mux). This lets the driver deliver every v3
     immediately (no deferral waiting for the meta to learn the last page's
     length).
   Layout after: [7:0]=0xBD, [15:8]=seq(drain-patched), [31:16]=fill_len,
   [47:32]=0, [53:48]=drops6(drain-patched), [55:54]=tag, [56]=1, [57]=0,
   [58]=1, [63:59]=hdr_idx.

## kl-eth hsplit14 changes

v3 handler (pages now arrive FIRST):
- `tag`, `hdr_idx=(w0>>59)&0x1F`, `fill=(w0>>16)&0xFFFF`, page from FIFO
  pairing (w1 addr verify unchanged).
- If `!asm[tag].active`: bind headers — parse the hs_hdr slot directly
  (hdrlen = 34+4*doff from slot byte 46>>4; seq from bytes 38-41); record
  `{hdr_idx, seq_base, delivered=0}`.
- **Deliver PER PAGE**: alloc skb (hdrlen), memcpy headers from the slot,
  patch: ip tot_len = hdrlen-14+fill, tcp seq = seq_base+delivered, recompute
  IP csum (as today's meta path), attach the page frag (len=fill, truesize=
  hs_pgsz), gso_size=1448 when fill>1448, CHECKSUM_UNNECESSARY,
  napi_gro_receive. `delivered += fill`.
- META handler shrinks: stats (rx_packets += segs), psh/ack/win are NOT
  retro-patched (already-delivered units carried the open header's ack/win —
  acceptable; psh only affects app-wake latency), clear asm[tag]. The stale-asm
  guard flips: a META with no active asm = normal for 0-payload closes.
- Teardown/resync: clear asm (exists).

## Sim updates (test_ring_bd.py)

- ALL hs tests flip expected BD order to pages…meta (basic_split, crossing,
  tag_interleave, famine, pressure) + assert v3 hdr_idx/fill_len.
- New: interleaved two-flow early-binding test (v3s of A and B interleave
  before either meta — driver-model binds per-tag headers correctly).
- Livelock probe: reap model's page/meta accounting is order-agnostic (verify).

## Expected effect + follow-ups

rtt ≈ page-fill + delivery (~1.5 ms) ⇒ per-flow headroom ≈ cwnd·MSS/rtt ≫ 125;
P4 should push toward the CPU ceiling (~550-600 aggregate at the measured
cy/B). Pairs best with 16K pages (early delivery recycles pages sooner —
famine pressure drops, so 32K's absorbency matters less; re-measure). Keep
`hs_pgsz`/`hs_page_bytes` STRICT pairing. TX gate after every swap.
