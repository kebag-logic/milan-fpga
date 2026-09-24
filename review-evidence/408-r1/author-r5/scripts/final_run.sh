#!/usr/bin/env bash
# [A261] scratch: re-run every gate and reviewer probe at the final head.
# usage: final_run.sh <chunk>   chunk = gate1b | whole-sdk | whole-absent+static
#                                       | plain | probes | canfail
set -u
L=$LANES/408-409-boot-gate-retire
D=$VALIDATION_STORAGE/408-a261
F=$D/final
SDK=$D/sdk/br-milan-rv32/host
GCC=$SDK/bin/riscv32-linux-gcc
export PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$PATH
mkdir -p "$F"
cd "$L" || exit 2
git rev-parse HEAD > "$F/head.txt"
test -z "$(git status --porcelain)" || { echo "DIRTY TREE"; exit 2; }
case "$1" in
gate1b)
  ( python3 -B sw/builder/test_firmware_compiler.py --sdk-destination "$SDK" \
      --audit "$F/gate1b-sdk.audit.jsonl" > "$F/gate1b-sdk.log" 2>&1
    echo "exit=$?" >> "$F/gate1b-sdk.log" ) &
  ( python3 -B sw/builder/test_firmware_compiler.py --absent \
      --audit "$F/gate1b-absent.audit.jsonl" > "$F/gate1b-absent.log" 2>&1
    echo "exit=$?" >> "$F/gate1b-absent.log" ) &
  wait
  python3 "$D/summarize_gate.py" "$F/gate1b-sdk.log" "$F/gate1b-absent.log"
  ;;
whole-sdk)
  python3 -B "$D/whole_suite.py" "$L" sdk "$SDK" "$F/whole-sdk.audit.jsonl" \
    > "$F/whole-sdk.log" 2>&1
  echo "exit=$?" >> "$F/whole-sdk.log"
  tail -n 4 "$F/whole-sdk.log"
  ;;
whole-absent+static)
  ( python3 -B "$D/whole_suite.py" "$L" absent "$F/whole-absent.audit.jsonl" \
      > "$F/whole-absent.log" 2>&1
    echo "exit=$?" >> "$F/whole-absent.log" ) &
  S=$F/static; mkdir -p "$S"; : > "$S/rc.txt"
  python3 -B scripts/docs_check.py > "$S/docs_check.log" 2>&1
  echo "docs_check (git) rc=$?" >> "$S/rc.txt"
  rm -rf "$D/nogit"; mkdir -p "$D/nogit"
  git archive HEAD | tar -x -C "$D/nogit"
  ( cd "$D/nogit" && test ! -e .git && python3 -B scripts/docs_check.py \
      > "$S/docs_check-nogit.log" 2>&1; echo "docs_check (no git) rc=$?" >> "$S/rc.txt" )
  python3 scripts/check_baremetal_only.py --check > "$S/baremetal.log" 2>&1
  echo "check_baremetal_only --check rc=$?" >> "$S/rc.txt"
  python3 scripts/check_baremetal_only.py --selftest > "$S/baremetal-selftest.log" 2>&1
  echo "check_baremetal_only --selftest rc=$?" >> "$S/rc.txt"
  python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9 \
    > "$S/em_dash.log" 2>&1
  echo "check_em_dash --base 759da623 rc=$?" >> "$S/rc.txt"
  python3 scripts/check_doc_style.py > "$S/doc_style.log" 2>&1
  echo "check_doc_style rc=$?" >> "$S/rc.txt"
  python3 scripts/gen_toc.py --check > "$S/gen_toc.log" 2>&1
  echo "gen_toc --check rc=$?" >> "$S/rc.txt"
  python3 scripts/check_doc_paths.py > "$S/doc_paths.log" 2>&1
  echo "check_doc_paths rc=$?" >> "$S/rc.txt"
  python3 scripts/check_py_idiom.py > "$S/py_idiom.log" 2>&1
  echo "check_py_idiom rc=$?" >> "$S/rc.txt"
  git diff --check 759da623072358afdb0e9d570a7b4b6a788492c9 HEAD > "$S/diff-check.log" 2>&1
  echo "git diff --check 759da623..HEAD rc=$?" >> "$S/rc.txt"
  git diff --check > "$S/diff-check-wt.log" 2>&1
  echo "git diff --check (worktree) rc=$?" >> "$S/rc.txt"
  python3 sw/builder/test_firmware_compiler.py --selftest > "$S/tfc-selftest.log" 2>&1
  echo "test_firmware_compiler --selftest rc=$?" >> "$S/rc.txt"
  wait
  cat "$S/rc.txt"
  for f in docs_check docs_check-nogit baremetal baremetal-selftest em_dash doc_style \
           gen_toc doc_paths py_idiom tfc-selftest; do
    echo "-- $f: $(tail -n 1 "$S/$f.log" | cut -c1-220)"
  done
  tail -n 4 "$F/whole-absent.log"
  ;;
plain)
  python3 -B sw/builder/test_builder.py --require-rv32 > "$F/plain-require-rv32.log" 2>&1
  echo "exit=$?" >> "$F/plain-require-rv32.log"
  tail -n 4 "$F/plain-require-rv32.log"
  python3 "$D/summarize_gate.py" "$F/plain-require-rv32.log" | head -3
  ;;
probes)
  R5=$D/r272-5/review-evidence/408-r1/reviews/R272-5/scripts
  P=$D/r273-6/review-evidence/408-r1/reviews/R273-6
  O=$F/r272-5; mkdir -p "$O/as-is" "$O/nine"
  R272_GCC=$GCC R272_OUT=$O/as-is python3 -B "$R5/r1/probe_gate1b.py" --tree "$L" \
    --absent --cases "$R5/r5/cases_r5_closure.py" --out "$O/as-is/closure-probe.json" \
    > "$O/as-is/closure-probe.log" 2>&1; echo "exit=$?" >> "$O/as-is/closure-probe.log"
  R272_GCC=$GCC R272_OUT=$O/nine python3 -B "$R5/r1/probe_gate1b.py" --tree "$L" \
    --absent --cases "$R5/r5/cases_r5_closure.py" --out "$O/nine/closure-probe.json" \
    --patch "$D/patch-nine-positions.json" \
    > "$O/nine/closure-probe.log" 2>&1; echo "exit=$?" >> "$O/nine/closure-probe.log"
  O=$F/r273-6; mkdir -p "$O/round2" "$O/round3" "$O/disconnect"
  ( cd "$P/probes" || exit 2
    python3 -B subset_probe.py "$L" "$GCC" "$O/subset-probe.jsonl" > "$O/subset-probe.log" 2>&1
    echo "subset_probe rc=$?" >> "$O/rc.txt"
    python3 -B lexer_oracle.py "$L" "$GCC" "$O/lexer-oracle.jsonl" > "$O/lexer-oracle.log" 2>&1
    echo "lexer_oracle rc=$?" >> "$O/rc.txt"
    python3 -B closure_extend.py "$L" "$GCC" "$O/closure-extend.jsonl" > "$O/closure-extend.log" 2>&1
    echo "closure_extend rc=$?" >> "$O/rc.txt"
    python3 -B boundary_probe.py "$L" "$GCC" "$O/boundary-probe.jsonl" > "$O/boundary-probe.log" 2>&1
    echo "boundary_probe rc=$?" >> "$O/rc.txt"
    python3 -B regex_audit.py "$L" > "$O/regex-audit.txt" 2>&1
    echo "regex_audit rc=$?" >> "$O/rc.txt"
    python3 -B round3/lexer_probe.py "$L" "$GCC" > "$O/round3/lexer-probe-head.jsonl" \
      2> "$O/round3/lexer-probe-head.err"
    echo "round3 lexer_probe rc=$?" >> "$O/rc.txt" )
  python3 "$D/summarize_closure_extend.py" "$O/closure-extend.jsonl" > "$O/closure-extend-summary.txt"
  export R273_LANE=$L R273_TOOL_BIN=$VALIDATION_TOOLS/verilator-v5.050/bin
  rm -rf "$P/receipts/probes"; mkdir -p "$P/scratch" "$P/receipts/probes"
  bash "$P/probes/run_probes.sh" "$P" "$L" "$SDK" \
    r1-head-absent:head:absent:round1/all_head.json r2-head-absent:head:absent:r2-cases.json \
    bom-head-absent:head:absent:bom.json extra-head-absent:head:absent:extra.json \
    grader-head-absent:head:absent:round1/grader.json hi-head-absent:head:absent:hi.json \
    md-head-absent:head:absent:md.json published-head-absent:head:absent:published.json \
    unread-head-absent:head:absent:unread.json v272-head-absent:head:absent:round1/verify_r272.json \
    >> "$O/rc.txt" 2>&1
  bash "$P/probes/run_probes.sh" "$P" "$L" "$SDK" \
    r1-head-sdk:head:sdk:round1/all_head.json r2-head-sdk:head:sdk:r2-cases.json \
    bom-head-sdk:head:sdk:bom.json extra-head-sdk:head:sdk:extra.json \
    grader-head-sdk:head:sdk:round1/grader.json >> "$O/rc.txt" 2>&1
  bash "$P/probes/run_probes.sh" "$P" "$L" "$SDK" \
    hi-head-sdk:head:sdk:hi.json md-head-sdk:head:sdk:md.json \
    published-head-sdk:head:sdk:published.json unread-head-sdk:head:sdk:unread.json \
    v272-head-sdk:head:sdk:round1/verify_r272.json >> "$O/rc.txt" 2>&1
  rm -rf "$O/probes"; cp -r "$P/receipts/probes" "$O/probes"
  ( cd "$P/scratch" || exit 2
    ( python3 -B "$P/probes/round2/probe_gate.py" --repo "$L" --absent --cases "$P/cases/r2-cases.json" \
        --spellings "$P/cases/r2-spellings.json" --out "$O/round2/r2-gate-absent.json" \
        --work "$P/scratch/r2work-absent" > "$O/round2/r2-gate-absent.log" 2>&1
      echo "r2-gate-absent rc=$?" >> "$O/rc.txt" ) &
    ( python3 -B "$P/probes/round2/probe_gate.py" --repo "$L" --sdk "$SDK" --cases "$P/cases/r2-cases.json" \
        --spellings "$P/cases/r2-spellings.json" --out "$O/round2/r2-gate-sdk.json" \
        --work "$P/scratch/r2work-sdk" > "$O/round2/r2-gate-sdk.log" 2>&1
      echo "r2-gate-sdk rc=$?" >> "$O/rc.txt" ) &
    ( python3 -B "$P/probes/probe.py" --absent --anchor mutations --labels "$P/receipts/allowlist-labels.txt" \
        --patch "$P/cases/disconnect-allowlist.patch.json" --out "$O/disconnect/allowlist-off-absent.json" \
        > "$O/disconnect/allowlist-off-absent.log" 2>&1
      echo "allowlist-off-absent rc=$?" >> "$O/rc.txt" ) &
    ( python3 -B "$P/probes/probe.py" --absent --anchor mutations \
        --out "$O/disconnect/mutations-intact-absent.json" > "$O/disconnect/mutations-intact-absent.log" 2>&1
      echo "mutations-intact-absent rc=$?" >> "$O/rc.txt" ) &
    wait
    python3 -B "$P/probes/probe.py" --sdk "$SDK" --anchor mutations --labels "$P/receipts/allowlist-labels.txt" \
      --patch "$P/cases/disconnect-allowlist.patch.json" --out "$O/disconnect/allowlist-off-sdk.json" \
      > "$O/disconnect/allowlist-off-sdk.log" 2>&1
    echo "allowlist-off-sdk rc=$?" >> "$O/rc.txt" )
  cat "$O/rc.txt"
  ;;
canfail)
  O=$F/canfail; mkdir -p "$O"
  for p in nbsp-splice registry-empty registry-extra nameless-admitted; do
    python3 -B "$D/disconnect.py" "$L" "$D/patch-$p.json" > "$O/$p-absent.log" 2>&1
    echo "$p absent exit=$?: $(grep -h 'GATE STOPPED\|GATE PASS' "$O/$p-absent.log" | cut -c1-200)"
  done
  python3 -B "$D/disconnect.py" "$L" "$D/patch-nbsp-splice.json" --sdk "$SDK" > "$O/nbsp-splice-sdk.log" 2>&1
  echo "nbsp-splice sdk exit=$?: $(grep -h 'GATE STOPPED\|GATE PASS' "$O/nbsp-splice-sdk.log" | cut -c1-200)"
  ( python3 -B "$D/disconnect.py" "$L" "$D/patch-nbsp-splice-nine.json" > "$O/nbsp-splice-nine-absent.log" 2>&1
    echo "nbsp-splice-nine absent exit=$?" ) &
  ( python3 -B "$D/disconnect.py" "$L" "$D/patch-nbsp-splice-nine.json" --sdk "$SDK" > "$O/nbsp-splice-nine-sdk.log" 2>&1
    echo "nbsp-splice-nine sdk exit=$?" ) &
  wait
  for m in absent sdk; do
    echo "nine/$m: $(grep -h 'GATE PASS\|GATE STOPPED\|GATE 1b PASS' "$O/nbsp-splice-nine-$m.log" | cut -c1-100 | tr '\n' ' ') $(grep -o '[0-9]*/[0-9]* mutations rejected' "$O/nbsp-splice-nine-$m.log") $(grep -o '[0-9]*/[0-9]* character-closure cells' "$O/nbsp-splice-nine-$m.log")"
  done
  ;;
*) echo "unknown chunk $1"; exit 2 ;;
esac
