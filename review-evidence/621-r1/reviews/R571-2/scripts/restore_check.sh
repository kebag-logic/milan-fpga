#!/bin/sh
# Usage: restore_check.sh <repo-root>
# Verifies the clone is at exact head bytes: HEAD/tree, clean index and work
# tree, no assume-unchanged/skip-worktree flags, every tracked blob rehashes to
# its index id with matching mode, required gitlinks checked out, and no
# ignored or untracked residue in the parent or initialised submodules.
set -u
root=$1
cd "$root" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
git diff --quiet HEAD && echo "worktree==HEAD: yes" || echo "worktree==HEAD: NO"
git diff --cached --quiet && echo "index==HEAD: yes" || echo "index==HEAD: NO"
echo "flagged entries (assume-unchanged/skip-worktree): $(git ls-files -v | grep -c '^[a-zS]')"
rehash() {
  git ls-files -s | python3 -I -c '
import os, stat, subprocess, sys
bad = n = 0
for line in sys.stdin:
    meta, path = line.rstrip("\n").split("\t", 1)
    mode, oid, _ = meta.split()
    if mode == "160000":
        continue
    n += 1
    st = os.lstat(path)
    if mode == "120000":
        ok = stat.S_ISLNK(st.st_mode)
        got = subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(path).encode(),
                             capture_output=True).stdout.decode().strip()
    else:
        exe = bool(st.st_mode & 0o100)
        ok = stat.S_ISREG(st.st_mode) and (mode == "100755") == exe
        got = subprocess.run(["git", "hash-object", path], capture_output=True, text=True).stdout.strip()
    if not ok or got != oid:
        bad += 1
        print("MISMATCH", path)
print(f"{n} tracked blobs rehashed, {bad} mismatches")
'
}
echo "parent: $(rehash)"
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$sub" | awk '{print $3}')
  have=$(git -C "$sub" rev-parse HEAD)
  top=$(git -C "$sub" rev-parse --show-toplevel)
  echo "gitlink $sub want $want have $have top $top match $([ "$want" = "$have" ] && echo yes || echo NO)"
  echo "  $sub: $(cd "$sub" && rehash)"
  echo "  $sub status --ignored entries: $(git -C "$sub" status --porcelain --ignored | wc -l)"
done
echo "parent status --ignored entries: $(git status --porcelain --ignored | wc -l)"
git status --porcelain --ignored
