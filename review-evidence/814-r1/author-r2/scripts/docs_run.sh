#!/usr/bin/env bash
# #814 (the #780 lane's driver, paths only): the docs workflow's gate steps at <rev>, as that lane ran them
# (scripts/round7/docs_steps.py: the run: bodies literally, GNU Make 4.3,
# CPython 3.12.3 with the workflow's pinned requirements), in a clean clone
# whose tsn-c-stack origin is set to its .gitmodules URL first (the builder
# legs' scripts/ci_case_receipts.py requires it; the clone takes its
# submodules from the lane's checkouts). Then builder leg 1 again with the
# LiteX interpreter, the five markdown gates on CPython 3.12.3
# (docs_steps_md312.py), and the no-git step's two gates on a git-archive
# export (its body deletes .git). The lane's local dev is the live dev tip.
# usage: docs_run.sh <rev>
set -u
rev=$1; h=${rev:0:8}
R7=$(cd "$(dirname "$0")" && pwd)
B=$VALIDATION_STORAGE/scratch/814-a703b/docs
C=$B/clone-docs-$h
O=$B/docs-$h
mkdir -p "$O"
[ -d "$C" ] || bash "$R7/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
# the em-dash gate fetches the pull request's base branch from origin: the clone's own dev, which
# make_clone.sh set to the live remote dev tip
git -C "$C" remote set-url origin "$C"
T=$C/third_party/tsn-c-stack
[ "$(git -C "$T" rev-parse --show-toplevel)" = "$T" ] || { echo "tsn-c-stack toplevel mismatch"; exit 2; }
url=$(git -C "$C" config -f .gitmodules submodule.third_party/tsn-c-stack.url)
git -C "$T" remote set-url origin "$url"
git -C "$T" remote get-url origin > "$O/tsn-c-stack-origin.txt"
git -C "$C" rev-parse dev > "$O/dev-ref.txt" 2>&1
PY=$VALIDATION_STORAGE/scratch/a662/ci312/bin/python3
date -Is > "$O/start"
$PY "$R7/docs_steps.py" "$O/all" "$C" > "$O/all.out" 2>&1; echo $? > "$O/all.rc"
DOCS_ONLY=gate_25_1 DOCS_EXTRA_ENV="MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3" \
  $PY "$R7/docs_steps.py" "$O/leg1-litex" "$C" > "$O/leg1-litex.out" 2>&1; echo $? > "$O/leg1-litex.rc"
$PY "$R7/docs_steps_md312.py" "$O/md312" "$C" > "$O/md312.out" 2>&1; echo $? > "$O/md312.rc"
N=$B/nogit-$h
rm -rf "$N"; mkdir -p "$N/tree"
git -C "$C" archive --format=tar HEAD | tar -x -C "$N/tree"
# as the job's checkout: no submodules
( cd "$N/tree" && PATH=$VALIDATION_STORAGE/scratch/a662/ci312/bin:$VALIDATION_STORAGE/scratch/a662/make43/bin:$PATH && \
  python3 scripts/docs_check.py > "$O/nogit_docs_check.log" 2>&1; echo "docs_check rc=$?" > "$O/nogit_summary.txt"; \
  python3 scripts/check_feature_status.py > "$O/nogit_feature_status.log" 2>&1; echo "feature_status rc=$?" >> "$O/nogit_summary.txt" )
date -Is > "$O/end"
