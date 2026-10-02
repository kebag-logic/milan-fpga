#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer checks (R433-2) under a real GNU make 4.3, the hosted runner's make.
# Usage: make43_checks.sh <disposable checkout of the head> <dir holding a make 4.3 binary named make>
#   1. the root suite's nested derivation as mclk_mutants.py runs it (parent make -C hands
#      MAKEFLAGS=w): count verilator command lines polluted by "Entering directory",
#      at the round-1 Makefile (57f4b742) and at the head;
#   2. scripts/check_entity_shape.py --self-test (the hosted docs-check step "Entity shape gate")
#      at the head, under make 4.3 and under the host make.
# Build make 4.3 from https://ftp.gnu.org/gnu/make/make-4.3.tar.gz
# (sha256 e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19).
set -u
T=$(cd "$1" && pwd); M43=$(cd "$2" && pwd)
cd "$T"
for rev in 57f4b742b504f5e69293aaa3e00d0470aa9b6071 HEAD; do
  git show "$rev:tb/verilator/milan_dp_mclk/Makefile" > tb/verilator/milan_dp_mclk/Makefile
  n=$(MAKEFLAGS=w MAKELEVEL=1 PATH="$M43:$PATH" make -s -C tb/verilator/milan_dp_mclk -n mclk-build 2>&1 \
      | grep -- '--Mdir' | grep -c 'Entering directory')
  echo "Makefile at $rev: verilator command lines carrying 'Entering directory' under make 4.3: $n"
done
git checkout -q -- tb/verilator/milan_dp_mclk/Makefile
echo "== check_entity_shape.py --self-test, make 4.3"
PATH="$M43:$PATH" python3 scripts/check_entity_shape.py --self-test > /tmp/es43.$$ 2>&1; echo "gate rc=$?"; tail -n 2 /tmp/es43.$$
echo "== check_entity_shape.py --self-test, host make ($(make --version | head -1))"
python3 scripts/check_entity_shape.py --self-test > /tmp/es44.$$ 2>&1; echo "gate rc=$?"; tail -n 2 /tmp/es44.$$
rm -f /tmp/es43.$$ /tmp/es44.$$
