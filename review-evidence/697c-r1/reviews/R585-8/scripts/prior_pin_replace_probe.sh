#!/bin/sh
# usage: pin_replace_probe.sh <milan-fpga checkout> <stack source repo> <work dir>
# Does ctrl_build.stack_pin accept a stack worktree holding ANOTHER revision's files when a refs/replace
# entry maps the pinned commit to that revision? Uses only a replace ref to an existing commit (ae982af,
# whose src/ bytes differ from the pin); no new commit is created. CONTRIBUTING's xvlog pin proof (#236)
# refuses this class by setting GIT_NO_REPLACE_OBJECTS=1; ctrl_reuse.py does too.
set -u
R=$1; SRC=$2; W=$3
PIN=$(git -C "$R" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
OTHER=$(git -C "$SRC" rev-parse ae982af)
rm -rf "$W"; git clone -q --no-checkout "$SRC" "$W/stack" && git -C "$W/stack" checkout -q --detach "$PIN"
check() { python3 -B -c "
import sys; sys.path[:0]=['$R/sw/firmware/ctrl/test','$R/sw/firmware/gtest']
from pathlib import Path; import ctrl_build
try: print('ACCEPTED: tsn-c-stack at', ctrl_build.stack_pin(Path('$W/stack'), '$PIN'))
except ctrl_build.Refusal as e: print('REFUSED:', e)"; }
echo "pin $PIN; substitute $OTHER"
echo "1. clean clone at the pin:"; check
P="src include tests examples scripts cmake CMakeLists.txt"
HAVE=$(for p in $P; do git -C "$W/stack" cat-file -e "$OTHER:$p" 2>/dev/null && echo $p; done)
( cd "$W/stack" && rm -rf $P && git archive "$OTHER" -- $HAVE | tar -x )
echo "2. worktree holds $OTHER's files under the proven paths, HEAD still the pin, no replace ref:"; check
git -C "$W/stack" replace "$PIN" "$OTHER"
echo "3. same worktree, refs/replace/$PIN -> $OTHER:"; check
echo "   HEAD reads: $(git -C "$W/stack" rev-parse HEAD); git status --short | wc -l: $(git -C "$W/stack" status --short | wc -l)"
echo "   src/adp.c on disk equals the pin's blob: $( [ "$(git -C "$W/stack" hash-object src/adp.c)" = "$(GIT_NO_REPLACE_OBJECTS=1 git -C "$W/stack" rev-parse "$PIN:src/adp.c")" ] && echo yes || echo no)"
echo "4. same, with GIT_NO_REPLACE_OBJECTS=1 in the environment (the repository's own pattern):"; GIT_NO_REPLACE_OBJECTS=1 check
