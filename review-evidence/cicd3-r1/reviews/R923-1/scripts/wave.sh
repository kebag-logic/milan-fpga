#!/bin/sh
# Start one wave of base/head mutation-driver arms, each cold then warm on its
# own compiler cache, in the background; each arm writes its own logs and rc.
#   wave.sh PACKET WAVE suite/driver.py...
set -u
P=$1 wave=$2; shift 2
S=$P/scratch
out=$P/receipts/mutants/$wave
mkdir -p "$out"
for spec in "$@"; do
  suite=${spec%/*} driver=${spec#*/}
  for arm in base head; do
    key="$arm-$suite-$(basename "$driver" .py)"
    nohup setsid sh -c "
      sh '$P/scripts/run_driver.sh' '$S/g$arm' '$suite' '$driver' '$out' '$S/tmp-g$arm' '$S/cc/$wave-$key' $arm-cold
      sh '$P/scripts/run_driver.sh' '$S/g$arm' '$suite' '$driver' '$out' '$S/tmp-g$arm' '$S/cc/$wave-$key' $arm-warm
      echo done > '$out/$key.done'" > "$S/$wave-$key.nohup" 2>&1 < /dev/null &
  done
done
echo "wave $wave started: $# drivers"
