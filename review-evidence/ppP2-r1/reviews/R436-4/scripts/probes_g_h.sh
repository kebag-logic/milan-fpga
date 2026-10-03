#!/usr/bin/env bash
# probes_g_h.sh JOBS : R436g (babble_probe.sh) on head, Z1, Z2, Z3, Z8 at 3/37/100 and
# R436h (resume_long_probe.sh) on head, Z10b at 3/37, JOBS at a time.
P=$(cd "$(dirname "$0")/.." && pwd)
{ for v in head Z1 Z2 Z3 Z8; do for t in 3 37 100; do echo "babble_probe.sh $v $t babble_${v}_$t"; done; done
  for v in head Z10b; do for t in 3 37; do echo "resume_long_probe.sh $v $t resumelong_${v}_$t"; done; done; } |
xargs -P "$1" -L1 bash -c "'$P/scripts/'\$0 \$1 \$2 > '$P/receipts/'\$3.log 2>&1; echo \$? > '$P/receipts/'\$3.rc"
