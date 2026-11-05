#!/bin/sh
# Reviewer helper: copy the run logs into receipts/ with host paths replaced
# by placeholders, record each run's rc and wall time, then write
# MANIFEST.sha256 over every publishable file (paths relative to the packet).
# Usage: collect_receipts.sh PACKET CLONE [PINNED_VERILATOR_DIR]
P=$1
CLONE=$2
PIN=${3:-}
S=$P/scratch
R=$P/receipts
mkdir -p "$R/runs"
san() {
  sed -e "s#$S#<scratch>#g" \
      -e "s#$CLONE#<clone>#g" \
      -e "s#$HOME/.local/share/containers/storage/overlay/[0-9a-f]*/diff#<pinned-verilator-root>#g" \
      ${PIN:+-e "s#$PIN#<pinned-verilator>#g"} \
      -e "s#$HOME#<home>#g" "$1"
}
: > "$R/runs/index.md"
printf '| Run | Command | rc | Seconds |\n|---|---|---:|---:|\n' >> "$R/runs/index.md"
for n in contract ucpu parser gaskets tsngen bench lint docs diagrams \
         engine-run arm extra probe3; do
  [ -f "$S/logs/$n.log" ] || continue
  san "$S/logs/$n.log" > "$R/runs/$n.log"
  rc=$(cat "$S/logs/$n.rc" 2>/dev/null || echo "none")
  if [ -f "$S/logs/$n.start" ] && [ -f "$S/logs/$n.end" ]; then
    secs=$(( $(cat "$S/logs/$n.end") - $(cat "$S/logs/$n.start") ))
  else secs="n/a"; fi
  printf '| %s | see REPORT.md | %s | %s |\n' "$n" "$rc" "$secs" >> "$R/runs/index.md"
done
[ -f "$S/logs/merge-tree.txt" ] && san "$S/logs/merge-tree.txt" > "$R/merge-tree.txt"
cd "$P" || exit 2
find receipts scripts -type f ! -name MANIFEST.sha256 | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256
echo "manifest entries: $(wc -l < MANIFEST.sha256)"
