<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# srp_encoder — KL_srp_encoder + KL_srp_domain + KL_srp_vlan suite

Exit 0 = PASS. `make` builds `srp_tb_wrap` (encoder wired to a **real**
`KL_pp_tx_slots` pool; Domain and VLAN singletons stand-alone) and runs
180 checks against an **independent** C++ packer written from 802.1Q
§10.8.1/§35.2.2 and Milan §4.2.7 — never from the RTL. Every captured frame
crossed the actual slot RAM through its serialize port.

## What it proves

**Encoder (docs/architecture/10 §3 + §7)** — E1..E12:
- byte-exact MRPDU emission for single- and multi-attribute PDUs, MSRP and
  MVRP (MVRP has **no** AttributeListLength field);
- `AttributeListLength` counts the VectorAttributes **plus** the
  AttributeList EndMark (802.1Q §35.2.2.6) — checked both byte-exact and at
  the hand-computed offset (a 4-byte Domain vector lists as 9, not 7);
- dual EndMark always explicit, so the EndMark precedes any MAC padding
  (Milan §4.2.7.1.3) even on a 30-byte frame;
- sorted-run detection: consecutive `{stream_id, DA}` (Talker, both fields
  stepping), `stream_id` (Listener), `{SRclassID, priority}` (Domain) and
  VID (MVRP) sequences fold into one VectorAttribute with NumberOfValues up
  to the table depth (12); a same-type non-successor (stream_id steps, DA
  frozen) starts a new vector in the same message;
- ThreePacked radix-6 and FourPacked radix-4 packing including tail padding
  (NoV=3 and NoV=5 lanes hand-computed);
- cadence aggregation: N pushed events sit silently, then ONE T-MRP-JOIN
  tick produces ONE alloc + ONE commit + ONE frame (the functional advance
  over the reference platform's one-frame-per-event vectors);
- LeaveAllEvent injection per application on the first VectorHeader of the
  next PDU only, consumed by that PDU;
- per-participant independence (an MSRP tick never drains the MVRP table),
  simultaneous ticks serialize MSRP-then-MVRP, full-table backpressure on
  the push handshake, unknown-type drop strobe.

**Domain (10 §6.1, F10.2)** — D1..D9: declare defaults {class A id 6,
priority 3, VID 2} at startup/LINK_UP (New); adopt a differing received
Class A Domain as withdraw-old (Lv) + re-declare (New) + one DOMAIN_CHANGE
strobe + class-D levels; identical parameters are no change; the certified
two-class bridge shape (FirstValue {5, 2, VID}, NoV=2) surfaces Class A as
value 1 with priority 3 by the §3 range rule; non-covering vectors ignored;
periodic/LeaveAll re-join the ADOPTED declaration and never revert; revert
happens on LINK_DOWN only, LINK_UP re-declares the defaults. Domain TX is
independent of gPTP state structurally — the module has no gPTP port.

**VLAN (10 §6.2, corrected F10.3)** — V1..V9: per-VID refcount keyed by
each user's OWN stream VID: two users of one VID produce exactly one join
(New, then JoinIn on the cadence); a Domain VID change moves nothing — a
new user brings the new VID and two VIDs are briefly live while the old one
stays frozen until its LAST user leaves (Lv); LeaveAll/periodic re-join
every VID with users; unknown-VID leave and table overflow are error
strobes, never wire events.

**Bridge** — B1: the harness plays the not-yet-landed event router, feeding
both FSMs' own re-join declarations through the encoder into byte-exact
frames end-to-end.

## Mutation ledger (each planted, seen to bite, then restored)

| # | Mutation (sed on the RTL) | Suite response |
|---|---|---|
| M1 | `KL_srp_encoder.sv`: AttributeListLength computed − 4 instead of − 2 (EndMark excluded) | 14 FAIL — every MSRP byte-exact check + the explicit listlen-offset check (`got 0007`) |
| M2 | `KL_srp_encoder.sv`: `ext_w` forced 0 (sorted-run detection disabled) | 12+ FAIL — E4/E5/E10/E12 lengths and NoV fields (every value emitted as its own vector) |
| M3 | `KL_srp_vlan.sv`: leave branch takes `found_v_r` alone (Lv on EVERY leave, refcount ignored) | 2 FAIL — "V6 a remaining user keeps the VID declared", "V6 still two live entries" |
| M4 | `KL_srp_domain.sv`: `surf_prio_w = rxdom_prio_i` (FirstValue equality instead of the §3 range rule) | 2 FAIL — both D6 two-class-shape checks |

Restored tree: `180 checks: 180 PASS, 0 FAIL`, `scripts/lint_hdl.sh` clean.

## Notes / interpretations recorded

- F10.2 says "adopt received FirstValue"; an endpoint declares only Class A,
  so what is adopted and re-declared is the **surfaced** Class A tuple
  {6, prio_first + (6 − SRclassID_first), VID} per 10 §3 — for a NoV=1
  class-6 vector the two readings are identical.
- The F10.2 revert edge (ADOPTED to DEFAULTS) fires on LINK_DOWN: the
  class-D levels revert at LINK_DOWN (nothing is declared on a dead link);
  LINK_UP performs the default declaration.
- A pending LeaveAll with an empty table rides the next PDU that carries
  attributes; Domain and VLAN re-declare on the LeaveAll cycle, so that PDU
  is the immediate next one in practice.
- The TX request face (`txreq_valid_o` held until accept + committed slot
  handle) matches the since-landed `KL_pp_tx_arbiter` requester contract
  (`req_valid_i[i]` + committed `tx_slot_i`, grant completes).
