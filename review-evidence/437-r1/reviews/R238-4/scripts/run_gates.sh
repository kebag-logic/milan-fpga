#!/usr/bin/env bash
# Run the #437 documentation gates at the checked-out head with one interpreter.
# Usage: run_gates.sh <python> <repo> <base> <outdir>
set -u
py=$(realpath -s "$1") repo=$2 base=$3 out=$(realpath -m "$4")
mkdir -p "$out"
cd "$repo" || exit 2
{
  echo "python: $("$py" --version 2>&1)"
  echo "head: $(git rev-parse HEAD) tree: $(git rev-parse 'HEAD^{tree}')"
  echo "status-porcelain-lines: $(git status --porcelain | wc -l)"
} > "$out/context.txt"
i=0
while IFS= read -r cmd; do
  i=$((i+1)); n=$(printf %02d $i)
  start=$(date +%s)
  eval "\"$py\" $cmd" > "$out/$n.log" 2>&1
  rc=$?
  printf '%s\trc=%s\t%ss\t%s\n' "$n" "$rc" "$(( $(date +%s) - start ))" "$cmd" >> "$out/EXITS.txt"
done <<CMDS
scripts/gen_toc.py --selftest
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
scripts/check_em_dash.py --selftest
scripts/check_em_dash.py --base $base
scripts/check_py_idiom.py
scripts/check_py_idiom.py --selftest
scripts/ci_events.py --check
scripts/check_hygiene.py --check
scripts/docs_check.py
scripts/check_doc_style.py
scripts/check_doc_paths.py
scripts/check_todo_ownership.py
CMDS
cat "$out/EXITS.txt"
