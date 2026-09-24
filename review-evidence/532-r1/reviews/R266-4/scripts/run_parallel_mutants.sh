#!/usr/bin/env bash
# run_parallel_mutants.sh SOURCE OUTDIR JOBS REPEATS MODES ID...: build the named
# mutants of SOURCE (scripts/act_slot_proof.sh) with proof_mutants.py (or $MUTANTS_PY) into OUTDIR,
# then run each mutant's --selftest REPEATS times in every mode of MODES
# (comma-separated: uid1000,uid0), JOBS self-tests at a time, each inside
# sandbox.sh MODE (new unprivileged user+net namespaces, only `lo`).
# Prints one line per run, sorted: ID rep=R mode=M KILLED|SURVIVED rc=N | failing cases.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
source=$1 outdir=$2 jobs=$3 repeats=$4 modes=$5
shift 5
mkdir -p "$outdir/tmp" "$outdir/runs"
python3 "$here/${MUTANTS_PY:-proof_mutants.py}" "$source" "$outdir" "$@" >"$outdir/list.txt"
one() {
  local ident=$1 mode=$2 rep=$3 rc=0 result failed verdict
  result=$outdir/runs/$ident.$mode.$rep.txt
  TMPDIR=$outdir/tmp "$here/sandbox.sh" "$mode" bash "$outdir/$ident/act_slot_proof.sh" --selftest \
    >"$result" 2>&1 || rc=$?
  failed=$(sed -n 's/^  FAIL \([^:]*\):.*/\1/p' "$result" | paste -sd';' -)
  if [ "$rc" -ne 0 ]; then verdict=KILLED; else verdict=SURVIVED; fi
  printf '%s rep=%s mode=%s %s rc=%s | failing cases: %s\n' "$ident" "$rep" "$mode" "$verdict" \
    "$rc" "${failed:-none}" >"$result.line"
}
export -f one
export outdir here
while IFS=$'\t' read -r ident _described; do
  for mode in ${modes//,/ }; do
    for rep in $(seq 1 "$repeats"); do printf '%s %s %s\n' "$ident" "$mode" "$rep"; done
  done
done <"$outdir/list.txt" | xargs -P "$jobs" -L 1 bash -c 'one "$0" "$1" "$2"'
cat "$outdir"/runs/*.line | sort -V
