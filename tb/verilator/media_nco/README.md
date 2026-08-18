# `media_nco` — the steerable media sample grid

Verifies `hdl/ieee1722/crf/KL_media_nco.sv`, the fractional-N divider that
generates `media_tick_p` — the one 48 kHz grid every channel in the datapath
advances on, in both directions.

```sh
make          # build + run, exit 0 = PASS
make clean
```

## Contents

- **[Why this module exists](#why-this-module-exists)** — The ONE-GRID rule: a single servo command must move the audio clock and the packet grid together, or two independently-servoed 48 kHz grids drift apart
- **[What the suite proves](#what-the-suite-proves)** — The NCO's sign, scale and clamp behaviour swept directly, where four naked wiring lines in the datapath had no suite that could exercise them
- **[The oracle is a closed form, not the DUT's recurrence](#the-oracle-is-a-closed-form-not-the-duts-recurrence)** — Why the reference model integrates analytically instead of re-implementing the DUT's accumulator — a model that copies the DUT cannot fail with it
- **[The servo path lives here on purpose](#the-servo-path-lives-here-on-purpose)** — Why the shared servo command is verified in this suite rather than at the datapath level, where a sign error reads as a slow drift instead of a runaway
- **[Mutation results](#mutation-results)** — The planted breaks that were confirmed to turn the suite red, and restored to green — the evidence the assertions actually bite
- **[Two shapes, deliberately](#two-shapes-deliberately)** — The two elaborations swept, and what each one covers that the other cannot
- **[What this suite does NOT prove](#what-this-suite-does-not-prove)** — The honest bound: timing closure, the physical MMCM response and anything requiring silicon are outside what a desk simulation can claim

## Why this module exists

The grid used to be an inline Bresenham divider in `milan_datapath.sv` whose
remainder was a `localparam`. It was exact against the board crystal and
structurally unable to follow anything else. Two consequences:

- a talker whose grid cannot be steered cannot be a media clock **sink**,
  which Milan v1.2 Section 7.2.2 makes mandatory ("For each supported clock domain,
  an AAF Media Talker shall implement a CRF Media Clock Input");
- a listener whose grid cannot be steered drains someone else's stream on its
  own crystal, and slips one sample per beat period. Bench 2026-08-10: one
  48 kHz sample every 1.96 s through the loopback lane, 10.6 ppm.

## What the suite proves

| # | Check | How |
|---|---|---|
| 1 | **`INTERNAL` is unchanged** | tick-for-tick against `LegacyBresenham`, a transcription of the VERSION 0x0040 block, over 600k clocks on both shapes |
| 2 | **The rate is exact** | integer test `\|E·FS − N·(CLK+trim)\| < FS` at every trim point — no dependence on how long the harness ran |
| 3 | **The phase never runs away** | elapsed clocks never a whole clock from `N·period`, in exact integer arithmetic |
| 4 | **The grid stays a grid** | every instantaneous period is `DIV−1`, `DIV` or `DIV+1` |
| 5 | **The LSB is `1e6/CLK_FREQ_HZ`** | measured secant over the full trim span vs the spec's own secant |
| 6 | **The sign is the one the datapath assumes** | `trim > 0` slows the grid |
| 7 | **A wild trim saturates** | 2× past the clamp equals the clamp, to 1e-3 ppm |
| 8 | **A live trim change is glitchless** | two mid-flight trim steps, period bounds hold throughout |
| 9 | **The servo path: sign, scale, gate** | 13 servo commands × 2 clock shapes against an independently-written oracle |

Check 5 deserves a note: the *exact* proof of the LSB is check 2 at `trim = ±1`,
which is integer-exact and needs no statistics. The ppm secant is the
human-readable confirmation, and it is taken across the full `±tmax` span
because an averaged-ppm estimate carries ~`480/N` ppm of quantisation — over a
2000-LSB span that is 1.6 % of a 0.01 ppm LSB, so a 1 % gate there would flake.

## The oracle is a closed form, not the DUT's recurrence

`nco_ref_model.h` states three defining properties of a first-order
fractional-N grid (average period, bounded phase, bounded instantaneous
period) rather than re-implementing the divider. The strongest single oracle
is the phase closed form:

```
phase at tick k  ==  ((k·(REM + trim)) mod DEN)      taken into [0, DEN)
```

This is what makes a **sub-LSB** remainder error visible in a handful of ticks.
Without it the bit-exactness check alone is far weaker than it looks: a 1-LSB
error in `REM_C` does not change the tick *pattern* for ~144,000 ticks, so a
600k-clock run cannot see it. That mutation was run and initially survived;
the phase oracle is the fix.

## The servo path lives here on purpose

`servo_trim_i` / `servo_en_i` convert `KL_mmcm_drp_servo`'s `u` (signed,
1/16 ppm, published on `A_MCSRV_STAT[31:16]`) into a grid trim:

```
trim = -(u * PPM_LSB_P) / 16,  then clamped to +/-TRIM_MAX_P
servo_en_i = 0  ->  ignore u entirely, free-run on trim_i
```

That arithmetic used to sit as four lines in `milan_datapath.sv`, where it
could not be exercised: at `clock_source = INTERNAL` the servo sits at `u = 0`,
so gated and ungated are both zero and **deleting the gate left the whole tree
green**. It was moved here, unchanged, so it could be swept. The two ways it
can be wrong are the two ways that matter — a sign error is a runaway servo,
not a wrong number — so both are checked directly rather than argued:

```
sign: u=+1600 -> +100.2099 ppm,  u=0 -> +0.1066,  u=-1600 -> -99.9767
gate: u=+3200 with servo_en=0 -> +0.1066 ppm,  servo_en=1 -> +200.0133
```

Both shapes report the same ppm for the same `u`. That is the cross-check that
the derivation is right rather than merely self-consistent: `PPM_LSB_P` scales
with the clock, so a ppm command has to mean a ppm on either.

The servo's own `U_MAX_P` clamp (±200 ppm = ±3200 in 1/16 ppm) lands inside
the NCO's derived `TRIM_MAX_P`, and the sweep runs past it on both sides so
the clamp interaction is covered too.

## Mutation results

| Mutation | Bites? |
|---|---|
| flip the trim sign (`+ trim_cl_w` → `− trim_cl_w`) | yes — 64 fail |
| `REM_C` → `REM_C + 1` (sub-LSB rate error) | yes — 38 fail *(only with the phase oracle)* |
| tie `un_w` to 0 (kill the borrow path) | yes — 7 fail |
| bypass the clamp | yes — 3 fail |
| drop the overflow subtraction in the phase update | yes — 93 fail |
| drop the servo negation | yes — 30 fail |
| `>>> 3` instead of `>>> 4` (wrong rescale) | yes — 18 fail |
| ignore `servo_en_i` | yes — 104 fail |

## Two shapes, deliberately

The wrap instantiates the module at **100 MHz** (AX7101) and **50 MHz** (Arty),
same `FS_HZ_P`. That is what proves the LSB tracks `CLK_FREQ_HZ_P` rather than
being a 100 MHz coincidence, and it exercises the derived `TRIM_MAX_P`
(32000 LSB at 100 MHz, 16000 at 50 MHz — both ±319.9 ppm, because the LSB
moves with the clock too).

## What this suite does NOT prove

- **Nothing about the loop.** It grades the actuator against a commanded `u`,
  including the conversion. Whether the *right* `u` arrives — the CRF error
  signal, the PI response, the clock-source selection — is `mmcm_servo`,
  `mmcm_servo_autorepair`, `crf_rx` and `milan_dp`, not here.
- **Nothing about which field carries `u`.** This suite is handed
  `servo_trim_i` directly. That the datapath wires it from
  `A_MCSRV_STAT[31:16]` rather than some other slice is a `milan_dp` question,
  and while the servo is idle its whole status word is zero, so `milan_dp`
  reports that as an open `[GAP]` rather than passing it.
- **Nothing about the other actuator.** `clk_audio` is steered by
  `KL_mmcm_drp_servo` from the same command; that they agree in *silicon* is a
  bench measurement, not a simulation one. The arithmetic that converts the
  servo's 1/16 ppm units into NCO LSB lives in `milan_datapath.sv` beside the
  servo instance, and is exercised by `milan_dp`.
- **Nothing about jitter.** Every period is one `clk_i` quantised by
  construction; what that does to a converter is an analog question.
- The 50 MHz shape never exercises the **borrow** path (`un_w`): its `REM_C` is
  32000 and the derived clamp is 16000, so `REM+trim` cannot go negative. The
  100 MHz shape covers it (`REM_C` 16000, clamp 32000, visible as period 2082
  at large negative trims).
