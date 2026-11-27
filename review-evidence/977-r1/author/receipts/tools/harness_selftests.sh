#!/bin/bash
# harness_selftests.sh CLONE OUT: the CPU budget harness's self-tests and checks in CLONE, each output into OUT.
C=$1 O=$2; mkdir -p "$O"; cd "$C/tb/verilator/ctrl_service_budget" || exit 3
H=$(git -C "$C" rev-parse --short=8 HEAD)
for t in "run.py --self-test" "kept_grade.py --selftest" "load_grade.py --selftest" "load_grade.py --check" \
         "flip_grade.py --selftest" "flip_grade.py --check --point 1x1/1if" "flip_grade.py --check --point 8x8/1if" \
         "shape_costs.py --selftest" "shape_costs.py --check"; do
  f=$O/$(echo "$t" | tr ' /' '__' | tr -s '_')-$H.txt
  python3 -B -I $t > "$f" 2>&1; echo "$t rc=$? $(tail -n 1 "$f" | cut -c1-100)"
done
