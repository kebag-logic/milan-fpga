#!/bin/bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer replay (R433-4) of the docs.yml docs-check steps the round-4/4b delta touches,
# each step's `run:` text executed verbatim from the workflow file at the head, plus
# the em-dash gate at the PR's merge base, then the merge's ratchet generators
# re-run with --write-budget and compared to the tracked bytes.
# Usage: docs_replay.sh <disposable checkout of the head> <em-dash base sha>
# Expects GNU make 4.3 and the pinned Markdown python first on PATH.
set -u
T=$(cd "$1" && pwd); BASE=$2
cd "$T" || exit 2
echo "make: $(make --version | head -1); python: $(command -v python3)"
fails=0
for i in 7 9 12 14 15 19 30 31 32 35 36 37 39 43 45 47 49; do
  name=$(python3 -c "import yaml,sys;print(yaml.safe_load(open('.github/workflows/docs.yml'))['jobs']['docs-check']['steps'][$i]['name'])")
  python3 -c "import yaml,sys;sys.stdout.write(yaml.safe_load(open('.github/workflows/docs.yml'))['jobs']['docs-check']['steps'][$i]['run'])" > /tmp/r433-4-step.$$
  bash -eo pipefail /tmp/r433-4-step.$$ > /tmp/r433-4-out.$$ 2>&1; rc=$?
  echo "step $i [$name] rc=$rc :: $(tail -n 1 /tmp/r433-4-out.$$ | cut -c1-160)"
  [ $rc -eq 0 ] || { fails=$((fails+1)); tail -n 20 /tmp/r433-4-out.$$; }
done
python3 scripts/check_em_dash.py --base "$BASE" > /tmp/r433-4-out.$$ 2>&1; rc=$?
echo "step 8 [em-dash, base $BASE] rc=$rc :: $(tail -n 1 /tmp/r433-4-out.$$)"; [ $rc -eq 0 ] || fails=$((fails+1))
echo "== generators re-recording the merge's ratchets"
python3 scripts/measure_naming.py --write-budget > /dev/null 2>&1; echo "measure_naming --write-budget rc=$?"
python3 scripts/check_port_contracts.py --write-budget > /dev/null 2>&1; echo "check_port_contracts --write-budget rc=$?"
python3 docs/diagrams/submodule_boundaries.gen.py > /dev/null 2>&1; echo "submodule_boundaries.gen.py (write) rc=$?"
echo "tracked files changed by the generators (empty = byte-identical):"
git status --short --untracked-files=no
git diff --stat
rm -f /tmp/r433-4-step.$$ /tmp/r433-4-out.$$
echo "failing steps: $fails"
exit $fails
