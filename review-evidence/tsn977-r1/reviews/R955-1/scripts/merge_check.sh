#!/bin/bash
# Verify the head merge brings in only main's content. Run inside a clone holding both parents.
set -u
H=5d03517f2ab42416654a8f2be2f71cfc51d82440; B=175cf9e052d5f38d81274436262b08a666447edb; M=c3bff8f3dea03870ea7ae62965db360b509ee3b3; X=a795471c0abc4e38f7e5146b4e539dd607b6f501
echo "head tree $(git rev-parse $H^{tree}) parents $(git rev-parse $H^1) $(git rev-parse $H^2) merge-base $(git merge-base $B $M)"
T=$(git merge-tree --write-tree $B $M | head -1); echo "auto-merge tree $T (conflicts listed by merge-tree, if any):"; git merge-tree --write-tree --name-only $B $M | sed -n '2,20p'
echo "files differing between the automatic merge tree and the head tree:"; git diff --name-only $T $H
echo "main-changed files whose head blob differs from main's:"; for f in $(git diff --name-only $X $M); do [ "$(git rev-parse $M:$f)" = "$(git rev-parse $H:$f)" ] || echo "  $f"; done
echo "branch-changed files whose head blob differs from the branch's:"; for f in $(git diff --name-only $X $B); do [ "$(git rev-parse $B:$f)" = "$(git rev-parse $H:$f)" ] || echo "  $f"; done
echo "files changed by neither side but differing at head from base $X:"; for f in $(git diff --name-only $X $H); do git diff --quiet $X $M -- $f && git diff --quiet $X $B -- $f && echo "  $f"; done
echo "CHANGELOG at head = main's plus the branch line only:"; diff <(git show $M:CHANGELOG.md) <(git show $H:CHANGELOG.md)
git show $B:CHANGELOG.md | grep -c "^- Visit only the marked sinks" 
echo "head CHANGELOG line equals the branch's line:"; diff <(git show $B:CHANGELOG.md | grep "^- Visit only the marked sinks") <(git show $H:CHANGELOG.md | grep "^- Visit only the marked sinks") && echo yes
echo "src/acmp.c head == branch: $( [ "$(git rev-parse $B:src/acmp.c)" = "$(git rev-parse $H:src/acmp.c)" ] && echo yes)"
echo "src/acmp.c main == base: $( [ "$(git rev-parse $M:src/acmp.c)" = "$(git rev-parse $X:src/acmp.c)" ] && echo yes)"
