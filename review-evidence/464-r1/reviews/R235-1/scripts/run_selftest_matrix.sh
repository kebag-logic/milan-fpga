#!/usr/bin/env bash
# R235: run `avdecc/gen_aem_store.py --self-test` in each scratch extract under
# each available interpreter, recording exit status, arm tallies and the final
# traceback line. -B: no bytecode; -E: ignore PYTHON* env; -s: no user site.
# Usage: run_selftest_matrix.sh <scratch-root> <out-dir>
set -uo pipefail
root=${1:?scratch root}
out=${2:?receipt dir}
mkdir -p "$out"
summary="$out/selftest-matrix.txt"
: > "$summary"
for label in head base src srcbase b7d0 da71; do
  for py in /usr/bin/python3.14 "$HOME/.local/bin/python3.12" "$HOME/.local/bin/python3.11"; do
    [ -x "$py" ] || continue
    ver=$("$py" -c 'import sys;print("%d.%d.%d"%sys.version_info[:3])')
    log="$out/selftest-$label-py$ver.log"
    (cd "$root/$label" && "$py" -B -E -s avdecc/gen_aem_store.py --self-test) > "$log" 2>&1
    rc=$?
    okn=$(grep -c '^\s*\[ok  \]' "$log")
    failn=$(grep -c '^\s*\[FAIL\]' "$log")
    last=$(grep -E '^[A-Za-z]*(Error|Exception)|self-test: (PASS|FAIL)' "$log" | tail -1)
    printf '%-8s py%-8s rc=%s ok=%s FAIL=%s | %s\n' "$label" "$ver" "$rc" "$okn" "$failn" "$last" | tee -a "$summary"
  done
done
