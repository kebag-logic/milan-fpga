#!/usr/bin/env bash
# Re-check R632-2-F1: run the scope selftest with a signing global config and
# with an exported GIT_DIR aimed at a victim repository; the selftest must pass
# and the victim's .git bytes must be unchanged.
# Usage: hostile_env_check.sh <shipping-tree> <empty-dir>
set -uo pipefail
ship="$1"; w="$2"; mkdir -p "$w/home" "$w/victim" "$w/tmp"
printf '[commit]\n\tgpgsign = true\n[user]\n\tsigningkey = DEADBEEF\n' > "$w/home/.gitconfig"
( cd "$w/victim" && HOME="$w/home" GIT_CONFIG_GLOBAL=/dev/null git -c user.name=v -c user.email=v@x.invalid init -q && HOME="$w/home" GIT_CONFIG_GLOBAL=/dev/null git -c user.name=v -c user.email=v@x.invalid -c commit.gpgsign=false commit -q --allow-empty -m victim )
before="$(cd "$w/victim/.git" && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)"
cd "$ship"
HOME="$w/home" TMPDIR="$w/tmp" PYTHONDONTWRITEBYTECODE=1 python3 scripts/ci_scope.py --selftest > "$w/signing.log" 2>&1; echo "signing-config selftest rc=$? ($(tail -1 "$w/signing.log"))"
HOME="$w/home" TMPDIR="$w/tmp" PYTHONDONTWRITEBYTECODE=1 GIT_DIR="$w/victim/.git" GIT_WORK_TREE="$w/victim" GIT_INDEX_FILE="$w/victim/.git/index" python3 scripts/ci_scope.py --selftest > "$w/gitdir.log" 2>&1; echo "exported-GIT_DIR selftest rc=$? ($(tail -1 "$w/gitdir.log"))"
after="$(cd "$w/victim/.git" && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)"
[ "$before" = "$after" ] && echo "victim .git bytes unchanged" || echo "VICTIM CHANGED"
