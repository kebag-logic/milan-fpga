# RX performance tuning map  -  maintainer's guide

*2026-07-11. Companion to **`RX_PERF_TUNING_MAP.drawio`** (open in
diagrams.net; three lanes: gateware / driver / kernel+consumer, every box
carries the knob, its location, current value, and the measured effect). This
page is the how-to-use; the diagram is the map; HEADER_SPLIT_DESIGN.md is the
silicon history; SESSION_HANDOFF.md is the live state.*

## How to change behavior safely (the loop)

1. **Find the knob on the diagram**  -  each is tagged with where it lives:
   elaboration param (rebuild, ~1 h, sweep 2–3 place directives, stagger 90 s),
   CSR (devmem-pokeable live, per-queue: q0 base `0xf0003024`, q1 `0xf0003098`,
   identical layouts), or module param (insmod, seconds).
2. **Respect the STRICT pairings** (violations are lethal, not degraded):
   `hs_pgsz` (driver) == `--hs-page-bytes` (gateware)  -  mismatch DMA-overruns
   kernel memory (panicked 2026-07-11); BD-256 drivers (hsplit10+) need the
   hsq6+ drain gate; hsplit=2 needs rx1-hs gateware (hsq8+); hsplit14+ needs
   hsq12+ (cut-through CQ order).
3. **Measure with the cell harness** (scratchpad `hscell3.sh`-class: peer
   `tx_bytes` 5 s deltas, first+last interval excluded, fresh cport bases every
   cell  -  TIME_WAIT silently kills flows), **always TX-gate after RX changes**,
   and check the forensic trio: per-queue drops (`0xf000303c`/`0xf00030b0`),
   dmesg desync/pairing, flow evenness.
4. **Interpret against the two laws** (bottom-right of the diagram): if drops
   > ~5/flow/s, absorbency is the problem (drop law); if drops ≈ 0 and
   throughput plateaus with idle CPU, a delivery hold is in the TCP loop
   (ACK-hold law)  -  find what buffers before ACK.

## The ranked extraction list (as of 2026-07-11)

1. AF_XDP ZC driver support: the one remaining above-500 consumer lane
   (zc-flip MEASURED and closed: 110-113 at 87 percent flipped; kernel batching
   exists, the economics do not work at 100 MHz. See PIPELINE_STAGES.md R8).
2. PAYCAP CSR widening (16-bit truncation): bigger aggregates for the copy lane.
3. Cut-through multi-flow: 8K pages or driver chunk-batching (hsplit14 v3 path).
4. `CONFIG_NET_SCH_FQ`: TX 2-proc fairness.
5. AREA-70: headroom for the AVDECC product blocks (byte-ring removal staged in
   PIPELINE_STAGES.md).
6. Hardening: SHIPPED (hsq14 capability CSR at 0xf000311c + hsplit16 probe-check).

## Regression net

`test_ring_bd.py` (42 tests incl. the full-gate, hs pressure, cut-through,
byte-ring-fold equivalence/quiesce
ordering + livelock probe)  -  plain python, ~25 min; every model mirrors the
real driver contract (RING_RD after reap, =0 after heal; defer-not-skip
pairing). Sim green before P&R, always.
