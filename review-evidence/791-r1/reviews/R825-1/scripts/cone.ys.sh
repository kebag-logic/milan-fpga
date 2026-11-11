#!/bin/bash
# cone.ys.sh <netlist.v> <out-cone.v>: cut the CPU's fetch and load PMA fault terms out of a VexiiRiscv netlist,
# with the PMA command address/size/op as free inputs, independent of decode.py. Refuses a cone holding state.
set -e
NL=$1; OUT=$2
yosys -q -l "$OUT.log" -p "
read_verilog $NL
hierarchy -top VexiiRiscv
proc
cd VexiiRiscv
setattr -set keep 1 w:FetchL1Plugin_logic_ctrl_pmaPort_cmd_address w:LsuCachelessPlugin_logic_onPma_port_cmd_address w:LsuCachelessPlugin_logic_onPma_port_cmd_size w:LsuCachelessPlugin_logic_onPma_port_cmd_op w:FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault w:LsuCachelessPlugin_logic_onPma_port_rsp_fault
opt_clean
expose -cut w:FetchL1Plugin_logic_ctrl_pmaPort_cmd_address w:LsuCachelessPlugin_logic_onPma_port_cmd_address w:LsuCachelessPlugin_logic_onPma_port_cmd_size w:LsuCachelessPlugin_logic_onPma_port_cmd_op
expose w:FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault w:LsuCachelessPlugin_logic_onPma_port_rsp_fault
select -set cone w:FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault w:LsuCachelessPlugin_logic_onPma_port_rsp_fault %ci*
select -set state t:\$*dff* t:\$mem* t:\$*latch* %u %u
select -assert-none @cone @state %i
select -set cells @cone %C
tee -o $OUT.stat stat @cone
delete * @cone %d
cd ..
select -clear
rename VexiiRiscv pma_cone
opt_clean -purge pma_cone
tee -o $OUT.ports select -list pma_cone/i:* pma_cone/o:*
select pma_cone
write_verilog -noattr -selected $OUT
"
