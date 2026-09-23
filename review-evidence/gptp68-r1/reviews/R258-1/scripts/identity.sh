#!/bin/bash
# Record the tool and object identities these receipts were produced with.
set -euo pipefail
. "$(dirname "$0")/env.sh"
v=$(command -v verilator)
echo "verilator wrapper: $v sha256 $(sha256sum "$v" | cut -d' ' -f1)"
echo "verilator version: $(verilator --version)"
real=$(sed -n 's/.* \(\/[^ ]*\/usr\/bin\/verilator\) .*/\1/p' "$v")
echo "verilator driver sha256 $(sha256sum "$real" | cut -d' ' -f1)"
echo "verilator_bin sha256 $(sha256sum "${real}_bin" | cut -d' ' -f1)"
echo "python: $(python3 --version)"
echo "c++: $(g++ --version | head -1)"
echo "review clone HEAD $(git -C "$CLONE" rev-parse HEAD) tree $(git -C "$CLONE" rev-parse 'HEAD^{tree}')"
echo "expected    HEAD $HEAD_SHA tree 10154fc3f95ccc542a6f5dcd8a58105d302fd1af"
echo "base $(git -C "$CLONE" rev-parse "$BASE_SHA") parent pin $PARENT_SHA"
echo "parent scratch HEAD $(git -C "$PACKET/scratch/parent" rev-parse HEAD)"
echo "parent gitlink gptp-processor at pin: $(git -C "$PACKET/scratch/parent" ls-tree HEAD gptp-processor)"
echo "verilog-axis scratch HEAD $(git -C "$PACKET/scratch/parent/third_party/verilog-axis" rev-parse HEAD)"
