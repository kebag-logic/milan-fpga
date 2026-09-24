#!/usr/bin/env bash
# sandbox.sh root|user TREE -- CMD...: run CMD in TREE inside a disposable,
# unprivileged, network-less namespace sandbox (new user, mount, net, pid, ipc,
# uts and cgroup namespaces; only `lo`). /run (and so /var/run, the Docker
# socket and sudo timestamps), /tmp and $HOME are replaced by empty tmpfs, TREE
# is bound read-only, and setuid helpers gain nothing because host root is not
# mapped. `root` runs CMD as the namespace's uid 0; `user` as uid 1000 with no
# capabilities, through a nested user namespace.
set -euo pipefail
mode=$1 tree=$2
shift 2
[ "$1" = -- ] && shift
case "$mode" in root|user) ;; *) echo "sandbox.sh: mode root|user" >&2; exit 2 ;; esac
exec unshare --user --map-root-user --mount --propagation private --net --pid --fork \
  --mount-proc --ipc --uts --cgroup -- bash -euo pipefail -c '
mode=$1 tree=$2; shift 2
mount -t tmpfs -o mode=0755 tmpfs /run
mount -t tmpfs -o mode=1777 tmpfs /tmp
mount -t tmpfs -o mode=0755 tmpfs "$HOME"
mkdir -p "$HOME/h" && chmod 0777 "$HOME/h"
mount --bind "$tree" "$tree"
mount -o remount,bind,ro "$tree"
cd "$tree"
export HOME=$HOME/h TMPDIR=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8
unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG SSH_AUTH_SOCK GH_TOKEN GITHUB_TOKEN
if [ "$mode" = user ]; then
  exec unshare --user --map-user=1000 --map-group=1000 -- "$@"
fi
exec "$@"
' sandbox "$mode" "$tree" "$@"
