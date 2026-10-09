#!/usr/bin/env bash
# Shape self-test with GNU Make 4.3 first on PATH. Arg 1: make-4.3 bin dir.
set -u
export PATH="$1:$PATH" PYTHONDONTWRITEBYTECODE=1
command -v make
make --version | head -1
python3 scripts/check_entity_shape.py --self-test
