#!/bin/bash
# probes_r3.sh: R821-2's probe_plat.py (all) and probe_aecp.py (head, handover), and R822-2's r822_probes.py
# (clean and the two probes its Verification line names), unchanged, against the probe clone at the head
S=<scratch>; W=$S/probes/wt; O=$S/probes3/final; rm -rf $O; mkdir -p $O; cd $O
python3 -I $S/scripts/reviewer2/probe_plat.py $W $O/plat all > $O/r821-plat.log 2>&1; echo $? > $O/r821-plat.rc
for m in head handover; do python3 -I $S/scripts/reviewer2/probe_aecp.py $W $O/aecp-$m $m > $O/r821-aecp-$m.log 2>&1; echo $? > $O/r821-aecp-$m.rc; done
python3 -B $S/scripts/reviewer2/r822_probes.py $W $O/r822 clean gate-skips-maap-and-srp depart-ignores-maap-and-srp-rings > $O/r822.log 2>&1; echo $? > $O/r822.rc
echo "head $(git -C $W rev-parse HEAD), clone changes after: $(git -C $W status --porcelain | wc -l)" > $O/final.txt
