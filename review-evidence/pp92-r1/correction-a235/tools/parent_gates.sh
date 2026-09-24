#!/usr/bin/env bash
# parent_gates.sh TAG — run the parent gates that read processor sources in the
# scratch parent clone as it stands (its checked-out commit and gitlink). One log
# per gate; rc.txt lists each exit code.
set -uo pipefail
tag=${1:?tag}
parent=$REVIEWS/pp92-a235-packet/scratch/milan-fpga
out=$REVIEWS/pp92-a235-packet/logs/parent-$tag
mkdir -p "$out"
cd "$parent" || exit 1
{ git log --oneline -1; git submodule status protocol-processor; git status --short; } > "$out/state.txt"
: > "$out/rc.txt"
while read -r gate; do
  [ -z "$gate" ] && continue
  name=$(echo "$gate" | tr ' /' '__')
  # shellcheck disable=SC2086
  timeout 1800 python3 $gate > "$out/$name.log" 2>&1
  echo "rc=$? python3 $gate" >> "$out/rc.txt"
done <<'EOF'
scripts/check_cpp_idiom.py
scripts/check_cpp_idiom.py --list
scripts/check_cpp_idiom.py --selftest
scripts/check_py_idiom.py
scripts/check_py_idiom.py --list
scripts/check_py_idiom.py --selftest
scripts/check_hygiene.py --check
scripts/check_sh_idiom.py
scripts/check_sv_idiom.py
scripts/check_todo_ownership.py
scripts/check_submodule_docs.py
scripts/measure_naming.py --check
scripts/measure_fail_fast.py --check
scripts/measure_test_evidence.py --check
EOF
cat "$out/state.txt" "$out/rc.txt"
