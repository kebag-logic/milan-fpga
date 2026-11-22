# Yosys portability at `62fcd154`

`bash syn/yosys/run.sh --shard k/4 --results <dir>` for k in 0..3, in a clean clone at `62fcd154`; 64 tops PASS (1 + 1 + 31 + 31), the tied-input inventory and tap-purity gates PASS, each shard rc 0.
