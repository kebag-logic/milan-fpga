| Job | Step | Name | Reads | rc | Log |
|---|---|---|---|---:|---|
| changes | scope | Classify the change conservatively | direct | 0 | `changes__scope.log` |
| changes | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | direct | 0 | `verilator-lint__ci_step_7.log` |
| verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | direct | 0 | `verilator-lint__ci_step_8.log` |
| verilator-lint | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| bdd-conformance | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| yosys-tool | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | through syn/yosys/run.sh | 0 | `yosys-elaboration__ci_step_7.log` |
| yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | through syn/ooc/dp_srcs.py, syn/ooc/pp_resource_gate.py | 0 | `yosys-elaboration__ci_step_8.log` |
| yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | through syn/yosys/ooc_selftest.py | 0 | `yosys-elaboration__ci_step_9.log` |
| yosys-elaboration | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| publication-census | ci_packages_3 | Resolve exact package downloads 3 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| publication-census | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | through sw/firmware/gtest/tally_selftest.py | 0 | `firmware-unit__ci_step_7.log` |
| firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-unit__ci_step_9.log` |
| firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | through sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py | 0 | `firmware-unit__ci_step_11.log` |
| firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | through sw/firmware/gtest/fw_coverage.py | 0 | `firmware-unit__ci_step_12.log` |
| firmware-unit | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-control-mutants__ci_step_8.log` |
| firmware-control-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-aecp-mutants__ci_step_8.log` |
| firmware-aecp-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-srp-mutants__ci_step_8.log` |
| firmware-srp-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-boundary__ci_step_8.log` |
| firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | through sw/firmware/ctrl/test/ctrl_boundary.py | 0 | `firmware-boundary__ci_step_9.log` |
| firmware-boundary | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-verilator__ci_step_13.log` |
| firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | through sw/firmware/ctrl/test/ctrl_boundary.py | 0 | `firmware-verilator__ci_step_14.log` |
| firmware-verilator | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | ci_collect | Collect actual runtime evidence | direct | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_observe | Observe the first failed job | direct | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | direct | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | direct | NOT RUN | cancels a hosted run |

17 steps ran, 28 not run with a reason, 0 bad
