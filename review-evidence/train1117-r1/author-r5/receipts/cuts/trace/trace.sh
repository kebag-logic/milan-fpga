#!/bin/bash
# trace.sh LABEL: the largest legal record of an attribution build (attr/b/LABEL/none, part0) traced by committed PC
# as the third window is (300,000 bus cycles before the first RXC after the aecp_long mark, 900,000 PCs), then split
# by function (perfunc.py). Scratch only.
set -u
T=<scratch>; . $T/bin/env.sh
L=$1 B=$T/attr/b/$1/none g=aecp-largest-notice
mark=$(grep -m1 '^MARK [0-9]* aecp_long\.' $B/part0/$g.log | awk '{print $2}')
first=$(awk -v m=${mark:-0} '$1=="RXC" && $2>=m {print $2; exit}' $B/part0/$g.log)
echo "$L: mark $mark first RXC $first $(date +%T)"
(cd $B/gateware && BUDGET_TRACE_AFTER=$((first - 300000)) BUDGET_TRACE_PCS=900000 $B/native/Vsim $B/part0/$g.txt - | grep '^PC ' > $T/cut/$L.pcs)
echo "$(wc -l < $T/cut/$L.pcs) PCs $(date +%T)"
python3 -I $T/cut/perfunc.py $B/image/ctrl_app.map $B/part0/$g.log $T/cut/$L.pcs 2 > $T/cut/$L.perfunc.txt
head -25 $T/cut/$L.perfunc.txt
