#!/usr/bin/env bash
# [A213] Run a staged tree's offline act_ci.py --selftest ONLY inside a
# disposable, network-less, unprivileged bubblewrap sandbox: new user, net,
# pid, ipc, uts and cgroup namespaces (only `lo`), read-only /usr and /etc,
# empty /home, /run, /tmp and /var, so no Docker socket, host home, credential
# or network is visible. Never used for a host-side runner invocation
# (runner-change bootstrap rule).
# Usage: run-selftest-sandbox.sh STAGE_TREE LABEL [root]
set -euo pipefail
stage=$(cd "$1" && pwd)
label=$2
uid_args=()
if [ "${3:-}" = root ]; then uid_args=(--uid 0 --gid 0); fi
set +e
bwrap --unshare-all --die-with-parent --new-session "${uid_args[@]}" \
  --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 \
  --symlink usr/bin /bin --symlink usr/bin /sbin --ro-bind /etc /etc \
  --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run --tmpfs /home \
  --tmpfs /var --bind "$stage" /work --chdir /work \
  --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /tmp \
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 \
  sh -c 'echo "sandbox uid=$(id -u) links=$(tail -n +3 /proc/net/dev | cut -d: -f1 | tr -d " " | tr "\n" " ")"; exec python3 scripts/act_ci.py --selftest'
rc=$?
set -e
echo "sandbox-selftest label=$label rc=$rc rev=$(git -C "$stage" rev-parse HEAD) dirty=$(git -C "$stage" status --porcelain | wc -l) act_ci.py sha256=$(sha256sum "$stage/scripts/act_ci.py" | cut -c1-64) as_root=${3:-no}"
exit "$rc"
