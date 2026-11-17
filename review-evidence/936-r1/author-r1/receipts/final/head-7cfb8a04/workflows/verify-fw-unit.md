Original file: <scratch>/wf/run-K/verify-fw-unit.md
Original size: 1778 bytes
Original sha256: 83b0abd5896b8649cde7328fd5dce61fd524ee9b7b57363fdde67071fd4fc9ce

Every run step of the jobs replayed at 7cfb8a04, each on its own fresh clone (run_wf.py)

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

6 steps run (6 rc 0), 4 not run with a reason, 0 bad
