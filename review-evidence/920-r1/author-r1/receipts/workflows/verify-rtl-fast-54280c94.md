| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | changes | ci_step_1 | Set CPU-derived job budgets | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | changes | scope | Classify the change conservatively | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | changes | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | verilator-lint | ci_step_1 | Set CPU-derived job budgets | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | verilator-lint | ci_step_2 | Fetch RTL dependencies | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | verilator-lint | ci_step_6 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | verilator-lint | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | bdd-conformance | ci_step_1 | Set CPU-derived job budgets | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | bdd-conformance | ci_step_3 | Fetch the processor model inputs | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | bdd-conformance | ci_step_4 | Install behave | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | bdd-conformance | ci_step_5 | Run the specification-facing suite | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | bdd-conformance | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | yosys-tool | ci_step_1 | Set CPU-derived job budgets | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | yosys-tool | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | yosys-elaboration | ci_step_1 | Set CPU-derived job budgets | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_step_2 | Fetch RTL dependencies | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_step_4 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl-fast | yosys-elaboration | ci_step_6 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl-fast | yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_step_10 | Prove both synthesis flows refuse active elaboration guards | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_step_11 | Prove the result cache refuses a planted entry | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | yosys-elaboration | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | publication-census | ci_step_1 | Set CPU-derived job budgets | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | publication-census | ci_step_2 | Set memory-derived census workers | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | publication-census | ci_step_4 | Fetch RTL dependencies | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | publication-census | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | publication-census | ci_step_8 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | publication-census | ci_step_9 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl-fast | publication-census | ci_step_11 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl-fast | publication-census | ci_step_12 | Run the publication census in every shape the builder builds | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | publication-census | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | split-cdc | ci_step_1 | Set CPU-derived job budgets | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | split-cdc | ci_step_2 | Fetch RTL dependencies | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | split-cdc | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | split-cdc | ci_step_6 | Build Yosys from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | split-cdc | ci_step_7 | Install the pinned Yosys and prove the version | NOT RUN | installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl-fast | split-cdc | ci_step_9 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl-fast | split-cdc | ci_step_10 | Prove every split crossing goes through an approved primitive | NOT RUN | outside this lane's gate list (#920: firmware units and campaigns, fw_coverage --check, the suite sweep, elaborate, docs): this change has no RTL, tooling, BDD or census input |
| rtl-fast | split-cdc | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-unit | ci_step_1 | Set CPU-derived job budgets | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-unit | ci_step_3 | Fetch RTL dependencies | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-unit | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-control-mutants | ci_step_1 | Set CPU-derived job budgets | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-control-mutants | ci_step_3 | Fetch RTL dependencies | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-control-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-control-mutants | ci_step_9 | Run the control mutation campaign | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-control-mutants | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-aecp-mutants | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-srp-mutants | ci_step_1 | Set CPU-derived job budgets | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-srp-mutants | ci_step_3 | Fetch RTL dependencies | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-srp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-srp-mutants | ci_step_9 | Run both SRP mutation campaigns and pin controls | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-srp-mutants | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-boundary | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-boundary__ci_step_1.log` |
| rtl-fast | firmware-boundary | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-boundary__ci_step_3.log` |
| rtl-fast | firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-boundary | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | 0 | `rtl-fast__firmware-boundary__ci_step_9.log` |
| rtl-fast | firmware-boundary | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-verilator | ci_step_1 | Set CPU-derived job budgets | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-verilator | ci_step_3 | Fetch RTL dependencies | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-verilator | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-verilator | ci_step_10 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| rtl-fast | firmware-verilator | ci_step_11 | Put Verilator on PATH and prove the version | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
| rtl-fast | firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | NOT RUN | run at f1f7c3e8, whose code this docs-only commit keeps (workflows/f1f7c3e8) |
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

3 steps ran, 104 not run with a reason, 0 bad
