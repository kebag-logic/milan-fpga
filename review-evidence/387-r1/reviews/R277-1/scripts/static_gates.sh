#!/bin/sh
# Focused static gates over the pages, diagrams, build files and harness the
# PR changes. Each command runs from the clone root; its exit status is
# recorded, never discarded. Usage: static_gates.sh <clone>
set -u
cd "$1" || exit 2
overall=0
run() {
  printf '### %s\n' "$*"
  "$@" > /tmp/.sg_out_$$ 2>&1
  st=$?
  tail -n 12 /tmp/.sg_out_$$
  printf '### exit %s: %s\n\n' "$st" "$*"
  [ "$st" = 0 ] || overall=1
  rm -f /tmp/.sg_out_$$
}
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
run python3 scripts/check_doc_style.py
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_gptp_docs.py --with-submodule
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_feature_status.py
run python3 scripts/check_doc_paths.py
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_hygiene.py --check
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/pp_srcs.py --check
echo "static_gates overall=$overall"
exit $overall
