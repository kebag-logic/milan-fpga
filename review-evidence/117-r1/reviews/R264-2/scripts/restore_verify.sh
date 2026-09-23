#!/usr/bin/env bash
# Verify a review clone is exactly the reviewed head: HEAD and tree ids, index
# equal to HEAD, every tracked regular file byte- and mode-identical to its
# blob, gitlinks at their pins, and no untracked or ignored file.
# usage: restore_verify.sh CLONE HEAD_SHA TREE_SHA
set -euo pipefail
clone=$1 head=$2 tree=$3
cd "$clone"
echo "HEAD $(git rev-parse HEAD) expected $head"
[ "$(git rev-parse HEAD)" = "$head" ]
echo "tree $(git rev-parse 'HEAD^{tree}') expected $tree"
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ]
git diff-index --cached --quiet HEAD && echo "index equals HEAD"
python3 - "$clone" <<'PY'
import os, subprocess, sys, stat
clone = sys.argv[1]
out = subprocess.run(['git', 'ls-files', '-s', '-z'], capture_output=True, check=True, cwd=clone).stdout
n = bad = links = 0
for ent in out.split(b'\0'):
    if not ent:
        continue
    meta, path = ent.split(b'\t', 1)
    mode, oid, stage = meta.split()
    p = os.path.join(clone, path.decode())
    if mode == b'160000':
        links += 1
        continue
    n += 1
    st = os.lstat(p)
    if mode == b'120000':
        ok = stat.S_ISLNK(st.st_mode) and os.readlink(p).encode() == subprocess.run(['git', 'cat-file', 'blob', oid], capture_output=True, cwd=clone).stdout
    else:
        h = subprocess.run(['git', 'hash-object', '--no-filters', p], capture_output=True, check=True, cwd=clone).stdout.strip()
        exe = bool(st.st_mode & 0o100)
        ok = h == oid and ((mode == b'100755') == exe) and stat.S_ISREG(st.st_mode)
    if not ok:
        bad += 1
        print('MISMATCH', path.decode())
print('tracked files checked %d, mismatches %d, gitlinks %d' % (n, bad, links))
sys.exit(1 if bad else 0)
PY
git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
git submodule status
extra=$(git status --porcelain --ignored | wc -l)
echo "untracked/ignored/modified entries: $extra"
[ "$extra" -eq 0 ]
echo RESTORE-VERIFY OK
