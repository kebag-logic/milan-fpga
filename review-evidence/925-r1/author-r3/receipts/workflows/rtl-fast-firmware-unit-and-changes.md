replay verification
head 5f625090; rtl-fast.yml's firmware-unit and changes jobs replayed step by step on fresh clones (run_wf.py), each run: step's rc or its stated reason (verify_wf.py's rows for these two jobs)
| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | changes | ci_step_1 | Set CPU-derived job budgets | 0 | `steps/rtl-fast__changes__ci_step_1.log` |
| rtl-fast | changes | scope | Classify the change conservatively | 0 | `steps/rtl-fast__changes__scope.log` |
| rtl-fast | changes | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-unit | ci_step_1 | Set CPU-derived job budgets | 0 | `steps/rtl-fast__firmware-unit__ci_step_1.log` |
| rtl-fast | firmware-unit | ci_step_3 | Fetch RTL dependencies | 0 | `steps/rtl-fast__firmware-unit__ci_step_3.log` |
| rtl-fast | firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | 0 | `steps/rtl-fast__firmware-unit__ci_step_7.log` |
| rtl-fast | firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| rtl-fast | firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | 0 | `steps/rtl-fast__firmware-unit__ci_step_10.log` |
| rtl-fast | firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | 0 | `steps/rtl-fast__firmware-unit__ci_step_11.log` |
| rtl-fast | firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | 0 | `steps/rtl-fast__firmware-unit__ci_step_12.log` |
| rtl-fast | firmware-unit | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |

firmware-unit: 6 ran rc 0, 4 not run with a reason, 0 bad
changes: 2 ran rc 0, 1 not run with a reason, 0 bad
