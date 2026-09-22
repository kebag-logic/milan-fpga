#!/usr/bin/env bash
# R222-3: focused documentation / CI-policy gates on the combined tree, in
# three fresh scratch contexts that the mutation probes never touch:
#   cand-nosub  Git clone at 72e16c61, no submodule initialized (docs-check's
#               pre-submodule phase, plus the #513 step's no-submodule claim)
#   cand-nogit  git-archive extraction, no .git (docs-check-no-git)
#   cand2       Git clone at 72e16c61 with the three pinned submodules
# Usage: 10_focused_static_gates.sh <review-clone> <scratch-root> <receipts-dir>
set -uo pipefail
review=$1; S=$2; OUT=$3
C=72e16c6172db723734317b105cff6c6e9168571a
D=52711029f374650dc93830d5ea28e81cb5c8f410
P=1496558d82cf35fc98dda0e781b2a1be643c301a
MB=88e9276b2a220c716f64a843f7e1eb8f9265e896
export PYTHONDONTWRITEBYTECODE=1 GIT_NO_REPLACE_OBJECTS=1
subs=(protocol-processor gptp-processor third_party/verilog-axis)

step() { # <dir> <cmd...>
  local dir=$1; shift
  local out rc
  out=$(cd "$dir" && "$@" 2>&1); rc=$?
  [ $rc -eq 0 ] || fail=$((fail+1))
  printf 'exit %-3s %s\n' "$rc" "$*"
  printf '%s\n' "$out" | grep -v '^\s*$' | tail -2 | sed 's/^/        | /'
}

setup() {
  rm -rf "$S/cand-nosub" "$S/cand-nogit" "$S/cand2"
  git clone -q --no-hardlinks --no-checkout "$review" "$S/cand-nosub"
  git -C "$S/cand-nosub" checkout -q --detach $C
  git clone -q --no-hardlinks --no-checkout "$review" "$S/cand2"
  git -C "$S/cand2" checkout -q --detach $C
  for s in "${subs[@]}"; do git -C "$S/cand2" config "submodule.$s.url" "$review/$s"; done
  git -C "$S/cand2" -c protocol.file.allow=always submodule -q update --init -- "${subs[@]}"
  mkdir -p "$S/cand-nogit"
  git -C "$S/cand2" archive --format=tar $C | tar -x -C "$S/cand-nogit"
}

nosub() {
  local d="$S/cand-nosub"; fail=0
  echo "head=$(git -C "$d" rev-parse HEAD) tree=$(git -C "$d" rev-parse 'HEAD^{tree}')"
  echo "submodule status prefixes: $(git -C "$d" submodule status | cut -c1 | tr -d '\n') (all '-' = uninitialized)"
  local base; base=$(git -C "$d" merge-base HEAD $D)
  echo "em-dash base = merge-base(HEAD, dev) = $base"
  step "$d" python3 scripts/docs_check.py
  step "$d" python3 scripts/check_em_dash.py --base "$base"
  step "$d" python3 scripts/check_doc_style.py
  step "$d" python3 scripts/check_doc_style.py --selftest
  step "$d" python3 scripts/check_gptp_docs.py
  step "$d" python3 scripts/check_gptp_docs.py --selftest
  step "$d" python3 docs/DOC_MAP.gen.py --check
  step "$d" python3 docs/DOC_MAP.gen.py --selftest
  step "$d" python3 docs/diagrams/timesync_chain.gen.py --check
  step "$d" python3 docs/diagrams/timesync_chain.gen.py --selftest
  step "$d" python3 scripts/check_solution_docs.py
  step "$d" python3 scripts/check_solution_docs.py --selftest
  step "$d" python3 docs/diagrams/submodule_boundaries.gen.py --check
  step "$d" python3 docs/diagrams/submodule_boundaries.gen.py --selftest
  step "$d" python3 scripts/check_submodule_docs.py
  step "$d" python3 scripts/check_submodule_docs.py --selftest
  step "$d" python3 scripts/check_diagram_pngs.py
  step "$d" python3 scripts/check_diagram_pngs.py --selftest
  step "$d" python3 scripts/check_feature_status.py --self-test
  step "$d" python3 docs/traceability/gen_module_matrix.py --check
  echo "-- #513 step, no submodule initialized (its documented claim)"
  step "$d" python3 avdecc/gen_aem_store.py --self-test
  echo "non-zero steps: $fail"
  echo "clone status lines after run: $(git -C "$d" status --porcelain --untracked-files=all | wc -l)"
}

nogit() {
  local d="$S/cand-nogit"; fail=0
  echo "extraction has .git: $([ -e "$d/.git" ] && echo yes || echo no)"
  local n=0 bad=0
  while IFS=$'\t' read -r meta path; do
    mode=${meta%% *}; rest=${meta#* }; oid=${rest#* }; oid=${oid%% *}
    case "$mode" in
      100644|100755)
        n=$((n+1))
        h=$(git hash-object --no-filters "$d/$path")
        [ "$h" = "$oid" ] || { bad=$((bad+1)); echo "MISMATCH $path"; }
        if [ -x "$d/$path" ]; then dm=100755; else dm=100644; fi
        [ "$dm" = "$mode" ] || { bad=$((bad+1)); echo "MODE $path"; } ;;
    esac
  done < <(git -C "$S/cand2" ls-tree -r $C)
  echo "archived regular files checked against candidate blobs/modes: $n mismatches: $bad"
  step "$d" python3 scripts/docs_check.py
  step "$d" python3 scripts/check_feature_status.py
  echo "non-zero steps: $fail"
}

withsub() {
  local d="$S/cand2"; fail=0
  echo "head=$(git -C "$d" rev-parse HEAD) submodules: $(git -C "$d" submodule status | cut -c1 | tr -d '\n')"
  step "$d" python3 scripts/docs_check.py
  step "$d" python3 scripts/check_doc_paths.py
  step "$d" python3 scripts/check_doc_style.py
  step "$d" python3 scripts/gen_toc.py --selftest
  step "$d" python3 scripts/gen_toc.py --verify-anchors
  step "$d" python3 scripts/gen_toc.py --check
  step "$d" python3 scripts/check_archive.py
  step "$d" python3 scripts/check_em_dash.py --base $D
  step "$d" python3 scripts/check_em_dash.py --base $P
  step "$d" python3 scripts/check_em_dash.py --base $MB
  step "$d" python3 scripts/check_em_dash.py --selftest
  step "$d" python3 scripts/check_py_idiom.py
  step "$d" python3 scripts/check_hygiene.py --check
  step "$d" python3 scripts/check_todo_ownership.py
  step "$d" python3 scripts/check_feature_status.py
  step "$d" python3 scripts/ci_events.py --check
  step "$d" python3 scripts/ci_events.py --selftest
  step "$d" git diff --check $D $C
  step "$d" git diff --check $P $C
  step "$d" git diff --check $MB $C
  echo "non-zero steps: $fail"
  echo "clone status lines after run: $(git -C "$d" status --porcelain --untracked-files=all | wc -l)"
}

setup > "$OUT/10-setup.txt" 2>&1
nosub  > "$OUT/10a-docs-nosub.txt" 2>&1 &
nogit  > "$OUT/10b-docs-nogit.txt" 2>&1 &
withsub > "$OUT/10c-static-withsub.txt" 2>&1 &
wait
cat "$OUT/10-setup.txt" "$OUT/10a-docs-nosub.txt" "$OUT/10b-docs-nogit.txt" "$OUT/10c-static-withsub.txt"
