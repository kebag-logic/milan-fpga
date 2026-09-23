#!/usr/bin/env bash
# Export one revision of the protocol-processor clone with `git archive` into a
# disposable directory and run the named Verilator suites there (default: the
# four SRP suites). The clone itself is never built in or written to.
#
# usage: run_srp_suites.sh <rev> <export-dir> [suite ...]
# env:   CLONE     path of the reviewed clone   (default: current directory)
#        VERILATOR simulator wrapper            (default: verilator on PATH)
#        JOBS      parallel suite builds, <= 8  (default: 4)
set -euo pipefail
rev=${1:?rev}; out=${2:?export dir}; shift 2
suites=("$@"); [ ${#suites[@]} -gt 0 ] || suites=(srp_decoder srp_encoder srp_stream_fsms srp_top)
CLONE=${CLONE:-$PWD}; VERILATOR=${VERILATOR:-verilator}; JOBS=${JOBS:-4}
[ "$JOBS" -le 8 ] || JOBS=8
rm -rf "$out"; mkdir -p "$out"
git -C "$CLONE" archive "$rev" | tar -x -C "$out"
echo "export: $(git -C "$CLONE" rev-parse "$rev") -> $out"
run_one() {
  local s=$1
  if (cd "$out/tb/$s" && make VERILATOR="$VERILATOR") >"$out/$s.log" 2>&1; then st=PASS; else st=FAIL; fi
  t=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/$s.log" | tail -1 || true)
  echo "$st $s ($t)"
}
export -f run_one; export out VERILATOR
printf '%s\n' "${suites[@]}" | xargs -P "$JOBS" -I{} bash -c 'run_one {}' | sort
