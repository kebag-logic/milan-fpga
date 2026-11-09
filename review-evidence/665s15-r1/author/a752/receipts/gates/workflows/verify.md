| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | changes | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__changes__ci_step_1.log` |
| rtl-fast | changes | scope | Classify the change conservatively | 0 | `rtl-fast__changes__scope.log` |
| rtl-fast | changes | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | verilator-lint | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__verilator-lint__ci_step_1.log` |
| rtl-fast | verilator-lint | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast__verilator-lint__ci_step_2.log` |
| rtl-fast | verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | verilator-lint | ci_step_6 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | 0 | `rtl-fast__verilator-lint__ci_step_7.log` |
| rtl-fast | verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | 0 | `rtl-fast__verilator-lint__ci_step_8.log` |
| rtl-fast | verilator-lint | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | bdd-conformance | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__bdd-conformance__ci_step_1.log` |
| rtl-fast | bdd-conformance | ci_step_3 | Fetch the processor model inputs | 0 | `rtl-fast__bdd-conformance__ci_step_3.log` |
| rtl-fast | bdd-conformance | ci_step_4 | Install behave | 0 | `rtl-fast__bdd-conformance__ci_step_4.log` |
| rtl-fast | bdd-conformance | ci_step_5 | Run the specification-facing suite | 0 | `rtl-fast__bdd-conformance__ci_step_5.log` |
| rtl-fast | bdd-conformance | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | yosys-tool | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__yosys-tool__ci_step_1.log` |
| rtl-fast | yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | yosys-tool | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | yosys-elaboration | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__yosys-elaboration__ci_step_1.log` |
| rtl-fast | yosys-elaboration | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast__yosys-elaboration__ci_step_2.log` |
| rtl-fast | yosys-elaboration | ci_step_4 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl-fast | yosys-elaboration | ci_step_6 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl-fast | yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | 0 | `rtl-fast__yosys-elaboration__ci_step_7.log` |
| rtl-fast | yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | 0 | `rtl-fast__yosys-elaboration__ci_step_8.log` |
| rtl-fast | yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | 0 | `rtl-fast__yosys-elaboration__ci_step_9.log` |
| rtl-fast | yosys-elaboration | ci_step_10 | Prove both synthesis flows refuse active elaboration guards | 0 | `rtl-fast__yosys-elaboration__ci_step_10.log` |
| rtl-fast | yosys-elaboration | ci_step_11 | Prove the result cache refuses a planted entry | 0 | `rtl-fast__yosys-elaboration__ci_step_11.log` |
| rtl-fast | yosys-elaboration | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | publication-census | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__publication-census__ci_step_1.log` |
| rtl-fast | publication-census | ci_step_2 | Set memory-derived census workers | 0 | `rtl-fast__publication-census__ci_step_2.log` |
| rtl-fast | publication-census | ci_step_4 | Fetch RTL dependencies | 0 | `rtl-fast__publication-census__ci_step_4.log` |
| rtl-fast | publication-census | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | publication-census | ci_step_8 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | publication-census | ci_step_9 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl-fast | publication-census | ci_step_11 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl-fast | publication-census | ci_step_12 | Run the publication census in every shape the builder builds | 0 | `rtl-fast__publication-census__ci_step_12.log` |
| rtl-fast | publication-census | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-unit | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-unit__ci_step_1.log` |
| rtl-fast | firmware-unit | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-unit__ci_step_3.log` |
| rtl-fast | firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | 0 | `rtl-fast__firmware-unit__ci_step_7.log` |
| rtl-fast | firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| rtl-fast | firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | 0 | `rtl-fast__firmware-unit__ci_step_10.log` |
| rtl-fast | firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | 0 | `rtl-fast__firmware-unit__ci_step_11.log` |
| rtl-fast | firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | 0 | `rtl-fast__firmware-unit__ci_step_12.log` |
| rtl-fast | firmware-unit | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-control-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-control-mutants__ci_step_1.log` |
| rtl-fast | firmware-control-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-control-mutants__ci_step_3.log` |
| rtl-fast | firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-control-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| rtl-fast | firmware-control-mutants | ci_step_9 | Run the control mutation campaign | 0 | `rtl-fast__firmware-control-mutants__ci_step_9.log` |
| rtl-fast | firmware-control-mutants | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_1.log` |
| rtl-fast | firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_3.log` |
| rtl-fast | firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| rtl-fast | firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| rtl-fast | firmware-aecp-mutants | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-srp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-srp-mutants__ci_step_1.log` |
| rtl-fast | firmware-srp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-srp-mutants__ci_step_3.log` |
| rtl-fast | firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-srp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| rtl-fast | firmware-srp-mutants | ci_step_9 | Run both SRP mutation campaigns and pin controls | 0 | `rtl-fast__firmware-srp-mutants__ci_step_9.log` |
| rtl-fast | firmware-srp-mutants | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-boundary | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-boundary__ci_step_1.log` |
| rtl-fast | firmware-boundary | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-boundary__ci_step_3.log` |
| rtl-fast | firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-boundary | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| rtl-fast | firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | 0 | `rtl-fast__firmware-boundary__ci_step_9.log` |
| rtl-fast | firmware-boundary | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-verilator | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-verilator__ci_step_1.log` |
| rtl-fast | firmware-verilator | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-verilator__ci_step_3.log` |
| rtl-fast | firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-verilator | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-verilator | ci_step_10 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | firmware-verilator | ci_step_11 | Put Verilator on PATH and prove the version | 0 | `rtl-fast__firmware-verilator__ci_step_11.log` |
| rtl-fast | firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| rtl-fast | firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | 0 | `rtl-fast__firmware-verilator__ci_step_14.log` |
| rtl-fast | firmware-verilator | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the aggregate job's CPU budget step, which sets budgets only for that job's verify of the hosted jobs' results, itself not run (below); the jobs it aggregates ran here step by step |
| rtl-fast | rtl-fast | ci_step_2 | Require every applicable fast gate to pass | NOT RUN | requires the hosted jobs' results; each job's steps ran here instead, with their rcs below |
| rtl-fast | rtl-fast | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl-fast | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | elaborate-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate__elaborate-gates-0__ci_step_1.log` |
| elaborate | elaborate-gates-0 | scope | Decide whether this head needs an elaboration | 0 | `elaborate__elaborate-gates-0__scope.log` |
| elaborate | elaborate-gates-0 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `elaborate__elaborate-gates-0__ci_step_4.log` |
| elaborate | elaborate-gates-0 | ci_step_6 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| elaborate | elaborate-gates-0 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv on PATH; the host's LiteX venv is the job's venv here |
| elaborate | elaborate-gates-0 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | pip-installs LiteX at the pinned revisions into the job's venv from the network; the host's LiteX venv carries them |
| elaborate | elaborate-gates-0 | ci_step_13 | Install sbt | NOT RUN | downloads sbt; the CPU netlist is generated offline from the pinned generator (COURSIER_MODE=offline) |
| elaborate | elaborate-gates-0 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source into the job's venv; it would rewrite the shared host venv |
| elaborate | elaborate-gates-0 | ci_step_15 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the job's venv; it would rewrite the shared host venv, which carries the series |
| elaborate | elaborate-gates-0 | ci_step_17 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| elaborate | elaborate-gates-0 | gate_15_0 | Elaboration gates, leg 0 of 2 | 0 | `elaborate__elaborate-gates-0__gate_15_0.log` |
| elaborate | elaborate-gates-0 | ci_step_19 | Keep the generated CPU netlist arguments for the next run | NOT RUN | keeps the generated netlist arguments in the runner's home cache for the next hosted run; no local gate |
| elaborate | elaborate-gates-0 | ci_step_20 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate | elaborate-gates-0 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | elaborate-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate__elaborate-gates-1__ci_step_1.log` |
| elaborate | elaborate-gates-1 | scope | Decide whether this head needs an elaboration | 0 | `elaborate__elaborate-gates-1__scope.log` |
| elaborate | elaborate-gates-1 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `elaborate__elaborate-gates-1__ci_step_4.log` |
| elaborate | elaborate-gates-1 | ci_step_6 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| elaborate | elaborate-gates-1 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv on PATH; the host's LiteX venv is the job's venv here |
| elaborate | elaborate-gates-1 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | pip-installs LiteX at the pinned revisions into the job's venv from the network; the host's LiteX venv carries them |
| elaborate | elaborate-gates-1 | ci_step_13 | Install sbt | NOT RUN | downloads sbt; the CPU netlist is generated offline from the pinned generator (COURSIER_MODE=offline) |
| elaborate | elaborate-gates-1 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source into the job's venv; it would rewrite the shared host venv |
| elaborate | elaborate-gates-1 | ci_step_15 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the job's venv; it would rewrite the shared host venv, which carries the series |
| elaborate | elaborate-gates-1 | ci_step_17 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| elaborate | elaborate-gates-1 | gate_15_1 | Elaboration gates, leg 1 of 2 | 0 | `elaborate__elaborate-gates-1__gate_15_1.log` |
| elaborate | elaborate-gates-1 | ci_packages_17 | Resolve exact package downloads 17 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| elaborate | elaborate-gates-1 | ci_step_22 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| elaborate | elaborate-gates-1 | ci_step_23 | Put Verilator on PATH and prove the version | 0 | `elaborate__elaborate-gates-1__ci_step_23.log` |
| elaborate | elaborate-gates-1 | gate_19 | Standalone LiteX simulation aggregate | 0 | `elaborate__elaborate-gates-1__gate_19.log` |
| elaborate | elaborate-gates-1 | ci_step_25 | Keep the generated CPU netlist arguments for the next run | NOT RUN | keeps the generated netlist arguments in the runner's home cache for the next hosted run; no local gate |
| elaborate | elaborate-gates-1 | ci_step_26 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate | elaborate-gates-1 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | elaborate | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the aggregate job's CPU budget step, which sets budgets only for that job's verify of the hosted jobs' results, itself not run (below); the jobs it aggregates ran here step by step |
| elaborate | elaborate | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only the hosted aggregate's verify uses |
| elaborate | elaborate | ci_step_6 | Require every gate exactly once | NOT RUN | verifies the hosted legs' uploaded receipts; each leg's gates ran here instead |
| elaborate | elaborate | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | full-ci-gate | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__full-ci-gate__ci_step_1.log` |
| rtl | full-ci-gate | target | Print the event and pin the one SHA this run validates | 0 | `rtl__full-ci-gate__target.log` |
| rtl | full-ci-gate | ci_step_4 | Assert the repository default branch is dev | NOT RUN | asks GitHub's API for the default branch with the hosted token |
| rtl | full-ci-gate | ci_step_5 | Hold every workflow file to its contract | 0 | `rtl__full-ci-gate__ci_step_5.log` |
| rtl | full-ci-gate | gate | Decide whether this exact head needs the exhaustive gates | 0 | `rtl__full-ci-gate__gate.log` |
| rtl | full-ci-gate | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | verilator-shards | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_step_2 | Fetch RTL dependencies | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_step_3 | Record the tree this worker validates | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | verilator-shards | ci_step_7 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl | verilator-shards | ci_step_8 | Put Verilator on PATH and prove the version | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_step_9 | Prove specialized suite ownership | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_packages_8 | Resolve exact package downloads 8 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | verilator-shards | ci_step_13 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl | verilator-shards | ci_packages_9 | Resolve exact package downloads 9 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | verilator-shards | ci_step_16 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | verilator-shards | ci_step_18 | Install sv2v for the netlist-level suite owner | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl | verilator-shards | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_step_21 | Run this exhaustive suite shard | NOT RUN | the 19 hosted workers' suites run here as the full sweep, four native-shards units of scripts/run_all_suites.sh (gates/sweep) |
| rtl | verilator-shards | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | physical-gptp | ci_step_1 | Set CPU-derived job budgets | NOT RUN | runs only on a schedule or a manual dispatch (rtl.yml: its if), never on a pull request |
| rtl | physical-gptp | ci_step_3 | Fetch RTL dependencies | NOT RUN | runs only on a schedule or a manual dispatch (rtl.yml: its if), never on a pull request |
| rtl | physical-gptp | ci_step_4 | Record the tree this worker validates | NOT RUN | runs only on a schedule or a manual dispatch (rtl.yml: its if), never on a pull request |
| rtl | physical-gptp | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | physical-gptp | ci_step_8 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl | physical-gptp | ci_step_9 | Put Verilator on PATH and prove the version | NOT RUN | runs only on a schedule or a manual dispatch (rtl.yml: its if), never on a pull request |
| rtl | physical-gptp | ci_step_10 | Prove physical suite selection | NOT RUN | runs only on a schedule or a manual dispatch (rtl.yml: its if), never on a pull request |
| rtl | physical-gptp | ci_step_11 | Run the physical gPTP suite with its own deadline | NOT RUN | runs only on a schedule or a manual dispatch (rtl.yml: its if), never on a pull request |
| rtl | physical-gptp | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | verilator-suites | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | verilator-suites | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | verilator-suites | ci_step_5 | Require every shard to have validated this run's SHA | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | verilator-suites | ci_step_6 | Prove exhaustive ownership and tally every log | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | verilator-suites | ci_step_7 | Require every Verilator worker to pass | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | verilator-suites | ci_step_8 | Require every case union to succeed | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | verilator-suites | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | yosys-shards-0-4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__yosys-shards-0-4__ci_step_1.log` |
| rtl | yosys-shards-0-4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl__yosys-shards-0-4__ci_step_2.log` |
| rtl | yosys-shards-0-4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl__yosys-shards-0-4__ci_step_3.log` |
| rtl | yosys-shards-0-4 | ci_step_5 | Restore the pinned Yosys build | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-0-4 | ci_packages_5 | Resolve exact package downloads 5 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | yosys-shards-0-4 | ci_step_8 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-0-4 | ci_step_10 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl | yosys-shards-0-4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl__yosys-shards-0-4__ci_step_12.log` |
| rtl | yosys-shards-0-4 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | yosys-shards-1-4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__yosys-shards-1-4__ci_step_1.log` |
| rtl | yosys-shards-1-4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl__yosys-shards-1-4__ci_step_2.log` |
| rtl | yosys-shards-1-4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl__yosys-shards-1-4__ci_step_3.log` |
| rtl | yosys-shards-1-4 | ci_step_5 | Restore the pinned Yosys build | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-1-4 | ci_packages_5 | Resolve exact package downloads 5 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | yosys-shards-1-4 | ci_step_8 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-1-4 | ci_step_10 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl | yosys-shards-1-4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl__yosys-shards-1-4__ci_step_12.log` |
| rtl | yosys-shards-1-4 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | yosys-shards-2-4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__yosys-shards-2-4__ci_step_1.log` |
| rtl | yosys-shards-2-4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl__yosys-shards-2-4__ci_step_2.log` |
| rtl | yosys-shards-2-4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl__yosys-shards-2-4__ci_step_3.log` |
| rtl | yosys-shards-2-4 | ci_step_5 | Restore the pinned Yosys build | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-2-4 | ci_packages_5 | Resolve exact package downloads 5 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | yosys-shards-2-4 | ci_step_8 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-2-4 | ci_step_10 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl | yosys-shards-2-4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl__yosys-shards-2-4__ci_step_12.log` |
| rtl | yosys-shards-2-4 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | yosys-shards-3-4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__yosys-shards-3-4__ci_step_1.log` |
| rtl | yosys-shards-3-4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl__yosys-shards-3-4__ci_step_2.log` |
| rtl | yosys-shards-3-4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl__yosys-shards-3-4__ci_step_3.log` |
| rtl | yosys-shards-3-4 | ci_step_5 | Restore the pinned Yosys build | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-3-4 | ci_packages_5 | Resolve exact package downloads 5 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | yosys-shards-3-4 | ci_step_8 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl | yosys-shards-3-4 | ci_step_10 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl | yosys-shards-3-4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl__yosys-shards-3-4__ci_step_12.log` |
| rtl | yosys-shards-3-4 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | yosys-portability | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | yosys-portability | ci_step_3 | Require every shard to have validated this run's SHA | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | yosys-portability | ci_step_4 | Reconcile the live inventory and structural gates | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | yosys-portability | ci_step_5 | Require every Yosys worker to pass | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | yosys-portability | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | yosys-tool | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__yosys-tool__ci_step_1.log` |
| rtl | yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl | yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl | yosys-tool | ci_step_6 | Package the pinned Yosys build | NOT RUN | packages the hosted /opt/yosys build for the shards; no /opt/yosys here |
| rtl | yosys-tool | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | union-milan_dp | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | union-milan_dp_mclk | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp_mclk | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp_mclk | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp_mclk | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | union-capture_coherence | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-capture_coherence | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-capture_coherence | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-capture_coherence | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | union-maap | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-maap | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-maap | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-maap | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | union-milan_dp_render | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp_render | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp_render | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-milan_dp_render | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | union-pp_shadow | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-pp_shadow | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-pp_shadow | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | collects and reconciles the hosted workers' uploaded artifacts; the local runs' own tallies stand instead |
| rtl | union-pp_shadow | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| rtl | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| docs | wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | `docs__wire-accountability__ci_step_1.log` |
| docs | wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | `docs__wire-accountability__ci_step_3.log` |
| docs | wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | `docs__wire-accountability__ci_step_4.log` |
| docs | wire-accountability | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 | `docs__docs-check-no-git__ci_step_1.log` |
| docs | docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | `docs__docs-check-no-git__ci_step_2.log` |
| docs | docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | `docs__docs-check-no-git__ci_step_3.log` |
| docs | docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs__docs-gates-0__ci_step_1.log` |
| docs | docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | `docs__docs-gates-0__gate_1.log` |
| docs | docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | `docs__docs-gates-0__ci_step_5.log` |
| docs | docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | `docs__docs-gates-0__ci_step_7.log` |
| docs | docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| docs | docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs | docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | `docs__docs-gates-0__gate_7.log` |
| docs | docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | `docs__docs-gates-0__gate_8.log` |
| docs | docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | `docs__docs-gates-0__gate_9.log` |
| docs | docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | `docs__docs-gates-0__gate_10.log` |
| docs | docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | `docs__docs-gates-0__gate_11.log` |
| docs | docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | `docs__docs-gates-0__gate_12.log` |
| docs | docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | `docs__docs-gates-0__gate_13.log` |
| docs | docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | `docs__docs-gates-0__gate_14.log` |
| docs | docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | `docs__docs-gates-0__gate_15.log` |
| docs | docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | `docs__docs-gates-0__gate_16.log` |
| docs | docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | `docs__docs-gates-0__ci_step_21.log` |
| docs | docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | `docs__docs-gates-0__gate_18.log` |
| docs | docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | `docs__docs-gates-0__gate_19.log` |
| docs | docs-gates-0 | ci_step_25 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs | docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | `docs__docs-gates-0__gate_21.log` |
| docs | docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| docs | docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | `docs__docs-gates-0__gate_24.log` |
| docs | docs-gates-0 | gate_26 | NVM record-space gate | 0 | `docs__docs-gates-0__gate_26.log` |
| docs | docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | `docs__docs-gates-0__gate_27.log` |
| docs | docs-gates-0 | gate_28 | Saved-state writer gate | 0 | `docs__docs-gates-0__gate_28.log` |
| docs | docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | `docs__docs-gates-0__gate_29.log` |
| docs | docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | `docs__docs-gates-0__gate_30.log` |
| docs | docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | `docs__docs-gates-0__gate_31.log` |
| docs | docs-gates-0 | gate_32 | Port contract gate | 0 | `docs__docs-gates-0__gate_32.log` |
| docs | docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | `docs__docs-gates-0__gate_33.log` |
| docs | docs-gates-0 | gate_34 | TODO ownership gate | 0 | `docs__docs-gates-0__gate_34.log` |
| docs | docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | `docs__docs-gates-0__gate_35.log` |
| docs | docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | `docs__docs-gates-0__gate_36.log` |
| docs | docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | `docs__docs-gates-0__gate_37.log` |
| docs | docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | `docs__docs-gates-0__gate_38.log` |
| docs | docs-gates-0 | gate_39 | Python idiom gate | 0 | `docs__docs-gates-0__gate_39.log` |
| docs | docs-gates-0 | gate_40 | Shell idiom gate | 0 | `docs__docs-gates-0__gate_40.log` |
| docs | docs-gates-0 | gate_43 | Doc cited-path gate | 0 | `docs__docs-gates-0__gate_43.log` |
| docs | docs-gates-0 | gate_44 | Archive integrity gate | 0 | `docs__docs-gates-0__gate_44.log` |
| docs | docs-gates-0 | gate_45 | Per-page contents gate | 0 | `docs__docs-gates-0__gate_45.log` |
| docs | docs-gates-0 | gate_46 | AEM store generator self-test | 0 | `docs__docs-gates-0__gate_46.log` |
| docs | docs-gates-0 | gate_47 | Sweep/build shape gate | 0 | `docs__docs-gates-0__gate_47.log` |
| docs | docs-gates-0 | gate_48 | Deploy shape gate | 0 | `docs__docs-gates-0__gate_48.log` |
| docs | docs-gates-0 | gate_49 | Entity shape gate | 0 | `docs__docs-gates-0__gate_49.log` |
| docs | docs-gates-0 | ci_step_52 | Fetch inventory dependencies | 0 | `docs__docs-gates-0__ci_step_52.log` |
| docs | docs-gates-0 | gate_50 | CI scheduling and evidence controls | 0 | `docs__docs-gates-0__gate_50.log` |
| docs | docs-gates-0 | ci_step_54 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs | docs-gates-0 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs__docs-gates-1__ci_step_1.log` |
| docs | docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 | `docs__docs-gates-1__ci_step_3.log` |
| docs | docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs__docs-gates-1__ci_step_5.log` |
| docs | docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs | docs-gates-1 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs | docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs__docs-gates-1__ci_step_9.log` |
| docs | docs-gates-1 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs | docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| docs | docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | `docs__docs-gates-1__gate_25_0.log` |
| docs | docs-gates-1 | ci_step_15 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs | docs-gates-1 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs__docs-gates-2__ci_step_1.log` |
| docs | docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 | `docs__docs-gates-2__ci_step_3.log` |
| docs | docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs__docs-gates-2__ci_step_5.log` |
| docs | docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs | docs-gates-2 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs | docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs__docs-gates-2__ci_step_9.log` |
| docs | docs-gates-2 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs | docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME; the pinned SDK is this host's <rv32-sdk>/host, on PATH |
| docs | docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | `docs__docs-gates-2__gate_25_1.log` |
| docs | docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | `docs__docs-gates-2__gate_41.log` |
| docs | docs-gates-2 | gate_42 | Local act runner contract gate | 0 | `docs__docs-gates-2__gate_42.log` |
| docs | docs-gates-2 | ci_step_17 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs | docs-gates-2 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | docs-check | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the aggregate job's CPU budget step, which sets budgets only for that job's verify of the hosted jobs' results, itself not run (below); the jobs it aggregates ran here step by step |
| docs | docs-check | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only docs-check's hosted verify uses |
| docs | docs-check | ci_step_6 | Require every gate exactly once | NOT RUN | verifies uploaded hosted receipts; this job's gates ran above |
| docs | docs-check | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| docs | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration, no local gate |
| docs | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration, no local gate |
| docs | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | reads a hosted run's artifacts |
| docs | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| docs | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | watches a hosted run |
| docs | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | cancels a hosted run |
| docs | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| docs | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| docs | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | cancels a hosted run |

136 steps ran, 221 not run with a reason, 0 bad
