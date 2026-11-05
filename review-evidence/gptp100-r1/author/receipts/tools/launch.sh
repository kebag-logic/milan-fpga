#!/bin/sh
# usage: launch.sh <unit suffix> <cpus> <spec.json>: one recorded-gates spec as its own unit (MemoryMax 10G)
set -eu
S=<scratch>
exec systemd-run --user --unit="milan-gptp100-a733-$1" --collect \
  --property=MemoryMax=10G --setenv=HOME=<home> \
  --setenv=PATH=$S/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  --setenv=TMPDIR=$S/tmp --setenv=MAKEFLAGS=-j4 \
  /usr/bin/taskset -c "$2" /usr/bin/python3 \
  <home>/milan-fpga-management/2026-09-21/run-recorded-gates.py "$3"
