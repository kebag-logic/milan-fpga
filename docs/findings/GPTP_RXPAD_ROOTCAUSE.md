# gPTP "bad message" — ROOT CAUSE (2026-07-12 night): RX DMA delivers 8-byte-padded frames

> **GATEWARE FIX IMPLEMENTED 2026-07-13 (commit 5638c95, in the hwts1 sweep):**
> the last-beat keep now threads through len_fifo as a 3-bit `pad`; single-frame
> BD w0 reports the TRUE length (beats*8 - pad, ACK-flush included), the
> byte-ring header stays PADDED (frozen ABI, zero driver change), RSC aggregates
> were already parse-derived. Gates: ring 7/7 + BD 45-PASS (new 68B-gPTP /
> 91B-replay / 66B-ACK true-length tests) + elab/codegen clean. The kl-eth
> PTP-trim becomes a no-op on fixed gateware and stays for old bitstreams.
> Silicon gate pending: RX perf regression (TCP ≥ switch baseline, 0-drop).

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


## SILICON RESULT (2026-07-12 night) — FIX VALIDATED
Driver trim applied (milan-tests-avb kl-eth 24438f3), .ko hot-swapped on the Arty:
- **"bad message": thousands/min -> 0.** ptp4l accepts every switch pdelay_req.
- Full pdelay handshake with the d&b switch BOTH ways (tcpdump): Arty sends
  pdelay_req + pdelay_resp; switch (3c:c0:c6:fe:02:18) sends pdelay_req +
  pdelay_resp + pdelay_resp_followup. 7 each per 8 s.
- `port 1 (eth0): peer port id set to 3cc0c6.fffe.fe0210-8` (switch recognized).
- `port 1 (eth0): setting asCapable` — **eth0 IS asCapable.** Our stack is
  fully proven end to end (RX delivery, timestamping, pdelay, PHC).
- Then `announce timeout` -> self-elects GM: the switch sends NO Announce/Sync
  on the board port (verified with pw0 forced GM priority1=100 — still no relay).

## Remaining (switch-side, NOT our stack)
The switch does per-port pdelay but does not relay a grandmaster's Sync/Announce
to the board ports (isolated/limited-port config; board<->board and board Announce
relay both absent). To get a SLAVE/offset-converged validation:
- **direct board<->board cable** — now unblocked (the RX-pad fix applies there
  too): the two boards peer directly, BMCA elects one GM, the other slaves, no
  switch relay needed. `sw/litex/gptp_direct_cable.sh` (both boards need the
  fixed .ko + /etc/gptp.cfg, now baked into the rootfs).
- OR switch management: enable 802.1AS GM relay on the board-facing ports.


## Bench note (end of session)
After ~a dozen FPGA reconfigs/reboots tonight the switch stopped sending pdelay
to the Arty port (0 inbound 88F7), while the DATA plane still works (pw0 pings
the Arty fine). This is switch-side flap-suppression / RSTP state on that port,
NOT the fix or our stack (both proven: bad=0, asCapable=1, full handshake
earlier the same session). To re-validate: power-cycle the switch (or re-enable
the board port in its management), then `ptp4l -i eth0 -f /etc/gptp.cfg -S -m`
should show asCapable within seconds. Cleaner path unaffected by switch state =
the direct board<->board cable (gptp_direct_cable.sh) — both boards now carry
the fixed .ko + /etc/gptp.cfg in flash.

## What's in flash now (arty, morning-ready)
arty_v10 bitstream (MVP talker) + fixed kl-eth (PTP-trim) + /etc/gptp.cfg +
S50milan. Verified from a flash boot: talker streaming (counters advance),
driver has the trim, gptp.cfg present, bad-message=0.


## FULL SYNC ACHIEVED (2026-07-13 early) — Sync/Follow_Up work through the switch
The user was right: sync/follow_up DO work. Demonstrated end to end:
- **Arty = grandmaster** (priority1 100, clockClass 6, software timestamps).
  It sends Sync (56/cap) + Follow_Up (56) + Announce — a complete two-step GM.
- The **switch relays** the Arty's time as a boundary clock (its own clock id
  3c:c0:c6:ff:fe:fe:02:10) to the gigabit uplink port.
- **pw0 (hardware timestamps) SLAVED to it and CONVERGED: rms 2-4 ns, max 4-8 ns,
  freq ~-26500 stable, delay -8.** A locked gPTP domain, Arty as time source.
So the whole chain works: our Sync/Follow_Up (post RX-pad fix) discipline a real
slave to single-digit nanoseconds through the AVB switch.

Direction notes:
- board -> uplink relay (Arty GM -> pw0 slave): WORKS, 2-4 ns lock.
- uplink -> board relay (pw0 GM -> Arty slave): flaky this session — the Arty
  board port kept getting flap-suppressed by the switch after ~a dozen FPGA
  reconfigs. When the port is live the pdelay + asCapable establish; a switch
  power-cycle (or the direct cable) gives the Arty a clean slave lock too.
- BMCA gotcha: 802.1AS forbids clientOnly/slaveOnly with !gmCapable; make a node
  "prefer slave" via gmCapable 1 + weak priority1/clockClass, not slaveOnly.

Net: gPTP is functionally PROVEN on the Milan endpoint. Remaining polish =
Phase B hardware timestamps (tighter than the -S software path; the fabric
already timestamps 0x88F7) for sub-ns and to satisfy tight switch thresholds.


## SWITCH BEHAVIOR MATRIX — definitive (2026-07-13 morning, post power-cycle)
The switch was power-cycled (~03:46, its PTP clock read 7 s in pdelay resps;
flap-suppression cleared). Systematic experiments, one variable at a time:

| Port | pdelay | accepts strong GM announce (slaves) | sends announce/sync (masters) |
|---|---|---|---|
| uplink (pw0) | always | NO — ignored pw0 100/cc6 for 25+ min (clean obs) | YES (self-GM at boot; relay when slaved on port 8) |
| port 8 (Arty) | always | YES — Arty 100/cc6 engaged the relay | no VALID observation (see revision) |
| port 7 (AX) | always | not proven either way (contaminated) | no VALID observation (see revision) |

- **REVISED 2026-07-13 (user pushback — correct): "the switch never masters
  into a board port" was OVERSTATED.** What the evidence actually supports is
  only "board-as-slave was never OBSERVED", because every master-role-into-
  board-port observation was structurally blind:
  * port 8 was the switch's SLAVE-side port whenever the relay was engaged —
    a slave port sending no Sync is CORRECT 802.1AS, not a finding;
  * port-7 observations ran through the AX's DEAF MAC (allmulti off — the
    kl-eth mc-filter gap): relayed Sync/Follow_Up INTO that port would be
    invisible to pmc/ptp4l; the only promisc (tcpdump) windows on port 7 ran
    during the multi-claimant chaos or before the relay engaged;
  * the parallel session's run (8bbe361) reported "zero gPTP incl. pdelay"
    on a port where pdelay demonstrably flows — its capture path is suspect
    (busybox `timeout tcpdump` fakes empty captures — rule 8).
  The plausible design reading: the appliance's board/edge ports are
  GM-source + pdelay ports and a board is simply not expected to receive
  Sync/Follow_Up from the switch in this role assignment.
- **SETTLED (2026-07-13, clean observation)**: with the Arty-GM relay
  demonstrably engaged (pw0 SLAVE rms 2 ns on the uplink at the same
  moment), a 60 s PROMISCUOUS capture on the AX port (MAC filter bypassed)
  shows **exactly 60 pdelay_req + 60 pdelay_resp + 60 resp_fup — zero
  Announce, zero Sync/Follow_Up**. The edge ports do not source sync BY
  DESIGN (they are GM-source/pdelay ports); this is the appliance's role
  assignment, not a malfunction, and matches the operator's expectation.
  Board-as-slave therefore validates over the direct board<->board cable
  (gptp_direct_cable.sh), full stop.
- **Multi-claimant confusion**: with 3 strong GMs at once (pw0 100 + Arty 100
  + AX 90, all cc6) the switch went announce-SILENT on every port (even its
  own self-GM stopped). Reverting to a SINGLE strong claimant (Arty 100/cc6,
  everyone else 248-254/cc248) re-engaged the relay within ~1 min. Keep the
  segment single-claimant.
- Re-proven end to end after the power-cycle: Arty GM -> switch (presents its
  own clock id 3cc0c6.fffe.fe0210, boundary-style) -> **pw0 SLAVE rms 3 ns,
  freq -26.5k** (same freq as last night = same Arty time source).
- The AX had been running the OLD un-trimmed kl-eth (adp2-era QSPI rootfs,
  up 14 h) -> "bad message" spam, asCapable never, its announces invisible.
  Hot-swapped the trim .ko (VM -> pw0 -> AX via `ssh cat`; the built artifact
  at br-milan-output/build/kl-eth-1.0/kl-eth.ko has the trim) -> badmsg=0,
  peer delay 450 us, full GM output on the wire. **RAM-only fix: the AX QSPI
  rootfs still ships the old driver — reflash for persistence.**
- ptp4l 4.4 sends PTPv2.1 headers (minorVersion 1) on gPTP; the switch
  handles them fine for pdelay AND (from the Arty, same 4.4) announce accept
  — version is NOT a factor (theory tested and dropped).
- Ops traps paid: both boards bake 192.168.127.1 (shared rootfs) — the Arty
  shadowed the AX until `ip addr del`; deleting the primary .1 also dropped
  the secondary .3 (busybox promote_secondaries off) — re-add .3 after.
  TWO sessions drove the bench concurrently this morning (this one + the
  8bbe361 session with amx-pi switch power control) — ptp4l restarts/kills
  from the other session look like silent crashes; check `ps` + attribute
  before debugging.
- LIVE-STATE DEPENDENCY: the current lock chain requires **allmulti pinned on
  both boards** (`ip link set eth0 allmulticast on`, MAC_CTRL 0x1B) until the
  kl_set_rx_mode fix (program allmulti/mc-hash when netdev_mc_count>0) ships
  with the Phase B kl-eth work. A reboot silently reverts to 0x13 = standalone
  ptp4l goes deaf.


## Arty-as-slave: exhaustively tested, blocked by switch role (2026-07-13)
Tried hard to get the Arty to SLAVE (discipline its own PHC from pw0-as-GM),
using the amx-pi switch power control:
- Fresh Arty boot (clean driver), AAF talker OFF (rule out multicast storm),
  `ip link set eth0 allmulticast on` (MAC_CTRL 0x13->0x1B; see driver-gap below),
  link held stable, switch power-cycled AGAINST the stable link + full STP/AS
  convergence (~2.5 min), pw0 = HW-timestamped GM.
- Result: the Arty's board port receives ZERO gPTP (asCapable=0, peer=0, bad=0)
  in this direction. Data plane is fine (pw0 pings the Arty). So the switch
  ACCEPTS a board port's time as a GM source (board->uplink relay to pw0 works,
  2-4 ns) but does NOT distribute a grandmaster's Sync to the board ports
  (uplink->board). That is a switch per-port ROLE/config (board ports are
  GM-source / slave-only from the switch's view), changeable only via the
  switch's management interface (d&b R1 / console) - power-cycling doesn't
  alter it. Clean board<->board direct cable remains the switch-free path.

## Driver gap found: kl-eth multicast RX needs allmulti
kl_set_rx_mode only reflects IFF_PROMISC/IFF_ALLMULTI into MAC_CTRL; it does NOT
program the per-address multicast filter for joined groups. So a standalone
ptp4l (which joins 01:80:C2:00:00:0E) does NOT receive gPTP multicast unless the
iface is in promisc or allmulti - earlier "working" runs had tcpdump up (promisc)
masking this. Workaround: `ip link set eth0 allmulticast on`. Proper fix: in
kl_set_rx_mode, set the allmulti MAC bit when netdev_mc_count>0 (or program the
gateware mc hash). Worth baking into the driver + S50milan for standalone gPTP.
