<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# acmp_listener — KL_pp_acmp_listener MTXW suite

Proves the ROM-driven Milan listener-SM executor
(`hdl/acmp/KL_pp_acmp_listener.sv`) against the full F05.3 transition matrix of
[05 §6.3](../../docs/architecture/05_acmp_engine.md): `make` = generate the
ROM + build + run, exit 0 = PASS, 2458 checks.

**The MTXW walk** ([09 §3](../../docs/architecture/09_verification.md)):
every one of the 112 cells (14 events x 8 states) is driven against an
**independent C++ matrix model transcribed from the doc table without
`gen_ltn_rom.py`** — two transcriptions of F05.3 that must agree through the
DUT's behavior; that is the point of the walk. Each sink is brought to the
cell's column state through legitimate stimulus only (no state backdoor),
then the row's physical event is applied and *every* observable compared
against the model: the full 384-bit F07.6 record write-back (shadowed from
the write port), committed 56-byte Milan ACMPDUs byte-exact (BIND/UNBIND/
GET_RX_STATE responses per F05.14, PROBE_TX per A5/A13), timer arm/cancel
ops with exact F08.1 deadlines (T-ACMP-CMD 200 ms, RETRY 4 s, NOTK 10 s,
DELAY = the scripted PRNG draw), the A15/A8/A4/A9/NVM/notify strobes with
payloads, and the RX-slot free.

Every `—`/`ign` cell is **proven inert** (state unchanged, no strobes, no
frames, no timer ops, no notification). Timer-row `—` cells split honestly:
states with no armed SM timer (UNB/PWA/SOK, 12 cells) get a spurious expiry
injected and full inertness checked; the 15 cells whose T-ID aliases the
shared per-sink slot (08 §5) are proven impossible by construction — the
suite checks the deadline armed on entry equals the state's *own* T-ID, so
the foreign expiry cannot exist — plus the model transcription must mark
them `—`. The `ign (note)` cells additionally prove the tk_disc/tk_reg
bookkeeping still tracks (the dagger conditionals depend on it).

Behavior checks beyond the walk: exact-duplicate probe (A13 bytes == A5
bytes, same `probe_seq`, `retried` set), double timeout -> `acmpsta` 7, both
arms of all three dagger cells, the **REF-BUG guard** (TalkerFailed rise in
SETTLED_RSV_OK takes no invented arc — the Table 5.30 'x' the doc pins),
REGISTERING_FAILED visible in GET_RX_STATE, LISTENER_UNKNOWN_ID for the
three commands + silent drop for probe responses, foreign-EID and
foreign-protocol silence, probe-response guard mismatch silence, the A1
lock gate (foreign holder blocked, holder passes, GET_RX_STATE unaffected),
boot preload -> PRB_W_AVAIL with discovery armed (07 §5.3), the
A11-swallows-stale-expiry race (a pending T-ACMP-CMD expiry must not tear
down a settlement that just landed), and cross-sink record isolation.

The harness emulates the four **landed** faces cycle-exactly: KL_pp_rx_slots
(sync read, one-cycle latency), KL_pp_tx_slots (request sampled, grant
pulsed the following cycle), KL_pp_timer_service (arm/cancel bus, owner-
tagged expiries), KL_pp_prng (busy then a one-cycle valid draw).

Mutation-proven 2026-08-11 (backup/sed/run/restore):
- **M1** `gen_ltn_rom.py`: drop A8 from the `BIND_NEW x SOK` cell -> 3 of
  2458 FAIL (missing teardown strobe, stale settled params survive rebind).
- **M2** RTL: invert the dagger tk condition (`!f_tk_disc` -> `f_tk_disc`)
  -> 21 FAIL (all three cond cells take the wrong arm in both directions).
- **M3** RTL: A11 no longer clears the pending-expiry bit -> 1 FAIL (the
  stale T-ACMP-CMD expiry surfaces after settlement and tears it down to
  PRB_W_AVAIL). Honest note: the first version of this scenario watched a
  20-tick window — shorter than the ~24-cycle retirement of the second work
  item — and the mutant survived vacuously; the window is now 60 ticks of
  required silence with the collector cleared. A surviving mutant proved
  the check wrong, not the design right.
- **M4** RTL: same-bind classification disabled (every BIND treated as
  new/different source) -> 389 FAIL (the whole BIND_SAME row re-probes and
  churns SRP instead of the v1.2 A6 short-circuit).
