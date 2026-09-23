#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Every R259-3 receipt, in order, in the foreground. Needs DATA (see env.sh),
# git, python3 and the pinned Verilator 5.050 wrapper. Writes only under the
# packet's receipts/ and scratch/; the reviewed clone is read, never written.
set -u
here=$(cd "$(dirname "$0")" && pwd)
. "$here/env.sh"
cd "$PACKET" || exit 2
rm -rf "$SCRATCH"/rom-* "$SCRATCH"/mp-*
R="sh $here/receipt.sh"
rc=0
$R identity-start sh "$here/identity.sh" || rc=1
$R rom-check python3 "$here/rom_check.py" || rc=1
$R rom-word-diff sh "$here/rom_word_diff.sh" || rc=1
$R servo-arith-model python3 "$here/servo_arith_model.py" || rc=1
$R docs-gates-head sh "$here/docs_gates.sh" || rc=1
$R engine-suite-head sh "$here/engine_suite.sh" "$HEAD_SHA" suite-head || rc=1
$R rom-consumer-suites-head sh "$here/rom_consumer_suites.sh" || rc=1
git -C "$CLONE" show "$PREV_SHA:hdl/ucode/gen_gptp_ucode.py" > "$SCRATCH/gen_cbccf22.py"
git -C "$CLONE" show "$BASE_SHA:hdl/ucode/gen_gptp_ucode.py" > "$SCRATCH/gen_base.py"
MP_WORK="$SCRATCH/mp-suite" \
MP_OTHER_GENS="cbccf22=$SCRATCH/gen_cbccf22.py:base c1b6174=$SCRATCH/gen_base.py" \
  $R mutation-suite-head python3 "$here/mutation_probe.py" \
  "$SCRATCH/suite-head/tb/verilator/engine/obj_dir/Vengine_sim" "$SCRATCH/suite-head" --set all
# exit 1 above is expected: one reviewer mutant (RV5) survives; see REPORT.md S1
$R probe-build sh "$here/probe_build.sh" || rc=1
MP_WORK="$SCRATCH/mp-probe" $R probe-phases-head python3 "$here/mutation_probe.py" \
  "$SCRATCH/probe-head/tb/verilator/engine/obj_dir/Vengine_probe" "$SCRATCH/probe-head" --set probe || rc=1
$R identity-end sh "$here/identity.sh" || rc=1
exit $rc
