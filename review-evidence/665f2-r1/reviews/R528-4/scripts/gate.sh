#!/usr/bin/env bash
# Run one named gate command from a repository root, recording its log,
# exit code, wall time and peak RSS under a receipts directory.
# Usage: gate.sh <repo-root> <receipts-dir> <name> <command...>
# Environment: MILAN_RV32_CC (pinned SDK compiler), VERILATOR_BIN_DIR (optional,
# prepended to PATH).
set -u
root=$1; out=$2; name=$3; shift 3
mkdir -p "$out"
if [ -n "${VERILATOR_BIN_DIR:-}" ]; then PATH="$VERILATOR_BIN_DIR:$PATH"; export PATH; fi
cd "$root" || exit 99
start=$(date +%s)
{ echo "# gate $name"; echo "# cwd $(pwd)"; echo "# head $(git rev-parse HEAD 2>/dev/null)";
  echo "# cmd $*"; echo "# start $(date -u +%FT%TZ)"; } > "$out/$name.log"
/usr/bin/time -f '# maxrss_kb %M' -a -o "$out/$name.log" "$@" >> "$out/$name.log" 2>&1
rc=$?
end=$(date +%s)
echo "# end $(date -u +%FT%TZ) wall_s $((end - start)) rc $rc" >> "$out/$name.log"
echo "$rc" > "$out/$name.rc"
exit "$rc"
