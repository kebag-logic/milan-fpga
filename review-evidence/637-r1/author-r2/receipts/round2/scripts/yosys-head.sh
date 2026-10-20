#!/usr/bin/env bash
# the full Yosys portability run (every top, structural gates) from a clean clone at the round-2 head
cd <scratch>/sweep-r2 || exit 2
export TMPDIR=<scratch>/r2/tmp
export PATH=<tools>/sv2v-v0.0.12:<scratch>/venv312/bin:$PATH
date -u +%FT%TZ; git rev-parse HEAD; git status --short; yosys -V; sv2v --version
rc=0; syn/yosys/run.sh || rc=$?
echo "YOSYS rc=$rc"; date -u +%FT%TZ
