#!/bin/sh
# Re-run the composition checks of this review on a clone at the candidate.
# Usage: run_checks.sh <clone> <packet-dir> <venv-python-with-tools/markdown/requirements.txt>
# The signed files (manifest.json, manifest.json.sig, allowed_signers) are read from <packet-dir>/receipts/signed.
set -u
C=$1; P=$2; VPY=$3
B=1f29f189279f9fc0132f4918e47342b87d22f33a
R=$P/receipts
cd "$C" || exit 2
test "$(git rev-parse HEAD)" = e377f0dde52fed99de54d9449c48ab22152dcf2e || { echo "wrong head"; exit 2; }
echo "merge-tree $(git merge-tree --write-tree HEAD^1 HEAD^2) candidate-tree $(git rev-parse HEAD^{tree}) head-tree $(git rev-parse HEAD^2^{tree})"
awk '{print $3" "$4}' "$R/signed/allowed_signers" > "${TMPDIR:-/tmp}/r757_k.pub"
ssh-keygen -lf "${TMPDIR:-/tmp}/r757_k.pub"
ssh-keygen -Y verify -f "$R/signed/allowed_signers" -I milan-local-ci -n milan-local-ci \
    -s "$R/signed/manifest.json.sig" < "$R/signed/manifest.json"; echo "verify rc=$?"
run() { n=$1; shift; "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc"; echo "$n rc=$(cat "$R/$n.rc")"; }
run docs_check python3 -I scripts/docs_check.py
run gen_toc_check "$VPY" -I scripts/gen_toc.py --check
run gen_toc_anchors "$VPY" -I scripts/gen_toc.py --verify-anchors
run em_dash "$VPY" -I scripts/check_em_dash.py --base "$B"
run baremetal python3 -I scripts/check_baremetal_only.py --check
run doc_paths python3 -I scripts/check_doc_paths.py
run doc_style python3 -I scripts/check_doc_style.py
run feature_status python3 -I scripts/check_feature_status.py
run solution_docs python3 -I scripts/check_solution_docs.py
run gptp_docs python3 -I scripts/check_gptp_docs.py
run ci_events_check python3 scripts/ci_events.py --check
run ci_gate_workflows python3 scripts/ci_gate_workflows.py --check
run diff_check git diff --check "$B" HEAD
git diff --quiet && git diff --cached --quiet && echo "worktree and index clean"
