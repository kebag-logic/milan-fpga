#!/usr/bin/env bash
# One revision's pp_top suite from a clean scratch export (01-export.sh): the
# Makefile's own `run` target (fixture guards, default build + run, fixture build
# + run, canonical summed tally), then `name-writes` on the same default model.
# Warnings are split per build from the single log. Usage: 04-pp_top.sh base|r2|head
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); REV=$1; export PATH=$PK/tools:$PATH
cd $PK/scratch/$REV/tb/pp_top && make clean > /dev/null
L=$PK/receipts/04-$REV-run.log
make run VERILATOR=verilator > $L 2>&1; echo "[$REV] make run rc=$?"
make name-writes VERILATOR=verilator > $PK/receipts/04-$REV-name-writes.log 2>&1; echo "[$REV] make name-writes rc=$?"
sed -i "s#$HOME#\$HOME#g; s#$PK#<packet>#g" $L $PK/receipts/04-$REV-name-writes.log
# split: default build = from the first verilator invocation after the guards up to
# ./obj_dir/Vpp_top_sim; fixture build = from the --Mdir obj_vid invocation to ./obj_vid/Vpp_top_vid
awk '/-o Vpp_top_sim$/ && !d {d=1} d==1 && /^\.\/obj_dir\/Vpp_top_sim$/ {d=2} d==1' $L > $PK/scratch/$REV-default-build.txt
awk '/--Mdir obj_vid/ {f=1} f==1 && /^\.\/obj_vid\/Vpp_top_vid$/ {f=2} f==1' $L > $PK/scratch/$REV-fixture-build.txt
for b in default fixture; do
  n=$(grep -cE 'warning:|%Warning' $PK/scratch/$REV-$b-build.txt); echo "[$REV] $b build: $(wc -l < $PK/scratch/$REV-$b-build.txt) log lines, $n warning lines"
  grep -E 'warning:|%Warning' $PK/scratch/$REV-$b-build.txt | sed "s#$PK#<packet>#g" | head -5
done
grep -E '^\[build |checks: .* PASS|^NW:|FAIL' $L | head -12
tail -1 $PK/receipts/04-$REV-name-writes.log | head -1; grep '^NW:' $PK/receipts/04-$REV-name-writes.log
