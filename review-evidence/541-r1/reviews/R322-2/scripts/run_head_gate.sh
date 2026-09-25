#!/bin/sh
# Export a commit to a disposable tree and run the crf_rx receiver gate with a
# pinned simulator. Usage: run_head_gate.sh <repo> <rev> <scratch-dir> <verilator>
set -eu
repo=$1; rev=$2; dest=$3; V=$4
rm -rf "$dest"; mkdir -p "$dest"
git -C "$repo" archive "$rev" | tar -x -C "$dest"
"$V" --version
cd "$dest/tb/verilator/crf_rx"
make VERILATOR="$V" discontinuity-build >build.log 2>&1 || { tail -50 build.log; exit 2; }
echo "== discontinuity at $rev =="
set +e
./obj_discontinuity/Vdiscontinuity > disc.log 2>&1; drc=$?
set -e
grep -E '^\[FAIL\]|RESULT|checks' disc.log | tail -20
grep -cE '^\[PASS\]' disc.log | sed 's/^/pass lines: /'
echo "discontinuity rc=$drc"
if [ "${MUTANTS:-1}" = 1 ]; then
  echo "== mutants.py at $rev =="
  set +e
  VERILATOR="$V" python3 mutants.py; mrc=$?
  set -e
  echo "mutants rc=$mrc"
fi
