#!/usr/bin/env bash
# [A208] Run the CANDIDATE runner's offline --selftest only inside a disposable,
# network-less rootless container (never on the host, never on a Docker daemon).
# The staged tree is a scratch clone of the lane at <rev>, so the container sees
# a real checkout the way the docs CI job does.
# Usage: run-selftest-podman.sh <rev> <label> [<container-user>]
set -euo pipefail
rev=$1
label=$2
user=${3:-0:0}
lane=$LANES/532-act-parallel-slots
src=/tmp/a208-stage-$label
rm -rf "$src"
git clone -q --no-hardlinks "$lane" "$src"
git -C "$src" checkout -q --detach "$rev"
chmod -R a+rX "$src"
set +e
podman run --rm --network none --cpus 8 --memory 8g --user "$user" \
  -v "$src:/src:ro" localhost/a208-selftest:ubuntu24 \
  sh -c 'cp -a /src /tmp/work && cd /tmp/work && id -u && python3 scripts/act_ci.py --selftest'
rc=$?
set -e
echo "container-selftest rc=$rc rev=$(git -C "$src" rev-parse HEAD) tree=$(git -C "$src" rev-parse 'HEAD^{tree}') act_ci.py sha256=$(sha256sum "$src/scripts/act_ci.py" | cut -c1-64) user=$user"
rm -rf "$src"
exit "$rc"
