| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | rtl-fast.changes | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.changes__ci_step_1.log` |
| rtl-fast | rtl-fast.changes | scope | Classify the change conservatively | 0 | `rtl-fast.changes__scope.log` |
| rtl-fast | changes | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.verilator-lint | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.verilator-lint__ci_step_1.log` |
| rtl-fast | rtl-fast.verilator-lint | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast.verilator-lint__ci_step_2.log` |
| rtl-fast | verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | verilator-lint | ci_step_6 | Build Verilator from source on cache miss | NOT RUN | builds the hosted /opt Verilator; the pinned Verilator 5.050 is on PATH here |
| rtl-fast | rtl-fast.verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | 0 | `rtl-fast.verilator-lint__ci_step_7.log` |
| rtl-fast | rtl-fast.verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | 0 | `rtl-fast.verilator-lint__ci_step_8.log` |
| rtl-fast | verilator-lint | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.bdd-conformance | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.bdd-conformance__ci_step_1.log` |
| rtl-fast | rtl-fast.bdd-conformance | ci_step_3 | Fetch the processor model inputs | 0 | `rtl-fast.bdd-conformance__ci_step_3.log` |
| rtl-fast | rtl-fast.bdd-conformance | ci_step_4 | Install behave | 0 | `rtl-fast.bdd-conformance__ci_step_4.log` |
| rtl-fast | rtl-fast.bdd-conformance | ci_step_5 | Run the specification-facing suite | 0 | `rtl-fast.bdd-conformance__ci_step_5.log` |
| rtl-fast | bdd-conformance | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.yosys-tool | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.yosys-tool__ci_step_1.log` |
| rtl-fast | yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl-fast | yosys-tool | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.yosys-elaboration__ci_step_1.log` |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast.yosys-elaboration__ci_step_2.log` |
| rtl-fast | yosys-elaboration | ci_step_4 | Install the pinned Yosys and prove the version | NOT RUN | sudo links /opt/yosys into /usr/local/bin; the host's Yosys 0.66 is on PATH (yosys -V in the substitute log) |
| rtl-fast | yosys-elaboration | ci_step_6 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | 0 | `rtl-fast.yosys-elaboration__ci_step_7.log` |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | 0 | `rtl-fast.yosys-elaboration__ci_step_8.log` |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | 0 | `rtl-fast.yosys-elaboration__ci_step_9.log` |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_10 | Prove both synthesis flows refuse active elaboration guards | 0 | `rtl-fast.yosys-elaboration__ci_step_10.log` |
| rtl-fast | rtl-fast.yosys-elaboration | ci_step_11 | Prove the result cache refuses a planted entry | 0 | `rtl-fast.yosys-elaboration__ci_step_11.log` |
| rtl-fast | yosys-elaboration | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.publication-census | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.publication-census__ci_step_1.log` |
| rtl-fast | rtl-fast.publication-census | ci_step_2 | Set memory-derived census workers | 0 | `rtl-fast.publication-census__ci_step_2.log` |
| rtl-fast | rtl-fast.publication-census | ci_step_4 | Fetch RTL dependencies | 0 | `rtl-fast.publication-census__ci_step_4.log` |
| rtl-fast | publication-census | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | publication-census | ci_step_8 | Build Yosys from source on cache miss | NOT RUN | builds the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl-fast | publication-census | ci_step_9 | Install the pinned Yosys and prove the version | NOT RUN | sudo links /opt/yosys into /usr/local/bin; the host's Yosys 0.66 is on PATH (yosys -V in the substitute log) |
| rtl-fast | publication-census | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| rtl-fast | rtl-fast.publication-census | ci_step_12 | Run the publication census in every shape the builder builds | 0 | `rtl-fast.publication-census__ci_step_12.log` |
| rtl-fast | publication-census | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.split-cdc | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.split-cdc__ci_step_1.log` |
| rtl-fast | rtl-fast.split-cdc | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast.split-cdc__ci_step_2.log` |
| rtl-fast | split-cdc | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | split-cdc | ci_step_6 | Build Yosys from source on cache miss | NOT RUN | builds the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl-fast | split-cdc | ci_step_7 | Install the pinned Yosys and prove the version | NOT RUN | sudo links /opt/yosys into /usr/local/bin; the host's Yosys 0.66 is on PATH (yosys -V in the substitute log) |
| rtl-fast | split-cdc | ci_step_9 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| rtl-fast | rtl-fast.split-cdc | ci_step_10 | Prove every split crossing goes through an approved primitive | 0 | `rtl-fast.split-cdc__ci_step_10.log` |
| rtl-fast | split-cdc | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.firmware-unit | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.firmware-unit__ci_step_1.log` |
| rtl-fast | rtl-fast.firmware-unit | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast.firmware-unit__ci_step_3.log` |
| rtl-fast | firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get; GoogleTest and GoogleMock 1.18.0 are installed on this host |
| rtl-fast | rtl-fast.firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | 0 | `rtl-fast.firmware-unit__ci_step_7.log` |
| rtl-fast | rtl-fast.firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast.firmware-unit__ci_step_9.log` |
| rtl-fast | rtl-fast.firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | 0 | `rtl-fast.firmware-unit__ci_step_10.log` |
| rtl-fast | rtl-fast.firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | 0 | `rtl-fast.firmware-unit__ci_step_11.log` |
| rtl-fast | rtl-fast.firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | 0 | `rtl-fast.firmware-unit__ci_step_12.log` |
| rtl-fast | firmware-unit | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.firmware-control-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.firmware-control-mutants__ci_step_1.log` |
| rtl-fast | rtl-fast.firmware-control-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast.firmware-control-mutants__ci_step_3.log` |
| rtl-fast | firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-control-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get; GoogleTest and GoogleMock 1.18.0 are installed on this host |
| rtl-fast | rtl-fast.firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast.firmware-control-mutants__ci_step_8.log` |
| rtl-fast | rtl-fast.firmware-control-mutants | ci_step_9 | Run the control mutation campaign | 0 | `rtl-fast.firmware-control-mutants__ci_step_9.log` |
| rtl-fast | firmware-control-mutants | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.firmware-aecp-mutants__ci_step_1.log` |
| rtl-fast | rtl-fast.firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast.firmware-aecp-mutants__ci_step_3.log` |
| rtl-fast | firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get; GoogleTest and GoogleMock 1.18.0 are installed on this host |
| rtl-fast | rtl-fast.firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast.firmware-aecp-mutants__ci_step_8.log` |
| rtl-fast | rtl-fast.firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | 0 | `rtl-fast.firmware-aecp-mutants__ci_step_9.log` |
| rtl-fast | firmware-aecp-mutants | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.firmware-srp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.firmware-srp-mutants__ci_step_1.log` |
| rtl-fast | rtl-fast.firmware-srp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast.firmware-srp-mutants__ci_step_3.log` |
| rtl-fast | firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-srp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get; GoogleTest and GoogleMock 1.18.0 are installed on this host |
| rtl-fast | rtl-fast.firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast.firmware-srp-mutants__ci_step_8.log` |
| rtl-fast | rtl-fast.firmware-srp-mutants | ci_step_9 | Run both SRP mutation campaigns and pin controls | 0 | `rtl-fast.firmware-srp-mutants__ci_step_9.log` |
| rtl-fast | firmware-srp-mutants | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.firmware-boundary | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.firmware-boundary__ci_step_1.log` |
| rtl-fast | rtl-fast.firmware-boundary | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast.firmware-boundary__ci_step_3.log` |
| rtl-fast | firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-boundary | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get; GoogleTest and GoogleMock 1.18.0 are installed on this host |
| rtl-fast | rtl-fast.firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast.firmware-boundary__ci_step_8.log` |
| rtl-fast | rtl-fast.firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | 0 | `rtl-fast.firmware-boundary__ci_step_9.log` |
| rtl-fast | firmware-boundary | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.firmware-verilator | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.firmware-verilator__ci_step_1.log` |
| rtl-fast | rtl-fast.firmware-verilator | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast.firmware-verilator__ci_step_3.log` |
| rtl-fast | firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-verilator | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get; GoogleTest and GoogleMock 1.18.0 are installed on this host |
| rtl-fast | firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl-fast | firmware-verilator | ci_step_10 | Build Verilator from source on cache miss | NOT RUN | builds the hosted /opt Verilator; the pinned Verilator 5.050 is on PATH here |
| rtl-fast | rtl-fast.firmware-verilator | ci_step_11 | Put Verilator on PATH and prove the version | 0 | `rtl-fast.firmware-verilator__ci_step_11.log` |
| rtl-fast | rtl-fast.firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast.firmware-verilator__ci_step_13.log` |
| rtl-fast | rtl-fast.firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | 0 | `rtl-fast.firmware-verilator__ci_step_14.log` |
| rtl-fast | firmware-verilator | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | rtl-fast.rtl-fast | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast.rtl-fast__ci_step_1.log` |
| rtl-fast | rtl-fast | ci_step_2 | Require every applicable fast gate to pass | NOT RUN | aggregates the hosted jobs' results (needs context); every job's steps are in this table |
| rtl-fast | rtl-fast | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl-fast | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | elaborate.elaborate-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate.elaborate-gates-0__ci_step_1.log` |
| elaborate | elaborate.elaborate-gates-0 | scope | Decide whether this head needs an elaboration | 0 | `elaborate.elaborate-gates-0__scope.log` |
| elaborate | elaborate.elaborate-gates-0 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `elaborate.elaborate-gates-0__ci_step_4.log` |
| elaborate | elaborate-gates-0 | ci_step_6 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| elaborate | elaborate-gates-0 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | the LiteX interpreter is the prepared venv (<litex>/venv), first on PATH |
| elaborate | elaborate-gates-0 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | the prepared LiteX venv carries the pinned revisions; installing would change a shared venv |
| elaborate | elaborate-gates-0 | ci_step_13 | Install sbt | NOT RUN | the prepared LiteX venv's VexiiRiscv netlists are generated already; no sbt build runs here |
| elaborate | elaborate-gates-0 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | copies netlist arguments into the shared LiteX venv; ci_litex_env.py runs as a substitute (litex-env log) |
| elaborate | elaborate-gates-0 | ci_step_15 | Apply the toolchain patch series | NOT RUN | patches the LiteX tree in place; the shared venv is patched already and is not changed here |
| elaborate | elaborate.elaborate-gates-0 | ci_step_17 | Install and verify the pinned RV32 SDK | 0 | `elaborate.elaborate-gates-0__ci_step_17.log` |
| elaborate | elaborate.elaborate-gates-0 | gate_15_0 | Elaboration gates, leg 0 of 2 | 0 | `elaborate.elaborate-gates-0__gate_15_0.log` |
| elaborate | elaborate-gates-0 | ci_step_19 | Keep the generated CPU netlist arguments for the next run | NOT RUN | a hosted cache step: copies the venv's netlist arguments into the runner's home |
| elaborate | elaborate-gates-0 | ci_step_20 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate | elaborate-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| elaborate | elaborate.elaborate-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate.elaborate-gates-1__ci_step_1.log` |
| elaborate | elaborate.elaborate-gates-1 | scope | Decide whether this head needs an elaboration | 0 | `elaborate.elaborate-gates-1__scope.log` |
| elaborate | elaborate.elaborate-gates-1 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `elaborate.elaborate-gates-1__ci_step_4.log` |
| elaborate | elaborate-gates-1 | ci_step_6 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| elaborate | elaborate-gates-1 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | the LiteX interpreter is the prepared venv (<litex>/venv), first on PATH |
| elaborate | elaborate-gates-1 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | the prepared LiteX venv carries the pinned revisions; installing would change a shared venv |
| elaborate | elaborate-gates-1 | ci_step_13 | Install sbt | NOT RUN | the prepared LiteX venv's VexiiRiscv netlists are generated already; no sbt build runs here |
| elaborate | elaborate-gates-1 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | copies netlist arguments into the shared LiteX venv; ci_litex_env.py runs as a substitute (litex-env log) |
| elaborate | elaborate-gates-1 | ci_step_15 | Apply the toolchain patch series | NOT RUN | patches the LiteX tree in place; the shared venv is patched already and is not changed here |
| elaborate | elaborate.elaborate-gates-1 | ci_step_17 | Install and verify the pinned RV32 SDK | 0 | `elaborate.elaborate-gates-1__ci_step_17.log` |
| elaborate | elaborate.elaborate-gates-1 | gate_15_1 | Elaboration gates, leg 1 of 2 | 0 | `elaborate.elaborate-gates-1__gate_15_1.log` |
| elaborate | elaborate-gates-1 | ci_packages_17 | Resolve exact package downloads 17 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| elaborate | elaborate-gates-1 | ci_step_22 | Build Verilator from source on cache miss | NOT RUN | builds the hosted /opt Verilator; the pinned Verilator 5.050 is on PATH here |
| elaborate | elaborate.elaborate-gates-1 | ci_step_23 | Put Verilator on PATH and prove the version | 0 | `elaborate.elaborate-gates-1__ci_step_23.log` |
| elaborate | elaborate.elaborate-gates-1 | gate_19 | Standalone LiteX simulation aggregate | 0 | `elaborate.elaborate-gates-1__gate_19.log` |
| elaborate | elaborate-gates-1 | ci_step_25 | Keep the generated CPU netlist arguments for the next run | NOT RUN | a hosted cache step: copies the venv's netlist arguments into the runner's home |
| elaborate | elaborate-gates-1 | ci_step_26 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate | elaborate-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| elaborate | elaborate.elaborate | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate.elaborate__ci_step_1.log` |
| elaborate | elaborate | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only the hosted verify and manifest steps use |
| elaborate | elaborate | ci_step_6 | Require every gate exactly once | NOT RUN | verifies the hosted jobs' uploaded receipts; this table is the local equivalent |
| elaborate | elaborate | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| elaborate | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| elaborate | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | rtl.full-ci-gate | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl.full-ci-gate__ci_step_1.log` |
| rtl | rtl.full-ci-gate | target | Print the event and pin the one SHA this run validates | 0 | `rtl.full-ci-gate__target.log` |
| rtl | full-ci-gate | ci_step_4 | Assert the repository default branch is dev | NOT RUN | queries the repository through the hosted token |
| rtl | rtl.full-ci-gate | ci_step_5 | Hold every workflow file to its contract | 0 | `rtl.full-ci-gate__ci_step_5.log` |
| rtl | rtl.full-ci-gate | gate | Decide whether this exact head needs the exhaustive gates | 0 | `rtl.full-ci-gate__gate.log` |
| rtl | full-ci-gate | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | verilator-shards | ci_step_1 | Set CPU-derived job budgets | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_step_2 | Fetch RTL dependencies | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_step_3 | Record the tree this worker validates | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | verilator-shards | ci_step_7 | Build Verilator from source on cache miss | NOT RUN | builds the hosted /opt Verilator; the pinned Verilator 5.050 is on PATH here |
| rtl | verilator-shards | ci_step_8 | Put Verilator on PATH and prove the version | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_step_9 | Prove specialized suite ownership | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_packages_8 | Resolve exact package downloads 8 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | verilator-shards | ci_step_13 | Build Yosys from source on cache miss | NOT RUN | builds the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl | verilator-shards | ci_packages_9 | Resolve exact package downloads 9 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | verilator-shards | ci_step_16 | Install the pinned Yosys and prove the version | NOT RUN | sudo links /opt/yosys into /usr/local/bin; the host's Yosys 0.66 is on PATH (yosys -V in the substitute log) |
| rtl | verilator-shards | ci_step_18 | Install sv2v for the netlist-level suite owner | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| rtl | verilator-shards | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_step_21 | Run this exhaustive suite shard | NOT RUN | replicated by the full sweep as four native shard units (receipts/sweep), the hosted 19-way split of the same suites; run at b6a60fbd, whose tree every sweep suite reads is unchanged at 7c97e99f (SUMMARY.md) |
| rtl | verilator-shards | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | physical-gptp | ci_step_1 | Set CPU-derived job budgets | NOT RUN | not triggered by a pull_request: the physical gPTP job runs nightly and on manual dispatch |
| rtl | physical-gptp | ci_step_3 | Fetch RTL dependencies | NOT RUN | not triggered by a pull_request: the physical gPTP job runs nightly and on manual dispatch |
| rtl | physical-gptp | ci_step_4 | Record the tree this worker validates | NOT RUN | not triggered by a pull_request: the physical gPTP job runs nightly and on manual dispatch |
| rtl | physical-gptp | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | physical-gptp | ci_step_8 | Build Verilator from source on cache miss | NOT RUN | builds the hosted /opt Verilator; the pinned Verilator 5.050 is on PATH here |
| rtl | physical-gptp | ci_step_9 | Put Verilator on PATH and prove the version | NOT RUN | not triggered by a pull_request: the physical gPTP job runs nightly and on manual dispatch |
| rtl | physical-gptp | ci_step_10 | Prove physical suite selection | NOT RUN | not triggered by a pull_request: the physical gPTP job runs nightly and on manual dispatch |
| rtl | physical-gptp | ci_step_11 | Run the physical gPTP suite with its own deadline | NOT RUN | not triggered by a pull_request: the physical gPTP job runs nightly and on manual dispatch |
| rtl | physical-gptp | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | verilator-suites | ci_step_1 | Set CPU-derived job budgets | NOT RUN | collects the hosted shards' uploaded logs; the native sweep's summary is the local equivalent |
| rtl | verilator-suites | ci_step_2 | Fetch inventory dependencies | NOT RUN | collects the hosted shards' uploaded logs; the native sweep's summary is the local equivalent |
| rtl | verilator-suites | ci_step_5 | Require every shard to have validated this run's SHA | NOT RUN | collects the hosted shards' uploaded logs; the native sweep's summary is the local equivalent |
| rtl | verilator-suites | ci_step_6 | Prove exhaustive ownership and tally every log | NOT RUN | collects the hosted shards' uploaded logs; the native sweep's summary is the local equivalent |
| rtl | verilator-suites | ci_step_7 | Require every Verilator worker to pass | NOT RUN | collects the hosted shards' uploaded logs; the native sweep's summary is the local equivalent |
| rtl | verilator-suites | ci_step_8 | Require every case union to succeed | NOT RUN | collects the hosted shards' uploaded logs; the native sweep's summary is the local equivalent |
| rtl | verilator-suites | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | rtl.yosys-shards.0of4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl.yosys-shards.0of4__ci_step_1.log` |
| rtl | rtl.yosys-shards.1of4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl.yosys-shards.1of4__ci_step_1.log` |
| rtl | rtl.yosys-shards.2of4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl.yosys-shards.2of4__ci_step_1.log` |
| rtl | rtl.yosys-shards.3of4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl.yosys-shards.3of4__ci_step_1.log` |
| rtl | rtl.yosys-shards.0of4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl.yosys-shards.0of4__ci_step_2.log` |
| rtl | rtl.yosys-shards.1of4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl.yosys-shards.1of4__ci_step_2.log` |
| rtl | rtl.yosys-shards.2of4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl.yosys-shards.2of4__ci_step_2.log` |
| rtl | rtl.yosys-shards.3of4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl.yosys-shards.3of4__ci_step_2.log` |
| rtl | rtl.yosys-shards.0of4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl.yosys-shards.0of4__ci_step_3.log` |
| rtl | rtl.yosys-shards.1of4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl.yosys-shards.1of4__ci_step_3.log` |
| rtl | rtl.yosys-shards.2of4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl.yosys-shards.2of4__ci_step_3.log` |
| rtl | rtl.yosys-shards.3of4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl.yosys-shards.3of4__ci_step_3.log` |
| rtl | yosys-shards | ci_step_5 | Restore the pinned Yosys build | NOT RUN | sudo unpacks the hosted Yosys into /opt; the host's Yosys 0.66 is on PATH |
| rtl | yosys-shards | ci_packages_5 | Resolve exact package downloads 5 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | yosys-shards | ci_step_8 | Install the pinned Yosys and prove the version | NOT RUN | sudo links /opt/yosys into /usr/local/bin; the host's Yosys 0.66 is on PATH (yosys -V in the substitute log) |
| rtl | yosys-shards | ci_step_10 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| rtl | rtl.yosys-shards.0of4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl.yosys-shards.0of4__ci_step_12.log` |
| rtl | rtl.yosys-shards.1of4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl.yosys-shards.1of4__ci_step_12.log` |
| rtl | rtl.yosys-shards.2of4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl.yosys-shards.2of4__ci_step_12.log` |
| rtl | rtl.yosys-shards.3of4 | ci_step_12 | Run this weighted portability shard | 0 | `rtl.yosys-shards.3of4__ci_step_12.log` |
| rtl | yosys-shards | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | rtl.yosys-portability | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl.yosys-portability__ci_step_1.log` |
| rtl | yosys-portability | ci_step_3 | Require every shard to have validated this run's SHA | NOT RUN | requires the hosted shards' uploaded results |
| rtl | yosys-portability | ci_step_4 | Reconcile the live inventory and structural gates | NOT RUN | reconciles the hosted shards' uploaded results; each shard's own run is in this table |
| rtl | yosys-portability | ci_step_5 | Require every Yosys worker to pass | NOT RUN | aggregates the hosted shards' results (needs context) |
| rtl | yosys-portability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | yosys-tool | ci_step_1 | Set CPU-derived job budgets | NOT RUN | builds and packages the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl | yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl | yosys-tool | ci_step_6 | Package the pinned Yosys build | NOT RUN | packages the hosted /opt Yosys build for the shards; the host's Yosys 0.66 is on PATH |
| rtl | yosys-tool | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | union-milan_dp | ci_step_1 | Set CPU-derived job budgets | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp | ci_step_2 | Fetch inventory dependencies | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | union-milan_dp_mclk | ci_step_1 | Set CPU-derived job budgets | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp_mclk | ci_step_2 | Fetch inventory dependencies | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp_mclk | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp_mclk | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | union-capture_coherence | ci_step_1 | Set CPU-derived job budgets | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-capture_coherence | ci_step_2 | Fetch inventory dependencies | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-capture_coherence | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-capture_coherence | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | union-maap | ci_step_1 | Set CPU-derived job budgets | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-maap | ci_step_2 | Fetch inventory dependencies | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-maap | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-maap | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | union-milan_dp_render | ci_step_1 | Set CPU-derived job budgets | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp_render | ci_step_2 | Fetch inventory dependencies | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp_render | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-milan_dp_render | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | union-pp_shadow | ci_step_1 | Set CPU-derived job budgets | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-pp_shadow | ci_step_2 | Fetch inventory dependencies | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-pp_shadow | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | joins the hosted shards' uploaded case receipts; the native sweep ran every case |
| rtl | union-pp_shadow | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| rtl | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | docs.wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | `docs.wire-accountability__ci_step_1.log` |
| docs | docs.wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | `docs.wire-accountability__ci_step_3.log` |
| docs | docs.wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | `docs.wire-accountability__ci_step_4.log` |
| docs | wire-accountability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs | docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | NOT RUN | writes the hosted job-source evidence; the next step strips .git in the clone and runs its gates |
| docs | docs.docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | `docs.docs-check-no-git__ci_step_2.log` |
| docs | docs.docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | `docs.docs-check-no-git__ci_step_3.log` |
| docs | docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs | docs.docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs.docs-gates-0__ci_step_1.log` |
| docs | docs.docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | `docs.docs-gates-0__gate_1.log` |
| docs | docs.docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | `docs.docs-gates-0__ci_step_5.log` |
| docs | docs.docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | `docs.docs-gates-0__ci_step_7.log` |
| docs | docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| docs | docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs | docs.docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | `docs.docs-gates-0__gate_7.log` |
| docs | docs.docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | `docs.docs-gates-0__gate_8.log` |
| docs | docs.docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | `docs.docs-gates-0__gate_9.log` |
| docs | docs.docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | `docs.docs-gates-0__gate_10.log` |
| docs | docs.docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | `docs.docs-gates-0__gate_11.log` |
| docs | docs.docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | `docs.docs-gates-0__gate_12.log` |
| docs | docs.docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | `docs.docs-gates-0__gate_13.log` |
| docs | docs.docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | `docs.docs-gates-0__gate_14.log` |
| docs | docs.docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | `docs.docs-gates-0__gate_15.log` |
| docs | docs.docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | `docs.docs-gates-0__gate_16.log` |
| docs | docs.docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | `docs.docs-gates-0__ci_step_21.log` |
| docs | docs.docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | `docs.docs-gates-0__gate_18.log` |
| docs | docs.docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | `docs.docs-gates-0__gate_19.log` |
| docs | docs-gates-0 | ci_step_25 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| docs | docs.docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | `docs.docs-gates-0__gate_21.log` |
| docs | docs.docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | `docs.docs-gates-0__ci_step_28.log` |
| docs | docs.docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | `docs.docs-gates-0__gate_24.log` |
| docs | docs.docs-gates-0 | gate_26 | NVM record-space gate | 0 | `docs.docs-gates-0__gate_26.log` |
| docs | docs.docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | `docs.docs-gates-0__gate_27.log` |
| docs | docs.docs-gates-0 | gate_28 | Saved-state writer gate | 0 | `docs.docs-gates-0__gate_28.log` |
| docs | docs.docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | `docs.docs-gates-0__gate_29.log` |
| docs | docs.docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | `docs.docs-gates-0__gate_30.log` |
| docs | docs.docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | `docs.docs-gates-0__gate_31.log` |
| docs | docs.docs-gates-0 | gate_32 | Port contract gate | 0 | `docs.docs-gates-0__gate_32.log` |
| docs | docs.docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | `docs.docs-gates-0__gate_33.log` |
| docs | docs.docs-gates-0 | gate_34 | TODO ownership gate | 0 | `docs.docs-gates-0__gate_34.log` |
| docs | docs.docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | `docs.docs-gates-0__gate_35.log` |
| docs | docs.docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | `docs.docs-gates-0__gate_36.log` |
| docs | docs.docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | `docs.docs-gates-0__gate_37.log` |
| docs | docs.docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | `docs.docs-gates-0__gate_38.log` |
| docs | docs.docs-gates-0 | gate_39 | Python idiom gate | 0 | `docs.docs-gates-0__gate_39.log` |
| docs | docs.docs-gates-0 | gate_40 | Shell idiom gate | 0 | `docs.docs-gates-0__gate_40.log` |
| docs | docs.docs-gates-0 | gate_43 | Doc cited-path gate | 0 | `docs.docs-gates-0__gate_43.log` |
| docs | docs.docs-gates-0 | gate_44 | Archive integrity gate | 0 | `docs.docs-gates-0__gate_44.log` |
| docs | docs.docs-gates-0 | gate_45 | Per-page contents gate | 0 | `docs.docs-gates-0__gate_45.log` |
| docs | docs.docs-gates-0 | gate_46 | AEM store generator self-test | 0 | `docs.docs-gates-0__gate_46.log` |
| docs | docs.docs-gates-0 | gate_47 | Sweep/build shape gate | 0 | `docs.docs-gates-0__gate_47.log` |
| docs | docs.docs-gates-0 | gate_48 | Deploy shape gate | 0 | `docs.docs-gates-0__gate_48.log` |
| docs | docs.docs-gates-0 | gate_49 | Entity shape gate | 0 | `docs.docs-gates-0__gate_49.log` |
| docs | docs.docs-gates-0 | ci_step_52 | Fetch inventory dependencies | 0 | `docs.docs-gates-0__ci_step_52.log` |
| docs | docs.docs-gates-0 | gate_50 | CI scheduling and evidence controls | 0 | `docs.docs-gates-0__gate_50.log` |
| docs | docs-gates-0 | ci_step_54 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs | docs-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs | docs.docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs.docs-gates-1__ci_step_1.log` |
| docs | docs.docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 | `docs.docs-gates-1__ci_step_3.log` |
| docs | docs.docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs.docs-gates-1__ci_step_5.log` |
| docs | docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| docs | docs-gates-1 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs | docs.docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs.docs-gates-1__ci_step_9.log` |
| docs | docs-gates-1 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| docs | docs.docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs.docs-gates-1__ci_step_13.log` |
| docs | docs.docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | `docs.docs-gates-1__gate_25_0.log` |
| docs | docs-gates-1 | ci_step_15 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs | docs-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs | docs.docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs.docs-gates-2__ci_step_1.log` |
| docs | docs.docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 | `docs.docs-gates-2__ci_step_3.log` |
| docs | docs.docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs.docs-gates-2__ci_step_5.log` |
| docs | docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| docs | docs-gates-2 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs | docs.docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs.docs-gates-2__ci_step_9.log` |
| docs | docs-gates-2 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| docs | docs.docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs.docs-gates-2__ci_step_13.log` |
| docs | docs.docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | `docs.docs-gates-2__gate_25_1.log` |
| docs | docs.docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | `docs.docs-gates-2__gate_41.log` |
| docs | docs.docs-gates-2 | gate_42 | Local act runner contract gate | 0 | `docs.docs-gates-2__gate_42.log` |
| docs | docs-gates-2 | ci_step_17 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs | docs-gates-2 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs | docs.docs-check | ci_step_1 | Set CPU-derived job budgets | 0 | `docs.docs-check__ci_step_1.log` |
| docs | docs-check | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only the hosted verify and manifest steps use |
| docs | docs-check | ci_step_6 | Require every gate exactly once | NOT RUN | verifies the hosted jobs' uploaded receipts; this table is the local equivalent |
| docs | docs-check | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run, no local gate |
| docs | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run, no local gate |

152 steps ran, 198 not run with a reason, 0 bad
verify_wf rc=0
