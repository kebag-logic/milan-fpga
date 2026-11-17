Original file: <scratch>/wf/run-R4/verify-firmware-aecp-mutants.md
Original size: 1411 bytes
Original sha256: 2e54b987fdfb7434d83a29301b10a58a453562678032aef2087242d843355b7f

Every run step of the jobs replayed at d1aa4c44, each on its own fresh clone (run_wf.py)

| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl-fast | firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_1.log` |
| rtl-fast | firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_3.log` |
| rtl-fast | firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | - | not run: resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| rtl-fast | firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | - | not run: sudo apt-get of GoogleTest and GoogleMock; this host has them installed |
| rtl-fast | firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | - | not run: downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link t |
| rtl-fast | firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| rtl-fast | firmware-aecp-mutants | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |

3 steps run (3 rc 0), 4 not run with a reason, 0 bad
