#!/bin/sh
# Usage: probes.sh <packet-dir> <verilator>
# Runs, concurrently, in disposable copies of the exact head under <packet>/scratch:
#   head : the engine suite (make run, four passes)
#   p1   : planted defect, receipt-timeout leg shifts flags by 1 (asCapable onto sync-ok)
#   p2   : planted defect, receipt-timeout leg shifts flags by 3 (gmPresent onto sync-ok)
# and regenerates the four tracked ROM images, comparing each to the committed bytes.
set -u
P=$1; V=$2; S=$P/scratch; R=$P/receipts
G=hdl/ucode/gen_gptp_ucode.py
OLD='    p.emit("ALU", rd=RU, ra=RT, rb=0, cnd=ALU_SHL, imm=SYNCOK_BY_AMGM_C)'
for k in 1 3; do
  d=$S/p$([ $k = 1 ] && echo 1 || echo 2)
  python3 -I - "$d/$G" "$OLD" "$k" <<'PY'
import sys
f,old,k=sys.argv[1:4]; s=open(f).read(); assert s.count(old)==1
open(f,'w').write(s.replace(old, old.replace('imm=SYNCOK_BY_AMGM_C','imm=%s'%k)))
PY
done
run() { ( cd "$S/$1/tb/verilator/engine" && make -B run VERILATOR="$V" ) > "$R/$1-engine.log" 2>&1; echo "$1 rc=$?" > "$R/$1-engine.rc"; }
run head & run p1 & run p2 &
( cd $S/head && I=$S/img && mkdir -p $I &&
  python3 $G --clk-hz 2000000 --cease-ms 3000 -o $I/engine.hex &&
  python3 $G -o $I/ucpu.hex && python3 $G --clk-hz 2000000 -o $I/tsngen.hex && python3 $G -o $I/ooc.hex &&
  for x in engine:tb/verilator/engine ucpu:tb/verilator/ucpu tsngen:tb/tsngen ooc:syn/ooc/work; do
    n=${x%%:*}; t=${x#*:}/gptp_ucode.hex
    if cmp -s $I/$n.hex $t; then echo "$n identical $(sha256sum < $t | cut -c1-64)"; else echo "$n DIFFERS"; fi
  done ) > $R/images.log 2>&1
wait
cat $R/*-engine.rc
