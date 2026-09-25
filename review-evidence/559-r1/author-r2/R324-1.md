[R324] NEGATIVE - exact head 32076148acb0b9122e8c92a44f8e2ebbc8169280

Round R324-1, internal independent review of issue #559 / PR #564 (executor [A307]).
Head `32076148acb0b9122e8c92a44f8e2ebbc8169280`, tree `1d25c86b6a9c2577103d27ecbfb6e1e686772518`, source base `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`.
All five lenses were applied. Two MAJOR findings, one MINOR and two SUGGESTIONs are open, so every lens is UNCLEAN at this head.

## Summary

The harness is real and it reproduces. The CPU is the board's cacheless RV32I VexiiRiscv (netlist sha256 `c208df0b...`, the same as the receipt). The buses are the product `MilanSoC` buses. The timed interval brackets ARM through a successful ATTEST, including every `nvm_rec_after()` walk. I rebuilt the unmodified head through the PR's own harness functions and got the author's 8x8 capture 0 to the cycle: 1,899,620 system cycles, with the same traffic counts (237,330 / 146 / 5,694).

The retained remedy, "50 ms is enough", survived every arm I ran. The published figure and margin did not:

| Arm (8x8, 2 captures, PR harness) | Max ms | 50 ms / max | Share of 25 ms bar |
|---|---|---|---|
| CPU 100 MHz, traffic ON (control, unmodified head) | 18.99632 | 2.6321x | 76.0% |
| CPU 100 MHz, traffic OFF (harness `no-traffic` arm) | **19.79024** | **2.5265x** | 79.2% |
| CPU 50 MHz, traffic ON | 24.15248 | 2.0702x | 96.6% |
| CPU 50 MHz, traffic OFF | 24.15108 | 2.0703x | 96.6% |
| CPU 50 MHz, traffic ON, CPU edges aligned to sys edges as on the PLL | **24.29902** | **2.0577x** | **97.2%** |

- **F1.** The traffic arm does not contend. At the documented 100 MHz configuration the copy is 4.18% *slower* without traffic. So the published "worst" (19.00433 ms, 2.6310x) is not the worst copy the harness produces.
- **F2.** The 8x8 figure depends on a 100 MHz CPU clock. That value comes from a yaml line that predates the cacheless-CPU clock split. The authoritative bare-metal contract says the cacheless CPU runs at 50 MHz, and no 8x8 closure with the CPU at 100 MHz is evidenced. At 50 MHz the copy is 24.15 to 24.30 ms. That still meets the 25 ms bar, but with 2.8% headroom rather than 24%.
- The expected "about 38 ms at 50 MHz" is refuted by measurement. The copy is dominated by system-domain DDR and ROM latency, not CPU cycles, so halving the CPU clock adds 27%, not 100%.

## Reconstruction

- **Order read.** First AGENTS.md, CONTRIBUTING.md (sections 3 and 6), docs/README.md and docs/testing/TESTING.md section 1.1. Then the issue #559 body and its comments: the [A10] assignment (comment 5828771434), [A307] TAKEN and [A307] REVIEW READY. Then `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 18, 19 and UNRESOLVED 6, `docs/litex/CLOCK_DOMAINS.md`, `docs/integration/BAREMETAL_FIRMWARE.md`, `KL_nvm_backend.sv`, `KL_pp_shadow.sv`, `milan_datapath.sv`, `sw/litex/milan_soc.py` and both AX7101 shape yamls. Then the diff `a3d795ae..32076148` (one commit, 8 files), the public evidence tree `c16e4aed.../review-evidence/559-r1`, the PR body and the exact-head hosted check runs.
- **Frozen acceptance.**
  1. Measure the 8x8 capture copy on the product firmware.
  2. Choose a remedy with a stated margin.
  3. Update section 18 and UNRESOLVED 6.
- **Assignment decisions.**
  - The route is a cycle-accurate simulation of the product SoC, "the board's cacheless RV32I VexiiRiscv variant and bus, as the board build configures them".
  - `nvm_rec_after` is included in the timed interval.
  - The bar is a worst-case 8x8 copy of at most 25 ms "over repeated captures, with controller traffic running".
  - Remedy order: enough, then a cheaper copy, then a resized hold.
- **Prior public review findings on PR #564.** None. The PR thread holds only the two review-start notices, and there are no PR reviews or line comments. Nothing to resolve or retain.

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs - the published worst case is not the worst copy, and the traffic arm does not contend

- **Where.**
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1561-1562` and the table at `:1582-1592`.
  - `:1702-1707` (UNRESOLVED 6).
  - `tb/verilator/nvm_capture_cpu/run.py:59-71` (`_grade_mutation`).
  - `tb/verilator/nvm_capture_cpu/README.md:44-57`.
  - `tb/verilator/nvm_capture_cpu/measurements.json`.
- **Authority.** The assignment's bar is the worst case over repeated captures with controller traffic running. That premise treats traffic as the stressing condition. Section 18 calls 19.00433 ms "the maximum" and derives "about 2.6310x hold margin". CONTRIBUTING section 3 says "Measure, don't assume".
- **Evidence.**
  - `receipts/probes/b8x8_100_nt`, the harness's own `--mutation no-traffic` arm at the documented 8x8 configuration: 1,979,024 and 1,978,694 system cycles (19.79024 ms).
  - `receipts/probes/b8x8_100`, the traffic-ON control on the unmodified head: 1,899,620 and 1,899,632. The traffic-OFF copy is 4.18% longer, and 4.14% above the published maximum.
  - At 50 MHz, traffic ON and OFF differ by under 0.01% (`b8x8_50`, `b8x8_50_nt`).
  - The public 1x1 control (`receipts/public_1x1_no_traffic_control.txt`) lies inside the 1x1 traffic-ON range.
  - The traffic does reach the PP and its descriptor reads do share the CPU's memory path. Both use `dma_bus` (`sw/litex/milan_soc.py:3018-3019`), and the NVM windows sit in DDR `main_ram` at `0x7f7ef000` and `0x7f7df000`. But 5,694 eight-byte reads per 1.9 M cycles is about 0.3% duty. The offered load is saturating at the MAC face, about 237k frames accepted per copy, yet only about 146 are answered.
  - `_grade_mutation` grades the no-traffic arm only on zero counters and a correct copy. It never compares elapsed time, so this was never tested.
- **Impact.**
  - The authoritative page presents a traffic-ON figure as the worst case and overstates the margin (2.6310x published, 2.5265x or less observed).
  - "With controller traffic running" reads as a stress condition, but it is not one: the offered traffic does not lengthen the copy, and at 100 MHz it shortens it.
  - A future hold-sizing argument that trusts the traffic arm to bound the copy would be unsound.
- **Required outcome.**
  - The reported worst case and margin are the maximum over every arm the harness runs, at least traffic ON and OFF, at 16 captures each.
  - The harness records and grades the timing of the no-traffic arm, not only its counters.
  - Section 18 and UNRESOLVED 6 state that the offered READ_DESCRIPTOR load does not measurably lengthen the copy, with the numbers. Otherwise they name and measure traffic that does contend on the copy's DDR path.
- **Verification.** Rerun both shapes at 16 captures with traffic ON and OFF. `measurements.json` carries both sets of rows, and the published maximum equals their overall maximum. A planted grading change that ignores the OFF arm's timing must make the harness fail.

### F2 - MAJOR - Conformance, RTL, Robustness, Docs - the 8x8 margin rests on an unestablished 100 MHz CPU clock, contrary to the bare-metal clock contract

- **Where.**
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1568`, "The shape recipes set CPU/system clocks to ... 100/100 MHz at 8x8".
  - `:1607`, "Configured clocks replace the blanket 50 MHz CPU assumption".
  - `:1707`, "At the configured 100 MHz CPU clock ... 2.6310x".
  - `tb/verilator/nvm_capture_cpu/README.md:66`.
  - `tb/verilator/nvm_capture_cpu/soc.py:135,162,171`.
- **Authority.**
  - AGENTS section 2: publish a conflict between documentation and implementation instead of choosing an interpretation privately. AGENTS section 6, RTL lens: clock assumptions must be valid.
  - `docs/integration/BAREMETAL_FIRMWARE.md:43` (build contract): "The cacheless CPU side and the 64-bit Milan plane run at 50 MHz."
  - `docs/litex/CLOCK_DOMAINS.md:101`: "Here, CPU execution is 50 MHz."
- **Evidence** (`receipts/trace.txt`).
  - The 100 MHz line, `configs/endstation_ax7101_8x8.yaml:56`, "single fast domain (AX timing CLOSED)", was introduced at `a94296d4` (2026-07-22). That predates two changes:
    - `1e80a106` (2026-08-19) moved the shipping cacheless core to 50 MHz because "the option-on fabric and cacheless CPU close here".
    - `dfcf83ce` (2026-08-26) made `with_cpu_clk = bool(milan_clk_freq)` unconditional, so every build now clocks the CPU from `milan` (`milan_soc.py:2565,2700`).
  - An 8x8 build today would therefore put the cacheless CPU at 100 MHz, a combination with no closure evidence in the tree. The builder asserts 50 MHz only for the 1x1 (`sw/builder/test_builder.py:3000`).
  - Measured with the PR harness and only the yaml clock changed (`receipts/probes/probe_edit_50mhz.patch`): 24.15248 ms with traffic, 24.15108 ms without. With the CPU's rising edges aligned to sys rising edges, as PLL outputs at zero phase are: 24.29902 ms (`probe_edits_50mhz_phase.patch`).
  - That is 97.2% of the 25 ms bar and a 2.06x hold margin. Against the hold's guaranteed floor (F4), it is 99.2% of half the hold.
  - The hold itself is sized from the live Milan clock (`milan_datapath.sv:7396` into `KL_pp_shadow.sv:962`), so it stays 50 ms at either clock.
- **Impact.**
  - The page retires the 50 MHz CPU assumption for 8x8 on the strength of a stale yaml value that conflicts with the bare-metal contract. It publishes only the favourable-clock margin.
  - At the clock the contract names, the bar is met with 0.70 ms of headroom, and that headroom is within this simulation's stated fidelity limits (fixed phase, 2 captures, physical DDR effects out of scope).
  - The conflict is not published for a decision.
- **Required outcome.**
  - Publish the conflict: the 8x8 yaml at 100 MHz against the bare-metal contract at 50 MHz. Then do one of these:
    - record the 8x8 worst case at a 50 MHz CPU (16 captures, max over F1's arms, with PLL-like edge alignment or a stated phase sweep), and state that margin;
    - cite timing-closure evidence for an 8x8 build with the cacheless CPU at 100 MHz.
  - Section 18 and UNRESOLVED 6 state which clock each figure holds for and why that is the clock the board would run.
- **Verification.** Section 18 carries the 50 MHz figure, or cites the closure evidence. `measurements.json` holds the matching rows and clock. The conflict appears on the issue as a recorded decision.

### F3 - MINOR - Docs, Tests - the new harness directory has no Makefile and TESTING.md does not say it is outside the sweep

- **Where.** `docs/testing/TESTING.md:372-373` and the suite index table. The directory `tb/verilator/nvm_capture_cpu/`.
- **Authority.** TESTING.md section 1.1, "reconciled against the tree", says "Every directory needs a `Makefile`; only `milan_dp_gptp` runs separately."
- **Evidence.** The directory has no Makefile. `scripts/suite_shards.py:48-55` silently skips it: 55 suites are selected and the harness is not one of them (`receipts/trace.txt`). It is not in the index, and nothing in TESTING.md names it as a manual harness or lists its prerequisites (the product LiteX set, the pinned RV32 SDK, a cached or offline-generated CPU netlist).
- **Impact.** The testing authority is now false about the tree, and a reader of the suite index cannot find the measurement harness or learn why hosted CI does not run it.
- **Required outcome.** TESTING.md states that the harness is a manual measurement outside the default and hosted sweep, why (its dependencies), and where its command and receipt live. Alternatively, amend the Makefile rule to admit it.
- **Verification.** `scripts/docs_check.py` and `check_doc_paths.py` stay green, and the page names `tb/verilator/nvm_capture_cpu`.

### F4 - SUGGESTION - Docs, RTL - the hold's guaranteed floor is 49 ms, not 50 ms

- **Where.** `hdl/milan/KL_nvm_backend.sv:603-615,723,777-780`. Margins in section 18 and UNRESOLVED 6.
- **Evidence.** `hold_r` loads 50 at ARM and counts free-running millisecond ticks. The first tick can come one cycle after ARM and expiry fires on the 50th tick, so the hold lasts between 49 ms plus one cycle and 50 ms. Half the guaranteed hold is 24.5 ms. That matters only at the 50 MHz figure of F2.
- **Suggested outcome.** State margins against the guaranteed floor, or state the 1 ms tick granularity.

### F5 - SUGGESTION - Tests, Docs - the simulated relative clock phase at 50/100 MHz is not the board's

- **Where.** `tb/verilator/nvm_capture_cpu/sim_main.cpp:124-127,161-162`. `README.md:35-36,98`.
- **Evidence.** Every clock first rises at half its period. At 50/100 MHz that puts the CPU's rising edges on sys falling edges, while the board PLL aligns rising edges. The measured effect at 8x8 and 50 MHz is +0.61% on silicon-like alignment (`b8x8_50_phase` against `b8x8_50`). At 100/100 MHz the sim edges already coincide. The published 1x1 figure (7.6x margin) is immaterially affected.
- **Suggested outcome.** The README names this as a substitution. If F2 adopts a 50 MHz figure, it uses aligned edges or states the phase.

## Assigned focus questions

1. **Which CPU, bus and substitutions?** The CPU is VexiiRiscv, `cpu_variant` `baremetal` (the product patch in the LiteX set), `xlen` 32, one hart, `with_cpu_clk` True, `with_dma` True, `l2_bytes` 0. Its netlist sha256 matches the receipt, and it is not NaxRiscv (`soc.py:131-152`, `receipts/probes/*/cpu_netlist.txt`). The buses are the product `MilanSoC`, including `cross_cpu_memory_ports`, the PP `desc`, `resp` and `nvm` masters on `dma_bus`, the LiteDRAM controller with MT41J256M16 timings, and the LiteSPI controller. Code runs from ROM and data sits in SRAM, while the NVM windows are in DDR, so each copied byte is one uncached DDR read and one DDR write through the CPU memory CDC. The substitutions:
   - **Clocks.** `_CRG` becomes ideal `SimClocks`. At 100/100 MHz the phase matches the board. At 50/100 MHz the sim is optimistic by 0.61% (F5).
   - **DDR.** `A7DDRPHY` becomes `SDRAMPHYModel` with the board PHY's `read_latency`, `write_latency`, `rdphase`, `wrphase`, CL and CWL. The model applies both latencies (`litedram/phy/model.py:640-676`), and the controller-side bank and refresh timing is unchanged. Leveling is off and physical DDR is not modelled. I found no way for this model to return data faster than the board PHY's controller-facing latency.
   - **SPI flash.** The flash device is `LiteSPIPHYModel`. It is read only in the prefill, before the timer starts.
   - **MAC.** With `with_mac=False`, traffic enters at the datapath MAC AXIS with no inter-frame gap and TX always ready. That is heavier than line rate, and the MAC owns no DDR port, so no DDR master is removed.
   - **BIOS.** Delays, CRC and memtest are disabled. All of that happens before the capture.
2. **Is the timed interval right?** Yes. The timer starts after `nvm_prefill_stage()` and the poison loop, immediately before the ARM strobe (`firmware.py:74-79`). It stops after the ATTEST readback succeeds (`:84-85`). The interval includes the ownership reads, every `nvm_rec_after()` call and the fence. The backend hold starts at `arm_ok_w` and ends at `attest_w`, inside the timed interval. `timer0` is the 100 MHz system timer (`CAPTURE_BOOT ... sys_hz=100000000`). It is a downcounter read as start minus end, with no wrap (1.98 M is far below 2^32). `run.py:48` converts `sys_cycles / sys_hz * 1000`, which is correct.
3. **Clock premise.** See F2. The 8x8 figure takes 100 MHz from `configs/endstation_ax7101_8x8.yaml:56` and the 1x1 figure takes 50 MHz from `configs/endstation_ax7101_1x1_tdm8.yaml:44`, through `soc.py:135,162`. The doc does state the clock each figure holds for, but not that the 8x8 clock is unestablished or that it conflicts with the bare-metal contract. At 50 MHz the measured copy is 24.15 to 24.30 ms, not about 38 ms, and it is still below 25 ms.
4. **Does the traffic contend, and is the control real?** Traffic is counted during the copy: requests, responses and descriptor-memory reads are all positive, and responses are checked for the AEM READ_DESCRIPTOR SUCCESS header. It shares the CPU's memory path topologically but does not lengthen the copy (F1). The no-traffic arm is a real control of the counters, zero in both my arms, but it is not a control of timing (F1).
5. **Do the docs replace the model?** Yes, in form. Section 18 replaces the formula and table and names every retired factor: 6 instructions per byte, 50 per record, 10 cycles per instruction, 30 cycles per access, 2 accesses per byte, the 2x penalty, and the blanket 50 MHz. The content is subject to F1 and F2.
6. **Is it runnable, and does hosted CI need an RV32 compiler or LiteX?** It is runnable as documented. With the stated prerequisites I reproduced the author's capture-0 row exactly. It is outside the hosted sweep because it has no Makefile, so hosted CI needs neither an RV32 compiler nor LiteX. `check_py_idiom`, `check_cpp_idiom` and `py_compile` pass on a host without LiteX installed (`receipts/static_gates.log`). TESTING.md does not state any of this (F3).

## Per-lens results (artifact-specific)

```text
[R324] MAJOR Conformance - docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1561-1562,1707 - F1 published worst case is not the harness's worst copy
[R324] MAJOR Conformance - configs/endstation_ax7101_8x8.yaml:56 vs docs/integration/BAREMETAL_FIRMWARE.md:43 - F2 unestablished 100 MHz CPU premise, conflict unpublished
[R324] PASS Conformance - tb/verilator/nvm_capture_cpu/soc.py:131-152 + receipts/probes/*/cpu_netlist.txt - product cacheless RV32I VexiiRiscv (not NaxRiscv), netlist c208df0b equals receipt; firmware.py:72-91 brackets ARM..ATTEST incl. nvm_rec_after (acceptance 1 route, assignment decision 1)
[R324] MAJOR RTL - sw/litex/milan_soc.py:2565,2700 + configs/endstation_ax7101_8x8.yaml:56 - F2 clock assumption for the 8x8 CPU not valid as established
[R324] SUGGESTION RTL - hdl/milan/KL_nvm_backend.sv:603-615,723,777-780 - F4 hold floor is 49 ms
[R324] PASS RTL - hdl/milan/milan_datapath.sv:7396 -> hdl/milan/KL_pp_shadow.sv:962 -> KL_nvm_backend CLK_HZ_P - hold is sized from the live Milan clock; no RTL in the diff (git diff --stat a3d795ae..32076148)
[R324] MAJOR Robustness - receipts/probes/b8x8_100_nt/capture.log vs b8x8_100 - F1 load condition does not stress the copy; worst case lies in the unloaded arm
[R324] MAJOR Robustness - receipts/probes/b8x8_50*/capture.log - F2 configuration-dependent margin (2.63x at 100 MHz, 2.06x at 50 MHz, 2.8% under the bar)
[R324] PASS Robustness - tb/verilator/nvm_capture_cpu/run.py:31-56, sim_main.cpp:131-137, firmware.py:88-91 - lapsed hold (ok=0, sys_cycles=0) fails the grade; anchor drift refused; simulated-time bound and clock-order refusal present
[R324] MAJOR Tests - tb/verilator/nvm_capture_cpu/run.py:59-71 - F1 no-traffic control never graded on timing
[R324] MINOR Tests - scripts/suite_shards.py:48-55 + tb/verilator/nvm_capture_cpu/ (no Makefile) - F3 silently outside the sweep
[R324] SUGGESTION Tests - tb/verilator/nvm_capture_cpu/sim_main.cpp:124-127 - F5 non-board relative phase at 50/100 MHz
[R324] PASS Tests - receipts/probes/b8x8_100/capture.log - unmodified head reproduces author row 0 exactly (1,899,620 cycles, 237,330/146/5,694); skip-copy arm leaves all bytes poisoned (public final-mut-skip-copy-uart.log); harness_sha256 and product_firmware_sha256 in measurements.json equal the head bytes
[R324] MAJOR Docs - docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1582-1592,1702-1707 - F1 figures and margin
[R324] MAJOR Docs - docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1568,1607,1707 - F2 clock statement and retirement of the 50 MHz assumption
[R324] MINOR Docs - docs/testing/TESTING.md:372-373 - F3 suite index and Makefile rule
[R324] PASS Docs - receipts/static_gates.log, receipts/markdown_gates.log - docs_check, check_doc_paths, check_doc_style, gen_toc --check/--verify-anchors, check_em_dash (0 findings over 175 added lines) all rc 0 at head; section 18 names every retired model factor
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2 open) | issue #559 body and assignment 5828771434; section 18 and UNRESOLVED 6; `soc.py`; `firmware.py`; `measurements.json`; five probe arms | R324-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| RTL | UNCLEAN (F2 open; F4 suggestion) | `KL_nvm_backend.sv` hold and tick; `KL_pp_shadow.sv:962`; `milan_datapath.sv:7396`; `milan_soc.py:2565,2700,3018-3184`; clock history `a94296d4`, `1e80a106`, `dfcf83ce` | R324-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| Robustness | UNCLEAN (F1, F2 open) | traffic ON/OFF at 100 and 50 MHz; phase-aligned arm; `run.py` grading; `sim_main.cpp` bounds | R324-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| Tests | UNCLEAN (F1, F3 open; F5 suggestion) | `run.py`, `sim_main.cpp`, `probe.py`, `firmware.py`; control reproduction; `suite_shards.py` discovery; public mutation logs | R324-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |
| Docs | UNCLEAN (F1, F2, F3 open) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md`; harness `README.md`; `TESTING.md`; `CLOCK_DOMAINS.md`; `BAREMETAL_FIRMWARE.md`; doc gates | R324-1 | 32076148acb0b9122e8c92a44f8e2ebbc8169280 |

## Probes and receipts

- **Arms.** Five disposable arms at 8x8, 2 captures each, under `scratch/` only. Each ran through the PR's own `soc.build`, `run._compile` and `run._grade` (`probe_step.py`). The single `verilator --build` call is split into a verilate step and a resumable make step so every command fits the foreground limit.
- **Environment.** Python packages came from scratch copies of the product LiteX set, with a symlink overlay of the CPU netlist cache so nothing shared could be written (`probe_setup.sh`, `probe_env.sh`). Every arm used the cached product netlist, and no generator ran.
- **Tools.** Scoped Verilator 5.050 (identity in `receipts/environment.txt`) and the pinned RV32 SDK, gcc 14.3.0.
- **Edits.** The only edits were the yaml clock line and, for the phase arm, the `sim_main.cpp` edge offset (patches in `receipts/probes/`).
- **Clone integrity.** Restored and verified. Index equals the HEAD tree, every tracked blob re-hashes equal, and the gitlinks are unchanged (external `efeb541a`, gptp-processor `e5dcea6e`, protocol-processor `09f9bf38`, verilog-axis `48ff7a7e`). A reviewer-created ignored `scripts/__pycache__` was removed, and `git status --porcelain --ignored` is empty (`receipts/clone_integrity.log`).
- **Hosted, exact head** (`receipts/hosted_check_runs.tsv`). 21 check runs succeeded, including rtl-fast, verilator-suites, the five Verilator shards, yosys-portability, elaborate, docs-check and docs-check-no-git. "Physical gPTP (nightly and manual)" is **skipped**, not executed. Hosted and act acceptance is the manager's.

## Real limits

- 2 captures per probe arm, not 16. Each 2-capture arm takes 6 to 8 minutes of wall clock, and a 16-capture arm does not fit one foreground command. The measured spread in 16 author rows is 0.075%.
- Phase was probed at two points only (default and PLL-aligned), not swept.
- The probe arms ran on Verilator 5.050, while the receipt records 5.052. Capture 0 reproduced exactly regardless.
- I did not run the 1x1 shape myself. The 1x1 conclusions use the public evidence.
- I did not run `run.py`'s `main()` literally, nor inside a network namespace. The netlist cache made the network irrelevant.
- No physical measurement: physical calibration NOT RUN, and simulation is not hardware proof. Debounce, memory ordering and board DDR timing remain UNRESOLVED 6.
- Full parent, PP, gPTP, Yosys and builder banks are out of scope here and are covered by the manager's source banks.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The candidate current-dev merge build at the merge turn.
- The external review R325.
- Physical calibration remains NOT RUN.
- A re-review at the corrected head once F1 to F3 are addressed. All five lenses must be re-covered at that head, since F1 and F2 touch the docs and the harness.

R324-1 FINISHED
