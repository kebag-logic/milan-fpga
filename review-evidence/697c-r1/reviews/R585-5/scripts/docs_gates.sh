#!/bin/bash
# Run the docs-job gates this PR's files touch, on a clone WITHOUT submodules
# (as the hosted docs job runs its first gates), one log line per gate.
# Usage: docs_gates.sh TREE BASE PYTHON OUT
set -u
tree=$1; base=$2; py=$3; out=$4
mkdir -p "$out"
cd "$tree" || exit 2
: > "$out/summary.txt"
g() { name=$1; shift; "$@" > "$out/$name.log" 2>&1; echo "$name rc=$?" | tee -a "$out/summary.txt"; }
g docs_check            $py scripts/docs_check.py
g em_dash               $py scripts/check_em_dash.py --base "$base"
g em_dash_selftest      $py scripts/check_em_dash.py --selftest
g doc_style             $py scripts/check_doc_style.py
g submodule_diagram     $py docs/diagrams/submodule_boundaries.gen.py --check
g submodule_diagram_st  $py docs/diagrams/submodule_boundaries.gen.py --selftest
g submodule_docs        $py scripts/check_submodule_docs.py
g submodule_docs_st     $py scripts/check_submodule_docs.py --selftest
g diagram_pngs          $py scripts/check_diagram_pngs.py
g gen_toc_check         $py scripts/gen_toc.py --check
g ci_events_check       $py scripts/ci_events.py --check
g ci_scope_selftest     $py scripts/ci_scope.py --selftest
g py_idiom              $py scripts/check_py_idiom.py
g baremetal_only        $py scripts/check_baremetal_only.py --check
