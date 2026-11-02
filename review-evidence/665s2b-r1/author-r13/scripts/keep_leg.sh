#!/bin/bash
# Keep one harness leg's receipts: build.json, the image digest, the label, results.json.gz, the driver log's end,
# the table, and the save-window analysis of its finished logs, with scratch and home paths replaced.
# usage: keep_leg.sh NAME LABEL
set -u
T=$VALIDATION_STORAGE/665s2b-a683p
S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts
O=$MANAGEMENT/2026-09-23/665s2b-a683p/receipts/measure/$1
mkdir -p "$O"
scrub() { sed -e "s#$T#<scratch>#g" -e "s#$WORKSPACE_HOME#\$HOME#g" -e "s#$VALIDATION_TOOLS#<tools>#g"; }
scrub < "$T/builds/$1/build.json" > "$O/build.json"
(cd "$T/builds/$1" && sha256sum image/ctrl_app.elf) | sed "s#  image/#  <scratch>/builds/$1/image/#" > "$O/image.txt"
printf '%s\n' "$2" > "$O/label.txt"
scrub < "$T/builds/$1/results/results.json" | gzip -n > "$O/results.json.gz"
{ head -1 "$T/logs/$1.log"; tail -80 "$T/logs/$1.log"; } | scrub > "$O/run.log"
scrub < "$T/builds/$1/results/table.md" > "$O/table.md"
logs=$(ls "$T/builds/$1/results/"*@*.log 2>/dev/null)
[ -n "$logs" ] && (ulimit -v 4000000; timeout 600 python3 -I $S/savewin.py $T/C1 $logs) 2>&1 | scrub > "$O/save-windows.txt"
[ -f "$T/builds/$1/results/save.log" ] && (ulimit -v 4000000; timeout 600 python3 -I $S/savephases.py $T/C1 save.change "$T/builds/$1/results/save.log") 2>&1 | scrub > "$O/save-alone.txt"
exit 0
