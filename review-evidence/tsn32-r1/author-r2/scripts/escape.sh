#!/bin/bash
# Each round 2 plant in src/acmp.c, against round 1's suite (9043b926) and this head's, with R824-1's suite_on_plant.sh.
set -u
S=<scratch> E=<scratch>/escape
export TOOLS=<tools>
export PATH=<tools>/clang-18/bin:$PATH
H=$(git -C $S/trees/head rev-parse HEAD)
python3 - <<'PY'
import json
S='<scratch>'
src=open(S+'/trees/head/src/acmp.c').read()
new=['walk-bind-second-word-unmarked','walk-unbind-second-word-unmarked','walk-release-second-word-unmarked','walk-probe-left-second-word-unmarked','walk-marks-never-cleared','walk-interface-marks-never-cleared','walk-clear-first-word-only']
for m in json.load(open(S+'/trees/head/tests/mutations.json')):
    if m['name'] in new:
        assert src.count(m['old'])==1
        open(S+'/escape/plants/'+m['name']+'.c','w').write(src.replace(m['old'],m['new']))
PY
for p in $E/plants/*.c; do
  n=$(basename $p .c)
  for rev in 9043b926532dc4ffb57218ee0eebca7564262289 $H; do
    echo "== $n at ${rev:0:8}"
    bash $S/r824/scripts/suite_on_plant.sh $S/trees/head $rev $p $E/run-$n-${rev:0:8}
    rm -rf $E/run-$n-${rev:0:8}/src
  done
done
