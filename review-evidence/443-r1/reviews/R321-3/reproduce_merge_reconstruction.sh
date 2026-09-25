#!/usr/bin/env bash
# Recompute the #443 composition candidate from real dev and compare trees.
# Usage: reproduce_merge_reconstruction.sh <clone>
# Needs Git >= 2.38 (merge-tree --write-tree). Writes only a loose commit
# object for the intermediate probe; no ref, index or worktree change.
set -u
cd "${1:?clone}" || exit 2
DEV=864b36f5e9450ef64f75ca3f0d68c44330e447d7     # real dev after #508
C508=b1b334725dcf12e084eaa3bb96b1e6865c052267    # train candidate for #508
C541=ec9cf454bf997fab230d0216dc609e737bc47caa    # train candidate for #541
H541=fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c    # #541 source head
SRC=b3458db0db5a7c8b15582d80b492620f05f62e70     # #443 reviewed source head
CAND=4ee96a61bf35402a6f88e1ebad1167e9873721c5    # composition candidate
tree() { git rev-parse "$1^{tree}"; }
echo "git $(git --version)"
echo "dev $DEV tree $(tree $DEV); C508 tree $(tree $C508): $([ "$(tree $DEV)" = "$(tree $C508)" ] && echo EQUAL || echo DIFFERENT)"
echo "candidate parents: $(git rev-parse $CAND^1) $(git rev-parse $CAND^2)"
echo "merge-base --all C541 SRC: $(git merge-base --all $C541 $SRC | tr '\n' ' ')"
T1=$(git merge-tree --write-tree "$DEV" "$H541"); rc1=$?
echo "step1 merge-tree dev+#541 head rc=$rc1 tree=$T1 equals C541 tree: $([ "$T1" = "$(tree $C541)" ] && echo YES || echo NO)"
P=$(git commit-tree "$T1" -p "$DEV" -p "$H541" -m probe)
T2=$(git merge-tree --write-tree "$P" "$SRC"); rc2=$?
echo "step2 merge-tree (dev+#541)+#443 source rc=$rc2 tree=$T2 merge-base $(git merge-base --all $P $SRC | tr '\n' ' ')"
echo "step2 equals candidate tree $(tree $CAND): $([ "$T2" = "$(tree $CAND)" ] && echo YES || echo NO)"
T3=$(git merge-tree --write-tree "$C541" "$SRC"); rc3=$?
echo "direct merge-tree C541+source rc=$rc3 tree=$T3 equals candidate: $([ "$T3" = "$(tree $CAND)" ] && echo YES || echo NO)"
echo "--- per-file origin of every path #443 changes (dev..source)"
for f in $(git diff --name-only "$DEV" "$SRC"); do
  c=$(git rev-parse "$CAND:$f"); s=$(git rev-parse "$SRC:$f"); p=$(git rev-parse -q --verify "$C541:$f" 2>/dev/null || echo absent)
  if [ "$c" = "$s" ]; then st="==source"; elif [ "$c" = "$p" ]; then st="==C541"; else st="COMBINED"; fi
  echo "$st $f"
done
echo "--- paths the #541 side changes (dev..C541)"
git diff --name-only "$DEV" "$C541"
echo "--- overlap"
comm -12 <(git diff --name-only "$DEV" "$C541" | sort) <(git diff --name-only "$DEV" "$SRC" | sort)
echo "--- candidate vs reviewed source: every differing path"
git diff --name-only "$SRC" "$CAND"
echo "--- KL_crf_rx.sv from 'module' to EOF, source vs candidate"
diff <(git show "$SRC:hdl/ieee1722/crf/KL_crf_rx.sv" | sed -n '/^module/,$p') \
     <(git show "$CAND:hdl/ieee1722/crf/KL_crf_rx.sv" | sed -n '/^module/,$p') \
  && echo "IDENTICAL (the differing lines sit in the file-header block comment)"
echo "--- submodule gitlinks: candidate / C541 / source"
for r in "$CAND" "$C541" "$SRC"; do git ls-tree "$r" external gptp-processor protocol-processor third_party/verilog-axis | awk '{print $3, $4}' | tr '\n' ' '; echo; done
