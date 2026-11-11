#!/bin/bash
# probes_final.sh: R821-1's fw_probes.py (every probe) and R822-1's run_probe_window.sh, unchanged, against the probe
# clone at the final head; then B20's channel receipt under its planted defect (b20mut.sh)
S=<scratch>; W=$S/probes/wt
cd $S/probes
python3 -B $S/scripts/reviewer/fw_probes.py $W $S/probes/r821 > $S/probes/r821.log 2>&1; echo $? > $S/probes/r821.rc
sh $S/scripts/reviewer/run_probe_window.sh $W $S/probes/r822-build <management>/2026-09-23/665s11-r822-1 > $S/probes/r822.log 2>&1; echo $? > $S/probes/r822.rc
rm -rf $S/probes/b20mut; $S/scripts/b20mut.sh > $S/probes/b20mut.out 2>&1
echo "head $(git -C $W rev-parse HEAD), clone changes after: $(git -C $W status --porcelain | wc -l)" > $S/probes/final.txt
