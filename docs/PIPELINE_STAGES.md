# The Milan NIC data pipeline, stage by stage

*2026-07-11. The canonical prose reference for developers (what each stage does
and where its code lives) and maintainers (which knob changes which behavior,
what was measured, what breaks if you get it wrong). The visual twin is
`RX_PERF_TUNING_MAP.drawio`. Silicon history lives in `HEADER_SPLIT_DESIGN.md`,
the live state in `SESSION_HANDOFF.md`. Referenced from the source headers of
`sw/litex/milan_soc.py` (gateware) and `the-private-test-repo fpga/kl-eth/kl-eth.c`
(driver).*

Conventions used below. "CSR" means a register you can poke live with devmem.
"Elab param" means a Python elaboration parameter: changing it requires a
Vivado rebuild (about one hour; always launch 2 or 3 place-directive variants
in parallel, staggered by 90 seconds because the elaborations share one
pythondata git checkout). "Module param" means an insmod argument. Per-queue
CSR blocks have identical layouts: queue 0 base 0xf0003024, queue 1 base
0xf0003098.

## RX stages

### Stage R1: wire, RGMII PHY, MAC

Purpose: bits to AXIS beats. Code: `MilanMAC` in `sw/litex/milan_soc.py`, the
RGMII PHY wrappers, LiteEth core underneath. The datapath runs at 100 MHz
(`--milan-clk-freq 100e6`) and exceeds 1 GbE line rate; this stage has never
been a bottleneck. Trap fixed long ago: LiteEth `last_be` is one-hot, AXIS
`tkeep` is a mask; the M-A3 bug (no frames on the wire at all) came from that
mismatch.

### Stage R2: flow steering (RxSteer, 2-queue builds)

Purpose: route each frame to queue 0 or queue 1 so two flows' protocol work
can proceed independently. Code: `class RxSteer` in `milan_soc.py`. The hash
is the XOR parity of every bit of the IPv4 4-tuple, so placement is
deterministic per connection: you can engineer a split by picking client
ports, and consecutive integers often share parity, so a naive port sequence
lands 3:1 rather than 2:2.

Knobs and traps:
- `hash_sel` CSR at 0xf0003094: 1 forces everything to queue 0.
- Non-IP, IHL not 5, or truncated heads go to queue 0 unconditionally.
- The steer counters at 0xf000308c / 0xf0003090 misreport under dual-active
  load. Trust them only as single-active deltas.

### Stage R3: RSC aggregation (RingDMAWriter slots)

Purpose: coalesce an in-order TCP flow into large aggregates so per-unit CPU
costs amortize (the RX twin of TSO). Code: the slot machinery inside
`class RingDMAWriter` (`milan_soc.py`), four slots per queue (`n_slots=4`).
An aggregate closes on: PSH flag, segment cap, byte cap, idle timeout,
lifetime cap, a same-flow sequence gap, slot pressure (park), or CQ pressure.

Knobs (per queue, offsets from the queue base):
- `rsc_bufsz` (PAYCAP) at +0x44, currently 57344. Warning: the CSR field is
  16 bits wide; writing 0x1C000 silently stores 0xC000. Widening it is the
  documented RTL lever for aggregates larger than 64 KB.
- `rsc_tout` at +0x48, idle close in 100 MHz ticks. `ethtool -C rx-usecs`
  writes this AND the driver poll cadence together; poke the CSR afterwards
  if you need them decoupled (measured: flat either way at P4 with 16K pages).
- `rsc_segcap` at +0x54, currently 60. Setting 10 was measured harmful
  (256 Mbit at P4, chaotic flows).

Measured law (the ACK-hold law): any store-and-forward hold enters the peer's
round-trip measurement, so throughput self-limits at HOLD_BYTES divided by the
fill cycle. This produced the famous ~375 Mbit plateau at every flow count
until the cut-through ordering (stage R5) removed the hold.

### Stage R4: page placement (header split)

Purpose: split headers from payload so the payload lands page-aligned and the
consumer can use it without repacking. Headers go to a per-queue header ring
(32 slots of 128 bytes, `hs_hdr_base` CSR at +0x60); payload streams into
posted pages at offset zero.

Knobs:
- `hs_page_bytes`, elab param `--hs-page-bytes`: the page size the crossing
  arithmetic assumes (one compare plus two modulo-page bit slices in the RTL).
  Built variants: 4096 (hsq13), 16384 (hsq10, hsq12, hsq14), 32768 (hsq11).
  Effects measured: 16K broke the drop famine (28 to 5 drops/s at P2); 32K
  cleaned P8 (122 to 15 drops/s); 4K qualifies pages for the kernel's
  zero-copy page flip.
- LETHAL PAIRING: the driver's `hs_pgsz` module param must equal the gateware
  value. A mismatch makes the writer DMA gateware-page strides into smaller
  driver pages, overwriting kernel memory (Bad page map panic, 2026-07-11).
  Since hsq14 the gateware exposes the value in the `milan_dma_hs_pgsz_cap`
  CSR at 0xf000311c and the hsplit16+ driver refuses to load on a mismatch.
  On older gateware the CSR reads zero and the driver warns and trusts you.

### Stage R5: completion queue and BD publication

Purpose: tell the driver what landed, in a corruption-proof order. Code: the
CQ block inside `RingDMAWriter` plus the WB (writeback) FSM states.

Structure and invariants, in the order they were earned:
- The internal CQ is `cq_depth=32` entries per queue, stored in one 128-bit
  LUTRAM `Memory` (sync write, async read). It was previously an Array of
  flops whose mux trees were the single largest slice consumer (converting it
  saved 4866 LUTs, build hsq7).
- Completion BDs are 16 bytes, written to a DRAM ring of `KL_BD_ENTRIES=256`.
  BD kinds: v1 single (w1 carries the buffer address), v2 meta (length, mss,
  segment count, ack, window, PSH, header index in w0 bits 63:59), v3 page
  (w1 carries the page address; since hsq12 w0 also carries the fill length
  in bits 31:16 and the header index in bits 63:59).
- The drain OR-patches the live sequence number (bits 15:8) and drop count
  (bits 53:48) at write time.
- THE FULL GATE (hsq6): the drain stalls when wr+16 equals the driver's
  rd_ptr. Before this gate the hardware lapped the ring under reap gaps;
  at 64 entries that tripped the 8-bit sequence check and caused the "RX BD
  desync" self-heal storms, and at 256 entries the lap aliased to zero and
  corrupted silently (the original reverted BD-256 attempt). Overload now
  becomes counted drops, never corruption.
- CUT-THROUGH ORDERING (hsq12): the opener allocates only the page entry;
  the meta entry is allocated at close, so completed pages drain immediately
  and the meta arrives last. Before hsq12 the meta was allocated first and
  blocked every page behind it until close (the mechanical cause of the
  ACK-hold law). All six close paths gained a `cq_room` gate because closing
  now allocates.

### Stage R6: driver reap and repost

Purpose: consume BDs, pair pages, keep the hardware fed. Code:
`kl_rx_one_bd()` and `kl_poll()` in `kl-eth.c`.

Behavior a maintainer must not break:
- Pages pop from the posted FIFO strictly in order; v1 and v3 BDs carry the
  buffer address and the driver verifies it. In hs mode a mismatch means lost
  sync and triggers a full resync (never skip-recycle: skipped pages may
  still be DMA targets of open aggregates; that was a real panic).
- The desync detector tolerates empty polls and interrogates the hardware
  every 64th bad poll (BD_BASE lost, or WR moved past an unparseable slot).
- Reposting draws fresh pool pages and carries unfulfilled debt to the next
  poll. The reap itself measured about 5 percent of the NAPI hart: the driver
  is not the CPU cost.
- Poll cadence: 20 microsecond kick timers on activity (all queues since
  hsplit12), self-rearm at `coalesce_us` while active. Topology verdict on
  this 2-hart part: the winning arrangement is the pipeline (all NAPI in
  softirq on cpu0, receivers on cpu1, `threaded=0`). Symmetric fanout
  measured strictly worse (281-381 pipeline vs 220 threaded-unpinned vs 206
  threaded-pinned). Queue-1 drop excess is the pipeline's tail latency, not
  a bug. The hsplit15 kthread binding code remains for parts with more harts.

### Stage R7: delivery to the stack

Purpose: turn BDs into skbs. Two generations exist, selected by driver
version (STRICT gateware pairing):
- hsplit12/13 on hsq10/hsq11: assemble page frags per tag, build one skb at
  the meta, deliver. Simple, but the delivery waits for the aggregate close.
- hsplit14+ on hsq12+: cut-through. Every v3 page is delivered immediately
  as a synthesized TCP segment run: header bytes copied from the header ring
  slot named by the v3's header index, IP total length patched, TCP sequence
  advanced by the bytes already delivered, PSH stripped except on the final
  unit, GSO metadata set per chunk, CHECKSUM_UNNECESSARY. The meta then only
  updates statistics and clears the per-tag state. Binding is lost-meta safe
  because a header-index change on a tag means a new aggregate. Correctness
  rests on RSC only ever aggregating in-sequence segments, so every early
  unit is a valid in-order prefix.
- Measured: cut-through holds the single-flow record (329) but currently
  loses multi-flow to the hsq10 keeper (staircase granularity plus per-unit
  cost); the parked follow-ups are 8K pages or chunk batching in the v3
  handler.

### Stage R8: the consumer

The consumer choice decides the record. All four lanes measured on the keeper:
- Socket read with copy (recv_spin, iperf3): 363-381 Mbit sustained at P4.
  The copy costs one cold DRAM read per cache line (about 18 cycles per 8
  bytes at 100 MHz); it is two thirds of the application hart.
- MSG_TRUNC (recv_trunc, ACKs but never copies): 585-594 sustained. This is
  the stack ceiling and the proof the goal is reachable by a copy-free
  consumer.
- AF_PACKET TPACKET_V3 mmap ring (tools_recv_ring.c): 124. Refuted: the
  kernel memcpys every unit into the ring on the NAPI hart; the zero-copy is
  consumer-side only.
- TCP_ZEROCOPY_RECEIVE page flip (tools_recv_zc.c on hsq13 at 4K pages):
  110-113 at 87 percent flipped. The mechanism works and the kernel path is
  already batched (vm_insert_pages, batch size 32); the cost is equilibrium
  economics: shallow queues make the per-call overhead land per-page, and
  forcing queue depth with paced consumption hits the receive-window wall
  instead (2.7 and 19.5 Mbit in the paced variants). Closed on this core and
  kernel.
- The remaining above-500 lane is AF_XDP with driver zero-copy support,
  which is campaign-scale work. The AVTP product plane does not need it.

## TX stages, briefly

TX is documented here for completeness; it holds 582-646 Mbit with two
processes and is scheduler-fairness bound, not NIC bound.
- T1: the driver builds descriptors in a cached BD ring (256 entries), one
  MMIO doorbell per batch, HW-TSO segments 64 KB GSO frames in gateware.
- T2: the reader DMAs payload straight from DRAM (cache state irrelevant),
  so TX pays almost no per-byte CPU on the send side.
- T3: the datapath (classifier, optional CBS shaper which resets DISABLED
  since the CBS_EN_RST bug, MAC) runs at 100 MHz.
- The hidden dependency: TX throughput requires its ACK stream (an RX flow)
  to be processed promptly; TX collapses if RX delivery stalls. Always gate
  TX after any RX change.
- Known follow-up: the kernel lacks CONFIG_NET_SCH_FQ, so two competing
  senders on the single netif queue are a fairness lottery (one can starve
  at about 82 Mbit).

## Obsolete and staged-for-removal code

Removed in the 2026-07-11 cleanup:
- Driver `rxzc` module param (`kl_rxzc_param`): declared and exported but
  never branched on; the build_skb path it once selected was deleted eras ago.

EXECUTED 2026-07-11 as an ELABORATION FOLD (better than deletion: the legacy
path stays in the source for forensics builds, ships folded out):
- Gateware: `RingDMAWriter`/`RingDMAReader` gained `legacy_ring` (SoC/CLI
  default FOLDED; `--legacy-ring` opts the fallback back in). Mechanics:
  `bd_shape` (a constant 1 when folded) hardwires every datapath SHAPE mux to
  the BD arm so the ring cones die at synthesis; `bd_mode` (bd_base != 0)
  remains the runtime ARMING gate at every dispatch site, so an old `bd=0`
  driver on folded gateware PARKS (frames overflow the drop-FIFO, counted
  ingress drops) instead of DMA-writing through `base`/address 0 - the
  hs_pgsz lethal-pairing lesson applied. Python-conditional arms (not
  generated when folded): the IDLE byte-ring dispatch + CHECK state and the
  WAIT_B ring commit (writer); the reader is read-only, its ring arms
  constant-fold and a bd_base==0 doorbell lands in the existing bad-BD
  resync.
- Verification: the ENTIRE BD test set was run against BOTH shapes (defaults
  temporarily flipped): test_ring_bd.py 40+2 and test_tx_bd.py all green
  folded; plus two permanent regressions - test_bd_folded_equivalence
  (bit-identical BD delivery) and test_bd_folded_unarmed_quiesce (bd_base=0:
  zero DMA writes, drops counted). test_ring_dma.py / test_ring_tx.py /
  test_ring_writeback.py exercise the byte-ring path and run on the legacy
  class default (True) - they cover `--legacy-ring` builds.
- Driver: `kl_rx_one()`/`kl_rx_ring_init()` (the bd=0 A/B lever) still exist
  and now require a `--legacy-ring` gateware; on folded gateware bd=0 simply
  never brings the interface up (probe path returns -ENODEV as before, and
  the HW parks even if forced).

## Build and driver lineage (what "hsqN" and "hsplitN" mean)

| Gateware | Change | Driver pairing |
|---|---|---|
| hsq3 | 2-queue keeper era, hs on q0 only | hsplit9/mslot60d |
| hsq4/hsq5 | CQD=32 single queue; livelock fix | hsplit9 |
| hsq6 | BD-ring full gate (the lap fix) | hsplit10 (BD 256) |
| hsq7 | CQ storage to LUTRAM (slice diet) | hsplit10 |
| hsq8 | 2-queue with rx1 hs-capable, strip-probes | hsplit11 (per-queue hs scoping) |
| hsq9 | META-at-head pressure fix (silicon-inert) | hsplit11 |
| hsq10 | 16K pages. THE RECORDS KEEPER | hsplit12 (hs_pgsz) |
| hsq11 | 32K pages | hsplit13 (napi_w) |
| hsq12 | Cut-through CQ ordering | hsplit14 (per-page delivery) |
| hsq13 | Cut-through at 4K pages (zc qualifier) | hsplit14 |
| hsq14 | hs_pgsz capability CSR (pairing hardening) | hsplit16 (probe-check; hsplit15 = the kthread-binding negative) |
| cbse | CBS sequential slope engine (AREA-70: -6.7K LUTs, multicycle XDC gone) | hsplit16 (TX-side change only) |
| cbsf | + byte-ring fold (legacy_ring, FOLDED default; --legacy-ring restores) | hsplit16 bd=1; the bd=0 A/B lever needs a --legacy-ring build |

Records as of 2026-07-11: TCP RX P4 381 steady / 374 over 120 s (hsq10 +
hsplit12), single-flow 329 (hsq12 + hsplit14), MSG_TRUNC ceiling 585-594,
TX 582-646, UDP TX 24 / RX 65 goodput. Every number's method: peer tx_bytes
5-second deltas, first and last intervals excluded, fresh client ports per
cell, TX gate after every RX change.
