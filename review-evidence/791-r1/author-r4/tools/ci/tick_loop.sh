#!/usr/bin/env bash
# tick_loop.sh <seconds>: tick the replay (up to 3 booked units) once a minute for <seconds>.
end=$(( $(date +%s) + $1 ))
cd "$(dirname "$0")"
while [ "$(date +%s)" -lt "$end" ]; do
  python3 ci_replay.py tick 596e2ae3708c4693e0929b530fea37020dc8db25 3 | grep -v "^no free"
  sleep 60
done
