#!/usr/bin/env bash
# Documentation gates at one tree: `make -j16 check` (the CI docs-gates job's
# target) and the module/testbench matrix check, each with its own log and rc.
# usage: gates.sh TREE LOGDIR TAG
# env:   WAVEDROM_VENV_BIN  directory whose python3 imports wavedrom 2.0.3.post3
set -uo pipefail
tree=$1; out=$2; tag=$3
mkdir -p "$out"
export PATH="${WAVEDROM_VENV_BIN:?}:$PATH"
{
  echo "tree: $(git -C "$tree" rev-parse HEAD) $(git -C "$tree" rev-parse 'HEAD^{tree}')"
  echo "python3: $(command -v python3)"; python3 -c 'import importlib.metadata as m; print("wavedrom", m.version("wavedrom"))'
  echo "mmdc: $(mmdc --version)"
} > "$out/$tag.tools.txt" 2>&1
( cd "$tree" && make -j16 check ) > "$out/$tag.make-check.log" 2>&1
echo $? > "$out/$tag.make-check.rc"
( cd "$tree" && python3 scripts/gen_matrix.py --check ) > "$out/$tag.gen-matrix.log" 2>&1
echo $? > "$out/$tag.gen-matrix.rc"
test -z "$(git -C "$tree" status --porcelain --untracked-files=no)"
echo $? > "$out/$tag.tree-clean-after.rc"
cat "$out/$tag".*.rc
