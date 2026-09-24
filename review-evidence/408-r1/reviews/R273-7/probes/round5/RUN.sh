#!/usr/bin/env bash
# R273-7 command record (run in the foreground, in this order). Variables:
#   PKT   this packet            REPO  a clean clone at 991d5965
#   SDK   a verified pinned SDK (scripts/ci_rv32_sdk.py --destination $SDK --archive <pinned archive>)
#   TOOLS the directory holding the pinned Verilator 5.050
set -eu
: "${PKT:?}" "${REPO:?}" "${SDK:?}" "${TOOLS:?}"
G=$SDK/bin/riscv32-linux-gcc
export PATH=$TOOLS:$PATH R273_TOOL_BIN=$TOOLS R273_LANE=$REPO
cd "$PKT/scratch"
# 1. gate 1b, both modes (from $REPO)
( cd "$REPO" && python3 -B sw/builder/test_firmware_compiler.py --sdk-destination "$SDK" --audit "$PKT/scratch/head-sdk.audit.jsonl" > "$PKT/scratch/head-sdk.log" 2>&1 )
( cd "$REPO" && python3 -B sw/builder/test_firmware_compiler.py --absent --audit "$PKT/scratch/head-absent.audit.jsonl" > "$PKT/scratch/head-absent.log" 2>&1 )
# 2. round-four case probes, unchanged, both modes
for s in r1:round1/all_head.json r2:r2-cases.json bom:bom.json extra:extra.json grader:round1/grader.json \
         hi:hi.json md:md.json published:published.json unread:unread.json v272:round1/verify_r272.json; do
  n=${s%%:*} c=${s#*:}
  bash "$PKT/probes/run_probes.sh" "$PKT" "$REPO" "$SDK" "$n-head-sdk:head:sdk:$c" "$n-head-absent:head:absent:$c"
done
python3 "$PKT/probes/round5/compare_pins.py" <round-four-receipts>/probes "$PKT/receipts/probes" r1 r2 bom extra grader hi md published unread v272
# 3. round-four standalone probes, unchanged
python3 -B "$PKT/probes/subset_probe.py" "$REPO" "$G" "$PKT/receipts/subset-probe-identifiers.jsonl"
python3 -B "$PKT/probes/boundary_probe.py" "$REPO" "$G" "$PKT/receipts/boundary-probe.jsonl"
python3 -B "$PKT/probes/regex_audit.py" "$REPO"
python3 -B "$PKT/probes/closure_extend.py" "$REPO" "$G" "$PKT/scratch/closure-extend.jsonl" || true   # exits 1 on raw HOLE count
python3 "$PKT/probes/round5/closure_summary.py" "$PKT/scratch/closure-extend.jsonl" <round-four-receipts>/closure-extend.jsonl
python3 -B "$PKT/probes/lexer_oracle.py" "$REPO" "$G" "$PKT/receipts/lexer-oracle.jsonl"
python3 -B "$PKT/probes/round3/lexer_probe.py" "$REPO" "$G" || true              # pre-existing NameError
python3 -B "$PKT/probes/round2/probe_gate.py" --repo "$REPO" --sdk "$SDK" --cases "$PKT/cases/r2-cases.json" --spellings "$PKT/cases/r2-spellings.json" --out "$PKT/receipts/round2/r2-gate-sdk.json" --work "$PKT/scratch/r2w-sdk"
python3 -B "$PKT/probes/round2/probe_gate.py" --repo "$REPO" --absent --cases "$PKT/cases/r2-cases.json" --spellings "$PKT/cases/r2-spellings.json" --out "$PKT/receipts/round2/r2-gate-absent.json" --work "$PKT/scratch/r2w-absent"
for m in "--sdk $SDK:sdk" "--absent:absent"; do
  python3 -B "$PKT/probes/probe.py" --anchor mutations --labels "$PKT/cases/round5/allowlist-labels.txt" --patch "$PKT/cases/disconnect-allowlist.patch.json" --cases "$PKT/cases/extra.json" ${m%%:*} --out "$PKT/receipts/disconnect/allowlist-off-${m#*:}.json"
done
# 4. round-five probes (new)
python3 -B "$PKT/probes/round5/new_cells_probe.py" "$REPO" "$PKT/scratch/mut" "$PKT/receipts/new-cells-probe.json"
python3 -B "$PKT/probes/round5/named_refusal_controls.py" "$REPO" "$PKT/scratch/ctl" "$PKT/receipts/named-refusal-controls.json"
bash "$PKT/probes/run_probes.sh" "$PKT" "$REPO" "$SDK" nulldir-head-sdk:head:sdk:round5/null-directive.json nulldir-head-absent:head:absent:round5/null-directive.json \
  nulldir-dev-sdk:759da623072358afdb0e9d570a7b4b6a788492c9:sdk:round5/null-directive.json nulldir-dev-absent:759da623072358afdb0e9d570a7b4b6a788492c9:absent:round5/null-directive.json
