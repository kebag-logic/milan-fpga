Original file: <scratch>/wf/run-J/verify-fw.md
Original size: 5380 bytes
Original sha256: 0c698fae8387985a2691c9027b843037cc2676a51af0863cc0081738b4c391af

Every run step of the jobs replayed at b496c99e, each on its own fresh clone (run_wf.py)

| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | firmware-unit | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-unit__ci_step_1.log` |
| rtl-fast | firmware-unit | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-unit__ci_step_3.log` |
| rtl-fast | firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failu | 0 | `rtl-fast__firmware-unit__ci_step_7.log` |
| rtl-fast | firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | 0 | `rtl-fast__firmware-unit__ci_step_10.log` |
| rtl-fast | firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | 0 | `rtl-fast__firmware-unit__ci_step_11.log` |
| rtl-fast | firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | 0 | `rtl-fast__firmware-unit__ci_step_12.log` |
| rtl-fast | firmware-unit | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-srp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-srp-mutants__ci_step_1.log` |
| rtl-fast | firmware-srp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-srp-mutants__ci_step_3.log` |
| rtl-fast | firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-srp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-srp-mutants | ci_step_9 | Run both SRP mutation campaigns and pin controls | 0 | `rtl-fast__firmware-srp-mutants__ci_step_9.log` |
| rtl-fast | firmware-srp-mutants | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_1.log` |
| rtl-fast | firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_3.log` |
| rtl-fast | firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| rtl-fast | firmware-aecp-mutants | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-control-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-control-mutants__ci_step_1.log` |
| rtl-fast | firmware-control-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-control-mutants__ci_step_3.log` |
| rtl-fast | firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-control-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-control-mutants | ci_step_9 | Run the control mutation campaign | 0 | `rtl-fast__firmware-control-mutants__ci_step_9.log` |
| rtl-fast | firmware-control-mutants | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |

15 steps run (15 rc 0), 16 not run with a reason, 0 bad
