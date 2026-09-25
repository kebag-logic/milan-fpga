[R325] POSITIVE - exact head b02af0480d3a3061df24683d522799d1759f7c33

# R325-3: external review of PR #564 (issue #559), round 3

Reviewer: [R325], external, in a cleared context. Head `b02af0480d3a3061df24683d522799d1759f7c33`, tree `8c9f216b462e2f0fd7b8da9c73e3f817a8555d32`, source base `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`. Delta reviewed: `32076148..b02af048` (round 2 `31808e65` and round 3 `b02af048`), read against the whole PR diff `a3d795ae..b02af048`.

## Verdict summary

- **No BLOCKER, MAJOR or MINOR finding is open.** There are two SUGGESTIONs (S1, S2). They are optional and do not affect lens coverage.
- **All five lenses are covered clean at this exact head.**
- I reran my own 50 MHz probe unchanged at this head: both shapes, traffic ON and OFF, 16 captures each, aligned edges. **All 64 rows match `measurements.json` exactly, field for field.**
  - The 8x8 maximum over both arms is **24.30454 ms**, the published figure. That leaves 0.19546 ms under the 24.5 ms STOP line, with a 2.0161x margin against the 49 ms floor.
  - The 1x1 maximum is **6.60642 ms** (7.4170x).
  - STOP did not trigger.
- `scripts/check_nvm_capture.py` does what the round-2 decision asks:
  - It needs no compiler, simulator or LiteX. It passes with only `python3` and `git` on PATH.
  - Its named bytes, records and clock controls each exit 1. So does the planted grader that ignores OFF timing.
  - It also fails closed on real source edits: either yaml clock, the harness contract clock, a contract payload constant, the product firmware, or any harness file.
- The `ci_events.py` pin of the new step matches the precedents and goes further than them. `--check` passes 1,655 items and `--selftest` passes 2,197 arms. Nine further mutations of my own are each refused by name.
- Hosted `docs-check` is green at this head. Its step list shows the capture gate, the CI contract gate and the act-runner self-test executed and passed.
- Every prior public finding on this PR (R325-1 F1-F3 and S1, R324-1 F1-F5) is resolved at this head. The table is below.

## Reconstruction

I read these in the order AGENTS.md section 6 sets:

1. AGENTS.md and CONTRIBUTING.md sections 2-3, then `docs/README.md`.
2. Issue #559: body, the Ready decision `5828771434`, the round-2 decision `5831090112`, the round-3 decision `5832136947`, and the executor comments `5830200540`, `5831802889` and `5832296849`.
3. The void notice `5832130021` and the review start `5832318171`.
4. The requirement and interface authorities:
   - `docs/integration/BAREMETAL_FIRMWARE.md:43`, the 50 MHz clock contract.
   - `hdl/milan/KL_nvm_backend.sv:145,603-615,723,777-780`, the hold.
   - `hdl/milan/milan_datapath.sv:7396` into `KL_pp_shadow.sv:962`, the hold's clock parameter.
   - `sw/litex/milan_soc.py:3980`, the writer's constants from `nvm_shape.firmware_constants`.
5. The diff and history, including the precedent commits `1576f089` and `5251942a`.
6. The executable evidence, including the author packets `author-r2` and `author-r3` in archive `c73f1dc8`.

I read prior public review findings only after my own pass and a provisional ledger.

## Assigned verification items

### (1) 50 MHz re-measurement, maximum over every arm, OFF timing graded

- **Probe.** `scripts/r325_head_probe.sh` is my round-2 probe with only its head constant changed (it now checks `b02af048`). It builds with the head harness unchanged and grades with `run.py`'s own `_grade`. `scripts/r325_sim_all.sh` runs the four simulations.
- **Identity.**
  - The CPU netlist `VexiiRiscvLitex_f5f08b17...` hashes to `c208df0b...`, the receipt value.
  - The instrumented firmware hashes are `368eb10b...` (ON) and `040b8450...` (OFF).
  - The `bios.bin` hashes are byte-identical to the receipt in all four arms (`receipts/build-identity.txt`). The compiled image is therefore the author's, even though my local compiler build differs (see limits).
  - The simulator is Verilator 5.052, as the receipt records.
  - The sim top carries `MILAN_CLK_FREQ_HZ=50000000`, so the backend's millisecond tick is derived from the simulated clock.
- **Results** (`receipts/compare_rows_50mhz.txt`, `receipts/sims/`). Every row is identical to the receipt in all ten fields.

  | Arm | Rows identical | Min ms | Max ms |
  |---|---|---|---|
  | 8x8 50 MHz ON | 16/16 | 24.29322 | 24.30454 |
  | 8x8 50 MHz OFF | 16/16 | 24.25516 | 24.26154 |
  | 1x1 50 MHz ON | 16/16 | 6.59822 | 6.60642 |
  | 1x1 50 MHz OFF | 16/16 | 6.58554 | 6.58857 |

  - The 8x8 maximum over both arms is 24.30454 ms. It equals the published maximum and the author-r2 capture logs row for row (`receipts/author-r2-vs-r325-3-rows.txt`).
  - Each run returned rc 0 from the simulator, and `run.py`'s grader passed it.
  - The OFF arms have zero requests, responses and reads in every row.
- **Simulator cross-check.** The 1x1 ON arm rebuilt with the CI-pinned Verilator 5.050 (identity verified: `Verilator 5.050 2026-07-01 rev v5.050`) reproduces all 16 rows exactly (`receipts/compare_rows_verilator5050_1x1_on.txt`).
- **100 MHz point.** I did not rerun it this round; it is non-contract. My R325-1 probe at `32076148` gave OFF 1,979,024 and 1,978,694 cycles and ON 1,899,620 and 1,899,632. Those are inside or equal to the receipt's 100 MHz rows, and at 100/100 MHz the new edge offset is zero.
- **OFF timing is graded.**
  - `run.py:67` applies the 24.5 ms limit to both arms, and `run.py:78-83` requires both arms in the maximum.
  - I planted four grader defects (`receipts/grader_mutations.log`). Each one fails in the gate's embedded controls, before any hash check:
    - skipping the OFF limit: "OFF timing limit was ignored";
    - an ON-only maximum: "OFF timing omitted from maximum";
    - a limit one tick looser: fails;
    - the old 25 ms limit: fails.
  - `--mutation ignore-off-timing` exits 1.

### (2) `scripts/check_nvm_capture.py`

- **What it derives.**
  - For each shape it runs the builder and AEM image generator into a temporary directory. It expands `nvm_shape.inventory` into records and sums `REC_HDR + payload` bytes (`:32-48`). `milan_soc.py:3980` builds the product writer's constants from the same `nvm_shape` module.
  - It reads `milan_clk_hz` and `sys_clk_hz` from the shape yaml.
  - It hashes the product firmware and every `.py` and `.cpp` file in the harness.
  - It regrades every receipt row with `run.grade_rows` and recomputes each maximum over both arms.
- **What it reads.**
  - `measurements.json`: the measured-for census and clocks, rows, maxima and hashes.
  - `recipe.CPU_HZ`, the contract clock constant. It is not derived from product source. It is pinned through `measured_for.cpu_hz` and the harness hash.
- **No compiler or simulation.** With PATH holding only `python3` and `git`, and `gcc`, `cc`, `verilator`, `riscv32-linux-gcc` and `make` all absent, it passes and imports no LiteX, migen, litedram or litespi module (`receipts/gate_python_only_path.log`). It does need `git` and PyYAML, both present on hosted runners.
- **Named controls** (`receipts/gate_*.log`).
  - The plain run passes.
  - `--mutation bytes`, `records`, `clock` and `ignore-off-timing` each exit 1 with the matching message.
  - The embedded controls also cover the configured-clock and system-clock inputs, the exact 24.5 ms boundary, and one tick over it.
- **Real source edits** (`receipts/gate_input_probes.log`). Each of these exits 1 with the correct reason:
  - the 8x8 yaml CPU clock set to 50 MHz;
  - the 8x8 yaml system clock changed;
  - `recipe.CPU_HZ` set to 40 MHz;
  - `nvm_contract.PAY["SUID"]` plus one (census 12,635 and 3,219);
  - one byte appended to the product firmware;
  - one byte appended to `soc.py`.

  A yaml edit the builder rejects fails through an uncaught `CalledProcessError`. That still gives rc 1.
- **The honest residual.**
  - The gate binds inputs to the receipt, not the receipt to a simulation. A yaml CPU clock change plus a matching `configured_cpu_hz` edit in `measurements.json` **passes with no measurement** (arm `RESIDUAL-yaml-clock-40MHz-plus-receipt-edit`, rc 0).
  - Faking a census change is harder. It needs edits to `run.py:55`'s hard-coded census, the harness hashes, the receipt rows, and the gate's own fixture. Without the fixture edit, my attempt failed in the embedded control.
  - Edits to the product RTL, the SoC integration and `nvm_shape.py` are not gated (the `UNGATED-*` arms, rc 0). The round-2 decision scoped the gate to census and clock. See S1.

### (3) The `ci_events.py` pin of the new step

- **Pin and position.** `scripts/ci_events.py:1012-1015` pins the step name `Capture measurement census and clock gate` and the single canonical line `python3 scripts/check_nvm_capture.py`.
  - It sits between `NVM record-space gate` and `Saved-state writer gate`, which puts it at step 28 of 50. `.github/workflows/docs.yml:222-224` agrees.
  - Hosted job step 29 is the same step: the hosted listing counts `Set up job` as step 1.
- **Counts and arms.**
  - The 49-to-50 count changes appear at every arm that states it, and `_carrier_script_edits` agrees.
  - The swap and rename arms moved from 42/43 to 43/44 because the new step shifts them.
  - Four new arms cover removal, reordering, renaming and `if: false` (`:7129-7140`).
- **Against the precedents.** `1576f089` and `5251942a` pinned their steps with the count and the canonical record alone. This change does that and adds step-specific arms.
- **My mutations** (`receipts/workflow_mutations.log`). Each is refused with a message naming step 28:
  - appending `|| true`;
  - appending `--mutation bytes`;
  - adding `continue-on-error`;
  - adding `if: always()`;
  - swapping in another script;
  - an appended command;
  - `set +e`;
  - a `shell:` override;
  - a step-level `BASH_ENV`.
- **Local runs at this head.**
  - `ci_events.py --check` passes 1,655 items; `--selftest` passes 2,197 arms, and the four `#559` arms are caught (`receipts/ci_events_*.log`).
  - `docs_check.py` reports 0 findings in both modes: git, and `GIT_DIR=/dev/null` with the expected inventory-parity skip.
  - I did not run `act_ci.py --selftest` on the host. My assignment excludes it; hosted evidence covers it.
- **Hosted at this head** (`receipts/hosted-check-runs.txt`, `receipts/hosted-docs-check-steps.txt`).
  - `docs-check` concluded success, and its `head_sha` is the exact head. All 55 steps succeeded, including step 29 (the capture gate), step 43 `CI event and SHA contract gate` and step 44 `Local act runner contract gate`.
  - `full-ci-gate` concluded success. It is the contract and decision preflight job, and its "Hold every workflow file to its contract" step passed.
  - `docs-check-no-git`, `rtl-fast`, `elaborate`, `yosys-elaboration`, `verilator-lint`, all four Yosys shards and all five Verilator shards succeeded. Shard 4/5 completed at 13:07:03 UTC. At my final poll at 13:08 UTC, 21 contexts were successful and 1 skipped.
  - `Physical gPTP` is skipped (nightly and manual only). That is a skip, not a pass.

### (4) Section 18 and UNRESOLVED 6

All in `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`.

- **Clock.** `:1560` restores "**Hold sizing uses the writer's actual clock.**", and `:1644` says "50 MHz is not retired". The 50 MHz contract clock, the aligned edges and the explicit override are stated. `:1565` and `:1746` point to #565, and `:1566` and `:1745` label the 100 MHz point non-contract.
- **Floor.** `:1569-1571` gives the 49 ms floor and why the first tick can arrive immediately after ARM. That matches `KL_nvm_backend.sv:777-780` (`hold_r` loads 50 at ARM and counts free-running ticks) and `:723` (it expires on the 50th tick).
- **Figures.** Every figure in the table at `:1582-1590` matches the receipt and my rows: ticks, milliseconds and margins. So do the 24.30454 ms maximum, 2.0161x, 0.19546 ms and 7.4170x.
- **Traffic.** `:1613-1619` states the traffic effect with numbers: 8x8 ON exceeds OFF by 0.04300 ms (0.177%), 1x1 by 0.01785 ms (0.271%), and at 100 MHz ON is 0.78591 ms faster. I recomputed each from the receipt.
  - The decision's wording expected "does not measurably lengthen". The page says "small but measurable" because a deterministic simulation does show a +0.18% difference. Reporting the numbers rather than the literal phrase is the truthful reading. It also satisfies R324-1 F1's alternative, and the page adds that no contention bound is established.
- **UNRESOLVED 6** (`:1734-1755`) carries the same figures, the floor, the #565 pointer, the gate's conditions and the retired model factors.

### (5) TESTING.md and `tb/verilator/README.md`

- **TESTING.md.**
  - `:164-167` names `nvm_capture_cpu` as the environment-dependent exception, outside local and hosted sweeps, and lists its prerequisites: the LiteX tree, the CPU netlist and the pinned RV32 SDK.
  - `:172` excludes it from the default driver.
  - `:376-381` states the Makefile exception and the compiler-free gate.
- **`tb/verilator/README.md`.** `:4-5` and `:79-85` say the same.
- **Discovery.** `scripts/suite_shards.py` selects only directories with a Makefile. It selects 55 of the 57 directories: `nvm_capture_cpu` has no Makefile and `milan_dp_gptp` is scheduled separately.
- **Substituted models.** The harness README's substitutions list (`:114-131`) names every substituted model:
  - clocks and their phase: ideal signals, aligned rising edges, a 5 ns offset at 50/100 MHz, audio clocks at their half-periods;
  - `SDRAMPHYModel` for `A7DDRPHY`;
  - MAC transport: direct AXIS injection, always-ready TX;
  - `LiteSPIPHYModel` for the flash device;
  - the UART console, with no baud-rate backpressure;
  - disabled BIOS delays;
  - the simulator version (`:133`).
- **Path gates.** The documentation gates in `receipts/doc_gates.log` all return 0 at this head (em-dash, style, TOC, anchors, doc paths, idiom ratchets, `git diff --check`). For TOC and anchors I used the locked Markdown requirements; the first system-Python attempt refused because a renderer dependency was absent, which is an environment refusal and not a finding.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Docs, Robustness - `tb/verilator/nvm_capture_cpu/README.md:146-153`; `scripts/check_nvm_capture.py:58-68` - state what the input gate does not bind

- **Evidence** (`receipts/gate_input_probes.log`).
  - A matching edit to `measurements.json` satisfies the gate with no measurement: arm `RESIDUAL-yaml-clock-40MHz-plus-receipt-edit`, rc 0.
  - Edits to the product RTL (`hdl/milan/KL_pp_shadow.sv`), the SoC integration (`sw/litex/milan_soc.py`) and `scripts/nvm_shape.py` pass: the `UNGATED-*` arms, rc 0.
  - LiteX component revisions and the CPU netlist are recorded in the receipt but not checked.
  - README `:152` says "Harness hashes prevent carrying evidence across measurement-path changes". A reader can take the product path as included, but the hashes cover only the harness directory.
- **Impact.** Nothing false is published. Section 18 says the remedy holds "only while measured inputs remain unchanged", and the round-2 decision scoped the gate to census and clock. With 0.19546 ms of headroom, though, a latency change on the CPU-to-DDR path is the likeliest way to cross 24.5 ms, and nothing flags it except review.
- **Suggested outcome.** One or two README sentences saying:
  - the gate trusts the receipt;
  - RTL, SoC integration, LiteX revisions and the CPU netlist are not bound;
  - a change there needs review judgement or a re-measurement.
- **Verification.** Read the README text.

### S2 - SUGGESTION - Tests - `tb/verilator/nvm_capture_cpu/run.py:62-66`; `scripts/check_nvm_capture.py:97-145` - no compiler-free control for the traffic-counter oracle

- **Evidence** (`receipts/grader_mutations.log`). Removing the ON-arm "all counters positive" or the OFF-arm "all counters zero" check fails only through the harness hash ("measurement harness changed"), not through a named control. The simulation-side `--mutation no-traffic` and `skip-copy` controls do cover them, but those need the full environment.
- **Suggested outcome.** Add fixture rows to `timing_controls()` with nonzero OFF counters and zero ON counters, and require `grade_rows` to refuse each.
- **Verification.** Each planted counter-oracle removal fails in the embedded control.

## Prior public findings at this head

| Prior finding | Status at `b02af048` | Evidence |
|---|---|---|
| R325-1 F1 MAJOR (8x8 figure at an unestablished 100 MHz; 50 MHz retired) | RESOLVED | The 50 MHz figure of record is 24.30454 ms and my rerun reproduces it exactly. The clock conflict was published and decided (`5831090112`, #565). Section 18 `:1560,1644` restores the actual-clock rule. The configuration is unchanged by decision. |
| R325-1 F2 MINOR (maximum not over conditions; traffic effect uncharacterised) | RESOLVED | Both arms, 16 captures each; the maximum is taken over both (`maximum_ms`, receipt `maxima`). `:1613-1619` gives the numbers. |
| R325-1 F3 MINOR (Makefile-less dir undocumented) | RESOLVED | `TESTING.md:164-167,172,376-381` and `tb/verilator/README.md:4-5,79-85` |
| R325-1 S1 SUGGESTION (name UART and simulator) | ADOPTED | README `:128,133` |
| R324-1 F1 MAJOR (worst case not over arms; OFF timing ungraded) | RESOLVED | OFF timing is graded at `run.py:67`. The planted grader controls fail (my item 1 probes). Traffic numbers are stated. |
| R324-1 F2 MAJOR (100 MHz premise) | RESOLVED | As R325-1 F1 |
| R324-1 F3 MINOR (Makefile, sweep) | RESOLVED | As R325-1 F3 |
| R324-1 F4 SUGGESTION (49 ms floor) | ADOPTED | `:1569-1571`; margins are stated against 49 ms |
| R324-1 F5 SUGGESTION (clock phase) | ADOPTED | Aligned edges at `sim_main.cpp:127-132,165-167`; README `:116-121` |
| Round-2 void (step not pinned) | RESOLVED | Item 3 |

## Per-lens results

```text
[R325] PASS Conformance - issue #559 decisions 5828771434/5831090112/5832136947 vs SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1653,1734-1755, measurements.json, scripts/check_nvm_capture.py, scripts/ci_events.py:1012-1015 - 50 MHz figure of record with aligned edges, max over both arms, 49 ms floor, STOP not triggered (24.30454 <= 24.5), gate fails on bytes/records/clock, yaml untouched with #565 pointer, round-3 pin per 1576f089/5251942a; reproduced 64/64 rows
[R325] PASS RTL - hdl/milan/KL_nvm_backend.sv:603-615,723,777-780; milan_datapath.sv:7396; tb/verilator/nvm_capture_cpu/sim_main.cpp:124-167; soc.py:117-121; generated sim.v MILAN_CLK_FREQ_HZ=50000000 - hold floor 49 ms from ARM to ATTEST, tick derived from the simulated clock, CPU rising edges coincide with sys rising edges (5 ns offset at 50/100, 0 at 100/100), integer-ps scheduling monotonic and overflow-safe for 30 s; no product RTL change in the PR
[R325] PASS Robustness - scripts/check_nvm_capture.py against real edits (receipts/gate_input_probes.log), workflow step mutations (receipts/workflow_mutations.log), run.py:51-83 boundary (24.5 ms accepted, +1 tick refused) - fails closed on every input edit including smaller copies and faster clocks; builder refusal still exits 1; residuals recorded as S1
[R325] PASS Tests - receipts/compare_rows_50mhz.txt, receipts/compare_rows_verilator5050_1x1_on.txt, receipts/grader_mutations.log, receipts/gate_*.log, receipts/ci_events_selftest.log - every named control can fail and does fail for its defect; four planted grader defects caught by embedded controls; ci_events 2197 arms including 4 new; measurement reproducible across Verilator 5.052 and 5.050; S2 is optional hardening
[R325] PASS Docs - SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1653,1734-1755; docs/testing/TESTING.md:164-172,376-381; tb/verilator/README.md:4-5,79-85; tb/verilator/nvm_capture_cpu/README.md:114-133,137-167; docs/testing/CI_WORKFLOWS.md:1184-1195 - every figure recomputed from the receipt; clock/floor/#565/non-contract/traffic statements present and true; Makefile exception with prerequisites; every substituted model named; docs_check both modes, em-dash, style, TOC, anchors, paths green
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue decisions; section 18 and UNRESOLVED 6; `measurements.json`; `check_nvm_capture.py`; `ci_events.py:1012-1015,7129-7140`; `docs.yml:222-224`; 64 re-measured rows | R325-3 | `b02af0480d3a3061df24683d522799d1759f7c33` |
| RTL | CLEAN | `KL_nvm_backend.sv` hold; `milan_datapath.sv:7396`; `sim_main.cpp` clock scheduler; `soc.py` override; generated sim top clock parameter | R325-3 | `b02af0480d3a3061df24683d522799d1759f7c33` |
| Robustness | CLEAN | Gate against real input edits and residual arms; 9 workflow mutations; limit boundary | R325-3 | `b02af0480d3a3061df24683d522799d1759f7c33` |
| Tests | CLEAN | Row comparisons (5.052 and 5.050); grader mutations; gate controls; `ci_events --check/--selftest`; hosted `docs-check` steps | R325-3 | `b02af0480d3a3061df24683d522799d1759f7c33` |
| Docs | CLEAN | Section 18 and UNRESOLVED 6; `TESTING.md`; `tb/verilator/README.md`; harness README; `CI_WORKFLOWS.md`; doc gates in both modes | R325-3 | `b02af0480d3a3061df24683d522799d1759f7c33` |

SUGGESTIONs S1 and S2 are optional and do not affect coverage.

## Receipts (listed in MANIFEST.sha256)

- **Scripts.** Each is portable and takes the clone and scratch paths as arguments:
  - `scripts/r325_head_probe.sh`, `scripts/r325_sim_all.sh`: build and simulate the probe arms;
  - `scripts/r325_compare_rows.py`: compare rows with the receipt;
  - `scripts/r325_gate_input_probes.sh`, `scripts/r325_grader_mutations.sh`, `scripts/r325_workflow_mutations.sh`: the mutation probes;
  - `scripts/r325_clone_integrity.sh`: the clone check.
- **Measurements.**
  - `receipts/sims/`: the four capture logs, grader outputs and rcs, the reduced `sources.json` clock specs, the Verilator identities, and the 5.050 1x1 run.
  - `receipts/compare_rows_50mhz.txt`, `receipts/compare_rows_verilator5050_1x1_on.txt`, `receipts/build-identity.txt`, `receipts/probe-environment.txt`, `receipts/author-r2-vs-r325-3-rows.txt`.
- **Gate and contract.**
  - `receipts/gate_{none,bytes,records,clock,ignore-off-timing}.log`, `receipts/gate_input_probes.log`, `receipts/gate_python_only_path.log`, `receipts/grader_mutations.log`.
  - `receipts/ci_events_check.log`, `receipts/ci_events_selftest.log`, `receipts/workflow_mutations.log`, `receipts/doc_gates.log`, `receipts/readme_literal_path.log`.
- **Hosted and clone.** `receipts/hosted-check-runs.txt`, `receipts/hosted-docs-check-steps.txt`, `receipts/hosted-full-ci-gate-steps.txt`, `receipts/clone-integrity.txt`.

## Real limits

- **Simulation only.** These are simulation measurements with ideal clocks. They cover one deterministic phase (aligned edges), a DDR PHY model and MAC-boundary traffic injection. Physical timing, DDR calibration, board memory ordering and debounce are unmeasured. Physical calibration was NOT RUN, and skipped field or physical jobs are not hardware proof.
- **Compiler.** My builds used a local Buildroot `riscv32-linux-gcc` 14.3.0, not the pinned bootlin 2025.08-1 archive the author and CI use. This is immaterial here: every `bios.bin` is byte-identical to the receipt. `receipts/readme_literal_path.log` records that my local toolchain ships its own `python3` and `meson`, so I kept the LiteX interpreter first on PATH. The pinned archive has no `python3`, so the README's "SDK bin first" is not a defect.
- **Not rerun this round.** I did not rerun the 100 MHz non-contract rows or the harness's simulation-side `skip-copy` and `no-traffic` controls. The former I checked against my R325-1 probe values.
- **Execution note.** The 8x8 simulations each run longer than a single foreground command allows. I launched the four simulations and the 5.050 check detached and waited on them in consecutive foreground polls until each finished (rc 0 recorded). No job was left running.
- **Not run by me.** Excluded by my assignment: `act_ci.py --selftest` on the host (the hosted `docs-check` step 44 ran it), the full builder, parent, PP, gPTP and Yosys banks, and Docker or act.
- **Clone.** The review clone was never edited. I removed the ignored `__pycache__` directories my runs created. `receipts/clone-integrity.txt` then proves:
  - HEAD and tree are the exact ids;
  - the index equals the HEAD tree, with every record at stage 0 and no assume-unchanged or skip-worktree flags;
  - all 898 tracked files hash from disk to their blobs, with correct modes;
  - the submodule gitlinks match (`gptp-processor` `e5dcea6e`, `protocol-processor` `09f9bf38`, `third_party/verilog-axis` `48ff7a7e`), with clean worktrees;
  - `external` was uninitialised at the start and is unchanged.

## Pending manager duties

- Hosted acceptance at the exact head. At my final poll, every context had concluded: 21 successful and `Physical gPTP` skipped.
- The act-first local replica and its acceptance.
- The current-dev candidate merge build and validation: source base `a3d795ae`, live dev `864b36f5`.
- Post-merge containment.
- The second positive review (internal lane).
- Maintainer merge authorisation.
- Issue closure and board state.
- #565 (8x8 configuration clock reconciliation) remains open. When it changes the 8x8 yaml clock, this gate will fail as designed and require re-measurement.

R325-3 FINISHED
