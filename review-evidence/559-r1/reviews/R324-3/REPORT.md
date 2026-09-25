[R324] POSITIVE - exact head b02af0480d3a3061df24683d522799d1759f7c33

Round R324-3, internal independent review of PR #564 for issue #559. Tree `8c9f216b462e2f0fd7b8da9c73e3f817a8555d32`, source base `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`. Reviewed delta: `32076148..b02af048` (round 2 `31808e65` and round 3 `b02af048`), read against the whole PR diff `a3d795ae..b02af048`.

All five lenses were applied independently. I have no open BLOCKER, MAJOR or MINOR finding. There are three SUGGESTIONs (S1 to S3). Every prior finding on this PR is resolved at this head (see "Prior findings").

## Reconstruction

I read the following in order:

1. AGENTS.md and CONTRIBUTING.md, including section 3 (the verification bar and "Measure, don't assume").
2. docs/README.md.
3. The body of issue #559 and its frozen acceptance criteria.
4. The public decisions on the issue: the route and remedy order (issuecomment-5828771434), round 2 (5831090112: 50 MHz contract clock with aligned edges, the yaml left to #565, hold 50 ms against a 49 ms floor, a hosted census/clock gate with a named control per input, STOP above 24.5 ms), and round 3 (5832136947: pin the step in `ci_events.py`).
5. The void notice 5832130021.
6. The authorities:
   - `docs/integration/BAREMETAL_FIRMWARE.md` (the cacheless CPU at 50 MHz);
   - `hdl/milan/KL_nvm_backend.sv` (hold and millisecond tick);
   - `hdl/milan/KL_pp_shadow.sv` (backend instantiation);
   - the product `nvm_capture()` in `sw/firmware/milan_baremetal/milan_baremetal.c`;
   - `scripts/nvm_shape.py` and `scripts/nvm_contract.py` (census);
   - `sw/builder/endstation_builder.py` (clock-derived artifacts);
   - `scripts/suite_shards.py` (sweep discovery).
7. The diff and history.
8. The public evidence archive `c73f1dc8` (author-r2, author-r3, and my own R324-1 probe scripts).

I read no other reviewer's report before writing my verdict. The verdict and ledger were fixed first (`receipts/independent_verdict_before_prior_findings.txt`, 13:14:14Z). The two round-1 reports were read afterwards, only to resolve their findings. The concurrent round-3 report of the other reviewer was not read.

## Verification results

### (1) 50 MHz probe reproduction

I used my round-1 probe method (`probe_step.py`, `probe_env.sh`, `probe_setup.sh`, `probe_edit_50mhz.patch`). The only change is two new arguments, `--cpu-hz` and `--traffic`, which pass the head's new harness inputs. The PR's harness modules are imported unchanged.

Environment: scoped Verilator 5.050 (identity in `receipts/environment.txt`), the pinned RV32 SDK (gcc 14.3.0), LiteX revisions equal to the receipt's `soc_component_revisions`, and CPU netlist `c208df0b...` equal to the receipt. Each foreground step is bounded at under 600 s, so long arms produce a prefix of rows. Each reproduced row is compared field by field with `measurements.json` (`compare_rows.py`, `receipts/probe_comparison.txt`).

| Arm (head, aligned edges, 16-capture build) | Rows reproduced | Equal to receipt (cycles and all traffic counters) | Receipt arm maximum |
|---|---|---|---|
| 8x8, 50 MHz, ON | 0-2 | yes (2,429,800 / 2,429,322 / 2,429,864) | 24.30454 ms (row 10, not reached) |
| 8x8, 50 MHz, OFF | 0-2 | yes, including the arm maximum at row 1 (2,426,154) | 24.26154 ms, reproduced |
| 1x1, 50 MHz, ON | 0-15 (all) | yes, 16/16 | 6.60642 ms, reproduced |
| 1x1, 50 MHz, OFF | 0-15 (all) | yes, 16/16 | 6.58857 ms, reproduced |
| 8x8 via my round-1 route (yaml edited to 50 MHz), ON | 0-2 | yes: identical to the head's override route | - |
| 8x8, round-1 shape (yaml 50 MHz, 2 captures) | 0 | 2,429,662 cycles, requests 151,767, reads 5,850: equal to my round-1 aligned probe row 0 | - |

The BIOS and instrumented-firmware SHA-256 of all four head arms equal the receipt's `bios_sha256` and `instrumented_firmware_sha256`. The simulation is deterministic: 41 of 41 reproduced rows match exactly, under Verilator 5.050 against the receipt's 5.052.

I recomputed the published maxima independently from the receipt's 96 rows, taking the maximum over every arm:

| Point | Worst capture | Margin against the 49 ms floor | Distance below 24.5 ms |
|---|---|---|---|
| 8x8 at 50 MHz | 2,430,454 ticks = 24.30454 ms (ON arm) | 2.0161x | 0.19546 ms |
| 1x1 at 50 MHz | 6.60642 ms | 7.4170x | - |
| 8x8 at 100 MHz (non-contract) | 19.79024 ms (OFF arm) | - | - |

STOP was correctly not triggered.

No-traffic timing is graded:

- `run.py:67-68` applies the half-floor limit to every row of every arm.
- `check_nvm_capture.py:97-118` pins it at the exact boundary (2,450,000 passes, 2,450,001 fails).
- My planted grader that exempts OFF from the limit fails the gate ("OFF timing limit was ignored").
- My planted `maximum_ms` that drops OFF fails the gate ("OFF timing omitted from maximum").
- The embedded `ignore-off-timing` control fails as named.

Receipts: `gate_mutations.log`, `gate_mut_ignore-off-timing.log`.

### (2) `scripts/check_nvm_capture.py`

**What it derives:**

- Closed-record bytes and records per shape (`:32-48`). It runs the builder's shape generators into a temporary directory and expands `nvm_shape.inventory`, so the result does not depend on what is materialized.
- The configured CPU and system clocks, read from each shape's yaml.
- SHA-256 of the product firmware and of every harness `.py`/`.cpp` file (`:61-67`).
- A regrade of all 96 rows through the harness's own `grade_rows`, and recomputed per-point maxima and margins (`:74-94`).

**What it reads:**

- `measurements.json` (`measured_for`, rows, summaries, maxima).
- The harness contract clock `recipe.CPU_HZ = 50_000_000` and `HOLD_FLOOR_MS = 49` (`recipe.py:5-6`).

**No compiler or simulation.** With PATH holding only python3 and git, a clean environment, no reachable compiler or simulator, and LiteX and migen not importable, the gate passes. It imports zero LiteX, migen or litedram modules (`receipts/gate_minimal_env.log`). It leaves the tree clean.

**Named controls.** `--mutation bytes`, `records` and `clock` each exit 1 with the input-drift message. `ignore-off-timing` exits 1. The embedded controls also cover configured-clock and system-clock.

**Real-source mutations.** Each was run in a scratch copy; all refuse (`receipts/gate_mutations.log`):

- 8x8 yaml CPU clock 100 to 50 MHz (so #565's reconciliation forces a new measurement, as intended);
- 1x1 yaml CPU clock;
- 8x8 system clock;
- `recipe.CPU_HZ`;
- `nvm_contract` RATE payload 4 to 8 bytes (census 12,634 to 12,638);
- one firmware byte;
- a dropped 8x8 OFF arm;
- one row over the half floor;
- a maximum edited alone;
- `measured_for` edited alone.

**Honest residual.** A self-consistent forgery passes the gate (arm `receipt-consistent-forgery`, rc 0): every row halved, then summaries and maxima recomputed. The gate proves that the receipt is internally consistent and was taken for today's inputs. It cannot prove that a simulation produced the rows. Authenticity rests on review of the recorded hashes and a reproduction like (1). A hold change and a SoC fabric edit are also outside its scope (`receipts/gate_residuals.log`). See S2 and S3.

### (3) Workflow-contract pin (`scripts/ci_events.py`)

**The pin:**

- Recorded name `Capture measurement census and clock gate` at `CARRIER_STEP_LISTS` `:1012-1015`, with canonical script `python3 scripts/check_nvm_capture.py`.
- Position 28, between `NVM record-space gate` and `Saved-state writer gate`, matching `.github/workflows/docs.yml:222-224`.
- Step count 49 to 50 at `:7083,7097,7110,7113,7131,7171` and in the RV32 arms at `:7693`.
- The shifted swap arm is 43/44 at `:7118`.
- Four new dedicated arms at `:7127-7140`: removed, reordered, renamed, `if: false`.

This is consistent with precedents `1576f089` and `5251942a` and stricter than them: the step carries a canonical `run`, like `1576f089`, plus dedicated arms.

**Commands (receipts `ci_events_check.log`, `ci_events_selftest.log`):**

- `--check`: rc 0, 1,655 contract items.
- `--selftest`: rc 0, 2,197 arms. The step is covered by the four `#559` arms plus the generic `carrier-script-407 docs-check step 28` arms (no-op, or-true, append-command, continue-on-error, missing record).

**My independent workflow mutations** (`receipts/workflow_mutations.log`). Each of these is refused by `--check`, naming the step or the count: removed, renamed, `|| true`, argument changed, `continue-on-error`, `if: false`, moved after the writer gate, duplicated.

**Documentation gates.** `docs_check` passes in both modes (Git inventory and `GIT_DIR=/dev/null`). With the locked renderer installed into a disposable scratch target, these pass (`receipts/static_gates.log`):

- em-dash (0 findings over 319 added lines);
- TOC check and anchors;
- doc style;
- doc paths;
- Python and C++ idioms;
- test evidence;
- naming;
- module matrix;
- `git diff --check`.

**Act runner contract gate.** Not run by me: the host act runner and its self-test are outside my allowance. The author's evidence is `author-r3/act-contract-selftest.log`. It stays with the manager (see "Pending manager duties").

**Hosted, exact head** (`receipts/hosted_check_runs.tsv`). All completed success: `docs-check`, `docs-check-no-git`, `full-ci-gate`, `rtl-fast`, `verilator-suites`, `yosys-portability`, `elaborate`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `wire-accountability`, `changes`, Verilator shards 0-4 and Yosys shards 0-3. `Physical gPTP (nightly and manual)` is skipped: a skipped context, not an execution.

- In hosted `docs-check`, runner step 29 `Capture measurement census and clock gate` executed and printed all seven controls and `PASS` (`receipts/hosted_docs_check_capture_step.log`).
- `full-ci-gate` (workflow `rtl-full`) executed "Hold every workflow file to its contract" successfully at this head (`receipts/hosted_full_ci_gate_steps.log`).

### (4) Section 18 and UNRESOLVED 6

`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` carries every required element:

- **50 MHz figures:** `:1557-1581`, and a per-arm table whose every range and margin I recomputed from the rows.
- **The 49 ms floor and its cause:** `:1568-1571`. `KL_nvm_backend.sv:777-780` loads `hold_r` at the accepted ARM, and `:723` expires it on the 50th free-running tick, so the hold lasts between 49 ms plus one cycle and 50 ms.
- **The actual-clock rule:** "Hold sizing uses the writer's actual clock" at `:1560` and `:1747`; "50 MHz is not retired" at `:1644`.
- **#565 pointer:** `:1565` and `:1746`.
- **Traffic statement with numbers:** `:1613-1619`. 0.04300 ms (0.177%) at 8x8, 0.01785 ms (0.271%) at 1x1, and 100 MHz ON 0.78591 ms faster, all verified. The docs honestly report a small measurable increase and state that the offered load is not an established worst-case bound.
- **100 MHz point labelled non-contract:** `:1566`, the table, and `:1745`.
- **Retired model factors named:** `:1640-1644`.

The ARM-to-ATTEST bracket (`firmware.py:72-87` against `milan_baremetal.c` `nvm_capture()`) starts before the ARM strobe and ends after a successful ATTEST. It therefore covers the whole held window, including the ownership reads and `nvm_rec_after()`.

### (5) Test documentation

- **The out-of-sweep exception, with prerequisites (LiteX tree, CPU netlist, pinned RV32 SDK):**
  - `docs/testing/TESTING.md:164-167`, `:172` and `:376-380`;
  - `tb/verilator/README.md:3-5` and `:79-85`;
  - harness README `:137-140`.
- **Consistent with discovery:** `suite_shards.discover_suites` selects only directories with a `Makefile`, and hosted shards are green.
- **Substituted models:** the harness README `:114-130` names clocks and phase, `SDRAMPHYModel` for `A7DDRPHY`, MAC AXIS injection, `LiteSPIPHYModel` flash, the simulated UART, and the disabled BIOS delays.

## Findings

### S1 - SUGGESTION - Docs, Tests

**Where:** `tb/verilator/nvm_capture_cpu/soc.py:105-121`, `tb/verilator/nvm_capture_cpu/README.md:43-45,114-130`, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1564,1648`. The explicit clock override is partial, and that is not stated.

**Evidence:**

- `soc.py` derives the builder artifacts from the unmodified 8x8 yaml (`eb._derive_artifacts`) before it overrides `milan_clk_hz` for `milan_soc` and the simulation clockers.
- `endstation_builder.py:5595` therefore generates `gptp_ucode.hex` with `--clk-hz 100000000`, while the simulated Milan/CPU clock is 50 MHz.
- Against a fully consistent yaml-50 MHz build, the only functional difference is `gptp_ucode.hex` (clock-dependent constants). Firmware headers, BIOS and instrumented firmware are identical (`receipts/override_vs_yaml_route.txt`).
- Measured rows 0-2 of both routes are cycle-identical.

**Impact:** none on the figure of record in what I measured. A reader of "overrides the stale 8x8 configuration explicitly" would assume the whole SoC is the 50 MHz product.

**Suggested outcome:** name this in the README's substitutions, or apply the override before artifact derivation.

**Verification:** the README states it, or `diff -r` of the generated directories shows no clock-dependent difference.

### S2 - SUGGESTION - Robustness, Tests

**Where:** `scripts/check_nvm_capture.py:32-94`, `tb/verilator/nvm_capture_cpu/recipe.py:6`. The gate does not pin the other side of the inequality, or the measured fabric.

**Evidence:**

- In a scratch copy, `T_HOLD_MS_P` 50 to 30 in `KL_nvm_backend.sv:145` leaves the gate green.
- An edit to `sw/litex/milan_soc.py`, the SoC and CDC the copy ran on, also leaves it green (`receipts/gate_residuals.log`).
- `HOLD_FLOOR_MS = 49` is a harness constant, not derived from the RTL.
- The round-2 decision scoped the gate to census and clock, so this is not a defect against the assignment.

**Impact:** a later hold or fabric change could falsify "50 ms is enough" with the gate green. Review of that change is the only guard.

**Suggested outcome:** derive the floor from the backend parameter and the `KL_pp_shadow` binding, or state these residuals in the README's gate section.

**Verification:** a hold-parameter mutation fails the gate, or the README names the residual.

### S3 - SUGGESTION - Docs, Tests

**Where:** `tb/verilator/nvm_capture_cpu/README.md:137-153`. The receipt's authenticity is not something the gate can check, and the README does not say so.

**Evidence:** a self-consistent rewrite of all rows, summaries and maxima passes (`receipts/gate_mutations.log`, arm `receipt-consistent-forgery`).

**Impact:** a reader could take a green gate as proof that the measurement happened.

**Suggested outcome:** one sentence saying that the gate checks consistency and input identity. A new or changed receipt still needs a reviewer reproduction against its recorded BIOS, firmware and netlist hashes.

**Verification:** the README states it.

## Clean lenses

```text
[R324] PASS Conformance - issue #559 acceptance 1-3 and decisions 5828771434/5831090112/5832136947 vs SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1651,1734-1755, measurements.json, BAREMETAL_FIRMWARE.md (50 MHz), receipts/probe_comparison.txt - 50 MHz figure of record with aligned edges, 16 captures per arm, max over every arm 24.30454 ms < 24.5 ms (STOP not triggered), 49 ms floor, 100 MHz non-contract, #565 pointer, retired factors named, 1x1 figure given; 41/41 reproduced rows equal the receipt
[R324] PASS RTL - KL_nvm_backend.sv:145,603-615,723,777-780; KL_pp_shadow.sv:961-973; soc.py:117-121,165-166; sim_main.cpp:127-136; milan_soc dp_params p_MILAN_CLK_FREQ_HZ - hold loads at ARM and expires on the 50th free-running tick (49 ms floor); the backend tick in the harness uses the overridden 50 MHz; CPU edges aligned 5 ns at 50/100 MHz; no product RTL, firmware or yaml change in the diff (git diff a3d795ae..b02af048 --stat)
[R324] PASS Robustness - scripts/check_nvm_capture.py:51-118,153-173 and run.py:51-83 under receipts/gate_mutations.log, gate_residuals.log, gate_minimal_env.log, workflow_mutations.log - fails closed on drift of any census/clock/firmware/harness input, a missing arm, a row over the limit, or an edited summary; runs with no compiler, simulator or LiteX; the workflow step cannot be removed, reordered, renamed, conditioned or swallowed; residuals documented as S2/S3
[R324] PASS Tests - check_nvm_capture.py controls (bytes, records, clock, configured-clock, system-clock, ignore-off-timing, off-time-limit), ci_events.py:1012-1015,7127-7140 plus generic step-28 arms, my planted grader mutations, real-source mutations and the four-arm probe reproduction - every named control fails for its own defect, including OFF timing; ci_events --check 1,655 items and --selftest 2,197 arms pass; hosted docs-check executed the gate at this head
[R324] PASS Docs - TESTING.md:164-167,172,376-380; tb/verilator/README.md:3-5,79-85; nvm_capture_cpu/README.md:1-167; CI_WORKFLOWS.md:1184-1195; SAVED_STATE_SNAPSHOT_OWNERSHIP.md sections 18 and UNRESOLVED 6 - Makefile exception with prerequisites, every substituted model named (S1 suggests one addition), step documented as in the precedents, numbers equal the receipt; docs_check both modes, em-dash, TOC/anchors, style and paths pass
```

## Prior findings on this PR, at this head

| Finding | Severity | Status at b02af048 | Evidence |
|---|---|---|---|
| R324-1 F1: the published worst case is not the maximum; traffic does not contend | MAJOR | RESOLVED | `check_nvm_capture.py:87-94` requires maxima over both arms. Section 18's table and `:1613-1619` give the numbers. The OFF timing limit is enforced and its planted control fails. My reproduction covers the OFF maximum. |
| R324-1 F2: 8x8 margin rests on a 100 MHz CPU | MAJOR | RESOLVED | The figure of record is at the 50 MHz contract clock (`run.py:108-109`, `soc.py:117-121`). 100 MHz is labelled non-contract. #565 is linked. "50 MHz is not retired" (`:1644`). The figure is reproduced. |
| R324-1 F3: Makefile-less directory not documented | MINOR | RESOLVED | `TESTING.md:164-167,376-380` and `tb/verilator/README.md:79-85` |
| R324-1 F4: hold floor is 49 ms | SUGGESTION | ADOPTED | `recipe.py:6`; section 18 `:1568-1571`; README `:6-8` |
| R324-1 F5: relative clock phase | SUGGESTION | ADOPTED | `sim_main.cpp:127-132`; README `:116-121`; round-1 row 0 reproduced at the head |
| R325-1 F1: wrong CPU clock for 8x8 | MAJOR | RESOLVED | as R324-1 F2 |
| R325-1 F2: maximum not over the harness's conditions; contention uncharacterized | MINOR | RESOLVED | as R324-1 F1 |
| R325-1 F3: Makefile-less directory | MINOR | RESOLVED | as R324-1 F3 |
| R325-1 S1: name every substituted model, including UART | SUGGESTION | ADOPTED | README `:114-130`. S1 above adds one item. |
| Void 5832130021: new step not pinned in `ci_events.py` | (voiding defect) | RESOLVED | `--check` and `--selftest` pass; the pin is at `:1012-1015`; count 50; hosted `docs-check` and `full-ci-gate` succeed |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #559 acceptance and the three decisions; section 18 and UNRESOLVED 6; `measurements.json`; `BAREMETAL_FIRMWARE.md`; four-arm probe reproduction | R324-3 | b02af0480d3a3061df24683d522799d1759f7c33 |
| RTL | CLEAN | `KL_nvm_backend.sv` hold and tick; `KL_pp_shadow.sv` binding; `soc.py`, `sim_main.cpp` clocking; override versus yaml route | R324-3 | b02af0480d3a3061df24683d522799d1759f7c33 |
| Robustness | CLEAN (S2 open, non-blocking) | `check_nvm_capture.py`, `run.py`, `ci_events.py` pin; mutation, residual and minimal-environment receipts | R324-3 | b02af0480d3a3061df24683d522799d1759f7c33 |
| Tests | CLEAN (S1-S3 open, non-blocking) | gate controls; `ci_events` check and self-test; workflow mutations; hosted `docs-check` step log; probe rows | R324-3 | b02af0480d3a3061df24683d522799d1759f7c33 |
| Docs | CLEAN (S1, S3 open, non-blocking) | `TESTING.md`; `tb/verilator/README.md`; harness README; `CI_WORKFLOWS.md`; section 18 and UNRESOLVED 6; documentation gates in both modes | R324-3 | b02af0480d3a3061df24683d522799d1759f7c33 |

## Limits

- **8x8 ON maximum not re-simulated.** The 16-capture 8x8 ON arm's maximum (row 10, 24.30454 ms) was not reached in a bounded foreground step. Rows 0-2 were reproduced exactly, and the simulation is deterministic across two routes and two simulator versions, but that one row rests on the receipt. The 8x8 100 MHz arms were not re-simulated. Their maxima were recomputed from the receipt rows.
- **Negative controls not rerun.** The harness's `skip-copy` and `no-traffic` simulation controls were not rerun. The OFF arms I ran exercise the no-traffic firmware path, with zero counters and graded timing.
- **Simulation only.** Physical timing, DDR calibration, board clock phase, Ethernet transport, debounce and silicon memory ordering remain unmeasured, as the docs state (UNRESOLVED 6). Physical calibration NOT RUN. Field skips are not hardware proof.
- **Not run by me:** the host act runner and its self-test, Docker, full parent, protocol-processor, gPTP, Yosys or builder banks, and hardware. The locked Markdown renderer was installed only into a disposable scratch target.
- **Bytecode caches removed.** Gate runs created ignored `__pycache__` directories in the clone and in `protocol-processor`, all created by this session. I removed them. Afterwards, 898 tracked blobs were re-hashed equal to the index with modes intact, index equals HEAD tree `8c9f216b`, `git status --porcelain --ignored` is empty in the superproject and in the three required submodules, and the gitlinks are gptp-processor `e5dcea6e`, protocol-processor `09f9bf38` and verilog-axis `48ff7a7e` (`external` is uninitialised, as cloned). Receipt: `receipts/clone_integrity.log`.

## Pending manager duties

- **Candidate merge validation.** Build and validate the current-dev candidate merge (source base `a3d795ae`, live dev `864b36f5`), including `scripts/check_nvm_capture.py` and `ci_events.py --check` on the merge result. Dev may change the census, the clocks or the `docs-check` step list, which would make the gate or the pin fail by design.
- **Act evidence.** Hosted and act acceptance at the exact head, and the act runner contract self-test.
- **Maintainer disposition.** Record the disposition of S1-S3 and the second positive review under CONTRIBUTING's review bar.
- **Merge authorization.** A maintainer must authorize the merge. Post-merge containment and closing issue #559 follow.

## Receipts

Everything is listed in `MANIFEST.sha256`:

- **Portable scripts:** `probe_env.sh`, `probe_setup.sh`, `probe_step.py`, `probe_edit_50mhz.patch`, `compare_rows.py`, `gate_mutations.sh`, `gate_residuals.sh`, `gate_minimal_env.sh`, `workflow_mutations.sh`.
- **Probe rows:** `receipts/probes/*/{capture.log,simulate.log,build_summary.txt}` and `receipts/probe_comparison.txt`.
- **Gate logs:** `receipts/gate_*.log`, `receipts/ci_events_*.log`, `receipts/workflow_mutations.log`, `receipts/static_gates.log`.
- **Hosted evidence:** `receipts/hosted_*`.
- **Route difference:** `receipts/override_vs_yaml_route.txt`.
- **Environment:** `receipts/environment.txt`.
- **Integrity and ordering:** `receipts/clone_integrity.log` and `receipts/independent_verdict_before_prior_findings.txt`.

R324-3 FINISHED
