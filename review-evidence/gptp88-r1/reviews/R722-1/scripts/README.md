# Reviewer scripts (R722-1, FPGA-gPTP PR #93)

All scripts read a tree and write only to their own temporary or log
directories. Run them with the pinned Verilator 5.050 first on PATH as
`verilator` (see `verilator_wrapper.py`).

| Script | Purpose |
|---|---|
| `rungate.sh <logdir> <name> <workdir> <cmd...>` | Runs one gate and keeps its log, rc and seconds |
| `engine_arm_shard.py <tree> <k> <n> [jobs]` | Runs shard k of n of the tree's own engine mutation arm, using its unchanged stage/build/verdict code |
| `reviewer_probes.py <tree> parser\|engine all [jobs]` | Plants reviewer-owned fault probes through each suite's own mutation helpers and reports every FAIL line |
| `rom_check.sh <repo> <out>` | Regenerates every ROM image from the base and head generators, then compares them with each other and with the tracked images |
| `ast_compare.py <a.py> <b.py>` | Exit 0 when two Python files differ only in comments and docstrings |

Receipts: `receipts/head-gates` (repository gates at head), `receipts/engine-arm`
(5 shards), `receipts/probes`, `receipts/parent-head` (scratch parent at dev
97aab1d0 with the companion applied and the gitlink at head),
`receipts/rom_check.txt`, `receipts/generator_ast_compare.txt`,
`receipts/clone_integrity.txt`, `receipts/companion_patch_sha256.txt`.
