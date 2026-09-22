<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# timer_service — KL_pp_timer_service suite

Proves the timer service (`hdl/common/KL_pp_timer_service.sv` — the
[08 §2/§3](../../docs/architecture/08_timing.md) F08.2 timebase and the 08 §5
deadline RAM sweep): `make` = build + run, exit 0 = PASS, 48 checks.

The suite runs compressed time per [09 §3](../../docs/architecture/09_verification.md)
TIM: `-GDIV_US_P=4 -GDIV_MS_P=5` (20 clk per ms) and `-GSLOTS_P=12` so a full
sweep fits inside one compressed ms. The C++ model is independent, never DUT
logic: expected time is pure cycle arithmetic (`now(c) = c / (DIV_US·DIV_MS)`
after reset release) and expected expiries come only from the arm history —
an armed slot with absolute deadline D fires exactly once, in the first sweep
whose `now_ms >= D`, within SLOTS + 2 cycles of that ms boundary.

Covered: reset state; free-running `now_ms_o` against the cycle model with
exact ms-tick spacing and whole-run monotonicity (+0/+1 per cycle, never
backwards); full sweeps with zero armed slots emitting nothing; six staggered
arms each firing exactly once at their own absolute ms with the right owner
tag and inside the right sweep window; cancel before expiry never firing;
re-arm after expiry firing again with the NEW owner and deadline (proves the
RAM rewrite, not a stale readback); two same-ms expiries serializing at one
per cycle in ascending slot order with cycle spacing equal to slot spacing;
an already-past deadline firing on the next sweep (wrap-safe age compare);
and expired slots staying disarmed through a quiet tail.

The suite also caught (pre-fix) the arm-races-the-sweep hazard: an arm landing
on the exact cycle the sweep reads that slot fired on the stale RAM data. The
RTL's one-cycle arm shadow now defers that slot to the next sweep, and check
T2/slot 0 arms deliberately mid-sweep to pin the fix.

Mutation-proven 2026-08-11 (each applied to a copy-backed original, run,
restored, rerun green at 48/48):

| Mutation | What it breaks | Result |
|---|---|---|
| M1: expiry self-disarm inverted (`armed_r[chk_slot_r] <= 1'b1`) | expired slots refire every sweep | fails 16 of 48 |
| M2: wrap-safe age compare `!age_w[31]` narrowed to `age_w == 0` | past-deadline arms never fire | fails 2 of 48 |
| M3: µs prescaler off-by-one (`== DIV_US_P` for `== DIV_US_P - 1`) | every timebase and expiry ms wrong | fails 28 of 48 |

All three are behavior-changing mutants (no equivalent mutants claimed).
