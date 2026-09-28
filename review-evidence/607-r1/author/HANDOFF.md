# [A408] Issue #607 handoff

Author validation complete; ready for independent review.

Branch: `607-xdc-clock-names`. Base: `54ce877371ee6e8878cf67294e86c2a8481b62f6`. Head: `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Executor: [A408]. Assigned independent reviewers: [R382] and [R383].
Assignment: https://github.com/kebag-logic/milan-fpga/issues/607#issuecomment-5865111793
Scope authority: #607 acceptance 1-4; linked #605 F1 findings; #395 AX7101 margin decision;
REQ-VER-02/03/04 and the repository integration/testing documentation.

## Acceptance evidence

| Item | Change with file:line | Proof |
|---|---|---|
| 1: real clock objects and supported hook | `sw/litex/milan_soc.py:245,268,424,449,458` retains the raw PLL clock output objects. `sw/litex/clock_constraints.py:38` resolves their names through the generated namespace. `sw/litex/clock_constraints.tcl:4,13` applies conditional class constraints after synthesis and requires exactly one clock on each selected net. | The committed tests cover renamed signals, both Ethernet ports, optional clock domains and hook order. Each completed fresh seed records 112 quasi-static cells with setup 4 / hold 3; its application log and warning census are below. |
| 2: effective 8 ns Ethernet data bound | `sw/litex/platforms/alinx_ax7101.py:301` selects the local subclass. `sw/litex/clock_constraints.py:16` removes exactly the known generic MultiReg command and refuses template drift. `sw/litex/clock_constraints.tcl:31,66` restores unrelated exceptions and applies 8 ns in both directions for sys and Milan. | Each completed seed has positive slack at an explicit 8.000 ns requirement in all four directions and `Max Delay Datapath Only` interaction, with no unsafe pair. The Tcl controls independently check the scoped exceptions. Installed LiteX was not edited. |
| 3: build refusal and planted wrong name | `sw/litex/clock_constraints.py:61` rejects emitted 12-4739 / 20-1307 diagnostics and missing logs. `sw/litex/milan_soc.py:3960` calls it after every completed shipping build, before manifest publication. `sw/builder/test_builder.py:27557` includes the tests in the complete bank. | `sw/builder/test_clock_constraints.py:163,206` covers both IDs at WARNING / CRITICAL WARNING / ERROR severity, missing logs, common build wiring, and the retained live wrong-name control. Both full banks and the live control pass at this head. |
| 4: fresh AX7101 1x1 TDM8 sweep | `sw/litex/clock_constraints.py:55` retains interaction and exception reports. The generated shipping recipe uses the three canonical placement directives, `AreaOptimized_high` synthesis and `ExploreArea` optimization. Each implementation and report process is limited to 16 threads. | The tables below report every completed seed and corner. Acceptance requires all three seeds, WNS >= +0.030 ns, WHS >= 0, TNS = THS = 0, and positive Ethernet slack against 8.000 ns. Current status: met. |

Documentation: `docs/integration/BUILDING.md:517`, `docs/litex/LITEX_SOC.md:56`,
and `docs/testing/RUNNING_TESTS.md:160` describe the repaired contract and evidence.

## Exception policy

The bounded hook is selected for AX7101 GMII; MII retains its existing asynchronous
groups. The implementation-log refusal is common to all shipping builds.
The 8 ns budget covers Ethernet data crossings. The existing asynchronous reset PRE-pin
exceptions and 2 ns reset inter-stage bound remain. Other MultiReg paths, including
asynchronous inputs, retain their exceptions. A changed upstream MultiReg template
causes an explicit refusal and must be adapted before that upstream version can build.
The inspected upstream definitions are `litex/build/xilinx/common.py:48,56`
(first-stage `mr_ff` tagging) and `litex/build/xilinx/vivado.py:242,249,256,263`
(generic MultiReg, reset PRE and reset inter-stage constraints), at the source
identity recorded in `installed-constraint-source.json`.

This explains the saved-checkpoint sys-to-Ethernet slack difference from the broad
exception-clearing probe in #605: retaining reset assertion exceptions measures the
bounded data paths. No per-register placement waiver, clock-frequency change, RTL
change, firmware change or installed-package edit is part of this implementation.

## Before and after constraint application

The shipping implementation log contains 14 emitted CRITICAL WARNING lines:
ten 12-4739, two 20-1307 and two 12-5201. A fifteenth substring match is echoed
source rather than an emitted warning. In its original interaction report,
eth -> sys and sys -> eth are False Path; eth -> Milan is timed unsafe at 4 ns;
Milan -> eth is partial false path / unsafe. The quasi-static relaxation was absent.

Read-only diagnostic reports under `$VALIDATION_STORAGE/607-a408-work` confirm that scoping the generic mask
away from the bounded data pairs applies the intended bound. The production hook
applied in memory to the saved checkpoint selects all raw clock nets and 112
quasi-static cells without a rejected-constraint diagnostic. These probes are
diagnostic evidence; the fresh builds below are the acceptance evidence.
`diagnostic-artifacts.json` records the retained probe, elaboration and control artifacts
by size and SHA-256, including exploratory attempts that did not complete.

The supplied shipping inputs and installed constraint-source identities are recorded
in `shipping-inputs.json` and `installed-constraint-source.json`. Their unchanged
hash verification is in `read-only-verification.json`. No checkpoint was saved into
the supplied build tree.


| Implementation | Warnings | Critical warnings | Errors | 12-4739 | 20-1307 | 12-5201 |
| --- | --- | --- | --- | --- | --- | --- |
| shipping input | 900 | 14 | 0 | 10 | 2 | 2 |
| AltSpreadLogic_high | 878 | 0 | 0 | 0 | 0 | 0 |
| ExtraTimingOpt | 878 | 0 | 0 | 0 | 0 | 0 |
| ExtraPostPlacementOpt | 877 | 0 | 0 | 0 | 0 | 0 |


Counts are emitted severity lines, excluding echoed source and repeated summary totals. The shipping log predates the assigned base; these are observed censuses of the supplied image and fresh candidates. `shipping-warning-census.json` retains the baseline count by diagnostic ID.

Application records from each completed implementation log:


`$VALIDATION_STORAGE/607-a408-work/build_ax7101_asl_350af5dcf/gateware/vivado.log`

```text
4218: CONSTRAINTS: quasi_static cells=112 setup=4 hold=3
4220: CONSTRAINTS: eth=eth_clocks0_rx bounded=milansoc_crg_clkout0 milansoc_crg_clkout1 async=milansoc_crg_pll_audio_fb milansoc_crg_audio_ref_raw milansoc_crg_audio_mclk_raw milansoc_crg_clkout2 milansoc_crg_clkout3 milansoc_crg_clkout4 budget_ns=8.000
4221: CONSTRAINTS: MultiReg eth=12 part=198 other=0
```


`$VALIDATION_STORAGE/607-a408-work/build_ax7101_eto_350af5dcf/gateware/vivado.log`

```text
4216: CONSTRAINTS: quasi_static cells=112 setup=4 hold=3
4218: CONSTRAINTS: eth=eth_clocks0_rx bounded=milansoc_crg_clkout0 milansoc_crg_clkout1 async=milansoc_crg_pll_audio_fb milansoc_crg_audio_ref_raw milansoc_crg_audio_mclk_raw milansoc_crg_clkout2 milansoc_crg_clkout3 milansoc_crg_clkout4 budget_ns=8.000
4219: CONSTRAINTS: MultiReg eth=12 part=198 other=0
```


`$VALIDATION_STORAGE/607-a408-work/build_ax7101_eppo_350af5dcf/gateware/vivado.log`

```text
4217: CONSTRAINTS: quasi_static cells=112 setup=4 hold=3
4219: CONSTRAINTS: eth=eth_clocks0_rx bounded=milansoc_crg_clkout0 milansoc_crg_clkout1 async=milansoc_crg_pll_audio_fb milansoc_crg_audio_ref_raw milansoc_crg_audio_mclk_raw milansoc_crg_clkout2 milansoc_crg_clkout3 milansoc_crg_clkout4 budget_ns=8.000
4220: CONSTRAINTS: MultiReg eth=12 part=198 other=0
```


## Planted wrong-name test

At head `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`, the live test returned rc 0 in 24.16 s. The planted
vendor invocation itself returned 0 while emitting both 12-4739 and 20-1307.
`check_implementation_log` raised the expected refusal containing both IDs, so the
test passed. The harness pass records the expected build-check failure.

Exact command: `$WORKSPACE_HOME/litex-milan/venv/bin/python -B sw/builder/test_clock_constraints.py --vivado $WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado --checkpoint $WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp --evidence-dir $VALIDATION_STORAGE/607-a408-work/live-plant-350af5dcf`.
Retained raw files: `$VALIDATION_STORAGE/607-a408-work/live-plant-350af5dcf` contains `wrong.xdc`,
`plant.tcl`, `vivado.log` and `exit-code.txt`. Receipt: `live-plant-result.json`.

The complete banks also test missing / ambiguous clocks, renamed namespaces,
both ports, optional domains, preservation of unrelated and reset exceptions,
empty / nonempty quasi-static classes and changed upstream templates. Seven
preparatory mutations were rejected: retained generic mask, 80 ns bound,
deleted quasi-static hook, wrong clock selection, deleted Ethernet hook call,
deleted log check and disabled 12-4739 detection. Those preparatory mutations
are not represented as a separate final-head mutation campaign.

## Fresh sweep timing

All outputs are under the physical data path. The exact build and report argv and
return codes, plus build durations, are in `sweep-results.json`; `run_sweep.py` and
`report_seed.tcl` reproduce the sequence. `PYTHONHASHSEED=0`,
`PYTHON_CPU_COUNT=16`, and `--vivado-max-threads 16` are used. Runs are sequential.
The existing RV32 SDK is selected with `LITEX_ENV_CC_TRIPLE=riscv32-linux`.

The 0 C and 85 C operating settings are reported separately below. They use
the vendor Slow/Fast timing models; this is static timing evidence, with no
hardware or temperature-chamber measurement in this assignment.


| Seed | C | Corner | WNS ns | TNS ns | WHS ns | THS ns |
| --- | --- | --- | --- | --- | --- | --- |
| asl | 0 | Slow | +0.034 | 0.000 | +0.123 | 0.000 |
| asl | 0 | Fast | +1.567 | 0.000 | +0.022 | 0.000 |
| asl | 85 | Slow | +0.034 | 0.000 | +0.123 | 0.000 |
| asl | 85 | Fast | +1.567 | 0.000 | +0.022 | 0.000 |
| eto | 0 | Slow | +0.268 | 0.000 | +0.126 | 0.000 |
| eto | 0 | Fast | +1.299 | 0.000 | +0.022 | 0.000 |
| eto | 85 | Slow | +0.268 | 0.000 | +0.126 | 0.000 |
| eto | 85 | Fast | +1.299 | 0.000 | +0.022 | 0.000 |
| eppo | 0 | Slow | +0.105 | 0.000 | +0.102 | 0.000 |
| eppo | 0 | Fast | +1.516 | 0.000 | +0.036 | 0.000 |
| eppo | 85 | Slow | +0.105 | 0.000 | +0.102 | 0.000 |
| eppo | 85 | Fast | +1.516 | 0.000 | +0.036 | 0.000 |


Ethernet slack against an explicitly checked **8.000 ns** datapath requirement:

| Seed | C | Corner | eth -> sys | sys -> eth | eth -> Milan | Milan -> eth |
| --- | --- | --- | --- | --- | --- | --- |
| asl | 0 | Slow | +6.597 | +6.742 | +6.293 | +6.664 |
| asl | 0 | Fast | +7.218 | +7.260 | +7.107 | +7.264 |
| asl | 85 | Slow | +6.597 | +6.742 | +6.293 | +6.664 |
| asl | 85 | Fast | +7.218 | +7.260 | +7.107 | +7.264 |
| eto | 0 | Slow | +6.290 | +6.773 | +6.477 | +6.655 |
| eto | 0 | Fast | +6.933 | +7.265 | +7.232 | +7.264 |
| eto | 85 | Slow | +6.290 | +6.773 | +6.477 | +6.655 |
| eto | 85 | Fast | +6.933 | +7.265 | +7.232 | +7.264 |
| eppo | 0 | Slow | +6.232 | +6.603 | +6.365 | +6.471 |
| eppo | 0 | Fast | +6.977 | +7.217 | +7.041 | +7.176 |
| eppo | 85 | Slow | +6.232 | +6.603 | +6.365 | +6.471 |
| eppo | 85 | Fast | +6.977 | +7.217 | +7.041 | +7.176 |


All reported Ethernet clock-interaction rows from the combined report for each seed follow, including the clean intra-domain row. Each of the four corner reports also contains all four pairs with the same constraint classification and no unsafe pair. The `Ignored` interaction class accompanies `Max Delay Datapath Only`; the path reports independently carry the 8.000 ns requirement.


`$VALIDATION_STORAGE/607-a408-work/build_ax7101_asl_350af5dcf/acceptance/seed_interaction.rpt`

```text
eth_clocks0_rx               eth_clocks0_rx               rise - rise     0.86     0.00            0         1658             8.00  rise - rise     0.08     0.00            0         1658             0.00  Clean                Partial False Path
eth_clocks0_rx               milansoc_crg_clkout0         rise - rise     6.60     0.00            0           13             8.00                                           0           13                   Ignored              Max Delay Datapath Only
eth_clocks0_rx               milansoc_crg_clkout1         rise - rise     6.29     0.00            0           50             8.00                                           0           50                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout0         eth_clocks0_rx               rise - rise     6.74     0.00            0           16             8.00                                           0           16                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout1         eth_clocks0_rx               rise - rise     6.66     0.00            0           14             8.00                                           0           14                   Ignored              Max Delay Datapath Only
```


`$VALIDATION_STORAGE/607-a408-work/build_ax7101_eto_350af5dcf/acceptance/seed_interaction.rpt`

```text
eth_clocks0_rx               eth_clocks0_rx               rise - rise     0.75     0.00            0         1658             8.00  rise - rise     0.11     0.00            0         1658             0.00  Clean                Partial False Path
eth_clocks0_rx               milansoc_crg_clkout0         rise - rise     6.29     0.00            0           13             8.00                                           0           13                   Ignored              Max Delay Datapath Only
eth_clocks0_rx               milansoc_crg_clkout1         rise - rise     6.48     0.00            0           50             8.00                                           0           50                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout0         eth_clocks0_rx               rise - rise     6.77     0.00            0           16             8.00                                           0           16                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout1         eth_clocks0_rx               rise - rise     6.66     0.00            0           14             8.00                                           0           14                   Ignored              Max Delay Datapath Only
```


`$VALIDATION_STORAGE/607-a408-work/build_ax7101_eppo_350af5dcf/acceptance/seed_interaction.rpt`

```text
eth_clocks0_rx               eth_clocks0_rx               rise - rise     0.92     0.00            0         1658             8.00  rise - rise     0.12     0.00            0         1658             0.00  Clean                Partial False Path
eth_clocks0_rx               milansoc_crg_clkout0         rise - rise     6.23     0.00            0           13             8.00                                           0           13                   Ignored              Max Delay Datapath Only
eth_clocks0_rx               milansoc_crg_clkout1         rise - rise     6.37     0.00            0           50             8.00                                           0           50                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout0         eth_clocks0_rx               rise - rise     6.60     0.00            0           16             8.00                                           0           16                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout1         eth_clocks0_rx               rise - rise     6.47     0.00            0           14             8.00                                           0           14                   Ignored              Max Delay Datapath Only
```


## Gate table

All final verdicts below are at `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`. Commands ran directly, without pipelines. `gate-results.json` retains each command, rc, duration, log path, size and SHA-256; `gate-summary.json` checks the final verdict set. Logs are under the physical data path.

| Gate | Command | rc | Seconds | Log |
| --- | --- | --- | --- | --- |
| builder-present | `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` | 0 | 766.77 | `builder-present.log` |
| builder-absent | `python3 -B $MANAGEMENT/2026-09-23/607-a408/run_builder_absent.py` | 0 | 558.04 | `builder-absent.log` |
| ci_scope-selftest | `python3 -B scripts/ci_scope.py --selftest` | 0 | 2.47 | `ci_scope-selftest.log` |
| gen_hdl_reference-selftest | `python3 -B scripts/gen_hdl_reference.py --selftest` | 0 | 0.21 | `gen_hdl_reference-selftest.log` |
| gen_hdl_reference-output | `python3 -B scripts/gen_hdl_reference.py --output $VALIDATION_STORAGE/607-a408-work/hdl-reference-350af5dcf` | 0 | 1.57 | `gen_hdl_reference-output-fresh.log` |
| gen_wavedrom-selftest | `python3 -B scripts/gen_wavedrom.py --selftest` | 0 | 0.11 | `gen_wavedrom-selftest.log` |
| gen_wavedrom-wd_axis_backpressure.json | `python3 -B scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.31 | `gen_wavedrom-wd_axis_backpressure.json.log` |
| gen_wavedrom-wd_cdc_handshake.json | `python3 -B scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.36 | `gen_wavedrom-wd_cdc_handshake.json.log` |
| gen_wavedrom-wd_gptp_pdelay.json | `python3 -B scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.31 | `gen_wavedrom-wd_gptp_pdelay.json.log` |
| measure_control_flow-selftest | `python3 -B scripts/measure_control_flow.py --selftest` | 0 | 0.16 | `measure_control_flow-selftest.log` |
| measure_cohesion-selftest | `python3 -B scripts/measure_cohesion.py --selftest` | 0 | 0.06 | `measure_cohesion-selftest.log` |
| test_firmware_compiler-selftest | `python3 -B sw/builder/test_firmware_compiler.py --selftest` | 0 | 1.62 | `test_firmware_compiler-selftest.log` |
| test_firmware_compiler-absent | `python3 -B sw/builder/test_firmware_compiler.py --absent --audit $VALIDATION_STORAGE/607-a408-work/firmware-absent.jsonl` | 0 | 436.95 | `test_firmware_compiler-absent.log` |
| check_nvm_record_space | `python3 -B scripts/check_nvm_record_space.py` | 0 | 1.97 | `check_nvm_record_space.log` |
| check_nvm_record_space-self-test | `python3 -B scripts/check_nvm_record_space.py --self-test` | 0 | 30.67 | `check_nvm_record_space-self-test.log` |
| check_nvm_capture | `python3 -B scripts/check_nvm_capture.py` | 0 | 0.77 | `check_nvm_capture.log` |
| check_soc_sources | `python3 -B scripts/check_soc_sources.py` | 0 | 0.11 | `check_soc_sources.log` |
| check_soc_sources-selftest | `python3 -B scripts/check_soc_sources.py --selftest` | 0 | 0.21 | `check_soc_sources-selftest.log` |
| iob_pack_selftest | `python3 -B sw/litex/iob_pack_selftest.py` | 0 | 2.12 | `iob_pack_selftest.log` |
| check_rtl_source_lists | `python3 -B scripts/check_rtl_source_lists.py` | 0 | 1.37 | `check_rtl_source_lists.log` |
| check_rtl_source_lists-selftest | `python3 -B scripts/check_rtl_source_lists.py --selftest` | 0 | 2.57 | `check_rtl_source_lists-selftest.log` |
| measure_naming-check | `python3 -B scripts/measure_naming.py --check` | 0 | 0.46 | `measure_naming-check.log` |
| measure_naming-selftest | `python3 -B scripts/measure_naming.py --selftest` | 0 | 0.46 | `measure_naming-selftest.log` |
| check_port_contracts | `python3 -B scripts/check_port_contracts.py` | 0 | 2.32 | `check_port_contracts.log` |
| check_port_contracts-selftest | `python3 -B scripts/check_port_contracts.py --selftest` | 0 | 2.67 | `check_port_contracts-selftest.log` |
| measure_fail_fast-check | `python3 -B scripts/measure_fail_fast.py --check` | 0 | 1.47 | `measure_fail_fast-check.log` |
| measure_fail_fast-selftest | `python3 -B scripts/measure_fail_fast.py --selftest` | 0 | 1.47 | `measure_fail_fast-selftest.log` |
| check_todo_ownership | `python3 -B scripts/check_todo_ownership.py` | 0 | 1.37 | `check_todo_ownership.log` |
| check_todo_ownership-selftest | `python3 -B scripts/check_todo_ownership.py --selftest` | 0 | 1.47 | `check_todo_ownership-selftest.log` |
| measure_test_evidence-check | `python3 -B scripts/measure_test_evidence.py --check` | 0 | 5.47 | `measure_test_evidence-check.log` |
| measure_test_evidence-selftest | `python3 -B scripts/measure_test_evidence.py --selftest` | 0 | 5.53 | `measure_test_evidence-selftest.log` |
| check_hygiene-check | `python3 -B scripts/check_hygiene.py --check` | 0 | 0.31 | `check_hygiene-check.log` |
| check_hygiene-selftest | `python3 -B scripts/check_hygiene.py --selftest` | 0 | 0.31 | `check_hygiene-selftest.log` |
| check_sv_idiom | `python3 -B scripts/check_sv_idiom.py` | 0 | 0.41 | `check_sv_idiom.log` |
| check_sv_idiom-selftest | `python3 -B scripts/check_sv_idiom.py --selftest` | 0 | 0.41 | `check_sv_idiom-selftest.log` |
| check_cpp_idiom | `python3 -B scripts/check_cpp_idiom.py` | 0 | 1.22 | `check_cpp_idiom.log` |
| check_cpp_idiom-selftest | `python3 -B scripts/check_cpp_idiom.py --selftest` | 0 | 1.32 | `check_cpp_idiom-selftest.log` |
| check_sh_idiom | `python3 -B scripts/check_sh_idiom.py` | 0 | 0.21 | `check_sh_idiom.log` |
| check_sh_idiom-selftest | `python3 -B scripts/check_sh_idiom.py --selftest` | 0 | 0.26 | `check_sh_idiom-selftest.log` |
| ci_events-check | `python3 -B scripts/ci_events.py --check` | 0 | 0.21 | `ci_events-check.log` |
| ci_events-selftest | `python3 -B scripts/ci_events.py --selftest` | 0 | 15.04 | `ci_events-selftest.log` |
| gen_aem_store-self-test | `python3 -B avdecc/gen_aem_store.py --self-test` | 0 | 0.06 | `gen_aem_store-self-test.log` |
| check_entity_shape-self-test | `python3 -B scripts/check_entity_shape.py --self-test` | 0 | 41.14 | `check_entity_shape-self-test.log` |
| check_wire_accountability-self-test | `python3 -B scripts/check_wire_accountability.py --self-test` | 0 | 0.26 | `check_wire_accountability-self-test.log` |
| docs_check | `python3 -B scripts/docs_check.py` | 0 | 4.27 | `docs_check.log` |
| check_doc_paths | `python3 -B scripts/check_doc_paths.py` | 0 | 0.06 | `check_doc_paths.log` |
| gen_toc-check | `python3 -B scripts/gen_toc.py --check` | 0 | 2.67 | `gen_toc-check.log` |
| gen_toc-selftest | `python3 -B scripts/gen_toc.py --selftest` | 0 | 0.87 | `gen_toc-selftest.log` |
| gen_toc-verify-anchors | `python3 -B scripts/gen_toc.py --verify-anchors` | 0 | 1.67 | `gen_toc-verify-anchors.log` |
| check_em_dash-base | `python3 -B scripts/check_em_dash.py --base 54ce877371ee6e8878cf67294e86c2a8481b62f6` | 0 | 3.12 | `check_em_dash-base.log` |
| check_em_dash-selftest | `python3 -B scripts/check_em_dash.py --selftest` | 0 | 3.07 | `check_em_dash-selftest.log` |
| check_feature_status-self-test | `python3 -B scripts/check_feature_status.py --self-test` | 0 | 0.66 | `check_feature_status-self-test.log` |
| check_doc_style | `python3 -B scripts/check_doc_style.py` | 0 | 0.06 | `check_doc_style.log` |
| check_doc_style-selftest | `python3 -B scripts/check_doc_style.py --selftest` | 0 | 0.06 | `check_doc_style-selftest.log` |
| check_solution_docs | `python3 -B scripts/check_solution_docs.py` | 0 | 0.11 | `check_solution_docs.log` |
| check_solution_docs-selftest | `python3 -B scripts/check_solution_docs.py --selftest` | 0 | 2.42 | `check_solution_docs-selftest.log` |
| check_baremetal_only-check | `python3 -B scripts/check_baremetal_only.py --check` | 0 | 14.84 | `check_baremetal_only-check.log` |
| check_baremetal_only-selftest | `python3 -B scripts/check_baremetal_only.py --selftest` | 0 | 6.63 | `check_baremetal_only-selftest.log` |
| check_py_idiom | `python3 -B scripts/check_py_idiom.py` | 0 | 3.52 | `check_py_idiom.log` |
| check_py_idiom-selftest | `python3 -B scripts/check_py_idiom.py --selftest` | 0 | 3.37 | `check_py_idiom-selftest.log` |
| check_gptp_docs-with-submodule | `python3 -B scripts/check_gptp_docs.py --with-submodule` | 0 | 0.16 | `check_gptp_docs-with-submodule.log` |
| check_gptp_docs-selftest | `python3 -B scripts/check_gptp_docs.py --selftest` | 0 | 0.21 | `check_gptp_docs-selftest.log` |
| check_submodule_docs | `python3 -B scripts/check_submodule_docs.py` | 0 | 0.41 | `check_submodule_docs.log` |
| check_submodule_docs-selftest | `python3 -B scripts/check_submodule_docs.py --selftest` | 0 | 0.06 | `check_submodule_docs-selftest.log` |
| check_archive | `python3 -B scripts/check_archive.py` | 0 | 0.31 | `check_archive.log` |
| check_archive-selftest | `python3 -B scripts/check_archive.py --selftest` | 0 | 0.06 | `check_archive-selftest.log` |
| gen_module_matrix-check | `python3 -B docs/traceability/gen_module_matrix.py --check` | 0 | 0.97 | `gen_module_matrix-check.log` |
| DOC_MAP.gen-check | `python3 -B docs/DOC_MAP.gen.py --check` | 0 | 0.41 | `DOC_MAP.gen-check.log` |
| DOC_MAP.gen-selftest | `python3 -B docs/DOC_MAP.gen.py --selftest` | 0 | 0.46 | `DOC_MAP.gen-selftest.log` |
| timesync_chain.gen-check | `python3 -B docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.36 | `timesync_chain.gen-check.log` |
| timesync_chain.gen-selftest | `python3 -B docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.41 | `timesync_chain.gen-selftest.log` |
| submodule_boundaries.gen-check | `python3 -B docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.41 | `submodule_boundaries.gen-check.log` |
| submodule_boundaries.gen-selftest | `python3 -B docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.51 | `submodule_boundaries.gen-selftest.log` |
| check_diagram_pngs | `python3 -B scripts/check_diagram_pngs.py` | 0 | 0.36 | `check_diagram_pngs.log` |
| check_diagram_pngs-selftest | `python3 -B scripts/check_diagram_pngs.py --selftest` | 0 | 6.73 | `check_diagram_pngs-selftest.log` |
| check_sweep_shape-self-test | `python3 -B scripts/check_sweep_shape.py --self-test` | 0 | 11.84 | `check_sweep_shape-self-test.log` |
| check_deploy_shape-selftest | `python3 -B scripts/check_deploy_shape.py --selftest` | 0 | 0.46 | `check_deploy_shape-selftest.log` |
| gptp-docs | `make -C gptp-processor docs` | 0 | 0.71 | `gptp-docs.log` |
| git-diff-worktree | `git diff --check` | 0 | 0.03 | `git-diff-worktree.log` |
| git-diff-committed | `git diff --check 54ce877371ee6e8878cf67294e86c2a8481b62f6 HEAD` | 0 | 0.03 | `git-diff-committed.log` |
| live-plant-head | `$WORKSPACE_HOME/litex-milan/venv/bin/python -B sw/builder/test_clock_constraints.py --vivado $WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado --checkpoint $WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp --evidence-dir $VALIDATION_STORAGE/607-a408-work/live-plant-350af5dcf` | 0 | 24.16 | `live-plant-head.log` |


Both complete builder banks ran with required elaboration. The compiler-present bank
also required RV32. Both reported the unavailable historical Arty calibration report;
the compiler-absent bank additionally reported the deliberately unavailable compiler
instruments. No required elaboration arm was skipped. `run_builder_absent.py` hides
only the three cross-compiler candidates through subprocess interception, retaining
host compiler probes; it does not alter or copy an SDK. The separate audited absence
control records its attempted compiler calls under the data directory.

The initial committed documentation run caught the reserved `kl_eth` token in the
new procedure name. The final commit renames it to `milan_eth_constraints`; the full
required banks and gates were rerun. No gate exception was added. The HDL reference
export initially refused a Git commit-graph warning, then a reused output directory;
the final run used a process-local `core.commitGraph=false` setting and a fresh
destination. Those refusals and successful reruns are retained, without repository
configuration changes.

The first sweep setup attempt stopped before implementation because the SDK Meson
launcher shadowed the working system Meson. The build-only PATH now prefers system
build utilities while retaining the same RV32 compiler. `sweep-environment-attempt.json`
records those failed setup attempts. The accepted runs used fresh directories.

## Artifact and review status

`sweep-artifacts.json` records sizes and SHA-256 values for the retained checkpoints,
bitstreams, implementation logs, generated constraints and reports. Large artifacts,
installed documentation dependencies and generated reference output remain under
the data path, outside this packet. `documentation-artifacts.json` identifies the
reference export by hash and size. The packet contains no checkpoint, toolchain,
SDK copy, environment, installed package or file over 200 KB.

`sweep-validation-result.json` records the final timing-table validation rc 0;
`final-state.json` records the closing commit, cleanliness, input-hash and packet checks.

Commits have one-line subjects, empty bodies and no trailers. No push, PR mutation,
merge, hardware access or flashing was performed. Independent review remains for
the assigned reviewers; this packet contains author validation, not a review verdict.
