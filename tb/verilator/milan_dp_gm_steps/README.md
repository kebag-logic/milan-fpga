<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# milan_dp_gm_steps: the GM step leg and its controls (#387, #602, #621)

This suite runs the `milan_dp` gmstep leg and its five acceptance controls
on their own worker. `../milan_dp` keeps the leg's one recipe, its harness
`sim_gmstep.cpp` and the generated images the leg reads at run time. This
directory owns the control driver, `gmstep_mutants.py`.

## Contents

- **[What runs](#what-runs)** -- The clean leg with every phase, then the controls.
- **[Why the controls leave out the #621 phase](#why-the-controls-leave-out-the-621-phase)** -- No named check is in it, and the explicit campaign keeps the whole leg.
- **[Why this is its own suite](#why-this-is-its-own-suite)** -- The measured cost of each `milan_dp` leg at base and at the #621 head.
- **[Running](#running)** -- The default target, the explicit campaign and the leg alone.

## What runs

| Step | Command | What it grades |
|---|---|---|
| 1 | `make -C ../milan_dp gmstep` | The clean leg with every phase: acquisition, media, baseline, the #387 1.5 s GM change, the #621 small steps (+10 ms and -10 ms under CRF, then INTERNAL selection), the selected CRF restart, the slew connection and the 32 coincident-restart delays |
| 2 | `python3 gmstep_mutants.py --no-small-steps` | The positive control, then the five controls the #387/#602 acceptances name, each on the leg without its #621 phase. Each control must fail its named check |

The [`milan_dp` README](../milan_dp/README.md#gm-step-re-base-leg-387) describes
the leg's phases and the whole control inventory.
The [gPTP plane design](../../../docs/design/GPTP_PLANE.md#peer-delay-during-phc-steps)
describes the #621 phase.

## Why the controls leave out the #621 phase

The harness flag `--no-small-steps` removes that one phase and nothing else.
The five sweep controls name these checks, none of them in the #621 phase:

| Control | Named check | Phase it lies in |
|---|---|---|
| the PHC re-base restart term is restored | restart: a PHC-only step leaves outgoing mr unchanged | GM change |
| the source-change term is removed | source control: a real source change toggles mr once | media |
| selected CRF `mr` propagation is removed | CRF control: selected CRF mr propagates exactly once | selected CRF restart |
| the grandmaster identity empties the render stage | render: every PDU not presented was refused by the stage and counted once | GM change |
| the step empties the render stage | render: every PDU not presented was refused by the stage and counted once | GM change |

#632 replaced the two render controls: the presentation stage takes no
re-base, so what they plant is the retired #387 re-base's effect on the queue,
which loses PDUs the clean leg presents, uncounted.

A separate profiled run at `83239549` spent 173 of its 222 CPU seconds there.
Running it in every control cost five runs of it, plus the positive control's.
At `83239549`, with the phase in every run, four controls broke no #621 check.
The restart-term control also broke the eight #621 `mr` and MEDIA_RESET checks.
Only its named check is graded, here and before.
`make gmstep-mutants` still runs every control through the whole leg.

## Why this is its own suite

On hosted run 38048622822 `milan_dp` reached its 4800 s limit at `83239549`.
Without that change, dev's own `milan_dp` took 2973 to 3520 s on hosted pushes.
That is over 60% of the limit already, so removing the #621 phase alone could
not restore the margin. The gmstep leg and its controls left `milan_dp` together.

Native per-leg times of `milan_dp`, one suite run per head, both started together
on the same loaded eight-core host with two-job Verilator builds. Seconds of wall
clock; the run legs also give their CPU seconds.

| Leg | Base `5603c353` | Head `83239549` | Change |
|---|---:|---:|---:|
| `gptp` build and run | 178.5 | 179.6 | +1.1 |
| `gptp-lat` build and run | 180.8 | 185.0 | +4.2 |
| `gmstep` build | 57.7 | 54.7 | -3.0 |
| `gmstep` clean run | 56.4 (47.8 CPU) | 262.1 (252.5 CPU) | +205.7 |
| twelve ordinary builds | 566.9 | 552.5 | -14.4 |
| `sim_pool`, twelve ordinary legs | 748.9 | 748.3 | -0.6 |
| `render_mutants.py` | 565.7 | 586.2 | +20.5 |
| `gmstep_mutants.py`: five control builds | 246.1 | 226.4 | -19.7 |
| `gmstep_mutants.py`: six runs, the positive control's included | 264.8 | 1326.4 | +1061.6 |
| generators, image tools and the driver's own work | 2.5 | 2.7 | +0.2 |
| whole suite, `make` start to end | 2870.1 | 4126.6 | +1256.5 |

The gmstep leg's seven runs cost the time.
Each run grew by the #621 phase, about 205 s.

At the split head `0e3eef5b`, each suite ran in its own clean checkout, the
two started together on the same host. Seconds of wall clock, with CPU seconds
in brackets:

| `milan_dp` leg | Head `83239549` | Split head `0e3eef5b` |
|---|---:|---:|
| `gptp` build and run | 179.6 (215.7) | 165.0 (199.1) |
| `gptp-lat` build and run | 185.1 (221.9) | 153.2 (183.3) |
| `gmstep` build and clean run | 316.8 (348.5) | moved |
| twelve ordinary builds | 552.4 (992.7) | 539.3 (927.1) |
| `sim_pool`, twelve ordinary legs | 748.3 (900.1) | 728.9 (871.1) |
| `render_mutants.py` | 586.2 (727.2) | 537.3 (666.0) |
| `gmstep_mutants.py` | 1555.0 | moved |
| whole suite, `make` start to end | 4126.6 | 2124.4 |

| `milan_dp_gm_steps` leg at `0e3eef5b` | Seconds |
|---|---:|
| `gmstep` build | 46.2 (81.6) |
| `gmstep` clean run, every phase | 216.8 (215.9) |
| `gmstep_mutants.py`: five control builds | 233.5 (409.9) |
| `gmstep_mutants.py`: six runs without the #621 phase, and its own work | 243.8 |
| whole suite, `make` start to end | 741.0 |

The host was less loaded during this pair, so the unchanged legs ran 2 to 17%
faster than in the first pair. The hosted projection below therefore removes the
gmstep share measured in the first pair rather than using the split-head total.

**Hosted projection.** The six dev pushes from run 37968528697 to run
38067159953 took 2972.7 to 3519.6 s for `milan_dp`, 1.036 to 1.226 times this
host's base total. At 1.226 the #621 head projects to 5060 s: both hosted runs
of it timed out at 4800 s. The gmstep leg and its controls were 627.3 s of the
2870.1 s base total, 21.9%. Without them those six windows become 2323 to
2750 s, at most 57.3% of 4800 s. This suite projects to 741.0 x 1.226 = 909 s,
50.5% of its 1800 s budget. Hosted runs confirm or replace these figures.

## Running

```sh
make -C tb/verilator/milan_dp_gm_steps
make -C tb/verilator/milan_dp_gm_steps gmstep-mutants
make -C tb/verilator/milan_dp gmstep
```

The first is the sweep's target. The second is the explicit campaign, outside the
sweep's deadline. The third runs the clean leg alone.
