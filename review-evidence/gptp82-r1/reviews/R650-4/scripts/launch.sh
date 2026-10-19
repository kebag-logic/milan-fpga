#!/bin/sh
# usage: launch.sh <packet>  - engine suite at head and base, then the head
# mutation arm in 18 shards, 4 at a time; each job leaves a .log and a .rc.
P=$1; S=$P/scratch; R=$P/receipts/runs
export PATH=$S/bin:$PATH
for t in head base; do
  ( cd $S/$t/tb/verilator/engine && make run >$R/engine-$t.log 2>&1; echo $? >$R/engine-$t.rc ) &
done
seq 0 17 | xargs -P 4 -I{} sh -c "python3 -I $P/scripts/shard.py $S/head/tb/verilator/engine {} 18 >$R/head-mutants-s{}.log 2>&1; echo \$? >$R/head-mutants-s{}.rc"
wait
echo done >$R/ALL.done
