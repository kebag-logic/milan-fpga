| Job | Step | Name | rc | Log |
|---|---|---|---:|---|
| elaborate-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate__elaborate-gates-0__ci_step_1.log` |
| elaborate-gates-0 | scope | Decide whether this head needs an elaboration | 0 | `elaborate__elaborate-gates-0__scope.log` |
| elaborate-gates-0 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `elaborate__elaborate-gates-0__ci_step_4.log` |
| elaborate-gates-0 | ci_step_6 | Install the pinned sv2v release | NOT RUN | installs sv2v into /usr/local/bin with sudo; sv2v v0.0.12 is already installed there |
| elaborate-gates-0 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv for the pip install that follows; the LiteX venv at the pinned revisions with the patch series applied is first on PATH here |
| elaborate-gates-0 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | pip-installs the LiteX pins into the runner's fresh venv; the LiteX venv at the pins is first on PATH here |
| elaborate-gates-0 | ci_step_13 | Install sbt | NOT RUN | downloads sbt 1.10.7 into /opt with sudo; the host's offline sbt and its coursier cache generate the CPU here |
| elaborate-gates-0 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source at the revision LiteX pins in the runner's fresh venv; the LiteX venv here carries it |
| elaborate-gates-0 | ci_step_15 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the runner's fresh LiteX; the LiteX venv here carries the series applied |
| elaborate-gates-0 | ci_step_17 | Install and verify the pinned RV32 SDK | 0 | `elaborate__elaborate-gates-0__ci_step_17.log` |
| elaborate-gates-0 | gate_15_0 | Elaboration gates, leg 0 of 2 | 0 | `elaborate__elaborate-gates-0__gate_15_0.log` |
| elaborate-gates-0 | ci_step_19 | Keep the generated CPU netlist arguments for the next run | 0 | `elaborate__elaborate-gates-0__ci_step_19.log` |
| elaborate-gates-0 | ci_step_20 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| elaborate-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `elaborate__elaborate-gates-1__ci_step_1.log` |
| elaborate-gates-1 | scope | Decide whether this head needs an elaboration | 0 | `elaborate__elaborate-gates-1__scope.log` |
| elaborate-gates-1 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `elaborate__elaborate-gates-1__ci_step_4.log` |
| elaborate-gates-1 | ci_step_6 | Install the pinned sv2v release | NOT RUN | installs sv2v into /usr/local/bin with sudo; sv2v v0.0.12 is already installed there |
| elaborate-gates-1 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv for the pip install that follows; the LiteX venv at the pinned revisions with the patch series applied is first on PATH here |
| elaborate-gates-1 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | pip-installs the LiteX pins into the runner's fresh venv; the LiteX venv at the pins is first on PATH here |
| elaborate-gates-1 | ci_step_13 | Install sbt | NOT RUN | downloads sbt 1.10.7 into /opt with sudo; the host's offline sbt and its coursier cache generate the CPU here |
| elaborate-gates-1 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source at the revision LiteX pins in the runner's fresh venv; the LiteX venv here carries it |
| elaborate-gates-1 | ci_step_15 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the runner's fresh LiteX; the LiteX venv here carries the series applied |
| elaborate-gates-1 | ci_step_17 | Install and verify the pinned RV32 SDK | 0 | `elaborate__elaborate-gates-1__ci_step_17.log` |
| elaborate-gates-1 | gate_15_1 | Elaboration gates, leg 1 of 2 | 0 | `elaborate__elaborate-gates-1__gate_15_1.log` |
| elaborate-gates-1 | ci_packages_17 | Resolve exact package downloads 17 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| elaborate-gates-1 | ci_step_22 | Build Verilator from source on cache miss | NOT RUN | builds Verilator v5.050 from source on a cache miss; the pinned v5.050 build is on PATH here |
| elaborate-gates-1 | ci_step_23 | Put Verilator on PATH and prove the version | NOT RUN | puts /opt/verilator on PATH and runs it from there; the pinned v5.050 build is on PATH here (verilator --version in the gate logs) |
| elaborate-gates-1 | gate_19 | Standalone LiteX simulation aggregate | 0 | `elaborate__elaborate-gates-1__gate_19.log` |
| elaborate-gates-1 | ci_step_25 | Keep the generated CPU netlist arguments for the next run | 0 | `elaborate__elaborate-gates-1__ci_step_25.log` |
| elaborate-gates-1 | ci_step_26 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| elaborate | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted gate receipts; each gate step ran above |
| elaborate | ci_step_4 | Install the pinned evidence reader | NOT RUN | verifies the hosted gate receipts; each gate step ran above |
| elaborate | ci_step_6 | Require every gate exactly once | NOT RUN | verifies the hosted gate receipts; each gate step ran above |
| elaborate | ci_record | Record actual job execution | NOT RUN | verifies the hosted gate receipts; each gate step ran above |
| ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration: cancels a hosted run |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration: cancels a hosted run |

13 steps ran, 33 not run with a reason, 0 bad
