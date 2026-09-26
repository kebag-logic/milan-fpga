#!/usr/bin/env bash
# Reviewer-owned reproduction for processor PR #124 at eb734969 (base 870ff88a).
# Usage: run_all.sh <processor-clone> <packet-dir> [<parent-gate-scripts-dir>]
# Writes disposable trees under <packet-dir>/scratch and receipts under
# <packet-dir>/receipts. The clone is only read (git archive / git clone).
# Needs python3, make, git, and a Verilator for the one desc_store suite run.
set -uo pipefail
CLONE=$(cd "$1" && pwd); PKT=$(cd "$2" && pwd)
BASE=870ff88ad35bbd532244e4c7e6d7661b9f6e1366
HEAD=eb734969154d5a75ff84b2779ff6088a2f4311a5
S=$PKT/scratch; R=$PKT/receipts; SC=$PKT/scripts
mkdir -p "$S" "$R"

# 1. exported trees
for t in base head; do rm -rf "$S/$t"; mkdir -p "$S/$t"; done
git -C "$CLONE" archive $BASE | tar -x -C "$S/base"
git -C "$CLONE" archive $HEAD | tar -x -C "$S/head"

# 2. every image the repository builds, at base and head
for t in base head; do rm -rf "$S/img-$t"; "$SC/images.sh" "$S/$t" "$S/img-$t" > "$R/images-$t.sha256"; done
if diff "$R/images-base.sha256" "$R/images-head.sha256"; then echo IDENTICAL; else echo DIFFERENT; fi > "$R/images-compare.txt"

# 3. the new tests at head, directly and through the Makefile target
( cd "$S/head/tb/desc_store" && { python3 -B test_gen_desc_image.py; echo "rc=$?"; } > "$R/head-tests-direct.log" 2>&1
  { make generator-check; echo "rc=$?"; } > "$R/head-generator-check.log" 2>&1 )

# 4. the head tests against the base generator (no check): refusals must fail
rm -rf "$S/base-plus-test"; cp -a "$S/base" "$S/base-plus-test"
cp "$S/head/tb/desc_store/test_gen_desc_image.py" "$S/base-plus-test/tb/desc_store/"
( cd "$S/base-plus-test/tb/desc_store" && { python3 -B test_gen_desc_image.py; echo "rc=$?"; } > "$R/head-tests-vs-base-generator.log" 2>&1 )

# 5. mutants (author's removal plus reviewer mutants)
python3 -B "$SC/mutants.py" "$S/head" "$S" "$R" > "$R/mutants-summary.txt" 2>&1; echo "rc=$?" >> "$R/mutants-summary.txt"

# 6. scripts/run_suites.sh on reduced trees (tb/common + tb/desc_store only)
for t in head mut-M0-remove-check; do
  tag=${t#mut-}; tag=${tag%-remove-check}; rt=$S/rs-$t
  rm -rf "$rt"; cp -a "$S/$t" "$rt"
  for d in "$rt"/tb/*/; do [ -f "$d/Makefile" ] && [ "$(basename "$d")" != desc_store ] && rm -rf "$d"; done
  ( cd "$rt" && { echo "reduced tree: tb/common + tb/desc_store only; verilator: $(verilator --version 2>&1)"
                  ./scripts/run_suites.sh; echo "rc=$?"; } > "$R/run_suites-reduced-$tag.log" 2>&1 )
done

# 7. bypass probes and the new test's legal models, base vs head
mkdir -p "$S/probe-tmp"
python3 -B "$SC/probes.py" "$S/base" "$S/head" "$S/probe-tmp" "$R/probes.json" > "$R/probes.log" 2>&1; echo "rc=$?" >> "$R/probes.log"
{ python3 -B "$SC/legal_models.py" "$S/base" "$S/head"; echo "rc=$?"; } > "$R/legal-models.log" 2>&1

# 8. documentation gates (CI docs-gates job + make check) and diff hygiene on a scratch clone
rm -rf "$S/gate-clone"; git clone -q --no-hardlinks "$CLONE" "$S/gate-clone"
( cd "$S/gate-clone" && git checkout -q --detach $HEAD && {
    echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
    for c in "make check" "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
             "python3 scripts/check-integrator-params.py" "python3 scripts/render-wavedrom.py --check" \
             "make stale" "python3 scripts/gen_matrix.py --check" "python3 scripts/check_upc_map.py" \
             "git diff --check $BASE $HEAD"; do
      echo "== $c"; $c; echo "rc=$?"; done; } > "$R/docs-gates.log" 2>&1 )

# 9. the review clone is still at exact head bytes
( cd "$CLONE" && {
  echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}') index-tree $(git write-tree)"
  git diff --quiet HEAD && echo "worktree==HEAD"; git diff --cached --quiet && echo "index==HEAD"
  echo "untracked/ignored entries: $(git status --porcelain --ignored | wc -l)"
  echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l); .gitmodules: $(test -f .gitmodules && echo present || echo absent)"
  diff <(git ls-files -s | awk '{print $1,$2,$4}') <(git ls-tree -r HEAD | awk '{print $1,$3,$4}') && echo "index blobs+modes == HEAD tree"
  diff <(git ls-tree -r HEAD | awk '{print $3,$4}') <(git ls-files -z | xargs -0 git hash-object -- | paste -d' ' - <(git ls-files)) \
    && echo "worktree blob bytes == HEAD tree"; } > "$R/clone-integrity.txt" 2>&1 )
# 10. parent consumer gates' per-file detectors (optional third argument: a
# directory holding check_py_idiom.py, code_quality_scope.py, py_idiom.budget,
# measure_test_evidence.py, suite_tally.py and test_evidence.budget fetched
# from kebag-logic/milan-fpga at dev 831f94f4 under scripts/)
if [ $# -ge 3 ]; then
  GATES=$(cd "$3" && pwd)
  { python3 -B "$SC/parent_idiom_scan.py" "$GATES" "$S/base" "$S/head"; echo "rc=$?"; } > "$R/parent-idiom-scan.log" 2>&1
  { python3 -B "$SC/parent_wallclock_scan.py" "$GATES" "$S/base" "$S/head"; echo "rc=$?"; } > "$R/parent-wallclock-scan.log" 2>&1
fi
echo "run_all done"
