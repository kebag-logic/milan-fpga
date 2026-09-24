#!/usr/bin/env bash
# writable_no_bit_probe.sh FILE: whether the proof's non-root writability clause
# ([ "$(id -u)" -ne 0 ] && [ -w FILE ]) holds for FILE with no write bit, first as
# the plain invoker, then inside an unprivileged user namespace that maps the
# invoker's own uid and keeps its namespace capabilities as ambient ones.
set -u
file=$1
stat -c 'mode=%a owner=%u' "$file"
clause='if [ "$(id -u)" -ne 0 ] && [ -w "$1" ]; then echo "uid=$(id -u): clause TRUE (writable, no write bit)"; else echo "uid=$(id -u): clause false"; fi; [ -n "$(find "$1" -maxdepth 0 -perm /0222)" ] && echo "write bit present" || echo "no write bit"'
bash -c "$clause" _ "$file"
unshare --user --map-user="$(id -u)" --map-group="$(id -g)" --keep-caps -- bash -c "$clause" _ "$file"
