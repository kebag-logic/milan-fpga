#!/usr/bin/env bash
# Log this unit's memory.current and anon bytes every 15 s while the given
# PID lives (polled every 5 s). Above 16 GB current, reclaim the unit's page
# cache. Above 17 GB anon, stop this unit's Vivado (nothing outside the
# unit): that is a failed measurement, never a silent overrun.
pid=$1; out=$2
cg=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-686-a565c.service
stop_vivado() {  # signal
  local p
  for p in $(cat "$cg/cgroup.procs"); do
    grep -q 'Xilinx/2026.1/Vivado' "/proc/$p/cmdline" 2>/dev/null && kill "-$1" "$p"
  done
}
n=0
while kill -0 "$pid" 2>/dev/null; do
  cur=$(cat "$cg/memory.current")
  anon=$(awk '$1=="anon"{print $2}' "$cg/memory.stat")
  [ $((n % 3)) -eq 0 ] && printf '%s %s %s\n' "$(date +%T)" "$cur" "$anon" >> "$out"
  n=$((n + 1))
  if [ "$cur" -gt 16000000000 ]; then
    echo 1G > "$cg/memory.reclaim" 2>/dev/null
  fi
  if [ "$anon" -gt 17000000000 ]; then
    printf '%s %s %s GUARD: stopping this unit'"'"'s vivado\n' "$(date +%T)" "$cur" "$anon" >> "$out"
    stop_vivado TERM; sleep 10; stop_vivado KILL
  fi
  sleep 5
done
