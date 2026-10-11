#!/bin/bash
# Verify a review clone is the exact head: HEAD and tree, index equal to HEAD's tree (paths, modes, blobs,
# gitlinks, stage 0, no assume-unchanged/skip-worktree flags), every tracked file's disk bytes and mode equal to
# its blob (read with replacement objects disabled), no replace refs, and each initialised submodule at its
# gitlink with clean tracked bytes and no replace refs, grafts, attributes or filters left.
# Usage: verify_clone.sh <clone> <expected head> <expected tree>
set -u
C=$(cd "$1" && pwd); H=$2; T=$3; export GIT_NO_REPLACE_OBJECTS=1; bad=0
say() { echo "$*"; }
[ "$(git -C "$C" rev-parse HEAD)" = "$H" ] && say "HEAD $H ok" || { say "HEAD MISMATCH"; bad=1; }
[ "$(git -C "$C" rev-parse HEAD^{tree})" = "$T" ] && say "tree $T ok" || { say "TREE MISMATCH"; bad=1; }
[ "$(git -C "$C" write-tree)" = "$T" ] && say "index writes the head tree" || { say "INDEX != HEAD tree"; bad=1; }
flags=$(git -C "$C" ls-files -v | grep -vc '^H ')
[ "$flags" = 0 ] && say "index flags: 0 entries not 'H'" || { say "INDEX FLAGS: $flags"; bad=1; }
stages=$(git -C "$C" ls-files --stage | awk '$3 != 0' | wc -l)
[ "$stages" = 0 ] && say "unmerged stages: 0" || { say "UNMERGED: $stages"; bad=1; }
[ -z "$(git -C "$C" replace -l)" ] && say "replace refs: none" || { say "REPLACE REFS PRESENT"; bad=1; }
[ ! -e "$(git -C "$C" rev-parse --git-path info/grafts)" ] && say "graft file: none" || { say "GRAFT FILE"; bad=1; }
# every tracked file's bytes and mode, hashed here from disk, against the index blob
python3 -I - "$C" <<'EOF' || bad=1
import hashlib, os, stat, subprocess, sys
c = sys.argv[1]
out = subprocess.run(["git", "-C", c, "ls-files", "-s", "-z"], capture_output=True, check=True).stdout
n = diff = 0
for rec in filter(None, out.split(b"\0")):
    meta, path = rec.split(b"\t", 1)
    mode, oid, _ = meta.split()
    if mode == b"160000":
        continue
    p = os.path.join(c.encode(), path)
    st = os.lstat(p)
    data = os.readlink(p) if stat.S_ISLNK(st.st_mode) else open(p, "rb").read()
    got = "120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & stat.S_IXUSR else "100644")
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    n += 1
    if got != mode.decode() or h != oid.decode():
        diff += 1
        print("DIFFERS:", path.decode(errors="replace"), mode.decode(), got)
print(f"tracked files checked from disk: {n}, differing in bytes or mode: {diff}")
sys.exit(1 if diff else 0)
EOF
git -C "$C" ls-files -s | awk '$1 == 160000 {print $2, $4}' | while read -r oid path; do
  if [ -e "$C/$path/.git" ]; then
    head=$(git -C "$C/$path" rev-parse HEAD); dirty=$(git -C "$C/$path" status --porcelain --untracked-files=all | wc -l)
    rep=$(git -C "$C/$path" replace -l | wc -l); gd=$(git -C "$C/$path" rev-parse --absolute-git-dir)
    extra=$(ls "$gd/info/grafts" "$gd/info/attributes" 2>/dev/null | wc -l); filt=$(git -C "$C/$path" config --get-regexp '^filter\.' | wc -l)
    st=ok; [ "$head" = "$oid" ] && [ "$dirty" = 0 ] && [ "$rep" = 0 ] && [ "$extra" = 0 ] && [ "$filt" = 0 ] || st=BAD
    echo "submodule $path gitlink $oid HEAD $head dirty $dirty replace $rep grafts/attributes $extra filters $filt: $st"
  else echo "submodule $path gitlink $oid: not initialised"; fi
done > "${TMPDIR:-/tmp}/verify_clone_subs.$$"
cat "${TMPDIR:-/tmp}/verify_clone_subs.$$"; grep -q ': BAD$' "${TMPDIR:-/tmp}/verify_clone_subs.$$" && bad=1
rm -f "${TMPDIR:-/tmp}/verify_clone_subs.$$"
echo "status --porcelain (tracked and untracked, ignored excluded): $(git -C "$C" status --porcelain | wc -l) lines"
[ $bad = 0 ] && echo "VERIFY: PASS" || echo "VERIFY: FAIL"
exit $bad
