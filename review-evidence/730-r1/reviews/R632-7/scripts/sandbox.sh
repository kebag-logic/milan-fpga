#!/usr/bin/env bash
# Run a command inside an unprivileged, disposable boundary: no network, no
# Docker socket (/run is not mounted), read-only system, a private /tmp, and
# only TREE writable. Usage: sandbox.sh TREE CMD [ARGS...]
#   SANDBOX_TREE_RO=1   bind TREE read-only instead
#   SANDBOX_RO=a:b      extra paths bound read-only (a venv, git alternates)
set -euo pipefail
tree=$(realpath "$1"); shift
mode=--bind
[ "${SANDBOX_TREE_RO:-0}" = 1 ] && mode=--ro-bind
extra=()
IFS=: read -r -a ro <<< "${SANDBOX_RO:-}"
for path in "${ro[@]}"; do [ -n "$path" ] && extra+=(--ro-bind "$path" "$path"); done
exec bwrap \
  --unshare-all --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib \
  --symlink usr/lib /lib64 --symlink usr/bin /sbin \
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp \
  "$mode" "$tree" "$tree" "${extra[@]}" --chdir "$tree" \
  --setenv HOME /tmp --setenv PATH /usr/bin --setenv LANG C.UTF-8 \
  --unsetenv DOCKER_HOST --unsetenv DOCKER_CONTEXT --unsetenv DOCKER_CONFIG \
  "$@"
