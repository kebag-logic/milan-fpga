#!/usr/bin/env bash
# poll for up to 540 s: unit anon max, Yosys/firmware/sweep progress; pause Yosys (SIGSTOP) above 10.8 GB unit anon
X=$VALIDATION_STORAGE/scratch/780-a670
cg=$(systemctl --user show milan-780-a670.service -p ControlGroup --value); mx=0
for i in $(seq 1 18); do
  a=$(awk '/^anon /{print int($2/1048576)}' /sys/fs/cgroup$cg/memory.stat); [ $a -gt $mx ] && mx=$a
  if [ $a -gt 10800 ]; then p=$(pgrep -f '^bash $MANAGEMENT/2026-09-23/780-a670/scripts/yosys_run.sh'); [ -n "$p" ] && kill -STOP -- -$(ps -o pgid= -p $p | tr -d ' ') && echo "PAUSED YOSYS at $a MB"; break; fi
  [ -n "${1:-}" ] && [ -e "$1" ] && break
  sleep 30
done
echo "max unit anon ${mx}MB; MemAvailable $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) GB"
echo "yosys: $(cat $X/r/yosys/run.rc 2>/dev/null || echo running) $(grep -c '\[PASS\]' $X/r/yosys/run.log 2>/dev/null) pass $(grep -c '\[FAIL\]' $X/r/yosys/run.log 2>/dev/null) fail"
echo "firmware: $(tail -1 $X/r/firmware/table.txt | cut -c1-90)"
for k in 0 1 2 3; do echo "shard$k $(systemctl --user is-active milan-780-a670-shard$k 2>/dev/null) suites=$(ls $X/sweep/shard-$k/logs 2>/dev/null | wc -l)"; done
