#!/bin/bash
# Usage: run_static.sh <clone> <packet> -- detached differential and static checks, logs/rc in receipts.
set -u
C=$1; P=$2; S=$P/scratch; R=$P/receipts
export PATH=$S/bin:$PATH VERILATOR=$S/bin/verilator TMPDIR=$S/tmp VERILATOR_JOBS=4
cd "$C"
job() { n=$1; shift; ( "$@" >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc" ) & }
job differential python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$S/differential"
job lint         python3 scripts/lint_rtl.py --check --jobs 4
job baseline     python3 syn/ooc/pp_resource_gate.py check-baseline
job docs_check   python3 scripts/docs_check.py
job gen_toc      python3 scripts/gen_toc.py --check
job em_dash      python3 scripts/check_em_dash.py --base 6aa25dec977c6ad78bf4ff6275de47fb81d0c246
job evidence     python3 scripts/measure_test_evidence.py --check
wait
