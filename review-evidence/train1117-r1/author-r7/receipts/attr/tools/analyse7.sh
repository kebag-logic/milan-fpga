#!/bin/bash
# analyse7.sh IMG...: the attribution experiment's reading, as the full re-measure read its legs (analyse6.sh's
# survey_point4.py, #665 round 28's tools): each repeat of each image's srp-talker-held leg and of its notice leg
# (aecp-fanout, the ordinary view's AECP notice item; aecp-largest-notice, the long view) surveyed alone, into out/.
set -u
T=<scratch>; . $T/bin/env.sh
declare -A CL=([A]=r7-A [B]=r7-B [C]=r7-C [D]=r7-D)
for I in "$@"; do
  C=$T/clones/${CL[$I]}
  for k in 1 2 3; do
    for leg in $I notice-$I; do
      L=$T/r7attr/$leg/rep$k; O=$T/r7attr/out/$leg-rep$k; rm -rf $O; mkdir -p $O
      SURVEY_POINT=8x8/1if SURVEY_NIF=1 python3 -I $T/r4meas/survey_point4.py $C $T/tools/survey $O/survey $L \
        > $O/survey.out 2>&1
      echo "$leg rep$k survey rc=$?"
    done
  done
done
