#!/usr/bin/env bash
# Usage: parent_gates.sh <processor-clone> <scratch-dir> <out-dir>
# Assembles a scratch parent (kebag-logic/milan-fpga dev 931f396e) with the
# protocol-processor gitlink moved to the candidate head and gptp-processor at
# its pin, then runs the three parent checkers that failed in round 1.
set -u
pp=$(cd "$1" && pwd); s=$2; out=$(mkdir -p "$3" && cd "$3" && pwd)
HEAD_PP=00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c
PARENT=931f396ec9f13271e9e67b755e18833d0024f234
GPTP=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
git clone -q --filter=blob:none --no-checkout https://github.com/kebag-logic/milan-fpga.git "$s/parent"
cd "$s/parent" && git checkout -q $PARENT
git submodule init protocol-processor gptp-processor >/dev/null
rm -rf protocol-processor gptp-processor
git clone -q "$pp" protocol-processor && git -C protocol-processor checkout -q $HEAD_PP
git clone -q https://github.com/Mister-M-alt/FPGA-gPTP.git gptp-processor && git -C gptp-processor checkout -q $GPTP
git update-index --cacheinfo 160000,$HEAD_PP,protocol-processor
git submodule status -- protocol-processor gptp-processor
for c in check_cpp_idiom check_py_idiom; do
  python3 scripts/$c.py > "$out/parent-$c.log" 2>&1; echo "rc=$?" >> "$out/parent-$c.log"
done
python3 scripts/measure_test_evidence.py --check > "$out/parent-measure_test_evidence.log" 2>&1
echo "rc=$?" >> "$out/parent-measure_test_evidence.log"
