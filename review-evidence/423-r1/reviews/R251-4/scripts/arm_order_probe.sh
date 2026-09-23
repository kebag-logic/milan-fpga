#!/bin/sh
# Arm-order control candidate: a redundant-merge branch with no net tree change
# whose commits are all replayed (replays get a distinct committer date).  Usage: arm_order_probe.sh <checker> <workdir>
checker=${1:?checker}; w=${2:?workdir}
rm -rf "$w"; mkdir -p "$w"; cd "$w" || exit 9
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=P GIT_AUTHOR_EMAIL=p@example.invalid GIT_COMMITTER_NAME=P GIT_COMMITTER_EMAIL=p@example.invalid
g() { git -c commit.gpgsign=false "$@"; }
g init -q -b main; printf 'keep\n' > keep; g add -A; g commit -qm O; O=$(git rev-parse HEAD)
g checkout -qb incoming; printf 'x\n' > x; g add -A; g commit -qm 'A adds x'; A=$(git rev-parse HEAD)
g checkout -qb pr "$O"; g merge -q --no-ff -m 'M redundant' incoming; g rm -q x; g commit -qm 'C removes x'; C=$(git rev-parse HEAD)
g checkout -q main; export GIT_COMMITTER_DATE="@1790000000 +0000"; g cherry-pick "$A" >/dev/null; g cherry-pick "$C" >/dev/null
printf 'later\n' > later; g add -A; g commit -qm 'unrelated later work'
PYTHONDONTWRITEBYTECODE=1 python3 "$checker" --no-fetch --base main pr; echo "rc=$?"
