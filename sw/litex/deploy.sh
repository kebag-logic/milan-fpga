#!/usr/bin/env bash
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Turnkey deploy for the Alinx AX7101: build the full Milan SoC bitstream, program it
# over JTAG, and open the console. Verified hardware wiring (identify by stable by-id;
# the /dev/ttyUSBn numbers flip on re-plug):
#   JTAG    = Digilent FT232H (0403:6014)  -> openFPGALoader -c ft232 (IDCODE = xc7a100t)
#   console = Silicon Labs CP2102N (10c4:ea60)
#
#   deploy.sh [all|build|load|console]     (default: all)
#     BAUD=115200   console baud (our SoC default; the factory demo is 9600)
#
# NOTE: `build` needs Vivado with Artix-7 device support (this host has only Spartan-7,
# so build is currently gated). `load` + `console` work today against any built .bit.
set -euo pipefail

HERE="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
STEP="${1:-all}"
BAUD="${BAUD:-115200}"
CONSOLE="$(ls /dev/serial/by-id/*CP2102* 2>/dev/null | head -1 || echo /dev/ttyUSB0)"

# All fabric blocks (NIC+DMA+MAC+DDR3), datapath in its own 50 MHz domain so sys+DDR3
# close a clean 100 MHz (see docs/TROUBLESHOOTING.md §16); --timing-opt for margin.
MILAN_OPTS="--all-blocks --milan-clk-freq 50e6 --timing-opt"
do_build()  { echo "[deploy] build  (Vivado P&R -> .bit)"; "$HERE/milan_soc.py" $MILAN_OPTS --build --uart-baudrate "$BAUD"; }
do_load()   { echo "[deploy] load   (JTAG, openFPGALoader -c ft232)"; "$HERE/milan_soc.py" $MILAN_OPTS --load --uart-baudrate "$BAUD"; }
do_console(){ echo "[deploy] console $CONSOLE @ $BAUD  (picocom; exit: Ctrl-a Ctrl-x)"; exec picocom -b "$BAUD" "$CONSOLE"; }

case "$STEP" in
    build)   do_build ;;
    load)    do_load ;;
    console) do_console ;;
    all)     do_build; do_load; do_console ;;
    *) echo "usage: $0 [all|build|load|console]"; exit 2 ;;
esac
