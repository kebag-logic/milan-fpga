#!/bin/sh
# Round R754-6 probes at head 2c500d0a. Usage: run_probes.sh <packet-dir>
# Trees under scratch/t/ are `git archive` extracts of the head (head, m1, m2,
# m4, m5) and of ef7dc985 (prev, prev_m4); m* carry the round 5 mutation
# patches (receipts/patches). Two sweeps at a time: each Verilator build is -j 8.
#   head        head sweep, head page                      want rc 0
#   m1 m2 m4 m5 head sweep over a srp_fresh_r clear mutant  want rc 1
#   oldpage     head sweep, 79fdea05 page (round 4 wording) want rc 1
#   prev_m4     ef7dc985 sweep over m4                     rc 0 shows the delta is what catches m4
set -u
P=$1; S=$P/scratch; R=$P/receipts
mkdir -p "$R" "$S/w"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
verilator --version > "$R/verilator_version.txt" 2>&1
one() {
  n=$1
  case $n in
    oldpage) python3 -I "$S/t/head/scripts/register_read_sweep.py" --page "$S/page_round4_wording.md" --work "$S/w/$n" ;;
    *)       python3 -I "$S/t/$n/scripts/register_read_sweep.py" --work "$S/w/$n" ;;
  esac > "$R/sweep_$n.log" 2>&1
  echo $? > "$R/sweep_$n.rc"
}
for pair in "head m4" "m1 m2" "m5 oldpage" "prev_m4"; do
  for n in $pair; do one "$n" & done
  wait
done
for f in "$R"/sweep_*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") :: $(tail -1 "${f%.rc}.log")"; done
