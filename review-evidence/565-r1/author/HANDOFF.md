# [A344] Issue #565 handoff

Status: local author work complete; independent review pending. All required command groups returned rc 0, with the declared unavailable arms listed below. The 8x8 50 MHz maximum is 24.30246 ms, below the 24.5 ms STOP threshold. No timing closure is claimed.
Branch: `565-8x8-clock`
Head: `054e59b41471ffbb3b4999a60c4cb04abcfc895f` (local, unpushed)
Base: `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`
Executor: [A344]. Internal reviewer: [R338]. External reviewer: [R339].

[Assignment](https://github.com/kebag-logic/milan-fpga/issues/565#issuecomment-5848231174); [capture decision](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112).

## Change list with file:line

- configs/endstation_ax7101_8x8.yaml:56: 50 MHz Milan/CPU target with build-contract basis and #565; no closure claim.
- docs/integration/BAREMETAL_FIRMWARE.md:55: identifies the 8x8 target and lack of cacheless placement/route evidence.
- hdl/ieee1722/aaf/README-parameters.md:29: derives the consumer clock from its selected shape instead of a stale board-wide 100 MHz value.
- scripts/check_nvm_capture.py:7: description now says the configured clock is recorded; executable gate unchanged.
- tb/verilator/nvm_capture_cpu/recipe.py:3 and soc.py:120: reconcile explanatory comments; executable harness unchanged.
- tb/verilator/nvm_capture_cpu/README.md:45: reconciled configuration and explicit comparison-clock/ROM scope.
- tb/verilator/nvm_capture_cpu/measurements.json:2: fresh date, input hashes, 96 rows, maxima and per-arm provenance.
- docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557 and :1740: reconciled clock and remeasurement basis.

## Consumer table, before and after

| Consumer | Before | After | Evidence |
|---|---|---|---|
| Builder loader / clock ordering | 100 MHz <= 100 MHz | 50 MHz <= 100 MHz | endstation_builder.py:3737,3772 |
| soc_params.json / sweep_opts / build_plan.md | --milan-clk-freq 100e6 | --milan-clk-freq 50e6 | endstation_builder.py:4649,4791,5342 |
| lwsrp_table.json / lwsrp_table.svh | module clocks 100000000 | module clocks 50000000 | endstation_builder.py:2326,2336 |
| gptp_ucode.hex | --clk-hz 100000000; 21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748 | --clk-hz 50000000; 78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b | endstation_builder.py:5626; 13312 bytes each |
| Main PLL / generated Milan clock | CLKOUT1_DIVIDE=16, 100 MHz | CLKOUT1_DIVIDE=32, 50 MHz | milan_soc.py:251; generated board-before/after gateware |
| CPU / datapath parameter | 100 MHz; MILAN_CLK_FREQ_HZ=100000000 | 50 MHz; MILAN_CLK_FREQ_HZ=50000000 | milan_soc.py:891,2565,2700,2945 |
| CPU clock selection / MAC domain | with_cpu_clk=True; milan_cd=milan | unchanged selection; selected domain now 50 MHz | milan_soc.py:2565,2700,2762; CPU memory CDC retained |
| System-timed firmware constants | CONFIG_CLOCK_FREQUENCY=100000000 | unchanged | System timer, UART and controller remain at sys frequency |
| Datapath clock derivations | PP_TIM_DIV_US_P=100; quarter tick 25000000; diagnostic ticks 100000000 | PP_TIM_DIV_US_P=50; quarter tick 12500000; diagnostic ticks 50000000 | milan_datapath.sv:214,240,245,314; all derive from MILAN_CLK_FREQ_HZ |
| PHC reset increment | 167772160 Q8.24 ns (10 ns) | 335544320 Q8.24 ns (20 ns) | milan_datapath.sv:2367; hdl/common/csr/milan_csr.sv:1182 |
| MAAP clock parameter | 100000000 | 50000000 | milan_datapath.sv:284 |
| MCLK divider exponent / source-settle error | 3 / 32 cycles | 2 / 16 cycles | milan_datapath.sv:656,5990; divider remains derived even where playback is pruned |
| Latency-tap re-arm timeout | 50000 cycles | 25000 cycles | milan_datapath.sv:7119; feature enable unchanged |
| Media NCO, CRF RX, grid alignment and AVTP RX monitor frequency inputs | 100000000 each | 50000000 each | milan_datapath.sv:764,5481,5647,5747 |
| MMCM servo, I2S playback and render setpoint frequency inputs | 100000000 each | 50000000 each | milan_datapath.sv:5567,6053,6192; optional feature pruning unchanged |
| gPTP and protocol-processor shadow clock inputs | 100000000 each | 50000000 each | milan_datapath.sv:6886,7386; gitlinks unchanged |
| PP bridges, system-cycle watchdogs | 3072 cycles, 12-bit counters | 6144 cycles, 13-bit counters | milan_soc.py:2194,3005; generated comparisons |
| PPS optional width (disabled in shape) | 100000 cycles if enabled | 50000 cycles if enabled | milan_soc.py:907, derived from clock |
| Generated XDC | 21076 bytes, SHA-256 28fae38e8ef8e1d4288289943424d023f04e996bcc4a9058f4e36e6214ce71a1 | byte-identical | Both full board elaborations rc 0. Derived clock follows PLL divider; system/audio/CDC constraints retain their recipe. |
| Capture configured_cpu_hz | 100000000 | 50000000, all six arms remeasured | check_nvm_capture.py:46; harness soc.py:119 |
| Simulation shape headers / inventories | Original descriptor geometry and NVM census | Byte-identical; suite clocks remain independently specified | csr, milan_dp, nvm_backend, nvm_cosim default chunks passed |
| Documentation | Stale configuration reconciliation; AAF parameter table assumes AX 100 MHz | Build-contract basis and shape-derived parameter wording; remeasured section 18 | BAREMETAL_FIRMWARE.md; snapshot section 18; harness README; hdl/ieee1722/aaf/README-parameters.md |

The 8x8 system clock remains 100 MHz, sample rate 48 kHz and audio PLL declaration 24.576 MHz. No other clock declaration carries a CLOSED claim. No timing closure is claimed. The optional playback block is disabled in this 8x8 shape.

## Other four configurations: byte identity

All 11 generated files per configuration are byte-identical: endstation_arty_4x4, endstation_arty_8ch, endstation_arty_current, endstation_ax7101_1x1_tdm8. Per-file SHA-256 and sizes are in artifacts-before.json and artifacts-after.json. Generated files remain in external scratch storage.

For 8x8 the changed files are soc_params.json, lwsrp_table.json, lwsrp_table.svh, build_plan.md, gptp_ucode.hex and sweep_opts.sh. Descriptor artifacts and adp_shape_defaults.svh are unchanged.

| Configuration | Files | Total bytes | Before SHA-256 | After SHA-256 | Result |
|---|---:|---:|---|---|---|
| endstation_arty_4x4 | 11 | 108837 | e5883cbb3878806c964a04fdfb1a78712eaca8c3943d51f30325b0d94c037f42 | e5883cbb3878806c964a04fdfb1a78712eaca8c3943d51f30325b0d94c037f42 | byte-identical |
| endstation_arty_8ch | 11 | 133649 | c9c5bf747aa16b4734d920d4957906c4b26351f34e4f1e5e23e04db59fcadf89 | c9c5bf747aa16b4734d920d4957906c4b26351f34e4f1e5e23e04db59fcadf89 | byte-identical |
| endstation_arty_current | 11 | 79350 | 2a681aa9b43469b0cb06771a869be61c99f90822aef40161533550f7aff2f661 | 2a681aa9b43469b0cb06771a869be61c99f90822aef40161533550f7aff2f661 | byte-identical |
| endstation_ax7101_1x1_tdm8 | 11 | 90240 | 55b221de20707e244f7c2164a3b163f47dc2efc22a66b316e9fe50cf1523bf38 | 55b221de20707e244f7c2164a3b163f47dc2efc22a66b316e9fe50cf1523bf38 | byte-identical |

Aggregate SHA-256 hashes sorted `filename<TAB>size<TAB>sha256<LF>` records; all per-file bytes were compared directly.

## Capture measurements

All six arms returned rc 0. Each has 16 captures, with successful attestation, closed ownership, matching destination bytes and the required traffic checks.

| Shape | CPU MHz | Traffic | Captures | Minimum ms | Maximum ms | 49 ms / maximum |
|---|---:|---|---:|---:|---:|---:|
| endstation_ax7101_8x8 | 50 | ON | 16 | 24.29290 | 24.30246 | 2.0163x |
| endstation_ax7101_8x8 | 50 | OFF | 16 | 24.25794 | 24.26154 | 2.0197x |
| endstation_ax7101_1x1_tdm8 | 50 | ON | 16 | 6.59814 | 6.60642 | 7.4170x |
| endstation_ax7101_1x1_tdm8 | 50 | OFF | 16 | 6.58554 | 6.58857 | 7.4371x |
| endstation_ax7101_8x8 | 100 | ON | 16 | 18.99012 | 19.00433 | 2.5784x |
| endstation_ax7101_8x8 | 100 | OFF | 16 | 19.78694 | 19.79024 | 2.4760x |

The contract 8x8 maximum leaves 0.19754 ms below 24.5 ms and gives 2.01625679x margin against the guaranteed 49 ms floor. The nominal hold remains 50 ms. Both non-contract arms are included in the refreshed receipt; neither changes the contract threshold. All 96 newly produced row dictionaries equal the previous row dictionaries, while configured clock, input hashes and build provenance are refreshed.

## ROM ledger

`syn/yosys/ooc.sh timestamp_counter` returned rc 0. Its mandatory preflight regenerated and checked all three processor ROMs against the ledger at the current gitlinks. All three digests are unchanged (rom-digests.json), so no --record-rom-digests run or ledger edit is needed. The changed configuration-specific gPTP image is different from the default generator image checked by this ledger: ooc.sh supplies no --clk-hz or station identity arguments.

## Issue #231 baseline report

Read FETCH_HEAD ae729bbfd90934f4d56d3b02f1ffc652496b414d after fetching origin 231-pp-shadow-baseline. No baseline files edited.

Its 8x8 timer and integrated CPU/Milan clock are explicitly 100 MHz. OOC constraints remain independently fixed at 100 MHz for both shapes. The 8x8 integrated synthesis figures (68,136 LUTs, -11.331 ns whole-design WNS), attribution variant, generated gPTP image and clock-derived timer parameters describe that 100 MHz build, not a 50 MHz rerun. Clock-dependent synthesis inputs can affect area as well as timing; no rescaling is justified. Historical figures and 1x1 results keep their original recipes. The 8x8 exceeds 63,400 LUTs by 4,736 and has no placement/route result in that baseline.

## Gate table

| Gate | Result |
|---|---|
| Full board elaboration, before and after generated arguments | rc 0 each; XDC identity and changed divider inspected |
| python3 -B scripts/lint_rtl.py --check | rc 0; 90 findings within ratchet 90 |
| syn/yosys/ooc.sh timestamp_counter | rc 0; mandatory three-ROM digest preflight passed |
| Full builder, pinned compiler | rc 0 (781.508 s); complete bank, 851 compiler invocations, selector mapped to the pinned SDK; existing gate 11 calibration report unavailable (NOT RUN) |
| Full builder, absent compiler | rc 0 (560.715 s); all three cross selectors hidden, original host probes retained; gate 1b compiler instruments intentionally NOT RUN, existing gate 11 calibration report unavailable |
| Default sweep shard 1/5 | rc 0; 21 suites, 173891 checks, 0 failures/timeouts; four declared external-field-campaign/freshness skips |
| Default sweep shard 3/5 | rc 0; 12 suites, 14432 checks, 0 failures/timeouts; includes csr and nvm_backend |
| Default sweep shard 4/5 | rc 0; 1 suite, 11206 checks, 0 failures/timeouts; the 8x8 integration leg alone passes 3524 checks |
| python3 -B scripts/docs_check.py | rc 0 (4.171 s) |
| GIT_DIR=/dev/null python3 -B scripts/docs_check.py | rc 0 (4.173 s) |
| python3 -B scripts/check_em_dash.py --base 831f94f4 | rc 0 (3.070 s) |
| python3 -B scripts/check_doc_style.py | rc 0 (0.064 s) |
| python3 -B scripts/gen_toc.py --check | rc 0 (2.418 s) |
| python3 -B scripts/gen_toc.py --verify-anchors | rc 0 (1.567 s) |
| python3 -B scripts/check_doc_paths.py | rc 0 (0.064 s) |
| python3 -B scripts/check_nvm_capture.py | rc 0 (0.715 s) |
| git diff --check | rc 0 (0.032 s) |

The first board-export attempt lacked the standard builder output location. Generated artifacts were placed there and both complete exports passed. No source repair was required.

## Retained independent clocks and comparison limits

The CSR and NxN datapath suites read descriptor shape headers, which contain no Milan frequency. Their fixed or accelerated test clocks remain test inputs. nvm_backend and nvm_cosim likewise derive geometry while retaining accelerated model clocks. The CPU capture harness records configured and effective clocks separately.

The 100 MHz non-contract capture point continues to override CPU/Milan clocks only; its gPTP image follows the selected 50 MHz config. Per-arm ROM hashes record that input. This comparison supplies no gPTP conformance or physical timing claim.

The fixed alternate sweep_extra.sh recipe and legacy bridge-test clock examples do not consume the 8x8 YAML; they remain unchanged. The selected board generation derives all live clock values from soc_params.json.

## Reproduction files

Small orchestration scripts accompany this handoff. They run repository commands in the foreground from the physical worktree, with explicit generous timeouts. `builder_modes.py` executes the complete builder bank through its main entry point, mapping only the compiler selector in present mode and hiding all three cross selectors in absent mode; host probes and native tests retain their original subprocess calls. No SDK or dependency files are installed or copied here.

Large build exports and logs remain under `$VALIDATION_STORAGE/565-a344`. Their size/hash manifests provide custody without copying those trees. All output-directory files must remain below 200 KB.

## Reproduction commands and limitations

All commands ran in the foreground from the physical worktree `$LANES/565-8x8-clock`. Long commands used explicit generous subprocess timeouts; no process was detached. The capture, builder and board generation used the existing pinned environment with `PYTHONHASHSEED=0`, `COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true` and `LITEX_ENV_CC_TRIPLE=riscv32-linux`. The PATH prefixed `$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin` and `$WORKSPACE_HOME/litex-milan/venv/bin`. Dependency pins and independent archive/netlist hashes are in environment-receipt.json.

The two full builder invocations were:

```sh
rtk proxy unshare -Urn $WORKSPACE_HOME/litex-milan/venv/bin/python3 -B $VALIDATION_STORAGE/565-a344/builder_modes.py present
rtk proxy unshare -Urn $WORKSPACE_HOME/litex-milan/venv/bin/python3 -B $VALIDATION_STORAGE/565-a344/builder_modes.py absent
```

The adapter invokes the complete test_builder.py main bank. Present mode passes --require-rv32 and maps only its historical absolute compiler selector to the already installed pinned compiler. Absent mode hides all three cross-compiler selectors while preserving host probes and native tests. The full logs and adapter are supplied. Present mode made 851 target-compiler calls. Both modes explicitly report the existing gate 11 calibration report as NOT RUN because the report is absent. Absent mode also reports gate 1b compiler instruments as intentionally NOT RUN. These arms contribute no evidence.

Every capture used this command pattern, with the six shape/clock/traffic combinations in the table:

```sh
rtk proxy unshare -Urn $WORKSPACE_HOME/litex-milan/venv/bin/python3 -B tb/verilator/nvm_capture_cpu/run.py --shape <shape> --cpu-hz <Hz> --captures 16 --traffic <on-or-off> --build-dir $VALIDATION_STORAGE/565-a344/capture-<shape-suffix>-<MHz>-<arm>
```

The per-arm result files and committed receipt record the expanded arguments. All six raw capture logs and graded measurement files accompany this handoff. The capture gate, recipe and SoC harness have identical executable ASTs to the base after excluding module docstrings; only descriptive text changed.

The selected default chunks ran sequentially with `SUITE_TIMEOUT=14400`:

```sh
rtk proxy scripts/run_all_suites.sh $VALIDATION_STORAGE/565-a344/sweep-1 --shard 1/5
rtk proxy scripts/run_all_suites.sh $VALIDATION_STORAGE/565-a344/sweep-3 --shard 3/5
rtk proxy scripts/run_all_suites.sh $VALIDATION_STORAGE/565-a344/sweep-4 --shard 4/5
```

Chunk 1 explicitly skips four external field-campaign/freshness arms because their optional traffic generator is absent. No evidence is claimed for those arms. The NVM co-simulation reports 465 checks and 39/39 mutants killed. Chunk 3 includes CSR and NVM backend; chunk 4 exercises the default datapath sweep, including 8x8. The remaining repository gates and exact arguments appear in the gate table and result JSON files. The ROM preflight used `OOC_TMP=$VALIDATION_STORAGE/565-a344/rom-digests`; the ledger stayed byte-identical.

The first em-dash check returned rc 2 because the system interpreter lacked html5lib. The final documentation and capture gates ran with the existing `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin` prepended to PATH. All six Markdown dependency versions match tools/markdown/requirements.txt. No package installation or dependency copy was needed. The original environment failure is retained in initial-em-dash.log and its result JSON. The no-Git docs mode explicitly skips its Git inventory-parity self-test as expected, while its other checks pass.

No hardware was used. No submodule was edited. The baseline was fetched and inspected without a checkout. No push, PR creation/edit, or merge was performed. Independent review and all later public workflow steps remain with the assigned roles.
