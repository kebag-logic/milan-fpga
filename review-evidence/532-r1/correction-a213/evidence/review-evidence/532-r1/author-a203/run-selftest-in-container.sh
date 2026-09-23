#!/usr/bin/env bash
# [A203] Run the CANDIDATE runner's offline --selftest only inside a disposable,
# network-less container on the scratch daemon (never as a host orchestrator).
# The staged tree is a scratch clone of the lane HEAD plus the exact working
# tree diff and untracked files, committed, so the container sees a real
# checkout the way the docs CI job does.
set -euo pipefail
label=$1
lane=$LANES/532-act-parallel-slots
scratch=$REVIEWS/532-a203-packet/scratch
docker_cli=(sudo -n docker -H unix:///run/a203-exp/docker.sock)
src=$scratch/selftest-src-$label
rm -rf "$src"
git clone -q --no-hardlinks "$lane" "$src"
git -C "$lane" diff HEAD --binary | git -C "$src" apply --index --allow-empty
git -C "$lane" ls-files --others --exclude-standard -z |
  while IFS= read -r -d '' path; do
    mkdir -p "$src/$(dirname "$path")"
    cp -p "$lane/$path" "$src/$path"
    git -C "$src" add -- "$path"
  done
git -C "$src" -c user.name=a203 -c user.email=a203@invalid commit -q --allow-empty -m candidate
name=a203-selftest-$label
"${docker_cli[@]}" rm -f "$name" >/dev/null 2>&1 || true
"${docker_cli[@]}" run -d --name "$name" --network none --cpuset-cpus=32-39 \
  --memory=8g --memory-swap=8g --label org.kebag-logic.milan-act-ci.owner=a203-selftest \
  a203-selftest:ubuntu24 tail -f /dev/null >/dev/null
"${docker_cli[@]}" cp "$src" "$name:/work"
set +e
"${docker_cli[@]}" exec -w /work "$name" python3 scripts/act_ci.py --selftest
rc=$?
set -e
"${docker_cli[@]}" rm -f "$name" >/dev/null
echo "container-selftest rc=$rc tree=$(git -C "$src" rev-parse HEAD^{tree})"
exit "$rc"
