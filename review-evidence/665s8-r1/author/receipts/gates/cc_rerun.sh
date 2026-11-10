#!/bin/bash
# cc_rerun.sh: the sweep's shard 2/4 capture_coherence (TIMEOUT at 2400 s, result unknown, on CPUs shared with another
# lane's shard) once more, uncontended, on a fresh clone of the gate head: run_all_suites.sh's own per-suite command
# (`timeout 2400 make -C tb/verilator/capture_coherence`, then `suite_tally.py --verdict` on its log), the sweep's env
S=$VALIDATION_STORAGE/665s8-a758b; H=$(cat $S/gates/HEAD); W=$S/cc-rerun/wt; O=$S/cc-rerun; mkdir -p $O
[ -d $W ] || bash $S/clone_at.sh $H $W > $O/clone.log 2>&1 || exit 3
cd $W || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c \
  TMPDIR=$O/tmp MAKEFLAGS="-j4 --no-print-directory" HOME=$WORKSPACE_HOME
mkdir -p $TMPDIR
{ echo "# head $H capture_coherence re-run (uncontended): timeout 2400 make -C tb/verilator/capture_coherence"; } > $O/capture_coherence.head
start=$(date +%s)
timeout 2400 make -C tb/verilator/capture_coherence > $O/capture_coherence.log 2>&1
rc=$?
echo "make rc=$rc wall=$(( $(date +%s) - start ))s" > $O/make.rc
python3 scripts/suite_tally.py --verdict $O/capture_coherence.log > $O/verdict.log 2>&1
echo "verdict rc=$?" >> $O/make.rc
git status --porcelain --untracked-files=no > $O/tree-after.txt
echo $rc > $O/rc
