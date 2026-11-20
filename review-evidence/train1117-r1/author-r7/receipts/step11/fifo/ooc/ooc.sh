#!/bin/bash
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd <scratch>/r5fifo/ooc && vivado -mode batch -source ooc.tcl -nojournal -log ooc.log > ooc.out 2>&1; echo $? > ooc.rc
