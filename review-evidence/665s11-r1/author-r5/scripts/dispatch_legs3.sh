#!/bin/bash
# Launch round 5's second legs as 8-wide ranges free (cpu_ranges.py pick), each its own unit: E1b, SHORTb, and A2b
# once A1b's build exists. Books nothing while it waits; logs to r5/units/dispatch3.log.
set -u
T=<scratch> R=$T/r5 PICK="python3 -I <management>/2026-09-23/cpu_ranges.py pick"
L=$R/units/dispatch3.log
launch() { name=$1; shift; p=$($PICK); [ -n "$p" ] || return 1
  bash $R/scripts/unit.sh $name $p "$@" >> $L 2>&1 && echo "$(date +%T) $name on $p" >> $L; }
pending="E1b SHORTb A2b"
while [ -n "$pending" ]; do
  next=""
  for n in $pending; do
    case $n in
      E1b) launch E1b bash $R/scripts/leg.sh $R/fp2 $R/legs2/E1 1x1 8 --variant answering-every-port || next="$next E1b";;
      SHORTb) launch SHORTb env LEGS=legs2 bash $R/scripts/short_legs2.sh $R/fp2 || next="$next SHORTb";;
      A2b) if [ -s $R/legs2/A/build.json ] && [ -e $R/legs2/A/native/Vsim ] && grep -q '^COMMAND .*native/Vsim' $R/units/A1b.log 2>/dev/null; then
             launch A2b bash $R/scripts/armA2.sh 2 $R/fp $R/legs2/A $R/units/A1b.log || next="$next A2b"
           else next="$next A2b"; fi;;
    esac
  done
  pending=$(echo $next)
  [ -n "$pending" ] && sleep 60
done
echo "$(date +%T) all launched" >> $L
