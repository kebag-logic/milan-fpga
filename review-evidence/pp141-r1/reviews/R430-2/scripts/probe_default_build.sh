#!/bin/sh
# usage: probe_default_build.sh EXPORT ARM   (ARM = sclks-bound-three | clks_row_two_bits | none)
# Plants one D3C negative control in a disposable export of the head and runs the
# whole default build of tb/pp_top (every section), printing every FAIL line.
set -e
t=$1; arm=$2; cd "$t"
case $arm in
  sclks-bound-three) git apply tb/pp_top/aecp_dispatch_mutations/sclks-bound-three.patch ;;
  clks_row_two_bits) python3 - <<'PY'
from pathlib import Path
p = Path("hdl/aecp/KL_aecp_dyn_state.sv"); s = p.read_text()
old = "          13'(SEL_CLKSRC_C): begin clksrc_r[cd_ix_w]  <= st_wdata_i[15:0];\n"
new = "          13'(SEL_CLKSRC_C): begin clksrc_r[cd_ix_w]  <= {14'd0, st_wdata_i[1:0]};\n"
assert s.count(old) == 1; p.write_text(s.replace(old, new))
PY
  ;;
  none) ;;
esac
cd tb/pp_top; make gsi-build >build.log 2>&1
set +e; ./obj_dir/Vpp_top_sim > sim.log 2>&1; echo "sim rc=$?"
grep -c '^FAIL' sim.log | sed 's/^/FAIL lines: /'; grep '^FAIL' sim.log; tail -2 sim.log
