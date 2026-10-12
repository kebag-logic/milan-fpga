#!/usr/bin/env bash
# Disposable composition fault probes. Each plants one defect in a tracked file,
# runs the gate that should read it, records the rc, and restores the file from HEAD.
# Usage: probes.sh <repo>   (requires a clean checkout; leaves it clean)
set -u
cd "$1" || exit 2
[ -z "$(git status --porcelain)" ] || { echo "dirty checkout"; exit 2; }
probe() { # name file python-edit expect gate...
  local name=$1 file=$2 edit=$3 expect=$4; shift 4
  python3 - "$file" "$edit" <<'PY' || { echo "$name: PLANT-FAILED"; git checkout -q -- "$file"; return; }
import sys,pathlib
p=pathlib.Path(sys.argv[1]); old,new=sys.argv[2].split("=>",1)
t=p.read_text(encoding="utf-8"); assert t.count(old)>=1, "anchor not found"
p.write_text(t.replace(old,new,1),encoding="utf-8")
PY
  "$@" >"$OUT/probe_$name.log" 2>&1; local rc=$?
  git checkout -q -- "$file"
  local verdict; if [ "$expect" = fail ]; then [ $rc -ne 0 ] && verdict=CAUGHT || verdict=MISSED; else verdict="rc=$rc(informational)"; fi
  printf '%-34s rc=%s expect=%s %s\n' "$name" "$rc" "$expect" "$verdict"
}
OUT=${OUT:-/tmp}
probe drop_gate_read_doc scripts/ci_scope.py '    "docs/design/SPLIT_CONTROL_MEMORY.md",
=>' fail python3 scripts/ci_scope.py --selftest
probe drop_scope_case scripts/ci_scope.py '        (["docs/design/SPLIT_CONTROL_MEMORY.md"], True),
=>' info python3 scripts/ci_scope.py --selftest
probe fw_job_if_unscoped .github/workflows/rtl-fast.yml "  firmware-srp-mutants:
    needs: changes
    if: \${{ needs.changes.outputs.rtl == 'true' }}=>  firmware-srp-mutants:
    needs: changes
    if: \${{ needs.changes.outputs.rtl == 'false' }}" fail python3 scripts/ci_events.py --check
probe doc_fw_timeout docs/testing/CI_WORKFLOWS.md "| \`firmware-srp-mutants\` | 45 min |=>| \`firmware-srp-mutants\` | 40 min |" info python3 scripts/ci_events.py --check
probe doc_seven_pages docs/testing/CI_WORKFLOWS.md "Seven pages under=>Six pages under" info python3 scripts/docs_check.py
probe doc_elab_heading docs/testing/CI_WORKFLOWS.md "## Elaboration
=>## Elaboration job
" fail python3 scripts/gen_toc.py --check
probe pr_para_emdash docs/testing/CI_WORKFLOWS.md "The split CPU is its own=>The split CPU — is its own" fail python3 scripts/check_em_dash.py --base dc4d06cbfec209cc2ff76806f4b49c51f46639ae
probe fw_shard_duplicated .github/workflows/rtl-fast.yml "--shard 3/4=>--shard 2/4" fail python3 scripts/ci_events.py --check
git status --porcelain
