#!/usr/bin/env bash
# Reviewer-owned reproduction for processor PR #124 round 2 at 11dd3e90
# (round-1 head eb734969, base 870ff88a).
# Usage: run_r2.sh <processor-clone> <packet-dir> <parent-gate-scripts-dir> [<round1-receipts-dir>]
# <parent-gate-scripts-dir> directly holds check_py_idiom.py, code_quality_scope.py,
# py_idiom.budget, measure_test_evidence.py, suite_tally.py and test_evidence.budget
# from kebag-logic/milan-fpga scripts/ at dev 831f94f4.
# The round-1 scripts under scripts/r1 are used byte-unchanged. Disposable trees
# go under <packet-dir>/scratch, receipts under <packet-dir>/receipts. The clone
# is only read (git archive / git clone). The optional fourth argument is the
# published R336-1 receipts directory, for round-1 vs round-2 comparisons.
set -uo pipefail
CLONE=$(cd "$1" && pwd); PKT=$(cd "$2" && pwd); GATES=$(cd "$3" && pwd)
R1REC=${4:+$(cd "$4" && pwd)}
BASE=870ff88ad35bbd532244e4c7e6d7661b9f6e1366
R1=eb734969154d5a75ff84b2779ff6088a2f4311a5
HEAD=11dd3e903685183250e7cd8ecc391b04fe7fd494
S=$PKT/scratch; R=$PKT/receipts; SC=$PKT/scripts; R1S=$SC/r1
mkdir -p "$S" "$R"

# 1. exported trees
for t in base r1 head; do rm -rf "${S:?}/$t"; mkdir -p "$S/$t"; done
git -C "$CLONE" archive $BASE | tar -x -C "$S/base"
git -C "$CLONE" archive $R1 | tar -x -C "$S/r1"
git -C "$CLONE" archive $HEAD | tar -x -C "$S/head"
{ git -C "$CLONE" diff --stat $R1 $HEAD; git -C "$CLONE" diff $R1 $HEAD; } > "$R/delta-r1-head.diff"
git -C "$CLONE" diff --stat $BASE $HEAD > "$R/diffstat-base-head.txt"

# 2. (item 1) round-1 parent scans, unchanged, base vs head and round 1 vs head
{ echo "## base -> head"; python3 -B "$R1S/parent_idiom_scan.py" "$GATES" "$S/base" "$S/head"; echo "rc=$?"
  echo "## round1 -> head"; python3 -B "$R1S/parent_idiom_scan.py" "$GATES" "$S/r1" "$S/head"; echo "rc=$?"; } > "$R/parent-idiom-scan.log" 2>&1
{ echo "## base -> head"; python3 -B "$R1S/parent_wallclock_scan.py" "$GATES" "$S/base" "$S/head"; echo "rc=$?"
  echo "## round1 -> head"; python3 -B "$R1S/parent_wallclock_scan.py" "$GATES" "$S/r1" "$S/head"; echo "rc=$?"; } > "$R/parent-wallclock-scan.log" 2>&1
( cd "$GATES" && sha256sum -- * ) > "$R/parent-gate-scripts.sha256"

# 3. (item 2) the docstring sketch against the rule, round 1 and head
{ python3 -B "$SC/sketch_probe.py" "$S/r1" "$S/head"; echo "rc=$?"
  echo "## head only"; python3 -B "$SC/sketch_probe.py" "$S/head"; echo "rc=$?"; } > "$R/sketch-probe.log" 2>&1

# 4. (item 3) behaviour: AST equivalence, test counts, images, mutants, probes
{ python3 -B "$SC/ast_equiv.py" "$S/r1" "$S/head"; echo "rc=$?"; } > "$R/ast-equiv.log" 2>&1
( cd "$S/head/tb/desc_store" && { python3 -B "$SC/count_cases.py" "$S/head"; echo "rc=$?"; } > "$R/head-count-cases.log" 2>&1
  { python3 -B test_gen_desc_image.py; echo "rc=$?"; } > "$R/head-tests-direct.log" 2>&1
  { make generator-check; echo "rc=$?"; } > "$R/head-generator-check.log" 2>&1 )
rm -rf "$S/base-plus-test"; cp -a "$S/base" "$S/base-plus-test"
cp "$S/head/tb/desc_store/test_gen_desc_image.py" "$S/base-plus-test/tb/desc_store/"
( cd "$S/base-plus-test/tb/desc_store" && { python3 -B test_gen_desc_image.py; echo "rc=$?"; } > "$R/head-tests-vs-base-generator.log" 2>&1 )
for t in base r1 head; do rm -rf "$S/img-$t"; bash "$R1S/images.sh" "$S/$t" "$S/img-$t" > "$R/images-$t.sha256"; done
{ for t in r1 head; do if diff "$R/images-base.sha256" "$R/images-$t.sha256"; then echo "base==$t IDENTICAL"; else echo "base!=$t DIFFERENT"; fi; done
  [ -n "$R1REC" ] && { if diff "$R1REC/images-head.sha256" "$R/images-head.sha256"; then echo "published R336-1 head digests==head IDENTICAL"; else echo "published R336-1 head digests!=head DIFFERENT"; fi; }
  echo "artifacts: $(wc -l < "$R/images-head.sha256")"; } > "$R/images-compare.txt"
mkdir -p "$R/mutants"
python3 -B "$R1S/mutants.py" "$S/head" "$S" "$R/mutants" > "$R/mutants-summary.txt" 2>&1; echo "rc=$?" >> "$R/mutants-summary.txt"
mkdir -p "$S/probe-tmp"
python3 -B "$R1S/probes.py" "$S/base" "$S/head" "$S/probe-tmp" "$R/probes.json" > "$R/probes.log" 2>&1; echo "rc=$?" >> "$R/probes.log"
{ python3 -B "$R1S/legal_models.py" "$S/base" "$S/head"; echo "rc=$?"; } > "$R/legal-models.log" 2>&1
if [ -n "$R1REC" ]; then
  { for pair in mutants-summary.txt:mutants-summary.txt mutants.json:mutants/mutants.json \
                probes.json:probes.json legal-models.log:legal-models.log; do
      a=$R1REC/${pair%%:*}; b=$R/${pair#*:}
      if diff "$a" "$b"; then echo "${pair%%:*}: published round 1 == round 2"; else echo "${pair%%:*}: DIFFERS"; fi; done
  } > "$R/round1-vs-round2.txt" 2>&1
fi

# 5. focused desc_store suite through scripts/run_suites.sh on reduced trees
for t in head mut-M0-remove-check; do
  tag=${t#mut-}; tag=${tag%-remove-check}; rt=$S/rs-$t
  rm -rf "$rt"; cp -a "$S/$t" "$rt"
  for d in "$rt"/tb/*/; do [ -f "$d/Makefile" ] && [ "$(basename "$d")" != desc_store ] && rm -rf "$d"; done
  ( cd "$rt" && { echo "reduced tree: tb/common + tb/desc_store only; verilator: $(command -v verilator) $(verilator --version 2>&1)"
                  ./scripts/run_suites.sh; echo "rc=$?"; } > "$R/run_suites-reduced-$tag.log" 2>&1 )
done

# 6. (item 4) documentation gates and diff hygiene on a scratch clone
rm -rf "$S/gate-clone"; git clone -q --no-hardlinks "$CLONE" "$S/gate-clone"
( cd "$S/gate-clone" && git checkout -q --detach $HEAD && {
    echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
    for c in "make check" "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
             "python3 scripts/check-integrator-params.py" "python3 scripts/render-wavedrom.py --check" \
             "make stale" "python3 scripts/gen_matrix.py --check" "python3 scripts/check_upc_map.py" \
             "git diff --check $BASE $HEAD" "git diff --check $R1 $HEAD"; do
      echo "== $c"; $c; echo "rc=$?"; done; } > "$R/docs-gates.log" 2>&1 )
echo "run_r2 done"
