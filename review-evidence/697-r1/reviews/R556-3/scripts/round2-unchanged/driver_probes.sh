#!/bin/bash
# SPDX-License-Identifier: MIT
# Reviewer-owned controls for the mutation driver in a disposable copy.
# usage: driver_probes.sh <git-repo> <rev> <scratch-dir>
set -u
REPO=$1; REV=$2; D=$3/driver-probes
rm -rf "$D"; mkdir -p "$D/tree"
git -C "$REPO" archive "$REV" | tar -x -C "$D/tree"
cd "$D/tree"
python3 -I - <<'EOF'
import json
t = json.load(open('tests/mutations.json'))
g = next(m for m in t if m['name'] == 'departing-keeps-index')
expiry = '\tif (reject_reentry()) {\n\t\treturn;\n\t}\n'
src = open('src/adp.c').read()
i = src.index('void adp_timer_expired(struct adp *a)\n{\n')
anchor = 'void adp_timer_expired(struct adp *a)\n{\n'
plants = [
    dict(g, name='p-genuine'),
    dict(g, name='p-unrelated-needle', kills=[{'test': 'AdpCore.A6toA8DeferredSends',
         'needle': 'A6 a refused send keeps ENTITY_AVAILABLE owed in DELAY'}]),
    {'name': 'p-crash', 'path': 'src/adp.c', 'old': anchor,
     'new': anchor + '\t*(volatile int *)0 = 0;\n', 'kills': g['kills'][:1]},
    {'name': 'p-exit0', 'path': 'src/adp.c', 'old': anchor,
     'new': anchor + '\t{ extern void exit(int); exit(0); }\n', 'kills': g['kills'][:1]},
]
json.dump(plants, open('tests/mutations.json', 'w'), indent=1)
EOF
grep -c 'A6 a refused send keeps ENTITY_AVAILABLE owed in DELAY' tests/test_adp.cpp > "$D/unrelated-needle-present.txt"
# stale evidence: a complete-looking passing-kill XML placed where p-exit0 will run
mkdir -p "$D/work/p-exit0"
printf '<testsuites tests="1" failures="1" errors="0" disabled="0"><testsuite><testcase classname="AdpCore" name="A6toA8DeferredSends" status="run" result="completed"><failure message="A8 SHUTDOWN with no room keeps ENTITY_DEPARTING owed, index reset"/></testcase></testsuite></testsuites>' > "$D/work/p-exit0/adp.xml"
GTEST_FILTER='-*' GTEST_ALSO_RUN_DISABLED_TESTS=1 python3 scripts/mutation.py --work "$D/work" --jobs 5 > "$D/campaign.log" 2>&1
echo "campaign rc $?"
python3 -I -c '
import json,sys
for r in json.load(open(sys.argv[1])): print(r["name"], r["status"], "rc", r.get("rc"), "tests", r.get("tests"), r.get("error",""))' "$D/work/results.json"
ls "$D/work/p-exit0"
