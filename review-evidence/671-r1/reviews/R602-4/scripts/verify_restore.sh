#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer restore check for PR #715 round R602-4: the clone is at the exact
# head, its index equals the head tree in mode, blob and path, every tracked
# worktree file re-hashes to its blob, nothing untracked or ignored remains,
# and the required gitlinks sit at their pins, clean.
# Usage: verify_restore.sh CLONE EXPECTED_HEAD
set -u
clone=$1
want=$2
cd "$clone" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "HEAD tree $(git rev-parse 'HEAD^{tree}')"
echo "index tree $(git write-tree)"
[ "$(git rev-parse HEAD)" = "$want" ] && echo "head matches: yes" || echo "head matches: NO"
echo "status lines incl. ignored: $(git status --short --ignored | wc -l)"
if diff <(git ls-files -s | awk '{print $1, $2, $4}') \
        <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null; then
	echo "ls-files -s equals ls-tree -r HEAD (mode, blob, path): yes"
else
	echo "ls-files -s equals ls-tree -r HEAD (mode, blob, path): NO"
fi
bad=0
git ls-files -s | while read -r mode blob stage path; do
	[ "$mode" = 160000 ] && continue
	if [ "$mode" = 120000 ]; then
		got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
	else
		got=$(git hash-object --no-filters -- "$path")
	fi
	[ "$got" = "$blob" ] || echo "MISMATCH $path"
done > /tmp/r602_4_rehash.$$
echo "worktree blob re-hash mismatches: $(wc -l < /tmp/r602_4_rehash.$$)"
cat /tmp/r602_4_rehash.$$
rm -f /tmp/r602_4_rehash.$$
for s in protocol-processor gptp-processor third_party/verilog-axis; do
	pin=$(git ls-tree HEAD "$s" | awk '{print $3}')
	got=$(git -C "$s" rev-parse HEAD)
	echo "gitlink $s pin $pin checkout $got status-lines $(git -C "$s" status --short --ignored | wc -l)"
done
git submodule status
