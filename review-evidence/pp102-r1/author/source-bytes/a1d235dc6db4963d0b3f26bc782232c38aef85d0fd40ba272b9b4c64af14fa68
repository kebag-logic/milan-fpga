<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# originator — KL_pp_originator suite

Proves the [03 §5](../../docs/architecture/03_packet_engine.md) originator +
inflight table (`hdl/packet_engine/KL_pp_originator.sv`): `make` = build +
run, exit 0 = PASS, 104 checks.

The C++ harness is an independent model, never DUT logic: it implements a
stub of the exact `KL_pp_timer_service` arm/expiry port protocol (arm =
{slot, owner tag, absolute-ms deadline}, cancel clears the armed bit, a
fired slot self-disarms), a
hold/release tally standing in for the `KL_pp_tx_slots` pool, and a
per-owner sequence-counter mirror — then checks every routed/failed
exchange, every pulse payload, and the arm-op stream op by op.

Covered: issue → grant carries the per-owner seq (previewed on `iss_seq_o`
so the engine can serialize it into the PDU first) + hold + send. The timer
does not arm while that handle waits in the TX lane queue, even if more than
the timeout duration passes. Serializer acceptance arms the full deadline =
now + the port-supplied timeout (T-constants stay in 08 F08.1, never in RTL);
response matched on {key, seq} routes to the owner,
disarms and releases; first timeout → ONE re-send request of the SAME held
slot (Milan's exact duplicate, [05 §6.4](../../docs/architecture/05_acmp_engine.md)
A13; the original seq still routes after the retry). The retry timer also
waits for serializer acceptance; second timeout → fail to owner + release with no timer cancel (the slot
self-disarmed); responses after fail and mismatched {seq}/{key} are
silently ignored but counted (F09.4 of
[09 §3](../../docs/architecture/09_verification.md), 8-bit counter proven to
wrap 255 → 0); three interleaved inflights route independently in scrambled
order; table-full refusal at INFLIGHT_P = 12 with the freed id reused;
response-beats-expiry priority both for another entry (response processed
first, retry the next cycle) and for the same entry in the same cycle (route
once, never retry/fail); stale expiries for freed entries and foreign owner
tags are inert; a serializer acceptance concurrent with another entry's
response is parked and later arms the correct timer. A cancellation concurrent
with another entry's response is also parked, then releases its held slot and
disarms its timer without loss. Final invariants: every
arm/cancel used a legal slot index,
every hold released exactly once, no armed slot and no inflight entry leaks.

Historical mutation baseline from 2026-08-11 at 81 checks
(backup/sed/run/restore, rerun green):
- CAM match drops the seq compare → 3 of 81 fail (mismatched-seq response
  routes; miss counters diverge).
- `retried` never set (retry forever) → 6 of 81 fail (second timeout
  re-sends instead of failing; entry and slot leak; post-fail response
  routes).
- response path forgets the slot release → 6 of 81 fail (hold/release
  balance broken across A/C1/C2/E/F and the final tally).

The 2026-08-19 concurrent-event regression is also mutation-proven at the
current 104-check shape. Ignoring the parked cancellation after a different
entry's response fails 6 of 104 checks, including the busy-table, timer, hold,
and release invariants. Restoring cancellation parking passes 104 of 104.
