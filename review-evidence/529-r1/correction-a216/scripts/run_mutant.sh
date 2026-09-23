#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# [A216] #529: build one sim_nxn leg against a datapath copy through the
# suite's own recipe (legs.mk), run it, and keep a receipt:
#   run_mutant.sh <nxn|nxndv|nxn8|nxn4c|notify> <datapath.sv> <tag> [harness]
# [harness] is a sim_nxn.cpp copy inside the suite directory (default: the
# tracked one), so a baseline harness can be run against the same mutant.
# The receipt names the datapath and harness hashes, the build and run exit
# codes, every [FAIL] line and the tally. The full run log is kept gzipped;
# the build directory is removed.
set -u
O=$MANAGEMENT/2026-09-23/529-a216
SUITE=$LANES/529-crf-input-counters/tb/verilator/milan_dp
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
leg=$1; dp=$(readlink -f "$2"); tag=$3; cpp=${4:-sim_nxn.cpp}
M=$O/scratch/obj_$tag
L=$O/logs/mutants/$tag.txt
mkdir -p "$O/logs/mutants" "$O/scratch"
cd "$SUITE" || exit 2
rm -rf "$M"
{
  echo "# leg=$leg tag=$tag"
  echo "# datapath sha256 $(sha256sum "$dp" | cut -d' ' -f1)"
  echo "# harness  sha256 $(sha256sum "$cpp" | cut -d' ' -f1) ($cpp)"
  echo "# simulator $(verilator --version)"
} > "$L"
make -f Makefile -f "$O/scripts/legs.mk" "a_$leg" DP_SRC="$dp" A_MDIR="$M" A_CPP="$cpp" \
  VERILATOR_JOBS=8 > "$M.build.log" 2>&1
brc=$?
echo "# build exit $brc" >> "$L"
if [ $brc -ne 0 ]; then
  tail -30 "$M.build.log" >> "$L"
  echo "$tag $leg BUILD-FAILED"
  exit 1
fi
bin=$(ls "$M"/Vmilan_dp_*)
"$bin" > "$M.run.log" 2>&1
rrc=$?
echo "# run exit $rrc" >> "$L"
grep -E '\[FAIL\]' "$M.run.log" >> "$L"
tail -2 "$M.run.log" >> "$L"
gzip -c "$M.run.log" > "$O/logs/mutants/$tag.run.log.gz"
tally=$(grep -E '^checks:' "$M.run.log" | tail -1)
crf=$(grep -cE '\[FAIL\] \[(CTRS|NOTIFY)-CRF\]' "$M.run.log")
echo "$tag $leg run-exit=$rrc $tally crf-red=$crf"
rm -rf "$M" "$M.build.log" "$M.run.log"
