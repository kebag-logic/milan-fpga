#!/bin/sh
# Scope of the follow-up delta 553edeb8..2accfadf: which paths moved, whether
# any test or other RTL byte moved, and whether the one .sv edit is
# comment-only (preprocessed output and lint output identical).
# Usage: 10_delta_scope.sh <clone> <scratch-dir>   (VERILATOR must be set)
set -eu
clone=$1
scratch=$2
: "${VERILATOR:?set VERILATOR to the pinned 5.050 binary}"
OLD=553edeb86b9144f7b15721255fbe5ad11ef1fe36
NEW=2accfadfd3d4d8a318e3e714ee0dc87fc84e4164
BASE=ede8d48ecd7c7f589a14b957951f040d92c99c70
cd "$clone"
echo "== verilator: $("$VERILATOR" --version)"
echo "== parents: $(git rev-parse "$NEW^") (expect $OLD); $(git rev-parse "$OLD^^") (expect $BASE)"
echo "== raw delta $OLD..$NEW (no renames)"
git diff --raw --no-renames --no-abbrev "$OLD" "$NEW"
echo "== per-subtree tree ids, old vs new"
for p in tb hdl docs scripts syn sw tests; do
  a=$(git rev-parse "$OLD:$p" 2>/dev/null || echo absent)
  b=$(git rev-parse "$NEW:$p" 2>/dev/null || echo absent)
  if [ "$a" = "$b" ]; then s=same; else s=DIFFERENT; fi
  echo "  $p: $s ($a / $b)"
done
echo "== gitlinks old vs new"
git ls-tree -r "$OLD" | awk '$2=="commit"' > "$scratch/gl_old.txt"
git ls-tree -r "$NEW" | awk '$2=="commit"' > "$scratch/gl_new.txt"
if cmp -s "$scratch/gl_old.txt" "$scratch/gl_new.txt"; then echo "  identical"; else echo "  DIFFERENT"; fi
cat "$scratch/gl_new.txt" | sed 's/^/  /'
echo "== hunk headers of the .sv edit"
git diff -U0 "$OLD" "$NEW" -- hdl/ieee1722/crf/KL_media_grid_align.sv | grep '^@@'
echo "== banner span in the new file (/* ... */ delimiters)"
git show "$NEW:hdl/ieee1722/crf/KL_media_grid_align.sv" | grep -n -E '^/\*|^\*/' | sed 's/^/  line /'
echo "== preprocessed (-E -P) identity, old vs new KL_media_grid_align.sv"
mkdir -p "$scratch/pp"
git show "$OLD:hdl/ieee1722/crf/KL_media_grid_align.sv" > "$scratch/pp/old.sv"
git show "$NEW:hdl/ieee1722/crf/KL_media_grid_align.sv" > "$scratch/pp/new.sv"
"$VERILATOR" -E -P "$scratch/pp/old.sv" > "$scratch/pp/old.E"
"$VERILATOR" -E -P "$scratch/pp/new.sv" > "$scratch/pp/new.E"
echo "  source sha256 old: $(sha256sum < "$scratch/pp/old.sv" | cut -d' ' -f1)"
echo "  source sha256 new: $(sha256sum < "$scratch/pp/new.sv" | cut -d' ' -f1)"
echo "  -E -P sha256 old:  $(sha256sum < "$scratch/pp/old.E" | cut -d' ' -f1)"
echo "  -E -P sha256 new:  $(sha256sum < "$scratch/pp/new.E" | cut -d' ' -f1)"
if cmp -s "$scratch/pp/old.E" "$scratch/pp/new.E"; then echo "  preprocessed output: IDENTICAL"; else echo "  preprocessed output: DIFFERENT"; fi
# control: the -E -P comparison can see a real edit (it is not vacuous)
sed 's/LOCK_KEEPOFF_CYC_P) ? KEEP_LO_C/LOCK_KEEPOFF_CYC_P) ? KEEP_HI_C/; s/(tst_next_w < KEEP_LO_C) ? KEEP_LO_C/(tst_next_w < KEEP_LO_C) ? KEEP_HI_C/' "$scratch/pp/new.sv" > "$scratch/pp/ctl.sv"
"$VERILATOR" -E -P "$scratch/pp/ctl.sv" > "$scratch/pp/ctl.E"
if cmp -s "$scratch/pp/ctl.sv" "$scratch/pp/new.sv"; then echo "  control: substitution found nothing (control INVALID)";
elif cmp -s "$scratch/pp/ctl.E" "$scratch/pp/new.E"; then echo "  control: a one-token logic edit is INVISIBLE (comparison vacuous)";
else echo "  control: a one-token logic edit changes -E -P output (comparison sees logic)"; fi
echo "== lint-only warnings, old vs new (module alone, -Wall, same file name, line numbers normalised)"
mkdir -p "$scratch/pp/lint_old" "$scratch/pp/lint_new"
cp "$scratch/pp/old.sv" "$scratch/pp/lint_old/KL_media_grid_align.sv"
cp "$scratch/pp/new.sv" "$scratch/pp/lint_new/KL_media_grid_align.sv"
for v in old new; do
  rc=0
  ( cd "$scratch/pp/lint_$v" && "$VERILATOR" --lint-only -Wall KL_media_grid_align.sv > lint.txt 2>&1 ) || rc=$?
  echo "  $v rc=$rc, $(grep -c '^%' "$scratch/pp/lint_$v/lint.txt" || true) diagnostic lines"
  sed -E 's/:[0-9]+:([0-9]+:)?/:L:/g; s/^ *[0-9]+ \|/ N |/' "$scratch/pp/lint_$v/lint.txt" > "$scratch/pp/lint_$v/lint.norm"
done
if cmp -s "$scratch/pp/lint_old/lint.norm" "$scratch/pp/lint_new/lint.norm"; then
  echo "  lint diagnostics (normalised): IDENTICAL"
else
  echo "  lint diagnostics (normalised): DIFFERENT"; diff "$scratch/pp/lint_old/lint.norm" "$scratch/pp/lint_new/lint.norm" || true
fi
grep '^%' "$scratch/pp/lint_new/lint.txt" | sed -E 's/:[0-9]+:([0-9]+:)?/:L:/g; s/^/  new: /'
