# [A698c] #665 Mark II split, lane S4 round 3: R738-F1, the clocks of the target harness's timing evidence

STATUS: REVIEW READY at `ac45db8f`. Every gate and run is rc 0 at that head (the target cases were built at `4e8348ec`, the harness commit, and regraded at the head). Every control, plant and mutant is caught.

- Checkout `$LANES/665-s4-f1-target`, local branch `s4-f1-target` (pushed by the manager as `665-s4-f1-target`, PR #812).
- Base `origin/dev-soft-core` `f4c9ad4f06f185378fd2646298aab51dd108e86f`. `origin` is `https://github.com/kebag-logic/milan-fpga.git`.
- Round-2 head `ee1c0be0b99f0131eb10908a19f080299aa0cbb8`. This round adds three commits on it, with no rebase:
  - `4e8348ec`: the harness and its self-test;
  - `91e33a78`: the docs;
  - `ac45db8f`: one README wording fix, one sentence a line.
- Head `ac45db8f18a5fde87c84be2225cc1be7d709eae9`. Nothing is pushed.
- Assignment: [A10] issuecomment-6511289316 on #665, S4 round 3, R738-F1 on PR #812. R738-1's report is in `665s4-r738-1/REPORT.md`.
- TAKEN: issuecomment-6511304923 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6514025062 (`REVIEW-READY-COMMENT.md`), posted with head `ac45db8f`.
- RTL: unchanged. The firmware is unchanged too; this round touches only the harness's Python and Markdown.

## The finding

R738-F1 is a MINOR, filed under Conformance, Tests and Docs.

- `run_cases` had `cpu_hz` and `sys_hz` from the build, but `results.json` (a bare list of results) and `table.md` dropped them.
- A standalone result could not say which clock its ms figures and its T_svc grading were at.

## Changes (file:line, reason), at `ac45db8f`

| Where | What, and why |
|---|---|
| `tb/verilator/nvm_split_target/run.py:23-28` | The docstring: every figure is converted and graded at the builds' recorded clocks, which `results.json` and `table.md` carry. A record without them, or with clocks that are not right for its figures, is refused (R738-F1). |
| `run.py:92-101` `clocks` | Reads the CPU and bus clocks every arm's `build.json` records, which come from the shape's constraints. It refuses builds that disagree, or that lack either clock as a whole positive number of hertz. Before this, `run_cases` took `any_spec`'s clocks unchecked. |
| `run.py:104-134` `run_cases` | Converts and grades at the `clk` it is given, the same clocks the record names. |
| `run.py:139-143` `record` | `results.json` becomes a record: `point`, `shape`, `cpu_hz`, `sys_hz`, `t_svc_ms` and `results`. Before, it was a bare list, which lost the clocks (the finding's first required change). |
| `run.py:146-149` `missing_clocks` | A finding for each clock that is missing, or is not a whole positive number of hertz. |
| `run.py:152-162` `figures`, `:165-177` `misconverted` | Each ms figure (the longest step; the capture's CPU time, elapsed time and longest step; each phase's longest step) must equal its CPU cycles at the record's CPU clock. Each phase's T_svc verdict and the step control's T_svc in cycles must be at that clock too. This catches a record labelled with a clock its figures were not converted at. |
| `run.py:180-182` `provenance` | `missing_clocks`, or else `misconverted`. |
| `run.py:185-189` `against_build` | A finding for each arm whose `build.json` records other clocks than the record names. This catches a run whose clocks are not its builds'. |
| `run.py:192-200` `mhz`, `clock_line` | The clocks line, rendered from the record's values in MHz and in hertz. No fixed "50 MHz" string. |
| `run.py:203-237` `table` | Refuses a record that fails `provenance` (ValueError). It puts the clocks line, then a blank line, above each of its three tables: the verdicts, the steps against T_svc and the phases. |
| `run.py:274-289` `main` | `clk = clocks(specs)`, then the record. `results.json` is written first, so that a refused run keeps its results for diagnosis. Then `against_build`, then `table`. A refusal exits 2 with no `table.md`. |
| `tb/verilator/nvm_split_target/target_selftest.py:9-12` | The docstring names the clock checks. |
| `target_selftest.py:41`, `:45-53` | `OTHER_CPU_HZ`/`OTHER_SYS_HZ` (62.5 MHz and 125 MHz), the differently clocked input. `RUN` is `run.py` loaded once under its own module name, so that the mutants can replace its functions. |
| `target_selftest.py:148-166` | `graded_commit` and `graded_record` grade the synthetic commit at any clocks. `report_checks` renders through `RUN`. |
| `target_selftest.py:171-210` | `rendered` and `refusal` turn a refusal, or a mutant's crash, into words. `unclocked_tables` lists every table header without a clocks line holding the given words one blank line above it. `main_run` runs `run.py`'s real `main` with `built` and `run_cases` replaced by synthetic ones, so it exercises main's own clock wiring. |
| `target_selftest.py:213-266` `clock_checks` | 12 new checks, listed below. |
| `target_selftest.py:488-510`, `:547-563` | The eight new mutants and their helpers. |
| `tb/verilator/nvm_split_target/README.md:43-48` | Run: what `results.json` and `table.md` carry, where the clocks come from, and when the run is refused. |
| `README.md:156-158`, `:169`, `:183-184`, `:200-201`, `:217-218` | Results: every figure is labelled with its clocks, CPU 50 MHz and bus 100 MHz, the clocks both points' builds recorded. |
| `README.md:251-259` | Self-test: the new clock checks. |
| `README.md:282-289` | The mutant table: the eight new mutants. |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:223` | Section 5: the 8x8 capture figure names its clocks (the finding's architecture-summary item). |
| `sw/firmware/ctrl_nvm/README.md:344-345` | The measured bullets name the bus clock beside the 50 MHz CPU, and say that each run's results carry them. |
| `PR-BODY.md` (output directory) | The F1 timing table and the boot figures name their clocks. Round 3 is described. |

No firmware function changed (`receipts/scope/rtl-unchanged.txt`: no file under `sw/firmware` other than Markdown). The Mark II unit-test rule therefore adds no units, and `fw_coverage.py --check` holds the ratchet. RTL is unchanged.

## New checks: planted mutant and failing words

Each new check, the mutant that must fail it, and the check's name (its failing words when it fails):

| Check (its words) | Planted mutant (`target_selftest.MUTANTS`) |
|---|---|
| `the results record carries the clocks its builds recorded, through JSON` | `clocks: results.json without its clocks` (`run.record` drops `cpu_hz` and `sys_hz`) |
| `a run at other clocks is reported at them: its clocks named, its figures converted at its CPU clock`: at 62.5 MHz the report reads `CPU 62.5 MHz (62,500,000 Hz), bus 125 MHz (125,000,000 Hz)`, has no `50 MHz` and shows the 40,000-cycle step as `0.640` ms, not `0.800` | `clocks: the report names the product clocks whatever it was given` (`run.clock_line` fixed at 50 and 100 MHz) |
| `every table of the report has the clocks beside it`, at 62.5 MHz and at 50 MHz | `clocks: the last table without its clock line` (`run.table` drops the clocks line above its last table) |
| `a record without its cpu_hz is refused`; `a record without its sys_hz is refused` (the words `no cpu_hz recorded` / `no sys_hz recorded`) | `clocks: a missing clock not refused` (`run.missing_clocks` returns nothing) |
| `a record whose clock is not a whole positive number of hertz is refused` (`62.5e6` as a float, `0`) | the same mutant |
| `a record whose CPU clock is not the one its figures were converted at is refused`: a 50 MHz record relabelled 62.5 MHz gives `is not 40,000 CPU cycles at 62,500,000 Hz` and `T_svc of 500,000 cycles` | `clocks: the figures not checked against the CPU clock` (`run.misconverted` returns nothing) |
| `a record whose clocks are not its builds' is refused, naming the build` | a direct check of `against_build`; its mutant is caught through main (below) |
| `builds that disagree on their clocks, lack one or are none are refused` | `clocks: the first build's clocks taken for all` (`run.clocks` takes the first build's and never refuses) |
| `run.py writes its builds' clocks to results.json and beside every table of table.md` (real `main`, builds at 62.5 and 125 MHz) | `clocks: an unconditional 50 MHz and 100 MHz for the run` (`run.clocks` returns the product clocks whatever the builds record) |
| `run.py refuses results graded at another CPU clock than their record names, writing no table` | (a check of main's wiring of `table`'s refusal; the `misconverted` mutant also fails it) |
| `run.py refuses a run whose clocks are not its builds', writing no table` (the run's clocks planted at 50 and 100 MHz over builds at 62.5 and 125 MHz: exit 2, no `table.md`) | `clocks: the record not compared with its builds'` (`run.against_build` returns nothing) |

Self-test at the head: `checks: 61   failures: 0`. That is 41 checks, then 20 mutants, every one caught. Round 2 had 29 checks and 12 mutants; this round adds 12 checks and 8 mutants (`receipts/gates-short/nvm_target_selftest.log`).

The probe `scripts/clock_probe.py` runs the checkout's own `run.py` (`receipts/clock-probe/clock-probe.log`, `PROBES PASS`):

- the synthetic commit at 62.5 and 125 MHz renders those clocks;
- round 2's published 8x8 `results.json`, the bare list with no clocks, is refused with `no cpu_hz recorded; no sys_hz recorded`;
- this round's 8x8 record relabelled to a 100 MHz CPU is refused with `commit: longest step 2.63858 ms is not 131,929 CPU cycles at 100,000,000 Hz; ...`;
- the record as written renders its 50 MHz and 100 MHz line.

## Measurements

Both points were built fresh at `4e8348ec` (`receipts/scope/runs-head.txt`), the commit that changes the harness. The two later commits change only Markdown (`receipts/scope/diffstat-round3.txt`). At the head `ac45db8f`, `--regrade` of both recorded runs reproduces `table.md` and `results.json` byte for byte (`receipts/regrade/`).

Every arm's `build.json` records `cpu_hz` 50,000,000 and `sys_hz` 100,000,000, at both points. Both runs exit `RC=0` (`receipts/target-*/run-tail.log`):

- every case passes;
- every control is caught: `slow-step` with `step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms` at 1x1 and 30.2139 ms at 8x8, and `step-over-t-svc` in all seven phases.

Each `results.json` is `{"point", "shape", "cpu_hz": 50000000, "sys_hz": 100000000, "t_svc_ms": 10.0, "results": [...]}`. Its `results` are identical to round 2's published list, key for key and value for value, at both points: the firmware and the grading are unchanged.

| Point (CPU 50 MHz, bus 100 MHz) | Capture, CPU time | Capture, elapsed | Longest step |
|---|---:|---:|---:|
| 1x1 | 1,361,143 cycles, 27.223 ms | 26,745,259 cycles, 534.905 ms | 101,098 cycles, 2.022 ms (program) |
| 8x8 | 5,161,328 cycles, 103.227 ms | 81,903,050 cycles, 1,638.061 ms | 131,929 cycles, 2.639 ms (capture) |

D5 on the current flash writer: `scripts/plant_d5_removed.py` at `ac45db8f` gives `PLANT CAUGHT`. Planted, it exits 1 with `FAIL: OFF timing limit was ignored`; unplanted, it exits 0 with `PASS: capture census, clocks, both timing arms and receipt agree` (`receipts/d5-plant/`).

The S2 harness (`ctrl_service_budget/run.py --record-budget-findings`, fresh builds at `ac45db8f`, `receipts/budget-*`):

- 1x1: `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, RC=0;
- 8x8: `17 groups graded, 0 refusals, 62 T_svc misses (62 of 182 probe instances, 30 of 129 paths)`, RC=0;
- both `table.md` files are byte-identical to round 2's and round 1's (sha256 `213f93c2...` and `3757c374...`).

As in round 2, these misses are composed rows graded against 10 ms. Regrading them at 20 ms per family belongs to the S2b lane.

The current flash writer's harness (`nvm_capture_cpu`) was not re-run. Its firmware, its harness and its receipt are unchanged since round 2, and `check_nvm_capture.py` regrades that receipt in the short gates (`nvm_capture`, rc 0) and in the D5 plant's unplanted arm. Its round-2 figures stand: at 8x8, with the CPU at 50 MHz and the bus at 100 MHz, at most 13.863 ms with traffic and 13.690 ms without.

## Gates

The runner is round 1's `scripts/gates_s4.py`, unchanged: one log per gate, and the tree checked clean before and after each gate. It ran as two invocations, each serial (`scripts/gates.sh`), both at `ac45db8f` (`receipts/gates-*/HEAD.txt`):

- `short`: every gate but the eleven long ones;
- `long`: the eleven long ones.

Receipts: `receipts/gates-short/` and `receipts/gates-long/`, each with its `summary.md`. Logs over 200 KB are kept as tails, with their full size and sha256 in `large-files.txt`.

| Gate set | Result |
|---|---|
| 97 gates: the docs workflow's check-mode commands (TOC, anchors, cited paths, em dash, doc style, doc map, the diagram and generator checks, and so on), the bare-metal scope gate, the idiom, naming, evidence and hygiene gates, `check_nvm_capture.py` (`nvm_capture`), `check_nvm_record_space.py` and its self-test, `test_nvm_firmware.py --self-test`, `ci_events` and the CI self-tests, `git diff --check` from the base, behave (`406 scenarios passed, 0 failed, 0 skipped`), `hdl_reference`, `firmware_compiler_absent`, the generator self-test, `nvm_split_target`'s self-test (`checks: 61   failures: 0`) and the S2 harness's self-test | `0 of 97 gates nonzero or left the tree dirty` |
| `ctrl_memory` | rc 0 |
| `builder_require_rv32` (`test_builder.py --require-rv32`) | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11's calibration report, which needs a vendor build tree, as in rounds 1 and 2 |
| `ctrl_nvm` (`test_ctrl_nvm.py --require-rv32 --self-test`) | rc 0, `OK across 5 shape(s), 435 tests, and all 109 planted defects reddened` |
| `ctrl_firmware` (`test_ctrl_firmware.py --require-rv32 --self-test`: the control, ACMP, MAAP, AECP and SRP campaigns) | rc 0, `test_ctrl_firmware: PASS`. 1,006 `[ok]` plants, none escaped (`ctrl_firmware-tally.txt`) |
| `fw_coverage.py --selftest` and `--check` | rc 0, `firmware coverage: PASS (31 files)`, 100 % lines and branches |
| `firmware_boundary`, in both modes (rtl-fast's step and the Verilator half) | rc 0 |
| `nvm_cosim`: `make` and `make lint` | rc 0, `465 checks: 465 PASS`, `39 of 39 mutant(s) killed by their named check` |
| `publication_census --check --selftest` | rc 0 |

`0 of 11 gates nonzero or left the tree dirty`.

| Run | Result |
|---|---|
| `nvm_split_target/run.py --point 1x1` and `--point 8x8`, fresh builds at `4e8348ec` | `RC=0` at each point. Clocks recorded: 50,000,000 / 100,000,000 Hz (`receipts/target-*/`) |
| the same, `--regrade` at `ac45db8f` | rc 0; `table.md` and `results.json` byte-identical (`receipts/regrade/`) |
| `ctrl_service_budget/run.py --point 1x1` and `--point 8x8 --record-budget-findings`, fresh builds at `ac45db8f` | `RC=0`: 18 and 17 groups graded, 0 refusals; tables byte-identical to round 2's |
| `scripts/plant_d5_removed.py` at `ac45db8f` | `PLANT CAUGHT`: planted rc 1 with `FAIL: OFF timing limit was ignored`; unplanted rc 0 |
| `scripts/clock_probe.py` | `PROBES PASS` |

Environments, outside the checkout and the output directory (`scripts/env.sh`), are round 2's:

- the product LiteX venv, ahead of the pinned RV32 SDK on PATH;
- a scratch `bin` holding only a link to the system `meson`;
- `LITEX_ENV_CC_TRIPLE=riscv32-linux`, `COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true` and `PYTHONHASHSEED=0`;
- the pinned Markdown renderer's venv;
- round 1's scratch venvs for `tools/hdl_reference/requirements.txt` and for behave.

Not run:

- the four-shard full sweep, since there is no RTL change (`receipts/scope/rtl-unchanged.txt`);
- Vivado;
- `nvm_capture_cpu`'s capture runs. Its firmware, harness and receipt are unchanged, and `check_nvm_capture.py` regrades the receipt.

## Shared files touched

None. Every file this round edits is this lane's own (`tb/verilator/nvm_split_target/`) or a doc page it already edited in round 2:

- `docs/ARCHITECTURE_HW_SW_SPLIT.md`, one line in section 5;
- `sw/firmware/ctrl_nvm/README.md`, two lines.

The S2 harness (`ctrl_service_budget/`), `ctrl_srp_image.py` and `ctrl_configs.py` are untouched.

## Open questions and assumptions

- **`results.json` changed shape**, from a bare list to a record that holds the list as `results`. `grep` finds no reader of it in the tree, and `--regrade` reads the recorded logs, not this file.
- **The CPU budget harness's own `table.md`** (S2's, shared with S2b) does not name its clocks either. R738-F1 is filed against `nvm_split_target`'s outputs, so S2's table is left to that harness's owners. A new Issue is the place for it if the reviewer wants it.
- **"Wrong" provenance, as checked.** Clocks are wrong when they are not every build's recorded clocks, or when they are not the clock the figures were converted at. Nothing in the record can show that the bus clock was used in a conversion, because no ms figure here is at the bus clock. The bus clock is held to the builds' record (`against_build`), and the CPU clock is held to both.
- **T_svc**: still `scenario.T_SVC_MS` = 10 ms at this base, as in round 2. It becomes 20 ms with S2b's change, with no edit here.
- **Mutation testing of `table`'s refusal.** Through `main`, the refusal is exercised by the `graded_at` check. The `misconverted` mutant fails that check, and its own direct check as well.
