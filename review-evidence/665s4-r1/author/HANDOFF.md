# [A698b] #665 Mark II split, lane S4 round 2: F1's capture contract under the owner's option (c)

STATUS: REVIEW READY at `ee1c0be0`. Every gate and run is rc 0 at that head; every control and plant is caught.

- Checkout `$LANES/665-s4-f1-target`, local branch `s4-f1-target`. The assignment names `665-s4-f1-target`; as in round 1, the branch is not renamed.
- Base `origin/dev-soft-core` `f4c9ad4f06f185378fd2646298aab51dd108e86f`. `origin` is `https://github.com/kebag-logic/milan-fpga.git`.
- Round-1 head `9c2f12a80494b9ee95441ca7f9c606ee6cfe617f`. This round adds two commits:
  - `5fbcc077`: the harness, its grader, cases and self-test;
  - `ee1c0be0`: the docs.
- Head `ee1c0be0b99f0131eb10908a19f080299aa0cbb8`. Nothing is pushed.
- Assignment: [A10] issuecomment-6504551000 on #665, the owner's decision of 2026-10-29 19:05, option (c).
- TAKEN: issuecomment-6506102855 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6510555986 (`REVIEW-READY-COMMENT.md`), posted with head `ee1c0be0`.
- Round 1: `../665s4-a698/` (HANDOFF, STOP issuecomment-6500265323, receipts).
- RTL: unchanged. The diff from the base touches no `.sv`, `.v` or SoC Python (`receipts/scope/`).

## Scope as interpreted

1. **The docs.** S4's first acceptance item and F1's capture contract are restated in the owner's wording, with the owner and the date, and each says which writer the 24.5 ms bound covers. The places:
   - `sw/firmware/ctrl_nvm/README.md`;
   - `docs/ARCHITECTURE_HW_SW_SPLIT.md`. Of the split design pages it is the only one that states a capture bound; `SPLIT_CONTROL_MEMORY.md` and `MAILBOX_SPLIT.md` state none;
   - the plan's S4 section (`665-a678/PLAN.md`, outside the repository);
   - `tb/verilator/nvm_split_target/README.md`, and one line in `tb/verilator/nvm_capture_cpu/README.md`, the current writer's own page.

   No `docs/history` edits.
2. **The harness.** `nvm_split_target` grades every F1 service step, in every phase and every case, against T_svc. A step over it fails its case, and with it the run. The capture's CPU time and elapsed time are recorded at both points, with no bound. No report presents 24.5 ms as F1's bound, and the self-test checks the report for it.
3. **The planted defects.**
   - **A step over T_svc:**
     - a firmware plant (`slow-step`), a real first service step spun to 30 ms;
     - a trace control (`step-over-t-svc`): each phase's longest step of the measured commit is stretched to exactly T_svc, then one cycle past it;
     - five grader mutants.
   - **The 24.5 ms check removed from the current flash writer's grader:**
     - an in-tree self-test check with its mutant;
     - a plant of the same removal in a scratch clone, run through `scripts/check_nvm_capture.py` (`scripts/plant_d5_removed.py`).
4. **T_svc's value.** The cases read `scenario.T_SVC_MS`, as they did in round 1.
   - At this base that is still the 10 ms proposal.
   - The owner approved 20 ms, graded per family as `min(T_svc, ceiling)`, on 2026-10-29 12:40 (issuecomment-6495692075). S2b's lane makes it normative in FR_NFR 3.4.1 and `scenario.py`.
   - 10 ms is under every family's bound (the lowest enabled one is SRP's 18 ms), so a step within 10 ms is within each.
   - This lane edits neither FR_NFR nor `scenario.py`. Once S2b's change lands, the cases grade against 20 ms with no edit here. The docs state both values.
5. **D5 on the current flash writer.** Nothing that `check_nvm_capture.py` hashes or reads is edited:
   - `tb/verilator/nvm_capture_cpu/*.py` and `*.cpp`;
   - `measurements.json`;
   - `milan_baremetal.c`.

   That writer keeps its 24.5 ms bound and its gated 8x8 maximum of 13.863 ms.

## Changes (file:line, reason), at `ee1c0be0`

| Where | What, and why |
|---|---|
| `tb/verilator/nvm_split_target/target_grade.py:20-32` | The docstring states the decision: every step is held to T_svc, the capture is measured with no bound, and 24.5 ms is D5's on the current writer, not F1's (assignment item 2). |
| `target_grade.py:51` | `recipe` and `BOUND_MS` are gone, with `nvm_capture_cpu` off the import path. F1's grader no longer reads the current writer's hold floor. |
| `target_grade.py:144-152` | `within_t_svc` and `over_t_svc`: one finding per service step, in any phase, over T_svc, naming the step and its phase. The comparison is in integers. |
| `target_grade.py:155-170` | `capture` records the CPU time, the elapsed time (first step's start to last step's end), and the longest step in cycles and ms. Its only finding is a capture that is not the shape's records plus its closing step. `fits` and the 24.5 ms finding are removed. |
| `target_grade.py:173-197` | `stretched` and `step_control` replace `lengthened`. The control plants T_svc in the measured commit, phase by phase: exactly T_svc adds no finding, and one cycle more adds exactly one, naming that step. |
| `target_grade.py:210` | `phases` uses the same integer comparison. |
| `target_grade.py:348-368` | `grade_case`: every non-control case records its service steps and longest step, and fails on a step over T_svc. A control `over T_svc` is caught by those findings. `t_svc_misses` is removed. |
| `tb/verilator/nvm_split_target/run.py:17-21`, `:100-101` | The exit-status docstring. `bound_control` (`capture-one-page-past`) is replaced by `tg.step_control`. |
| `run.py:118-142` | The report: a per-case table of steps against T_svc, and the capture as "measured (no bound of its own)" with its CPU and elapsed time. Each phase is marked within T_svc. |
| `run.py:145-152`, `:164` | `exit_status` fails on any case that did not pass. `--record-budget-findings` is removed, so a step over T_svc can no longer be recorded instead of failed. |
| `tb/verilator/nvm_split_target/target_cases.py:98-103`, `:141` | The plant `slow-step`: the store's first service step spins on its own clock to 30 ms, over T_svc. It runs as the case `slow-step` on the fixture with blank flash, a control graded by `over T_svc`. |
| `target_cases.py:120-121` | The `Case.control` docstring names the two rule-graded controls. |
| `tb/verilator/nvm_split_target/target_selftest.py:47-66` | `FIRST`, `GAP` and `LIMIT`. `commit_log` takes the other phases' length. |
| `target_selftest.py:69-91` | `capture_checks`: CPU and elapsed time; a capture of twice 24.5 ms with every step within T_svc is no finding; a missing record; the phases. |
| `target_selftest.py:94-125` | `t_svc_checks`: exactly T_svc passes and one cycle over is named, in every phase; any one stretched step, idle included; the step control; a step over T_svc fails its case. |
| `target_selftest.py:128-141` | `report_checks`: the report names T_svc, gives the capture no bound, says "elapsed", and contains no "24.5". |
| `target_selftest.py:144-153` | `boot_log` takes the service step's length; `service_log`. |
| `target_selftest.py:257-271` | `control_checks` adds the `over T_svc` control: caught one cycle over T_svc, and not at T_svc. |
| `target_selftest.py:274-328` | D5 on the current flash writer. `shipping_grader` imports a scratch copy of `nvm_capture_cpu/run.py`, as `shipping_source` leaves it. `d5_checks` requires two things of that grader: its 24.5 ms check is in its source exactly once, and it passes a capture of exactly 24.5 ms and refuses one system tick more. |
| `target_selftest.py:331-412` | `checks` and the mutant table, which now names its owner (the grader or this module): 12 mutants, listed below. |
| `tb/verilator/nvm_split_target/README.md` | The contract line; Grading (every step against T_svc, both T_svc values, the capture measured); the new section "The capture's timing" (the owner's wording, the date, and which writer 24.5 ms covers); Results (rc 0, the capture's CPU and elapsed time); the controls, the self-test and its mutants. |
| `sw/firmware/ctrl_nvm/README.md:36`, `:278`, `:322-339`, `:345-357` | The Contents line. "Five statements". The new statement "The capture's time" (the owner's decision, its date and its four points). The measured bullets: T_svc for every step, both values, and the capture's CPU and elapsed time recorded, not bounded. |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:166-175` | Section 2: the owner's decision with its link and date. F1 is not held to 24.5 ms, with the reason; steps within T_svc; the capture recorded; 24.5 ms covers the current writer's capture. "The existing capture bound ... remain integration obligations" becomes "The boot deadlines remain ...". |
| `ARCHITECTURE_HW_SW_SPLIT.md:222-223` | Section 5: "the capture misses its 24.5 ms bound" becomes every step within T_svc, the capture recorded, with the 8x8 figures. |
| `ARCHITECTURE_HW_SW_SPLIT.md:263-264` | Section 6: the #640 ruling's saved-state capture bound is D5's 24.5 ms on the current writer, and F1 is held to T_svc per step. |
| `tb/verilator/nvm_capture_cpu/README.md:9-10` | The current writer's page says its 24.5 ms bound is D5's on that writer, and that F1 is not held to it. The README is not one of the files `check_nvm_capture.py` hashes, which are only `.py` and `.cpp`. |
| `665-a678/PLAN.md` S4 (outside the repository) | The first acceptance item restated in the owner's wording, and the mutants and measurements lines (`receipts/plan/plan-s4-section.md`). |

No firmware function changed, so the Mark II unit-test rule adds no units, and `fw_coverage.py --check` holds the ratchet. The plant `slow-step` edits a scratch copy of the store only (`build.mutated_source`).

## New checks: planted mutant and failing words

| Check | Planted defect | Failing words |
|---|---|---|
| target `slow-step` (1x1 and 8x8) | `nvm_store.c` `nvm_store_service`: on the first step, `while (nvm_now() - nvm.now_us < 30000u) {}` | 1x1: `step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms`; 8x8: `30.2139 ms` |
| target `step-over-t-svc` (1x1 and 8x8) | each phase's longest step of the measured commit stretched to exactly T_svc (500,000 cycles), then one CPU cycle more | caught in `capture, erase, idle, poll, program, read, seal`: at T_svc no finding is added; one cycle more adds exactly `step N (<phase>) takes 10.0000 ms of CPU time, over T_svc 10.0 ms` |
| self-test mutant `steps: strictly below T_svc` | `within_t_svc` uses `<` | `a step of exactly T_svc passes, in the capture, seal, erase, poll, program and read phases` fails |
| self-test mutant `steps: only the capture's steps graded` | `over_t_svc` keeps capture findings only | `a step one CPU cycle over T_svc is a finding naming it and its phase, ...` fails |
| self-test mutant `steps: the idle step not graded` | `over_t_svc` drops idle findings | `any one step stretched one cycle over T_svc, the idle step among them, ...` fails |
| self-test mutant `steps: no step graded against T_svc` | `over_t_svc` returns nothing | `a service step over T_svc fails its case, one at T_svc does not` fails |
| self-test mutant `step control: the planted cycle not added` | `stretched` returns the observation unchanged | `the step control: each phase's longest step at T_svc passes and one cycle past it is caught` fails |
| self-test mutant `capture: the closing step is not the capture's` | `service` marks no closing step | `the capture's CPU time is its steps' cycles, its elapsed time ...` fails |
| self-test mutant `capture: the elapsed time is its CPU time` | `capture` reports CPU time as elapsed | the same check fails |
| self-test mutant `capture: the current writer's 24.5 ms bound imposed on F1` | `capture` adds a finding over 24.5 ms | `a capture of twice 24.5 ms of CPU time, every step within T_svc, is no finding` fails |
| self-test mutant `the current flash writer: its 24.5 ms check removed from its grader` | `grade_rows`'s three-line 24.5 ms check deleted from `nvm_capture_cpu/run.py`'s source, imported from a scratch copy | `the current flash writer's capture is held to 24.5 ms: exactly 24.5 ms passes, one system tick more is refused` fails |
| D5 plant on the gate (`scripts/plant_d5_removed.py`) | the same three lines deleted from `tb/verilator/nvm_capture_cpu/run.py` in a shared local clone at the head (the submodules cloned at their pinned commits), then `python3 scripts/check_nvm_capture.py` | planted: rc 1, `FAIL: OFF timing limit was ignored`; the unplanted clone: rc 0, `PASS: capture census, clocks, both timing arms and receipt agree` |
| self-test `the report grades every step against T_svc and gives the capture no bound` | (a check, not a plant) the report of a synthetic commit | would fail on `24.5` anywhere in the report, or no `T_svc`, `no bound of its own` or `elapsed` |

The round-1 checks are unchanged except for these removals, which this round's decision retires:

- the control `capture-one-page-past`;
- the self-test checks `a capture at exactly its bound fits` and `a capture one page of its own cost past its bound is caught`;
- the mutants `capture: strictly below the bound`, `capture: the bound is the whole hold floor` and `capture: the planted page is not added`.

## Measurements, at `ee1c0be0`

All on the S2 harness's test SoC: the shipping VexiiRiscv at 50 MHz, the split's 4 KiB instruction cache, LiteSPI on the split SoC's generated map. Every record of the shape is dirty, and each is latched from its real owner. Receipts: `receipts/target-1x1/` and `receipts/target-8x8/`, which hold `table.md`, `results.json`, every case's log and script, and `commit-steps.csv`.

**The capture, recorded with no bound** (the owner's option (c)):

| Point | Records, container | Capture steps | CPU time | Elapsed | Longest capture step | Fixed a step, cycles | A payload byte, cycles |
|---|---|---:|---:|---:|---:|---:|---:|
| 1x1 | 54, 3,336 B | 55 | 1,361,143 cycles, 27.223 ms | 26,745,259 cycles, 534.905 ms | 40,771 cycles, 0.815 ms | 11,062 | 263.7 |
| 8x8 | 164, 13,256 B | 165 | 5,161,328 cycles, 103.227 ms | 81,903,050 cycles, 1,638.061 ms | 131,929 cycles, 2.639 ms | 16,500 | 205.5 |

**Every step against T_svc** (10 ms at this base, 500,000 CPU cycles): within at both points, in every phase and every case.

| Phase (the commit) | 1x1: steps, longest (ms) | 8x8: steps, longest (ms) |
|---|---|---|
| capture | 55, 0.815 | 165, 2.639 |
| seal | 14, 0.688 | 52, 0.697 |
| erase | 1, 0.248 | 1, 0.252 |
| poll | 15, 0.237 | 53, 0.246 |
| program | 14, 2.022 | 52, 2.032 |
| read | 28, 1.907 | 104, 1.920 |
| idle | 203, 0.200 | 215, 0.207 |

The boot cases' longest service step is 0.188 to 0.196 ms (43 steps each at 8x8, 41 at 1x1).

**The boots** (`nvm_store_boot`, CPU cycles), unchanged from round 1:

- 1x1: valid 5,027,209, absent 506,631, torn 8,255,898 and version 504,698;
- 8x8: valid 24,423,878, absent 1,746,898, torn 37,255,159 and version 1,744,933.

**The current flash writer** (`nvm_capture_cpu`, 8x8, 50 MHz, 16 captures, `receipts/capture-cpu/`):

- with traffic, 13.848 to 13.863 ms;
- without, 13.675 to 13.690 ms;
- both RC=0 and under its 24.5 ms, identical to round 1;
- the `skip-copy` and `no-traffic` controls at 1x1: RC=0, each `caught by destination-byte or concurrent-traffic oracle`.

**The S2 harness** (`receipts/budget-*`):

- 1x1: `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, RC=0;
- 8x8: `17 groups graded, 0 refusals, 62 T_svc misses (62 of 182 probe instances, 30 of 129 paths)`, RC=0;
- both `table.md` files are byte-identical to round 1's (sha256 `213f93c2...` and `3757c374...`).

These misses are composed rows, graded against 10 ms with `--record-budget-findings`. Re-grading them at 20 ms per family belongs to the S2b lane (issuecomment-6495692075). This lane's change does not move them.

## Gates, at `ee1c0be0` (the head; all rc 0)

The runner is `scripts/gates_s4.py`, round 1's: one log per gate, the tree checked clean before and after each. It ran as two invocations, each serial (`scripts/gates.sh`):

- `short`: every gate but the eleven long ones;
- `long`: the eleven long ones, started once the target cases' builds were done.

Receipts: `receipts/gates-short/` and `receipts/gates-long/`, each with its `summary.md` or `summary-partial.md`.

| Gate set | Result |
|---|---|
| 97 gates: the docs workflow's check-mode commands (TOC, anchors, cited paths, em dash, doc style, doc map, the diagram and generator checks, and so on), the bare-metal scope gate, the idiom, naming, evidence and hygiene gates, `check_nvm_capture.py` (`nvm_capture`), `check_nvm_record_space.py` and its self-test, `test_nvm_firmware.py --self-test`, `ci_events` and the CI self-tests, `git diff --check` from the base, behave (`406 scenarios passed, 0 failed, 0 skipped`), `hdl_reference`, `firmware_compiler_absent`, the generator self-test, `nvm_split_target`'s self-test (`checks: 41   failures: 0`) and the S2 harness's self-test | `0 of 97 gates nonzero or left the tree dirty` |
| `ctrl_memory` | rc 0 |
| `builder_require_rv32` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11's calibration report, which needs a vendor build tree, as in round 1) |
| `ctrl_nvm`: `test_ctrl_nvm.py --require-rv32 --self-test` | rc 0, `OK across 5 shape(s), 435 tests, and all 109 planted defects reddened` |
| `ctrl_firmware`: `test_ctrl_firmware.py --require-rv32 --self-test` (the control, ACMP, MAAP, AECP and SRP campaigns) | rc 0, `test_ctrl_firmware: PASS`, 1,006 `[ok]` plants, none escaped (`ctrl_firmware-tally.txt`) |
| `fw_coverage.py --selftest` and `--check` | rc 0, `firmware coverage: PASS (31 files)`, 100 % lines and branches |
| `firmware_boundary` in both modes (rtl-fast's step, and the Verilator half) | rc 0 |
| `nvm_cosim`: `make` and `make lint` | rc 0, `465 checks: 465 PASS`, `39 of 39 mutant(s) killed by their named check` |
| `publication_census --check --selftest` | rc 0 |

| Run | Result |
|---|---|
| `nvm_split_target/run.py --point 1x1` and `--point 8x8` (fresh builds) | `RC=0` at each point: every case `pass`, every control `caught` (`receipts/target-*/run-tail.log`) |
| `ctrl_service_budget/run.py --point 1x1` and `--point 8x8 --record-budget-findings` (fresh builds) | `RC=0`: 18 and 17 groups graded, 0 refusals; tables byte-identical to round 1's |
| `nvm_capture_cpu/run.py`, 8x8 at 50 MHz, 16 captures, traffic on and off | `RC=0` each; 13.848 to 13.863 ms, and 13.675 to 13.690 ms |
| `nvm_capture_cpu` controls `skip-copy` and `no-traffic`, 1x1 | `RC=0`, each `caught by destination-byte or concurrent-traffic oracle` |
| `scripts/plant_d5_removed.py` (the current writer's 24.5 ms check removed, `check_nvm_capture.py` in a shared clone) | `PLANT CAUGHT`: planted rc 1, `FAIL: OFF timing limit was ignored`; unplanted rc 0 |

Environments, outside the checkout and the output directory (`scripts/env.sh`):

- the product LiteX venv, ahead of the pinned RV32 SDK on PATH (the SDK's `host/bin` carries its own `python3`);
- a scratch `bin` holding only a link to the system `meson`, ahead of the SDK's `meson` shim;
- `LITEX_ENV_CC_TRIPLE=riscv32-linux`, `COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true` and `PYTHONHASHSEED=0`;
- the pinned Markdown renderer's venv;
- round 1's scratch venvs for `tools/hdl_reference/requirements.txt` (hash-pinned) and for behave.

The capture harness ran without a network namespace, as in round 1; the offline variables were set.

Not run:

- the four-shard full sweep, since there is no RTL change (`receipts/scope/rtl-unchanged.txt`);
- Vivado, since no route is needed;
- `nvm_capture_cpu`'s 1x1 and 100 MHz arms. Neither its firmware nor its harness changed, and `check_nvm_capture.py` regrades the whole receipt.

## Shared files touched

None this round. Every file this round edits is this lane's own: the `nvm_split_target` harness and the docs. Two exceptions:

- `docs/ARCHITECTURE_HW_SW_SPLIT.md`: section 2 gains nine lines, and sections 5 and 6 two lines each;
- `tb/verilator/nvm_capture_cpu/README.md`: two lines.

The S2 harness files that round 1 shared with S2b (`build.py`, `split_soc.py`, `selftest.py`, `README.md`, `sim_main.cpp` and `grade.py`) are untouched this round, as are `ctrl_srp_image.py` and `ctrl_configs.py`.

## Open questions and assumptions

- **T_svc's value at this base.** The cases grade against `scenario.T_SVC_MS`, 10 ms at `f4c9ad4f`.
  - The owner's ruling quotes FR_NFR 3.4.1 "as amended (20 ms, graded per family)". That amendment is S2b's change and is not on this base.
  - The docs quote the ruling, and they state that the cases grade against the 10 ms proposal until it lands. These docs are the nvm_split_target and ctrl_nvm READMEs; `ARCHITECTURE_HW_SW_SPLIT.md` quotes the ruling only.
  - Once S2b's `scenario.py` lands, the cases read 20 ms with no edit here. The docs that quote 10 ms should then be updated: `ctrl_nvm/README.md` and the `nvm_split_target` README. Whoever merges second does that.
  - F1's longest step is 2.639 ms, so either value passes.
- **The per-family rule for F1's steps.** F1 is not one of the ruling's families. A saved-state step consumes the budget of the path it delays, under FR_NFR 3.4.1 "Backlog, preemption, state access and saved-state service consume this budget". That is the S2 harness's composed grading, not this harness's. The cases hold each F1 step to T_svc alone, as the ruling says.
- **The current writer's 24.5 ms check.** The hosted guard is `check_nvm_capture.py` in the docs workflow, unchanged. `nvm_split_target`'s self-test, which also guards it, runs in the lane gates and in no hosted workflow. Wiring it into one would change `ci_events`' recorded step counts, which is out of scope here.
- **Removed:** `nvm_split_target/run.py --record-budget-findings`. Under the ruling, T_svc is F1's only timing bound, so a step over it fails the run and can no longer be recorded in its place. The S2 harness keeps its own flag.
- **The capture's elapsed time** runs from its first step's start to its last step's end. It includes the loop's ticks between steps, one record a 10 ms tick, so it is the loop's pacing, not CPU work.
