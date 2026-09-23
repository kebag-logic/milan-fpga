set -u
ROOT='<candidate-clone>'
OUT='<packet>/scratch/preflight-out'
LOGS_READY=0
cancelled() {
  echo "CANCELLED: $1; no completed sweep result" >&2
  exit "$2"
}
trap 'cancelled INT 130' INT
trap 'cancelled TERM 143' TERM
. 'receipts/preflight_under_owner/extracted_functions.sh'
echo "owner-context: pid $$ ppid $PPID sid $(ps -o sid= -p $$ | tr -d ' ') pgid $(ps -o pgid= -p $$ | tr -d ' ')"
grep -E '^(PPid|NSpid)' /proc/$$/status
prepare_logs
run_preflight_gates
echo "PREFLIGHT: PASS (every gate returned; containment rc=${selftest_rc:-unset})"
