[A614] REVIEW READY

Commit: `08adb21af0a72d839ce30b6c461503dad269d4d6`
Branch: `737-ci-30min`, from round-four head `84ee9ea1`; clean worktree; not pushed (origin still holds `84ee9ea1`). The coordinating role publishes it.

Round 4 ([6180908502](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180908502)) is complete. F1, S1, S2, S4, R1 and R2 are unchanged from STOP [6181763440](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181763440). S3 is done under the answer [6181778634](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181778634).

**S3: the builder gate in measured legs.**
- **Driver entry point only** (`4e39fb266`, `0838c64f9`). `sw/builder/test_builder.py --list` prints the ordered 103-gate inventory. `--gates a,b` runs that subsequence and refuses unknown, repeated or out-of-order names before any gate runs. `--receipt` records each gate's verdict and the NOT RUN rows it added. The literal run list stays in its one `for fn` loop. With no option the run is as before: the docs bank's default run has 103 gates, the same verdict and no SUBSET line. No gate, assertion, fixture, timeout, NOT RUN arm or firmware behaviour changed.
- **Measured split** (`fb81a89e4`). `scripts/ci_builder_legs.py` puts `test_baremetal_profile_contract` alone in leg 0 (945.2 of 1292.7 s) and the other 102 gates in leg 1. The generator turns the template's one command into `gate_14_0` on worker 0 and `gate_14_1` on worker 1, before the LiteX aggregate. Each runs the template command, adding only the selection and a receipt bound to head and tree. Two workers remain, so the runner is unchanged.
- **Union-level requirements.** `--require-elaboration` and `--require-rv32` are judged on the union, never per leg. The leg runner names the 15 LiteX-consulting gates and the RV32 gate, and the self-test checks those names against the driver source. The `elaborate` aggregate refuses unless every gate ran exactly once in its leg and passed, and each named gate is in the fresh inventory and ran in a leg carrying its flag. The driver's own `--require-elaboration` verdict is then applied to the union NOT RUN ledger.

**Projection** (hosted run 38495894212, scaled by `1441 / 1292.671`; legs measured beside other builder runs, which only lengthens them):
- `elaborate-gates-0` = `2144 - 593 - 3 - 1441 + 1146 + 60` = 1313 s;
- `elaborate-gates-1` = `2144 - 1441 + 409 + 60` = 1172 s;
- both are within their 1620 s bounds. The workflow is 1313 + 270 = 1583 s, 26.4 minutes (it was 31.3).

**Equality, in the shipping image (8 GiB, 16 CPUs, no network).**
- At `0838c64f`: unsharded rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`; leg 0 rc 0 (1028.3 s); leg 1 rc 0 (367.3 s). `ci_builder_legs.py union --reference` returns rc 0. Every per-gate verdict and the ordered NOT RUN ledger are equal: `[gate 1b]` MAKEFLAGS from leg 0, `[gate 11]` calibration report from leg 1. The production aggregate (`ci_gate_receipts.py record` and `verify`) accepts the real receipts. Printed output: 96 gates byte-identical, 7 identical once temporary paths and elapsed seconds are masked.
- At this head: unsharded rc 0 (1311.1 s); leg 0 rc 0 (984.8 s); leg 1 rc 0 (348.1 s). The union check against the reference returns rc 0, with the same per-gate verdict digest (`47dc3c6a…`) as at `0838c64f`. The aggregate replay returns rc 0. Printed output is again 96 + 7 masked, with none different.

**Planted controls.**
- A reworded boot-order claim fails the unsharded run and leg 0 with the same assertion; leg 1 passes.
- A removed FPU refusal fails the unsharded run and leg 1 at `test_soc_option_refusals`; leg 0 passes.
- Leg 1 run without `--require-elaboration` passes by itself; the aggregate refuses the union, naming all 15 elaboration gates.
- The self-test refuses, by name, the elaboration gate deleted, lost with its leg, skipped in its leg, moved to a leg that never ran, or run without its flag; and the RV32 gate without `--require-rv32`.
- Mutations: 7/7 fail the scheduling self-test, including deleting `test_every_recipe_elaborates` from the real run list ("absent from the driver inventory"); 2/2 pristine copies pass.

**Found by execution before any hosted run, and fixed.**
- `3ca77034f`: the leg runner's parser swallowed `--receipt`. Every generated leg body is now parsed in the self-test.
- `0838c64f9`: a `gates = (...)` tuple broke `test_rom_clock_skip_reaches_the_ledger`, which reads the one run-list loop.

**Validation at `08adb21a`.**
- Docs-check bank: 40/40 steps rc 0, including the builder gate (1363 s) and the CI-event contract (5,212 arms).
- docs-check-no-git: rc 0.
- Runner contract gate: rc 0 (104.5 s), read-only, no socket; runner SHA-256 unchanged, `f968f676…`.
- rtl-fast: no step body changed; `pp_srcs.py --check --selftest` and the scope self-test pass.

Acceptance criteria: round-4 items 1-3 are met, with the evidence above. The CI assertion replacement ledger (equal or stronger, with executed controls) is in `HANDOFF.md`.

Open risks/questions:
- These are projections, not hosted times; hosted readback decides.
- The union's verdict line repeats the driver's "listed above" wording, although the union prints its ledger only in the JSON.
- No owner-level decision is requested. This is an author handoff, not a review verdict.
