#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# r1_controls_vs_committed.sh JOBS
# Round-1 planted controls (R459-1 scripts/make_controls.py, run UNCHANGED)
# and the round-1 stall probe's defect edit (the same search/replace text as
# R459-1 scripts/run_campaign.sh `stall2`, without the stall) applied to the
# exact head's hdl/srp, then each COMMITTED suite that builds the edited file
# run by its default `make` in a fresh `git archive` of the head: srp_top (all files), srp_stream_fsms (talker,
# listener), srp_admission (admission); pp_top too for the equivalent edits.
# A defect control is killed when the suite exits non-zero with a FAIL: line;
# an equivalent edit must leave every suite passing.
set -u
J=${1:-6}
P=${P:-$(cd "$(dirname "$0")/.." && pwd)}
. "$P/scripts/env.sh"
CLONE=${CLONE:?set CLONE to a clone that holds the exact head}
H=$S/head; C=$S/ctl; T=$S/ct
rm -rf "$C" "$T"; mkdir -p "$C" "$T"
python3 "$S/r1/scripts/make_controls.py" "$H/hdl/srp" "$C"
# the stall probe's defect, without the stall (R459-1 run_campaign.sh stall2)
python3 - "$H/hdl/srp" "$C" <<'PY'
import pathlib, shutil, sys
h, c = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
d = c / "tf-tk-write-ignores-full" / "srp"
shutil.copytree(h, d)
s = (d / "KL_srp_top.sv").read_text()
a = "    if (tf_push_w[0]) begin\n      tf_tk_ram_r"; assert s.count(a) == 1
(d / "KL_srp_top.sv").write_text(s.replace(a, "    if (tk_arm_v_w) begin\n      tf_tk_ram_r"))
with open(c / "controls.tsv", "a") as f:
    f.write("tf-tk-write-ignores-full\tcatch\tKL_srp_top.sv\n")
PY
jobs=$T/jobs.txt; : > "$jobs"
while IFS=$'\t' read -r name expect f; do
  t=$T/$name
  mkdir -p "$t"
  git -C "$CLONE" archive "$HEAD" | tar -x -C "$t"
  rm -rf "$t/hdl/srp"; cp -r "$C/$name/srp" "$t/hdl/srp"
  diff -rq "$H/hdl/srp" "$t/hdl/srp" > "$t/edit.diffq"
  suites="srp_top"
  case $f in
    KL_srp_talker_fsm.sv|KL_srp_listener_fsm.sv) suites="$suites srp_stream_fsms" ;;
    KL_srp_admission.sv) suites="$suites srp_admission" ;;
  esac
  [ "$expect" = equiv ] && suites="$suites pp_top"
  for s in $suites; do
    echo "$name $expect $s" >> "$jobs"
  done
done < "$C/controls.tsv"
xargs -P "$J" -L 1 bash -c 'n=$0; e=$1; s=$2; d='"$T"'/$n; make -C "$d/tb/$s" > "$d/$s.log" 2>&1; echo $? > "$d/$s.rc"' < "$jobs"
echo "controls done"
