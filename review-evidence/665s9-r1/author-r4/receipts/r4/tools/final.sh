#!/usr/bin/env bash
# final.sh <head> <group>: one group of round 4's delta gates on its own clean clone of <head>; each gate's log is
# gates/<name>.log ending in rc=N. groups: builder (test_builder --require-rv32, then git diff --check against the
# merge base), mbx (make, then the full mutant campaign), docs (every docs.yml job, then the verifier)
set -uo pipefail
H=$1; GRP=$2; S=<scratch>; G=$S/gates
source $S/tools/env.sh
mkdir -p "$G"
fresh() { rm -rf "$S/clones/$1"; mkdir -p $S/clones; bash $S/tools/clone.sh "$S/clones/$1" "$H" > "$G/$1-clone.log" 2>&1 || { echo "rc=99 clone" >> "$G/$1-clone.log"; exit 99; }; }
gate() { local name=$1 dir=$2; shift 2; (cd "$dir" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")" >> "$G/progress.txt"; }
case $GRP in
  builder)
    fresh builder
    PATH=$LITEX:$SDK:$PATH gate test-builder "$S/clones/builder" python3 sw/builder/test_builder.py --require-rv32
    gate builder-tree-after "$S/clones/builder" git status --porcelain
    gate diff-check "$S/clones/builder" git diff --check 1d6bf5556a "$H" ;;
  mbx)
    fresh mbx
    gate mbx-make "$S/clones/mbx/tb/verilator/mbx" make VBUILD_JOBS=16
    VBUILD_JOBS=4 gate mbx-mutants "$S/clones/mbx/tb/verilator/mbx" python3 -B mutants.py --jobs 8
    gate mbx-tree-after "$S/clones/mbx" git status --porcelain ;;
  docs)
    rm -rf "$S/docsyml-root"
    for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
      /usr/bin/python3 -I $S/tools/docsyml/run_docs_yml.py "$H" $job "$S/docsyml-root" >> "$G/docsyml-run.log" 2>&1
      echo "$(date +%T) docs $job rc=$?" >> "$G/progress.txt"
    done
    /usr/bin/python3 -I $S/tools/docsyml/verify_docs_yml.py "$H" "$S/docsyml-root" > "$G/docsyml-verify.log" 2>&1
    echo "rc=$?" >> "$G/docsyml-verify.log"; echo "$(date +%T) docs-verify $(tail -n1 $G/docsyml-verify.log)" >> "$G/progress.txt" ;;
esac
echo "$(date +%T) group $GRP DONE" >> "$G/progress.txt"
