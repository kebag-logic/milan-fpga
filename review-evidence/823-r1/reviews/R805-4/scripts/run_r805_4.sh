#!/bin/sh
# Reproduce the R805-4 reviewer runs on a clean clone of the reviewed head.
# Usage: run_r805_4.sh <clone> <receipts-dir> <pinned-verilator>
# The clone must be at 30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14 with its
# submodules initialised. Nothing here writes outside <clone>'s ignored build
# directories and <receipts-dir>.
set -u
C=$1; R=$2; V=$3
mkdir -p "$R"
cd "$C" || exit 2
git rev-parse HEAD > "$R/head.txt"
B=a9d69c774dee18b90eead74c9f2dda24cf8fdeb8
# the merge commit's tree against a fresh merge of its two parents
git merge-tree --write-tree --name-only f3e902f2a96bb27eac6ed7780c70905af34f389e \
    1d6bf5556ae28764361d85012b86394eb467d294 > "$R/merge_tree.txt"; echo $? >> "$R/merge_tree.txt"
git cat-file -p 3bcf0cdd | head -3 >> "$R/merge_tree.txt"
comm -12 <(git diff --name-only $B f3e902f2 | sort) <(git diff --name-only $B 1d6bf555 | sort) > "$R/both_sides_files.txt"
python3 -B scripts/check_nvm_format_32x32.py > "$R/fmt32_gate.log" 2>&1; echo $? > "$R/fmt32_gate.rc"
python3 -B scripts/check_nvm_format_32x32.py --self-test > "$R/fmt32_selftest.log" 2>&1; echo $? > "$R/fmt32_selftest.rc"
T=$(mktemp -d)
{ python3 -B docs/diagrams/flash_layout.gen.py "$T/flash_layout"
  cmp "$T/flash_layout.svg" docs/diagrams/flash_layout.svg && echo SVG_IDENTICAL
  cmp "$T/flash_layout.drawio" docs/diagrams/flash_layout.drawio && echo DRAWIO_IDENTICAL
  rsvg-convert -w 1800 docs/diagrams/flash_layout.svg -o "$T/head.png" && cmp "$T/head.png" docs/diagrams/flash_layout.png && echo PNG_IDENTICAL
  python3 -B sw/litex/flash_map.py; echo flash_map rc=$?
  python3 -B scripts/nvm_layout3.py | tail -3; echo layout3 rc=$?
  python3 -B scripts/check_nvm_klj3.py --self-test | tail -1; echo klj3 rc=$?
} > "$R/regen_and_small_gates.log" 2>&1
python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4 \
    > "$R/ctrl_nvm_selftest.log" 2>&1; echo $? > "$R/ctrl_nvm_selftest.rc"
make -C tb/verilator/milan_dp -j6 VERILATOR="$V" twin > "$R/twin.log" 2>&1; echo $? > "$R/twin.rc"
make -C tb/verilator/milan_dp -j6 VERILATOR="$V" twin-plants > "$R/twin-plants.log" 2>&1; echo $? > "$R/twin-plants.rc"
git status --porcelain > "$R/status_after.txt"
