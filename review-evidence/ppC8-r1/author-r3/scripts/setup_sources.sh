#!/bin/bash
# Fetch the parent's pinned submodules and PR #634 into scratch (no lane checkout used).
set -euo pipefail
S=$VALIDATION_STORAGE/c8-a501/src
cd "$S"
[ -d gptp-processor.git ] || git clone --bare -q https://github.com/Mister-M-alt/FPGA-gPTP.git gptp-processor.git
git -C gptp-processor.git cat-file -e 5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d^{commit}
[ -d verilog-axis.git ] || git clone --bare -q https://github.com/alexforencich/verilog-axis verilog-axis.git
git -C verilog-axis.git cat-file -e 48ff7a7e2ef782cf778d47910cf85835c64b1bce^{commit}
[ -d milan-fpga-pr634.git ] || git init --bare -q milan-fpga-pr634.git
git -C milan-fpga-pr634.git fetch -q https://github.com/kebag-logic/milan-fpga.git +refs/pull/634/head:refs/heads/pr634
git -C milan-fpga-pr634.git rev-parse pr634
echo SOURCES-OK
