# Reviewer scripts (R711-1)

Set `PACKET` (this packet), `CHECKOUT` (a clean checkout at `f884c7e9fb71cdb94c12e3228b1412801c34e1f4`) and `TOOLS` (the pinned tools: Verilator 5.050), with the product LiteX tree and the pinned RV32 SDK under `$HOME` as the harness README's prerequisites name them.

- `env.sh`, `bg.sh`, `bgdir.sh`: the environment and the detached runner (log and rc file per job under `receipts/`).
- `ctrl_mem_probe.c`: exhaustive reference check of `sw/firmware/ctrl/plat/ctrl_mem.c` (compiled with `-Dmemcpy=kl_memcpy` and the like), every offset pair, length to 200, overlap both ways, guard pages.
- `dma_reviewer_plants.py CHECKOUT SCRATCH`: ten planted defects in `KL_mbx_dma.sv`, each built against the tree's own bench with the Makefile's recipe.
- `dma_len_probe.cpp`: `KL_mbx_dma` alone at its 12-bit length boundary (build with `verilator --cc --exe --build --top-module KL_mbx_dma KL_mbx_pkg.sv KL_mbx_dma.sv dma_len_probe.cpp`).
- `merge_sides.py BASE LANE S1 HEAD FILE...`: the lines each merge side added that the head no longer holds.

Harness legs: `bg.sh h50-8x8-A python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <dir> --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings --jobs 4` (and `--point 1x1`); the 100 MHz leg is the same command from a clone with the author's published `harness-profile-merged.patch` applied and `CSB_CPU_HZ=100000000`.
