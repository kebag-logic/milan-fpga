#!/bin/bash
# per_pass_probe.sh PROBE_TREE OUT: raise the 1x1/1if polls' base in both stated tables (poll_grade.STATED_US and
# load_grade's 1x1/1if row) from 225 us to each probe figure, and grade the flip check's 1x1/1if rows at each.
set -u
P=$1 O=$2; mkdir -p "$O"; cd "$P" || exit 3
D=tb/verilator/ctrl_service_budget
cp $D/poll_grade.py /tmp/.pg.$$; cp $D/load_grade.py /tmp/.lg.$$
for b in ${BASES:-225 242 243 244}; do
  cp /tmp/.pg.$$ $D/poll_grade.py; cp /tmp/.lg.$$ $D/load_grade.py
  sed -i "s/STATED_US = {1: dict(base=225,/STATED_US = {1: dict(base=$b,/" $D/poll_grade.py
  sed -i "211s/'base': 225,/'base': $b,/" $D/load_grade.py
  echo "base $b: poll $(grep -c "dict(base=$b," $D/poll_grade.py) load $(sed -n 211p $D/load_grade.py | grep -c "'base': $b,")" > "$O/base-$b.log"
  python3 -B $D/flip_grade.py --check --point 1x1/1if >> "$O/base-$b.log" 2>&1; echo $? > "$O/base-$b.rc"
done
cp /tmp/.pg.$$ $D/poll_grade.py; cp /tmp/.lg.$$ $D/load_grade.py; rm -f /tmp/.pg.$$ /tmp/.lg.$$
