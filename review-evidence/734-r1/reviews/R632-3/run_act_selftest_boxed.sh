#!/usr/bin/env bash
# Run the candidate runner's offline selftest only inside a disposable,
# network-less, credential-less bubblewrap boundary (no Docker, no privilege).
# Usage: run_act_selftest_boxed.sh <readonly-candidate-tree> <writable-box-dir> <mode: ordinary|flat>
set -euo pipefail
cand="$1"; box="$2"; mode="$3"
rm -rf "$box"; mkdir -p "$box/home" "$box/tmp" "$box/install"
inner='set -euo pipefail
cd /box/tmp
if [ "$MODE" = ordinary ]; then
  python3 /cand/scripts/act_ci.py --selftest
else
  install -m 0555 /cand/scripts/act_ci.py /box/install/act_ci.py
  ls -la /box/install
  python3 -I /box/install/act_ci.py --selftest --worktree /cand
fi'
exec bwrap --unshare-all --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin \
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /run --tmpfs /var \
  --ro-bind "$cand" /cand --bind "$box" /box \
  --clearenv --setenv PATH /usr/bin --setenv HOME /box/home --setenv TMPDIR /box/tmp \
  --setenv PYTHONDONTWRITEBYTECODE 1 --setenv LANG C.UTF-8 --setenv MODE "$mode" \
  bash -c "$inner"
