#!/usr/bin/env bash
# Disposable mutation probes of scripts/ci_scope.py --selftest.
# Usage: ci_scope_mutants.sh <checkout> <head-sha> <parent-sha> <scratch-dir> <receipt-dir>
set -u
repo=$1 head=$2 parent=$3 scratch=$4 rec=$5
mkdir -p "$scratch" "$rec"
probe() {  # name, python mutation snippet operating on variable s (file text)
  name=$1 mut=$2 d="$scratch/$1"
  rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive "$head" | tar -x -C "$d"
  (cd "$d" && git init -q && git add -A >/dev/null 2>&1)
  if [ -n "$mut" ]; then
    python3 -I - "$d/scripts/ci_scope.py" "$repo" "$parent" <<PY
import sys, subprocess
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
orig = s
$mut
assert s != orig, "mutation did not apply"
open(p, "w", encoding="utf-8").write(s)
PY
    [ $? -eq 0 ] || { echo "$name APPLY-FAILED" >> "$rec/ci_scope_mutants.tsv"; return; }
  fi
  (cd "$d" && python3 -I scripts/ci_scope.py --selftest) > "$rec/mutant_$name.log" 2>&1
  rc=$?
  printf '%s\trc=%s\tFAIL-lines=%s\n' "$name" "$rc" "$(grep -c '^  FAIL' "$rec/mutant_$name.log")" >> "$rec/ci_scope_mutants.tsv"
}
: > "$rec/ci_scope_mutants.tsv"
probe M0_control ""
probe M1_drop_table_entry 's = s.replace("    \"docs/design/MAILBOX_SPLIT.md\",\n", "", 1)'
probe M2_drop_case 's = s.replace("        ([\"docs/design/MAILBOX_SPLIT.md\"], True),\n", "", 1)'
probe M3_parent_ci_scope 's = subprocess.run(["git","-C",sys.argv[2],"show",sys.argv[3]+":scripts/ci_scope.py"],capture_output=True,text=True,check=True).stdout'
cat "$rec/ci_scope_mutants.tsv"
