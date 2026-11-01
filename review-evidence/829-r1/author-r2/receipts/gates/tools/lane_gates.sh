#!/usr/bin/env bash
# The rtl-fast and suite gates this change touches, one log and one rc per gate, never piped, on a clean clone of the head.
set -u
H=$1; S=$VALIDATION_STORAGE/829-a725c; W=$S/gates/lane-wt; O=$MANAGEMENT/2026-09-23/829-a725c/receipts/gates/lane; G=$S/gates/lane-logs
mkdir -p "$O" "$G"
[ -d "$W" ] || $S/tools/clone_at.sh "$H" "$W"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
BASE=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j4 --no-print-directory" CI_CAMPAIGN_JOBS=4 PYTHONHASHSEED=0
LITEX=$WORKSPACE_HOME/litex-milan/venv/bin/python3
DOCS=$VALIDATION_STORAGE/sync-a723b/venv-docs/bin
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
P=$BASE
run diffcheck "git diff --check 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD"
run lint_rtl "python3 scripts/lint_rtl.py --check --self-test --jobs 4"
run pp_srcs "python3 scripts/pp_srcs.py --check --selftest"
run gen_chain_pinned "MILAN_LITEX_PYTHON=$LITEX $LITEX sw/litex/gen_mac_tx_model.py --check"
run gptp_tx_timestamp "$LITEX sw/litex/test_gptp_tx_timestamp.py"
run gptp_shadow "make -C tb/verilator/gptp_shadow"
run gptp_plane "make -C tb/verilator/gptp_plane"
run milan_dp_gptp "make -C tb/verilator/milan_dp gptp"
run milan_dp_gptp_lat "make -C tb/verilator/milan_dp gptp-lat"
P=$DOCS:$BASE
run behave "cd tests && behave --no-capture -f plain"
run mdvenv_docs "$VALIDATION_STORAGE/818-mdvenv/bin/python3 scripts/docs_check.py"
run mdvenv_style "$VALIDATION_STORAGE/818-mdvenv/bin/python3 scripts/check_doc_style.py"
run mdvenv_toc "$VALIDATION_STORAGE/818-mdvenv/bin/python3 scripts/gen_toc.py --selftest && $VALIDATION_STORAGE/818-mdvenv/bin/python3 scripts/gen_toc.py --verify-anchors && $VALIDATION_STORAGE/818-mdvenv/bin/python3 scripts/gen_toc.py --check"
run builder_leg0_litex "python3 scripts/ci_builder_legs.py run 0 --receipt $G/builder-leg0-litex.json -- python3 sw/builder/test_builder.py --require-rv32"
run builder_leg1_litex "python3 scripts/ci_builder_legs.py run 1 --receipt $G/builder-leg1-litex.json -- python3 sw/builder/test_builder.py --require-rv32"
git status --short > "$G/tree-after.txt"
echo done > "$G/DONE"
