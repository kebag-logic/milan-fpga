#!/bin/bash
# rtl.sh: rtl.yml's gate and physical jobs by the step runner, and its four portability shards by their own command
: "${CPUS:?CPUS unset}"
G=<scratch>/gates; H=$(cat $G/HEAD); R=$G/rtl; mkdir -p $R/logs
$G/wf_jobs.sh rtl $R full-ci-gate
W=$R/yosys-wt
[ -d $W ] || bash <scratch>/clone_at.sh $H $W > $R/logs/yosys-clone.log 2>&1
cd $W || exit 3
export PATH=<data>/tools/md-venv-40cdefe08ebd/bin:<data>/tools/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=$R/tmp YOSYS_VERSION=v0.66
mkdir -p $TMPDIR
for k in 0 1 2 3; do
  { echo "# head $H rtl.yml yosys-shards shard $k/4: syn/yosys/run.sh --shard $k/4"; taskset -c "$CPUS" syn/yosys/run.sh --shard $k/4 --results $R/yosys-results-$k --cache $R/yosys-cache-$k; } > $R/logs/rtl-yosys-shard-$k.log 2>&1
  echo "yosys-shard-$k $?" >> $R/jobs.txt
done
git status --short > $R/logs/yosys-tree-after.txt
echo done >> $R/jobs.txt
