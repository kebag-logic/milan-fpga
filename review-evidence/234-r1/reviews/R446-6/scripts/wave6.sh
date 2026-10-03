#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer round-6 launcher: start one wave of independent campaigns detached, one raw log and rc file each.
# Usage: wave6.sh <1|2|3> <checkout> <packet> <run-root>
#   wave 1: gates (run_gates.sh), the round-5 names probe, the round-6 list probe, three fuzz runs
#   wave 2: round-4/5 case probes, the round-6 generator probe, the real-data checks, prior probe groups light and
#           reasons, the round-4 generative probe
#   wave 3: prior probe group mutants, the round-5 equivalence probe (needs wave 1's names scratch)
# <run-root> holds symlink mirrors A/ and B/ of the measurement directories; nothing under it is written.
set -u
WAVE=$1; REPO=$(cd "$2" && pwd); P=$(cd "$3" && pwd); RUN=$(cd "$4" && pwd)
S=$P/scratch; R=$P/receipts; SC=$P/scripts
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$R"/{gates,r4-probes,r5-probes,r6-probes,fuzz,real,prior-probes} "$S"
start() {  # name, receipt-subdir, command...
  local name=$1 dir=$2; shift 2
  setsid nohup bash -c '"$@" > "$0.raw" 2>&1; echo $? > "$0.rc"' "$R/$dir/$name" "$@" < /dev/null > /dev/null 2>&1 &
}
GATE="python3 $REPO/syn/ooc/pp_resource_gate.py"
case $WAVE in
1)
  start gates-runner gates env PYTHON_CPU_COUNT=4 bash "$SC/run_gates.sh" "$REPO" "$R/gates" "$S/make43/bin" 4
  start probe-r5-names r5-probes python3 -B "$SC/probe_r5_names.py" "$REPO" "$S/names5" --jobs 4
  start probe-r6-lists r6-probes python3 -B "$SC/probe_r6_lists.py" "$REPO" "$S/lists6" --jobs 4
  start fuzz-fixtures-20000 fuzz $GATE --fuzz 20000
  start fuzz-A-route-20000 fuzz $GATE --fuzz 20000 check "$RUN/A/work/ax7101/gateware" --endpoint route-1x1
  start fuzz-A-ooc-1x1-5000 fuzz $GATE --fuzz 5000 check "$RUN/A/work/ax7101-ooc" --endpoint ooc-1x1
  ;;
2)
  start probe-r4-generative r4-probes python3 -B "$SC/probe_r4_generative.py" "$REPO" "$S/gen" --jobs 3
  start probe-r4-structure r4-probes python3 -B "$SC/probe_r4_structure.py" "$REPO" "$RUN/A/work/ax7101/gateware" "$S/structure"
  start probe-r4-adhoc r4-probes python3 -B "$SC/probe_r4_adhoc.py" "$REPO" "$RUN" \
    "$S/ev/review-evidence/234-r1/author/evidence" "$S/armq-census.tsv" "$S/adhoc"
  start probe-r447-3-cases r4-probes python3 -B "$SC/probe_r447_3_cases.py" "$REPO" "$RUN/B/work/ax7101/gateware" "$S/r447"
  start probe-r5-cases r5-probes python3 -B "$SC/probe_r5_cases.py" "$REPO" "$RUN/A/work/ax7101/gateware" "$S/cases5"
  start probe-r6-generator r6-probes python3 -B "$SC/probe_r6_generator.py" "$REPO" "$S/gen6full" 20000
  start prior-light prior-probes bash "$SC/run_prior_probes.sh" light "$REPO" "$RUN" \
    "$S/ev/review-evidence/234-r1/author/evidence" "$(dirname "$P")" "$R/prior-probes" "$S/prior"
  start prior-reasons prior-probes bash "$SC/run_prior_probes.sh" reasons "$REPO" "$RUN" \
    "$S/ev/review-evidence/234-r1/author/evidence" "$(dirname "$P")" "$R/prior-probes" "$S/prior"
  for spec in "A-route A/work/ax7101/gateware route-1x1" "A-ooc-1x1 A/work/ax7101-ooc ooc-1x1" \
      "A-ooc-8x8 A/work/ax8x8-ooc ooc-8x8" "A-ooc-1x1-10ns A/work/ax7101-ooc10 ooc-1x1" \
      "B-route B/work/ax7101/gateware route-1x1" "B-ooc-1x1 B/work/ax7101-ooc ooc-1x1" \
      "B-ooc-8x8 B/work/ax8x8-ooc ooc-8x8"; do
    set -- $spec
    start "$1" real bash -c 'cd "$0" && python3 syn/ooc/pp_resource_gate.py check "$1" --endpoint "$2"' "$REPO" "$RUN/$2" "$3"
  done
  start check-baseline real bash -c 'cd "$0" && python3 syn/ooc/pp_resource_gate.py check-baseline' "$REPO"
  ;;
3)
  start prior-mutants prior-probes bash "$SC/run_prior_probes.sh" mutants "$REPO" "$RUN" \
    "$S/ev/review-evidence/234-r1/author/evidence" "$(dirname "$P")" "$R/prior-probes" "$S/prior"
  start probe-r5-equiv r5-probes python3 -B "$SC/probe_r5_equiv.py" "$REPO" "$S/names5" "$S/equiv5"
  ;;
esac
echo "wave $WAVE started $(date -u +%FT%TZ)" >> "$R/waves.txt"
