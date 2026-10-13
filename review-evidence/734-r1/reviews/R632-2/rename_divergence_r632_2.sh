#!/usr/bin/env bash
# [R632] round 2: hosted (GitHub-style merge, rename-aware) vs replay
# (merge-base three-dot) when dev renames a page the PR edits into a
# gate-read path. Usage: rename_divergence_r632_2.sh <shipping> <empty-dir>
set -euo pipefail
ship="$(cd "$1" && pwd)"; r="$2"; g(){ git -c user.name=p -c user.email=p@x.invalid -C "$r" "$@"; }
g init -q; mkdir -p "$r/scripts" "$r/docs/reference"
git -C "$ship" show HEAD:scripts/ci_scope.py > "$r/scripts/ci_scope.py"
printf 'line %s\n' $(seq 1 40) > "$r/docs/page.md"; g add .; g commit -qm R; R=$(g rev-parse HEAD)
g mv docs/page.md docs/reference/REGISTER_MAP.md; g commit -qm "dev rename into a gate-read page"; L=$(g rev-parse HEAD)
g checkout -q --detach $R; sed -i 's/line 20/line twenty/' "$r/docs/page.md"; g commit -qam "PR edits the page"; H=$(g rev-parse HEAD)
M=$(g commit-tree "$(g merge-tree --write-tree $L $H | head -1)" -p $L -p $H -m merge)
hosted=$(g diff --no-renames --name-only $M^1 $M); replay=$(g diff --no-renames --name-only "$(g merge-base --all $L $H)" $H)
echo "hosted files: $hosted -> rtl=$(cd "$r" && echo "$hosted" | python3 scripts/ci_scope.py)"
echo "replay files: $replay -> rtl=$(cd "$r" && echo "$replay" | python3 scripts/ci_scope.py)"
