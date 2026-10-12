#!/usr/bin/env bash
# Object-store and repository-configuration probes of the tsn-c-stack pin proof (#697, PR #705).
# usage: forge_probes.sh <head checkout> <previous-head checkout> <stack checkout at the pin> <work dir>
# Each probe builds a fresh stack clone whose objects are all loose in its own store, spoils it, and runs each
# checkout's pin CLI (ctrl_build.py --stack-pin DIR) on it, printing the exit status, the verdict line and how
# many times a recorder program named by a repository's configuration ran.
set -u
HEAD_REPO=$(realpath "$1"); OLD_REPO=$(realpath "$2"); SRC=$(realpath "$3"); WORK=$(realpath -m "$4")
rm -rf "$WORK"; mkdir -p "$WORK"
PIN=$(git -C "$HEAD_REPO" ls-files --stage third_party/tsn-c-stack | awk '{print $2}')
EDITED=src/adp.c

recorder() {  # $1: log file; prints the recorder's path
  local r="$WORK/recorder-$RANDOM"
  printf '#!/bin/sh\necho "ran $*" >> %s\nexit 1\n' "$1" > "$r"; chmod +x "$r"; echo "$r"
}
loose_clone() {  # $1: dir
  git init -q "$1"
  git -C "$1" -c fetch.unpackLimit=1000000 fetch -q --no-tags "$SRC" "$PIN"
  git -C "$1" -c advice.detachedHead=false checkout -q "$PIN"
  [ -z "$(ls "$1/.git/objects/pack")" ] || { echo "SETUP: pack kept"; exit 3; }
}
obj() { echo "$1/.git/objects/${2:0:2}/${2:2}"; }
forge() {  # $1 dir, $2 victim id, $3 source id: the victim's loose file replaced by a new file with the source's
  local v; v=$(obj "$1" "$2"); cp "$(obj "$1" "$3")" "$v.new"; mv -f "$v.new" "$v"
}
edit() { printf '\n/* probe edit */\n' >> "$1/$EDITED"; }
remade() {  # $1 dir, $2 tree id, $3 entry name, $4 new id: prints the new tree id
  git -C "$1" ls-tree -z "$2" | perl -0 -pe 's/^(\d+ \w+) [0-9a-f]+\t\Q'"$3"'\E\0/$1 '"$4"'\t'"$3"'\0/' \
    | git -C "$1" mktree -z
}
edited_blob() { git -C "$1" hash-object -w "$1/$EDITED"; }
run_both() {  # $1 label, $2 dir, $3 recorder log (optional)
  local log=${3:-/dev/null}
  for side in head old; do
    local repo=$HEAD_REPO; [ $side = old ] && repo=$OLD_REPO
    local before=0; [ -f "$log" ] && before=$(wc -l < "$log")
    out=$(cd "$WORK" && python3 -I "$repo/sw/firmware/ctrl/test/ctrl_build.py" --stack-pin "$2" 2>&1); rc=$?
    local after=0; [ -f "$log" ] && after=$(wc -l < "$log")
    echo "$1 | $side | exit $rc | recorder runs $((after - before)) | $(echo "$out" | tail -1 | cut -c1-260)"
  done
}
fresh() { rm -rf "$WORK/s"; loose_clone "$WORK/s"; }

fresh; run_both "P0 clean loose clone" "$WORK/s"
fresh; edit "$WORK/s"; run_both "P1 source edited" "$WORK/s"

fresh; S=$WORK/s; edit "$S"; B=$(edited_blob "$S"); SRCT=$(git -C "$S" rev-parse "$PIN:src")
forge "$S" "$SRCT" "$(remade "$S" "$SRCT" adp.c "$B")"; run_both "P2 forged src/ subtree + edit" "$S"

fresh; S=$WORK/s; edit "$S"; B=$(edited_blob "$S"); SRCT=$(git -C "$S" rev-parse "$PIN:src")
ROOT=$(git -C "$S" rev-parse "$PIN^{tree}"); NSRC=$(remade "$S" "$SRCT" adp.c "$B")
forge "$S" "$ROOT" "$(remade "$S" "$ROOT" src "$NSRC")"; run_both "P3 forged root tree + edit" "$S"

fresh; S=$WORK/s; edit "$S"; B=$(edited_blob "$S"); SRCT=$(git -C "$S" rev-parse "$PIN:src")
ROOT=$(git -C "$S" rev-parse "$PIN^{tree}"); NROOT=$(remade "$S" "$ROOT" src "$(remade "$S" "$SRCT" adp.c "$B")")
NC=$(git -C "$S" cat-file commit "$PIN" | sed "1s/^tree .*/tree $NROOT/" | git -C "$S" hash-object -t commit -w --stdin)
forge "$S" "$PIN" "$NC"; run_both "P4 forged pinned commit + edit" "$S"

# a tree two levels down: the first file at depth >= 3 in the pin
fresh; S=$WORK/s; DEEP=$(git -C "$S" ls-tree -r --name-only "$PIN" | awk -F/ 'NF>=3{print; exit}')
if [ -n "$DEEP" ]; then
  printf '\n# probe edit\n' >> "$S/$DEEP"; B=$(git -C "$S" hash-object -w "$S/$DEEP")
  D=$(dirname "$DEEP"); DT=$(git -C "$S" rev-parse "$PIN:$D")
  forge "$S" "$DT" "$(remade "$S" "$DT" "$(basename "$DEEP")" "$B")"; run_both "P5 forged $D/ tree (depth 2) + edit of $DEEP" "$S"
else echo "P5 no file at depth >= 3 in the pin"; fi

fresh; S=$WORK/s; edit "$S"; B=$(edited_blob "$S"); forge "$S" "$(git -C "$S" rev-parse "$PIN:$EDITED")" "$B"
run_both "P6 forged blob + edit" "$S"

# type confusion: the src/ tree's loose file holds a commit whose tree is the forged src/ tree
fresh; S=$WORK/s; edit "$S"; B=$(edited_blob "$S"); SRCT=$(git -C "$S" rev-parse "$PIN:src")
NSRC=$(remade "$S" "$SRCT" adp.c "$B")
TC=$(printf 'tree %s\nauthor a <a> 0 +0000\ncommitter a <a> 0 +0000\n\nx\n' "$NSRC" | git -C "$S" hash-object -t commit -w --stdin)
forge "$S" "$SRCT" "$TC"; run_both "P7 src/ tree's file holds a commit peeling to a forged src/ tree + edit" "$S"

# the forged src/ tree served by an alternate store, the clone's own copy removed
fresh; S=$WORK/s; edit "$S"; B=$(edited_blob "$S"); SRCT=$(git -C "$S" rev-parse "$PIN:src")
NSRC=$(remade "$S" "$SRCT" adp.c "$B"); ALT=$WORK/alt; rm -rf "$ALT"; mkdir -p "$ALT/${SRCT:0:2}"
cp "$(obj "$S" "$NSRC")" "$ALT/${SRCT:0:2}/${SRCT:2}"; rm -f "$(obj "$S" "$SRCT")"; echo "$ALT" > "$S/.git/objects/info/alternates"
run_both "P8 forged src/ tree from an alternate store + edit" "$S"

fresh; S=$WORK/s; SRCT=$(git -C "$S" rev-parse "$PIN:src"); V=$(obj "$S" "$SRCT"); head -c 40 /dev/urandom > "$V.new"; mv -f "$V.new" "$V"
run_both "P9 src/ tree's loose file corrupt (random bytes)" "$S"

fresh; S=$WORK/s; rm -f "$(obj "$S" "$(git -C "$S" rev-parse "$PIN:src")")"; run_both "P10 src/ tree object missing" "$S"

# the repositories' own core.fsmonitor
LOG=$WORK/fsmon.log; REC=$(recorder "$LOG")
fresh; S=$WORK/s; git -C "$S" config core.fsmonitor "$REC"; edit "$S"; run_both "P11 stack config core.fsmonitor + edit" "$S" "$LOG"
fresh; S=$WORK/s; for repo in "$HEAD_REPO" "$OLD_REPO"; do git -C "$repo" config core.fsmonitor "$REC"; done
run_both "P12 superproject config core.fsmonitor (clean stack)" "$S" "$LOG"
for repo in "$HEAD_REPO" "$OLD_REPO"; do git -C "$repo" config --unset core.fsmonitor; done

# the stack's own configuration making it a partial clone whose promisor remote's transport is a program:
# an object of the pin missing, so Git fetches it lazily through core.sshCommand
LOG2=$WORK/lazy.log; REC2=$(recorder "$LOG2")
fresh; S=$WORK/s; rm -f "$(obj "$S" "$(git -C "$S" rev-parse "$PIN:src")")"
git -C "$S" config core.repositoryformatversion 1; git -C "$S" config extensions.partialClone probe
git -C "$S" config remote.probe.url ssh://probe.invalid/x; git -C "$S" config remote.probe.promisor true
git -C "$S" config core.sshCommand "$REC2"
run_both "P13 stack config partial clone, core.sshCommand a recorder, src/ tree missing" "$S" "$LOG2"

# the same, the recorder serving the missing object from an intact store, and leaving a process behind that
# edits the checked source after the proof has decided
LOG3=$WORK/serve.log; SERVE=$WORK/serve.sh
cat > "$SERVE" <<EOF
#!/bin/sh
echo "ran \$*" >> $LOG3
( sleep 2; printf '\n/* edited after the check */\n' >> $WORK/s/$EDITED; echo edited >> $LOG3.edit ) >/dev/null 2>&1 </dev/null &
exec git upload-pack $SRC
EOF
chmod +x "$SERVE"
for side in head old; do
  repo=$HEAD_REPO; [ $side = old ] && repo=$OLD_REPO
  fresh; S=$WORK/s; rm -f "$(obj "$S" "$(git -C "$S" rev-parse "$PIN:src")")" "$LOG3" "$LOG3.edit"
  git -C "$S" config core.repositoryformatversion 1; git -C "$S" config extensions.partialClone probe
  git -C "$S" config remote.probe.url ssh://probe.invalid/x; git -C "$S" config remote.probe.promisor true
  git -C "$S" config core.sshCommand "$SERVE"
  out=$(cd "$WORK" && python3 -I "$repo/sw/firmware/ctrl/test/ctrl_build.py" --stack-pin "$S" 2>&1); rc=$?
  sleep 4
  after=$(cd "$WORK" && python3 -I "$repo/sw/firmware/ctrl/test/ctrl_build.py" --stack-pin "$S" 2>&1 | tail -1 | cut -c1-200)
  echo "P14 partial clone served by a recorder that edits later | $side | exit $rc | recorder runs $(wc -l < "$LOG3" 2>/dev/null || echo 0) | $(echo "$out" | tail -1 | cut -c1-200) | later edit: $(cat "$LOG3.edit" 2>/dev/null || echo none) | proof rerun: $after"
done
git -C "$SRC" status --porcelain | head -3
echo "probes done"
