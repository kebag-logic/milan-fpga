#!/bin/bash
# The round 2 runs of this packet, in order. Round 1's scripts are used unchanged (receipts/r1-scripts.sha256).
# usage: TOOLS=<pinned toolchain dir> runs.sh REPO   (REPO: a clone holding a530ecaf, 9043b926, 9deb0ddb, fa31d4c8, ea4af6f)
# Two compiler variants, each a directory whose scratch/bin is first in PATH (env.sh):
#   pinned: scratch/bin/{clang,clang++,clang-18} -> the pinned Clang 18.1.3 (round 1's setup)
#   host:   scratch/hostclang/scratch/bin/{clang,clang++} -> the host's Clang, clang-18 -> the pinned Clang 18.1.3,
#           with a byte-identical copy of scripts/ in scratch/hostclang/scripts
set -eu
REPO=$1; D=$(cd "$(dirname "$0")/.." && pwd); S=$D/scratch; H=a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e
bash $D/scripts/ci_run.sh "$REPO" $H $S/ciA                         # pinned clang as clang++
bash $S/hostclang/scripts/ci_run.sh "$REPO" $H $S/ciB               # host clang as clang/clang++
for M in 16 32 33 64 255; do bash $D/scripts/build_dwalk.sh "$REPO" $H 9deb0ddb $S/dwalk-$M $M; done
bash $D/scripts/matrix.sh $S $S/matrix 20000
python3 -I $D/scripts/plant_merge_audit.py "$REPO" ea4af6f fa31d4c8 9deb0ddb $H
python3 -I $D/scripts/plant_delta.py "$REPO" 9043b926 $H
bash $D/scripts/merge_survival.sh "$REPO" ea4af6f fa31d4c8 9deb0ddb $H CMakeLists.txt include/acmp.h scripts/mutation.py \
     src/acmp.c tests/test_acmp.cpp tests/test_acmp_walk.cpp tests/test_acmp_wide.cpp
python3 -I $D/scripts/plant_kills.py $S/ciB/build-validation/mutations/results.json $S/ciB/src/tests/mutations.json
python3 -I $D/scripts/plant_failures.py $S/ciB/build-validation/mutations/results.json walk-bind-second-word-unmarked \
     walk-unbind-second-word-unmarked walk-release-second-word-unmarked walk-probe-left-second-word-unmarked \
     walk-marks-never-cleared walk-interface-marks-never-cleared walk-clear-first-word-only
# probe controls: round 1's plant diffs applied to the head's src/acmp.c (patch -o)
for c in c1-started-unmarked c2-release-mark-word0 c3-release-mark-low-only c4-probe-left-mark-word0; do
  bash $D/scripts/suite_on_plant.sh "$REPO" $H $S/plants/$c.c $S/sop-$c
  bash $D/scripts/build_dwalk.sh "$REPO" $H 9deb0ddb $S/dw-$c 33 $S/plants/$c.c
  for L in 0 1; do env LIFT=$L SINKS=33 STEPS=20000 SEED=1 $S/dw-$c/dwalk | head -1; done
done
bash $D/scripts/sanitizer_gate.sh $S/ciB/src $S/san "$(command -v clang)" "$(command -v clang++)"
bash $D/scripts/struct_size.sh "$REPO" 9deb0ddb $H $S/ssize
python3 -I $D/scripts/verify_manifest.py "${EVIDENCE:?set EVIDENCE to review-evidence/tsn32-r1 of milan-fpga bd10795e}"
