#!/usr/bin/env bash
# usage: job.sh <name> <workdir> <command...>  -> receipts/<name>.log, receipts/<name>.rc
P=$REVIEWS/pp230-r458-3-packet
name=$1; wd=$2; shift 2
export PATH=$P/scratch/bin:$PATH
rm -f $P/receipts/$name.rc
cd "$wd" || { echo 127 > $P/receipts/$name.rc; exit; }
{ echo "# job $name in ${wd#$P/} : $*"; echo "# start $(date -u +%FT%TZ)"; } > $P/receipts/$name.log
"$@" >> $P/receipts/$name.log 2>&1; rc=$?
echo "# end $(date -u +%FT%TZ) rc=$rc" >> $P/receipts/$name.log
echo $rc > $P/receipts/$name.rc
