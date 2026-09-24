#!/usr/bin/env bash
# sandbox.sh uid1000|uid0 CMD...: run CMD in new unprivileged user+net namespaces
# (only `lo`, no route), as the invoker's uid mapped to itself, or as namespace uid 0.
# No privilege is gained on the host; a setuid binary cannot elevate from here.
set -euo pipefail
mode=$1; shift
case "$mode" in
  uid1000) exec unshare --user --map-user="$(id -u)" --map-group="$(id -g)" --net -- "$@" ;;
  uid0) exec unshare --user --map-root-user --net -- "$@" ;;
  *) echo "usage: sandbox.sh uid1000|uid0 CMD..." >&2; exit 2 ;;
esac
