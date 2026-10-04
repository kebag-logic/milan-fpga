#!/usr/bin/env bash
# Run the docs gates the lane names, at the checked-out head, each unpiped with its rc.
# Usage: docs_gates.sh <repo> <md-venv-python> <outdir>
set -u
repo=${1:?repo}; mdpy=${2:?md venv python}; out=${3:?outdir}
mkdir -p "$out"
cd "$repo" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
echo "md python <md-venv>/bin/python: $("$mdpy" -c 'import sys; from importlib.metadata import version as v; print("python", sys.version.split()[0], "cmarkgfm", v("cmarkgfm"), "html5lib", v("html5lib"))' 2>&1)"
i=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  i=$((i+1))
  log="$out/gate_$(printf %02d $i).log"
  eval "$cmd" > "$log" 2>&1
  rc=$?
  printf 'rc=%d  %s  (log %s, %s lines; last: %s)\n' "$rc" "${cmd//\"$mdpy\"/<md-venv>/bin/python}" "$(basename "$log")" "$(wc -l < "$log")" "$(tail -1 "$log" | cut -c1-140)"
done <<EOF
"$mdpy" scripts/docs_check.py
"$mdpy" scripts/check_doc_style.py
"$mdpy" scripts/gen_toc.py --check
"$mdpy" scripts/gen_toc.py --verify-anchors
"$mdpy" scripts/check_em_dash.py --base 6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5
"$mdpy" scripts/check_em_dash.py --base 6f76d612a3191b77ac8a1fe2b9c66da42aeb405a
"$mdpy" scripts/check_em_dash.py --selftest
"$mdpy" scripts/check_doc_paths.py
python3 scripts/ci_scope.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_feature_status.py --self-test
git diff --check 6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5 HEAD
git diff --check 6f76d612a3191b77ac8a1fe2b9c66da42aeb405a HEAD
EOF
