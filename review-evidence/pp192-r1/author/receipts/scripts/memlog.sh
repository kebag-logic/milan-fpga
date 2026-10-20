#!/usr/bin/env bash
# samples this session's service unit's MemoryCurrent every 15 s into memlog.txt (bytes)
U=$(sed -n 's#^0::.*/##p' /proc/self/cgroup)
while :; do
  m=$(systemctl --user show "$U" -p MemoryCurrent --value 2>/dev/null)
  echo "$(date +%s) $m $(pgrep -c -f 'pinned-verilator-5.050/verilator' || true)" >> <scratch>/memlog.txt
  sleep 15
done
