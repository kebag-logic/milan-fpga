#!/usr/bin/env bash
# Reviewer probe R546-1: unbounded sequential equivalence of two converted
# receivers (gold = upstream receiver, gate = candidate) by k-induction.
# usage: r546_equiv.sh GOLD.v GATE.v WORKDIR   -> exit 0 equivalent, 1 not
set -euo pipefail
gold=$1 gate=$2 work=$3
mkdir -p "$work"
sed 's/^module rxcap(/module gold(/' "$gold" > "$work/gold.v"
sed 's/^module rxcap(/module gate(/' "$gate" > "$work/gate.v"
cat > "$work/equiv.ys" <<EOF
read_verilog $work/gold.v
read_verilog $work/gate.v
proc
opt_clean
miter -equiv -flatten -make_outputs gold gate miter
hierarchy -top miter
flatten
opt_clean
sat -verify -tempinduct -prove trigger 0 -set-init-zero -maxsteps 8 -show-inputs -show-outputs miter
EOF
yosys -q -l "$work/equiv.log" -s "$work/equiv.ys" >/dev/null 2>&1 && rc=0 || rc=$?
if [ "$rc" -eq 0 ] && grep -q 'Induction step proven: SUCCESS' "$work/equiv.log"; then
  echo "EQUIV: PROVEN (k-induction)"; exit 0
fi
echo "EQUIV: NOT PROVEN (yosys rc $rc)"; exit 1
