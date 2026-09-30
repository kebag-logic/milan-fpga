#!/usr/bin/env bash
# Export the exact head into a disposable tree and pin the CI Verilator (v5.050).
# Usage: 20-setup.sh <repo> <scratch-dir> <reference-verilator-wrapper>
set -euo pipefail
R=${1:?repo}; S=${2:?scratch}; REF=${3:?wrapper}
HEAD_C=47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346
rm -rf "$S/tree"; mkdir -p "$S/tree" "$S/bin" "$S/tmp"
git -C "$R" archive "$HEAD_C" | tar -x -C "$S/tree"
# the export carries no .git: give it one pinned to the same objects so tools
# that call git (patch drivers, doc gates) see the exact head
git -C "$S/tree" init -q && git -C "$S/tree" fetch -q "$R" "$HEAD_C" && git -C "$S/tree" reset -q "$HEAD_C"
git -C "$S/tree" rev-parse HEAD; git -C "$S/tree" status --short | head
cp "$REF" "$S/bin/verilator"
echo "wrapper sha256: $(sha256sum "$S/bin/verilator" | cut -d' ' -f1)"
cat "$S/bin/verilator"
PATH="$S/bin:$PATH" verilator --version
PATH="$S/bin:$PATH" command -v verilator
