# PTP timestamp metadata pipeline — root cause & fix (2026-07-13, Phase B)

## Symptom
Phase B (HW frame timestamps → SO_TIMESTAMPING) brought up the kl-eth record
consumer (`hwts1`) against arty_v10 silicon: the dma-ts WishboneDMAWriter armed
correctly (base/length/loop/enable readback OK at 0xf0003100) but its `offset`
stayed **0 forever** — zero records — while ptp4l demonstrably pushed ~19 TX +
~3 RX 0x88F7 frames/s through both ptp_ts_top taps. ptp4l in HW mode faulted
with "timed out while polling for tx timestamp".

## Root cause (found in sim, not on the bench)
`ptp_ts_top`'s metadata path had **no testbench anywhere** (tb/verilator/
ptp_sync only covers the CSR CDC). A new harness — `tb/verilator/ptp_ts`,
frames at both real ingress profiles — reproduced the silence immediately:

The original core decided a record at *timestamp-handshake return* time:
`if (dest_req && is_ptp)`. `dest_req` arrives a fixed ~6-10 clks after SOP
(pulse-CDC + 4-phase handshake), but `is_ptp` (registered ethertype compare)
only becomes true once frame **beat 1** has arrived. That races both ways:

- **slow beats** (MII 100M into the 50 MHz datapath ≈ one beat / 32 clks —
  the Arty profile): dest_req fires while eth_type still holds the *previous*
  frame's value → the FIRST PTP frame after reset records nothing, and every
  subsequent one pairs the current timestamp with stale metadata
  (one-frame-late seq). Exactly the silicon behavior.
- **back-to-back minimal frames** (TX / GMII profile): dest_req can land
  *after* tlast instead — record lost the other way.

Two adjacent latent bugs surfaced by the same TB:
- `axis_mux_rr_2in_1out` drove `m_tvalid = s_tvalid && s_tready`, i.e. valid
  combinationally depends on ready — an AXI-Stream protocol violation that
  deadlocks against any sink that waits for valid before asserting ready.
- The source-domain capture overwrote `src_in` mid-handshake if a new SOP
  arrived before `src_rcv` returned (only possible <8 clks apart — but free
  to guard).

## Fix (hdl/ptp_timestamp/ptp_ts_core.sv, commit 32e5c41)
Decoupled capture / qualify / emit:
- `dest_req` only fills a holding register (`ts_hold`, one per SOP);
- the frame **qualifies at TLAST**, when `eth_type_valid && is_ptp &&
  ptp_seq_id_valid` are all definitively known (`qual_pend` + seq snapshot);
- the emitter fires on `qual_pend && ts_hold_v` — either arrival order works;
- a non-PTP tlast **consumes** its capture (can't poison the next frame);
  a new SOP clears a stale unpaired qual (missed capture self-heals);
- capture skipped while a handshake is in flight (`!src_send`).
Plus the mux violation fixed (`m_tvalid = s_tvalid`).

## Record contract (from the TB — the kl-eth driver matches this)
16 B per record, two 64-bit beats in order: **word0 = timestamp** (integer ns
of the DISCIPLINED 0x500 PHC counter — same epoch as /dev/ptp0), **word1 =
{40'0, seq_id[15:0], 7'0, direction}** (dir 0=RX 1=TX). `seq_id` compares
equal to the frame's big-endian sequenceId — **no byte swap in the driver**.
Records arrive in wire order per direction (RR mux across directions).

## Gates
- NEW `tb/verilator/ptp_ts`: 7 cases ALL PASS (slow-first-frame, slow-second,
  fast RX, fast TX + o_tx_ts_ready pulse, non-PTP no-poison, ts_m_axis
  backpressure, TX+RX interleave). TB monitor samples pre-edge (a post-edge
  monitor misses the beat consumed at a backpressure-release edge — TB bug
  found while blaming the DUT).
- milan_dp harness: 26 checks, 0 failures (fixed core inside the datapath).
- Yosys portability: milan_datapath re-passes (also fixed: run.sh was missing
  aaf_talker_i2s.sv since the MVP-talker merge — unrelated omission).

## Driver / DT side (the-private-test-repo 5b942c3, kl-eth `hwts1`)
- dma-ts record consumer: coherent 4 KB loop ring, empty-slot sentinel
  (word0==0, re-zeroed on consume → no MMIO polling); TX = one-deep pending
  skb completed via `skb_tstamp_tx` (IRQ_TX_TS_READY drain + NAPI fallback +
  20 ms unstick); RX = tiny wire-order fifo matched by FIFO ORDER with seq as
  the consistency check (pdelay_resp & resp_fup share a seq — order, not seq
  lookup, disambiguates), bounded 200 µs late-record poll.
- `ndo_hwtstamp_get/set` + HW caps in `get_ts_info`; engine **lazy-armed** on
  the first enable so stale-DT boards are never poked; `dma_ts_addr=`
  module param overrides a rotted DT window explicitly.
- **DT rot fixed**: dma-ts is 0xf0003100 on ALL current builds (dts carried
  0x3038/0x3064/0x3074 across three generations); the dts `tlm` window
  (0xf0004000) now points at the SDRAM controller CSRs — dropped (block is
  stripped on current builds). Sub-page ioremap is page-granular, which is
  why nothing crashed — reads just returned other blocks' registers.
- Latent Phase A bug fixed on the way: `kl_ptp_adjfine` used `div_s64`
  (s32 divisor!) with 65536000000 → truncated to 1111490560 → every adjfine
  over-corrected ~59x. Never bitten because the GM role doesn't servo;
  would have wrecked the first real slave lock. `-Woverflow` caught it.
- set_rx_mode now reflects any joined multicast group as ALLMULTI (the MAC
  has no per-group filter) — standalone ptp4l (joins 01:80:C2:00:00:0E) was
  deaf without a tcpdump holding promisc (commit 8bbe361's finding).

## Validation status
Fixed gateware is in the `hwts1` arty sweep (eppo/asl/eto, launched
2026-07-13). Remaining on silicon once a seed meets timing: JTAG-load →
`ptp4l -f gptp_gm.cfg` (no -S) as GM → follow_up flows with HW t1 (TX
records), pdelay t2/t3 via RX records, pw0 lock quality vs the rms 3-4 ns
SW-ts baseline; then the RX-pad true-length gate (PTP-trim becomes a no-op,
TCP RX ≥ the 94 Mbit switch baseline, 0-drop). Arty-as-slave with HW ts =
direct-cable session (switch never masters into board ports —
GPTP_RXPAD_ROOTCAUSE.md matrix).
