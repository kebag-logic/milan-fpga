# [A698d] #665 Mark II split, lane S4 round 4: R738-F2, a refused run beside an earlier run's table

STATUS: REVIEW READY. Head `4d9b901c`, no commit added since the holds. All 108 gates (97 short, 11 long), both target points, both S2 harness points, the D5 plant and the three probes are rc 0 at it.

- Checkout `$LANES/665-s4-f1-target`, local branch `s4-f1-target` (pushed by the manager as `665-s4-f1-target`, PR #812, at round 3's `ac45db8f`).
- Base `origin/dev-soft-core` `f4c9ad4f06f185378fd2646298aab51dd108e86f`. `origin` is `https://github.com/kebag-logic/milan-fpga.git`.
- Round-3 head `ac45db8f18a5fde87c84be2225cc1be7d709eae9`. This round adds two commits on it, with no rebase, no force and no merge:
  - `75126928`: the harness and its self-test;
  - `4d9b901c`: the harness README.
- Head `4d9b901cd42fb21ac7c05432b88bb6c00061064a`.
- Assignment: [A10] issuecomment-6514339158 on #665, S4 round 4, R738-F2 on PR #812. R738-2's report is issuecomment-6514335214 (packet `665s4-r738-2/REPORT.md`).
- TAKEN: issuecomment-6514468865 (`TAKEN-COMMENT.md`), posted 2026-10-30 before the hold. Not posted again.
- REVIEW READY: issuecomment-6673556780 (`REVIEW-READY-COMMENT.md`), posted 2026-11-06 at head `4d9b901c`.
- RTL: unchanged. Firmware: unchanged. This round touches only the target harness's Python and its README.

## Resume, 2026-11-05

The owner's hold (issuecomment-6515668991, 2026-10-30 06:22) stopped this round mid-gates. On resume:

- The tree was clean. Both round-4 commits were complete as committed: `git diff ac45db8f 4d9b901c` holds the whole fix, its checks, its mutants and the README.
- The short set (97 gates), both target points, both S2 harness points, the D5 plant and the three probes had all finished rc 0 at `4d9b901c` before the hold. Their receipts are reused unchanged; every one records that head (`receipts/gates-short/HEAD.txt`, `receipts/scope/runs-head.txt`).
- The long set had finished only `ctrl_memory` (rc 0) and was killed inside `builder_require_rv32` (a `KeyboardInterrupt` in the runner). That partial run is discarded. All eleven long gates re-ran from the start at `4d9b901c`.
- No new commit. Nothing the rulings since the hold change needs an edit in this lane's files (below).

### Second resume, 2026-11-05 18:37 (host reset at 13:10)

- The tree was clean at `4d9b901c`, with no uncommitted edit. No comment was posted on #665 in the morning session, and none has been posted on #665 since 2026-11-04 15:45.
- At the reset, the long re-run had finished seven of its eleven gates, all rc 0 with the tree clean at `4d9b901c` (`receipts/gates-long/runner.log`, `HEAD.txt`): `ctrl_memory`, `builder_require_rv32`, `ctrl_nvm`, `ctrl_firmware`, `fw_coverage_selftest`, `fw_coverage` and `firmware_boundary_verilator`. Their logs are complete and are kept as they stand. The runner died before it wrote `summary.md`.
- It was inside `nvm_cosim` when the host went down. That log stops at `building 42 build(s)`, and it is kept as `receipts/gates-long/nvm_cosim-cut-by-host-reset.log`, which is not evidence.
- The four gates not finished (`nvm_cosim`, `nvm_cosim_lint`, `firmware_boundary`, `publication_census`) re-ran from the start at the same head, through the same runner (`scripts/gates.sh rest`), into `receipts/gates-long-rest/`. `nvm_cosim` removes and rebuilds each build and run directory itself (`run_cases.py:206-209`, `:280-281`), so the reset's half-written builds could not be reused.
- `dev-soft-core` is still `a68536fa`. The merge question below stands unchanged.
- This session's unit is `milan-665s4-a698d-r2.service`, pinned to CPUs 48-63. `cpu_ranges.py show` reads that affinity as busy. No other unit was started.
- The four finished rc 0 with the tree clean (`receipts/gates-long-rest/runner.log`), just before the owner's hold of 19:17.

### Third resume, 2026-11-06 01:45 (owner hold of 2026-11-05 19:17)

- The tree was clean at `4d9b901c`, with no uncommitted edit. All eleven long gates had finished rc 0 at that head before the hold, so nothing re-ran; this session only joined the receipts and wrote the comment.
- No `[A698d]` comment had been posted since TAKEN. On #665 since the hold there is only S2b's [A683u] REVIEW READY (issuecomment-6673169386), which names no S4 item. `dev-soft-core` is still `a68536fa` (`git ls-remote`), so the merge question below stands. The remote `665-s4-f1-target` is still round 3's `ac45db8f`.

## Rulings since the round was assigned, and what they change here

| Ruling | What it changes for S4 |
|---|---|
| [A10] issuecomment-6514866239 (owner, 2026-10-30 05:17): the split CPU clock is 100 MHz, on `sys` | Its own words: "S4's figures are recorded at the clocks its builds name, and that stays valid". S2b moves the CPU to `sys`, and S2b has not merged. At `dev-soft-core` `a68536fa` the split CPU is still on the Milan clock, and this lane's builds record `cpu_hz` 50,000,000 and `sys_hz` 100,000,000 (`receipts/target-*/build-clocks.txt`). Every figure names those clocks (round 3). The harness reads `cpu_hz` from each build's `build.json`, so a run after S2b merges grades and labels at 100 MHz with no edit here. No change. |
| T_svc 20 ms, per family `min(T_svc, 10 % ceiling)`, SRP 18 ms (issuecomment-6495692075; restated in 6634982529) | The docs already say this (`docs/ARCHITECTURE_HW_SW_SPLIT.md`, `tb/verilator/nvm_split_target/README.md` "The capture's timing": "10 ms is under every family's bound, the 18 ms of SRP's included"). At this base `scenario.T_SVC_MS` is still 10.0, and S2b makes 20 ms normative. No change. |
| [A10] issuecomment-6630265194 and issuecomment-6634982529 (S2b rounds 15 and 16) | THE RETRY's 20 ms bound, the SRP lever, the share by construction: all S2b's, in files this lane does not touch. The one item for every lane is the booking rule (below). |
| Booking: every CPU range through `cpu_ranges.py` | Every gate and run of this round ran inside this lane's own unit, `milan-665s4-a698d-r.service`, pinned to CPUs 112-127. That is the unit affinity `cpu_ranges.py` reads as a booking. No other unit was started (no sweep, no shards, no Vivado), so no other range was booked. |

## The live base no longer merges cleanly (open question for the manager)

`receipts/scope/merge-check.txt`, `receipts/scope/merge-conflict-hunks.txt`:

- Onto `dev-soft-core` `5b5f4336` (the assignment's statement): `git merge-tree --write-tree` rc 0, tree `48bb5d60`. Still true.
- Onto the live `dev-soft-core` `a68536fa` (#830's dev sync, and since): rc 1, **two conflicts**, both in the S2 CPU budget harness, a shared file this lane changed in round 1 (`0d61b327`):
  - `tb/verilator/ctrl_service_budget/split_soc.py`. `dcd56703` (#814) wraps the harness's `FlashBoundary` in `milan_soc.stage_spi_phy` and keeps `with_master=False` with a separate `LiteSPIMaster`. This lane's `0d61b327` gives `FlashBoundary` the generic PHY's two CSRs and a divisor, uses `with_master=True` (one CSR bank, as the split SoC's `add_spi_flash` lays it out) and checks the `spiflash` and `timer0` banks against the split SoC's map. The docstring conflicts the same way.
  - `tb/verilator/ctrl_service_budget/README.md`, two hunks: the flash's description, and the paragraph on whether an address changes an access's cost.
- The resolution looks mechanical: stage this lane's `FlashBoundary(..., divisor)` and keep `with_master=True` and the placement checks. `stage_spi_phy` keeps the PHY's CSR names ("the stage becomes the PHY's submodule `stage`, so the PHY's CSR names are unchanged"). It is not free, though. The stage adds bus cycles to every flash access ("two a word in a burst, eight a new burst"). So every S4 figure (the capture, every step, the boots) and the S2 harness's tables would move at a merged head, and both points would need re-measuring, with every gate.
- **Not done here.** The round says "add commits on top of `ac45db8f`, with no rebase" and names no merge. S2b's merge of `a68536fa` was ordered in its resume ([A683o] issuecomment-6563800676). A merge commit resolving a conflict between two lanes' harness changes is the kind of choice AGENTS.md section 2 says to publish, not make privately.
- **The question:** merge `a68536fa` into this branch in a round of its own (resolution as above, both points re-measured), or merge the PR another way. Neither changes R738-F2's fix, which is in `tb/verilator/nvm_split_target/` only. `a68536fa` changes no file there or under `sw/firmware/ctrl_nvm`.

## The finding

R738-F2 is a MINOR, filed under Conformance, Robustness, Tests and Docs.

- `main` wrote `results.json` before it checked the record's clocks against its builds' and before `table` checked its figures, and it never removed an earlier `table.md`.
- So a refused run (exit 2) in a reused `--out` left the earlier run's success table, byte for byte, beside a new, refused `results.json`.
- The self-test's `main_run` used a fresh directory per call, so it never saw this.

## Changes (file:line, reason)

| Where | What, and why |
|---|---|
| `tb/verilator/nvm_split_target/run.py:30-33` | Docstring: `results.json` and `table.md` are one validated run's; a refused run leaves only `refused.json` (R738-F2). |
| `run.py:242-243` `ACCEPTED`, `REFUSAL` | The names of the accepted pair and of the refusal record. |
| `run.py:246-250` `clear` | Removes `results.json`, `table.md` and `refused.json` from `--out`. Called at the start of every run and by `refuse`. Before, nothing removed an earlier run's outputs. |
| `run.py:253-262` `accept` | Validates first (`against_build`, then `table`, which applies `provenance`), and writes `results.json` and `table.md` only after both pass. Before, `main` wrote `results.json` before either check (the finding's cause). |
| `run.py:265-273` `refuse` | A refused run's only output: `clear`, which removes anything of the pair already written (for example if writing `table.md` failed after `results.json`), then `refused.json` holding `refused` (the words) and `record` (the refused record, or `null` when the refusal came before one was made). It has no `cpu_hz`, `sys_hz` or `results` at its top, so no reader of an accepted record can take it for one. If the directory cannot be written, the run still exits 2 and says so. |
| `run.py:312-325` `main` | `clear` before building, then `accept`; any `RuntimeError`, `OSError` or `ValueError` prints `REFUSED:`, calls `refuse` and exits 2. |
| `tb/verilator/nvm_split_target/target_selftest.py:12-14` | Docstring: the reused-directory checks. |
| `target_selftest.py:194-231` `Run`, `main_run`, `RUN_JSON` | `main_run` takes `root` (an output directory to reuse; default a fresh one, as before) and `builds` (per-arm build clocks, for a missing or disagreeing build clock). It returns `refused.json` too, and a crash under a mutant becomes status -1 instead of an exception. |
| `target_selftest.py:234-246` `accepted`, `refused_alone` | What an accepted run leaves (exit 0, `results.json` at its clocks, every table clocked, no refusal) and what a refused run leaves (exit 2, no `results.json`, no `table.md`, `refused.json` naming the refusal and shaped like no record). |
| `target_selftest.py:249-295` `reused_checks` | 7 new checks, listed below. |
| `target_selftest.py:339-350` (`clock_checks`) | The two fresh-directory refusal controls are kept. They now also require no `results.json`, and the "not its builds'" control reads the refused record's clocks from `refused.json`, where round 3 read them from `results.json`. |
| `target_selftest.py:600-626`, `:677-688` | The five new mutants and their helpers. |
| `tb/verilator/nvm_split_target/README.md:43-53` | Run: an accepted run writes the pair; a refused run leaves `refused.json` alone; what `clear`, `accept` and `refuse` do. The old sentence promised "no `table.md`" but the code broke that promise on a reused directory. |
| `README.md:263-269` | Self-test: the reused-directory checks. |
| `README.md:300-304` | Mutant table: the five new mutants. |

No firmware function changed, so the Mark II unit-test rule adds no units; `fw_coverage.py --check` holds the ratchet. RTL is unchanged.

## New checks: planted mutant and failing words

| Check (its words) | Planted mutant (`target_selftest.MUTANTS`) |
|---|---|
| `a success, then a build without its CPU clock in the same directory: the refusal alone, no table or results left` (refused by `run.clocks`, before any record: `refused.json` has `record: null`) | `reuse: an earlier run's results and refusal left in place` (`run.clear` does nothing) |
| `a success, then builds that disagree on their clocks in the same directory: the refusal alone, no table or results left` | the same mutant fails it too |
| `a success, then clocks that are not its builds' in the same directory: the refusal alone, no table or results left` (refused by `against_build`) | the same mutant fails it too |
| `a success, then results misconverted in the same directory: the refusal alone, no table or results left` (refused by `table`'s `provenance`) | `reuse: the refused record written as results.json` (`run.refuse` writes the record where the accepted one goes) |
| `a refusal, then a success in the same directory: the success's pair alone, no refusal left` | `reuse: an earlier refusal left beside a success` (`run.clear` removes the pair but not `refused.json`) |
| `accept writes nothing for a record it refuses` | `reuse: results.json written before its record is validated` (round 3's ordering, in `run.accept`) |
| `refuse removes a pair already written and leaves its refusal alone` | `reuse: a refusal leaves a pair already written` (`run.refuse` without its `clear`) |

Every one of the four "success, then refusal" checks also fails under `reuse: an earlier run's results and refusal left in place` and under `reuse: the refused record written as results.json`. Each mutant's full failing set is in `receipts/probes/reuse-mutant-failures.txt`.

The design has two layers of defence, and each covers for the other. The first is `clear` at the start of every run. The second is validating before writing, together with `refuse`'s own `clear`. So round 3's ordering alone, or a `refuse` without its `clear` alone, leaves no stale file through `main`. Each of those two mutants is therefore planted against a direct check of `accept` or `refuse`, and that check fails on it.

Self-test at the head: `checks: 73   failures: 0`. That is 48 checks, then 25 mutants, every one caught. Round 3 had 41 checks and 20 mutants; this round adds 7 checks and 5 mutants. The two fresh-directory refusal controls are kept and tightened (`receipts/gates-short/nvm_target_selftest.log`).

## Probes

- **`scripts/reuse_probe.py`** (`receipts/probes/reuse-probe.log`, `PROBE PASS`). It runs `main` with R738-2's producer substitutions, against round 3's `run.py` (`git show ac45db8f:...`, in scratch) and against the checkout's:
  - **round 3**: a success, then each of the four refusals, exits 2. Each leaves `['results.json', 'table.md']`, and the table is the earlier run's, byte for byte (the finding, reproduced);
  - **the checkout**: each leaves `['refused.json']` alone, and a refusal followed by a success leaves `['results.json', 'table.md']`.
- **`scripts/real_refusal_probe.py`**, on each point's fresh build: R738-2's real `--regrade` probe (`receipts/probes/real-refusal-{1x1,8x8}.log`, `PROBE PASS` at each point).
  - With `cpu_hz` deleted from the capture build's `build.json`, `--regrade` exits 2 with `REFUSED: the builds record different clocks (CPU Hz, bus Hz): {'capture-all': (None, 100000000), ...`. It leaves only `refused.json`, whose top keys are `record` and `refused`.
  - With `build.json` restored byte for byte, `--regrade` exits 0. It leaves `results.json` and `table.md`, byte-identical to the fresh run's.

## Measurements

Both points were built fresh at the head `4d9b901c` (`receipts/scope/runs-head.txt`). Every arm's `build.json` records `cpu_hz` 50,000,000 and `sys_hz` 100,000,000, at both points (`receipts/target-*/build-clocks.txt`). Both runs exit `RC=0` (`receipts/target-*/run-tail.log`):

- every case passes;
- every control is caught: `slow-step` with `step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms` at 1x1 and 30.2139 ms at 8x8, and `step-over-t-svc` in all seven phases.

`results.json` and `table.md` are byte-identical to round 3's at both points (`receipts/probes/round3-identity.txt`): the grading and the firmware are unchanged. The capture, at CPU 50 MHz and bus 100 MHz:

| Point | Capture, CPU time | Capture, elapsed | Longest step |
|---|---:|---:|---:|
| 1x1 | 1,361,143 cycles, 27.223 ms | 26,745,259 cycles, 534.905 ms | 101,098 cycles, 2.022 ms (program) |
| 8x8 | 5,161,328 cycles, 103.227 ms | 81,903,050 cycles, 1,638.061 ms | 131,929 cycles, 2.639 ms (capture) |

D5 on the current flash writer: `scripts/plant_d5_removed.py` at the head gives `PLANT CAUGHT`. Planted, it exits 1 with `FAIL: OFF timing limit was ignored`; unplanted, it exits 0 with `PASS: capture census, clocks, both timing arms and receipt agree` (`receipts/d5-plant/`).

The S2 harness (`ctrl_service_budget/run.py --record-budget-findings`, fresh builds at the head, `receipts/budget-*`):

- 1x1: `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, RC=0;
- 8x8: `17 groups graded, 0 refusals, 62 T_svc misses (62 of 182 probe instances, 30 of 129 paths)`, RC=0;
- both `table.md` files are byte-identical to round 3's.

As before, these misses are composed rows graded against 10 ms. Regrading them at 20 ms per family belongs to S2b.

## Gates

The runner is round 1's `scripts/gates_s4.py`, unchanged. It writes one log per gate and checks that the tree is clean before and after each gate. It ran as two invocations at `4d9b901c`, each serial (`scripts/gates.sh`), with nothing else reading the checkout beside them:

- `short`: every gate but the eleven long ones (2026-10-30, before the hold);
- `long`: the eleven long ones. They re-ran on 2026-11-05 after the hold killed the first attempt. The host reset at 13:10 cut that re-run after seven gates (`receipts/gates-long/`). The other four ran from the start at the same head at 18:39 (`receipts/gates-long-rest/`).

Receipts are in `receipts/gates-short/`, `receipts/gates-long/` and `receipts/gates-long-rest/`. Each holds the runner's log and `HEAD.txt`. The two complete invocations also hold their `summary.md`; the cut one has none. Logs over 200 KB are kept as tails, with their full size and sha256 in `large-files.txt`.

| Gate set | Result |
|---|---|
| 97 gates. They cover the docs workflow's check-mode commands (TOC, anchors, cited paths, em dash, doc style, doc map, and the diagram and generator checks), the bare-metal scope gate, and the idiom, naming, evidence and hygiene gates. They also cover `check_nvm_capture.py` (`nvm_capture`), `check_nvm_record_space.py` and its self-test, `test_nvm_firmware.py --self-test`, `ci_events` and the CI self-tests, and `git diff --check` from the base. The rest: behave (`406 scenarios passed, 0 failed, 0 skipped`), `hdl_reference`, `firmware_compiler_absent`, the generator self-test, `nvm_split_target`'s self-test (`checks: 73   failures: 0`) and the S2 harness's self-test | `0 of 97 gates nonzero or left the tree dirty` |
| `ctrl_memory` | rc 0, `test_ctrl_memory: 0 failure(s)` |
| `builder_require_rv32` (`test_builder.py --require-rv32`) | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11's calibration report, which needs a vendor build tree, as in rounds 1 to 3 |
| `ctrl_nvm` (`test_ctrl_nvm.py --require-rv32 --self-test`) | rc 0, `OK across 5 shape(s), 435 tests, and all 109 planted defects reddened` |
| `ctrl_firmware` (`test_ctrl_firmware.py --require-rv32 --self-test`: the control, ACMP, MAAP, AECP and SRP campaigns) | rc 0, `test_ctrl_firmware: PASS`. 1,006 `[ok]` plants, none escaped (`ctrl_firmware-tally.txt`; the full log's size and sha256 in `large-files.txt`) |
| `fw_coverage.py --selftest` and `--check` | rc 0: `29 of 29 planted cases read as planted`; `firmware coverage: PASS (31 files)`, 100 % lines and branches, `nvm_flash_litespi.c` among them |
| `firmware_boundary`, in both modes (rtl-fast's step and the Verilator half) | rc 0, `ctrl_boundary: PASS` in each, 0 findings |
| `nvm_cosim`: `make` and `make lint` | rc 0, `465 checks: 465 PASS, 0 FAIL`, `39 of 39 mutant(s) killed by their named check` |
| `publication_census --check --selftest` | rc 0, `checks: 234   failures: 0`, `selftest: 0 of 138 arm(s) failed` |

`0 of 11 gates nonzero or left the tree dirty` (`receipts/gates-long-summary.md`, joined by `scripts/long_summary.py` from the two runner logs; it refuses a gate missing, a gate in both parts, or two heads).

| Run | Result |
|---|---|
| `nvm_split_target/run.py --point 1x1` and `--point 8x8`, fresh builds at `4d9b901c` | `RC=0` at each point; clocks recorded 50,000,000 / 100,000,000 Hz; outputs byte-identical to round 3's |
| `scripts/real_refusal_probe.py` at each point | `PROBE PASS`: missing `cpu_hz` gives rc 2 and `refused.json` alone; restored gives rc 0 and the pair byte-identical |
| `scripts/reuse_probe.py` | `PROBE PASS`: round 3 leaves the stale table, the checkout does not |
| `ctrl_service_budget/run.py --point 1x1` and `--point 8x8 --record-budget-findings`, fresh builds at `4d9b901c` | `RC=0`: 18 and 17 groups graded, 0 refusals; tables byte-identical to round 3's |
| `scripts/plant_d5_removed.py` at `4d9b901c` | `PLANT CAUGHT` |

Environments (`scripts/env.sh`) are round 3's. They sit outside the checkout and the output directory:

- the product LiteX venv, ahead of the pinned RV32 SDK on PATH;
- a scratch `bin` holding only a link to the system `meson`;
- `LITEX_ENV_CC_TRIPLE=riscv32-linux`, `COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true` and `PYTHONHASHSEED=0`;
- the pinned Markdown renderer's venv;
- round 1's scratch venvs for `tools/hdl_reference/requirements.txt` and for behave.

Not run:

- the four-shard full sweep, because RTL is unchanged (`receipts/scope/rtl-unchanged.txt`);
- Vivado;
- `nvm_capture_cpu`'s capture runs. That writer's firmware, harness and receipt are unchanged, and `check_nvm_capture.py` regrades the receipt.

## Shared files touched

None this round. All three files are this lane's own, under `tb/verilator/nvm_split_target/`. Round 1 touched the shared S2 harness (`tb/verilator/ctrl_service_budget/`), `docs/ARCHITECTURE_HW_SW_SPLIT.md` and two files under `sw/firmware/ctrl/test/`. Two of those, in the S2 harness, now conflict with the live base (above).

## Open questions and assumptions

- **The live base.** The branch conflicts with `dev-soft-core` `a68536fa` in two S2-harness files (above). That needs a ruling.
- **After S2b merges.** The target harness's README says it runs on "the shipping VexiiRiscv at 50 MHz", and every figure in the lane's docs is labelled CPU 50 MHz, bus 100 MHz. That is what this base builds, and [A10] issuecomment-6514866239 keeps those figures valid. Once the CPU is on `sys` at 100 MHz, a re-run reports at 100 MHz with no code change. The README's sentence and the docs' figures would then be restated from that run.
- **`refused.json` is new.** It is a diagnostic, not evidence. It is written only by a refused run and removed by the next run. Nothing in the tree reads it, or `results.json`.
- **`--regrade` now removes the previous `results.json` and `table.md` before it regrades.** A reviewer who wants to compare a regrade with an earlier run must keep a copy first, as `real_refusal_probe.py` does.
- **An unwritable output directory.** If `refuse` itself cannot write, the run still exits 2 and prints `REFUSED: and its refusal not recorded in ...`. That branch is not exercised by the self-test, because it would have to make a directory unwritable.
- **R737-1's retained suggestions S2 to S4** are outside this delta and unchanged.
- **T_svc** is still `scenario.T_SVC_MS` = 10 ms at this base.
