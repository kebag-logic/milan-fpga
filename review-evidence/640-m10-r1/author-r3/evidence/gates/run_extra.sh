#!/usr/bin/env bash
# The gate-read pages' readers and the census coverage steps, on the clean clone, after run_all.sh.
G=$VALIDATION_STORAGE/640-a720m/gates
E=$MANAGEMENT/2026-09-23/640-a720l/evidence/census
export PATH="$G/venv/bin:$PATH" RUNNER_TEMP=$G/runner_temp TMPDIR=$G/tmpdir
cd $G/wt
run() { local id="$1"; shift; ( set -o pipefail; timeout 560 bash -c "$*" ) > $G/logs/$id.log 2>&1; local rc=$?; echo $rc > $G/logs/$id.rc; printf '%s\trc=%s\t%s\n' $id $rc "$(tail -1 $G/logs/$id.log | cut -c1-140)"; }
run reader_check_baseline "python3 syn/ooc/pp_resource_gate.py check-baseline"
run reader_service_bounds "rm -rf $G/sb_out && python3 -I $G/service_bounds_arm.py $G/wt $G/sb_out"
run census_coverage "python3 -I $E/census_coverage.py $G/wt $E/basis_soc_hierarchy.txt $E/basis_csr.csv $E/basis_place_top_excerpt.rpt"
C=$G/control_r1; rm -rf $C; mkdir -p $C/docs/design $C/sw/litex
git -C $G/wt show 3f8ed303:docs/design/MARK_II_AREA_PLAN.md > $C/docs/design/MARK_II_AREA_PLAN.md
cp $G/wt/sw/litex/milan_soc.py $C/sw/litex/
run census_coverage_control "! python3 -I $E/census_coverage.py $C $E/basis_soc_hierarchy.txt $E/basis_csr.csv $E/basis_place_top_excerpt.rpt"
git -C $G/wt status --short > $G/logs/final_status_extra.txt
