Final head 5f625090: every elaborate run step verified, rc 0
| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| elaborate | elaborate-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `steps/elaborate__elaborate-gates-0__ci_step_1.log` |
| elaborate | elaborate-gates-0 | scope | Decide whether this head needs an elaboration | 0 | `steps/elaborate__elaborate-gates-0__scope.log` |
| elaborate | elaborate-gates-0 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `steps/elaborate__elaborate-gates-0__ci_step_4.log` |
| elaborate | elaborate-gates-0 | ci_step_6 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| elaborate | elaborate-gates-0 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv on PATH; the host's LiteX venv is the job's venv here |
| elaborate | elaborate-gates-0 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | pip-installs LiteX at the pinned revisions into the job's venv from the network; the host's LiteX venv carries them |
| elaborate | elaborate-gates-0 | ci_step_13 | Install sbt | NOT RUN | downloads sbt; the CPU netlist is generated offline from the pinned generator (COURSIER_MODE=offline) |
| elaborate | elaborate-gates-0 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source into the job's venv; it would rewrite the shared host venv |
| elaborate | elaborate-gates-0 | ci_step_15 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the job's venv; it would rewrite the shared host venv, which carries the series |
| elaborate | elaborate-gates-0 | ci_step_17 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| elaborate | elaborate-gates-0 | gate_15_0 | Elaboration gates, leg 0 of 2 | 0 | `steps/elaborate__elaborate-gates-0__gate_15_0.log` |
| elaborate | elaborate-gates-0 | ci_step_19 | Keep the generated CPU netlist arguments for the next run | NOT RUN | keeps the generated netlist arguments in the runner's home cache for the next hosted run; no local gate |
| elaborate | elaborate-gates-0 | ci_step_20 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate | elaborate-gates-0 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | elaborate-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `steps/elaborate__elaborate-gates-1__ci_step_1.log` |
| elaborate | elaborate-gates-1 | scope | Decide whether this head needs an elaboration | 0 | `steps/elaborate__elaborate-gates-1__scope.log` |
| elaborate | elaborate-gates-1 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 | `steps/elaborate__elaborate-gates-1__ci_step_4.log` |
| elaborate | elaborate-gates-1 | ci_step_6 | Install the pinned sv2v release | NOT RUN | downloads sv2v and installs it with sudo; /usr/local/bin/sv2v here is the pinned v0.0.12 |
| elaborate | elaborate-gates-1 | ci_step_8 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv on PATH; the host's LiteX venv is the job's venv here |
| elaborate | elaborate-gates-1 | ci_step_10 | Install LiteX at the pinned revisions | NOT RUN | pip-installs LiteX at the pinned revisions into the job's venv from the network; the host's LiteX venv carries them |
| elaborate | elaborate-gates-1 | ci_step_13 | Install sbt | NOT RUN | downloads sbt; the CPU netlist is generated offline from the pinned generator (COURSIER_MODE=offline) |
| elaborate | elaborate-gates-1 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source into the job's venv; it would rewrite the shared host venv |
| elaborate | elaborate-gates-1 | ci_step_15 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the job's venv; it would rewrite the shared host venv, which carries the series |
| elaborate | elaborate-gates-1 | ci_step_17 | Install and verify the pinned RV32 SDK | NOT RUN | downloads the pinned RV32 SDK into $HOME/br-milan-rv32/host; here the runner's $HOME/br-milan-rv32 is a link to the host's pinned SDK (<home>/br-milan-rv32), which the step would have installed |
| elaborate | elaborate-gates-1 | gate_15_1 | Elaboration gates, leg 1 of 2 | 0 | `steps/elaborate__elaborate-gates-1__gate_15_1.log` |
| elaborate | elaborate-gates-1 | ci_packages_17 | Resolve exact package downloads 17 | NOT RUN | resolves apt package downloads for the hosted image; this host has the packages installed and no apt |
| elaborate | elaborate-gates-1 | ci_step_22 | Build Verilator from source on cache miss | NOT RUN | builds the tool into /opt with sudo apt on a cache miss; the pinned build is installed here (Verilator 5.050, Yosys 0.66) |
| elaborate | elaborate-gates-1 | ci_step_23 | Put Verilator on PATH and prove the version | 0 | `steps/elaborate__elaborate-gates-1__ci_step_23.log` |
| elaborate | elaborate-gates-1 | gate_19 | Standalone LiteX simulation aggregate | 0 | `steps/elaborate__elaborate-gates-1__gate_19.log` |
| elaborate | elaborate-gates-1 | ci_step_25 | Keep the generated CPU netlist arguments for the next run | NOT RUN | keeps the generated netlist arguments in the runner's home cache for the next hosted run; no local gate |
| elaborate | elaborate-gates-1 | ci_step_26 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| elaborate | elaborate-gates-1 | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | elaborate | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the aggregate job's CPU budget step, which sets budgets only for that job's verify of the hosted jobs' results, itself not run (below); the jobs it aggregates ran here step by step |
| elaborate | elaborate | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only the hosted aggregate's verify uses |
| elaborate | elaborate | ci_step_6 | Require every gate exactly once | NOT RUN | verifies the hosted legs' uploaded receipts; each leg's gates ran here instead |
| elaborate | elaborate | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records or uploads GitHub's own step results; needs the hosted step context |
| elaborate | ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |
| elaborate | ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration of the hosted run (its artifacts, its token, its cancellation); no local gate |

10 steps ran, 36 not run with a reason, 0 bad
