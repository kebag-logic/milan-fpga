[A114] Scheduling update, 2026-09-15: the owner deferred physical I2S/TDM interface and wire-to-pin audio verification to [#448](https://github.com/kebag-logic/milan-fpga/issues/448) and [milestone 9](https://github.com/kebag-logic/milan-fpga/milestone/9), due December 31, 2026, because suitable measurement equipment is unavailable. The corresponding serial-audio evidence remains open. This issue retains its gPTP synchronization, GM loss/return, wire protocol and fabric-publication scope; none of its acceptance boxes is marked passed by the deferral. Full issue closure still requires the linked deferred evidence. Original scope and acceptance are preserved below.

---

## Objective

Record the silicon evidence that closes the fabric-gPTP product transition:
synchronization of one AX7101 DUT against the Milan-validated reference peer,
GM loss and return induced through the peer or the bench switch, wire
conformance, publication ownership, and unchanged audio behavior. Two matched
FPGA DUTs are not required.

Subticket of #110; its result gates the physical acceptance in #116.

## Hardware dependency

Bench roles as of 2026-09-06: `pw0` is retired; `pw1` is the ATDECC controller
(la_avdecc) and the PipeWire endpoint host; the Ubuntu server carries the two
inline capture taps; the AX7101 console and JTAG sit on the build box. The
owner must confirm bench power and connectivity before starting.

## Already delivered

- [x] `fuzz_ptp` exists in `tsn_fuzz` and runs against the integrated plane
      (PR #123 and its follow-ups). Donor allowances are retired by the parent
      issue lanes.

## Bench sequence

1. Build and flash the AX7101 DUT from the exact candidate commit, dependency
   pins, VERSION, firmware, descriptor image, and manifest; record the
   reference peer's firmware identity. Refuse VERSION skew between the build
   and the flashed image.
2. Prove the DUT port reaches asCapable against the reference peer with no
   software gPTP daemon; capture Sync, Announce, Pdelay cadence, and the 15 ms
   Pdelay response turnaround.
3. Induce GM loss and return through the reference peer or the bench switch and
   measure them against the recorded baseline, including automatic recovery and
   the resulting stream state.
4. Read the fabric-driven publication CSRs and `tu` on silicon and correlate
   them with the wire capture.
5. Run Behave, la_avdecc, Hive, latency, and audio end-to-end checks with the
   plane selected; record tone/continuity evidence.
6. Run the latency measurements owned by #64 and the egress-window exposure
   measurements owned by #213 when their prerequisites are present.

## Acceptance

- [ ] The AX7101 DUT reaches and retains asCapable against the Milan-validated
      reference peer inside Milan limits with compliant message
      intervals/turnaround and no software gPTP daemon.
- [ ] GM loss and return, induced through the peer or the bench switch, recover
      automatically within the documented bound.
- [ ] Publication words and `tu` are demonstrably fabric-owned on the booted
      image.
- [ ] External conformance, latency, and audio continuity pass without a stale
      or skipped mandatory row.
- [ ] Findings include topology, capture points, raw artifacts, exact hashes,
      tool revisions, and methodology under `docs/findings/`.


