<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# maap — KL_pp_maap (IEEE 1722-2016 Annex B) unit suite

The MAAP engine against **independent** expectations: frame bytes from the
Figure B.1 offsets, the walk from Table B.7, timer bounds from B.3.4, the
compare_MAC rule from B.3.6.4 — never DUT logic. The engine runs with its
real services (KL_pp_prng kinds 5/6/7, KL_pp_timer_service compressed to
1 ms = 10 clk, KL_pp_tx_slots); the C++ side plays the TX arbiter's lane and
the talker's allocator face; records are injected pre-parsed exactly as the
validator's MAAP lanes deliver them.

What it proves (U0..U16):

- cold start: `generate_address` inside the Table B.9 pool with the block
  fit, then 4 byte-exact PROBEs (1 + `MAAP_PROBE_RETRANSMITS`) at spacings
  measured inside the exclusive (500, 600) ms probe bounds, the first
  ANNOUNCE back-to-back with the fourth (probeCount!), the claim valid only
  from DEFEND, and the (30, 32) s announce cadence;
- the full Table B.7 conflict matrix: rProbe! defended in DEFEND with the
  byte-exact B.3.6.6 overlap fields and **no** tie-break, ignored or yielded
  in PROBE by compare_MAC; rDefend!/rAnnounce! yielding unconditionally in
  PROBE and by compare_MAC in DEFEND; footnote-b non-overlap and empty-range
  ignores; reserved message types ignored (B.2.2); maap_version tolerance
  (B.2.3.2);
- yield mechanics: re-randomized range (never the seed), fresh 4-probe walk,
  re-address counter, and the per-source conflict fan-out lowest-first;
- the allocator seam under the shim contract: accept-and-answer at the
  accepting edge, refuse while probing or parked, grant base + s in DEFEND,
  refuse s >= count (with the count change fanning out conflicts), RELEASE
  acknowledged as a no-op;
- the engage arcs: Release! (engage fall) tears down with **no** PDU
  (footnote c), PortOperational! (link bounce) restarts with a fresh range,
  and footnote-a seeding probes the provisioned offset first.

Run: `make` (exit 0 = PASS).
