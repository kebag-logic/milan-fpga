[A681f] TAKEN
Branch: `665-s2-cpu-budget` (PR #792), head `f58d049beb377c3f535628067022d4d5b51e8208`, base `dev-soft-core` `e76a755a`. Round 6 adds commits on top.
Authoritative references: the round-6 assignment (issuecomment-6435512208); hosted run 40408916714, job `firmware-boundary`, step "Hold the TSN stack boundary over the firmware builders' compiles"; `sw/firmware/ctrl/test/ctrl_configs.py` (BUILDERS, PART_OF, OUTSIDE, SUITES and its module docstring); `sw/firmware/ctrl/README.md`; AGENTS.md section 5.

Interpreted scope:
- The hosted refusal names six harness files, not only `build.py`. The full message lists `build.py`, `fixture_variant.py`, `runtime_ssp.py` and `selftest.py` (programs) and `scenario.py` and `split_soc.py` (modules that compiled nothing in the capture).
- The message also names two more categories than the assignment quotes. Its full text continues "compiles none of the firmware's (OUTSIDE) or compiles only in a suite (SUITES)".
- I will classify each of the six by what it does, using the gate's own four categories, and give the reason in the entry.
- `build.py` cannot honestly be PART_OF, because no known builder runs it. Its parent is `run.py`, which names no firmware tree.
- `build.py` in BUILDERS would oblige a hosted job to run it under the capture. Neither firmware job can do that:
  - `firmware()` imports the picolibc and compiler-rt data packages, which no hosted job installs.
  - The full build also needs the LiteX SoC export, the VexiiRiscv netlist and Verilator.
  - Fixing that needs an edit under `.github/` and to the CI generators. That is outside this lane's scope.
- So `build.py` goes in OUTSIDE, with a reason modelled on the existing `tb/verilator/milan_dp/Makefile` entry:
  - It delegates the image to `ctrl_srp_image.py`, unchanged. The gate's own capture runs that builder at these shapes, interface counts and AECP composition (`ctrl_runs.image_runs`).
  - Its own compiles build the test SoC's Verilator model.
- The four that compile nothing, or only the out-of-checkout runtime, go in OUTSIDE.
- `fixture_variant.py` compiles only in the harness's labelled variant arms, from an edited copy of the fixture, so it goes in SUITES.
- This departs from the two options the assignment names. If the manager wants `build.py` in BUILDERS, that needs a hosted-job change first; I will not make it.
- No gate code changes. No firmware or harness behaviour changes, and no measurement or published figure changes.

Validation plan, all at the new head, rc 0, never piped:
- The boundary gate exactly as `rtl-fast.yml` runs it: `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`. Also its `--only verilator` sibling.
- The rest of rtl-fast's firmware jobs' steps (firmware-unit, the three mutant shards plus shard 0).
- The harness self-test and its mutants.
- `python3 scripts/check_baremetal_only.py --check`.
- The full docs-check set, and `cd tests && behave`.
- The boundary gate joins my standing gate table from this round on.
- A planted removal of each new entry, to show the gate refuses it by name.

Blockers: none. Open question for the manager: BUILDERS against OUTSIDE for `build.py` (above).
