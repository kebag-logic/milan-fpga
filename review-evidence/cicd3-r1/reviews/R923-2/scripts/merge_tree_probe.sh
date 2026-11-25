#!/bin/sh
# usage: merge_tree_probe.sh GITDIR   (a clone holding the six commits below, e.g. fetched by SHA)
# Classifies every path that differs between the two hosted merge trees: the PR's own delta
# (45d5c35a..9c625393) or the base's (2509db68..e608f8d8); anything else is printed as UNEXPLAINED.
set -u
g() { git -C "$1" "$@"; }
G=$1
m1=dd5cf5798833575a051a7dccf4e248ba290702a7; m2=241f036e9e93c6cb84acca8bf9c78beefa8b1e94
for c in $m1 $m2; do git -C "$G" log -1 --format="$c tree %T parents %P" $c; done
git -C "$G" diff --name-only "$m1^{tree}" "$m2^{tree}" | sort > /tmp/mt.$$; git -C "$G" diff --name-only 45d5c35a 9c62539365 | sort > /tmp/pr.$$
git -C "$G" diff --name-only 2509db68 e608f8d8 | sort > /tmp/base.$$
echo "paths differing between merge trees: $(wc -l < /tmp/mt.$$)"; echo "of them in the PR delta: $(comm -12 /tmp/mt.$$ /tmp/pr.$$ | wc -l)"
echo "of them in the base delta: $(comm -12 /tmp/mt.$$ /tmp/base.$$ | wc -l)"; echo "in both: $(comm -12 /tmp/pr.$$ /tmp/base.$$ | tr '\n' ' ')"
echo "UNEXPLAINED: $(comm -23 /tmp/mt.$$ "$(sort -u /tmp/pr.$$ /tmp/base.$$ > /tmp/u.$$; echo /tmp/u.$$)" | tr '\n' ' ')"
echo "PR delta paths:"; sed 's/^/  /' /tmp/pr.$$
git -C "$G" diff 2509db68 e608f8d8 -- gptp-processor | grep Subproject
rm -f /tmp/mt.$$ /tmp/pr.$$ /tmp/base.$$ /tmp/u.$$
