#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Rerun this reviewer's round-1 to round-3 probes unchanged against a checkout, one log and rc per probe.
# Usage: run_prior_probes.sh <group: light|mutants|reasons> <checkout> <run-root> <evidence-dir> <prior-packets-dir> <receipt-dir> <scratch-dir>
#   <run-root>     holds A/ and B/ measurement directories (A/work/ax7101/gateware, ...)
#   <evidence-dir> review-evidence/234-r1/author/evidence of the public evidence branch
set -u
GROUP=$1; REPO=$(cd "$2" && pwd); RUN=$3; EV=$4; PRIOR=$5; OUT=$(mkdir -p "$6" && cd "$6" && pwd); SCR=$7
export PYTHONDONTWRITEBYTECODE=1
R1=$PRIOR/234-r446-1-packet; R2=$PRIOR/234-r446-2-packet; R3=$PRIOR/234-r446-3-packet
ROUTE=$RUN/A/work/ax7101/gateware
one() {  # name, command...
  local name=$1; shift
  ( cd "$OUT" && "$@" > "$OUT/$name.log" 2>&1; echo $? > "$OUT/$name.rc" ) &
}
case $GROUP in
light)
  mkdir -p "$SCR"/{policy,route,numbers,untested,r447}
  one r1-probe-gate-cli python3 -B "$R1/probe_gate_cli.py" "$REPO"
  one r1-reconcile python3 -B "$R1/reconcile.py" "$REPO" "$EV"
  one r2-partition-rederive python3 -B "$R2/partition_rederive.py" "$REPO" "$EV"
  one r2-probe-malformed-record python3 -B "$R2/probe_malformed_record.py" "$REPO"
  one r2-probe-policy-pin python3 -B "$R2/probe_policy_pin.py" "$REPO" "$SCR/policy"
  one r2-probe-route-status python3 -B "$R2/probe_route_status.py" "$REPO" "$ROUTE" "$SCR/route"
  one r3-probe-r3-numbers python3 -B "$R3/probe_r3_numbers.py" "$REPO" "$ROUTE" "$SCR/numbers"
  one r3-probe-r3-untested python3 -B "$R3/probe_r3_untested.py" "$REPO" "$ROUTE" "$SCR/untested"
  one r3-probe-r447-2-cases python3 -B "$R3/probe_r447_2_cases.py" "$REPO" "$ROUTE" "$SCR/r447"
  one r3-probe-hierarchy-equiv python3 -B "$R3/probe_hierarchy_equiv.py" "$REPO" "$R3/r3-rank-old-0feff20f.py" \
    "$ROUTE/baseline_hierarchy.rpt" "$RUN/A/work/ax7101-ooc/baseline_hierarchy.rpt" \
    "$RUN/A/work/ax7101-ooc10/baseline_hierarchy.rpt" "$RUN/A/work/ax8x8-ooc/baseline_hierarchy.rpt" \
    "$RUN/B/work/ax7101/gateware/baseline_hierarchy.rpt" "$RUN/B/work/ax7101-ooc/baseline_hierarchy.rpt" \
    "$RUN/B/work/ax8x8-ooc/baseline_hierarchy.rpt"
  ;;
mutants)
  one r1-probe-gate-mutants python3 -B "$R1/probe_gate_mutants.py" "$REPO" --jobs 5
  one r2-probe-extra-mutants python3 -B "$R2/probe_extra_mutants.py" "$REPO" --jobs 5
  one r3-probe-r3-mutants python3 -B "$R3/probe_r3_mutants.py" "$REPO" --jobs 5
  ;;
reasons)
  one r1-probe-pr-mutant-reasons python3 -B "$R1/probe_pr_mutant_reasons.py" "$REPO"
  ;;
esac
wait
for rc in "$OUT"/*.rc; do echo "$(basename "$rc" .rc) rc=$(cat "$rc")"; done > "$OUT/summary-$GROUP.txt"
