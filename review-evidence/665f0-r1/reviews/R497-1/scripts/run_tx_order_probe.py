#!/usr/bin/env python3
"""Reuse the already-built, unchanged Wishbone RTL model from run_focused.py."""
import pathlib,re,subprocess,sys
p=pathlib.Path(__file__).resolve().parents[1]; r=pathlib.Path(sys.argv[1]).resolve()
obj=p/'scratch/cosim-tree/tb/verilator/mbx/obj_cosim'
root=pathlib.Path(re.search(r'^VERILATOR_ROOT = (.*)$',(obj/'Vtb_mbx_top.mk').read_text(),re.M)[1])
exe=p/'scratch/tx-order-probe'
cmd=['g++','-std=c++17','-O2','-pthread','-I'+str(obj),'-I'+str(root/'include'),'-I'+str(root/'include/vltstd'),'-I'+str(r/'tb/verilator/mbx'),'-I'+str(r/'sw/firmware/ctrl/mbx'),str(p/'scripts/tx_order_probe.cpp'),str(obj/'Vtb_mbx_top__ALL.a'),str(obj/'verilated.o'),str(obj/'verilated_threads.o'),'-o',str(exe)]
subprocess.run(cmd,check=True)
sys.exit(subprocess.run([str(exe)]).returncode)
