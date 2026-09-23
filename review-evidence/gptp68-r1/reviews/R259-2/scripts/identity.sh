#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Record the review clone's identity and the pinned Verilator identity.
set -eu
. "$(dirname "$0")/env.sh"
cd "$CLONE"
echo "head:      $(git rev-parse HEAD)"
echo "tree:      $(git rev-parse 'HEAD^{tree}')"
test "$(git rev-parse HEAD)" = "$HEAD_SHA"
test "$(git rev-parse 'HEAD^{tree}')" = "$HEAD_TREE"
echo "status:    $(git status --porcelain=v1 --untracked-files=all | wc -l) entries"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
echo "submodules: $(git ls-files -s | awk '$1=="160000"' | wc -l) gitlinks"
git ls-files -s | awk '$1=="160000"'
echo "parents:   $(git rev-parse HEAD^1) (reviewed head), merge-base with base: $(git merge-base HEAD "$BASE_SHA")"
echo "ancestry:  base is ancestor: $(git merge-base --is-ancestor "$BASE_SHA" HEAD && echo yes || echo no)"
echo "commits base..head:"; git log --format='  %H %s' "$BASE_SHA..HEAD"
echo "message lines: $(git log -1 --format=%B HEAD | sed '/^$/d' | wc -l) (head), $(git log -1 --format=%B "$REVIEWED_SHA" | sed '/^$/d' | wc -l) (reviewed)"
w="$PIN_BIN/verilator"
echo "wrapper sha256: $(sha256sum "$w" | cut -d' ' -f1)"
test "$(sha256sum "$w" | cut -d' ' -f1)" = "$WRAPPER_SHA256"
bin=$(sed -n 's/.* \(\/[^ ]*\/usr\/bin\/verilator\) .*/\1/p' "$w")
echo "verilator_bin sha256: $(sha256sum "${bin}_bin" | cut -d' ' -f1)"
echo "version: $(verilator --version)"
echo "system verilator (unused): $(/usr/bin/verilator --version 2>/dev/null || echo absent)"
echo "python: $(python3 --version)"
