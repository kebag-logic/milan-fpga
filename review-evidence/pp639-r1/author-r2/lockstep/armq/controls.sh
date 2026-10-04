#!/bin/sh
# controls.sh <head top.sv>: one mutated extract per planted control
set -e
H="$1"
x() { name=$1; shift; python3 extract.py "$H" armq_dut ctl_$name.sv "$@"; }
x wr_at_head   --mutate 'assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];' 'assign wr_ix_w = armq_hd_r[g];'
x wr_at_mid    --mutate 'assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];' 'assign wr_ix_w = armq_hd_r[g] + armq_mid_w[g][1:0];'
x head_stuck   --mutate 'armq_hd_r[i]         <= armq_hd_r[i] + 2'"'"'d1;' 'armq_hd_r[i]         <= armq_hd_r[i];'
x read_tail    --mutate 'assign armq_hd_w[g] = mem_r[armq_hd_r[g]];' 'assign armq_hd_w[g] = mem_r[wr_ix_w];'
x write_refused --mutate 'if (armq_push_ok_w[g]) mem_r[wr_ix_w]' 'if (armq_in_vld_w[g]) mem_r[wr_ix_w]'
x ring_of_three --mutate 'armq_hd_r[i]         <= armq_hd_r[i] + 2'"'"'d1;' 'armq_hd_r[i]         <= (armq_hd_r[i] == 2'"'"'d2) ? 2'"'"'d0 : armq_hd_r[i] + 2'"'"'d1;'
# not a control: the head index is not reset (the ring may start anywhere)
x probe_head_unreset --mutate 'armq_hd_r  <= '"'"'0;' '/* head not reset */'
