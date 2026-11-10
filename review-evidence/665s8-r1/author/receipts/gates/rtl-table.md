| Job | Step | Name | rc | Log |
|---|---|---|---:|---|
| full-ci-gate | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__full-ci-gate__ci_step_1.log` |
| full-ci-gate | target | Print the event and pin the one SHA this run validates | 0 | `rtl__full-ci-gate__target.log` |
| full-ci-gate | ci_step_4 | Assert the repository default branch is dev | NOT RUN | asks the hosted repository for its default branch (gh api) on a push event; a pull request event passes it, and the ruleset is the hosted repository's |
| full-ci-gate | ci_step_5 | Hold every workflow file to its contract | 0 | `rtl__full-ci-gate__ci_step_5.log` |
| full-ci-gate | gate | Decide whether this exact head needs the exhaustive gates | 0 | `rtl__full-ci-gate__gate.log` |
| full-ci-gate | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| verilator-shards | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_2 | Fetch RTL dependencies | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_3 | Record the tree this worker validates | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_7 | Build Verilator from source on cache miss | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_8 | Put Verilator on PATH and prove the version | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_9 | Prove specialized suite ownership | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_packages_8 | Resolve exact package downloads 8 | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_13 | Build Yosys from source on cache miss | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_packages_9 | Resolve exact package downloads 9 | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_16 | Install the pinned Yosys and prove the version | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_18 | Install sv2v for the netlist-level suite owner | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_step_21 | Run this exhaustive suite shard | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| verilator-shards | ci_record | Record actual job execution | NOT RUN | the 19 hosted shards of scripts/run_all_suites.sh: the full sweep ran instead as four native shards (scripts/run_all_suites.sh --shard k/4), one clone and one unit each, on this head |
| physical-gptp | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__physical-gptp__ci_step_1.log` |
| physical-gptp | ci_step_3 | Fetch RTL dependencies | 0 | `rtl__physical-gptp__ci_step_3.log` |
| physical-gptp | ci_step_4 | Record the tree this worker validates | 0 | `rtl__physical-gptp__ci_step_4.log` |
| physical-gptp | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| physical-gptp | ci_step_8 | Build Verilator from source on cache miss | NOT RUN | builds Verilator v5.050 from source on a cache miss; the pinned v5.050 build is on PATH here |
| physical-gptp | ci_step_9 | Put Verilator on PATH and prove the version | NOT RUN | puts /opt/verilator on PATH and runs it from there; the pinned v5.050 build is on PATH here (verilator --version in the gate logs) |
| physical-gptp | ci_step_10 | Prove physical suite selection | 0 | `rtl__physical-gptp__ci_step_10.log` |
| physical-gptp | ci_step_11 | Run the physical gPTP suite with its own deadline | BAD 2 | `rtl__physical-gptp__ci_step_11.log` |
| physical-gptp | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| verilator-suites | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| verilator-suites | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| verilator-suites | ci_step_5 | Require every shard to have validated this run's SHA | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| verilator-suites | ci_step_6 | Prove exhaustive ownership and tally every log | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| verilator-suites | ci_step_7 | Require every Verilator worker to pass | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| verilator-suites | ci_step_8 | Require every case union to succeed | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| verilator-suites | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded receipts; the four native shards' tallies stand for them |
| yosys-shards | ci_step_1 | Set CPU-derived job budgets | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_step_2 | Fetch RTL dependencies | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_step_3 | Record the tree this worker validates | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_step_5 | Restore the pinned Yosys build | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_packages_5 | Resolve exact package downloads 5 | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_step_8 | Install the pinned Yosys and prove the version | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_step_10 | Install the pinned sv2v release | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_step_12 | Run this weighted portability shard | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-shards | ci_record | Record actual job execution | NOT RUN | the four hosted portability shards take the matrix's shard number; each ran here as syn/yosys/run.sh --shard k/4 with its own results and cache (rtl-yosys-shard-k logs) |
| yosys-portability | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted portability shards' uploaded receipts; the four local shards' results stand for them |
| yosys-portability | ci_step_3 | Require every shard to have validated this run's SHA | NOT RUN | verifies the hosted portability shards' uploaded receipts; the four local shards' results stand for them |
| yosys-portability | ci_step_4 | Reconcile the live inventory and structural gates | NOT RUN | verifies the hosted portability shards' uploaded receipts; the four local shards' results stand for them |
| yosys-portability | ci_step_5 | Require every Yosys worker to pass | NOT RUN | verifies the hosted portability shards' uploaded receipts; the four local shards' results stand for them |
| yosys-portability | ci_record | Record actual job execution | NOT RUN | verifies the hosted portability shards' uploaded receipts; the four local shards' results stand for them |
| yosys-tool | ci_step_1 | Set CPU-derived job budgets | NOT RUN | builds and packages Yosys v0.66 for the shards; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | builds and packages Yosys v0.66 for the shards; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds and packages Yosys v0.66 for the shards; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| yosys-tool | ci_step_6 | Package the pinned Yosys build | NOT RUN | builds and packages Yosys v0.66 for the shards; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| yosys-tool | ci_record | Record actual job execution | NOT RUN | builds and packages Yosys v0.66 for the shards; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| union-milan_dp | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_mclk | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_mclk | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_mclk | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_mclk | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-capture_coherence | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-capture_coherence | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-capture_coherence | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-capture_coherence | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-maap | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-maap | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-maap | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-maap | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_render | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_render | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_render | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-milan_dp_render | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-pp_shadow | ci_step_1 | Set CPU-derived job budgets | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-pp_shadow | ci_step_2 | Fetch inventory dependencies | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-pp_shadow | ci_step_4 | Require successful owners and every case exactly once | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
| union-pp_shadow | ci_record | Record actual job execution | NOT RUN | verifies the hosted shards' uploaded case receipts; the native sweep ran every case |
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

9 steps ran, 81 not run with a reason, 1 bad
