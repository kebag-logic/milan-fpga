#!/usr/bin/env bash
# ooc_term.sh <src>: the bound-talker term out of context, at one and two interfaces, head and term-tied-off,
# with the mailbox's recipe (docs/design/MAILBOX_SPLIT.md, Measured area). One Vivado at a time.
set -u
L=$1; S=<scratch>; O=$S/ooc
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd "$L" || exit 3
head=$(git rev-parse HEAD)
R=hdl/milan/mailbox
python3 -B sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out "$O/if2-gen" > "$O/if2-gen.log" 2>&1 || exit 4
for n in 1 2; do for v in head tied; do
  d=$O/if$n-$v; rm -rf "$d"; mkdir -p "$d/src"
  cp $R/KL_mbx_pkg.sv $R/KL_mbx_ring.sv $R/KL_mbx_rx.sv $R/KL_mbx_tx.sv $R/KL_mbx_evt.sv $R/KL_mbx.sv \
     $R/KL_mbx_wb.sv $R/KL_mbx_axil.sv tb/verilator/mbx/tb_mbx_top.sv "$d/src/"
  [ $n = 2 ] && cp "$O/if2-gen/KL_mbx_pkg.sv" "$O/if2-gen/KL_mbx.sv" "$d/src/"
  if [ $v = tied ]; then
    python3 - "$d/src" <<'PY' || exit 5
import sys
from pathlib import Path
src = Path(sys.argv[1])
for name, old, new in (
        ("KL_mbx_rx.sv", "  assign bound_hit_w = |(match_r & live_w);", "  assign bound_hit_w = 1'b0;"),
        ("KL_mbx.sv", "    .bnd_req_i       (host_req_i && bnd_at_w),", "    .bnd_req_i       (1'b0),"),
        ("KL_mbx.sv", "    .bnd_we_i        (wr_w && bnd_at_w),", "    .bnd_we_i        (1'b0),")):
    p = src / name
    t = p.read_text()
    assert t.count(old) == 1, (name, old)
    p.write_text(t.replace(old, new))
PY
  fi
  cat > "$d/ooc.tcl" <<TCL
read_verilog -sv [list src/KL_mbx_pkg.sv src/KL_mbx_ring.sv src/KL_mbx_rx.sv src/KL_mbx_tx.sv src/KL_mbx_evt.sv \
  src/KL_mbx.sv src/KL_mbx_wb.sv src/KL_mbx_axil.sv src/tb_mbx_top.sv]
synth_design -mode out_of_context -top tb_mbx_top -part xc7a100tfgg484-2 -generic HOST_P=0
create_clock -period 10.000 -name clk [get_ports clk_i]
opt_design
place_design
route_design
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_route_status -file route_status.rpt
TCL
  ( cd "$d" && sha256sum src/* > src.sha256 && vivado -mode batch -nojournal -nolog -source ooc.tcl > vivado.out 2>&1; echo $? > rc )
  echo "if$n $v rc=$(cat $d/rc) head=$head"
done; done
echo done > "$O/DONE"
