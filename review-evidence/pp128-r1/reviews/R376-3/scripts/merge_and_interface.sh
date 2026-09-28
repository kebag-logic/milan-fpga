#!/usr/bin/env bash
# Read-only git checks for R376-3: merge composition, comment-only talker delta,
# talker interface identity. Uses git show/diff/merge-tree only (no checkout
# writes; merge-tree writes objects, never refs or the worktree).
# Usage: merge_and_interface.sh <clone> <head> <main-parent> <branch-parent> <round2-head> <branch-base>
set -euo pipefail
cd "$1"; head=$2 main=$3 br=$4 r2=$5 base=$6
t=hdl/acmp/KL_acmp_talker.sv
strip() { git show "$1:$t" | python3 -c '
import re,sys; s=sys.stdin.read(); s=re.sub(r"/\*.*?\*/","",s,flags=re.S); s=re.sub(r"//[^\n]*","",s)
print("\n".join(l.rstrip() for l in s.splitlines() if l.strip()))'; }
echo "HEAD^1 $(git rev-parse "$head^1")  HEAD^2 $(git rev-parse "$head^2")"
echo "overlap($base..$br, $base..$main): $(comm -12 <(git diff --name-only "$base" "$br" | sort) <(git diff --name-only "$base" "$main" | sort) | wc -l)"
echo "merge-tree $(git merge-tree --write-tree "$br" "$main")  head tree $(git rev-parse "$head^{tree}")"
diff <(strip "$r2") <(strip "$br") >/dev/null && echo "talker $r2..$br comment-only: yes"
hdr() { strip "$1" | awk '/^module KL_acmp_talker/{f=1} f{print} /\);/{if(f&&++n==2)exit}'; }
cmp <(hdr "$main") <(hdr "$head") && echo "talker header (parameters, ports, first declarations) identical $main vs $head: yes"
echo "hdl/ changed $main..$head: $(git diff --name-only "$main" "$head" -- hdl | tr '\n' ' ')"
