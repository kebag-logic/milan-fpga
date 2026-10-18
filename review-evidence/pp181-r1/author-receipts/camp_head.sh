#!/usr/bin/env bash
# head campaigns at the final head: streams a and b together, then the two that refuse an existing output
S=<data>/tmp/pp181-a635; T=<data>/lanes/pp181-cut
$S/campaigns.sh $T head a & $S/campaigns.sh $T head b & wait
$S/campaigns2.sh $T head
echo CAMP-HEAD-DONE > $S/camp/head/done.txt
