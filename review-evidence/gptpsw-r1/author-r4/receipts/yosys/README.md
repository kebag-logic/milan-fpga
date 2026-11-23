# Yosys portability at `a6323318`

`bash syn/yosys/run.sh --shard k/4 --results <dir>` for k in 0..3 in a clean clone at `a6323318`: 64 tops PASS (1 + 1 + 31 + 31), the tied-input inventory and tap-purity gates PASS, each shard rc 0. Nothing Yosys reads moved after `a6323318` (`ba2c8ed6` changes `sw/builder/test_builder.py` alone).
