#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe for PR #172: run tb/name_state at the shipping name capacity
# (the parent binds DESC_NAME_ENTRIES_P to its generated AEM_NAME_ENTRIES_C,
# the exact name count) and plant a capacity-boundary defect.
#
# usage: capacity_probe.sh CLONE OUTDIR VERILATOR IMG1x1 IMG8x8
#   CLONE   processor checkout at the reviewed head (read only)
#   OUTDIR  new directory for the probe trees, builds and logs
set -eu
clone=$1; out=$2; vl=$3; img1=$4; img8=$5
mkdir "$out"
mk() {  # mk TREE CAPACITY [boundary]
  t=$out/$1
  for d in hdl tb/common tb/pp_top tb/name_state; do
    mkdir -p "$t/$(dirname $d)"; cp -r "$clone/$d" "$t/$d"
  done
  sed -i "s/\.DESC_NAME_ENTRIES_P (128)/.DESC_NAME_ENTRIES_P ($2)/" "$t/tb/name_state/run.py"
  test "$(grep -c "DESC_NAME_ENTRIES_P ($2)" "$t/tb/name_state/run.py")" = 1
  if [ "${3:-}" = boundary ]; then
    # the name trigger drops the table's last entry (ordinal N_NAME_P - 1)
    f=$t/hdl/aecp/KL_aecp_nvm_writer.sv
    old="    if (nchg_i \&\& (32'(nchg_ord_i) < N_NAME_P)) begin"
    test "$(grep -c "if (nchg_i && (32'(nchg_ord_i) < N_NAME_P)) begin" "$f")" = 1
    sed -i "s/$old/    if (nchg_i \&\& (32'(nchg_ord_i) < N_NAME_P - 1)) begin/" "$f"
    test "$(grep -c "N_NAME_P - 1)) begin" "$f")" = 1
  fi
}
mk cap39 39; mk cap107 107; mk cap128-boundary 128 boundary; mk cap39-boundary 39 boundary
run() {  # run TAG TREE ARGS...
  tag=$1; tree=$2; shift 2; mkdir "$out/w-$tag"
  set +e
  python3 "$out/$tree/tb/name_state/run.py" --root "$out/$tree" --verilator "$vl" \
      --work "$out/w-$tag" "$@" > "$out/$tag.log" 2>&1
  echo $? > "$out/$tag.rc"
  set -e
}
run cap39-1x1 cap39 --image "$img1" --aaf 1 &
run cap107-8x8 cap107 --image "$img8" --aaf 8 &
run cap128-boundary-synth cap128-boundary &
run cap39-boundary-1x1 cap39-boundary --image "$img1" --aaf 1 &
wait
for t in cap39-1x1 cap107-8x8 cap128-boundary-synth cap39-boundary-1x1; do
  echo "$t rc=$(cat "$out/$t.rc")"; grep -E '^FAIL|checks:' "$out/$t.log" || true
done
# expected: cap39-1x1 and cap107-8x8 rc 0 (shipping capacity passes);
# cap128-boundary-synth rc 0 (defect SURVIVES the PR's 128-capacity suite);
# cap39-boundary-1x1 rc 1 with N3/N5 ordinal 38 and N6 failing.
