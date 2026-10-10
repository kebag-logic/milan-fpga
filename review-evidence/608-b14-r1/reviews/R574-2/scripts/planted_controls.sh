#!/usr/bin/env bash
# Show the recompute scripts detect altered records: copy the needed records,
# plant one change each, and compare outputs with the clean run.
# Usage: planted_controls.sh <archive-author-dir> <scratch-dir>
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
a=$1 s=$2
rm -rf "$s" && mkdir -p "$s"
cp -r "$a/item2" "$a/item3" "$a/soak" "$a/restore" "$s/"
clean_ledger=$(python3 -I "$here/slip_lb_ledger.py" "$s" | grep "soak steps")
clean_item3=$(python3 -I "$here/item3_hold.py" "$s" | grep cycle-002)
# plant 1: SLIP_LB at the 10-minute soak read 0x92 -> 0x94
sed -i 's/^\(0x900008d4  \)92 00/\194 00/' "$s/soak/console-soak-010.txt"
p1=$(python3 -I "$here/slip_lb_ledger.py" "$s" | grep "soak steps")
# plant 2: move cycle 2's DUT Talker Advertise Lv by +10 ms
sed -i 's/^2\.840873289\tDUT\tTalkerAdvertise\tLv/2.850873289\tDUT\tTalkerAdvertise\tLv/' "$s/item3/cycles/cycle-002/msrp.tsv"
p2=$(python3 -I "$here/item3_hold.py" "$s" | grep cycle-002)
echo "clean ledger:   $clean_ledger"
echo "planted ledger: $p1"
[ "$clean_ledger" != "$p1" ] && echo "plant 1 DETECTED" || echo "plant 1 MISSED"
echo "clean item3:   $clean_item3"
echo "planted item3: $p2"
[ "$clean_item3" != "$p2" ] && echo "plant 2 DETECTED" || echo "plant 2 MISSED"
