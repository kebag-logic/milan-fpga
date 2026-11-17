Original file: <scratch>/wf/run-J/verify-shard-4.md
Original size: 2671 bytes
Original sha256: 1a9c447bff131197e8d29e22c0da32ff269f0df626a0883f66395234295b9e31

Every run step of the jobs replayed at b496c99e, each on its own fresh clone (run_wf.py)

| Workflow | Job | Step | Name | rc | Log or reason |
|---|---|---|---|---:|---|
| rtl | verilator-shards-4 | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl__verilator-shards-4__ci_step_1.log` |
| rtl | verilator-shards-4 | ci_step_2 | Fetch RTL dependencies | 0 | `rtl__verilator-shards-4__ci_step_2.log` |
| rtl | verilator-shards-4 | ci_step_3 | Record the tree this worker validates | 0 | `rtl__verilator-shards-4__ci_step_3.log` |
| rtl | verilator-shards-4 | ci_packages_4 | Resolve exact package downloads 4 | - | not run: resolves apt package downloads for the Verilator build on a cache miss; this host has no apt, and the pinned V |
| rtl | verilator-shards-4 | ci_step_7 | Build Verilator from source on cache miss | - | not run: builds Verilator v5.050 into /opt with sudo on a cache miss; the pinned v5.050 build is installed here, and st |
| rtl | verilator-shards-4 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | `rtl__verilator-shards-4__ci_step_8.log` |
| rtl | verilator-shards-4 | ci_step_9 | Prove specialized suite ownership | 0 | `rtl__verilator-shards-4__ci_step_9.log` |
| rtl | verilator-shards-4 | ci_packages_8 | Resolve exact package downloads 8 | - | not run: if: matrix.shard == 3 (the netlist-level suite owner's Yosys); no shard replayed here is shard 3 |
| rtl | verilator-shards-4 | ci_step_13 | Build Yosys from source on cache miss | - | not run: if: matrix.shard == 3 (builds Yosys); no shard replayed here is shard 3 |
| rtl | verilator-shards-4 | ci_packages_9 | Resolve exact package downloads 9 | - | not run: if: matrix.shard == 3 (Yosys runtime package); no shard replayed here is shard 3 |
| rtl | verilator-shards-4 | ci_step_16 | Install the pinned Yosys and prove the version | - | not run: if: matrix.shard == 3 (installs Yosys); no shard replayed here is shard 3 |
| rtl | verilator-shards-4 | ci_step_18 | Install sv2v for the netlist-level suite owner | - | not run: if: matrix.shard == 3 (installs sv2v); no shard replayed here is shard 3 |
| rtl | verilator-shards-4 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | - | not run: if: matrix.shard == 1; clones tsn-gen from GitHub and builds packet_gen at TSN_GEN_REV deca300c9eb4, exporting |
| rtl | verilator-shards-4 | ci_step_21 | Run this exhaustive suite shard | 0 | `rtl__verilator-shards-4__ci_step_21.log` |
| rtl | verilator-shards-4 | ci_record | Record actual job execution | - | not run: records or uploads GitHub's own step results; needs the hosted step context |

6 steps run (6 rc 0), 9 not run with a reason, 0 bad
