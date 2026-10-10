#!/usr/bin/env bash
# R590-2: the cheap documentation and code-quality gates the diff touches,
# each with its own log and rc file. Usage: gates.sh CLONE MDPY PY312 BASE OUTDIR
set -u
CLONE="$1"; MDPY="$2"; PY312="$3"; BASE="$4"; OUT="$5"
mkdir -p "$OUT"
export PYTHONDONTWRITEBYTECODE=1
cd "$CLONE" || exit 2
g() { local name="$1"; shift; "$@" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc"; }
g docs_check "$MDPY" -B scripts/docs_check.py
g em_dash "$MDPY" -B scripts/check_em_dash.py --base "$BASE"
g doc_style "$MDPY" -B scripts/check_doc_style.py
g toc_check "$MDPY" -B scripts/gen_toc.py --check
g toc_anchors "$MDPY" -B scripts/gen_toc.py --verify-anchors
g doc_paths "$MDPY" -B scripts/check_doc_paths.py
g doc_map "$MDPY" -B docs/DOC_MAP.gen.py --check
g py_idiom "$PY312" -B scripts/check_py_idiom.py
g sh_idiom "$PY312" -B scripts/check_sh_idiom.py
g naming "$PY312" -B scripts/measure_naming.py --check
g fail_fast "$PY312" -B scripts/measure_fail_fast.py --check
g test_evidence "$PY312" -B scripts/measure_test_evidence.py --check
g hygiene "$PY312" -B scripts/check_hygiene.py --check
g todo "$PY312" -B scripts/check_todo_ownership.py
g soc_sources "$PY312" -B scripts/check_soc_sources.py
g resource_baseline "$PY312" -B syn/ooc/pp_resource_gate.py check-baseline
g litex_list scripts/run_litex_sims.sh --list
g diff_check git diff --check "$BASE" HEAD
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
