#!/bin/bash
# Record tool and tree identity for this review's receipts.
set -eu
. "$(dirname "$0")/env.sh"
echo "date: $(date -u +%FT%TZ)"
echo "verilator wrapper: $PINNED_BIN/verilator sha256 $(sha256sum "$PINNED_BIN/verilator" | cut -d' ' -f1)"
verilator --version
echo "VERILATOR_ROOT=$VERILATOR_ROOT"
echo "verilator_bin sha256 $(sha256sum "$(dirname "$(dirname "$VERILATOR_ROOT")")/bin/verilator_bin" | cut -d' ' -f1)"
g++ --version | head -1
python3 --version
cd "$REVIEW_CLONE"
echo "clone HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
test "$(git rev-parse HEAD)" = "$HEAD_SHA"
test "$(git rev-parse 'HEAD^')" = "$BASE_SHA"
echo "status-porcelain-lines $(git status --porcelain=v1 --ignored=no | wc -l)"
echo "gitlinks: $(git ls-files -s | awk '$1=="160000"' | wc -l)"
