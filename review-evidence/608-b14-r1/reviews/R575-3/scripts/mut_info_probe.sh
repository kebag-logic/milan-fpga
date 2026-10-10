#!/bin/sh
# Mutation probe: grade a per-frame FRAMES_RX advance as FAIL instead of INFO
# and confirm counters_contract_milan.feature detects it. $1 = scratch tree
# extracted with `git archive HEAD tests tb/tools`.
set -u
T="$1"
python3 -I - "$T/tb/tools/torture_campaign.py" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old='        return ("INFO", dict(base, reading="per-frame",'
assert s.count(old)==1, s.count(old)
open(p,"w").write(s.replace(old,'        return ("FAIL", dict(base, reading="per-frame",'))
PY
cd "$T/tests" && behave -f progress features/counters_contract_milan.feature
