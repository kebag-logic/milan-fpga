# media_grid_align - the #74 grid-alignment loop, closed over the real NCO

`KL_media_grid_align` steering `KL_media_nco` exactly as `milan_datapath`
wires them: `u_o -> servo_trim_i`, one selection gate (`sel_i`) feeding both.
The C++ harness IS the physical grid - it pulses the frame marker on a
double-precision fractional-period model of the TDM fsync - and the oracle
is the NCO's `tick_o`, graded through the harness's own copy of the
junction pend/consume law (the same law behind `KL_chan_map_capture`'s
`tdm_dup_cnt_o`/`tdm_skip_cnt_o`), never an internal signal. Arms G7-G9
read the counters of a REAL `KL_chan_map_capture`, wired on the same frame
marker and tick as `milan_datapath` wires it, instead of that copy.

The reference rate is the true divider plan: `100 MHz * 391/1591 / 512 =
47,999.4893 Hz`, the -10.6393 ppm Plan A that slips one sample every
1.9582 s free-running (the [media boundary](../../../docs/design/TIME_SYNC.md#media-boundary)
table; measured in the [historical Section 3.5.1](../../../docs/history/v1/design/TIME_SYNC.md#351-the-grid-phase-contract--clk_tdm_i-clk_audio_i-media_tick_p-74);
`tb/verilator/milan_dp/sim_aclk.cpp`).

## Contents

- **[Arms](#arms)** -- The ten closed-loop arms G0-G9: deselected free-run, engagement and acquisition in both rate directions, the feed watchdog, mid-lock deselect, the beyond-authority clamp with recovery, a lock raced onto the tick from either side, and one free-running passage each way.
- **[The negative control](#the-negative-control)** -- the inverted-sign, no-keep-off and old-coincidence builds must fail.
- **[What this suite caught while it was being written](#what-this-suite-caught-while-it-was-being-written)** -- The two detector fold schemes that passed a desk check and failed loudly here, and the sign-chain pin G2/G3 holds in both directions.
- **[Boundaries](#boundaries)** -- What this suite deliberately does not own: selection truth, the MMCM servo and the fsync CDC belong to the datapath-level arms in `tb/verilator/milan_dp`.

## Arms

| Arm | Pins |
|-----|------|
| G0  | deselected: no command, no engagement, with a live feed |
| G1  | deselected NCO is bit-exact nominal (4800 ticks / 10M cycles) |
| G2  | select at Plan A: engage, acquire with the phase never past 300 cycles (0.14 sample), ZERO junction slips through acquisition, u settles ~-170 LSB (= -10.64 ppm in 1/16 ppm units), locked ticks count with frames |
| G3  | the mirrored +10.64 ppm feed: zero slips, u flips to ~+170 |
| G4  | feed watchdog: silence disengages (u = 0, exact free-run), frames re-engage from a fresh reference and reacquire |
| G5  | deselect mid-lock: instant disengage, bit-exact free-run returns |
| G6  | a 400 ppm feed (beyond the +/-200 ppm authority): u parks at the clamp, slips honestly, and conditional integration makes recovery a re-acquisition rather than a ~1.5 s integrator bleed |
| G7  | #74 item 2: the engaging frame lands ON a tick, then every marker arrives 0 or 1 edge late (the root's capture FIFO pop). The real junction counters stay at zero over eight 0.2 s windows after 0.6 s of settling, the marker stays at least 12 cycles off every tick, and at that lock a held frame is exactly one dup and a surplus frame exactly one skip |
| G8  | the same from below: the engaging frame lands 1-2 edges BEFORE a tick; after 1 s the counters stay at zero over 0.2 s and the marker stays at least 12 cycles off. Acquisition from this side crosses the tick and back, and the jittered crossings print balanced dup/skip pairs |
| G9  | free-running (deselected), the marker 20 edges from a tick: one slow passage is exactly one dup in the plan direction and exactly one skip in the mirrored one |

## The negative control

`MGA_MUT_U_SIGN` compiles the wrap with the loop's command sign inverted
into the NCO - the runaway the sign chain exists to prevent - and the
default `make` runs that build expecting FAILURE (it dies in [G2] with the
phase past five samples). If the mutant ever passes, the sign checks have
gone vacuous.

Two more mutants hold the #74 item 2 arms to the same standard, and each
must fail on its own arm, not merely somewhere:

- `MGA_MUT_NO_KEEPOFF` builds the loop with `LOCK_KEEPOFF_CYC_P = 0`, so it
  locks on its raw engagement capture. [G7] must fail on its junction
  counters: once the integrator has walked the marker back onto the tick,
  the jittered marker dithers across it and counts 1,000 to 1,400 dup/skip
  pairs in every 0.2 s window from then on.
- `MGA_MUT_COIN` builds a copy of `KL_chan_map_capture` whose coincidence
  branch drops the pending marker again (the recipe refuses the copy if the
  substitution finds nothing to revert). [G9] must fail: the slow passage
  counts about a dozen dups, and the mirrored one counts dups and no skip.

## What this suite caught while it was being written

Both detector fold schemes that preceded the tracking unwrapper passed a
desk check and failed here, loudly (u parked at -3200, phase past 2.5
samples): first the +/-DIV/2 wrap misaligned with the slip events' full-DIV
folds, then the pend/consume fold lost +/-DIV at every frame+tick
coincidence - and a CONVERGED loop sits exactly where pulses coincide. The
sign chain (err > 0 = ticks fast = command DOWN, into a port that speaks
the servo's "u > 0 = speed up") is pinned by G2/G3 in both directions; the
first-cut windup cost is recorded in G6's expectation. The dead ends are
documented in the module's detector banner.

## Boundaries

Selection truth (what drives `sel_i` in the datapath), the CRF-side MMCM
servo, and the fsync CDC are out of scope here: the datapath-level arms in
`tb/verilator/milan_dp` own them. This suite owns the loop's law.
