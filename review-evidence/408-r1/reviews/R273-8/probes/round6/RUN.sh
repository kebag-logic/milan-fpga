#!/usr/bin/env bash
# R273-8 command record (run in the foreground, in this order). The probes
# and cases of round five (R273-7) are reused byte for byte
# (receipts/probes-unchanged-vs-r273-7.txt); only this file, delta_probe.py,
# empty_comment_check.py, closure_on_guard.py and cases/round6/ are new.
# Variables:
#   PKT   this packet            REPO  a clean clone at 062e89ad
#   PREV  the round-five packet's receipts directory (comparison baseline)
#   SDK   a verified pinned SDK (scripts/ci_rv32_sdk.py --destination $SDK --archive <pinned archive>)
#   TOOLS the directory holding the pinned Verilator 5.050
set -eu
: "${PKT:?}" "${REPO:?}" "${PREV:?}" "${SDK:?}" "${TOOLS:?}"
G=$SDK/bin/riscv32-linux-gcc
DEV=759da623072358afdb0e9d570a7b4b6a788492c9
PARENT=991d59653ff82ccf73ef4df9477de1df8c8c5964
export PATH=$TOOLS:$PATH R273_TOOL_BIN=$TOOLS R273_LANE=$REPO
cd "$PKT/scratch"
# 1. gate 1b, both modes, concurrently (from $REPO)
( cd "$REPO" && python3 -B sw/builder/test_firmware_compiler.py --sdk-destination "$SDK" --require-rv32 --audit "$PKT/scratch/head-sdk.audit.jsonl" > "$PKT/scratch/head-sdk.log" 2>&1 ) &
( cd "$REPO" && python3 -B sw/builder/test_firmware_compiler.py --absent --audit "$PKT/scratch/head-absent.audit.jsonl" > "$PKT/scratch/head-absent.log" 2>&1 ) &
wait
# 2. round-four and round-five case probes, unchanged, both modes, then per-case verdict/pin comparison
bash "$PKT/probes/run_probes.sh" "$PKT" "$REPO" "$SDK" r1-head-sdk:head:sdk:round1/all_head.json r1-head-absent:head:absent:round1/all_head.json \
  r2-head-sdk:head:sdk:r2-cases.json r2-head-absent:head:absent:r2-cases.json bom-head-sdk:head:sdk:bom.json bom-head-absent:head:absent:bom.json \
  extra-head-sdk:head:sdk:extra.json extra-head-absent:head:absent:extra.json
bash "$PKT/probes/run_probes.sh" "$PKT" "$REPO" "$SDK" grader-head-sdk:head:sdk:round1/grader.json grader-head-absent:head:absent:round1/grader.json \
  hi-head-sdk:head:sdk:hi.json hi-head-absent:head:absent:hi.json md-head-sdk:head:sdk:md.json md-head-absent:head:absent:md.json \
  published-head-sdk:head:sdk:published.json published-head-absent:head:absent:published.json
bash "$PKT/probes/run_probes.sh" "$PKT" "$REPO" "$SDK" unread-head-sdk:head:sdk:unread.json unread-head-absent:head:absent:unread.json \
  v272-head-sdk:head:sdk:round1/verify_r272.json v272-head-absent:head:absent:round1/verify_r272.json \
  nulldir-head-sdk:head:sdk:round5/null-directive.json nulldir-head-absent:head:absent:round5/null-directive.json \
  nulldir-dev-sdk:$DEV:sdk:round5/null-directive.json nulldir-dev-absent:$DEV:absent:round5/null-directive.json
python3 "$PKT/probes/round5/compare_pins.py" "$PREV/probes" "$PKT/receipts/probes" r1 r2 bom extra grader hi md published unread v272 nulldir > "$PKT/receipts/probes-vs-round5.txt"
# 3. standalone probes, unchanged
python3 -B "$PKT/probes/subset_probe.py" "$REPO" "$G" "$PKT/receipts/subset-probe-identifiers.jsonl" > "$PKT/receipts/subset-probe.log" 2>&1
python3 -B "$PKT/probes/boundary_probe.py" "$REPO" "$G" "$PKT/receipts/boundary-probe.jsonl" > "$PKT/receipts/boundary-probe.log" 2>&1
python3 -B "$PKT/probes/regex_audit.py" "$REPO" > "$PKT/receipts/regex-audit.txt" 2>&1
python3 -B "$PKT/probes/closure_extend.py" "$REPO" "$G" "$PKT/scratch/closure-extend.jsonl" > "$PKT/receipts/closure-extend.log" 2>&1 || true   # exits 1 on raw HOLE count
python3 "$PKT/probes/round5/closure_summary.py" "$PKT/scratch/closure-extend.jsonl" "$PREV/closure-extend.jsonl" > "$PKT/receipts/closure-extend-summary.txt"
python3 -B "$PKT/probes/lexer_oracle.py" "$REPO" "$G" "$PKT/receipts/lexer-oracle.jsonl" > "$PKT/receipts/lexer-oracle.log" 2>&1
python3 -B "$PKT/probes/round3/lexer_probe.py" "$REPO" "$G" > "$PKT/scratch/round3-lexer-probe.log" 2>&1 || true   # pre-existing NameError
python3 -B "$PKT/probes/round2/probe_gate.py" --repo "$REPO" --sdk "$SDK" --cases "$PKT/cases/r2-cases.json" --spellings "$PKT/cases/r2-spellings.json" --out "$PKT/receipts/round2/r2-gate-sdk.json" --work "$PKT/scratch/r2w-sdk"
python3 -B "$PKT/probes/round2/probe_gate.py" --repo "$REPO" --absent --cases "$PKT/cases/r2-cases.json" --spellings "$PKT/cases/r2-spellings.json" --out "$PKT/receipts/round2/r2-gate-absent.json" --work "$PKT/scratch/r2w-absent"
for m in "--sdk $SDK:sdk" "--absent:absent"; do
  python3 -B "$PKT/probes/probe.py" --anchor mutations --labels "$PKT/cases/round5/allowlist-labels.txt" --patch "$PKT/cases/disconnect-allowlist.patch.json" --cases "$PKT/cases/extra.json" ${m%%:*} --out "$PKT/receipts/disconnect/allowlist-off-${m#*:}.json"
done
# 4. round-five probes, unchanged
python3 -B "$PKT/probes/round5/new_cells_probe.py" "$REPO" "$PKT/scratch/mut" "$PKT/receipts/new-cells-probe.json" > "$PKT/receipts/new-cells-probe.log"
python3 -B "$PKT/probes/round5/named_refusal_controls.py" "$REPO" "$PKT/scratch/ctl" "$PKT/receipts/named-refusal-controls.json" > "$PKT/receipts/named-refusal-controls.log"
# 5. round-six delta probes (new)
mkdir -p "$PKT/scratch/parent" "$PKT/scratch/delta"
git -C "$REPO" archive $PARENT sw/builder docs/integration/BAREMETAL_FIRMWARE.md | tar -x -C "$PKT/scratch/parent"
python3 -B "$PKT/probes/round6/delta_probe.py" "$PKT/scratch/parent" "$REPO" "$G" "$PKT/scratch/delta" "$PKT/receipts/delta-probe.json" > "$PKT/receipts/delta-probe.log" 2>&1
python3 -B "$PKT/probes/round6/empty_comment_check.py" "$PKT/scratch/delta" "$G" > "$PKT/receipts/empty-comment-check.log" 2>&1
bash "$PKT/probes/run_probes.sh" "$PKT" "$REPO" "$SDK" nd6-head-sdk:head:sdk:round6/null-directive-more.json nd6-head-absent:head:absent:round6/null-directive-more.json \
  nd6-dev-sdk:$DEV:sdk:round6/null-directive-more.json nd6-dev-absent:$DEV:absent:round6/null-directive-more.json
python3 -B "$PKT/probes/round6/closure_on_guard.py" "$REPO" "$PKT/cases/round6/null-directive-more.json" > "$PKT/receipts/closure-on-null-directives.log"
# 6. static checks (receipts/static-checks.log) from $REPO: docs_check.py, check_baremetal_only.py --check,
#    check_em_dash.py --base $DEV, check_doc_style.py, gen_toc.py --check, check_doc_paths.py,
#    check_py_idiom.py, git diff --check $PARENT..HEAD and $DEV..HEAD
