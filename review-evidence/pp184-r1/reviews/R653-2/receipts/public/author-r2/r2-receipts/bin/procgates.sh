#!/usr/bin/env bash
# procgates.sh <tag> <tree> <export>: the processor gates other than run_suites.sh, in order, via gate.sh
set -u
tag="$1"; tree="$2"; exp="$3"
G=<scratch>/r2/bin/gate.sh
"$G" "$tag-lint"   "$tree" ./scripts/lint_hdl.sh
GATE_VENV=<scratch>/venv-wd "$G" "$tag-check" "$tree" make check
"$G" "$tag-matrix" "$tree" python3 scripts/gen_matrix.py --check
"$G" "$tag-yosys"  "$tree" ./syn/yosys/run.sh
"$G" "$tag-guards" "$exp" python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
echo "procgates $tag done"
