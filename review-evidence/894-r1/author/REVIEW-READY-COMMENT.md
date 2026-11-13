[A773] REVIEW READY

Commit: `12180198b087d4cfdd531d0de5d3753211b35616` (branch `894-tiers`, ordinary commits on round 1's `f9442a10`; nothing pushed).

Changed:
- **THE TIERS in the control loop** (`ctrl_loop.c`, `ctrl_loop.h`). Tier 1 runs first: AECP first, past its cap while the pass has spent at most `CTRL_LOOP_DRAIN_US`, then ACMP, ADP and MAAP. Tier 2 runs only once tier 1 left none: SRP's records in a slice of `CTRL_LOOP_SLICE_US` from the pass's start, and THE TRANSMIT's build and THE RETRY's round each a slice of a pass given whole, the round only after SRP. A queue's first notice is tier 1's.
- **The slice** is the ruling's rule at the costs measured on the image under the tiers: 1,200 us at 1x1/1if (least relative margin 0.2673, the last queued notice binding; 1,050 us gives 0.2610 and 1,300 us 0.2650). It is 1,300 us at 8x8/2if, which the ruling leaves unchosen.
- **SRP's build resumes across slices** with the frames of the build made whole (`srp_mbx.c`). It is compared byte for byte by `Srp.ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole`.
- **AECP's owed-notice queue** (`aecp.c`, `aecp_mbx.*`) meets the ruling's conditions (a) to (d), with `Queued.*` and `tests/features/aecp_owed_notices.feature`. The poll sends the queue's notices inside AECP's send, before a waiting command's answer, as the tree sent its notices before.
- **The datapath events' sink cost** is measured on new harness pads (`datapath-events`): 35, 30 and 25 us at 1x1/1if, and 35, 35 and 25 us at 8x8/2if, in `rows_tiers.DATAPATH_US`. The rows had assumed 60 and 95.
- **Every cost measured again on the image under the tiers** (#665 round 28's cost tools over every leg), each the larger of that and the committed table's (`load_grade.py`, `poll_grade.py`). Eight rose: at 1x1/1if an AECP record 205 to 235 us, ADP's timer slot 110 to 115, the TICK 40 to 45, a pass's events' fixed part 25 to 30 and the polls' base 155 to 160; at 8x8/2if AECP's timer slot 95 to 105, a notice 270 to 275 and ACMP's owed frame 185 to 195.
- **The built design** (`rows_tiers.BUILT`) is the flip check's rows, `flip_grade.py --design built`; `--design as-built` stays.
- **`slice_grade.py`**: the slice gate (#665 round 23, item 1).
- **Planted defects**, each failing its named test on its words: 17 for the loop, 19 for the queue and the first notice, 4 for the resumed build, 1 for the fan-out, 8 for the slice gate and 1 for the built rows.
- **`CTRL_LOOP_BUILD_PASS_US`** is restated at 1x1/1if from its measurement under the tiers: 955 us, the image unchanged.

**Rows by every source, the built design** (`rows_tiers.py`, ms; bounds 20, 90, 90, 20, 125):

| Point | Slice | R4 | R5 | R6 | First queued notice | Last queued notice | MRPDU (reported) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1/1if | 1,200 us | 12.71 | 54.59 | 52.85 | 14.60 | 91.59 | 29.00 |
| 8x8/2if | 1,300 us | 42.47 | 187.97 | 178.28 | 20.25 | 647.23 | 89.01 |

**By measurement** (the CPU budget harness, the head's image, ms; least margin relative to the bound):

| Point | Tier 1 (20) | SRP (90) | First of a queue | Every queued notice | MRPDU (20) | Heaviest pass (share 2.0) |
|---|---:|---:|---:|---:|---:|---:|
| 1x1/1if | 6.562 ACMP (0.672) | 9.044 (0.900) | 5.947 of 20 | 17.228 of 125 (0.862) | 1.052 | 1.561 |
| 8x8/2if (stress: every source at its contract rate) | 9.605 ACMP (0.520) | 13.937 (0.845) | 3.572 of 22 | 53.336 of the stated 62 (0.140) | 5.572 | 2.280 (F3) |

The three egress-held paths of tsn-c-stack #26 miss as round 28 recorded, at both points.

Validation (once on the head, each on a fresh clean clone):
- **Workflows.** Every `run:` step of the four workflows a pull request triggers: 139 ran and 226 not run with a stated reason. One step's verdict was UNKNOWN, the standalone LiteX aggregate (exit 92): the loaded pool's 900 s wall clock killed `test_soc_timing_cuts`, and the other seven passed. Run again alone in its job's clean clone with `LITEX_SIM_TIMEOUT=1800`, it passed 8 of 8 with rc 0. Every job's tree was clean afterwards.
- **Firmware plants and coverage.** The control campaign caught 697 of 697, the AECP campaign 243 and the SRP campaign 344, with 0 escaped. `fw_coverage.py --check` passes.
- **Lane gates.** `test_builder.py --require-rv32` passes (all gates but the 2 not run that #810 records). Behave passes 511 scenarios. `git diff --check` is clean, and the idiom, docs and boundary gates pass. The harness self-test has 0 failures with 210 plants caught; `rows_tiers` refuses 509 of 509 and the flip check 319 of 319. `load_grade.py --check` passes (0.470 and 0.457). `flip_grade.py --check --point 1x1/1if` passes.
- **Sweep.** 62 of 65 suites pass in the sweep, with 0 in-suite failures. The 3 the loaded pool's wall clock stopped (`milan_dp`, `milan_dp_gm_steps` and `milan_dp_render`) pass when re-run alone with the clock doubled.
- **Harness at both points.** Each leg's image was built again at the head. The image each leg runs is byte-identical, and so is its sample log. At 8x8/2if the split SoC's one-interface images, which only export the flash port's map, differ in the slice's one-interface arm alone, and the map is identical. The regrades: 1x1/1if rc 0; 8x8/2if rc 0 but for F2.

Acceptance criteria:
- **(1) THE TIERS: met.** `Loop.L22`, `L23`, `L26` and `L27`, with 17 plants; the slice gate.
- **(2) `aecp_ready`: met.** Conditions (a) to (d) each have a test and a plant.
- **(3) The datapath sink cost: met.** It is measured and stated.
- **(4) The built design in `rows_tiers.py`: met.** `flip_grade.py --check --point 1x1/1if` passes at the built costs, and `rows_grade.py` is unchanged.
- **(5) Both points re-measured: met.** The tables above; the 1x1/1if load is 0.470 at the pin and 0.457 with tsn-c-stack #32, at most 0.70.
- **(6) The gate pass: met,** as above.
- **No STOP condition holds.**

Open risks/questions:
- **F1.** The 8x8/2if size fixture is 664 B of rom over its 57.5-RAMB36 ledger. Its harness build refuses on a clean clone, and the 8x8/2if runs used a 58.0 plan for measurement only.
- **F2.** At 8x8/2if a Domain adoption's first build slice is 1.58 ms, over the 1.3 ms slice and `CTRL_LOOP_BUILD_ONE_PASS_US`.
- **F3.** At 8x8/2if 11 of 16,874 passes in the notice groups are over THE SHARE, at most 2.280 ms.
- **The MRPDU row.** By every source it is 29.00 ms at 1x1/1if, over the 20 ms the loop before the tiers held it to; which bound holds it under the tiers is to be decided.
- **The per-point slice** is an interpretation: 8x8/2if is kept at 1,300 us.

The HANDOFF records every change, check, plant and correction, with the run history.
