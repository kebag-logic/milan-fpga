#!/usr/bin/env bash
# Two disposable mutants of the processor pin, each built and run in its own
# scratch export, in parallel; each must FAIL the section it targets.
#  m1_fail_aem_status : non-AEM response-memory failure answers as at b2db3a97
#                       (ENTITY_MISBEHAVING, no echo) -> DL8/DL9 must fail
#  m2_rb_keeps_cfg    : the configuration-valid flag ignores the D3 roll-back
#                       reset -> AD6 must fail
# Usage: pp_mutants.sh <clone> <scratch> <outdir> <verilator>
set -u
clone=$1; scr=$2; out=$3; V=$4; mkdir -p "$out"
E=hdl/aecp/KL_aecp_engine.sv
one() {
  name=$1 sect=$2; d="$scr/$name"; rm -rf "$d"; mkdir -p "$d"
  git -C "$clone/protocol-processor" archive 631eeb342ca1e3fa80e734077a56a943aee76ff1 | tar -x -C "$d"
  case $name in
    m1_fail_aem_status)
      # both fail-path branches (A_ALLOC, A_WR) gated off: `if (st_echo_w) begin`
      sed -i 's/^\(            \)if (st_echo_w) begin$/\1if (1'"'"'b0 \&\& st_echo_w) begin/' "$d/$E" ;;
    m2_rb_keeps_cfg)
      sed -i 's/^    if (!store_rst_n_w) begin$/    if (!rst_n) begin/' "$d/$E" ;;
  esac
  diff -u "$clone/protocol-processor/$E" "$d/$E" >"$out/$name.patch"
  n=$(grep -c '^+[^+]' "$out/$name.patch"); echo "$n" >"$out/$name.edits"
  ( cd "$d/tb/pp_top" && make VERILATOR="$V" gsi-build >"$out/$name.build.log" 2>&1 \
      && ./obj_dir/Vpp_top_sim "$sect" >"$out/$name.run.log" 2>&1; echo $? >"$out/$name.rc" )
}
one m1_fail_aem_status --deadline-only &
one m2_rb_keeps_cfg --adp-only &
wait
for n in m1_fail_aem_status m2_rb_keeps_cfg; do
  printf '%s edits=%s rc=%s : %s\n' "$n" "$(cat "$out/$n.edits")" "$(cat "$out/$n.rc")" \
    "$(tail -n 1 "$out/$n.run.log" 2>/dev/null)"
done
