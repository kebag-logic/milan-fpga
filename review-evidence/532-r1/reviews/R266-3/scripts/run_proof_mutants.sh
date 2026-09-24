#!/usr/bin/env bash
# run_proof_mutants.sh SOURCE OUTDIR MODE [ID...]: build the mutants of SOURCE
# (scripts/act_slot_proof.sh) into OUTDIR and run each one's --selftest, one at a
# time, inside sandbox.sh MODE (uid1000 or uid0; new user+net namespaces).
# Prints one line per mutant: ID KILLED|SURVIVED rc=N and the failing cases.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
source=$1 outdir=$2 mode=$3
shift 3
mkdir -p "$outdir"
python3 "$here/proof_mutants.py" "$source" "$outdir" "$@" >"$outdir/list.txt"
mkdir -p "$outdir/tmp"
while IFS=$'\t' read -r ident described; do
  rc=0
  TMPDIR=$outdir/tmp "$here/sandbox.sh" "$mode" bash "$outdir/$ident/act_slot_proof.sh" --selftest \
    >"$outdir/$ident/selftest-$mode.txt" 2>&1 || rc=$?
  failed=$(sed -n 's/^  FAIL \([^:]*\):.*/\1/p' "$outdir/$ident/selftest-$mode.txt" | paste -sd';' -)
  if [ "$rc" -ne 0 ]; then verdict=KILLED; else verdict=SURVIVED; fi
  printf '%s %s rc=%s mode=%s | %s | failing cases: %s\n' "$ident" "$verdict" "$rc" "$mode" \
    "$described" "${failed:-none}"
done <"$outdir/list.txt"
