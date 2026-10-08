#!/usr/bin/env bash
# Composition gate-bite probes on a disposable clone of the candidate.
#   probes.sh <probe-clone> <docs-python> <litex-python> <outdir>
# Each probe: confirm the gate is green on exact head bytes, plant one defect
# in the composed file, require the gate to go red, then restore the bytes and
# require them to equal the candidate blob again.
set -u
CLONE=$1 DPY=$2 LPY=$3 OUT=$4
HERE=$(dirname "$(realpath "$0")")
HEAD_OID=b959830acd53a868febfe362974e33e144481aa7
DEV=99e4eb6c14462aafa84bb1ac597fd241abc1a240
mkdir -p "$OUT"
cd "$CLONE" || exit 2
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
fail=0

gate() { "$@" >>"$LOG" 2>&1; echo $?; }

probe() {  # name file python-edit-expression gate-command...
    local name=$1 file=$2 edit=$3; shift 3
    LOG="$OUT/probe_$name.log"; : >"$LOG"
    local blob; blob=$(git rev-parse "HEAD:$file")
    echo "## clean run" >>"$LOG"; local clean; clean=$(gate "$@")
    "$DPY" -I -c "import sys,pathlib; p=pathlib.Path(sys.argv[1]); t=p.read_text(); n=$edit; assert n!=t, 'edit did not apply'; p.write_text(n)" "$file" >>"$LOG" 2>&1 \
        || { echo "$name: EDIT FAILED"; fail=1; return; }
    git diff --stat -- "$file" >>"$LOG" 2>&1
    # A gate that diffs a base against HEAD sees only committed bytes, so the
    # plant is committed locally in this disposable clone and dropped after.
    [ "${COMMIT_PLANT:-0}" = 1 ] && git -c user.name=probe -c user.email=probe@invalid \
        commit -q --no-verify -m probe -- "$file" >>"$LOG" 2>&1
    echo "## planted run" >>"$LOG"; local planted; planted=$(gate "$@")
    git checkout -q --detach "$HEAD_OID" 2>/dev/null; git checkout -q -- "$file"
    [ "$(git rev-parse HEAD)" = "$HEAD_OID" ] || { echo "$name: HEAD NOT RESTORED"; fail=1; }
    local after; after=$(git hash-object "$file")
    local verdict=KILLED
    [ "$clean" = 0 ] && [ "$planted" != 0 ] && [ "$after" = "$blob" ] || { verdict=SURVIVED; fail=1; }
    echo "$name: clean_rc=$clean planted_rc=$planted restored=$([ "$after" = "$blob" ] && echo yes || echo NO) $verdict" | tee -a "$LOG"
}

B=docs/integration/BUILDING.md
# P1: an em dash added inside the PR's merged option table is judged against the dev parent.
COMMIT_PLANT=1 probe em_dash_pr_region $B "t.replace('Refused: the recipe does not enable', 'Refused — the recipe does not enable', 1)" \
    "$DPY" scripts/check_em_dash.py --base $DEV
# P2: an em dash added inside the predecessor's merged GMII region is judged too.
COMMIT_PLANT=1 probe em_dash_dev_region $B "t.replace('Sampled reset masks the captured', 'Sampled reset — masks the captured', 1)" \
    "$DPY" scripts/check_em_dash.py --base $DEV
# P3: the solution CPU-contract block on the composed page is read by its checker.
probe solution_cpu_block $B "t.replace('| \`deploy.sh\` | \`vexiiriscv\` | \`1\` | \`32\` | \`baremetal\` | \`0\` |', '| \`deploy.sh\` | \`vexiiriscv\` | \`1\` | \`32\` | \`baremetal\` | \`8192\` |', 1)" \
    "$DPY" scripts/check_solution_docs.py
# P4: a Contents entry that no longer matches the composed page's headings.
probe toc_contents $B "t.replace('## 2. The named configurations\n', '## 2. The named build configurations\n', 1)" \
    "$DPY" scripts/gen_toc.py --check
# P5: the refusal bank still bites at the candidate with the predecessor's patched LiteX.
probe vexii_fpu_refusal sw/litex/milan_soc.py "t.replace('        if with_fpu:\n            raise ValueError(\"--with-fpu is unsupported', '        if False:\n            raise ValueError(\"--with-fpu is unsupported', 1)" \
    "$LPY" sw/builder/test_soc_options.py
# P6: the predecessor's patch-series inventory is what gate 23h reconciles: drop 0007 from apply.sh.
probe apply_series_0007 sw/litex/patches/apply.sh "t.replace('    \"liteeth 0007-liteeth-gmii-rx-capture.patch\"\n', '', 1)" \
    "$LPY" -I "$HERE/builder_subset.py"
exit $fail
