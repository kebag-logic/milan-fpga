#!/usr/bin/env bash
# Probe: what sw/builder/endstation_builder.py actually refuses for the
# bare-metal profile and for clocks. Runs against a read-only checkout;
# writes only under $OUT. Usage: probe_builder_clock_and_profile.sh <repo> <out>
set -u
REPO=$1; OUT=$(realpath -m "$2")
mkdir -p "$OUT"
BASE="$REPO/configs/endstation_ax7101_8x8.yaml"
run() { # name, sed-expression-or-append
  local name=$1; shift
  local cfg="$REPO/configs/.probe_${name}.yaml"
  cp "$BASE" "$cfg"
  "$@" "$cfg"
  local od="$OUT/$name"; rm -rf "$od"; mkdir -p "$od"
  ( cd "$REPO" && python3 -B sw/builder/endstation_builder.py "$cfg" -o "$od" ) >"$OUT/$name.log" 2>&1
  local rc=$?
  rm -f "$cfg"; rm -rf "$REPO/configs/generated/.probe_${name}"  # builder always writes gen/ here
  local msg; msg=$(grep -m1 -i 'error\|must\|requires\|not none' "$OUT/$name.log" | cut -c1-160)
  printf '%-28s rc=%d %s\n' "$name" "$rc" "$msg"
}
clk() { sed -i "s/^\(    milan_clk_hz: \)[0-9]*/\1$1/" "$2"; }
run baseline_50MHz       true
run milan_75MHz          clk 75000000
run milan_100MHz         clk 100000000
run milan_33MHz          clk 33000000
run milan_62p5MHz        clk 62500000
run milan_gt_sys_150MHz  clk 150000000
run milan_12p345678MHz  clk 12345678
run milan_1MHz          clk 1000000
run flashboot_linux      sed -i 's/^\(    flashboot: \)baremetal/\1linux/'
run flashboot_none       sed -i 's/^\(    flashboot: \)baremetal/\1none/'
run l2_4096              sed -i 's/^\(    l2_bytes: \)0/\14096/'
addsoc() { printf 'soc:\n%s\n' "$1" >> "$2"; }
run soc_scala_noncache   addsoc '  scala_args: ["alu-count=1"]'
run soc_scala_cache      addsoc '  scala_args: ["lsu-l1-sets=64"]'
run soc_with_fpu_key     addsoc '  with_fpu: true'
run soc_xlen64           addsoc '  xlen: 64'
run soc_cpu_count2       addsoc '  cpu_count: 2'
run soc_naxriscv         addsoc '  cpu: naxriscv'
