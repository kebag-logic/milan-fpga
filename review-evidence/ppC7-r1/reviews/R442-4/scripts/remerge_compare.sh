#!/usr/bin/env bash
# Redo the round-4 merge in a scratch clone and compare it with the published head.
# Usage: remerge_compare.sh REVIEW_CLONE SCRATCH_DIR
# 09's one conflict is resolved mechanically: main's section 8.6 first, then the
# lane's counters section renumbered 8.7. Everything else is git's own merge.
set -u
src=$1 dir=$2
G=/usr/bin/git
rm -rf "$dir" && $G clone -q "$src" "$dir" && cd "$dir" || exit 1
$G -c advice.detachedHead=false checkout -q 9758a98aeee958be7dcdc171943550227e73aaf7
$G -c user.name=r -c user.email=r@x merge --no-ff --no-edit \
  ddb3119dbbce59f81bf7a536a1ad90a20546edb2 2>&1 | /usr/bin/grep -E 'CONFLICT|Auto-merging'
echo "conflicted: $($G diff --name-only --diff-filter=U | tr '\n' ' ')"
python3 - <<'PY'
import re
p = 'docs/architecture/09_verification.md'
s = open(p).read()
m = re.search(r'<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> [0-9a-f]+\n', s, re.S)
ours = m.group(1).replace('### 8.6 The counters face', '### 8.7 The counters face')
open(p, 'w').write(s[:m.start()] + m.group(2) + '\n' + ours + s[m.end():])
PY
$G add -A
echo "== mechanical merge vs published af751a5 (expected: only 00's GAP-05 citation)"
$G diff --cached --stat af751a5aa9a809c982949cfb838a0de1fffc3e46 | cat
$G diff --cached -U0 af751a5aa9a809c982949cfb838a0de1fffc3e46 | /usr/bin/grep '^[-+]' | /usr/bin/grep -o '09 §8\.[0-9]\](architecture/09_verification.md#8[0-9a-z-]*)'
mb=c74711d45a8bbc0d6b38cb49211b26a4a6413e88
echo "== main's side (c74711d..ddb3119) vs (9758a98..af751a5), changed lines per file"
for f in $($G diff --name-only $mb ddb3119dbbce59f81bf7a536a1ad90a20546edb2); do
  d=$(diff <($G diff -U0 $mb ddb3119dbbce59f81bf7a536a1ad90a20546edb2 -- "$f" | /usr/bin/grep '^[-+]' | /usr/bin/grep -v '^+++\|^---') \
           <($G diff -U0 9758a98 af751a5aa9a809c982949cfb838a0de1fffc3e46 -- "$f" | /usr/bin/grep '^[-+]' | /usr/bin/grep -v '^+++\|^---'))
  [ -n "$d" ] && { echo "-- $f"; echo "$d" | cut -c1-160; }
done
echo "== the lane's side (c74711d..9758a98) vs (ddb3119..af751a5), changed lines per file"
for f in $($G diff --name-only ddb3119dbbce59f81bf7a536a1ad90a20546edb2 af751a5aa9a809c982949cfb838a0de1fffc3e46); do
  d=$(diff <($G diff -U0 $mb 9758a98 -- "$f" | /usr/bin/grep '^[-+]' | /usr/bin/grep -v '^+++\|^---') \
           <($G diff -U0 ddb3119dbbce59f81bf7a536a1ad90a20546edb2 af751a5aa9a809c982949cfb838a0de1fffc3e46 -- "$f" | /usr/bin/grep '^[-+]' | /usr/bin/grep -v '^+++\|^---'))
  [ -n "$d" ] && { echo "-- $f"; echo "$d" | cut -c1-160; }
done
echo "== shortstats"
$G diff --shortstat $mb 9758a98; $G diff --shortstat ddb3119dbbce59f81bf7a536a1ad90a20546edb2 af751a5aa9a809c982949cfb838a0de1fffc3e46
