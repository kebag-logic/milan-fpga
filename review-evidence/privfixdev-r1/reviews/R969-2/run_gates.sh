#!/bin/bash
# Run the focused gates for PR #1030 in parallel; each gate writes logs/<name>.log and logs/<name>.rc.
# usage: run_gates.sh <head-clone> <base-tree> <out-dir>
H=$1; B=$2; O=$3; mkdir -p "$O"
g() { local n=$1 d=$2; shift 2; ( cd "$d" && "$@" ) > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc"; }
BASE=e275d7950ef3385753e6a15d2e191ba855b171ed
g doc_style        "$H" python3 -I scripts/check_doc_style.py &
g doc_style_self   "$H" python3 -I scripts/check_doc_style.py --selftest &
g em_dash          "$H" python3 -I scripts/check_em_dash.py --base $BASE &
g em_dash_self     "$H" python3 -I scripts/check_em_dash.py --selftest &
g toc_check        "$H" python3 -I scripts/gen_toc.py --check &
g toc_anchors      "$H" python3 -I scripts/gen_toc.py --verify-anchors &
g doc_paths        "$H" python3 -I scripts/check_doc_paths.py &
g docs_check       "$H" python3 -I scripts/docs_check.py &
g hygiene          "$H" python3 -I scripts/check_hygiene.py --check &
g py_idiom         "$H" python3 -I scripts/check_py_idiom.py &
g sh_idiom         "$H" python3 -I scripts/check_sh_idiom.py &
g bash_n           "$H" bash -n tb/tools/check_tu_on_wire.sh &
g baremetal_check  "$H" python3 -I scripts/check_baremetal_only.py --check &
g baremetal_self   "$H" python3 -I scripts/check_baremetal_only.py --selftest &
g baremetal_self_base "$B" python3 -I scripts/check_baremetal_only.py --selftest &
g wire_truth_self  "$H" python3 -I tb/tools/avtp_wire_truth.py --self-test &
g wire_truth_self_base "$B" python3 -I tb/tools/avtp_wire_truth.py --self-test &
g torture_self     "$H" python3 -I tb/tools/torture_campaign.py --self-test &
g torture_self_base "$B" python3 -I tb/tools/torture_campaign.py --self-test &
g behave_touched   "$H/tests" behave -f progress features/milan_streaming_licence.feature features/torture_campaign_plan.feature features/wire_truth_avtp.feature &
g behave_touched_base "$B/tests" behave -f progress features/milan_streaming_licence.feature features/torture_campaign_plan.feature features/wire_truth_avtp.feature &
wait
for f in "$O"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done
