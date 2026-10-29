#!/bin/sh
# usage: launch.sh <unit suffix> <cpus> <spec.json>: run one recorded-gates
# spec as its own unit (MemoryMax 10G), pinned to <cpus>
set -eu
S=<scratch>
exec systemd-run --user --unit="milan-gptp94-a695b-$1" --collect \
  --property=MemoryMax=10G --setenv=HOME=<home> \
  --setenv=PATH=$S/bin:<user-bin>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  --setenv=TMPDIR=$S/tmp \
  /usr/bin/taskset -c "$2" /usr/bin/python3 \
  <management>/2026-09-21/run-recorded-gates.py "$3"
