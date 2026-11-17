Original file: <scratch>/wf/run-J/verify-bnd.md
Original size: 4436 bytes
Original sha256: 1c325854687909e7cb7093a818a3f27d1784a91e8c141cf5f2bbdd30395f0039

Every run step of the jobs replayed at b496c99e, each on its own fresh clone (run_wf.py)

| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | firmware-boundary | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-boundary__ci_step_1.log` |
| rtl-fast | firmware-boundary | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-boundary__ci_step_3.log` |
| rtl-fast | firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-boundary | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' comp | 0 | `rtl-fast__firmware-boundary__ci_step_9.log` |
| rtl-fast | firmware-boundary | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | firmware-verilator | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-verilator__ci_step_1.log` |
| rtl-fast | firmware-verilator | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-verilator__ci_step_3.log` |
| rtl-fast | firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-verilator | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-verilator | ci_step_10 | Build Verilator from source on cache miss | - | not run: builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050,  |
| rtl-fast | firmware-verilator | ci_step_11 | Put Verilator on PATH and prove the version | 0 | `rtl-fast__firmware-verilator__ci_step_11.log` |
| rtl-fast | firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' com | 0 | `rtl-fast__firmware-verilator__ci_step_14.log` |
| rtl-fast | firmware-verilator | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |
| rtl-fast | split-cdc | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__split-cdc__ci_step_1.log` |
| rtl-fast | split-cdc | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast__split-cdc__ci_step_2.log` |
| rtl-fast | split-cdc | ci_packages_3 | Resolve exact package downloads 3 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | split-cdc | ci_step_6 | Build Yosys from source on cache miss | - | not run: builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050,  |
| rtl-fast | split-cdc | ci_step_7 | Install the pinned Yosys and prove the version | - | not run: installs the hosted job's /opt/yosys build with sudo; /usr/bin/yosys here is Yosys 0.66 |
| rtl-fast | split-cdc | ci_step_9 | Install the pinned sv2v release | - | not run: downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| rtl-fast | split-cdc | ci_step_10 | Prove every split crossing goes through an approved primitiv | 0 | `rtl-fast__split-cdc__ci_step_10.log` |
| rtl-fast | split-cdc | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |

10 steps run (10 rc 0), 15 not run with a reason, 0 bad
