#!/bin/bash
# The harness at both points at the final head: every leg regraded from its own clone moved to the head.
H=$1 T=<scratch>
bash $T/scripts/head28.sh $H GA8 8x8
bash $T/scripts/head28.sh $H GA1 1x1
bash $T/scripts/head28.sh $H GN8 8x8 --variant answering-every-port
bash $T/scripts/head28.sh $H GN1 1x1 --variant answering-every-port
bash $T/scripts/head28.sh $H GB8 8x8 --variant answering-ports --groups aecp
bash $T/scripts/head28.sh $H GB1 1x1 --variant answering-ports --groups aecp
