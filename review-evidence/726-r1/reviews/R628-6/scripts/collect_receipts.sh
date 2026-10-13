#!/bin/sh
# collect_receipts.sh PACKET CLONE : copy runtime logs from PACKET/scratch into
# PACKET/receipts/runs with workspace paths normalized ($PACKET, $CLONE, $HOME).
# Numbers, check names, return codes and verdicts are not altered.
P=$1; C=$2
O="$P/receipts/runs"; mkdir -p "$O"
norm() { sed -e "s|$P|\$PACKET|g" -e "s|$C|\$CLONE|g" -e "s|$HOME|\$HOME|g" "$1" > "$2"; }
for d in "$P"/scratch/w_* "$P"/scratch/m_* "$P"/scratch/b_s1 "$P"/scratch/b_s8 \
         "$P"/scratch/r5_* "$P"/scratch/my_* "$P"/scratch/f5_* "$P"/scratch/tk_*; do
  [ -d "$d" ] || continue
  n=$(basename "$d")
  for f in run.log escape.log omit.log; do
    [ -f "$d/$f" ] && norm "$d/$f" "$O/$n.$f"
  done
  for f in "$d"/shift_*.log; do
    [ -f "$f" ] && norm "$f" "$O/$n.$(basename "$f")"
  done
done
for f in "$P"/receipts/*.log; do
  norm "$f" "$f.tmp" && mv "$f.tmp" "$f"
done
for f in "$P"/receipts/gates/*.log; do
  norm "$f" "$f.tmp" && mv "$f.tmp" "$f"
done
