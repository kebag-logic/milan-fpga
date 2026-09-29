#!/bin/sh
# R405-5: seeded faults on disposable copies of the live PR body; each must
# make the named checker fail. Usage: r405_5_probes.sh <packet-dir> <606 page>
P=$1; PAGE=$2; S=$P/scratch/probes; mkdir -p $S
B=$P/receipts/pr622_body.md; C=$P/receipts/census_r405_5.txt
run() { python3 $P/scripts/r405_5_body_census.py "$1" $C $PAGE >/dev/null 2>&1; echo $?; }
echo "control body_census rc=$(run $B) (expect 0)"
sed 's/210 state-changing ACMP commands/210 ACMP commands/' $B > $S/m1.md; echo "M1 drop 'state-changing' rc=$(run $S/m1.md) (expect 1)"
sed 's/(105 `CONNECT_RX`, 105 `DISCONNECT_RX`)/(106 `CONNECT_RX`, 104 `DISCONNECT_RX`)/' $B > $S/m2.md; echo "M2 split 106/104 rc=$(run $S/m2.md) (expect 1)"
sed 's/^Relates to #606$/Closes #606/' $B > $S/m3.md; echo "M3 Relates->Closes #606 rc=$(run $S/m3.md) (expect 1)"
sed 's/228 GET_COUNTERS and 4 READ_DESCRIPTOR/228 GET_COUNTERS and 5 READ_DESCRIPTOR/' $B > $S/m4.md; echo "M4 READ_DESCRIPTOR 5 rc=$(run $S/m4.md) (expect 1)"
awk 'BEGIN{d=0} /^\| #606 item 3: first bind/ && !d {sub(/PASS, 5 of 5/,"PASS, 4 of 5"); d=1} {print}' $B > $S/m5.md
python3 $P/scripts/r405_tables.py $B $S/m5.md | tail -1 | sed 's/^/M5 table cell changed, tables: /'
python3 $P/scripts/r405_tables.py $B $B | tail -1 | sed 's/^/control tables: /'
