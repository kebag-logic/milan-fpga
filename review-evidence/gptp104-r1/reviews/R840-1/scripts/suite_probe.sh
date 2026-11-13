#!/bin/sh
# The in-tree engine suite (make run) at the head in two exported trees at
# different paths, sharing one ccache directory under scratch: cold, then
# warm through CCACHE_BASEDIR; lists the files each run adds; then make -n
# views of `all` and of OBJCACHE= and an unwritable cache.
. $REVIEWS/gptp104-r840-1-packet/scripts/env.sh
out=$P/receipts/suite; mkdir -p $out
export CCACHE_DIR=$S/cc/suite; rm -rf $CCACHE_DIR; mkdir -p $CCACHE_DIR
for c in suite1 suite2-other-path; do
  (cd $S/$c && find . -type f | sort) > $out/$c.files-before.txt
  ccache -z > /dev/null
  make -C $S/$c/tb/verilator/engine run > $out/$c.make-run.log 2>&1; echo "rc=$?" > $out/$c.make-run.rc
  ccache --print-stats > $out/$c.ccache-stats
  (cd $S/$c && find . -type f | sort) > $out/$c.files-after.txt
  comm -13 $out/$c.files-before.txt $out/$c.files-after.txt | sed 's|^\./||' | cut -d/ -f1-4 | sort -u > $out/$c.added-dirs.txt
done
make -C $S/suite1/tb/verilator/engine -n all > $out/suite1.make-n-all.log 2>&1
make -C $S/suite1/tb/verilator/engine clean > /dev/null 2>&1
mkdir -p $S/cc/ro2; chmod 555 $S/cc/ro2
CCACHE_DIR=$S/cc/ro2 make -C $S/suite1/tb/verilator/engine run > $out/suite1.unwritable-cache.log 2>&1; echo "rc=$?" > $out/suite1.unwritable-cache.rc
chmod 755 $S/cc/ro2
echo done > $out/DONE
