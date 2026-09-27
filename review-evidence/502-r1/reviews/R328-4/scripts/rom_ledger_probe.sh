#!/bin/sh
# R328-4 disposable probe: prove ooc.sh consumes the candidate pin's ROM ledger rows.
# A: drop the 870ff88a rows -> expect a "no recorded content digest" refusal.
# B: corrupt the 870ff88a ucode.hex digest -> expect a "content digest mismatch" refusal.
# The tracked ledger is restored from HEAD after each arm and its blob id re-verified.
# Usage: rom_ledger_probe.sh <candidate-clone> <receipt-dir> <ooc-tmp>
set -u
C=$1; OUT=$2; T=$3
PIN=870ff88ad35bbd532244e4c7e6d7661b9f6e1366
L=syn/yosys/rom_digests.tsv
cd "$C" || exit 2
mkdir -p "$OUT" "$T"
want=$(git rev-parse "HEAD:$L")
restore() {
  git checkout -- "$L"
  got=$(git hash-object "$L")
  [ "$got" = "$want" ] || { echo "RESTORE FAILED $got != $want"; exit 3; }
  echo "restored $L blob $got"
}
verdict=0
# Arm A
grep -v "^$PIN	" "$L" > "$T/ledger.a" && cp "$T/ledger.a" "$L"
OOC_TMP="$T/a" bash syn/yosys/ooc.sh KL_pp_shadow > "$OUT/probe_A.log" 2>&1; rcA=$?
restore
if [ "$rcA" -ne 0 ] && grep -q "no recorded content digest" "$OUT/probe_A.log"; then
  echo "A: refused as expected (rc $rcA)"; else echo "A: NOT refused (rc $rcA)"; verdict=1; fi
# Arm B
awk -v p="$PIN" 'BEGIN{FS=OFS="\t"} $1==p && $2=="ucode.hex"{$3="0000000000000000000000000000000000000000000000000000000000000000"} {print}' "$L" > "$T/ledger.b" && cp "$T/ledger.b" "$L"
OOC_TMP="$T/b" bash syn/yosys/ooc.sh KL_pp_shadow > "$OUT/probe_B.log" 2>&1; rcB=$?
restore
if [ "$rcB" -ne 0 ] && grep -q "content digest mismatch" "$OUT/probe_B.log"; then
  echo "B: refused as expected (rc $rcB)"; else echo "B: NOT refused (rc $rcB)"; verdict=1; fi
git diff --quiet -- "$L" && echo "ledger clean vs index"
exit $verdict
