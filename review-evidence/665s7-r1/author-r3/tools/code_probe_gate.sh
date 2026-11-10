#!/usr/bin/env bash
# code_probe_gate.sh: R814-1's code_probe.py, unchanged (sha256 0e5d16ae...736c), arms join-10cs and join-15cs, on
# the srptx gate clone of the head after make srptx ran there; then the clone's git status
set -uo pipefail
S=/data-2/milan/tmp/665s7-a757c; T=$MANAGEMENT/2026-09-23/665s7-a757c/tools; V=$VALIDATION_TOOLS/pinned-verilator-5.050
export TMPDIR=$S/tmp VERILATOR=$V/verilator MAKEFLAGS=-j16
export PATH=$V:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
rm -rf $S/cprobe
(cd $S && python3 -I $T/code_probe.py $S/gates/srptx $S/cprobe 2 join-10cs join-15cs) > $S/gates/code-probe.log 2>&1
echo "rc=$?" >> $S/gates/code-probe.log
(cd $S/gates/srptx && git status --porcelain --ignored=no) > $S/gates/code-probe-clean.log 2>&1
echo "rc=$?" >> $S/gates/code-probe-clean.log
