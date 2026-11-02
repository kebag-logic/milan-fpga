#!/bin/sh
# Round 6 sweeps on a clean clone of the head and on four RTL mutant copies.
# Usage: run_sweeps.sh <scratch> <out> <name>...
# Names: head (the clone), round4 (the clone, against the 79fdea05 page),
# m1 m2 m4 m5 (copies of the head with the reviewers' RTL patches applied).
# Runs the named sweeps at once; each writes <name>.log, .rc and .time.
S=$1; O=$2; shift 2
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
mkdir -p "$O"
verilator --version > "$O/verilator_version.txt" 2>&1
one() {
  n=$1
  case $n in
    head)   set -- "$S/clone/scripts/register_read_sweep.py" --work "$S/w/$n" ;;
    round4) set -- "$S/clone/scripts/register_read_sweep.py" --page "$S/page_round4.md" --work "$S/w/$n" ;;
    *)      set -- "$S/$n/scripts/register_read_sweep.py" --work "$S/w/$n" ;;
  esac
  /usr/bin/time -f "maxrss_kb=%M elapsed=%e" -o "$O/sweep_$n.time" python3 -I -B "$@" > "$O/sweep_$n.log" 2>&1
  echo $? > "$O/sweep_$n.rc"
}
for n in "$@"; do one "$n" & done
wait
for n in "$@"; do echo "sweep_$n rc=$(cat "$O/sweep_$n.rc") $(cat "$O/sweep_$n.time")"; tail -1 "$O/sweep_$n.log"; done
