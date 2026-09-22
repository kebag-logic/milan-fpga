<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# prng — KL_pp_prng suite

Proves the [08 §3](../../docs/architecture/08_timing.md) F08.2 PRNG
(`hdl/common/KL_pp_prng.sv`): `make` = build + run, exit 0 = PASS, 57 checks.

The C++ harness is an independent model written from the documented contract
(F08.2 + IEEE 1722.1-2021 §6.2.4.2.2 practice), never from the RTL: the
primitive polynomial x^64+x^63+x^61+x^60+1 in right-shift Galois form, a
16-elementary-step advance per cycle (decimation by 16 — maximal because
gcd(16, 2^64-1) = 1), seed = entity_id XOR cycles-since-reset latched at the
FIRST link-up rise only (zero seed replaced by a nonzero substitute), and
rejection-sampled range draws replayed attempt-by-attempt on the free-running
stream. For an LFSR, bit-exactness against the polynomial IS the spec — the
independence lives in deriving every expectation (seed value, accept cycle,
draw value, range bounds) from the contract, not from DUT internals. All DUT
outputs are registered, so the harness samples post-edge and steps the model
in lockstep on every rising edge.

Covered: raw stream bit-exact over 10k steps (plus never-zero and
advances-every-cycle); seed = entity_id XOR counter verified against an
independently counted cycle mirror; re-seeding on a second link-up rise
forbidden (stream continues bit-exact across the flap, with a changed
entity_id on the port); the zero-seed substitute; two entity_ids diverging in
all 64 of the first 64 post-seed states (the XOR of two maximal-LFSR streams
is itself a never-zero stream); per-kind draws (6000/9000/12000/2200/2200 for
kinds 0-4) each bit-matching the model's predicted value AND accept cycle,
in-bounds, mean within 5 % of the range midpoint, both endpoints actually
drawn for kinds 0-3 and 2 %-proximity for kind 4; rejection genuinely occurs
where the mask overshoots the span (kind 3, span 5001 vs mask 0x1FFF+1:
39 % of draws take at least one retry, asserted > 20 % and < 60 %) and mostly
does not where it is tight (kind 0: 2 %, asserted < 10 %); busy/valid
handshake; and a request arriving mid-draw is dropped, not queued.

Design finding baked into the RTL: with a 1-step advance, consecutive
rejection retries share 15 of the 16 draw-window bits (next attempt =
rejected value >> 1), which concentrates accepted-after-reject values in the
upper-middle of the span — measured mean 12854.4 ms on the 10000..15000
range, 11 sigma above the midpoint. The 16-step advance replaces the whole
window each cycle and restores the F08.2 unbiasedness claim (measured mean
12527.3, 0.9 sigma).

Mutation-proven 2026-08-11 (each applied to a copy-backed original, run,
restored, rerun green 57/57):

| Mutation | What it breaks | Fails |
|---|---|---|
| accept `<=` -> `<` | off-by-one: the top endpoint becomes undrawable | 11 of 57 (max endpoint never drawn for kinds 0-2, value/accept-cycle mismatches) |
| seed-once guard removed | re-seeds on every link-up rise | 14 of 57 (both flap checks + downstream stream/draw divergence) |
| rejection disabled (`accept_w = 1'b1`) | raw mask overshoots the range | 22 of 57 (out-of-bounds draws, e.g. kind 0 max 1023; rejection-rate checks) |
| advance 16 steps -> 1 step | retry-correlation bias returns | 18 of 57 (stream checks + every draw-prediction check) |

None of the four is behavior-equivalent — each fails a different subset for a
different stated reason.
