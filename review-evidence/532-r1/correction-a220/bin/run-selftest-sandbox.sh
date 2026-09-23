#!/usr/bin/env bash
# [A220] Run the lane's offline act_ci.py --selftest ONLY inside a disposable,
# network-less, unprivileged bubblewrap sandbox: new user, net, pid, ipc, uts
# and cgroup namespaces (only lo), read-only /usr and /etc, empty /home, /run,
# /tmp and /var, and the lane tree bound READ-ONLY at /work, so the self-test
# can neither write the lane nor see a Docker socket, host home, credential or
# network. An optional third argument is a file bound read-only over
# /work/scripts/act_ci.py (a mutant); the lane's own file is never modified.
# Never used for a host-side runner invocation (runner-change bootstrap rule).
# Usage: run-selftest-sandbox.sh LANE_TREE user|root [ACT_CI_OVERRIDE]
set -euo pipefail
tree=$(cd "$1" && pwd)
uid_args=()
if [ "$2" = root ]; then uid_args=(--uid 0 --gid 0); fi
override=()
if [ -n "${3:-}" ]; then override=(--ro-bind "$(realpath "$3")" /work/scripts/act_ci.py); fi
set +e
bwrap --unshare-all --die-with-parent --new-session "${uid_args[@]}" \
  --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 \
  --symlink usr/bin /bin --symlink usr/bin /sbin --ro-bind /etc /etc \
  --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run --tmpfs /home \
  --tmpfs /var --ro-bind "$tree" /work "${override[@]}" --chdir /work \
  --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /tmp \
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 \
  sh -c 'echo "sandbox uid=$(id -u) links=$(tail -n +3 /proc/net/dev | cut -d: -f1 | tr -d " " | tr "\n" " ")"; exec python3 scripts/act_ci.py --selftest'
rc=$?
set -e
digest=$(sha256sum "${3:-$tree/scripts/act_ci.py}" | cut -c1-64)
echo "sandbox-selftest rc=$rc head=$(git -C "$tree" rev-parse HEAD) dirty=$(git -C "$tree" status --porcelain | wc -l) act_ci.py sha256=$digest as=$2"
exit "$rc"
