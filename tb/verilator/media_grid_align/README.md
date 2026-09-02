# media_grid_align - the #74 grid-alignment loop, closed over the real NCO

`KL_media_grid_align` steering `KL_media_nco` exactly as `milan_datapath`
wires them: `u_o -> servo_trim_i`, one selection gate (`sel_i`) feeding both.
The C++ harness IS the physical grid - it pulses the frame marker on a
double-precision fractional-period model of the TDM fsync - and the oracle
is the NCO's `tick_o`, graded through the harness's own copy of the
junction pend/consume law (the same law behind `KL_chan_map_capture`'s
`tdm_dup_cnt_o`/`tdm_skip_cnt_o`), never an internal signal.

The reference rate is the true divider plan: `100 MHz * 391/1591 / 512 =
47,999.4893 Hz`, the -10.6393 ppm Plan A that slips one sample every
1.9582 s free-running ([Section 3.5.1 of TIME_SYNC.md](../../../docs/design/TIME_SYNC.md),
`tb/verilator/milan_dp/sim_aclk.cpp`).

## Contents

- **[Arms](#arms)** — The seven closed-loop arms G0-G6: deselected free-run, engagement and acquisition in both rate directions, the feed watchdog, mid-lock deselect, and the beyond-authority clamp with recovery.
- **[What this suite caught while it was being written](#what-this-suite-caught-while-it-was-being-written)** — The two detector fold schemes that passed a desk check and failed loudly here, and the sign-chain pin G2/G3 holds in both directions.
- **[Boundaries](#boundaries)** — What this suite deliberately does not own: selection truth, the MMCM servo and the fsync CDC belong to the datapath-level arms in `tb/verilator/milan_dp`.

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
