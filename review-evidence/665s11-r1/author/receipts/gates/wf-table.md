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
| elaborate | elaborate-gates-0 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source in the shared LiteX venv's pythondata package, which already holds it at the pinned revision (the venv's CPU builds generate their netlists offline from it); running it would change a shared venv |
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
| elaborate | elaborate-gates-1 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source in the shared LiteX venv's pythondata package, which already holds it at the pinned revision (the venv's CPU builds generate their netlists offline from it); running it would change a shared venv |
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
| rtl | verilator-shards | ci_step_1 | Set CPU-derived job budgets | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
| rtl | verilator-shards | ci_step_2 | Fetch RTL dependencies | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
| rtl | verilator-shards | ci_step_3 | Record the tree this worker validates | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
| rtl | verilator-shards | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | verilator-shards | ci_step_7 | Build Verilator from source on cache miss | NOT RUN | builds the hosted /opt Verilator; the pinned Verilator 5.050 is on PATH here |
| rtl | verilator-shards | ci_step_8 | Put Verilator on PATH and prove the version | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
| rtl | verilator-shards | ci_step_9 | Prove specialized suite ownership | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
| rtl | verilator-shards | ci_packages_8 | Resolve exact package downloads 8 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | verilator-shards | ci_step_13 | Build Yosys from source on cache miss | NOT RUN | builds the hosted /opt Yosys; the host's Yosys 0.66 is on PATH |
| rtl | verilator-shards | ci_packages_9 | Resolve exact package downloads 9 | NOT RUN | apt package index for the hosted runner; this host has the packages installed |
| rtl | verilator-shards | ci_step_16 | Install the pinned Yosys and prove the version | NOT RUN | sudo links /opt/yosys into /usr/local/bin; the host's Yosys 0.66 is on PATH (yosys -V in the substitute log) |
| rtl | verilator-shards | ci_step_18 | Install sv2v for the netlist-level suite owner | NOT RUN | sudo installs into /usr/local/bin; the pinned sv2v v0.0.12 is on PATH |
| rtl | verilator-shards | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
| rtl | verilator-shards | ci_step_21 | Run this exhaustive suite shard | NOT RUN | replicated by the full sweep at this head as four native shard units (receipts/sweep), the hosted 19-way split of the same suites |
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

88 steps ran, 167 not run with a reason, 0 bad
