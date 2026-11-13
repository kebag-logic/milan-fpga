#!/bin/bash
S=/data-2/milan/tmp/665s2b-a683zo
bash $S/scripts/leg30.sh $S/L30-GB GB8 8x8 1 --groups aecp --variant answering-ports
bash $S/scripts/leg30.sh $S/L30-GB GB1 1x1 1 --groups aecp --variant answering-ports
