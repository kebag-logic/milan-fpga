#!/usr/bin/env bash
# collect_route.sh <image-root> <stem> <directive> <label>: one route's receipts into round2/receipts/route/<label>/:
# the sign-off per corner, the placed utilisation (util.py's columns and the report itself, host paths removed), the
# identity gate's line, the planned control memory, and the bitstream's sha256 and size.
set -u
R=$1; STEM=$2; D=$3; L=$4
H=$MANAGEMENT/2026-09-23/923-a789/round2
O=$H/receipts/route/$L; mkdir -p "$O"
W=$R/$STEM; G=$W/build_$D/gateware
LOG=/data-2/milan/tmp/923-a789/logs/$( [ "$R" = /data-2/milan/tmp/923-a789/image ] && echo "image-$STEM-$D" || echo "baseimage-$STEM").log
python3 $MANAGEMENT/2026-09-23/923-a789/round1/scripts/signoff.py "$G" > "$O/signoff.txt" 2>&1; echo "signoff rc=$?" >> "$O/signoff.txt"
python3 $H/scripts/util.py "$G" | sed "s#^$G#gateware#" > "$O/utilization.txt"
sed -E 's#/data-2/[^ ]*#<scratch>#g; s#$WORKSPACE_HOME/[^ ]*#<home>#g' "$G/alinx_ax7101_utilization_place.rpt" > "$O/alinx_ax7101_utilization_place.rpt"
grep -E '^head |^== BUILD|^image identity|^identity rc|"tiles"|"bytes"' "$LOG" | sed -E 's#/data-2/[^ ]*#<scratch>#g; s/\b([0-9a-f]{8})[0-9a-f]{32}\b/\1/g' > "$O/build-lines.txt"
for f in "$G"/*.bit; do echo "$(sha256sum < "$f" | cut -c1-64)  $(stat -c %s "$f") B  $(basename "$f")"; done > "$O/bitstream.sha256"
[ -f "$W/image/ctrl_app.elf" ] && echo "$(sha256sum < "$W/image/ctrl_app.elf" | cut -c1-64)  $(stat -c %s "$W/image/ctrl_app.elf") B  ctrl_app.elf" >> "$O/bitstream.sha256"
ls "$O"
