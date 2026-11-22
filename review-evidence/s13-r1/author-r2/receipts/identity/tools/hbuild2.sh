#!/bin/bash
# hbuild2.sh CLONE OUT: hbuild.sh at 1x1 then at 8x8-1if (one point at a time: the arms of one point share the clone's
# builder output), then each arm whose image is missing rebuilt alone.
set -u
S=<scratch>; C=$1; O=$2
for P in 1x1 8x8-1if; do bash $S/bin/hbuild.sh $C $O $P; done
for P in 1x1 8x8-1if; do
  while read -r p v h rest; do
    if [ ${#h} -ne 64 ]; then echo "== $p $v has no image; rebuilt alone"; rm -rf $O/$p/$v
      . $S/bin/fwenv.sh; declare -A N=([none]=22 [answering-every-port]=6 [answering-ports]=22 [answering-later]=3 [declaring-outputs]=4 [shutdown-entry]=2 [talker-notices]=2 [valid-destinations]=3)
      MAKEFLAGS="-j8 --no-print-directory" python3 -B $S/tools/legs.py build $C $O/$p/$v $p $v ${N[$v]} > $O/$p/$v.build.log 2>&1
      echo "   $p $v $(sha256sum $O/$p/$v/image/ctrl_app.elf | cut -c1-64)"; fi
  done < $O/$P/hashes.txt
done
echo "END $(date -Iseconds)"
