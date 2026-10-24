#!/usr/bin/env bash
# Review R695-1 of PR #783 (issue #780) at exact head
# 25f05752f7e50e3cf7e27008e434ffde930b4b6f: the commands this round ran.
#
# Usage: run_r695_1.sh <clean clone at the head> <packet dir> <verilator 5.050> <sv2v dir>
# Every probe runs in a disposable copy under <packet>/scratch; the clone
# named first is only read.
set -euo pipefail
SRC=$(cd "$1" && pwd); PKT=$(cd "$2" && pwd); V=$3; SV=$4
S=$PKT/scratch; R=$PKT/receipts; mkdir -p "$S" "$R"
test "$(git -C "$SRC" rev-parse HEAD)" = 25f05752f7e50e3cf7e27008e434ffde930b4b6f
test "$(git -C "$SRC" rev-parse HEAD:protocol-processor)" = ed2118035e4cec76fb1b59cfbf8a053aeacc8af8
test "$(git -C "$SRC" rev-parse HEAD:gptp-processor)" = 55680bff3b287b9a7b0c759f51471fa617c17335
for d in plain head old checks rom; do rm -rf "${S:?}/$d"; cp -a "$SRC" "$S/$d"; done
git -C "$S/old/protocol-processor" checkout -q 93fb0b2d736b36588ea7321e25fba2f8819ea41f
python3 -I "$PKT/scripts/gavb_probe.py" "$S/head/tb/verilator/pp_shadow/sim_main.cpp"
python3 -I "$PKT/scripts/gavb_probe.py" "$S/old/tb/verilator/pp_shadow/sim_main.cpp"

job() { local n=$1 d=$2; shift 2; ( cd "$d" && bash -c "$*" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
job pp_shadow_base_head "$S/plain" "make -C tb/verilator/pp_shadow run-base VERILATOR=$V VERILATOR_JOBS=3"
job probe_gavb_head     "$S/head"  "make -C tb/verilator/pp_shadow run-base VERILATOR=$V VERILATOR_JOBS=3"
job probe_gavb_old93fb  "$S/old"   "make -C tb/verilator/pp_shadow run-base VERILATOR=$V VERILATOR_JOBS=3"
job behave_head         "$S/plain" "cd tests && behave --no-capture -f plain"
job rom_record          "$S/rom"   "bash syn/yosys/ooc.sh --record-rom-digests && git diff --exit-code syn/yosys/rom_digests.tsv && git status --short"
wait

python3 -P "$PKT/scripts/probe_behave_model_gavb.py" "$S/plain" > "$R/probe_behave_model_gavb.txt"

( cd "$S/checks"
  : > "$R/pincheck_summary.tsv"; i=0
  for c in "python3 syn/ooc/pp_resource_gate.py check-baseline" \
           "python3 docs/diagrams/submodule_boundaries.gen.py --check" \
           "python3 docs/diagrams/timesync_chain.gen.py --check" \
           "python3 scripts/check_submodule_docs.py" \
           "python3 scripts/check_gptp_docs.py --with-submodule" \
           "python3 scripts/check_port_contracts.py" \
           "python3 scripts/measure_naming.py --check" \
           "python3 scripts/measure_test_evidence.py --check" \
           "python3 protocol-processor/scripts/check-integrator-params.py" \
           "python3 scripts/lint_rtl.py --check"; do
    i=$((i+1)); rc=0; $c > "$R/pincheck_$i.log" 2>&1 || rc=$?
    printf '%s\trc=%s\n' "$c" "$rc" >> "$R/pincheck_summary.tsv"
  done )

# ROM ledger rows are consulted at this pin: verify, then a planted wrong row must refuse.
( cd "$S/rom"
  rc=0; PATH=$SV:$PATH bash syn/yosys/ooc.sh tcam > "$R/ooc_tcam_digest_verify.log" 2>&1 || rc=$?; echo $rc > "$R/ooc_tcam_digest_verify.rc"
  sed -i 's/^\(ed2118035e4cec76fb1b59cfbf8a053aeacc8af8\tucode.hex\t\)1f/\100/' syn/yosys/rom_digests.tsv
  rc=0; PATH=$SV:$PATH bash syn/yosys/ooc.sh tcam > "$R/ooc_tcam_digest_mutant.log" 2>&1 || rc=$?; echo "mutant rc=$rc" > "$R/ooc_tcam_digest_mutant.rc"
  git checkout -- syn/yosys/rom_digests.tsv )

# milan_dp at the head (sim_pool accepts SIM_JOBS 1 or 2 only).
( cd "$S/plain" && rc=0 && make -j6 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2 VERILATOR="$V" > "$R/milan_dp_head.log" 2>&1 || rc=$?; echo $rc > "$R/milan_dp_head.rc" )
