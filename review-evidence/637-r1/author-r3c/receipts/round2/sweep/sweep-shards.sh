#!/usr/bin/env bash
# the full suite sweep at the round-2 head as the runner's four shards, one after another, each a complete
# run with its own log dir and rc; a shard already passed (rc file 0) is not rerun, a cut one reruns whole
cd <scratch>/sweep-r2 || exit 2
export TMPDIR=<scratch>/r2/tmp
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2 SIM_JOBS=2 MAKEFLAGS="-j2 --no-print-directory"
base=<scratch>/r2/sweep-shards; mkdir -p "$base"
for i in 0 1 2 3; do
  rcf="$base/shard-$i.rc"
  if [ -f "$rcf" ] && [ "$(cat "$rcf")" = 0 ]; then continue; fi
  rm -f "$rcf"
  out="$base/logs-$i"; rm -rf "$out"; mkdir -p "$out"
  {
    date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; python3 --version
    rc=0; scripts/run_all_suites.sh "$out" --shard "$i/4" || rc=$?
    echo "SHARD $i/4 rc=$rc"; date -u +%FT%TZ
    echo "$rc" > "$rcf"
  } > "$base/shard-$i.log" 2>&1
done
echo done > "$base/ALL-DONE"
