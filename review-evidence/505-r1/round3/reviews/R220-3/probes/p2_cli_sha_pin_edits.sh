#!/usr/bin/env bash
# p2 (R220-3): the F3 gap edits and one carrier control, each through the
# real `ci_events.py --check` CLI of the tree under test, on disposable
# `git archive` copies. Usage: p2_cli_sha_pin_edits.sh <clone> <rev> <scratch>
set -uo pipefail
clone=$1 rev=$2 scratch=$3
export PYTHONDONTWRITEBYTECODE=1
fresh() {  # fresh copy of <rev> at $scratch/$1
  rm -rf "$scratch/$1"; mkdir -p "$scratch/$1"
  git -C "$clone" archive "$rev" | tar -x -C "$scratch/$1"
}
run() {  # run --check in copy $1, print exit status and the verdict lines
  (cd "$scratch/$1" && python3 -B scripts/ci_events.py --check) > "$scratch/$1.out" 2>&1
  rc=$?
  echo "[$1] exit=$rc"
  grep -E '^ci_events:|^  FAIL' "$scratch/$1.out" | cut -c1-400
}
echo "rev=$rev"

fresh pristine; run pristine

# E1: delete the checkout-HEAD mismatch block (the `if ... fi` of the pin step)
fresh e1-delete-if-block
python3 -B - "$scratch/e1-delete-if-block/.github/workflows/rtl.yml" <<'EOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
block = ('          if [ "$head" != "$GITHUB_SHA" ]; then\n'
         '            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
         '            exit 1\n'
         '          fi\n')
assert t.count(block) == 1, t.count(block)
open(p, "w", encoding="utf-8").write(t.replace(block, ""))
EOF
git -C "$scratch" diff --no-index --stat pristine/.github/workflows/rtl.yml e1-delete-if-block/.github/workflows/rtl.yml | tail -1
run e1-delete-if-block

# E2: replace that block's `exit 1` with `true`
fresh e2-exit1-true
python3 -B - "$scratch/e2-exit1-true/.github/workflows/rtl.yml" <<'EOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
old = ('            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
       '            exit 1\n')
new = ('            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
       '            true\n')
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
EOF
run e2-exit1-true

# E3: drop the pin step's `target_sha` publication line
fresh e3-drop-target-sha
python3 -B - "$scratch/e3-drop-target-sha/.github/workflows/rtl.yml" <<'EOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
old = '          echo "target_sha=$GITHUB_SHA" >> "$GITHUB_OUTPUT"\n'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, ""))
EOF
run e3-drop-target-sha

# C1 (control): the AC5 edit on a carrier -- `|| true` on the Python idiom call
fresh c1-carrier-or-true
python3 -B - "$scratch/c1-carrier-or-true/.github/workflows/docs.yml" <<'EOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
old = '          python3 scripts/check_py_idiom.py\n'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, '          python3 scripts/check_py_idiom.py || true\n'))
EOF
run c1-carrier-or-true
