#!/usr/bin/env bash
# Composition facts for a merge-train candidate: the shared files, the merge
# reproduction, the differences against each parent, the ledger arithmetic in
# the shared Mark II documents, and the clone's integrity.
# Usage: composition_check.sh <candidate-clone> <script-dir>
set -u
clone="$1"; here="$2"
dev=ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5
src=ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937
cd "$clone" || exit 2
git() { command git "$@" 2>/dev/null; }
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
echo "parents $(git rev-parse HEAD^1) $(git rev-parse HEAD^2)"
mb=$(git merge-base "$dev" "$src"); echo "merge-base $mb"
echo "merge-tree $(git merge-tree --write-tree "$dev" "$src" | head -1)"
echo "== files both lanes change since the merge base"
comm -12 <(git diff --name-only "$mb" "$dev" | sort) <(git diff --name-only "$mb" "$src" | sort)
echo "== candidate vs dev minus PR file set (empty = exact)"
comm -3 <(git diff --name-only "$dev" HEAD | sort) <(git diff --name-only "$mb" "$src" | sort)
echo "== candidate vs PR head minus dev file set (empty = exact)"
comm -3 <(git diff --name-only "$src" HEAD | sort) <(git diff --name-only "$mb" "$dev" | sort)
echo "== hdl/ and tb/ paths differing between candidate and PR head"
git diff --name-only "$src" HEAD -- hdl tb
echo "== M6 port/parameter lines changed in the datapath and shadow"
git diff "$mb" "$src" -- hdl/milan/milan_datapath.sv hdl/milan/KL_pp_shadow.sv | grep -E '^[-+]' | grep -ciE '^\S\s*(input|output|inout|parameter)\b'
echo "== suite texts in docs/testing/TESTING.md"
grep -n 'test_retained_cdc_storage.py` (#640 lane M2)' docs/testing/TESTING.md | cut -c1-80
grep -n '#640 M6 lockstep leg' docs/testing/TESTING.md | cut -c1-80
echo "== ledger arithmetic"
python3 -I "$here/ledger_arith.py" docs/design/MARK_II_AREA_PLAN.md docs/design/AREA_BUDGET.md
echo "== integrity"
echo "status-lines $(command git status --porcelain --untracked-files=all | wc -l)"
command git diff-index --quiet HEAD; echo "diff-index rc $?"
command git diff --quiet; echo "worktree-vs-index rc $?"
git ls-tree HEAD | grep ' commit '
command git submodule status 2>/dev/null
