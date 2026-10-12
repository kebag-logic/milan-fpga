#!/usr/bin/env bash
# R585-14 independent probes of the pin proof (ctrl_build.py --stack-pin) at a superproject checkout.
# usage: r585_14_probes.sh <superproject-checkout-with-tsn-c-stack-initialised> <scratch-dir>
# Each probe makes a fresh clone of the stack, plants one state, runs the pin check, and prints
# the probe id, the exit status, how many times a recorder program ran, and the check's last line.
set -u
TOP=$(cd "$1" && pwd); OUT=$2
STACK=$TOP/third_party/tsn-c-stack
CHECK=$TOP/sw/firmware/ctrl/test/ctrl_build.py
PIN=$(git -C "$TOP" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
mkdir -p "$OUT"

fresh() {  # fresh <dir> [loose]: clone of the stack at the pin; loose: every object loose, no alternates
  rm -rf "$1"; mkdir -p "$1"
  if [ "${2:-}" = loose ]; then
    git init -q "$1/s"
    git -C "$1/s" -c fetch.unpackLimit=1000000 fetch -q --no-tags "$STACK" "$PIN"
    git -C "$1/s" -c advice.detachedHead=false checkout -q "$PIN"
  else
    git -c advice.detachedHead=false clone -q --no-hardlinks "$STACK" "$1/s"
    git -C "$1/s" -c advice.detachedHead=false checkout -q "$PIN"
  fi
  printf '#!/bin/sh\necho "$0 $*" >> "%s/ran"\nexit 1\n' "$1" > "$1/rec"; chmod +x "$1/rec"
}
obj() { echo "$1/s/.git/objects/${2:0:2}/${2:2}"; }
forge() {  # forge <dir> <victim> <source>: victim's loose file replaced by a copy of source's
  local v s; v=$(obj "$1" "$2"); s=$(obj "$1" "$3"); cp "$s" "$v.new"; chmod 444 "$v.new"; mv -f "$v.new" "$v"
}
mktree_with() {  # mktree_with <repo> <tree> <name> <oid>: tree with entry name -> oid
  git -C "$1" ls-tree -z "$2" | python3 -I -c '
import sys
name, oid = sys.argv[1], sys.argv[2]
out = []
for e in filter(None, sys.stdin.buffer.read().split(b"\0")):
    meta, n = e.split(b"\t", 1)
    if n.decode() == name:
        m, t, _ = meta.split(b" ")
        meta = b" ".join((m, t, oid.encode()))
    out.append(meta + b"\t" + n)
sys.stdout.buffer.write(b"\0".join(out) + b"\0")' "$3" "$4" | git -C "$1" mktree -z
}
run() {  # run <id> <dir>
  local o rc n
  o=$(python3 -I "$CHECK" --stack-pin "$2/s" 2>&1); rc=$?
  n=$( [ -f "$2/ran" ] && wc -l < "$2/ran" || echo 0)
  printf '%s rc=%s RAN=%s :: %s\n' "$1" "$rc" "$n" "$(printf '%s' "$o" | tail -1)"
}

D=$OUT/p
# Q0 clean clone
fresh "$D" && run Q0-clean "$D"
# Q1 forged nested tree two levels down (the first subtree of a subtree), beside an edit under it
fresh "$D" loose
sub=$(git -C "$D/s" ls-tree -r -t "$PIN" | awk '$2=="tree" && $4 ~ /\// {print $4; exit}')
file=$(git -C "$D/s" ls-tree -r "$PIN" -- "$sub" | awk '$2=="blob"{print $4; exit}')
echo "  Q1 nested tree: $sub, file: $file"
printf '\n/* r585-14 */\n' >> "$D/s/$file"
blob=$(git -C "$D/s" hash-object -w "$D/s/$file")
old=$(git -C "$D/s" rev-parse "$PIN:$sub")
new=$(mktree_with "$D/s" "$old" "$(basename "$file")" "$blob")
forge "$D" "$old" "$new"; run Q1-forged-nested-tree "$D"
# Q2 forged root tree, beside an edit of src/adp.c
fresh "$D" loose
printf '\n/* r585-14 */\n' >> "$D/s/src/adp.c"
blob=$(git -C "$D/s" hash-object -w "$D/s/src/adp.c")
src=$(git -C "$D/s" rev-parse "$PIN:src"); nsrc=$(mktree_with "$D/s" "$src" adp.c "$blob")
root=$(git -C "$D/s" rev-parse "$PIN^{tree}"); nroot=$(mktree_with "$D/s" "$root" src "$nsrc")
forge "$D" "$root" "$nroot"; run Q2-forged-root-tree "$D"
# Q3 forged src/ tree reached only through objects/info/alternates (own store lacks it)
fresh "$D" loose
mkdir -p "$D/alt" && git init -q --bare "$D/alt/a.git"
printf '\n/* r585-14 */\n' >> "$D/s/src/adp.c"
blob=$(git -C "$D/s" hash-object -w "$D/s/src/adp.c")
nsrc=$(mktree_with "$D/s" "$src" adp.c "$blob")
mkdir -p "$D/alt/a.git/objects/${src:0:2}"; cp "$(obj "$D" "$nsrc")" "$D/alt/a.git/objects/${src:0:2}/${src:2}"
rm -f "$(obj "$D" "$src")"; echo "$D/alt/a.git/objects" > "$D/s/.git/objects/info/alternates"
run Q3-forged-tree-via-alternates "$D"
# Q4 forged tree inside a pack (no loose copy): pack the forged bytes under the pinned id is not possible with
#    git's own tools, so instead the pinned tree is held only in a pack and its loose copy truncated (corrupt)
fresh "$D" loose
f=$(obj "$D" "$src"); head -c 20 < "$f" > "$f.tmp"; mv -f "$f.tmp" "$f"
run Q4-corrupt-loose-tree "$D"
# Q5 mixed-case refused key in the stack's config, written by hand
fresh "$D"
printf '[Core]\n\tFSMonitor = %s/rec\n[Remote "origin"]\n\tUploadPack = %s/rec\n' "$D" "$D" >> "$D/s/.git/config"
run Q5-mixed-case-keys "$D"
# Q6 key with no value (implicit true) outside the allowlist, and inside it
fresh "$D"; printf '[core]\n\tsshCommand\n' >> "$D/s/.git/config"; run Q6a-valueless-refused-key "$D"
fresh "$D"; printf '[core]\n\tbare = false\n\tfilemode\n' >> "$D/s/.git/config"; run Q6b-valueless-allowlisted "$D"
# Q7 dotted subsection that ends in an allowlisted variable name of another family
fresh "$D"; git -C "$D/s" config 'remote.a.b.c.url' x; run Q7a-dotted-subsection-allowlisted "$D"
fresh "$D"; git -C "$D/s" config 'core.x.filemode' true; run Q7b-subsection-on-flat-key "$D"
fresh "$D"; git -C "$D/s" config 'remote.url' x; run Q7c-flat-key-of-subsection-family "$D"
# Q8 conditional include (includeIf) naming the recorder as core.fsmonitor
fresh "$D"; printf '[core]\n\tfsmonitor = %s/rec\n' "$D" > "$D/inc"
git -C "$D/s" config "includeIf.gitdir:/.path" "$D/inc"; run Q8-includeif "$D"
# Q9 unreadable configuration (syntax error): fail closed, before any object read
fresh "$D"; printf '[core\n' >> "$D/s/.git/config"; run Q9-broken-config "$D"
# Q10 core.worktree pointing elsewhere (allowlisted key, hostile value)
fresh "$D"; mkdir -p "$D/elsewhere"; git -C "$D/s" config core.worktree "$D/elsewhere"; run Q10-worktree-elsewhere "$D"
# Q11 sha256 object format extension
fresh "$D"; git -C "$D/s" config core.repositoryformatversion 1; git -C "$D/s" config extensions.objectFormat sha256
run Q11-objectformat-extension "$D"
# Q12 partial clone, uploadpack recorder, src/ tree missing, GIT_NO_LAZY_FETCH and allowlist both on (as shipped)
fresh "$D" loose
for kv in core.repositoryformatversion=1 extensions.partialClone=origin "remote.origin.url=$D/s" \
          remote.origin.promisor=true "remote.origin.uploadpack=$D/rec"; do git -C "$D/s" config "${kv%%=*}" "${kv#*=}"; done
rm -f "$(obj "$D" "$src")"; run Q12-promisor-uploadpack-missing-tree "$D"
# Q13 the same state read by Git directly with the helper's own environment (lazy-fetch layer alone)
env -i PATH="$PATH" GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null/no-grafts GIT_CONFIG_NOSYSTEM=1 \
  GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 git -c core.fsmonitor=false -C "$D/s" cat-file tree "$src" >/dev/null 2>&1
echo "Q13-git-direct-with-GIT_NO_LAZY_FETCH rc=$? RAN=$( [ -f "$D/ran" ] && wc -l < "$D/ran" || echo 0)"
env -i PATH="$PATH" GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null/no-grafts GIT_CONFIG_NOSYSTEM=1 \
  GIT_CONFIG_GLOBAL=/dev/null git -c core.fsmonitor=false -C "$D/s" cat-file tree "$src" >/dev/null 2>&1
echo "Q14-git-direct-without-GIT_NO_LAZY_FETCH rc=$? RAN=$( [ -f "$D/ran" ] && wc -l < "$D/ran" || echo 0)"
# Q15 worktree scope key allowlisted (core.worktree in config.worktree needs extensions.worktreeConfig: refused)
fresh "$D"; git -C "$D/s" config extensions.worktreeConfig true; run Q15-worktreeconfig-extension-alone "$D"
# Q16 repository whose .git file points to another gitdir holding the pin (relocated store), genuine objects
fresh "$D"; mv "$D/s/.git" "$D/gitdir"; echo "gitdir: $D/gitdir" > "$D/s/.git"; git -C "$D/s" config core.worktree "$D/s"
run Q16-gitfile-relocated-genuine "$D"
rm -rf "$D"
