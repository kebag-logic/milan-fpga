#!/usr/bin/env bash
# focused_gates.sh: run inside sandbox.sh from a disposable clone at the head;
# the focused static gates for the files this PR touches. One line per gate.
set -uo pipefail
gate() { local name=$1; shift; local out rc; out=$("$@" 2>&1); rc=$?; printf '== %s rc=%s\n%s\n' "$name" "$rc" "$(printf '%s\n' "$out" | tail -3)"; }
gate "bash -n act_slot_proof.sh" bash -n scripts/act_slot_proof.sh
gate "py_compile act_ci.py" python3 -c 'import ast,sys; ast.parse(open("scripts/act_ci.py").read())'
gate "git diff --check 759da623..HEAD" git diff --check 759da623072358afdb0e9d570a7b4b6a788492c9 HEAD
gate "git diff --check 604297bb..HEAD" git diff --check 604297bb41d6c8005d07539289b10bfa99273cdd HEAD
gate "check_py_idiom" python3 scripts/check_py_idiom.py
gate "check_sh_idiom" python3 scripts/check_sh_idiom.py
gate "docs_check" python3 scripts/docs_check.py
gate "check_em_dash --base 759da623" python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
gate "gen_toc --check" python3 scripts/gen_toc.py --check
gate "gen_toc --verify-anchors" python3 scripts/gen_toc.py --verify-anchors
gate "check_doc_paths" python3 scripts/check_doc_paths.py
gate "check_doc_style" python3 scripts/check_doc_style.py
gate "check_baremetal_only --check" python3 scripts/check_baremetal_only.py --check
gate "check_baremetal_only --selftest" python3 scripts/check_baremetal_only.py --selftest
