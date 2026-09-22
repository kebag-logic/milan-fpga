#!/usr/bin/env bash
# Capture review-checkout integrity: HEAD, tree, index digest, status, submodule
# gitlinks and working-tree blob/mode/kind digest. Read-only.
# Usage: 00_integrity.sh <label>   (writes receipts/integrity-<label>.txt)
set -euo pipefail
R=$VALIDATION_STORAGE/reviews/r222-478-r2
OUT=$WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-r2-r222/receipts
label=${1:-snapshot}
f="$OUT/integrity-$label.txt"
{
  echo "date: $(date -Is)"
  echo "HEAD: $(git -C "$R" rev-parse HEAD)"
  echo "HEAD^{tree}: $(git -C "$R" rev-parse 'HEAD^{tree}')"
  echo "write-tree(index): $(git -C "$R" write-tree 2>/dev/null || echo ERR)"
  echo "ls-files -s sha256: $(git -C "$R" ls-files -s | sha256sum | cut -d' ' -f1)"
  echo "ls-files -s count: $(git -C "$R" ls-files -s | wc -l)"
  echo "ls-tree -r HEAD sha256: $(git -C "$R" ls-tree -r HEAD | sha256sum | cut -d' ' -f1)"
  echo "gitlinks (mode 160000):"
  git -C "$R" ls-files -s | awk '$1=="160000"'
  echo "status --porcelain=v2 --ignored=no --untracked-files=all:"
  git -C "$R" status --porcelain=v2 --untracked-files=all
  echo "(end status)"
  echo "submodule status:"
  git -C "$R" submodule status
  echo "diff-index HEAD (tracked working changes):"
  git -C "$R" diff-index --no-renames HEAD --
  echo "(end diff-index)"
  # Working-tree content check: hash every tracked regular file / symlink and
  # compare with the index blob id; report mismatches and mode differences.
  echo "worktree-vs-index blob/mode/kind check:"
  git -C "$R" ls-files -s -z | python3 -c '
import sys, os, subprocess, stat
R = sys.argv[1]
data = sys.stdin.buffer.read().split(b"\0")
bad = 0; n = 0
for ent in data:
    if not ent: continue
    meta, path = ent.split(b"\t", 1)
    mode, sha, stage = meta.split()
    p = os.path.join(R.encode(), path)
    n += 1
    mode = mode.decode(); sha = sha.decode()
    if mode == "160000":
        if not os.path.isdir(p):
            print("KIND-MISMATCH gitlink not dir", path.decode()); bad += 1
        continue
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        print("MISSING", path.decode()); bad += 1; continue
    if mode == "120000":
        if not stat.S_ISLNK(st.st_mode):
            print("KIND-MISMATCH expected symlink", path.decode()); bad += 1; continue
        target = os.readlink(p)
        h = subprocess.run(["git","hash-object","--stdin"], input=target, capture_output=True).stdout.decode().strip()
    else:
        if not stat.S_ISREG(st.st_mode):
            print("KIND-MISMATCH expected regular", path.decode()); bad += 1; continue
        exe = bool(st.st_mode & 0o111)
        if (mode == "100755") != exe:
            print("MODE-MISMATCH", mode, oct(st.st_mode), path.decode()); bad += 1
        h = subprocess.run(["git","hash-object","--no-filters",p], capture_output=True).stdout.decode().strip()
    if h != sha:
        print("BLOB-MISMATCH", path.decode(), sha, h); bad += 1
print(f"checked {n} index entries; mismatches={bad}")
' "$R"
  echo "submodule HEADs vs gitlinks:"
  git -C "$R" ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r sha path; do
    if [ -e "$R/$path/.git" ]; then
      echo "$path gitlink=$sha subHEAD=$(git -C "$R/$path" rev-parse HEAD) dirty=$(git -C "$R/$path" status --porcelain | wc -l)"
    else
      echo "$path gitlink=$sha (not initialized)"
    fi
  done
} > "$f" 2>&1
echo "wrote $f"
