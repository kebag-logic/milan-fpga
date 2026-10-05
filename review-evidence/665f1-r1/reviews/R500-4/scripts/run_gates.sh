#!/bin/sh
# The focused companion gates run at the review head, concurrently, each with
# its own log and rc file. MDPY is a Python with the pinned Markdown renderer
# (tools/markdown/requirements.txt). Usage: run_gates.sh <clone> <packet> <mdpy>
set -u
CLONE=$1; P=$2; MDPY=$3; R=$P/receipts/gates
export TMPDIR=$P/scratch/tmp
mkdir -p "$R"; cd "$CLONE" || exit 2
g() { n=$1; shift; ( timeout 590 "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
g nvm_hosttest python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
g nvm_capture python3 scripts/check_nvm_capture.py
g nvm_record_space python3 scripts/check_nvm_record_space.py
g nvm_record_space_self python3 scripts/check_nvm_record_space.py --self-test
g cpp_idiom python3 scripts/check_cpp_idiom.py
g py_idiom python3 scripts/check_py_idiom.py
g hygiene python3 scripts/check_hygiene.py
g docs_check python3 scripts/docs_check.py
g doc_style python3 scripts/check_doc_style.py
g doc_paths python3 scripts/check_doc_paths.py
g baremetal python3 scripts/check_baremetal_only.py --check
g diff_check git diff --check fa450d301805881ad713b67521477bf042ddadfd HEAD
g em_dash "$MDPY" scripts/check_em_dash.py --base 28f9666feab2b2ba287643c63ed3a16b1e0bb863
g em_dash_fa45 "$MDPY" scripts/check_em_dash.py --base fa450d301805881ad713b67521477bf042ddadfd
g gen_toc "$MDPY" scripts/gen_toc.py --check
g gen_toc_anchors "$MDPY" scripts/gen_toc.py --verify-anchors
wait
