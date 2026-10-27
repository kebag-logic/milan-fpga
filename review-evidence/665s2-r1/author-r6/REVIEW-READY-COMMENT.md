[A681f] REVIEW READY
Commit: `e0e1b4649ea3af908a8f32eccaad7903fa2cc134` (one commit on round 5's `f58d049b`; one-line subject, no body, no trailers; not pushed. The manager pushes.)

Changed:
- `sw/firmware/ctrl/test/ctrl_configs.py` (+26 lines, entries only): classifies the six harness files that hosted run 40408916714 refused by name.
  - In OUTSIDE: `build.py`, `runtime_ssp.py`, `scenario.py`, `selftest.py` and `split_soc.py`.
  - In SUITES: `fixture_variant.py`.
  - Each entry says what the file compiles.
  - `build.py` follows the existing `tb/verilator/milan_dp/Makefile` entry. It delegates every firmware compile to `ctrl_srp_image.py`, run unchanged at the shapes, interface counts and AECP composition the gate already runs it at (`ctrl_runs.image_runs`). Its own compiles build the test SoC's Verilator model.
- `tb/verilator/ctrl_service_budget/README.md:107-117`: the classification, and the rule that a new file here naming the firmware's tree must be listed.
- No gate code, firmware, harness code, measurement or figure changed.

Why not the assignment's two options (published in TAKEN before any edit):
- PART_OF would be false: no known builder runs these files.
- BUILDERS obliges a hosted job to run `build.py` under the capture. No job can: it needs the picolibc and compiler-rt data packages and the patched LiteX tree beside Verilator. That is a workflow and generator change, outside this lane.

Validation (all at `e0e1b464`, rc 0, never piped):
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`, exactly as `rtl-fast.yml` writes it: `ctrl_boundary: PASS`, `0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved`. The tree was clean after it.
- Its `--only verilator` sibling, on the pinned Verilator 5.050: `ctrl_boundary: PASS`.
- 107 gates in one serial runner, every one rc 0 with the tree clean after it:
  - every step of rtl-fast's firmware jobs (`test_ctrl_firmware: PASS` on shards 0 to 3; the store suite, 435 tests; coverage `PASS (30 files)`);
  - the harness self-test: 87 checks, 62 of 62 mutants caught; all 62 README mutant rows match;
  - `python3 scripts/check_baremetal_only.py --check`: 0 findings across 1431 files;
  - the full docs-check set (em dash gate: 0 findings over 655 added lines);
  - `cd tests && behave`: 406/406 scenarios.
- Full Verilator sweep, because a shared file changed: 64 of 64 suites, 2,190,531 checks, 0 failures.
- Each new entry is load-bearing. A probe runs the gate's own `ctrl_configs.held` on a stub capture:
  - removing any one entry refuses that file by name;
  - at `f58d049b` the probe's refusal is byte-identical to the hosted one.
- No image change: all nine harness images (six arms, three controls) were rebuilt at this head. Each ELF's sha256 equals the one in round 2's `build.json`.

Acceptance criteria:
1. Registered by what each file does, with the reasons above. Met, with the published departure from the two named options. The gate is not weakened: its code and controls are unchanged, and every entry is load-bearing.
2. The gate, exactly as the workflow runs it, at the new head: rc 0. Also rc 0: the other firmware jobs, the self-test and mutants, the bare-metal gate, the docs gates and behave. Met.
3. Both boundary runs are in the standing gate table. Met.
4. No measurement change and no image or figure change, so the STOP condition is not met.
5. Rows within T_svc: still not met (the measurement STOP). So the PR body keeps "Relates to #665".

Open risks/questions:
- For the manager: whether `build.py` should become a known builder. That needs a hosted job with the runtime packages, the patched LiteX tree and Verilator, plus a build-only mode. It would be a CI change and a new Issue.
- Disclosed: `build.py`'s firmware-tree digest covers `sw/firmware/ctrl`, so it now includes `ctrl_configs.py`. A harness build made before this commit is refused for reuse and must be rebuilt. The images rebuild byte-identical.
- An earlier local commit carried an inaccurate reason ("no hosted job installs the test SoC's packages"; `firmware-boundary` installs the LiteX pins). It was amended before any push. Every gate was rerun from the start at `e0e1b464`.
