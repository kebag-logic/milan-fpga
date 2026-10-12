#!/usr/bin/env bash
# Run the PR's listed repository gates (act_ci.py's self-test runs separately)
# concurrently, each inside sandbox.sh on a fresh git copy of HEAD.
# Usage: run_gates.sh PACKET CLONE HEAD [EXTRA_PATH]
# One log and one rc file per gate under PACKET/receipts/gates/.
set -u
P=$1; CLONE=$2; HEAD=$3; EXTRA=${4:-}
COPY=$P/scratch/gitcopy
rm -rf "$COPY"
git clone -q --no-checkout "$CLONE" "$COPY" && git -C "$COPY" checkout -q --detach "$HEAD" || exit 2
G=$P/receipts/gates; rm -rf "$G"; mkdir -p "$G"
SB=$P/scripts/sandbox.sh
run() { local name=$1; shift; ( SANDBOX_RO="$EXTRA" "$SB" "$COPY" env PATH="${EXTRA:+$EXTRA/bin:}/usr/bin" "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc" ) & }
run ci-events-check python3 scripts/ci_events.py --check
run ci-events-selftest python3 scripts/ci_events.py --selftest
run slot-proof-selftest scripts/act_slot_proof.sh --selftest
run py-idiom python3 scripts/check_py_idiom.py
run py-idiom-selftest python3 scripts/check_py_idiom.py --selftest
run baremetal-check python3 scripts/check_baremetal_only.py --check
run baremetal-selftest python3 scripts/check_baremetal_only.py --selftest
run docs-check python3 scripts/docs_check.py
run doc-style python3 scripts/check_doc_style.py
run toc-check python3 scripts/gen_toc.py --check
run toc-anchors python3 scripts/gen_toc.py --verify-anchors
run em-dash python3 scripts/check_em_dash.py --base dc4d06cb
run doc-paths python3 scripts/check_doc_paths.py
run diff-check git -c safe.directory='*' diff --check dc4d06cb HEAD
wait
for f in "$G"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") | $(tail -1 "${f%.rc}.log" | cut -c1-140)"; done
