# gPTP "bad message" — ROOT CAUSE (2026-07-12 night): RX DMA delivers 8-byte-padded frames

## The overturn
Earlier conclusion ("the switch doesn't run gPTP on the board ports") was WRONG.
Verified with an inbound-only capture while ptp4l runs: the switch **does** send
gPTP pdelay_req to the Arty port — src 3c:c0:c6:fe:02:18 (switch port-8 MAC),
clock id 0x3cc0c6fffefe0210, ~2.6/s, valid PTPv2, messageLength 54. (My first
captures showed zero because /tmp/gptp.cfg was wiped on the v10 reboot so ptp4l
wasn't running — but the switch sends pdelay unconditionally regardless.)

## The actual bug
ptp4l rejects every pdelay_req as "bad message". tcpdump parses them fine, so
the bytes are valid — but the FRAME is **72 bytes** on delivery, not 68
(14 eth + 54 PTP). The extra 4 bytes are ZERO **DMA alignment padding**:

- `RingDMAWriter` (sw/litex/milan_soc.py) delivers each RX frame padded to an
  8-byte boundary and reports the **padded** length. Docstring line ~545:
  "length = padded payload bytes". Length = `frame_beats << 3` (line ~1251;
  `ack_beats` comment line ~1005 "len_bytes = beats*8").
- The ingress registers s_data/s_valid/s_last (lines ~1114-1118) but **discards
  `sink.keep`** — so the last beat's valid-byte count is lost and length rounds
  up to beats*8. pdelay 68B → 9 beats → 72B reported.
- Driver kl-eth requires `(len & 7)==0` (ring desync check) and delivers the
  full padded skb. The gateware comment (line ~1127) even anticipated trimming
  ("pskb_trim_rcsum subtracts trimmed bytes itself") but the true length was
  never threaded through, so the driver can't trim.
- TCP/IP/UDP ignore the 4 pad bytes (length fields govern) → never noticed.
  ptp4l parses the 4 trailing zeros as a bogus TLV → EBADMSG "bad message".

## The fix (careful, sim-gated — NOT a rushed change)
Thread the true byte length from the ingress last-beat `keep`:
1. len_fifo (line ~656) `[("beats",11),("csum",16)]` → add `("pad",3)`.
2. Ingress: register `s_keep`; at the last beat (s_last) push
   `pad = 8 - popcount(s_keep)` (0-7) into len_fifo.
3. Descriptor length delivered to the driver = `(frame_beats<<3) - pad` (TRUE).
   - **BD path (ACTIVE, bd mode)**: BD word0 `len_bytes` → true length. SAFE:
     the posted buffer is max-frame, the BD ring advances by a fixed 16 B, and
     the driver uses `len` only to size the skb → no ring/alignment impact, NO
     driver change.
   - **byte-ring path (legacy/inactive under bd mode)**: keep the header length
     PADDED (the driver advances `rx_rd += 8 + len` and checks `len & 7`), OR
     also change the driver to re-pad the advance `((len+7)&~7)`.
   - **RSC path**: the coalesced aggregate's last segment carries the pad; a
     coalesced frame's reported bytes must subtract only the final beat's pad.
4. Gate on the RX sims (test_ring_dma.py, test_ring_bd.py) — lengths must be
   exact — then rebuild and re-run the RX perf regression (200+ Mbit, 0-drop)
   before trusting it. This touches the crown-jewel RX datapath; do it awake.

## After the fix
gPTP should converge: switch sends pdelay → ptp4l responds → asCapable → the
switch (or the real GM behind it) sends Sync/Announce → kl-eth PHC disciplines.
Endpoint is otherwise READY (RX passthrough verified, promisc on, TCAM
accept-all, PHC adjfine/adjtime validated). This ALSO explains any other strict
L2 protocol parser that would choke on the pad (future lwSRP MSRP/MVRP RX).
