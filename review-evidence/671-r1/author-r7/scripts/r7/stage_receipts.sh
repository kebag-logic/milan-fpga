#!/usr/bin/env bash
# Copy round 7's logs under one staging directory, named as the handoff's gate
# table names them, for collect_receipts.py. Usage: stage_receipts.sh <r7-scratch> <stage>
set -u
r7=$1; stage=$2
rm -rf "$stage"; mkdir -p "$stage"
link() { mkdir -p "$(dirname "$stage/$2")"; cp "$r7/$1" "$stage/$2"; }
link logs/selftest.log selftest.log
link logs/selftest_final.log selftest_final.log
link logs/controls_driver.log controls/driver.log
for f in "$r7"/logs/controls/*.log; do link "logs/controls/$(basename "$f")" "controls/$(basename "$f")"; done
for d in vsuites vsuites_final fwunit rtlfast builder builder_final docsrep final; do
  for f in "$r7/logs/$d"/*.log; do link "logs/$d/$(basename "$f")" "$d/$(basename "$f")"; done
done
for f in driver-a.log driver-b.log; do link "capture/$f" "capture/$f"; done
for arm in 1x1-50-on 1x1-50-off 8x8-50-on 8x8-50-off 8x8-100-on 8x8-100-off; do
  link "capture/run-$arm.log" "capture/run-$arm.log"
  link "capture/$arm/capture-$arm/measurement.json" "capture/$arm/measurement.json"
done
link logs/assemble.log assemble.log
link logs/refresh.log refresh.log
link logs/capture_gate_at_merge.log capture_gate_at_merge.log
link size/fw_size.txt size/fw_size.txt
