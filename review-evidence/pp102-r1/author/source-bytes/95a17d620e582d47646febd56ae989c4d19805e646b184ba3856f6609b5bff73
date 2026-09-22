<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# tb/rx_validator — KL_pp_rx_validator suite

Exit 0 = PASS. `make` builds with Verilator and runs `sim_main.cpp`
(tally line: `276 checks: 276 PASS, 0 FAIL`).

## What it proves

The shared RX front end of [03 §3](../../docs/architecture/03_packet_engine.md):
the F03.2 flow, the front-end F03.6 rules, and F03.4 field extraction —
against an **independent C++ frame model** that reads expectations straight
from hand-built byte-exact wire frames (documented offsets, never DUT logic).
The RX slot pool is a **C++ stub of KL_pp_rx_slots' write-side port
protocol** (combinational alloc grant, byte accumulation until `wr_last`,
commit/abort bookkeeping).

- **DA gate**: own unicast + `91-E0-F0-01-00-00` pass; foreign unicast and
  foreign multicast count `rx_da` (F11/F11b); a frame ending before the DA
  completes counts `rx_da` (F17a).
- **EtherType gate**: non-0x22F0 on a 1722.1 DA counts `rx_ethertype`
  (F10); a 1722.1-DA frame ending before the EtherType completes too (F17b).
- **Subtype demux**: FA/FB/FC accepted; unknown subtype dropped + counted +
  slot aborted (F9). FB message types demux to AEM/MVU/AA (F1/F6/F6b).
- **V8**: `h != 0` and `version != 0` dropped + `rx_version` + abort
  (F8/F8b, F09.4 TOL rows).
- **V1**: `cdl + 12 > frame payload` dropped + `rx_length` + abort (F7);
  header torn mid-common-header ditto (F17c/F17d); inbound `cdl + 12`
  beyond the slot capacity dropped (F16).
- **V2**: padded 64-B minimum frame parsed by cdl — committed slot holds
  exactly `cdl + 12` bytes, padding excluded (F2).
- **V3**: Milan 56-B truncated ACMPDU accepted with every field (F3);
  IEEE 2013 short form accepted with tail fields (sequence_id @48,
  unique_ids) read as 0 (F4).
- **V9**: MSRP (`01-80-C2-00-00-0E` + 0x22EA) and MVRP
  (`01-80-C2-00-00-21` + 0x88F5) frames routed **byte-exactly** onto the
  MRP stream, one `mrp_last`, zero slot/counter interaction (F12/F13);
  LLDP (0x88CC) and 802.1X (0x888E) on the same group DAs ignored with no
  count and no leak (F14/F14b) — DA alone is not sufficient.
- **Parsed-header beat**: field-by-field compare (protocol, msg_type,
  status/valid_time, cdl, src_mac, controller/target EIDs, sequence_id,
  u/cr, opcode, operands, rx_slot handle) for AECP (F1/F2), ACMP BIND_RX
  (listener unique_id selected, F3) and PROBE_TX (talker side, F4), ADP
  (valid_time in the status lane, ctlr = 0, F5).
- **Slot protocol**: commit-on-good with byte-exact slot content; abort on
  every mid-frame rule failure; a pool-refused alloc is silent here
  (`rx_overrun` belongs to the pool) — no commit, no abort, no counter (F15).
- **Robustness**: rx_valid bubbles mid-frame (F18), back-to-back
  MRP → AECP → ACMP frames with no idle gap (F19), `rx_da` saturates at
  0xFFFF and never wraps (F20), and a good frame still parses after the
  saturation soak (F21).

## Known model limits

- The stub grants slots round-robin; the real pool grants lowest-free.
  The suite treats the granted index as an opaque handle (checked equal
  between `hdr_rx_slot_o` and the stub's granted slot), so grant policy is
  deliberately out of scope here (it is proven in `tb/rx_slots`).
- The early-alloc design decision (slot requested right after the
  EtherType gate) means a full pool counts `rx_overrun` in the pool even
  for frames that would later fail subtype/version/length; the suite pins
  the validator side of that contract (refusal = total silence).

## Mutation proof (all planted breaks bite; restored + rerun green)

| Mutation | What was broken | What fails |
|---|---|---|
| M1 | h/version gate inverted (`!= 4'h0` → `== 4'hF`) | F8/F8b: `rx_version` stays 0, bad frames commit + emit hdr beats instead of aborting (8 FAILs) |
| M2 | V1 boundary off-by-one (`pcnt_end >= cdl+12` → `>`) | F1 and every exact-fit frame: counted `rx_length` + aborted instead of committed (101 FAILs) |
| M3 | V9 DA-alone routing (MSRP EtherType pair check dropped) | F14: 60 LLDP bytes leak onto the MRP stream (1 FAIL) |
