#!/bin/bash
# The harness at the final head, every leg: each build regraded from its own clone moved to the head.
H=$1 T=/data-2/milan/tmp/665s2b-a683zo
bash $T/scripts/head30.sh $H GA8 GA8 8x8 &
bash $T/scripts/head30.sh $H GA1 GA1 1x1 &
bash $T/scripts/head30.sh $H GN8 GN8 8x8 --variant answering-every-port &
bash $T/scripts/head30.sh $H GN1 GN1 1x1 --variant answering-every-port &
wait
bash $T/scripts/head30.sh $H GB8 GB 8x8 --groups aecp --variant answering-ports
bash $T/scripts/head30.sh $H GB1 GB 1x1 --groups aecp --variant answering-ports
