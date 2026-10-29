#!/bin/bash
# Keep one harness leg's receipts: build.json, the image digest, the label, results.json.gz, the driver log and the
# table, with scratch and home paths replaced.
# usage: keep_leg.sh NAME LABEL
set -u
T=$VALIDATION_STORAGE/665s2b-a683m
O=$MANAGEMENT/2026-09-23/665s2b-a683m/receipts/measure/$1
mkdir -p "$O"
scrub() { sed -e "s#$T#<scratch>#g" -e "s#$WORKSPACE_HOME#\$HOME#g" -e "s#$VALIDATION_TOOLS#<tools>#g"; }
scrub < "$T/builds/$1/build.json" > "$O/build.json"
(cd "$T/builds/$1" && sha256sum image/ctrl_app.elf) | sed "s#  image/#  <scratch>/builds/$1/image/#" > "$O/image.txt"
printf '%s\n' "$2" > "$O/label.txt"
scrub < "$T/builds/$1/results/results.json" | gzip -n > "$O/results.json.gz"
scrub < "$T/logs/$1.log" > "$O/run.log"
scrub < "$T/builds/$1/results/table.md" > "$O/table.md"
ls -la "$O"
