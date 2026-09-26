#!/usr/bin/env bash
# [R326] round R326-1 review probes for issue #567 / PR #569.
# Usage: r326_checks.sh <clone> <packet> <section>...
# Each section writes receipts/<section>.log and receipts/<section>.rc.
# Commands run in the foreground, one at a time; every gate status is taken
# directly (no pipelines around a gate).
set -u
CLONE=$(cd "$1" && pwd); PACKET=$(cd "$2" && pwd); shift 2
HEAD_EXP=54b4c3bbbc8cdea5ced0be29c9226fdf82233b74
BASE=7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
OLD=990f96526bb89356c963a260ebbdcf2a77e6623a
NEW=0922e43408f891fc0b84a84691df86b4fd0f1c0d
PINBIN=${PINBIN:-$VALIDATION_STORAGE/567-manager-r1/pinned-tool-bin}
R=$PACKET/receipts; S=$PACKET/scratch
mkdir -p "$R" "$S"

step() { # <label> <cmd...> : run, log rc
  echo "### $1"; shift
  echo "\$ $*"
  "$@"; local rc=$?
  echo "### rc=$rc"
  return $rc
}

identity() {
  cd "$CLONE" || return 2
  local fail=0
  step head git rev-parse HEAD 'HEAD^{tree}' || fail=1
  [ "$(git rev-parse HEAD)" = "$HEAD_EXP" ] || { echo "HEAD MISMATCH"; fail=1; }
  step status git status --porcelain=v2 --ignore-submodules=none || fail=1
  [ -z "$(git status --porcelain --ignore-submodules=none)" ] || { echo "DIRTY"; fail=1; }
  step gitlinks git ls-files --stage -- protocol-processor gptp-processor third_party/verilog-axis external || fail=1
  step substatus git submodule status || fail=1
  for m in protocol-processor gptp-processor third_party/verilog-axis; do
    [ -z "$(git -C "$m" status --porcelain)" ] || { echo "SUBMODULE DIRTY $m"; fail=1; }
    [ "$(git -C "$m" rev-parse HEAD)" = "$(git rev-parse ":$m")" ] || { echo "SUBMODULE MISMATCH $m"; fail=1; }
  done
  step index-check git diff --cached --quiet || fail=1
  step tracked-bytes git diff --quiet HEAD || fail=1
  return $fail
}

delta() {
  cd "$CLONE" || return 2
  local fail=0
  step pr-stat git diff --stat "$BASE..$HEAD_EXP" || fail=1
  step pr-names git diff --name-status "$BASE..$HEAD_EXP" || fail=1
  step pr-log git log --format='%H %an %s' "$BASE..$HEAD_EXP" || fail=1
  echo "## commit message shape (one line, no trailers)"
  for c in $(git rev-list "$BASE..$HEAD_EXP"); do
    n=$(git log -1 --format=%B "$c" | sed '/^$/d' | wc -l); echo "$c lines=$n"
    [ "$n" -eq 1 ] || fail=1
  done
  echo "## parent RTL / tb / syn-script / VERSION untouched (expect empty)"
  out=$(git diff --name-only "$BASE..$HEAD_EXP" -- hdl tb/verilator/*/*.sv tb/verilator/*/*.cpp tb/verilator/*/Makefile syn/yosys/*.sh syn/ooc VERSION scripts sw avdecc tests)
  echo "[$out]"; [ -z "$out" ] || fail=1
  echo "## gitlink move"
  step gitlink-old git rev-parse "$BASE:protocol-processor" || fail=1
  step gitlink-new git rev-parse "$HEAD_EXP:protocol-processor" || fail=1
  [ "$(git rev-parse "$BASE:protocol-processor")" = "$OLD" ] || fail=1
  [ "$(git rev-parse "$HEAD_EXP:protocol-processor")" = "$NEW" ] || fail=1
  for m in gptp-processor third_party/verilog-axis external; do
    [ "$(git rev-parse "$BASE:$m")" = "$(git rev-parse "$HEAD_EXP:$m")" ] || { echo "OTHER GITLINK MOVED $m"; fail=1; }
  done
  cd protocol-processor || return 2
  step pp-ancestor git merge-base --is-ancestor "$OLD" "$NEW" || fail=1
  step pp-log git log --format='%H %s' "$OLD..$NEW" || fail=1
  step pp-stat git diff --stat "$OLD" "$NEW" || fail=1
  echo "## processor hdl/ delta (expect empty)"
  out=$(git diff --stat "$OLD" "$NEW" -- hdl/); echo "[$out]"; [ -z "$out" ] || fail=1
  step pp-hdl-trees git rev-parse "$OLD:hdl" "$NEW:hdl" || fail=1
  [ "$(git rev-parse "$OLD:hdl")" = "$(git rev-parse "$NEW:hdl")" ] || fail=1
  return $fail
}

ledger() {
  cd "$CLONE" || return 2
  local fail=0
  echo "## rows for old and new pin"
  grep -n -e "^$OLD" -e "^$NEW" syn/yosys/rom_digests.tsv
  a=$(grep "^$OLD" syn/yosys/rom_digests.tsv | cut -f2,3); b=$(grep "^$NEW" syn/yosys/rom_digests.tsv | cut -f2,3)
  echo "old=[$a]"; echo "new=[$b]"
  [ -n "$a" ] && [ "$a" = "$b" ] || { echo "ROW MISMATCH"; fail=1; }
  [ "$(grep -c "^$NEW" syn/yosys/rom_digests.tsv)" -eq 2 ] || fail=1
  step ledger-diff git diff "$BASE..$HEAD_EXP" -- syn/yosys/rom_digests.tsv || fail=1
  echo "## sortedness and row shape"
  grep -v '^#' syn/yosys/rom_digests.tsv > "$S/ledger.body"
  LC_ALL=C sort -c "$S/ledger.body" && echo sorted-ok || fail=1
  awk -F'\t' 'NF!=3 || length($1)!=40 || length($3)!=64 {bad=1; print "BAD", NR, $0} END{exit bad}' "$S/ledger.body" || fail=1
  echo "## independent ROM generation from archived processor hdl at both pins"
  for p in "$OLD" "$NEW"; do
    d="$S/pp-$p"; rm -rf "$d"; mkdir -p "$d"
    git -C protocol-processor archive "$p" hdl | tar -x -C "$d" || fail=1
    (cd "$d" && python3 hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex >/dev/null && python3 hdl/aecp/ucode/gen_ucode.py -o ucode.hex >/dev/null) || fail=1
    echo "$p $(sha256sum "$d/ltn_rom.hex" | cut -c1-64) $(sha256sum "$d/ucode.hex" | cut -c1-64)"
  done
  x=$(sha256sum "$S/pp-$OLD/ltn_rom.hex" | cut -c1-64); y=$(grep "^$NEW	ltn_rom.hex" syn/yosys/rom_digests.tsv | cut -f3)
  [ "$x" = "$y" ] || { echo "LTN DIGEST != LEDGER"; fail=1; }
  x=$(sha256sum "$S/pp-$NEW/ucode.hex" | cut -c1-64); y=$(grep "^$NEW	ucode.hex" syn/yosys/rom_digests.tsv | cut -f3)
  [ "$x" = "$y" ] || { echo "UCODE DIGEST != LEDGER"; fail=1; }
  echo "## repository tool re-record reproduces the committed ledger byte for byte"
  cp -p syn/yosys/rom_digests.tsv "$S/rom_digests.head.tsv"
  (cd syn/yosys && OOC_TMP="$S/ooc-record" step record ./ooc.sh --record-rom-digests) || fail=1
  step record-diff git diff --exit-code -- syn/yosys/rom_digests.tsv || fail=1
  echo "## negative probe: without the new rows the OOC path refuses the pin"
  grep -v "^$NEW" "$S/rom_digests.head.tsv" > syn/yosys/rom_digests.tsv
  (cd syn/yosys && OOC_TMP="$S/ooc-neg" ./ooc.sh KL_pp_shadow) > "$S/ooc-neg.log" 2>&1; nrc=$?
  cat "$S/ooc-neg.log"; echo "neg rc=$nrc"
  [ "$nrc" -eq 2 ] && grep -q "no recorded content digest for ltn_rom.hex at protocol-processor pin $NEW" "$S/ooc-neg.log" || { echo "NEGATIVE PROBE DID NOT REFUSE AS EXPECTED"; fail=1; }
  echo "## negative probe 2: a wrong digest for the new pin is refused"
  sed "s/^\($NEW	ucode.hex	\).*/\1$(printf '0%.0s' $(seq 64))/" "$S/rom_digests.head.tsv" > syn/yosys/rom_digests.tsv
  (cd syn/yosys && OOC_TMP="$S/ooc-neg2" ./ooc.sh KL_pp_shadow) > "$S/ooc-neg2.log" 2>&1; nrc=$?
  cat "$S/ooc-neg2.log"; echo "neg2 rc=$nrc"
  [ "$nrc" -eq 2 ] && grep -q "content digest mismatch for ucode.hex at protocol-processor pin $NEW" "$S/ooc-neg2.log" || { echo "NEGATIVE PROBE 2 DID NOT REFUSE AS EXPECTED"; fail=1; }
  cp -p "$S/rom_digests.head.tsv" syn/yosys/rom_digests.tsv
  step restored git diff --exit-code -- syn/yosys/rom_digests.tsv || fail=1
  return $fail
}

ooc() {
  cd "$CLONE/syn/yosys" || return 2
  OOC_TMP="$S/ooc-pos" step ooc-KL_pp_shadow ./ooc.sh KL_pp_shadow
}

params() {
  cd "$CLONE" || return 2
  local fail=0
  step checker python3 protocol-processor/scripts/check-integrator-params.py || fail=1
  step independent python3 "$PACKET/scripts/r326_params.py" "$CLONE" || fail=1
  echo "## mutation: checker must fail on a guide missing one row"
  grep -v '^| `N_CONTROL_P`' protocol-processor/docs/guides/integrator.md > "$S/integrator.minus.md"
  python3 protocol-processor/scripts/check-integrator-params.py --guide "$S/integrator.minus.md"; m=$?
  echo "mutant rc=$m"; [ "$m" -eq 1 ] || fail=1
  echo "## mutation: checker at the old pin's guide (pre-inventory) must fail"
  git -C protocol-processor show "$OLD:docs/guides/integrator.md" > "$S/integrator.old.md"
  python3 protocol-processor/scripts/check-integrator-params.py --guide "$S/integrator.old.md"; m=$?
  echo "old-guide rc=$m"; [ "$m" -eq 1 ] || fail=1
  return $fail
}

diagram() {
  cd "$CLONE" || return 2
  local fail=0
  step gen-selftest python3 docs/diagrams/submodule_boundaries.gen.py --selftest || fail=1
  step gen-check python3 docs/diagrams/submodule_boundaries.gen.py --check || fail=1
  step submodule-docs python3 scripts/check_submodule_docs.py || fail=1
  step diagram-pngs python3 scripts/check_diagram_pngs.py || fail=1
  echo "## regenerate with the repository generator in place, then compare tracked bytes"
  step regen-doc-sha sha256sum docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.svg docs/diagrams/submodule_boundaries.png docs/diagrams/PNG_MANIFEST.json
  step regen python3 docs/diagrams/submodule_boundaries.gen.py || fail=1
  step regen-diff git diff --exit-code --stat -- docs/diagrams || fail=1
  git checkout -- docs/diagrams
  step regen-doc-sha-after sha256sum docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.svg docs/diagrams/submodule_boundaries.png docs/diagrams/PNG_MANIFEST.json
  echo "## old-pin diagram must fail the check (gate can see a stale pin)"
  git show "$BASE:docs/diagrams/submodule_boundaries.drawio" > docs/diagrams/submodule_boundaries.drawio
  python3 docs/diagrams/submodule_boundaries.gen.py --check; m=$?
  python3 scripts/check_submodule_docs.py; m2=$?
  echo "stale-drawio gen-check rc=$m submodule-docs rc=$m2"
  git checkout -- docs/diagrams
  [ "$m" -ne 0 ] && [ "$m2" -ne 0 ] || fail=1
  step restored git diff --exit-code -- docs/diagrams || fail=1
  echo "## stale-pin text survey (current-tense references to the old pin)"
  git grep -n -e 990f9652 -e 990f96526 -- ':!docs/history' ':!syn/yosys/rom_digests.tsv'
  return $fail
}

gates_docs() {
  cd "$CLONE" || return 2
  local fail=0
  step docs-git python3 -B scripts/docs_check.py || fail=1
  d="$S/nogit-export"; rm -rf "$d"; mkdir -p "$d"
  git archive HEAD | tar -x -C "$d"
  (cd "$d" && step docs-nogit python3 -B scripts/docs_check.py) || fail=1
  step em-dash python3 -B scripts/check_em_dash.py --base "$BASE" || fail=1
  step doc-style python3 -B scripts/check_doc_style.py || fail=1
  step toc python3 -B scripts/gen_toc.py --check || fail=1
  step toc-anchors python3 -B scripts/gen_toc.py --verify-anchors || fail=1
  step doc-paths python3 -B scripts/check_doc_paths.py || fail=1
  step diff-check git diff --check "$BASE" "$HEAD_EXP" || fail=1
  return $fail
}

gates_static() {
  cd "$CLONE" || return 2
  local fail=0
  step rtl-source-lists python3 scripts/check_rtl_source_lists.py || fail=1
  step rtl-source-lists-selftest python3 scripts/check_rtl_source_lists_selftest.py || fail=1
  step soc-sources python3 scripts/check_soc_sources.py || fail=1
  step xvlog-gate python3 scripts/xvlog_gate.py --check || fail=1
  step lint-rtl python3 scripts/lint_rtl.py --check || fail=1
  step sv-idiom python3 scripts/check_sv_idiom.py || fail=1
  step cpp-idiom python3 scripts/check_cpp_idiom.py || fail=1
  step py-idiom python3 scripts/check_py_idiom.py || fail=1
  step sh-idiom python3 scripts/check_sh_idiom.py || fail=1
  step port-contracts python3 scripts/check_port_contracts.py || fail=1
  step naming python3 scripts/measure_naming.py --check || fail=1
  step test-evidence python3 scripts/measure_test_evidence.py --check || fail=1
  step todo-ownership python3 scripts/check_todo_ownership.py || fail=1
  step hygiene python3 scripts/check_hygiene.py || fail=1
  step module-matrix python3 docs/traceability/gen_module_matrix.py --check || fail=1
  step feature-status python3 scripts/check_feature_status.py || fail=1
  return $fail
}

pp_shadow() {
  cd "$CLONE" || return 2
  step pp_shadow make -C tb/verilator/pp_shadow
}

milan_dp_notify() {
  cd "$CLONE" || return 2
  step milan_dp-notify make -C tb/verilator/milan_dp notify
}

yosys_elab() {
  cd "$CLONE" || return 2
  step yosys-elab syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
}

behave_tests() {
  cd "$CLONE/tests" || return 2
  step behave behave --no-capture -f progress
}

export PATH="$PINBIN:$PATH"
overall=0
for sec in "$@"; do
  "$sec" > "$R/$sec.log" 2>&1; rc=$?
  echo "$rc" > "$R/$sec.rc"
  echo "section $sec rc=$rc"
  [ "$rc" -eq 0 ] || overall=1
done
exit $overall
