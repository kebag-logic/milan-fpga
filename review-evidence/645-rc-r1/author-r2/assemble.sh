#!/usr/bin/env bash
# scratch: copy small evidence into the packet; large files get size and SHA-256 only
set -u
P=$MANAGEMENT/2026-09-23/645-a620
S=/tmp/a620
mkdir -p $P/b17 $P/campaign/fix $P/campaign/base $P/suites $P/gates $P/area $P/controls/sc_plants $P/wallclock $P/tally
cp $S/b17_derive.py $S/b17_burst.py $P/b17/
python3 -I $S/b17_derive.py $S/b17 > $P/b17/derive.txt
python3 -I $S/b17_burst.py $S/b17 > $P/b17/burst.txt
for v in fix base; do
  cp $S/sweep_$v/*.log $S/sweep_$v/*.rc $S/sweep_$v/*.command.json $S/sweep_$v/bind.md $P/campaign/$v/
  cp $S/summ_$v.md $P/campaign/summary-$v.md
done
cp $S/summ_bind.py $S/inside_check.py $P/campaign/
{ echo "== base"; python3 -I $S/inside_check.py $S/sweep_base; echo "== fix"; python3 -I $S/inside_check.py $S/sweep_fix; } > $P/campaign/inside_check.txt
: > $P/suites/LARGE.sha256
for f in $S/suites/*; do
  b=$(basename $f)
  sz=$(stat -c %s $f)
  if [ "$sz" -gt 200000 ]; then
    echo "$(sha256sum $f | cut -d' ' -f1)  $sz  $b" >> $P/suites/LARGE.sha256
    { echo "# excerpt of $b ($sz bytes, SHA-256 in LARGE.sha256): its tally, verdict and FAIL lines"; grep -n -E 'checks|RESULT|\[FAIL\]|caught|SURVIV|RECENTRE|sim_pool|Error|rc=' $f | tail -200; tail -5 $f; } > $P/suites/$b.excerpt.txt
  else
    cp $f $P/suites/
  fi
done
cp $S/tally/tally.txt $S/tally/*.verdict $P/tally/ 2>/dev/null
for f in $S/gates/*; do
  sz=$(stat -c %s $f)
  if [ "$sz" -gt 200000 ]; then echo "$(sha256sum $f | cut -d' ' -f1)  $sz  $(basename $f)" >> $P/gates/LARGE.sha256; else cp $f $P/gates/; fi
done
cp $S/area2/*.sv $S/area2/ooc.tcl $S/area2/mk_ooc.py $S/area2/*.stat.txt $P/area/
for d in $S/area2/viv_*; do n=$(basename $d); n=${n#viv_}; cp $d/$n.vivado.util.txt $d/$n.vivado.timing.txt $P/area/; done
cp $S/sc_plants/plant_sc.py $S/sc_plants/plants.log $P/controls/sc_plants/
for d in $S/sc_plants/out/*; do n=$(basename $d); cp $d/6250000/run.log $P/controls/sc_plants/$n.run.log 2>/dev/null; done
cp $S/wallclock.sh $S/wallclock/result.txt $P/wallclock/
for f in $S/wallclock/five.log $S/wallclock/four.log; do sz=$(stat -c %s $f); if [ "$sz" -gt 200000 ]; then echo "$(sha256sum $f | cut -d' ' -f1)  $sz  $(basename $f)" >> $P/wallclock/LARGE.sha256; else cp $f $P/wallclock/; fi; done
cp $S/run_chain.sh $S/assemble.sh $P/
find $P -type f -size +200k -printf 'OVER 200 KB: %p %s\n'
