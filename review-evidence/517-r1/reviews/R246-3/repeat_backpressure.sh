#!/bin/sh
# Prior R246-1 F2 re-check: run test_sim_pool_backpressure.py N times with
# SIGINT at its default and N times inherited ignored (as `cmd &` in a
# non-interactive shell gives it). usage: repeat_backpressure.sh <clone> <N>
D="$1/tb/verilator/milan_dp"; N="$2"
cd "$D" || exit 2
fail=0
for mode in default ignored; do
  i=1
  while [ "$i" -le "$N" ]; do
    if [ "$mode" = ignored ]; then
      out=$(sh -c "trap '' INT; exec python3 test_sim_pool_backpressure.py" 2>&1); rc=$?
    else
      out=$(python3 test_sim_pool_backpressure.py 2>&1); rc=$?
    fi
    printf 'mode=%s run=%s rc=%s %s\n' "$mode" "$i" "$rc" "$(printf '%s\n' "$out" | tail -n 1)"
    [ "$rc" -eq 0 ] || fail=1
    i=$((i+1))
  done
done
echo "REPEAT_FAIL=$fail"
exit "$fail"
