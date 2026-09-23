#!/usr/bin/env bash
# [R267] Run a runner file's offline --selftest ONLY inside a disposable,
# network-less, unprivileged sandbox (bubblewrap: new user, net, pid, ipc, uts
# and cgroup namespaces; read-only /usr and /etc; empty /home, /run and /tmp).
# No Docker daemon socket, no host home, no credential and no network are
# visible inside. Never used for a host-side runner invocation.
#
# Usage: run-selftest-sandbox.sh STAGE_TREE RUNNER_RELATIVE_PATH LABEL [root]
#   STAGE_TREE  a disposable clone at the revision under test (scratch only)
#   RUNNER_...  e.g. scripts/act_ci.py (a mutant copy may be named instead)
#   LABEL       receipt label
#   root        map the sandbox user to uid 0 inside its own user namespace
set -euo pipefail
stage=$(cd "$1" && pwd)
runner=$2
label=$3
as_root=${4:-}
uid_args=()
if [ "$as_root" = root ]; then uid_args=(--uid 0 --gid 0); fi
set +e
bwrap --unshare-all --die-with-parent --new-session "${uid_args[@]}" \
  --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 \
  --symlink usr/bin /bin --symlink usr/bin /sbin --ro-bind /etc /etc \
  --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run --tmpfs /home \
  --tmpfs /var --bind "$stage" /work --chdir /work \
  --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /tmp \
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 \
  sh -c 'id -u; ip -o link 2>/dev/null | cut -d: -f2 | tr -d " " | tr "\n" " "; echo; exec python3 '"$runner"' --selftest'
rc=$?
set -e
echo "sandbox-selftest label=$label rc=$rc rev=$(git -C "$stage" rev-parse HEAD) runner=$runner sha256=$(sha256sum "$stage/$runner" | cut -c1-64) as_root=${as_root:-no}"
exit "$rc"
