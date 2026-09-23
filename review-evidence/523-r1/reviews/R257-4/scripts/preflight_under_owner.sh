#!/usr/bin/env bash
# Run a candidate sweep's own preflight gates, verbatim, under its own process
# owner, without selecting or running any Verilator suite.
# Usage: preflight_under_owner.sh <repo> <outdir> <receipt-dir>
# The functions preflight, prepare_logs and run_preflight_gates are extracted
# byte-for-byte from <repo>/scripts/run_all_suites.sh; their text and digest are
# recorded. The body runs as `owned_process.py -- bash body`, i.e. in a new
# session with descendant adoption and a parent-death binding, as the sweep
# shell does. Terminal INT/TERM traps mirror the sweep's.
set -euo pipefail
repo=$(cd "$1" && pwd)
out=$2
receipts=$3
mkdir -p "$out" "$receipts"
sweep="$repo/scripts/run_all_suites.sh"
funcs="$receipts/extracted_functions.sh"
awk '/^(preflight|prepare_logs|run_preflight_gates)\(\) \{$/{on=1} on{print} on&&/^\}$/{on=0}' "$sweep" > "$funcs"
{
  echo "sweep sha256: $(sha256sum "$sweep" | cut -d' ' -f1)"
  echo "extracted sha256: $(sha256sum "$funcs" | cut -d' ' -f1)"
  echo "extracted lines: $(wc -l < "$funcs")"
  echo "functions: $(grep -cE '^(preflight|prepare_logs|run_preflight_gates)\(\) \{$' "$funcs")"
} > "$receipts/extraction.txt"
body="$receipts/body.sh"
cat > "$body" <<EOF
set -u
ROOT='$repo'
OUT='$out'
LOGS_READY=0
cancelled() {
  echo "CANCELLED: \$1; no completed sweep result" >&2
  exit "\$2"
}
trap 'cancelled INT 130' INT
trap 'cancelled TERM 143' TERM
. '$funcs'
echo "owner-context: pid \$\$ ppid \$PPID sid \$(ps -o sid= -p \$\$ | tr -d ' ') pgid \$(ps -o pgid= -p \$\$ | tr -d ' ')"
grep -E '^(PPid|NSpid)' /proc/\$\$/status
prepare_logs
run_preflight_gates
echo "PREFLIGHT: PASS (every gate returned; containment rc=\${selftest_rc:-unset})"
EOF
set +e
start=$(date +%s)
python3 "$repo/scripts/owned_process.py" -- bash "$body" > "$receipts/owner_stdout.txt" 2> "$receipts/owner_stderr.txt"
rc=$?
end=$(date +%s)
set -e
echo "owner exit: $rc  seconds: $((end - start))" | tee "$receipts/owner_exit.txt"
cp "$out"/preflight/*.log "$receipts/" 2>/dev/null || true
ls -la "$receipts" >> "$receipts/owner_exit.txt"
exit "$rc"
