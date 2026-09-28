#!/bin/sh
# Disposable probes of the .gitattributes whitespace exemption, in a scratch clone.
# usage: whitespace_probes.sh <path-to-processor-clone> <scratch-dir>
set -u
CLONE=$1; W=$2/wsclone
BASE=16be6768f710e79450aace277abacd6c2c3336e5
HEAD=0404675dcd8788d29cb15a831a8c182438bf1c92
rm -rf "$W"; git clone -q --no-checkout "$CLONE" "$W"; cd "$W"
git -c advice.detachedHead=false checkout -q "$HEAD"
echo "## P0 control: exact head, rc expected 0"
git --no-pager diff --check $BASE HEAD >/dev/null; echo "rc=$?"
echo "## P1 exemption removed from the worktree (attribute absent): rc expected 2"
mv .gitattributes /tmp/.ga.$$; git --no-pager diff --check $BASE HEAD > ../p1.out; echo "rc=$?"
echo "hits: $(grep -c ': trailing whitespace\.$' ../p1.out) trailing-whitespace, $(grep -c 'new blank line at EOF' ../p1.out) blank-at-EOF, files: $(grep -E '^[^+].*:[0-9]+: ' ../p1.out | cut -d: -f1 | sort -u | wc -l), outside mutations/: $(grep -E '^[^+].*:[0-9]+: ' ../p1.out | cut -d: -f1 | grep -vc '^tb/srp_top/mutations/')"
mv /tmp/.ga.$$ .gitattributes
git config user.email probe@invalid; git config user.name probe
echo "## P2 space-before-tab inserted into a mutation patch: still flagged (rc expected 2)"
printf ' \tspace-before-tab\n' >> tb/srp_top/mutations/talker-no-own.patch
git --no-pager diff --check HEAD; echo "rc=$?"; git checkout -q -- tb/srp_top/mutations/talker-no-own.patch
echo "## P3 trailing whitespace in a non-patch file beside the patches: flagged (rc expected 2)"
printf 'x \n' >> tb/srp_top/README.md; git --no-pager diff --check HEAD; echo "rc=$?"; git checkout -q -- tb/srp_top/README.md
echo "## P4 trailing whitespace in a nested .patch below mutations/: flagged (rc expected 2)"
mkdir -p tb/srp_top/mutations/sub; printf 'x \n' > tb/srp_top/mutations/sub/x.patch; git add -N tb/srp_top/mutations/sub/x.patch
git --no-pager diff --check HEAD; echo "rc=$?"; git rm -q --cached tb/srp_top/mutations/sub/x.patch; rm -rf tb/srp_top/mutations/sub
echo "## P5 trailing whitespace on a new mutation-patch line: exempt by design (rc expected 0)"
printf '+added \n' >> tb/srp_top/mutations/talker-no-own.patch; git --no-pager diff --check HEAD; echo "rc=$?"; git checkout -q -- tb/srp_top/mutations/talker-no-own.patch
echo "## P6 git apply --check of every patch against the head hdl tree (outside any repo)"
T=$(mktemp -d "$2/apply.XXXX"); git archive HEAD hdl | tar -x -C "$T"; ok=0; bad=0
for p in tb/srp_top/mutations/*.patch; do
  if (cd "$T" && git apply --check "$W/$p") 2>/dev/null; then ok=$((ok+1)); else bad=$((bad+1)); echo "REJECT $p"; fi
done; echo "apply --check: $ok accepted, $bad rejected"
echo "## P7 git apply --check of every patch at the scratch clone root (in-repo; attribute present)"
ok=0; bad=0
for p in tb/srp_top/mutations/*.patch; do
  if git apply --check --whitespace=nowarn "$p" 2>/dev/null; then ok=$((ok+1)); else bad=$((bad+1)); fi
done; echo "apply --check in repo: $ok accepted, $bad rejected"
echo "## final state"; git status --porcelain; git rev-parse HEAD
rm -rf "$T"
