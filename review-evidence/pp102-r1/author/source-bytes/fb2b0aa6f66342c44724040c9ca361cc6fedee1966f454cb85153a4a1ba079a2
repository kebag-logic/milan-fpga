<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# adp_engine — KL_adp_engine suite

Proves the ADP engine (`hdl/adp/KL_adp_engine.sv`) against
[04](../../docs/architecture/04_adp_engine.md) in full: `make` = build + run,
exit 0 = PASS, 533 checks.

The top (`tb_adp_top.sv`) is pure wiring: the engine plus the **real
`KL_pp_prng`** (draw port tapped), so the two DISTINCT delay-draw kinds are
graded against the actual rejection sampler. Everything else is an
independent C++ model, never DUT logic: the timer-service arm/expiry
contract (absolute-ms deadlines, harness-owned `now_ms`), the
`KL_pp_tx_slots` alloc/write/commit protocol (one-cycle grant a cycle after
the request, grant withholding, in-slot write bounds), the `KL_pp_rx_slots`
sync-read/free contract, the dispatch valid/ready pop face (txn packed by an
independent 393-bit `pp_txn_t` codec), and an 82-byte wire-frame builder
written straight from the 04 §3 field-sourcing table + F04.5 offsets.

Covered: byte-exact ADPDU for **both** message types (all 82 wire bytes,
entity_id at wire byte 18, F04.6 caps 0x0000C588, cdl 56, Δ5 valid_time
10/0); the F04.2 advertise SM — startup kind-1 draw, T-ADP-ADV 5 s re-arm
per send, DISCOVER (eid 0 / own / foreign / ignored-in-DELAY), GM_CHANGE
re-advertise + GPTP_GM_CHANGED tick + gm sampled at build, LINK_DOWN with
**no** departing then kind-2 re-entry, disable ⇒ ENTITY_DEPARTING; the 04 §5
available_index doc rule (0 at power-up, ++ after each AVAILABLE, departing
carries the pre-reset value then resets to 0); statistical draw separation
(40 kind-1 ≤ 2000, 40 kind-2 ≤ 4000, kind-2 max > 2000, maxima differ); the
F04.3 per-sink discovery SM — gm/domain guard both ways, multi-sink fan-out
once each, restart pair (DEPARTED then DISCOVERED) on stale index,
stale+foreign-GM departure, interface_index mismatch ignored (record
untouched), DEPARTING per matched sink, T-ADP-NOADP = rx valid_time (20 s
and 10 s arms) with aging ⇒ DEPARTED, unbind disarm + cancel; and the pool
protocol invariants accumulated over the whole run (never oversize, never a
write before grant, alloc_req always one cycle, one TX request per
committed 82-byte frame).

Interop note: the available_index rule implements the DOC (04 §5 /
IEEE §6.2.2.15) and **diverges from the reference platform's
every-ADPDU increment** — adjudication against live controllers
(Hive / la_avdecc) is required before cutover; the engine banner carries
the same warning.

Mutation-proven 2026-08-11 (backup/sed/run/restore):
1. merged draw kinds (`ADP_DRAW_KIND_START_C` → `ADP_DRAW_KIND_DELAY_C` in
   the request picker, the review §8 item 5 bug class) — **291 of 533
   fail** (the engine's kind-consistency guard discards the mis-kinded
   draw, so the startup advertise never happens);
2. reference-platform available_index (increment on every ADPDU, no reset
   on DEPARTING) — **2 fail** (P7 reset-to-0 + restart-index-0 frame);
3. ENTITY_DEPARTING queued on link-down (Milan §5.6.3.5.6 violation) —
   **5 fail** (P6 no-departing window + P7 frame mismatches; the P6
   window was widened to 150 idle cycles after this mutant initially
   escaped the too-short 5-cycle window);
4. talker-restart detector deleted (stale index treated as fresh) —
   **1 fail** (P9e restart pair).

Known limits (honestly): the suite runs the shipping shape (1 interface,
8 sinks) only; the timer service and slot pools are modeled, not
instantiated (their own suites own those RTL contracts); event-port
ordering between a NOADP expiry and a same-sink iteration in flight is
not exercised (rare, ACMP re-probes either way).
