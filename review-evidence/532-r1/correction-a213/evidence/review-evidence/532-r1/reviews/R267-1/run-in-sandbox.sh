#!/usr/bin/env bash
# [R267] Run one packet probe script against a base and a head stage clone
# ONLY inside a disposable network-less unprivileged sandbox (same boundary as
# run-selftest-sandbox.sh). Stage clones are bound read-only at /base and /head.
# Usage: run-in-sandbox.sh BASE_STAGE HEAD_STAGE PROBE.py [root]
set -euo pipefail
base=$(cd "$1" && pwd)
head=$(cd "$2" && pwd)
probe=$(cd "$(dirname "$3")" && pwd)/$(basename "$3")
uid_args=()
if [ "${4:-}" = root ]; then uid_args=(--uid 0 --gid 0); fi
exec bwrap --unshare-all --die-with-parent --new-session "${uid_args[@]}" \
  --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 \
  --symlink usr/bin /bin --symlink usr/bin /sbin --ro-bind /etc /etc \
  --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run --tmpfs /home --tmpfs /var \
  --ro-bind "$base" /base --ro-bind "$head" /head --ro-bind "$probe" /probe.py \
  --chdir /tmp --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /tmp \
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 \
  python3 -I /probe.py
