#!/usr/bin/env bash
# Guard self-test with the pinned sv2v 0.0.12 first on PATH. Arg 1: its bin dir.
set -u
export PATH="$1:$PATH" PYTHONDONTWRITEBYTECODE=1
yosys -V
sv2v --version
python3 syn/yosys/guard_selftest.py
